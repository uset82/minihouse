# MiniHouse · integrated cross-section feasibility

**State:** SCREENING — PARAMETRIC, NO GEOMETRY FROZEN, NO PITCH SELECTED. Not a design decision and not a compliance certificate.

- Required free height: **2.2 m** (TEK17 §12-7(2)(c), S025).
- Transport screening value: **4.00 m** (S022; general value, not a route permit).
- Envelope thicknesses: [envelope screening](verificacion-envolvente.md) — the wall needs ~189 mm of mineral wool and the roof ~247 mm once thermal bridging counts.
- z = 0 at the chassis top. `stack` includes the chassis depth, the trailer deck and the supports, so `transport = ridge top + stack`, consistent with [verificación de altura libre](verificacion-altura-libre.md).

## 1. Why this needed its own calculation

The room-height screen compared the eave with 2.2 m and the ridge with 4.00 m, but it treated the roof as a **line with no thickness**. A real roof has a build-up, and because that thickness is perpendicular to the slope its vertical cost is **t/cos θ** — so steepening the pitch costs twice: once through the ridge rise, and again through the roof thickness standing up. Meanwhile the envelope screen pushed the floor build-up from an assumed 150 mm to something closer to **250 mm**.

Both corrections eat the same budget, so they had to be applied together:

    ridge top = t_floor + h_wall + 1500·tan θ + t_roof / cos θ

## 2. Tallest wall that fits, and the coverage it buys

`h` is the wall height from finished floor to the underside of the roof at the eave, which is exactly the free height at the wall. `cov` is the fraction of the half-width that reaches 2.2 m.

| Pitch | Stack | Floor | Roof | Max wall | Coverage |
|---:|---:|---:|---:|---:|---:|
| 5° | 1100 | 200 | 250 | 2318 | 100% |
| 5° | 1100 | 200 | 300 | 2268 | 100% |
| 5° | 1100 | 200 | 350 | 2217 | 100% |
| 5° | 1100 | 250 | 250 | 2268 | 100% |
| 5° | 1100 | 250 | 300 | 2218 | 100% |
| 5° | 1100 | 250 | 350 | 2167 | 75% **partial** |
| 5° | 1100 | 300 | 250 | 2218 | 100% |
| 5° | 1100 | 300 | 300 | 2168 | 75% **partial** |
| 5° | 1100 | 300 | 350 | 2117 | 37% **partial** |
| 10° | 1100 | 200 | 250 | 2182 | 93% **partial** |
| 10° | 1100 | 200 | 300 | 2131 | 74% **partial** |
| 10° | 1100 | 200 | 350 | 2080 | 55% **partial** |
| 10° | 1100 | 250 | 250 | 2132 | 74% **partial** |
| 10° | 1100 | 250 | 300 | 2081 | 55% **partial** |
| 10° | 1100 | 250 | 350 | 2030 | 36% **partial** |
| 10° | 1100 | 300 | 250 | 2082 | 55% **partial** |
| 10° | 1100 | 300 | 300 | 2031 | 36% **partial** |
| 10° | 1100 | 300 | 350 | 1980 | 17% **partial** |
| 15° | 1100 | 200 | 250 | 2039 | 60% **partial** |
| 15° | 1100 | 200 | 300 | 1988 | 47% **partial** |
| 15° | 1100 | 200 | 350 | 1936 | 34% **partial** |
| 15° | 1100 | 250 | 250 | 1989 | 48% **partial** |
| 15° | 1100 | 250 | 300 | 1938 | 35% **partial** |
| 15° | 1100 | 250 | 350 | 1886 | 22% **partial** |
| 15° | 1100 | 300 | 250 | 1939 | 35% **partial** |
| 15° | 1100 | 300 | 300 | 1888 | 22% **partial** |
| 15° | 1100 | 300 | 350 | 1836 | 9% **partial** |
| 20° | 1100 | 200 | 250 | 1888 | 43% **partial** |
| 20° | 1100 | 200 | 300 | 1835 | 33% **partial** |
| 20° | 1100 | 200 | 350 | 1782 | 23% **partial** |
| 20° | 1100 | 250 | 250 | 1838 | 34% **partial** |
| 20° | 1100 | 250 | 300 | 1785 | 24% **partial** |
| 20° | 1100 | 250 | 350 | 1732 | 14% **partial** |
| 20° | 1100 | 300 | 250 | 1788 | 24% **partial** |
| 20° | 1100 | 300 | 300 | 1735 | 15% **partial** |
| 20° | 1100 | 300 | 350 | 1682 | 5% **partial** |
| 25° | 1100 | 200 | 250 | 1725 | 32% **partial** |
| 25° | 1100 | 200 | 300 | 1670 | 24% **partial** |
| 25° | 1100 | 200 | 350 | 1614 | 16% **partial** |
| 25° | 1100 | 250 | 250 | 1675 | 25% **partial** |
| 25° | 1100 | 250 | 300 | 1620 | 17% **partial** |
| 25° | 1100 | 250 | 350 | 1564 | 9% **partial** |
| 25° | 1100 | 300 | 250 | 1625 | 18% **partial** |
| 25° | 1100 | 300 | 300 | 1570 | 10% **partial** |
| 25° | 1100 | 300 | 350 | 1514 | 2% **partial** |

Only the 1100 mm stack is shown; the 900 mm case is in the JSON companion. **A wall shorter than 2200 mm cannot give 2.2 m anywhere at the eave**, so any row below 2200 mm is already partial before the pitch is considered.

## 3. Steepest pitch that still gives 2.2 m everywhere

| Stack | Floor | Roof | Max pitch, full coverage |
|---:|---:|---:|---:|
| 900 | 200 | 250 | 16.3° |
| 900 | 200 | 300 | 14.6° |
| 900 | 200 | 350 | 12.8° |
| 900 | 250 | 250 | 14.6° |
| 900 | 250 | 300 | 12.8° |
| 900 | 250 | 350 | 11.1° |
| 900 | 300 | 250 | 12.9° |
| 900 | 300 | 300 | 11.1° |
| 900 | 300 | 350 | 9.3° |
| 1100 | 200 | 250 | 9.3° |
| 1100 | 200 | 300 | 7.5° |
| 1100 | 200 | 350 | 5.7° |
| 1100 | 250 | 250 | 7.5° |
| 1100 | 250 | 300 | 5.7° |
| 1100 | 250 | 350 | 3.8° |
| 1100 | 300 | 250 | 5.7° |
| 1100 | 300 | 300 | 3.8° |
| 1100 | 300 | 350 | 1.9° |

The range runs from **16.3°** in the most favourable combination to **1.9°** in the least. Note what that means for the gable intent in the reference images: **a 20° roof cannot deliver 2.2 m over the full width under a 4.00 m transport limit with a realistic envelope**, and it is not close.

## 4. What would have to give at the reference case

Reference: **20°**, **1100 mm** stack, **250 mm** floor, **300 mm** roof.

Result: max wall **1785 mm** and coverage **24%**. That means a strip about **717 mm wide** along the ridge reaches 2.2 m, in a cabin whose internal width is about 2470 mm. §12-7(2)(d) does permit parts of a room to be lower, so this is not automatically a breach — but a 720 mm band is not a design, it is a technicality.

Each lever, moved on its own until full coverage is reached:

| Lever | Reference | Value needed | Change |
|---|---:|---:|---:|
| Transport stack | 1100 mm | **685 mm** | -415 mm |
| Floor build-up | 250 mm | **not achievable** | even zero would not reach it |
| Roof build-up | 300 mm | **not achievable** | even zero would not reach it |
| Transport limit | 4000 mm | **4415 mm** | +415 mm |
| Pitch | 20.0 ° | **5.7 °** | -14.3 ° |

**Two of the five levers do not exist at this reference case.** The required floor build-up and the roof build-up come out **negative**, which means that even a build-up of zero would not deliver full coverage. Those are not tight constraints, they are closed doors — and the envelope is already at the §14-3 minimum, so it is not available as a way out.

Read the table as a map of the trade, not a list of recommendations. What is actually left:

- **The stack is the cheapest lever and the least discussed.** It is a property of the trailer and the supports, not of the cabin, and it is negotiated with a carrier (C-06). Dropping it buys wall height one for one — but it has to fall by more than a third, which is a conversation with the carrier, not a rounding.
- **The roof build-up cannot be reduced**, because it is where the §14-3 insulation and the §11-4(3) no. 6 fire constraint both land. That lever is already spent.
- **The transport limit is a permit question, not a design one.** A dispensation above 4.00 m exists in principle (S009, VegSak) but turns every move into an application — which for a cabin that moves repeatedly is a different project.
- **Reducing the pitch is the only lever that stays inside the design**, because it relieves both the ridge rise and the t/cos θ term at once. The cost is architectural: the gable in the reference images becomes shallow, and the roof-space volume that a sleeping loft would use disappears.

## 5. The floor-area penalty nobody has costed yet

A 264 mm wall build-up takes **528 mm** off each dimension. The internal floor becomes **2.47 × 5.47 m = 13.53 m²** against a gross **18.0 m²** — a loss of **4.5 m²**, or **25%** of the building.

That is the same 189 mm of mineral wool that §14-3 demands, arriving as a spatial cost. It still fits the ≤30 m² mikrohus route with room to spare, so it is not a compliance problem; it is a liveability problem, and at 18 m² gross there is not much to give away.

## 6. What this changes

1. **The 20° gable and full-width 2.2 m are mutually exclusive under 4.00 m** with a realistic envelope. The design has to choose: shallower pitch, partial coverage, a lower stack, or a dispensation.
2. **The earlier room-height screen was optimistic**, not wrong: it answered the question it was asked, with the roof treated as a line and the floor at 150 mm. Both assumptions have now been replaced by values the other screens produced.
3. **C-02 now has a sharper question attached to it.** It is no longer "what is the floor build-up" but "what is the floor build-up, the roof build-up and the trailer stack, together" — because the three only make sense as a set.
4. **Nothing here selects a pitch.** The tables are a map of the trade, not a decision.

## 7. Limits

- **Parametric only.** No geometry is frozen, no material is selected and no member is sized. The build-ups are round numbers bracketing what the envelope screen implies.
- **The transport limit is a screening value**, not a route permit. The real constraint is the vegliste for the actual route (C-03), which is unknown.
- **The definition of the stack matters and must be confirmed with the carrier.** It is taken here as everything below the chassis top — chassis depth, trailer deck and supports. If a carrier quotes a deck height that excludes the chassis, the real stack is ~250 mm larger and every result in this report gets worse, not better.
- **No allowance for salients**, roof overhangs, chimney, vents, lifting ears or the trailer's own structure above deck. Each of those consumes height and none is modelled.
- **Free height is measured to the underside of the roof plane**, ignoring any ceiling lining, tie beams, collar ties or services in the roof space. A structural roof will lose more height than this.
- Nothing here is a compliance certificate or a fabrication release.

## 8. Source and status

- §12-7(2)(c) 2.2 m: S025. §14-3 U-values: S011. §11-4(3) no. 6 roof: S024.
- Transport screening value 4.00 m: S022. Dispensation route: S009.
- Generated by `scripts/section_feasibility.py`; JSON companion: `knowledge/comparisons/section-feasibility.json`.
- SCREENING ONLY — no pitch, no build-up, no geometry fixed.
