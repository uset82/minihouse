# MiniHouse · envelope thermal and moisture screening

**State:** SCREENING — GENERIC MATERIAL DATA, NO PRODUCTS SELECTED. Not a thermal calculation of the built element, not a hygrothermal simulation and not a compliance certificate.

- Limits: TEK17 **§14-3** (S011) — U wall ≤0.22, roof ≤0.18, floor ≤0.18, glazing ≤1.2 W/m²K.
- Moisture requirement: TEK17 **§13-13** (S012/S023) — vapour barrier on the warm side, **Sd ≥ 10 m**, vapour-open wind barrier behind a ventilated cavity.
- Physics: the four-condition moisture test from S010.
- All λ and μ values are **generic**, not manufacturer data. They are good enough to size an envelope and not good enough to buy one.

## 1. The build-ups as modelled

Inside to outside. `R` is the layer resistance, `Sd` the vapour diffusion resistance. Rows marked *not counted* sit outside a well-ventilated cavity and are excluded from the U-value, as ISO 6946 requires.

**Wall** — 150 mm insulation, R total 4.80 m²K/W

| Layer | d mm | R m²K/W | Sd m | Counted |
|---|---:|---:|---:|---|
| timber lining | 13.0 | 0.100 | 0.65 | yes |
| vapour barrier | 0.2 | 0.000 | 10.00 | yes |
| mineral wool between studs | 150.0 | 4.286 | 0.15 | yes |
| wind barrier board | 12.0 | 0.240 | 0.06 | yes |
| ventilated cavity | 0.0 | 0.170 | 0.00 | not counted |
| reclaimed timber cladding | 25.0 | 0.192 | 1.25 | yes |

Clear-field U = **0.209** W/m²K against a limit of **0.22** (PASS).

**Roof** — 200 mm insulation, R total 6.09 m²K/W

| Layer | d mm | R m²K/W | Sd m | Counted |
|---|---:|---:|---:|---|
| timber ceiling lining | 13.0 | 0.100 | 0.65 | yes |
| vapour barrier | 0.2 | 0.000 | 10.00 | yes |
| mineral wool between rafters | 200.0 | 5.714 | 0.20 | yes |
| roof board | 18.0 | 0.138 | 0.90 | yes |
| underlay | 0.5 | 0.000 | 0.50 | yes |
| ventilated cavity | 0.0 | 0.200 | 0.00 | not counted |
| standing-seam metal | 0.6 | 0.000 | 0.00 | yes |

Clear-field U = **0.164** W/m²K against a limit of **0.18** (PASS).

**Floor** — 200 mm insulation, R total 6.23 m²K/W

| Layer | d mm | R m²K/W | Sd m | Counted |
|---|---:|---:|---:|---|
| timber floor deck | 22.0 | 0.169 | 1.10 | yes |
| mineral wool between joists | 200.0 | 5.714 | 0.20 | yes |
| structural board | 18.0 | 0.138 | 0.90 | yes |
| ventilated void over chassis | 0.0 | 0.170 | 0.00 | not counted |

Clear-field U = **0.160** W/m²K against a limit of **0.18** (PASS).

## 2. The stud penalty — and why the clear-field number is a trap

§14-3's U-value is a **whole-element** value. A timber-stud wall is a parallel path: the studs short-circuit the insulation, and the area they occupy is not small. The table below is the same element with a fraction of the insulated layer replaced by timber (λ 0.13 W/mK against 0.035 for mineral wool).

| Element | Clear field | 10 % studs | 15 % | 20 % | Limit |
|---|---:|---:|---:|---:|---:|
| Wall | 0.209 | 0.248 **FAIL** | 0.267 **FAIL** | 0.287 **FAIL** | 0.22 |
| Roof | 0.164 | 0.200 **FAIL** | 0.218 **FAIL** | 0.236 **FAIL** | 0.18 |
| Floor | 0.160 | 0.193 **FAIL** | 0.209 **FAIL** | 0.226 **FAIL** | 0.18 |

**This is the finding that matters.** All three elements pass §14-3 on the clear field — wall 0.209, roof 0.164, floor 0.160 W/m²K — and **all three fail once the studs are counted**: at a 15 % stud fraction the wall goes to 0.267 (+28 %), the roof to 0.218 and the floor to 0.209. The penalty is 20–30 % for a detail that is invisible in a layer-by-layer calculation. Continuous insulation, a cross-battened service zone or an insulating sheathing board is not a refinement here — it is the difference between passing and failing.

Insulation thickness needed to meet §14-3, clear field versus with studs:

| Element | Clear field | 10 % studs | 15 % | 20 % |
|---|---:|---:|---:|---:|
| Wall | 141 mm | 172 mm | 189 mm | 207 mm |
| Roof | 181 mm | 224 mm | 247 mm | 271 mm |
| Floor | 176 mm | 217 mm | 238 mm | 260 mm |

The wall needs about **189 mm** of mineral wool at a 15 % stud fraction, against **141 mm** in the clear field. That difference lands directly on the two constraints already identified elsewhere: the **2.2 m** room height of §12-7(2)(c) and the **4.00 m** transport screening value. **Envelope thickness is not a free parameter — it competes with both.** See [verificación de altura libre](verificacion-altura-libre.md).

## 3. Moisture: where the vapour resistance sits decides everything

Steady state, 20 °C indoors, 0 °C outdoors at 85% RH — a Bergen winter, not a cold inland site. The diffusion path stops at the ventilated cavity, so the cladding and the cavity are outside it. A row is only dry if **no** interface reaches saturation.

| Build-up | Total Sd | At RH 40 % | Rate, 90 d | At RH 55 % | Rate, 90 d |
|---|---:|---|---:|---|---:|
| Sd 10 m barrier (TEK17 §13-13) | 10.86 m | **dry** | — | **dry** | — |
| Sd 2 m barrier (a weak retarder) | 2.86 m | **dry** | — | **dry** | — |
| no barrier, vapour-open wind barrier | 0.86 m | **dry** | — | **dry** | — |
| no barrier, tight sheathing Sd 2 m | 2.80 m | after mineral wool between studs | 0.41 kg/m² | after mineral wool between studs | 1.09 kg/m² |

The result is not the one the usual rule of thumb predicts, and it is worth reading carefully:

- **The §13-13 wall stays dry at both humidities.** With Sd 10 m almost the whole vapour pressure drop happens across the barrier, so the insulation and the wind barrier never see a partial pressure above saturation. Total Sd 10.9 m, condensation: none.
- **Weakening the barrier to Sd 2 m does not, on its own, cause condensation here** (total Sd 2.86 m, dry at 40 % and 55 %). Diffusion alone does not condemn a weak barrier when the cold side is open.
- **Removing the barrier entirely also stays dry** (total Sd 0.86 m), for the same reason: with a vapour-open wood-fibre wind barrier nothing traps the vapour, so nothing accumulates.
- **But the same barrier-free wall with a tight sheathing board (Sd 2 m) is the worst case in the table** — 0.41 kg/m² over 90 days at 40 % RH and 1.09 kg/m² at 55 %. That is the classic cold-climate error: a vapour-tight layer on the **cold** side. It is worse than having no barrier at all, because the vapour gets in and cannot get out.

**So the four rows do not say that the vapour barrier is unnecessary.** They say that the dominant failure mode in this build-up is a **cold-side trap**, not a missing warm-side barrier — and that the wind barrier board, which nobody photographs and nobody specifies carefully, is the component that decides the answer.

That distinction matters because **Glaser cannot see the other three moisture paths**. S010's four-condition test asks for moisture, a path, a force and a susceptible material; steady-state diffusion is only one path. Air leakage carries far more vapour than diffusion, and it is invisible to this model. A barrier-free wall that is dry in a Glaser calculation can still be wet in service because of a single unsealed penetration.

Read §13-13 in that light and its Sd ≥ 10 m is not a diffusion calculation. It is a **robustness requirement**: it keeps the wall dry when the cold side is not as open as designed, when indoor humidity runs above the assumption, when the barrier is also doing air-barrier duty, and when the build-up is repeated by someone who has not read this report. The regulation is buying tolerance, not a number.

Two corollaries the model does make visible:

- **A service cavity between the barrier and the lining moves the barrier deeper and colder**, where the same Sd holds less margin. If a service zone is wanted, the barrier belongs in front of it, not behind.
- **The wind barrier board is a design decision, not a commodity.** Swapping a vapour-open board for a foil-faced one converts a tolerable wall into the worst row of the table without changing anything visible.

## 4. What this changes in the design

1. **The wall thickness is now a number.** ~189 mm of mineral wool at 15 % studs, plus lining, barrier, wind barrier, cavity and cladding — of the order of 250–270 mm total. Two walls of that thickness take 500–540 mm out of a 3000 mm floor width.
2. **The room-height and transport constraints tighten accordingly.** Floor and roof build-ups grow for the same reason, and the eave allowance at 20° with a 1100 mm stack is only 154 mm. This is the same collision from a different direction.
3. **Continuous insulation or a cross-battened zone stops being optional** if the element is to stay under 0.22 W/m²K at a realistic stud fraction.
4. **The steel chassis is a linear thermal bridge this script does not model.** A steel member crossing the floor insulation can dominate the junction. It needs a thermal-break detail; no Ψ value is claimed here.
5. **The reclaimed timber is thermally almost irrelevant** — 25 mm of cladding is R ≈ 0.19 m²K/W, and outside the ventilated cavity it is not counted at all. Its role is weather, not insulation, which matches the brief's decision to keep it non-structural and reversible.

## 5. Limits

- **Generic λ and μ values.** No product has been selected; manufacturer data would move the U-values by a few percent — not the conclusions, but the exact thicknesses.
- **Steady-state Glaser only.** No convection, no capillary redistribution, no hygroscopic buffering, no solar-driven inward diffusion, no rain penetration. A real hygrothermal assessment (WUFI or equivalent) is a specialist deliverable.
- **One-dimensional.** Junctions, corners, the chassis and window reveals are where buildings actually fail, and none of them is in this model.
- **The design conditions are assumptions**: 20 °C / 40% indoors and 0 °C / 85% outdoors. A Bergen winter mean is not the same as a diffusion design case.
- **No energy-frame calculation.** §14-2 does not apply on the likely routes (S020/S021), so this is an element-level check against §14-3, not an energy performance result.
- Nothing here is a compliance certificate, a product specification or a fabrication release.

## 6. Source and status

- TEK17 §14-3 U-values: S011. §13-13 vapour barrier and cavity: S012, S023.
- Moisture mechanisms: S010.
- Ventilated-layer treatment: ISO 6946 convention, applied here as a modelling rule.
- Generated by `scripts/envelope_check.py`; JSON companion: `knowledge/comparisons/envelope-check.json`.
- SCREENING ONLY — no construction fixed, no product approved.
