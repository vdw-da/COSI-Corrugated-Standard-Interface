# ADR-000002 — Quality check structure: header + `checks` array

**Implementation checkpoint — 14 October 2026:** Atomic-check/cadence wording and the qualitative NOK example are aligned; the numeric exception enum and existing payload structure are preserved. Earlier pending-alignment statements describe the prior recording stage. The aligned package was subsequently approved on 16 October 2026; see the [decision register](decision-register.md).

- **Status:** Accepted; qualitative-result wording amended by maintainer 2026-10-13
- **Date:** 2026-06-09
- **Decided by:** Working group, 2026-06-09
- **Source:** [2026-06-09 team meeting notes](2026-06-09-notes.md)
- **Asset class:** `quality`

## Context

The original quality check shape carried a single `actualValue` and one `result` per check. The working group agreed this cannot express how many pieces fell into each outcome (good vs. out-of-tolerance), whether out-of-tolerance pieces were ejected, or which tolerance bound was crossed.

## Decision

Each quality check becomes a **header** plus a **`checks` array**:

- **Header** — describes the check and its tolerance: `errorType`, `lowerLimit`, `upperLimit`, and `uom` (the unit of the limits).
- **`checks` array** — atomic quality checks with counted outcomes (September 30 clarification below):
  - `quantity` — number of pieces covered by this check.
  - `uom` — unit of the count (`pcs`).
  - `result` — `OK` / `NOK`.
  - `ejected` — boolean; whether the pieces covered by a `NOK` check were ejected. Present on `NOK` checks.
  - `exception` — numeric tolerance-deviation reason on `NOK` checks: `lower-violation` or `upper-violation`. Omit for non-numeric failures without a violated numeric bound (October 13 amendment below).

`OK` entries carry only `quantity`, `uom`, `result`. The old `actualValue` field is removed.

## Current interpretation — atomic checks, reconciled 14 October 2026

The maintainer's **30 September 2026** clarification defines each array item as an atomic check. Receiving applications group checks, calculate
report totals and determine report completion. This editorial reconciliation replaces the
earlier report-bucket interpretation, without changing the header/array shape or June cadence
in ADR-000001. No cumulative-report or completion protocol follows from this message.
The October 13 qualitative OK/NOK amendment below remains unchanged.

Example — a check with both tolerance bounds (the meeting notes illustrated this on `warp`; shown here on `caliper`, which has both a lower and an upper limit so both `exception` values are valid):

```json
"caliper": {
  "errorType": "Caliper", "lowerLimit": 3.8, "upperLimit": 4.2, "uom": "mm",
  "checks": [
    { "quantity": 8,    "uom": "pcs", "result": "NOK", "ejected": true,  "exception": "lower-violation" },
    { "quantity": 14,   "uom": "pcs", "result": "NOK", "ejected": false, "exception": "upper-violation" },
    { "quantity": 2400, "uom": "pcs", "result": "OK" }
  ]
}
```

## Enum values — `exception`

| Value | Meaning |
|-------|---------|
| `lower-violation` | Measured value fell below `lowerLimit`. |
| `upper-violation` | Measured value exceeded `upperLimit`. |

These are lowercase-hyphen per the enum casing rule (naming-conventions.md § 8). Documented in [`message-properties.md`](../docs/message-properties.md).

## Decisions taken applying this ADR

- **Count `uom` = `pcs`** — consistent with naming-conventions.md § 6 preferred values and the `performance` asset class (the meeting notes wrote `Sht`).
- **Non-numeric checks** (e.g. paper quality, glue applied, elephant foot) may report `OK` or `NOK`, with null tolerance limits and no invented numeric `exception`. This is the current rule under the October 13 amendment below, replacing the former single-`OK` interpretation. `actualValue` remains removed everywhere.

## Consequences

- `examples/quality/quality.json` is updated to the new shape.
- The `exception` enum values are documented in `message-properties.md` and enforced as a closed enum in `schemas/quality.schema.json`.
- `schemas/quality.schema.json` and the [Quality Check Shape](../docs/message-properties.md#quality-check-shape) reference in Message Properties (cross-referenced from Naming Conventions § 7) implement this structure; the example validates against the schema.


## Amendment — qualitative OK and NOK, 13 October 2026

**Decided by:** Maintainer, 2026-10-13. **Source:** explicit “agreed, next” to the bounded
qualitative-result clarification during v1.0 finalization; not attributed to the June meeting.

Non-numeric checks may report `OK` or `NOK`. Their tolerance limits are `null`; the existing
nullable header unit remains `null` when not applicable. When no numerical tolerance bound
was violated, omit `exception` rather than inventing a lower/upper violation. Preserve the
existing ejection information: `ejected` indicates whether the pieces reported as `NOK` were
ejected. `OK` entries retain their existing shape.

This replaces the former application clause restricting non-numeric checks to a single `OK`
bucket and narrows the generic exception description to numerical bound violations. The old
OK-only interpretation is superseded, not a competing current option. Existing numeric
`lower-violation`/`upper-violation` meanings and the closed enum remain unchanged. No new field,
enum value, reporting workflow or change to quality-message cadence is adopted.

The schema permits non-numeric `NOK` with null limits and omitted exception. Naming
Conventions, Message Properties, the guide and the qualitative-failure example implement this
meaning. Payload approval followed with the aligned package on 16 October 2026.
