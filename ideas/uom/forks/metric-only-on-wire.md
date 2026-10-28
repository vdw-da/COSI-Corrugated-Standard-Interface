# Fork 1 — Metric-only on the wire

> Premise: the COSI standard guarantees metric units in the payload. Imperial sources are responsible for converting to SI *before* emitting a VDW message — typically in the translation/transformation layer that already sits between producer and consumer.

## What changes

### Envelope (`schemas/envelope.schema.json`)

**Either** add an optional `unitSystem` field pinned to `metric`, **or** add nothing at all.

```jsonc
"unitSystem": {
  "type": "string",
  "const": "metric",
  "default": "metric",
  "description": "All measurements in payload use metric/SI units. Producers MAY include this field to assert the contract explicitly."
}
```

I lean toward including it as `const: "metric"`. It costs ~20 bytes when present and gives a forward-compatibility hook: if the team later changes its mind and wants imperial on the wire, the field already exists and only its `enum` widens. No envelope schema break.

### New file: `schemas/_dimensions.schema.json` (metric only)

```jsonc
{
  "$id": "cosi:dimensions:1.0",
  "$defs": {
    "Length":          { "type": "string", "enum": ["mm","cm","m","km"],
                         "x-uncefact": { "mm":"MMT","cm":"CMT","m":"MTR","km":"KMT" } },
    "Area":            { "type": "string", "enum": ["mm²","cm²","m²"],
                         "x-uncefact": { "mm²":"MMK","cm²":"CMK","m²":"MTK" } },
    "Volume":          { "type": "string", "enum": ["mL","L","m3"],
                         "x-uncefact": { "mL":"MLT","L":"LTR","m3":"MTQ" } },
    "Mass":            { "type": "string", "enum": ["g","kg","t"],
                         "x-uncefact": { "g":"GRM","kg":"KGM","t":"TNE" } },
    "LengthPerTime":   { "type": "string", "enum": ["m/s","m/min"],
                         "x-uncefact": { "m/s":"MTS","m/min":"2X" } },
    "CountPerTime":    { "type": "string", "enum": ["pcs/s","pcs/min","pcs/h"] },
    "Temperature":     { "type": "string", "enum": ["°C","K"],
                         "x-uncefact": { "°C":"CEL","K":"KEL" } },
    "Energy":          { "type": "string", "enum": ["Wh","kWh","MJ"],
                         "x-uncefact": { "Wh":"WHR","kWh":"KWH","MJ":"MJ" } },
    "Pressure":        { "type": "string", "enum": ["Pa","kPa","bar"],
                         "x-uncefact": { "Pa":"PAL","kPa":"KPA","bar":"BAR" } },
    "Force":           { "type": "string", "enum": ["N","kN"],
                         "x-uncefact": { "N":"NEW","kN":"KNT" } },
    "Humidity":        { "type": "string", "enum": ["%RH"] },
    "Grammage":        { "type": "string", "enum": ["g/m²"],
                         "x-uncefact": { "g/m²":"GM" } },
    "ColourDistance":  { "type": "string", "enum": ["dE2000","dE94","dE76"] },
    "PrintResolution": { "type": "string", "enum": ["dpi"] },
    "Viscosity":       { "type": "string", "enum": ["s","cP","mPa·s"] },
    "Duration":        { "type": "string", "enum": ["s","min","h"],
                         "x-uncefact": { "s":"SEC","min":"MIN","h":"HUR" } },
    "Ratio":           { "type": "string", "enum": ["1","%"],
                         "x-uncefact": { "%":"P1" } },
    "Quantity":        { "type": "string", "enum": ["pcs","stacks","rolls","sheets","pallets"] }
  }
}
```

Note: I renamed `Count` → `Quantity` per Decision 5 (stacks/rolls/pcs are quantities).

### Asset-class schemas

Replace existing `"const": "..."` pins with `$ref` to the dimension catalog. Example diff for `performance.schema.json`:

```diff
- "water":       { "allOf": [{ "$ref": "#/$defs/Quantity" }], "properties": { "uom": { "const": "m3"     } } },
- "electricity": { "allOf": [{ "$ref": "#/$defs/Quantity" }], "properties": { "uom": { "const": "Wh"     } } },
- "steam":       { "allOf": [{ "$ref": "#/$defs/Quantity" }], "properties": { "uom": { "const": "kg"     } } },
- "air":         { "allOf": [{ "$ref": "#/$defs/Quantity" }], "properties": { "uom": { "const": "m3"     } } },
- "stacks":      { "allOf": [{ "$ref": "#/$defs/Quantity" }], "properties": { "uom": { "const": "stacks" } } }
+ "water":       { "allOf": [{ "$ref": "#/$defs/Measurement" }], "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Volume"   } } },
+ "electricity": { "allOf": [{ "$ref": "#/$defs/Measurement" }], "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Energy"   } } },
+ "steam":       { "allOf": [{ "$ref": "#/$defs/Measurement" }], "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Mass"     } } },
+ "air":         { "allOf": [{ "$ref": "#/$defs/Measurement" }], "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Volume"   } } },
+ "stacks":      { "allOf": [{ "$ref": "#/$defs/Measurement" }], "properties": { "uom": { "$ref": "_dimensions.schema.json#/$defs/Quantity" } } }
```

(I'd also rename the inline `$defs/Quantity` shape — which is "an object with value+uom" — to `Measurement`, freeing the name `Quantity` for the dimension. Cosmetic but reduces confusion.)

### `docs/units.md` (new)

The metric-only fork's units doc is shorter: one column per row (no imperial). Drafted in [`../draft-units-doc.md`](../draft-units-doc.md) — see metric-only variant at the bottom.

### `docs/naming-conventions.md` §6

Shrinks to a one-paragraph pointer: "*Unit of measure values are defined in `docs/units.md`. The field is always named `uom`; the legal values are bound by dimension in `_dimensions.schema.json`.*"

### Other docs (TG, MP)

- TG: add one paragraph in §6 (Quality) or a new short section: "*The standard is metric on the wire. Sources using imperial units must convert to SI in the producing connector.*"
- MP: add `unitSystem` to the envelope table.

### Examples

Unchanged. Already metric. Optionally add `"unitSystem": "metric"` to one or two as illustration.

## Pros of this fork

- **Simplest possible standard.** No imperial enums. No conversion ambiguity.
- **Strongest validation.** A field's uom enum is small and unambiguous.
- **Aligns with how most JSON-based industry standards behave** (ISO-leaning).
- **Forward-compatible.** The optional `unitSystem: "metric"` const can later widen to `enum: ["metric","imperial"]` without breaking existing messages.

## Cons of this fork

- **Pushes conversion to producers.** A US/UK source must convert before emitting. The "translation/transformation service" you described is a natural home for this — but it's still work that has to happen.
- **Loses the source-unit information.** A consumer can no longer tell whether the original sensor was in °F or °C — only the converted °C is visible. (Mitigation: nothing in the standard prevents a producer from including an out-of-band source-unit annotation on a field, if needed later.)
- **Less aligned with team's expressed wish** ("we want to consider imperial/metric in the long term"). This fork interprets that as "imperial-aware at the edge, not on the wire."

## What this fork is *for*

The team that says: **the standard should be uniform on the wire**, with conversion handled by integration code. Closest to how OPC UA companion specifications behave (SI-first).

See JSON fragment: [`../fragments/01-envelope-with-unitsystem.json`](../fragments/01-envelope-with-unitsystem.json) (the `metricExample` block; ignore `imperialExample`).
