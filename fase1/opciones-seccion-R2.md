# MiniHouse · R2 section options

**State:** OPTIONS — NO SELECTION, NO GEOMETRY FROZEN. Four configurations, computed with the same section model, so the choice can be made on numbers.

- Constraint set: **2.2 m** free height (§12-7(2)(c), S025), **4.00 m** transport screening value (S022), floor 250 mm and roof 300 mm from the [envelope screen](verificacion-envolvente.md).
- The conflict is established in [verificación de sección](verificacion-seccion.md) and is not re-derived here.
- Internal width after a 264 mm wall: **2.47 × 5.47 m = 13.53 m²**.

## 1. The four configurations

| Option | Pitch | Stack | Limit | Wall at eave | 2.2 m band | Low zone | Transport |
|---|---:|---:|---:|---:|---:|---:|---:|
| **R2-A** Shallow gable, full headroom | 8° | 900 | 4000 | 2336 | full width | — | 4000 |
| **R2-B** 20° gable, low side zones | 20° | 1100 | 4000 | 1785 | 718 mm | 1141 mm/side | 4000 |
| **R2-C** 15° gable on a low loader | 15° | 700 | 4000 | 2337 | full width | — | 4000 |
| **R2-D** 20° gable with a dispensation | 20° | 1100 | 4400 | 2185 | 2916 mm | 42 mm/side | 4400 |

`Wall at eave` is the free height at the wall, which is also the tallest the wall can be under the limit. `Low zone` is the strip along each long wall that sits below 2.2 m.

## 2. The build-ups these numbers came from — and a correction

The four options above were solved with **floor 250 mm and roof 300 mm**, described as coming from the envelope screen. **They do not.** Those are round numbers, and the envelope solver returns a **thicker floor and a thinner roof** at the same U-values:

| Timber fraction | Floor build-up | Roof build-up | vs 250 / 300 |
|---:|---:|---:|---|
| 15 % | **281 mm** (241 insulation) | **278 mm** (245 insulation) | floor +31, roof -22 |
| 12 % | **268 mm** (228 insulation) | **264 mm** (232 insulation) | floor +18, roof -36 |
| 8 % | **250 mm** (210 insulation) | **246 mm** (214 insulation) | floor +0, roof -54 |

**The floor is 31 mm thicker than assumed and the roof 22 mm thinner, so the two nearly cancel** — the published wall heights are optimistic by only about 7 mm. The reference case was close, not wrong, and the −422 mm deficit is robust.

What is not close is the **timber fraction**. It is the member width divided by the centres, not a material property, so the envelope screen's uniform 15 % is a choice rather than a result. Re-solving the same four options across the plausible range:

| Option | Published | 15 % studs | 12 % effective | 8 % field |
|---|---:|---:|---:|---:|
| **R2-A** | 2336 / 100 % | 2328 / 100 % | 2355 / 100 % | 2390 / 100 % |
| **R2-B** | 1785 / 24 % | 1778 / 23 % | 1806 / 28 % | 1842 / 34 % |
| **R2-C** | 2337 / 100 % | 2330 / 100 % | 2357 / 100 % | 2393 / 100 % |
| **R2-D** | 2185 / 97 % | 2178 / 96 % | 2206 / 100 % | 2242 / 100 % |

The framing is worth more than the build-up correction by an order of magnitude: at 8 % **R2-B rises from 23 % to 34 %** of the width and **R2-D reaches full coverage**. That does not rescue R2-B — it is still a partial-coverage option — but it changes how much the low zone has to absorb, and it is the only lever of any size that costs nothing at the transport limit.

**The lesson is the same one the roof determination produced:** state the member width and the centres, not a fraction. A fraction written as though it were a property turns a screening choice into a false basis.

### What the dispensation actually has to ask for

R2-D is described as a dispensation to **4400 mm**. That is a round number too, and it is not enough. The limit at which the 2.2 m band reaches the full width at 20° and a 1100 mm stack is:

| Build-ups | Limit needed for full coverage | vs the 4400 mm in the option table |
|---|---:|---|
| 15 % timber fraction | **4422 mm** | **short by 22 mm** |
| 12 % timber fraction | **4394 mm** | 6 mm to spare |
| 8 % timber fraction | **4358 mm** | 42 mm to spare |

**At the envelope screen's own 15 % the dispensation is 22 mm short**, and even at the published 250 / 300 build-ups it needs 4415 mm. So R2-D's 4400 mm was never the threshold for full coverage — it was a round number that happened to land at 97 %.

The framing relief fixes it: at 12 % or less, 4400 mm is enough. That is worth knowing before the application is written, because **the number in the application is the one that gets assessed**, and asking for 4400 when 4422 is needed invites a refusal that a slightly different frame would have avoided.

## 3. What each one costs

| Option | What it costs | What it depends on |
|---|---|---|
| **R2-A** | the roof reads almost flat; the gable in the reference images becomes a ridge line | nothing new — the pitch is the only thing that changes |
| **R2-B** | 2.2 m only over the central band; bathroom, kitchen and storage move to the low zones | the coverage-fraction decision, and a plan that uses the low zones |
| **R2-C** | a specialised low-deck trailer, which may cost more per move and is not available on every route | a trailer with a 700 mm deck (C-06) |
| **R2-D** | a permit application before every move, and the risk that one route refuses it after the cabin is built | a VegSak dispensation on every move |

## 4. The low zone is not waste — it is the plan

R2-B is the only option that keeps the 20° gable without a permit or a special trailer, and it is the one that looks like a compromise. The numbers say otherwise.

| Option | 2.2 m band | Low zone per side | Low-zone area per side | Height at the wall |
|---|---:|---:|---:|---:|
| **R2-A** | full | — | — | 2336 mm |
| **R2-B** | 718 mm | 1141 mm | 6.24 m² | 1785 mm |
| **R2-C** | full | — | — | 2337 mm |
| **R2-D** | 2916 mm | 42 mm | 0.23 m² | 2185 mm |

In R2-B the low zone is **1141 mm deep along each 6 m wall** — **6.24 m² per side** — with the ceiling running from **1785 mm at the wall up to 2.2 m** where it meets the band. That is enough for:

- a **bathroom** ~1.1 × 2.0 m against a long wall, with the shower at the high end;
- a **kitchen run** at 600 mm depth with wall cabinets, which needs no headroom at all;
- **full-height storage** along the remainder, which is the scarcest thing in an 18 m² cabin.

This is the ordinary logic of an attic flat, and it changes the reading of the earlier result: **24 % coverage is not a failure, it is a plan constraint** — provided the plan puts the low-headroom functions at the edges and keeps the central band for standing, sitting and circulation.

The one thing it rules out is a **sleeping loft**. The free height at the ridge is **2331 mm**, so there is no 1600 mm of headroom above a loft floor at 2.2 m. A loft would need a much steeper roof, which the transport limit does not allow.

**But read §4 before treating R2-B as viable.** This reading only holds if the wall really reaches 1785 mm and nothing else in the transport budget is spent. It is a contingent option, not a robust one.

## 5. Tolerance: none of these options has any

Every option above solves **to** the limit, so the wall height quoted is a maximum and the transport height is exactly 4.00 m (or 4.40 m for R2-D). Real roofs have ridge caps, overhangs, vents and lifting ears. Taking a **100 mm** reserve off the wall changes the picture unevenly:

| Option | Wall (max) | Wall with reserve | Coverage, max | Coverage with reserve | Survives |
|---|---:|---:|---:|---:|---|
| **R2-A** | 2336 mm | 2236 mm | 100% | 100% | yes |
| **R2-B** | 1785 mm | 1685 mm | 24% | 6% | **no** |
| **R2-C** | 2337 mm | 2237 mm | 100% | 100% | yes |
| **R2-D** | 2185 mm | 2085 mm | 97% | 79% | **no** |

This is the sharpest thing in the report. **R2-A and R2-C absorb a reserve and still give full headroom. R2-B does not**: its 24 % coverage is bought with every millimetre of the budget, and a 100 mm allowance takes it to single digits. An option that only works at exactly zero tolerance is not a robust option — it is a calculation.

**The framing relief does not change that verdict, and it is worth showing why.** Slimming the frame to an 8 % fraction buys 57 mm of wall on R2-B and takes its coverage from 23 % to 34 % — but the same 100 mm reserve then takes it back to **16 %**, and R2-D from 100 % to **89 %**:

| Option | 15 % framing, with reserve | 8 % framing, with reserve |
|---|---:|---:|
| **R2-A** | 100 % | 100 % |
| **R2-B** | 4 % | 16 % |
| **R2-C** | 100 % | 100 % |
| **R2-D** | 78 % | 89 % |

So the reserve test separates the options the same way however the frame is built: **only R2-A and R2-C survive it.** That is a stronger conclusion than the original table, because it now survives the one correction that could have overturned it.

## 6. How the options divide

- **Full 2.2 m across the width:** R2-A, R2-C — these close the room-height question completely and pay for it elsewhere.
- **Effectively full, at 4.40 m:** R2-D.
- **Genuinely partial:** R2-B — keeps the gable and turns the low zones into programme, but only with zero tolerance.
- **None of them gives a loft**, because the transport limit caps the ridge height before a loft becomes possible.

## 7. What has to be decided, and by whom

| Question | Owner | Effect on the choice |
|---|---|---|
| How much is the 20° gable worth? | **Carlos** | decides between R2-A and R2-B more than any technical input |
| What trailer deck height is actually available? | carrier (**C-06**) | decides whether R2-C exists at all |
| Is a VegSak dispensation acceptable on every move? | **Carlos** | decides whether R2-D is a design or a habit |
| What floor and roof build-up will really be built? | **C-02** | shifts every number in this table by tens of millimetres |
| What fraction of the floor must reach 2.2 m? | **Carlos** + municipality | decides whether R2-B's 24 % is acceptable |

**No option is recommended here.** The technical work has narrowed the choice to four; the rest is a value judgement about how the cabin should look and how it should be moved, and that belongs to Carlos.

## 8. Limits

- **Parametric and coarse.** Build-ups are round numbers consistent with the envelope screen; no material, member or product is selected.
- **No salients, overhangs, chimney, vents or lifting ears** are in the transport height. Each would consume margin, and R2-A and R2-C have none to spare.
- **The 4.00 m limit is a screening value**, not a route permit; R2-D assumes 4.40 m is obtainable, which has not been checked against any vegliste.
- **Free height is to the underside of the roof plane**, ignoring lining, ties and services.
- Nothing here is a compliance certificate, a siting approval or a fabrication release.

## 9. Source and status

- §12-7(2)(c) 2.2 m: S025. §14-3 envelope: S011 + [envelope screen](verificacion-envolvente.md).
- Transport screening value: S022. Dispensation route: S009.
- Section model: `scripts/section_feasibility.py`. Generated by `scripts/section_options.py`; JSON companion: `knowledge/comparisons/section-options.json`.
- OPTIONS ONLY — no pitch, build-up or geometry selected.
