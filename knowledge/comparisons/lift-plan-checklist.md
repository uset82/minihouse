# Lift plan checklist · MiniHouse (requirements, not an authorised plan)

Status: Stage 4. This is a **requirements and checklist document**. The real lift plan must be prepared, approved and executed by the competent lifting company under Norwegian work law (Arbeidstilsynet); this document does not authorise any manoeuvre.

## 1. Three distinct point types — must be drawn on one marked-up plan, with revision

- [ ] **Support points** — where the module rests when installed / on the trailer (C-05, C-06).
- [ ] **Lashing points** — EN 12195-1 securing, certified points, STF/LC of straps.
- [ ] **Lifting points** — I-1 high corners (z≈3000) or I-2 base corners (z≈0), with ear geometry and inspection access.

These three are never assumed coincident.

## 2. Verified inputs (all currently BLOCKED)

- [ ] W and full 3D CG (x_G, y_G, z_G) from the real inventory + four load-cell weighing (C-07).
- [ ] Configuration: tanks full/empty, batteries, removable items (C-07).
- [ ] Crane model, load chart, radius, hook height (C-04).
- [ ] Allowable wind for the manoeuvre.
- [ ] Route and vehicle (C-03, C-06) + vegliste check / VegSak dispensation (S009).
- [ ] Number of transport cycles → fatigue check under EN 1993-1-9 (C-03).

## 3. Rigging calculations (D003)

- [ ] T = V/sin α, H = V·cot α, α from horizontal — verified. Geometry-only screen for candidate corner/inset layouts and I-1/I-2: [lift-geometry-screen.md](lift-geometry-screen.md); no sling or variant selected.
- [ ] Leg-length tolerance and pre-tension considered.
- [ ] Unequal distribution: at minimum the **two-effective-leg** pattern (doubles V_leg) with a dynamic factor fixed by the specialist.
- [ ] Dynamic component as a multiple of self weight (S008 §7.2).
- [ ] Hook positioned over CG; module attitude checked with inclinometer during instrumented lift.
- [ ] Spreader evaluated: a full-plan-size frame avoids horizontal/shear forces in the unit (S008); a purpose-made accessory may fall under EN 13155:2020+A1:2025.

## 4. Structural acceptance

- [ ] Peak force per lift point (including eccentricity M_e = F·e) delivered by structural engineer.
- [ ] Four deformation limits fixed a priori: floor deflection, aperture diagonal change, corner differential torsion, local lift-point deformation (clause-map.md).
- [ ] Corner node qualified by full-path test to failure (D002, S007 method), with specimen count and acceptance factors set before testing.

## 5. Site and execution

- [ ] Rigging removal feasibility after setting down (S007: straps under module or ground-beam points can be difficult to remove).
- [ ] Base-lift upper-corner damage risk explicitly checked if I-2 is chosen (S008 §7.2).
- [ ] Exclusion zone, appointed lift supervisor, communication plan, stop-work criteria.
- [ ] Weather-tightness during transport (wind buffeting) — S008 §7.1.
- [ ] Pilot road test instrumentation: triaxial accelerometers on trailer and module, diagonals on one longitudinal wall, one transverse wall and roof/floor, before/after inspection of doors, windows, seals and cladding.

## 6. Authority

- [ ] Lift plan signed by the competent lifting company (Arbeidstilsynet rules).
- [ ] Structural calculations signed by the responsible engineer.
- [ ] Transport permits/dispensation confirmed with Statens vegvesen where required.

## 7. Source basis added 2026-11-16

- ESTA GD25001-EN (S017, `knowledge/refs/ESTA-GD25001-lifting-guideline.pdf`) §3.2: mass/CG, dimensions, lifting-point number/capacity/position and wind shape are required inputs to a lifting plan.
- ESTA §3.4.1: below-CG attachment is a critical lift; the projected sling stability triangle must contain the CG in all directions.
- ESTA §5.3: a full engineered lift plan has lifting, rigging and (dis)assembly arrangements with revision status and the stated load/rigging/wind/ground data.
- ESTA is industry guidance, not Norwegian law; the competent lifting company's approved plan and Norwegian work law remain controlling.

## Status

Requirements assembled; nothing here authorises a real lift. Blocked on C-01…C-09.
