# ADR-000015 — `faultCode` is constrained to the closed 40-code enum

- **Status:** Accepted (ratified by the focus group 2026-09-24)
- **Date:** 2026-09-09
- **Decided by:** Focus group, 2026-09-07; amended by the maintainer, 2026-09-08
- **Ratified by:** Focus group, 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-07 (finding #18)
- **Asset class:** `maintenance-measurement`

## Context

`faultCode` was a free string, although its own description and `docs/corrugated-faults.md` define a
closed three-letter table. Any value validated, including lower-case or invented codes.

## Decision

`faultCode` carries the **explicit `enum` of the 40 published codes plus `null`**, generated from
the fault table and round-trip verified against it. Vendors may optionally publish `internalCode`
as a free vendor string; it may be omitted or null. Every new entry in the `faultCode` list
requires a new version of the standard.

## Consequences

- Codes outside the table are rejected: `XYZ` and `vib` do not validate. `VIB`, `OTH` (not
  classifiable), `UNK` (cause unclear) and `null` are valid.
- The ISO citation is editioned as **ISO 14224:2016, Annex B** across all doc surfaces.

## Amendment note

D-2609-07 minutes the constraint as the pattern `^[A-Z]{3}$`. The maintainer shipped a closed
`enum` instead, which is **stricter** than minuted: a pattern accepts any three capitals. The
grounds are that the code table is fixed for v1.0 — no additions before a version change — and
`docs/naming-conventions.md` § 10 requires a closed value set to be expressed as `"enum": [...]`.

**On normative status:** in the ISO 14224 *first edition (1999)* the foreword states that annexes
A–D are "for information only" — a recommended taxonomy, not a normative constraint. The 2016
edition was not available to verify (paid document), so the published wording claims only the
edition and annex, never normative status. The closedness of the VDW list is **VDW's own decision**.

The focus group approved the closed enum, optional `internalCode`, and a new standard version
for every added code on **2026-09-24**, as confirmed by the maintainer on 2026-09-29.
During verification on 2026-09-29, `internalCode` was found in the schema's
`required` list despite the fault-code document describing it as optional. It was removed
from `required` to match the approved decision.
