# Option D — UN/CEFACT common codes

## Idea in one line

Drop ISO 80000 symbols (`m/min`, `Wh`, `°C`) from the payload and use UN/CEFACT Recommendation 20 common codes instead (`KMH` adjusted as `2X` for m/min, `WHR`, `CEL`).

## What the payload looks like

```json
"speed":  { "value": 182,  "uom": "2X"  }   // 2X = metre per minute
"water":  { "value": 1.24, "uom": "MTQ" }   // MTQ = m³
"steam":  { "value": 340,  "uom": "KGM" }   // KGM = kilogram
"temp":   { "value": 21.5, "uom": "CEL" }   // CEL = °C
"speedI": { "value": 600,  "uom": "FTM" }   // FTM = foot per minute
```

| Symbol today | UN/CEFACT code | Note |
|---|---|---|
| `m` | `MTR` | metre |
| `mm` | `MMT` | millimetre |
| `m²` | `MTK` | square metre |
| `m3` | `MTQ` | cubic metre |
| `kg` | `KGM` | kilogram |
| `t` | `TNE` | metric tonne |
| `g/m²` | `GM` | gram per square metre |
| `m/min` | `2X` | metre per minute |
| `pcs/h` | `H87/HUR` | piece per hour (composite, no single code) |
| `°C` | `CEL` | degree Celsius |
| `°F` | `FAH` | degree Fahrenheit |
| `Wh` | `WHR` | watt-hour |
| `kWh` | `KWH` | kilowatt-hour |
| `%` | `P1` | percent |
| `%RH` | (no code) | relative humidity has no Rec 20 code |
| `dpi` | (no code) | print resolution has no Rec 20 code |
| `dE2000` | (no code) | colour distance has no Rec 20 code |
| `ft` | `FOT` | foot |
| `in` | `INH` | inch |
| `lb` | `LBR` | pound |

## Pros

- **Direct OPC UA round-trip.** If an upstream OPC UA server emits `EUInformation { unitId: 5066068 }` (= `MTR`), the JSON message carries the same code verbatim. No conversion table.
- **Imperial coverage is built in.** Imperial codes are first-class — no second-class citizen treatment.
- **Stable, externally governed.** UNECE maintains the list. We don't.

## Cons

- **Unreadable.** A human looking at the JSON sees `2X` instead of `m/min`. The current standard advertises self-describing JSON as a virtue; this erodes that.
- **Composite units have no codes.** `pcs/h`, `kg/m²`, `dE2000`, `dpi`, `%RH` — the things specific to our domain — either don't exist in Rec 20 or are kludged. We'd need a parallel "extended" code list, and now we have two systems.
- **Hurts onboarding.** Implementers look up codes for every field; symbol form is universally readable.

## Variant: ISO symbols primary, UN/CEFACT as schema annotation

Keep `m/min` etc. in the payload, but annotate each dimension/uom in the schema with its Rec 20 code as a non-validating `x-uncefact` keyword:

```jsonc
"$defs": {
  "Length": {
    "type": "string",
    "enum": ["mm", "cm", "m", "km", "in", "ft"],
    "x-uncefact": { "mm": "MMT", "cm": "CMT", "m": "MTR", "km": "KMT", "in": "INH", "ft": "FOT" }
  }
}
```

A consumer wanting OPC UA interop has a lookup table; everyone else ignores it. Best of both — but it does mean we ship the mapping with the standard.

## Verdict

UN/CEFACT codes in the payload: **no** — readability loss outweighs the gain. UN/CEFACT codes as **schema-side annotation**: **yes**, low cost, helpful for OPC UA round-trip. This variant folds naturally into [Option E](05-option-E-unit-catalog.md).

See JSON fragments: [`fragments/04-uncefact-payload-style.json`](fragments/04-uncefact-payload-style.json), [`fragments/04b-uncefact-as-annotation.json`](fragments/04b-uncefact-as-annotation.json).
