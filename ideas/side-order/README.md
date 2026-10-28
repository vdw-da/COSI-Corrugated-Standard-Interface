# Ideas — Side Order Modelling

**Status:** Resolved — variant **B2** approved by the working group on **2026-07-15** and
implemented in the corrugator schema. The maintainer confirmed closure on **2026-09-29**.
This folder preserves historical alternatives and sketches; it is not pending design work.
See [ADR-000004](../../adr/ADR-000004-side-order-modelling.md).

## Reference

Context for this proposal to be found in [ADR-000004 — Side order modelling](../../adr/ADR-000004-side-order-modelling.md).

## Files in this folder

### Option proposals

- [`01-option-A-separate-object.md`](01-option-A-separate-object.md) — dedicated `sideOrders` array with a lean schema.
- [`02-option-B-extended-orders.md`](02-option-B-extended-orders.md) — single `orders` array with an `orderType` flag and relaxed required fields.

### Supporting

- `fragments/` — JSON snippets per option for side-by-side comparison.
  - [`fragments/01-separate-side-order.json`](fragments/01-separate-side-order.json)
  - [`fragments/02-extended-orders-with-flag.json`](fragments/02-extended-orders-with-flag.json)
