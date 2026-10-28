# ADR-000004 — Side order modelling: separate object vs. extended orders array

- **Status:** Accepted for B2 (2026-07-15)
- **Date:** 2026-06-18
- **Decided by:** Breakout session 2026-06-18; variant B2 accepted by the working group 2026-07-15
- **Source:** [2026-06-18 breakout session notes](2026-06-18-notes.md), [ideas/side-order/](../ideas/side-order/README.md)
- **Asset class:** `setup-corrugator`

## Context

There are 2 possible sources where we want a simplified order aside of the production order:

- **Excessive high trim** — The trim exceeds a set maximum and needs to be sent down the line for waste (exceeding maximum suction trim).
- **Side order** — Sheets produced when the layour of orders leaves a lot of room on the web width, for reselling or internal usage (non-waste)

Both cases require the setup message to add this information to the setup, including width, length, and downstream handling (cutoff knife).

The current `orders` array describes full production orders with full details. A side order can/should be simpler: no scoring, no preprint, etc.
However there is an overlap and it could be seen as a reduced order.
As such 2 plausbile variants/solutions were identified:

- **Option A** — a separate `sideOrders` array with a lean dedicated schema.
- **Option B** — keep one `orders` array, add an `orderType` enum, relax required fields.

Full proposal with JSON fragments can be found in [`ideas/side-order/`](../ideas/side-order/README.md).

## Decision

### Feedback 14/07/2026:
(Fosber) option B is preferred 
(Mitsubishi) option B get support 
(BHS) option A is the simplest/preferred but B***2*** also works with drawback: B2 adds complexer validation but could be harder with some code generators/implementation. The simplest B1 approach leaves too much risk so not preferred.

### conclusion

Though there is a risk of compatibility with generator, option B seems to be more broader preferred and the standard likes to abstract implemenation.
So going for B2.

## Tradeoffs

| Criterion | Option A (separate) | Option B (extending existing) |
|-----------|:---:|:---:|
| Validation strictness | ✓✓ | ✓ (with `if`/`then`) |
| No fake/placeholder data | ✓✓ | ✗ (depending on implementation) |
| Schema readability | ✓ | ✗ (conditional logic) |
| Domain clarity | ✓✓ | ✓ |


## Consequences (applied)

- `schemas/setup-corrugator.schema.json` carries `orderType` and conditional requirements for
  production versus side/waste orders within one `orders` array (B2).
- `examples/setup/setup-corrugator.json` uses the accepted `orders` structure and `orderType`.
- `ideas/side-order/` preserves the alternatives as historical material. The maintainer confirmed
  the maintainer confirmed on 2026-09-29 that the existing B2 approval resolves it.
