# Option B — Schema-bound dimension

## Idea in one line

The *dimension* of each measurement field lives in the JSON Schema, not the payload. Validation rejects a uom that doesn't belong to the field's dimension. Payload size unchanged.

## How it works

Define a shared `$defs` block (in a new `schemas/_dimensions.schema.json` or inline) that lists, for each dimension, the set of legal uom values — metric and imperial both.

```jsonc
"$defs": {
  "Length":       { "type": "string", "enum": ["mm", "cm", "m", "km", "in", "ft", "yd"] },
  "Area":         { "type": "string", "enum": ["mm²", "cm²", "m²", "in²", "ft²"] },
  "Mass":         { "type": "string", "enum": ["g", "kg", "t", "oz", "lb"] },
  "Speed_Length": { "type": "string", "enum": ["m/min", "m/s", "ft/min", "fpm"] },
  "Speed_Count":  { "type": "string", "enum": ["pcs/h", "pcs/min", "pcs/s"] },
  "Temperature":  { "type": "string", "enum": ["°C", "°F", "K"] },
  "Energy":       { "type": "string", "enum": ["Wh", "kWh", "MJ", "BTU"] },
  "Volume":       { "type": "string", "enum": ["m3", "L", "ft3", "gal_us"] },
  "Pressure":     { "type": "string", "enum": ["kN", "bar", "psi", "kPa"] },
  "Ratio":        { "type": "string", "enum": ["%", "%RH", "1"] },
  "Count":        { "type": "string", "enum": ["pcs", "stacks", "rolls"] }
}
```

Each measurement field then references the dimension instead of pinning a single uom:

```jsonc
// Before (current performance.schema.json L45-49):
"water":       { "allOf": [{"$ref":"#/$defs/Quantity"}],
                 "properties": { "uom": { "const": "m3" } } }

// After:
"water":       { "allOf": [{"$ref":"#/$defs/Quantity"}],
                 "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Volume" } } }
```

## What the payload looks like

Identical to today. No new fields, no `dim` per value.

```json
"water": { "value": 1.24, "uom": "m3" }   // metric — valid
"water": { "value": 327,  "uom": "gal_us" } // imperial — also valid because Volume allows it
"water": { "value": 1.24, "uom": "kg"  }   // INVALID — Mass is not Volume
```

## Pros

- **Zero payload bloat.** Dimension is metadata, not data.
- **Validatable today.** Any standard JSON Schema validator gives us the dimension check for free.
- **Imperial unlocked.** Each dimension's `enum` lists both metric and imperial members; producers send what they have.
- **Decision is documented in code.** Each field's dimension is visible in the schema — readable, reviewable, diffable.

## Cons

- **Schema gets larger.** ~20–30 lines for the dimension definitions, plus a touch more verbosity at each field site (one `$ref` instead of a `const`).
- **Doesn't tell the consumer whether the *whole message* is metric or imperial.** A downstream that wants a fast "are we in feet or metres" check has to look at every uom.
- **Dimensions must be named once and used consistently.** Bikeshedding risk: `Speed_Length` vs `Velocity` vs `LinearSpeed`.

## Variant: cross-field constraint

You could add a JSON Schema `if/then` that ties a field's uom to the envelope `unitSystem` (when present): "if envelope says metric, uom must be in {`m`, `m/min`, ...}". This works but adds significant schema complexity. Probably skip unless we need it.

## When this is the right answer

Whenever we want *validation* of dimension correctness. This is the option that actually answers the team's "seconds is not a width" request. It does not address the "metric vs imperial default" framing — that's [Option A](01-option-A-envelope-unit-system.md).

**A + B together** is the natural pairing — A gives the envelope-level summary, B gives the per-field validation. The dimension catalog used by B is essentially [Option E](05-option-E-unit-catalog.md) factored out into its own file.

See JSON fragment: [`fragments/02-schema-bound-dimension-snippet.json`](fragments/02-schema-bound-dimension-snippet.json).
