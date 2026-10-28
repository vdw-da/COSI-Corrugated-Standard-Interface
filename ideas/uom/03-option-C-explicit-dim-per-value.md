# Option C — Explicit `dim` per value

## Idea in one line

Every measurement carries its dimension explicitly alongside `value` and `uom`. Self-describing to a fault.

## What the payload looks like

```json
"speed":  { "dim": "speed_length",   "value": 182,  "uom": "m/min" }
"water":  { "dim": "volume",         "value": 1.24, "uom": "m3"    }
"weight": { "dim": "mass",           "value": 3.85, "uom": "t"     }
```

## Why someone would propose this

- A consumer that has never seen the schema can still understand the message — pure self-description.
- Generic ETL / pipeline code can route values by dimension without a field-name table.
- Plays well with QUDT-style downstream tooling (`dim` → `qudt:QuantityKind`).

## Why it's wrong for us

- **Payload bloat is significant.** A performance HBT today has ~15 measurement objects. Adding `"dim": "..."` to each adds 15–25 bytes per measurement × every 5-second HBT × every machine. Over a year that's tens of MB per machine of redundant constant data.
- **Redundant with field name.** `weight` is always `mass`. `water` is always `volume`. Forcing the producer to send `"dim": "mass"` next to a field literally called `weight` is asking for typos and divergence.
- **Doesn't actually buy validation that [Option B](02-option-B-schema-bound-dimension.md) doesn't give for free.** The schema knows `weight` is mass; sending `dim` doesn't change that.
- **Two sources of truth.** What happens when payload says `"dim": "mass"` but the schema says it's `"length"`? Now we need a tie-breaker rule.

## When this *would* be the right answer

Only if measurements were **dynamically named** — e.g., a generic `sensors: [{name, value, uom, dim}]` array where the consumer truly doesn't know what each entry is. Our schema is field-named (`weight`, `water`, `speed`), so dimension is already implied by name.

## Tepid endorsement only for the dimensionless-explicit case

There's one narrow place where explicit `dim` helps: **dimensionless values** like `pcs`, `stacks`, `dE2000`, `dpi`. These have no traditional dimension, so a small explicit annotation prevents confusion. But this can be solved with [Option B](02-option-B-schema-bound-dimension.md)'s `Count` / `Ratio` / `Dimensionless` enums without putting anything in the payload.

## Verdict

Rejected as a default approach. Included here for completeness so the team can see why we're not going this way.

See JSON fragment: [`fragments/03-explicit-dim-style.json`](fragments/03-explicit-dim-style.json).
