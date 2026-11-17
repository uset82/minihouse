#!/usr/bin/env python3
"""MiniHouse · R1 gable frame geometric skeleton (CONCEPTUAL — NO SECTIONS).

Emits node and member tables for all four R1 gable pitches. This is a
coordinate skeleton only: no profile, mass, connection, release, load,
resistance or fabrication claim. It simply makes the R1 roof geometry
available to CAD/IFC/structural workflows as an auditable member list.

Datum: same coordinate frame as R1 screening — x 0..6000 mm along the module,
y 0..3000 mm across, z=0 at the chassis top reference; eave z=3000 mm is a
screening datum inherited from R0, not a final wall height.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r1_gable_options import LENGTH_MM, WIDTH_MM, EAVE_Z_MM, PITCHES_DEG, option  # noqa: E402

X_FRAMES_MM = (0.0, 1200.0, 2400.0, 3600.0, 4800.0, 6000.0)
Y_SIDES_MM = (0.0, WIDTH_MM)
Y_RIDGE_MM = WIDTH_MM / 2.0
PROFILE = "PROFILE_NOT_SELECTED"
STATUS = "CONCEPTUAL — GEOMETRY ONLY — NOT FOR FABRICATION"

NOTES = [
    "Eave z=3000 mm is inherited from R0 as a screening datum, not a final wall specification.",
    "Ridge z = eave z + rise; rise = (B/2)·tan(pitch) from the verified R1 option model.",
    "All profiles are placeholders; no section, mass, material, connection or release is defined.",
    "This is a line skeleton, not a wall/roof build-up and not a structural model.",
    "No pitch is selected: all four options are emitted for sensitivity work only.",
]


def _nid(prefix, x, y=None):
    base = f"{prefix}{int(round(x)):04d}"
    return base if y is None else f"{base}Y{int(round(y)):04d}"


def build_option(pitch_deg: float) -> dict:
    opt = option(pitch_deg)
    rise = opt["rise_mm"]
    ridge_z = opt["ridge_z_mm"]

    nodes = []
    members = []

    def node(node_id, x, y, z, role):
        nodes.append({
            "node_id": node_id,
            "x_mm": round(x, 1),
            "y_mm": round(y, 1),
            "z_mm": round(z, 1),
            "role": role,
        })

    def member(member_id, role, ni, nj):
        a = next(n for n in nodes if n["node_id"] == ni)
        b = next(n for n in nodes if n["node_id"] == nj)
        length = math.dist(
            (a["x_mm"], a["y_mm"], a["z_mm"]),
            (b["x_mm"], b["y_mm"], b["z_mm"]),
        )
        members.append({
            "member_id": member_id,
            "role": role,
            "node_i": ni,
            "node_j": nj,
            "xi_mm": a["x_mm"], "yi_mm": a["y_mm"], "zi_mm": a["z_mm"],
            "xj_mm": b["x_mm"], "yj_mm": b["y_mm"], "zj_mm": b["z_mm"],
            "length_mm": round(length, 1),
            "profile": PROFILE,
            "status": STATUS,
        })

    # Nodes: chassis top datum, eaves, ridge, and centre tie at end frames.
    for x in X_FRAMES_MM:
        for y in Y_SIDES_MM:
            node(_nid("C", x, y), x, y, 0.0, "chassis_datum")
            node(_nid("E", x, y), x, y, EAVE_Z_MM, "eave")
        node(_nid("R", x), x, Y_RIDGE_MM, ridge_z, "ridge")
        if x in (X_FRAMES_MM[0], X_FRAMES_MM[-1]):
            node(_nid("T", x), x, Y_RIDGE_MM, EAVE_Z_MM, "end_tie")

    # Chassis datum skeleton: two longitudinal lines and six transverse lines.
    for y in Y_SIDES_MM:
        for k, (x1, x2) in enumerate(zip(X_FRAMES_MM[:-1], X_FRAMES_MM[1:]), 1):
            member(f"CH_LONG_Y{int(y)}_{k}", "chassis_longitudinal",
                   _nid("C", x1, y), _nid("C", x2, y))
    for x in X_FRAMES_MM:
        member(f"CH_CROSS_X{int(x)}", "chassis_cross",
               _nid("C", x, Y_SIDES_MM[0]), _nid("C", x, Y_SIDES_MM[1]))

    # Vertical posts at every frame line (wall-frame placeholders).
    for x in X_FRAMES_MM:
        for y in Y_SIDES_MM:
            member(f"POST_X{int(x)}_Y{int(y)}", "wall_post",
                   _nid("C", x, y), _nid("E", x, y))

    # Eave beams and ridge beam.
    for y in Y_SIDES_MM:
        for k, (x1, x2) in enumerate(zip(X_FRAMES_MM[:-1], X_FRAMES_MM[1:]), 1):
            member(f"EAVE_Y{int(y)}_{k}", "eave_beam",
                   _nid("E", x1, y), _nid("E", x2, y))
    for k, (x1, x2) in enumerate(zip(X_FRAMES_MM[:-1], X_FRAMES_MM[1:]), 1):
        member(f"RIDGE_{k}", "ridge_beam", _nid("R", x1), _nid("R", x2))

    # Rafters on every frame line.
    for x in X_FRAMES_MM:
        member(f"RAFTER_X{int(x)}_L", "rafter_left",
               _nid("E", x, Y_SIDES_MM[0]), _nid("R", x))
        member(f"RAFTER_X{int(x)}_R", "rafter_right",
               _nid("R", x), _nid("E", x, Y_SIDES_MM[1]))

    # End-frame tie and king post to close the gable triangle.
    for x in (X_FRAMES_MM[0], X_FRAMES_MM[-1]):
        member(f"TIE_X{int(x)}", "end_tie",
               _nid("E", x, Y_SIDES_MM[0]), _nid("E", x, Y_SIDES_MM[1]))
        member(f"KING_X{int(x)}", "king_post", _nid("T", x), _nid("R", x))

    return {
        "pitch_deg": pitch_deg,
        "rise_mm": round(rise, 1),
        "ridge_z_mm": ridge_z,
        "eave_z_mm": EAVE_Z_MM,
        "nodes": nodes,
        "members": members,
    }


def all_options():
    return {
        "revision": "R1-FRAME-SKELETON",
        "state": "CONCEPTUAL — GEOMETRY ONLY — NO PITCH SELECTED — NOT FOR FABRICATION",
        "units": "mm",
        "basis": {
            "length_mm": LENGTH_MM,
            "width_mm": WIDTH_MM,
            "eave_z_mm_screening_datum": EAVE_Z_MM,
            "x_frames_mm": list(X_FRAMES_MM),
            "y_sides_mm": list(Y_SIDES_MM),
            "ridge_y_mm": Y_RIDGE_MM,
        },
        "notes": NOTES,
        "options": [build_option(p) for p in PITCHES_DEG],
    }


def write_csv(model, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "pitch_deg", "member_id", "role", "node_i", "node_j",
        "xi_mm", "yi_mm", "zi_mm", "xj_mm", "yj_mm", "zj_mm",
        "length_mm", "profile", "status",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for opt in model["options"]:
            for m in opt["members"]:
                writer.writerow({"pitch_deg": opt["pitch_deg"], **m})


def markdown(model):
    lines = [
        "# MiniHouse · R1 geometric frame skeleton",
        "",
        "**State:** CONCEPTUAL — GEOMETRY ONLY. **No pitch selected. No section, mass or connection defined.**",
        "",
        "This is a coordinate skeleton for CAD/IFC/structural handoff, not a structural model.",
        "All members use the placeholder `PROFILE_NOT_SELECTED`.",
        "",
        "| Pitch deg | Rise mm | Ridge z mm | Nodes | Members | Rafter length mm |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for opt in model["options"]:
        rafter = next(m for m in opt["members"] if m["role"] == "rafter_left")
        lines.append(
            f"| {opt['pitch_deg']:.0f} | {opt['rise_mm']:.1f} | {opt['ridge_z_mm']:.1f} | "
            f"{len(opt['nodes'])} | {len(opt['members'])} | {rafter['length_mm']:.1f} |"
        )
    lines += [
        "",
        "## Member roles",
        "",
        "chassis_longitudinal, chassis_cross, wall_post, eave_beam, ridge_beam, "
        "rafter_left, rafter_right, end_tie, king_post.",
        "",
        "## Limits",
        "",
    ]
    lines += [f"- {note}" for note in NOTES]
    lines += [
        "- Generated by `scripts/r1_frame_skeleton.py`; CSV/JSON companions are the machine-readable outputs.",
        "- CONCEPTUAL — NOT FOR FABRICATION. No lift authorised.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    model = all_options()
    assert len(model["options"]) == len(PITCHES_DEG)
    ridges = []
    for opt in model["options"]:
        ridges.append(opt["ridge_z_mm"])
        assert len(opt["nodes"]) == 32
        assert len(opt["members"]) == 59
        node_ids = [n["node_id"] for n in opt["nodes"]]
        member_ids = [m["member_id"] for m in opt["members"]]
        assert len(set(node_ids)) == len(node_ids)
        assert len(set(member_ids)) == len(member_ids)
        ridge = next(n for n in opt["nodes"] if n["role"] == "ridge" and n["x_mm"] == 0.0)
        assert abs(ridge["y_mm"] - WIDTH_MM / 2.0) < 1e-9
        assert abs(ridge["z_mm"] - opt["ridge_z_mm"]) < 1e-9
        assert all(m["length_mm"] > 0 for m in opt["members"])
        assert all(m["profile"] == PROFILE for m in opt["members"])
        rafters = [m for m in opt["members"] if m["role"].startswith("rafter")]
        assert len(rafters) == 12
        expected = (WIDTH_MM / 2.0) / math.cos(math.radians(opt["pitch_deg"]))
        assert abs(rafters[0]["length_mm"] - expected) < 0.11
    assert ridges == sorted(ridges)
    print("R1 frame skeleton self-test OK: 4 options, 32 nodes/59 members each, ridge and rafter checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-csv", help="write combined member CSV")
    ap.add_argument("--out-json", help="write full node/member JSON model")
    ap.add_argument("--out-md", help="write summary Markdown")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    model = all_options()
    if args.out_csv:
        write_csv(model, Path(args.out_csv))
        print(f"wrote {args.out_csv}")
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(model), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not any((args.out_csv, args.out_json, args.out_md)):
        print(json.dumps(model, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
