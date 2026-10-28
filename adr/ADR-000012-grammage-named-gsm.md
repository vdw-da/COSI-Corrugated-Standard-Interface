# ADR-000012 — Paper grammage is named `gsm` on both machine types

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Focus group, 2026-09-07
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-03 (finding #43)
- **Asset class:** `setup-corrugator`, `setup-converting`

## Context

One physical property carried two names: `weight` on the corrugator and `grammage` on converting.
A consumer reading both machine types had to know that the two fields mean the same thing. Neither
name was kept.

## Decision

The field is named **`gsm`** on both machine types, with `uom` **`g/m²`**. The imperial counterpart
is not part of v1.0 (see [ADR-000013](ADR-000013-metric-only-for-v1.md)).

## Consequences

- `weight` and `grammage` no longer exist on either machine type.
- `gsm` is an abbreviation, and `docs/naming-conventions.md` § 3 admits abbreviations only from an
  explicit permitted list. The row was added when the rename was applied and approved by the
  maintainer on 2026-09-29.
- The parked imperial idea must carry **`lb/MSF`**, not `MSF`: `MSF` is thousand square feet, an
  *area* unit, and recording it as the unit of a basis weight is dimensionally wrong. Approved
  by the maintainer on 2026-09-29.
