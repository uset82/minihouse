# MiniHouse · architectural and building-physics brief (R0 conceptual)

Status: Stage 5, updated 2026-11-16. Based on R0 geometry (`fase1/geometria-R0.md`), TEK17 (S005, S011, S012), moisture physics (S010), SCI P272 (S008), and Carlos's declared intent: **market Norway, mainly Bergen; use = emergency cabin** (2026-11-16). Numeric energy and indoor-climate limits retrieved — see §4.

**Important geometry change:** the reference images show a **gable roof**, not the monopitch assumed in R0 S-03. See §1 and `fase1/registro-decisiones.md` section F.

## 1. Spatial strategy (from R0 assumptions, all conceptual)

- Exterior 6000 × 3000 mm; H total 3200 mm; clear interior 2400 mm — S-01/S-02. **Roof: gable (two slopes) per Carlos's reference images; pitch NOT dimensioned.** The monopitch +200 mm in R0 S-03 is superseded as intent; R0 plans remain a coordinate frame only until a revised revision is drawn.
- Bathroom at x ≈ 0–1200 mm, living/kitchen remainder (S-04).
- Openings all govern aperture-diagonal deformation: P-01 door (900 × 2050, y=3000), V-01 (1200 × 1100, y=3000), V-02 (1000 × 900, y=0), V-03 (500 × 500, y=0).
- Chassis reference axes y≈150 and y≈2850; cross members @1200 mm. Steel section **undefined**.

Design tension to manage: the largest opening (V-01, 1200 mm) sits in the long façade that also carries the chassis line — the window head/sill detail must not interrupt the load path without a documented transfer.

## 2. Cold-climate envelope — governing principles

From S010, apply the four-condition moisture test (moisture, path, force, susceptible material) to each of these:

| Failure mechanism | Route/force | Control in this module |
|---|---|---|
| Rain penetration through reclaimed timber cladding | Absorption, penetration, splash | Vented rainscreen cavity, continuous top-to-bottom, with vent openings top and bottom; overlapping/flashed joints; drained cavity |
| Interstitial condensation at steel studs (thermal bridging) | Vapour diffusion + convection through air leaks | Continuous air barrier; correctly placed vapour control layer on the warm side; thermal break at steel-to-envelope interfaces; avoid concealed steel cold spots |
| Built-in moisture in reclaimed timber | Water in timber at installation | Measure moisture content before enclosure; allow drying; do not close wet timber behind vapour-impermeable layers |
| Ground capillary rise at chassis/floor | Wicking from support | Capillary break between chassis and ground/support; drainage away from base; keep cladding clear of standing water |
| Wind-buffeting rain during transport | Wind-driven rain while wrapped | Weather-tight temporary wrap during transport (S008 §7.1), with joints detailed against ingress |

Ventilation drying (S010) is especially important where vapour-impermeable claddings or roofing are used — provide clear air spaces and vent holes.

## 3. Reclaimed timber

- Default role: **reversible cladding/finish**, not structural (rules.md §2, SN-CEN/TS 1090-201 for steel reuse; NS-EN 1995 if timber ever carries load).
- Per-piece/lot record: species if known, origin, moisture content, defects, previous use, proposed location. Traceability before installation.
- Any structural use needs documented species, grade, moisture, defects and connections — otherwise stay out of the structural model.

## 4. Regulatory inputs — status (UPDATED 2026-11-16)

- TEK17 §10-2 (S005): strength/stiffness/stability during execution and final state; documented material properties. **Confirmed.**
- DIBK mikrohus regime (S018): if the emergency cabin is legally a detached year-round dwelling with one unit, 18 m² is within the ≤30 m² limit; one storey, ≤4.5 m above ground, 2.2 m room height, all main dwelling functions, minimum energy and documentation still apply. **Conditional on C-01; not applied yet.**
- TEK17 §13-2 (S012): dwelling ventilation — whole module **1.2 m³/h per m² floor area** when occupied (18 m² → **21.6 m³/h**); bedrooms 26 m³/h per bed place; non-permanent rooms 0.7 m³/h per m²; extract rates kitchen/bath/toilet/utility listed. **Retrieved.**
- TEK17 §13-9 (S012): no groundwater, rainwater, use-water or humidity penetration causing moisture damage, mould or hygiene problems; moisture-sensitive products kept dry in storage/transport/construction. **Retrieved.**
- TEK17 §13-13 (S012): air- and vapour-tight layer on warm side; **vapour barrier Sd ≥ 10 m**; vapour-open wind barrier facing a ventilated cavity; airtight joints; no other high-vapour-resistance layer. **Retrieved** — directly confirms the rainscreen strategy in §2.
- TEK17 §14-2/§14-3 (S011): energy frame for småhus = **100 + 1600/A kWh/m²·yr** (≈188.9 for 18 m², classification pending C-01); absolute minimum U-values wall ≤0.22, roof ≤0.18, floor ≤0.18, windows/doors ≤1.2 W/m²K; airtightness ≤1.5 h⁻¹ at 50 Pa. Alternative measure route: wall ≤0.18, roof ≤0.13, floor ≤0.10, windows ≤0.80, SFP ≤1.5, air leakage ≤0.6 h⁻¹. **Retrieved.**
- Remaining §13 sections (13-1, 13-4 thermal, 13-5 radon, 13-6 sound, 13-10…13-12, 13-14, 13-15) not yet retrieved. Energy calculation itself requires NS 3031:2014 (not available) and a climate/use definition (C-01).

The envelope can now be specified numerically at the TEK17 minimum level, but the final U-values and the energy frame still depend on use classification and an NS 3031 calculation.

## 5. Open questions that still block this brief

- **C-01 partially answered:** market Norway / mainly Bergen; use = emergency cabin. Still needed: exact site and legal classification (permanent dwelling vs. temporary/emergency accommodation) — this decides whether the §14-2 småhus energy frame applies and which snow/wind values govern.
- **C-09 partially answered:** the two reference images are now in `images/` (intent only, not dimensioned).
- Still open: **C-02** final dimensions/salients, **C-07** equipment masses, **C-08** reclaimed timber quantity/species/state, plus roof pitch and the final Bergen site coordinates for wind/snow.

Bergen context (coastal, high rainfall, wind-driven rain) reinforces the ventilated rainscreen and vapour-control strategy in §2; specific snow/wind numbers remain pending the Norwegian NA and site data.

## 6. State

CONCEPTUAL — NOT FOR FABRICATION. No energy or moisture performance has been calculated; only principles and failure mechanisms are recorded.
