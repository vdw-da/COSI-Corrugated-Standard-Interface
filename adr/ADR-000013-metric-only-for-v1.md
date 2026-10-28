# ADR-000013 — v1.0 is metric only; imperial is deferred to v1.1

- **Status:** Accepted
- **Date:** 2026-09-09
- **Updated:** 2026-10-01
- **Decided by:** Focus group, 2026-09-07; working group, 2026-10-01 (reported by the maintainer)
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-04 (finding #21a)
- **Asset class:** — (standard-wide)

## Context

Metric-only was a tendency from the 2026-07-15 session, never written down. Left implicit, it read
as an omission — a reader could not tell whether imperial units were forbidden or simply not yet
covered.

## Decision

v1.0 is **metric only**, using the units and tokens defined for each field. The existing
field-specific tokens, including `pcs`, `dpi`, `station` and `FEFCO`, remain as fixed in
[ADR-000016](ADR-000016-schema-corrections-to-documented-intent.md). Imperial sources convert before
publishing. The rule is written explicitly in `docs/naming-conventions.md` § 6 *Unit system* and in
the technical guide, rather than left to inference. **Imperial UOMs are not part of v1.0 and
are postponed to v1.1.** The deferred work is recorded in `ideas/uom/`.

## October 1 outcome

The working group decided on **2026-10-01**, as reported by the maintainer, to exclude
imperial UOMs from v1.0 and postpone them to v1.1. This confirms the metric-only v1.0 scope
and specifies v1.1 as the deferred version.

## Editorial reconciliation — 14 October 2026

The former blanket sentence “All units are SI / ISO 80000 symbols” was too broad for the
field-specific tokens already fixed in ADR-000016 and present in the schemas. The decision
wording now preserves both recorded choices: metric measurement scope and the existing
field-specific tokens. This corrects the generalization; it does not add units, change a
schema constraint or admit general imperial-unit support. The October 1 deferral is unchanged.

## Consequences

- A producer converts measurements to the field-defined units before publishing; the existing
  fixed tokens above remain valid. General imperial-unit alternatives are deferred to v1.1.
- `ideas/uom/` holds the deferred work and must carry `lb/MSF` as the imperial grammage unit
  (see [ADR-000012](ADR-000012-grammage-named-gsm.md); notation approved by the maintainer on 2026-09-29).
- **Working-group decision, 2026-10-01:** the proposed limited imperial extension is excluded from
  v1.0; imperial UOM support is deferred to v1.1. The current metric-only schemas remain
  consistent with the v1.0 scope decision.
