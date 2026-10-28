# COSI — Corrugated Fault Codes

**Version:** 1.0 (prepublication)\
**Publication date:** 2026-11-01\
**Scope:** The closed `faultCode` value set

3-letter failure mode codes for corrugated manufacturing, adapted from the failure-mode notations
of **ISO 14224:2016, Annex B**. A non-null `faultCode` uses a code from this table;
`internalCode` can carry optional vendor-specific detail. The maintenance measurement schema
permits `faultCode: null` when the measurement is within limits.

**Closed set for v1.0.** The 40 codes below are the complete permitted non-null value set for `faultCode`,
enforced as an `enum` in [`schemas/maintenance-measurement.schema.json`](../schemas/maintenance-measurement.schema.json).
Adding a code requires a version change of this standard. Use `OTH` when a fault is not
classifiable and `UNK` when the cause is unclear.

| Code | Description | Examples |
|------|-------------|---------|
| AIR | Abnormal instrument/sensor reading | Incorrect moisture value, faulty encoder, photoelectric switch dirty |
| BRD | Breakdown / major failure | Main drive failed, bearing seized, gearbox damage |
| CLW | Inter-line communication / signal fault | PLC communication disturbed, bus error, no signal from upstream/downstream |
| DOP | Delayed operation | Sluggish heating control, delayed vacuum/drive start |
| ELP | External leakage – process medium | Glue leak, steam/condensate leak, oil on web |
| ELU | External leakage – utility medium | Pneumatic leak, hydraulic leak, cooling water loss |
| ERO | Erratic/unstable output | Web oscillates, speed hunting, register drift |
| FOF | Faulty output frequency / speed | Motor control unstable, line speed fluctuates |
| FOV | Faulty output voltage / supply | Undervoltage drives, spikes, faulty PSU |
| FTC | Failure to close on demand | Guard/slide/valve won't close, glue valve won't shut |
| FTF | Failure to function on demand | Tool change won't start, no vacuum, print unit won't engage |
| FTI | Failure to function as intended | Poor cutting, creasing too shallow/deep, uneven glue |
| FTO | Failure to open on demand | Flap won't open, print unit won't disengage, gap adjust stuck |
| FTR | Failure to regulate/control | Web tension control not working, temperature drift, register control ineffective |
| FTS | Failure to start on demand | Aggregates don't start, line stuck in start mode |
| HIO | High output | Overspeed, excessive web tension, pneumatic overpressure |
| ILP | Internal leakage – process medium | Glue backflow, steam valve internally leaking |
| ILU | Internal leakage – utility medium | Valve internally leaking, hydraulic block bypass |
| INL | Internal leakage (general) | Leak inside aggregate without clear medium |
| LCP | Leakage in closed position | Glue valve drips when closed, steam valve passes |
| LOO | Low output | Vacuum too weak, pressure too low, drive power missing |
| NOI | Noise | Rubbing in print unit, whistling pneumatics, rattling chains |
| OHE | Overheating | Hot bearing, heater zone above setpoint, motor/drive overtemp |
| OTH | Other | Not classifiable / special case |
| PCL | Premature closure | Safety shutdown closes hood, glue valve closes sporadically |
| PDE | Parameter deviation | Moisture high/low, temperature out of tolerance, web tension too high |
| PLU | Plugged/choked | Glue filter blocked, ink chamber clogged, extraction blocked |
| POW | Insufficient power/energy supply | Air pressure low, steam supply drops, mains power missing |
| PTF | Power/signal transmission failure | Sensor cable break, slip ring signal lost, valve not actuated |
| SER | Minor in-service problems | Contamination, loose bolts, worn scrapers |
| SHH | Spurious high alarm level | False web break alarm, moisture high alarm without cause |
| SLL | Spurious low alarm level | Low pressure alarm despite OK, vacuum alarm sporadic |
| SLP | Slippage | Belt slip, web slips on roll, conveyor chatter |
| SPO | Spurious operation | Unwanted print unit opening, die cutter triggers without order |
| STD | Structural/mechanical deficiency | Damaged creaser wheel, broken knife, worn roll, corrosion |
| STP | Failure to stop on demand | Line runs on, aggregate ignores stop |
| UNK | Unknown | Cause unclear / incomplete message |
| UST | Spurious stop | Emergency stop without cause, safety chain trips sporadically |
| VIB | Vibration | Roll imbalance, print unit vibration, die cutter knocking |
| VLO | Very low output | Almost no glue, vacuum near zero, barely visible print |

---

[Imprint and Privacy Notice (Impressum / Datenschutz)](../IMPRINT-PRIVACY.md)
