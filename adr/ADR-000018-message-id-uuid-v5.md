# ADR-000018 — `messageID` and `correlationID` are UUID version 5

**Implementation checkpoint — 14 October 2026:** Envelope descriptions, glossary and guide distinguish producer allocation from UUID format and preserve assigned IDs for retries/replays, including across restart. Earlier pending-alignment statements describe the prior recording stage. The aligned package was subsequently approved on 16 October 2026; see the [decision register](decision-register.md).

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decided by:** Working group, 2026-07-15
- **Source:** [2026-07-15 meeting notes](2026-07-15-notes.md) (minuted as M-0715-1)
- **Generation/retry clarification:** Maintainer, 2026-10-12 — distinct message instances need distinct identities; retries preserve the assigned identity
- **Asset class:** — (envelope, all asset classes)

## Context

The envelope identifiers were originally specified as UUID **version 3** (name-based, MD5). The
group revisited this on 2026-07-15. Version 3 and version 5 are both name-based and deterministic;
they differ in hash function — MD5 versus SHA-1.

Backward compatibility with systems already emitting v3 was raised as the one argument for staying,
but no concrete case was produced.

## Decision

`messageID` and `correlationID` are **UUID version 5** (name-based, SHA-1). Both fields are
constrained in `envelope.schema.json` by `format: uuid` plus a pattern pinning the version nibble to
`5` and the variant nibble to `[89ab]`.

## Consequences

- The version nibble is enforced, so a v3 UUID does not validate.
- The same namespace and name produce the same UUID. Producers must distinguish new message
  instances in their generation inputs and preserve the assigned ID on retries/replays.
  De-duplication depends on that preservation, not on UUID v5 alone (see clarification below).
- MD5 is not used for anything security-bearing here — the move to SHA-1 is about not specifying a
  broken hash, not about a threat model.

## Alternatives

- **Stay on v3.** Rejected: compatibility was mentioned but no clear use case was offered, and the
  standard is not yet released.
- **UUID v4 (random).** Not considered by the group. Preserving an assigned v4 ID would also
  support de-duplication; that fact does not change the accepted v5 choice.

## Amendment note — generation and retry consistency, 12 October 2026

During the setup-converting/connectionId discussion, the maintainer accepted the explanation
of UUID generation and instructed **“good, agreed. memorize consistency!”** This clarification
retains the working group's v5 decision and replaces the previous Consequences/Alternatives
claims that v4 cannot support de-duplication or that v5 alone supplies the required identity.

**A new message instance has a distinct `messageID`, even when its content matches an earlier
message. Retransmitting or replaying the same instance preserves its assigned `messageID`.**
Producers must maintain this distinction across restart. Using only the payload as the v5 name
cannot distinguish separate instances with identical content. Schema validation checks the
UUID representation/version; it cannot establish uniqueness across messages.

A unique producer namespace plus a persistent, never-reused message number illustrates how
an implementation can generate the IDs. This is an example, not a mandated storage or generation
algorithm. No universal namespace, counter format or receiver-side recomputation is prescribed
by this clarification. Request outcomes follow ADR-000006; transport recovery follows ADR-000010.

[ADR-000022](ADR-000022-mqtt-last-will.md) records UUID v5 for `connectionId` with the same
generation discipline, scoped to a connection rather than a message instance. Each record
remains authoritative for its own identifier; their different lifetimes are intentional.

Normative schema descriptions, examples, glossary, properties and guide implement this
clarification. This amendment records the maintainer’s October 12 confirmation.
See [RFC 9562 §§ 5.5 and 6.5](https://www.rfc-editor.org/rfc/rfc9562.html#section-5.5).
