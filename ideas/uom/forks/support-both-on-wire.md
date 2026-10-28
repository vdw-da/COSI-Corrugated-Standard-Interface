# Fork 2 — Support metric AND imperial on the wire

> Premise: the COSI standard supports both unit systems natively. A US/UK source can emit imperial uoms directly; a European source emits metric. The envelope declares which world the message lives in.

## What changes

### Envelope (`schemas/envelope.schema.json`)

```jsonc
"unitSystem": {
  "type": "string",
  "enum": ["metric", "imperial"],
  "default": "metric",
  "description": "Unit system for all measurements in payload. Omit to default to 'metric'. A single message uses one system end-to-end (no mixed messages)."
}
```

Per Decision 1, mixed messages are not allowed — so we deliberately do **not** add `"mixed"` to the enum.

We deliberately do **not** cross-validate (no `if/then` that ties the envelope flag to the per-field uoms). Reason: schema complexity grows fast, and the per-field uom enum already excludes wrong-system uoms from the wrong dimension. A producer that puts `m/min` in an `unitSystem: imperial` message is technically inconsistent but the message still validates and the consumer can still read it. Trade-off accepted.

### New file: `schemas/_dimensions.schema.json` (metric + imperial)

```jsonc
{
  "$id": "cosi:dimensions:1.0",
  "$defs": {
    "Length":          { "type": "string", "enum": ["mm","cm","m","km","in","ft","yd"],
                         "x-uncefact": { "mm":"MMT","cm":"CMT","m":"MTR","km":"KMT","in":"INH","ft":"FOT","yd":"YRD" },
                         "x-toSI":     { "mm":0.001,"cm":0.01,"m":1,"km":1000,"in":0.0254,"ft":0.3048,"yd":0.9144 } },
    "Area":            { "type": "string", "enum": ["mm²","cm²","m²","in²","ft²"],
                         "x-uncefact": { "mm²":"MMK","cm²":"CMK","m²":"MTK","in²":"INK","ft²":"FTK" } },
    "Volume":          { "type": "string", "enum": ["mL","L","m3","ft3","gal_us"],
                         "x-uncefact": { "mL":"MLT","L":"LTR","m3":"MTQ","ft3":"FTQ","gal_us":"GLL" } },
    "Mass":            { "type": "string", "enum": ["g","kg","t","oz","lb"],
                         "x-uncefact": { "g":"GRM","kg":"KGM","t":"TNE","oz":"ONZ","lb":"LBR" } },
    "LengthPerTime":   { "type": "string", "enum": ["m/s","m/min","ft/min","fpm"],
                         "x-uncefact": { "m/s":"MTS","m/min":"2X","ft/min":"FR","fpm":"FR" } },
    "CountPerTime":    { "type": "string", "enum": ["pcs/s","pcs/min","pcs/h"] },
    "Temperature":     { "type": "string", "enum": ["°C","K","°F"],
                         "x-uncefact": { "°C":"CEL","K":"KEL","°F":"FAH" } },
    "Energy":          { "type": "string", "enum": ["Wh","kWh","MJ","BTU"],
                         "x-uncefact": { "Wh":"WHR","kWh":"KWH","MJ":"MJ","BTU":"BTU" } },
    "Pressure":        { "type": "string", "enum": ["Pa","kPa","bar","psi"],
                         "x-uncefact": { "Pa":"PAL","kPa":"KPA","bar":"BAR","psi":"PS" } },
    "Force":           { "type": "string", "enum": ["N","kN","lbf"],
                         "x-uncefact": { "N":"NEW","kN":"KNT","lbf":"C62" } },
    "Humidity":        { "type": "string", "enum": ["%RH"] },
    "Grammage":        { "type": "string", "enum": ["g/m²","oz/ft²"],
                         "x-uncefact": { "g/m²":"GM","oz/ft²":"37" } },
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

`Count` → `Quantity` per Decision 5. `x-toSI` conversion factors are shown on `Length` as illustration; including them on every dimension is a separate decision (see "Open" below).

### Asset-class schemas

Same diff as the metric-only fork — `const: "..."` → `$ref` to the dimension. The dimensions' enums now include imperial members. No per-asset-class change required.

For `speed` (Decision 6 — polymorphic by assetClass):

```jsonc
// performance.schema.json (corrugator context):
"speed": { ..., "uom": { "$ref": "_dimensions.schema.json#/$defs/LengthPerTime" } }

// setup-converting.schema.json:
"speed": { ..., "uom": { "$ref": "_dimensions.schema.json#/$defs/CountPerTime"  } }
```

### `docs/units.md` (new)

Full version with metric + imperial columns, Rec 20 codes, and (optionally) SI conversion factors. Drafted in [`../draft-units-doc.md`](../draft-units-doc.md).

### `docs/naming-conventions.md` §6

Shrinks to pointer (same as metric-only fork).

### Other docs (TG, MP)

- TG: paragraph explaining that both unit systems are valid; one per message; envelope flag is the declared system; per-field `uom` is the authoritative value.
- MP: `unitSystem` row added to envelope table with the two-value enum.

### Examples

Existing metric examples remain unchanged. **Add one imperial example** (e.g., `examples/performance/performance-imperial.json`) showing a US corrugator emitting `ft/min`, `BTU`, `lb`, `°F` with `"unitSystem": "imperial"` on the envelope. The schemas validate both.

## Pros of this fork

- **No data loss at the edge.** Source units flow through to the consumer; conversion (if needed) happens at the consumer.
- **Matches the team's expressed intent** ("imperial/metric in the long term").
- **Backward compatible.** Existing metric messages remain valid because `unitSystem` defaults to `metric`.
- **The translation/transformation layer is freed** — it doesn't *have* to convert; it only must if the consumer specifically wants SI.

## Cons of this fork

- **Larger dimension catalog.** Each dimension carries 5–7 uoms instead of 3–4.
- **Consumers must be conversion-aware** for any analytics that aggregate cross-region data (a fleet view comparing m/min and ft/min must convert).
- **`%RH`, `dpi`, `dE2000` etc. don't have imperial counterparts** — they sit in single-value enums whether the fork is metric-only or both. Not a real con; just a reminder these don't gain anything by this fork.
- **Per-field uom enums get wider, weakening the "right uom for this field" intuition.** A producer could emit `°F` on a temperature field in an `unitSystem: "metric"` message and the schema wouldn't reject it (we chose no cross-validation). Mitigation: producers should set `unitSystem` correctly; the contract is documentation + reviews, not schema.

## What this fork is *for*

The team that says: **let imperial flow on the wire, let translation services convert when needed, don't lose source-unit fidelity**.

See JSON fragment: [`../fragments/01-envelope-with-unitsystem.json`](../fragments/01-envelope-with-unitsystem.json) — both `metricExample` and `imperialExample` are valid in this fork.

## Open within this fork

- **Conversion factors (`x-toSI`) — include or skip?**
  - **Include:** consumers and analytics tooling get a single source of truth. Cost: maintenance, rounding/precision policy.
  - **Skip:** keep catalog minimal; consumers Google the conversion. Lower maintenance.
  - I'd lean **include** because the cost is one column in `units.md` per row, and analytics consumers will appreciate it.

- **Should `unitSystem` be required or optional?**
  - **Required:** producer must declare. Stronger contract, slightly more verbose.
  - **Optional with `metric` default:** matches current behaviour for existing producers, minimal disruption.
  - I'd lean **optional**.
