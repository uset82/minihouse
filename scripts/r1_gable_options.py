#!/usr/bin/env python3
"""MiniHouse · R1 gable-roof screening options (CONCEPTUAL — NOT FOR FABRICATION).

Creates geometric sensitivity options for the declared gable-roof intent.
It does NOT select a pitch and does NOT define structure, roof build-up,
overhangs, transport restraints or fabrication details.

Basis:
- R0 footprint and frame: fase1/geometria-R0.md / knowledge/comparisons/r0-model.json
- Declared intent: gable roof, ridge centred across the 3000 mm width (S016)
- ESTA GD25001-EN S017: projected wind area and 1.2 m2/t guidance threshold

Units: mm and m2. z=0 is the top face of the chassis reference frame.
"""
import argparse
import json
import math
from pathlib import Path

LENGTH_MM = 6000.0
WIDTH_MM = 3000.0
EAVE_Z_MM = 3000.0          # inherited from R0 low-edge wall height; NOT final
R0_HEIGHT_MM = 3200.0       # R0 total height, monopitch reference only
PITCHES_DEG = (5.0, 10.0, 15.0, 20.0)
DECK_SUPPORT_MM = (900.0, 1100.0, 1300.0)  # illustrative stack only, NOT project data
ESTA_WIND_RATIO_M2_PER_T = 1.2
NORMAL_HEIGHT_SCREENING_MM = 4000.0  # Statens vegvesen summary of Directive 96/53/EC, general height

NOTES = [
    "Gable roof intent is declared by Carlos's reference images (S016); pitch is NOT dimensioned.",
    "No pitch is selected here. R1 remains open until C-02 gives pitch/eave/ridge dimensions.",
    "Eave height 3000 mm is inherited from R0 as a screening datum only; it is not a wall spec.",
    "Roof area is geometric surface only: no build-up, overlap, waste, purlins or cladding mass.",
    "Loaded height = module ridge height + deck/support stack. Stack values are illustrative; carrier must confirm.",
    "4.00 m height screening comes from Statens vegvesen's summary of Directive 96/53/EC; national rules and route still control.",
    "ESTA wind area is a screening check using projected bounding areas; the crane company must set allowable wind.",
]


def option(pitch_deg: float) -> dict:
    p = math.radians(pitch_deg)
    half_width = WIDTH_MM / 2.0
    rise = half_width * math.tan(p)
    ridge_z = EAVE_Z_MM + rise
    slope_length = half_width / math.cos(p)

    roof_one_side_m2 = (LENGTH_MM / 1000.0) * (slope_length / 1000.0)
    roof_two_sides_m2 = 2.0 * roof_one_side_m2
    gable_one_end_m2 = 0.5 * (WIDTH_MM / 1000.0) * (rise / 1000.0)
    gable_two_ends_m2 = 2.0 * gable_one_end_m2

    # Conservative projected areas for ESTA screening.
    # Wind normal to long facade: length x (eave + one roof-slope projection).
    area_long_m2 = (LENGTH_MM / 1000.0) * ((EAVE_Z_MM + rise) / 1000.0)
    # Wind normal to gable end: width x eave wall + two triangular halves = width x (eave + rise/2).
    area_end_m2 = (WIDTH_MM / 1000.0) * ((EAVE_Z_MM + rise / 2.0) / 1000.0)
    area_max_m2 = max(area_long_m2, area_end_m2)
    min_mass_t = area_max_m2 / ESTA_WIND_RATIO_M2_PER_T

    return {
        "pitch_deg": pitch_deg,
        "rise_mm": round(rise, 1),
        "eave_z_mm": EAVE_Z_MM,
        "ridge_z_mm": round(ridge_z, 1),
        "delta_vs_R0_height_mm": round(ridge_z - R0_HEIGHT_MM, 1),
        "slope_length_mm": round(slope_length, 1),
        "roof_surface_one_slope_m2": round(roof_one_side_m2, 3),
        "roof_surface_two_slopes_m2": round(roof_two_sides_m2, 3),
        "gable_end_area_one_m2": round(gable_one_end_m2, 3),
        "gable_end_area_two_m2": round(gable_two_ends_m2, 3),
        "projected_wind_area_long_m2": round(area_long_m2, 3),
        "projected_wind_area_end_m2": round(area_end_m2, 3),
        "projected_wind_area_max_m2": round(area_max_m2, 3),
        "min_mass_for_1p2_m2_per_t_t": round(min_mass_t, 2),
        "max_deck_plus_support_for_4m_mm": round(NORMAL_HEIGHT_SCREENING_MM - ridge_z, 1),
        "loaded_height_examples_mm": [
            {
                "deck_plus_support_mm": stack,
                "loaded_height_mm": round(ridge_z + stack, 1),
                "status": "ILLUSTRATIVE — carrier to confirm",
            }
            for stack in DECK_SUPPORT_MM
        ],
    }


def build_model() -> dict:
    return {
        "revision": "R1-OPTIONS",
        "state": "CONCEPTUAL — NOT FOR FABRICATION — PITCH NOT SELECTED",
        "units": "mm, m2, tonnes",
        "basis": {
            "length_mm": LENGTH_MM,
            "width_mm": WIDTH_MM,
            "ridge_position": "centred at y=1500 mm",
            "eave_z_mm_screening_datum": EAVE_Z_MM,
            "R0_total_height_mm_reference": R0_HEIGHT_MM,
            "esta_wind_ratio_m2_per_t": ESTA_WIND_RATIO_M2_PER_T,
        },
        "options": [option(p) for p in PITCHES_DEG],
        "notes": NOTES,
        "excluded": [
            "steel sections", "roof build-up", "overhangs", "purlins", "cladding mass",
            "trailer deck specification", "legal height limit", "fabrication release",
        ],
    }


def markdown(model: dict) -> str:
    lines = [
        "# MiniHouse · R1 gable-roof screening options",
        "",
        "**State:** CONCEPTUAL — NOT FOR FABRICATION. **No pitch has been selected.** "
        "This is a sensitivity study for the declared gable-roof intent, not a design decision.",
        "",
        "## Basis",
        "",
        f"- Footprint: {LENGTH_MM/1000:.1f} × {WIDTH_MM/1000:.1f} m; ridge centred across the width, per S016.",
        f"- Screening eave datum: {EAVE_Z_MM:.0f} mm above chassis (inherited from R0 low-edge wall height, not final).",
        f"- R0 total height reference: {R0_HEIGHT_MM:.0f} mm with the superseded monopitch roof.",
        "- ESTA GD25001-EN (S017) is guidance, not Norwegian law; wind limits must be set by the crane company.",
        "",
        "## 1. Geometry sensitivity",
        "",
        "| Pitch | Rise mm | Ridge z mm | Δ vs R0 mm | Roof surface, 2 slopes m² | Gable ends, 2 m² | Slope length mm |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for o in model["options"]:
        lines.append(
            f"| {o['pitch_deg']:.0f}° | {o['rise_mm']:.1f} | {o['ridge_z_mm']:.1f} | "
            f"{o['delta_vs_R0_height_mm']:+.1f} | {o['roof_surface_two_slopes_m2']:.3f} | "
            f"{o['gable_end_area_two_m2']:.3f} | {o['slope_length_mm']:.1f} |"
        )

    lines += [
        "",
        "Formulae: `rise = (B/2)·tan(θ)`; `slope length = (B/2)/cos(θ)`; "
        "`roof surface = 2·L·slope length`; `two gable ends = B·rise`.",
        "",
        "## 2. Transport-height sensitivity",
        "",
        "Loaded height = ridge height + trailer deck + transport supports. "
        "The stack values below are illustrative only. The 4.00 m screening value comes from Statens vegvesen's "
        "summary of Directive 96/53/EC (general height); it is not a route-specific permit. Carrier and "
        "Statens vegvesen must confirm the applicable domestic rule and any dispensation.",
        "",
        "| Pitch | Ridge mm | Max stack to stay at 4.00 m | Loaded @900 mm | @1100 mm | @1300 mm |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for o in model["options"]:
        vals = [f"{v['loaded_height_mm']:.0f}" for v in o["loaded_height_examples_mm"]]
        lines.append(
            f"| {o['pitch_deg']:.0f}° | {o['ridge_z_mm']:.1f} | "
            f"{o['max_deck_plus_support_for_4m_mm']:.0f} | {vals[0]} | {vals[1]} | {vals[2]} |"
        )

    lines += [
        "",
        "## 3. ESTA wind-area screening",
        "",
        "Projected areas are conservative bounding areas. The minimum mass shown is the mass that would keep "
        "the ratio at or below ESTA's 1.2 m²/t guidance threshold; below it, the crane operating company must "
        "calculate a reduced permissible wind speed.",
        "",
        "| Pitch | Long-side area m² | Gable-end area m² | Max area m² | Min mass for 1.2 m²/t, t |",
        "|---:|---:|---:|---:|---:|",
    ]
    for o in model["options"]:
        lines.append(
            f"| {o['pitch_deg']:.0f}° | {o['projected_wind_area_long_m2']:.3f} | "
            f"{o['projected_wind_area_end_m2']:.3f} | {o['projected_wind_area_max_m2']:.3f} | "
            f"{o['min_mass_for_1p2_m2_per_t_t']:.2f} |"
        )

    lines += [
        "",
        "## 4. Interpretation",
        "",
        "- A steeper pitch raises the ridge and increases roof/gable area, transport height and wind exposure.",
        "- With the 3000 mm eave screening datum, all options exceed 4.00 m once a 900 mm stack is added. "
        "At 5° the stack must be at most about 869 mm to stay at 4.00 m; at 20° only about 454 mm. "
        "A lower eave datum, low-loader setup or special transport may be needed.",
        "- Even at 5°, the conservative projected area requires roughly 16 t to avoid the ESTA wind-speed caveat; "
        "the real MiniHouse mass is not yet known, so the lift plan must verify this before relying on crane-chart wind limits.",
        "- No recommendation is made here. The decision needs C-02 (pitch/eave/ridge), C-06 (deck/support) "
        "and confirmation from carrier and crane company.",
        "",
        "## 5. Source and status",
        "",
        "- Geometry basis: R0 frame and declared gable intent (S016).",
        "- Wind screening basis: ESTA GD25001-EN §3.2 and §3.4 wind guidance (S017).",
        "- Height screening basis: Statens vegvesen, Forenklet oversikt etter direktiv 96/53/EF, general height 4.00 m (S022).",
        "- Generated by `scripts/r1_gable_options.py`; JSON companion: "
        "`knowledge/comparisons/r1-gable-options.json`.",
        "- CONCEPTUAL — NOT FOR FABRICATION. No pitch selected. No lift authorised.",
        "",
    ]
    return "\n".join(lines)


def selftest() -> None:
    opts = [option(p) for p in PITCHES_DEG]
    assert all(o["rise_mm"] > 0 for o in opts)
    assert [o["rise_mm"] for o in opts] == sorted(o["rise_mm"] for o in opts)
    for o in opts:
        p = math.radians(o["pitch_deg"])
        expected_rise = (WIDTH_MM / 2.0) * math.tan(p)
        assert abs(o["rise_mm"] - expected_rise) < 0.05
        assert abs(o["ridge_z_mm"] - (EAVE_Z_MM + expected_rise)) < 0.05
        assert o["slope_length_mm"] > WIDTH_MM / 2.0
        assert o["roof_surface_two_slopes_m2"] > 2 * LENGTH_MM * WIDTH_MM / 2 / 1e6
        assert o["projected_wind_area_max_m2"] > 0
        assert o["min_mass_for_1p2_m2_per_t_t"] > 0
        assert o["max_deck_plus_support_for_4m_mm"] > 0
    assert len(opts[0]["loaded_height_examples_mm"]) == len(DECK_SUPPORT_MM)
    print("R1 self-test OK: 4 pitch options, monotonic rise, geometry and wind checks passed")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON options model")
    ap.add_argument("--out-md", help="write Markdown screening report")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    model = build_model()
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
