# ADR-000025 — Publication imprint and privacy information

- **Status:** Accepted for publication structure and source preservation; legal text review pending
- **Date:** 2026-10-26
- **Decided by:** Maintainer, 2026-10-26
- **Source:** Maintainer request of 26 October 2026; external data protection adviser, email of 22 October 2026 at 16:37 and two supplied DOCX attachments, transcribed below with correspondence identities redacted
- **Asset class:** — (publication-wide; no protocol change)

## Context

VDW publishes COSI under [ADR-000020](ADR-000020-standard-named-cosi.md).
The [1 October publication decisions](2026-10-01-notes.md#b1-publication-timing)
and the decision register establish publication ownership and format. They do not
settle the legal notice or GitHub privacy information. The supplied advice identifies
missing information in the PDF imprint and requires privacy-policy updates and
clearly labelled links before external access is granted. This is a new publication
concern, complementary to those decisions; it does not supersede COSI licensing,
repository ownership, document authority, or technical approval.

## Decision

Maintain one English [Imprint and Privacy Notice](../IMPRINT-PRIVACY.md) in the
repository root, with clearly labelled links to VDW's official Impressum and
Datenschutzerklärung. Link it from the main README and the five publication-source documents under
`docs/`. Do not add generic legal-navigation footers to ADRs, meeting records, ideas
or the changelog; retain substantive source references where relevant. Preserve the German advice and attachment text in this ADR, with names and email
addresses removed from the correspondence; retain the unredacted source privately. Place the legal information on a dedicated single-column PDF page immediately
after the original imprint: cover on physical page 1, imprint/credits on page 2,
and “Impressum / Legal Notice” and “Privacy” on page 3. Retain the original imprint
layout and Markdown/JSON source-authority disclaimers. Omit the English draft label
and introductory translation/review paragraph from the notice; review status is
recorded in this ADR. A root-level notice avoids creating an
additional publication volume through the builder's automatic discovery of docs/*.md.

This accepts the maintainer's requested structure and implementation, not a legal
compliance certification or approval of new processing practices. The English notice
remains a draft pending VDW/data protection review. The supplied email requires VDW
to update its full privacy policy and establish GitHub-account links before external
linking/access. Repository footers and PDFs alone do not complete those external tasks.
The email separately promises a documented review of the data processing agreement;
it does not state that review has already been completed. No publication or access
change is authorized by this record.

## Amendment note — 26 October 2026: separate legal page

The maintainer rejected the dense two-column PDF preview and requested a second
front-matter page for “Impressum / Legal Notice” and “Privacy”, without the English
draft label or explanatory paragraph. This replaces the earlier clause combining
credits and legal text on physical page 2. The current layout is stated above;
the earlier 8.5 pt two-column layout is superseded. Removing presentation labels
does not resolve or approve the legal review findings below.

## Amendment note — 26 October 2026: limit navigation links

The maintainer narrowed the earlier instruction to link every Markdown file.
The current navigation scope is the main README and the five Markdown documents
converted to PDF. This supersedes the blanket footer requirement for ADRs, meeting
records, ideas and the changelog. Relevant references within this legal decision
remain. The dedicated legal page in all six PDFs and the external GitHub-account
linking follow-up are unchanged.

## Amendment note — 27 October 2026: redact correspondence identities

The maintainer instructed that names and email addresses be removed from this ADR.
This replaces the 26 October requirement to publish the original email in full:
the public record now preserves the German advice with role-based redactions,
while the unredacted transcription remains in private source evidence. The deciding
authority is recorded by role. Attachment text and fingerprints, accepted publication
structure and outstanding legal-review findings are unchanged. Required publisher
and contact information in the imprint remains public. This amendment does not
purge earlier Git history or authorise a remote repository change.

## Amendment note — 28 October 2026: six PDF volumes

The maintainer confirmed that the publication set comprises six PDF documents:
Technical Guide, Glossary, Naming Conventions, Message Properties, Corrugated
Faults, and Schemas and Samples. This replaces the earlier five-PDF count in the
publication workflow and decision register. The sixth volume is generated from
schemas and examples; there are still five publication-source Markdown documents.
The main README and those five Markdown sources retain legal-navigation links,
and all six PDFs include the legal page. Packaging requires six reviewed PDFs.
This count correction does not approve a particular PDF build or authorise release.

## Alternatives considered

**Keep only the existing PDF credits.** Rejected: the supplied advice expressly says
that those details do not cover all required information under section 5 DDG, and
credits do not explain GitHub or inquiry processing.

**Copy a complete independent website privacy policy into every document.** Rejected:
it would create multiple policy versions and import unrelated website processing.
A shared notice with links to the full VDW policy keeps the publication information
consistent; the two supplied supplements remain available in English.

**Silently repair ambiguous wording during translation.** Rejected: choosing a legal
basis or recipients would assert facts and policies not established by the sources.
Preserve meaning and submit concrete review findings separately.

## Consequences

**Positive**

- Readers can find publisher and privacy information from the main README and
  the publication documents.
- Redacted advice and source text remain self-contained and traceable.
- A shared PDF implementation applies the same legal information to all six volumes.

**Negative**

- Linked policies and publisher details require maintenance; PDFs are dated snapshots.
- The dedicated legal page adds one page to each publication.
- Translation and implementation cannot complete VDW's external policy/contract work.

**Follow-ups**

- VDW updates “Eigene Dienste” between “Audio- und Videokonferenzen” and “Unsere
  Social-Media-Auftritte”, and replaces “Anfrage per E-Mail, Telefon oder Telefax”,
  as instructed in the email; confirm the actual live result before external access.
- VDW establishes clearly labelled Impressum and Datenschutz links at GitHub-account /
  organisation level as well as repository level; verify unauthenticated accessibility.
- VDW/data protection adviser resolves the findings below and approves the English
  wording; record the resulting approved text and authority as an amendment here.
- Obtain the promised documented processing-agreement review for the actual GitHub
  account/product arrangement. Do not assert a signed/reviewed agreement without evidence.
- Review the imprint and legal pages in all six rebuilt PDFs, hyperlinks and source correspondence
  before replacing the approved publication PDFs.

## Review findings and unaccepted proposals

Assessment dated 26 October 2026. These are findings and proposed clarifications,
not accepted VDW processing rules or a determination of legal compliance.

1. **Imprint:** the attachments contain no imprint text. The English notice uses
   publisher identity, registered address, representative, register, VAT ID and
   electronic contact from the [official VDW imprint](https://wellpappen-industrie.de/impressum/),
   checked during this work. VDW should confirm that its scope explicitly covers the
   COSI GitHub presence. Its website copyright wording must not replace COSI's Apache
   License 2.0. [Section 5 DDG](https://www.gesetze-im-internet.de/ddg/__5.html)
   requires readily identifiable, directly accessible and permanently available
   provider information where applicable.
2. **Disclosure ambiguity:** “Diese Daten geben wir nicht ohne Ihre Einwilligung
   weiter” is followed by forwarding to working groups when necessary. Confirm
   whether recipients are internal authorised personnel or representatives of other
   organisations, what identifying data they need, and the basis for disclosure.
   If forwarding relies on consent, say “With your consent, we may forward …”.
   If a different lawful basis applies, replace the blanket consent promise with
   wording identifying the recipients, purpose and that basis. Neither option is
   adopted here; minimise or anonymise identifying details where feasible.
3. **GitHub legal basis and retention:** the GitHub supplement states purposes but
   does not identify VDW's legal basis or storage periods/criteria. Confirm these for
   access administration, collaboration and published contributions. If Article
   6(1)(f) applies, state the actual legitimate interest and provide the Article 21
   objection information. Do not automatically borrow the inquiry paragraph's basis.
4. **Complete information:** the two supplements are not a complete Article 13/14
   notice. Ensure the combined policy covers controller and applicable DPO contacts,
   recipients, transfers/safeguards, retention, rights including complaint/objection,
   any obligation to provide data and consequences, and any applicable automated
   decision-making information. See the [German supervisory authority's guidance](https://www.datenschutz.sachsen.de/informationspflichten.html).
   Whether Article 14 also applies depends on how personal data are obtained.
5. **GitHub roles and transfers:** the email describes VDW-provided accounts. GitHub's
   [privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)
   distinguishes organisation-provided accounts from processing where GitHub is
   controller. Confirm the actual account/product, contracting entity and agreement;
   avoid saying GitHub is exclusively a processor for every visitor. GitHub's statement
   describes DPF participation; independent verification of the supplied DPF registry
   entry was not possible in this check. Verify active coverage and the applicable
   transfer mechanism before release; certification alone does not complete VDW's duties.
6. **Public contributions and deletion:** explain visibility of identifying data in
   public issues, contributions and Git history if those features are used. Distinguish
   private inquiries from public submissions; explain applicable retention and limits
   to removing third-party copies. Do not promise erasure from every clone. This is
   a proposed policy clarification, not a decision to enable community features.
7. **Evidence still needed:** the VDW privacy page retrieved during this check did not
   expose a GitHub section. That is not proof that no update exists elsewhere or that
   the retrieved page is current. Obtain VDW confirmation and check the live page,
   account links and documented contract review before treating the email's work as done.

## Redacted email — German

Transcription of the email supplied by the maintainer. Names and email addresses
in the headers, greetings and signature are replaced with role labels.
Blank-line spacing is normalised; substantive advice is preserved. No original .eml or full mail
transport headers were supplied, so this is not represented as a byte-for-byte email archive.

```text
Von: [externe Datenschutzberatung; Name und E-Mail-Adresse entfernt]
Datum: Donnerstag, 22. Oktober 2026 um 16:37
An: [VDW; Name und E-Mail-Adresse entfernt]
Cc: [VDW; Name und E-Mail-Adresse entfernt]
Betreff: AW: Dokumente COSI 1.0

[Persönliche Anrede entfernt]

[Persönliche Anrede entfernt]

vielen Dank für den heutigen Telefonat sowie die Zusendung der Dokumente.

Im Hinblick auf den Zugriff externer Nutzer*innen sind Ihrerseits folgende Punkte zu berücksichtigen:

Datenschutzerklärung: Anbei finden Sie Zwei Absätze für die Datenschutzerklärung:

1.       Absatz „Nutzung von GitHub und Freigabe von Inhalten“: Bitte ergänzen Sie Ihre Datenschutzerklärung um den beigefügten Absatz unter der Kategorie „Eigene Dienste“. Platzieren Sie sie zwischen den Abschnitten „Audio- und Videokonferenzen“ und „Unsere Social-Media-Auftritte“.

2.       Bitte ersetzen Sie den Absatz „Anfrage per E-Mail, Telefon oder Telefax“ durch den von mir erstellten Text im Anhang. Damit werden die datenschutzrechtlichen Informationspflichten im Zusammenhang mit der Übermittlung von Fragen und Vorschlägen an die veröffentlichte E-Mail-Adresse abgedeckt.

Bitte ergänzen Sie Links zum Impressum (das Impressum in den Dokumenten enthält nicht alle erforderlichen Angaben gemäß § 5 DDG) und zur Datenschutzerklärung in Ihrem GitHub-Account. Wichtig ist, dass die Links mit „Impressum“ und „Datenschutz“ bzw. „Datenschutzerklärung“ bezeichnet sind oder aus der Beschriftung eindeutig hervorgeht, dass sie zu diesen Informationen führen.

Sobald Sie die entsprechenden Informationen in der Datenschutzerklärung ergänzt und die erforderlichen Verlinkungen eingerichtet haben, können Sie mit der Verlinkung der Inhalte und der Vergabe der Zugriffsrechte beginnen.

Ich werde den Auftragsverarbeitungsvertrag in Kürze auf die Einhaltung der datenschutzrechtlichen Anforderungen prüfen und die Prüfung entsprechend dokumentieren. Dies ist erforderlich, da VDW die GitHub-Accounts zur Verfügung stellt und GitHub insoweit als Auftragsverarbeiter für VDW agiert.

Bei Fragen stehe ich Ihnen jederzeit gerne zur Verfügung.

Viele Grüße

[Name entfernt]

i.A. [Name entfernt]

zert. Datenschutzbeauftragte (TÜV)
```

## Original attachments — German

The following paragraphs are extracted in document order from the supplied DOCX files.
Word formatting is not reproduced. SHA-256 values identify the original binary files;
the text below is self-contained and does not depend on private working files.

### Absatz DSE_Anfrage per E-Mail, Telefon oder Telefax ergänzt um GitHub_10-2026.docx

SHA-256: `fb7e1740dd029c20681f4abba29fce81fb4975f932dea1a8fa541ae5b5053423`

```text
Anfrage per E-Mail, Telefon oder Telefax
Wenn Sie uns per E-Mail, Telefon oder Telefax kontaktieren, wird Ihre Anfrage inklusive aller daraus hervorgehenden personenbezogenen Daten (Name, Anfrage) zum Zwecke der Bearbeitung Ihres Anliegens bei uns gespeichert und verarbeitet. Diese Daten geben wir nicht ohne Ihre Einwilligung weiter.
Beziehen sich Ihre Anfragen auf über GitHub bereitgestellte Dokumente oder Inhalte, können diese an die zuständigen Arbeitsgruppen weitergeleitet werden, sofern dies zur Prüfung oder weiteren Bearbeitung der Anfrage erforderlich ist. Anfragen, die nicht weiterbearbeitet werden, werden gelöscht.
Die Verarbeitung dieser Daten erfolgt auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage mit der Erfüllung eines Vertrags zusammenhängt oder zur Durchführung vorvertraglicher Maßnahmen erforderlich ist. In allen übrigen Fällen beruht die Verarbeitung auf unserem berechtigten Interesse an der effektiven Bearbeitung der an uns gerichteten Anfragen (Art. 6 Abs. 1 lit. f DSGVO) oder auf Ihrer Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) sofern diese abgefragt wurde; die Einwilligung ist jederzeit widerrufbar. Die von Ihnen an uns per Kontaktanfragen übersandten Daten verbleiben bei uns, bis Sie uns zur Löschung auffordern, Ihre Einwilligung zur Speicherung widerrufen oder der Zweck für die Datenspeicherung entfällt (z. B. nach abgeschlossener Bearbeitung Ihres Anliegens). Zwingende gesetzliche Bestimmungen – insbesondere gesetzliche Aufbewahrungsfristen – bleiben unberührt.
```

### Absatz DSE_Nutzung von GitHub_10-2026.docx

SHA-256: `2d0f2cf8465c939bf7199cc533432d5b8f4e54eab22a3f7c91d203f64b3eea94`

```text
Nutzung von GitHub und Freigabe von Inhalten
Wir nutzen die Plattform GitHub zur Bereitstellung, Verwaltung und Zusammenarbeit an digitalen Inhalten. Hierzu können bestimmte Repositories, Dateien, Dokumentationen und projektbezogene Informationen innerhalb unserer GitHub-Organisation gezielt für externe Nutzer freigegeben werden. Dabei können personenbezogene Daten verarbeitet werden (wie z.B. GitHub-Benutzername, E-Mail-Adresse), soweit diese in den freigegebenen Inhalten enthalten sind, im Rahmen der Nutzung der Plattform anfallen oder zur Erteilung einer Freigabe nötig sind. Die Verarbeitung erfolgt zum Zweck der Bereitstellung und gemeinsamen Nutzung der betreffenden Inhalte sowie der Zusammenarbeit mit externen Nutzern.
Anbieter der Plattform ist GitHub, Inc., USA. Details zu deren Umgang mit Ihren personenbezogenen Daten entnehmen Sie der Datenschutzerklärung von GitHub: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
Das Unternehmen verfügt über eine Zertifizierung nach dem „EU-US Data Privacy Framework“ (DPF). Der DPF ist ein Übereinkommen zwischen der Europäischen Union und den USA, der die Einhaltung europäischer Datenschutzstandards bei Datenverarbeitungen in den USA gewährleisten soll. Jedes nach dem DPF zertifizierte Unternehmen verpflichtet sich, diese Datenschutzstandards einzuhalten. Weitere Informationen hierzu erhalten Sie vom Anbieter unter folgendem Link:
https://www.dataprivacyframework.gov/s/participant-search/participant-detail?contact=true&id=a2zt0000000GnywAAC&status=Active

```

## References

- [English imprint and privacy notice](../IMPRINT-PRIVACY.md)
- [VDW Impressum](https://wellpappen-industrie.de/impressum/)
- [VDW Datenschutzerklärung](https://wellpappen-industrie.de/datenschutz/)
- [GitHub Data Protection Agreement](https://github.com/customer-terms/github-data-protection-agreement)
- [GDPR, Articles 6, 12–14, 21, 28 and 44–49](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)
