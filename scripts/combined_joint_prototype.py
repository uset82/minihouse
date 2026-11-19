#!/usr/bin/env python3
"""MiniHouse · combined printable joint article (R0).

CONCEPTUAL — NOT FOR FABRICATION.

One mock-up that joins the two earlier questions: real M6 bolted laps AND the
two upstanding fins with the sandwich-wall locating gap. It is a hybrid mock-up:
joint-region footprint at ~1:2, full-size M6 hardware, channel section
exaggerated to print. It is neither a scaled frame nor a specified steel
section. Four numbered members interlace 1 under 2, 2 under 3, 3 under 4,
4 under 1. The split lap at the 4/1 corner opens that closed cycle.

Tests assembly sequence, hole/slot fit, wrench access and fin/slot coexistence.
It proves NOTHING about steel or bolt capacity, preload, corrosion, thermal
bridging, Norwegian code compliance, fabrication release or lifting.

Usage:
  python combined_joint_prototype.py --selftest
  python combined_joint_prototype.py
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bolted_lap_prototype import (  # noqa: E402
    Shell, circle, ear_clip, extrude_region, extrude_tris,
    write_3mf, write_stl,
)
import ocp_step  # noqa: E402

BED = 180.0
BAR_W = 50.0
BAR_L = 150.0
BAR_T = 2.0
SPLIT_U = 75.0
JOG = 2.0
JOG_HALF = 1.0
BOLT_D = 6.0
HOLE_D = 6.4
NUT_AF = 10.0
POCKET_AF = 10.2
BOSS_D = 20.0
BOSS_H = 5.5
WRENCH_D = 24.0
WRENCH_H = 18.0
FIN_T = 1.2
FIN_H = 7.0
CORNER_KEEP_OUT = WRENCH_D / 2.0 + 2.0
WALL_REF_T = 1.0
SEGMENTS = 24
CROSS_X = (30.0, 120.0)
CROSS_Y = (30.0, 120.0)

# Sketch numbering: 1 left/horizontal at y=30, 2 vertical at x=30,
# 3 horizontal at y=120, 4 vertical at x=120. (x, y, lower, upper).
CROSSINGS = (
    (30.0, 30.0, 1, 2),
    (30.0, 120.0, 2, 3),
    (120.0, 120.0, 3, 4),
    (120.0, 30.0, 4, 1),
)
SPLIT_PLY = 4
SPLIT_CROSSING = (120.0, 30.0)
LEVELS = {1: (0.0, JOG), 2: (JOG, 0.0), 3: (JOG, 0.0), 4: (0.0, JOG)}
THREAD_PLY = 4

STATUS = "CONCEPTUAL — NOT FOR FABRICATION"
SCOPE = "assembly sequence, M6 fit, wrench access and fin/slot coexistence only"
NO_CLAIM = "no strength claim"
NEEDLES = (STATUS, SCOPE, NO_CLAIM, "1 → 2 → 3 → 4 → 1", "M6", "47.6",
           "C-02", "EN 1993-1-8", "NS-EN 1090-2", "thermal bridge",
           "not printed", "not measured")


def ply_map(ply):
    """Local (u along bar, v across bar) -> global (x,y)."""
    if ply in (1, 3):
        center = CROSS_Y[0] if ply == 1 else CROSS_Y[1]
        return lambda u, v: (u, center + v)
    center = CROSS_X[0] if ply == 2 else CROSS_X[1]
    return lambda u, v: (center - v, u)


def u_of_crossing(ply, crossing):
    mp = ply_map(ply)
    x, y = crossing[0], crossing[1]
    # Invert the local map at v=0.
    if ply in (1, 3):
        return x
    return y


def precedence():
    return {lower: upper for _x, _y, lower, upper in CROSSINGS}


def vertical_order():
    """Kahn's algorithm: None means the closed weave has no rigid order."""
    edges = precedence()
    indeg = {i: 0 for i in range(1, 5)}
    succ = defaultdict(list)
    for a, b in edges.items():
        succ[a].append(b)
        indeg[b] += 1
    queue = [i for i in range(1, 5) if indeg[i] == 0]
    out = []
    while queue:
        node = queue.pop()
        out.append(node)
        for nxt in succ[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return out if len(out) == 4 else None


def cycle_nodes():
    nxt = precedence()
    start = 1
    out = [start]
    for _ in range(4):
        start = nxt[start]
        out.append(start)
    return out


def bbox(shells):
    boxes = [sh.bbox() for sh in shells if sh.bbox() is not None]
    return tuple((min(b[i][0] for b in boxes), max(b[i][1] for b in boxes))
                 for i in range(3))


def half_polygon(u0, u1, v0, v1, hole_u, notch=False):
    """Rectangle, optionally with an open split from the low-u edge to hole_u."""
    if not notch:
        return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    g = HOLE_D / 2.0
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1),
            (u0, g), (hole_u, g), (hole_u, -g), (u0, -g)]


def build_ply(ply):
    """One numbered member: two base halves, dogleg, fins, bosses (and split)."""
    mp = ply_map(ply)
    v0, v1 = -BAR_W / 2.0, BAR_W / 2.0
    lo, hi = LEVELS[ply]
    shells = []

    for idx, (u0, u1, lvl) in enumerate(((0.0, SPLIT_U, lo),
                                         (SPLIT_U, BAR_L, hi)), 1):
        hole_u = CROSS_X[0] if idx == 1 else CROSS_X[1]
        notch = (ply == SPLIT_PLY and idx == 1)
        outer = [mp(u, v) for u, v in half_polygon(u0, u1, v0, v1, hole_u, notch)]
        if notch:
            # Open split: a rectangular gap replaces the closed hole so the
            # hook can be slipped around the crossing member's bolt.
            shells.append(extrude_tris(f"ply{ply}_half{idx}",
                                       ear_clip(outer), lvl, lvl + BAR_T))
            continue
        ring = circle(hole_u, 0.0, HOLE_D / 2.0, ccw=True)
        hole = [mp(u, v) for u, v in ring]
        shells.append(extrude_region(f"ply{ply}_half{idx}", outer, hole,
                                     lvl, lvl + BAR_T))

    web_outer = [mp(SPLIT_U - JOG_HALF, v0), mp(SPLIT_U + JOG_HALF, v0),
                 mp(SPLIT_U + JOG_HALF, v1), mp(SPLIT_U - JOG_HALF, v1)]
    shells.append(extrude_region(f"ply{ply}_dogleg", web_outer, None,
                                 min(lo, hi), max(lo, hi) + BAR_T))

    # Two fins per half, interrupted at each bolt pad by CORNER_KEEP_OUT.
    for idx, (u0, u1, lvl) in enumerate(((0.0, SPLIT_U, lo),
                                         (SPLIT_U, BAR_L, hi)), 1):
        hole_u = CROSS_X[0] if idx == 1 else CROSS_X[1]
        spans = [(u0, max(u0, hole_u - CORNER_KEEP_OUT)),
                 (min(u1, hole_u + CORNER_KEEP_OUT), u1)]
        for side, (vlo, vhi) in enumerate(((v0, v0 + FIN_T), (v1 - FIN_T, v1)), 1):
            for seg, (a, b) in enumerate(spans, 1):
                if b - a <= FIN_T:
                    continue
                fin = [mp(a, vlo), mp(b, vlo), mp(b, vhi), mp(a, vhi)]
                shells.append(extrude_region(
                    f"ply{ply}_fin{idx}_{side}_{seg}", fin, None,
                    lvl + BAR_T, lvl + BAR_T + FIN_H))

    # Nut-seat bosses; the split corner is an open hook and has no printed boss.
    for n, u in enumerate(CROSS_X, 1):
        if ply == SPLIT_PLY and u == CROSS_X[0]:
            continue
        z0 = (lo if n == 1 else hi) + BAR_T
        outer = [mp(u + px, py) for px, py in circle(0.0, 0.0, BOSS_D / 2.0)]
        inner = [mp(u + px, py) for px, py in
                 circle(0.0, 0.0, POCKET_AF / 2.0, ccw=True)]
        shells.append(extrude_region(f"ply{ply}_boss{n}", outer, inner,
                                     z0, z0 + BOSS_H, outer_ring=outer))

    return shells


def reference_bolts():
    """Twelve reference M6 solids for STEP only — never printed."""
    shells = []
    z_bot, z_top = -10.0, 16.0
    for x, y, _a, _b in CROSSINGS:
        tag = f"bolt_{x:.0f}_{y:.0f}"
        shells.append(extrude_region(tag + "_shaft",
                                     circle(x, y, BOLT_D / 2.0), None,
                                     z_bot, z_top))
        shells.append(extrude_region(tag + "_head",
                                     circle(x, y, 5.0), None,
                                     z_top, z_top + 4.0))
        shells.append(extrude_region(tag + "_nut",
                                     circle(x, y, NUT_AF / 2.0), None,
                                     z_bot - 4.0, z_bot))
    return shells


def wall_references():
    """Four thin reference strips in the fin slot — not a sandwich build-up."""
    shells = []
    for ply in range(1, 5):
        mp = ply_map(ply)
        lo, hi = LEVELS[ply]
        outer = [mp(CROSS_X[0], -WALL_REF_T / 2.0),
                 mp(CROSS_X[1], -WALL_REF_T / 2.0),
                 mp(CROSS_X[1], WALL_REF_T / 2.0),
                 mp(CROSS_X[0], WALL_REF_T / 2.0)]
        shells.append(extrude_region(f"wall_ref_{ply}", outer, None,
                                     min(lo, hi) + BAR_T,
                                     max(lo, hi) + BAR_T + FIN_H))
    return shells


def geometry():
    plies = {i: build_ply(i) for i in range(1, 5)}
    printed = [sh for i in range(1, 5) for sh in plies[i]]
    walls = wall_references()
    bolts = reference_bolts()
    bb = bbox(printed)
    full_bb = bbox(printed + walls + bolts)
    size = tuple(round(b[1] - b[0], 3) for b in bb)
    full_size = tuple(round(b[1] - b[0], 3) for b in full_bb)
    margins = tuple(round((BED - s) / 2.0, 3) for s in size)
    return {"plies": plies, "printed": printed, "walls": walls,
            "bolts": bolts, "size": size, "full_size": full_size,
            "margins": margins, "bbox": bb}


def clearance():
    return {"hole_clearance_mm": round(HOLE_D - BOLT_D, 6),
            "nut_seat_clearance_mm": round(POCKET_AF - NUT_AF, 6),
            "ligament_mm": round((BAR_W - HOLE_D) / 2.0, 6),
            "edge_margin_mm": round((BAR_W - BOSS_D) / 2.0, 6),
            "min_wrench_spare_mm": round(CORNER_KEEP_OUT - WRENCH_D / 2.0, 6)}


def record(step_backend=None, step_solids=None):
    g = geometry()
    cl = clearance()
    return {
        "status": STATUS,
        "scope": SCOPE,
        "no_claim": NO_CLAIM,
        "printer": {"model": "Bambu A1 mini", "bed_mm": [BED, BED, BED]},
        "scale": {
            "layout": "joint region only, about 1:2 of a nominal 100 mm bar",
            "hardware": "M6 at real size",
            "section": "exaggerated to print, not to scale",
            "statement": ("hybrid mock-up: joint-region footprint at ~1:2, "
                          "full-size M6 hardware, channel section exaggerated "
                          "to print; neither a scaled frame nor a specified "
                          "steel section"),
        },
        "size_mm": list(g["size"]),
        "step_bbox_mm": list(g["full_size"]),
        "bed_margins_mm": list(g["margins"]),
        "hardware": {
            "bolt_d_mm": BOLT_D, "hole_d_mm": HOLE_D,
            "nut_af_mm": NUT_AF, "pocket_af_mm": POCKET_AF,
            "boss_d_mm": BOSS_D, "boss_h_mm": BOSS_H,
            "wrench_d_mm": WRENCH_D, "wrench_h_mm": WRENCH_H,
        },
        "channel": {
            "bar_width_mm": BAR_W, "fin_thickness_mm": FIN_T,
            "fin_height_mm": FIN_H, "clear_slot_mm": BAR_W - 2 * FIN_T,
            "wall_reference": "C-02 build-up OPEN; locating gap only",
        },
        "weave": {
            "cycle": cycle_nodes(),
            "vertical_order": vertical_order(),
            "threaded_ply": THREAD_PLY,
            "closure": "split lap",
            "split_ply": SPLIT_PLY,
            "split_crossing_mm": list(SPLIT_CROSSING),
            "corner_keep_out_mm": CORNER_KEEP_OUT,
        },
        "clearances": cl,
        "shells": {
            "printed": len(g["printed"]),
            "wall_references": len(g["walls"]),
            "bolt_references": len(g["bolts"]),
        },
        "step_solids": step_solids,
        "step_backend": step_backend or "not generated",
        "print_and_measurement": "not printed, not measured",
        "neighbors": ("EN 1993-1-8 PENDING; NS-EN 1090-2 not held; "
                      "thermal bridge re-opened; no weld, EXC or lift claim"),
    }


def markdown(rec):
    g = geometry()
    cl = rec["clearances"]
    L = [
        "# MiniHouse · combined printable joint article (R0)",
        "",
        STATUS + ". " + SCOPE + ". " + NO_CLAIM + ".",
        "",
        "## 1. What this is",
        "",
        "One printed joint region combining the two earlier questions: four numbered "
        "members interlaced **1 → 2 → 3 → 4 → 1**, bolted at the laps, each formed as a "
        "U-channel with two fins and the sandwich wall between them. The closed cycle "
        "has no rigid assembly order. The **split lap** at the 4/1 corner opens it: "
        "ply 4 has an open hook there instead of a closed hole.",
        "",
        "## 2. Scale, declared",
        "",
        rec["scale"]["statement"] + ".",
        "",
        f"Footprint **{rec['size_mm'][0]:.1f} × {rec['size_mm'][1]:.1f} mm** in a "
        f"{BED:.0f} mm bed; margins {rec['bed_margins_mm']} mm. M6 is real size; "
        f"the channel is exaggerated. The clear slot is **{rec['channel']['clear_slot_mm']:.1f} mm** "
        "and is a locating gap, **not** the C-02 sandwich build-up, which remains open.",
        "",
        f"The STEP also carries 12 M6 reference bolts and 4 wall-strip references; "
        f"its full bounding box is **{rec['step_bbox_mm'][0]:.1f} × "
        f"{rec['step_bbox_mm'][1]:.1f} × {rec['step_bbox_mm'][2]:.1f} mm**. "
        "Those references are exchange aids, not printed parts. The four printable "
        f"shells alone are {rec['size_mm'][0]:.1f} × {rec['size_mm'][1]:.1f} × "
        f"{rec['size_mm'][2]:.1f} mm.",
        "",
        "## 3. Assembly and measurement",
        "",
        f"| Check | Value |", f"|---|---|",
        f"| Bolt / hole | M6 / Ø{rec['hardware']['hole_d_mm']:.1f} mm |",
        f"| Hole clearance | {cl['hole_clearance_mm']:.1f} mm |",
        f"| Nut seat | AF{rec['hardware']['pocket_af_mm']:.1f} for AF{rec['hardware']['nut_af_mm']:.1f} "
        f"({cl['nut_seat_clearance_mm']:.1f} mm) |",
        f"| Ligament / edge margin | {cl['ligament_mm']:.1f} / {cl['edge_margin_mm']:.1f} mm |",
        f"| Wrench keep-out spare | {cl['min_wrench_spare_mm']:.1f} mm |",
        f"| Fin / slot | {rec['channel']['fin_height_mm']:.1f} mm high, "
        f"{rec['channel']['fin_thickness_mm']:.1f} mm thick / "
        f"{rec['channel']['clear_slot_mm']:.1f} mm |",
        "",
        "Fins stop before the bolt pads so the Ø24 wrench can reach every nut. "
        "The split lap is an open hook: the bolt passes through the gap and the "
        "crossing member's hole. Print four bodies, then measure hole and slot "
        "diameters, stacked thickness and wrench swing over three assembly cycles.",
        "",
        "## 4. Files and boundaries",
        "",
        "- `fase1/prototipo/union-combinada-R0/ply1.stl` … `ply4.stl` — four print bodies.",
        "- `fase1/prototipo/union-combinada-R0/combined_joint_3mf.3mf` — multi-object print file.",
        "- `fase1/prototipo/union-combinada-R0/combined_joint.step` — printed shells plus reference bolts "
        f"and wall strips; {rec['step_backend']}.",
        "- `fase1/prototipo/union-combinada-R0/MiniHouse_Combined_Joint_R0.f3d` — native Fusion archive.",
        f"- `fase1/prototipo/union-combinada-R0/fusion-screenshot.png` — viewport, only if the bridge was live.",
        f"- `knowledge/comparisons/combined-joint-prototype.json` — the same numbers, machine readable.",
        "",
        f"{STATUS}. Geometry defined, **not printed, not measured**. This tests only "
        "assembly, fit and access. No steel section, grade, bolt class, preload, weld, "
        "EXC, capacity, thermal-bridge resolution, code compliance or lift approval is "
        "claimed. EN 1993-1-8 joints remain PENDING, NS-EN 1090-2 is not held and the "
        "woven-base thermal bridge is **re-opened**. Only the responsible engineer may "
        "mark anything \"Approved for Fabrication\" (rules.md §5).",
        "",
    ]
    return "\n".join(L)


def selftest():
    rec = record()
    g = geometry()
    assert rec["weave"]["cycle"] == [1, 2, 3, 4, 1]
    assert rec["weave"]["vertical_order"] is None
    assert rec["weave"]["threaded_ply"] == 4
    assert rec["weave"]["closure"] == "split lap"
    assert rec["weave"]["split_ply"] == 4
    assert rec["weave"]["split_crossing_mm"] == [120.0, 30.0]
    cl = rec["clearances"]
    assert cl["hole_clearance_mm"] == 0.4
    assert cl["nut_seat_clearance_mm"] >= 0.2
    assert cl["ligament_mm"] == 21.8
    assert cl["min_wrench_spare_mm"] > 0
    assert abs(rec["channel"]["clear_slot_mm"] - 47.6) < 1e-9
    assert rec["size_mm"] == [150.0, 150.0, 11.0]
    assert rec["step_bbox_mm"] == [150.0, 150.0, 34.0]
    assert max(g["size"]) <= BED and min(g["margins"]) >= 10
    assert len(g["plies"]) == 4
    assert len(g["walls"]) == 4 and len(g["bolts"]) == 12
    for sh in g["printed"] + g["walls"] + g["bolts"]:
        assert sh.watertight(), sh.name
        directed = Counter()
        for a, b, c in sh.oriented_triangles():
            for u, v in ((a, b), (b, c), (c, a)):
                directed[(u, v)] += 1
        assert all(n == 1 for n in directed.values()), sh.name
        assert all(directed.get((v, u)) == 1 for (u, v) in directed), sh.name
    fins = [sh for sh in g["printed"] if "_fin" in sh.name]
    assert len(fins) >= 16
    assert any("_half1" in sh.name for sh in g["plies"][4])
    txt = markdown(rec)
    for needle in NEEDLES:
        assert needle in txt, needle
    import tempfile
    import zipfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        assert write_stl(td / "p.stl", g["plies"][1]) > 0
        assert write_3mf(td / "a.3mf", g["plies"]) == 4
        with zipfile.ZipFile(td / "a.3mf") as z:
            assert "3D/3dmodel.model" in z.namelist()
        step = td / "a.step"
        shells = g["printed"] + g["walls"] + g["bolts"]
        if ocp_step.available():
            n = ocp_step.write_step(step, shells)
        else:
            from bolted_lap_prototype import StepWriter
            n = StepWriter().write(step, shells)
        body = step.read_text(encoding="utf-8")
        assert body.count("MANIFOLD_SOLID_BREP(") == n == len(shells)
        assert body.rstrip().endswith("END-ISO-10303-21;")
    print(f"Combined joint self-test OK: {g['size']} mm in {BED:.0f} mm bed, "
          f"{len(g['printed'])} printed shells, {len(g['bolts'])} reference bolts, "
          f"split lap at {SPLIT_CROSSING}, clearance {cl['min_wrench_spare_mm']:.1f} mm.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out-dir", default="fase1/prototipo/union-combinada-R0")
    ap.add_argument("--out-md", default="fase1/prototipo-combinado-R0.md")
    ap.add_argument("--out-json", default="knowledge/comparisons/combined-joint-prototype.json")
    ap.add_argument("--fusion-verified", action="store_true",
                    help="set only after a live Fusion import has been checked")
    a = ap.parse_args()
    if a.selftest:
        return 0 if selftest() else 1
    g = geometry()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        write_stl(out / f"ply{i}.stl", g["plies"][i])
    write_3mf(out / "combined_joint_3mf.3mf", g["plies"])
    shells = g["printed"] + g["walls"] + g["bolts"]
    if ocp_step.available():
        step_backend = ("OCCT STEP export; Fusion import verified on 2706.1.17"
                        if a.fusion_verified else
                        "OCCT STEP export; Fusion import pending live check")
        nsol = ocp_step.write_step(out / "combined_joint.step", shells)
    else:
        from bolted_lap_prototype import StepWriter
        step_backend = "stdlib STEP fallback; Fusion import NOT verified"
        nsol = StepWriter().write(out / "combined_joint.step", shells)
        print("WARNING: OCCT not installed; STEP may import as empty components in Fusion.")
    rec = record(step_backend, nsol)
    Path(a.out_md).write_text(markdown(rec), encoding="utf-8")
    Path(a.out_json).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
    print(f"Wrote combined joint: {a.out_dir}, {a.out_md}, {a.out_json} ({nsol} solids).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
