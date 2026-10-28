# Queue management — proposed v1.1 work

**Current status:** excluded from v1.0 by the working group, 2026-10-01. v1.1 remains a
candidate, not a commitment. Maintainer naming clarification, 2026-10-14: `queue` and
`queue-delete`. Payloads/protocols remain deferred. The proposal text below is historical;
its references to pending deferral are superseded by the October 1 decision.
**Decision:** [ADR-000007](../../adr/ADR-000007-queue-schema-retained-state-baseline.md) and
[ADR-000008](../../adr/ADR-000008-delete-request.md). The deferred queue reference name is
`setupRef`, confirmed by the focus group on September 24.

## Proposed decision

Exclude queue management from COSI v1.0 and carry it as one coordinated v1.1 idea:

- Queue state exchange, including the `queue` asset class and retained queue snapshot.
- Adding setups to a managed production queue, updating queued setups, deleting/cancelling
  them, and changing their sequence.
- Queue authority, commitment restrictions, conflict handling, acceptance, duplicate handling,
  persistence, reconnect and restart recovery needed to make those operations interoperable.

This is a proposal to defer the complete queue capability, including add-and-report. It does
not approve a particular v1.1 protocol or promise delivery in v1.1. The existing setup data
models and setup-response approach are not automatically withdrawn; their v1.0 documentation
must describe the remaining scope without promising queue operations.

**S2 clarification, 2026-09-29:** machine-side setup parameter changes, including operator edits,
are published back to ERP/MES through the existing setup message types. This return path remains
in scope independently of the proposed queue deferral; see the [ADR-000005](../../adr/ADR-000005-remove-actuals-from-setup.md).

## Why defer

**Meeting arguments:** [deferral rationale, gap inventory and production examples](deferral-rationale.md).
This distinguishes maintainer-confirmed principles from the protocol details and validation
still outstanding, and provides wording for the October 1 discussion.

The September queue analysis found substantial unresolved behaviour around competing MES/HMI
changes, production consuming the queue, delayed and duplicate requests, pinned setup versions,
atomic acceptance and recovery after restart. A sound implementation and independent
interoperability validation do not fit the remaining time before the October 1 release.

The first draft recommended declarative synchronization. The subsequent review explicitly
rejected approving that design as written: retained state and revision counters alone did not
establish the claimed safety. A conditional full-queue replacement request remains a candidate
alongside a corrected declarative design. Neither has been selected.

Even a limited add-and-report profile needs defined identity, placement, acceptance, duplicate
handling and recovery. The review therefore offered a complete limited contract **or deferral**.
The maintainer now proposes deferral, replacing the earlier add-and-report suggestion.

The retained setup execution and response meanings are recorded in
[ADR-000006](../../adr/ADR-000006-response-setup-schema-approach.md). The deferred queue
principles remain design inputs, not an approved queue protocol.

## Alignment required if the group accepts

| Surface | Required change before publication |
|---|---|
| `queue` schema and example | Preserve as v1.1 design material; exclude from the v1.0 normative schema/example set |
| Envelope | Remove the v1.0 `queue` asset-class choice and payload reference |
| README, guide, glossary, properties and topic table | Remove queue capability claims and queue-specific retained-state requirements; state the deferral explicitly |
| Setup schemas, examples and guide | Review `previousSetupId` and every placement/update statement; remove queue-management semantics from the v1.0 contract and define the remaining setup exchange boundary |
| Setup response | Preserve the accepted response approach (ADR-000006); reconcile its meaning with the remaining setup scope without implying queue admission or guaranteed production |
| ADR-000007 / ADR-000008 | Record deferral and the resulting v1.0 scope; keep their design history |
| `ideas/queue-delete/` | Keep the alternatives as background under this combined v1.1 work item |
| Topic and schema scope | Align topic coverage and record `queue` as scoped out; decide the remaining topic and schema questions |
| Validation and release records | Validate the remaining v1.0 examples and update the changelog, schema inventory and counts |

**Implementation checkpoint, 2026-10-14:** the former normative
[queue schema](queue.schema.json) and [example](queue.json) are archived here unchanged as
historical design material. They are not valid v1.0 messages. The normative envelope excludes
queue and the corrugator setup no longer carries queue-placement `previousSetupId`.
The former field was an optional string/null identifying the predecessor, with null described
as appending to the list; that queue-placement meaning is deferred, not a setup requirement.
The table above records the earlier planned migration; it does not reopen settled scope.
Last Will follows ADR-000022; delivery and recovery follow ADR-000010. Queue deferral
does not change those decisions or permit retaining setup instructions and responses.

## Work required for a future version

Develop one reviewed contract covering execution identity, setup-body versions, machine authority,
local operator changes, commitment, atomic edits, durable results, bounded history and recovery.
Compare conditional requests with persistent reconciliation against the same requirements.
Validate competing edits, duplicates, delayed messages, production progress, lost results,
restart/power loss, missing history, storage limits and protocol migration with independent peers.
The release label alone does not establish compatibility with existing implementations.
