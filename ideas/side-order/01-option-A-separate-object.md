# Option A — Separate `sideOrders` Array

## Idea in one line

Add a new optional `sideOrders` array at the payload root (alongside an unchanged `orders`). Each side order is a **lean object** that describes only what a side strip actually needs — no scoring, no preprint, no pallet config e.g..

## Schema addition

A new `SideOrder` definition and a new top-level `sideOrders` property:

```jsonc
// $defs addition
"SideOrder": {
  "description": "A simplified order representing a side strip.",
  "type": "object",
  "required": ["side", "orderType", "sheetWidth", "sheetLength", "cutoffAllocation"],
  "properties": {
    "side":        { "type": "string", "enum": ["left", "right"], "description": "Side of the corrugator web this strip occupies." },
    "orderType":   { "type": "string", "enum": ["waste-run", "side-order"], "description": "Distinguishes between waste and a true side order." },
    "sheetWidth":  { "$ref": "#/$defs/QuantityMM", "description": "Strip width in mm (measured from web edge)." },
    "sheetLength": { "$ref": "#/$defs/QuantityMM", "description": "Cut-off length in mm." },
    "cutoffAllocation": { "type": "integer", "minimum": 0, "description": "Cut-off sheet allocation." }
    }
  },
  "additionalProperties": false
```

Top-level property:

```jsonc
"sideOrders": {
  "type": "array",
  "maxItems": 2,
  "items": { "$ref": "#/$defs/SideOrder" },
  "description": "Optional side orders. Omit or leave empty when all trim is evacuated normally."
}
```

## open questions

 - Do we need the array to allow both sides, or will 1 be enough? (i.e. will it ever occur to have 2?)
 - Do we prefer left/right side order definition or is this to be taken into account the L2Rsequence as well?

## How the payload looks

```jsonc
{
  "setupSettings": { /* ... */ },
  "boardGradeSettings": { /* ... */ },
  "orders": [
    { /* full production order 1 */ },
    { /* full production order 2 */ }
  ],
  "sideOrders": [
    {
      "side": "left",
      "orderType": "waste-run",
      "sheetWidth":  { "value": 120, "uom": "mm" },
      "sheetLength": { "value": 1200, "uom": "mm" },
      "cutoffAllocation": 0
    }
  ],
  "periphery": [ /* ... */ ]
}
```

## Pros

- **Strict validation** — production orders keep their full required-field set untouched. Side orders have their own lean contract.
- **No fake data** — MES doesn't need to come up with specific fields.
- **Semantic clarity** — `sideOrders` tells the consumer immediately "this is a different kind of thing." No flag-checking logic needed.
- **Flexibility** — Easier to deviate the 2 defs without impact on the other.
- **Compatibility** — Seems to be more in line with current implementations.

## references

See JSON fragment: [`fragments/01-separate-side-order.json`](fragments/01-separate-side-order.json).
