# ADR-000017 — Unit symbol and terminology corrections for v1.0

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Focus group, 2026-09-07
- **Source:** [2026-09-07 notes](2026-09-07-notes.md) D-2609-07 (findings #17, #34)
- **Asset class:** `performance` (#17); glossary only (#34)

## Context

Two unit notations disagreed with the standard's own rules. They are collected in one record
because neither carries a design question a future reader would ask "why?" about — the answer in
both cases is "because the referenced standard says so".

The third item minuted alongside these, `faultCode`, is **not** here: it changed what validates and
has its own record, [ADR-000015](ADR-000015-faultcode-closed-enum.md).

## Decision

- **Volume is written `m³`**, per ISO, replacing plain `m3` — performance water and air, and the
  preferred-units table.
- **`kicks/h` is dropped** from the glossary in favour of **`pcs/h`**.

## Consequences

- `m³` is the wire value; the literal `m3` appears in no schema and no example.
- `kicks/h` was an orphan — present in no schema and in no example — so removing it changes no
  message. It was glossary-only debris.
