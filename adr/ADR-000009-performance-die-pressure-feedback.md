# ADR-000009 — Die pressure feedback in the performance payload

- **Status:** Accepted (ratified by the focus group 2026-09-24)
- **Date:** 2026-08-19
- **Decided by:** Maintainer, consolidating PR #5 (proposal by Daniel Malolepszy)
- **Ratified by:** Focus group, 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Source:** PR #5 `proposalDieCutPressureFeedback` (proposal by Daniel Malolepszy); no covering meeting note existed
- **Asset class:** `performance`

## Context

ADR-000005 removed actuals/feedback from **setup** messages. Die-cut pressure is a value that changes
during production (tool wear compensation), so feedback belongs in the **performance** message.
PR #5 added an optional `diePressure` element to the performance payload for flat-bed die cutters.

As merged, the structure nested three levels deep
(`payload.diePressure.diePressure.diePressure.value`) — an artifact of the proposal, with no ADR,
no documentation, and no example.

## Decision

- The performance payload carries an **optional** top-level `diePressure` element for flat-bed die
  cutters: a single quantity `{ "value": <number>, "uom": "kN" }` (uom fixed to `kN`, matching
  `dieCutter.diePressure` in the converting setup schema).
- The redundant nesting from PR #5 is flattened.

## Consequences

- `schemas/performance.schema.json`: `DiePressureItem` = Quantity with `uom` const `kN`;
  payload property `diePressure` references it directly.
- Technical guide § 3.5 lists the optional die-pressure reading.
- The shipped performance example (a corrugator) deliberately does **not** carry `diePressure` —
  it applies to flat-bed die cutters only.

## Open question

Whether multiple die-pressure sensors per machine need an array form — extendable later without
breaking the single-value contract only if done before v1.0 freeze; otherwise a v1.1 topic.
