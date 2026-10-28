# Why queue management should be deferred from v1.0

**Current disposition — 14 October 2026:** Historical rationale: the October 1 meeting accepted queue exclusion from v1.0 (ADR-000007). Normative artifacts were archived October 14. The requested decision and October 1 release assumptions below are historical, not current deadlines.

**Prepared:** 2026-09-29 for the October 1 scope decision.
**Status:** argument supporting the maintainer's proposal; deferral is not yet approved.
**Decision:** the exclusion is recorded in [ADR-000007](../../adr/ADR-000007-queue-schema-retained-state-baseline.md).

## Suggested explanation to the working group

> Queue management determines which work a machine will produce, in which order, and with which
> settings. Our current schemas describe a queue, but the standard does not yet provide a complete
> interoperable contract for changing it while production, operator actions and communication
> failures occur. We have identified cases where incomplete rules could repeat completed work,
> apply the wrong setup revision, undo an operator change, or leave the MES unable to determine
> whether a request succeeded.
>
> Several principles are already defined in our working notes, but the protocol, recovery limits,
> machine-specific restrictions and interoperability evidence remain unfinished. Those gaps need
> a coordinated design and validation effort. We cannot responsibly complete that before this
> release. I propose removing the queue capability from v1.0 and preserving delete, update,
> reordering, queue state and recovery as one v1.1 work item. This gives implementers an explicit
> scope boundary and lets us standardize the capability once its behaviour can be relied upon.

## What is already settled, and what that does not complete

The September definition review recorded maintainer-confirmed principles: one setup identity per execution, machine authority over the actual queue, protection
against conflicting stale edits, all-or-nothing acceptance, stable outcomes for repeated requests,
and recovery across restart/power loss. It also says working-group ratification and alignment of
schemas and documentation remained outstanding. The retained setup meanings are now recorded
in [ADR-000006](../../adr/ADR-000006-response-setup-schema-approach.md); queue-specific
principles remain deferred design inputs.

The September 24 confirmations recorded so far approve `setupRef` naming and the existing
setup-response approach. They do not approve a complete queue protocol. In particular, having
`OK` / `NOK` and correlation fields does not define every queue operation or its recovery procedure.

The current [queue schema](../../ideas/queue-management/queue.schema.json) carries setup references and optional
sequence numbers. The [corrugator setup schema](../../schemas/setup-corrugator.schema.json) has a
`previousSetupId`; the converting setup has no equivalent explicit setup execution identifier.
The [guide](../../docs/technical-guide.md) describes full-setup resubmission and retained queue
state. These pieces do not yet form one complete state-transition contract.

## Gaps that must be closed before standardizing the capability

The examples below are failure scenarios permitted by missing or incomplete rules, not claims
that every vendor implementation fails. Some rows concern the proposed synchronization design;
others concern the existing v1.0 draft. A vendor could add safeguards, but interoperable peers
need agreed obligations and observable outcomes.

| Area | What remains to be specified or aligned | Why it matters in production |
|---|---|---|
| **1. Supported operations and placement** | Complete semantics for add, update, delete and reorder; insertion with absent/unknown predecessors; array order versus `sequenceNumber`; effect of resending an existing setup. The earlier add/report-only wording was itself incomplete. | Two vendors may append, move, replace or duplicate work in response to the same valid message. |
| **2. Execution, request and setup identities** | Wire representation, scope and reuse rules for execution identity versus a request identity and a setup-body version; consistent corrugator/converting mapping; interruption, resumption and partial completion. | Repeating a request, revising pending work and scheduling another run must not be confused. |
| **3. Lifecycle and commitment restrictions** | Represent waiting, committed and producing work; distinguish completion from cancellation; define which moves, deletions and setting changes remain allowed at each stage, including overlapping machine stages. | A change valid when prepared may be invalid once tooling preparation or production starts. |
| **4. Conflict detection and atomic application** | Define the edit precondition and version-change rules; make conflict checks, commitment checks, body selection, application and durable result recording consistent with concurrent PLC and HMI changes. The all-or-nothing principle needs an implementable contract. | The machine could approve a reorder against an old state and then apply it after an operator or production transition has made it invalid. |
| **5. Local operator control and remote authority** | Remote enable/disable, local override and handover; representation of locally added, changed and deleted work; how a planner adopts a permitted local change. | Automatic reconciliation can repeatedly undo an operator's change or restore work the operator deliberately removed. |
| **6. Delayed and superseded requests** | Policy for older requests after a newer one was rejected; distinction between highest observed, processed and accepted revisions; controlled initialization/recovery instead of an undefined unconditional-update path. | A delayed old plan can restore an intention that the MES has already replaced or cancelled. |
| **7. Duplicate handling and lost outcomes** | Stable request identity and content checks, result availability period, outstanding-request limits, retry behaviour and outcome recovery after history expires. A last-result field cannot necessarily answer earlier requests. | After a lost response, the MES may repeat a change or wait forever without knowing whether it already took effect. |
| **8. Durable acceptance and uncertain execution** | Implement and validate the confirmed restart guarantee; define persisted/recoverable evidence and the procedure for declaring and clearing recovery-required state. Physical completion may be uncertain even when a message was processed. | Replaying an old accepted plan after memory loss can reintroduce work already produced. |
| **9. Exact setup versions and dependency acquisition** | Bind accepted executions to exact setup-body versions; obtain missing versions; define wait/reject/retry behaviour when plan and body arrive separately; retain the accepted version when a replacement is rejected. | A plan for setup A version 1 can resolve to version 2, or a restarted controller can lose the version it actually accepted. |
| **10. Cancellation and cleanup** | Distinguish removing scheduled work, completing execution and retiring its setup body; wait for confirmed removal and preserve all versions still needed by active work or recovery. | A rejected cancellation could still be followed by deletion of the setup data required by the running machine. |
| **11. Snapshot freshness and startup readiness** | Current-session and queue-version meaning, publication triggers, bootstrap completeness, recovery state and readiness after reconnection. Existing timestamps alone do not establish those semantics. | The MES may treat an old snapshot as current or submit work before the machine has recovered its state. |
| **12. Planner failover and restored state** | Authorized planner handover, protection against obsolete writers, revision reset and identity rules, controller replacement, broker loss and backup restore. | A replacement MES starting its counter at 1 may never be accepted; an old planner or restored record may reintroduce stale intent. |
| **13. Capacity and bounded storage** | Maximum queue/body sizes, retained versions and result history; behaviour when storage is full; abandoned uploads and cleanup responsibilities. | An implementation may lose accepted work or become unavailable when its unspecified storage assumptions are exceeded. |
| **14. Progress during continuous production** | Which changes invalidate an edit, bounded retries and outstanding work, backoff, and conditions under which an edit can eventually succeed. Report-only changes should not accidentally cause endless conflicts. | Every edit can be rejected while the machine keeps advancing, even though each rejection individually follows the rules. |
| **15. Portable rejection and recovery actions** | Unambiguous protocol outcomes for stale state, missing dependencies, immutable work, capacity and unsupported operations; field-path grammar and recovery actions. Preserve vendor error details without requiring peers to infer protocol state from free text. | The MES cannot know whether to retry, refresh state, fetch a setup body or request operator intervention. |
| **16. Capability differences across machines** | A minimum interoperable profile and representation of permitted operations or field changes. A single mutable flag may not describe “quantity change allowed, tooling change forbidden.” | Implementations can both claim support but disagree about ordinary operations on committed or active work. |
| **17. Versioning and migration** | Contract identification, routing, coexistence with existing integrations, retained-state conversion, ownership during cutover and rollback. A v1.1 label does not itself make changed semantics compatible. | Old setup consumers and a new queue reconciler could both control the same queue, or interpret the same identifier differently. |
| **18. Implementation and interoperability evidence** | An executable behavioural model, representative machine validation and independent peer tests for races, duplicate delivery, delayed data, crash points, missing history and resource limits. | JSON-valid messages can still cause incompatible state transitions. Passing schema examples establishes message shape, not reliable queue behaviour. |

## Five concrete examples for the meeting

1. **Production and reordering race:** the MES reads A–B–C and asks for B–A–C. The controller
   commits A to preparation before applying the request. The contract must determine whether
   the whole request is rejected and what state/result the MES receives.
2. **Accepted change, lost response:** the machine applies a change, the response is lost, and
   the controller restarts. Retrying must recover the earlier outcome without applying the
   change again. The required history, retention limit and uncertain-state recovery are unfinished.
3. **Completed work reappears:** a retained plan contains A–B. A completes; protocol history is
   then lost. Reading A–B again must not authorize producing A a second time.
4. **Wrong setup revision:** a plan refers to A, but a newer A body arrives before the plan is
   processed. A plain setup reference cannot establish which settings that plan intended.
5. **Cancellation rejected, recovery data removed:** the MES requests deletion of active A,
   then removes its setup body. If the machine rejects the deletion, it still needs A's body.
   Cleanup must follow accepted lifecycle transitions, not merely the sender's request.

## Why small fixes do not complete the contract

**Adding a delete message** resolves a message shape. It still needs authority, commitment,
acknowledgement, retries, cancellation semantics and recovery. Deletion therefore belongs with
the other queue operations in one design.

**Adding a revision counter** helps detect stale edits. It does not define execution identity,
durable outcomes, exact setup versions, failover or what to do after history loss. It can also
prevent progress if every status publication invalidates an edit.

**Retaining a queue or desired plan** makes a stored snapshot available. The draft still has to
define how completed work, rejected plans, missing setup versions and uncertain machine state
are distinguished during recovery. Commands and declarative synchronization both need those rules;
the later review did not establish either as inherently sufficient.

**Keeping only add-and-report** is a possible smaller future profile, but it still needs placement,
identity, acceptance, duplicate protection, commitment and restart behaviour. The earlier review
explicitly found that the proposed limited wording left these obligations unresolved. It cannot
be presented as an already completed fallback for this release.

**Leaving the details to each vendor** may produce working private integrations. Without a shared
minimum contract it does not provide the interoperability that a common queue standard promises.

## What to preserve for v1.1, and what must change for v1.0

Preserve the working definitions, `setupRef` naming, alternatives and review findings. Develop
the operation and recovery contract together, compare conditional requests with declarative
reconciliation fairly, and test independent implementations against the same production scenarios.
Assign an owner and agree a validation plan before committing to a release date.

For v1.0, an accepted deferral requires coordinated removal of the queue capability from the
normative schema set, envelope, examples, topic mapping and capability claims. The remaining
setup data/response boundary must be explicit, including the disposition of predecessor and
queue-update semantics. Removing `queue.schema.json` alone would leave contradictory promises.
The [proposal inventory](README.md#alignment-required-if-the-group-accepts) lists these changes.

Delivery and recovery for remaining message types follow ADR-000010. This proposal
reduces the queue-specific work; it does not establish overall release readiness.

## Evidence and limits

This paper combines current repository evidence with the September 11 queue review and the later
maintainer-confirmed definitions. The local review covered the scenarios and design concerns
summarized here, using nine finite countermodels and three positive controls.
Those models expose missing obligations under stated assumptions; they are not an exhaustive
verification, broker simulation or test of a deployed PLC implementation.

The definitions recorded after the review settle several principles, so this paper does not
repeat the historical claim that authority, membership, atomicity or restart protection have
never been considered. The remaining release argument is that those principles still need a
ratified, aligned and validated interoperable protocol.

