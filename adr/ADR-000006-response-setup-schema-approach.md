# ADR-000006 — Setup response schema approach

- **Status:** Accepted; payload approved by André Seifert, 2026-10-16
- **Date:** 2026-07-14
- **Decided by:** Working group, 2026-07-14; focus group ratification, 2026-09-24; maintainer clarifications, 2026-09-11 and 2026-10-13–14
- **Source:** [July 14 meeting notes](2026-07-14-notes.md); [September 24 confirmed decisions](2026-09-24-notes.md); dated maintainer confirmations below
- **Asset class:** `setup-response`, replying to `setup-corrugator` or `setup-converting`

## Context

Setup requests need an application outcome distinct from MQTT transport acknowledgment.
Machines may report the first field error or multiple errors. Both machine types use the same
response structure.

## Decision

ERP/MES sends a setup instruction; the machine returns `setup-response`. The response envelope's
required `correlationID` is the original setup request's `messageID`.

- `result: OK`: the machine checked and applied the requested change in full. This does not
  guarantee that production has started or will complete successfully. An OK response has no errors.
- `result: NOK`: none of the request's changes were applied. A non-empty `errors` array contains
  one or more objects with `fieldRef`, `description` and `manufacturerCode`.

`manufacturerCode` is a manufacturer-specific non-negative integer, not a standardized error-code list.
`fieldRef` is an RFC 6901 JSON Pointer rooted at the full original setup message. For example,
`/payload/orders/0/sheetLength/value` identifies the first order's sheet-length value. Use the
JSON string form, zero-based array indices, and `~0` / `~1` escaping for `~` / `/`. Dotted paths
and URI fragments are not accepted alternatives. A syntactically valid pointer does not prove
that its location matches the reported error. See [RFC 6901](https://www.rfc-editor.org/rfc/rfc6901.html).

## Request identity and recovery

A missing response means the outcome is unknown. An unchanged retry preserves the request's
`messageID` and event timestamp. A machine that already processed it returns its original
outcome without applying the change again. Changed instructions or a request to reconsider a
rejection use a new message identity, even when they concern the same planned execution.
Reusing an identity with changed content is an error.

Acceptance survives connection loss, controller restart and power loss. Accepted work and its
request association must be preserved or recovered to prevent unintended repetition. Loss or
expiry of history must not turn an old request into a new instruction. If the relevant state
cannot be established reliably, the machine communicates that recovery is required and blocks
affected remote changes until the state has been established and communicated. Unrelated known
production need not stop.

These are observable outcome rules, not a prescribed storage design, retention period or new
recovery wire protocol. Transport conditions are recorded in
[ADR-000010](ADR-000010-bidirectional-east-west-only.md#delivery-and-reconnection).

## Setup execution identity

A setup describes one planned production execution on a machine. A corrugator execution may
produce several orders together; a converting execution concerns a particular processing
operation. Revising instructions or continuing the same execution after interruption preserves
its execution identity. Scheduling a separate execution creates a new identity, even if the
order, article and settings are unchanged.

A corrugator `setupSettings.setupId` is unique within its site and machine. A quality message's
`setupRef` references that identifier in the same site/machine context. This preserves the
existing string representation and does not redefine converting job/order/task references.
Execution identity is distinct from message identity under
[ADR-000018](ADR-000018-message-id-uuid-v5.md).

Queue operations are outside v1.0 under [ADR-000007](ADR-000007-queue-schema-retained-state-baseline.md).
Queue admission is not a setup-processing response. Machine-side changed settings return
through setup messages as specified by [ADR-000005](ADR-000005-remove-actuals-from-setup.md).
Setup instructions and setup responses are not retained MQTT messages.

## Clarifications and amendments

| Date | Authority | Decision |
|---|---|---|
| 2026-09-11 | Maintainer | Confirm execution lifetime, all-or-nothing outcomes, unchanged retries, unknown missing outcomes and preservation/recovery of accepted work across restart and power loss. Queue-specific definitions from that review are excluded by the later queue deferral. |
| 2026-09-24 | Focus group | Ratify the original OK/NOK response approach and envelope correlation. |
| 2026-10-13 | Maintainer | Confirm continuation of the same execution and corrugator reference scope; select JSON Pointer for fieldRef, replacing the earlier ambiguous pointer/path wording and dotted examples. Preserve the bounded recovery baseline without a new recovery protocol. |
| 2026-10-14 | Maintainer | Rename `response-setup` to `setup-response` for consistency. The old spelling is historical. The ADR number and filename remain stable. |

The accepted schema identifier is `cosi:setup-response-payload:1.0`; the topic message-type
segment and schema/example filenames use `setup-response` under ADR-000021.

## Consequences

- Producers can return one or multiple field errors without changing the response schema.
- Responses distinguish application outcomes from transport delivery and production completion.
- Producers and receivers preserve request identity separately from execution identity.
- The decision does not standardize manufacturer error meanings or a queue-management protocol.
