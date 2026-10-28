# Decisions recorded — 2026-05-27 Q&A

Captured verbatim from a 7-question walk-through. These are working decisions to take to the team; nothing in `schemas/`, `examples/`, or `docs/` has been changed.

| # | Question | Decision | Implication |
|---|---|---|---|
| 1 | Mixed unit systems in one message? | **No — one system per machine.** | The envelope is the right place for a `unitSystem` flag (rather than per-field). |
| 2 | Metric-only on wire, or support both natively? | **Fork the proposal — produce both designs.** | See [`forks/metric-only-on-wire.md`](forks/metric-only-on-wire.md) and [`forks/support-both-on-wire.md`](forks/support-both-on-wire.md). |
| 3 | Consumers parse uom or just display? | **Both happen / not sure.** | Keep ISO 80000 symbols on the wire **and** add UN/CEFACT codes as schema-side `x-uncefact` annotation. Display-only consumers ignore it; parsing consumers use it. |
| 4 | OPC UA upstream relevance? | **VDW is the lingua franca; a translation/transformation layer sits in front of each producer and consumer.** | The `x-uncefact` annotation is most valuable *to those translation services* — they can map VDW ↔ OPC UA (and other standards) without their own lookup tables. Include the annotation. |
| 5 | Odd quantities (pcs, stacks, dE2000, dpi, %RH, viscosity)? | **Each gets its own named dimension.** stacks/rolls/pcs are quantities (`Count`, or possibly renamed `Quantity`). | Catalog grows to ~16 dimensions but validation is strict — `dpi` on a temperature field is rejected, `dE2000` on a count field is rejected. |
| 6 | `speed` field shared between corrugator (length/time) and converting (count/time)? | **Polymorphic by assetClass.** Keep one `speed` field; bind it to `LengthPerTime` in corrugator schemas and to `CountPerTime` in converting schemas. | Non-breaking to current producers; each schema cleanly binds to one dimension. |
| 7 | `docs/units.md` as fourth core owner doc? | **Yes in principle — but prepare in `ideas/uom/` only.** Team discussion and approval required before any change touches `docs/`, `schemas/`, `examples/`. | This file and everything next to it stay inside `ideas/uom/`. |

## What is now settled (subject to team approval)

- Envelope-level `unitSystem` is the right shape **if** we support imperial natively (Decision 1).
- Per-value `uom` stays authoritative; no `dim` field per value (rejected via Decision 5 + the original Option C analysis).
- Dimension binding lives in the schema, not the payload.
- A new `_dimensions.schema.json` is the source of truth; `x-uncefact` annotations sit alongside.
- `speed` is polymorphic by asset class.
- Each "odd" quantity earns its own dimension.

## What is still forked

- Whether imperial is supported on the wire at all. Decision 2 was "produce both designs." Once the team picks one, the other fork can be deleted.

## What is *not* yet decided

- Conversion factors in the catalog — include as informative (`x-toSI`) or skip? (See [`forks/support-both-on-wire.md`](forks/support-both-on-wire.md) for the trade-off.)
- Whether `Count` should be renamed to `Quantity` to align with the user's wording in Decision 5. (Cosmetic; can be settled at review.)
- Whether `unitSystem` should also be optional in the **metric-only** fork (e.g., as `"metric"` const) so a future imperial extension wouldn't be breaking — see metric-only fork.
