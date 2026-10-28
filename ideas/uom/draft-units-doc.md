# DRAFT — `docs/units.md`

This is a **draft**. It lives in `ideas/uom/` until the team approves it. If approved, the content below would move to `docs/units.md` and become the canonical owner of unit-of-measure information.

Two variants are shown below — one per fork.

---

# Variant A — Metric-only-on-wire fork

```markdown
# Units of Measure & Physical Dimensions

This document is the canonical reference for the unit-of-measure (`uom`) values used in COSI messages.

> **Wire format:** the standard is **metric (SI-leaning)** on the wire. Sources using imperial units must convert to SI in the producing connector. Imperial unit symbols are **not** valid `uom` values.

## How units are bound

Each measurement field in an asset-class schema declares a **dimension**. The dimension constrains which `uom` values are accepted by validation. Dimensions are defined once in `schemas/_dimensions.schema.json` and referenced by `$ref` from each asset-class schema.

This means: a width field bound to `Length` cannot accept `°C`; a temperature field bound to `Temperature` cannot accept `m/min`.

## Dimension catalog

The `Rec 20` column lists the UN/CEFACT Recommendation 20 code, included as a non-validating `x-uncefact` annotation in the schema for translation-layer interop (e.g., with OPC UA `EUInformation`).

### Length — dimension `Length`

| Symbol | Rec 20 |
|--------|--------|
| `mm`   | MMT    |
| `cm`   | CMT    |
| `m` ✦  | MTR    |
| `km`   | KMT    |

### Area — dimension `Area`

| Symbol | Rec 20 |
|--------|--------|
| `mm²`  | MMK    |
| `cm²`  | CMK    |
| `m²` ✦ | MTK    |

### Volume — dimension `Volume`

| Symbol | Rec 20 |
|--------|--------|
| `mL`   | MLT    |
| `L`    | LTR    |
| `m3` ✦ | MTQ    |

### Mass — dimension `Mass`

| Symbol | Rec 20 |
|--------|--------|
| `g`    | GRM    |
| `kg` ✦ | KGM    |
| `t`    | TNE    |

### Linear speed — dimension `LengthPerTime`

| Symbol  | Rec 20 |
|---------|--------|
| `m/s` ✦ | MTS    |
| `m/min` | 2X     |

### Throughput — dimension `CountPerTime`

| Symbol    | Rec 20  |
|-----------|---------|
| `pcs/s` ✦ | —       |
| `pcs/min` | —       |
| `pcs/h`   | —       |

### Temperature — dimension `Temperature`

| Symbol | Rec 20 |
|--------|--------|
| `°C` ✦ | CEL    |
| `K`    | KEL    |

### Energy — dimension `Energy`

| Symbol  | Rec 20 |
|---------|--------|
| `Wh`    | WHR    |
| `kWh` ✦ | KWH    |
| `MJ`    | MJ     |

### Pressure — dimension `Pressure`

| Symbol  | Rec 20 |
|---------|--------|
| `Pa` ✦  | PAL    |
| `kPa`   | KPA    |
| `bar`   | BAR    |

### Force — dimension `Force`

| Symbol | Rec 20 |
|--------|--------|
| `N` ✦  | NEW    |
| `kN`   | KNT    |

### Other dimensions

| Dimension          | Symbols                          |
|--------------------|----------------------------------|
| `Humidity`         | `%RH`                            |
| `Grammage`         | `g/m²` (Rec 20: GM)              |
| `ColourDistance`   | `dE2000`, `dE94`, `dE76`         |
| `PrintResolution`  | `dpi`                            |
| `Viscosity`        | `s` (Ford cup), `cP`, `mPa·s`    |
| `Duration`         | `s`, `min`, `h`                  |
| `Ratio`            | `1`, `%`                         |
| `Quantity`         | `pcs`, `stacks`, `rolls`, `sheets`, `pallets` |

✦ = canonical SI unit for this dimension. Producers SHOULD use the canonical unit when no other constraint applies.

## Adding a new uom

1. Add the symbol to the appropriate dimension's `enum` in `schemas/_dimensions.schema.json`.
2. Add a row to the table in this document.
3. If a Rec 20 code exists for the unit, add it to the `x-uncefact` map in the dimension definition.
4. Submit for review.

If the new uom does not belong to any existing dimension, propose a new dimension. New dimensions require team approval.
```

---

# Variant B — Support-both fork

```markdown
# Units of Measure & Physical Dimensions

This document is the canonical reference for the unit-of-measure (`uom`) values used in COSI messages.

> **Wire format:** the standard supports **both metric and imperial** units. The envelope field `unitSystem` declares which system a message uses (`"metric"` by default, `"imperial"` to opt in). Per-field `uom` is always present and authoritative.
> Mixed-system messages are not supported.

## How units are bound

Each measurement field in an asset-class schema declares a **dimension**. The dimension constrains which `uom` values are accepted by validation — including both metric and imperial members of that dimension.

This means: a width field bound to `Length` accepts `mm`, `m`, `in`, `ft` — but rejects `°C`, `s`, `kg`.

## Dimension catalog

- `System` column: `metric` or `imperial`.
- `Rec 20` column: UN/CEFACT Recommendation 20 code, included as a non-validating `x-uncefact` annotation in the schema.
- `→ SI` column: multiplier to convert this unit's numeric value to the canonical SI unit (column marked ✦). Used by consumers performing cross-system aggregation.

### Length — dimension `Length`

| Symbol | System   | Rec 20 | → SI (m)  |
|--------|----------|--------|-----------|
| `mm`   | metric   | MMT    | 0.001     |
| `cm`   | metric   | CMT    | 0.01      |
| `m` ✦  | metric   | MTR    | 1         |
| `km`   | metric   | KMT    | 1000      |
| `in`   | imperial | INH    | 0.0254    |
| `ft`   | imperial | FOT    | 0.3048    |
| `yd`   | imperial | YRD    | 0.9144    |

### Area — dimension `Area`

| Symbol | System   | Rec 20 | → SI (m²) |
|--------|----------|--------|-----------|
| `mm²`  | metric   | MMK    | 0.000001  |
| `cm²`  | metric   | CMK    | 0.0001    |
| `m²` ✦ | metric   | MTK    | 1         |
| `in²`  | imperial | INK    | 0.00064516|
| `ft²`  | imperial | FTK    | 0.092903  |

### Volume — dimension `Volume`

| Symbol   | System   | Rec 20 | → SI (m³) |
|----------|----------|--------|-----------|
| `mL`     | metric   | MLT    | 1e-6      |
| `L`      | metric   | LTR    | 0.001     |
| `m3` ✦   | metric   | MTQ    | 1         |
| `ft3`    | imperial | FTQ    | 0.0283168 |
| `gal_us` | imperial | GLL    | 0.0037854 |

### Mass — dimension `Mass`

| Symbol | System   | Rec 20 | → SI (kg) |
|--------|----------|--------|-----------|
| `g`    | metric   | GRM    | 0.001     |
| `kg` ✦ | metric   | KGM    | 1         |
| `t`    | metric   | TNE    | 1000      |
| `oz`   | imperial | ONZ    | 0.0283495 |
| `lb`   | imperial | LBR    | 0.453592  |

### Linear speed — dimension `LengthPerTime`

| Symbol   | System   | Rec 20 | → SI (m/s) |
|----------|----------|--------|------------|
| `m/s` ✦  | metric   | MTS    | 1          |
| `m/min`  | metric   | 2X     | 0.016667   |
| `ft/min` | imperial | FR     | 0.00508    |
| `fpm`    | imperial | FR     | 0.00508    |

### Temperature — dimension `Temperature`

Affine, not linear — conversion is not a multiplier. See § Conversion notes.

| Symbol | System   | Rec 20 |
|--------|----------|--------|
| `°C` ✦ | metric   | CEL    |
| `K`    | metric   | KEL    |
| `°F`   | imperial | FAH    |

### Energy — dimension `Energy`

| Symbol  | System   | Rec 20 | → SI (J)  |
|---------|----------|--------|-----------|
| `Wh`    | metric   | WHR    | 3600      |
| `kWh` ✦ | metric   | KWH    | 3.6e6     |
| `MJ`    | metric   | MJ     | 1e6       |
| `BTU`   | imperial | BTU    | 1055.06   |

### Pressure — dimension `Pressure`

| Symbol | System   | Rec 20 | → SI (Pa) |
|--------|----------|--------|-----------|
| `Pa` ✦ | metric   | PAL    | 1         |
| `kPa`  | metric   | KPA    | 1000      |
| `bar`  | metric   | BAR    | 100000    |
| `psi`  | imperial | PS     | 6894.76   |

### Force — dimension `Force`

| Symbol | System   | Rec 20 | → SI (N)  |
|--------|----------|--------|-----------|
| `N` ✦  | metric   | NEW    | 1         |
| `kN`   | metric   | KNT    | 1000      |
| `lbf`  | imperial | C62    | 4.44822   |

### Other dimensions

| Dimension         | Symbols                                              |
|-------------------|------------------------------------------------------|
| `CountPerTime`    | `pcs/s` ✦, `pcs/min`, `pcs/h`                        |
| `Humidity`        | `%RH`                                                |
| `Grammage`        | `g/m²` (Rec 20: GM), `oz/ft²` (Rec 20: 37)           |
| `ColourDistance`  | `dE2000`, `dE94`, `dE76`                             |
| `PrintResolution` | `dpi`                                                |
| `Viscosity`       | `s` (Ford cup), `cP`, `mPa·s`                        |
| `Duration`        | `s` ✦, `min`, `h`                                    |
| `Ratio`           | `1`, `%`                                             |
| `Quantity`        | `pcs`, `stacks`, `rolls`, `sheets`, `pallets`        |

✦ = canonical SI unit. Conversion factors are informative — producers MUST send the value in whatever uom they declare; conversion is the consumer's responsibility.

## Conversion notes

- **Temperature** is affine, not linear. `°C → K`: add 273.15. `°F → °C`: `(F − 32) × 5/9`. Do not use a single multiplier.
- **Ford-cup viscosity (`s`)** is not a linear function of `cP` / `mPa·s` — it depends on cup geometry. Treat `s` as a measurement on its own, not interconvertible without context.
- **dpi vs lpi**: only `dpi` is in the catalog; if `lpi` is needed, propose a separate dimension or accept it under `PrintResolution`.

## Adding a new uom

1. Add the symbol to the appropriate dimension's `enum` in `schemas/_dimensions.schema.json`.
2. Add a row to the table in this document with system, Rec 20 (if any), and conversion factor.
3. If a Rec 20 code exists for the unit, add it to the `x-uncefact` map in the dimension definition.
4. Submit for review.

If the new uom does not belong to any existing dimension, propose a new dimension. New dimensions require team approval.
```
