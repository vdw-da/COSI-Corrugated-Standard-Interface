# Changelog

## Unreleased — v1.0 finalization, 16 October 2026

- Rename `response-setup` to `setup-response` across the active asset class, payload schema ID,
  schema/example files and documentation references (ADR-000006 naming amendment).
- Use `queue` and `queue-delete` for deferred queue material; queue remains excluded from v1.0.
- André Seifert approved the aligned package and schemas on 16 October 2026.
  The six final PDFs will follow; release artifacts and publication remain pending.


All notable changes to **COSI — the Corrugated Standard Interface** are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow the
standard's own version marker — the one carried by the technical guide and by the schema `$id`s —
not an independent numbering.

Each entry cites the decision record that authorises it. The records themselves live in
[`adr/`](adr/) and are indexed in [`adr/decision-register.md`](adr/decision-register.md).

## [1.0] — Unreleased; target 2026-11-01

**Prepublication.** This is the planned first public version. The former October 1 “Released”
metadata was premature and is corrected; no public release is asserted. The 0.9 draft circulated
inside the working group only. The aligned package and schemas are approved by André Seifert
(16 October 2026); final PDFs and publication remain outstanding.

### Added

**Message envelope** — a common JSON envelope shared by every message: `messageID`, `assetClass`, `schemaId`,
`messageType`, `machineId`, `timestamp`, `status`, `payload`, conditional `correlationID` and
`connectionId`. schemaId matches the full payload identifier/version (ADR-000021).
`messageID` and `correlationID` are UUID version 5 ([ADR-000018](adr/ADR-000018-message-id-uuid-v5.md));
ordinary envelope timestamps are UTC with a `Z` suffix; the dedicated Last Will requires null ([ADR-000016](adr/ADR-000016-schema-corrections-to-documented-intent.md)).

**Eight asset classes** covering four business cases and optional OT connection-loss notification:

| Business case | Asset classes |
|---|---|
| Performance | `performance` |
| Setup | `setup-corrugator`, `setup-converting`, `setup-response` |
| Maintenance | `maintenance-document`, `maintenance-measurement` |
| Quality | `quality` |
| OT connection loss | `lastwill` |

**Ten JSON Schema documents** (draft 2020-12) — the envelope, a shared `common-types` definition
set, and one payload schema per asset class. Each schema identifies itself as `cosi:<name>:1.0`
([ADR-000020](adr/ADR-000020-standard-named-cosi.md)), and cross-schema references resolve through
those URN `$id`s, so the schemas validate with standard tooling as published
([ADR-000016](adr/ADR-000016-schema-corrections-to-documented-intent.md)).

**Nine example messages** covering all eight payload asset classes and both setup response outcomes,
each validating against the envelope and its payload schema.

**Six PDF publication volumes**, comprising five Markdown specification documents — [technical guide](docs/technical-guide.md),
[glossary](docs/glossary.md), [naming conventions](docs/naming-conventions.md),
[message properties](docs/message-properties.md), and the closed
[corrugated fault-code table](docs/corrugated-faults.md) of 40 three-letter codes adapted from
ISO 14224:2016, Annex B ([ADR-000015](adr/ADR-000015-faultcode-closed-enum.md)),
plus [Schemas and Samples](docs/pdf/1.0/cosi-schemas-and-samples-v1.0.pdf), generated
from the JSON schemas and examples. The six-volume count was confirmed by the
maintainer on 28 October 2026 ([ADR-000025](adr/ADR-000025-publication-imprint-and-privacy.md#amendment-note--28-october-2026-six-pdf-volumes)).

**Communication directions** — the standard defines which directions are permitted at all: east-west
exchange is bidirectional inside a zone, every north-south crossing of the IT/OT boundary runs
through the Level 3.5 broker, and direct crossings are prohibited in both directions
([ADR-000010](adr/ADR-000010-bidirectional-east-west-only.md)).

**Extension point** — a `customProps` object on both setup payloads carries manufacturer- and
site-specific properties. Its content is not standardized, and consumers ignore unknown keys, so
standard operation never depends on proprietary extensions
([ADR-000019](adr/ADR-000019-custom-props-extension-object.md)).

### October 14 alignment

- Apply required schemaId, concrete topic mappings and plant-owned identifier spelling
  ([ADR-000021](adr/ADR-000021-mqtt-topic-scheme-and-schema-identification.md)).
- Implement optional dedicated OT Last Will: empty payload, null timestamp, fresh/shared UUID v5
  connectionId; document QoS 1/non-retained and Keep Alive without subscriber-analysis requirements
  ([ADR-000022](adr/ADR-000022-mqtt-last-will.md)).
- Archive queue artifacts and remove previousSetupId queue placement from the normative setup
  contract; keep setup/response and machine-side settings feedback
  ([ADR-000007](adr/ADR-000007-queue-schema-retained-state-baseline.md)).
- Apply JSON Pointer fieldRef, sheets-per-stack stackCount and physical stackHeight in mm;
  align cumulative counters, current contents and execution identities to the
  [quantity definitions](adr/ADR-000023-performance-quantity-meanings.md) and
  [setup outcome rules](adr/ADR-000006-response-setup-schema-approach.md).
- Clarify atomic quality checks and qualitative NOK; make movement optional by supplier/customer
  agreement while preserving its enum and required statusId.
- Restore both authentication options with certificates preferred; retain field-specific null
  rules and the existing delivery baseline; leave the document-update service for future work.
  See the [decision register dispositions](adr/decision-register.md).

### Conventions fixed for 1.0

- **Metric only.** Existing field-specific unit/count/classification tokens retain their defined
  uses; imperial measurement sources convert before publishing. General imperial-unit support
  is an explicit non-goal for 1.0, deferred to v1.1
  ([ADR-000013](adr/ADR-000013-metric-only-for-v1.md)).
- **Numeric precision is not prescribed.** Producers send the precision their source provides;
  consumers must not assume a fixed number of decimal places.
- **Field naming** — casing, language, permitted abbreviations, `uom` values and enum style are
  governed by [naming conventions](docs/naming-conventions.md).
