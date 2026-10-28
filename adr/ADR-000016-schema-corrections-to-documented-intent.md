# ADR-000016 — Six schema corrections enforcing already-documented intent

**Implementation checkpoint — 14 October 2026:** The dedicated Last Will-only null envelope timestamp exception in ADR-000022 is implemented; ordinary messages still require UTC Z timestamps. Earlier pending-alignment statements describe the prior recording stage. The aligned package was subsequently approved on 16 October 2026; see the [decision register](decision-register.md).

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Maintainer (editorial — preserves documented meaning rather than changing it)
- **Source:** findings #2, #6, #7, #8, #22, #44 (formerly register IDs ED-01 … ED-06)
- **Asset class:** — (multiple)

## Context

Six places where the **schema permitted what the documentation already forbade**. In each case the
prose in `docs/` or in the schema's own `description` stated a constraint that the schema did not
enforce, so a non-conformant message validated cleanly. These are collected in one record because
they share a single rationale; individually none of them is a design choice.

Correcting them is not a change of meaning — it is making the artifact say what it always claimed.
That is why they were taken without the working group, under C1's "mechanical consistency" rule.

## Decision

| # | Correction | Finding |
|---|---|---|
| 1 | Cross-schema `$ref`s changed from relative filenames to the URN `$id`s | #2 |
| 2 | `correlationID` conditionally required in the setup-response branch (named `response-setup` when applied; renamed by ADR-000006 on 2026-10-14) | #6 |
| 3 | Timestamps restricted to UTC `Z`, enforced by pattern; Last Will-only null exception subsequently decided in ADR-000022 (see amendment below) | #7 |
| 4 | Quality `exception` closed to `lower-violation` / `upper-violation` | #8 |
| 5 | `color` (flexo print) resolved to a free string with an open unit scheme (ARGB, Pantone, ERP reference) | #22 |
| 6 | Twelve setup fields with documented fixed units tightened to a `uom` `const` (`kN`, `g/m²`, `pcs`, `dpi`, `station`, FEFCO) | #44 |

## Consequences

- **#1 is the significant one:** the 0.9 draft schemas combined URN `$id`s with relative file
  `$ref`s, which is unresolvable per RFC 3986. Standard tooling — ajv included — could not validate
  them at all. The schemas ship validatable. The `$id` scheme itself was left alone here — see the
  amendment note below.
- #2, #3, #4 and #6 close gaps that previously let a non-conformant message validate: a non-UTC
  offset, a missing `correlationID`, a free-text `exception`, or a wrong `uom` now fail.
- #5 removes a contradiction rather than tightening anything — the description said "ARGB hex"
  while the type was a numeric quantity.
- All nine examples validate after the change.

## Amendment note — 2026-09-09

This record originally stated that the decided `$id` scheme was unchanged, which was true when it
was written. It no longer is: [ADR-000020](ADR-000020-standard-named-cosi.md) renames the standard
to **COSI** and replaces every identifier `vdw:transparent-data:<x>:1.0` with `cosi:<x>:1.0`.

The correction in this record — cross-schema `$ref`s resolving through the URN `$id`s rather than
through relative filenames — is unaffected. Only the URN strings changed; the mechanism did not.

## Amendment note — 2026-10-11: Last Will-only timestamp exception

Correction 3 remains the timestamp rule for every message **except the dedicated `lastwill`**.
The maintainer approved `timestamp: null` for that message only in
[ADR-000022](ADR-000022-mqtt-last-will.md#decision).
That ADR owns the exception: the future loss time is unavailable when the Will is prepared.
All other messages still require the UTC `Z` timestamp. The conditional schema enforcement was
applied in the coordinated implementation pass of 14 October 2026 (`schemas/envelope.schema.json`).
No other correction in this record is superseded.


## Field applicability clarification — 13 October 2026

**Confirmed by maintainer:** required fields remain required, optional measurements remain
optional, and null is permitted only where the particular field allows it. Zero is a reported
numerical zero, not a placeholder for unavailable data. Missing quality results do not mean OK.
Existing inactive-device conventions remain in force.

This clarification replaces the blanket instruction to omit only structurally unrelated fields
where that instruction conflicted with optional fields. It adds no sensor, metric, capability
discovery, field or general null permission. The schema's field-specific contract controls.
