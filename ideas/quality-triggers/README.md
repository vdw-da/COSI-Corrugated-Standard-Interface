# Configurable quality triggers — future idea

**Status:** outside v1.0; scope confirmed by the maintainer on 2026-09-29.
**Sources:** [ADR-000001](../../adr/ADR-000001-quality-message-end-of-job-mandatory.md)
with the maintainer’s scope confirmation of 2026-09-29 recorded there.

For v1.0, a quality message at the end of each job is mandatory. Additional in-process quality
messages are optional and use the existing quality payload and `cos` trigger.

A standardized vocabulary and configuration mechanism for in-process triggers and intervals
are future work. Earlier examples include flute changes, roll changes, every specified number
of pallets or sheets, and downtime exceeding a configured duration. These are ideas, not
mandatory reporting triggers or approved field definitions.

No future release date or protocol is committed. The existing end-of-job reporting obligation
and optional in-process messages remain in scope.
