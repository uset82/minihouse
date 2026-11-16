# MiniHouse · Known / Assumed / Unknown register

Date: 2026-11-16. Status after executing the knowledge acquisition plan. Maps to rules.md §2 (measured / manufacturer / assumed) and §3 (provenance + condition of application).

## KNOWN (verified at primary source or derived and checked)

| Item | Basis | Where |
|---|---|---|
| Beam formulas M_A, M_mid, δ_mid (ideal symmetric overhang) | SymPy derivation, numbers reproduced | D001, verify_beam.py |
| Sling geometry T=V/sinα, H=V·cotα and 4-leg indeterminacy | derived + numeric check | D003, verify_rigging.py |
| EN 1993 part identities (1-2 fire, 1-8 joints, 1-9 fatigue…) | JRC official page | S004, C001 |
| TEK17 §10-2 requirement: strength/stiffness/stability during execution and final state; documented materials | DIBK official text | S005 |
| Eurocode generations: first to March 2028, second early 2028 | SCI (UK source) | S003 |
| QUB test data: 17.5 kN design load, 6 lift points, failure modes, peak loads/CoV | primary paper, full text | S007 |
| SCI P272: 20% inset lift points, base-lift corner damage risk, dynamic factor requirement, full-plan spreader preferred | primary guide, full text | S008 |
| SCI P272 UK transport limits are not applicable to Norway | source caveat | S008, C002 |
| VegSak dispensation workflow, §5 weights/dimensions, vegliste/Vegkart | Statens vegvesen official | S009 |
| Moisture control four-condition principle + drying mechanisms | Lstiburek & Straube | S010 |
| Example mass calculator self-test passes | executed | scripts/masas_cg.py |
| Model's illustrative numbers are hypothetical, not module data | derived + report | C003 |
| TEK17 §14-3 minimum U-values and airtightness | DIBK official | S011 |
| TEK17 §14-2 småhus energy frame 100+1600/A and measure route | DIBK official | S011 |
| TEK17 §13-2 ventilation rates and §13-13 vapour barrier Sd≥10 m | DIBK official | S012 |
| Arbeidstilsynet crane training (>2 tm) and competent control of lifting gear | Lovdata official | S013 |
| Norwegian NA texts are paywalled — hard access blocker | investigation | S014 |
| Market = Norway, mainly Bergen; use = emergency cabin | Carlos, 2026-11-16 | fase1 section F |
| Reference images show a gable roof (R0 monopitch superseded as intent) | Carlos images + fase1 section F | S016 |

## ASSUMED (working values, must not drive design)

| Item | Value | Source |
|---|---|---|
| S-01…S-08 geometry assumptions | H=3200, clear=2400, bathroom at x=0–1200, no collaborating walls, etc. **S-03 monopitch superseded by declared gable intent; pitch unknown** | fase1/registro-decisiones.md, section F |
| 3,000 kg / EI=1.68 MN·m² / q=2.4525 kN/m beam example | illustrative only | S000, C003 |
| Example mass inventory | 2,200 kg, CG (2.545,1.471,0.741) — explicitly "NO ES DATO DEL PROYECTO" | fase1/inventario-masas-ejemplo.csv |
| 20% inset (1.2 m) as lift point candidate | SCI recommendation for LGS modules; not yet justified for this chassis | S008, lift-variants.md |

## UNKNOWN (blocking, with owner/question)

| Item | Blocked by | Effect |
|---|---|---|
| Exact Bergen site, legal use classification, final dimensions, salients | C-01 (partial), C-02 | TEK17 class, snow/wind, geometry freeze |
| Route, transport frequency, trailer | C-03, C-06 | vegliste check, fatigue, lashing, dynamics |
| Crane, radius, hook height, lift company | C-04 | lift variant, spreader, plan |
| Final support type and ground | C-05 | reactions, settlement, anchorage |
| Equipment masses, tanks, batteries | C-07 | mass/CG → all calculations |
| Reclaimed timber quantity, species, state | C-08 | envelope mass, traceability |
| Original dimensioned sketches (images are intent only) | C-09 (partial) | no dimensions may be taken from renders |
| Norwegian National Annex coefficients (γ, ψ, α…) | paywalled (S014) | no code verification possible |
| NS 3031:2014 energy calculation method | purchase | cannot verify §14-2 energy frame |
| Remaining TEK17 §13 sections (thermal/radon/sound/rain/wet rooms) | retrieval | detail design |
| Specific written lift-plan paragraph | not located in §§10/13 | do not claim a paragraph number |
| Architecture theory books (Ching, Mallgrave, Maggi) | to acquire | visual/spatial design depth |
| Steel section, plate thickness, weld, ear detail | Fase 2/3 | no fabrication |
| Autodesk exchange test result | no product access | interface stays pending |

## State

All engineering outputs remain **conceptual**. Nothing here releases geometry for fabrication or authorises a lift (rules.md §5).
