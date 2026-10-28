# MQTT Last Will and persistent sessions — proposal for October 1

**Historical proposal, not the v1.0 contract.** The current producer decision is
[ADR-000022](../../adr/ADR-000022-mqtt-last-will.md): optional OT-only dedicated Last Will,
empty payload, null timestamp, fresh shared connection UUID v5, QoS 1, non-retention and
enabled Keep Alive. Subscriber analysis and handling are outside the standard.
Transport and recovery follow [ADR-000010](../../adr/ADR-000010-bidirectional-east-west-only.md#delivery-and-reconnection).
Stronger outbox, persistence, history and recovery-window proposals below were not adopted.
Pending-decision and implementation instructions below describe the former proposal, not current work.
ERP/MES Last Will remains a [future idea](erp-mes-last-will.md).

## Notification scope and remaining representation

Last Will registration is optional for OT equipment in v1.0. The dedicated `lastwill` asset
class announces unexpected connection loss using `status: lastwill`. The equipment's physical
state is not established by the notification. Required empty `payload: {}`, trigger and timestamp are recorded in ADR-000022; lifecycle details remain to be decided.

The client supplies the Will payload during CONNECT; the broker later publishes it when the
connection ends without an orderly DISCONNECT. It cannot supply future production readings or
the future loss time. Publication may be delayed, including by broker failure. Source:
[MQTT 3.1.1 §§ 3.1.2.5–3.1.2.7 and 3.1.3.3](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/errata01/os/mqtt-v3.1.1-errata01-os-complete.html).

## Earlier performance-based candidate — superseded

The earlier proposal prepared [this example](performance-last-will.json) at connection establishment:

```json
{
  "messageID": "0ad7e62f-45ae-5a24-a789-df85831847f1",
  "schemaId": "cosi:performance-payload:1.0",
  "assetClass": "performance",
  "messageType": "cos",
  "machineId": "corrugator-01",
  "timestamp": null,
  "status": "lastwill",
  "payload": {
    "speed": null,
    "inputs": [],
    "outputs": []
  }
}
```

The UUID is illustrative; each connection's Will requires its own message identity under the
existing UUID v5 rule. Re-deliveries of that Will preserve its identity. A later connection
must not reuse the prior Will's identity.

| Element | Proposed meaning |
|---|---|
| `assetClass: performance` | Reuse the performance payload family, without a new asset class |
| `schemaId: cosi:performance-payload:1.0` | Full payload schema identifier, following ADR-000021; required envelope field awaiting implementation |
| `messageType: cos` | Proposed reuse of the existing change-of-status trigger; the decided `lastwill` status identifies the Will |
| `timestamp: null` | The disconnected client cannot know the future event time. Permit null only for this Will variant; normal messages retain their existing event-time rule |
| `status: lastwill` | Decided notification status. Identifies the Last Will without asserting that production stopped or the machine powered down |
| `speed: null` | No current speed observation; never fabricate zero speed |
| Empty `inputs` / `outputs` | No stream observations in this notification; do not clear stream inventories or reset accumulated values |
| Other measurements omitted | No fabricated final counters and no cached values presented as current readings |

This is a **status notification using a performance-shaped payload**, not a new production
sample. Receivers preserve earlier measurements with their original timestamps and mark
current connectivity/state as unavailable. They must not derive production stop duration or
final job totals from this notification alone.

**Current validation:** the minimal payload fits the performance payload structure. The full
candidate does not validate against the current envelope: `schemaId` is not yet allowed,
`lastwill` is not yet in the status enum, and `timestamp` cannot currently be null.
The dedicated Last Will trigger and null timestamp are now decided in ADR-000022;
this historical performance representation is superseded. Empty arrays/null speed must not clear inventories or counters.

**Runtime values:** the client can fill its JSON template before sending CONNECT. Standard
MQTT does not expand placeholders when the broker later publishes the stored Will payload.
A connection-time timestamp cannot stand for the future disconnection time. The candidate
therefore proposes `timestamp: null`; a broker-generated timestamp would require an explicitly
defined broker extension and would identify the broker's observation/publication time.
See [MQTT 3.1.1 § 3.1.3.3](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html).

## MQTT publication settings and lifecycle — preparation history

Consumer-analysis recommendations in this section are superseded by the October 13 scope
correction in ADR-000022; accepted producer settings remain authoritative there.

**Proposed baseline:** Will QoS 1, retain false. This introduces a live loss notification
without introducing a persistent availability-state protocol. Late subscribers still need
the agreed heartbeat/startup policy; new subscribers cannot rely on recovering a past Will. Existing persistent subscribers may
receive a pending Will after reconnection and must handle its age/connection identity.
If the group wants a retained availability state, define its online replacement, reconnect
behaviour and late-subscriber semantics explicitly rather than retaining a measurement snapshot.

The topic is `cosi/<site>/<machine>/lastwill/send`, following ADR-000021 and ADR-000022.
The client must be authorized to register that topic. **Keep Alive boundary accepted October 13:**
enable non-zero MQTT Keep Alive when using Last Will; leave its interval to the installation.
COSI specifies no fixed loss-detection or notification deadline; its heartbeat cadence is unchanged.
Transport connectivity does not prove that the measurement application remains healthy.

An orderly shutdown keeps the existing final `offline` message followed by orderly disconnect.
The Last Will covers unexpected connection loss; it does not redefine `offline` as a confirmed
physical shutdown. On reconnect, the machine publishes fresh actual state and resumes heartbeats.
The maintainer confirmed on 2026-09-29 that a disconnected system receives its messages via
its bus subscription after reconnecting, subject to the transport conditions in ADR-000010. The Will reports connection loss; the broker session provides missed-message delivery.

For MQTT 3.1.1, this requires a preserved session (`CleanSession = 0`), an existing subscription
and QoS 1 or 2 delivery; reconnecting with a fresh subscription alone does not replay missed
non-retained messages. See [MQTT 3.1.1 § 3.1.2.4](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/cs01/mqtt-v3.1.1-cs01.html).
Confirm session/storage limits and missing-session handling before claiming a recovery guarantee.
Messages generated while the publisher cannot reach the broker require sender retry/buffering;
subscriber session storage alone cannot recover them. Duplicate/delayed-message handling and
current-state recovery also remain to be defined. These are operating conditions to settle,
not newly approved requirements.

## Current disposition

The Last Will producer contract is settled in ADR-000022. Consumer analysis, availability
tracking and reactions are outside COSI requirements, not remaining choices. This supersedes
the earlier receiver-handling rule and questions preserved in the preparation history.
The accepted producer contract is implemented. Final package approval remains separate;
the stronger recovery proposals in this document were not adopted.

## Implementation and validation if approved

Align the envelope's conditional rules, dedicated `lastwill` payload schema, message-property
tables, guide, glossary, topic mapping and examples. Keep normal performance validation intact.
Validate the accepted producer message fields, Will registration settings and fresh connection
identity on reconnect. Consumer availability algorithms and reactions are not conformance
requirements. Apply the agreed representation during coordinated alignment; recording decisions
is not implementation or final approval.
