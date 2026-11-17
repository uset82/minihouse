# MiniHouse · the roof under TEK17 chapter 11

**State:** DETERMINATION — NOT A FIRE-ENGINEERING REPORT, NOT A STRUCTURAL CHECK.
S024 leaves one interpretation open and says it must be settled before the roof build-up is frozen ([S024](../knowledge/sources/S024.md)). This document settles the part of it that can be settled, and prices the part that cannot.

## 1. The question, stated properly

§11-4(3) no. 6 lets a roof be built **without a specified fire resistance** where it has no decisive importance for stability in the escape phase. If the roof *is* part of the **main load-bearing system**, no. 6 is not available and no. 4 gives **R 15** instead. The card records that this depends on the structural system, which is not chosen, and warns against assuming the cheaper reading.

That is correct as far as it goes. But it is not the question that decides the build-up.

## 2. Four branches, one insulation conclusion

| Branch | What it asks of the rafters | What it asks of the insulation | Lining |
|---|---|---|---|
| **no. 4 — roof is part of the main system** | R 15 on the load-bearing roof (§11-4(3) no. 4, BKL 1, risk class 4) | A2-s1,d0 (§11-9 D main rule) | none required by §11-4(3) |
| **no. 6.1 — fire-cell-dividing element** | no specified roof resistance; the element below is dimensioned for two-sided fire | A2-s1,d0 (§11-9 D main rule) | two-sided fire-cell element |
| **no. 6.2 — all roof materials A2-s1,d0** | no specified roof resistance | A2-s1,d0 (explicit in 6.2) | none — but no timber anywhere in the roof |
| **no. 6.3 — protected from below** | no specified roof resistance | A2-s1,d0 (explicit in 6.3) | K210 B-s1,d0, or D-s2,d0 in risk class 4 |

**The insulation column is identical in all four rows.** That is the finding: the interpretation question governs the **rafters** and the **lining**, and it does not govern the insulation at all.

The reason is that §11-9 D is an independent clause. Its main rule requires insulation meeting **A2-s1,d0**, and the only exception that could reach a timber roof is no. 7 — which requires a **load-bearing substrate meeting A2-s1,d0 with documented R-class**. A timber rafter is not that. So the insulation is A2-s1,d0 whether the roof is main-system or not, and no. 6.2 and 6.3 say the same thing in their own words.

**Consequence: the roof build-up can be frozen now.** It is mineral wool, and the interpretation question is not a blocker for it — it is a blocker for the rafter section and the ceiling lining.

Two branches can also be closed immediately:

- **no. 6.2 is unavailable.** It requires *all* materials in the roof construction, including insulation, to satisfy A2-s1,d0. A timber rafter and a timber deck cannot, so 6.2 describes a non-combustible roof — a different building.
- **no. 6.1 is available but architectural.** A two-sided fire-cell element between the roof and the room is a fire-rated ceiling, which is a decision about the section, not about the fire strategy.

That leaves **6.3** as the realistic route for a timber roof: a **K210 B-s1,d0** lining below, or **D-s2,d0** in risk class 4, with A2-s1,d0 insulation.

## 3. What R 15 actually costs the rafter

If the roof turns out to be main-system, the rafters need R 15 — and for a slender timber member R 15 is a **charring** problem, not a thickness problem. EN 1995-1-2 gives a notional charring rate of **0.65 mm/min** for softwood and a zero-strength layer of 7 mm, scaled by k₀ = t/20 for short fires. At 15 minutes that is an effective loss of **15.0 mm** per exposed face.

**Charring attacks the narrow dimension twice.** A rafter exposed on three sides loses the char depth from each side *and* from the bottom:

| Rafter mm | Residual mm | Section modulus retained | Width needed for parity |
|---|---|---:|---:|
| 48 × 198 | 18 × 183 | **32 %** | 78 mm |
| 48 × 223 | 18 × 208 | **33 %** | 78 mm |
| 73 × 198 | 43 × 183 | **50 %** | 103 mm |
| 73 × 223 | 43 × 208 | **51 %** | 103 mm |
| 98 × 198 | 68 × 183 | **59 %** | 128 mm |
| 98 × 223 | 68 × 208 | **60 %** | 128 mm |

A **48 mm** rafter keeps only about a third of its section modulus, because it loses 30 mm of its 48 mm width. Going deeper barely helps — the loss is in the width, not the depth, and 48 × 223 does no better than 48 × 198. The column on the right is the uncomfortable one: parity needs **78 mm** of width, and the next stock size above that is **98 mm** — the rafter doubles in width to keep the same fire capacity.

Whether that matters depends on the accidental load, which is **not known** — there is no structural model and no C-07. So it is swept rather than assumed:

| Accidental moment as fraction of cold capacity | Rafters that pass | Rafters that fail |
|---|---|---|
| 40 % | 73x198, 73x223, 98x198, 98x223 | 48x198, 48x223 |
| 50 % | 73x198, 73x223, 98x198, 98x223 | 48x198, 48x223 |
| 60 % | 98x223 | 48x198, 48x223, 73x198, 73x223, 98x198 |
| 70 % | *none* | 48x198, 48x223, 73x198, 73x223, 98x198, 98x223 |

The pattern is what matters rather than any single cell: **the ordinary 48 mm rafter fails at every swept load**, and it takes roughly 73 mm of width before the residual section is even half the cold one.

There are two ways out, and they converge:

1. **Protect the rafters from below.** A lining delays the start of charring, and if it holds for the fire duration the section is unreduced.
2. **Use a wider rafter.** 78 mm for parity, so in practice 98 mm stock — which changes the rafter width, not the depth, and therefore does not touch the section.

Route 1 is also what **no. 6.3** requires, and what §11-9 D no. 7 would require if combustible insulation were ever justified. **So the fire requirement and the insulation requirement land on the same detail: a lining below the rafters.** That is the useful convergence in this chapter — three clauses, one drawing.

## 4. What the determination costs the section

The insulation is mineral wool, so the wood-fibre option is off the table without a documented fire-engineering analysis. That has a thickness consequence:

| Insulation | λ W/mK | Thickness for U 0.18 | Vertical at 20° | Permitted |
|---|---:|---:|---:|---|
| mineral wool (A2-s1,d0) | 0.035 | **245 mm** | 261 mm | yes |
| wood fibre (combustible) | 0.040 | **268 mm** | 286 mm | **no** |

So the fire determination costs about **23 mm** of roof thickness against wood fibre, which at 20° is **25 mm of eave height** — small against the 422 mm deficit the section already carries, and not the reason the section does not close. It is worth stating because it is the only part of this chapter that touches the binding constraint, and it turns out to be cheap.

## 5. The timber fraction is a geometry result, and that corrects a basis

Widening the rafter to satisfy R 15 is not free, because the timber fraction in a roof is **not a material property** — it is the member width divided by the centres. The envelope screen assumes a uniform **15 %**, which at 600 mm centres means **90 mm** members. For the slender framing this cabin would actually use, 15 % is conservative:

| Centres mm | Member mm | Timber fraction | Wool for U 0.18 | Vertical at 20° |
|---:|---:|---:|---:|---:|
| 400 | 48 | 12.0 % | **232 mm** | 246 mm |
| 400 | 73 | 18.2 % | **260 mm** | 277 mm |
| 400 | 98 | 24.5 % | **289 mm** | 308 mm |
| 600 | 48 | 8.0 % | **214 mm** | 228 mm |
| 600 | 73 | 12.2 % | **232 mm** | 247 mm |
| 600 | 98 | 16.3 % | **251 mm** | 267 mm |

This cuts both ways, and the two directions are worth separating.

**It may give the section relief, and the size of that relief is uncertain.** At 48 mm members on 600 mm centres the roof field needs **214 mm** of wool, against the 245 mm the envelope screen reports from its uniform 15 %. But the field fraction is not the **effective** fraction: sole and top plates, noggins, jack studs at openings and the double studs at the ridge all add timber that the width-over-centres figure ignores. At an effective 12 % the roof needs **232 mm**. So the honest range is **214–232 mm**, i.e. **13 to 31 mm** less than the screen, or **14 to 33 mm of eave height** returned to a section that is 422 mm short. It is real but it is not free money, and it depends on how the frame is actually built.

**It also makes the fire branch expensive.** If R 15 forces **98 mm** rafters the timber fraction rises to 16.3 % and the roof needs **251 mm** — **37 mm more** than the slender case, which at 20° is **40 mm of eave height**. So the real cost of the unfavourable fire reading to the section is about **40 mm**, not the 25 mm the insulation choice costs.

**This is a correction to the envelope screen's basis, and it is recorded as one.** The 15 % was a defensible screening value but it was applied as though it were a property. It is not: the project should state the **member width and the centres**, not the fraction — which is one more thing that waits on the structural scheme.

## 6. What this changes

1. **The roof build-up is no longer blocked.** The insulation is A2-s1,d0 in every branch, so it can be frozen as mineral wool now, without waiting for the structural scheme.
2. **What remains open is narrower than recorded.** The question is not "is the roof main-system" in general; it is "do the rafters need R 15, and is the lining K210" — two questions about one detail, and both are answered by the same lining.
3. **R 15 is a charring problem, and a 48 mm rafter does not survive it.** Parity needs 78 mm of width, so in practice 98 mm stock — the rafter doubles in width, not in depth.
4. **No. 6.2 is closed** — it describes a non-combustible roof, which this is not.
5. **The envelope screen may have 13–31 mm of thickness it did not need to spend.** A uniform 15 % timber fraction implies 90 mm members; slender framing on wide centres needs 214–232 mm rather than 245 mm, which is **14–33 mm of eave height**. It is the cheapest relief available and it is not free: plates, noggins and jack studs push the effective fraction back up.
6. **The fire branch costs 40 mm of eave height**, because wider rafters raise the timber fraction. That is the largest coupling between chapter 11 and the section, and it is bigger than the insulation choice costs.
7. **State width and centres, not a fraction.** A stud fraction is a geometry result; writing it as a material property is how a screening assumption becomes a false basis.

## 7. Limits

- **Not a fire-engineering analysis.** The branch structure is a reading of the retrieved text; a fire engineer must confirm it.
- **Not a structural check.** The charring model gives a residual section and a ratio; it does not verify the rafter, because the loads and the structural system are unknown.
- The accidental load is **swept, not known**. No structural model exists and C-07 is open.
- Charring is modelled on three sides with the top against the deck. Deck, lining and connection charring are outside this screen.
- The insulation thicknesses come from the envelope solver at a 15 % stud fraction with generic λ; no product is selected.
- Smoke, toxicity, BROOF(t2), fire-service access and sprayed protection are outside.
- Nothing here is a compliance statement or a design release.

- Generated by `scripts/cubierta_incendio.py`; JSON companion: `knowledge/comparisons/cubierta-incendio.json`.
