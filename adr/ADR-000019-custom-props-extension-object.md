# ADR-000019 — `customProps` extension object on both setup payloads

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Working group, 2026-07-20
- **Source:** [2026-07-20 meeting notes](2026-07-20-notes.md) (minuted as M-0720-1)
- **Asset class:** `setup-corrugator`, `setup-converting`

## Context

Design principle § 1.2 promises **extensibility** — manufacturers may carry information beyond the
baseline — while standard operation must not depend on proprietary extensions. Without a named place
for vendor data, that promise is met either by inventing ad-hoc top-level fields, which collide
across vendors, or by forbidding extension outright, which contradicts the principle.

## Decision

A **`customProps`** object is available on both setup payloads for manufacturer- and site-specific
properties. It is defined once as `CustomProps` in `common-types.schema.json` and referenced at both
payload roots and on corrugator orders.

Its content is **not standardized by this specification**, and **consumers must ignore unknown
keys**.

## Consequences

- Vendor extensions have one predictable location instead of appearing as unrecognised top-level
  fields, so `additionalProperties: false` can stay strict everywhere else.
- A consumer that ignores `customProps` entirely remains fully conformant — this is what keeps
  standard operation independent of proprietary extensions.
- Nothing inside `customProps` can be relied on for interoperability, by construction. Anything that
  *should* be interoperable belongs in the standard, not in here.
