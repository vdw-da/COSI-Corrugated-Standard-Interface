import assert from "node:assert/strict";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { validateRepository } from "../scripts/validate-examples.mjs";

const root = fileURLToPath(new URL("../", import.meta.url));
const cli = join(root, "scripts/validate-examples.mjs");

function fixture(t) {
  const dir = mkdtempSync(join(tmpdir(), "cosi-validation-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  for (const name of ["schemas", "examples"]) cpSync(join(root, name), join(dir, name), { recursive: true });
  return dir;
}

function changeJson(dir, path, change) {
  const file = join(dir, path);
  const data = JSON.parse(readFileSync(file, "utf8"));
  change(data);
  writeFileSync(file, JSON.stringify(data));
}

function fails(dir, pattern) {
  const output = [];
  assert.equal(validateRepository({ root: dir, log: (line) => output.push(line) }), 1);
  assert.match(output.join("\n"), pattern);
}

test("CLI validates all examples from outside the repository", (t) => {
  const cwd = mkdtempSync(join(tmpdir(), "cosi-cwd-"));
  t.after(() => rmSync(cwd, { recursive: true, force: true }));
  const run = spawnSync(process.execPath, [cli], { cwd, encoding: "utf8" });
  assert.equal(run.status, 0, run.stdout + run.stderr);
  assert.match(run.stdout, /PASS .*schemas compiled/);
});

test("CLI supports a selected file and fails for a missing file", () => {
  const selected = spawnSync(process.execPath, [cli, "examples/lastwill/lastwill.json"], { cwd: root, encoding: "utf8" });
  assert.equal(selected.status, 0, selected.stdout + selected.stderr);
  assert.match(selected.stdout, /1\/1 examples valid/);
  const missing = spawnSync(process.execPath, [cli, "examples/nonexistent.json"], { cwd: root, encoding: "utf8" });
  assert.equal(missing.status, 1);
  assert.match(missing.stdout, /FAIL.*nonexistent/);
});

test("a broken cross-schema reference fails without rewriting it", (t) => {
  const dir = fixture(t);
  changeJson(dir, "schemas/envelope.schema.json", (schema) => {
    schema.oneOf[0].properties.payload.$ref = "performance.schema.json";
  });
  const file = join(dir, "schemas/envelope.schema.json");
  const before = readFileSync(file, "utf8");
  fails(dir, /unresolved \$ref performance\.schema\.json/);
  assert.equal(readFileSync(file, "utf8"), before);
});

test("unused schemas are compiled and broken local fragments fail", (t) => {
  const dir = fixture(t);
  writeFileSync(join(dir, "schemas/unused.schema.json"), JSON.stringify({
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: "cosi:unused:1.0", $ref: "#/$defs/missing",
  }));
  fails(dir, /unused\.schema\.json/);
});

test("duplicate schema IDs fail", (t) => {
  const dir = fixture(t);
  cpSync(join(dir, "schemas/quality.schema.json"), join(dir, "schemas/duplicate.schema.json"));
  fails(dir, /duplicate \$id/);
});

test("invalid schema syntax fails", (t) => {
  const dir = fixture(t);
  changeJson(dir, "schemas/quality.schema.json", (schema) => { schema.type = "not-a-type"; });
  fails(dir, /quality\.schema\.json: invalid schema/);
});

test("no examples is a failure, not an empty successful run", (t) => {
  const dir = fixture(t);
  rmSync(join(dir, "examples"), { recursive: true });
  mkdirSync(join(dir, "examples"));
  fails(dir, /No example JSON files/);
});

test("a malformed example does not prevent checking the remaining files", (t) => {
  const dir = fixture(t);
  writeFileSync(join(dir, "examples/lastwill/lastwill.json"), "{");
  const output = [];
  assert.equal(validateRepository({ root: dir, log: (line) => output.push(line) }), 1);
  assert.match(output.join("\n"), /FAIL.*lastwill\/lastwill\.json/);
  assert.match(output.join("\n"), /OK.*setup\/setup-corrugator\.json/);
});

for (const [name, path, mutate, error] of [
  ["missing schemaId", "examples/performance/performance.json", (m) => { delete m.schemaId; }, /envelope:.*schemaId/],
  ["mismatched schemaId", "examples/performance/performance.json", (m) => { m.schemaId = "cosi:quality-payload:1.0"; }, /envelope:/],
  ["invalid payload", "examples/performance/performance.json", (m) => { delete m.payload.speed; }, /payload:.*speed/],
  ["nonempty Will", "examples/lastwill/lastwill.json", (m) => { m.payload.extra = true; }, /payload:.*additional properties/],
  ["non-null Will timestamp", "examples/lastwill/lastwill.json", (m) => { m.timestamp = "2026-10-14T12:00:00Z"; }, /envelope:/],
  ["missing response correlation", "examples/setup-response/setup-response.json", (m) => { delete m.correlationID; }, /envelope:.*correlationID/],
]) {
  test(`rejects ${name}`, (t) => {
    const dir = fixture(t);
    changeJson(dir, path, mutate);
    fails(dir, error);
  });
}
