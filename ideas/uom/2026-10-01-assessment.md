# Imperial support — scope and effort for the October 1 decision

**Current disposition — 14 October 2026:** Historical assessment: the October 1 decision retained metric-only v1.0 and imperial deferral to v1.1. ADR-000013 controls; the pending-decision wording below preserves preparation history.

**Status:** assessment, 2026-09-29. Prepared for working-group discussion; the decision above supersedes the proposal below.
The current published draft remains metric-only under ADR-000013 until the group revises it.

## Assessment

A narrowly scoped extension could be relatively inexpensive in this repository. Quantities
already carry `uom`, so allowing selected imperial/US customary units does not inherently
require new message types or a different payload structure. Actual integration effort depends
on whether producers and consumers already interpret `uom` or assume fixed metric units.

Do not equate accepting more strings with interoperable imperial support. The unit vocabulary,
field meanings, validation and consumer obligations need an agreed scope. No implementation
time estimate or consumer-readiness verification has been completed.

## Current repository evidence

A scan on 2026-09-29 found **17 unit constraint locations across four schema files** that
include metric units. Shared definitions apply to multiple fields. These are review locations,
not a count of mandatory changes: electricity may continue using Wh, for example.

| Schema | Locations to review |
|---|---:|
| `common-types.schema.json` | 1: shared `QuantityMM` |
| `setup-corrugator.schema.json` | 4: grammage, scoring dimensions, speed, running length |
| `setup-converting.schema.json` | 6: forces, glue amount, panel dimensions, grammage |
| `performance.schema.json` | 6: water, electricity, steam, air, speed, die force |

Other quantities use a free-string `uom` or carry metric meaning only in their descriptions.
Quality and maintenance therefore also need review, even when an imperial string already passes
validation. Existing schema acceptance does not override the metric-only rule in the guide.

## A limited implementation path for discussion

1. Keep `uom` as the authoritative unit per value or quantity group. All values in a group
   continue to share its unit. A new envelope-level unit-system flag is not required merely
   to support additional units; decide it separately if the group needs it.
2. Agree a short list of permitted units for each relevant physical quantity. Candidate pairs
   include mm/in, m/min/ft/min and g/m²/lb/MSF. Keep existing counts and other suitable units.
3. Extend the relevant constraints and shared quantity definitions. Review names and descriptions
   such as `QuantityMM` and `gsm` so they do not imply that the numeric value always uses metric
   units when `uom` says otherwise. Document the chosen meaning without gratuitous field renames.
4. State how receivers handle supported units and unsupported units. Existing metric messages
   should remain valid; that alone does not make new imperial messages usable by old receivers.
5. Align the guide, naming rules, unit reference, examples and ADR-000013. Validate metric and
   imperial examples across applicable message types, and test incorrect physical units and
   numerical equivalence after conversion.

This limited path does not require adopting every feature in the older unit-system drafts,
such as a general dimension catalogue, extra unit aliases or UN/CEFACT annotations.

## Decisions that determine risk and cost

| Decision | Why it matters |
|---|---|
| Exact unit list | “Imperial” is not an unambiguous symbol catalogue. US and UK volume units differ, and BTU variants exist; specify the actual supported units. |
| Per-value units versus one system per message | Existing messages are already labelled per value/group. A global flag introduces another declaration whose consistency must be defined. |
| Quantity versus field name | Die-pressure fields in this repository use kN, a force; their counterpart must preserve force, not change to pressure. The field `gsm` also needs clear interpretation if carrying lb/MSF. |
| Conversion responsibilities | A sender, adapter or consumer must handle conversion where required. Temperature conversion includes an offset; a single multiplicative factor is not universal. |
| Consumer support | A consumer written against `uom: mm` as a constant may reject or misinterpret inches. Producer-to-consumer compatibility must be checked, including both setup directions. |
| Validation coverage | Widening a few enums does not fix fields whose units are unconstrained or implied only in prose. Review applicable units consistently without expanding this into unrelated redesign. |

Unit-definition and conversion reference: [NIST SP 811, Appendix B.8](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8).

## Older drafts need revision before adoption

The existing `support-both-on-wire.md` fork proposes a new `unitSystem` flag, a broad dimension
catalogue and no cross-validation of the flag against field units. It uses `oz/ft²` for grammage
rather than the newly confirmed `lb/MSF` and contains stale spellings and relative schema-reference
examples. Its claim of compatibility establishes that old metric examples can still validate;
it does not establish that existing consumers can process new imperial values. These drafts are
design inputs, not implementation-ready or newly approved policy.

## Requested group outcome

Decide whether to retain metric-only for v1.0 or approve a limited native imperial/US customary
extension. If approving the extension, agree its unit list, receiver obligations, owner and
validation required before publication. Record any amendment to ADR-000013 explicitly.
Approval of `lb/MSF` spelling by the maintainer on September 29 does not by itself authorize imperial messages.
