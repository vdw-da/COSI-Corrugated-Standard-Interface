import { readFileSync, readdirSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const repositoryRoot = fileURLToPath(new URL("../", import.meta.url));
const draft = "https://json-schema.org/draft/2020-12/schema";

function readJson(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch (error) {
    throw new Error(`${file}: ${error.message}`);
  }
}

function checkReferences(value, ids, file) {
  if (!value || typeof value !== "object") return;
  for (const [key, item] of Object.entries(value)) {
    if ((key === "$ref" || key === "$dynamicRef") && typeof item === "string") {
      const target = item.split("#")[0];
      if (target && !ids.has(target)) {
        throw new Error(`${file}: unresolved ${key} ${item}; use a declared schema $id, not a relative filename`);
      }
    } else {
      checkReferences(item, ids, file);
    }
  }
}

function loadSchemas(root) {
  const schemaDir = join(root, "schemas");
  const files = readdirSync(schemaDir).filter((file) => file.endsWith(".schema.json")).sort();
  if (!files.length) throw new Error("No schemas found in schemas/");
  const byFile = new Map();
  const ids = new Set();
  const ajv = new Ajv2020({ allErrors: true, strict: false });
  addFormats(ajv);

  for (const file of files) {
    const schema = readJson(join(schemaDir, file));
    if (!schema || typeof schema !== "object" || Array.isArray(schema) ||
        schema.$schema !== draft || typeof schema.$id !== "string" || !schema.$id.startsWith("cosi:")) {
      throw new Error(`${file}: expected a draft 2020-12 schema with a cosi: $id`);
    }
    if (ids.has(schema.$id)) throw new Error(`${file}: duplicate $id ${schema.$id}`);
    if (!ajv.validateSchema(schema)) {
      throw new Error(`${file}: invalid schema: ${ajv.errorsText()}`);
    }
    ids.add(schema.$id);
    byFile.set(file, schema);
  }

  // Validate the published schemas as-is. Never rewrite a broken reference.
  for (const [file, schema] of byFile) {
    checkReferences(schema, ids, file);
    ajv.addSchema(schema);
  }
  for (const [file, schema] of byFile) {
    try {
      ajv.getSchema(schema.$id); // Compile every schema, including ones unused by examples.
    } catch (error) {
      throw new Error(`${file}: ${error.message}`);
    }
  }
  const envelope = byFile.get("envelope.schema.json");
  if (!envelope) throw new Error("Missing schemas/envelope.schema.json");
  return { ajv, byFile, envelope };
}

/** Validate the full example set, or explicit JSON files. Return a process exit code. */
export function validateRepository({ root = repositoryRoot, files = [], log = console.log } = {}) {
  try {
    const { ajv, byFile, envelope } = loadSchemas(root);
    const exampleDir = join(root, "examples");
    const selected = files.length ? files.map((file) => resolve(file)) :
      readdirSync(exampleDir, { recursive: true, withFileTypes: true })
        .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
        .map((entry) => join(entry.parentPath, entry.name)).sort();
    if (!selected.length) throw new Error("No example JSON files found in examples/");

    let failed = 0;
    const validateEnvelope = ajv.getSchema(envelope.$id);
    for (const file of selected) {
      const label = relative(root, file).split("\\").join("/");
      try {
        const message = readJson(file);
        let valid = true;
        if (!validateEnvelope(message)) {
          valid = false;
          log(`FAIL  ${label} — envelope: ${ajv.errorsText(validateEnvelope.errors, { separator: "; " })}`);
        }
        const payloadSchema = byFile.get(`${message?.assetClass}.schema.json`);
        if (!payloadSchema) {
          valid = false;
          log(`FAIL  ${label} — no payload schema for assetClass ${JSON.stringify(message?.assetClass)}`);
        } else {
          const validatePayload = ajv.getSchema(payloadSchema.$id);
          if (!validatePayload(message?.payload)) {
            valid = false;
            log(`FAIL  ${label} — payload: ${ajv.errorsText(validatePayload.errors, { separator: "; " })}`);
          }
        }
        if (valid) log(`OK    ${label} (${message.assetClass})`);
        else failed++;
      } catch (error) {
        failed++;
        log(`FAIL  ${label} — ${error.message}`);
      }
    }
    log(`${failed ? "FAIL" : "PASS"}  ${byFile.size} schemas compiled; ${selected.length - failed}/${selected.length} examples valid (envelope + payload).`);
    return failed ? 1 : 0;
  } catch (error) {
    log(`FAIL  ${error.message}`);
    return 1;
  }
}

export function main(args = process.argv.slice(2)) {
  if (args.includes("--help") || args.includes("-h")) {
    console.log("Usage: npm run validate [-- path/to/example.json ...]\nWithout paths, validates every JSON file under examples/. Paths are relative to the working directory.");
    return 0;
  }
  if (args.some((arg) => arg.startsWith("-"))) {
    console.error("Unknown option. Use --help for usage.");
    return 1;
  }
  return validateRepository({ files: args });
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  process.exitCode = main();
}
