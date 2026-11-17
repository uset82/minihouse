# MiniHouse · Knowledge base index

Plan: [docs/knowledge-acquisition-plan.md](../docs/knowledge-acquisition-plan.md). Created 2026-11-16.

## Domains and stage status

| ID | Domain | Stage | Gate | Status |
|---|---|---|---|---|
| D1 | Mathematics & mechanics foundations | 1 | re-derive beam formula + 24.634 / 1.490 mm | **PASSED** (D001, 2026-11-16) |
| D2 | Structural mechanics & steel design (EC3) | 2 | clause-path table, NA unknowns listed | **PARTIAL** — clause map done; NA values confirmed paywalled/blocked (S014) |
| D3 | Connections, joints & lifting details | 3 | full load path + 8 failure modes | **PASSED** — D002, 12 modes (2026-11-16) |
| D4 | Modular construction & DfMA | 3 | lift comparison framework written | **PASSED** — lift-variants.md (2026-11-16) |
| D5 | Lifting, rigging, transport, infrastructure | 4 | lift-plan checklist + angle table verified | **PASSED** — D003 + lift-plan-checklist.md + lift-geometry-screen.md (2026-11-17); real plan still blocked on C-01…C-09 |
| D6 | Norwegian regulatory context | 6 | compliance matrix verified/pending | **SUBSTANTIALLY CLOSED** — TEK17 Chapter 13 route map (S023), Chapter 11 fire route (S024), Chapter 12 admitted set (S025), Chapter 7 hazard classes (S026) and Chapters 9/15/16/17 (S027, S028) and Chapters 2/4 (S029), §14-2/3/5 and Arbeidstilsynet §§10-1/2/3, 13-1/3 verified; no hazard map, ground investigation or site check yet; NA texts paywalled and now a documentation blocker too (S029); §2-2(3) margin statement outstanding, NS 3031 route-dependent, C-01 classification pending |
| D7 | Architecture, building physics, design | 5 | module brief + moisture mechanisms | **PASSED at requirements level** — brief + TEK17 numeric limits (S011/S012/S023/S024/S025/S026/S027/S028), §13-7 daylight, §12-7 room-height and §14-3/§13-13 envelope screens incorporated; NS 3031 energy calc, real material data and theory books pending |
| D8 | Numerical methods, FEM, tooling | 7 | selftest + R0 model + exchange procedure | **PASSED as prepared** — selftest OK, r0-model.json, exchange procedure, mass readiness/sensitivity tool, R1 geometric skeleton generator (2026-11-17); actual exchange still PENDING (no Autodesk access) |
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
| S012 | DIBK — TEK17 §§13-2/13-9/13-13 Indoor climate | regulation | official, free | — | §13-9/13-13 numbers retained; §13-2 rates verified but NOT applicable to mikrohus route (see S023) |
| S013 | Lovdata — forskrift om utførelse av arbeid §§10-1/2/3, 13-1/3 | regulation | official, free | — | crane training, competent control of lifting gear |
| S014 | Norwegian National Annex access investigation | finding | — | — | NA values paywalled — hard blocker |
| S015 | The Turing Way — reproducible research | book (open) | open access | — | research compendium principles |
| S016 | Carlos's reference images (ChatGPT renders) | images | local | — | intent only: gable roof, Bergen context; NOT dimensioned |
| S017 | ESTA — Lifting Operation Risk Management Guide GD25001-EN | industry guidance | free PDF local | — | not law; load data, stability triangle, engineered lift-plan drawings |
| S018 | DIBK — Rules for mikrohus til boligformål | regulation guidance | official, free | — | conditional on legal use classification; 30 m² BRA, 4.5 m, 2.2 m etc. |
| S019 | NS-EN 1090-2 access status | standard finding | paywalled/unavailable | — | steel execution clauses not available; no EXC/weld claims |
| S020 | DIBK — TEK17 §1-2 application to specific measures | regulation/guidance | official, free | — | detached ≤30 m², holiday home, temporary building routes; C-01 branch point |
| S021 | DIBK — TEK17 §14-5 and §14-4 energy exceptions | regulation | official, free | — | §14-2 excluded for detached ≤70 m²; correction to earlier MiniHouse energy note |
| S022 | Statens vegvesen — Directive 96/53/EC dimensions summary | official PDF | free PDF local | — | general height 4.00 m screening; not a route permit |
| S023 | DIBK — TEK17 Chapter 13 sections applicable to mikrohus route | regulation | official, free | — | §13-1(1), §13-4/5/7, §13-9…13-16 apply; §13-2/3/6/8 do not; ventilation scope correction |
| S024 | DIBK — TEK17 Chapter 11 fire safety for a single-storey dwelling | regulation | official, free | — | risk class 4 / BKL 1; R 15 under §11-4(3) no. 4; escape windows, detection, extinguishing, fire-service access |
| S025 | DIBK — TEK17 Chapter 12 layout, sections applicable to the mikrohus route | regulation | official, free | — | only 8 provisions apply; 2.4 m room height and all accessibility rules exempt; 2.2 m from §12-7(2)(c) |
| S026 | DIBK — TEK17 Chapter 7 safety against natural hazards | regulation | official, free | — | flood F1/F2/F3 and landslide S1/S2/S3; MiniHouse is F2 (1/200) and S2 (1/1000); quick-clay regime below the marine limit; §7-4 not a route for a private cabin |
| S027 | DIBK — TEK17 Chapter 9 external environment | regulation | official, free | — | §9-2 has no manufacturer-free route, so reclaimed timber has no documented compliance instrument; §9-3 is a second siting gate; §9-6's 10-tonne limb cannot be crossed by building the cabin, only by aggregation |
| S028 | DIBK — TEK17 Chapters 15, 16 and 17 installations, lift control, climate | regulation | official, free | — | no small-building exemption anywhere in chapter 15; §15-6/§15-8 0.90 m head is a minimum burial depth; chapters 16 and 17 and §§15-2/15-9…15-15 not applicable |
| S029 | DIBK + Lovdata — TEK17 Chapters 2 and 4 documentation and FDV | regulation | official, free | veiledning for §§2-2/2-3/2-4/4-2 **not retrieved** (DIBK pages returned navigation only) | §2-2(2) allows analysis only where no ytelse is given; §2-2(3) sets the admissibility test for every screen; §4-1(2) exemption rejected for this building; FDV must be a versioned, site-specific file |

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
| C004 | Earlier MiniHouse notes applied §13-2 ventilation rates to the mikrohus route | **corrected** — S023 limits that route to §13-1(1) functional ventilation |

## Comparisons / reports

| file | contents |
|---|---|
| clause-map.md | EC3 clause-path map, Norwegian NA unknowns |
| lift-variants.md | I-1 vs I-2 framework and McAvoy test method |
| lift-geometry-screen.md | normalized sling angles/lengths and T/W, H/W for corner vs 20% inset layouts, I-1/I-2, plus a mass-to-tonnes view that shows the ranking is mass-independent; no variant selected |
| lift-geometry-screen.json | machine-readable companion to the lift geometry screen |
| lift-plan-checklist.md | requirements checklist (not an authorised plan) |
| module-brief.md | architectural and building-physics brief |
| compliance-matrix.md | Norwegian compliance, verified/pending by row |
| autodesk-exchange.md | SMLX / IFC exchange procedure, environment status |
| r0-model.json | parametric R0 geometry generated by scripts/r0_parametric.py |
| known-assumed-unknown.md | consolidated K/A/U register |
| ../scripts/mass_sensitivity.py | C-07 readiness check and CG/reaction sensitivity ranking; no project masses invented |
| ../competence-memos.md | per-domain PhD-level capability check |
| ../docs/plan-diseno-construccion.md | revised design/construction plan mapping the ChatGPT draft into canonical Fase 0–4 |
| r1-gable-options.json | parametric gable-roof sensitivity: 5/10/15/20°, ridge height, area, loaded-height, inverse 4.00 m eave envelope and wind screening; no selection |
| r1-frame-skeleton.json | geometric node/member skeleton for all four R1 pitches; 32 nodes and 59 members per option, no sections or masses |
| ../fase2/miembros-R1-opciones.csv | machine-readable member table generated from the R1 skeleton |
| ../fase2/miembros-R1-opciones.md | readable summary of the R1 geometric skeleton |
| daylight-check.json | TEK17 §13-7 simplified-route screening: qualifying glass, LT/frame-factor scenarios, minimum LT |
| fire-check.json | TEK17 Chapter 11 screening: classification, R 15, escape-window pass/fail per aperture, surface and insulation classes, extract duct, detection, extinguishing, fire-service access |
| ../scripts/fire_check.py | reproducible Chapter 11 screen; escape-window dimensions, door free width, separation threshold |
| room-height-check.json | TEK17 §12-7 room-height trade-off: eave vs 2.2 m coverage vs transport height, floor build-up swept |
| ../scripts/room_height_check.py | reproducible §12-7 screen; largest pitch for full-width 2.2 m per stack and floor build-up |
| natural-hazard-screen.json | TEK17 chapter 7 screening: F1–F3/S1–S3 probabilities, flood datum sensitivity to sea-level rise, infinite-slope FS grid, 50 kPa ceiling |
| ../scripts/natural_hazard_screen.py | reproducible chapter 7 screen; class probabilities, required FFL, slope FS with no pass state |
| envelope-check.json | TEK17 §14-3/§13-13 screening: layered U-values with the ventilated-layer rule, stud parallel-path penalty, minimum insulation thickness, Glaser moisture profiles for four barrier qualities |
| ../scripts/envelope_check.py | reproducible envelope screen; U-value, stud penalty, thickness solver, steady-state Glaser |
| section-feasibility.json | integrated cross-section: max wall height per pitch/stack/floor/roof, full-coverage pitch cap, lever inversion, floor-area penalty |
| ../scripts/section_feasibility.py | reproducible section solver; ridge geometry with t/cos θ, coverage, lever analysis |
| section-options.json | four R2 section options: pitch, stack, limit, wall height, band and low-zone widths, loft check, tolerance to a 100 mm reserve |
| ../scripts/section_options.py | reproducible options generator; each option solved against the same section model |
| instalaciones-check.json | TEK17 chapters 9/15/16/17 screening: applicability map with four determinations, §9-6 waste-plan switch and cabin-mass sweep, §15-6/§15-8 backflow head as a minimum burial depth, stove and chimney chain |
| ../scripts/instalaciones_check.py | reproducible installations screen; waste-plan limbs, backflow inversion, stove limits, chimney chain |
| documentacion-check.json | TEK17 chapter 2/4 audit: §2-2(2) ytelse-vs-function gate, §2-2(3) admissibility matrix across thirteen screening reports, §2-3/§2-4 stages, §4-1 FDV list and exemption test |
| ../scripts/documentacion_check.py | reproducible documentation audit; state/limits/basis gates, margin observation, §4-1 exemption determination |
| puentes-termicas.json | thermal-bridge screen: §14-3 sets no bridge limit, 61.10 m junction inventory, Ψ″ per detailing level, compensation cost in mm, size effect 18→150 m² |
| ../scripts/puentes_termicas.py | reproducible bridge screen; junction inventory, normalised Ψ″, compensation in insulation millimetres, benchmark inverse |
| condensacion-union.json | junction condensation screen (ISO 13788): f_Rsi per construction, critical factor, required added resistance, condensation/mould thresholds, corner and humidity sensitivity |
| ../scripts/condensacion_union.py | reproducible f_Rsi screen; temperature factor, critical factor inverse, required thermal break in m²K/W |
| cubierta-incendio.json | roof under chapter 11: four §11-4(3) branches with the invariant insulation class, EN 1995-1-2 charring residual sections, timber-fraction geometry, section cost |
| ../scripts/cubierta_incendio.py | reproducible roof determination; branch invariance, charring and d0, rafter width vs centres, insulation thickness |
| ventanas.json | escape windows §11-13 priced against daylight §13-7: three readings, the cheapest set satisfying each, the union set, the equal-minimum aperture band, daylight relief and heat cost |
| ../scripts/ventanas_check.py | reproducible window screen; §11-13 qualification imported from fire_check, qualifying glass from daylight_check, three readings solved and priced |
| incertidumbre.json | margin adequacy under §2-2(3): four kinds of uncertainty, three sweeps (wall U vs framing, section vs timber fraction, Ψ″ vs detailing), and the adequacy verdict per row |
| ../scripts/incertidumbre.py | reproducible adequacy test; sweeps the three computable rows and states the kind for the rest |
| puente-2d.json | 2D conduction at the floor-edge junction (ISO 10211): mesh validation, six variants, the pad sweep, Ψ per metre, and the cost of putting the steel inside |
| ../scripts/puente_2d.py | reproducible 2D solver; finite volumes with Robin films, 1D reproduction, flux conservation, mesh convergence, f_Rsi and Ψ |
| estrategia-incendio.json | chapter 11 determinations and their coupling: which clauses are engaged by the safe-place/rømningsvei question, the two packages priced, §11-9 shown independent, travel distance |
| ../scripts/estrategia_incendio.py | reproducible determination map; clause engagement per package, window cost imported from ventanas_check, door figures from fire_check |
| ventilacion.json | §13-1(1) ventilation: documented alternative rates, extract schedule, the pressure a sealed envelope imposes, stove combustion air, barrier penetrations |
| ../scripts/ventilacion_check.py | reproducible ventilation screen; rate arithmetic from §13-2, leakage-pressure inversion, fan deliverability, flue margin |
| aporte-aire.json | make-up air sizing: orifice areas against design depression, wind holdability, flue adequacy, tempering load, diffusion share of the barrier |
| ../scripts/aporte_aire.py | reproducible make-up air screen; orifice law, bisection against envelope leakage, the buildable/adequate intersection test, heat and diffusion shares |
| ../fase1/verificacion-luz-diurna.md | readable daylight screening report from the current aperture table |
| ../fase1/verificacion-incendio.md | readable fire screening report from the current aperture table |
| ../fase1/verificacion-instalaciones.md | readable installations screening: applicability map, waste-plan switch, backflow burial depth, stove/chimney chain |
| ../fase1/verificacion-documentacion.md | readable documentation audit: the §2-2(2) gate, the §2-2(3) matrix, and why §2-2(4) is unsatisfied by construction |
| ../fase1/verificacion-puentes-termicas.md | readable thermal-bridge report: no limit on the applying route, junction inventory, what ordinary detailing costs, compensation priced in millimetres, why the benchmark is mis-specified at 18 m² |
| ../fase1/determinacion-cubierta-incendio.md | readable roof determination: the four branches converge on mineral wool, R 15 costs a 78 mm rafter, and the timber fraction is a geometry result |
| ../fase1/verificacion-condensacion-union.md | readable junction condensation report: bare steel condenses below 6 °C, mould governing over condensation, and why the 1D requirement of 0.358 m²K/W was 0.44 short of the 2D one |
| ../fase1/declaracion-de-margenes.md | §2-2(3) declaration of margins: operational definition, one currency per analysis type, fourteen rows with signs (2 positive / 7 negative / 3 undefined / 2 zero), and why R2 is a requirement rather than a preference |
| ../fase1/verificacion-puente-2d.md | readable 2D junction report: the solver validated against 1D, six variants, the governing point moving off the steel at the first millimetre of pad, 20 mm not 9, wrapping beating padding by 3.01 W/K, and the perimeter joist as parallel-path conduction rather than a junction |
| ../fase1/verificacion-ventilacion.md | readable ventilation report: the documented rates, why a fan in a sealed box depressurises it, the flue reversing by −130 Pa, and the penetrations the barrier must accept |
| ../fase1/verificacion-aporte-aire.md | readable make-up air report: a 113 mm inlet at 10 Pa removes 98 Pa, why no buildable inlet makes the flue adequate, row 14 retired by a room-sealed stove, 905 W of tempering load, and the hole as a control problem rather than a diffusion one |
| ../fase1/determinacion-estrategia-incendio.md | readable chapter 11 determination: the escape windows and the door width are one question, both packages priced at 0.29 m², why §11-9 is not coupled, and the 5.04 m travel distance |
| ../fase1/verificacion-incertidumbre.md | readable adequacy report: four kinds of uncertainty, the three sweeps, why the thinnest positive margin is not demonstrated, and why two rows are zero by construction |
| ../fase1/verificacion-ventanas.md | readable window report: the three readings of §11-13 priced against §13-7 daylight, why the escape fix is also the daylight fix, and why the bathroom window moves to the gable |
| ../fase1/verificacion-altura-libre.md | readable room-height screening report for the R1 gable |
| ../fase1/cribado-riesgos-naturales.md | readable chapter 7 procedure: gate sequence, flood datum, slope screen, quick-clay gate, decision rules |
| ../fase1/verificacion-envolvente.md | readable envelope report: build-ups, U-values with and without studs, insulation thickness needed, moisture profiles |
| ../fase1/verificacion-seccion.md | readable integrated section report: wall height vs pitch vs stack vs build-ups, coverage, what has to give |
| ../fase1/opciones-seccion-R2.md | four R2 options with what each costs, the low-zone plan logic and the tolerance test |
| ../fase1/r1-opciones-techo.md | readable R1 gable-roof sensitivity report generated from that model, including the inverse eave envelope |
| ../fase1/solicitud-datos.md | prioritised P0/P1/P2 questionnaire for C-01…C-09 |
| ../fase1/clasificacion-uso-decision.md | use-classification decision tree, municipal query template and transport-height warning |

## Rules

- No claim enters the index without provenance and condition of application.
- Paywalled works are listed as *to acquire*, never copied unlawfully.
- Aggregator results are leads only; confirm at official domains.
- A domain is "known" only when its exit gate in the plan is passed.
