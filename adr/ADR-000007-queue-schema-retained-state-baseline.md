# ADR-000007 - Queue schema retained-state baseline

**Implementation checkpoint — 14 October 2026:** Queue schema/example are archived under ideas/queue-management; the normative envelope, inventories and setup flow exclude queue. The queue-placement previousSetupId field is removed from corrugator setup. Earlier pending-alignment statements describe the prior recording stage. The aligned package was subsequently approved on 16 October 2026; see the [decision register](decision-register.md).

- **Status:** Deferred beyond v1.0 (v1.1 candidate)
- **Date:** 2026-07-14
- **Decided by:** Working group, 2026-07-14
- **Source:** [2026-07-14 meeting notes](2026-07-14-notes.md)
- **Asset class:** `queue`

## Scope disposition — 1 October 2026

The working group excluded **queue management from v1.0**, while retaining setup exchange.
Source: [October 1 meeting notes, A2](2026-10-01-notes.md#a2-queue-management).
A future v1.1 is a candidate, not a commitment to the historical design below.
No queue/delete mechanism is selected for v1.0. The retained setup/response contract is
defined by [ADR-000006](ADR-000006-response-setup-schema-approach.md).

The earlier context and proposals below are preserved as design history and do not authorize
queue capabilities in the v1.0 release.

## Context

The 2026-07-14 discussion aligned on the following:

A queue schema is needed to have a view on the current production status, this can serve several purposes including feedback on success, sequence changes, progress updates, etc...

The meeting agreed on a separation of concerns:

- setup messages (`setup-corrugator`, `setup-converting`) carry modifications
- queue data should represent the latest queue state as a retained MQTT message
- queue ownership and publication are on the corrugator/converting machine side

A lightweight baseline is created to start feedback.

## Historical decision / proposal

Introduce `assetClass = queue` with payload schema `queue.schema.json` using:

- `queueList` (array) as the full queue snapshot
- per item required `setupRef` (commonly known as `setupId`; naming approved by the focus group 2026-09-24, see [meeting record](2026-09-24-notes.md))
- optional `sequenceNumber` for explicit queue order when available

## Future design questions

- Right now the `QueueItem` is a bit of a stub:
   - should we add the sequenceNumber and if so optional or mandatory
   - What other fields would we expect on this `QueueItem` knowing the goal is not to contain detailed data or serve feedback purposes.

## Consequences

- Consumers can read current queue state without replaying setup events.
- Queue ordering can be communicated incrementally while sequence semantics are still being finalized.
- Future ADRs can extend queue items with richer metadata without breaking the initial contract.
