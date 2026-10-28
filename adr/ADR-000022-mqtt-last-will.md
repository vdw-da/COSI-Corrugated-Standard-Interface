# ADR-000022 — Optional MQTT Last Will for OT equipment in COSI v1.0

- **Status:** Accepted; aligned package approved by André Seifert, 2026-10-16
- **Date:** 2026-10-01
- **Decided by:** Working group, 2026-10-01; maintainer amendments, 2026-10-01 and 2026-10-11–13
- **Source:** [October 1 meeting notes, A4](2026-10-01-notes.md#a4-last-will-and-persistent-mqtt-session); dated maintainer confirmations below
- **Asset class:** `lastwill`

## Context

MQTT Last Will lets the broker publish a message supplied by a client when its connection
ends unexpectedly. The notification concerns connectivity, not proof of a physical machine stop.
The client prepares the Will before the future disconnection time is known.

## Decision

Last Will is optional for OT equipment. ERP/MES Last Will is outside v1.0.

| Property | Required value when Last Will is used |
|---|---|
| Topic | `cosi/<site>/<machine>/lastwill/send` |
| `assetClass` | `lastwill` |
| `schemaId` | `cosi:lastwill-payload:1.0` |
| `messageType` | `cos` |
| `status` | `lastwill` |
| `timestamp` | `null` |
| `payload` | Required empty object `{}`; no properties, including `customProps` |
| `connectionId` | Top-level lowercase, hyphenated, 36-character UUID v5 |
| MQTT Will QoS | 1 |
| MQTT Will Retain | false |
| MQTT Keep Alive | Enabled, with a non-zero installation-defined interval |

The regular envelope requirements, including `messageID` and `machineId`, also apply.
The null timestamp exception applies only to Last Will. Other messages retain their required
UTC event timestamp with a `Z` suffix under [ADR-000016](ADR-000016-schema-corrections-to-documented-intent.md).
A connection timestamp must not be presented as the time of its future loss.

Each MQTT connection has a fresh, globally distinct `connectionId`, including after restart
or reuse of the MQTT client ID. Its Will and its normal equipment messages share that identifier
when Last Will is enabled. Connection and message identities have separate lifetimes.

Producers ensure distinct UUID v5 generation inputs for distinct connections. Allocation is
implementation-defined; a producer namespace and persistent counter are an example, not a
required algorithm. UUID format alone proves neither global uniqueness nor connection freshness.
The representation follows [ADR-000018](ADR-000018-message-id-uuid-v5.md):

```text
^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$
```

COSI specifies no fixed loss-detection or notification deadline. Whether and how subscribers
analyze the Will, determine current availability or react to delayed or older notifications
is outside the standard. No subscriber algorithm is required.

## Decision history and supersession

| Date | Authority | Decision |
|---|---|---|
| 2026-10-01 | Working group | Include Last Will with a dedicated status; the meeting proposed using a performance message. |
| 2026-10-01 | Maintainer | Optional OT-only scope; `lastwill` status, dedicated asset class, schema and topic. |
| 2026-10-11 | Maintainer | Reaffirm the dedicated message, explicitly superseding the performance-message approach in the October 1 minutes. Select `cos`, null timestamp, QoS 1, non-retention and a fresh shared connection identity. |
| 2026-10-12 | Maintainer | Place `connectionId` in the envelope; use lowercase hyphenated UUID v5, globally distinct across producers and restarts, with allocation left to implementations. The proposed UUID v4 alternative was not accepted. |
| 2026-10-13 | Maintainer | Require an empty payload; enable Keep Alive with installation-defined timing and no fixed COSI deadline. |
| 2026-10-13 | Maintainer | Exclude consumer analysis and handling from COSI. This supersedes in full the earlier same-day rule that an older-connection Will must not change current availability, including its validation criterion. The subsequent uncertainty-handling proposal was not accepted. |

The original October 1 meeting outcome remains recorded in the minutes. Its performance
representation is historical; it is not an alternative v1.0 contract. Earlier proposed
freshness windows, timestamp ordering, MQTT 5 Will Delay settings and consumer rules were not
adopted. The settled producer contract above is the current decision.

## Consequences

- Connection loss has a dedicated message rather than artificial performance measurements.
- Producers must allocate connection identities and register the specified MQTT Will settings.
- Subscribers choose their availability assessment and response; uniform reactions are not promised.
- Schema validation can check message shape and identifier format, but cannot establish actual
  connection allocation or broker behavior.
- Additional Will payload fields require a future contract change.

Transport recovery follows [ADR-000010](ADR-000010-bidirectional-east-west-only.md#delivery-and-reconnection).
The schemas, example and normative documentation implement this decision. André Seifert
approved the aligned package on 16 October 2026; final PDFs and publication remain pending.

MQTT transmits the Will payload supplied at connection time; it does not fill JSON placeholders
at publication. See [MQTT 3.1.1 §3.1.3.3](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
and [MQTT 5 §3.1.3.4](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html).
