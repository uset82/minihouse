#!/usr/bin/env python3
"""MiniHouse · TEK17 §13-7 daylight screening (CONDITIONAL ON C-01).

Uses the simplified dwelling route from S023:

    Ag >= 0.07 * ABRA / LT

where Ag is qualifying glass area at least 0.8 m above the floor and not in a
light well. The script reads the current aperture table, excludes the door
(no documented glazing), and reports the minimum light transmittance needed
for several frame factors. It is a screening check, not a daylight simulation
and not a compliance certificate.

Usage:
  python daylight_check.py fase1/tabla-aberturas.csv --abra 18 \
      --out-md fase1/verificacion-luz-diurna.md \
      --out-json knowledge/comparisons/daylight-check.json
  python daylight_check.py --selftest
"""
import argparse
import csv
import json
import sys
from pathlib import Path

SILL_LIMIT_MM = 800.0
FRAME_FACTORS = (1.0, 0.90, 0.85, 0.80)
LT_SCENARIOS = (0.40, 0.50, 0.60, 0.70, 0.80)
COEFFICIENT = 0.07


def qualifying_area_m2(width_mm, height_mm, sill_mm):
    """Glass area at least 0.8 m above the floor; partial panes are prorated."""
    top = sill_mm + height_mm
    if top <= SILL_LIMIT_MM:
        return 0.0
    effective_height = top - max(sill_mm, SILL_LIMIT_MM)
    return width_mm * effective_height / 1e6


def read_openings(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    openings = []
    for row in rows:
        if not row["id"].strip().upper().startswith("V-"):
            continue
        try:
            width = float(row["ancho_mm"])
            height = float(row["alto_mm"])
            sill = float(row["z_antepecho_mm"])
        except (KeyError, ValueError) as exc:
            raise SystemExit(f"ERROR apertura {row.get('id', '?')}: {exc}")
        openings.append({
            "id": row["id"].strip(),
            "description": row["descripcion"].strip(),
            "sill_mm": sill,
            "width_mm": width,
            "height_mm": height,
            "gross_m2": round(width * height / 1e6, 3),
            "qualifying_m2": round(qualifying_area_m2(width, height, sill), 3),
        })
    if not openings:
        raise SystemExit("ERROR: no window rows (V-*) found")
    return openings


def evaluate(openings, abra_m2):
    gross = sum(o["gross_m2"] for o in openings)
    qualifying = sum(o["qualifying_m2"] for o in openings)
    if abra_m2 <= 0 or qualifying <= 0:
        raise SystemExit("ERROR: ABRA and qualifying glass area must be positive")
    scenarios = []
    for lt in LT_SCENARIOS:
        required = COEFFICIENT * abra_m2 / lt
        row = {"LT": lt, "required_m2": round(required, 3), "by_frame_factor": {}}
        for ff in FRAME_FACTORS:
            effective = qualifying * ff
            row["by_frame_factor"][f"{ff:.2f}"] = {
                "effective_m2": round(effective, 3),
                "pass": effective >= required,
            }
        scenarios.append(row)
    minimum_lt = {
        f"{ff:.2f}": round(COEFFICIENT * abra_m2 / (qualifying * ff), 4)
        for ff in FRAME_FACTORS
    }
    return {
        "gross_m2": round(gross, 3),
        "qualifying_m2": round(qualifying, 3),
        "abra_m2": abra_m2,
        "scenarios": scenarios,
        "minimum_lt": minimum_lt,
    }


def markdown(openings, result, source_path):
    lines = [
        "# MiniHouse · TEK17 §13-7 daylight screening",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a daylight simulation and not a compliance certificate.",
        "",
        f"- Aperture table: `{source_path}`",
        f"- Heated floor area used: **{result['abra_m2']:.1f} m²** (R0 assumption; final BRA pending C-02).",
        "- Simplified dwelling route from S023: `Ag >= 0.07·ABRA/LT`.",
        "- Only windows `V-*` are counted; the door is excluded because its glazing is not documented.",
        "- Qualifying glass is at least 0.8 m above the floor; partial panes are prorated.",
        "",
        "## 1. Window areas",
        "",
        "| ID | Description | Sill mm | Width × height mm | Gross m² | Qualifying m² |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for o in openings:
        lines.append(
            f"| {o['id']} | {o['description']} | {o['sill_mm']:.0f} | "
            f"{o['width_mm']:.0f} × {o['height_mm']:.0f} | {o['gross_m2']:.3f} | "
            f"{o['qualifying_m2']:.3f} |"
        )
    lines += [
        f"| **Total** | | | | **{result['gross_m2']:.3f}** | **{result['qualifying_m2']:.3f}** |",
        "",
        "## 2. Required vs available",
        "",
        "Cells show `effective Ag / required Ag`; PASS means effective glass area is at least the simplified-route requirement. "
        "Frame factor is the fraction of gross qualifying glass that remains after frame/glazing reduction.",
        "",
        "| LT | Required Ag m² | ff 1.00 | ff 0.90 | ff 0.85 | ff 0.80 |",
        "|---:|---:|---|---|---|---|",
    ]
    for row in result["scenarios"]:
        cells = []
        for ff in FRAME_FACTORS:
            item = row["by_frame_factor"][f"{ff:.2f}"]
            cells.append(f"{item['effective_m2']:.2f} / {row['required_m2']:.2f} "
                         f"{'PASS' if item['pass'] else 'FAIL'}")
        lines.append(
            f"| {row['LT']:.2f} | {row['required_m2']:.2f} | " + " | ".join(cells) + " |"
        )
    lines += [
        "",
        "## 3. Minimum light transmittance",
        "",
        "| Frame factor | Effective Ag m² | Minimum LT to satisfy §13-7 |",
        "|---:|---:|---:|",
    ]
    for ff in FRAME_FACTORS:
        key = f"{ff:.2f}"
        lines.append(
            f"| {ff:.2f} | {result['qualifying_m2'] * ff:.3f} | {result['minimum_lt'][key]:.4f} |"
        )
    lines += [
        "",
        "## 4. Interpretation",
        "",
        f"- Gross window area is **{result['gross_m2']:.2f} m²**; all sills are at or above 900 mm, "
        f"so the qualifying area is also **{result['qualifying_m2']:.2f} m²** before frame reduction.",
        f"- With no frame reduction (ff=1.00), the minimum LT is **{result['minimum_lt']['1.00']:.3f}**. "
        f"At ff=0.85 it rises to **{result['minimum_lt']['0.85']:.3f}**; at ff=0.80, "
        f"**{result['minimum_lt']['0.80']:.3f}**.",
        "- If the actual glazing LT or frame factor is lower, the design needs more glass, better glazing, "
        "or the general daylight-factor route (average DF >= 2.0 % with CIE 171:2006-validated simulation).",
        "- The door may add qualifying glass if its glazing is documented; it is conservatively excluded here.",
        "- The simplified route depends on the final legal use being the mikrohus/dwelling route; if C-01 lands "
        "on a temporary building, confirm §13-7 applicability with the municipality.",
        "",
        "## 5. Source and status",
        "",
        "- TEK17 §13-7 and simplified dwelling route: S023.",
        "- Aperture geometry: `fase1/tabla-aberturas.csv` (R0 conceptual).",
        "- Generated by `scripts/daylight_check.py`; JSON companion: `knowledge/comparisons/daylight-check.json`.",
        "- SCREENING ONLY — no compliance certificate, no fabrication release.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    assert abs(qualifying_area_m2(1200, 1100, 900) - 1.32) < 1e-9
    assert abs(qualifying_area_m2(500, 500, 700) - 0.20) < 1e-9
    assert qualifying_area_m2(500, 100, 700) == 0.0
    openings = [
        {"id": "V-1", "description": "a", "sill_mm": 900, "width_mm": 1200,
         "height_mm": 1100, "gross_m2": 1.32, "qualifying_m2": 1.32},
        {"id": "V-2", "description": "b", "sill_mm": 1100, "width_mm": 1000,
         "height_mm": 900, "gross_m2": 0.90, "qualifying_m2": 0.90},
        {"id": "V-3", "description": "c", "sill_mm": 1500, "width_mm": 500,
         "height_mm": 500, "gross_m2": 0.25, "qualifying_m2": 0.25},
    ]
    result = evaluate(openings, 18.0)
    assert abs(result["gross_m2"] - 2.47) < 1e-9
    assert abs(result["qualifying_m2"] - 2.47) < 1e-9
    assert abs(result["minimum_lt"]["1.00"] - 1.26 / 2.47) < 1e-4
    assert abs(result["minimum_lt"]["0.80"] - 1.26 / (2.47 * 0.8)) < 1e-4
    # At LT=0.60, required = 2.10; ff=0.85 gives 2.0995 -> just fails.
    row = next(r for r in result["scenarios"] if abs(r["LT"] - 0.60) < 1e-9)
    assert row["by_frame_factor"]["0.85"]["pass"] is False
    assert row["by_frame_factor"]["0.90"]["pass"] is True
    print("Daylight self-test OK: qualifying area, total, minimum LT and frame-factor pass/fail checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aperturas", nargs="?")
    ap.add_argument("--abra", type=float, default=18.0, help="heated floor area m2 (default 18)")
    ap.add_argument("--out-md", help="write Markdown report")
    ap.add_argument("--out-json", help="write JSON result")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return
    if not args.aperturas:
        ap.error("falta el CSV de aberturas (o use --selftest)")

    openings = read_openings(args.aperturas)
    result = evaluate(openings, args.abra)
    model = {"state": "SCREENING — CONDITIONAL ON C-01", "openings": openings, **result}
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(openings, result, args.aperturas), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(markdown(openings, result, args.aperturas))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
