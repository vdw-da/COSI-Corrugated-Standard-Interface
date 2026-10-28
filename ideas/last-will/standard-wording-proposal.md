# Last Will and persistent MQTT sessions — proposed standard wording

**Historical proposal, not the v1.0 contract.** The current producer decision is
[ADR-000022](../../adr/ADR-000022-mqtt-last-will.md): optional OT-only dedicated Last Will,
empty payload, null timestamp, fresh shared connection UUID v5, QoS 1, non-retention and
enabled Keep Alive. Subscriber analysis and handling are outside the standard.
Transport and recovery follow [ADR-000010](../../adr/ADR-000010-bidirectional-east-west-only.md#delivery-and-reconnection).
Stronger outbox, persistence, history and recovery-window proposals below were not adopted.
Pending-decision and implementation instructions below describe the former proposal, not current work.
ERP/MES Last Will remains a [future idea](erp-mes-last-will.md).

## Decision proposed to the group

The optional OT Last Will producer contract is settled; apply ADR-000022 during alignment.
Adopt persistent MQTT sessions for delivery to temporarily disconnected subscribers. Require QoS 1 publishing and
subscriptions for the v1.0 message roles retained after the scope decisions. Apply the
subscription rule to machine, adapter and ERP/MES clients in both directions.

Keep transport buffering at the broker distinct from the machine's production queue proposed
for v1.1. Deferring production-queue management does not defer MQTT session persistence.

Recommend a documented, plant-agreed recovery window and capacity rather than an arbitrary
universal duration. The installation must state its supported outage duration and traffic
volume before commissioning. The group must approve this approach or specify a common minimum.

## Where to document it

| Standard location | Proposed change |
|---|---|
| Technical Guide § 2.2, Transport Protocol | Make QoS 1 the required baseline and reference § 2.5 for persistent sessions and recovery |
| Technical Guide § 2.3.6, Data Integrity & Reliability | Replace “Enable only when required” with the persistent-session requirement below; align the QoS row |
| Technical Guide § 2.5.1, Graceful Shutdown | Keep the final `offline` message; distinguish it from Last Will and reference new § 2.5.4 |
| Technical Guide § 2.5.2, Retry on Message Failure | Clarify the boundary between sender retries and broker-held subscriber delivery; resolve the three-retry limit as described below |
| Technical Guide § 2.5.3, Reconnection Behavior | Replace with the session-resumption wording below |
| Technical Guide, new § 2.5.4 / § 2.5.5 | Add Last Will and recovery limits/gap handling |
| Message Properties, envelope / `messageType` / timestamp / status | Document the approved Will variant and delayed-message interpretation |
| Glossary | Define persistent session, Session Present, Last Will and retained message; align QoS wording |
| Envelope, dedicated Last Will schema and examples | Add `lastwill` with `$id: cosi:lastwill-payload:1.0` and its envelope mapping; use the accepted empty payload during coordinated implementation |

ADR-000022 records the accepted Last Will details.
Use the topic pattern in ADR-000021 and the producer contract in ADR-000022 for the Will schema
change. Consumer freshness analysis is outside scope and is not a prerequisite for publication.
The existing candidate remains superseded preparation material.

## Draft clauses for the Technical Guide

**Historical preparation:** Last Will consumer-analysis/availability clauses below were
superseded by the October 13 scope correction in ADR-000022. They must not enter the normative
rewrite or its conformance checks. The stronger recovery proposals remain unapproved.

### § 2.2 and § 2.3.6 — transport baseline

> COSI publications and subscriptions shall use MQTT QoS 1. Clients receiving COSI messages
> shall maintain persistent sessions so that a temporary disconnection does not discard their
> subscriptions or pending delivery within the installation's documented recovery limits.
> Clients shall use a stable, unique MQTT Client Identifier per logical client. Independent
> clients shall not share an identifier, and routine reconnection shall not reset the session.

This deliberately changes QoS 1 from recommended to required. The group may narrow the
message roles covered, but any exceptions must be explicit; the draft includes heartbeats.
Capacity planning must therefore account for accumulated heartbeat traffic.

### § 2.5.3 — reconnection and subscription recovery

> Clients shall reconnect automatically and attempt to resume their previous session. MQTT
> 3.1.1 clients shall use `CleanSession = 0`. MQTT 5 clients shall use `Clean Start = 0`
> on reconnection and a non-zero Session Expiry Interval sufficient for the documented recovery
> window. A deliberate session reset is a recovery/commissioning operation, not normal reconnect.
>
> On connection, clients shall inspect `Session Present` in CONNACK. If the expected session
> exists, clients shall resume delivery using its stored subscriptions. If it is absent, clients
> shall establish and verify their subscriptions again and report the loss of expected session
> continuity through monitoring. An initial connection establishes subscriptions; it does not
> recover messages published before those subscriptions existed.
>
> Replayed messages shall preserve their original `messageID` and event `timestamp`.
> Receivers shall process duplicates idempotently and interpret delayed data at its original
> event time. Historical heartbeats shall not establish current connection health. MQTT delivery
> acknowledgement shall not be interpreted as application acceptance of a setup instruction.
> Fresh machine state and normal heartbeat publication shall resume on reconnection.

The version-specific settings follow [MQTT 3.1.1 §§ 3.1.2.4 and 3.2.2.2][mqtt311] and
[MQTT 5 §§ 3.1.2.4, 3.1.2.11.2 and 3.2.2][mqtt5]. Session expiry and message expiry are
different: a long-lived session does not prevent individual messages from expiring.

### New § 2.5.4 — unexpected disconnection and Last Will

> Last Will registration is optional. A COSI publishing client for OT equipment may register one
> on connection. When configured, the Will shall use the dedicated `lastwill` notification on
> `cosi/<site>/<machine>/lastwill/send`, with accepted Will QoS 1 and
> `retain = false`. For MQTT 5, the proposed baseline is Will Delay Interval zero. A non-zero
> Keep Alive shall be configured and its detection interval documented.
>
> The notification means that the client's connection was lost and current machine state is
> unknown. It shall not assert that production stopped, fabricate a zero speed, reset counters
> or supply a connection-time timestamp as the time of disconnection. Planned shutdown shall
> continue to use the final `offline` message followed by orderly MQTT disconnect.
>
> A returning machine shall publish fresh state. Consumers shall distinguish earlier connection
> loss notifications from the current connection before changing current availability state.

**Decided message identification:** `assetClass: lastwill`, required
`schemaId: cosi:lastwill-payload:1.0` and `status: lastwill`.
Trigger, timestamp and required empty `payload: {}` with no properties are decided in ADR-000022. The
[performance-based candidate](performance-last-will.json) is superseded design history;
its empty performance fields are not requirements for the dedicated Last Will schema.

**Historical question — now outside COSI scope under ADR-000022:** establishing
freshness relative to startup/live messages. A stable MQTT Client Identifier identifies the
logical client, not a particular connection, and is not automatically visible in delivered
application payloads. A unique Will `messageID` alone does not establish this ordering.

A non-retained Will can still reach an existing persistent subscriber after reconnection.
A genuinely new subscriber cannot rely on receiving a past Will. The same delayed-notification
rule must therefore work with session replay. MQTT Will lifecycle rules are in
[MQTT 3.1.1 § 3.1.2][mqtt311] and [MQTT 5 § 3.1.3.2.2][mqtt5].

### New § 2.5.5 — recovery limits and gaps

> The installation documentation shall specify the supported outage window, expected message
> load, session lifetime, pending-message capacity, restart persistence and overflow behaviour.
> Broker and client configuration shall support that declared window and load. Any message
> expiry shall be documented by message role and shall not silently contradict the recovery
> guarantee. Unlimited storage or replay is not required.
>
> Unexpected session loss, storage exhaustion or expiry affecting expected delivery shall be
> surfaced through monitoring. Reconnection alone shall not be reported as proof that all
> missed messages were recovered. The installation shall document how operators reconcile
> missing reports or uncertain instruction outcomes and establish current state.

This is a proposed COSI operating requirement, not a claim that MQTT provides a universal
history-complete signal. Storage limits are recognized in [MQTT 3.1.1 § 4.1][mqtt311].

### § 2.5.2 — sender outage boundary and retry clarification

> Persistent subscriber sessions recover messages already accepted by the broker. They do
> not recover messages that a disconnected publisher has not sent. Implementations shall
> document their local buffering and retry limits and surface undeliverable messages.

**Proposed handling of the existing three-retry rule:** keep three attempts as the immediate
retry cycle; where a message must survive a publisher outage, retain it in a durable local
outbox and retry after reconnection, within the documented capacity and outage window. Preserve
its ID and timestamp. Alert on exhaustion/overflow; do not silently discard a required report.
This would amend the current “undeliverable after three attempts” rule and needs explicit
approval. Persistent sessions alone must not be presented as approval of this outbox extension.

## Group sign-off and subsequent validation

At TOP 19, decide the persistent-session/QoS baseline, plant-defined versus common minimum
recovery limits, the sender-outbox extension and the Last Will representation/freshness rule.
Assign owners for any remaining text or schema work before November 1 publication.

After implementation, verify a ten-minute subscriber outage, lost session, broker restart,
publisher outage, exhausted storage, duplicate reports and delayed Will after fresh state.
Check both directions and confirm required job-end quality reports survive within the declared
limits. These are acceptance scenarios for the proposed change, not tests already passed.

[mqtt311]: https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/errata01/os/mqtt-v3.1.1-errata01-os-complete.html
[mqtt5]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html
