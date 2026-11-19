# MiniHouse · Known / Assumed / Unknown register

Baseline: 2026-11-17. R0 prototype exchange and fit findings updated 2026-11-19. Includes the knowledge acquisition plan, the Chapter 11, 12 and 7 retrievals, and the envelope screening. Maps to rules.md §2 (measured / manufacturer / assumed) and §3 (provenance + condition of application).

## KNOWN (verified at primary source or derived and checked)

| Item | Basis | Where |
|---|---|---|
| Combined R0 STEP imported and saved in Fusion 2706.1.17 | `MiniHouse Combined Joint R0` / `MiniHouse_Combined_Joint_R0`; seven descriptive parameters. Four print parts (51 shells) span 150 × 150 × 11 mm. Twelve reference solids represent **four** fasteners; four more represent wall strips. Including references: 67 bodies, 150 × 150 × 34 mm. | [AL, canonical archive and screenshot](../../fase1/registro-decisiones.md#al-result-2026-11-19-fusion-exchange-confirmed-physical-fit-not-demonstrated) |
| Rectangular frame R0 fails right-corner alignment | `member(3)` uses `B - W` (67 mm) instead of `L - W` (142 mm), placing it 75 mm inboard. A 150 × 75 mm outline and 48 imported bodies do not establish assembly. | [Frame generator](../../scripts/frame_model.py) |
| Combined R0 fails two nominal hardware fits | The pocket is circular Ø10.2 mm; a hex AF10 nut measures 11.55 mm across corners. Member 4's open notch ends at the bolt centreline, leaving solid material within the Ø6 mm shank footprint. Neither the nut nor the shank can fully seat as modelled. | [Joint generator](../../scripts/combined_joint_prototype.py), `build_ply` and `half_polygon` |
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
| TEK17 §14-2 numbers are correctly transcribed but not applicable to likely MiniHouse routes | DIBK official + scope correction | S011, S020, S021 |
| TEK17 §14-5(1): detached ≤70 m² heated BRA applies only §§14-1, 14-3, 14-4(1); no §14-2 | DIBK official | S021 |
| TEK17 §1-2 routes for detached dwelling / holiday home / temporary building | DIBK official | S020 |
| General 4.00 m height screening value from Directive 96/53/EC summary | Statens vegvesen official PDF | S022 |
| TEK17 §13-13 vapour barrier Sd≥10 m; §13-2 rates transcribed but NOT applicable to mikrohus route | DIBK official + scope correction | S012, S023 |
| TEK17 Chapter 13 applicable set for mikrohus route: §13-1(1), §13-4/5/7, §13-9…13-16; §§13-2/3/6/8 exempt | DIBK official | S023 |
| TEK17 §11-2/§11-3: bolig and fritidsbolig are both risk class 4; one storey → BKL 1 | DIBK official | S024 |
| TEK17 §11-4(3) no. 4: BKL 1 + risk class 4 → **R 15**, not the R 30 in Table 1 | DIBK official | S024 |
| TEK17 §11-13(4) escape-window dimensions: h ≥600, w ≥500, h+w ≥1500, sill ≤1000 mm | DIBK official | S024 |
| Current R0 apertures produce only **one** qualifying escape window (V-01); V-02 and V-03 fail | derived + script | S024, fire_check.py |
| TEK17 §11-12 dwelling detection: interconnected mains smoke alarms, ≥1 per storey, ≥60 dB, four named zones | DIBK official | S024 |
| TEK17 §11-6 separation 8.0 m; §11-17 access 50 m and 1200 l/min small-house water | DIBK official | S024 |
| TEK17 §11-9 BKL 1 surface classes: walls/ceiling D-s2,d0 (cell ≤200 m²), external cladding D-s3,d0, roof BROOF(t2) with metal assumed, unclassified cavity surfaces allowed | DIBK official | S024 |
| TEK17 §11-9 insulation main rule A2-s1,d0; no. 7 needs an A2-s1,d0 load-bearing substrate, so timber rafters do not qualify | DIBK official | S024 |
| TEK17 §11-10: dwelling kitchen extract EI 15 A2-s1,d0 if not in a shaft, own duct with grease filter; ≥30 min cable function in fire class 1 | DIBK official | S024 |
| TEK17 Chapter 12 admitted set is only 8 provisions; all accessibility rules and the 2.4 m room height are exempt | DIBK §1-2(2)(d) | S020, S025 |
| TEK17 §12-7(2)(c): room height **2.2 m** on the mikrohus route | DIBK official | S025 |
| Full-width 2.2 m at 20° / 1100 mm stack caps at 20.1° for a 150 mm floor build-up | derived + script | S025, room_height_check.py |
| TEK17 §12-5/§12-11: level differences >0.5 m secured; §12-15 guardrail 1.0 m up to 10 m; §12-17 glazing secured up to 0.8 m | DIBK official | S025 |
| The 0.86 m door width comes from §11-14, not §12-13(2)(a), which is exempt | DIBK official, cross-chapter | S024, S025 |
| TEK17 §7-2/§7-3: MiniHouse is flood class **F2 (1/200)** and landslide class **S2 (1/1000)**, independent of C-01 | DIBK official | S026 |
| TEK17 §7-1 boundary: snow, wind and seismic are §10-2, **not** chapter 7 | DIBK official | S026 |
| TEK17 §7-3: outdoor area of an S2 building may be assessed at the S1 level (1/100); design-to-withstand ceiling ≈50 kPa | DIBK official | S026 |
| TEK17 §7-3 quick clay: below the marine limit the ground must be investigated **even outside mapped zones**; tiltakskategori K0–K3, and a new dwelling is not a K0 example | DIBK official | S026 |
| F2 at 1/200 is a 22.2 % chance of at least one exceedance in 50 years | derived | natural_hazard_screen.py |
| 50 kPa ≈ 5.1 t/m² ≈ 2.8 m of soil at 18 kN/m³ | derived | natural_hazard_screen.py |
| A well-ventilated cavity and everything outside it are excluded from the U-value (ISO 6946); counting them flatters a wall by ~0.02 W/m²K | modelling rule + derived | envelope_check.py |
| Clear-field U-values of the modelled wall/roof/floor are 0.209/0.164/0.160; **all three exceed §14-3 once a 15 % stud fraction is counted** (0.267/0.218/0.209) | derived | envelope_check.py |
| Insulation needed for §14-3 at a 15 % stud fraction: wall ~189 mm, roof ~247 mm, floor ~238 mm (clear field 141/181/176) | derived | envelope_check.py |
| With a vapour-open wind barrier the modelled wall stays dry in a steady-state Glaser check at 40 % and 55 % indoor RH, with or without a vapour barrier; **no barrier + tight sheathing (Sd 2 m) condenses 0.41 kg/m² in 90 d at 40 % RH, 1.09 at 55 %** | derived | envelope_check.py |
| Integrated section: at 20° / 1100 mm stack / 250 mm floor / 300 mm roof the max eave wall is **1785 mm** and only **~24 %** of the width reaches 2.2 m; the full-coverage pitch cap runs **1.9°–16.3°** across the swept cases | derived | section_feasibility.py |
| At the reference case the floor and roof build-ups would have to go **negative** to restore full coverage — those two levers are closed | derived | section_feasibility.py |
| A 264 mm wall build-up costs **4.5 m²** of the 18.0 m² gross floor, a 25 % loss | derived | section_feasibility.py |
| Four R2 options computed on the same model: 8°/900 (full headroom), 20°/1100 (24 %), 15°/700 (full), 20°/1100 at 4.40 m (97 %) | derived | section_options.py |
| R2-B's low zones are **1141 mm deep per side, 6.24 m² in plan**, ceiling 1785→2200 mm — usable for bathroom, kitchen run and storage | derived | section_options.py |
| **No option has tolerance**: a 100 mm reserve drops R2-B to 6 % and R2-D to 79 %; R2-A and R2-C survive | derived | section_options.py |
| No option admits a sleeping loft: ridge free height 2331 mm at 20°, needing 1600 mm above a 2.2 m loft floor | derived | section_options.py |
| Arbeidstilsynet crane training (>2 tm) and competent control of lifting gear | Lovdata official | S013 |
| Norwegian NA texts are paywalled — hard access blocker | investigation | S014 |
| Market = Norway, mainly Bergen; use = emergency cabin | Carlos, 2026-11-16 | fase1 section F |
| Reference images show a gable roof (R0 monopitch superseded as intent) | Carlos images + fase1 section F | S016 |
| TEK17 chapter 9 is **not** the noise/water chapter: it is pollution, hazardous substances, ground, nature types and construction waste; noise is §13-6 (exempt) and water/sewage are chapter 15 | DIBK official | S027 |
| **§9-2 has no manufacturer-free compliance route**, so reclaimed timber has no documented instrument — only a professional assessment, which is a testing question | DIBK official + reasoning | S027 |
| **§9-3 is a second siting gate**: contaminated-ground investigation before applying, municipal tiltaksplan before excavation, and the municipality may prohibit | DIBK official | S027 |
| **§9-6's 10-tonne limb cannot be crossed by building an 18 m² cabin** — the mass needed is 33–200 t; it can only be crossed by §9-6(2) aggregation with a demolition | derived | instalaciones_check.py |
| §9-7 covers **existing buildings only**, so a new-build cabin is outside it; §9-8 (70 wt%) and §9-9 inherit the §9-6 switch | DIBK official | S027 |
| §9-10 stove limits: **5 g/kg** with catalyst, **10 g/kg** otherwise, per NS 3059:1994, tested to NS 3058:1994 | DIBK official | S027 |
| **Chapter 15 has no small-building exemption anywhere**; a cabin is fully in scope for §15-1/15-3/15-5/15-6 | DIBK official | S028 |
| §15-3 chimney: **T400** minimum for solid fuel, constant cross-section, **≥2 free sides** for crack visibility, feiing access | DIBK official | S028 |
| **The 0.90 m backflow head is a minimum burial depth**: `d_crown ≥ 900 + d_trap − h_ffl`, about **560 mm** at a 400 mm floor and 60 mm trap | derived | instalaciones_check.py |
| A municipal main clears the 0.90 m rule by ~**940 mm**; a shallow sealed-tank connection **fails by 160 mm** | derived | instalaciones_check.py |
| §15-8(1)'s **100-year** stormwater figure is a design capacity and §7-2's **1/200** is a safety class — different instruments | DIBK official | S028 |
| **Four determinations**: §15-2 central heating, §§15-9…15-15 lifting devices for persons, chapter 16 lift safety control, §17-1 greenhouse gas account — none apply | DIBK official | S028 |
| **Chapter 16 is lift safety control, not documentation**; documentation is chapters 2 and 4 | DIBK official | S028 |
| **§2-2(2) allows analysis only where the regulation gives a function and no number** — a given ytelse (U-values, R 15, 2.2 m, 0.86 m, 0.90 m, 10 t, F2/S2, the 100-year basis) must simply be met | Lovdata FOR-2017-06-19-840 | S029 |
| §2-2(3) requires of any analysis: method suitable and valid, assumptions described, assumptions justified, **safety margins stated** | Lovdata | S029 |
| Only **3 of 9** screening reports state a numeric margin, in three different currencies (4.00 m screening value, 100 mm project reserve, 1.4 material factor) | derived | documentacion_check.py |
| §2-2(4) is **unsatisfied by construction**: the assumed performances do not yet give a sufficient basis for detailed design | derived | S029 |
| **§4-1(2) "small and simple" exemption considered and rejected** — its examples are unheated, unserviced, non-dwelling; MiniHouse has 6 of 6 FDV categories | DIBK official | S029 |
| FDV must be **ajour**, match the building as built, and state the design's premises and limitations; handed to the owner against a receipt, in a Scandinavian language | DIBK official | S029 |
| The paywalled Norwegian NAs are a **documentation** blocker as well as a design blocker (§2-1 requires NAs to be applied) | DIBK official | S029 |
| The lift screen's **ranking is mass-independent** — every ratio is per unit W, so C-07 blocks procurement (accessory capacity), not the layout choice | derived | lift_geometry_screen.py |
| At the reference geometry the spread between worst and best case is a factor of about **1.36** in per-leg tension | derived | lift_geometry_screen.py |
| **§14-3 sets no thermal-bridge limit.** The only figure, ≤0.05 W/m²K normalised, sits in §14-2's route, exempt via §14-5(1); passing every §14-3 number does not bound the junctions | DIBK S011 vs S021 | puentes_termicas.py |
| The 18 m² plan carries **61.10 m** of linear detail — 3.39 m per m² of floor (floor perimeter 18.00, eave 18.00, corners 8.80, reveals 16.30) | derived | puentes_termicas.py |
| Ordinary detailing reads **0.210 W/m²K** (4.2× the benchmark, 16 % of heat loss); poor 0.397, good 0.117 — none meets 0.05 | derived, generic Ψ | puentes_termicas.py |
| Compensation is **arithmetically open and geometrically shut**: +53 mm wall, +65 mm roof, +65 mm floor, and the roof share costs 69 mm of eave height against a 422 mm deficit | derived | puentes_termicas.py + section_feasibility.py |
| The 0.05 W/m²K benchmark is **mis-specified at 18 m²** — it implies a mean Ψ of 0.0147 W/mK, under half of good practice, and 0.075 W/mK on a 150 m² dwelling. State bridge targets **per metre** | derived | puentes_termicas.py |
| A 6:2 plan costs about **6 %** more perimeter than a square of the same area, and normalised Ψ″ falls from 0.199 to 0.066 between 18 and 150 m² at constant detailing | derived | puentes_termicas.py |
| **§2-2(3) has a single margin declaration**: one currency per analysis type, fifteen rows with signs — **2 positive, 7 negative, 4 undefined, 2 zero by construction** | derived | fase1/declaracion-de-margenes.md |
| **No ytelse is discharged at R0**: of the 31 ytelser in the §2-2(4) overview, 0 are met, 9 are not met, 20 undetermined and 2 do not apply | derived | ytelsesoversikt.py |
| **The preaccepted category is empty**: no foundation, no site-assembled envelope and no conventional roof means no preaccepted route, so every functional requirement is carried by an analysis or a stated number | derived | S030, ytelsesoversikt.py |
| **No declared margin is adequate by the declaration's own test** (positive *and* larger than its uncertainty): 0 adequate, 5 not adequate, 4 untestable — of the **nine** rows where §2-2(3) requires a margin. The other six are four stated ytelser and two determinations, and the ytelser are in a *stricter* regime, not a laxer one | derived | incertidumbre.py, S030 |
| The wall U moves **0.051 W/m²K** across the 8–23 % framing band at a fixed 189 mm, so its sign is set by a framing choice; the section moves **139 mm** but stays negative throughout; the bridges move **0.28 W/m²K** across detailing levels and stay above the benchmark | derived | incertidumbre.py |
| Row 2's **+40 mm** door margin is a nominal leaf size, not a free width — ordinary frame and hinge build-ups spend 30–60 mm, so the sign is unknown | derived | incertidumbre.py |
| At 23 % timber fraction the section deficit is **−498 mm**, not −422: the published figure is the 15 % mid-band value | derived | incertidumbre.py + section_options.py |
| By magnitude the **binding margin is the escape window at −500 mm** (V-03's sum rule and sill under the strictest §11-13 reading); by consequence it is the **section at −422 mm**, because the window closes by enlarging a hole and the section does not. The thinnest positive margin is the **+40 mm** door free width (900 mm leaf vs 860 mm required) | derived | declaracion-de-margenes.md + verificacion-ventanas.md |
| The natural-hazard **F2/S2 classes are themselves the margin**; the 1.4 factor is a partial factor on slope-model strength parameters and is **not** a margin on the class | derived | S026 + declaracion-de-margenes.md |
| A 10 mm steel plate contributes **0.0002 m²K/W**, so a 1D path gives **f_Rsi 0.236** against a required **0.754**; its surface sits at −2.9 °C at −10 °C outside | derived, ISO 13788 | condensacion_union.py |
| In 2D the same plate reads **0.377**, not 0.236 — lateral feed from the floor warms it, so the 1D value was **pessimistic** about the steel, and the direction of error the screen stated was wrong | derived, ISO 10211 | puente_2d.py |
| The steel stops being the coldest point at the **first millimetre of pad**; from 3 mm the **timber wall corner** governs at every thickness | derived, ISO 10211 | puente_2d.py |
| Wrapping the steel **below the floor, outside the insulation** gives **f_Rsi 0.921** and **Ψ +0.027**, identical to the bare timber corner — no pad, no thickness; 60 mm of pad reaches only 0.863 | derived, ISO 10211 | puente_2d.py |
| The floor-edge junction costs **3.50 W/K** with the steel inside and **0.49 W/K** wrapped — a **3.01 W/K** difference, about **16 %** of the envelope's element heat loss over 18 m of perimeter | derived, ISO 10211 | puente_2d.py |
| A joist parallel to the wall appears to add **+0.014 W/mK** to Ψ, but the whole of it is the floor's own parallel-path conduction (U **0.1363 → 0.1716** at a 12 % fraction); referenced to the joisted floor U the junction is unchanged at **+0.028**, and f_Rsi only falls 0.921 → **0.906** | derived, ISO 10211 | puente_2d.py |
| A bare chassis junction condenses whenever outdoors falls below **5.9 °C**; with a 0.358 m²K/W break that falls to about −41 °C, i.e. never | derived | condensacion_union.py |
| A 1D path needs **0.358 m²K/W** of thermal break (≈9 mm rigid foam, ≈47 mm timber, ≈54 mm neoprene); a 22 mm timber deck alone reaches only 0.617 and fails | derived | condensacion_union.py |
| In 2D the requirement is **0.80 m²K/W — 20 mm of foam, not 9**, because the corner governs once the steel is padded; 9 mm gives **0.693** against 0.754 | derived, ISO 10211 | puente_2d.py |
| **Mould governs over condensation** at the junction (0.358 vs 0.193 m²K/W), and the **floor-to-wall corner** governs over the flat wall (0.726 vs 0.358) | derived | condensacion_union.py |
| Indoor humidity moves the junction requirement harder than outdoor temperature: 40→60 % RH multiplies it **3.5×**, −5→−20 °C only **2.0×** | derived | condensacion_union.py |
| All four branches of §11-4(3) — no. 4 R 15 and no. 6.1/6.2/6.3 — require **A2-s1,d0 roof insulation**, so the interpretation question does not block the build-up | derived from DIBK S024 + §11-9 D | cubierta_incendio.py |
| **No. 6.2 is unavailable** to a timber roof: it demands every material in the roof construction, insulation included, to be A2-s1,d0 | derived | S024 |
| At 15 minutes the effective char depth is **15.0 mm** per face (0.65 mm/min plus k₀·d0), and a rafter exposed on three sides loses it twice across its width | EN 1995-1-2 §3.4.2 | cubierta_incendio.py |
| A **48 × 198** rafter retains **32 %** of its section modulus under R 15; parity needs **78 mm** of width, i.e. **98 mm** stock. It fails at every swept accidental load | derived | cubierta_incendio.py |
| §11-13 has **three readings** for this cabin and the R0 aperture table passes one: minimal (door to grade is a safe place) needs nothing, fire-cell (two qualifying windows) needs a **100 mm** sill drop on V-02 at no cost in glass, room-by-room needs **0.29 m²** on V-03 | derived | ventanas_check.py |
| The sentence «one accessible escape window is sufficient in a dwelling unit» is about **fire-service access under §11-17**, **not** a relaxation of «vinduer» in §11-13(4) — reading it as one makes the R0 table pass | derived from S024 | S024.md |
| The **bathroom has no direct exit** and its only opening, V-03, fails on three counts — it is the room the three readings disagree about | derived | geometria-R0.md + tabla-aberturas.csv |
| A qualifying aperture has **two equal minima** at 600 × 900 and 900 × 600 (0.54 m²), bulging to 0.5625 m² at 750 × 750; the absolute minimum is a 500 × 1000 slot at 0.50 m² | derived | ventanas_check.py |
| The escape fix is **also the daylight fix**: qualifying glass 2.47 → 2.76 m², minimum LT 0.600 → 0.537 at ff 0.85 — the only lever that moves two requirements at once | derived | ventanas_check.py |
| The bathroom's back wall is **1200 mm**, so a 900 mm aperture leaves **150 mm** piers; the gable at x=0 is **3000 mm** and takes it | derived | geometria-R0.md |
| The added glass costs **+0.284 W/K** and the added reveal **+0.050 W/K** — the two **add**, they do not cancel, because glass displaces wall but lengthens the opening perimeter | derived | ventanas_check.py |
| The **stud fraction is width ÷ centres**, not a material property: 15 % at 600 c/c implies 90 mm members. At 48 mm on 600 the roof needs **214 mm**, at 98 mm **251 mm** | derived | cubierta_incendio.py |
| The R2 options were solved with **floor 250 / roof 300**, which are round numbers, not the envelope solver's output: it returns **281 / 278 mm** at a 15 % fraction, so the published wall heights are ~**7 mm** optimistic | derived | section_options.py |
| Full coverage at 20° and a 1100 mm stack needs a transport limit of **4415 mm** at the published build-ups, **4422 mm** at 15 % and **4358 mm** at 8 % — so **R2-D's 4400 mm is 22 mm short** | derived | section_options.py |
| The timber fraction moves R2-B from 23 % to **34 %** coverage and R2-D to **100 %** between 15 % and 8 % — the only section lever that costs nothing at the transport limit | derived | section_options.py |

## ASSUMED (working values, must not drive design)

| Item | Value | Source |
|---|---|---|
| S-01…S-08 geometry assumptions | H=3200, clear=2400, bathroom at x=0–1200, no collaborating walls, etc. **S-03 monopitch superseded by declared gable intent; pitch unknown** | fase1/registro-decisiones.md, section F |
| 3,000 kg / EI=1.68 MN·m² / q=2.4525 kN/m beam example | illustrative only | S000, C003 |
| Example mass inventory | 2,200 kg, CG (2.545,1.471,0.741) — explicitly "NO ES DATO DEL PROYECTO" | fase1/inventario-masas-ejemplo.csv |
| 20% inset (1.2 m) as lift point candidate | SCI recommendation for LGS modules; not yet justified for this chassis | S008, lift-variants.md |
| Printed-joint layout | 1:2 of a nominal 100 mm flat bar, **2 mm PETG** strip so ply 4 can thread, M6 at full size, Ø6.4 clearance hole, Ø10.2 circular nut seat, 150 × 150 × 9.5 mm article | bolted_lap_prototype.py — values for a print test only, **not** a steel section |
| Printed-joint process assumptions | PETG over PLA for repeated assembly, 0.4 mm nozzle, free nuts with two-sided wrench access; no captive nut modelled | Bambu/FFF sources cited in the generated sheet; no print has been made |
| Frame model section | Plan 1:40, base **2 mm**, fins **7 mm**, channel **8 mm**, clear wall slot **5.6 mm**, schematic Ø2 mm corner holes | frame_model.py — section exaggerated, **not** a steel profile |
| Frame model numbering | 1 left, 2 top, 3 right, 4 bottom, matching the hand sketch; four crossmembers at 30/60/90/120 mm model scale | frame_model.py, derived from the canonical 1200 mm centres |

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
| NS 3031:2014 energy calculation method | purchase | not needed for full §14-2 frame on likely routes; may be needed for heat-loss/thermal-bridge documentation |
| Final Chapter 13 route and documented §13-1(1) alternative ventilation quantities | C-01 classification | cannot fix ventilation design; §13-2 rates apply only if an ordinary dwelling route is confirmed (S023) |
| Whether the roof is part of the main load-bearing system (R 15) or a roof-only construction eligible for §11-4(3) no. 6 | structural system not chosen | **no longer blocks the build-up** — all four branches force A2-s1,d0 insulation, so the roof is mineral wool either way. What it still decides is the **rafter** (R 15 charring: 48 mm keeps 32 % of its section modulus) and the **lining** class |
| The **member width and centres** of the roof and wall frame | Fase 2 / structural scheme | the stud fraction is width ÷ centres, so this sets the insulation thickness — and the 15 % currently used implies 90 mm members, which may be conservative |
| Whether one qualifying escape window satisfies §11-13(4) for a one-room cabin | municipal / fire-engineer confirmation | single-direction escape route cannot be finalised (S024) |
| §11-13 Table 1 travel distance for risk class 4 | not listed in the retrieved table | must not be quoted; moot by geometry at 18 m² |
| Whether the cabin counts as an escape route for §11-9 surface classes | municipal / fire-engineer confirmation | D-s2,d0 vs B-s1,d0 decides whether reclaimed timber can stay exposed. **Independent of §11-13**: a cell containing no rømningsvei is still a cell |
| §11-13(4) and §11-14 are engaged by the **same** question — safe place or rømningsvei — so declaration rows 2/3/4 move together | derived from S024 | estrategia_incendio.py |
| Maximum internal travel distance is **5.04 m** (bathroom corner to the nearest door jamb, straight line) against the 15 m figure in §11-14; the risk-class-4 Table 1 row was never retrieved | derived, plan geometry | estrategia_incendio.py |
| Exposed interior timber at the R0 reference section is **48.5 m²** — the area a B-s1,d0 answer would have to document or cover | derived | estrategia_incendio.py |
| §13-1(1) requires documented alternative air quantities; none existed, and §13-2's rates do not bind on this route | derived from S012/S023 | ventilacion_check.py |
| A sealed 36.9 m³ cabin at 1.5 h⁻¹ @50 Pa holds **106–140 Pa** of negative pressure to supply the fitted extract; the both-boosted flow needs 406 Pa and is not deliverable at all | derived | ventilacion_check.py |
| The flue reverses by **−130 Pa** at the highest achievable pressure, so the stove needs its own outdoor combustion air | derived, assumption ranges | ventilacion_check.py |
| A **113 mm** inlet at **10 Pa** of design depression supplies the make-up air and removes **98 Pa** of the 106 Pa the basic extract carries | derived, Cd 0.6 assumed | aporte_aire.py |
| Make-up air **cannot** make row 14 adequate: the only adequate depression (2 Pa) needs a 181 mm inlet and is below the pressure a 3 m/s breeze puts on a wall; the conclusion holds even without a size limit | derived, flue draught is an assumption range | aporte_aire.py |
| A **room-sealed** stove retires row 14 instead of improving it — the only negative row with a costless resolution | derived from the pressure argument | aporte_aire.py |
| The make-up air costs **905 W** at 30 K, **1.65×** the fabric loss of 18.3 W/K, so heat recovery is a precondition | derived | aporte_aire.py |
| The inlet carries **0.8 %** of the barrier's diffusion conductance — a control problem, not a diffusion one | derived | aporte_aire.py |
| The airtightness limit is **stricter in q50 than it looks in n50**: A/V is **1.80 m⁻¹** against ~0.77 for a compact two-storey house, so 1.5 h⁻¹ demands **0.83 m³/(h·m²)** — 2.3× lower | derived | tetthet_test.py |
| **The envelope has a floor**: below **1.19 h⁻¹** a sealed cabin cannot be fed by leakage at a 150 Pa fan, so the 90 m³/h basic extract stalls. Not a requirement — the inlet's fault case | derived, fan range generic | tetthet_test.py |
| The test target is **1.30 h⁻¹**, not the limit and not "as tight as possible": acceptance is **1.36** at a 10 % measurement uncertainty, so a 20 % test fails a cabin built to target | derived | tetthet_test.py |
| The make-up inlet is **113→116 mm** across the whole airtightness band, so it can be ordered **before** the measurement | derived | tetthet_test.py |
| The floor is not on the ground: a ventilated void over the chassis, so §13-5's "barrier against the ground" describes a detail the building does not contain | derived from envelope_check + S023 | radon_check.py |
| Cabin radon concentration is bounded by **E/Q** whatever the void does — **3.6–36 Bq/m³** on ordinary ground against a 200 limit | derived, exhalation rate is a generic range | radon_check.py |
| **Alum shale breaks the bound**: at 300 mBq/(m²·s) it is **216 Bq/m³**, so the sign is a site fact and C-01 decides it | derived, exhalation is an assumption | radon_check.py |
| A radon barrier is an **airtightness** item, not an Sd one — the Sd ≥ 10 m vapour barrier does not satisfy it by construction | derived from the transport mechanism | radon_check.py |
| The radon barrier's continuity is the **floor-to-wall junction**, 18 m of the same corner the 2D screen solved | derived | radon_check.py |
| Required fraction of the floor reaching 2.2 m free height | §12-7(1)/(2)(d) give no percentage | decides whether 20° is viable at a realistic floor build-up (S025) |
| Floor build-up above the chassis datum | C-02 | the 154 mm eave allowance at 20°/1100 mm is consumed by it |
| Whether the plot intersects a mapped flood (1/200) or landslide (1/1000) zone, and the mapped flood level | C-01 site | decides whether the plot survives §7-2/§7-3 at all |
| Whether the plot lies **below the marine limit** | C-01 site + NGU maps | forces a geotechnical investigation regardless of hazard mapping (S026) |
| Whether the flood area has great depth or strong current | C-01 site + flood data | escalates the target from F2 (1/200) to F3 (1/1000) |
| Local sea-level-rise rate and the service life used for storm surge | Kartverket + project decision | sets the flood datum a finished floor must clear |
| Tiltakskategori (K0–K3) and geotechnical scope | qualified geotechnical engineer | a new dwelling cannot be assumed to be K0 (S026) |
| Real λ and μ of the materials actually used, including the reclaimed timber | product selection (Fase 2) | the U-values move a few percent; the stud-penalty conclusion does not |
| Effective stud fraction and stud spacing | structural layout (Fase 2) | decides whether the wall needs 172 or 207 mm of insulation |
| Ψ value of the chassis-to-wall junction | junction detail not drawn; the 2D screen models a **plate**, not a member | a linear thermal bridge that could dominate the floor perimeter |
| Whether the wind barrier board is genuinely vapour-open | product selection | decides whether the wall is the dry case or the worst case in the envelope screen |
| Whether the escape window needs a guardrail/restrictor when the floor is >0.5 m above ground | §12-5 vs §11-13(4) | an unresolved tension, not a design assumption |
| Whether a loft stair is operation-only or part of the escape route | §12-14(5)(b) | decides whether stair dimensions apply at all |
| TEK17 Chapter 7 natural hazards — requirements and classes now verified, but **no hazard map, flood level or marine-limit check done** | C-01 site + NVE/NGU/Kartverket | a Bergen plot can fail chapter 7 before the cabin design matters; the assessment must also be repeated at every new deployment site |
| Whether the plot carries a designated **utvalgt naturtype** and whether the plan settles it (§9-4) | C-01 site + naturbase + plan status | no size exemption; the konsekvensanalyse cannot be dispensed from |
| Whether the ground is **contaminated** (§9-3) | C-01 site + forurensningsforskriften ch. 2 | a municipal tiltaksplan is needed before any excavation, and building can be prohibited |
| Whether the project **includes a demolition** that supplies the reclaimed timber | C-08 project definition | decides whether §9-6/9-8/9-9 apply at all, and whether §9-7 applies to the source building |
| Whether reclaimed timber carries lead paint, CCA or other preservative, PCB sealant or asbestos dust | C-08 testing | the only §9-2 route left is a professional assessment, so this is a cost and a lead time |
| What the drain connects to: municipal main, gravity tank or pumped tank | C-01 site + C-06 | decides whether the 0.90 m head is satisfied with 940 mm to spare or fails by 160 mm |
| Whether a wood stove is fitted, and which | brief / C-01 | triggers §9-10 emissions, §15-1 heating duties and §15-3 chimney geometry together |
| Whether the chimney can keep **two free sides** on an 18 m² plan | plan layout (Fase 2) | a positional constraint competing with clearances and the 45 °C surface limit |
| The **uncertainty** of each screen's model, needed to judge whether its margin is adequate (§2-2(3)) | responsible designer | the declaration now states every margin with its sign, but most screens do not quantify their own uncertainty, so "adequate" cannot yet be tested |
| Whether the FDV file is a versioned, site-specific structure or a single binder | documentation architecture | a re-sited building changes premises at every move, and FDV must stay *ajour* |
| Whether a move changes n50 at all | first re-test after a deployment | §4-2 makes the test a per-deployment record; the first re-test is also the experiment |
| **NS-EN ISO 9972:2015** — the airtightness method itself, which §14-3's number presupposes | to acquire (S031) | the test procedure, its point count, pressure range and uncertainty rule cannot be quoted; the specification is written to survive acquisition but a tester needs the document |
| The **chassis profile** and whether the floor insulation can wrap outside the steel rather than be interrupted by it | Fase 2 (chassis design) | the governing junction is not even geometrically defined, so no Ψ can be calculated |
| Whether a thermal-bridge target is adopted, and in **which currency** (mean Ψ per metre, or the normalised W/m²K) | responsible designer / Carlos | the 0.05 W/m²K figure is not adoptable at 18 m²; the currency decision has to precede any target |
| Whether the chassis member is **visible indoors**, under a deck, or wrapped by insulation | Fase 2 (chassis design) | decides whether f_Rsi is 0.236 (condenses below 6 °C) or not governed at all |
| Specific written lift-plan paragraph | not located in §§10/13 | do not claim a paragraph number |
| Architecture theory books (Ching, Mallgrave, Maggi) | to acquire | visual/spatial design depth |
| Steel section, plate thickness, weld, ear detail | Fase 2/3 | no fabrication |
| Real flat-bar/angle size, bolt class and nut strategy for the woven base | Carlos / responsible engineer | the 2 mm PETG and M6 values describe a print test, not a specified joint; no capacity claim is possible |
| Whether the sandwich-panel interface needs its own detail | C-02 build-up | the 34 mm slot only locates the test article; it is not a scaled wall build-up |
| Woven flat bar versus the wrapped-steel junction previously priced at Ψ +0.027 | Fase 2 junction detail | the thermal-bridge answer is **re-opened**, not carried over |
| Whether the U-channel fin height and slot width are buildable with the chosen sandwich panel | C-02 build-up | the 5.6 mm slot is a printed-model value, not a specified wall thickness |
| Physical assembly, seating of real hardware and wrench access | A corrected revision, verified corner and seat geometry, then a measured bench test | Do not print the rectangular frame R0 or combined joint R0 as proof of fit. Neither was printed, assembled or measured. |
| Suitability of the combined joint's 47.6 mm locating gap for an actual wall | C-02 wall build-up | The gap and reference strips show intended wall position, not panel specification or fit. |
| Robot–Advance Steel exchange | Test with those applications and the intended SMLX route | Fusion STEP imports (48 frame, 32 flat coupon, 67 combined) establish visibility only; they do not validate this exchange or release a design. |

## State

All engineering outputs remain **conceptual**. Nothing here releases geometry for fabrication or authorises a lift (rules.md §5).
