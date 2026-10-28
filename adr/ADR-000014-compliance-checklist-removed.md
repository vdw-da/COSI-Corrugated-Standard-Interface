# ADR-000014 — The compliance checklist is removed from the standard for v1.0

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Focus group, 2026-09-07 (owner: André Seifert)
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-05 (finding #30)
- **Asset class:** — (standard-wide)

## Context

Appendix B announced a compliance checklist that was never written, and at the same time mandated
that every implementation "shall be validated against this checklist before deployment". That is a
binding requirement pointing at a document that does not exist — unsatisfiable by construction.

## Decision

Remove the compliance checklist from the standard for v1.0, **including its binding mandate**.
Appendix B and the "shall be validated" sentence are deleted from the technical guide.

## Consequences

- No implementation can be held to an unpublished checklist.
- The guide's § 8 heading and Appendix A are unchanged.
- If the group later wants a conformance programme, it is a new decision with a real document
  behind it — not a revival of this text.
