# Option B — Extended `orders` Array with Type Flag

## Idea in one line

Keep a single `orders` array for all order-like outputs. Add an `orderType` field and relax `required` — fields that don't apply to side orders become optional or nullable.

## Schema changes

### New `orderType` field on every order

Required for deviations in scheme and logic.

This also mitigates the readability/distinguishing the side order and waste cases from regular production orders.

```jsonc
"orderType": {
  "type": "string",
  "enum": ["production", "waste-run", "side-order"],
  "default": "production",
  "description": "'production' = standard corrugator order (default). 'waste-run' = trim strip too wide for the trim system. 'side-order' = productive order cut from the side strip."
}
```

### l2rSequenceNumber 

As the side order or waste strip is part of the orders list, the sequence and location can be determined by the regular l2rSequenceNumber field in line with other orders. Alternatively left or right allocation could be used.

### Relaxed `required` list

The current `required` list has an extensive field list. For side orders, many of these are meaningless. Two sub-options:

**B1 — Shrink `required` globally:**

```jsonc
"required": ["orderType", "sheetWidth", "sheetLength"]
```

All other fields become optional. Production orders are *expected* to have them (documented), but not *enforced* by the schema.

**B2 — Conditional required via `if`/`then`:**

```jsonc
"if": { "properties": { "orderType": { "const": "production" } } },
"then": {
  "required": ["orderRef", "partRef", "articleRef", "customerName", "processingMachine",
               "destinationLine", "sheetWidth", "sheetLength", "cuts", "numberOfOuts",
               "cutoffAllocation", "preprint", "scoringProfiles", "scoringPositions",
               "stackHeight", "stackCount", "lastRun", "dischargeDirection",
               "intermediateLayer", "palletType"]
},
"else": {
  "required": ["l2rSequenceNumber", "sheetWidth", "sheetLength", "cutoffAllocation"]
}
```

This preserves strict validation for production orders while allowing lean side orders. Note that while this is supported by several tools and part of the schema version referred, there are still some tools not supporting it.

## How the payload looks

```jsonc
{
  "setupSettings": { /* ... */ },
  "boardGradeSettings": { /* ... */ },
  "orders": [
    {
      "orderType": "production",
      "orderRef": "ORD-2026-4711",
      "partRef": "PART-001",
      "articleRef": "ART-0201-BC",
      "customerName": "Acme Packaging GmbH",
      "processingMachine": "FFG-LINE-02",
      "destinationLine": 2,
      "l2rSequenceNumber": 1,
      "sheetWidth":  { "value": 1480, "uom": "mm" },
      "sheetLength": { "value": 1200, "uom": "mm" },
      "cuts": { "uom": "cuts", "target": 5200 },
      "numberOfOuts": 2,
      "cutoffAllocation": 0,
      "preprint": { /* full preprint block */ },
      "scoringProfiles": [ /* ... */ ],
      "scoringPositions": [ /* 24 positions */ ],
      "stackHeight": { "value": 80, "uom": "pcs" },
      "stackCount": { "value": 65, "uom": "stacks" },
      "lastRun": false,
      "dischargeDirection": "OS",
      "intermediateLayer": false,
      "palletType": "Euro"
    },
    {
      "orderType": "waste-run",
      "l2rSequenceNumber": 0,
      "sheetWidth":  { "value": 120, "uom": "mm" },
      "sheetLength": { "value": 1200, "uom": "mm" },
      "cutoffAllocation": 0
    }
  ],
  "periphery": [ /* ... */ ]
}
```

## Pros

- **No merging required** — Consistent format even for "dummy orders", 1 array results in a consistent full layout.
- **Consistency in format** — A shared def leads to less duplication or risk of deviation over time.
- **Abstracting implementation** — Using generic orders format, it could allow more flexibility; in case MES **can** provide and machine **can** parse, this would possibly be more future proof (standard over implementation).
- **Clarity** — Less explicit than the side order schema, the enum/flag still allows it to be very readable.

## references

See JSON fragment: [`fragments/02-extended-orders-with-flag.json`](fragments/02-extended-orders-with-flag.json).
