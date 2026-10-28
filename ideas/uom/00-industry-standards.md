# 00 — Industry standards for units & dimensions

There is no shortage of prior art. We do not need to invent anything; we need to pick which standard to align with and what to expose on the wire.

## The five candidates

### 1. ISO 80000 — *Quantities and units*

What the project already implicitly references (`m`, `kg`, `°C`, `m²`, `Wh`, etc.).

- **Defines:** quantities (length, mass, temperature…), their dimensions, and recommended unit symbols.
- **Strength:** Human-readable. The symbols we already use.
- **Weakness:** No machine-parseable code list; no formal "this symbol belongs to this dimension" assertion that a JSON Schema can consume directly. We would build that ourselves.
- **Imperial:** Outside scope — ISO 80000 is SI-first. Imperial units appear only as conversion examples.

### 2. UCUM — *Unified Code for Units of Measure*

The gold standard in HL7 / FHIR. Extremely comprehensive; covers SI, imperial, customary, traditional. ~1000+ codes.

- **Codes look like:** `m`, `m/s`, `[ft_i]/min` (imperial foot per minute), `[degF]`, `kg.m2/s2`.
- **Strength:** Machine-parseable, expression algebra (you can build `kg.m/s2` from atoms), wide imperial coverage.
- **Weakness:** Bracketed imperial syntax (`[ft_i]`, `[degF]`) is ugly. Overkill for an industrial machine-data feed. Tooling outside healthcare is patchy.
- **Imperial:** Yes, first-class.

### 3. UN/CEFACT Recommendation 20 — *Codes for Units of Measure used in International Trade*

3-letter codes maintained by UNECE. Used in EDI, e-invoicing, customs, **and crucially OPC UA `EUInformation`** — the de-facto standard for unit codes in industrial automation.

- **Codes look like:** `MTR` (metre), `KMH` (km/h), `KGM` (kilogram), `WTT` (watt), `WHR` (watt-hour), `FOT` (foot), `FTM` (foot per minute), `LBR` (pound), `FAH` (°F), `MTK` (m²), `MMT` (millimetre).
- **Strength:** This **is** what corrugator / converting OEMs emit on OPC UA today. Adoption already exists upstream. Imperial coverage is solid. Stable, governed.
- **Weakness:** Opaque to humans (`KMH` is fine, `WTT` is not). No expression algebra — only registered codes work.
- **Imperial:** Yes, first-class.

### 4. QUDT — *Quantities, Units, Dimensions and Types*

RDF/OWL ontology. Defines `qudt:QuantityKind` (the dimension), `qudt:Unit` (specific units), conversion factors, and the relationship between them.

- **Strength:** This is exactly the "dimension binding" the team is asking for, formalized. You can say "this field is `qudt:Width` (kind = Length)" and the legal units fall out automatically.
- **Weakness:** Semantic-web stack. JSON-LD or full RDF tooling at the consumer. Heavy for a machine-data feed.
- **Imperial:** Yes, first-class.

### 5. OPC UA `EUInformation` + ISA-95

Not a unit standard itself — it's the **transport** that the automation world has already converged on. Internally it carries UN/CEFACT Rec 20 codes.

- **Codes:** UN/CEFACT (see #3).
- **Relevance:** Every PLC, every OPC UA server, every MES tagged with units uses this. If our standard takes JSON messages downstream of an OPC UA layer, the cheapest path is to mirror what the OPC UA side already says.

## Comparison

| Standard | Format | Imperial | Dimension model | Adoption in our sector |
|---|---|:---:|---|---|
| ISO 80000 | `m/min`, `°C` | weak | informal | high (human-facing) |
| UCUM | `[ft_i]/min` | strong | implicit via algebra | low (healthcare) |
| UN/CEFACT Rec 20 | `KMH`, `WTT` | strong | none (flat code list) | **high (OPC UA, ISA-95, EDI)** |
| QUDT | URIs | strong | explicit (`qudt:QuantityKind`) | low (semantic web) |
| OPC UA `EUInformation` | wrapper around #3 | strong | none | **highest in automation** |

## What this implies for us

- **Keep ISO 80000 symbols on the wire for readability** — they're what implementers expect to *see*, and the docs already use them.
- **Borrow QUDT's dimension *concept*** (the `QuantityKind` idea) but not its RDF tooling — implement dimension binding as a flat catalog in `docs/units.md`.
- **Offer UN/CEFACT codes as an alternate** for consumers that want to round-trip with OPC UA without translation tables. This could be a per-field annotation in the schema (`x-uncefact: "KMH"`), not in the payload.
- **Skip UCUM.** Too healthcare-shaped, ugly imperial syntax.
- **Don't adopt JSON-LD / QUDT URIs.** Heavy and unfamiliar to the implementer audience.

The recommendation in [`06-recommendation.md`](06-recommendation.md) builds on this: ISO 80000 symbols stay primary; dimensions are introduced as a *catalog concept* (QUDT-flavoured but flat); UN/CEFACT codes appear only as a schema-side annotation for downstream interop.
