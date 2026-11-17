# MiniHouse · thermal bridges and the chassis junction

**State:** CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO Ψ CALCULATED, NO PRODUCT SELECTED.
The envelope screen meets §14-3 on all three elements and then says it does not model the steel chassis ([S011](../knowledge/sources/S011.md)). This report quantifies what that omission is worth.

## 1. The regulation does not cap the junctions on this route

This is the finding that makes the rest matter. TEK17's only numeric thermal-bridge figure is the **normalised value ≤ 0.05 W/m²K**, and it appears in **§14-2's** alternative energy-measures route. **§14-5(1) exempts a detached building up to 70 m² from §14-2.** **§14-3 sets no thermal-bridge limit** — the route that *does* apply caps the element U-values and the airtightness and says nothing about linear bridges.

So on the applying route:

| Check | Capped? |
|---|---|
| U wall 0.22 / roof 0.18 / floor 0.18 / glazing 1.2 | **yes**, §14-3 |
| Air leakage 1.5 h⁻¹ @50 Pa | **yes**, §14-3 |
| Normalised thermal bridge value | **no** — the 0.05 figure is in the exempt §14-2 route |

A building can therefore pass every §14-3 number while losing a large share of its heat at the joints, and the regulation will not object. The 0.05 figure is still the best benchmark available, and this report uses it — but as a **voluntary target, not a compliance obligation**, and it is labelled that way throughout.

## 2. The junction inventory

Footprint 6.0 × 3.0 m, so **18.0 m** of perimeter against **18.0 m²** of floor. A nominal 2200 mm wall height and the R0 aperture table give:

| Junction | Length m |
|---|---:|
| floor / chassis perimeter | 18.00 |
| eave (wall to roof) | 18.00 |
| external corner (4 x wall height) | 8.80 |
| opening reveals | 16.30 |
| **total linear detail** | **61.10** |

That is **3.39 m of linear detail per square metre of floor**, and it is the quantity that decides whether the junctions matter. The floor perimeter alone is as long as the whole building.

## 3. What ordinary detailing costs

Ψ values below are **generic screening ranges from ordinary practice — not project data and not a calculation.** Real values need a 2D analysis to NS-EN ISO 10211 on a drawn detail, and no detail exists.

| Detailing | Ψ floor / eave / corner / reveal | Ψ″ W/m²K | × benchmark | Bridge loss W/K | Share of heat loss |
|---|---|---:|---:|---:|---:|
| **poor** | 0.20 / 0.10 / 0.05 / 0.08 | 0.397 | **7.9×** | 7.14 | 27 % |
| **ordinary** | 0.10 / 0.05 / 0.03 / 0.05 | 0.210 | **4.2×** | 3.78 | 16 % |
| **good** | 0.05 / 0.03 / 0.02 / 0.03 | 0.117 | **2.3×** | 2.10 | 10 % |

Element heat loss for comparison: **19.63 W/K**, from the §14-3-compliant build-ups at a 15 % stud fraction.

**Even the good column is 2.3× the benchmark.** Ordinary detailing lands at just over four times it and poor detailing at eight. There is no reading of this table in which the junctions are a footnote.

## 4. The size effect, isolated

Normalised bridge length scales roughly as 1/√area. Holding the **same detailing** and varying only the footprint:

| Floor area m² | Square perimeter m | Perimeter per m² | Ψ″ at ordinary detailing |
|---:|---:|---:|---:|
| 18 | 17.0 | 0.94 | 0.199 |
| 50 | 28.3 | 0.57 | 0.116 |
| 100 | 40.0 | 0.40 | 0.081 |
| 150 | 49.0 | 0.33 | 0.066 |

The 18 m² cabin carries **2.9×** the perimeter per square metre of a 150 m² dwelling, and its Ψ″ is **3.0×** as large with identical detailing. The requirement set is weakest exactly where this building type is most exposed — and the exemption in §14-5(1) removes the one limit that would have noticed.

A second, smaller point: the 6:2 aspect ratio costs about **6 %** more perimeter than a square of the same area. A squarer plan would be thermally cheaper, which is worth remembering when the 6 m length is a transport decision rather than an architectural one.

## 5. What compensation would cost, in millimetres

The first version of this section claimed the junctions *cannot* be offset by insulation. That was wrong, and the self-test in this script is what caught it: holding total heat loss constant only asks the elements to absorb the bridge loss by scaling every element U by

```
f = (H_elements − H_bridges) / H_elements
```

which stays positive at all three detailing levels. Compensation is therefore arithmetically open. The envelope solver prices it:

| Detailing | f | Wall +mm | Roof +mm | Floor +mm |
|---|---:|---:|---:|---:|
| **poor** | 0.636 | +127 | +156 | +156 |
| **ordinary** | 0.807 | +53 | +65 | +65 |
| **good** | 0.893 | +27 | +33 | +33 |

At ordinary detailing the wall grows from **189 to 242 mm**, the roof from 245 to 310 mm and the floor from 241 to 306 mm.

**The roof is the one that closes the door.** A roof build-up costs its thickness divided by cos θ in the vertical direction, so +65 mm of mineral wool costs **69 mm of eave height**. The section solver already shows the eave landing near 1785 mm against a 2200 mm requirement — a deficit of **422 mm**. Compensating the roof alone would consume about **16 %** of that deficit, and the wall's extra 53 mm eats into the 18 m² gross area in plan.

So the honest statement is narrower than the one this report first made, and stronger: **compensation is arithmetically available and geometrically closed.** Insulation thickness is not a lever the section has room to pull. **The junction has to be designed, not offset** — and the reason is the room height and the transport limit, not the arithmetic.

## 6. The benchmark is the wrong instrument for this building

To reach the voluntary 0.05 W/m²K benchmark across **61.1 m** of linear detail on an 18 m² plan, the mean Ψ would have to be **0.0147 W/mK**.

That number deserves to be read against what real details achieve. The **good** scenario in §3 averages **0.0325 W/mK** across its four junction types, so the benchmark demands a mean detail at **45 % of good practice** — on all 61 m, including 16.3 m of window reveals, which are the hardest linear detail in any wall.

The same 0.05 applied to a 150 m² dwelling, with roughly 0.67 m of detail per m² instead of 3.39, implies a mean Ψ of about **0.075 W/mK** — five times looser. The benchmark is normalised by floor area, and floor area is exactly what a small building has least of.

**Conclusion: do not adopt 0.05 W/m²K as a MiniHouse target.** It was calibrated on dwellings and transplanted here it stops being a target and becomes a different requirement. If a bridge target is wanted, it should be stated **per metre of linear detail** — a mean Ψ — where the number means the same thing at any size. The normalised figure will read high for this building no matter how well it is detailed, and the report should say that rather than chase it.

## 7. What this changes

1. **The chassis junction is a design driver, not a detail.** It is the largest single thermal decision in the building and it is not drawn.
2. **§14-3 will not catch it.** Element U-values and airtightness pass; the junctions are unbounded on the applying route. Passing the numbers is not the same as being efficient, and the gap is where small buildings are weakest.
3. **Compensation is arithmetically open and geometrically shut.** Insulating away ordinary detailing costs about 53 mm of wall, 65 mm of roof and 65 mm of floor; the roof share alone is 69 mm of eave height against a 422 mm deficit. The lever exists and there is no room to pull it.
4. **The 0.05 W/m²K benchmark is not adoptable at 18 m².** It implies a mean Ψ of 0.0147 W/mK — under half of good practice — because it is normalised by an area this building barely has. State any bridge target per metre, not per m².
5. **The 6:2 plan is thermally expensive.** About 6 % more perimeter than a square of the same area, on top of an already unfavourable size.
6. **The chassis detail and the thermal detail are one drawing.** Floor insulation wrapping outside the steel rather than being interrupted by it is the only route to a low Ψ at the governing junction, and that decision belongs to whoever profiles the chassis.

## 8. Limits

- **No Ψ has been calculated.** The values in §3 are generic screening ranges, not results, and the real figures require a 2D analysis to NS-EN ISO 10211 on a drawn detail that does not exist.
- The chassis profile is not selected, so the dominant junction is not even geometrically defined.
- Moisture risk at the junction is **not** assessed here. A cold steel member crossing the insulation is a condensation risk as well as a heat-loss one, and §13-13's vapour-barrier rule interacts with it. That is a separate analysis.
- Wall height is nominal at 2200 mm; the corner length scales with the R2 option and the numbers move slightly with it.
- No airtightness model. §14-3's 1.5 h⁻¹ is a separate requirement and a separate failure mode.
- Nothing here is a junction design, a compliance statement or an energy calculation.

- Generated by `scripts/puentes_termicas.py`; JSON companion: `knowledge/comparisons/puentes-termicas.json`.
