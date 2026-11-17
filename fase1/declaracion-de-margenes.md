# MiniHouse · Declaration of margins under TEK17 §2-2(3)

**State:** DECLARATION — NOT A COMPLIANCE STATEMENT, NOT A DESIGN RELEASE.
Every value below is a screening value taken from the report named in the row. No number here
is a measurement, and the declaration is void as soon as R2 is chosen and the geometry moves.

**Why this document exists.** §2-2(3) allows compliance to be shown by analysis only if the
method is *suitable and valid*, the assumptions are *described*, the assumptions are
*justified*, and the **necessary safety margins are stated**. The audit in
[`documentacion_check.py`](../scripts/documentacion_check.py) found the first three met across
all thirteen screening reports and the fourth met by only three, in three different currencies.
This document replaces those three partial statements with one position.

It reaches a conclusion the project has been avoiding: **it is not short of a margin
statement. It is short of margin.**

---

## 1. What the word has been doing

Three different things have been called "a margin" in this repository, and they are not
interchangeable:

| Called a margin | What it actually is | Why it is not a margin |
|---|---|---|
| The **4.00 m** general height value (S022) | A regulatory screening value | It is the *limit*, not an allowance against it. Using it as a design dimension leaves zero |
| The **100 mm** R2 reserve | A dimensional allowance | This one is a genuine margin — and the R2 solver shows it destroys two of four options |
| The **1.4** material factor (natural hazards) | A partial factor on soil strength | It is not a margin on the hazard class, and applying it as one double-counts |

A margin is therefore defined here operationally, so that it can be checked:

> **margin = value available − value required**, expressed in the units of the governing
> quantity, signed, and accompanied by the uncertainty of the model that produced it.

A margin is *stated* only when all four parts are present. A margin is *adequate* only when it
is positive and larger than that uncertainty. Where a quantity cannot be fixed yet, the entry
is **undefined** — and undefined is a legitimate entry that must not be filled with a
plausible number.

---

## 2. Every screen, with its margin

| # | Screen | Governing quantity | Available | Required | Margin | Verdict |
|---|---|---|---:|---:|---:|---|
| 1 | Daylight §13-7 | Light transmittance LT | product not chosen | 0.510 (ff 1.00) – 0.638 (ff 0.80) | **undefined** | waits on glazing |
| 2 | Fire ch. 11 — door | Free width | 900 mm leaf | 860 mm | **+40 mm** | **positive, thinnest in the project** |
| 3 | Fire ch. 11 — escape window sill | Sill height, worst window | 1500 mm (V-03) · 1100 (V-02) · 900 (V-01) | ≤1000 mm | **−500 / −100 / +100 mm** | **negative on two of three** |
| 4 | Fire ch. 11 — escape window size | h / w / h+w, worst window | 500 / 500 / 1000 mm (V-03) | 600 / 500 / 1500 mm | **−100 / 0 / −500 mm** | **negative** |
| 5 | Room height §12-7 | Eave height at 20°, 1100 mm stack | 1778 mm | 2200 mm | **−422 mm**, band −358 to −498 | **negative** |
| 6 | Natural hazards ch. 7 | Freeboard above flood datum | 300 mm | no regulatory figure | +300 mm | positive but a **project choice**, not a regulatory number |
| 7 | Envelope §14-3 — wall U | W/m²K | 0.2202 at the solved 189 mm | 0.22 | **0 mm by construction**; band +0.024 to −0.027 | **zero by construction**, and the band changes sign |
| 8 | Thermal bridges | Ψ″ W/m²K | 0.210 ordinary detailing | 0.05 (voluntary) | **−0.160** | **negative** against a non-binding benchmark; one junction now calculated, 0.027 wrapped to 0.195 unwrapped |
| 9 | Integrated section | Width reaching 2.2 m | ~24 % | no fraction given | **undefined** | no limit exists to measure against |
| 10 | R2 options | Transport envelope | 4000 mm | 4000 mm | **0 mm**, then **−100 mm** with the reserve | **zero by construction**; the R2-D dispensation is itself **22 mm short** at a 15 % timber fraction |
| 11 | Installations — drain | Cover above main crown | +940 / −160 mm | 560 mm minimum | +940 / **−160 mm** | **site-dependent, negative on one route** |
| 12 | Lift geometry | Per-leg tension | undefined | accessory capacity | **undefined** | C-07 missing |
| 13 | Condensation at the junction | Added resistance m²K/W | 0.000 bare / 0.409 with a 6 mm pad | **0.80** (2D) | **−0.80 / −0.39** | **negative**, and the 1D requirement of 0.358 was 0.44 too small |
| 14 | Ventilation §13-1(1) — flue | Net draught at the flue, Pa | **−130 Pa** at the highest pressure the extract can hold | **> 0 Pa** | **−130 Pa** | **negative — the flue reverses; only a room-sealed stove retires it** |

**Tally: two rows are positive, and one of those is a project choice rather than a regulatory
number.** Seven are negative, three are undefined, and **two are zero by construction**. The fire
margins do not offset anything outside chapter 11.

Rows 3 and 4 are stated on the **worst** window, not the best one, because that is how a
requirement has a margin. An earlier version of this table reported V-01 — the only window that
qualifies — and recorded **+100 mm** of sill and **+500 / +700 / +800 mm** of size. Those numbers
are true of V-01 and false of the requirement: two of the three windows fail, and
[the window screen](verificacion-ventanas.md) shows that under the strictest reading of §11-13
the aperture table has the **largest dimensional deficit in the project**, −500 mm, ahead of the
section's −422 mm.

That is the answer to §2-2(3), and it is not the answer the project wanted: the margins cannot
be *stated as adequate*, because most of them are not positive.

**Three of these rows are one determination, and the tally is conditional on it.** §11-13(4) is
written as an *alternative*: the exit leads either to a safe place, or to a rømningsvei with a
single direction and then the windows are required. §11-14 governs the rømningsvei and doors in
or to it. So if the door discharges to a safe place, **(4) is not engaged and §11-14 has nothing
to govern** — and rows 2, 3 and 4 all stop being requirements at once. Ten rows would then carry
a margin instead of thirteen, and the tally would read **1 positive / 4 negative / 3 undefined /
2 zero**: the only positive row left would be the flood freeboard, which is a project choice.
[The chapter 11 determination screen](determinacion-estrategia-incendio.md) prices both answers.

The table therefore states the **conservative** answer throughout, as §9 records for rows 3 and
4. That is deliberate: a margin measured against a requirement the building does not have is not
a margin, and a margin measured against a requirement it might not have is at least a bound.

**Row 14 is the only negative row with a costless resolution, and it has not been adopted.**
[The make-up air screen](verificacion-aporte-aire.md) sizes the remedy the ventilation screen left
unnamed — a **113 mm** inlet at **10 Pa** of design depression, which is one wall valve and takes
98 Pa out of the 106 Pa the basic extract would otherwise carry — and then shows that the remedy
cannot rescue the flue. The only depression that satisfies the §2-2(3) adequacy test needs a
**181 mm** inlet at 2 Pa, and 2 Pa is below the pressure a 3 m/s breeze puts on a wall: a passive
inlet cannot hold a set pressure at all. A **room-sealed** stove removes the coupling instead of
shrinking it, because its flue is balanced against the outside and the cabin's pressure never
enters the draught. So this row does not become positive — **it stops being a margin** — and that
is a specification decision, not a calculation. Until it is taken, the row stands at **−130 Pa**.

What does **not** move with that answer is §11-9's surface class. A fire cell that contains no
rømningsvei is still a fire cell, so **D-s2,d0** governs walls and ceiling whatever §11-13
decides — which is the answer that keeps reclaimed timber exposed. The two questions are
independent, and coupling them would have condemned the interior on a reading that does not
reach it.

**One screen deliberately has no row.** The R 15 charring check on the roof rafters
([determinación de la cubierta](determinacion-cubierta-incendio.md)) is **conditional** on which
branch of §11-4(3) applies, and that branch is undetermined. Its margin is therefore not
undefined-in-principle but *undefined-until-a-condition-is-decided*, which is a different state
and should not be merged with rows 1, 9 and 12. It acquires a row the moment the structural
scheme settles the branch — and on the numbers it already has, a 48 mm rafter would enter that
row negative.

---

## 3. The four currencies, and which one governs what

Stating every margin in one unit is impossible; stating each in the right unit is not. The rule
adopted here is one currency per analysis type:

| Analysis type | Currency | Why |
|---|---|---|
| Dimensional (height, pitch, transport, door width) | **mm** on the governing dimension | the quantity is a length and the limit is a length |
| Thermal (U-values) | **W/m²K** on the element | §14-3 gives element values |
| Thermal (junctions) | **W/mK mean Ψ per metre**, not W/m²K normalised | the normalised figure is area-dependent and mis-specified at 18 m² (see §6) |
| Moisture (temperature factor) | **m²K/W of added resistance** | f_Rsi is dimensionless, but the thing a detailer chooses is a thickness, so the margin is priced in resistance |
| Probabilistic (flood, landslide) | **annual probability** | the class *is* the margin — see §5 |
| Resistance (lifting, structure) | **dimensionless factor** on resistance | the quantity is a capacity ratio |
| Product-dependent (glazing, timber) | **undefined until the product is chosen** | a plausible number here would be an invention |

---

## 4. The margins are not additive, and «binding» means two different things

The envelope margin (zero by construction at the solved 189 mm) and the section margin
(−422 mm) sit on different quantities, so they cannot be traded off numerically. They are physically coupled in
the opposite direction: **the only way to recover the envelope margin at a 15 % stud fraction is
more insulation, and more insulation costs room height and transport envelope.** The thermal
bridge screen prices that trade exactly — +65 mm of roof insulation costs **69 mm of eave
height** — so spending one margin buys the other's deficit.

The correct object is therefore not a margin but a **margin vector**, and the design is
governed by its minimum component.

**Which component is the minimum depends on what "governed" means, and the two readings differ.**
By magnitude the minimum is now the escape window at **−500 mm** (row 3/4, V-03's sum rule). By
consequence it is still the section at **−422 mm** — the floor is 31 mm thicker than the R2
options assumed and the roof 22 mm thinner, so the two nearly cancel and the published wall
heights are optimistic by about 7 mm. The difference is that the window deficit is **closed by
enlarging a hole** and the section deficit is **closed by a dispensation or a shallower pitch**.
So the escape window is the largest number and the section is the one that constrains the
concept; both statements are true and neither replaces the other.

A third distinction matters for how the vector is read. Two of the seven negative rows —
the escape window and the R2 transport envelope — are negative **because the design was never
asked to satisfy them yet**: the aperture table is R0 and every R2 option was solved *to*
4000 mm. Those are open decisions, not physical limits. The section's −422 mm and the
condensation's −0.358 m²K/W are physical: no choice of window or option removes them without
changing the geometry.

---

## 5. The natural-hazard margin is already inside the class — do not add a factor

This is the one place where the project has been double-counting. TEK17 fixes flood at
**F2 = 1/200** and landslide at **S2 = 1/1000**. Those classes *are* the safety margin: they
are the regulation's own statement of how much rarer than the design event the hazard must be.
A 1/200 event has a 22 % chance of being exceeded in 50 years; that is the allowance.

Applying a **1.4 material factor** on top is not a margin on the class. It is a partial factor
on the *strength parameters* of a slope-stability model, which is a different calculation with a
different purpose. Both may be legitimate; conflating them is not. The screen must therefore
say which it is using, and the honest entry today is: **the class margin is given and met by
definition; the model's parameter factor is unverified and therefore not stated.**

---

## 6. The two junction rows, and why one is negative against a number that does not bind

Row 8 reads −0.160 W/m²K against 0.05, but **0.05 does not bind this building**: it sits in
§14-2's route, exempt via §14-5(1). The row is included because the project needs to see the
gap, not because it is a breach. The bridge screen also shows why the figure should not be
adopted as a target at all — at 18 m² it implies a mean Ψ of 0.0147 W/mK, under half of good
practice. **The stated target, if any, belongs per metre.**

Row 13 is the same junction read the other way, and its currency is different because its
consequence is. The energy margin can be negative without the building failing; the moisture
margin cannot. As drawn there is no break at all, so the available resistance is 0.000 and the
margin is simply minus the requirement.

**That requirement was wrong, and the 2D calculation found out by how much.** The 1D screen
priced the break on the steel: f_Rsi **0.236** against the 0.754 the mould criterion requires,
which is 0.358 m²K/W of added resistance, about 9 mm of rigid foam. [The 2D
screen](verificacion-puente-2d.md) solves the same junction and returns **0.377** for the steel —
higher, because lateral feed from the surrounding floor warms the member — and then shows that
the steel **stops being the governing surface at the first millimetre of pad**. From 3 mm onward
the timber corner is the coldest point, and it needs **0.80 m²K/W**: 20 mm of foam reaches 0.754,
9 mm reaches 0.693.

So the row reads **−0.80 as drawn and −0.39 with a 6 mm pad**, and the 1D answer was 0.44 short
of the requirement rather than 0.05 over it. This is the row where a one-sided bound was not
merely conservative but **wrong in sign**, and it is why the margin is now stated in the currency
of the 2D requirement.

It also shows that the currency itself is incomplete. Wrapping the steel outside the insulation
meets the criterion with **no added resistance at all** — f_Rsi 0.921, identical to the bare
timber corner — so what the detailer chooses is a **position**, not only a thickness. A margin
expressed in m²K/W cannot express that, and row 13 is the only row in this table with that
property.

**Row 14 is new, and it is the only row in this table that is a safety margin.** §13-1(1) asks
for documented alternative air quantities, and [the ventilation screen](verificacion-ventilacion.md)
produces them — but also shows what they cost. A mechanical extract in a sealed 36.9 m³ cabin
does not move air; it lowers the pressure until the envelope's leakage supplies the difference.
At the airtightness §14-3 requires, the fitted extract holds the cabin at **106–140 Pa** of
negative pressure, and a chimney's natural draught is **10–20 Pa**. The flue therefore reverses,
by **−130 Pa** at the highest pressure the fan can actually hold.

That is a carbon-monoxide margin, not an energy one, and it is negative for a reason no
insulation choice touches: the make-up air path. It is also the reason this row cannot be read
alone — the make-up air has to enter somewhere, and every entry point is a hole in the barrier
that row 13's moisture strategy depends on. **Rows 13 and 14 are the same drawing.**

---

## 7. What follows

1. **§2-2(3) cannot be satisfied by writing a number down.** The demand is for margins that are
   *necessary* — that is, evidence the design has not been driven to the limit. Six negative,
   two zero by construction and three undefined entries are the opposite of that evidence, and
   [the adequacy screen](verificacion-incertidumbre.md) shows that **not one row clears the
   declaration's own test** of being positive and larger than its uncertainty.
2. **R2 stops being a preference and becomes a regulatory requirement.** The binding dimension
   has no margin because every R2 option was solved **to** 4000 mm. Choosing an option that
   deliberately gives some back — a shallower pitch, a lower stack, or a dispensation — is what
   produces a positive margin on the governing quantity. That choice is Carlos's.
3. **The escape-window deficit closes for the price of a hole.** V-02's sill drops 100 mm at no
   cost in glass; V-03 goes from 500 × 500 to 900 × 600 for 0.29 m², and that same change
   relieves the daylight row by 0.06 of LT. Two negative rows and one undefined row move
   together, which is the only place in this table where one decision fixes three.
4. **"Undefined" must survive into the next revision.** Rows 1, 9 and 12 are undefined because
   a product, a fraction and a mass are missing. Filling them with plausible values would make
   this document look complete and be worthless.
5. **One margin statement per analysis, reissued when the geometry moves.** This document is
   versioned with the geometry, like the FDV file, and for the same reason.

---

## 8. Is any margin adequate? The answer is none

§1 defines a margin as adequate only when it is positive **and larger than the uncertainty of the
model that produced it**. [The adequacy screen](verificacion-incertidumbre.md) populates that
column and runs the test. It separates four kinds of uncertainty — model, input, interpretation
and construction — because only the second can be reduced by gathering data.

**No row clears the test.** Eight fail it outright; the other five cannot be judged, because
two of them have their sign set outside the model and three have no number at all:

| Row | Declared | Why it is not adequate |
|---|---|---|
| 2 — door free width | +40 mm | **not demonstrated.** 40 mm is the leaf minus a frame and hinge build-up nobody has specified; ordinary door sets spend 30–60 mm on it, so the sign is unknown |
| 3, 4 — escape windows | −500 mm | **sign set by the interpretation**: −500 under the strictest reading, +100 on V-01 under the minimal one |
| 5 — room height | −422 mm | **negative across the whole band** (−358 to −498), so the sign is robust — but the published figure is mid-band, not the worst case |
| 7 — wall U | 0 by construction | the thickness was **solved** to hit 0.22, so the margin is zero by definition; the band across 8–23 % runs +0.024 to −0.027 |
| 8 — thermal bridges | −0.160 | **negative at every detailing level** (−0.067 to −0.347), but the magnitude moves by a factor of three. One junction is now calculated and brackets the generic 0.10 the sweep assumed |
| 10 — R2 transport | 0 | **zero by construction** — every option was solved *to* 4000 mm |
| 11 — drain cover | −160 mm | **sign set by the site**, not by the model |
| 13 — condensation | −0.80 | **the sign was inverted by 2D.** The 1D requirement of 0.358 was computed on a surface that stops governing at the first millimetre of pad; the corner needs 0.80 |
| 6 — flood freeboard | +300 mm | positive, but the number is a **project choice**, not a requirement, so there is nothing to be adequate *to* |
| 1, 9, 12 | undefined | a product, a limit and a mass are missing. No sweep substitutes for them |

Three findings follow that this document did not previously carry.

**The thinnest positive margin is not a margin.** Row 2's +40 mm is a nominal leaf size, not a
free width. It is the only positive row that is not a project choice, and it rests on a
dimension no drawing gives.

**Two rows are zero by construction, and only one was admitted.** The transport envelope was
flagged; the wall U was not. Both are dimensions **solved to their limit**, which means the
margin is zero because of how the design was produced, not because the design happens to land
there. That is one failure mode, and it should be named once.

**The section's −422 mm is mid-band.** Every value from 8 % to 23 % timber fraction is negative,
so the timber fraction cannot rescue the section — it is a lever on the *size* of the deficit,
not on its sign. But the R2 report's sensitivity table runs down to 8 % and never up, so −422 mm
is the 15 % value being quoted where a worst case belongs. At 23 % the deficit is **−498 mm**.

## 9. Limits

- No margin here is a measurement. Every "available" value is a screening value from the report
  named in the source list.
- **Construction tolerance is absent from every row.** It is the fourth kind of uncertainty and
  no detail or specification exists to carry it. The adequacy screen records the absence rather
  than filling it.
- Rows 3 and 4 assume the R0 aperture table and the **strictest** reading of §11-13. Under the
  minimal reading — the door to grade is a safe place — they would be positive on V-01 alone.
  The declaration states the strictest because that is the reading the design will be built to,
  and a margin measured against a reading the building does not meet is not a margin.
- Row 5 uses the reference case (20°, 1100 mm stack, 281 mm floor, 278 mm roof) from the
  integrated section solver; other cases move it, and the solver's own table should be read for
  any other combination. The 250 / 300 mm build-ups it was first solved with give −415 mm, which
  is the number this document carried until the envelope solver replaced the round figures.
- Row 7's older figures, 0.267 and 0.209, belong to the **150 mm default** thickness and are
  kept in the envelope report as the diagnostic that shows the stud penalty is what breaks the
  wall. They are not the design's margin and this table no longer presents them as one.
- Row 13's requirement is the **2D** one, from a steel *plate* of 10 mm in a section that is not
  a chassis member. The profile does not exist (C-07), so the plate is a place-holder that makes
  the *difference* between detailing choices meaningful while leaving the absolute value
  unconfirmed. The 3D corner, the joists and the vapour field are all outside that model.
- **One quantity has a large margin and cannot be declared.** The maximum travel distance inside
  the cabin is **5.04 m**, and the loosest figure anywhere in the retrieved §11-14 text is 15 m,
  which would be a margin of +10 m. But §11-14's figures are for the distance from the *door of
  the fire cell* to the nearest stair or exit, and the §11-13 Table 1 row for risk class 4 was
  never retrieved. The applicable limit is therefore **unknown**, which makes this entry
  undefined rather than positive — and it is the only undefined entry in this document that a
  document could close. See [the chapter 11 determination](determinacion-estrategia-incendio.md).
- Nothing here is a compliance statement, a design release or a lift authorisation.

---

*Sources: [daylight](verificacion-luz-diurna.md), [fire](verificacion-incendio.md),
[room height](verificacion-altura-libre.md), [natural hazards](cribado-riesgos-naturales.md),
[envelope](verificacion-envolvente.md), [thermal bridges](verificacion-puentes-termicas.md),
[condensation at the junction](verificacion-condensacion-union.md), [the 2D
junction](verificacion-puente-2d.md), [ventilation](verificacion-ventilacion.md),
[integrated section](verificacion-seccion.md), [R2 options](opciones-seccion-R2.md),
[installations](verificacion-instalaciones.md),
[lift geometry](../knowledge/comparisons/lift-geometry-screen.md). Gate:
[S029](../knowledge/sources/S029.md).*
