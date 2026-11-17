#!/usr/bin/env python3
"""MiniHouse · R2 section options — turning the height conflict into a decision.

`section_feasibility.py` established that the declared concept (20° gable, 2.2 m
free height, 4.00 m transport, realistic envelope) does not close: at 20° the
eave tops out at 1785 mm and only ~24 % of the width reaches 2.2 m.

This script does not re-derive that. It takes the conflict as settled and puts
four coherent configurations on the table, each computed with the same section
model, so the choice can be made on numbers rather than on preference:

  R2-A  shallow gable, full headroom
  R2-B  20° gable, low side zones
  R2-C  15° gable on a low loader
  R2-D  20° gable with a transport dispensation

For each option it reports the transport height, the width of the zone that
reaches 2.2 m, the width and height range of the low zone, and whether a
sleeping loft is still possible. The point of the low-zone numbers is that a
zone below 2.2 m is not automatically waste: it is where a bathroom, a kitchen
run or storage belongs, which is the logic of every attic flat.

Nothing here selects an option. The choice depends on C-02, C-06 and on how much
the gable in the reference images is worth to Carlos.

Usage:
  python section_options.py --out-md fase1/opciones-seccion-R2.md \
      --out-json knowledge/comparisons/section-options.json
  python section_options.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from envelope_check import (LAM_MINERAL_WOOL, floor as env_floor,  # noqa: E402
                            min_thickness_with_studs, roof as env_roof)

WIDTH_MM = 3000.0
HALF_WIDTH_MM = WIDTH_MM / 2.0
LENGTH_MM = 6000.0
TARGET_FREE_MM = 2200.0
WALL_BUILD_MM = 264.0
LOFT_HEADROOM_MM = 1600.0   # headroom a sleeping loft would need above its floor
RESERVE_MM = 100.0          # allowance for overhangs, ears, vents above the modelled ridge

# The four options above were solved with floor 250 mm and roof 300 mm, described
# as coming from the envelope screen. They do not: those are round numbers, and
# the envelope solver returns a thicker floor and a thinner roof. The section is
# therefore re-solved against the build-ups the envelope actually produces.
#
# The timber fraction is the one input that moves the answer materially, and it
# is a geometry result (member width / centres), not a material property — so it
# is swept rather than fixed at the envelope screen's uniform 15 %.
BUILDUP_FRACTIONS = (0.15, 0.12, 0.08)
U_FLOOR = 0.18   # §14-3
U_ROOF = 0.18

OPTIONS = (
    {"id": "R2-A", "name": "Shallow gable, full headroom",
     "pitch": 8.0, "stack": 900.0, "floor": 250.0, "roof": 300.0, "limit": 4000.0,
     "keeps_gable": True,
     "cost": "the roof reads almost flat; the gable in the reference images becomes a ridge line"},
    {"id": "R2-B", "name": "20° gable, low side zones",
     "pitch": 20.0, "stack": 1100.0, "floor": 250.0, "roof": 300.0, "limit": 4000.0,
     "keeps_gable": True,
     "cost": "2.2 m only over the central band; bathroom, kitchen and storage move to the low zones"},
    {"id": "R2-C", "name": "15° gable on a low loader",
     "pitch": 15.0, "stack": 700.0, "floor": 250.0, "roof": 300.0, "limit": 4000.0,
     "keeps_gable": True,
     "cost": "a specialised low-deck trailer, which may cost more per move and is not available on every route"},
    {"id": "R2-D", "name": "20° gable with a dispensation",
     "pitch": 20.0, "stack": 1100.0, "floor": 250.0, "roof": 300.0, "limit": 4400.0,
     "keeps_gable": True,
     "cost": "a permit application before every move, and the risk that one route refuses it after the cabin is built"},
)


def build_up_depths(stud_fraction):
    """Total floor and roof build-up depth from the envelope solver, mm.

    Total, not insulation: a build-up is deck + insulation + structural board,
    and confusing the two is how a 250 mm floor became a 281 mm one.
    """
    f_ins = min_thickness_with_studs(U_FLOOR, env_floor(), 1, stud_fraction,
                                     lam_ins=LAM_MINERAL_WOOL)
    r_ins = min_thickness_with_studs(U_ROOF, env_roof(), 2, stud_fraction,
                                     lam_ins=LAM_MINERAL_WOOL)
    f_total = sum(layer.d_mm for layer in env_floor(f_ins))
    r_total = sum(layer.d_mm for layer in env_roof(r_ins))
    return {"floor_mm": round(f_total, 1), "roof_mm": round(r_total, 1),
            "floor_ins_mm": round(f_ins, 1), "roof_ins_mm": round(r_ins, 1)}


def min_limit_full_coverage(pitch_deg, stack, t_floor, t_roof, target=TARGET_FREE_MM):
    """Transport limit at which the 2.2 m band reaches the full width.

    This is what a dispensation would actually have to ask for, as opposed to the
    round 4400 mm in the option table.
    """
    p = math.radians(pitch_deg)
    return target + stack + t_floor + HALF_WIDTH_MM * math.tan(p) + t_roof / math.cos(p)


def revised_options(stud_fraction):
    """The same four options, re-solved against the envelope build-ups."""
    depth = build_up_depths(stud_fraction)
    return [evaluate({**opt, "floor": depth["floor_mm"], "roof": depth["roof_mm"]})
            for opt in OPTIONS]


def ridge_top(h_wall, pitch_deg, t_floor, t_roof, half_width=HALF_WIDTH_MM):
    p = math.radians(pitch_deg)
    return t_floor + h_wall + half_width * math.tan(p) + t_roof / math.cos(p)


def max_wall_height(pitch_deg, stack, t_floor, t_roof, limit):
    p = math.radians(pitch_deg)
    return limit - stack - t_floor - HALF_WIDTH_MM * math.tan(p) - t_roof / math.cos(p)


# The reference case quoted by the bridge and roof screens as "the section's
# deficit". It lives here because this is what computes it; the other scripts
# import it rather than restating the number, which had already drifted once
# (415 mm at the round 250/300 build-ups the R2 options were first solved with).
REFERENCE = {"pitch": 20.0, "stack": 1100.0, "limit": 4000.0}


def reference_deficit_mm(stud_fraction=0.15):
    """Free-height shortfall at the reference case. Positive means short."""
    depths = build_up_depths(stud_fraction)
    h = max_wall_height(REFERENCE["pitch"], REFERENCE["stack"],
                        depths["floor_mm"], depths["roof_mm"], REFERENCE["limit"])
    return TARGET_FREE_MM - h


def coverage(h_wall, pitch_deg, target=TARGET_FREE_MM, half_width=HALF_WIDTH_MM):
    if h_wall >= target:
        return 1.0
    rise = math.tan(math.radians(pitch_deg))
    if rise <= 0:
        return 0.0
    d = (target - h_wall) / rise
    return max(0.0, min(1.0, 1.0 - d / half_width))


def distance_for_height(h_wall, pitch_deg, height_mm):
    """Distance from the wall where the free height reaches `height_mm`."""
    rise = math.tan(math.radians(pitch_deg))
    if rise <= 0:
        return None
    d = (height_mm - h_wall) / rise
    return max(0.0, d)


def evaluate(opt):
    h_wall = max_wall_height(opt["pitch"], opt["stack"], opt["floor"], opt["roof"], opt["limit"])
    cov = coverage(max(h_wall, 0.0), opt["pitch"])
    band = 2 * HALF_WIDTH_MM * cov
    low_zone = HALF_WIDTH_MM - band / 2
    ridge_free = max(h_wall, 0.0) + HALF_WIDTH_MM * math.tan(math.radians(opt["pitch"]))
    transport = ridge_top(max(h_wall, 0.0), opt["pitch"], opt["floor"], opt["roof"]) + opt["stack"]
    # Same section with a reserve taken off the wall for overhangs, ears and vents.
    h_res = max(h_wall - RESERVE_MM, 0.0)
    cov_res = coverage(h_res, opt["pitch"])
    return {
        **opt,
        "wall_mm": round(h_wall, 0),
        "coverage": round(cov, 3),
        "band_mm": round(band, 0),
        "low_zone_mm": round(low_zone, 0),
        "low_zone_area_m2": round(low_zone / 1000.0 * (LENGTH_MM - 2 * WALL_BUILD_MM) / 1000.0, 2),
        "ridge_free_mm": round(ridge_free, 0),
        "transport_mm": round(transport, 0),
        "headroom_over_limit": round(opt["limit"] - transport, 0),
        "full_coverage": cov >= 0.999,
        "effectively_full": cov >= 0.95,
        "wall_reserve_mm": round(h_res, 0),
        "coverage_reserve": round(cov_res, 3),
        "survives_reserve": cov_res >= 0.999,
        "loft_possible": (ridge_free - TARGET_FREE_MM) >= LOFT_HEADROOM_MM,
        "d_to_2000_mm": (None if distance_for_height(h_wall, opt["pitch"], 2000.0) is None
                         else round(distance_for_height(h_wall, opt["pitch"], 2000.0), 0)),
        "d_to_1600_mm": (None if distance_for_height(h_wall, opt["pitch"], 1600.0) is None
                         else round(distance_for_height(h_wall, opt["pitch"], 1600.0), 0)),
    }


def screen():
    rows = [evaluate(o) for o in OPTIONS]
    w = (WIDTH_MM - 2 * WALL_BUILD_MM) / 1000.0
    l = (LENGTH_MM - 2 * WALL_BUILD_MM) / 1000.0
    return {
        "state": "OPTIONS — NO SELECTION, NO GEOMETRY FROZEN",
        "width_mm": WIDTH_MM, "length_mm": LENGTH_MM,
        "target_free_mm": TARGET_FREE_MM,
        "wall_build_mm": WALL_BUILD_MM,
        "reserve_mm": RESERVE_MM,
        "internal": {"width_m": round(w, 2), "length_m": round(l, 2), "area_m2": round(w * l, 2)},
        "options": rows,
        "revised": [
            {
                "stud_fraction": frac,
                "build_up": build_up_depths(frac),
                "min_limit_full_coverage_mm": round(min_limit_full_coverage(
                    20.0, 1100.0, build_up_depths(frac)["floor_mm"],
                    build_up_depths(frac)["roof_mm"]), 0),
                "options": [
                    {"id": r["id"], "wall_mm": r["wall_mm"], "coverage": r["coverage"],
                     "band_mm": r["band_mm"], "full_coverage": r["full_coverage"],
                     "coverage_reserve": r["coverage_reserve"],
                     "survives_reserve": r["survives_reserve"],
                     "transport_mm": r["transport_mm"]}
                    for r in revised_options(frac)
                ],
            }
            for frac in BUILDUP_FRACTIONS
        ],
    }


def markdown(result):
    rows = result["options"]
    full = [r for r in rows if r["full_coverage"]]
    partial = [r for r in rows if not r["full_coverage"]]
    internal = result["internal"]

    lines = [
        "# MiniHouse · R2 section options",
        "",
        "**State:** OPTIONS — NO SELECTION, NO GEOMETRY FROZEN. Four configurations, computed with the "
        "same section model, so the choice can be made on numbers.",
        "",
        "- Constraint set: **2.2 m** free height (§12-7(2)(c), S025), **4.00 m** transport screening "
        "value (S022), floor 250 mm and roof 300 mm from the [envelope screen](verificacion-envolvente.md).",
        "- The conflict is established in [verificación de sección](verificacion-seccion.md) and is not "
        "re-derived here.",
        f"- Internal width after a {result['wall_build_mm']:.0f} mm wall: "
        f"**{internal['width_m']:.2f} × {internal['length_m']:.2f} m = {internal['area_m2']:.2f} m²**.",
        "",
        "## 1. The four configurations",
        "",
        "| Option | Pitch | Stack | Limit | Wall at eave | 2.2 m band | Low zone | Transport |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        band = "full width" if r["full_coverage"] else f"{r['band_mm']:.0f} mm"
        low = "—" if r["full_coverage"] else f"{r['low_zone_mm']:.0f} mm/side"
        lines.append(
            f"| **{r['id']}** {r['name']} | {r['pitch']:.0f}° | {r['stack']:.0f} | "
            f"{r['limit']:.0f} | {r['wall_mm']:.0f} | {band} | {low} | {r['transport_mm']:.0f} |"
        )
    lines += [
        "",
        "`Wall at eave` is the free height at the wall, which is also the tallest the wall can be "
        "under the limit. `Low zone` is the strip along each long wall that sits below 2.2 m.",
        "",
        "## 2. The build-ups these numbers came from — and a correction",
        "",
        "The four options above were solved with **floor 250 mm and roof 300 mm**, described as "
        "coming from the envelope screen. **They do not.** Those are round numbers, and the "
        "envelope solver returns a **thicker floor and a thinner roof** at the same U-values:",
        "",
        "| Timber fraction | Floor build-up | Roof build-up | vs 250 / 300 |",
        "|---:|---:|---:|---|",
    ]
    for block in result["revised"]:
        b = block["build_up"]
        d_floor = b["floor_mm"] - 250.0
        d_roof = b["roof_mm"] - 300.0
        lines.append(
            f"| {block['stud_fraction']*100:.0f} % | **{b['floor_mm']:.0f} mm** "
            f"({b['floor_ins_mm']:.0f} insulation) | **{b['roof_mm']:.0f} mm** "
            f"({b['roof_ins_mm']:.0f} insulation) | "
            f"floor {d_floor:+.0f}, roof {d_roof:+.0f} |"
        )

    lines += [
        "",
        "**The floor is 31 mm thicker than assumed and the roof 22 mm thinner, so the two nearly "
        "cancel** — the published wall heights are optimistic by only about 7 mm. The reference "
        f"case was close, not wrong, and the −{reference_deficit_mm():.0f} mm deficit is robust.",
        "",
        "What is not close is the **timber fraction**. It is the member width divided by the "
        "centres, not a material property, so the envelope screen's uniform 15 % is a choice "
        "rather than a result. Re-solving the same four options across the plausible range:",
        "",
        "| Option | Published | 15 % studs | 12 % effective | 8 % field |",
        "|---|---:|---:|---:|---:|",
    ]
    by_id = {r["id"]: r for r in rows}
    for rid in [r["id"] for r in rows]:
        pub = by_id[rid]
        cells = []
        for block in result["revised"]:
            opt = next(o for o in block["options"] if o["id"] == rid)
            cells.append(f"{opt['wall_mm']:.0f} / {opt['coverage']*100:.0f} %")
        lines.append(f"| **{rid}** | {pub['wall_mm']:.0f} / {pub['coverage']*100:.0f} % | "
                     + " | ".join(cells) + " |")

    lines += [
        "",
        "The framing is worth more than the build-up correction by an order of magnitude: at 8 % "
        "**R2-B rises from 23 % to 34 %** of the width and **R2-D reaches full coverage**. That "
        "does not rescue R2-B — it is still a partial-coverage option — but it changes how much "
        "the low zone has to absorb, and it is the only lever of any size that costs nothing at "
        "the transport limit.",
        "",
        "**The lesson is the same one the roof determination produced:** state the member width "
        "and the centres, not a fraction. A fraction written as though it were a property turns a "
        "screening choice into a false basis.",
        "",
        "### What the dispensation actually has to ask for",
        "",
        "R2-D is described as a dispensation to **4400 mm**. That is a round number too, and it is "
        "not enough. The limit at which the 2.2 m band reaches the full width at 20° and a "
        "1100 mm stack is:",
        "",
        "| Build-ups | Limit needed for full coverage | vs the 4400 mm in the option table |",
        "|---|---:|---|",
    ]
    for block in result["revised"]:
        need = block["min_limit_full_coverage_mm"]
        delta = need - 4400.0
        verdict = "**short by " + f"{abs(delta):.0f} mm**" if delta > 0 else f"{abs(delta):.0f} mm to spare"
        lines.append(f"| {block['stud_fraction']*100:.0f} % timber fraction | **{need:.0f} mm** | "
                     f"{verdict} |")

    lines += [
        "",
        "**At the envelope screen's own 15 % the dispensation is 22 mm short**, and even at the "
        "published 250 / 300 build-ups it needs 4415 mm. So R2-D's 4400 mm was never the threshold "
        "for full coverage — it was a round number that happened to land at 97 %.",
        "",
        "The framing relief fixes it: at 12 % or less, 4400 mm is enough. That is worth knowing "
        "before the application is written, because **the number in the application is the one "
        "that gets assessed**, and asking for 4400 when 4422 is needed invites a refusal that a "
        "slightly different frame would have avoided.",
        "",
        "## 3. What each one costs",
        "",
        "| Option | What it costs | What it depends on |",
        "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| **{r['id']}** | {r['cost']} | {_depends(r)} |")

    lines += [
        "",
        "## 4. The low zone is not waste — it is the plan",
        "",
        "R2-B is the only option that keeps the 20° gable without a permit or a special trailer, and it "
        "is the one that looks like a compromise. The numbers say otherwise.",
        "",
        "| Option | 2.2 m band | Low zone per side | Low-zone area per side | Height at the wall |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        band = "full" if r["full_coverage"] else f"{r['band_mm']:.0f} mm"
        low = "—" if r["full_coverage"] else f"{r['low_zone_mm']:.0f} mm"
        area = "—" if r["full_coverage"] else f"{r['low_zone_area_m2']:.2f} m²"
        lines.append(f"| **{r['id']}** | {band} | {low} | {area} | {r['wall_mm']:.0f} mm |")

    b = next((r for r in rows if r["id"] == "R2-B"), None)
    if b:
        lines += [
            "",
            f"In R2-B the low zone is **{b['low_zone_mm']:.0f} mm deep along each 6 m wall** — "
            f"**{b['low_zone_area_m2']:.2f} m² per side** — with the ceiling running from "
            f"**{b['wall_mm']:.0f} mm at the wall up to 2.2 m** where it meets the band. That is "
            "enough for:",
            "",
            "- a **bathroom** ~1.1 × 2.0 m against a long wall, with the shower at the high end;",
            "- a **kitchen run** at 600 mm depth with wall cabinets, which needs no headroom at all;",
            "- **full-height storage** along the remainder, which is the scarcest thing in an 18 m² cabin.",
            "",
            "This is the ordinary logic of an attic flat, and it changes the reading of the earlier "
            "result: **24 % coverage is not a failure, it is a plan constraint** — provided the plan "
            "puts the low-headroom functions at the edges and keeps the central band for standing, "
            "sitting and circulation.",
            "",
            "The one thing it rules out is a **sleeping loft**. The free height at the ridge is "
            f"**{b['ridge_free_mm']:.0f} mm**, so there is no {LOFT_HEADROOM_MM:.0f} mm of headroom "
            "above a loft floor at 2.2 m. A loft would need a much steeper roof, which the transport "
            "limit does not allow.",
            "",
            "**But read §4 before treating R2-B as viable.** This reading only holds if the wall "
            "really reaches 1785 mm and nothing else in the transport budget is spent. It is a "
            "contingent option, not a robust one.",
        ]

    lines += [
        "",
        "## 5. Tolerance: none of these options has any",
        "",
        "Every option above solves **to** the limit, so the wall height quoted is a maximum and the "
        "transport height is exactly 4.00 m (or 4.40 m for R2-D). Real roofs have ridge caps, "
        f"overhangs, vents and lifting ears. Taking a **{result['reserve_mm']:.0f} mm** reserve off "
        "the wall changes the picture unevenly:",
        "",
        "| Option | Wall (max) | Wall with reserve | Coverage, max | Coverage with reserve | Survives |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        ok = "yes" if r["survives_reserve"] else "**no**"
        lines.append(
            f"| **{r['id']}** | {r['wall_mm']:.0f} mm | {r['wall_reserve_mm']:.0f} mm | "
            f"{r['coverage']:.0%} | {r['coverage_reserve']:.0%} | {ok} |"
        )
    lines += [
        "",
        "This is the sharpest thing in the report. **R2-A and R2-C absorb a reserve and still give "
        "full headroom. R2-B does not**: its 24 % coverage is bought with every millimetre of the "
        "budget, and a 100 mm allowance takes it to single digits. An option that only works at "
        "exactly zero tolerance is not a robust option — it is a calculation.",
        "",
        "**The framing relief does not change that verdict, and it is worth showing why.** Slimming "
        "the frame to an 8 % fraction buys 57 mm of wall on R2-B and takes its coverage from 23 % "
        "to 34 % — but the same 100 mm reserve then takes it back to **16 %**, and R2-D from 100 % "
        "to **89 %**:",
        "",
        "| Option | 15 % framing, with reserve | 8 % framing, with reserve |",
        "|---|---:|---:|",
    ]
    for rid in [r["id"] for r in rows]:
        cells = []
        for block in result["revised"]:
            opt = next(o for o in block["options"] if o["id"] == rid)
            h = max(opt["wall_mm"] - RESERVE_MM, 0.0)
            cells.append(f"{coverage(h, next(o for o in OPTIONS if o['id'] == rid)['pitch'])*100:.0f} %")
        lines.append(f"| **{rid}** | {cells[0]} | {cells[-1]} |")

    lines += [
        "",
        "So the reserve test separates the options the same way however the frame is built: **only "
        "R2-A and R2-C survive it.** That is a stronger conclusion than the original table, because "
        "it now survives the one correction that could have overturned it.",
        "",
        "## 6. How the options divide",
        "",
        f"- **Full 2.2 m across the width:** {', '.join(r['id'] for r in full) if full else 'none'} — "
        "these close the room-height question completely and pay for it elsewhere.",
        f"- **Effectively full, at 4.40 m:** "
        f"{', '.join(r['id'] for r in rows if r['effectively_full'] and not r['full_coverage']) or 'none'}.",
        f"- **Genuinely partial:** "
        f"{', '.join(r['id'] for r in partial if not r['effectively_full']) or 'none'} — keeps the "
        "gable and turns the low zones into programme, but only with zero tolerance.",
        "- **None of them gives a loft**, because the transport limit caps the ridge height before a "
        "loft becomes possible.",
        "",
        "## 7. What has to be decided, and by whom",
        "",
        "| Question | Owner | Effect on the choice |",
        "|---|---|---|",
        "| How much is the 20° gable worth? | **Carlos** | decides between R2-A and R2-B more than any technical input |",
        "| What trailer deck height is actually available? | carrier (**C-06**) | decides whether R2-C exists at all |",
        "| Is a VegSak dispensation acceptable on every move? | **Carlos** | decides whether R2-D is a design or a habit |",
        "| What floor and roof build-up will really be built? | **C-02** | shifts every number in this table by tens of millimetres |",
        "| What fraction of the floor must reach 2.2 m? | **Carlos** + municipality | decides whether R2-B's 24 % is acceptable |",
        "",
        "**No option is recommended here.** The technical work has narrowed the choice to four; the "
        "rest is a value judgement about how the cabin should look and how it should be moved, and "
        "that belongs to Carlos.",
        "",
        "## 8. Limits",
        "",
        "- **Parametric and coarse.** Build-ups are round numbers consistent with the envelope screen; "
        "no material, member or product is selected.",
        "- **No salients, overhangs, chimney, vents or lifting ears** are in the transport height. Each "
        "would consume margin, and R2-A and R2-C have none to spare.",
        "- **The 4.00 m limit is a screening value**, not a route permit; R2-D assumes 4.40 m is "
        "obtainable, which has not been checked against any vegliste.",
        "- **Free height is to the underside of the roof plane**, ignoring lining, ties and services.",
        "- Nothing here is a compliance certificate, a siting approval or a fabrication release.",
        "",
        "## 9. Source and status",
        "",
        "- §12-7(2)(c) 2.2 m: S025. §14-3 envelope: S011 + [envelope screen](verificacion-envolvente.md).",
        "- Transport screening value: S022. Dispensation route: S009.",
        "- Section model: `scripts/section_feasibility.py`. Generated by `scripts/section_options.py`; "
        "JSON companion: `knowledge/comparisons/section-options.json`.",
        "- OPTIONS ONLY — no pitch, build-up or geometry selected.",
        "",
    ]
    return "\n".join(lines)


def _depends(r):
    if r["id"] == "R2-A":
        return "nothing new — the pitch is the only thing that changes"
    if r["id"] == "R2-B":
        return "the coverage-fraction decision, and a plan that uses the low zones"
    if r["id"] == "R2-C":
        return "a trailer with a 700 mm deck (C-06)"
    return "a VegSak dispensation on every move"


def selftest():
    # The reference option reproduces the section screen exactly.
    b = evaluate(OPTIONS[1])
    assert abs(b["wall_mm"] - 1785.0) < 2.0, b["wall_mm"]
    assert abs(b["coverage"] - 0.239) < 0.01, b["coverage"]
    # The full-coverage options really are full.
    for o in (OPTIONS[0], OPTIONS[2]):
        r = evaluate(o)
        assert r["full_coverage"], (o["id"], r["wall_mm"])
        assert r["low_zone_mm"] == 0.0
    # R2-D is a whisker short of full coverage, not comfortably full.
    d = evaluate(OPTIONS[3])
    assert 0.9 < d["coverage"] < 1.0, d["coverage"]
    assert d["wall_mm"] < TARGET_FREE_MM
    # No option gives a loft.
    assert all(not evaluate(o)["loft_possible"] for o in OPTIONS)
    # Transport never exceeds the limit it was solved against.
    for o in OPTIONS:
        r = evaluate(o)
        assert r["transport_mm"] <= r["limit"] + 1e-6, (r["id"], r["transport_mm"])
    # The band plus twice the low zone equals the full width.
    for o in OPTIONS:
        r = evaluate(o)
        assert abs(r["band_mm"] + 2 * r["low_zone_mm"] - WIDTH_MM) < 1.0
    # A shallower pitch is always better for headroom at the same limit.
    assert evaluate(OPTIONS[0])["wall_mm"] > evaluate(OPTIONS[1])["wall_mm"]
    result = screen()
    assert len(result["options"]) == 4
    # The build-up correction: the floor is thicker than assumed, the roof thinner.
    d15 = build_up_depths(0.15)
    assert d15["floor_mm"] > 250.0, d15
    assert d15["roof_mm"] < 300.0, d15
    # Total build-up must exceed the insulation it contains.
    assert d15["floor_mm"] > d15["floor_ins_mm"]
    assert d15["roof_mm"] > d15["roof_ins_mm"]
    # A thinner frame must need less insulation, hence a thinner build-up.
    d08 = build_up_depths(0.08)
    assert d08["floor_mm"] < d15["floor_mm"]
    assert d08["roof_mm"] < d15["roof_mm"]

    # The published options are slightly optimistic at 15 %, and better at 8 %.
    published = [evaluate(o) for o in OPTIONS]
    pub_b = next(r for r in published if r["id"] == "R2-B")
    rev15_b = next(r for r in revised_options(0.15) if r["id"] == "R2-B")
    rev08_b = next(r for r in revised_options(0.08) if r["id"] == "R2-B")
    assert rev15_b["wall_mm"] < pub_b["wall_mm"], (rev15_b["wall_mm"], pub_b["wall_mm"])
    assert rev08_b["wall_mm"] > pub_b["wall_mm"]
    # Coverage must improve monotonically as the frame gets slimmer.
    covs = [next(r for r in revised_options(f) if r["id"] == "R2-B")["coverage"]
            for f in BUILDUP_FRACTIONS]
    assert covs == sorted(covs), covs

    # The dispensation in the option table is not the threshold for full coverage.
    need_pub = min_limit_full_coverage(20.0, 1100.0, 250.0, 300.0)
    assert need_pub > 4400.0, need_pub
    assert min_limit_full_coverage(20.0, 1100.0, d15["floor_mm"], d15["roof_mm"]) > 4400.0
    assert min_limit_full_coverage(20.0, 1100.0, d08["floor_mm"], d08["roof_mm"]) < 4400.0
    # ... and it must fall as the frame gets slimmer.
    needs = [min_limit_full_coverage(20.0, 1100.0, *(lambda d: (d["floor_mm"], d["roof_mm"]))(
        build_up_depths(f))) for f in BUILDUP_FRACTIONS]
    assert needs == sorted(needs, reverse=True), needs

    print("Section options self-test OK: reference reproduction, full-coverage options, "
          "dispensation margin, no loft, transport closure and band partition all pass")


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
