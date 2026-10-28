# ADR-000003 — Add dedicated `InfeedSettings` sub-object and extract infeed info

- **Status:** Accepted
- **Ratified by:** Focus group, 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Date:** 2026-06-18
- **Decided by:** Breakout session, 2026-06-18
- **Source:** [2026-06-18 breakout session notes](2026-06-18-notes.md)
- **Asset class:** `setup-converting`

## Context

Prior on machineSetting we had skipfeed directly. A concern was raised if we should also have multi-feed. The underling need seems to relate to ratio's broadly.
This was moved to a dedicated infeed section so the `numberIn` can be defined explicitly. Also along moved (`inputWidth`, `inputLength`) from the  `machineSettings`.

## Decision

Create a new `InfeedSettings` definition in `$defs` and reference it from `machineSettings.infeedSettings`:

- **Move** `inputWidth` and `inputLength` from `machineSettings` into `InfeedSettings`.
- **Add** `active` (boolean), `feedType` (open enum — e.g., `"vacuum"`, `"gripper"`), and `numberIn` (sheets per cycle).
- **Remove** `skipFeed` from `machineSettings` — feed behaviour is now expressed within the infeed object.

### Resulting `InfeedSettings` shape

```json
"InfeedSettings": {
  "type": "object",
  "required": ["active", "feedType", "inputWidth", "inputLength", "numberIn"],
  "properties": {
    "active":      { "type": "boolean" },
    "feedType":    { "type": ["string", "null"] },
    "inputWidth":  { "$ref": "#/$defs/QuantityMM" },
    "inputLength": { "$ref": "#/$defs/QuantityMM" },
    "numberIn":    { "type": "number", "minimum": 0 }
  },
  "additionalProperties": false
}
```

Referenced from `machineSettings`:

```json
"infeedSettings": { "$ref": "#/$defs/InfeedSettings" }
```

## Consequences

- **Updated files:** the schema and examples implement this structure. The focus group confirmed acceptance on 2026-09-24.

## Further questions

1. **Should infeed move to `periphery`?** — the infeed could be modelled as a periphery device (`"deviceType": "infeed"`). However every machine has it and this retains the original location of the moved fields.
