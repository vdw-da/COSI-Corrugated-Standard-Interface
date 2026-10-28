# ADR-000026 — Publish industry commitment names without implementation schedules

- **Status:** Accepted publication scope; additional responsibility wording prepared for legal review
- **Date:** 2026-10-26
- **Decided by:** Maintainer (André Seifert), 2026-10-26
- **Source:** Maintainer request to publish the company names from `20261026_COSI_Committment_overview_V 3.xlsx`, with logos where available, as an appendix before the Technical Guide revision history
- **Asset class:** — (publication-wide; non-normative)

## Context

The maintainer supplied a commitment overview containing organisation names and
implementation-related information. The publication should identify industry support
without disclosing the accompanying schedules, retrofit details or internal remarks.
The overview records expressions of commitment, not completed implementations or
certification. FEFCO is an industry association, so the collective label is
“organisations” rather than describing every entry as a company.

[ADR-000020](ADR-000020-standard-named-cosi.md) establishes COSI's identity and VDW's
publisher role. The [October publication decision](2026-10-01-notes.md#b1-publication-timing)
controls official publication. [ADR-000025](ADR-000025-publication-imprint-and-privacy.md)
controls legal information and navigation. None determines how industry commitments
are presented; this decision complements them without changing their authority.

## Decision

Add a non-normative appendix page headed **Commitment from the Industry** immediately
before **Revision History** in the Technical Guide. Publish only the organisation
names selected from rows whose **COSI 1.0 Commitment** value is **Yes**, accompanied
by identifiable company/group logos where available. Include all qualifying rows,
including those outside the workbook's saved filter range. The supplied version has
22 qualifying entries. Sort the displayed names alphabetically; normalise incidental
whitespace and stray trailing punctuation without changing the named entities.
Apply the company-supplied Palm correction recorded below to its displayed name
and logo; the original workbook remains unchanged as historical source evidence.

The [Technical Guide appendix](../docs/technical-guide.md#commitment-from-the-industry)
is the canonical displayed list. It presents expressions of commitment to COSI 1.0,
not promises of availability, completed implementation, product approval or
certification. No implementation dates, roadmap milestones, retrofit statements,
status colours, conditions, contact details or internal remarks are copied into
public documents, logo metadata, image descriptions or PDF metadata. The source
workbook remains private; do not publish it or convert its worksheets to an image.

Use source artwork rather than generated or redrawn logos, preserve its proportions,
and record asset provenance in [the logo source inventory](../docs/assets/industry/sources.json).
A group/brand logo identifies the workbook's named entity; it does not expand that
entity's commitment to other group companies. Third-party logos remain outside the document's Apache licence grant, as stated
in the asset ownership notice. Names remain selectable text in the PDF. Render the appendix as a single page, with revision history starting on the
following page. This is a publication presentation change, not a protocol requirement
or authorization to publish the repository or replace reviewed release PDFs.

## Amendment note — 26 October 2026: names, logos and responsibility

The maintainer requested an additional protective statement concerning VDW's role
in publishing company names and logos. This amends the presentation of the existing
appendix, not its membership or the earlier exclusion of implementation schedules.
The short two-sentence appendix footer is replaced by a notice identifying ownership,
limiting the meaning of the listing, distinguishing the organisations' commitments
from VDW's obligations, and providing a corrections/rights contact. The former
no-availability/no-certification meaning is preserved in the expanded wording.

**Authority and status:** the maintainer authorised adding a protective notice on
26 October 2026. The text below is the assistant-prepared wording for VDW's legal
review; no approval by VDW's legal adviser or determination of enforceability is
recorded. It appears in the review preview without adding a draft label to the PDF.
The publication decision remains accepted; this wording's legal review is outstanding.

### Wording prepared for review

Company names and logos identify the listed organisations; all rights remain with
their respective owners. Inclusion grants no rights to reuse the logos and does not
constitute VDW endorsement or certification of any company, product or service.
VDW neither guarantees implementation, availability or performance nor undertakes
to fulfil the organisations' implementation commitments. Liability that cannot
lawfully be excluded or limited remains unaffected. Corrections or rights-related
concerns: transparente-daten@vdw-da.de.

### Scope and limits

A severability clause deals with the consequences of invalid contractual provisions;
it does not establish logo-use rights. A blanket statement that VDW has no
responsibility for names or logos is not adopted. VDW's own publication activity and
applicable liability remain subject to law. The notice does not establish permission
to reproduce artwork, validate an inaccurate listing, or replace checking the actual
basis for logo use. No company indemnity or contractual waiver is inferred.

[Section 23 MarkenG](https://www.gesetze-im-internet.de/markeng/__23.html) permits
certain identification/reference uses subject to honest commercial practices; it
is not an unrestricted permission for every logo presentation. Logo artwork may
also be protected by copyright; [section 31 UrhG](https://www.gesetze-im-internet.de/urhg/__31.html)
addresses grants of usage rights. [Section 276(3) BGB](https://www.gesetze-im-internet.de/bgb/__276.html)
prevents advance release from liability for intentional conduct in its contractual
scope. These sources support avoiding a blanket exemption, not a conclusion that
this notice resolves all legal issues. VDW's adviser should check the wording and
the actual publication/brand-use circumstances before release.

## Amendment note — 26 October 2026: Palm company correction

**Authority:** the maintainer relayed Palm’s updated company name and supplied JPEG
on 26 October 2026. For Palm’s existing entry only, **Palm Papierfabrik GmbH&Co KG**
replaces the workbook-derived **Palm Industrie Beteiligungs-GmbH**, and the supplied
“Palm Packaging” artwork replaces the previously retrieved website logo. The old
name and artwork are superseded for the current publication. This is a correction
to the existing listing, not an additional organisation or an expansion of commitment.
The other 21 entries and the exclusion of implementation schedules are unchanged.

The supplied JPEG is converted to PNG without altering its pixels or proportions
for the established PDF pipeline. Its source fingerprint and the published asset
fingerprint are recorded in the logo source inventory. The original workbook is
retained as provenance; the maintainer-relayed correction controls Palm’s current
published identity. This does not resolve the separate legal-review follow-ups.

## Source provenance

Workbook: `20261026_COSI_Committment_overview_V 3.xlsx`.
Worksheet: `COSI Commitments`. Selection: organisation names in column A where
column B is `Yes`; 22 entries. The saved filter range does not cover the entire list.

SHA-256 of the original workbook:
`5cfe0e946ee000fa8bfc8376e040184ce9995bd0cc15a40b0b057d61ec724e9a`.

This fingerprint preserves provenance without making the public decision depend on
a private file or disclosing the excluded columns. The maintainer's supplied list
is the authority for inclusion; finding a logo online is not evidence of commitment.

## Alternatives considered

**Publish the complete overview or a worksheet screenshot.** Rejected: it exposes
implementation information the maintainer explicitly excluded and could turn
qualified planning statements into apparent public delivery promises.

**Publish names only.** A valid fallback when suitable artwork cannot be verified,
but logos improve recognition and were requested where available. Keep full names
alongside logos so similar brands and group identities do not obscure the listed entity.

**Treat the list as a certified implementation catalogue.** Rejected: the source
establishes commitments, not conformity testing or current product availability.

## Consequences

**Positive**

- Readers can identify participating organisations on one appendix page.
- Delivery planning and internal review information remain private.
- Exact names and logo provenance are reviewable independently of the private workbook.

**Negative**

- Logos and organisation identities can change and need publication review.
- Group logos may be broader than the legal entity named in the workbook.
- A one-page layout constrains logo size and requires layout review when the list grows.

**Follow-ups**

- Review the full appendix, alphabetical order, name fidelity, logo association and
  placement before revision history in the rebuilt Technical Guide.
- VDW obtains legal review of the additional responsibility notice and verifies
  appropriate brand usage for publication. No separate company logo
  permission or endorsement beyond the supplied commitment list is claimed here.
- Most artwork was obtained from the organisations' own sites on 26 October 2026.
  WITRON's direct website retrieval was blocked: the AEB partner-hosted logo was
  visually compared with WITRON's official brochure, page 7. The brochure is dated
  2022; current brand approval for that fallback remains to be confirmed. The source
  inventory records this exception rather than claiming a current official download.
- Preserve the private original and the selection evidence; future membership changes
  require an updated source and a dated amendment, not inference from website logos.

## References

- [Technical Guide appendix](../docs/technical-guide.md#commitment-from-the-industry)
- [Logo sources and retrieval details](../docs/assets/industry/sources.json)
- [Logo ownership notice](../docs/assets/industry/NOTICE.txt)
- [WITRON official brochure used for visual comparison](https://witron.de/fileadmin/user_upload/flyer/ma_aio_flyer_en.pdf)
