# MiniHouse · escape windows (§11-13) against daylight (§13-7)

**State:** SCREENING — CONDITIONAL ON C-01. Not a fire strategy, not a daylight simulation, not a compliance certificate.

- Aperture table: `fase1/tabla-aberturas.csv` (R0 conceptual, unchanged by this screen).
- §11-13 from S024; §13-7 simplified dwelling route from S023.
- Escape-window and qualifying-glass definitions are imported from `fire_check.py` and `daylight_check.py`, so the three screens share one definition each.

## 1. What §11-13 requires, and the sentence that is easy to misread

§11-13(1) asks for **one exit to a safe place**, or exits to two independent escape routes, or one exit to an escape route with two directions. §11-13(4) then allows the exit from a fire cell to lead to a **single-direction** escape route, «forutsatt at hver branncelle har **vinduer** som er utformet og tilrettelagt for sikker rømning».

The dimensions table in S024 also carries the line **«one accessible escape window is sufficient in a dwelling unit»**. That sentence sits under *fire-service access*, and it is about the window the fire service can reach under §11-17 — it is **not** a relaxation of «vinduer» in §11-13(4). Reading it as one would make the current table pass. It should not be read that way.

So the requirement attaches to the **fire cell**, and whether the cabin's single door to grade already satisfies §11-13(1) decides whether §11-13(4) is engaged at all. That is a determination, not a calculation. What this screen can do is price each answer.

## 2. The room model

| Room | x range mm | Direct exit | Openings |
|---|---|---|---|
| bathroom | 0–1200 | **no** | V-03 |
| main room | 1200–6000 | yes — P-01 | V-01, V-02 |

The bathroom has **no direct exit** and one opening, V-03, which does not qualify. That is the structural fact the three readings disagree about.

## 3. The current table

| ID | Room | Size mm | Sill mm | h+w mm | Qualifies | Fails | Qualifying glass m² |
|---|---|---|---:|---:|---|---|---:|
| V-01 | main room | 1200 × 1100 | 900 | 2300 | yes | — | 1.320 |
| V-02 | main room | 1000 × 900 | 1100 | 1900 | **no** | sill | 0.900 |
| V-03 | bathroom | 500 × 500 | 1500 | 1000 | **no** | height, sum, sill | 0.250 |

**1 qualifying escape window** (V-01). V-02 fails **only** on the sill — 100 mm too high. V-03 fails on three counts.

## 4. The three readings, priced

| Reading | What it requires | Changes needed | Added glass m² | Resulting qualifying windows |
|---|---|---|---:|---|
| **R-A** minimal | the door to grade is a safe place; (4) not engaged | none | 0.00 | 1 (V-01) |
| **R-B** fire cell | the cell needs «vinduer», plural | V-02 1000 × 900 @ sill 1100 → 1000 × 900 @ sill 1000 | 0.00 | 2 (V-01, V-02) |
| **R-C** room by room | the bathroom has no direct exit | V-03 500 × 500 @ sill 1500 → 500 × 1000 @ sill 1000 | 0.25 | 2 (V-01, V-03) |

Reading by reading:

### R-A — minimal

§11-13(1) needs one exit to a safe place, and the door discharges to grade. §11-13(4) relaxes the two-direction rule; if the exit already reaches a safe place, (4) is not engaged.

- No change to the aperture table.
- Weakness: the safe place is a site condition, not a property of the module. A transportable cabin cannot carry its escape strategy in its siting.

### R-B — fire cell

§11-13(4) engaged: «hver branncelle har vinduer» — the cell needs at least two qualifying windows.

- **V-02** (main room): 1000 × 900 @ sill 1100 → 1000 × 900 @ sill 1000, +0.00 m² gross, +0.00 m² qualifying.
- Weakness: turns on whether the plural in «vinduer» binds for a one-room cell.

### R-C — room by room

every room without a direct exit needs its own qualifying window; here that is the bathroom, whose only opening is V-03.

- **V-03** (bathroom): 500 × 500 @ sill 1500 → 500 × 1000 @ sill 1000, +0.25 m² gross, +0.25 m² qualifying.
- Weakness: not stated in §11-13 as retrieved; it is guidance practice.

## 5. The set that satisfies all three

Designing to the strictest reading means the interpretation stops mattering — the municipality's answer to C-01 cannot then break the design. The union of R-A, R-B and R-C is:

| ID | Room | Now | Proposed | Added glass m² |
|---|---|---|---|---:|
| V-02 | MAIN | 1000 × 900 @ sill 1100 | **1000 × 900 @ sill 1000** | +0.00 |
| V-03 | BATH | 500 × 500 @ sill 1500 | **900 × 600 @ sill 1000** | +0.29 |
| | | | **Total** | **+0.29** |

That yields **3 qualifying windows** (V-01, V-02, V-03) — not three openings on one wall, which would be a weaker claim: V-01 and V-02 sit on opposite façades, 3000 mm apart.

### Why 900 mm and not the literal minimum

The area of a qualifying aperture has **two equal minima** on the sum-rule line: 600 × 900 and 900 × 600, both **0.54 m²**. Between them it bulges to 0.5625 m² at the 45° point (750 × 750), so a square window is the *worst* choice in that band. The absolute minimum is a 500 × 1000 slot at **0.50 m²**.

So the 500 mm slot saves 0.04 m² of glass and 0.008 of LT, and costs the one thing that matters here: a 500 mm aperture is a slot to climb through sideways. **900 × 600 is the widest aperture at the equal-minimum area**, and it is a standard Norwegian module. Take it.

### The bathroom window has a placement problem

V-03 sits on the y=0 wall, and the bathroom's back wall is only **1200 mm** long. At 900 mm wide the piers are 150 mm each side — too thin for a weathertight corner return and for the frame fixings.

The bathroom's **gable wall at x=0 is 3000 mm** and takes a 900 × 600 opening comfortably. Moving V-03 there costs nothing in daylight — the §13-7 count is orientation-blind — and it is the difference between a window that satisfies the letter and one a person can actually leave through.

## 6. Daylight before and after

| Set | Qualifying glass m² | Min LT, ff 1.00 | ff 0.90 | ff 0.85 | ff 0.80 |
|---|---:|---:|---:|---:|---:|
| Current | 2.47 | 0.510 | 0.567 | 0.600 | 0.638 |
| Literal minimum (500 mm slot) | 2.72 | 0.463 | 0.515 | 0.545 | 0.579 |
| Recommended (900 mm) | 2.76 | 0.457 | 0.507 | 0.537 | 0.571 |

The two bathroom-window options differ by 0.04 m² of glass, which is 0.008 of LT. **The wall geometry decides, not the daylight.**

### Where the two requirements actually converge

| Frame factor | Min LT now | Min LT after the escape fix | Relief |
|---:|---:|---:|---:|
| 1.00 | 0.510 | 0.457 | −0.054 |
| 0.90 | 0.567 | 0.507 | −0.060 |
| 0.85 | 0.600 | 0.537 | −0.063 |
| 0.80 | 0.638 | 0.571 | −0.067 |

The escape fix is **also** the daylight fix. At a frame factor of 0.85 the current table needs a light transmittance of **0.600**; after the fix it needs **0.537**. The same change relieves the daylight screen by 0.06 of LT at no extra cost, and it is the only lever that does so without adding a fourth opening.

Whether either figure is achievable is a **product question** — no glazing is specified yet — so this screen does not claim the daylight requirement is met. It claims the requirement is now 0.06 lower than it was.

## 7. What the fix costs in heat

| Item | Value |
|---|---:|
| Added glass | 0.29 m² |
| U window − U wall at the §14-3 limits | 0.98 W/m²K |
| Element loss from the added glass | +0.284 W/K |
| Added opening perimeter | +1.00 m |
| Reveal bridges at Ψ 0.05 W/mK (ordinary) | +0.050 W/K |
| **Total marginal heat loss** | **+0.334 W/K** |
| Share of the element loss (19.4 W/K) | 1.7 % |

The two effects **add**, they do not cancel: the glass displaces wall, which saves heat, but it also lengthens the opening perimeter, which costs heat at the reveal detail. The reveal is about a sixth of the glass figure, and both together are under two per cent of the envelope.

That is small enough not to move the R2 choice, and it is the second time the reveal has appeared as a real cost rather than a rounding term. The first was the 16.3 m reveal inventory in the bridge screen.

## 8. What this screen does not settle

1. **Which reading applies.** That is a municipal / fire-engineer determination. The screen prices the three so the question can be asked with numbers attached.
2. **Whether V-02 may drop its sill to 1000 mm.** It is the kitchen window; a 900 mm worktop plus a splashback normally puts the sill at about 1050 mm. The 100 mm drop is a joinery decision, not a free move.
3. **What sits under the bathroom window.** §11-13 allows a 1.0 m sill «unless measures ease escape»; a WC or a shower tray under the opening raises the effective sill. The sanitary layout is not drawn.
4. **The §11-13 Table 1 travel distance for risk class 4**, still absent from the retrieved table. Moot by geometry at 18 m².
5. **Whether the whole cabin is a rømningsvei** for §11-9 surface classes. That question is unchanged by this screen and still governs whether reclaimed timber may stay exposed.
6. **Whether the bathroom door gives 0.86 m free width.** A 1200 mm bathroom with a 900 mm leaf leaves 150 mm each side; not checked here.

## 9. Source and status

- TEK17 §11-13 and §11-14: S024. §13-7: S023.
- Plan and aperture geometry: `fase1/geometria-R0.md`, `fase1/tabla-aberturas.csv` (R0 conceptual).
- Generated by `scripts/ventanas_check.py`; JSON companion: `knowledge/comparisons/ventanas.json`.
- SCREENING ONLY — no fire strategy, no compliance certificate, no fabrication release.
