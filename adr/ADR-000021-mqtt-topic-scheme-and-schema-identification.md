# ADR-000021 — MQTT topic scheme and schema identification

- **Status:** Accepted
- **Date:** 2026-10-01
- **Decided by:** Maintainer, 2026-10-01; topic version and direction confirmed by the working group, 2026-10-01
- **Source:** Explicit maintainer answers on topic structure, identifier ownership, direction, spelling and the required `schemaId` field carrying the full schema identifier
- **Asset class:** — (standard-wide)
- **Implementation:** Applied to schemas/examples/guide on 2026-10-14; aligned package approved by André Seifert, 2026-10-16

## Context

A common topic mapping defines routing, plant-owned equipment identities and message
directions. The decisions below supersede the earlier versioned topic proposal. The
[October 1 meeting, A3](2026-10-01-notes.md#a3-definition-of-the-mqtt-topics) confirms omission
of the topic version and inclusion of send/receive.

## Decision

The topic pattern is:

```text
cosi/<site>/<machine>/<message-type>/<direction>
```

| Element | Decision |
|---|---|
| Prefix | Fixed `cosi` root |
| Site | Site identifier unique within the broker's `cosi` namespace |
| Machine | Machine identifier unique within its site |
| Identifier ownership | Plant owners maintain the authoritative site/machine identifier list, guarantee uniqueness and communicate the identifiers to all providers. ERP, MES and machine providers map their own identifiers to the plant definitions. |
| Message type | Exact `assetClass` value, such as `setup-corrugator`, `performance` or `maintenance-measurement`. The topic segment does not use the envelope's trigger field `messageType` (`hbt`, `cos`, `onetime`). |
| Direction | Machine perspective: `send` means machine → ERP/MES; `receive` means ERP/MES → machine |
| Spelling | Every segment uses only lowercase letters `a-z`, digits `0-9` and hyphens `-` |
| Version | No version segment in the topic. Each JSON message's envelope carries the required `schemaId` field containing the full applicable payload schema identifier, including its version. |

The full schema identifier follows the applicable payload schema's `$id`, for example
`cosi:performance-payload:1.0` for a performance payload. The existing `-payload` suffix
is retained. This decision preserves the identifier scheme established by
[ADR-000020](ADR-000020-standard-named-cosi.md).

Setup instructions and machine-side changed setup settings use the same `assetClass` and
different directions, consistent with the S2 clarification in
[ADR-000005](ADR-000005-remove-actuals-from-setup.md):

```text
cosi/plant-1/corrugator-01/setup-corrugator/receive
cosi/plant-1/corrugator-01/setup-corrugator/send
```

## Schema identification in JSON

Every message envelope must contain **`schemaId`**, a required string holding the full
identifier of the applicable payload schema. For a performance message, the declaration is:

```json
"schemaId": "cosi:performance-payload:1.0"
```

The identifier must correspond to the message's `assetClass` and the schema version used
for its payload. The field name, full identifier and retention of `-payload` were confirmed
by the maintainer on 2026-10-01.

The envelope and all normative examples include this field. A schema document's `$id` is not itself a declaration inside a
transmitted JSON message.

## Consequences

- Fill the guide's topic mapping from the agreed pattern and applicable message directions.
- Document plant ownership of identifiers and provider mapping obligations.
- Add required `schemaId` to the envelope and align validation, examples and
  message-property documentation with the published schema identifiers and `assetClass`.
- Align topic examples and identifier spelling across the documentation.
- Topic names remain stable across schema versions; consumers identify the applicable schema
  from the JSON message.

The normative schemas, examples and guide implement this mapping. Queue scope is governed by
ADR-000007/000008, Last Will by ADR-000022 and transport recovery by ADR-000010.


## Naming cross-reference — 14 October 2026

ADR-000006 now names the setup acknowledgment `setup-response`. Under this ADR's existing
rules, its topic is `cosi/<site>/<machine>/setup-response/send`, and its payload schema identifier
is `cosi:setup-response-payload:1.0`. This is an application of the existing topic/identifier
rules, not a new topic scheme. Queue names remain deferred under ADR-000007/000008.
