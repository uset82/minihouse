# MiniHouse · combined printable joint article (R0)

CONCEPTUAL — NOT FOR FABRICATION. assembly sequence, M6 fit, wrench access and fin/slot coexistence only. no strength claim.

## 1. What this is

One printed joint region combining the two earlier questions: four numbered members interlaced **1 → 2 → 3 → 4 → 1**, bolted at the laps, each formed as a U-channel with two fins and the sandwich wall between them. The closed cycle has no rigid assembly order. The **split lap** at the 4/1 corner opens it: ply 4 has an open hook there instead of a closed hole.

## 2. Scale, declared

hybrid mock-up: joint-region footprint at ~1:2, full-size M6 hardware, channel section exaggerated to print; neither a scaled frame nor a specified steel section.

Footprint **150.0 × 150.0 mm** in a 180 mm bed; margins [15.0, 15.0, 84.5] mm. M6 is real size; the channel is exaggerated. The clear slot is **47.6 mm** and is a locating gap, **not** the C-02 sandwich build-up, which remains open.

The STEP also carries 12 M6 reference bolts and 4 wall-strip references; its full bounding box is **150.0 × 150.0 × 34.0 mm**. Those references are exchange aids, not printed parts. The four printable shells alone are 150.0 × 150.0 × 11.0 mm.

## 3. Assembly and measurement

| Check | Value |
|---|---|
| Bolt / hole | M6 / Ø6.4 mm |
| Hole clearance | 0.4 mm |
| Nut seat | AF10.2 for AF10.0 (0.2 mm) |
| Ligament / edge margin | 21.8 / 15.0 mm |
| Wrench keep-out spare | 2.0 mm |
| Fin / slot | 7.0 mm high, 1.2 mm thick / 47.6 mm |

Fins stop before the bolt pads so the Ø24 wrench can reach every nut. The split lap is an open hook: the bolt passes through the gap and the crossing member's hole. Print four bodies, then measure hole and slot diameters, stacked thickness and wrench swing over three assembly cycles.

## 4. Files and boundaries

- `fase1/prototipo/union-combinada-R0/ply1.stl` … `ply4.stl` — four print bodies.
- `fase1/prototipo/union-combinada-R0/combined_joint_3mf.3mf` — multi-object print file.
- `fase1/prototipo/union-combinada-R0/combined_joint.step` — printed shells plus reference bolts and wall strips; OCCT STEP export; Fusion import verified on 2706.1.17.
- `fase1/prototipo/union-combinada-R0/MiniHouse_Combined_Joint_R0.f3d` — native Fusion archive.
- `fase1/prototipo/union-combinada-R0/fusion-screenshot.png` — viewport, only if the bridge was live.
- `knowledge/comparisons/combined-joint-prototype.json` — the same numbers, machine readable.

CONCEPTUAL — NOT FOR FABRICATION. Geometry defined, **not printed, not measured**. This tests only assembly, fit and access. No steel section, grade, bolt class, preload, weld, EXC, capacity, thermal-bridge resolution, code compliance or lift approval is claimed. EN 1993-1-8 joints remain PENDING, NS-EN 1090-2 is not held and the woven-base thermal bridge is **re-opened**. Only the responsible engineer may mark anything "Approved for Fabrication" (rules.md §5).
