# Option E — External unit catalog

## Idea in one line

Create a single document (`docs/units.md`) and a single schema file (`schemas/_dimensions.schema.json`) that together own all knowledge about dimensions, units, and metric/imperial pairs. Everything else references it.

## What it contains

### `docs/units.md` (the human-facing doc)

A table per dimension. For each dimension: SI primary, accepted metric variants, accepted imperial variants, the UN/CEFACT code for each, and (optionally) the canonical-to-SI conversion factor for downstream consumers.

```markdown
## Length — dimension `length`

| Symbol | System   | Rec 20 code | → SI (m)  |
|--------|----------|-------------|-----------|
| `mm`   | metric   | MMT         | 0.001     |
| `cm`   | metric   | CMT         | 0.01      |
| `m`    | metric ✦ | MTR         | 1         |
| `km`   | metric   | KMT         | 1000      |
| `in`   | imperial | INH         | 0.0254    |
| `ft`   | imperial | FOT         | 0.3048    |
| `yd`   | imperial | YRD         | 0.9144    |

✦ = canonical SI unit for this dimension.
```

Repeat for: `area`, `volume`, `mass`, `length_per_time` (linear speed), `count_per_time` (throughput), `temperature`, `energy`, `power`, `pressure`, `force`, `humidity`, `count` (pcs, stacks, sheets), `ratio` (%), `duration`, plus the corrugated-specific ones (`grammage`, `colour_distance`, `print_resolution`, `viscosity`).

### `schemas/_dimensions.schema.json` (the machine-facing definitions)

The same information in JSON Schema form — one `$defs` entry per dimension, with the uom enum. Schemas reference it via `$ref` (see [Option B](02-option-B-schema-bound-dimension.md)).

```jsonc
{
  "$id": "cosi:dimensions:1.0",
  "$defs": {
    "Length":            { "type": "string", "enum": ["mm","cm","m","km","in","ft","yd"] },
    "Area":              { "type": "string", "enum": ["mm²","cm²","m²","in²","ft²"] },
    "Volume":            { "type": "string", "enum": ["m3","L","ft3","gal_us"] },
    "Mass":              { "type": "string", "enum": ["g","kg","t","oz","lb"] },
    "LengthPerTime":     { "type": "string", "enum": ["m/min","m/s","ft/min"] },
    "CountPerTime":      { "type": "string", "enum": ["pcs/h","pcs/min","pcs/s"] },
    "Temperature":       { "type": "string", "enum": ["°C","°F","K"] },
    "Energy":            { "type": "string", "enum": ["Wh","kWh","MJ","BTU"] },
    "Pressure":          { "type": "string", "enum": ["bar","kPa","psi"] },
    "Humidity":          { "type": "string", "enum": ["%RH"] },
    "Grammage":          { "type": "string", "enum": ["g/m²","oz/ft²"] },
    "ColourDistance":    { "type": "string", "enum": ["dE2000","dE76"] },
    "PrintResolution":   { "type": "string", "enum": ["dpi"] },
    "Viscosity":         { "type": "string", "enum": ["s","cP","mPa·s"] },
    "Ratio":             { "type": "string", "enum": ["%","1"] },
    "Count":             { "type": "string", "enum": ["pcs","stacks","rolls","sheets"] },
    "Duration":          { "type": "string", "enum": ["s","min","h"] }
  }
}
```

Where it helps OPC UA interop, an `x-uncefact` annotation accompanies the enum without affecting validation (see [Option D variant](04-option-D-uncefact-codes.md#variant-iso-symbols-primary-uncefact-as-schema-annotation)).

## How the asset-class schemas change

```diff
- "water":  { "allOf":[{"$ref":"#/$defs/Quantity"}],
-             "properties": { "uom": { "const": "m3" } } }
+ "water":  { "allOf":[{"$ref":"#/$defs/Quantity"}],
+             "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Volume" } } }
```

A reviewer of `performance.schema.json` can now read "water is volume" at a glance and follow the link to see the legal units.

## Pros

- **One file owns unit knowledge.** Today, valid units leak across `naming-conventions.md` §6, individual schema `const`s, and `examples/`. Centralization is overdue regardless of the imperial question.
- **Payload unchanged.** Nothing new on the wire.
- **Adding imperial is a one-line edit per dimension** (`"in"` joins the `Length` enum).
- **Documentation single-sources** — `docs/units.md` and `_dimensions.schema.json` always agree because the doc table generates from the schema (or vice versa) at review time.
- **Pairs naturally with Option A** — envelope-level switch + per-field dimension binding = full coverage.

## Cons

- **One more file to maintain.** And one more relative `$ref` for schema loaders to resolve. JSON Schema validators that don't follow external refs need configuration.
- **Doesn't tell the consumer whether the whole message is metric or imperial** without scanning every uom. Solved by adding [Option A](01-option-A-envelope-unit-system.md).
- **Adds an "ownership" entry to the document-ownership rules.** `docs/units.md` becomes the canonical owner of unit lists, so NC §6 must shrink to a pointer.

## Interaction with current NC §6

Currently NC §6 ("Preferred uom values") lists symbols inline. With Option E, that table moves to `docs/units.md` (richer: now with imperial + Rec 20 code + SI conversion). NC §6 becomes a one-paragraph pointer. This is consistent with the **ownership rule** already in place — units are big enough now to deserve their own owner doc.

## When this is the right answer

Almost always, if we're doing this at all. It's the cheapest way to introduce imperial + dimension binding without bloating payloads. It's also the only way the consumer-side conversion to SI gets a single source of truth for conversion factors.

See JSON fragment: [`fragments/05-unit-catalog.json`](fragments/05-unit-catalog.json).
