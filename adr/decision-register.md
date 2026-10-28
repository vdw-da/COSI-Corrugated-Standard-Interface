# Decision register — COSI

**Version:** 1.0 · **Updated:** 26 October 2026

The ADRs below record the current decisions and their dated amendments. Meeting records
identify the original authority. André Seifert approved the aligned package on 16 October 2026;
final PDFs and publication remain pending. Schema approval status is listed in the [README](../README.md#schemas).

## Architecture and data decisions

| Record | Decision | Status |
|---|---|---|
| [ADR-000001](ADR-000001-quality-message-end-of-job-mandatory.md) | Quality message required at job end; additional messages optional. Trigger configuration is outside v1.0. | Accepted |
| [ADR-000002](ADR-000002-quality-check-structure-checks-array.md) | [Quality header and atomic checks array](../docs/message-properties.md#quality-check-shape); qualitative OK/NOK permitted; numeric exceptions identify violated bounds. | Accepted |
| [ADR-000003](ADR-000003-setup-converting-infeed-settings-extraction.md) | Converting infeed settings use a dedicated object with input dimensions, feed type and sheets per cycle. | Accepted |
| [ADR-000004](ADR-000004-side-order-modelling.md) | Corrugator orders use orderType for production, side-order and waste-run (variant B2). | Accepted |
| [ADR-000005](ADR-000005-remove-actuals-from-setup.md) | Setup carries instructions and machine-side changed settings; production actuals use observation messages. | Accepted |
| [ADR-000006](ADR-000006-response-setup-schema-approach.md) | Setup-response reports all-or-nothing OK/NOK, correlates to the request and uses JSON Pointer field references and manufacturer-defined non-negative integer error codes; execution and retry identities remain distinct. | Accepted |
| [ADR-000007](ADR-000007-queue-schema-retained-state-baseline.md) | Queue state and management are excluded from v1.0; the historical retained-state design is deferred. | Deferred beyond v1.0 |
| [ADR-000008](ADR-000008-delete-request.md) | Queue deletion is excluded from v1.0; queue-delete is the deferred name; no deletion mechanism is selected. | Deferred beyond v1.0 |
| [ADR-000009](ADR-000009-performance-die-pressure-feedback.md) | Performance diePressure is one optional quantity in kN. | Accepted |
| [ADR-000010](ADR-000010-bidirectional-east-west-only.md) | IT/OT crossings use the Level 3.5 MQTT broker; horizontal MQTT and cloud are optional. Existing authentication and bounded delivery rules apply. | Accepted |
| [ADR-000011](ADR-000011-l2r-sequence-number-required.md) | Every non-empty corrugator order requires l2rSequenceNumber. | Accepted |
| [ADR-000012](ADR-000012-grammage-named-gsm.md) | Paper grammage uses gsm with g/m²; the deferred imperial notation is lb/MSF. | Accepted |
| [ADR-000013](ADR-000013-metric-only-for-v1.md) | v1.0 uses metric measurements and the defined field tokens; general imperial support is deferred to v1.1. | Accepted |
| [ADR-000014](ADR-000014-compliance-checklist-removed.md) | The compliance checklist and its binding mandate are removed from v1.0. | Accepted |
| [ADR-000015](ADR-000015-faultcode-closed-enum.md) | faultCode is the closed 40-code list plus null; internalCode is optional; adding a code requires a new standard version. | Accepted |
| [ADR-000016](ADR-000016-schema-corrections-to-documented-intent.md) | Schemas enforce documented references, correlation, UTC timestamps, numeric exceptions, color representation and fixed units; applicability follows each field. | Accepted |
| [ADR-000017](ADR-000017-unit-symbol-and-terminology-corrections.md) | Use m³ instead of m3 and pcs/h instead of kicks/h. | Accepted |
| [ADR-000018](ADR-000018-message-id-uuid-v5.md) | Message and correlation identifiers use UUID v5; new instances have distinct identities and retries preserve the assigned identity. | Accepted |
| [ADR-000019](ADR-000019-custom-props-extension-object.md) | customProps is permitted at setup payload roots and corrugator orders; unknown extension keys are ignored. | Accepted |
| [ADR-000020](ADR-000020-standard-named-cosi.md) | The standard is COSI — Corrugated Standard Interface; schema identifiers use cosi; VDW is the publisher. | Accepted |
| [ADR-000021](ADR-000021-mqtt-topic-scheme-and-schema-identification.md) | Topics use cosi/site/machine/assetClass/direction; plant-owned identifiers and required payload schemaId identify the contract. | Accepted |
| [ADR-000022](ADR-000022-mqtt-last-will.md) | Optional OT Last Will uses a dedicated message, empty payload, shared fresh connection UUID v5, QoS 1, no retention and enabled Keep Alive; subscriber handling is outside scope. | Accepted |
| [ADR-000023](ADR-000023-performance-quantity-meanings.md) | Production counters, event quantities and current contents retain distinct meanings; stackCount is sheets per stack and stackHeight is physical height. Manual refeeding accounting is excluded. | Accepted by maintainer |
| [ADR-000024](ADR-000024-maintenance-document-service-scope.md) | Maintenance messages and local document availability remain; automatic document-update and fault-lifecycle protocols are not defined in v1.0. | Accepted by maintainer |

## Publication decisions

| Record | Decision | Status |
|---|---|---|
| [ADR-000025](ADR-000025-publication-imprint-and-privacy.md) | One English imprint/privacy notice linked from the main README and the five publication-source Markdown documents and rendered on a separate legal page after the original PDF imprint; German advice preserved with correspondence identities redacted. VDW policy/account-link updates and legal review remain prerequisites for completion. | Structure accepted by maintainer, 26 October 2026; legal wording review pending; correspondence identities redacted by maintainer instruction, 27 October 2026 |
| [ADR-000026](ADR-000026-industry-commitment-publication.md) | Publish the 22 organisation names from the supplied commitment overview, with sourced logos, in a non-normative Technical Guide appendix before revision history; exclude implementation schedules and internal details; add an attribution/responsibility notice; apply Palm’s supplied name and logo correction. | Publication scope accepted by maintainer, 26 October 2026; responsibility wording prepared for legal review |

## Additional meeting and publication decisions

| Decision | Authority and source |
|---|---|
| Numeric precision follows the source data type; no fixed decimal places or additional precision limits. | Focus group, 24 September 2026; [numeric precision](2026-09-24-notes.md#numeric-precision) |
| common-types.schema.json is approved. | Focus group, 24 September 2026; [common types](2026-09-24-notes.md#common-types-approval) |
| ERP/MES supplies target speed according to plant business rules; no common calculation method is prescribed. | Focus group, 24 September 2026; [target-speed baseline](2026-09-24-notes.md#target-speed-baseline) |
| Movement provision is optional by supplier/customer agreement; supplied values use the defined enum. statusId remains required in a supplied logistics entry. | Working group, 1 October 2026; maintainer clarification, 14 October; [movement](2026-10-01-notes.md#a5-clarification-by-maintainer--14-october-2026) |
| Quality impact ratings are outside v1.0. | Working group, 9 June 2026; [meeting record](2026-06-09-notes.md) |
| Publication target is 1 November 2026; VDW publishes the standard and official press release. Company communication follows official publication. Christiane Trumpp coordinates publication and press for VDW. | [October 1 publication decision](2026-10-01-notes.md#b1-publication-timing); ownership confirmed by André Seifert, 14 October 2026 |
| Publish PDFs on the web, without hard copies, and make a public repository copy. Each release includes six reviewed PDFs (including Schemas and Samples) committed under docs/pdf/&lt;version&gt;/; that folder contains only PDFs. | [October 1 format decision](2026-10-01-notes.md#b3-publication-format-and-repository) and [public copy](2026-10-01-notes.md#c3-contact-and-community); PDF workflow confirmed by André Seifert, 14 October 2026; six-volume count confirmed by maintainer, 28 October 2026 ([ADR-000025](ADR-000025-publication-imprint-and-privacy.md#amendment-note--28-october-2026-six-pdf-volumes)) |
| The PDF edition reproduces the Markdown source; the Markdown for the corresponding document version in the official GitHub repository prevails in case of discrepancies. | André Seifert, 16 October 2026; [Document Authority](../docs/technical-guide.md#document-authority) |
| Below the authors: “Technical editors: technical specification development and quality assurance.” André Seifert (ePS) and Robin Boeckxstaens (OMP). | [October 1 addendum](2026-10-01-notes.md#b4-addendum-to-the-technical-guide); exact credit confirmed by André Seifert, 14 October 2026 |
| The aligned v1.0 package and schemas are approved; the final PDFs follow separately (current set: six volumes). Push to the existing repository is authorized; artifact creation and publication remain pending. | André Seifert, 16 October 2026: “the final package is approved. Push to github now. We do not yet want to build the artifacts.”; current PDF count clarified in [ADR-000025](ADR-000025-publication-imprint-and-privacy.md#amendment-note--28-october-2026-six-pdf-volumes) |
| The technical commission collects feedback from installations. Testing/sandbox design is deferred to a future meeting. | [October 1 maintenance decision](2026-10-01-notes.md#c1-maintenance-and-versioning) and [testing discussion](2026-10-01-notes.md#c2-testing) |
