# Lift variant comparison framework · I-1 vs I-2

Status: framework established (Stage 3). No numeric forces yet — blocked on verified mass/CG (C-07) and crane (C-04).

## Definitions (from `fase1/condiciones-transporte-izaje.md`)

- **I-1** — lift at high corner nodes, z ≈ 3000 mm, four candidate legs.
- **I-2** — lift from base corners, z ≈ 0, four points, possible spreader.
- **I-3** — eccentric / two-point sensitivity case (engineer's decision).

## Evidence-informed starting positions

| Aspect | High lift (I-1) | Base lift (I-2) | Source |
|---|---|---|---|
| Structural logic | Load enters through upper frame; roof/purlins may need strengthening | Load enters at chassis directly — short load path | S007 §3 |
| Known risk | Bracket eccentricity bends/distorts connected thin elements below design load | Cable angle change over top corner can locally damage upper corner | S007, S008 §7.2 |
| Lift-point position | 20% inset from each end preferred for stability (1.2 m on 6 m); corners need lifting frame/cross-beams | Same inset logic may apply; confirm with model | S008 §7.2 |
| Equipment | Corner lift generally needs spreader frame or cross-beams | Straps under module or to ground-beam points; frame removal can be difficult on site | S007 §3, S008 |
| Spreader | Heavy frame equal to plan dimensions avoids horizontal/shear forces in the unit | Can verticalise legs; if purpose-made may fall under EN 13155 | S008, S000 |

## Comparison criteria (must be evaluated with the same masses)

1. Peak force per lift point, including dynamic factor and unequal-leg distribution (at least the 2-effective-leg pattern — S000, `fase1/condiciones-transporte-izaje.md`).
2. Horizontal component H on the stringers from sloping legs.
3. Change of diagonal in P-01 and V-01…V-03.
4. Differential torsion between the four corners.
5. Ear-to-profile eccentricity M_e = F·e.
6. Local tube/plate deformation at the lift point.
7. Inspection and test accessibility.
8. Need for, and mass of, a spreader; EN 13155 implications if purpose-built.
9. Site practicality — removal of rigging after setting down.
10. Robustness/failure-of-one-point behaviour.

## Test protocol to mirror (S007, McAvoy method)

- Specimen = full load path: ear/eye + plate/bracket + profile + connection (screws or weld), not an isolated plate.
- At least two bracket/detail variants and both eccentric and concentric load application.
- Displacement control, load to failure, record F–δ curve, peak load, initial stiffness, peak and ultimate displacement, failure mode and permanent deformation.
- Number of specimens and acceptance factors fixed **a priori** by the responsible engineer — no post-test safety factor.
- Report coefficient of variation: S007 saw CoV 10% on peak load but 45% on peak displacement — deformation is far more scattered than strength.

## Blockers

W and 3D CG verified; z_G; crane/radius (C-04); allowable wind; hook height; number of transport cycles (C-03).
