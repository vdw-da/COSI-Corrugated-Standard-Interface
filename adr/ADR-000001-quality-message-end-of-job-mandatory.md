# ADR-000001 — Quality message at end of job mandatory, in-process optional

- **Status:** Accepted
- **Date:** 2026-06-09
- **Decided by:** Working group, 2026-06-09
- **Scope confirmation:** Maintainer, 2026-09-29; atomic-check interpretation confirmed 2026-09-30
- **Source:** [2026-06-09 team meeting notes](2026-06-09-notes.md)
- **Asset class:** `quality`

## Context

Two quality reporting use cases surfaced in the working group:

- A **statistics summary at job end** — the complete quality record for a finished job.
- **Every quality check immediately** — event-driven reporting where a detected deviation requires immediate action.

These were the original reporting use cases. The later maintainer clarification below
distinguishes message cadence from report construction by the receiving application.

A related idea was raised: a setup message could define which **triggers** and intervals apply to which job and machine — e.g., every flute change, every *n* pallets, every roll change, every 1000 sheets, every 1500 in-feeds, after downtime longer than 10 min. Fosber noted this can produce a very large number of messages, and the group judged a full trigger definition likely too much for v1 scope.

## Decision

A quality message **at the end of each job is mandatory**. Additional quality messages **may optionally** be sent at any time during the job for use cases that require immediate action.

## Current interpretation — atomic checks, reconciled 14 October 2026

The maintainer clarified on **30 September** that each array item is an atomic quality check
and report construction belongs to the receiving application. This dated maintainer
confirmation is recorded here and in [ADR-000002](ADR-000002-quality-check-structure-checks-array.md).
This editorial reconciliation applies that existing clarification; it is not a new decision.
It supersedes the earlier complete-summary interpretation in this ADR's context and consequences.
The mandatory job-end message and optional additional messages remain unchanged. A message
need not be a complete or cumulative job report, and cadence defines no report-completion protocol.

## Consequences

- Every completed job requires a quality message at job end. The receiving application builds
  reports from the atomic checks; the message does not promise a complete job summary.
- In-process quality messages are optional and event-driven; both cadences use the existing `cos` message type and the same payload structure.
- Defining the trigger/interval vocabulary that would fire in-process messages is deferred — out of scope for v1, tracked as a [future idea](../ideas/quality-triggers/README.md).

## Documentation

Reflected in the Technical Guide, *Business Case: Quality* — § 6.3 Key Concepts, "Reporting Cadence".
