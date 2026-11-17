#!/usr/bin/env python3
"""MiniHouse · TEK17 Chapter 11 fire screening.

Screens the current conceptual geometry against the dimensional provisions of
TEK17 chapter 11 for a single-storey dwelling (risikoklasse 4, brannklasse 1).
It reproduces the escape-window check in S024 and reports the fire-class,
fire-cell, detection, extinguishing and fire-service-access requirements that
follow from the same route.

This is a screening tool. It does not perform a fire-engineering analysis, does
not produce a fire strategy document and does not certify compliance.

Usage:
  python fire_check.py fase1/tabla-aberturas.csv \
      --separation-m 8.0 --travel-m 6.0 \
      --out-md fase1/verificacion-incendio.md \
      --out-json knowledge/comparisons/fire-check.json
  python fire_check.py --selftest
"""
import argparse
import csv
import json
import sys
from pathlib import Path

# --- §11-2 / §11-3 -----------------------------------------------------------
RISIKOKLASSE = 4          # bolig and fritidsbolig both land here
BRANNKLASSE = 1           # risk class 4, one storey

# --- §11-4 ------------------------------------------------------------------
R_MAIN_MIN = 15           # §11-4(3) no. 4: BKL 1 + risk class 4 -> R 15
R_TABLE_BKL1 = 30         # Table 1 nominal value, superseded by no. 4 here

# --- §11-6 ------------------------------------------------------------------
MIN_SEPARATION_M = 8.0
CAMPING_SEPARATION_M = 4.0

# --- §11-8 ------------------------------------------------------------------
FIRE_CELL_EI_BKL1 = 30

# --- §11-12 -----------------------------------------------------------------
SMOKE_ALARM_MIN_DB = 60
DWELLING_ALARM_ZONES = (
    "kjøkken (kitchen)",
    "stue (living room)",
    "sone utenfor soverom (zone outside bedrooms)",
    "tekniske rom (technical rooms)",
)

# --- §11-13 -----------------------------------------------------------------
ESCAPE_MIN_HEIGHT_MM = 600.0
ESCAPE_MIN_WIDTH_MM = 500.0
ESCAPE_MIN_SUM_MM = 1500.0
ESCAPE_MAX_SILL_MM = 1000.0
ESCAPE_MAX_SILL_ABOVE_GROUND_MM = 5000.0
ESCAPE_MAX_SILL_ABOVE_GROUND_LADDER_MM = 7500.0

# --- §11-14 -----------------------------------------------------------------
MIN_FREE_WIDTH_MM = 860.0     # risk classes 1, 2 and 4

# --- §11-9 ------------------------------------------------------------------
SURFACE_WALL_CEILING = "D-s2,d0"
SURFACE_WALL_CEILING_ESCAPE = "B-s1,d0"
SURFACE_EXTERNAL = "D-s3,d0"
CLADDING_CELL = "K210 D-s2,d0"
ROOF_COVERING = "BROOF(t2)"
INSULATION_MAIN = "A2-s1,d0"
SMALL_FIRE_CELL_M2 = 200.0

# --- §11-10 -----------------------------------------------------------------
KITCHEN_EXTRACT_DWELLING = "EI 15 A2-s1,d0"
CABLE_FUNCTION_MIN = 30       # minutes, fire class 1
CABLE_LOW_ENERGY_MJ_M = 50.0  # approx. threshold per running metre

# --- §11-16 -----------------------------------------------------------------
HOSE_MIN_DIAMETER_MM = 10.0
HOSE_MAX_LENGTH_M = 30.0
EXTINGUISHER_POWDER_KG = 6.0
EXTINGUISHER_FOAM_L = 9.0
EXTINGUISHER_MIN_L_21A = 6.0

# --- §11-17 -----------------------------------------------------------------
MAX_ACCESS_DISTANCE_M = 50.0
WATER_SMALLHOUSE_LPM = 1200
HYDRANT_MIN_M = 25.0
HYDRANT_MAX_M = 50.0
MAX_HOSE_LAY_M = 50.0


def escape_window(width_mm, height_mm, sill_mm):
    """Screen one opening against §11-13(4) escape-window dimensions."""
    checks = {
        "height_ok": height_mm >= ESCAPE_MIN_HEIGHT_MM,
        "width_ok": width_mm >= ESCAPE_MIN_WIDTH_MM,
        "sum_ok": (height_mm + width_mm) >= ESCAPE_MIN_SUM_MM,
        "sill_ok": sill_mm <= ESCAPE_MAX_SILL_MM,
    }
    return {
        "height_mm": height_mm,
        "width_mm": width_mm,
        "sum_mm": height_mm + width_mm,
        "sill_mm": sill_mm,
        "checks": checks,
        "qualifies": all(checks.values()),
        "fails": [k.replace("_ok", "") for k, v in checks.items() if not v],
    }


def read_openings(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    windows, doors = [], []
    for row in rows:
        ident = row["id"].strip()
        try:
            width = float(row["ancho_mm"])
            height = float(row["alto_mm"])
            sill = float(row["z_antepecho_mm"])
        except (KeyError, ValueError) as exc:
            raise SystemExit(f"ERROR apertura {ident or '?'}: {exc}")
        item = {
            "id": ident,
            "description": row["descripcion"].strip(),
            "width_mm": width,
            "height_mm": height,
            "sill_mm": sill,
        }
        if ident.upper().startswith("V-"):
            windows.append({**item, **escape_window(width, height, sill)})
        else:
            doors.append(item)
    if not windows:
        raise SystemExit("ERROR: no window rows (V-*) found")
    return windows, doors


def screen(windows, doors, separation_m, travel_m, storey_count=1, cell_area_m2=18.0):
    qualifying = [w for w in windows if w["qualifies"]]
    door_margin = None
    if doors:
        leaf = min(d["width_mm"] for d in doors)
        door_margin = round(leaf - MIN_FREE_WIDTH_MM, 1)

    return {
        "state": "SCREENING — CONDITIONAL ON C-01",
        "classification": {
            "risikoklasse": RISIKOKLASSE,
            "brannklasse": BRANNKLASSE,
            "storeys": storey_count,
            "note": "bolig and fritidsbolig share risk class 4 / BKL 1 in one storey",
        },
        "load_bearing": {
            "required_R_minutes": R_MAIN_MIN,
            "table_value_bkl1_minutes": R_TABLE_BKL1,
            "governing_clause": "§11-4(3) no. 4",
            "applies_to": "main and secondary load-bearing system",
        },
        "fire_cell": {
            "boenhet_is_own_cell": True,
            "general_EI_minutes_bkl1": FIRE_CELL_EI_BKL1,
            "cell_area_m2": cell_area_m2,
            "small_cell_threshold_m2": SMALL_FIRE_CELL_M2,
            "note": "single boenhet with no adjoining unit; no area-based exemption exists",
        },
        "materials": {
            "wall_ceiling": SURFACE_WALL_CEILING,
            "wall_ceiling_if_escape_route": SURFACE_WALL_CEILING_ESCAPE,
            "external_cladding": SURFACE_EXTERNAL,
            "cladding": CLADDING_CELL,
            "roof_covering": ROOF_COVERING,
            "insulation_main_rule": INSULATION_MAIN,
            "timber_interior_admissible": cell_area_m2 <= SMALL_FIRE_CELL_M2,
            "caveat": "only if the cabin is not treated as an escape route; B-s1,d0 would apply otherwise",
        },
        "installations": {
            "kitchen_extract": KITCHEN_EXTRACT_DWELLING,
            "own_duct_with_grease_filter": True,
            "cable_function_minutes": CABLE_FUNCTION_MIN,
            "cable_low_energy_mj_per_m": CABLE_LOW_ENERGY_MJ_M,
        },
        "separation": {
            "distance_m": separation_m,
            "required_m": MIN_SEPARATION_M,
            "pass": separation_m >= MIN_SEPARATION_M,
            "camping_alternative_m": CAMPING_SEPARATION_M,
        },
        "escape": {
            "qualifying_windows": [w["id"] for w in qualifying],
            "qualifying_count": len(qualifying),
            "single_direction_ok": len(qualifying) >= 1,
            "plural_wording_note": "§11-13(4) says 'vinduer' (plural) per fire cell; "
                                   "confirm whether one window satisfies a one-room cabin",
            "travel_m": travel_m,
            "travel_limit_m": None,
            "travel_note": "§11-13 Table 1 as retrieved does not list risk class 4",
            "min_free_width_mm": MIN_FREE_WIDTH_MM,
            "door_leaf_min_mm": min((d["width_mm"] for d in doors), default=None),
            "door_free_width_margin_mm": door_margin,
        },
        "detection": {
            "system": "interconnected mains-powered smoke alarms with battery backup",
            "full_alarm_system_required": False,
            "min_per_storey": 1,
            "zones": list(DWELLING_ALARM_ZONES),
            "min_db": SMOKE_ALARM_MIN_DB,
        },
        "manual_extinguishing": {
            "options": ["hand-held extinguisher", "fire hose reaching all rooms"],
            "hose_min_diameter_mm": HOSE_MIN_DIAMETER_MM,
            "hose_max_length_m": HOSE_MAX_LENGTH_M,
            "powder_kg": EXTINGUISHER_POWDER_KG,
            "foam_l": EXTINGUISHER_FOAM_L,
            "alt_l_21A": EXTINGUISHER_MIN_L_21A,
            "marking_required": False,
        },
        "fire_service": {
            "max_access_distance_m": MAX_ACCESS_DISTANCE_M,
            "water_smallhouse_lpm": WATER_SMALLHOUSE_LPM,
            "hydrant_min_m": HYDRANT_MIN_M,
            "hydrant_max_m": HYDRANT_MAX_M,
            "max_hose_lay_m": MAX_HOSE_LAY_M,
            "orientation_plan_required": False,
        },
    }


def markdown(windows, doors, result, source_path):
    esc = result["escape"]
    lines = [
        "# MiniHouse · TEK17 Chapter 11 fire screening",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a fire-engineering analysis, "
        "not a fire strategy document and not a compliance certificate.",
        "",
        f"- Aperture table: `{source_path}`",
        "- Governing route: **risikoklasse 4 / brannklasse 1** (bolig and fritidsbolig "
        "both land here in one storey — see S024).",
        "- Requirements source: S024 (DIBK, TEK17 chapter 11).",
        "",
        "## 1. Classification and load-bearing resistance",
        "",
        "| Item | Value | Clause |",
        "|---|---|---|",
        f"| Risikoklasse | {result['classification']['risikoklasse']} | §11-2 Table 1 |",
        f"| Brannklasse, one storey | BKL {result['classification']['brannklasse']} | §11-3 Table 1 |",
        f"| Required load-bearing resistance | **R {result['load_bearing']['required_R_minutes']}** | "
        f"{result['load_bearing']['governing_clause']} |",
        f"| Table 1 nominal value, BKL 1 | R {result['load_bearing']['table_value_bkl1_minutes']} | "
        "§11-4 Table 1 (superseded here by no. 4) |",
        f"| Fire-cell resistance, general BKL 1 | EI {result['fire_cell']['general_EI_minutes_bkl1']} | "
        "§11-8 Table 1 |",
        "",
        "R 15 governs, not R 30: §11-4(3) no. 4 allows a BKL 1 building in risk class 4 "
        "to have both the main and the secondary load-bearing system at R 15.",
        "",
        "## 2. Escape windows (§11-13(4))",
        "",
        "| ID | Size mm | Sill mm | Height+width mm | h≥600 | w≥500 | sum≥1500 | sill≤1000 | Verdict |",
        "|---|---|---:|---:|---|---|---|---|---|",
    ]
    for w in windows:
        c = w["checks"]
        mark = lambda ok: "PASS" if ok else "**FAIL**"
        lines.append(
            f"| {w['id']} | {w['width_mm']:.0f} × {w['height_mm']:.0f} | {w['sill_mm']:.0f} | "
            f"{w['sum_mm']:.0f} | {mark(c['height_ok'])} | {mark(c['width_ok'])} | "
            f"{mark(c['sum_ok'])} | {mark(c['sill_ok'])} | "
            f"{'qualifies' if w['qualifies'] else 'does not qualify'} |"
        )
    lines += [
        "",
        f"**Qualifying escape windows: {esc['qualifying_count']}** "
        f"({', '.join(esc['qualifying_windows']) if esc['qualifying_windows'] else 'none'}).",
        "",
        "Doors are not escape windows. They are checked only against the §11-14 free width:",
        "",
        "| Door | Leaf mm | Free width required mm | Margin mm |",
        "|---|---:|---:|---:|",
    ]
    for d in doors:
        margin = d["width_mm"] - MIN_FREE_WIDTH_MM
        lines.append(
            f"| {d['id']} | {d['width_mm']:.0f} | {MIN_FREE_WIDTH_MM:.0f} | {margin:+.0f} |"
        )
    lines += [
        "",
        "A 900 mm leaf leaves only 40 mm for frame, hinge and stop build-up before the "
        "0.86 m free width is lost. Confirm the free width on the door schedule; do not "
        "assume the nominal leaf size satisfies it.",
        "",
        "## 3. Other chapter 11 provisions",
        "",
        "| Provision | Requirement for MiniHouse | Status |",
        "|---|---|---|",
        f"| §11-6 separation | ≥ {result['separation']['required_m']:.1f} m to other low buildings "
        f"(input: {result['separation']['distance_m']:.1f} m) | "
        f"{'PASS' if result['separation']['pass'] else '**FAIL** — needs separation or siting change'} |",
        "| §11-7 sectioning | no driver at 18 m²; every threshold is ≥ 800 m² | not applicable in practice |",
        "| §11-8 fire cells | single boenhet is one cell; no area exemption exists | as designed |",
        f"| §11-9 surfaces | walls/ceiling **{result['materials']['wall_ceiling']}**, cladding "
        f"**{result['materials']['cladding']}**, external **{result['materials']['external_cladding']}**, "
        f"roof **{result['materials']['roof_covering']}** | timber interior admissible if not an escape route |",
        f"| §11-9 insulation | main rule **{result['materials']['insulation_main_rule']}**; no. 7 needs an "
        "A2-s1,d0 load-bearing substrate | roof insulation converges on mineral wool |",
        f"| §11-10 kitchen extract | own duct with grease filter, **{result['installations']['kitchen_extract']}** "
        "if not in a shaft | required |",
        f"| §11-10 cables | **≥{result['installations']['cable_function_minutes']} min** function if "
        "required during fire; low-energy exemption below "
        f"~{result['installations']['cable_low_energy_mj_per_m']:.0f} MJ/m | check extract fan and dampers |",
        "| §11-12 detection | interconnected mains smoke alarms, battery backup, "
        f"≥1 per storey, ≥{result['detection']['min_db']} dB with doors closed | required |",
        "| §11-12 zones | kitchen, living room, zone outside bedrooms, technical rooms | 4 zones |",
        "| §11-16 manual extinguishing | one extinguisher or a "
        f"≥{result['manual_extinguishing']['hose_min_diameter_mm']:.0f} mm form-stable hose "
        f"(≤{result['manual_extinguishing']['hose_max_length_m']:.0f} m) | required |",
        "| §11-16 marking | not required where equipment serves one dwelling unit | exempt |",
        f"| §11-17 access | ≤ {result['fire_service']['max_access_distance_m']:.0f} m driving "
        "distance to the main entrance | site-dependent |",
        f"| §11-17 water | ≥ {result['fire_service']['water_smallhouse_lpm']} l/min in small-house "
        "areas | site-dependent |",
        f"| §11-17 hydrant | {result['fire_service']['hydrant_min_m']:.0f}–"
        f"{result['fire_service']['hydrant_max_m']:.0f} m from the main attack route entrance "
        "| site-dependent |",
        "| §11-17 orientation plan | not required for risk class 4 | not applicable |",
        "",
        "## 4. What this screen does not settle",
        "",
        "1. Whether the roof belongs to the main load-bearing system (R 15) or is a roof-only "
        "construction eligible for §11-4(3) no. 6. The answer changes the roof build-up.",
        "2. Whether one qualifying escape window satisfies §11-13(4) for a one-room cabin.",
        "3. Whether the technical cupboard needs EI 30 separation.",
        "4. The §11-13 Table 1 travel distance for risk class 4, which the retrieved table "
        "does not list.",
        "5. Whether the whole cabin counts as an escape route for §11-9 surface classes. "
        "D-s2,d0 keeps exposed reclaimed timber viable; B-s1,d0 would not.",
        "6. Whether any wood-fibre insulation can be justified in the roof under §11-9 D no. 7 "
        "or by documented analysis.",
        "",
        "## 5. Source and status",
        "",
        "- TEK17 chapter 11: S024.",
        "- Aperture geometry: `fase1/tabla-aberturas.csv` (R0 conceptual).",
        "- Generated by `scripts/fire_check.py`; JSON companion: "
        "`knowledge/comparisons/fire-check.json`.",
        "- SCREENING ONLY — no fire strategy, no compliance certificate, no fabrication release.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # Dimensions from the R0 aperture table.
    v01 = escape_window(1200, 1100, 900)
    v02 = escape_window(1000, 900, 1100)
    v03 = escape_window(500, 500, 1500)
    assert v01["qualifies"] is True, v01
    assert v02["qualifies"] is False and v02["fails"] == ["sill"], v02
    assert v03["qualifies"] is False, v03
    assert set(v03["fails"]) == {"height", "sum", "sill"}, v03
    assert v03["sum_mm"] == 1000.0

    # Boundary behaviour: 900 + 600 = 1500 exactly at the sum limit.
    assert escape_window(900, 600, 1000)["qualifies"] is True       # exactly at the limits
    assert escape_window(900, 600, 1001)["qualifies"] is False      # sill one mm over
    assert escape_window(901, 599, 1000)["qualifies"] is False      # height one mm under
    # A 500 x 600 window passes both individual minima but fails the sum rule.
    assert escape_window(500, 600, 900)["fails"] == ["sum"]

    windows = [
        {"id": "V-01", "description": "a", "width_mm": 1200, "height_mm": 1100,
         "sill_mm": 900, **{k: v for k, v in v01.items()
                            if k not in ("width_mm", "height_mm", "sill_mm")}},
        {"id": "V-02", "description": "b", "width_mm": 1000, "height_mm": 900,
         "sill_mm": 1100, **{k: v for k, v in v02.items()
                             if k not in ("width_mm", "height_mm", "sill_mm")}},
        {"id": "V-03", "description": "c", "width_mm": 500, "height_mm": 500,
         "sill_mm": 1500, **{k: v for k, v in v03.items()
                             if k not in ("width_mm", "height_mm", "sill_mm")}},
    ]
    doors = [{"id": "P-01", "width_mm": 900, "height_mm": 2050, "sill_mm": 0}]
    result = screen(windows, doors, separation_m=8.0, travel_m=6.0)
    assert result["escape"]["qualifying_count"] == 1
    assert result["escape"]["qualifying_windows"] == ["V-01"]
    assert result["escape"]["door_free_width_margin_mm"] == 40.0
    assert result["separation"]["pass"] is True
    assert screen(windows, doors, 7.9, 6.0)["separation"]["pass"] is False
    assert result["load_bearing"]["required_R_minutes"] == 15
    assert len(result["detection"]["zones"]) == 4
    # §11-9: D-s2,d0 keeps exposed timber viable in a cell up to 200 m2.
    assert result["materials"]["wall_ceiling"] == "D-s2,d0"
    assert result["materials"]["wall_ceiling_if_escape_route"] == "B-s1,d0"
    assert result["materials"]["timber_interior_admissible"] is True
    assert screen(windows, doors, 8.0, 6.0, cell_area_m2=250)["materials"][
        "timber_interior_admissible"] is False
    assert result["installations"]["kitchen_extract"] == "EI 15 A2-s1,d0"
    assert result["installations"]["cable_function_minutes"] == 30
    print("Fire self-test OK: escape-window dimensions, boundary cases, door margin, "
          "separation threshold, R15 selection, surface classes and extract duct all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aperturas", nargs="?")
    ap.add_argument("--separation-m", type=float, default=MIN_SEPARATION_M,
                    help="distance to the nearest other building (default 8.0)")
    ap.add_argument("--travel-m", type=float, default=6.0,
                    help="longest travel distance to an exit (default 6.0)")
    ap.add_argument("--storeys", type=int, default=1)
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return
    if not args.aperturas:
        ap.error("falta el CSV de aberturas (o use --selftest)")

    windows, doors = read_openings(args.aperturas)
    result = screen(windows, doors, args.separation_m, args.travel_m, args.storeys)
    model = {"windows": windows, "doors": doors, **result}
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(windows, doors, result, args.aperturas), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(markdown(windows, doors, result, args.aperturas))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
