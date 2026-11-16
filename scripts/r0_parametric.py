#!/usr/bin/env python3
"""MiniHouse · Parametric R0 geometry definition (CONCEPTUAL — NOT FOR FABRICATION).

Single source of truth for the R0 reference geometry from fase1/geometria-R0.md.
Emits a JSON model that can be consumed by SolidCraft (via its CLI/bridge) or
any CAD/CAE script, plus a concise summary. Dimensions in mm; CG source frame
per geometria-R0.md: origin at chassis exterior corner, +x length, +y width,
+z up.

This is a geometry reference only: NO steel section, plate thickness, weld or
lifting ear is defined. Section choice is blocked on Fase 2 analysis.
"""
import argparse
import json

R0 = {
    "revision": "R0",
    "state": "CONCEPTUAL — NOT FOR FABRICATION",
    "units": "mm",
    "frame": {
        "origin": "exterior chassis corner, top face of floor stringer",
        "axes": "+x longitudinal 0..6000, +y transverse 0..3000, +z up",
    },
    "dimensions": {
        "length_mm": 6000,
        "width_mm": 3000,
        "height_total_mm": 3200,       # S-01
        "clear_height_mm": 2400,       # S-02
        "roof_rise_mm": 200,           # S-03, monopitch -> ~3.8 deg
        "roof_ridge_y_mm": 0,
        "max_salient_mm_per_side": 50, # S-06 -> transport width <= 3100
    },
    "chassis_axes": {
        "stringers_y_mm": [150, 2850],
        "cross_members_x_mm": [0, 1200, 2400, 3600, 4800, 6000],
        "section": "UNDEFINED — EI in report does not identify a profile",
    },
    "openings": [  # from fase1/tabla-aberturas.csv
        {"id": "P-01", "facade": "y=3000", "x_center": 4500, "sill_z": 0, "width": 900, "height": 2050},
        {"id": "V-01", "facade": "y=3000", "x_center": 2400, "sill_z": 900, "width": 1200, "height": 1100},
        {"id": "V-02", "facade": "y=0", "x_center": 2400, "sill_z": 1100, "width": 1000, "height": 900},
        {"id": "V-03", "facade": "y=0", "x_center": 600, "sill_z": 1500, "width": 500, "height": 500},
    ],
    "bathroom_zone": {"x_min": 0, "x_max": 1200},  # S-04
    "lift_candidates": {
        "high": {"z_mm": 3000, "x_mm": [0, 6000], "y_mm": [0, 3000],
                 "note": "corner nodes; SCI P272 suggests 20% inset (~1200) as more stable"},
        "low": {"z_mm": 0, "x_mm": [0, 6000], "y_mm": [0, 3000]},
        "status": "candidates only — decision from Fase 2 analysis",
    },
    "excluded": ["steel sections", "plate thicknesses", "welds", "lifting ears",
                 "anchors", "timber details", "services"],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", help="write JSON model to this path")
    a = p.parse_args()
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(R0, f, indent=2, ensure_ascii=False)
        print(f"wrote {a.out}")
    else:
        print(json.dumps(R0, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
