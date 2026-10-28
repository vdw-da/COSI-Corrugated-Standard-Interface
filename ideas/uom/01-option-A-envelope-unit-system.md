# Option A — Envelope-level `unitSystem`

## Idea in one line

Add an optional `unitSystem` field on the envelope. Default = `metric`. If omitted, consumer assumes metric. To send imperial, set `"unitSystem": "imperial"` and the whole payload's units shift.

## Envelope addition

```json
"unitSystem": {
  "type": "string",
  "enum": ["metric", "imperial"],
  "default": "metric",
  "description": "Unit system for all measurements in payload. Omit to default to metric."
}
```

## How payload changes

It doesn't, much. Per-value `uom` is still declared (NC §6 stays). The envelope flag is just a sanity assertion + a default for any consumer that *would* want to omit `uom` later.

```json
{
  "messageID":   "...",
  "assetClass":  "performance",
  "messageType": "hbt",
  "machineId":   "CORR-LINE-01",
  "timestamp":   "2026-05-04T06:30:00.000Z",
  "status":      "run",
  "unitSystem":  "imperial",
  "payload": {
    "speed":  { "uom": "ft/min", "current": 600, "target": 660 }
  }
}
```

## What the schema does

Each measurement field's `uom` enum lists **both** the metric and imperial symbols valid for its dimension. Validation passes either way. The envelope flag is a hint to the consumer; cross-validation ("if envelope says imperial then uom must be imperial") is optional and probably not worth the schema complexity.

```jsonc
// inside speed (corrugator):
"uom": { "type": "string", "enum": ["m/min", "ft/min"] }
```

## Pros

- **Tiny payload impact** — one envelope field, only present on non-metric machines.
- **Backward compatible** — current metric messages remain valid (omit = metric).
- **Matches how factories actually segment** — units are a regional/site property, not a per-message decision.
- **Operator-readable** — a single field tells you what world the rest of the JSON lives in.

## Cons

- **Does not solve dimension validation** on its own. A producer can still put `"uom": "s"` on a width field. This option needs to be combined with B or E.
- **Mixed units in one message become awkward.** If we ever need them (e.g., metric speed + imperial pressure on the same machine), the flag is misleading.
- **Asks consumers to do conversion** — same as today, but now they're prompted by the flag to do it deliberately.

## Variant: `unitSystem: "mixed"`

Allow `mixed` as a third value, signalling "per-field uom is authoritative, do not assume a region." This rescues the rare mixed-unit case at the cost of one more enum value.

```jsonc
"unitSystem": { "enum": ["metric", "imperial", "mixed"], "default": "metric" }
```

I'd lean toward **not** adding `mixed` — `uom` is always present per-value, so a consumer can already handle mixed by ignoring the envelope flag. Keep the enum at two.

## When this is the right answer

If we believe (and we should ask the team) that a single machine site emits one unit system consistently, this is enough. The dimension validation is a separate concern handled by B or E.

See JSON fragment: [`fragments/01-envelope-with-unitsystem.json`](fragments/01-envelope-with-unitsystem.json).
