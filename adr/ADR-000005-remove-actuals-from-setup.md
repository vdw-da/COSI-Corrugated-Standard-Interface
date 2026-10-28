# ADR-000005 — Remove actuals/feedback data from setup messages

- **Status:** Accepted
- **Ratified by:** Focus group, 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Date:** 2026-06-18
- **Decided by:** Breakout session, 2026-06-18
- **Source:** [2026-06-18 breakout session notes](2026-06-18-notes.md)
- **Asset class:** `setup-corrugator`, `setup-converting`

## Context

Setup messages currently mix two concerns:

1. **Intent** — what the machine *should* do: target speed, scheduled length, order layout, scoring positions, etc.
2. **Feedback** — what the machine *actually did*: actual speed, average speed, actual cuts, actual running length, waste totals, start/end timestamps.

While the intent of the message should be **setup** and not feedback.

## Decision

**Production actuals should not be part of setup messages.** These include actual production
quantities, waste, elapsed times and measured production performance.

**Clarification, 2026-09-29:** changes to setup parameters on the machine, including operator
edits, must be published back to ERP/MES through the corresponding setup message. Those values
are changed setup settings and belong to the existing S2 use case. The earlier broad word
"feedback" does not prohibit that return path. This is the maintainer’s clarification of 2026-09-29.

## Consequences

 - Updated schema setup-corrugator and setup-converting, as well as examples.
