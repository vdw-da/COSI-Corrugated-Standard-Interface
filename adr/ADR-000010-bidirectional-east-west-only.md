# ADR-000010 — Bidirectional data flow is east-west only; north-south is brokered

- **Status:** Accepted (ratified by the focus group 2026-09-24)
- **Date:** 2026-09-08
- **Decided by:** Focus group 2026-09-07; amended by the maintainer 2026-09-08
- **Ratified by:** Focus group 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-06 (finding #37); closes technical guide Open Issue 03
- **Asset class:** — (architecture-wide)

## Context

Guide § 4.10 Open Issue 03 asked whether setup data can be returned to machines without
requiring manufacturer cloud services. § 2.4 already names Level 3.5 the **IT/OT Integration
Layer** and requires all data to be accessible at Levels 3–4, with Level 5 (cloud) optional.
What was missing was a rule stating which communication directions are permitted at all.

## Decision

- **East-west** — peer-to-peer exchange inside one zone (controller ↔ controller in OT;
  ERP ↔ MES in IT) — is bidirectional and need not use MQTT. Direct hardware-to-hardware control is out of scope
  of this standard.
- **North-south** — any exchange crossing the IT/OT boundary — is permitted **only** through
  the Level 3.5 MQTT broker.
- Direct crossings of the IT/OT boundary are prohibited in **both** directions. A manufacturer
  offering a non-MQTT interface must provide an MQTT adapter (§ 2.2, § 4.2).
- Cloud services (Level 5) remain optional and must not be required for standard operation.

## Consequences

- Guide § 2.4 gains a **Communication Directions** block; the glossary gains OT, IT,
  north-south and east-west.
- The § 4 setup instruction/response exchange and machine-side changed-settings feedback
  are **brokered north-south** flows and stay permitted; see
  [ADR-000006](ADR-000006-response-setup-schema-approach.md) and
  [ADR-000005](ADR-000005-remove-actuals-from-setup.md).
- A REST call from an ERP straight into a machine controller is non-conformant, as is a
  controller calling an IT system directly.
- Guide Open Issue 03 was closed and its former § 4.10 was retitled *Issue Log*. The
  maintainer-approved editorial consolidation on 2026-10-16 places the cloud-independence
  explanation in § 4.1, referring to § 2.4; the communication rules are unchanged.
  Issue 05 (§ 3.7, target speed baseline) was separate; it is defined by the
  [focus-group record](2026-09-24-notes.md): ERP/MES supplies it under plant business rules.

## Amendment note

**Scope reconciliation — 14 October 2026:** the earlier consequence illustrated
`setup → response → queue`. Its queue stage is historical following the working group's
October 1 exclusion in [ADR-000007](ADR-000007-queue-schema-retained-state-baseline.md)
and [ADR-000008](ADR-000008-delete-request.md). The current consequence above reflects that
existing exclusion; no communication-direction rule is changed. Horizontal traffic within
either zone need not use MQTT, as clarified by the maintainer during October finalization
and stated in Technical Guide § 2.4.

D-2609-06 as minuted reads: bidirectional is "**never** permitted north-south, i.e. between the
production level and the supervisory/cloud level". Read literally that outlaws the standard's
own setup write path (§ 4, ADR-000006, ADR-000007, ADR-000008). Maintainer corrections, 2026-09-08:

1. The axis is **IT/OT segmentation, not cloud**; the prohibition is on **direct** crossings.
   Brokered north-south via Level 3.5 is the normal, required path.
2. The zone split is stated explicitly as **OT = Levels 0–3, IT = Levels 4–5**. This follows
   from the existing name of Level 3.5 but was never written down.
3. The prohibition is **symmetric** — both IT→OT and OT→IT direct. The minute and the initial
   correction addressed IT→OT only.

All three published wider than the original minute. The focus group approved the IT/OT zone
split, brokered crossings via Level 3.5, and the prohibition on direct crossings in both
directions on **2026-09-24**, with cloud remaining optional. The maintainer confirmed this
outcome on 2026-09-29.


## Delivery and reconnection

**Maintainer confirmation, 2026-10-13:** retain the existing transport/retry baseline and
subscription-based recovery direction. This consolidates the existing guide rules and the
September 29 recovery clarification; it does not add a stronger persistence protocol.

QoS 1 is recommended generally; persistent sessions are enabled when required. A sender retries
a failed send up to three times after the original attempt, then logs and surfaces an
undeliverable message locally. Retries preserve the original event timestamp and assigned
message identity. Last Will has its explicit QoS 1 requirement under
[ADR-000022](ADR-000022-mqtt-last-will.md).

After reconnection, equipment resumes heartbeats and pending COS delivery. IT consumers restore
applicable subscriptions; connecting does not oblige them to publish equipment telemetry.
Recovery depends on the retained session, subscriptions, QoS and broker storage/expiry limits.
Re-subscribing cannot recover data that was never stored or has expired. MQTT acknowledgment
confirms transport delivery at the relevant hop, not setup acceptance or production completion.

No universal replay guarantee, full heartbeat history, fixed outage window, mandatory durable
outbox, storage technology or operator recovery workflow is prescribed. These stronger proposals
were not adopted. Setup request outcomes remain governed by
[ADR-000006](ADR-000006-response-setup-schema-approach.md).

## Authentication source correction — 14 October 2026

The maintainer checked §2.3.2 of the original Word document and confirmed that both
username/password and X.509 client certificates are permitted. Authentication is mandatory
over the required TLS transport; certificates are preferred for machines, not mandatory.
Anonymous access is prohibited.

This restores the original source meaning. The certificate-only checklist introduced during
Word-to-Markdown conversion was erroneous, not a competing accepted security requirement.
The source verification is the maintainer's; no independent inspection of the Word original
is claimed. Network boundaries and TLS requirements are unchanged.
