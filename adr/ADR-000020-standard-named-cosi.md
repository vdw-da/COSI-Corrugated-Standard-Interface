# ADR-000020 — The standard is named COSI; schema identifiers use the `cosi:` prefix

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Maintainer, 2026-09-09
- **Ratified by:** Focus group, 2026-09-24 — [confirmed meeting record](2026-09-24-notes.md)
- **Source:** repository name `vdw-da/COSI-Corrugated-Standard-Interface`; maintainer instruction
- **Asset class:** — (standard-wide)

## Context

The repository carried three names for one thing: the git remote is
**COSI — Corrugated Standard Interface**, the README title was `vdw-transparent-data`, and every
document, schema title and schema `$id` said **VDW Transparent Data**. "Transparent Data" was the
name of the VDW initiative under which the work started; COSI is the name of the standard the
initiative produced.

v1.0 is the first public version. Schema `$id`s are permanent identifiers: once published, changing
one is a breaking change requiring a version bump. This is therefore the only moment at which the
identity can be corrected at no cost.

## Decision

- The standard is **COSI — Corrugated Standard Interface**. The short form **COSI** is used in
  document titles and running text; the full form appears on the README and the guide's cover.
- Schema identifiers drop the initiative name entirely: `vdw:transparent-data:<x>:1.0` becomes
  **`cosi:<x>:1.0`** — for example `cosi:envelope:1.0`, `cosi:setup-corrugator-payload:1.0`.
- **VDW remains the publishing association** and is unchanged wherever it names the organisation:
  the working group, the copyright holder, the contact. Renaming the standard does not rename its
  publisher.

## Consequences

- All ten schemas change `$id`, and every cross-schema `$ref` with them. Because `$ref`s resolve
  through the `$id`s, the two must move together — they did, and all nine examples validate.
- No consumer is affected: nothing public carried the old URNs.
- Anything referring to the old identifiers — a draft integration, a saved schema copy, a local
  tool — must be repointed. This is the last release at which that is free.
- [ADR-000016](ADR-000016-schema-corrections-to-documented-intent.md) stated that the decided `$id`
  scheme was unchanged. That is superseded here and an amendment note records it.

## Alternatives

- **`cosi:transparent-data:<x>:1.0`** — a literal prefix swap, keeping the initiative name as a
  middle segment. Rejected: it names two standards in one identifier and reproduces the
  two-names-for-one-thing problem in machine-readable form.
- **Rename the prose only, leave the URNs.** Rejected: the standard would ship called COSI while
  every schema identified itself as something else — and after publication the URNs are frozen.
