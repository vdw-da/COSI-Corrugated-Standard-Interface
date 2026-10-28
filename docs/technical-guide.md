# COSI Technical Guide

**Version:** 1.0  
**Updated:** 2026-10-16\
**Publication date:** 2026-11-01\
**Status:** Prepublication — package approved

---

## Document Information

**Working Group:** VDW (Association of the German Corrugated Cardboard Industry e.V.)  
**Standard:** COSI — Corrugated Standard Interface

**Authors:**

- Michael Sachs
- Robert Schmid
- Daniel Malolepszy
- Dennis Strasser
- Tobias Winkler
- André Seifert

**Technical editors:** technical specification development and quality assurance.

- André Seifert (ePS)
- Robin Boeckxstaens (OMP)

---

## Document Authority

The PDF edition is a reproduction of the Markdown source published in the
[official COSI GitHub repository](https://github.com/vdw-da/COSI-Corrugated-Standard-Interface).
In the event of any discrepancy, the Markdown source for the corresponding document version
shall prevail.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Definitions and Interface Specifications](#2-definitions-and-interface-specifications)
   - 2.1 Terminology
   - 2.2 Data Interface Specifications
   - 2.3 MQTT Security Requirements
   - 2.4 Data Architecture
   - 2.5 Resiliency & Retry
   - 2.6 Documentation Management
3. [Business Case: Performance](#3-business-case-performance)
4. [Business Case: Setup](#4-business-case-setup)
5. [Business Case: Maintenance](#5-business-case-maintenance)
6. [Business Case: Quality](#6-business-case-quality)
7. [Future Extensions](#7-future-extensions)
8. [Appendices](#8-appendices)

---

## 1. Introduction

This technical guide defines standardized data interfaces and protocols for transparent data exchange in the corrugated cardboard manufacturing industry. Required fields and permitted optional data are defined by the schemas. Manufacturer extensions are allowed only at the declared `customProps` locations in setup payloads.

### 1.1 Scope and Purpose

The COSI standard enables:

- **Interoperability**: Standardized data exchange between machines and enterprise systems
- **Transparency**: Real-time visibility into production, quality, and maintenance data
- **Efficiency**: Reduced setup times, improved performance tracking, and optimized maintenance
- **Vendor Neutrality**: Common protocol independent of machine manufacturer

### 1.2 Design Principles

- **Baseline Standard**: Required fields remain required; optional measurements remain optional. Use `null` only where the field permits it, omit optional unavailable measurements where appropriate, and report zero only for an actual zero. No additional sensor or universal minimum measurement set is required.
- **Extensibility**: `customProps` on the setup payloads and corrugator orders carries vendor/site data. Consumers ignore unknown keys. Other objects remain closed as defined by their schemas ([ADR-000019](../adr/ADR-000019-custom-props-extension-object.md)).
- **Independence**: Standard operation must not depend on proprietary extensions
- **Local Data Management**: All data managed locally; cloud services are optional

---

## 2. Definitions and Interface Specifications

### 2.1 Terminology

#### Time-Based Terms

**Heartbeat (HBT)**  
Periodic equipment messages providing observations at their original event time. A delayed heartbeat is a historical observation, not proof of current connectivity.

- **Frequency**: Minimum every 5 seconds, maximum every 1 second
- **Cadence**: HBT cadence should reflect production rhythm — faster lines toward the 1 s bound, slower lines toward the 5 s bound. No fixed formula required.

**Change of Status (COS)**  
Event-driven message transmitted whenever the machine or system state changes.

- **Examples**: Stack discharge, transition between setup/run/stop states, alarm conditions
- **Requirement**: Immediate transmission upon state change

#### Status Values

Ordinary messages carry a `status` field representing the machine operational state at the time of the reported event. The dedicated Last Will uses `lastwill` to identify connection loss, without asserting a physical production stop (§ 2.5.4). The `offline` value is reserved for the final message transmitted before a controlled shutdown (see § 2.5.1).

For the full value list and descriptions, see the `status — Machine state` enum in [`message-properties.md`](message-properties.md).

#### System Boundaries

**Production Scope**

For consumption, production, and input quantities, the interface covers the complete machine system:

- **Corrugators**: Full corrugating line from roll stand through stacker
- **Converting Equipment**: Complete process from infeed conveyor (pre-prefeeder) to outfeed conveyor (post-palletizer/robot)
- **Requirement**: Manufacturers must define consistent output metrics within these boundaries

**Logistics Scope**

Logistics data should be reported by functional area:

- Roll logistics and storage
- Intermediate storage and material handling
- Finished goods removal
- Packaging line operations

#### Data Formatting

**Number Formatting**

- Use standard JSON data types ([JSON Data Type Specification](https://www.json.org/json-en.html))
- Include units with all measurements
- **Metric only** — use the units and field-specific tokens defined by the schemas and `docs/naming-conventions.md` § 6. Existing tokens such as `pcs`, `dpi` and `FEFCO` retain their defined uses. Imperial sources convert before publishing; general imperial-unit support is deferred to v1.1.
- **Numeric precision follows the data type** — producers send the precision their source data type provides; consumers must not assume a fixed number of decimal places. COSI imposes no additional precision restrictions or limits.

**Message Validation**

- Each message type must have a corresponding JSON schema
- Schemas enable automated validation of message structure and content
- Validation checks structure and declared constraints; it does not establish measurement accuracy, identifier uniqueness or delivery

---

### 2.2 Data Interface Specifications

#### Message Format

**Standard Protocol**

- **Format**: JSON (JavaScript Object Notation)
- **Encoding**: UTF-8
- **Requirement**: Manufacturers deviating from standard JSON must provide machine-side interpreter/adapter

#### Transport Protocol

**MQTT Server Architecture**

- **Protocol**: MQTT (Message Queuing Telemetry Transport)
- **Version**: MQTT 3.1.1 or higher recommended
- **Port**: 8883 (TLS encrypted) required; 1883 (unencrypted) must be disabled
- **Quality of Service**: QoS 1 recommended for production environments
- **Architecture**: Publish-subscribe model with broker-based message distribution

**Protocol Variants**

- Minimize protocol variations to ensure interoperability
- MQTT is required for COSI exchanges crossing the IT/OT boundary; horizontal exchanges within either zone may use other protocols (§ 2.4)
- Alternative protocols (e.g., REST API) are not part of this standard

#### Business Case Mapping

Each message uses the topic pattern `cosi/<site>/<machine>/<assetClass>/<direction>`.
Direction is from the machine's perspective: `send` is machine → IT; `receive` is IT → machine.
The asset-class segment is not the envelope trigger `messageType`. All segments use only
lowercase letters `a-z`, digits `0-9` and hyphens. There is no topic version segment.

The plant owner maintains and communicates the authoritative identifiers: site is unique within
the broker's `cosi` namespace, machine within site. Providers map their internal identifiers to
these definitions; envelope `machineId` matches the machine topic segment. Topics group equipment
traffic by this site/machine identity.

Every envelope requires `schemaId`, the full applicable payload `$id`, including version and
`-payload`, for example `cosi:performance-payload:1.0`. It must match `assetClass` and the payload
contract ([ADR-000021](../adr/ADR-000021-mqtt-topic-scheme-and-schema-identification.md)).

| Business Case | Chapter | `assetClass` | `messageType` | MQTT Topic Pattern |
|---------------|---------|--------------|---------------|---------------------|
| Performance | § 3 | `performance` | `hbt`, `cos` | `cosi/<site>/<machine>/performance/send` |
| Setup — Corrugator S1 | § 4 | `setup-corrugator` | `cos` | `cosi/<site>/<machine>/setup-corrugator/receive` |
| Setup — Corrugator S2 | § 4 | `setup-corrugator` | `cos` | `cosi/<site>/<machine>/setup-corrugator/send` |
| Setup — Converting S1 | § 4 | `setup-converting` | `cos` | `cosi/<site>/<machine>/setup-converting/receive` |
| Setup — Converting S2 | § 4 | `setup-converting` | `cos` | `cosi/<site>/<machine>/setup-converting/send` |
| Setup — Response | § 4 | `setup-response` | `cos` | `cosi/<site>/<machine>/setup-response/send` |
| Maintenance — Documents | § 5 | `maintenance-document` | `onetime` | `cosi/<site>/<machine>/maintenance-document/send` |
| Maintenance — Measurements | § 5 | `maintenance-measurement` | `cos` | `cosi/<site>/<machine>/maintenance-measurement/send` |
| Quality | § 6 | `quality` | `cos` | `cosi/<site>/<machine>/quality/send` |
| Optional OT Last Will | § 2.5.4 | `lastwill` | `cos` | `cosi/<site>/<machine>/lastwill/send` |

For example, ERP/MES sends instructions on
`cosi/plant-1/corr-line-01/setup-corrugator/receive`; the machine returns changed settings on
`cosi/plant-1/corr-line-01/setup-corrugator/send` and processing results on
`cosi/plant-1/corr-line-01/setup-response/send`. Machine observations use, for example,
`cosi/plant-1/corr-line-01/performance/send` or `cosi/plant-1/ffg-line-02/quality/send`.

Machines publish performance, quality and maintenance data. An MES or other consumer is not
required to publish machine telemetry or heartbeats merely because it connects. `hbt` and `cos`
describe publication triggers, not application acknowledgment requirements. Setup processing uses
`setup-response`; no general application acknowledgment of telemetry is required.

Queue management (`queue`, `queue-delete`) is excluded from v1.0; v1.1 is a candidate, not a
commitment ([ADR-000007](../adr/ADR-000007-queue-schema-retained-state-baseline.md)).

Envelope, payload, and enum value details for each asset class are defined in [`message-properties.md`](message-properties.md).

---

### 2.3 MQTT Security Requirements

Security is critical for industrial environments. The following checklist defines recommended security measures for MQTT implementations.

#### 2.3.1 Transport Security

| Requirement | Description | Priority |
|-------------|-------------|----------|
| TLS Encryption | Use TLS encryption on port 8883 | **Mandatory** |
| Disable Unencrypted | Disable unencrypted MQTT (port 1883) | **Mandatory** |
| TLS Version | Use TLS 1.2 or higher | **Mandatory** |
| Cipher Suites | Disable weak cipher suites | Required |
| Certificate Management | Use valid, non-expired certificates | **Mandatory** |

#### 2.3.2 Authentication

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Anonymous Access | No anonymous access allowed | **Mandatory** |
| Authentication Method | Username/password OR X.509 client certificates | **Mandatory** |
| Preferred Method | X.509 client certificates for machines | Recommended |
| Password Policy | Strong passwords with regular rotation | Required |
| Credential Rotation | Periodic credential updates with UI support | Recommended |
| Decommissioning | Immediate credential revocation for retired devices | **Mandatory** |

#### 2.3.3 Authorization (Access Control)

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Access Control Lists | Implement topic-based ACLs | **Mandatory** |
| Publish Permissions | Restrict publish rights per device | **Mandatory** |
| Subscribe Permissions | Restrict subscribe rights per role | **Mandatory** |
| Topic Separation | Use hierarchical topics (e.g., `cosi/plant-1/corr-line-01/#`) | Required |

#### 2.3.4 Network Security

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Internal Hosting | Broker hosted inside internal network | **Mandatory** |
| No Internet Exposure | No direct internet access to broker | **Mandatory** |
| Firewall Protection | Configure firewall rules for broker | **Mandatory** |
| IP Whitelisting | Allow only required IP addresses | Required |
| Network Segmentation | Separate production from office IT network | Recommended |

#### 2.3.5 Broker Hardening

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Minimize Services | Disable unused services and ports | Required |
| Software Updates | Keep broker software current | **Mandatory** |
| Audit Logging | Enable comprehensive logging | **Mandatory** |
| Brute-Force Protection | Limit connection attempts | Required |
| Rate Limiting | Configure connection rate limits | Recommended |
| Message Size Limits | Set maximum message size | Recommended |

#### 2.3.6 Data Integrity & Reliability

| Requirement | Description | Priority |
|-------------|-------------|----------|
| QoS Level | Use QoS 1 in production environments | Recommended |
| Persistent Sessions | Enable only when required | Required |
| Payload Validation | Validate JSON schema for all messages | **Mandatory** |
| Anomaly Detection | Monitor abnormal publish rates | Recommended |

#### 2.3.7 Monitoring & Incident Response

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Failed Login Monitoring | Track and alert on failed authentication | Required |
| Subscription Monitoring | Monitor unusual topic subscriptions | Recommended |
| Connection Logging | Log all client connections/disconnections | Required |
| Traffic Analysis | Set alerts for abnormal patterns | Recommended |
| Undeliverable Message Alerts | Surface messages exhausted by the retry policy (see § 2.5.2) | Required |
| Incident Procedures | Define response procedures | **Mandatory** |

#### 2.3.8 Device Security

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Firmware Security | Secure and verify device firmware | Required |
| Default Credentials | Disable all default credentials | **Mandatory** |
| Secure Storage | Store certificates in TPM or secure storage | Recommended |
| Firmware Updates | Regular firmware updates | Required |
| Service Minimization | Remove unused services from devices | Recommended |

#### 2.3.9 Backup & Redundancy

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Configuration Backup | Regular backup of broker configuration | **Mandatory** |
| Certificate Backup | Secure backup of certificates and keys | **Mandatory** |
| Broker Redundancy | Implement cluster or failover | Recommended |
| Restore Testing | Periodic restore procedure tests | Required |

#### 2.3.10 Minimum Secure Baseline

For production and quality data collection, the following represents the minimum secure configuration:

✓ MQTT 3.1.1 or higher over TLS (port 8883)  
✓ Username/password or X.509 client certificate authentication; certificates preferred (§ 2.3.2)\
✓ Strict ACL per machine  
✓ Broker in internal network  
✓ Firewall protection  
✓ Comprehensive logging enabled  

---

### 2.4 Data Architecture

The system follows a layered architecture approach:

**Level 0 - Sensors & Actuators**  
Field devices and hardware components

**Level 1 - PLC**  
Programmable Logic Controllers managing machine operations

**Level 2 - Machine Control Systems**  
Individual system controllers (corrugator, converter, logistics systems)

**Level 3 - Machine Interpreters & OPC-UA Integration**  
Data transformation and protocol conversion layer (MQTT directly or via OPC-UA)

**Level 3.5 - IT/OT Integration Layer**  
Data broker (MQTT) providing interface between operational technology and information technology

**Level 4 - Local Data Servers**  
Plant-level data storage and business logic

**Level 5 - Central Services / Cloud** (Optional)  
Enterprise-wide services and optional cloud integration

All data must be accessible at Level 3-4. Cloud services (Level 5) are optional and must not be required for standard operation.

**Communication Directions**

Level 3.5 separates the two zones of the architecture: **OT** (operational technology, Levels 0–3) and **IT** (information technology, Levels 4–5).

- **East-west** — exchange between peers inside one zone (controller ↔ controller in OT; ERP ↔ MES in IT) — is bidirectional and need not use MQTT; MQTT is optional for those horizontal exchanges. Direct hardware-to-hardware control (e.g. a stacker signalling the conveyor on discharge) is out of scope of this standard.
- **North-south** — any exchange crossing the IT/OT boundary — is permitted **only** through the Level 3.5 message broker. Setup instructions, setup responses, machine-side changed settings and machine observations are brokered north-south flows.
- Direct crossings of the IT/OT boundary are prohibited in **both** directions: IT systems must not address machine controllers directly, and machine controllers must not address IT systems directly, bypassing Level 3.5. A manufacturer offering a non-MQTT interface must provide an MQTT adapter (§ 2.2 and § 4.2).

---

### 2.5 Resiliency & Retry

Reliable data delivery is essential for transparent reporting. The following requirements define how machines and systems must behave during shutdown and after message transmission failures.

#### 2.5.1 Graceful Shutdown

Before a machine is physically powered down, it **must** transmit a final message carrying the status value `offline`.

- **Purpose**: Distinguishes a planned, orderly shutdown from an unexpected connection loss or fault
- **Trigger**: Last message issued by the machine prior to power-down or controlled disconnect
- **Status Value**: `offline`

The message reports the controlled shutdown at its event time. Its absence alone does not establish a cause of lost connectivity. Subscriber availability assessment is outside the Last Will contract.

#### 2.5.2 Retry on Message Failure

If a message cannot be delivered successfully (no broker acknowledgement, connection error, QoS 1 timeout, etc.), the sender **shall** retry transmission.

| Parameter | Value |
|-----------|-------|
| Maximum retries | **3** attempts after the original failed message |
| Termination | Successful broker acknowledgement (per MQTT QoS 1) |
| On exhaustion | Message is considered undeliverable; log locally and surface via monitoring (see § 2.3.7) |
| Ordering | Retried messages preserve the original event timestamp (see Timestamp section of [`message-properties.md`](message-properties.md)) |
| De-duplication | Retries/replays preserve the assigned `messageID`, including across restart. A new message instance uses a new ID even for identical content; UUID v5 alone neither allocates unique identities nor performs de-duplication |

#### 2.5.3 Reconnection Behavior

Following loss of broker connectivity, clients should attempt automatic reconnection. Once the
connection is re-established, equipment resumes its heartbeat cadence and pending COS delivery.
An IT consumer restores its applicable subscriptions; it need not emit equipment heartbeats.
Subscription recovery depends on the session still existing, its subscriptions and QoS, and the
broker's configured retention and storage limits. Re-subscribing alone does not recover messages
that were never stored or have expired. QoS acknowledgment confirms transport delivery at the
relevant MQTT hop, not application acceptance or completion of production.

COSI retains the retry baseline above and persistent sessions when required (§ 2.3.6). It does
not promise unlimited replay, recovery of every heartbeat, or delivery across every outage, and
does not prescribe durable outboxes or a universal storage/recovery period. Delayed messages
retain their original event time and message identity. Setup request outcomes follow § 4.8.

#### 2.5.4 Optional OT Last Will

OT equipment may register the dedicated Last Will defined by
[ADR-000022](../adr/ADR-000022-mqtt-last-will.md). IT-system Last Will is outside v1.0.
When used, register the message on `cosi/<site>/<machine>/lastwill/send` with MQTT **Will QoS 1**,
**retain false**, and **non-zero Keep Alive**. The installation chooses the Keep Alive interval;
COSI specifies no loss-detection or notification deadline and does not change heartbeat cadence.
These are MQTT settings, not JSON fields.

The Will envelope uses `assetClass: lastwill`, `schemaId: cosi:lastwill-payload:1.0`,
`messageType: cos`, `status: lastwill`, required `timestamp: null` and required empty `payload: {}`.
The future connection-loss time is unknown when the client registers the Will. Only this dedicated
message permits a null envelope timestamp; ordinary events keep their UTC `Z` timestamps.
The payload permits no properties, including extensions.

For each connection using Last Will, the equipment assigns a fresh globally unique `connectionId`
and includes it in that connection's Will and normal equipment messages. Reconnect or restart
creates a new connection identity even if the MQTT client ID is reused. The identifier is a
lowercase, hyphenated UUID v5, distinct from both the MQTT client ID and per-message `messageID`.
Producers ensure distinct v5 generation inputs across connections, including after restart;
the namespace/allocation algorithm is implementation-defined. UUID format does not establish
uniqueness or connection order. Equipment not using Last Will has no such requirement.

The [Will example](../examples/lastwill/lastwill.json) and
[performance example](../examples/performance/performance.json) share an illustrative connection
identity. The Will identifies connection loss; it does not assert a physical production stop.
Whether and how subscribers analyze or handle the notification is outside COSI requirements.

---

### 2.6 Documentation Management

Machine documentation (operator manuals, maintenance procedures, training materials, specifications) is part of the standard and must be made available alongside the data interface.

- **Format**: PDF for all machine documentation
- **Tagging**: Unique identifiers per machine unit and task category
- **Categories**: Operator manuals, maintenance procedures, training materials, specifications
- **Intervals**: Daily, weekly, monthly, yearly maintenance procedures
- **Availability**: Documents must be accessible locally via unique references
- **Updates**: Change service mechanism (to be defined in future revisions)
- **Storage**: Local storage required; external cloud storage optional

Document links do not authorize direct IT/OT crossings. Access must respect § 2.4. COSI v1.0
does not define an automatic document-update, full-list synchronization or transfer service.

---

## 3. Business Case: Performance

### 3.1 Overview

Performance monitoring provides real-time visibility into machine productivity, enabling optimization of throughput, efficiency, and resource utilization.

### 3.2 Use Cases

Application-level reporting, analysis and planning use the exchanged data; their functionality
is not prescribed by COSI. The scope distinctions below apply to the data exchange.

| ID | Description | Expected Benefits | Status |
|----|-------------|-------------------|--------|
| P1 | Simplified performance data acquisition without external sensors (setup time, run speed, breakdowns, downtime, maximum speed) | Simplified connection of new machines to ERP/MES; data consistency with manufacturer tools | In scope |
| P2 | Machine-internal downtime information feeding ERP/MES documentation | Reduced documentation effort; improved data quality for analysis | Out of scope |
| P3 | Anomaly detection per customer/board grade/job/shift | Reduced recurring analysis effort; faster response to issues | In scope |

### 3.3 Key Performance Indicators

The following indicators illustrate possible uses of COSI data. They do not prescribe
mandatory calculations or additional message fields.

#### Production Metrics

- **Throughput**: Pieces per hour, square meters per hour
- **Productivity**: Square meters per full-time equivalent (m²/FTE)
- **Utilization/OEE**: Overall Equipment Effectiveness
- **Speed Metrics**: Actual speed, target speed, maximum speed
- **Dimensional Factors**: Working width, square meters per sheet

#### Downtime & Availability

- **Stop Frequency**: Number of stops per time period
- **Stop Duration**: Individual and cumulative stop times
- **Stop Classification**: Categorized by type and cause
- **MTBF**: Mean Time Between Failures

#### Resource Consumption

- **Energy Consumption**: Power usage per unit output
- **Material Consumption**: Raw material usage and waste
- **Efficiency Ratios**: Output versus input metrics

### 3.4 Benefits

**Primary Benefits**

- **Productivity Optimization**: Identify and reduce duration/frequency of production stops
- **Performance Improvement**: Enhance first-run and repeat-run performance through historical analysis
- **Anomaly Detection**: Rapid identification and response to deviations
- **Training Reduction**: Reduced operator training requirements through automated monitoring
- **Plug-and-Play Integration**: Connect new machines without additional sensors

**Statistical Process Monitoring**

- Track standard deviations for repeat jobs
- Establish baseline performance metrics
- Identify best-in-class benchmarks for cross-company comparison

### 3.5 Data Requirements

Detailed datasets and field definitions live alongside the standard:

- **Performance payload** — [`schemas/performance.schema.json`](../schemas/performance.schema.json): header, energy / water / steam / air consumption, input and output material streams, speed, optional logistics status, and an optional die-pressure reading (flat-bed die cutters).
- **Envelope and enum values** — [`message-properties.md`](message-properties.md).

Providing movement status is optional and subject to agreement between supplier and customer.
When provided, use the defined *Movement status* values in [`message-properties.md`](message-properties.md).
`logisticsStatus` is optional; each supplied item still requires `statusId`.

#### Quantity interpretation

Input/output and resource-consumption quantities are **cumulative counters** for their identified
machine/stream or execution/job scope and counting period. Compare successive compatible readings;
do not add them. Readings of 1,000 and 1,300 pieces in one period establish an increase of 300.
Changing `hbt` to `cos` does not change that arithmetic. Current speed and die pressure are
observations; logistics quantities describe **current contents** at the identified location.
Two buffer readings of 240 pieces do not establish throughput of 480 pieces.

Article identity alone does not identify a period. Machine/stream counters need not reset at
job changes; an article change alone is not a reset. Stops and communication interruptions do
not begin a new period. A reset or scope change must be distinguishable from continuing counting.
Continue after restart only where continuity can be established. Close a controlled period with
its final total; if the total cannot be recovered, its history is incomplete, not zero. Never
calculate a delta across incompatible periods. A late closing total belongs to its original
period and must not be counted again as new production. These meanings do not introduce a new
reset, correction or recovery message.

Measured consumption and calculated job shares must be distinguishable. An allocation identifies
its source total, period and allocation basis; shares and any unassigned remainder reconcile
with that total, allowing for rounding. Reporting only a measured total is permitted; no
universal allocation formula is prescribed. Allocations are subdivisions, not extra consumption.
The existing payload fields are retained; COSI v1.0 adds no allocation or period-control fields.

A piece is one discrete unit at the defined counting point or location. Compare or combine only
compatible units and counting bases. Event totals concern the participating streams of that
event; a COS carrying an output counter remains cumulative. A discharge and an output counter
may describe the same material and must not be added together. The schema defines no separate
discharge-event payload.

Performance `stacks` counts **physical stacks**. Setup `stackCount` gives **requested sheets per
stack** and `stackHeight` gives **physical height in mm**. Three stacks of 200 sheets mean three
stacks and 600 pieces. Two actual stacks of 200 and 80 sheets mean two stacks and 280 pieces;
use actual contents and participating outs, not the target multiplied by all configured outs.
S2 feedback reports changed setup settings, not actual output.

For the same scope, period and unit, total output comprises non-overlapping good, rejected and
unclassified output. Missing quality information does not make output good. This interpretation
does not introduce classification counters into the performance schema. Manual refeeding during
setup, such as reusing a sheet while adjusting print register, requires no autonomous detection
or correction by COSI machines; any operator accounting belongs to the MES/shop-floor application.


### 3.6 Application Examples

The following examples illustrate application uses of data and context. They introduce no
additional message fields or interface requirements.

| Data or Context | Affected Area | Purpose |
|------------------|---------------|---------|
| Downtime (corrugator/converting); major breakdowns; production plans | Production / Planning | Timestamp and duration of planned stops |
| Paper quality changes | Converting | Adjust base settings (target speed, die-cutting pressure, etc.) |
| Converting speed | Converting | Optimize transport logistics; prioritize fast-running machines to prevent idle time |

### 3.7 Target Speed Baseline

The target-speed baseline is the reference speed supplied by ERP/MES according to the plant's
business rules. Its derivation may differ between plants and implementations. COSI does not
prescribe a calculation method, a local-performance rule, a cross-site benchmark or a theoretical
model. The interface communicates the resulting target value with its unit of measure.

---

## 4. Business Case: Setup

### 4.1 Overview

Setup data exchange enables automated machine configuration, reducing setup times and improving process consistency through bidirectional data flow between ERP/MES and production equipment via the message bus.

Bidirectional setup exchange does not require manufacturer cloud services; the communication
rules in § 2.4 apply.

### 4.2 Technology Decision

**Protocol:** MQTT across the IT/OT boundary, with the transport/retry conditions in § 2.5 and application setup responses in § 4.8

- Setup processing is confirmed with `setup-response`; a broker acknowledgment alone does not confirm application acceptance
- Bidirectional communication essential for setup operations

**Non-Standard Alternative:** REST API (not part of this standard; manufacturers using REST API must provide MQTT adapter)

### 4.3 Use Cases

Application-level reporting, analysis and planning use the exchanged data; their functionality
is not prescribed by COSI. The scope distinctions below apply to the data exchange.

| ID | Description | Expected Benefits | Status |
|----|-------------|-------------------|--------|
| S1 | Job order and setup data transmission from ERP/MES to machine (non-machine-specific data) | Reduced setup times; elimination of manual data entry | In scope |
| S2 | Machine setting adjustments fed back to ERP/MES to save optimal setup parameters | Repeatability analysis; setup time optimization | In scope |
| S3 | Tool and cliché identification to match target versus actual and record runtime | Precise runtime documentation; prevention of incorrect tool usage | In scope |

**S2 message path:** when setup settings change on the machine controller, including operator
changes to dimensions or other setup parameters, the machine must publish the changed setup
back to ERP/MES using the corresponding `setup-corrugator` or `setup-converting` message
with the `cos` trigger. The message uses the applicable setup payload schema and travels
through the Level 3.5 broker. These messages report the changed setup parameters; production
actuals such as produced quantities and waste belong in their reporting messages.

### 4.4 Key Concepts

#### Setup execution and identity

A setup describes instructions for one planned execution: potentially several simultaneous
orders on a corrugator, or one processing operation on a converting machine. Revisions for the
same pending execution and continuation after interruption preserve its identity. A separately
scheduled execution has a new identity even if order, article and settings are unchanged.

Corrugator `setupSettings.setupId` is unique within site/machine. Quality `setupRef` references
that identifier in the same context. Different machines may reuse a setup identifier; distinct
executions on one machine may not. Existing converting job/order/task references keep their
meanings. These definitions establish no queue or update-control protocol.

#### Setup Time Definition

**Setup time is measured from the last good sheet of the previous order to the first good sheet of the current order.**

This includes:
- Tool changes
- Machine adjustments
- Test runs and quality verification
- Material changeovers

### 4.5 Key Performance Indicators

The following indicators illustrate possible uses of COSI data. They do not prescribe
mandatory calculations or additional message fields.

#### Setup Efficiency

- **Actual vs. Target Setup Time**: Variance analysis
- **Setup Pattern Classification**: Categorization by complexity
- **Recipe/Setting Data**: Optimal parameter storage and retrieval
- **Forward Sequence Adherence**: Compliance with planned setup sequences

#### Process Stability

- Deviation detection from optimal settings
- Process weakness identification
- Best practice establishment
- Current machine setup documentation

### 4.6 Benefits

**Primary Benefits**

- **Downtime Reduction**: Minimize planned downtimes through efficient setup
- **Waste Reduction**: Fewer test sheets and material waste
- **Process Stability**: Consistent setup through documented best practices
- **Live Guidance**: Enable real-time setup assistance (e.g., instructional videos)
- **Pattern Analysis**: Identify and optimize common setup patterns

**Quality Improvements**

- Reduced variation in repeat setups
- Faster achievement of quality targets
- Improved first-good-sheet ratios

### 4.7 Data Requirements

Detailed datasets and field definitions live alongside the standard:

- **Corrugator setup payload** — [`schemas/setup-corrugator.schema.json`](../schemas/setup-corrugator.schema.json): setup settings, board grade, orders (scoring, preprint, stack settings and waste/side strips), periphery (single-facer, double-backer, fanfold, tape).
- **Converting setup payload** — [`schemas/setup-converting.schema.json`](../schemas/setup-converting.schema.json): job settings, article specifications, raw material, machine settings, periphery (flexo-print, digital-inkjet, die-cutter, folder-gluer, stitcher, taper, bundle-strapper, palletizer).
- **Envelope and enum values** — [`message-properties.md`](message-properties.md).

### 4.8 Setup Response

ERP/MES sends setup instructions (S1) using `setup-corrugator` or `setup-converting` on the
`receive` topic. The machine processes the request and returns `setup-response` on its `send`
topic. The response envelope's required `correlationID` is the original request's `messageID`.

- `result: OK` means the machine checked and applied the requested setup change in full.
  It does not guarantee production has started or will complete successfully.
- `result: NOK` means none of that request's changes were applied. `errors` contains one or
  more field errors, each with `fieldRef`, `description` and manufacturer-specific `manufacturerCode`.

`fieldRef` is an RFC 6901 JSON Pointer rooted at the **full original setup message**, for example
`/payload/orders/0/sheetWidth/value`. Array indices start at zero; `~` and `/` in property names
are escaped as `~0` and `~1`. Use the JSON string form, not a URI fragment or dotted path.
See [ADR-000006](../adr/ADR-000006-response-setup-schema-approach.md).

A missing result means the outcome is unknown. Retrying the unchanged request preserves its
assigned `messageID`; a machine that already processed it returns its original outcome without
applying the change again. Changed instructions or a request to reconsider a rejection get a
new `messageID`, even if they concern the same execution. Reusing an ID with changed content is
an error. Acceptance survives reconnect/restart: accepted work and its request association must
be preserved or recovered to prevent unintended repetition. Lost history must not turn an old
request into a new instruction. If state cannot be established reliably, affected remote changes
remain blocked until it is established and communicated. COSI v1.0 prescribes no new recovery
wire protocol, storage algorithm or retention period (§ 2.5).

The machine also publishes machine-side changed settings, including operator edits, on the
corresponding setup `send` topic (S2, § 4.3). This closes the loop so ERP/MES can learn from
adjustments. Setup and response messages must **not** use the MQTT retain flag.

Queue management is excluded from v1.0. Neither a queue snapshot nor queue admission serves
as the setup processing response; no queue insertion, ordering, deletion or update protocol is
specified here. Deferred material is preserved under [queue management](../ideas/queue-management/README.md).

### 4.9 Application Examples

The following examples illustrate application uses of data and context. They introduce no
additional message fields or interface requirements.

| Data or Context | Affected Area | Purpose |
|------------------|---------------|---------|
| Trigger values for setup | Whole Machine | Detect non-compliant setup sequences; identify time losses |
| Setting values over time | Whole Machine | Detect deviations; identify optimal settings per article |
| Periphery values | Periphery Equipment | Detect deviations; identify optimal peripheral settings |

---

## 5. Business Case: Maintenance

### 5.1 Overview

Maintenance data interfaces enable condition-based maintenance planning, reducing unplanned downtime and optimizing maintenance resource allocation through automated monitoring and predictive maintenance triggers.

### 5.2 Use Cases

Application-level reporting, analysis and planning use the exchanged data; their functionality
is not prescribed by COSI. The scope distinctions below apply to the data exchange.

| ID | Description | Expected Benefits | Status |
|----|-------------|-------------------|--------|
| M1 | Automatic generation of reports and warnings per customer, article, job | Reduced manual effort; expanded analysis and service capabilities | Out of scope |
| M2 | Interface to maintenance software for generating inspection/maintenance jobs based on runtime, events, and sensor thresholds | Optimized machine condition; fewer unplanned downtimes | In scope |

### 5.3 Key Concepts

#### Condition-Based Maintenance

**Monitoring Parameters**

- Motor power consumption
- Vibration analysis
- Temperature monitoring
- Usage counters (cuts, cycles, runtime)
- Operator experience feedback

**Predictive Maintenance Triggers**

- Runtime thresholds
- Event-based triggers
- Sensor limit violations
- Customer-specific tolerance settings
- Part/tool/auxiliary replacement indicators

### 5.4 Key Performance Indicators

The following indicators illustrate possible uses of COSI data. They do not prescribe
mandatory calculations or additional message fields.

#### Maintenance Efficiency

- **Planned vs. Unplanned Downtime Ratio**
- **MTBF** (Mean Time Between Failures)
- **MTTR** (Mean Time To Repair)
- **Maintenance Staff Utilization**
- **Preventive vs. Reactive Maintenance Ratio**

#### Cost Optimization

- Inventory cost reduction
- Optimized spare parts supply chain
- Improved SLA (Service Level Agreement) compliance
- Reduced emergency maintenance costs

### 5.5 Benefits

**Primary Benefits**

- **Simplified Workflows**: Automated maintenance job generation
- **Inventory Optimization**: Reduced spare parts inventory costs
- **Preventive Replacement**: Component replacement before failure
- **Optimized Supply Chain**: Better spare parts planning and SLA management
- **Reduced Downtime**: Fewer unplanned production interruptions
- **Resource Optimization**: Better utilization of maintenance staff

**Process Improvements**

- Realistic, condition-based maintenance schedules
- Clear maintenance instructions linked to specific tasks
- Integration of sensor data with operator knowledge
- Comprehensive documentation of maintenance activities

### 5.6 Data Requirements

Detailed datasets and field definitions live alongside the standard:

- **Maintenance document payload** — [`schemas/maintenance-document.schema.json`](../schemas/maintenance-document.schema.json): per-component manual links and recurring service task definitions with frequency triggers.
- **Maintenance measurement payload** — [`schemas/maintenance-measurement.schema.json`](../schemas/maintenance-measurement.schema.json): measured value vs. tolerance limits, fault classification (`faultCode`, `severity`), a required document-reference object with nullable fields when no link is available.
- **3-letter failure mode codes** — [`corrugated-faults.md`](corrugated-faults.md): closed set of 40 codes adapted from ISO 14224:2016, Annex B.
- **Envelope, severity enum, and reference fields** — [`message-properties.md`](message-properties.md).

Maintenance measurements report observations at the message timestamp; they do not define a
fault opening, update or clearance protocol.

### 5.7 Failure Severity Classification

Each maintenance measurement carries the required `failure` object, including `severity` (nullable as defined by the schema). Non-null severity supports operator attention and downstream alerting. The standard defines three levels — `info`, `warning`, `critical` — covering a spectrum from informational notifications through to immediate-action critical events that may trigger automatic machine stops.

For the value list and full definitions, see the *Failure severity* enum in [`message-properties.md`](message-properties.md).

---

## 6. Business Case: Quality

### 6.1 Overview

Quality data interfaces enable automated quality deviation detection and reporting, improving quality documentation and facilitating root-cause analysis.

### 6.2 Use Cases

Application-level reporting, analysis and planning use the exchanged data; their functionality
is not prescribed by COSI. The scope distinctions below apply to the data exchange.

| ID | Description | Expected Benefits | Status |
|----|-------------|-------------------|--------|
| Q1 | Detect quality deviations and generate automated quality reports | Reduced manual effort; expanded analysis and service capabilities | In scope |
| Q2 | Quality reports for customers, articles, and orders | Comprehensive quality documentation; customer transparency | In scope |

### 6.3 Key Concepts

#### Quality Deviation Categorization

Quality monitoring focuses on categorizing and clustering deviations to enable:

- Systematic root-cause analysis
- Corrective action tracking
- Experience value accumulation for planning
- Trend analysis across jobs, grades, and shifts

#### Good-Output Ratio Tracking

Measurement of good-sheet ratios across:

- Customer segments
- Board grades
- Production shifts
- Machine configurations
- Operator assignments

#### Reporting Cadence

A quality message at the **end of each job is mandatory**. Additional messages may be sent at
any time during the job; both use `cos` and the same payload structure. Each `checks` array item
is an atomic quality check with a counted outcome. Messages are not required to be complete or
cumulative job reports. The receiving application builds reports and handles aggregation and
repeated delivery; job-end cadence alone does not define a report-completion protocol.
In-process triggers/interval configuration and impact ratings remain deferred
([ADR-000001](../adr/ADR-000001-quality-message-end-of-job-mandatory.md),
[ADR-000002](../adr/ADR-000002-quality-check-structure-checks-array.md)).

Qualitative checks may report `OK` or `NOK` with null tolerance limits and null header `uom`
where no unit applies. Retain ejection information for NOK. Use `exception` only for a numeric
lower/upper-bound violation; omit it when no such bound was violated. Do not invent a numeric
reason for qualitative rejection. Missing checks or an empty checks array do not establish OK
output, and multiple failed checks can concern the same pieces.

### 6.4 Key Performance Indicators

The following indicators illustrate possible uses of COSI data. They do not prescribe
mandatory calculations or additional message fields.

- **Good-Sheet Ratio**: Percentage of production meeting quality standards
- **Deviation Categorization**: Classification by defect type and severity
- **Quality Evaluation**: Scoring and trending of quality metrics
- **Distribution Analysis**: Quality performance across jobs, grades, and shifts

### 6.5 Benefits

**Primary Benefits**

- **Experience Integration**: Feed quality data into production planning
- **Documentation Quality**: Improved error documentation accuracy
- **Root-Cause Analysis**: Systematic identification of quality issues
- **Corrective Actions**: Enable evidence-based improvements

**Process Improvements**

- Reduced quality-related waste
- Faster quality deviation response
- Improved customer satisfaction through documentation
- Data-driven quality improvement initiatives

### 6.6 Data Requirements

Detailed datasets and field definitions live alongside the standard:

- **Quality payload** — [`schemas/quality.schema.json`](../schemas/quality.schema.json): per-job quality checks grouped by production section (corrugating, folder-gluing, die-cutting, logistics, printing).
- **Quality Fields matrix** — see *Quality Fields* in [`message-properties.md`](message-properties.md) for quality concepts and illustrative units; payload field names and constraints are defined in the quality schema.
- **Envelope and common reference fields** — [`message-properties.md`](message-properties.md).

### 6.7 Quality Deviation Types

Quality deviations are organised into four categories:

- **Dimensional Quality** — geometric accuracy of sheets and stacks (warp, format, gaps, stack dimensions).
- **Material Quality** — physical and chemical characteristics of the substrate (moisture, temperature, raw-material verification, fishtailing).
- **Process Quality** — operational quality of converting steps (print defects, colour accuracy, registration, creasing, gluing).
- **Output Quality** — aggregate quality outcomes (waste-free ratio, first-good-sheet success rate).

The *Quality Fields* matrix in [`message-properties.md`](message-properties.md) relates these
categories to checks and application measures. The quality schema defines the transmitted fields
and their constraints.

---

## 7. Future Extensions

Additional interfaces and capabilities are outside COSI v1.0 unless explicitly defined in this
version. Ideas for future extensions can be submitted to the COSI working group by email or
through the [GitHub repository](https://github.com/vdw-da/COSI-Corrugated-Standard-Interface).
Proposals are retained in the repository's `ideas/` directory; they do not constitute a
commitment to inclusion or a delivery date.

---

## 8. Appendices

### Appendix A: Glossary and Allowed Values

The glossary and allowed values for all data fields are maintained in companion Markdown documents:

- **Glossary — Standard Terms**: `docs/glossary.md` — authoritative definitions for all terminology used in this document
- **Message envelope, payload, and enum values**: `docs/message-properties.md` — permitted values for all interface fields
- **Field naming and format rules**: `docs/naming-conventions.md` — camelCase, suffixes, units of measure, qualifier vocabulary

All manufacturers and end users must use these standardized terms and value sets consistently in documentation, interfaces, and KPI calculations to ensure interoperability.

---

### Commitment from the Industry

The following organisations have expressed their commitment to COSI 1.0.

| | | |
|:---:|:---:|:---:|
| ![BHS Corrugated Maschinen- und Anlagenbau GmbH logo](assets/industry/bhs.png) **BHS Corrugated Maschinen- und Anlagenbau GmbH** | ![BOBST Mex SA logo](assets/industry/bobst.png) **BOBST Mex SA** | ![DS Smith Packaging Deutschland Stiftung & Co. KG logo](assets/industry/dssmith.png) **DS Smith Packaging Deutschland Stiftung & Co. KG** |
| ![Dücker Conveyor Systems GmbH logo](assets/industry/duecker.png) **Dücker Conveyor Systems GmbH** | ![EMBA Machinery AB logo](assets/industry/emba.png) **EMBA Machinery AB** | ![ePS (eProductivity Software) logo](assets/industry/eps.png) **ePS (eProductivity Software)** |
| ![FEFCO AISBL logo](assets/industry/fefco.png) **FEFCO AISBL** | ![Fosber Group logo](assets/industry/fosber.png) **Fosber Group** | ![Göpfert Maschinen GmbH logo](assets/industry/goepfert.png) **Göpfert Maschinen GmbH** |
| ![Hans Kolb Wellpappe GmbH & Co. KG logo](assets/industry/kolb.png) **Hans Kolb Wellpappe GmbH & Co. KG** | ![Klingele Paper & Packaging SE & Co. KG logo](assets/industry/klingele.png) **Klingele Paper & Packaging SE & Co. KG** | ![Koenig & Bauer AG logo](assets/industry/koenigbauer.png) **Koenig & Bauer AG** |
| ![MINDA Industrieanlagen GmbH logo](assets/industry/minda.png) **MINDA Industrieanlagen GmbH** | ![Mitsubishi Heavy Industries EMEA, Ltd. logo](assets/industry/mhi.png) **Mitsubishi Heavy Industries EMEA, Ltd.** | ![Mondi AG logo](assets/industry/mondi.png) **Mondi AG** |
| ![OM Partners n.v. logo](assets/industry/omp.png) **OM Partners n.v.** | ![openpack GmbH logo](assets/industry/openpack.png) **openpack GmbH** | ![Palm Papierfabrik GmbH&Co KG logo](assets/industry/palm.png) **Palm Papierfabrik GmbH&Co KG** |
| ![SSH Software und Systemberatung GmbH logo](assets/industry/ssh.png) **SSH Software und Systemberatung GmbH** | ![THIMM Verpackung GmbH + Co. KG logo](assets/industry/thimm.png) **THIMM Verpackung GmbH + Co. KG** | ![Wilhelm Bahmüller Maschinenbau Präzisionswerkzeuge GmbH logo](assets/industry/bahmueller.png) **Wilhelm Bahmüller Maschinenbau Präzisionswerkzeuge GmbH** |
| ![WITRON Logistik + Informatik GmbH & Co. KG logo](assets/industry/witron.png) **WITRON Logistik + Informatik GmbH & Co. KG** |  |  |

**Names, logos and responsibility**

Company names and logos identify the listed organisations; all rights remain with
their respective owners. Inclusion grants no rights to reuse the logos and does not
constitute VDW endorsement or certification of any company, product or service.
VDW neither guarantees implementation, availability or performance nor undertakes
to fulfil the organisations' implementation commitments. Liability that cannot
lawfully be excluded or limited remains unaffected. Corrections or rights-related
concerns: [transparente-daten@vdw-da.de](mailto:transparente-daten@vdw-da.de).

---

## Revision History

| Version | Date | Author(s) | Changes |
|---------|------|-----------|---------|
| 1.0 (prepublication) | 1 November 2026 (planned) | Working Group / technical editors | Initial publication |

The [CHANGELOG](../CHANGELOG.md) is the authoritative record of what each version contains and what
changed between versions; this table carries the version identity of *this document*.

---

## Contact Information

**VDW Working Group "COSI"**  
Association of the German Corrugated Cardboard Industry e.V. (VDW)

For questions or feedback regarding this technical guide, please contact the VDW Working Group through official channels.

---

## License and Usage

This document is licensed under the Apache License, Version 2.0. See the repository
[LICENSE](../LICENSE) for the license text. Third-party company logos are excluded;
see the [logo ownership notice](assets/industry/NOTICE.txt).

---

[Imprint and Privacy Notice (Impressum / Datenschutz)](../IMPRINT-PRIVACY.md)
