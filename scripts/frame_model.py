#!/usr/bin/env python3
"""MiniHouse · printable 6 × 3 m frame model, scaled to fit an A1 mini.

CONCEPTUAL — NOT FOR FABRICATION.

This is the FRAME, not a joint coupon. The four numbered perimeter members are
woven 1 under 2, 2 under 3, 3 under 4, 4 under 1 — a closed cycle, so one member
must flex during assembly. Each member is a U-channel: a flat base with two
upstanding fins, and the aluminium/insulation sandwich wall sits between them,
as in the folded-paper model. Four crossmembers at 1200 mm centres complete the
base layout.

Plan dimensions are 1:40 (6000 × 3000 mm -> 150 × 75 mm). The section is
exaggerated and NOT to scale: a 2 mm printed base and 7 mm fins make the channel
printable. Fastener holes are schematic; the real M6 lap is tested separately in
bolted_lap_prototype.py. No steel section, bolt class or EXC is selected here.

Usage:
  python frame_model.py --selftest
  python frame_model.py --out-dir fase1/prototipo/marco-R0 \
      --out-md fase1/modelo-marco-R0.md \
      --out-json knowledge/comparisons/frame-model.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bolted_lap_prototype import (  # noqa: E402
    Shell, StepWriter, circle, extrude_region, write_3mf, write_stl,
)

STATUS = "CONCEPTUAL — NOT FOR FABRICATION"
SCOPE = "frame layout and channel geometry only"
NO_CLAIM = "no strength claim"
BED = 180.0
SCALE = 40.0
L = 6000.0 / SCALE      # 150 mm
B = 3000.0 / SCALE      # 75 mm
W = 8.0                 # exaggerated channel width
BASE_T = 2.0
LOW, HIGH = 0.0, BASE_T
FIN_H = 7.0
FIN_T = 1.2
FIN_END = 8.0
MID_W = 1.0
HOLE_R = 1.0
CROSS_W = 4.0
CROSS_X = (30.0, 60.0, 90.0, 120.0)
WALL_REF_T = 1.0
BOLT_R = 0.8
NEEDLES = (STATUS, SCOPE, NO_CLAIM, "1:40", "not to scale",
           "sandwich wall", "EN 1993-1-8", "thermal bridge")

# (level at u=0, level at u=length): 1 under 2, 2 under 3, 3 under 4, 4 under 1.
LEVELS = {1: (HIGH, LOW), 2: (HIGH, LOW), 3: (LOW, HIGH), 4: (LOW, HIGH)}
PRECEDENCE = {1: 2, 2: 3, 3: 4, 4: 1}


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def member(ply):
    """Local u runs along the member; v runs across its 8 mm channel."""
    if ply in (1, 3):
        x0 = 0.0 if ply == 1 else B - W
        return {"len": B, "mp": lambda u, v: (x0 + v, u), "vertical": True,
                "holes": (4.0, B - 4.0), "levels": LEVELS[ply]}
    y0 = B - W if ply == 2 else 0.0
    return {"len": L, "mp": lambda u, v: (u, y0 + v), "vertical": False,
            "holes": (4.0, L - 4.0), "levels": LEVELS[ply]}


def build_member(ply):
    m = member(ply)
    mp, length = m["mp"], m["len"]
    mid = length / 2.0
    lo, hi = m["levels"]
    shells = []

    for idx, (u0, u1, lvl, hole_u) in enumerate((
            (0.0, mid, lo, m["holes"][0]), (mid, length, hi, m["holes"][1])), 1):
        outer = [mp(u0, 0.0), mp(u1, 0.0), mp(u1, W), mp(u0, W)]
        hole = [mp(hole_u + dx, W / 2.0 + dy) for dx, dy in circle(0.0, 0.0, HOLE_R)]
        shells.append(extrude_region(f"ply{ply}_base{idx}", outer, hole, lvl, lvl + BASE_T))

        for side, (v0, v1) in enumerate(((0.0, FIN_T), (W - FIN_T, W)), 1):
            fa, fb = FIN_END, u1 if idx == 1 else length - FIN_END
            fa = FIN_END if idx == 1 else mid
            fb = mid if idx == 1 else length - FIN_END
            fin = [mp(fa, v0), mp(fb, v0), mp(fb, v1), mp(fa, v1)]
            shells.append(extrude_region(f"ply{ply}_fin{idx}_{side}", fin, None,
                                         lvl + BASE_T, lvl + BASE_T + FIN_H))

    web = [mp(mid - MID_W, 0.0), mp(mid + MID_W, 0.0),
           mp(mid + MID_W, W), mp(mid - MID_W, W)]
    shells.append(extrude_region(f"ply{ply}_dogleg", web, None,
                                 min(lo, hi), max(lo, hi) + BASE_T))
    for side, (v0, v1) in enumerate(((0.0, FIN_T), (W - FIN_T, W)), 1):
        fw = [mp(mid - MID_W, v0), mp(mid + MID_W, v0),
              mp(mid + MID_W, v1), mp(mid - MID_W, v1)]
        shells.append(extrude_region(f"ply{ply}_finweb{side}", fw, None,
                                     min(lo, hi) + BASE_T, max(lo, hi) + BASE_T + FIN_H))
    return shells


def build_crossmembers():
    out = []
    for x in CROSS_X:
        out.append(extrude_region(f"cross_{x:.0f}", rect(x, W, x + CROSS_W, B - W),
                                  None, LOW, LOW + BASE_T))
    return out


def wall_references():
    """Reference solids only — these show where the sandwich walls sit."""
    out = []
    out.append(extrude_region("wall_left", rect(FIN_T, FIN_END, W - FIN_T, B - FIN_END),
                              None, BASE_T, BASE_T + WALL_REF_T))
    out.append(extrude_region("wall_right",
                              rect(B - W + FIN_T, FIN_END, B - FIN_T, B - FIN_END),
                              None, BASE_T, BASE_T + WALL_REF_T))
    out.append(extrude_region("wall_top",
                              rect(FIN_END, B - W + FIN_T, L - FIN_END, B - FIN_T),
                              None, HIGH + BASE_T, HIGH + BASE_T + WALL_REF_T))
    out.append(extrude_region("wall_bottom", rect(FIN_END, FIN_T, L - FIN_END, W - FIN_T),
                              None, LOW + BASE_T, LOW + BASE_T + WALL_REF_T))
    return out


def bolt_references():
    out = []
    for x, y in ((4.0, 4.0), (4.0, B - 4.0), (L - 4.0, B - 4.0), (L - 4.0, 4.0)):
        out.append(extrude_region(f"bolt_ref_{x:.0f}_{y:.0f}",
                                  circle(x, y, BOLT_R), None, -1.0, 5.0))
    return out


def geometry():
    plies = {i: build_member(i) for i in range(1, 5)}
    cross = build_crossmembers()
    printed = [s for i in range(1, 5) for s in plies[i]] + cross
    bs = [s.bbox() for s in printed]
    box = [(min(b[i][0] for b in bs), max(b[i][1] for b in bs)) for i in range(3)]
    return {"plies": plies, "cross": cross, "printed": printed,
            "walls": wall_references(), "bolts": bolt_references(), "box": box,
            "size": tuple(round(b[1] - b[0], 3) for b in box),
            "margins": tuple(round(BED - (b[1] - b[0]), 3) for b in box)}


def vertical_order():
    indeg = {i: 0 for i in range(1, 5)}
    succ = {}
    for a, b in PRECEDENCE.items():
        succ[a] = succ.get(a, []) + [b]
        indeg[b] += 1
    ready = [i for i in indeg if indeg[i] == 0]
    out = []
    while ready:
        n = ready.pop(0)
        out.append(n)
        for m in succ.get(n, []):
            indeg[m] -= 1
            if indeg[m] == 0:
                ready.append(m)
    return out if len(out) == 4 else None


def record():
    g = geometry()
    return {
        "status": STATUS, "scope": SCOPE, "scale_plan": f"1:{SCALE:.0f}",
        "real_mm": [6000.0, 3000.0], "model_mm": [L, B], "bed_mm": [BED, BED, BED],
        "size_mm": list(g["size"]), "bed_margins_mm": list(g["margins"]),
        "section_note": "plan 1:40; base 2 mm and fins 7 mm exaggerated, not to scale",
        "channel": {"width_mm": W, "fin_height_mm": FIN_H, "fin_thickness_mm": FIN_T,
                    "clear_slot_mm": round(W - 2 * FIN_T, 2)},
        "crossmembers": {"count": len(CROSS_X), "centres_mm": list(CROSS_X),
                         "real_centres_mm": [x * SCALE for x in CROSS_X]},
        "weave": {"precedence": PRECEDENCE, "vertical_order": vertical_order(),
                  "note": "closed cycle; one member must flex during assembly"},
        "counts": {"printed_shells": len(g["printed"]),
                   "wall_reference_solids": len(g["walls"]),
                   "bolt_reference_solids": len(g["bolts"])},
        "holes": {"diameter_mm": round(2 * HOLE_R, 2),
                  "note": "schematic at frame scale; use the M6 joint coupon for the real detail"},
        "needs": NEEDLES,
    }


def table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def markdown(rec):
    L_ = [
        "# MiniHouse frame — printable layout model, R0",
        "",
        f"**{STATUS}. {SCOPE}. {NO_CLAIM}.**",
        "",
        "## 1. What this is",
        "",
        "This is the **6 × 3 m base frame**, not a lap coupon. The four perimeter members are "
        "numbered as in the sketch: **1** left, **2** top, **3** right, **4** bottom. "
        "They pass over and under one another at the corners — 1 under 2, 2 under 3, "
        "3 under 4, 4 under 1 — so the precedence is a closed cycle and no rigid assembly "
        "order exists. Each member is a U-channel: a flat base with two upstanding fins, "
        "and the aluminium/insulation **sandwich wall** sits between the fins, as in the "
        "folded-paper model. Four crossmembers at 1200 mm centres complete the base.",
        "",
        "## 2. Scale, declared",
        "",
        "Plan dimensions are **1:40**: 6000 × 3000 mm becomes **150 × 75 mm**, fitting an "
        "A1 mini bed of 180 mm with 15 mm and 52.5 mm margins per axis. The **section is "
        "not to scale** — a 2 mm base and 7 mm fins are used so the channel can be printed. "
        "The frame-scale holes are schematic; the real M6 lap is tested separately in "
        "`bolted_lap_prototype.py`.",
        "",
    ]
    L_ += table(["Item", "Model", "Real / basis"], [
        ["Footprint", "150 × 75 mm", "6000 × 3000 mm at 1:40"],
        ["Channel base", f"{W:.1f} mm wide, {BASE_T:.1f} mm thick", "exaggerated, not to scale"],
        ["Fins", f"{FIN_H:.1f} mm high, {FIN_T:.1f} mm thick", "sandwich wall between them"],
        ["Clear slot", f"{W - 2 * FIN_T:.1f} mm", "wall locating channel"],
        ["Crossmembers", f"{len(CROSS_X)} at {', '.join(f'{x:.0f}' for x in CROSS_X)} mm",
         "1200 mm centres in the real frame"],
        ["Bed margins", ", ".join(f"{m:.1f}" for m in rec["bed_margins_mm"]) + " mm", "A1 mini"],
    ])
    L_ += [
        "",
        "## 3. Assembly",
        "",
        "The four-member precedence is **1 → 2 → 3 → 4 → 1**: a topological sort returns "
        f"`{rec['weave']['vertical_order']}`. Lay 1, place 2 over it, place 3 over 2, then "
        "flex 4 under 1 and over 3. The U-fins stop short of the corners so the weave stays "
        "visible and does not collide. Tightening order and torque are not specified.",
        "",
        "## 4. Files and boundaries",
        "",
        "- `fase1/prototipo/marco-R0/ply1.stl` … `ply4.stl` — printed frame members.",
        "- `fase1/prototipo/marco-R0/crossmembers.stl` — the four crossmembers.",
        "- `fase1/prototipo/marco-R0/frame_3mf.3mf` — five print objects.",
        "- `fase1/prototipo/marco-R0/frame.step` — frame plus reference walls and bolts; "
        "Fusion import **not verified here**.",
        "",
        f"{STATUS}. The model proves the layout, the channel and the assembly sequence only. "
        f"{NO_CLAIM}: nothing here sizes steel, bolts or welds. No steel grade, bolt class, "
        "weld, plate thickness or EXC is selected. EN 1993-1-8 joints remain PENDING and "
        "NS-EN 1090-2 is paywalled. The sandwich wall is only a reference solid — its "
        "build-up is C-02 and remains open. A woven base re-opens the steel thermal bridge; "
        "the earlier wrapped-steel Ψ +0.027 is not inherited. Only the responsible engineer "
        "may mark anything \"Approved for Fabrication\" (rules.md §5).",
        "",
    ]
    return "\n".join(L_)


def selftest():
    rec = record()
    g = geometry()
    assert rec["weave"]["vertical_order"] is None
    assert rec["real_mm"] == [6000.0, 3000.0]
    assert rec["model_mm"] == [150.0, 75.0]
    assert max(g["size"]) <= BED and min(g["margins"]) >= 10.0
    assert rec["channel"]["clear_slot_mm"] == 5.6
    assert len(g["cross"]) == 4 and [x * SCALE for x in CROSS_X] == [1200.0, 2400.0, 3600.0, 4800.0]
    assert all(s.watertight() for s in g["printed"])
    assert all(s.watertight() for s in g["walls"] + g["bolts"])
    for ply in range(1, 5):
        for sh in g["plies"][ply]:
            if "_base" not in sh.name:
                continue
            ztop = max(p[2] for p in sh.verts)
            area = 0.0
            for a, b, c in sh.tris:
                pa, pb, pc = (sh.verts[i] for i in (a, b, c))
                if all(abs(p[2] - ztop) < 1e-6 for p in (pa, pb, pc)):
                    area += abs((pb[0] - pa[0]) * (pc[1] - pa[1])
                                - (pb[1] - pa[1]) * (pc[0] - pa[0])) / 2.0
            bb = sh.bbox()
            expected = ((bb[0][1] - bb[0][0]) * (bb[1][1] - bb[1][0])
                        - 3.141592653589793 * HOLE_R ** 2)
            assert abs(area - expected) < 0.1, (sh.name, area, expected)
    txt = markdown(rec)
    for needle in NEEDLES:
        assert needle in txt, needle
    import tempfile
    import zipfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        assert write_stl(td / "p.stl", g["plies"][1]) > 0
        assert write_3mf(td / "a.3mf", {**{i: g["plies"][i] for i in range(1, 5)},
                                        5: g["cross"]}) == 5
        with zipfile.ZipFile(td / "a.3mf") as z:
            assert "3D/3dmodel.model" in z.namelist()
        step = td / "a.step"
        solids = StepWriter().write(step, g["printed"] + g["walls"] + g["bolts"])
        assert solids == step.read_text(encoding="utf-8").count("MANIFOLD_SOLID_BREP(")
    print(f"Frame self-test OK: {g['size']} mm from 6000×3000 at 1:40, "
          f"{len(g['printed'])} printed shells, closed weave cycle, "
          f"{rec['channel']['clear_slot_mm']:.1f} mm wall slot.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out-dir", default="fase1/prototipo/marco-R0")
    ap.add_argument("--out-md", default="fase1/modelo-marco-R0.md")
    ap.add_argument("--out-json", default="knowledge/comparisons/frame-model.json")
    a = ap.parse_args()
    if a.selftest:
        return 0 if selftest() else 1
    rec, g = record(), geometry()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        write_stl(out / f"ply{i}.stl", g["plies"][i])
    write_stl(out / "crossmembers.stl", g["cross"])
    write_3mf(out / "frame_3mf.3mf", {**{i: g["plies"][i] for i in range(1, 5)}, 5: g["cross"]})
    rec["step_solids"] = StepWriter().write(out / "frame.step",
                                            g["printed"] + g["walls"] + g["bolts"])
    Path(a.out_md).write_text(markdown(rec), encoding="utf-8")
    Path(a.out_json).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
    print(f"Wrote scaled frame: {a.out_dir}, {a.out_md}, {a.out_json}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
