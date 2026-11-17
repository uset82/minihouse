#!/usr/bin/env python3
"""MiniHouse · ventilation under §13-1(1), and the pressure it puts on the envelope.

§13-1(1) requires ventilation that secures satisfactory air quality, adapted to
the room design, the intended use, the pollution and the moisture load. It is
outcome-based: no m³/h schedule is given. On the mikrohus route §13-2's numeric
rates do **not** apply (S020, S023), and the guidance is explicit that
alternative air quantities may be used **but must be documented**. The project
has recorded that sentence four times and has never produced the quantities.

That is the gap this screen closes — and closing it turns up something the
chapter 13 work has not looked at, because it is a pressure problem rather than
a rate problem.

**A mechanical extract in a sealed box does not move air.** It lowers the
pressure until leakage supplies the difference. At the airtightness §14-3
requires — 1.5 h⁻¹ at 50 Pa — a 36.9 m³ cabin leaks about 55 m³/h at 50 Pa, so
an extract of 90 m³/h can only be met by holding the cabin at roughly **106 Pa
of negative pressure**, and a boosted 108 m³/h at about **140 Pa**. Those are
not small numbers: a chimney's natural draught is of the order of 10–20 Pa, so a
wood stove would back-draught; and §13-5's radon barrier is defeated by exactly
this mechanism, because sustained negative pressure pulls soil gas through the
floor.

The figures above are the ones this module computes, not ones typed by hand; the
self-test recomputes them from the constants. The report carries them, and it is
the report that is authoritative if the two ever disagree.

So the ventilation design is not a fan schedule. It is a decision about where
the make-up air comes from — and every answer to that is a hole in the vapour
barrier the junction depends on.

Usage:
  python ventilacion_check.py --out-md fase1/verificacion-ventilacion.md \
      --out-json knowledge/comparisons/ventilacion.json
  python ventilacion_check.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import section_options as so       # noqa: E402

# --- the building, at the R0 reference section -------------------------------
FLOOR_AREA_M2 = 18.0
PLAN_L_MM = 6000.0
PLAN_W_MM = 3000.0

# --- airtightness, §14-3 (S011): the limit, used as the design value ---------
N50_PER_H = 1.5
LEAKAGE_EXPONENT = 0.65     # the usual envelope exponent; stated, not measured
REFERENCE_PRESSURE_PA = 50.0

# --- §13-2's rates, which do not bind but are the regulation's own statement
# of what "satisfactory" looks like for a dwelling (S012). Adopted voluntarily
# as the documented alternative §13-1(1) asks for; never presented as a target.
WHOLE_DWELLING_M3H_PER_M2 = 1.2
BED_PLACE_M3H = 26.0
NON_PERMANENT_M3H_PER_M2 = 0.7
BED_PLACES = 2              # C-01 open: a cabin for two is the stated use

# --- pre-accepted extract volumes, basic / boosted (S012) --------------------
EXTRACT = {
    "kitchen": (36.0, 108.0),
    "bathroom": (54.0, 108.0),
    "toilet": (36.0, 36.0),
    "utility": (36.0, 72.0),
}
# What this cabin actually has: a kitchen run and a bathroom.
EXTRACT_FITTED = ("kitchen", "bathroom")

# A domestic extract fan develops of the order of 50-150 Pa. Above that it
# stalls: the specified flow is simply not delivered, which is a ventilation
# deficit rather than a pressure problem. Stated as a range, not a product.
FAN_AVAILABLE_PA = (50.0, 100.0, 150.0)

# --- the stove ---------------------------------------------------------------
# Combustion air for a small wood stove. Not from the admitted sources: a generic
# building-physics range, stated as an assumption and swept.
STOVE_AIR_M3H = (8.0, 15.0, 25.0)
# A chimney's natural draught, same caveat. The comparison is the point, not the
# exact figure.
FLUE_DRAUGHT_PA = (10.0, 20.0)

# --- the barrier penetrations a ventilation design needs ---------------------
PENETRATIONS = (
    ("cooker-hood extract", "§11-10: own duct, grease filter, EI 15 A2-s1,d0 if not in a shaft"),
    ("bathroom extract", "wet-room extract, ducted outside the barrier"),
    ("make-up air intake", "the one that decides the pressure balance"),
    ("stove combustion air", "direct from outside, below the firebox"),
    ("stove flue", "through the roof; the barrier is interrupted at the ceiling"),
    ("pressure-equalising vent", "only if the design chooses a passive route"),
)


def fmt(value, spec="+.0f"):
    """Format with a typographic minus, so the report matches the declaration.

    The declaration renders this margin as −130 Pa; a report that renders it as
    -130 Pa is the same number in a different glyph, which is exactly how a
    needle goes missing from a guard block.
    """
    return f"{value:{spec}}".replace("-", "−")


def volume_m3():
    """Internal volume at the reference section: plan area × mean height."""
    depths = so.build_up_depths(0.15)
    h_eave = so.max_wall_height(so.REFERENCE["pitch"], so.REFERENCE["stack"],
                                depths["floor_mm"], depths["roof_mm"],
                                so.REFERENCE["limit"])
    rise = (PLAN_W_MM / 2.0) * math.tan(math.radians(so.REFERENCE["pitch"]))
    mean_h = h_eave + rise / 2.0
    return {"eave_mm": round(h_eave, 1), "rise_mm": round(rise, 1),
            "mean_height_mm": round(mean_h, 1),
            "volume_m3": round(FLOOR_AREA_M2 * mean_h / 1000.0, 2)}


def documented_rates():
    """The alternative air quantities §13-1(1) requires to be documented."""
    whole = FLOOR_AREA_M2 * WHOLE_DWELLING_M3H_PER_M2
    beds = BED_PLACES * BED_PLACE_M3H
    basic = sum(EXTRACT[k][0] for k in EXTRACT_FITTED)
    # The boosted column is per room, and the source does not say whether both
    # rooms boost together. Rather than pick, both readings are carried: the
    # system at one room boosted, and both simultaneously. The second is the
    # upper bound and it is the one that exposes the stall.
    boosted_one = max(EXTRACT[k][1] for k in EXTRACT_FITTED)
    boosted_all = sum(EXTRACT[k][1] for k in EXTRACT_FITTED)
    return {
        "whole_dwelling_m3h": round(whole, 1),
        "bed_places_m3h": round(beds, 1),
        "governing_m3h": round(max(whole, beds), 1),
        "extract_basic_m3h": round(basic, 1),
        "extract_boosted_one_m3h": round(boosted_one, 1),
        "extract_boosted_all_m3h": round(boosted_all, 1),
        "basis": "§13-2 rates adopted voluntarily; they do not bind on this route",
        "note": "supply must equal extract in boosted mode (S012); the source does not "
                "say whether both wet rooms boost at once, so both readings are carried",
    }


def pressure_for_flow(flow_m3h, vol):
    """Room pressure needed to draw `flow_m3h` through the envelope's leakage.

    Q = Q50 · (Δp / 50)^n, with Q50 = n50 · V. Inverted for Δp. This is the
    pressure the cabin settles at when the extract has no dedicated make-up.
    """
    q50 = N50_PER_H * vol["volume_m3"]
    if flow_m3h <= 0.0:
        return 0.0
    return REFERENCE_PRESSURE_PA * (flow_m3h / q50) ** (1.0 / LEAKAGE_EXPONENT)


def balance():
    vol = volume_m3()
    rates = documented_rates()
    rows = []
    for label, flow in (("basic", rates["extract_basic_m3h"]),
                        ("boosted, one room", rates["extract_boosted_one_m3h"]),
                        ("boosted, both rooms", rates["extract_boosted_all_m3h"])):
        dp = pressure_for_flow(flow, vol)
        rows.append({"mode": label, "extract_m3h": flow,
                     "leakage_at_50pa_m3h": round(N50_PER_H * vol["volume_m3"], 1),
                     "pressure_pa": round(dp, 1),
                     "deliverable": dp <= max(FAN_AVAILABLE_PA),
                     "supplied_by": "envelope leakage"})
    # What a fan at the top of the range can actually pull through this envelope.
    best_flow = (N50_PER_H * vol["volume_m3"]) * (
        max(FAN_AVAILABLE_PA) / REFERENCE_PRESSURE_PA) ** LEAKAGE_EXPONENT
    return {"volume": vol, "rates": rates, "rows": rows,
            "n50": N50_PER_H, "exponent": LEAKAGE_EXPONENT,
            "fan_available_pa": list(FAN_AVAILABLE_PA),
            "max_deliverable_m3h": round(best_flow, 1)}


def stove_check():
    """Does the room pressure reverse the flue?

    Only pressures the fan can actually hold are used. A flow the fan cannot
    deliver is not a pressure the cabin sits at, so quoting it against the flue
    would overstate the case.
    """
    b = balance()
    deliverable = [r for r in b["rows"] if r["deliverable"]]
    worst = max(r["pressure_pa"] for r in deliverable)
    worst_mode = max(deliverable, key=lambda r: r["pressure_pa"])["mode"]
    out = []
    for air in STOVE_AIR_M3H:
        out.append({"combustion_air_m3h": air,
                    "share_of_basic_extract": round(air / b["rates"]["extract_basic_m3h"], 3)})
    return {"cases": out, "worst_pressure_pa": round(worst, 1),
            "worst_mode": worst_mode,
            "flue_draught_pa": list(FLUE_DRAUGHT_PA),
            "reverses": worst > min(FLUE_DRAUGHT_PA),
            "margin_pa": round(min(FLUE_DRAUGHT_PA) - worst, 1)}


def screen():
    b = balance()
    st = stove_check()
    return {
        "state": "SCREENING — CONDITIONAL ON C-01. Not a ventilation design, not a "
                 "compliance statement, not a mould-risk analysis.",
        "basis": {"sources": ["S011", "S012", "S023"], "floor_area_m2": FLOOR_AREA_M2},
        "balance": b,
        "stove": st,
        "penetrations": [{"item": i, "requirement": r} for i, r in PENETRATIONS],
        "rh_loop": {
            "assumed_by": "verificacion-condensacion-union.md, 50 % RH indoor",
            "direction": "lower indoor RH reduces the required break, so 50 % is conservative",
            "closed": False,
            "why": "closing it needs a dynamic moisture model with the timber buffering, "
                   "which this screen does not attempt",
        },
        "excluded": ["ventilation design", "duct sizing", "mould-risk analysis",
                     "radon measurement", "compliance statement"],
    }


def markdown(model):
    b = model["balance"]
    st = model["stove"]
    v, r = b["volume"], b["rates"]

    L = [
        "# MiniHouse · ventilation under §13-1(1), and the pressure it puts on the envelope",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a ventilation design, not a "
        "compliance statement, not a mould-risk analysis.",
        "",
        f"- Floor area {model['basis']['floor_area_m2']:.0f} m²; internal volume "
        f"**{v['volume_m3']:.1f} m³** at the reference section (eave {v['eave_mm']:.0f} mm, "
        f"ridge {v['eave_mm'] + v['rise_mm']:.0f} mm, mean {v['mean_height_mm']:.0f} mm).",
        f"- Airtightness **{b['n50']:.1f} h⁻¹ at 50 Pa** (§14-3), used as the design value.",
        f"- Leakage exponent **{b['exponent']:.2f}**, stated rather than measured.",
        "- Generated by `scripts/ventilacion_check.py`; JSON companion: "
        "`knowledge/comparisons/ventilacion.json`.",
        "",
        "## 1. Why this screen exists",
        "",
        "§13-1(1) requires ventilation that secures **satisfactory air quality**, adapted to the "
        "room design, the use, the pollution and the moisture load. It gives no number. On the "
        "mikrohus route §13-2's numeric rates do **not** apply, and the guidance is explicit "
        "that alternative air quantities may be used **but must be documented** "
        "([S023](../knowledge/sources/S023.md)).",
        "",
        "The project has recorded that sentence repeatedly and has never produced the "
        "quantities. This is the last requirement in the §2-2(2) list classified as an "
        "**analysis** that had no analysis behind it.",
        "",
        "## 2. The quantities, documented",
        "",
        "The most defensible alternative is not an invented number: it is §13-2's own rates, "
        "adopted voluntarily, because they are the regulation's statement of what satisfactory "
        "means for a dwelling. **They do not bind here** — that distinction is the whole reason "
        "the sentence has to be written down rather than assumed.",
        "",
        "| Quantity | Value | Basis |",
        "|---|---:|---|",
        f"| Whole dwelling | **{r['whole_dwelling_m3h']:.1f} m³/h** | 18 m² × 1.2 m³/h·m² (§13-2) |",
        f"| Bed places | **{r['bed_places_m3h']:.1f} m³/h** | {BED_PLACES} × 26 m³/h |",
        f"| Governing | **{r['governing_m3h']:.1f} m³/h** | the larger of the two |",
        f"| Extract, basic | **{r['extract_basic_m3h']:.1f} m³/h** | kitchen 36 + bathroom 54 |",
        f"| Extract, boosted — one room | **{r['extract_boosted_one_m3h']:.1f} m³/h** | the larger single figure |",
        f"| Extract, boosted — both rooms | **{r['extract_boosted_all_m3h']:.1f} m³/h** | kitchen 108 + bathroom 108 |",
        "",
        "The fitted extract is the kitchen and the bathroom, and those two dominate the "
        "requirement: the pre-accepted volumes are **larger than the whole-dwelling rate**, "
        "which is normal and is why the extract governs the design rather than the supply "
        "figure.",
        "",
        "**The source does not say whether both wet rooms boost simultaneously**, so both "
        "readings are carried rather than one being chosen. The second is the upper bound, and "
        "it is the one that exposes the problem below.",
        "",
        "## 3. The problem the rates hide: a fan in a sealed box does not move air",
        "",
        "A mechanical extract lowers the pressure until the envelope's leakage supplies the "
        "difference. With `Q = Q50 · (Δp/50)^n` and "
        f"`Q50 = {b['n50']:.1f} × {v['volume_m3']:.1f} = {b['rows'][0]['leakage_at_50pa_m3h']:.1f} m³/h`, "
        "the cabin settles at:",
        "",
        "| Extract mode | Extract m³/h | Room pressure Pa | Achievable at ≤150 Pa? |",
        "|---|---:|---:|---|",
    ]
    for row in b["rows"]:
        ok = "yes, at the top end" if row["deliverable"] else "**no — the fan stalls**"
        L.append(f"| {row['mode']} | {row['extract_m3h']:.0f} | **{row['pressure_pa']:.0f}** | {ok} |")

    L += [
        "",
        f"A domestic extract fan develops of the order of "
        f"{b['fan_available_pa'][0]:.0f}–{b['fan_available_pa'][-1]:.0f} Pa, and at that top "
        f"end it can pull only **{b['max_deliverable_m3h']:.0f} m³/h** through this envelope. So "
        "the last row is not a pressure the cabin would sit at — it is a flow the fan **cannot "
        "deliver**. The specified boosted rate is unachievable without make-up air, and the "
        "shortfall is a ventilation deficit, not a fan selection problem.",
        "",
        "**Even the deliverable rows are not small numbers.** A chimney's natural draught is of "
        f"the order of {st['flue_draught_pa'][0]:.0f}–{st['flue_draught_pa'][1]:.0f} Pa, so at "
        f"**{b['rows'][0]['pressure_pa']:.0f} Pa** of negative pressure the flue does not merely "
        "underperform — it reverses. And §13-5 applies to this building: sustained negative "
        "pressure is exactly the mechanism that draws soil gas through the floor and defeats a "
        "radon barrier, whatever its airtightness.",
        "",
        "So the design is not a fan schedule. It is a decision about **where the make-up air "
        "comes from**, and every answer is a hole in the vapour barrier.",
        "",
        "[The make-up air screen](verificacion-aporte-aire.md) sizes that decision, and tests "
        "whether the same opening can rescue the flue. It cannot — which is why this screen "
        "ends on a decision and the next one ends on a specification.",
        "",
        "## 4. The stove, and why it cannot be an afterthought",
        "",
        "| Combustion air m³/h | Share of the basic extract |",
        "|---:|---:|",
    ]
    for c in st["cases"]:
        L.append(f"| {c['combustion_air_m3h']:.0f} | {c['share_of_basic_extract'] * 100:.0f} % |")

    L += [
        "",
        f"The margin against the flue reversing is **{fmt(st['margin_pa'])} Pa** at the highest "
        f"pressure the fan can actually hold ({st['worst_pressure_pa']:.0f} Pa, "
        f"{st['worst_mode']}) — negative, which is the finding. A wood stove in this cabin needs "
        "**its own outdoor air intake**, "
        "not a share of the room air, and that intake is a fourth penetration of the barrier.",
        "",
        "## 5. The penetrations, counted",
        "",
        "The envelope's moisture strategy rests on a continuous warm-side barrier at Sd ≥ 10 m. "
        "Each of these interrupts it, and none of them is optional:",
        "",
        "| Penetration | What it must do |",
        "|---|---|",
    ]
    for p in model["penetrations"]:
        L.append(f"| {p['item']} | {p['requirement']} |")

    L += [
        "",
        "The [2D junction screen](verificacion-puente-2d.md) says in as many words that it "
        "cannot see the barrier penetration: convective leakage through a barrier defect carries "
        "far more vapour than diffusion and is invisible to any conduction model. This screen "
        "does not model it either — it **counts** it, which is the most that can be done before "
        "a detail exists.",
        "",
        "## 6. The loop this does not close",
        "",
        "The [condensation screen](verificacion-condensacion-union.md) assumes **50 % indoor "
        "RH**, and its requirement scales hard with it — 40→60 % multiplies the required break "
        "by about 3.5×. Ventilation is what sets that RH, so the two are one problem.",
        "",
        "This screen does **not** close it, deliberately. A steady-state mass balance without "
        "the timber buffering gives an indoor concentration above saturation at any plausible "
        "rate, which is obviously wrong — the buffering is not a correction, it is most of the "
        "answer in a cabin whose interior is 48 m² of timber. A defensible closure needs a "
        "dynamic sorption model and material data the project does not hold.",
        "",
        "What can be said is the **direction**: the 50 % assumption is conservative, because "
        "lower RH reduces the required break. If the ventilation design holds the cabin below "
        "50 %, the junction requirement only gets easier. That is worth stating precisely "
        "because the opposite would be a design emergency.",
        "",
        "## 7. Limits",
        "",
        "- The rates in §2 are §13-2's, **adopted voluntarily**. They do not bind on this route "
        "and must not be reported as a requirement.",
        "- The leakage exponent 0.65 is a generic value. The pressures scale with it, and a "
        "measured n would move them.",
        "- The stove's combustion air and the flue draught are **assumption ranges**, not "
        "source values. The comparison is the finding; the exact figures are not.",
        "- No duct is sized, no fan is selected and no make-up air path is designed. This is a "
        "pressure screen, not a ventilation design.",
        "- §13-5's radon limit is not assessed. The screen only states that the mechanism is "
        "engaged.",
        "- Nothing here is a compliance statement or a design release.",
        "",
        "- Generated by `scripts/ventilacion_check.py`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    model = screen()
    b, st = model["balance"], model["stove"]
    v, r = b["volume"], b["rates"]

    # The volume must be plausible for an 18 m² plan between 1.7 and 2.9 m mean.
    assert 18.0 * 1.7 < v["volume_m3"] < 18.0 * 2.9, v["volume_m3"]

    # The adopted rates must be §13-2's arithmetic, not retyped numbers.
    assert abs(r["whole_dwelling_m3h"] - FLOOR_AREA_M2 * 1.2) < 1e-9
    assert abs(r["bed_places_m3h"] - BED_PLACES * 26.0) < 1e-9
    assert r["governing_m3h"] == max(r["whole_dwelling_m3h"], r["bed_places_m3h"])
    assert r["extract_basic_m3h"] == 36.0 + 54.0
    assert r["extract_boosted_one_m3h"] == 108.0
    assert r["extract_boosted_all_m3h"] == 108.0 + 108.0

    # Pressure must be monotone in flow and must reproduce Q50 at 50 Pa.
    assert abs(pressure_for_flow(N50_PER_H * v["volume_m3"], v) - 50.0) < 1e-9
    assert pressure_for_flow(0.0, v) == 0.0
    assert pressure_for_flow(120.0, v) > pressure_for_flow(60.0, v)

    # THE lock: at the fitted extract the cabin is far below atmospheric. If a
    # future edit makes the make-up implicit, this stops being true and fails.
    for row in b["rows"]:
        assert row["pressure_pa"] > 60.0, row
    assert (b["rows"][0]["pressure_pa"] < b["rows"][1]["pressure_pa"]
            < b["rows"][2]["pressure_pa"]), b["rows"]
    # One room boosted is at the edge of what a fan develops; both at once is
    # not deliverable at all, so that flow cannot be met without make-up air.
    assert b["rows"][1]["deliverable"] is True, b["rows"][1]
    assert b["rows"][2]["deliverable"] is False, b["rows"][2]
    assert b["max_deliverable_m3h"] > r["extract_boosted_one_m3h"]
    assert b["max_deliverable_m3h"] < r["extract_boosted_all_m3h"], b["max_deliverable_m3h"]

    # And the flue reverses: the margin must be negative, which is the finding.
    assert st["reverses"] is True, st
    assert st["margin_pa"] < 0.0, st["margin_pa"]
    # The flue margin must use an ACHIEVABLE pressure, not the stalled row:
    # quoting 406 Pa against a 10 Pa draught would overstate the case.
    assert st["worst_mode"] != "boosted, both rooms", st["worst_mode"]
    assert st["worst_pressure_pa"] <= max(b["fan_available_pa"]), st

    # The RH loop must be declared open, not quietly closed.
    assert model["rh_loop"]["closed"] is False
    assert "conservative" in model["rh_loop"]["direction"]

    # Every penetration must carry a requirement, or the count is decorative.
    assert len(model["penetrations"]) >= 5
    assert all(p["requirement"] for p in model["penetrations"])

    # The glyph must match the declaration, which renders the same margin as
    # −130 Pa. A report that prints -130 Pa is how a guard needle goes missing.
    rendered = markdown(model)
    assert f"**{fmt(st['margin_pa'])} Pa**" in rendered
    assert "-130 Pa" not in rendered, "ASCII hyphen in the rendered margin"
    assert "−130 Pa" in rendered

    print(f"Ventilation self-test OK: {v['volume_m3']:.1f} m³ at the reference section, "
          f"documented rates {r['governing_m3h']:.1f} m³/h against a "
          f"{r['extract_boosted_one_m3h']:.0f}–{r['extract_boosted_all_m3h']:.0f} m³/h boosted extract, "
          f"{b['rows'][0]['pressure_pa']:.0f}–{b['rows'][2]['pressure_pa']:.0f} Pa of negative "
          f"pressure with no make-up, only {b['max_deliverable_m3h']:.0f} m³/h deliverable at "
          f"the fan's limit, the flue reverses by {st['margin_pa']:.0f} Pa, and the RH loop is "
          f"declared open")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON model")
    ap.add_argument("--out-md", help="write Markdown report")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args()

    if args.selftest:
        selftest()
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
    sys.stdout.reconfigure(encoding="utf-8")
    main()
