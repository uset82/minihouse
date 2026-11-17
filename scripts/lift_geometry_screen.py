#!/usr/bin/env python3
"""MiniHouse · lift geometry screen (CONCEPTUAL — NOT A LIFT PLAN).

Computes sling geometry and normalized force ratios for candidate lift-point
layouts using the verified D003 relations:

    alpha = atan(vertical / plan_radius)
    T/V = 1 / sin(alpha)
    H/V = cot(alpha) = plan_radius / vertical

The hook is assumed directly above the CG. Forces are normalized to total
weight W; multiply by the real W only after C-07 mass/CG verification.
No WLL, dynamic factor, wind, crane chart or rigging design is selected.

A note on what mass does and does not change. Every ratio in this screen is
per unit W, so the *ranking* of layouts and verticals is **mass-independent**:
a heavier module does not make the corner layout better or worse, it only
makes every force larger in proportion. What mass adds is the conversion to
tonnes, and therefore whether a given accessory or crane can carry the result.
That is why C-07 blocks procurement, not the geometry choice. The example
masses in MASS_SCENARIOS_KG are for scaling only and are **not project data**.
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r1_gable_options import LENGTH_MM, WIDTH_MM, EAVE_Z_MM  # noqa: E402

VERTICALS_MM = (3000.0, 4000.0, 5000.0)
HOOK_CG_ASSUMPTION = "hook directly above centred CG"
G = 9.80665  # m/s2, for the kN view
# EXAMPLE masses for scaling only. C-07 is unanswered; nothing here is project data.
MASS_SCENARIOS_KG = (2000.0, 3000.0, 4000.0, 5000.0, 6000.0)
LAYOUTS = {
    "corner": {
        "description": "four extreme corners",
        "x_mm": (0.0, LENGTH_MM),
        "y_mm": (0.0, WIDTH_MM),
    },
    "inset20": {
        "description": "20% inset from each end along length, corners across width (SCI P272 starting point)",
        "x_mm": (0.2 * LENGTH_MM, 0.8 * LENGTH_MM),
        "y_mm": (0.0, WIDTH_MM),
    },
}
CASES = {
    "I-1": {
        "description": "high frame nodes at the eave datum",
        "lift_z_mm": EAVE_Z_MM,
        "esta_note": "attachments at/just below CG region; verify slope and corner damage",
    },
    "I-2": {
        "description": "base corners / chassis lift points",
        "lift_z_mm": 0.0,
        "esta_note": "below-CG lifting is a critical lift under ESTA §3.4.1; stability triangle must contain CG",
    },
}

NOTES = [
    "Normalized to total weight W: ideal four-leg sharing uses V_leg = W/4; two-effective-leg pattern uses V_leg = W/2 (D003).",
    "Four legs are statically indeterminate; perfect W/4 sharing is an idealization, not a design force.",
    "Plan radius uses a centred CG and hook directly above it; eccentric CG changes every leg force.",
    "Vertical means hook elevation minus lift-point elevation; it is a geometry scenario, not a crane selection.",
    "I-2 attaches below the CG and is an ESTA critical lift until the company proves otherwise.",
    "No sling WLL, dynamic factor, wind, leg-length tolerance, pre-tension or structural acceptance is defined here.",
]


def sling(alpha_deg: float) -> tuple:
    """Return (T/V, H/V) for alpha measured from horizontal."""
    a = math.radians(alpha_deg)
    return 1.0 / math.sin(a), 1.0 / math.tan(a)


def point_set(layout: dict) -> dict:
    xs, ys = layout["x_mm"], layout["y_mm"]
    cx, cy = LENGTH_MM / 2.0, WIDTH_MM / 2.0
    dx = max(abs(x - cx) for x in xs)
    dy = max(abs(y - cy) for y in ys)
    return {"dx_mm": round(dx, 1), "dy_mm": round(dy, 1),
            "plan_radius_mm": round(math.hypot(dx, dy), 1)}


def leg_force_tonnes(t_per_v: float, mass_kg: float, legs: int) -> float:
    """Per-leg force in tonnes for a total module mass and an effective leg count.

    legs = 4 is the ideal four-leg sharing; legs = 2 is the two-effective-leg
    pattern that governs accessory selection (D003). This is a static force:
    no dynamic factor, no unequal-leg factor, no wind.
    """
    return t_per_v * (mass_kg / 1000.0) / legs


def mass_view(rows: list, masses=MASS_SCENARIOS_KG) -> list:
    """Convert the dimensionless rows to tonnes at each example mass."""
    out = []
    for row in rows:
        for mass in masses:
            out.append({
                "case": row["case"],
                "layout": row["layout"],
                "vertical_mm": row["vertical_mm"],
                "mass_kg": mass,
                "T_leg_t_ideal_4leg": round(leg_force_tonnes(row["T_per_V"], mass, 4), 3),
                "T_leg_t_two_effective_legs": round(leg_force_tonnes(row["T_per_V"], mass, 2), 3),
                "H_leg_t_ideal_4leg": round(leg_force_tonnes(row["H_per_V"], mass, 4), 3),
            })
    return out


def screen() -> dict:
    rows = []
    for case_id, case in CASES.items():
        for layout_id, layout in LAYOUTS.items():
            pts = point_set(layout)
            r = pts["plan_radius_mm"]
            for vertical in VERTICALS_MM:
                alpha = math.degrees(math.atan2(vertical, r))
                t_per_v, h_per_v = sling(alpha)
                rows.append({
                    "case": case_id,
                    "case_description": case["description"],
                    "esta_note": case["esta_note"],
                    "layout": layout_id,
                    "layout_description": layout["description"],
                    "dx_mm": pts["dx_mm"],
                    "dy_mm": pts["dy_mm"],
                    "plan_radius_mm": r,
                    "vertical_mm": vertical,
                    "hook_z_mm": round(case["lift_z_mm"] + vertical, 1),
                    "alpha_from_horizontal_deg": round(alpha, 2),
                    "sling_length_mm": round(math.hypot(r, vertical), 1),
                    "T_per_V": round(t_per_v, 4),
                    "H_per_V": round(h_per_v, 4),
                    "T_per_W_ideal_4leg": round(t_per_v / 4.0, 4),
                    "T_per_W_two_effective_legs": round(t_per_v / 2.0, 4),
                    "H_per_W_ideal_4leg": round(h_per_v / 4.0, 4),
                    "H_per_W_two_effective_legs": round(h_per_v / 2.0, 4),
                })
    return {
        "revision": "LIFT-GEOMETRY-SCREEN",
        "state": "CONCEPTUAL — NOT FOR FABRICATION — NO LIFT VARIANT SELECTED",
        "units": "mm, degrees, dimensionless ratios per W",
        "assumption": HOOK_CG_ASSUMPTION,
        "basis": {
            "length_mm": LENGTH_MM,
            "width_mm": WIDTH_MM,
            "eave_z_mm_screening_datum": EAVE_Z_MM,
            "vertical_scenarios_mm": list(VERTICALS_MM),
            "formula": "alpha=atan(vertical/plan_radius); T/V=1/sin(alpha); H/V=cot(alpha)",
        },
        "point_sets": {
            key: {"description": value["description"], **point_set(value)}
            for key, value in LAYOUTS.items()
        },
        "rows": rows,
        "mass_view": mass_view(rows),
        "mass_view_note": (
            "Example masses for scaling only — NOT project data. Every ratio above is per "
            "unit W, so the layout ranking is mass-independent; mass only converts to tonnes."
        ),
        "notes": NOTES,
        "excluded": [
            "actual mass and CG", "dynamic factor", "sling WLL", "crane chart",
            "wind", "leg-length tolerance", "pre-tension", "structural acceptance",
        ],
    }


def markdown(model: dict) -> str:
    lines = [
        "# MiniHouse · lift geometry screen",
        "",
        "**State:** CONCEPTUAL — NOT A LIFT PLAN. **No lift variant or sling has been selected.** "
        "This is a geometry-and-ratio screen using the verified D003 relations.",
        "",
        "## Basis",
        "",
        f"- Footprint {LENGTH_MM/1000:.1f} × {WIDTH_MM/1000:.1f} m; eave screening datum {EAVE_Z_MM:.0f} mm.",
        f"- Assumption: {HOOK_CG_ASSUMPTION}. Eccentric CG is not modelled.",
        "- Vertical = hook elevation minus lift-point elevation: 3000 / 4000 / 5000 mm scenarios only.",
        "- D003: `T = V/sin(alpha)`, `H = V·cot(alpha)`, alpha from horizontal.",
        "",
        "## 1. Candidate point sets",
        "",
        "| Layout | Description | dx mm | dy mm | Plan radius mm |",
        "|---|---|---:|---:|---:|",
    ]
    for key, pts in model["point_sets"].items():
        lines.append(
            f"| {key} | {pts['description']} | {pts['dx_mm']:.0f} | {pts['dy_mm']:.0f} | "
            f"{pts['plan_radius_mm']:.1f} |"
        )

    lines += [
        "",
        "## 2. Normalized sling geometry",
        "",
        "Ratios are per unit total weight `W`. For the ideal four-leg case `V_leg = W/4`; "
        "for the two-effective-leg pattern `V_leg = W/2` (D003). These are not design forces.",
        "",
        "| Case | Layout | Vertical mm | Hook z mm | alpha ° | Sling mm | T/W ideal4 | T/W two-leg | H/W ideal4 | H/W two-leg |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in model["rows"]:
        lines.append(
            f"| {r['case']} | {r['layout']} | {r['vertical_mm']:.0f} | {r['hook_z_mm']:.0f} | "
            f"{r['alpha_from_horizontal_deg']:.1f} | {r['sling_length_mm']:.0f} | "
            f"{r['T_per_W_ideal_4leg']:.3f} | {r['T_per_W_two_effective_legs']:.3f} | "
            f"{r['H_per_W_ideal_4leg']:.3f} | {r['H_per_W_two_effective_legs']:.3f} |"
        )

    # --- mass conversion, deliberately narrow: two verticals, two layouts, I-1 only.
    worst, best = min(VERTICALS_MM), max(VERTICALS_MM)
    mv = model["mass_view"]

    def pick(layout, vertical, mass):
        for row in mv:
            if (row["case"] == "I-1" and row["layout"] == layout
                    and row["vertical_mm"] == vertical and row["mass_kg"] == mass):
                return row["T_leg_t_two_effective_legs"]
        raise KeyError((layout, vertical, mass))

    lines += [
        "",
        "## 3. What mass adds — and what it does not",
        "",
        "Every ratio above is per unit `W`, so the **ranking of layouts and verticals is "
        "mass-independent**: a heavier module does not make the corner layout better or "
        "worse, it scales every force in proportion. Mass therefore does not change the "
        "*choice*; it changes whether a given accessory or crane can carry the result. That "
        "is why C-07 blocks procurement rather than the geometry decision.",
        "",
        "Per-leg tension in **tonnes**, two-effective-leg pattern (the case that governs "
        "accessory selection, D003), case I-1:",
        "",
        "| Example mass kg | corner, "
        f"{worst:.0f} mm | corner, {best:.0f} mm | inset20, {worst:.0f} mm | "
        f"inset20, {best:.0f} mm |",
        "|---:|---:|---:|---:|---:|",
    ]
    for mass in MASS_SCENARIOS_KG:
        cells = [
            f"{pick('corner', worst, mass):.2f}",
            f"{pick('corner', best, mass):.2f}",
            f"{pick('inset20', worst, mass):.2f}",
            f"{pick('inset20', best, mass):.2f}",
        ]
        lines.append(f"| {mass:.0f} | " + " | ".join(cells) + " |")

    lines += [
        "",
        "**These masses are for scaling only. None of them is project data.** The useful "
        "reading is the spread rather than any single cell: at a fixed mass the difference "
        "between the worst and best geometry in that table is a factor of about "
        f"**{pick('corner', worst, MASS_SCENARIOS_KG[0]) / pick('inset20', best, MASS_SCENARIOS_KG[0]):.2f}**, "
        "which is what the layout and hook height are buying. A dynamic factor and the "
        "unequal-leg factor multiply all of it afterwards, and both belong to the crane "
        "company — they are not applied here.",
        "",
        "Rigging self-weight is **not** included: it adds to the hook load but not to the "
        "module, so it must be added before any crane capacity check.",
        "",
        "## 4. Interpretation",
        "",
        "- The `inset20` layout shortens the plan radius, so for the same vertical it gives a steeper sling, "
        "lower tension and lower horizontal thrust than the extreme-corner layout. This is a starting point "
        "from SCI P272, not a justification for this chassis.",
        "- At the same vertical, I-1 and I-2 have identical geometry ratios because vertical is measured from "
        "the lift point. The difference is structural: I-1 loads the upper frame; I-2 loads the chassis and "
        "is a below-CG critical lift under ESTA §3.4.1.",
        "- Hook height above the lift point is the governing geometric variable. A low hook makes alpha small "
        "and multiplies both tension and horizontal thrust; the crane company must set the real geometry.",
        "- Multiply `T/W` by the verified total weight only after C-07. Apply the specialist's dynamic factor "
        "and unequal-leg distribution before selecting any lifting accessory.",
        "",
        "## 5. Source and status",
        "",
        "- D003: sling geometry and four-leg indeterminacy (verified).",
        "- SCI P272 (S008): 20% inset lift-point starting point; full-plan spreader avoids horizontal/shear forces.",
        "- ESTA GD25001-EN (S017): below-CG lift = critical; projected sling triangle must contain CG.",
        "- Generated by `scripts/lift_geometry_screen.py`; JSON companion: "
        "`knowledge/comparisons/lift-geometry-screen.json`.",
        "- CONCEPTUAL — NOT FOR FABRICATION. No variant selected. No lift authorised.",
        "",
    ]
    return "\n".join(lines)


def selftest() -> None:
    # D003 reference at alpha = 60 degrees: T/V = 1.155, H/V = 0.577.
    tv, hv = sling(60.0)
    assert abs(tv - 1.1547) < 0.001 and abs(hv - 0.5774) < 0.001
    model = screen()
    assert len(model["rows"]) == len(CASES) * len(LAYOUTS) * len(VERTICALS_MM)
    for row in model["rows"]:
        assert 0.0 < row["alpha_from_horizontal_deg"] < 90.0
        assert row["T_per_V"] >= 1.0
        assert row["H_per_V"] > 0.0
        assert abs(row["T_per_W_two_effective_legs"] - 2 * row["T_per_W_ideal_4leg"]) <= 1e-4
        assert abs(row["H_per_W_two_effective_legs"] - 2 * row["H_per_W_ideal_4leg"]) <= 1e-4
        assert abs(row["sling_length_mm"] - math.hypot(row["plan_radius_mm"], row["vertical_mm"])) < 0.11
    # More vertical -> steeper, lower T and H; inset20 better than corners at same vertical.
    for case in CASES:
        for layout in LAYOUTS:
            seq = [r for r in model["rows"] if r["case"] == case and r["layout"] == layout]
            assert [r["T_per_V"] for r in seq] == sorted([r["T_per_V"] for r in seq], reverse=True)
            assert [r["H_per_V"] for r in seq] == sorted([r["H_per_V"] for r in seq], reverse=True)
        for vertical in VERTICALS_MM:
            corner = next(r for r in model["rows"] if r["case"] == case and r["layout"] == "corner"
                          and r["vertical_mm"] == vertical)
            inset = next(r for r in model["rows"] if r["case"] == case and r["layout"] == "inset20"
                         and r["vertical_mm"] == vertical)
            assert inset["H_per_V"] < corner["H_per_V"]
            assert inset["T_per_V"] < corner["T_per_V"]
    print("Lift geometry self-test OK: D003 reference, monotonic angles, inset and two-leg checks passed")


def selftest_mass() -> None:
    """The mass conversion must be linear, and must not disturb the ratios."""
    assert abs(leg_force_tonnes(1.0, 4000.0, 4) - 1.0) < 1e-12
    assert abs(leg_force_tonnes(2.0, 4000.0, 4) - 2.0) < 1e-12
    # Two effective legs carry exactly twice the four-leg ideal.
    for t in (1.0, 1.1547, 2.5):
        assert abs(leg_force_tonnes(t, 3000.0, 2) - 2 * leg_force_tonnes(t, 3000.0, 4)) < 1e-12
    # Linear in mass.
    for mass in MASS_SCENARIOS_KG:
        a = leg_force_tonnes(1.5, mass, 2)
        b = leg_force_tonnes(1.5, 2 * mass, 2)
        assert abs(b - 2 * a) < 1e-12
    model = screen()
    assert len(model["mass_view"]) == len(model["rows"]) * len(MASS_SCENARIOS_KG)
    # Mass must not reorder anything: for a fixed mass and case, the inset20 layout
    # still beats the corner layout at every vertical.
    for mass in MASS_SCENARIOS_KG:
        for vertical in VERTICALS_MM:
            corner = next(r for r in model["mass_view"] if r["case"] == "I-1"
                          and r["layout"] == "corner" and r["vertical_mm"] == vertical
                          and r["mass_kg"] == mass)
            inset = next(r for r in model["mass_view"] if r["case"] == "I-1"
                         and r["layout"] == "inset20" and r["vertical_mm"] == vertical
                         and r["mass_kg"] == mass)
            assert inset["T_leg_t_two_effective_legs"] < corner["T_leg_t_two_effective_legs"]
    print("Lift mass self-test OK: linear in mass, two-leg = 2x four-leg, ranking preserved")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON screen model")
    ap.add_argument("--out-md", help="write Markdown screening report")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        selftest_mass()
        return

    model = screen()
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {path}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(model), encoding="utf-8")
        print(f"wrote {path}")
    if not args.out_json and not args.out_md:
        print(json.dumps(model, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
