# MiniHouse · Knowledge Acquisition Plan

Date: 2026-11-16 · Owner: lead engineering agent (Inge) · Status: proposed, ready to execute
Purpose: build PhD-level engineering, architecture and design competence specifically for MiniHouse — not generic reading.

---

## 0. What "PhD level" means operationally

Volume of reading is not the target. Competence is defined by five abilities, each with a pass gate:

1. **Derive from first principles** — reproduce the CG, reaction, beam, sling and torsion relations without looking them up; unit-check and limit-check every one.
2. **Navigate the code path** — for any verification, name the clause, the Norwegian National Annex and the limits of validity; say which coefficients cannot be fixed yet.
3. **Critique a source** — detect errors of the kind where the report's McAvoy precedent cites EN 1993-1-2 (fire) for joint design instead of EN 1993-1-8. Separate fact, manufacturer data and assumption.
4. **Verify numerically** — repeat governing cases in an independent solver with tolerances fixed *before* comparison; explain any disagreement.
5. **Synthesise into a decision** — turn knowledge into a defensible concept choice, labelled conceptual / calculated / tested / released.

Evidence of competence is a written memo per topic: derivation → numbers → provenance → limitations → falsifiable check. Nothing counts as "known" until its gate is passed.

---

## 1. Baseline already in the project

- **Research report** (`references/investigacion-estructural-casita-6x3.md`, 279 lines) plus the original PDF (`documents/…pdf`, 15 pp.; pp. 13–15 hold the real source URLs that the Markdown's `citeturn` markers replace).
- **Six role definitions and six skills** in `.agents/` — they already encode the working method and the prohibitions.
- **Fase 1 R0 deliverables** — decisions log, geometry, aperture table, three SVG plans, transport/lift worksheet, mass/CG calculator with passing self-test.
- **Verified anchors**: the 3,000 kg beam is hypothetical; four supports are not W/4; EN 13155:2020+A1:2025 is current; first-generation Eurocodes remain applicable in Norway until the second generation (~2028); transport width 2.55–3.25 m is the divisible-load band.

---

## 2. Domain map

| ID | Domain | Why it matters here | Priority |
|---|---|---|---|
| D1 | Mathematics & mechanics foundations | Derive every formula; understand what the ideal beam omits | 1 |
| D2 | Structural mechanics & steel design (EC3) | Chassis, members, stability, serviceability | 1 |
| D3 | Connections, joints & lifting details | Corner nodes and ears are where the concept can fail | 1 |
| D4 | Modular construction & DfMA | Transport/lift forces are additional design actions | 1 |
| D5 | Lifting, rigging, transport & infrastructure | Core problem of the project | 1 |
| D6 | Norwegian regulatory context | TEK17, NA, vegvesen, Arbeidstilsynet define legality | 1 |
| D7 | Architecture, building physics & design | Volumetric layout, cold-climate envelope, reclaimed timber | 2 |
| D8 | Numerical methods, FEM & tooling | Robot, independent solvers, Autodesk exchange, SolidCraft | 2 |
| D9 | Research method & verification | Makes the knowledge defensible and reproducible | 2 |

---

## 3. Staged collection plan (execute in this order)

### Stage 0 — Set up the knowledge base
Create `knowledge/INDEX.md`, `sources/`, `derivations/`, `critique/` and the source-card template (§4). Register the baseline report and PDF as `S000`/`S001` with their caveats. No external acquisition yet.

### Stage 1 — Foundations: mathematics, mechanics, FEM theory
**Objective:** derive, not memorize.

| Source | Type / access | Use |
|---|---|---|
| MIT OCW 3.11 Mechanics of Materials (Roylance) | free notes | Beam deflection; already cited by the report |
| MIT OCW 18.06 Linear Algebra (Strang) | free video/notes | FEM matrices, eigenvalue problems |
| MIT OCW dynamics / vibrations (1.050, 2.003) | free | Transport vibration, modal tests |
| learnaboutstructures.com free online textbook | free | Structural mechanics reference |
| Gere & Goodno, *Mechanics of Materials*; Hibbeler, *Mechanics of Materials* | paid reference — record, acquire lawfully | Standard undergraduate spine |
| Chopra, *Dynamics of Structures* | paid reference | Modal/dynamic analysis at depth |
| Fish & Belytschko, *A First Course in Finite Elements* | paid reference | FEM formulation, not just solver use |
| Timoshenko & Gere, *Theory of Elastic Stability* | paid reference | Buckling and second-order effects |

**Exit gate:** re-derive `δ_mid = (q/EI)[5(L−2a)⁴/384 − a²(L−2a)²/16]`; reproduce 24.634 mm (a=0) and 1.490 mm (a=1.2 m); explain in writing why Euler–Bernoulli cannot represent the module's torsion, joints and point loads.

### Stage 2 — Normative spine: codes and steel design
**Objective:** a clause-level map of every check the module needs.

| Source | Type / access | Use |
|---|---|---|
| EN 1990; EN 1991-1-1/-1-3/-1-4 | standards | Basis, combinations, actions, snow, wind |
| EN 1993-1-1, -1-3, -1-5, -1-8, -1-9 | standards | Members, cold-formed, plates, joints, fatigue |
| EN 1995; EN 1090-2:2018+A1:2024; CEN/TS 1090-201:2024 | standards | Timber, execution, steel reuse |
| Norwegian National Annexes (NS-EN …) | standards | Coefficients — currently unknown |
| JRC, *Design of Steel Buildings — Worked Examples* (`handbook3.pdf`) | free | Worked EC3 examples |
| steelconstruction.info — Design / Design codes and standards | free, current | Authoritative commentary, first-gen status |
| Jaspart & Weynand, *Design of Joints in Steel and Composite Structures* (ECCS/Wiley 2016/2017) | paid reference | Joint design in depth |

**Exit gate:** clause-path table for `M_Ed ≤ M_Rd`, `N_Ed ≤ N_b,Rd`, joint check and serviceability; list every γ/ψ still awaiting the NA; record the EN 1993-1-2 mis-citation as a critique entry.

### Stage 3 — Modular construction, connections, lifting details
**Objective:** understand the load path through a real module, not an ideal beam.

| Source | Type / access | Use |
|---|---|---|
| Lawson, Ogden & Goodier, *Design in Modular Construction* (CRC, 2014; verify 2nd ed. status) | paid reference | 40+ case studies; transport and lift actions |
| SCI P272, *Modular Construction using Light Steel Framing* | free PDF | Handling forces chapter |
| McAvoy / Queen's University Belfast lifting-system paper | free PDF — URL in report p. 13 | Prototype bracket tests to failure; six lift points |
| QUB full paper PDF (`pureadmin.qub.ac.uk/…153518889…pdf`) | free | Original method and failure modes |
| Springer 2025 chapter on modular steel column substructure | paper | Current connection research |
| Boothroyd & Dewhurst, *Design for Manufacture and Assembly* | paid reference | DfMA discipline |

**Exit gate:** draw the complete load path for one corner node; list at least eight local failure modes (net section, bearing, block tearing, plate bending, RHS wall, stiffeners, weld throat, eccentricity); write the high-lift vs base-lift comparison framework.

### Stage 4 — Lifting, rigging, transport, infrastructure
**Objective:** the physical operation and its legal frame.

| Source | Type / access | Use |
|---|---|---|
| EN 13155:2020+A1:2025 | standard | Non-fixed lifting attachments; spreaders/fatigue |
| EN 12195-1 | standard | Load securing, sliding/tipping/direct lashing |
| Forskrift om bruk av kjøretøy, cap. 5; Statens vegvesen veglister / VegSak; 2026 høring on weights & dimensions | official, free | Route, dispensation, width band |
| Arbeidstilsynet, forskrift om utførelse av arbeid | official, free | Lift planning obligations |
| Oceaneering / STM-type proof-load and NDT regimes | industry practice | Test planning model |
| DNV-ST-N001 (optional) | paid | Rigorous marine-lift methodology |

**Exit gate:** a lift-plan checklist distinguishing support / lashing / lift points; a four-leg unequal-distribution scenario; the rigging-angle sensitivity table (already sketched in `fase1/condiciones-transporte-izaje.md`) verified against `T = V/sin α`, `H = V·cot α`.

### Stage 5 — Architecture, building physics, design
**Objective:** a habitable, buildable, cold-climate module — not just a chassis.

| Source | Type / access | Use |
|---|---|---|
| Ching, *Form, Space, and Order*; *Building Construction Illustrated* | paid reference | Spatial and construction fundamentals |
| Mallgrave (ed.), *Architectural Theory* | paid reference | PhD-level theory survey |
| Maggi, *Structure and Architecture* | paid reference | Structural–architectural integration |
| Hens, *Building Physics*; SINTEF/Byggforskserien details | paid / subscription | Heat, air, moisture in cold climate |
| Banham, *The Architecture of the Well-tempered Environment*; Olgyay, *Design with Climate* | paid reference | Environmental design lineage |
| TEK17 chapters on energy, moisture, fire, acoustics (DIBK) | official, free | Applicable requirements |

**Exit gate:** a short architectural brief for the 6 × 3 m module — spatial strategy, cold-climate envelope build-up, three moisture failure mechanisms and the details that prevent them, and a reclaimed-timber traceability approach.

### Stage 6 — Norwegian regulatory context (parallel with 2, 4, 5)
Collect DIBK TEK17, NS-EN national annexes, Byggforskserien, Statens vegvesen and Arbeidstilsynet material into a compliance matrix with status *verified / pending*, source URL and access date. Re-check the first-vs-second-generation Eurocode timeline before any coefficient is used.

### Stage 7 — Tools and verification chain
**Objective:** make the knowledge executable.

| Source | Use |
|---|---|
| Autodesk official docs: Robot SDK/API, Advance Steel COM/.NET, SMLX sync limits, AutoCAD, Revit/IFC, APS Data Management | Confirm what can and cannot be automated; SMLX is not a perfect twin |
| PyNite, Frame3DD, CalculiX, Code_Aster, IfcOpenShell docs | Independent verification stack |
| SolidCraft docs/CLI/MCP | Parametric R0 geometry, STEP/IGES/DXF exchange |
| Python NumPy / SciPy / pandas / matplotlib | Reproducible calculation and plotting |

**Exit gate:** mass calculator self-test passes; a parametric R0 model exists in SolidCraft; a written Robot ↔ Advance Steel bar-exchange test procedure includes the mandatory before/after difference table; environment limitations (no live connectors) recorded.

### Stage 8 — Synthesis, critique and competence gates
| Source | Use |
|---|---|
| Booth, Colomb & Williams, *The Craft of Research* | PhD-level argument and evidence standards |
| *The Turing Way* (free online) | Reproducible computational work |
| ASME V&V / Oberkampf guidance | Model validation language |
| Hevner et al., design science research methodology | Structuring design decisions |

**Exit gate:** one memo per domain containing derivation, evidence, limitations and a falsifiable check; a consolidated *known / assumed / unknown* register; updates to `PROJECT.md` and `fase1/` as real answers arrive.

---

## 4. Capture system

```
knowledge/
  INDEX.md                 master index: domain, priority, reading state, gate status
  sources/S000.md …        one card per source
  derivations/D000.md …    formulas derived from first principles, with unit checks
  critique/caveats.md      source errors, inappropriate references, validity limits
  comparisons/             Robot vs independent solver; IFC vs analytical model
```

Source-card template:

```text
id | title | author | year | type | edition | URL or ISBN
access: OA / paid / library / to-acquire        license:
key claims (3–6):
formulas:
limits and caveats:
used_in: [project decisions / files]
verified_by:        date:
```

Derivation-card template: `statement → assumptions → derivation → unit check → numerical check → where it is valid / where it fails`.

---

## 5. Priority and integrity rules

1. Project-relevant before general; D1–D6 before D7–D9.
2. Primary sources (standards, original papers, official docs) before commentary.
3. Free and verifiable before paywalled. Paywalled books are recorded as *to acquire* with ISBN — never copied illegally. Lawful library access is preferred.
4. Some search results were aggregators in other languages; they are leads only. Every source must be confirmed at its official domain before it enters the register.
5. Every claim carries provenance **and** condition of application (`rules.md` §3).
6. No source is "known" until its stage exit gate is passed.

---

## 6. Explicit limits

- I produce engineering work; I am not a licensed engineer. Fabrication release, structural sign-off and authorisation of a real lift remain with the qualified human authority (`rules.md` §5).
- Reading a book is not competence. Only gated, written derivations and verifications count.
- No copyrighted full text will be stored without lawful access; metadata and open-access sources only.

---

## 7. Immediate next action

1. Scaffold `knowledge/` and register the baseline report + PDF.
2. Start Stage 1 (foundations) and Stage 2 (codes) in parallel — both are needed before any Fase 2 calculation.
3. Request from Carlos: answers to C-01…C-09 in `fase1/registro-decisiones.md`, and confirmation of lawful access to the paid references (or preference for open-access substitutes).
