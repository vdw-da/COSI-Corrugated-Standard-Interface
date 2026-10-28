# Ideas — Unit System & Physical Domain

**Current disposition — 14 October 2026:** The October 1 working group retained metric-only v1.0 and deferred imperial support to v1.1 (ADR-000013). The older October 1 discussion invitation below is historical, not a pending v1.0 decision.

**Status:** Brainstorm only. Nothing in `schemas/` or `examples/` is touched. This folder is a scratchpad for the team discussion.

> **v1.0 decision (D-2609-04, focus group 2026-09-07):** v1.0 is **metric only**, written as a
> rule in `docs/naming-conventions.md` § 6. Imperial support is **booked as an idea for 1.x** —
> this folder is that idea. For whoever picks it up: the imperial counterpart of `g/m²` is
> **`lb/MSF`** (pounds per thousand square feet). `MSF` alone is *thousand square feet*, an area
> unit, and is dimensionally wrong as a basis weight. The maintainer approved `lb/MSF` on
> **2026-09-29**; see [ADR-000012](../../adr/ADR-000012-grammage-named-gsm.md).
> The October 1 working group retained metric-only v1.0 and deferred imperial support to v1.1
> under [ADR-000013](../../adr/ADR-000013-metric-only-for-v1.md). The
> [scope assessment](2026-10-01-assessment.md) is historical preparation.
> Older drafts below are design inputs; their proposals are not current v1.0 policy.

## What we're trying to solve

Two requests from the team feedback:

1. **Imperial / metric coexistence.** Today the standard implicitly assumes metric (NC §6 lists metric symbols only; `performance.schema.json` even pins specific symbols via `"const": "m3"`, `"const": "Wh"`, `"const": "kg"`). A North-American line emitting `ft/min`, `BTU`, `lb`, `°F` cannot satisfy the current schemas.
2. **Physical domain (a.k.a. *quantity kind* / *dimension*).** Today nothing prevents a producer from sending `"uom": "s"` on a width field, or `"uom": "m/min"` on a temperature. We want the schema (or a validator) to know that *width* belongs to dimension *length* and therefore only `mm`, `cm`, `m`, `in`, `ft` are admissible.

These two are linked: once we know the dimension of a field, the legal uom set follows — including its metric/imperial members.

## The design tension

| | Smaller payload | Self-describing | Validatable |
|---|:---:|:---:|:---:|
| Drop `uom`, infer from field | ✓✓ | ✗ | ✗ |
| Current (`uom` per value) | ✓ | ✓ (partial) | ✗ (no dimension check) |
| Add `dim` per value | ✗ | ✓✓ | ✓ |
| Dimension in schema, not payload | ✓ | ✓ (partial) | ✓ |
| Envelope `unitSystem` switch | ✓ | ✓ | partial |

The cheapest payload puts dimension knowledge in the **schema** (consumer-side), not in every message. The cost is that the schema must enumerate the legal uom set per field — but that's a one-time cost we already partly pay (see the `const` usages).

## Files in this folder

### Conceptual options (first pass, 2026-05-27)

- [`00-industry-standards.md`](00-industry-standards.md) — what UCUM, UN/CEFACT, QUDT, OPC UA, ISO 80000 actually do and whether any of them belong in this standard.
- [`01-option-A-envelope-unit-system.md`](01-option-A-envelope-unit-system.md) — single switch on the envelope, default metric.
- [`02-option-B-schema-bound-dimension.md`](02-option-B-schema-bound-dimension.md) — dimension lives in the JSON Schema; payload unchanged.
- [`03-option-C-explicit-dim-per-value.md`](03-option-C-explicit-dim-per-value.md) — `dim` field alongside every `value`/`uom` (rejected; included for completeness).
- [`04-option-D-uncefact-codes.md`](04-option-D-uncefact-codes.md) — UN/CEFACT common codes (rejected in payload; accepted as schema annotation).
- [`05-option-E-unit-catalog.md`](05-option-E-unit-catalog.md) — external dimension→uom registry (`docs/units.md`), referenced from schemas via `$defs`.
- [`06-recommendation.md`](06-recommendation.md) — my recommended hybrid, tradeoff matrix.

### After the 2026-05-27 Q&A

- [`decisions-recorded.md`](decisions-recorded.md) — verbatim record of the 7 decisions taken.
- [`forks/metric-only-on-wire.md`](forks/metric-only-on-wire.md) — full design for the simpler path (standard stays SI; producers convert at the edge).
- [`forks/support-both-on-wire.md`](forks/support-both-on-wire.md) — full design for native imperial + metric on the wire.
- [`draft-units-doc.md`](draft-units-doc.md) — what `docs/units.md` would look like (both fork variants drafted side-by-side).

### Supporting

- `fragments/` — JSON snippets per option so they can be compared side-by-side.

## Status of the original 7 grill questions

| # | Question | Status | Outcome |
|---|---|---|---|
| 1 | Mixed units in one message? | ✅ resolved | One system per machine. Envelope-level flag is correct shape. |
| 2 | Consumers parse or display `uom`? | ✅ resolved | Both happen → keep ISO symbols + add `x-uncefact` schema annotation. |
| 3 | OPC UA upstream relevance? | ✅ resolved | A translation layer sits in front of every producer/consumer; the `x-uncefact` annotation is for *that* layer's benefit. |
| 4 | Metric-only on wire vs support both? | 🔀 **forked** | Both designs are written up — team decision required. See `forks/`. |
| 5 | Dimensionless / odd quantities? | ✅ resolved | Each gets its own dimension. `pcs`/`stacks`/`rolls` are `Quantity`. |
| 6 | `speed` field — length/time or count/time? | ✅ resolved | Polymorphic by `assetClass`. Same field name; corrugator binds to `LengthPerTime`, converting binds to `CountPerTime`. |
| 7 | Promote `docs/units.md` to fourth core doc? | ✅ in-principle yes, but draft-only in `ideas/uom/` until team approval. |

## Next step for the team

1. Read [`decisions-recorded.md`](decisions-recorded.md) — what's already settled.
2. Pick a fork: [`forks/metric-only-on-wire.md`](forks/metric-only-on-wire.md) vs [`forks/support-both-on-wire.md`](forks/support-both-on-wire.md).
3. Confirm the four secondary items still flagged "Open" inside the chosen fork.
4. After approval: promote draft artifacts (`draft-units-doc.md`, the `_dimensions.schema.json` shown inline in the forks) out of `ideas/uom/` into `docs/` and `schemas/`.
