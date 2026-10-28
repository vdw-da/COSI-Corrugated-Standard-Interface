# ERP/MES (IT) Last Will — idea for the next version

**Status:** outside COSI v1.0; parked for the next version by the maintainer on 2026-10-01.
**Decision:** [ADR-000022](../../adr/ADR-000022-mqtt-last-will.md).

COSI v1.0 includes optional Last Will for **OT equipment**. Standardized Last Will
notifications for **ERP/MES (IT) clients** are a future extension.

## Purpose

Allow interested equipment or monitoring systems to receive an ERP/MES client's
connection-loss notification. An ERP/MES client can serve multiple machines or sites,
so the extension needs an IT-system identity and an appropriate topic arrangement.

## Questions for the next version

- How to identify an ERP/MES client and its scope across sites and equipment.
- Which availability topic and message representation to use.
- How interested equipment and monitoring systems discover and subscribe to that topic.
- What optionality, publication settings, reconnect and freshness rules apply.

A shared IT-system availability topic is a possible approach discussed during preparation.
No topic name, schema or distribution design is approved by this deferral.

The deferral concerns IT Last Will notifications. Persistent sessions and offline delivery
follow [ADR-000010](../../adr/ADR-000010-bidirectional-east-west-only.md#delivery-and-reconnection).
