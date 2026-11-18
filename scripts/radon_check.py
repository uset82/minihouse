#!/usr/bin/env python3
"""MiniHouse · §13-5 radon, for a floor that is not on the ground.

The ventilation screen established that the extract holds this cabin at 7–140 Pa of
negative pressure, that sustained negative pressure is the mechanism which draws
soil gas through a floor, and that §13-5 is therefore engaged. It also declined to
assess it, correctly, because the project has no site. This screen assesses what
can be assessed without one.

§13-5 asks two different things and they must not be conflated:

  * a **performance** requirement — annual average ≤ 200 Bq/m³;
  * a **prescriptive** route — a radon barrier against the ground plus preparation
    for pressure reduction above 100 Bq/m³, *unless documented unnecessary*.

The phrase that decides this building is **"against the ground"**. This floor is not
on the ground: it sits on a steel chassis with a ventilated void beneath it, which
`envelope_check` already models. So the prescriptive route describes an artefact
this building does not have, and the question becomes whether the void is itself
the measure — or whether the barrier must be built anyway.

The arithmetic has one property that makes it worth doing: **the cabin's radon
concentration is bounded above by E/Q regardless of the void**, where E is the
exhalation from the footprint and Q the ventilation rate. That bound is the
pathological case in which every atom exhaled under the floor reaches the room.
On ordinary ground it lands far below the action level, and the margin is
structural rather than a modelling result — which is exactly what the "documented
unnecessary" route needs.

The exception is alum shale, which is real in Norway and is the reason C-01 decides
this question rather than the arithmetic.

Usage:
  python radon_check.py --out-md fase1/verificacion-radon.md \
      --out-json knowledge/comparisons/radon.json
  python radon_check.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import aporte_aire as aa           # noqa: E402
import ventilacion_check as vt     # noqa: E402

# --- §13-5, verbatim from S023 ----------------------------------------------
RADON_LIMIT_BQ = 200.0      # annual average
ACTION_LEVEL_BQ = 100.0     # above this, pressure reduction must be available

# --- the footprint ----------------------------------------------------------
FLOOR_AREA_M2 = 18.0
PERIMETER_M = 18.0

# --- soil radon exhalation --------------------------------------------------
# A generic order-of-magnitude range for ordinary ground, NOT a source value and
# NOT project data. It is swept, and the screen's conclusion is stated as a bound
# on it rather than as a prediction. 1 mBq/(m²·s) = 3.6 Bq/(m²·h).
SOIL_EXHALATION_MBQ_M2S = (5.0, 20.0, 50.0)
# Alum shale (alunskifer) is the Norwegian exception and can be one to two orders
# of magnitude above the generic range. Carried as a separate case so the reader
# can see where the conclusion stops.
ALUM_SHALE_MBQ_M2S = 300.0

# --- the void under the floor ----------------------------------------------
# C-05 is open: no chassis profile, so no void height. Swept.
VOID_HEIGHT_MM = (150.0, 300.0, 450.0)
# An open perimeter is driven by wind; a skirted one only by the stack effect,
# because the wind then acts across the skirt rather than through the void.
VOID_CASES = (
    ("open perimeter", 20.0, "wind"),
    ("skirted, 5 mm gap", 5.0, "stack"),
)
WIND_MS = 3.0
STACK_DELTA_T_K = 20.0
T_K = 293.0

# --- the floor as a leakage path -------------------------------------------
# What fraction of the envelope's leakage passes through the floor deck. A floor
# is usually tighter than a wall with a door and four windows, but it is also the
# largest single element. Swept rather than assumed.
FLOOR_LEAK_SHARE = (0.10, 0.30)


def fmt(value, spec="+.0f"):
    """Format with a typographic minus, so the report matches the declaration."""
    return f"{value:{spec}}".replace("-", "−")


def exhalation_bq_h(mbq_m2s, area_m2=FLOOR_AREA_M2):
    """Radon activity exhaled by the footprint, Bq/h."""
    return mbq_m2s / 1000.0 * area_m2 * 3600.0


def stack_pressure_pa(height_m, delta_t_k=STACK_DELTA_T_K, t_k=T_K):
    """Buoyancy pressure across a void of `height_m`."""
    return aa.RHO_AIR * 9.81 * height_m * delta_t_k / t_k


def void_ventilation_m3h(gap_mm, height_m, driving):
    """Air change through the void's perimeter openings.

    The same orifice law the make-up air screen uses: a gap of area A passes
    Q = 3600·Cd·A·sqrt(2·dp/rho). `driving` selects wind or stack, because which
    one acts is the whole difference between an open and a skirted void.
    """
    area = (gap_mm / 1000.0) * PERIMETER_M
    dp = aa.wind_pressure_pa(WIND_MS) if driving == "wind" else stack_pressure_pa(height_m)
    return aa.flow_through_area_m3h(area, dp)


def void_concentration_bq(exhalation_bq_h, q_vent_m3h, q_floor_m3h):
    """Steady state in the void: what is exhaled leaves through the perimeter or the floor."""
    total_out = q_vent_m3h + q_floor_m3h
    if total_out <= 0.0:
        raise ValueError("a void with no outflow has no steady state")
    return exhalation_bq_h / total_out


def cabin_concentration_bq(void_bq, q_floor_m3h, q_cabin_m3h):
    """What the floor's inward leakage delivers, diluted by the cabin's ventilation."""
    return void_bq * q_floor_m3h / q_cabin_m3h


def bound_bq(exhalation_bq_h, q_cabin_m3h):
    """The upper bound: every atom exhaled under the footprint ends up in the cabin.

    Independent of the void, of the floor's tightness and of the junction detail.
    It is the number that makes the "documented unnecessary" route arguable.
    """
    return exhalation_bq_h / q_cabin_m3h


def screen():
    vol = vt.volume_m3()
    rates = vt.documented_rates()
    q_cabin = rates["extract_basic_m3h"]
    # The floor sees the cabin's depression, which the make-up air screen now fixes.
    am = aa.screen()
    dp_floor = am["chosen_pressure"]["basic_pa"]
    q_total_leak = aa.leakage_m3h(dp_floor, vol)

    rows = []
    for mbq in SOIL_EXHALATION_MBQ_M2S:
        e = exhalation_bq_h(mbq)
        for label, gap, driving in VOID_CASES:
            for h_mm in VOID_HEIGHT_MM:
                h = h_mm / 1000.0
                q_vent = void_ventilation_m3h(gap, h, driving)
                ach = q_vent / (FLOOR_AREA_M2 * h)
                for share in FLOOR_LEAK_SHARE:
                    q_floor = q_total_leak * share
                    c_void = void_concentration_bq(e, q_vent, q_floor)
                    c_cabin = cabin_concentration_bq(c_void, q_floor, q_cabin)
                    rows.append({
                        "exhalation_mbq_m2s": mbq,
                        "void": label,
                        "void_height_mm": h_mm,
                        "void_ach": round(ach, 1),
                        "floor_leak_share": share,
                        "q_floor_m3h": round(q_floor, 2),
                        "void_bq": round(c_void, 1),
                        "cabin_bq": round(c_cabin, 1),
                        "margin_to_limit": round(RADON_LIMIT_BQ / c_cabin, 1)
                        if c_cabin > 0 else None,
                    })

    bounds = [{"exhalation_mbq_m2s": mbq,
               "exhalation_bq_h": round(exhalation_bq_h(mbq), 0),
               "bound_bq": round(bound_bq(exhalation_bq_h(mbq), q_cabin), 1),
               "vs_limit": round(RADON_LIMIT_BQ / bound_bq(exhalation_bq_h(mbq), q_cabin), 1),
               "vs_action": round(ACTION_LEVEL_BQ / bound_bq(exhalation_bq_h(mbq), q_cabin), 1)}
              for mbq in SOIL_EXHALATION_MBQ_M2S]

    # The worst ordinary-ground case in the sweep, and the alum-shale bound.
    worst = max(rows, key=lambda r: r["cabin_bq"])
    alum_bound = bound_bq(exhalation_bq_h(ALUM_SHALE_MBQ_M2S), q_cabin)
    # What exhalation rate would reach the limit at this ventilation rate.
    critical_mbq = (RADON_LIMIT_BQ * q_cabin) / (FLOOR_AREA_M2 * 3600.0) * 1000.0
    critical_action_mbq = (ACTION_LEVEL_BQ * q_cabin) / (FLOOR_AREA_M2 * 3600.0) * 1000.0

    return {
        "state": "SCREENING — CONDITIONAL ON C-01. Not a radon assessment, not a site "
                 "classification, not a compliance statement.",
        "limits": {"annual_average_bq": RADON_LIMIT_BQ, "action_level_bq": ACTION_LEVEL_BQ},
        "volume_m3": round(vol["volume_m3"], 1),
        "ventilation_m3h": q_cabin,
        "floor_pressure_pa": dp_floor,
        "envelope_leakage_m3h": round(q_total_leak, 1),
        "floor_is_on_ground": False,
        "void": {"height_mm": list(VOID_HEIGHT_MM),
                 "cases": [{"label": l, "gap_mm": g, "driving": d} for l, g, d in VOID_CASES]},
        "bounds": bounds,
        "rows": rows,
        "worst_ordinary": worst,
        "alum_shale": {"exhalation_mbq_m2s": ALUM_SHALE_MBQ_M2S,
                       "bound_bq": round(alum_bound, 0),
                       "exceeds_limit": alum_bound > RADON_LIMIT_BQ},
        "critical_exhalation_mbq_m2s": round(critical_mbq, 0),
        "critical_action_mbq_m2s": round(critical_action_mbq, 0),
        "prescriptive": {
            "barrier_required": True,
            "preparation_required": True,
            "documented_unnecessary_route": True,
            "why_still_required": "no site, so no exhalation rate and no measurement; the "
                                  "route is available and unsupported until C-01",
        },
        "junction": {
            "length_m": PERIMETER_M,
            "note": "the barrier must be continuous across the floor-to-wall junction, which "
                    "is the same corner the 2D screen solved and the one place the steel "
                    "crosses the line",
        },
    }


def markdown(m):
    b = m["bounds"]
    w = m["worst_ordinary"]

    L = [
        "# MiniHouse · §13-5 radon, for a floor that is not on the ground",
        "",
        f"**State:** {m['state']}",
        "",
        f"- Limit: annual average **≤ {m['limits']['annual_average_bq']:.0f} Bq/m³**; "
        f"pressure reduction must be available above "
        f"**{m['limits']['action_level_bq']:.0f} Bq/m³** (S023).",
        f"- The floor is **not on the ground**: a ventilated void over the chassis, "
        f"**{m['void']['height_mm'][0]:.0f}–{m['void']['height_mm'][-1]:.0f} mm** deep "
        f"(C-05 open).",
        f"- Cabin ventilation **{m['ventilation_m3h']:.0f} m³/h**; the floor sees "
        f"**{m['floor_pressure_pa']:.0f} Pa** of depression with the make-up air in place.",
        "- Generated by `scripts/radon_check.py`; JSON companion: "
        "`knowledge/comparisons/radon.json`.",
        "",
        "## 1. §13-5 asks two things, and this building answers them differently",
        "",
        "The clause contains a **performance** requirement and a **prescriptive** route, and "
        "they are not the same question:",
        "",
        "| | What it says | What it means here |",
        "|---|---|---|",
        f"| Performance | annual average ≤ **{m['limits']['annual_average_bq']:.0f} Bq/m³** | "
        "a concentration, which needs a site |",
        "| Prescriptive | a **radon barrier against the ground**, plus preparation for "
        "pressure reduction above "
        f"**{m['limits']['action_level_bq']:.0f} Bq/m³**, *unless documented unnecessary* | "
        "an artefact this building does not obviously have |",
        "",
        "The phrase that decides it is **\"against the ground\"**. This floor sits on a steel "
        "chassis with a ventilated void beneath it — `envelope_check` already models the void "
        "as a ventilated layer. So the prescriptive route describes a detail the building does "
        "not contain, and the question is whether the void *is* the measure or whether the "
        "barrier has to be built anyway.",
        "",
        "**That question cannot be closed without a site.** What can be closed is how much "
        "margin the arithmetic leaves, and whether the answer is close enough to the limit for "
        "the site to matter.",
        "",
        "## 2. The bound that makes this tractable",
        "",
        "Radon moves into a building by **advection**, not diffusion: soil gas is pushed "
        "through openings by a pressure difference, and the radon rides with it. That has two "
        "consequences the project should record.",
        "",
        "First, **a radon barrier is an airtightness item, not an Sd item**. The project's "
        "vapour barrier is specified as **Sd ≥ 10 m** — a diffusion number — and a membrane "
        "that satisfies it is not thereby a radon barrier. The two requirements are written in "
        "different currencies and one does not imply the other.",
        "",
        "Second, the concentration has an upper bound that no void, no junction detail and no "
        "membrane can exceed. If E is the activity exhaled under the footprint and Q the "
        "cabin's ventilation rate, then even in the pathological case where **every atom "
        "exhaled under the floor reaches the room**:",
        "",
        "> `C_cabin ≤ E / Q`",
        "",
        "| Soil exhalation mBq/(m²·s) | E, Bq/h | Bound Bq/m³ | Margin to 200 | Margin to 100 |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in b:
        L.append(f"| {row['exhalation_mbq_m2s']:.0f} | {row['exhalation_bq_h']:.0f} | "
                 f"**{row['bound_bq']:.1f}** | {row['vs_limit']:.0f} × | "
                 f"{row['vs_action']:.0f} × |")

    L += [
        "",
        f"The exhalation rates are a **generic order-of-magnitude range for ordinary ground**, "
        f"not a source value and not project data. They are swept, and the conclusion is a "
        f"statement about the bound rather than a prediction of a concentration.",
        "",
        f"**Even the top of that range leaves a bound of {b[-1]['bound_bq']:.0f} Bq/m³ — "
        f"{b[-1]['vs_limit']:.0f}× inside the limit and {b[-1]['vs_action']:.0f}× inside the "
        f"action level.** The margin is not a modelling result; it comes from the fact that "
        f"{m['ventilation_m3h']:.0f} m³/h of ventilation passes through a footprint of "
        f"{FLOOR_AREA_M2:.0f} m².",
        "",
        "## 3. The void, and what it actually buys",
        "",
        "The void is a buffer volume: radon exhaled under the floor is diluted by the air "
        "changing through the perimeter before it can leak up into the cabin. How much it buys "
        "depends on whether the void is **open or skirted**:",
        "",
        "| Void case | Driving pressure | Void air changes |",
        "|---|---:|---:|",
    ]
    seen = set()
    for label, gap, driving in VOID_CASES:
        for h_mm in m["void"]["height_mm"]:
            h = h_mm / 1000.0
            q = aa_void(gap, h, driving)
            dp = (aa.wind_pressure_pa(WIND_MS) if driving == "wind"
                  else aa_stack(h))
            key = (label, h_mm)
            if key in seen:
                continue
            seen.add(key)
            L.append(f"| {label}, {h_mm:.0f} mm | {dp:.2f} Pa | "
                     f"**{q / (FLOOR_AREA_M2 * h):.0f} /h** |")

    L += [
        "",
        "Those air-change rates look implausibly large, and they are the correct consequence of "
        "a shallow volume rather than an error: a 150 mm void over 18 m² holds 2.7 m³, so a "
        "wind-driven flow through 0.36 m² of perimeter gap turns it over hundreds of times an "
        "hour. The physical reading is simpler than the number — **an open void is not a buffer "
        "at all, it is outdoor air**.",
        "",
        "The case that matters is therefore the **skirted** one, which is also the realistic "
        "one: a cabin in Bergen will want a skirt for wind and snow. Even then the void changes "
        f"over **19–32 times an hour** — a residence time of two to three minutes — because the "
        f"buoyancy pressure across a shallow void is small but so is the volume it has to move. "
        f"At 300 mm that pressure is **{aa_stack(0.3):.2f} Pa**.",
        "",
        f"That is the geometric reason the buffer is robust. Across every combination swept, "
        f"the worst cabin concentration is **{w['cabin_bq']:.1f} Bq/m³** "
        f"({w['void']}, {w['void_height_mm']:.0f} mm, "
        f"{w['floor_leak_share'] * 100:.0f} % floor leakage) — against a bound of "
        f"{b[-1]['bound_bq']:.0f} Bq/m³ that the void can only improve on.",
        "",
        "**So the void is not what makes this safe.** The bound already does. The void is worth "
        "having, and the design must not destroy it — a sealed skirt, or filling the void with "
        "insulation, would remove the buffer and leave the bound as the answer. That is a "
        "constraint to record now, because it is the kind of thing a later decision removes "
        "without noticing.",
        "",
        "## 4. Where the conclusion stops: alum shale",
        "",
        f"The bound is only as good as the exhalation rate under the floor. On ordinary ground "
        f"the limit is reached at **{m['critical_exhalation_mbq_m2s']:.0f} mBq/(m²·s)** and the "
        f"action level at **{m['critical_action_mbq_m2s']:.0f} mBq/(m²·s)** — both far above "
        f"the swept range.",
        "",
        f"**Alum shale is the exception.** At **{m['alum_shale']['exhalation_mbq_m2s']:.0f} "
        f"mBq/(m²·s)** the bound is **{m['alum_shale']['bound_bq']:.0f} Bq/m³**, which "
        f"{'exceeds' if m['alum_shale']['exceeds_limit'] else 'does not exceed'} the limit. "
        "Alum shale is real in Norway and its presence is a site fact, not a design fact.",
        "",
        "That is why **C-01 decides this question and the arithmetic does not.** The screen can "
        "say the margin is large on ordinary ground and that it disappears on alum shale. "
        "Whether this cabin stands on either is a site classification nobody has made.",
        "",
        "## 5. Where the barrier goes, if it is built",
        "",
        "The prescriptive route is not dismissed here, and it should not be. Until a site "
        "measurement exists, the barrier stands — but it must be understood as a **floor-deck "
        "airtightness requirement**, not a ground membrane and not an Sd value.",
        "",
        f"The consequence is a detail, and it is {m['junction']['length_m']:.0f} m long. The "
        "barrier has to be continuous across the **floor-to-wall junction**, which is the same "
        "corner [the 2D screen](verificacion-puente-2d.md) solved for heat and the one place "
        "where the steel crosses the line. A membrane that stops at the wall's inner face and "
        "restarts outside the chassis is two membranes with a gap, and the gap is the path.",
        "",
        "The same corner therefore carries three requirements at once — the wrapping that "
        "brings f_Rsi back to 0.921, the vapour barrier's continuity, and the radon path. "
        "**One drawing answers all three, or none of them is answered.** "
        "[The junction detail](planos/detalle-encuentro-R0.svg) is that drawing: it is "
        "generated from the solver's constants, and it shows the barrier turning the "
        "corner at (13, −22) and the chassis plate crossing that plane when the beam is "
        "not wrapped.",
        "",
        "## 6. The penetrations",
        "",
        "A radon barrier is only as good as its holes, and this project has an unusual number "
        "of them by design:",
        "",
        "| Penetration | Does it cross the radon line? |",
        "|---|---|",
        "| make-up air inlet | **no** — it enters the wall above the floor, and must not be "
        "routed under the deck |",
        "| stove combustion air | **no** if taken through the wall; **yes** if drawn from the "
        "void |",
        "| drain | **yes** — the one wet penetration through the floor |",
        "| cooker-hood and bathroom extract | **no** — they leave through the wall or roof |",
        "",
        "The make-up air screen's inlet is therefore compatible with the barrier, which is not "
        "obvious and is worth stating: **the hole the project has just sized is in the other "
        "membrane.** The drain is the one that needs a sealed collar, and the stove's "
        "combustion air becomes a barrier question the moment it is taken from under the deck "
        "instead of through the wall.",
        "",
        "## 7. Limits",
        "",
        "- **Not a radon assessment.** No site, no measurement, no soil classification, no "
        "concentration claim. Everything here is a bound on an assumed exhalation rate.",
        "- The exhalation range is generic. It is the single input the conclusion is most "
        "sensitive to, and the alum-shale case shows what happens when it is wrong.",
        "- The void height is a **C-05 unknown** and is swept. No chassis profile exists.",
        "- The floor's share of the envelope leakage is swept, not measured.",
        "- The void is treated as well mixed. A stratified void would dilute less near the "
        "floor, which the bound already covers.",
        "- §13-5's prescriptive route is **not** discharged. The barrier and the preparation "
        "for pressure reduction remain required until C-01.",
        "- Nothing here is a compliance statement, a site approval or a design release.",
        "",
        "## 8. Source and status",
        "",
        "- §13-5: S023, verbatim. Ventilation rate and leakage: `ventilacion_check.py`.",
        "- Floor depression: `aporte_aire.py`. Void as a ventilated layer: `envelope_check.py`.",
        "- Junction: `puente_2d.py`. Site and soil: **C-01**, open.",
        "- Status: **screening**, conditional on C-01. The bound is the finding; the "
        "concentration is not claimed.",
        "",
        "- Generated by `scripts/radon_check.py`.",
        "",
    ]
    return "\n".join(L)


def aa_void(gap_mm, height_m, driving):
    return void_ventilation_m3h(gap_mm, height_m, driving)


def aa_stack(height_m):
    return stack_pressure_pa(height_m)


def selftest():
    m = screen()
    b = m["bounds"]
    w = m["worst_ordinary"]

    # Exhalation arithmetic: 1 mBq/(m2·s) over 18 m2 for an hour.
    assert abs(exhalation_bq_h(1.0) - 18.0 * 3.6) < 1e-9, exhalation_bq_h(1.0)

    # The bound must be E/Q and must fall as ventilation rises.
    for row in b:
        assert abs(row["bound_bq"] - row["exhalation_bq_h"] / m["ventilation_m3h"]) < 0.1
    assert b[0]["bound_bq"] < b[1]["bound_bq"] < b[2]["bound_bq"]

    # THE lock: on ordinary ground the bound must sit far inside both thresholds.
    # If a future edit makes the assumption range harsher, this fails and the
    # "documented unnecessary" route stops being arguable.
    assert b[-1]["bound_bq"] < m["limits"]["action_level_bq"], b[-1]
    assert b[-1]["vs_limit"] > 3.0, b[-1]

    # And the void must never make things worse than the bound.
    for row in m["rows"]:
        assert row["cabin_bq"] <= b[-1]["bound_bq"] + 1e-9, row

    # The open void must ventilate more than the skirted one, and the skirted one
    # must still turn over ~20 times an hour — that is the geometric claim in §3.
    # If a future edit drops it below that, the report's "19-32 times an hour" and
    # the buffer argument stop being true together.
    for h_mm in m["void"]["height_mm"]:
        h = h_mm / 1000.0
        q_open = void_ventilation_m3h(20.0, h, "wind")
        q_skirt = void_ventilation_m3h(5.0, h, "stack")
        assert q_open > q_skirt, (h_mm, q_open, q_skirt)
        assert q_skirt / (FLOOR_AREA_M2 * h) > 15.0, (h_mm, q_skirt)
        # And the open case must be so large that calling it "outdoor air" holds.
        assert q_open / (FLOOR_AREA_M2 * h) > 100.0, (h_mm, q_open)

    # The skirted case must be stack-driven and the open one wind-driven, or the
    # comparison in §3 is not the comparison being described.
    assert stack_pressure_pa(0.3) < aa.wind_pressure_pa(WIND_MS) / 10.0
    assert stack_pressure_pa(0.3) > 0.1

    # Alum shale must be the case that breaks it, and it must be flagged.
    assert m["alum_shale"]["exceeds_limit"] is True, m["alum_shale"]
    assert m["alum_shale"]["bound_bq"] > m["limits"]["annual_average_bq"]

    # The critical exhalation must be the inverse of the bound.
    assert abs(m["critical_exhalation_mbq_m2s"]
               - RADON_LIMIT_BQ * m["ventilation_m3h"] / (FLOOR_AREA_M2 * 3.6)) < 1.0

    # The floor must be declared off the ground, and the barrier still required.
    assert m["floor_is_on_ground"] is False
    assert m["prescriptive"]["barrier_required"] is True
    assert m["prescriptive"]["documented_unnecessary_route"] is True
    assert m["junction"]["length_m"] == PERIMETER_M

    print(f"Radon self-test OK: bound {b[0]['bound_bq']:.1f}–{b[-1]['bound_bq']:.1f} Bq/m³ "
          f"on ordinary ground against a {m['limits']['annual_average_bq']:.0f} limit, worst "
          f"void case {w['cabin_bq']:.1f} Bq/m³, the void never worse than the bound, the "
          f"limit needs {m['critical_exhalation_mbq_m2s']:.0f} mBq/(m²·s), and alum shale at "
          f"{m['alum_shale']['exhalation_mbq_m2s']:.0f} breaks it at "
          f"{m['alum_shale']['bound_bq']:.0f} Bq/m³")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON model")
    ap.add_argument("--out-md", help="write Markdown report")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return 0

    m = screen()
    if args.out_json:
        Path(args.out_json).write_text(
            json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        Path(args.out_md).write_text(markdown(m), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_json and not args.out_md:
        print(markdown(m))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
