# MiniHouse · Knowledge base index

Plan: [docs/knowledge-acquisition-plan.md](../docs/knowledge-acquisition-plan.md). Created 2026-11-16.

## Domains and stage status

| ID | Domain | Stage | Gate | Status |
|---|---|---|---|---|
| D1 | Mathematics & mechanics foundations | 1 | re-derive beam formula + 24.634 / 1.490 mm | **PASSED** (D001, 2026-11-16) |
| D2 | Structural mechanics & steel design (EC3) | 2 | clause-path table, NA unknowns listed | **PARTIAL** — clause map done; NA values confirmed paywalled/blocked (S014) |
| D3 | Connections, joints & lifting details | 3 | full load path + 8 failure modes | **PASSED** — D002, 12 modes (2026-11-16) |
| D4 | Modular construction & DfMA | 3 | lift comparison framework written | **PASSED** — lift-variants.md (2026-11-16) |
| D5 | Lifting, rigging, transport, infrastructure | 4 | lift-plan checklist + angle table verified | **PASSED** — D003 + lift-plan-checklist.md (2026-11-16); real plan still blocked on C-01…C-09 |
| D6 | Norwegian regulatory context | 6 | compliance matrix verified/pending | **SUBSTANTIALLY CLOSED** — TEK17 §13-2/9/13, §14-2/3 and Arbeidstilsynet §§10-1/2/3, 13-1/3 verified; NA texts paywalled, NS 3031 & minor §13 sections pending |
| D7 | Architecture, building physics, design | 5 | module brief + moisture mechanisms | **PASSED at requirements level** — brief + TEK17 numeric limits (S011/S012) incorporated; NS 3031 energy calc & theory books pending |
| D8 | Numerical methods, FEM, tooling | 7 | selftest + R0 model + exchange procedure | **PASSED as prepared** — selftest OK, r0-model.json, exchange procedure written (2026-11-16); actual exchange still PENDING (no Autodesk access) |
| D9 | Research method & verification | 8 | per-domain memos + known/assumed/unknown register | **PARTIAL** — memos + register + Turing Way (S015); Craft of Research / Hevner / ASME V&V to acquire |

## Sources

| id | title | type | access | gate | notes |
|---|---|---|---|---|---|
| S000 | Engineering research report, 6 × 3 m transportable module (Markdown, 279 lines) | report | local | — | Working copy; `citeturn` markers replace real URLs |
| S001 | Same report, original PDF (15 pp.) | report | local | — | pp. 13–15 contain the full source list |
| S002 | Introduction to Structural Analysis | free textbook | open web | — | learnaboutstructures.com; 11 chapters |
| S003 | Steel Construction Info — Design codes and standards | UK guidance | open web | — | Eurocode structure/timing only; UK NA NOT valid for Norway |
| S004 | JRC — Eurocode 3 official page | standard index | open web | — | authoritative EN 1993 part list |
| S005 | DIBK — TEK17 §10-2 Konstruksjonssikkerhet | regulation | official, free | — | execution + final state requirement |
| S006 | JRC — Jaspart & Weynand, Design of joints | book/guide | to acquire lawfully | — | EN 1993-1-8 authoritative guide |
| S007 | QUB/McAvoy lifting-system paper (CERI 2018) | paper | open access, PDF local | — | 6 lift points, 17.5 kN design, tests to failure |
| S008 | SCI P272 — Modular Construction using Light Steel Framing | guide | free PDF local | — | 20% inset lift points; UK transport limits NOT valid for Norway |
| S009 | Statens vegvesen — VegSak special transport dispensation | official | open web | — | dispensation via VegSak, §5 weights/dimensions |
| S010 | Building Science — Moisture Physics (Lstiburek & Straube) | presentation | free PDF local | — | 4-condition moisture test; ventilation drying |
| S011 | DIBK — TEK17 §§14-2/14-3 Energy | regulation | official, free | — | U-values, air leakage, energy frame — NUMBERS |
| S012 | DIBK — TEK17 §§13-2/13-9/13-13 Indoor climate | regulation | official, free | — | airflow rates, Sd≥10m vapour barrier — NUMBERS |
| S013 | Lovdata — forskrift om utførelse av arbeid §§10-1/2/3, 13-1/3 | regulation | official, free | — | crane training, competent control of lifting gear |
| S014 | Norwegian National Annex access investigation | finding | — | — | NA values paywalled — hard blocker |
| S015 | The Turing Way — reproducible research | book (open) | open access | — | research compendium principles |
| S016 | Carlos's reference images (ChatGPT renders) | images | local | — | intent only: gable roof, Bergen context; NOT dimensioned |
| S017 | ESTA — Lifting Operation Risk Management Guide GD25001-EN | industry guidance | free PDF local | — | not law; load data, stability triangle, engineered lift-plan drawings |
| S018 | DIBK — Rules for mikrohus til boligformål | regulation guidance | official, free | — | conditional on legal use classification; 30 m² BRA, 4.5 m, 2.2 m etc. |
| S019 | NS-EN 1090-2 access status | standard finding | paywalled/unavailable | — | steel execution clauses not available; no EXC/weld claims |

## Derivations

| id | statement | status |
|---|---|---|
| D001 | Symmetric overhanging beam: M_A, M_mid, delta_mid | **verified** — symbolic + numeric, sign convention documented |
| D002 | Corner lifting-node load path and 12 failure modes | **established** from S007/S006/S000 |
| D003 | Sling geometry and four-leg distribution | **verified** — symbolic/numeric script, table reproduced |

## Critique

| id | issue | status |
|---|---|---|
| C001 | McAvoy precedent cites EN 1993-1-2 (fire) for joint design; correct part is EN 1993-1-8 | **confirmed** at JRC primary source (S004) |
| C002 | steelconstruction.info NA guidance is UK-only | recorded |
| C003 | 3,000 kg beam numbers are hypothetical, not module data | confirmed by D001 |

## Comparisons / reports

| file | contents |
|---|---|
| clause-map.md | EC3 clause-path map, Norwegian NA unknowns |
| lift-variants.md | I-1 vs I-2 framework and McAvoy test method |
| lift-plan-checklist.md | requirements checklist (not an authorised plan) |
| module-brief.md | architectural and building-physics brief |
| compliance-matrix.md | Norwegian compliance, verified/pending by row |
| autodesk-exchange.md | SMLX / IFC exchange procedure, environment status |
| r0-model.json | parametric R0 geometry generated by scripts/r0_parametric.py |
| known-assumed-unknown.md | consolidated K/A/U register |
| ../competence-memos.md | per-domain PhD-level capability check |
| ../docs/plan-diseno-construccion.md | revised design/construction plan mapping the ChatGPT draft into canonical Fase 0–4 |
| r1-gable-options.json | parametric gable-roof sensitivity: 5/10/15/20°, ridge height, area, loaded-height and wind screening; no selection |
| ../fase1/r1-opciones-techo.md | readable R1 gable-roof sensitivity report generated from that model |
| ../fase1/solicitud-datos.md | prioritised P0/P1/P2 questionnaire for C-01…C-09 |

## Rules

- No claim enters the index without provenance and condition of application.
- Paywalled works are listed as *to acquire*, never copied unlawfully.
- Aggregator results are leads only; confirm at official domains.
- A domain is "known" only when its exit gate in the plan is passed.
