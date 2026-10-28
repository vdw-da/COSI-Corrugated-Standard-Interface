# COSI — Message Properties

**Version:** 1.0 (prepublication)\
**Publication date:** 2026-11-01\
**Scope:** Common envelope fields, permitted values, timestamp format, and quality check structure

## Envelope Structure

Every COSI message is a JSON object validated against `envelope.schema.json`. Requiredness and conditional use are specified in the table below.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messageID` | `string (UUID v5)` | required | Globally unique assigned identity for one message instance. Distinct instances need distinct v5 inputs; retries/replays preserve the assigned ID, including across restart. |
| `correlationID` | `string (UUID v5)` | conditional | Required for `setup-response`: the original setup messageID. Optional for other related messages. |
| `assetClass` | `string (enum)` | required | Business domain — determines which payload schema applies. |
| `messageType` | `string (enum)` | required | Transmission trigger. |
| `machineId` | `string` | required | Plant-owned identifier, unique within site; matches the topic machine segment using lowercase letters, digits and hyphens. |
| `timestamp` | `string (ISO 8601) or null` | required | Original event time in UTC, ending in Z; required null only for the dedicated Last Will. |
| `status` | `string (enum)` | required | Machine state at event time; lastwill is reserved for the dedicated connection-loss notification. |
| `payload` | `object` | required | Payload selected by assetClass and schemaId. Last Will requires an empty object with no properties. |
| `schemaId` | `string` | required | Full applicable payload schema $id, including version; must match assetClass. |
| `connectionId` | `string (UUID v5)` | conditional | Required on the Will and normal equipment messages for a connection using Last Will; fresh globally unique ID on each reconnect/restart. |

All three UUID fields use lowercase hyphenated UUID v5 text. UUID v5 alone does not allocate
unique inputs or perform de-duplication; producer namespace/allocation methods are implementation
choices. Schema validation checks representation, not global uniqueness. `connectionId` identifies
one connection, not the stable MQTT client or an individual message. Conditional shared use on
normal messages depends on the MQTT connection configuration and cannot be established by
validating an isolated JSON message.

## Common Reference Fields

Reference fields used across asset classes — included in payloads where applicable. Not every payload carries every reference; placement depends on whether the asset class is job-bound, setup-bound, or component-bound. See the individual payload schemas for which fields are required per asset class.

| Field | Type | Description |
|-------|------|-------------|
| `jobRef` | `string \| null` | Manufacturing order reference from ERP / MES. |
| `articleRef` | `string \| null` | Article / product specification reference. |
| `taskRef` | `string \| null` | Manufacturing step reference within the order. |
| `setupRef` | `string \| null` | References corrugator setupSettings.setupId within the same site/machine context; null where not applicable. |

## Timestamp Format

**Semantics.** The `timestamp` field represents the moment the **event itself occurred** (e.g., the instant a stack was discharged, a status transitioned, or a measurement was taken). It is **not** the time the message was assembled, serialised, or transmitted. This distinction matters when messages are buffered, retried (see § 2.5.2 of the Technical Guide), or replayed after a reconnect — the timestamp must continue to reflect the original event.

**Last Will exception.** The dedicated `lastwill` message requires `timestamp: null`: its future
publication time is unknown when it is registered. No other asset class permits a null envelope timestamp.

**Format.** Ordinary envelope timestamps use **ISO 8601 UTC**: `YYYY-MM-DDThh:mm:ss.SSSZ`.
Fractional seconds may be omitted or contain one to three digits.

The `Z` suffix is mandatory. No local time zones — always UTC.

```
2026-05-04T06:30:00.000Z    ✓
2026-05-04T06:30:00+01:00   ✗
```

---

## Enum Values

### `assetClass`

| Value | `messageType` | Description |
|-------|---------------|-------------|
| `performance` | `hbt` / `cos` | Machine throughput, speed, energy, and logistics status. |
| `setup-corrugator` | `cos` | Corrugator setup parameters: ERP/MES sends instructions; the machine publishes changed setup settings back to ERP/MES, including operator edits. |
| `setup-converting` | `cos` | Converting setup parameters: ERP/MES sends instructions; the machine publishes changed setup settings back to ERP/MES, including operator edits. |
| `lastwill` | `cos` | Optional OT connection-loss notification. Requires status lastwill, timestamp null, connectionId and payload {}. |
| `setup-response` | `cos` | Corrugator/converting acknowledgement of setup processing: `OK` for accepted setup or `NOK` with one or multiple field-level errors. Correlation to the original setup message is done through `correlationID`. |
| `maintenance-document` | `onetime` | Static reference data per component: manual PDF links and service task definitions with frequency triggers (`h`, `m²`, `pcs`, `cycles`). COSI v1.0 does not define an automatic document-update service. |
| `maintenance-measurement` | `cos` | Event-driven measurement report: measured value against upper/lower limits, fault classification (`faultCode`, `severity`), and a required document-reference object with nullable fields. |
| `quality` | `cos` | Atomic quality checks. Job-end message mandatory; additional messages optional; applications build reports. |

### `messageType`

| Value | Trigger | Typical use |
|-------|---------|-------------|
| `hbt` | Periodic (min. every 5 s) | Continuous performance values at fixed intervals. |
| `cos` | Event-driven | State changes — run/stop/fault, stack discharge, setup triggers. |
| `onetime` | On demand / once | Static reference data (manuals, component lists, task definitions). |

### `status` — Machine state

| Value | Description |
|-------|-------------|
| `unknown` | State cannot be determined. |
| `stop` | Machine not producing; line speed = 0. |
| `run` | Production running at any line speed > 0. |
| `fault` | Stop caused by a failure requiring intervention. |
| `setup` | Not producing due to setup / changeover activities. |
| `maintenance` | Not producing due to maintenance activities. |
| `offline` | Machine intentionally taken out of operation. Final message before a controlled shutdown (§ 2.5.1). |
| `lastwill` | Dedicated Last Will notification of connection loss; not a physical machine-state assertion (§ 2.5.4). Invalid as the status of other asset classes. |

### Failure severity

| Value | Meaning |
|-------|---------|
| `info` | Minor impact with no measurable production loss. Notification only; no immediate action required. |
| `warning` | Deviation from target parameters. Operator reaction required to prevent degradation to critical status. |
| `critical` | Immediate operator reaction required to prevent production loss or equipment damage. May trigger automatic machine stop. |

### Check result

| Value | Meaning |
|-------|---------|
| `OK` | Meets the applicable numeric or qualitative criterion. |
| `NOK` | Does not meet the applicable numeric or qualitative criterion. |

### `exception` — Quality check deviation reason

Set only for a numeric tolerance-bound violation on a NOK check. Omit for OK and for qualitative NOK without a numeric bound violation; qualitative limits are null, and header uom is null when not applicable. Retain ejection information on NOK. Defined in [ADR-000002](../adr/ADR-000002-quality-check-structure-checks-array.md).

| Value | Meaning |
|-------|---------|
| `lower-violation` | Measured value fell below `lowerLimit`. |
| `upper-violation` | Measured value exceeded `upperLimit`. |

### Movement status

Providing movement status is optional and subject to agreement between supplier and customer. When provided, use the movement values defined here.

| Value | Description |
|-------|-------------|
| `running` | Conveyor or section moving at nominal speed. |
| `stopped` | No movement. |
| `moving-left` | Lateral movement — left direction. |
| `moving-right` | Lateral movement — right direction. |
| `moving-forward` | Longitudinal movement — forward direction. |
| `moving-backward` | Longitudinal movement — backward direction. |
| `rotate-clockwise` | Rotational movement — clockwise. |
| `rotate-counterclockwise` | Rotational movement — counter-clockwise. |

### Failure mode code

3-letter codes adapted from ISO 14224:2016, Annex B, for corrugated manufacturing. Closed set of 40 codes, enforced as an `enum` in the schema — see [Corrugated Faults](corrugated-faults.md) for the full table.

---

## Quality Check Shape

Every quality check uses a single uniform shape regardless of whether the value is numeric, boolean, or qualitative:

| Field | Type | Description |
|---|---|---|
| `errorType` | `string` | Human-readable check label in English |
| `lowerLimit` | `number \| null` | Lower tolerance bound. Null for non-numeric checks |
| `upperLimit` | `number \| null` | Upper tolerance bound. Null for non-numeric checks |
| `uom` | `string \| null` | Unit of measure. Null when not applicable |
| `checks` | `array` | Atomic quality checks with counted outcomes; the receiving application builds reports |

Each `checks` array entry uses the following fields:

| Field | Type | Description |
|---|---|---|
| `quantity` | `number` | Number of pieces covered by this check |
| `uom` | `string` | Unit of the count; use `pcs` |
| `result` | `"OK" \| "NOK"` | Outcome for the counted pieces |
| `ejected` | `boolean` | Whether pieces covered by a NOK check were ejected; retain on NOK |
| `exception` | `"lower-violation" \| "upper-violation"` | Numeric bound violated on NOK; omit if no numeric bound was violated |

OK entries contain `quantity`, `uom` and `result`. Qualitative checks may report OK or NOK
with null limits and null header uom when not applicable. Qualitative NOK does not require an
invented numeric exception. Missing or empty checks do not establish OK output. Neither an
individual message nor its checks array is required to be a cumulative or complete job report.


---

## Quality Fields

The matrix below groups quality checks and application measures into four useful categories
(see § 6.7 of the [Technical Guide](technical-guide.md)). These are descriptive labels and
illustrative units, not additional JSON fields or unit constraints. Transmitted checks use
[Quality Check Shape](#quality-check-shape); the payload schema groups them by production section.

### Dimensional Quality

| Field or Measure | Illustrative Unit | Description |
|-------|-------|-------------|
| Warp / Flatness | `%` | Percentage deviation from flat. |
| Format Accuracy | `mm` | Dimensional accuracy (Length × Width × Height). |
| Gaps | `mm` | Gap width measurement. |
| Stack Accuracy | `mm` | Pallet stack dimensions (L × W × H). |

### Material Quality

| Field or Measure | Illustrative Unit | Description |
|-------|-------|-------------|
| Moisture Content | `%RH` | Percentage relative humidity. |
| Temperature | `°C` | Material temperature. |
| Correct Raw Material Usage | — | Qualitative verification reported as OK/NOK; null limits and header uom when not applicable. |
| Fishtailing | `%` | Percentage of affected sheets. |

### Process Quality

| Field or Measure | Illustrative Unit | Description |
|-------|-------|-------------|
| Print Defects | `pcs` | Quantity of defective prints. |
| Colour Accuracy | `dE2000` | Delta E 2000 colour difference. |
| Register Accuracy | `mm` | Registration deviation measurement. |
| Crease Quality | — | Crease consistency and depth. |
| Glue Application Quality | — | Coverage and bond strength. |

### Output Quality

These percentages are application-level measures derived from production and quality data.
They are not standalone percentage fields in the quality payload. The schema's `wasteFree`
entry uses the common quality-check structure; first-good-sheet success rate is an application KPI.

| Field or Measure | Illustrative Unit | Description |
|-------|-------|-------------|
| Waste-Free Percentage | `%` | Production without quality-related waste. |
| First-Good-Sheet Success Rate | `%` | Setup quality metric. |

The complete set of payload fields and their constraints is defined in
[`schemas/quality.schema.json`](../schemas/quality.schema.json), using the common check structure
recorded in ADR-000002.

---

[Imprint and Privacy Notice (Impressum / Datenschutz)](../IMPRINT-PRIVACY.md)
