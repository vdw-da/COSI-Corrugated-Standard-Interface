# ADR-000023 — Performance quantity meanings

- **Status:** Accepted by maintainer; aligned package approved by André Seifert, 2026-10-16
- **Date:** 2026-09-12
- **Recorded as ADR:** 2026-10-14
- **Decided by:** Maintainer, 2026-09-12; stack and scope clarifications, 2026-10-13
- **Source:** Maintainer-confirmed quantity definitions and October 13 confirmations, consolidated from the local definition review without changing their meaning
- **Asset class:** `performance`; related setup and quality quantity descriptions

## Context

Counters, event quantities and current inventory describe different things. Treating every
message as additional production, or treating requested setup settings as measured output,
produces incorrect totals. These existing field meanings require one permanent decision record.

## Decision

| Quantity | Meaning |
|---|---|
| Input/output production and consumption counters | Cumulative readings within a defined scope and counting period |
| Event quantities | The material associated with one identified event; repeated delivery does not create another event |
| Logistics quantities | Current contents at the identified location and observation time |
| A piece | One discrete material/product unit at the identified counting point; the counting basis stays consistent within its scope and period |
| `stackCount` | Sheets per stack, in `pcs` |
| `stackHeight` | Physical stack height, in `mm` |
| Performance `stacks` | Number of physical stacks, interpreted as a cumulative counter or current contents according to its field location |

Compare or combine quantities only when scope, period, unit and counting basis are compatible.
A message trigger does not change a field's quantity meaning. A COS inventory reading is not
additional production. Requested setup values do not establish actual material quantities.

Counter continuity belongs to its defined scope and period, not to an article change alone.
A reset starts a new counting period. Close the previous period with its final total when known;
if it is unavailable, identify that period as incomplete rather than treating the missing total
as zero. A late closing total completes the earlier period without counting already reported
quantities again. Current measurements and inventory need not increase monotonically.

Measured consumption belongs to the scope where it was measured. A calculated job allocation
identifies the source total, period and allocation rule. Allocations plus any identifiable
unassigned remainder reconcile to that total, allowing for rounding; they are subdivisions,
not additional consumption. Machines may report only the measured total. COSI prescribes no
universal allocation formula or mandatory job-allocation capability.

Output classification concerns the same material at the same counting point. Good, rejected
and unclassified quantities are non-overlapping and together form total output for compatible
scope, period and unit. Missing quality information is not evidence of good output. This
meaning does not introduce new classification fields or a correction protocol.

Three physical stacks of 200 sheets contain 600 pieces; `stackCount` is 200, not three.
Two actual stacks of 200 and 80 sheets contain 280 pieces. Use actual quantities and participating
outs; a setup target multiplied by configured outs is not proof of actual output.

## Scope and provenance

The maintainer confirmed the counter, allocation, piece, classification and sheets-per-stack
meanings on September 12. On October 13, the maintainer confirmed physical stack height in
millimetres and performance counts of physical stacks. Those clarifications replace the former
incorrect schema descriptions of stackCount as a number of stacks and stackHeight in pieces.

The maintainer excluded manual repeated-processing accounting from v1.0 on October 13.
Machines are not required to recognize manually refed sheets or adjust their counters for
that action. Operator-entered accounting belongs to an MES/shop-floor application when needed;
COSI does not prescribe that application's workflow.

This record consolidates accepted meanings already applied in the schemas and
[Technical Guide §3.5](../docs/technical-guide.md#35-data-requirements).
It adds no fields, sensors, allocation capability, correction operation or delivery guarantee.
Setup execution identity and responses are governed by
[ADR-000006](ADR-000006-response-setup-schema-approach.md); setup excludes production actuals
under [ADR-000005](ADR-000005-remove-actuals-from-setup.md).
