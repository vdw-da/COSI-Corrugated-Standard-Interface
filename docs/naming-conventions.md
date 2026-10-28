# COSI — Naming Convention

**Version:** 1.0 (prepublication)\
**Publication date:** 2026-11-01\
**Scope:** All JSON field names across envelope, payload, and schema definitions

---

## 1. Case Style

All JSON field names use **camelCase**.

```
machineId       ✓
machine_id      ✗
MachineId       ✗
```

---

## 2. Language

All field names are **English**. Domain terms originating from German or other languages must be translated to their English equivalent before use as a field name.

---

## 3. Abbreviations

Avoid abbreviations unless the abbreviated form is the universally recognised standard in the corrugated manufacturing or industrial automation domain.

**Permitted abbreviations:**

| Abbreviation | Meaning |
|---|---|
| `uom` | Unit of measure |
| `hbt` | Heartbeat |
| `cos` | Change of status |
| `lm` | Linear metres |
| `pH` | Potential of hydrogen |
| `dE2000` | Delta E 2000 colour difference |
| `OEE` | Overall Equipment Effectiveness |
| `FSC` | Forest Stewardship Council certification |
| `gsm` | Grams per square metre — paper grammage |
| `ID` | Identifier — envelope-level only (see §4) |

---

## 4. Identifier Suffixes

### `ID` — Envelope-level globally unique identifiers

Reserved for the two envelope fields that carry globally unique message identifiers:

```json
"messageID":     "uuid",
"correlationID": "uuid"
```

### `Id` — Other identifiers

All other identifier fields use lowercase `Id`:

```json
"machineId", "colorId", "statusId", "streamId", "schemaId", "connectionId"
```

`connectionId` is globally unique despite its `Id` spelling; only the two established message identifiers use `ID`. See [Message Properties](message-properties.md).

### `Ref` — Cross-system references

Fields that reference an entity managed in an external system (ERP, MES, machine) use the `Ref` suffix. Their requiredness and permission to use null are field-specific; follow the payload schema.

| Field | Meaning |
|---|---|
| `jobRef` | Manufacturing order reference |
| `articleRef` | Article / product specification reference |
| `taskRef` | Manufacturing step reference within the order |
| `setupRef` | Corrugator quality reference to setupSettings.setupId within the same site/machine context |

---

## 5. Boolean Fields

Boolean fields use a descriptive adjective. The `is*` prefix is not used.

```
active          ✓
crossFlute      ✓
autoStopFeed    ✓
isActive        ✗
```

---

## 6. Units of Measure

### Field name

The unit of measure field is always named **`uom`**. The name `unit` is not used — it is ambiguous with production unit, pallet unit, and similar domain concepts.

### Per-value declaration

Every field that carries a measured quantity includes its own `uom`. There is no global unit declaration at the message or envelope level. Messages are self-describing.

### Unit system

**v1.0 is metric only.** Use the unit symbols and field-specific tokens defined by the
schemas and this document. Existing tokens such as `pcs`, `stacks`, `cuts`, `cycles`, `dpi`,
`station`, `FEFCO` and `dE2000` retain their specified uses; not every token is an SI unit symbol.
Imperial measurement alternatives (`in`, `ft/min`, `°F`, `BTU`, `psi`, …) are **not** valid in
v1.0 — producers convert those measurements to metric before publishing. General imperial-unit
support is deferred to v1.1. See [ADR-000013](../adr/ADR-000013-metric-only-for-v1.md) and the
existing fixed-token corrections in [ADR-000016](../adr/ADR-000016-schema-corrections-to-documented-intent.md).

### Numeric precision

Numeric precision follows the data type. Producers send the precision their source data type
provides; consumers must not assume a fixed number of decimal places. COSI imposes no additional
precision restrictions or limits.

### Preferred `uom` values

| Quantity | `uom` value |
|---|---|
| Length | `mm` or `m` |
| Area | `m²` |
| Weight | `t` (metric tonne) |
| Grammage (`gsm`) | `g/m²` |
| Speed — converting | `pcs/h` |
| Speed — corrugator | `m/min` |
| Temperature | `°C` |
| Humidity | `%RH` |
| Energy | `Wh` |
| Steam | `kg` |
| Water / Air volume | `m³` |
| Colour accuracy | `dE2000` |
| Ink viscosity | `s` (seconds, Ford cup) |
| Force / Pressure | `kN` |
| Print resolution | `dpi` |

---

## 7. Quality Check Shape

Quality checks use the common structure described in
[Message Properties — Quality Check Shape](message-properties.md#quality-check-shape).
Field naming, enum casing and null handling follow the conventions in this document.

---

## 8. Enum Casing Rules

The default enum style is **lowercase**, using **hyphens** for multi-word values. Preserve the
exact case of values defined for a particular field.

**Existing exceptions:** check/setup-response results use `OK` / `NOK`; failure-mode codes use
the uppercase values in the fault-code table (ADR-000015). Unit symbols and classification
tokens retain their defined spelling (for example `Wh`, `g/m²`, `FEFCO`). Suggested values for
open enums retain their documented spelling; § 10 does not restrict them to a closed list.

For the full value lists and descriptions, see [`message-properties.md`](message-properties.md).

---

## 9. Arrays vs Objects

| Use | When |
|---|---|
| **Array** | Variable-length, positional, or repeating items (stream items, colours, periphery devices) |
| **Object** | Named, fixed sets of fields (quality check sections, machine settings groups) |

---

## 10. Open vs Closed Enumerations

Some fields have a defined set of known values but must remain extensible to allow industry-specific or future additions without breaking validation.

| Type | When to use | Schema implementation |
|---|---|---|
| **Closed enum** | The value set is complete and fixed by the standard (e.g., machine status values, check result OK/NOK, failure severity, failure mode code) | `"enum": [...]` — validation rejects unknown values |
| **Open enum** | The value set has well-known suggestions but producers may send additional values (e.g., FSC certification level, glue style, discharge direction) | `"type": "string"` with suggested values listed in `description` — validation accepts any string |

Suggested values for open enums must be documented in the schema `description` field, not enforced via `enum`.

---

## 11. Null vs Absent

- Required fields remain required. Use `null` only where that specific field permits it.
- Optional unavailable or inapplicable measurements may be omitted where appropriate.
- Zero is a reported zero, not a substitute for an unavailable value.
- Preserve the specified inactive-device conventions (for example zero positions for unused scoring knives).
- An empty or absent set of quality checks does not mean the material is OK.

---

## 12. Qualified Value Groups

Measurements that carry multiple temporal or contextual variants of the same physical value are represented as a **grouped object**. The group name is the measurement concept; the qualifier is the key within the group; `uom` is declared once at the group level.

The vocabulary below explains qualifier names; it does not authorize all qualifiers in every
payload or determine message triggers. Each schema defines the permitted fields, requiredness
and null values. Setup carries settings, not production actuals.

### Qualifier Vocabulary

| Qualifier | Meaning | Typical message type |
|---|---|---|
| `target` | Reference or goal value — best practice or job-specific aim | HBT, COS |
| `scheduled` | Value committed in the production plan (from ERP / MES) | COS |
| `actual` | Final measured or achieved value for a completed period | COS |
| `current` | Reading at the original event/observation time | HBT |
| `average` | Computed mean over the reporting period | HBT, COS |
| `minimum` | Minimum value reached over the reporting period | COS |
| `maximum` | Maximum value reached over the reporting period | COS |

### Example from the performance payload

The `speed` object below is taken from the
[performance example](../examples/performance/performance.json). Its shared `uom` applies to
both readings. The [performance schema](../schemas/performance.schema.json) requires `current`
and `uom`, permits `target`, and permits no other properties in this object.

```json
{
  "speed": {
    "uom": "m/min",
    "current": 182,
    "target": 200
  }
}
```

This is a payload fragment, not a complete message.

### Rules

- Include only schema-permitted qualifiers; omit an inapplicable qualifier only when optional.
- Use `null` for an unavailable qualifier only where its schema permits null; do not omit required fields.
- All values within a group share the same `uom`. If two variants of the same measurement require different units, they must be modelled as separate fields.

---

[Imprint and Privacy Notice (Impressum / Datenschutz)](../IMPRINT-PRIVACY.md)
