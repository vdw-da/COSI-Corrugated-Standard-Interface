# COSI — Glossary

**Version:** 1.0 (prepublication)\
**Publication date:** 2026-11-01\
**Scope:** Standard definitions for all COSI domain terminology

| Term | Abbreviation | Standard definition | Notes / usage |
|------|-------------|---------------------|---------------|
| Corrugator | — | Complete corrugating line from roll handling/infeed through wet end and dry end to stacker/outfeed. | Use when referring to the full corrugated board production line. |
| Converting machine | — | Any downstream processing machine (flexo folder gluer, die-cutter, casemaker, printer, laminator, etc.) from infeed/prefeeder to outfeed/palletiser. | Use "converting" consistently instead of mixed German/English terms. |
| MQTT | — | Message Queuing Telemetry Transport — publish-subscribe transport for COSI IT/OT crossings. | Horizontal exchanges within IT or OT may use other protocols. TLS :8883; QoS 1 recommended; dedicated Will QoS 1 required. |
| Quality of Service | QoS | MQTT delivery guarantee level: 0 (at most once), 1 (at least once), 2 (exactly once). | QoS 1 is the baseline for production environments. |
| Heartbeat message | HBT | Periodic message at a defined cycle (typically 1–5 s) independent of state changes. | Used for continuous performance values. |
| Change-of-status message | COS | Event message emitted whenever a machine or system state changes. | Used for discrete events (run/stop/fault, stack discharge, setup triggers). |
| Asset class | `assetClass` | Business domain of a message — determines which payload schema applies. | Values: `performance`, `setup-corrugator`, `setup-converting`, `setup-response`, `maintenance-document`, `maintenance-measurement`, `quality`, `lastwill`. See message-properties.md. |
| Message ID | `messageID` | Globally unique UUID v5 assigned to one message instance. | Distinct instances need distinct generation inputs even for identical content. Retries/replays preserve the assigned ID across restart. |
| Correlation ID | `correlationID` | UUID v5 linking related messages; required for `setup-response` and equal to the original setup messageID. | Optional for other asset classes. |
| UUID v5 | — | Name-based UUID using namespace and name; identical inputs produce the same UUID. | Lowercase hyphenated form for messageID, correlationID and connectionId. Producers allocate distinct inputs; v5 alone neither guarantees uniqueness nor performs de-duplication. |
| One-time data | — | Static or rarely changing reference data. | Documents and task definitions use `onetime`; COSI v1.0 does not define an automatic document-update service. |
| Machine boundary | — | The complete machine within agreed process limits (corrugator: full line; converting: infeed → outfeed). | All input/output/consumption values refer to this boundary. |
| Machine state | — | Discrete operating mode of the machine. | Use only: `unknown`, `stop`, `run`, `fault`, `setup`, `maintenance`, `offline`. |
| Run | `run` | Production running at any line speed >0 within defined boundary. | Standard state label for performance reporting. |
| Stop | `stop` | Machine not producing; line speed = 0 within boundary. | Planned and unplanned stops are sub-categories. |
| Fault | `fault` | Stop caused by a failure requiring intervention; may be accompanied by failure code. | Use with ISO-aligned failure mode codes. |
| Setup state | `setup` | Machine operating state during setup activities. | Distinct from setup instructions for a planned execution. |
| Setup execution | — | Instructions for one planned production execution: possibly several corrugator orders, or a converting processing operation. | Pending revisions and continuation after interruption preserve identity; a separately scheduled execution has a new identity. Corrugator setupId is unique within site/machine. |
| Maintenance | `maintenance` | Machine is not producing due to maintenance activities. | |
| Offline | `offline` | Machine intentionally taken out of operation. | Final message before a controlled shutdown (see Technical Guide § 2.5.1). |
| Changeover | — | Planned activity between jobs, from last good sheet of previous job to first good sheet of next job. | Often called "Setup" in colloquial usage; *Setup time* KPI uses this definition. |
| Setup time | — | Duration measured from the last good sheet of the previous order to the first good sheet of the current order — includes tool changes, machine adjustments, test runs, and material changeovers. | Primary setup KPI. See Technical Guide § 4.4. |
| Stopper | — | Any event causing speed reduction or stop within the boundary. | Prefer "stopper" over mixed terms such as disturbance, blocking, etc. |
| Throughput | — | Output per time. | Use units `m²/h` or `pcs/h`; specify which. |
| OEE | — | Overall Equipment Effectiveness combining availability, performance, and quality. | If calculated, document formula and boundary. |
| Mean Time Between Failures | MTBF | Average operating time between successive failures of a component or system. | Performance and maintenance KPI. |
| Mean Time To Repair | MTTR | Average time to restore a failed component or system to operation. | Maintenance KPI; lower values indicate faster recovery. |
| Job reference | — | Unique identifier for an order/job (from cut list or job list). | Stable across systems (ERP/MES/machine). |
| Article number | — | Unique identifier of a product variant or SKU. | May repeat across jobs. |
| FEFCO | — | European Federation of Corrugated Board Manufacturers — publisher of the standardised box-style code system. | The code identifies the box construction (e.g., 0201 = standard slotted carton). Used as `boxType` in converting setup. |
| FSC | — | Forest Stewardship Council certification — verifies responsibly sourced paper fibres. | Levels: 100%, 75%, Recycled. Used as `requiredFSC` in corrugator setup. |
| Target speed | — | Reference speed supplied by ERP/MES according to the plant’s business rules. | Derivation may vary by implementation; COSI prescribes no baseline calculation method. |
| Running length | lm | Linear metres of board processed within boundary. | Use SI metre; `lm` as field label is acceptable. |
| Area | m² | Board area at the defined counting point or location. | Input/output counters are cumulative within scope/period; logistics quantities are current contents. Article changes alone do not reset counters. |
| Weight | t | Metric tonnes of board processed within boundary. | |
| Grammage | gsm | Mass of paper per unit area. | Expressed in `g/m²`; use the schema field name `gsm`. |
| Pieces | pcs | Discrete material or product units at an identified counting point or location. | Define a consistent counting basis within the scope/period; compare only compatible quantities. |
| Stacks | `stacks` | Number of physical stacks. | Performance input/output counts are cumulative; logistics counts are current contents. Not sheets per stack. |
| Stack count | `stackCount` | Requested number of sheets per stack in corrugator setup. | Three stacks of 200 sheets have stackCount 200, stacks 3 and pieces 600. |
| Stack height | `stackHeight` | Physical stack height in millimetres. | Setup is a requested setting; quality checks evaluate physical height. |
| Counting period | — | Period within which cumulative readings of the same scope are comparable. | Stops do not reset it. Reset/scope change must be distinguishable; do not calculate deltas across periods. Incomplete totals are not zero. |
| Allocated consumption | — | Calculated share of a measured total for a stated source period and allocation basis. | Shares plus identifiable remainder reconcile to the source total; measured-total-only reporting is permitted. |
| Current contents | — | Material present at a location at observation time. | Logistics quantities are inventory observations, not accumulated throughput. |
| Left-to-right | L2R | The order in which orders are physically arranged across the corrugator web, numbered from left to right when looking downstream (towards stacker/in the direction of board travel). Position 0 is the leftmost order on the web. | Used as `l2rSequenceNumber` on each order in the setup-corrugator payload to define the layout.|
| Flute | — | Wave-shaped corrugated paper layer between liners; defines board profile and stacking strength. | Standard flute types: A, B, C, E, F, BC. |
| Caliper | — | Thickness of paper or board, measured in mm. | Used as both paper specification and quality measurement. |
| Trigger | — | Timestamped setup- or process-relevant event (e.g., tool installed, wash program started). | See the COS definition and the applicable payload schema for message usage. |
| Periphery | — | Auxiliary devices connected to the machine (e.g., glue unit, ink kitchen, stacker robot). | The applicable setup schema defines where periphery settings are represented. |
| Single-facer | SF | Corrugator section that bonds one fluting layer to one liner. | A corrugator typically has one to three single-facers. |
| Double-backer | DB | Corrugator section that bonds the final liner to assembled board, completing the corrugated structure. | Final wet-end section before cutting and stacking. |
| Fanfold | — | Periphery device producing accordion-folded corrugated material instead of cut sheets. | Order-assignable. |
| Tape applicator | — | Periphery device applying reinforcement or splice tape during corrugation. | |
| Flexographic printing | flexo-print | Direct relief-printing process using flexible plates on cylindrical print stations. | Standard print process for corrugated board. |
| Printing plate | cliché, plate | Flexible plate mounted on a flexo-print cylinder, carrying the artwork for one ink colour. | "Cliché" is the European term; standard field name is `plateId`. |
| Die-cutter | — | Converting periphery that uses a shaped tool (die) to cut and crease blanks from board sheets. | Rotary or flat-bed variants. |
| Folder-gluer | FFG | Converting machine that folds and glues die-cut blanks into finished boxes. | Often combined with flexo printing into a Flexo Folder Gluer (FFG) line. |
| Stitcher | — | Converting periphery that joins box panels with metal staples instead of glue. | Used for large or heavy-duty boxes. |
| Palletizer | — | Converting periphery that stacks finished boxes or bundles onto pallets in defined patterns. | Includes strapping, wrapping, and label placement. |
| Failure mode | — | Standardized classification of a fault, adapted from ISO 14224:2016, Annex B. | `faultCode` — closed set of 40 three-letter codes ([corrugated-faults.md](corrugated-faults.md)), plus optional vendor `internalCode`. |
| Failure severity | — | Impact level of a fault: `info`, `warning`, `critical`. | Use these exact lowercase values. |
| Quality check | — | Atomic check with counted outcome in a `checks` array under its label, limits and unit. | Numeric or qualitative OK/NOK; receiving applications build reports. A message is not a complete/cumulative report. |
| Check result | — | `OK` or `NOK` against the applicable numeric or qualitative criterion. | Qualitative limits may be null; omit exception unless a numeric bound was violated. Missing checks do not establish OK. |
| First-good-sheet | — | First sheet meeting all quality criteria after a setup or order change. | Marks the end of setup time and the start of productive run. |
| Warp | — | Deviation of a board sheet from flat, expressed as a percentage. | Quality KPI; high warp causes feeding and stacking issues. |
| Register | — | Alignment between successive print stations, or between print and die-cutting. | Reported as longitudinal offset in mm; high register error indicates print mis-alignment. |
| Fishtailing | — | Defect where sheet edges fan out unevenly during folding, giving a fishtail shape. | Quality KPI in folding/gluing; reported as percentage of affected sheets. |
| Maintenance document | `maintenance-document` | One-time message carrying static reference data for a machine component: manual links and service task definitions with frequency triggers. | `assetClass=maintenance-document`, `messageType=onetime`. COSI v1.0 does not define an automatic document-update service. |
| Maintenance measurement | `maintenance-measurement` | Event-driven observation at its original timestamp, with required failure and document-reference objects whose individual fields may be null as permitted. | `assetClass=maintenance-measurement`, `messageType=cos`. Triggers when a threshold is crossed or a condition is detected. |
| Service task | — | A defined maintenance activity for a component, with a frequency trigger (runtime hours, area, pieces, or cycles) and a linked procedure document. | Frequency source must be specified (e.g., motor runtime, production counter). |
| Frequency trigger | — | The counter or threshold that initiates a service task: `h` (hours), `m²` (area), `pcs` (pieces), or `cycles`. | Defined in the maintenance-document payload. |
| Operational technology | OT | Hardware and software directly monitoring or controlling physical production — Levels 0–3 of the architecture (sensors, PLCs, machine control systems, interpreters). | See Technical Guide § 2.4. |
| Information technology | IT | Business and data systems above the production floor — Levels 4–5 (local data servers, ERP/MES, central/cloud services). | See Technical Guide § 2.4. |
| North-south | — | Communication crossing the IT/OT boundary. Permitted only through the Level 3.5 message broker; direct crossings are prohibited in both directions. | Setup, response and machine observation messages are brokered north-south flows. See ADR-000010. |
| East-west | — | Peer-to-peer communication inside one zone (controller ↔ controller in OT, ERP ↔ MES in IT). MQTT is optional within a zone; direct hardware-to-hardware control is out of scope of this standard. | See Technical Guide § 2.4 and ADR-000010. |
| Schema identifier | `schemaId` | Required full payload schema identifier, including version, matching assetClass. | Example: `cosi:performance-payload:1.0`; topic has no version segment. |
| Connection identifier | `connectionId` | Globally unique UUID v5 for one MQTT connection using Last Will. | Shared by its Will and normal equipment messages; fresh on reconnect/restart, distinct from MQTT client ID and messageID. |
| Last Will | `lastwill` | Optional OT connection-loss notification registered with MQTT. | Dedicated message, null timestamp and empty payload; QoS 1, non-retained, Keep Alive enabled. Consumer analysis/handling is outside COSI. |

---

[Imprint and Privacy Notice (Impressum / Datenschutz)](../IMPRINT-PRIVACY.md)
