#!/usr/bin/env python3
"""MiniHouse · integrated cross-section feasibility (height, pitch, envelope, transport).

Three separate screens have been pointing at the same cubic metres:

  * §12-7(2)(c) wants **2.2 m** of free height (room_height_check.py);
  * §14-3 wants an envelope thick enough that the wall needs ~189 mm of
    mineral wool and the roof ~247 mm (envelope_check.py);
  * the transport screening value is **4.00 m** including the trailer stack.

Each was computed on its own, and the room-height screen treated the roof as a
line with no thickness. This script solves them together, in one cross-section,
because they are not independent: every millimetre of floor build-up, roof
thickness or stack is a millimetre taken from the wall height, and the wall
height is what buys free height at the eave.

Section, with z = 0 at the chassis top:

    ridge top   = t_floor + h_wall + (W/2)·tan(pitch) + t_roof/cos(pitch)
    transport   = ridge top + stack            <= 4.00 m
    free height at distance d from the wall = h_wall + d·tan(pitch)

The roof thickness is perpendicular to the slope, so its vertical cost is
t_roof/cos(pitch) — which grows as the pitch steepens, on top of the ridge rise.
That double penalty is why the answer is not intuitive.

Usage:
  python section_feasibility.py --out-md fase1/verificacion-seccion.md \
      --out-json knowledge/comparisons/section-feasibility.json
  python section_feasibility.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

WIDTH_MM = 3000.0
HALF_WIDTH_MM = WIDTH_MM / 2.0
TARGET_FREE_MM = 2200.0
TRANSPORT_LIMIT_MM = 4000.0

PITCHES = (5.0, 10.0, 15.0, 20.0, 25.0)
STACKS = (900.0, 1100.0)
# Floor and roof build-ups consistent with envelope_check.py: ~238 mm of floor
# insulation plus deck and structure, ~247 mm of roof insulation plus board.
FLOOR_BUILDS = (200.0, 250.0, 300.0)
ROOF_BUILDS = (250.0, 300.0, 350.0)

# Wall thickness from the envelope screen, for the floor-area penalty.
WALL_BUILD_MM = 264.0
LENGTH_MM = 6000.0

# Reference case used for the "what has to give" analysis.
REF_PITCH = 20.0
REF_STACK = 1100.0
REF_FLOOR = 250.0
REF_ROOF = 300.0


def ridge_top(h_wall, pitch_deg, t_floor, t_roof, half_width=HALF_WIDTH_MM):
    """Height of the top of the roof above the chassis top."""
    p = math.radians(pitch_deg)
    return t_floor + h_wall + half_width * math.tan(p) + t_roof / math.cos(p)


def transport_height(h_wall, pitch_deg, stack, t_floor, t_roof):
    return ridge_top(h_wall, pitch_deg, t_floor, t_roof) + stack


def max_wall_height(pitch_deg, stack, t_floor, t_roof, limit=TRANSPORT_LIMIT_MM):
    """Tallest wall that still fits under the transport limit."""
    p = math.radians(pitch_deg)
    return limit - stack - t_floor - HALF_WIDTH_MM * math.tan(p) - t_roof / math.cos(p)


def coverage(h_wall, pitch_deg, target=TARGET_FREE_MM, half_width=HALF_WIDTH_MM):
    """Fraction of the half-width whose free height reaches the target."""
    if h_wall >= target:
        return 1.0
    rise = math.tan(math.radians(pitch_deg))
    if rise <= 0:
        return 0.0
    d = (target - h_wall) / rise
    return max(0.0, min(1.0, 1.0 - d / half_width))


def required_limit(h_wall, pitch_deg, stack, t_floor, t_roof):
    """Transport limit that a chosen design would need."""
    return transport_height(h_wall, pitch_deg, stack, t_floor, t_roof)


def max_pitch_full_coverage(stack, t_floor, t_roof, limit=TRANSPORT_LIMIT_MM,
                            target=TARGET_FREE_MM):
    """Steepest pitch at which the wall can still reach the target everywhere."""
    lo, hi = 0.01, 60.0
    if max_wall_height(lo, stack, t_floor, t_roof, limit) < target:
        return 0.0
    if max_wall_height(hi, stack, t_floor, t_roof, limit) >= target:
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if max_wall_height(mid, stack, t_floor, t_roof, limit) >= target:
            lo = mid
        else:
            hi = mid
    return lo


def max_stack_full_coverage(pitch_deg, t_floor, t_roof, limit=TRANSPORT_LIMIT_MM,
                            target=TARGET_FREE_MM):
    """Largest stack that still allows full 2.2 m coverage."""
    p = math.radians(pitch_deg)
    return (limit - t_floor - target - HALF_WIDTH_MM * math.tan(p)
            - t_roof / math.cos(p))


def max_floor_full_coverage(pitch_deg, stack, t_roof, limit=TRANSPORT_LIMIT_MM,
                            target=TARGET_FREE_MM):
    p = math.radians(pitch_deg)
    return (limit - stack - target - HALF_WIDTH_MM * math.tan(p)
            - t_roof / math.cos(p))


def max_roof_full_coverage(pitch_deg, stack, t_floor, limit=TRANSPORT_LIMIT_MM,
                           target=TARGET_FREE_MM):
    p = math.radians(pitch_deg)
    return (limit - stack - t_floor - target - HALF_WIDTH_MM * math.tan(p)) * math.cos(p)


def internal_area(wall_mm=WALL_BUILD_MM, length_mm=LENGTH_MM, width_mm=WIDTH_MM):
    """Internal floor area once the envelope thickness is taken off both sides."""
    w = (width_mm - 2 * wall_mm) / 1000.0
    l = (length_mm - 2 * wall_mm) / 1000.0
    return w, l, w * l


def screen():
    rows = []
    for pitch in PITCHES:
        for stack in STACKS:
            for t_f in FLOOR_BUILDS:
                for t_r in ROOF_BUILDS:
                    h = max_wall_height(pitch, stack, t_f, t_r)
                    cov = coverage(max(h, 0.0), pitch)
                    rows.append({
                        "pitch_deg": pitch, "stack_mm": stack,
                        "floor_mm": t_f, "roof_mm": t_r,
                        "max_wall_mm": round(h, 1),
                        "coverage": round(cov, 3),
                        "full_coverage": cov >= 0.999,
                        "transport_at_full": round(
                            transport_height(max(h, TARGET_FREE_MM), pitch, stack, t_f, t_r), 1),
                    })

    pitches = []
    for stack in STACKS:
        for t_f in FLOOR_BUILDS:
            for t_r in ROOF_BUILDS:
                pitches.append({
                    "stack_mm": stack, "floor_mm": t_f, "roof_mm": t_r,
                    "max_pitch_full_deg": round(
                        max_pitch_full_coverage(stack, t_f, t_r), 2),
                })

    w, l, area = internal_area()
    levers = {
        "reference": {"pitch_deg": REF_PITCH, "stack_mm": REF_STACK,
                      "floor_mm": REF_FLOOR, "roof_mm": REF_ROOF,
                      "max_wall_mm": round(max_wall_height(REF_PITCH, REF_STACK, REF_FLOOR, REF_ROOF), 1),
                      "coverage": round(coverage(max(max_wall_height(
                          REF_PITCH, REF_STACK, REF_FLOOR, REF_ROOF), 0.0), REF_PITCH), 3)},
        "stack_for_full_coverage": round(
            max_stack_full_coverage(REF_PITCH, REF_FLOOR, REF_ROOF), 1),
        "floor_for_full_coverage": round(
            max_floor_full_coverage(REF_PITCH, REF_STACK, REF_ROOF), 1),
        "roof_for_full_coverage": round(
            max_roof_full_coverage(REF_PITCH, REF_STACK, REF_FLOOR), 1),
        "limit_for_full_coverage": round(
            required_limit(TARGET_FREE_MM, REF_PITCH, REF_STACK, REF_FLOOR, REF_ROOF), 1),
        "pitch_for_full_coverage": round(
            max_pitch_full_coverage(REF_STACK, REF_FLOOR, REF_ROOF), 2),
    }

    return {
        "state": "SCREENING — PARAMETRIC, NO GEOMETRY FROZEN, NO PITCH SELECTED",
        "width_mm": WIDTH_MM, "target_free_mm": TARGET_FREE_MM,
        "transport_limit_mm": TRANSPORT_LIMIT_MM,
        "rows": rows, "pitches": pitches, "levers": levers,
        "internal": {"width_m": round(w, 3), "length_m": round(l, 3),
                     "area_m2": round(area, 2),
                     "gross_area_m2": round(LENGTH_MM * WIDTH_MM / 1e6, 2),
                     "loss_m2": round(LENGTH_MM * WIDTH_MM / 1e6 - area, 2),
                     "wall_build_mm": WALL_BUILD_MM},
    }


def markdown(result):
    L = result["levers"]
    ref = L["reference"]
    internal = result["internal"]
    lines = [
        "# MiniHouse · integrated cross-section feasibility",
        "",
        "**State:** SCREENING — PARAMETRIC, NO GEOMETRY FROZEN, NO PITCH SELECTED. Not a design "
        "decision and not a compliance certificate.",
        "",
        "- Required free height: **2.2 m** (TEK17 §12-7(2)(c), S025).",
        "- Transport screening value: **4.00 m** (S022; general value, not a route permit).",
        "- Envelope thicknesses: [envelope screening](verificacion-envolvente.md) — the wall needs "
        "~189 mm of mineral wool and the roof ~247 mm once thermal bridging counts.",
        "- z = 0 at the chassis top. `stack` includes the chassis depth, the trailer deck and the "
        "supports, so `transport = ridge top + stack`, consistent with "
        "[verificación de altura libre](verificacion-altura-libre.md).",
        "",
        "## 1. Why this needed its own calculation",
        "",
        "The room-height screen compared the eave with 2.2 m and the ridge with 4.00 m, but it "
        "treated the roof as a **line with no thickness**. A real roof has a build-up, and because "
        "that thickness is perpendicular to the slope its vertical cost is **t/cos θ** — so "
        "steepening the pitch costs twice: once through the ridge rise, and again through the roof "
        "thickness standing up. Meanwhile the envelope screen pushed the floor build-up from an "
        "assumed 150 mm to something closer to **250 mm**.",
        "",
        "Both corrections eat the same budget, so they had to be applied together:",
        "",
        "    ridge top = t_floor + h_wall + 1500·tan θ + t_roof / cos θ",
        "",
        "## 2. Tallest wall that fits, and the coverage it buys",
        "",
        "`h` is the wall height from finished floor to the underside of the roof at the eave, which "
        "is exactly the free height at the wall. `cov` is the fraction of the half-width that "
        "reaches 2.2 m.",
        "",
        "| Pitch | Stack | Floor | Roof | Max wall | Coverage |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for r in result["rows"]:
        if r["stack_mm"] != max(STACKS):
            continue
        mark = "" if r["full_coverage"] else " **partial**"
        lines.append(
            f"| {r['pitch_deg']:.0f}° | {r['stack_mm']:.0f} | {r['floor_mm']:.0f} | "
            f"{r['roof_mm']:.0f} | {r['max_wall_mm']:.0f} | {r['coverage']:.0%}{mark} |"
        )
    lines += [
        "",
        "Only the 1100 mm stack is shown; the 900 mm case is in the JSON companion. **A wall shorter "
        "than 2200 mm cannot give 2.2 m anywhere at the eave**, so any row below 2200 mm is already "
        "partial before the pitch is considered.",
        "",
        "## 3. Steepest pitch that still gives 2.2 m everywhere",
        "",
        "| Stack | Floor | Roof | Max pitch, full coverage |",
        "|---:|---:|---:|---:|",
    ]
    for p in result["pitches"]:
        mark = "" if p["max_pitch_full_deg"] > 0 else " **none**"
        lines.append(
            f"| {p['stack_mm']:.0f} | {p['floor_mm']:.0f} | {p['roof_mm']:.0f} | "
            f"{p['max_pitch_full_deg']:.1f}°{mark} |"
        )
    worst = min(result["pitches"], key=lambda p: p["max_pitch_full_deg"])
    best = max(result["pitches"], key=lambda p: p["max_pitch_full_deg"])
    lines += [
        "",
        f"The range runs from **{best['max_pitch_full_deg']:.1f}°** in the most favourable "
        f"combination to **{worst['max_pitch_full_deg']:.1f}°** in the least. Note what that means "
        "for the gable intent in the reference images: **a 20° roof cannot deliver 2.2 m over the "
        "full width under a 4.00 m transport limit with a realistic envelope**, and it is not close.",
        "",
        "## 4. What would have to give at the reference case",
        "",
        f"Reference: **{ref['pitch_deg']:.0f}°**, **{ref['stack_mm']:.0f} mm** stack, "
        f"**{ref['floor_mm']:.0f} mm** floor, **{ref['roof_mm']:.0f} mm** roof.",
        "",
        f"Result: max wall **{ref['max_wall_mm']:.0f} mm** and coverage **{ref['coverage']:.0%}**. "
        f"That means a strip about **{2 * HALF_WIDTH_MM * ref['coverage']:.0f} mm wide** along the "
        "ridge reaches 2.2 m, in a cabin whose internal width is about 2470 mm. §12-7(2)(d) does "
        "permit parts of a room to be lower, so this is not automatically a breach — but a 720 mm "
        "band is not a design, it is a technicality.",
        "",
        "Each lever, moved on its own until full coverage is reached:",
        "",
        "| Lever | Reference | Value needed | Change |",
        "|---|---:|---:|---:|",
    ]

    def lever_row(label, ref_value, needed, unit, dec=0):
        if needed <= 0:
            return (f"| {label} | {ref_value:.{dec}f} {unit} | **not achievable** | "
                    "even zero would not reach it |")
        return (f"| {label} | {ref_value:.{dec}f} {unit} | **{needed:.{dec}f} {unit}** | "
                f"{needed - ref_value:+.{dec}f} {unit} |")

    lines += [
        lever_row("Transport stack", ref["stack_mm"], L["stack_for_full_coverage"], "mm"),
        lever_row("Floor build-up", ref["floor_mm"], L["floor_for_full_coverage"], "mm"),
        lever_row("Roof build-up", ref["roof_mm"], L["roof_for_full_coverage"], "mm"),
        lever_row("Transport limit", 4000.0, L["limit_for_full_coverage"], "mm"),
        lever_row("Pitch", ref["pitch_deg"], L["pitch_for_full_coverage"], "°", dec=1),
    ]

    closed = [name for name, value in (
        ("floor build-up", L["floor_for_full_coverage"]),
        ("roof build-up", L["roof_for_full_coverage"]),
    ) if value <= 0]
    lines += [""]
    if closed:
        lines += [
            f"**Two of the five levers do not exist at this reference case.** The required "
            f"{' and the '.join(closed)} come out **negative**, which means that even a build-up of "
            "zero would not deliver full coverage. Those are not tight constraints, they are closed "
            "doors — and the envelope is already at the §14-3 minimum, so it is not available as a "
            "way out.",
            "",
        ]
    lines += [
        "Read the table as a map of the trade, not a list of recommendations. What is actually left:",
        "",
        "- **The stack is the cheapest lever and the least discussed.** It is a property of the "
        "trailer and the supports, not of the cabin, and it is negotiated with a carrier (C-06). "
        "Dropping it buys wall height one for one — but it has to fall by more than a third, which "
        "is a conversation with the carrier, not a rounding.",
        "- **The roof build-up cannot be reduced**, because it is where the §14-3 insulation and the "
        "§11-4(3) no. 6 fire constraint both land. That lever is already spent.",
        "- **The transport limit is a permit question, not a design one.** A dispensation above "
        "4.00 m exists in principle (S009, VegSak) but turns every move into an application — which "
        "for a cabin that moves repeatedly is a different project.",
        "- **Reducing the pitch is the only lever that stays inside the design**, because it "
        "relieves both the ridge rise and the t/cos θ term at once. The cost is architectural: the "
        "gable in the reference images becomes shallow, and the roof-space volume that a sleeping "
        "loft would use disappears.",
        "",
        "## 5. The floor-area penalty nobody has costed yet",
        "",
        f"A {internal['wall_build_mm']:.0f} mm wall build-up takes **{internal['wall_build_mm'] * 2:.0f} mm** "
        f"off each dimension. The internal floor becomes **{internal['width_m']:.2f} × "
        f"{internal['length_m']:.2f} m = {internal['area_m2']:.2f} m²** against a gross "
        f"**{internal['gross_area_m2']:.1f} m²** — a loss of **{internal['loss_m2']:.1f} m²**, or "
        f"**{internal['loss_m2'] / internal['gross_area_m2']:.0%}** of the building.",
        "",
        "That is the same 189 mm of mineral wool that §14-3 demands, arriving as a spatial cost. It "
        "still fits the ≤30 m² mikrohus route with room to spare, so it is not a compliance problem; "
        "it is a liveability problem, and at 18 m² gross there is not much to give away.",
        "",
        "## 6. What this changes",
        "",
        "1. **The 20° gable and full-width 2.2 m are mutually exclusive under 4.00 m** with a "
        "realistic envelope. The design has to choose: shallower pitch, partial coverage, a lower "
        "stack, or a dispensation.",
        "2. **The earlier room-height screen was optimistic**, not wrong: it answered the question "
        "it was asked, with the roof treated as a line and the floor at 150 mm. Both assumptions "
        "have now been replaced by values the other screens produced.",
        "3. **C-02 now has a sharper question attached to it.** It is no longer \"what is the floor "
        "build-up\" but \"what is the floor build-up, the roof build-up and the trailer stack, "
        "together\" — because the three only make sense as a set.",
        "4. **Nothing here selects a pitch.** The tables are a map of the trade, not a decision.",
        "",
        "## 7. Limits",
        "",
        "- **Parametric only.** No geometry is frozen, no material is selected and no member is "
        "sized. The build-ups are round numbers bracketing what the envelope screen implies.",
        "- **The transport limit is a screening value**, not a route permit. The real constraint is "
        "the vegliste for the actual route (C-03), which is unknown.",
        "- **The definition of the stack matters and must be confirmed with the carrier.** It is "
        "taken here as everything below the chassis top — chassis depth, trailer deck and supports. "
        "If a carrier quotes a deck height that excludes the chassis, the real stack is ~250 mm "
        "larger and every result in this report gets worse, not better.",
        "- **No allowance for salients**, roof overhangs, chimney, vents, lifting ears or the "
        "trailer's own structure above deck. Each of those consumes height and none is modelled.",
        "- **Free height is measured to the underside of the roof plane**, ignoring any ceiling "
        "lining, tie beams, collar ties or services in the roof space. A structural roof will lose "
        "more height than this.",
        "- Nothing here is a compliance certificate or a fabrication release.",
        "",
        "## 8. Source and status",
        "",
        "- §12-7(2)(c) 2.2 m: S025. §14-3 U-values: S011. §11-4(3) no. 6 roof: S024.",
        "- Transport screening value 4.00 m: S022. Dispensation route: S009.",
        "- Generated by `scripts/section_feasibility.py`; JSON companion: "
        "`knowledge/comparisons/section-feasibility.json`.",
        "- SCREENING ONLY — no pitch, no build-up, no geometry fixed.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # At zero pitch and zero build-ups, the wall gets the whole budget.
    assert abs(max_wall_height(0.0, 1000.0, 0.0, 0.0) - 3000.0) < 1e-6
    # The roof thickness costs t/cos(theta), not t.
    assert abs(ridge_top(2000.0, 0.0, 0.0, 300.0) - 2300.0) < 1e-6
    assert abs(ridge_top(2000.0, 60.0, 0.0, 300.0)
               - (2000.0 + 1500.0 * math.tan(math.radians(60.0)) + 600.0)) < 1e-6
    # Transport identity closes.
    h = max_wall_height(15.0, 1000.0, 250.0, 300.0)
    assert abs(transport_height(h, 15.0, 1000.0, 250.0, 300.0) - 4000.0) < 1e-6
    # Coverage is full when the wall already reaches the target, zero at the wall otherwise.
    assert coverage(2300.0, 20.0) == 1.0
    assert coverage(1200.0, 20.0) == 0.0
    # Monotone: a steeper pitch always lowers the permissible wall.
    assert max_wall_height(20.0, 1100.0, 250.0, 300.0) < max_wall_height(10.0, 1100.0, 250.0, 300.0)
    # A taller stack always lowers it.
    assert max_wall_height(20.0, 1100.0, 250.0, 300.0) < max_wall_height(20.0, 900.0, 250.0, 300.0)
    # The pitch cap is the angle at which the wall exactly reaches the target.
    cap = max_pitch_full_coverage(1100.0, 250.0, 300.0)
    assert 0.0 < cap < 60.0
    assert abs(max_wall_height(cap, 1100.0, 250.0, 300.0) - TARGET_FREE_MM) < 0.5
    # The reference case is partial, not full: that is the finding.
    h_ref = max_wall_height(REF_PITCH, REF_STACK, REF_FLOOR, REF_ROOF)
    assert h_ref < TARGET_FREE_MM
    assert coverage(max(h_ref, 0.0), REF_PITCH) < 0.5
    # Every lever, solved, actually restores full coverage.
    assert abs(max_wall_height(REF_PITCH, max_stack_full_coverage(REF_PITCH, REF_FLOOR, REF_ROOF),
                               REF_FLOOR, REF_ROOF) - TARGET_FREE_MM) < 0.5
    assert abs(max_wall_height(REF_PITCH, REF_STACK,
                               max_floor_full_coverage(REF_PITCH, REF_STACK, REF_ROOF),
                               REF_ROOF) - TARGET_FREE_MM) < 0.5
    assert abs(max_wall_height(REF_PITCH, REF_STACK, REF_FLOOR,
                               max_roof_full_coverage(REF_PITCH, REF_STACK, REF_FLOOR))
               - TARGET_FREE_MM) < 0.5
    # The internal area is smaller than the gross area, by the wall on both sides.
    w, l, area = internal_area()
    assert area < 18.0 and w < 3.0 and l < 6.0
    result = screen()
    assert len(result["rows"]) == len(PITCHES) * len(STACKS) * len(FLOOR_BUILDS) * len(ROOF_BUILDS)
    assert len(result["pitches"]) == len(STACKS) * len(FLOOR_BUILDS) * len(ROOF_BUILDS)
    print("Section self-test OK: ridge geometry, t/cos theta, transport identity, monotonicity, "
          "pitch cap, lever inversion and floor-area penalty all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    result = screen()
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
