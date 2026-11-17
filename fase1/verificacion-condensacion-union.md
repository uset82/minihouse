# MiniHouse · condensation at the chassis junction

**State:** CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO 2D CALCULATION, NO PRODUCT SELECTED.
The thermal-bridge screen prices this junction in energy and defers moisture as a separate analysis ([puentes térmicos](verificacion-puentes-termicas.md)). This is that analysis, in the only form available without a drawn detail.

## 1. The two chapters meet here, and neither covers it

§14-3 caps **heat loss**. §13-13 caps **vapour resistance** and requires the barrier on the warm side ([S012](../knowledge/sources/S012.md), [S023](../knowledge/sources/S023.md)). Neither says anything about the **temperature of a steel member that crosses the insulation line**, and that temperature is what decides whether the junction condenses. It is the one place where the envelope's two governing requirements leave a gap between them.

## 2. The temperature factor

NS-EN ISO 13788 assesses surface condensation by the temperature factor

```
f_Rsi = (theta_si - theta_e) / (theta_i - theta_e)
```

For a one-dimensional path this reduces to `f = 1 - R_si/R_total`. It tends to **0** as the construction approaches a bare surface film and to **1** as the resistance grows. The critical value comes from the surface humidity that matters — 80 % for mould, 100 % for condensation:

| Criterion | Critical f | Meaning |
|---|---:|---|
| Mould (80 % surface RH) | **0.754** | the surface must stay above this at design conditions |
| Condensation (100 %) | **0.642** | below this the surface runs wet |

Design conditions: **20 °C / 50 %** indoors, **-10 °C** outdoors, dew point **9.3 °C**. The outdoor value is a screening figure — the real one comes from the National Annex and the site, and neither is held.

## 3. What a bare chassis does

A 10 mm steel plate contributes **0.0002 m²K/W**. That is not a small resistance; it is nothing. The inner surface of a steel member bridging the insulation therefore sits one surface film away from outdoor air:

| Construction | Added R m²K/W | f_Rsi | Surface °C | Mould | Condensation |
|---|---:|---:|---:|---|---|
| A. steel exposed indoors | 0.000 | **0.236** | -2.9 | **FAIL** | **FAIL** |
| B. steel under a 22 mm timber deck | 0.169 | **0.617** | 8.5 | **FAIL** | **FAIL** |
| C. steel + 6 mm PU pad + timber deck | 0.409 | **0.776** | 13.3 | pass | pass |
| D. steel + 10 mm PU pad + timber deck | 0.569 | **0.824** | 14.7 | pass | pass |
| E. steel + neoprene 6 mm + timber deck | 0.209 | **0.657** | 9.7 | **FAIL** | pass |

**The bare case is not marginal, it is catastrophic.** f = 0.236 against a required 0.754, so the surface sits at **-2.9 °C** when it is −10 °C outside — below the 9.3 °C dew point, so it is wet, and below freezing, so it is frost. It condenses whenever the outdoor temperature falls below **5.9 °C**, which on the Bergen coast is most of the heating season rather than a cold snap.

That is worth stating plainly because it is not an energy argument. A junction that condenses for six months a year will rot the timber it touches, and no amount of insulation elsewhere in the wall changes it.

## 4. What it takes to pass

On a one-dimensional path, reaching the mould criterion needs an **added resistance of 0.358 m²K/W** between the steel and the warm side. Expressed as a single layer of one material:

| Material | λ W/mK | Resistance of 10 mm | Thickness needed |
|---|---:|---:|---:|
| timber | 0.130 | 0.077 | **47 mm** |
| rigid PU foam | 0.025 | 0.400 | **9 mm** |
| neoprene | 0.150 | 0.067 | **54 mm** |

**Mould governs, not condensation.** The condensation criterion needs only 0.193 m²K/W, so a detail sized for mould is automatically dry. Sizing to the condensation limit alone would leave a surface that stays wet enough for long enough to grow things.

## 5. The requirement moves with the assumptions

| Indoor RH | Critical f | Added R needed |
|---|---:|---:|
| 40 % | 0.642 | **0.193** |
| 50 % | 0.754 | **0.358** |
| 60 % | 0.848 | **0.684** |

| Outdoor design | Critical f | Added R needed |
|---|---:|---:|
| -5 °C | 0.705 | **0.270** |
| -10 °C | 0.754 | **0.358** |
| -15 °C | 0.789 | **0.446** |
| -20 °C | 0.816 | **0.534** |

**Indoor humidity moves the requirement harder than the weather does.** Across the swept ranges, 40 → 60 % RH multiplies the required break by **3.5×**, while −5 → −20 °C outdoors multiplies it by only **2.0×**. And 60 % is what a small heated space with a stove, cooking and washing produces — so ventilation (§13-1(1)) and the wet room stop being comfort items and become part of the junction design.

## 6. The corner is worse than the wall

| Surface | R_si | Bare f_Rsi | Added R needed |
|---|---:|---:|---:|
| flat wall | 0.13 | 0.236 | **0.358** |
| floor, downward | 0.17 | 0.191 | **0.481** |
| concave corner | 0.25 | 0.139 | **0.726** |

The network can also be run with the higher surface film resistance a concave junction has — the air in a corner is stiller and the surface sees less of the room, and some national annexes to ISO 13788 use 0.20–0.25 there. Under that treatment the required break roughly doubles.

**This is a 1D stand-in for a 2D effect, so it must not be added to the caveat in §7** — it is the same physics seen through a different lens. What it does establish is that the floor-to-wall corner, where the chassis perimeter beam sits, is the governing point rather than the flat wall, and that a break sized on the flat wall is sized on the easier of the two.

## 7. The limit of this screen, and it has now been measured

The one-dimensional network used above **ignores lateral heat flow**, and a linear junction concentrates exactly that. So no f_Rsi here can be read as a bound on the building — and [the 2D calculation](verificacion-puente-2d.md) has since been run on the same junction, which turns that caution into three specific corrections:

1. **The direction of the error was backwards for the steel.** This screen gives 0.236 for the bare member; 2D gives **0.377**. Lateral feed from the surrounding floor warms the steel, so the 1D value was a *lower* bound on that surface, not an upper one. The number was a bound and the stated sign of the error was wrong.
2. **The steel is not the governing surface once any break is built.** From the first millimetre of pad the coldest point moves to the **timber corner**, and it stays there for every thickness. A break sized to protect the steel is sized on the surface that has already stopped governing.
3. **So the requirement is larger than this screen says.** In 2D, 20 mm of rigid foam reaches the criterion and 9 mm does not — 0.693 against 0.754. The requirement is **0.80 m²K/W**, not 0.358, and the difference is not a refinement: the 1D answer is 0.44 m²K/W short.

What survives unchanged is the conclusion: **a thermal break is mandatory and it has a size.** What does not survive is the claim that the size is a floor this screen can certify — it is a floor on a surface that stops governing as soon as it is built.

There is a second thing this screen cannot see at all: the **vapour barrier penetration**. A chassis member passing through the wall interrupts the barrier, and §13-13's Sd ≥ 10 m is only satisfied if that interruption is sealed. Convective leakage through a barrier defect carries far more vapour than diffusion and is invisible to any 1D model — the same limitation the envelope screen records.

## 8. What this changes

1. **The chassis junction is a moisture problem before it is an energy problem.** The thermal-bridge screen said it costs 16 % of heat loss; this one says a naive detail condenses below 5.9 °C. The second is the one that damages the building.
2. **A thermal break is mandatory, and it has a size.** Not "a thermal break" as a gesture: **0.80 m²K/W** on the governing surface, which is 20 mm of rigid foam or 104 mm of timber. A timber deck alone is not enough — it reaches only 0.617. Padding is not the only option and it is the worse one: putting the steel outside the insulation recovers the bare corner exactly, at no thickness at all.
3. **Size for mould, not for condensation.** The condensation limit is the weaker of the two and sizing to it leaves a surface that is wet but not dripping.
4. **The governing point is the floor-to-wall corner**, where the perimeter beam is and where R_si is highest. A detail that works on the flat wall may not work there.
5. **Indoor humidity is a design parameter.** Moving from 40 % to 60 % multiplies the required break by 3.5×, more than the whole outdoor range does, so ventilation (§13-1(1)) and the wet room stop being comfort items and become part of the junction design.

## 9. Limits

- **The numbers here are 1D and are not bounds on the building.** [The 2D screen](verificacion-puente-2d.md) corrects the requirement from 0.358 to 0.80 m²K/W and shows the governing surface is not the one this network computes.
- **No junction detail exists.** The 2D screen models a steel plate, not a chassis member: the profile is not selected, so the geometry that would make this a design value does not exist either.
- The outdoor design temperature is a **screening value**; the National Annex and the site are both missing (S014, C-01).
- Interstitial condensation inside the wall is **not** modelled here — the envelope screen's Glaser profile covers the field of the wall, not the junction.
- Air leakage and the barrier penetration are outside any 1D model and are recorded, not assessed.
- No product is selected. The layer resistances use generic lambda values.
- Nothing here is a junction design, a compliance statement or an energy calculation.

- Generated by `scripts/condensacion_union.py`; JSON companion: `knowledge/comparisons/condensacion-union.json`.
