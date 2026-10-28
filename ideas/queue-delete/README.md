# Queue delete — deferred design fragments (ADR-000008)

**Current scope:** excluded from v1.0 by the working group on October 1. On October 14 the
maintainer confirmed the name `queue-delete`, alongside `queue`. The renamed sketches below
preserve unapproved historical payload alternatives; naming does not approve a protocol or
restore this capability to v1.0. See ADR-000008's dated naming clarification.

Two candidate shapes for the 2026-07-20 decision
(*"queue.json add 'deleterequest' as status, array of setupRefID or jobRefID to be deleted"*).
Nothing here is part of the standard yet — see [ADR-000008](../../adr/ADR-000008-delete-request.md).

## Historical Option A — extend the queue payload

Queue message doubles as command channel via a payload-level discriminator.
⚠ Conflicts with ADR-000007 retained-state semantics (a retained deleterequest replays on reconnect).

```json
// queue.schema.json payload (sketch)
{
  "queueStatus": "deleterequest",
  "deleteList": [
    { "setupRef": "SETUP-2026-0882" },
    { "jobRef": "JOB-2026-1104" }
  ]
}
```

With `queueStatus: "snapshot"` (default) the payload carries `queueList` as today.

## Historical Option B — separate `queue-delete` asset class (earlier recommendation)

Non-retained `cos` message, MES/ERP → machine. The machine confirms by re-publishing the retained
queue snapshot.

```json
// envelope (new assetClass value: queue-delete)
{
  "messageID": "…uuid v5…",
  "assetClass": "queue-delete",
  "messageType": "cos",
  "machineId": "CORR-LINE-01",
  "timestamp": "2026-08-19T09:00:00.000Z",
  "status": "run",
  "payload": {
    "deleteList": [
      { "setupRef": "SETUP-2026-0882" },
      { "jobRef": "JOB-2026-1104" }
    ]
  }
}
```

```json
// queue-delete.schema.json payload (sketch)
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "cosi:queue-delete-payload:1.0",
  "title": "COSI — Delete Request Payload",
  "type": "object",
  "required": ["deleteList"],
  "additionalProperties": false,
  "properties": {
    "deleteList": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "oneOf": [
          { "required": ["setupRef"] },
          { "required": ["jobRef"] }
        ],
        "properties": {
          "setupRef": { "type": "string", "minLength": 1, "description": "Setup to remove from the machine queue." },
          "jobRef":   { "type": "string", "minLength": 1, "description": "Job whose queued setups are to be removed." }
        },
        "additionalProperties": false
      }
    }
  }
}
```
