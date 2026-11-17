# MiniHouse · the chapter 11 determinations, and which clauses move together

**State:** DETERMINATION — NOT A FIRE-ENGINEERING ANALYSIS, NOT A COMPLIANCE STATEMENT. Nothing here decides what the municipality will accept; it decides which question to put to it, and prices both answers.

- Basis: the verified clause texts in S024 read against the **R0 layout**. Risk class 4, brannklasse 1.
- The window cost is imported from the window screen and the door figures from the fire screen, so this report cannot drift from either.
- **Screening values**, not measurements: the travel distance is a straight line and the timber area is computed at the reference section.

## 1. What this adds

Chapter 11's clauses are verified in [S024](../knowledge/sources/S024.md), and the project has priced several of its open questions separately: the escape windows in [the window screen](verificacion-ventanas.md), the roof branch in [the roof determination](determinacion-cubierta-incendio.md), the door width in [the fire screen](verificacion-incendio.md). What nobody has asked is whether two of those questions are the same question — and two of them are.

## 2. The coupling

> §11-13(4): «… kan utgangen fra branncelle enten føre til **sikkert sted**, eller til **rømningsvei** som bare har én rømningsretning, forutsatt at hver branncelle har vinduer …»

The allowance is written as an **alternative**: either the exit leads to a safe place, *or* it leads to a rømningsvei with one direction and then the windows are required. It is not a permission that applies on top of a safe-place exit.

§11-14 then governs the **rømningsvei** — its free width, and the width of doors in or to it. If there is no rømningsvei, §11-14 has nothing to govern.

So one answer decides both, and with them three rows of the declaration of margins:

| Clause | Engaged when the exit reaches a safe place | Engaged when it reaches a rømningsvei |
|---|---|---|
| §11-13(1) | yes — that is how it is satisfied | yes — via the (4) allowance |
| §11-13(4) windows | **no** | **yes** |
| §11-14 free width | **no** | **yes** |
| §11-17 fire service | yes | yes |

Declaration rows **2, 3, 4** are therefore not three margins. They are one determination read three ways, and the table has been carrying them as if they were independent.

## 3. The two packages, priced

| | **P1** — safe place | **P2** — rømningsvei |
|---|---|---|
| Reading | the door discharges to a safe place | the exit leads to a rømningsvei with one direction |
| Basis | §11-13(1) satisfied directly — one exit to a safe place | §11-13(4) engaged — the allowance needs qualifying windows in every cell |
| Windows | none required as escape windows | a qualifying window in every room without a direct exit |
| Door width | §11-14 does not apply: there is no rømningsvei to be in or to | §11-14 applies: 0.86 m free width in the door |
| Cost | nothing | 0.29 m² of glass and a 100 mm sill drop |
| Risk | the municipality may not accept grade outside the door as a safe place | none — this is the conservative answer, and it is buildable |

**P2's window cost is the one already measured**: 0.29 m² of added glass, a 100 mm sill drop on V-02, and the minimum light transmittance requirement falls to 0.537 — the only lever in the project that closes two screens at once.

**P1's cost is nothing, and that is the whole difficulty.** It is the answer the design wants, it is available on the text, and it is the answer a project is least entitled to award itself.

## 4. What is *not* coupled, and why it matters

The obvious next step is to say that a strict answer on windows also raises the interior surfaces to **B-s1,d0** under §11-9, and that reclaimed timber therefore cannot stay exposed. **That is wrong, and it is wrong in both directions.**

§11-9 Table 1A separates fire cells that *are* an escape route from those that are not. In the ordinary reading a rømningsvei is a route **outside** the fire cell — the cell's exit leads to it — so a cell that contains none is not one. A cell that contains no rømningsvei is still a cell, so the ≤200 m² row applies to it whatever §11-13 decides. The two questions are independent:

| Clause | Value either way | Why it does not move |
|---|---|---|
| §11-9 surfaces | **D-s2,d0 walls and ceiling (cell ≤200 m²)** | a fire cell that contains no rømningsvei is still a fire cell, and the ≤200 m² row applies to it whatever §11-13 decides |
| §11-9 cladding | **K210 D-s2,d0** | the cladding is metal, so it meets either row without a product choice |
| §11-9 insulation | **A2-s1,d0** | already forced by §11-4(3) no. 6 as well; the roof is mineral wool either way |
| §11-17 fire service | **one accessible window** | applies on both packages, and V-01 already satisfies it |

This cuts both ways and both are worth stating. A strict answer on windows does **not** condemn the timber interior. And a favourable answer on windows does **not** entitle the project to call the interior an escape route's surface either — the D-s2,d0 row applies on its own terms.

## 5. Travel distance: satisfied, and the table row is still missing

The furthest point of the bathroom from the nearest door jamb is **5.04 m** — from (0, 0) mm to the jamb at 4050 mm. That is a **straight line**, so it is a lower bound on the walking path and the margin below is an upper bound.

| Figure | Value | Source |
|---|---:|---|
| Maximum internal distance | **5.04 m** | plan geometry, straight line |
| Door of the fire cell to the nearest exit, one stair | 15 m | §11-14, S024 |
| Same, several stairs or exits | 30 m | §11-14, S024 |

So the margin against the loosest figure the retrieved text contains is **+10.0 m**. But §11-14's figures are for the distance from the **door of the fire cell** to the nearest stair or exit — not for travel inside the cell — and the §11-13 Table 1 row for risk class 4 is **not in the retrieved text**. The honest statement is therefore: the cabin's internal distance is small, it is comfortably inside every figure the source does contain, and the applicable row has never been read.

This is the one place in chapter 11 where the answer is very unlikely to be the constraint. It should still be confirmed rather than assumed, because the number is cheap to check and the assumption would be invisible in the drawing.

## 6. The door, under each package

§11-14 asks for **860 mm** free width in risk class 4. A 900 mm leaf is **40 mm** wider than that, which is where declaration row 2's +40 mm comes from — and the declaration already says it is not a margin, because the free width is the leaf minus a frame and hinge build-up nobody has specified.

Under **P1** the clause does not apply at all, so the 900 mm leaf stops being a requirement and becomes a choice. That does not make the door better; it means the project would be choosing 900 mm for reasons of its own, and should say so rather than book it as a margin.

Under **P2** the clause applies and the +40 mm is a real margin on a real requirement — still undemonstrated, for the reason the adequacy screen gives.

## 7. The question to put, and it is one question

The project has been carrying the window question and the door-width question as separate items. They are one. The technical cupboard, the escape-route classification and the travel distance are genuinely separate, and none of them is decided here. Put the coupled pair as one question with two priced answers:

> **Does the exit from the cabin lead directly to a safe place, or to a rømningsvei with a single escape direction?**

If a safe place: no escape windows are required, §11-14 does not apply, and the aperture table stands as drawn.

If a rømningsvei: every room without a direct exit needs a qualifying window, the door needs 0.86 m free width, and both are buildable for 0.29 m² of glass and a 100 mm sill.

Either way, the interior surfaces stay **D-s2,d0** unless the municipality separately decides the cabin *is* an escape route — which is the one answer that would put the reclaimed timber in question, and it is a different question from this one.

## 8. Limits

- The determinations here are readings of S024 against the R0 layout. They are **not** a fire-engineering analysis and **not** a municipal decision.
- The travel distance is a straight line from a room corner to a door jamb. The real path is longer, and the bathroom door is not modelled.
- The interior timber area, **48.5 m²**, is computed at the R0 reference section (eave 1778 mm, ridge 2324 mm) and moves with whichever R2 option is chosen.
- No B-s1,d0 product is specified, so no cost is attached to the surface class. The area is given so that the cost can be priced when a product exists.
- Nothing here is a compliance statement, a fire strategy or a design release.

- Generated by `scripts/estrategia_incendio.py`; JSON companion: `knowledge/comparisons/estrategia-incendio.json`.
