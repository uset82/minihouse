# MiniHouse frame — printable layout model, R0

**CONCEPTUAL — NOT FOR FABRICATION. frame layout and channel geometry only. no strength claim.**

## 1. What this is

This is the **6 × 3 m base frame**, not a lap coupon. The four perimeter members are numbered as in the sketch: **1** left, **2** top, **3** right, **4** bottom. They pass over and under one another at the corners — 1 under 2, 2 under 3, 3 under 4, 4 under 1 — so the precedence is a closed cycle and no rigid assembly order exists. Each member is a U-channel: a flat base with two upstanding fins, and the aluminium/insulation **sandwich wall** sits between the fins, as in the folded-paper model. Four crossmembers at 1200 mm centres complete the base.

## 2. Scale, declared

Plan dimensions are **1:40**: 6000 × 3000 mm becomes **150 × 75 mm**, fitting an A1 mini bed of 180 mm with margins [30.0, 105.0, 169.0] mm (x, y, z). The **section is not to scale** — a 2 mm base and 7 mm fins are used so the channel can be printed. The frame-scale holes are schematic; the real M6 lap is tested separately in `bolted_lap_prototype.py`.

| Item | Model | Real / basis |
|---|---|---|
| Footprint | 150 × 75 mm | 6000 × 3000 mm at 1:40 |
| Channel base | 8.0 mm wide, 2.0 mm thick | exaggerated, not to scale |
| Fins | 7.0 mm high, 1.2 mm thick | sandwich wall between them |
| Clear slot | 5.6 mm | wall locating channel |
| Crossmembers | 4 at 30, 60, 90, 120 mm | 1200 mm centres in the real frame |
| Bed margins | 30.0, 105.0, 169.0 mm | A1 mini |

## 3. Assembly

The four-member precedence is **1 → 2 → 3 → 4 → 1**: a topological sort returns `None`. Lay 1, place 2 over it, place 3 over 2, then flex 4 under 1 and over 3. The U-fins stop short of the corners so the weave stays visible and does not collide. Tightening order and torque are not specified.

## 4. Files and boundaries

- `fase1/prototipo/marco-R0/ply1.stl` … `ply4.stl` — printed frame members.
- `fase1/prototipo/marco-R0/crossmembers.stl` — the four crossmembers.
- `fase1/prototipo/marco-R0/frame_3mf.3mf` — five print objects.
- `fase1/prototipo/marco-R0/frame.step` — frame plus reference walls and bolts; OCCT STEP export; Fusion import verified on 2706.1.17.
- `fase1/prototipo/marco-R0/frame.f3d` — native Fusion archive exported after importing the STEP: 48 bodies, 150 × 75 mm. It is a viewing/handoff file, not a released design.

CONCEPTUAL — NOT FOR FABRICATION. The model proves the layout, the channel and the assembly sequence only. no strength claim: nothing here sizes steel, bolts or welds. No steel grade, bolt class, weld, plate thickness or EXC is selected. EN 1993-1-8 joints remain PENDING and NS-EN 1090-2 is paywalled. The sandwich wall is only a reference solid — its build-up is C-02 and remains open. A woven base re-opens the steel thermal bridge; the earlier wrapped-steel Ψ +0.027 is not inherited. Only the responsible engineer may mark anything "Approved for Fabrication" (rules.md §5).
