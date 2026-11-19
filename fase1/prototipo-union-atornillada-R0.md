# Woven bolted base joint — printable test article, R0

**CONCEPTUAL — NOT FOR FABRICATION. assembly sequence and tool access only. no strength claim.**

## 1. What the sketches show, and what they do not

The hand sketch numbers four members 1–4 and alternates them over and under at the corners, with bolts at the laps; the folded-paper model demonstrates the thread. No dimension on either image is reliable, so none is used as project data. The project still has no defined steel section: `fase2/miembros-R0.csv` is `PROV` and `fase2/miembros-R1-opciones.md` is `PROFILE_NOT_SELECTED`. This article is a joint-region mock-up, not a frame, not a section choice and not a release.

## 2. The thing that changes the design

A closed four-bar weave has **no rigid assembly order**. Each bar is under one neighbour and over the next, so the precedence graph is the cycle 1 → 2 → 3 → 4 → 1. A topological sort returns `None`, not an order. Paper works because paper bends; PETG at 2.0 mm can too. Ply **4** is the marked flexible strip and is threaded last. The print tests exactly whether that move is possible and whether the bolts then lock it.

## 3. Geometry (mixed scale, declared)

The layout is 1:2 of a nominal 100 mm flat bar. The thickness is deliberately thinner so the strip can thread, and the fasteners are full size because printed threads below M6 are unreliable.

| Item | Value | Basis |
|---|---|---|
| Print envelope | 180 × 180 × 180 mm | Bambu A1 mini (verified) |
| Article size | 150.0 × 150.0 × 9.5 mm | computed bounding box of printed shells |
| Bar | 50 × 150 × 2.0 mm | 1:2 layout, flexural thickness |
| Bolt / hole | M6 / Ø6.4 mm | clearance 0.4 mm |
| Nut seat | Ø10.2 mm (hex approximated circular) | 0.2 mm clearance |
| Wrench keep-out | Ø24 × 18 mm | tool access, not a printed part |
| Panel slot | 34 mm | locating gap only — not a scaled sandwich wall |

## 4. Assembly sequence

1. Lay ply 1 flat. 2. Place ply 2 over it at (30,30). 3. Place ply 3 over ply 2 at (30,120). 4. Bow and thread ply 4 from the open side: **under** ply 1 at (120,30), **over** ply 3 at (120,120). 5. Insert four M6 bolts from above, washers and free nuts below; tighten centre-outward as a handling convention only. Disassembly is the exact reverse.

Captive nuts are not modelled; the test deliberately uses two-sided nut access, because wrench clearance is one of the things being measured.

## 5. Numeric proofs and what to measure

| Crossing | Lap | Nearest other ply | Spare over Ø24 wrench |
|---|---|---|---|
| (30, 30) | 1/2 | 65.0 mm | 53.0 mm |
| (120, 30) | 4/1 | 65.0 mm | 53.0 mm |
| (30, 120) | 2/3 | 65.0 mm | 53.0 mm |
| (120, 120) | 3/4 | 65.0 mm | 53.0 mm |

Hole edge margin 5.0 mm; ligament 21.8 mm; minimum wrench spare 53.0 mm; bed margins 30, 30, 170 mm.

Measure on the printed part: actual hole diameter at each lap; inter-ply gap; assembled stack height; minimum wrench swing; number of assembly steps; three assembly/disassembly cycles without member fracture.

## 6. Files

- `scripts/bolted_lap_prototype.py` — generator and self-test.
- `fase1/prototipo/ply1.stl` … `ply4.stl` — four print bodies; PETG, 0.4 mm nozzle.
- `fase1/prototipo/joint_3mf.3mf` — multi-object print file.
- `fase1/prototipo/joint.step` — STEP with four plies and reference bolts; OCCT STEP export; Fusion import verified on 2706.1.17 Do not call it a validated CAD part.
- `knowledge/comparisons/bolted-lap-prototype.json` — the same numbers, machine readable.

## 7. Boundaries

This print validates assembly sequence and tool access only. It says nothing about steel or bolt capacity, preload, galvanic corrosion, thermal bridge, condensation in a Norwegian climate or regulatory compliance. No steel grade, bolt class, weld, plate thickness or EXC is selected. S355 remains rejected web copy. The EN 1993-1-8 joints row is **PENDING** and NS-EN 1090-2 is paywalled. Changing the base to a woven flat bar re-opens the insulated-junction detail (previously Ψ +0.027 with wrapped steel); it does not solve it. Only the responsible engineer may mark anything "Approved for Fabrication" (rules.md §5).

Sources: Bambu Lab Wiki build volumes (18 May 2026); RepRap FFF Design Guide; Steel Construction Info on preloaded bolting; All3DP PETG vs PLA (19 Dec 2024).
