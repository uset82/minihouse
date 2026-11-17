#!/usr/bin/env python3
"""MiniHouse · TEK17 §12-7(2)(c)/(d) room-height screening for the R1 gable.

The mikrohus route requires a room height of 2.2 m (§12-7(2)(c)) and allows
parts of a room to be lower, including a sloped ceiling below 2.2 m
(§12-7(2)(d) and its pre-accepted solutions). This script quantifies the
trade-off between three things that were previously compared only in prose:

  1. the free height reached at the eave,
  2. how much of the 3 m floor width reaches 2.2 m,
  3. the resulting transport height against the 4.00 m screening value.

Free height is measured floor-to-ceiling, so the floor build-up above the
chassis datum is an explicit parameter, never a hidden assumption. The script
sweeps it and reports the sensitivity.

This is a screening tool. It does not decide how much of the floor must reach
2.2 m: that is a functional judgement under §12-7(1) and (2)(d), to be
documented by the responsible designer, not assumed here.

Usage:
  python room_height_check.py --out-md fase1/verificacion-altura-libre.md \
      --out-json knowledge/comparisons/room-height-check.json
  python room_height_check.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

WIDTH_MM = 3000.0
HALF_WIDTH_MM = WIDTH_MM / 2.0
PITCHES = (5.0, 10.0, 15.0, 20.0)
TARGET_FREE_MM = 2200.0
TRANSPORT_LIMIT_MM = 4000.0
STACKS = (900.0, 1100.0)
FLOOR_Z = (100.0, 150.0, 200.0, 250.0)
COVERAGE_TARGETS = (1.00, 0.75, 0.60)


def free_height(eave_z, floor_z, pitch_deg, d_mm):
    """Free height at horizontal distance d from the wall, toward the ridge."""
    return (eave_z - floor_z) + d_mm * math.tan(math.radians(pitch_deg))


def contour_d(eave_z, floor_z, pitch_deg, target_mm=TARGET_FREE_MM):
    """Distance from the wall where free height reaches the target (0 if already met)."""
    at_wall = eave_z - floor_z
    if at_wall >= target_mm:
        return 0.0
    rise = math.tan(math.radians(pitch_deg))
    if rise <= 0:
        return HALF_WIDTH_MM
    return min(HALF_WIDTH_MM, (target_mm - at_wall) / rise)


def coverage(eave_z, floor_z, pitch_deg, target_mm=TARGET_FREE_MM):
    """Fraction of the floor width whose free height reaches the target."""
    d = contour_d(eave_z, floor_z, pitch_deg, target_mm)
    return max(0.0, min(1.0, 1.0 - d / HALF_WIDTH_MM))


def required_eave(floor_z, pitch_deg, target_coverage, target_mm=TARGET_FREE_MM):
    """Eave height that gives the target coverage."""
    d = (1.0 - target_coverage) * HALF_WIDTH_MM
    return target_mm + floor_z - d * math.tan(math.radians(pitch_deg))


def ridge_z(eave_z, pitch_deg):
    return eave_z + HALF_WIDTH_MM * math.tan(math.radians(pitch_deg))


def transport_z(ridge, stack):
    return ridge + stack


def max_eave_for_transport(pitch_deg, stack, limit_mm=TRANSPORT_LIMIT_MM):
    return limit_mm - stack - HALF_WIDTH_MM * math.tan(math.radians(pitch_deg))


def max_pitch_for_full_coverage(floor_z, stack, limit_mm=TRANSPORT_LIMIT_MM):
    """Largest pitch at which the whole width can reach the target under the limit."""
    slack = limit_mm - stack - TARGET_FREE_MM - floor_z
    if slack <= 0:
        return 0.0
    return math.degrees(math.atan(slack / HALF_WIDTH_MM))


def screen(width_mm=WIDTH_MM, pitches=PITCHES, stacks=STACKS, floor_z=FLOOR_Z,
           targets=COVERAGE_TARGETS):
    rows = []
    for pitch in pitches:
        rise = (width_mm / 2.0) * math.tan(math.radians(pitch))
        for stack in stacks:
            cap = limit_mm = TRANSPORT_LIMIT_MM
            eave_cap = max_eave_for_transport(pitch, stack, cap)
            entry = {
                "pitch_deg": pitch,
                "rise_mm": round(rise, 1),
                "stack_mm": stack,
                "max_eave_for_4m_mm": round(eave_cap, 1),
                "max_pitch_full_coverage_deg": {},
                "cases": [],
            }
            for fz in floor_z:
                entry["max_pitch_full_coverage_deg"][f"{fz:.0f}"] = round(
                    max_pitch_for_full_coverage(fz, stack, limit_mm), 2)
                for target in targets:
                    eave_req = required_eave(fz, pitch, target)
                    ridge = ridge_z(eave_req, pitch)
                    trans = transport_z(ridge, stack)
                    entry["cases"].append({
                        "floor_z_mm": fz,
                        "coverage": target,
                        "required_eave_mm": round(eave_req, 1),
                        "ridge_mm": round(ridge, 1),
                        "transport_mm": round(trans, 1),
                        "margin_mm": round(limit_mm - trans, 1),
                        "fits": trans <= limit_mm,
                        "coverage_at_eave_cap": round(coverage(eave_cap, fz, pitch), 3),
                    })
            rows.append(entry)
    return {
        "state": "SCREENING — CONDITIONAL ON C-01/C-02",
        "width_mm": width_mm,
        "half_width_mm": width_mm / 2.0,
        "target_free_mm": TARGET_FREE_MM,
        "transport_limit_mm": TRANSPORT_LIMIT_MM,
        "rows": rows,
    }


def markdown(result):
    lines = [
        "# MiniHouse · TEK17 §12-7 room-height screening for the R1 gable",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01/C-02. Not a design decision and not a compliance certificate.",
        "",
        f"- Floor width: **{result['width_mm']:.0f} mm**; half-width {result['half_width_mm']:.0f} mm.",
        f"- Required free height on the mikrohus route: **{result['target_free_mm']:.0f} mm** (§12-7(2)(c)).",
        f"- Transport screening value: **{result['transport_limit_mm']:.0f} mm** (S022; general value, not a route permit).",
        "- Free height is measured **floor to ceiling**, so the floor build-up above the chassis datum is a parameter, not an assumption.",
        "",
        "## 1. How much of the floor reaches 2.2 m at the eave",
        "",
        "For each pitch and trailer stack, the table shows the highest eave that still fits under 4.00 m, and the resulting fraction of the floor width that reaches 2.2 m free height, for several floor build-ups.",
        "",
        "| Pitch | Rise mm | Stack mm | Max eave for 4.00 m | Coverage, floor 100 | floor 150 | floor 200 | floor 250 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["rows"]:
        cov = {c["floor_z_mm"]: c["coverage_at_eave_cap"] for c in row["cases"]}
        cells = " | ".join(
            f"{cov[fz]:.0%}" if cov[fz] >= 0.999 else f"{cov[fz]:.1%}"
            for fz in (100.0, 150.0, 200.0, 250.0)
        )
        lines.append(
            f"| {row['pitch_deg']:.0f}° | {row['rise_mm']:.0f} | {row['stack_mm']:.0f} | "
            f"{row['max_eave_for_4m_mm']:.0f} | {cells} |"
        )
    lines += [
        "",
        "## 2. Eave needed for a chosen coverage",
        "",
        "Cells show `eave mm → transport mm (margin)`. A negative margin means the case does not fit under 4.00 m.",
        "",
        "| Pitch | Stack | Floor | 100 % of width | 75 % | 60 % |",
        "|---:|---:|---:|---|---|---|",
    ]
    for row in result["rows"]:
        for fz in (100.0, 150.0, 200.0, 250.0):
            cells = []
            for target in COVERAGE_TARGETS:
                c = next(x for x in row["cases"]
                         if x["floor_z_mm"] == fz and abs(x["coverage"] - target) < 1e-9)
                flag = "" if c["fits"] else " **OVER**"
                cells.append(
                    f"{c['required_eave_mm']:.0f} → {c['transport_mm']:.0f} "
                    f"({c['margin_mm']:+.0f}){flag}"
                )
            lines.append(
                f"| {row['pitch_deg']:.0f}° | {row['stack_mm']:.0f} | {fz:.0f} | "
                + " | ".join(cells) + " |"
            )
    lines += [
        "",
        "## 3. Largest pitch that still gives 2.2 m over the whole width",
        "",
        "| Stack | Floor 100 | Floor 150 | Floor 200 | Floor 250 |",
        "|---:|---:|---:|---:|---:|",
    ]
    seen = []
    for row in result["rows"]:
        if row["stack_mm"] in seen:
            continue
        seen.append(row["stack_mm"])
        vals = " | ".join(
            f"{row['max_pitch_full_coverage_deg'][f'{fz:.0f}']:.1f}°"
            for fz in (100.0, 150.0, 200.0, 250.0)
        )
        lines.append(f"| {row['stack_mm']:.0f} | {vals} |")
    tight = [
        r for r in result["rows"]
        if r["stack_mm"] == max(seen) and r["pitch_deg"] == max(PITCHES)
    ]
    lines += [
        "",
        "## 4. Interpretation",
        "",
        "- **§12-7(2)(d) changes what the eave has to be, not whether the height fits.** The earlier R1 warning compared the maximum eave directly with 2.2 m and called the 154 mm difference the whole allowance. Under (2)(d) and its pre-accepted solution 2 a sloped ceiling **may go below 2.2 m in parts**, so the eave is not the room-height datum. But if **full-width** 2.2 m is wanted, that 154 mm is exactly the allowance for the floor build-up — and a normal timber floor on steel consumes almost all of it.",
    ]
    if tight:
        cap = tight[0]["max_pitch_full_coverage_deg"]
        lines.append(
            f"- **At {tight[0]['pitch_deg']:.0f}° with a {tight[0]['stack_mm']:.0f} mm stack the full-coverage pitch cap is "
            f"{cap['100']:.1f}° / {cap['150']:.1f}° / {cap['200']:.1f}° / {cap['250']:.1f}° for floor build-ups of "
            "100 / 150 / 200 / 250 mm.** A 20° pitch therefore sits **almost exactly on the limit** at a 150 mm floor "
            "build-up and **passes it** beyond roughly 200 mm. This is a real constraint, not a comfortable margin."
        )
    lines += [
        "- **The steeper the pitch, the tighter it gets** — because the ridge rises faster than the eave falls. A 5–15° roof keeps a wide margin; 20° is where the two limits meet.",
        "- **Relief comes from accepting partial coverage**, which (2)(d) permits. The tables quantify the trade: dropping to 75 % or 60 % of the width buys eave height, and with it transport margin.",
        "- **What the regulation does not state is a required fraction.** §12-7(1) requires the layout to suit its function and (2)(d) allows lower parts where function is unaffected. That is a judgement to document, not a value to default.",
        "- **The floor build-up is not yet defined (C-02).** Until it is, read the range rather than a single column, and do not treat 150 mm as project data.",
        "",
        "## 5. Source and status",
        "",
        "- TEK17 §12-7(2)(c) and (2)(d): S025.",
        "- Transport screening value 4.00 m: S022 (general value, not a route permit).",
        "- Geometry width 3000 mm: R0 assumption, final C-02 pending.",
        "- Generated by `scripts/room_height_check.py`; JSON companion: `knowledge/comparisons/room-height-check.json`.",
        "- **Superseded in scope, not in arithmetic.** This screen treats the roof as a line with no "
        "thickness, and it sweeps the floor build-up from 100 mm. A real roof build-up costs "
        "**t/cos θ** vertically, and the envelope screen pushes the floor to ~250 mm. Both omissions "
        "flatter the result. The integrated answer is in "
        "[verificación de sección](verificacion-seccion.md): at 20° with a 1100 mm stack, a 250 mm "
        "floor and a 300 mm roof, the wall cannot even reach 2.2 m and only ~24 % of the width "
        "qualifies.",
        "- SCREENING ONLY — no geometry freeze, no compliance certificate, no fabrication release.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # Cross-check against the R1 inverse envelope: 20 deg, 1100 mm stack, 3000 mm width.
    assert abs(max_eave_for_transport(20.0, 1100.0) - 2354.1) < 0.2
    assert abs(ridge_z(2200.0, 20.0) - 2745.9) < 0.2
    # Free height at the wall equals eave minus floor build-up.
    assert abs(free_height(2354.1, 150.0, 20.0, 0.0) - 2204.1) < 0.2
    # Coverage is full when the wall already reaches the target.
    assert coverage(2354.1, 150.0, 20.0) == 1.0
    # With a 250 mm floor the wall falls short and coverage drops below 1.
    cov = coverage(2354.1, 250.0, 20.0)
    assert 0.80 < cov < 0.85, cov
    # Required eave for full coverage is target plus floor build-up.
    assert abs(required_eave(150.0, 20.0, 1.0) - 2350.0) < 1e-6
    # Contour distance is zero at or above the target.
    assert contour_d(2500.0, 150.0, 20.0) == 0.0
    # Monotonic: steeper pitch needs a lower eave for the same coverage.
    assert required_eave(150.0, 20.0, 0.6) < required_eave(150.0, 10.0, 0.6)
    # Transport identity closes.
    e = required_eave(150.0, 20.0, 0.6)
    assert abs(transport_z(ridge_z(e, 20.0), 1100.0)
               - (e + 1500.0 * math.tan(math.radians(20.0)) + 1100.0)) < 1e-6
    # Full-coverage pitch cap falls as the stack grows.
    assert max_pitch_for_full_coverage(150.0, 1100.0) < max_pitch_for_full_coverage(150.0, 900.0)
    result = screen()
    assert len(result["rows"]) == len(PITCHES) * len(STACKS)
    assert all(len(r["cases"]) == len(FLOOR_Z) * len(COVERAGE_TARGETS) for r in result["rows"])
    print("Room-height self-test OK: R1 cross-check, coverage, inverse eave, "
          "monotonicity and transport identity all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--width", type=float, default=WIDTH_MM)
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    result = screen(width_mm=args.width)
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(result), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(markdown(result))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
