# ADR-000008 — Delete request for queued setups

- **Status:** Deferred beyond v1.0 (v1.1 candidate)
- **Date:** 2026-08-19
- **Decided by:** Maintainer draft from the 2026-07-20 decision note; v1.0 scope exclusion by the working group, 2026-10-01
- **Source:** [2026-07-20 meeting notes](2026-07-20-notes.md), [2026-07-14 meeting notes](2026-07-14-notes.md) (CRUD chapter)
- **Asset class:** `queue-delete` (deferred; naming confirmed 2026-10-14); `queue` remains the queue-state name

## Scope disposition — 1 October 2026

The working group excluded **queue management from v1.0**, while retaining setup exchange.
Source: [October 1 meeting notes, A2](2026-10-01-notes.md#a2-queue-management).
A future v1.1 is a candidate, not a commitment to the historical design below.
No queue/delete mechanism is selected for v1.0. The retained setup/response contract is
defined by [ADR-000006](ADR-000006-response-setup-schema-approach.md).

The earlier context and proposals below are preserved as design history and do not authorize
queue capabilities in the v1.0 release.

## Naming clarification — 14 October 2026

**Confirmed by maintainer:** “if there is still anything on the queue, we have queue and
queue-delete”. The names are `queue` for queue state and `queue-delete` for the deferred deletion
message. This supersedes `request-delete` as its candidate message name. The earlier inline
`deleterequest` discriminator and alternative shapes below remain historical design evidence,
not a second accepted v1.0 operation. Naming does not restore queue management to v1.0 or approve
any deferred payload, deletion semantics, acknowledgment, retention or recovery mechanism.
Keep this ADR's filename stable; use the current name in deferred explanatory material.

## Context

CRUD handling for setups was left partially open (2026-07-14): *update* is covered by re-sending the
full setup; *delete* remained uncovered. The 2026-07-20 meeting decided:

> queue.json add "deleterequest" as status, array of setupRefID or jobRefID to be deleted from
> Machine Controller

The note is terse; two readings are possible, both drafted in
[`ideas/queue-delete/`](../ideas/queue-delete/README.md):

- **Option A — extend the queue message.** The queue payload gains a payload-level discriminator
  (`"deleterequest"`) plus a `deleteList` array. Faithful to the note's wording ("queue.json").
  **Conflict:** ADR-000007 defines the queue message as machine-owned **retained** state. A delete
  *request* flows in the opposite direction (MES → machine) and must not be retained — a retained
  deleterequest would replay against the machine on every reconnect.
- **Option B — separate request message.** New asset class `request-delete` (non-retained, `cos`),
  payload = `deleteList` array of `setupRef` / `jobRef` items. The machine confirms by publishing
  the updated retained queue snapshot (and may respond via `response-setup`-style acknowledgement).
  Preserves ADR-000007 ownership/retain semantics and mirrors the established setup → queue flow.

## Historical decision / proposal

**Historical proposal, 2026-09-29:** defer delete together with the complete queue-management
capability to the v1.1 ideas. No Option A/B selection was made for v1.0.
See the [combined proposal](../ideas/queue-management/README.md). This proposal was superseded by the October 1 scope disposition above.

**Earlier draft recommendation (retained as design history): Option B** — it keeps the queue message
a pure retained snapshot (ADR-000007) and keeps commands and state separated (2026-07-14
"separation of concerns" agreement).

## Future design questions

1. Future design: choose a delete mechanism as part of the complete queue protocol; scope was excluded from v1.0 on October 1.
2. Naming: the note says `setupRefID`/`jobRefID`; naming-conventions § 4 prescribes `setupRef` /
   `jobRef` for cross-system references. The queue-item name is now settled as `setupRef`
   (focus group 2026-09-24); the delete-request shape remains pending.
3. Should a delete request be acknowledged (analogous to `response-setup`), and with which asset class?
4. Delete semantics: reject when the setup is already running? Idempotent when unknown?

## Consequences (once accepted)

- Option B: new `request-delete.schema.json`, envelope `assetClass` enum + oneOf extension,
  example, README/docs/glossary updates.
- Option A: queue schema gains the discriminator + `deleteList`; retain-semantics guidance must be
  rewritten in ADR-000007/technical guide.
