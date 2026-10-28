# ADR-000024 — Maintenance document and observation scope

- **Status:** Accepted by maintainer; payloads approved by André Seifert, 2026-10-16
- **Date:** 2026-10-14
- **Decided by:** Maintainer, 2026-10-14
- **Source:** Maintainer confirmation to retain existing maintenance messages and local document availability, and defer the automatic document-update service; Technical Guide §§2.6 and former 5.8 (current observation guidance in §5.6 after the maintainer-approved editorial consolidation, 2026-10-16)
- **Asset class:** `maintenance-document`, `maintenance-measurement`

## Context

The guide described a document-update service as both future work and already defined.
The existing messages provide document references, component information and service tasks;
they do not define an automatic synchronization service.

## Decision

Retain the existing maintenance-document/task messages and local document availability.
An automatic document-update service belongs to a future revision. The proposed startup,
change-notification, new-consumer acquisition and full-list replacement protocol is not part
of v1.0. No particular local file-store design is prescribed.

Maintenance measurements report observations at their envelope event time, with the existing
value, limits and fault classification. They do not define a fault-occurrence open/update/clear
protocol; an older observation does not establish current fault clearance.

Document references do not override the network boundary in
[ADR-000010](ADR-000010-bidirectional-east-west-only.md). Local access and permitted IT/OT
crossings apply without adding a new file-transfer protocol or stronger recovery guarantee.
Fault codes remain governed by [ADR-000015](ADR-000015-faultcode-closed-enum.md).

## Consequences and provenance

The October 14 maintainer confirmation resolves the guide's service-description conflict.
The observation and network-boundary statements restate the existing fields and communication
rules; they are not additional maintainer decisions creating a lifecycle or transfer service.
Existing fields remain available, while implementations choose document management within the
stated access requirements. André Seifert approved both maintenance payloads with the aligned package on 16 October 2026.
