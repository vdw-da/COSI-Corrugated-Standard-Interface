# 06 — Recommendation & tradeoff matrix

## Tradeoff matrix

| Option | Payload cost | Validation power | Imperial support | OPC UA interop | Implementation cost |
|---|:---:|:---:|:---:|:---:|:---:|
| **A** Envelope `unitSystem` | +1 field/msg (~20 bytes) | none | flag only | n/a | tiny |
| **B** Schema-bound dimension | 0 | strong | per-dimension enum | n/a | medium (refactor schemas) |
| **C** Explicit `dim` per value | +1 field per measurement (~15 bytes × N) | strong but duplicative | implicit | n/a | medium |
| **D** UN/CEFACT codes in payload | 0 (sometimes smaller) | weak | yes | strong | high (translate everything) |
| **D-v** UN/CEFACT as schema annotation | 0 | unchanged | unchanged | strong | small |
| **E** External unit catalog | 0 | strong (via B) | yes | (with D-v) yes | medium (one new file + ref refactor) |

## Recommended combination: **A + B + E + D-variant**

In plain English:

1. **Envelope gains an optional `unitSystem` field.** Default `metric`. If absent → metric is assumed. Set to `imperial` to assert the whole payload is imperial. *(from Option A)*

2. **A new `schemas/_dimensions.schema.json`** owns one `$defs` per dimension, with each dimension's full uom enum (metric + imperial). *(from Option E)*

3. **Each asset-class schema replaces its `"uom": {"const": "…"}` pins with `{"$ref": "_dimensions.schema.json#/$defs/Volume"}` etc.** Dimension is now schema-checked. *(from Option B)*

4. **Each dimension definition carries an `x-uncefact` annotation** mapping each symbol to its Rec 20 code. Non-validating, but lets OPC UA-adjacent consumers round-trip. *(from Option D-variant)*

5. **`docs/units.md` becomes the canonical owner** of the dimension table — symbol, system (metric/imperial), Rec 20 code, SI conversion factor. NC §6 shrinks to a one-paragraph pointer (consistent with the existing docs-ownership-model). *(from Option E)*

6. **Payload shape and existing examples remain unchanged.** Per-value `uom` is still authoritative — the envelope flag is hint + default; the schema enforces the dimension; the catalog documents conversion.

## Why this combination

- **A alone** answers the metric/imperial framing but not the "seconds on a width field" framing.
- **B alone** answers the dimension framing but doesn't give a producer a single high-level switch.
- **A + B** answers both with minimal payload impact (~20 bytes per envelope, zero per measurement).
- **E** is implementation hygiene — without it, B's dimension list ends up duplicated across six asset-class schemas.
- **D-variant** is cheap insurance for the OPC UA crowd.

## Estimated payload impact

A 5-second performance HBT today: ~750 bytes JSON.
- After A: +20 bytes when `unitSystem: "imperial"` is present, 0 bytes otherwise.
- After B/E/D-v: 0 bytes.

Trivial.

## What would change in the existing files (informational — not doing it now)

| File | Change |
|---|---|
| `schemas/envelope.schema.json` | Add optional `unitSystem` property |
| `schemas/_dimensions.schema.json` | **New file** — dimension `$defs` |
| `schemas/performance.schema.json` | Replace 5× `"const": "<unit>"` with `$ref` to dimensions |
| `schemas/quality.schema.json` | Same pattern |
| `schemas/setup-corrugator.schema.json` | Same pattern |
| `schemas/setup-converting.schema.json` | Same pattern |
| `schemas/maintenance-*.schema.json` | Same pattern |
| `docs/units.md` | **New file** — canonical dimension table |
| `docs/naming-conventions.md` §6 | Shrink to pointer to `docs/units.md` |
| `docs/message-properties.md` | Add `unitSystem` envelope row |
| `docs/technical-guide.md` | One paragraph on dimension binding & metric default |
| `examples/**/*.json` | No changes needed (still metric, still self-describing) |
| Add 1 example showing `unitSystem: "imperial"` | optional but recommended |

## Open decisions you still need to make

1. **`unitSystem` mandatory or optional?** I lean optional with `metric` as default. Confirm.
2. **Allow `"mixed"` as a value?** I'd say no — `uom` per value is already authoritative.
3. **Do we cross-validate** (envelope `imperial` ⇒ all uoms must be from imperial subset)? I'd say no — adds schema complexity for a check that consumers can do themselves if they care.
4. **Where do `pcs`, `stacks`, `dpi`, `dE2000`, `%RH` live in the dimension catalog?** I've proposed `Count`, `PrintResolution`, `ColourDistance`, `Humidity` as standalone dimensions. Some teams collapse all of these into `Dimensionless`. Pick one philosophy.
5. **`Speed` is two dimensions** in the corrugated world (`LengthPerTime` for corrugator m/min, `CountPerTime` for converting pcs/h). Either:
   - keep one `speed` field and let its uom enum span both (current behaviour, but uom enum mixes dimensions — purist would object), or
   - split into `lineSpeed` (length/time) and `throughput` (count/time). Cleaner but a breaking change.
6. **Conversion factors in `docs/units.md`** — include them as informative for consumers, or stay out of the conversion business entirely? Including them is helpful but creates a maintenance surface and a precision/rounding policy question.
7. **`docs/units.md` ownership** — should it become the fourth core doc (alongside TG, MP, NC) in the ownership model?

## Where I'd push back on the team's framing

> "*the unit-system should be part of each message ... overwrite with imperial, then this needs to become part of the envelope*"

Agree — envelope. But the envelope flag *alone* won't reject `"uom": "s"` on a width. The team's "physical domain" idea is a separate concept and needs to live in the schema (or catalog), not in the envelope. The two solutions complement each other; they don't replace each other.

> "*detailed enough, but at the same time not blowing up the payload too much*"

The cheapest solutions push complexity into the schema and out of the payload. Option C does the opposite — putting `dim` next to every value. I'd reject C for that reason alone.
