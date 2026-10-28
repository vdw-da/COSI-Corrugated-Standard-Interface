# ADR-000011 — `l2rSequenceNumber` is required on every corrugator order

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Focus group, 2026-09-07
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-02 (finding #16)
- **Asset class:** `setup-corrugator`

## Context

The glossary stated that `l2rSequenceNumber` is carried "on each order". The schema required it
only in the non-production `else` branch, so a production order could omit it and still validate.
One of the two was wrong; the group decided which.

## Decision

In `setup-corrugator`, `l2rSequenceNumber` is **required on every non-empty order object** in the
`orders` array — production and non-production alike. The schema is corrected; the glossary was
already right and is unchanged.

## Consequences

- Every order object in `orders` must carry `l2rSequenceNumber`; a production order that omits it
  does not validate.
- The left-to-right position of every order is always available to a consumer, which is what the
  field exists for.
