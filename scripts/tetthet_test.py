#!/usr/bin/env python3
"""MiniHouse · the §14-3 airtightness test, specified and not performed

Row 14.5 of the ytelsesoversikt is the cheapest in the document: n50 ≤ 1.5 h⁻¹ at
50 Pa, one fan, one afternoon. This script turns that sentence into a test
specification — and the specification turns out to say something the sentence did
not, because the arithmetic of a small building is not the arithmetic of a house.

Three things happen here that a hand-written page would not do:

  * **n50 is volume-normalised and this building is envelope-heavy.** A/V is 1.80
    against ~0.8 for a compact two-storey house, so the same 1.5 h⁻¹ asks for a q50
    roughly two and a half times lower. The limit is easy in absolute flow (55 m³/h)
    and hard per square metre of envelope carrying 61 m of linear detail.

  * **The envelope has a floor as well as a ceiling.** §14-3 rewards tightness; the
    extract needs to be fed. In a sealed cabin the depression the fan must hold
    rises as leakage falls, and at 1.19 h⁻¹ it reaches the fan's ceiling. That is
    not a requirement — it is a fault case — but it is why the target is 1.30 rather
    than "as tight as we can build".

  * **The measurement is not exact, so the acceptance threshold is not the limit.**
    The declaration's own rule — a margin is adequate only if positive and larger
    than its own uncertainty — applied to a measurement puts acceptance at 1.36 for
    a 10 % test, not 1.50.

What this file does NOT do: report a measurement. None exists. The requirement stays
undischarged, and the honest status of row 14.5 is unchanged. A specification is to a
measurement what a screening is to a verification: the same shape, one step short.

The standard (NS-EN ISO 9972:2015) is **not held** — see knowledge/sources/S031.md.
No clause number, point count, pressure range or uncertainty rule is quoted from it,
because reconstructing a document nobody here has read is the failure mode the
knowledge rules exist to prevent. Everything that depends on the standard is marked
to be confirmed when it is acquired.

Usage:
  python tetthet_test.py --out-md fase1/especificacion-ensayo-tetthet.md \
      --out-json knowledge/comparisons/tetthet.json
  python tetthet_test.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import aporte_aire as aa           # noqa: E402
import estrategia_incendio as ei   # noqa: E402
import puentes_termicas as pt      # noqa: E402
import ventilacion_check as vt     # noqa: E402

# --- the requirement, owned by the ventilation screen -----------------------
N50_LIMIT = vt.N50_PER_H           # 1.5 h⁻¹ at 50 Pa, §14-3 (S011)
REFERENCE_PA = vt.REFERENCE_PRESSURE_PA
N_EXPONENT = vt.LEAKAGE_EXPONENT   # 0.65, stated rather than measured

# --- the standard -----------------------------------------------------------
STANDARD = "NS-EN ISO 9972:2015"
STANDARD_HELD = False

# --- measurement uncertainty -------------------------------------------------
# Relative expanded uncertainty (k = 2) on n50. Two bands: a single-fan test with a
# calibrated plate in still air, and a typical field test. STATED, NOT DERIVED — the
# standard does not fix one figure for all buildings, and quoting a generic value as
# if it were a product property is the defect this project keeps repairing. The
# sensitivity to this choice is tabulated rather than hidden.
U_REL = {"favourable": 0.05, "typical": 0.10, "poor": 0.20}

# --- the target --------------------------------------------------------------
# Chosen as the middle of a band, not as a round number: the upper edge is the
# measurement (§5), the lower edge is the fan's ceiling (§6).
TARGET_N50 = 1.30

# --- test pressures ----------------------------------------------------------
# The standard's point count is not quoted (see the docstring). These are the
# pressures the fan must be able to reach so that the slope of the log-log fit —
# and therefore the exponent the screens assume — can be measured at all.
TEST_PRESSURES_PA = (10.0, 25.0, 50.0, 75.0, 100.0)

# --- comparators -------------------------------------------------------------
# Envelope-to-volume ratio of ordinary dwellings, for the q50 comparison only.
# Computed from stated dimensions so the arithmetic is visible rather than asserted.
COMPARATORS = (
    ("120 m² two-storey", 12.0, 10.0, 5.0),
    ("120 m² single-storey", 12.0, 10.0, 2.5),
)


def geometry():
    """Envelope area, volume and the two ratios that decide how hard the limit is."""
    vol = vt.volume_m3()
    a = ei.interior_timber_m2()
    # The barrier sits on the internal face, so the envelope is the internal face area:
    # walls and ceiling (ei) plus the floor (vt owns the plan area).
    a_env = a["net_m2"] + vt.FLOOR_AREA_M2
    joints = pt.junction_lengths_m()
    joint_m = sum(joints.values())
    v = vol["volume_m3"]
    return {
        "volume_m3": round(v, 2),
        "envelope_m2": round(a_env, 2),
        "walls_and_ceiling_m2": a["net_m2"],
        "floor_m2": vt.FLOOR_AREA_M2,
        "a_over_v": round(a_env / v, 3),
        "joint_m": round(joint_m, 2),
        "joints": {k: round(x, 2) for k, x in joints.items()},
        "joint_per_m2": round(joint_m / a_env, 3),
    }


def comparators():
    out = []
    for label, l, w, h in COMPARATORS:
        vol = l * w * h
        area = 2.0 * l * w + 2.0 * (l + w) * h
        out.append({"label": label, "a_over_v": round(area / vol, 3)})
    return out


def leakage_m3h(n50, dp_pa, volume_m3, n=N_EXPONENT):
    """Q = Q50 · (Δp/50)^n with Q50 = n50 · V.

    Parameterised by n50 because the whole point of §6 is to sweep it. At n50 = 1.5
    and n = 0.65 this must reproduce aporte_aire.leakage_m3h exactly — the self-test
    checks that, so this file cannot quietly acquire a second leakage law.
    """
    return n50 * volume_m3 * (dp_pa / REFERENCE_PA) ** n


def flows(g):
    q50 = N50_LIMIT * g["volume_m3"]
    rows = []
    for dp in TEST_PRESSURES_PA:
        rows.append({"dp_pa": dp,
                     "flow_m3h": round(leakage_m3h(N50_LIMIT, dp, g["volume_m3"]), 1)})
    return {
        "q50_m3h": round(q50, 1),
        "q50_per_m2_env": round(q50 / g["envelope_m2"], 3),
        "q50_per_m2_floor": round(q50 / g["floor_m2"], 2),
        "q50_per_m_joint": round(q50 / g["joint_m"], 2),
        "test_points": rows,
        "max_test_flow_m3h": rows[-1]["flow_m3h"],
    }


def acceptance():
    """The n50 a measurement must show to demonstrate the limit, per uncertainty band."""
    out = {}
    for label, u in U_REL.items():
        out[label] = {"u_rel": u, "n50_accept": round(N50_LIMIT / (1.0 + u), 3)}
    return out


def sealed_case(g):
    """The depression a sealed cabin settles at, as the envelope gets tighter.

    This is aporte_aire's own inversion, run over n50 instead of fixed at 1.5:
    the fan needs the basic extract, and leakage is the only supply.
    """
    rates = vt.documented_rates()
    fan_max = max(vt.FAN_AVAILABLE_PA)
    rows = []
    for n50 in (1.50, 1.40, 1.30, 1.20, 1.19):
        q50 = n50 * g["volume_m3"]
        dp = REFERENCE_PA * (rates["extract_basic_m3h"] / q50) ** (1.0 / N_EXPONENT)
        rows.append({"n50": n50, "q50_m3h": round(q50, 1), "pressure_pa": round(dp, 1),
                     "spare_pa": round(fan_max - dp, 1), "deliverable": dp <= fan_max})
    # The n50 at which the basic extract reaches the fan's ceiling. Closed form:
    # dp = 50 · (Q/Q50)^(1/n) = fan_max  →  Q50 = Q / (fan_max/50)^n.
    q50_floor = rates["extract_basic_m3h"] / (fan_max / REFERENCE_PA) ** N_EXPONENT
    return {
        "extract_basic_m3h": rates["extract_basic_m3h"],
        "fan_max_pa": fan_max,
        "rows": rows,
        "n50_floor": round(q50_floor / g["volume_m3"], 3),
    }


def exponent_band(g):
    """What the assumed exponent is worth: the same n50, three exponents."""
    rates = vt.documented_rates()
    q50 = N50_LIMIT * g["volume_m3"]
    out = []
    for n in (0.50, N_EXPONENT, 0.80):
        dp = REFERENCE_PA * (rates["extract_basic_m3h"] / q50) ** (1.0 / n)
        out.append({"n": n, "pressure_pa": round(dp, 1)})
    return out


def inlet_band(g):
    """The make-up inlet across the airtightness band, at the screen's design point.

    aporte_aire sizes the inlet for the boosted one-room extract at 10 Pa. Its area
    is set by that extract, not by the leakage, so it barely moves — which is the
    procurement consequence in §7.
    """
    rates = vt.documented_rates()
    dp = 10.0
    out = []
    for n50 in (1.50, 1.40, 1.30, 1.20):
        leak = leakage_m3h(n50, dp, g["volume_m3"])
        inlet_flow = rates["extract_boosted_one_m3h"] - leak
        area = aa.orifice_area_m2(inlet_flow, dp)
        out.append({"n50": n50, "leakage_m3h": round(leak, 1),
                    "inlet_m3h": round(inlet_flow, 1),
                    "area_cm2": round(area * 1e4, 1),
                    "diameter_mm": round(aa.diameter_mm(area), 1)})
    return out


def screen():
    g = geometry()
    f = flows(g)
    acc = acceptance()
    sc = sealed_case(g)
    return {
        "state": "SPECIFICATION — NO MEASUREMENT EXISTS. Not a compliance statement.",
        "requirement": {"n50_limit": N50_LIMIT, "reference_pa": REFERENCE_PA,
                        "source": "TEK17 §14-3 (S011)"},
        "standard": {"name": STANDARD, "held": STANDARD_HELD, "card": "S031"},
        "geometry": g,
        "comparators": comparators(),
        "flows": f,
        "uncertainty": acc,
        "target_n50": TARGET_N50,
        "sealed_case": sc,
        "exponent_band": exponent_band(g),
        "inlet_band": inlet_band(g),
    }


def sgn(v, fmt=".0f"):
    """Signed number with the typographic minus this project uses everywhere."""
    s = f"{abs(v):{fmt}}"
    return ("−" if v < 0 else "+") + s


def table(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def markdown():
    m = screen()
    g, f, sc = m["geometry"], m["flows"], m["sealed_case"]
    acc = m["uncertainty"]
    comp = {c["label"]: c["a_over_v"] for c in m["comparators"]}
    two_storey = comp["120 m² two-storey"]
    one_storey = comp["120 m² single-storey"]
    target = m["target_n50"]
    floor = sc["n50_floor"]
    accept_typical = acc["typical"]["n50_accept"]

    L = [
        "# MiniHouse · the airtightness test: specified, and not performed",
        "",
        "**State:** SPECIFICATION — **NO MEASUREMENT EXISTS**. This is a plan to measure, "
        "not a measurement. It does not close §14-3's airtightness requirement and must not "
        "be reported as doing so.",
        "",
        f"- Requirement **n50 ≤ {N50_LIMIT:.1f} h⁻¹ at {REFERENCE_PA:.0f} Pa** "
        "(§14-3, [S011](../knowledge/sources/S011.md)).",
        f"- Internal volume **{g['volume_m3']:.2f} m³**; envelope **{g['envelope_m2']:.2f} m²**; "
        f"**Q50 = {f['q50_m3h']:.1f} m³/h** at the limit.",
        f"- Target **{target:.2f} h⁻¹**; acceptance **{accept_typical:.2f}** measured, so a "
        f"10 % uncertainty still clears {N50_LIMIT:.1f}.",
        f"- Standard **{STANDARD}** — **not held** "
        "([S031](../knowledge/sources/S031.md)).",
        "- Generated by `scripts/tetthet_test.py`; JSON companion "
        "`knowledge/comparisons/tetthet.json`.",
        "",
        "## 1. Why this document exists, and what it is not",
        "",
        "The [ytelsesoversikt](ytelsesoversikt.md) calls row 14.5 the cheapest in the "
        "document, and it is: a pressure test on an 18 m² building is one fan and one "
        "afternoon. But *cheap* and *available* are different things, and this is where they "
        "separate. **You cannot pressure-test a building that does not exist.** The afternoon "
        "is not this week; it is the end of fabrication, and again at handover. So the row "
        "stays `undetermined` and what changes is only that the work is now specified rather "
        "than named.",
        "",
        "That is worth being blunt about, because the temptation is to call the row closed. A "
        "specification is to a measurement what a screening is to a verification: the same "
        "shape, one step short — and this project has already been bitten once by confusing "
        "the two.",
        "",
        "## 2. The number, and the geometry it is attached to",
        "",
        "n50 is a **volume-normalised** quantity, and this building carries an unusual amount "
        "of envelope per unit of volume.",
        "",
    ]
    L += table(
        ["Quantity", "Value", "How"],
        [["Internal volume V", f"{g['volume_m3']:.2f} m³", "18 m² × mean height 2051 mm"],
         ["Envelope area A_E", f"{g['envelope_m2']:.2f} m²",
          f"walls and ceiling {g['walls_and_ceiling_m2']:.2f} + floor {g['floor_m2']:.2f}"],
         ["A_E/V", f"**{g['a_over_v']:.2f} m⁻¹**", "the number that makes the limit hard"],
         ["Q50 at the limit", f"**{f['q50_m3h']:.1f} m³/h**", f"{N50_LIMIT:.1f} × V"],
         ["q50 at the limit", f"**{f['q50_per_m2_env']:.2f} m³/(h·m²)**", "Q50 / A_E"],
         ["Linear detail", f"{g['joint_m']:.2f} m",
          "floor, eave, corners, opening reveals"],
         ["Joint density", f"**{g['joint_per_m2']:.2f} m/m²**", "joints / A_E"],
         ["Leakage per metre at 50 Pa", f"**{f['q50_per_m_joint']:.2f} m³/(h·m)**",
          "Q50 / joint length"]],
        ["---", "---:", "---"])
    L += [
        "",
        f"A compact two-storey dwelling reaches A/V ≈ **{two_storey:.2f}** and a "
        f"single-storey one ≈ **{one_storey:.2f}**; this cabin is **{g['a_over_v']:.2f}**. For "
        f"the same n50 it must therefore hold a q50 **{g['a_over_v'] / two_storey:.1f}×** lower "
        f"than the two-storey house and **{g['a_over_v'] / one_storey:.1f}×** lower than the "
        "single-storey one.",
        "",
        f"In absolute flow the target is trivial — {f['q50_m3h']:.0f} m³/h is a bathroom fan. "
        f"In relative terms it is not: **{f['q50_per_m2_env']:.2f} m³/(h·m²) across "
        f"{g['envelope_m2']:.1f} m² of envelope carrying {g['joint_m']:.0f} m of linear detail, "
        f"or {f['q50_per_m_joint']:.2f} m³/h per metre of joint at 50 Pa.**",
        "",
        "That is the whole reason the test is worth buying. The number is easy to reach and "
        "easy to miss, and which one happened is not knowable from the drawings.",
        "",
        "## 3. The standard, and the fact that the project does not hold it",
        "",
        f"The method is defined by **{STANDARD}**, which replaced NS-EN 13829. The project has "
        "**no copy** ([S031](../knowledge/sources/S031.md), recorded *to acquire*), so this "
        "document does **not** quote its clauses, its number of measurement points, its "
        "pressure range or its uncertainty treatment. Those are properties of a document "
        "nobody here has read, and reconstructing them from memory is the exact failure the "
        "knowledge rules exist to prevent.",
        "",
        "What can be said without it:",
        "",
        "- The standard defines **more than one test method**, and they do not give the same "
        "number. A test of the envelope with the deliberate openings sealed is not the same "
        "measurement as a test of the building as used. **The method must be named on the "
        "certificate**, because a number without its method is not reproducible — and §2-3(1)'s "
        "guidance requires the evidence to be *verifiable in the project*.",
        "- **The project needs both.** §14-3's n50 is a property of the envelope, so the "
        "envelope test is the one that answers the regulation. The ventilation and radon "
        "screens need the leakage the extract actually works against, which is the in-use "
        "state.",
        "- The in-use number is **the larger of the two wherever an intentional opening "
        "stands open in use**. This building's inlet is closable, so the gap between the two "
        "methods is set by how the inlet is left — which is the same control problem "
        "[the make-up air screen](verificacion-aporte-aire.md) ends on. Where every opening "
        "is closable and closed, the two methods converge. An envelope-test pass therefore "
        "does **not** by itself demonstrate an in-use pass, and if only one method can be "
        "run it must be the in-use one, because it bounds the other.",
        "",
        "**Recommendation, to be confirmed when the standard is acquired:** envelope test for "
        "the §14-3 figure, in-use test recorded alongside, both with the method named.",
        "",
        "## 4. Two tests, not one — and the first one is the one that matters",
        "",
    ]
    L += table(
        ["Test", "When", "What it can do"],
        [["**T1**", "after the barrier and the lining battens, before the interior boards",
          "**locate** leaks"],
         ["**T2**", "at completion, before handover", "**count** them"]],
        ["---", "---", "---"])
    L += [
        "",
        "A single test at completion tells you a number. Only T1 can tell you **where**, "
        "because once the boards go on the barrier is invisible — which is precisely the case "
        "§2-4's guidance names for photographs: *bygningsdeler som bygges inn og er vanskelig "
        "tilgjengelige*. This project's two load-bearing details are in that category: the "
        "wrapped steel at the floor edge, and the barrier's turn at (13, −22) in "
        "[the junction detail](planos/detalle-encuentro-R0.svg). Both are photographed, and "
        "both are only reachable at T1.",
        "",
        "If only one test can be afforded, **T1 is the one that can still change the "
        "building**; T2 is the one the FDV file needs. At one fan and an afternoon each, the "
        "choice should not arise.",
        "",
        "## 5. Acceptance, and why the target is not 1.5",
        "",
        "The limit is **absolute**. The [declaration of margins](declaracion-de-margenes.md) "
        "records that a numeric level is not a tolerance unless one is granted in a forskrift "
        "or a vedtak, and none is. A measurement of 1.52 h⁻¹ is a **deviation** needing "
        "dispensation under PBL ch. 19, not a rounding.",
        "",
        "But a measurement is not exact either, and the declaration's own rule applies "
        "unchanged: **a margin is adequate only if it is positive and larger than its own "
        "uncertainty.** Applied to a measurement, that rule moves the acceptance threshold "
        "below the limit:",
        "",
    ]
    L += table(
        ["Test quality", "Relative uncertainty (k = 2)", "n50 that still demonstrates ≤ 1.5"],
        [["favourable — calibrated plate, still air", f"{acc['favourable']['u_rel'] * 100:.0f} %",
          f"**{acc['favourable']['n50_accept']:.2f}**"],
         ["typical field test", f"{acc['typical']['u_rel'] * 100:.0f} %",
          f"**{acc['typical']['n50_accept']:.2f}**"],
         ["poor — wind, one point per level", f"{acc['poor']['u_rel'] * 100:.0f} %",
          f"{acc['poor']['n50_accept']:.2f}"]],
        ["---", "---:", "---:"])
    L += [
        "",
        f"So the acceptance criterion is **measured n50 ≤ {accept_typical:.2f} h⁻¹ with a "
        f"declared 10 % uncertainty**, and the construction target is **{target:.2f}**.",
        "",
        f"**{target:.2f} is not a round number pulled from the air.** It is a target chosen to "
        f"clear a typical test ({accept_typical:.2f}) while staying clear of the fault case in "
        f"§6 ({floor:.2f}) — and a poor test would fail it, which is an argument about the "
        "test rather than about the building. **The quality of the measurement is part of the "
        "acceptance**: a 20 % test can fail a cabin that was built to target, and the way to "
        "avoid that is to buy a good test, not a tight cabin.",
        "",
        "## 6. The lower edge, and the two requirements that pull apart",
        "",
        "§14-3 rewards a tighter envelope. The project's answer to §13-1(1) — a mechanical "
        "extract — needs to be **fed**. In a sealed cabin the only supply is leakage, so the "
        "depression the fan must hold *rises* as the envelope improves:",
        "",
    ]
    L += table(
        ["n50 h⁻¹", "Q50 m³/h", f"Basic extract ({sc['extract_basic_m3h']:.0f} m³/h), sealed cabin",
         f"Spare to the {sc['fan_max_pa']:.0f} Pa ceiling"],
        [[f"{r['n50']:.2f}", f"{r['q50_m3h']:.1f}", f"{r['pressure_pa']:.0f} Pa",
          f"{sgn(r['spare_pa'])} Pa"] for r in sc["rows"]],
        ["---:", "---:", "---:", "---:"])
    L += [
        "",
        f"The bottom two rows are the finding. **The envelope has a floor as well as a "
        f"ceiling**, and the floor is **{floor:.2f} h⁻¹** at a {sc['fan_max_pa']:.0f} Pa fan "
        f"and a {sc['extract_basic_m3h']:.0f} m³/h basic extract: at 1.20 the spare is "
        f"{sgn(sc['rows'][3]['spare_pa'])} Pa, and at 1.19 it is negative — **the fan stalls** "
        "and the extract cannot be delivered at all, so the make-up inlet becomes the only "
        "supply.",
        "",
        f"A **{sc['rows'][3]['spare_pa']:.0f} Pa** spare at 1.20 h⁻¹ is not a margin. It is "
        "smaller than any plausible uncertainty in a fan curve, so by the declaration's own "
        "rule the row is not demonstrated even though the arithmetic says *deliverable*.",
        "",
        "That floor is **not a requirement**. With the inlet working, the pressure is held at "
        "10 Pa and n50 does not enter at all. It is a **fault case**, and it is the reason the "
        "inlet must be interlocked with the extract rather than left to the occupant: at "
        "1.50 h⁻¹ a closed inlet leaves the cabin at "
        f"{sc['rows'][0]['pressure_pa']:.0f} Pa; at 1.20 it leaves it at "
        f"{sc['rows'][3]['pressure_pa']:.0f} Pa, which is the fan's ceiling and, per "
        "[the make-up air screen](verificacion-aporte-aire.md), the flue's reversal.",
        "",
        f"**So «as tight as we can build» is not the instruction.** The instruction is "
        f"{target:.2f}, and it is a band, not a minimum.",
        "",
        "## 7. What the inlet costs across the band — almost nothing",
        "",
        "The inlet is sized by the design extract, not by the leakage, so it barely moves as "
        "the envelope improves:",
        "",
    ]
    L += table(
        ["n50", "Leakage at 10 Pa m³/h", "Inlet flow m³/h", "Area cm²", "Diameter mm"],
        [[f"{r['n50']:.2f}", f"{r['leakage_m3h']:.1f}", f"{r['inlet_m3h']:.1f}",
          f"{r['area_cm2']:.1f}", f"{r['diameter_mm']:.0f}"] for r in m["inlet_band"]],
        ["---:", "---:", "---:", "---:", "---:"])
    L += [
        "",
        f"**The inlet can be ordered before the envelope is measured**, because its size does "
        f"not depend on the result — {m['inlet_band'][0]['diameter_mm']:.0f} mm at the limit, "
        f"{m['inlet_band'][-1]['diameter_mm']:.0f} mm at the target's lower neighbour. That is "
        "a procurement consequence worth having: the one component the test might have been "
        "thought to gate is the one it does not.",
        "",
        "## 8. The test measures two numbers, and the project assumes both",
        "",
        f"The screens use n50 **and** the leakage exponent n = {N_EXPONENT:.2f}. The test "
        "returns both — n from the slope of the log-log fit, which is why the points must "
        "span a range rather than cluster:",
        "",
    ]
    L += table(
        ["Assumed exponent n", f"Basic extract at {N50_LIMIT:.1f} h⁻¹"],
        [[f"{r['n']:.2f}" + (" (assumed)" if r["n"] == N_EXPONENT else ""),
          f"{r['pressure_pa']:.0f} Pa"] for r in m["exponent_band"]],
        ["---:", "---:"])
    spread = (max(r["pressure_pa"] for r in m["exponent_band"])
              - min(r["pressure_pa"] for r in m["exponent_band"]))
    L += [
        "",
        f"A **{spread:.0f} Pa** spread on the ventilation screen's headline number, from an "
        "assumption nobody has tested. The measurement replaces it in the ventilation, "
        "make-up air and radon screens at once.",
        "",
        "## 9. What a result does to the other three screens",
        "",
        "- **Ventilation** — the sealed-case pressures scale as Q50^(1/n), so a measured n50 "
        "replaces the 1.5 in all three rows of that screen's pressure table, and a measured n "
        "replaces the exponent that produced them.",
        "- **Make-up air** — the inlet area is nearly insensitive (§7), but its "
        "*justification* changes: at 1.50 h⁻¹ the inlet is advisable, at 1.20 it is mandatory.",
        "- **Radon** — the floor's inward leakage is a share of the envelope leakage at the "
        "floor's pressure, so a tighter envelope reduces the delivered radon as well as the "
        "depression. That is the one place where tighter is unambiguously better, and it is "
        "why the bound `C ≤ E/Q` survives either result.",
        "",
        "## 10. After a move",
        "",
        "§4-2 requires the owner to keep the documentation current «ved endringer i "
        "bruksforutsetninger, eller ved fysisk utførelse». A module that is lifted, transported "
        "and reconnected meets that condition at every deployment: the envelope travels "
        "intact, but every installation connection is remade. **The test is therefore a "
        "per-deployment record, not a one-off**, and the FDV file carries the T2 certificate of "
        "the most recent one.",
        "",
        "Whether a move can change n50 at all is a question the project cannot answer without "
        "a second measurement. The honest position: **the first re-test is also the "
        "experiment.**",
        "",
        "## 11. Limits",
        "",
        "- **No measurement exists.** This document specifies a test; it does not report one, "
        "and §14-3's airtightness remains undischarged. Row 14.5 of the ytelsesoversikt stays "
        "`undetermined`.",
        "- **The standard is not held.** No clause number, point count, pressure range or "
        "uncertainty rule is quoted from it; everything that depends on it is marked to be "
        "confirmed on acquisition.",
        "- The uncertainty bands (5 / 10 / 20 %) are **stated, not derived**, and the "
        "acceptance threshold moves with them — that sensitivity is tabulated rather than "
        "hidden.",
        f"- The {sc['fan_max_pa']:.0f} Pa fan ceiling is the ventilation screen's generic "
        "range, not a selected product.",
        f"- The floor of {floor:.2f} h⁻¹ inherits the {sc['extract_basic_m3h']:.0f} m³/h basic "
        f"extract and the {N_EXPONENT:.2f} exponent; both are assumptions until measured.",
        "- The envelope area is the internal face area, which is where the barrier sits. "
        "External areas would give a lower q50 and a flattering comparison.",
        "- Nothing here is a compliance statement, a design release or a fabrication "
        "instruction.",
        "",
        "- Generated by `scripts/tetthet_test.py`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    g = geometry()
    f = flows(g)
    sc = sealed_case(g)
    acc = acceptance()

    # The envelope is walls + ceiling + floor, and the volume is the screens' volume.
    assert abs(g["envelope_m2"] - (g["walls_and_ceiling_m2"] + g["floor_m2"])) < 0.01, g
    assert abs(g["volume_m3"] - vt.volume_m3()["volume_m3"]) < 0.01, g

    # The central claim of §2: this building is envelope-heavy, and the limit is
    # therefore stricter in q50 than it looks in n50.
    assert g["a_over_v"] > 1.6, g["a_over_v"]
    assert 0.0 < f["q50_per_m2_env"] < 1.0, f["q50_per_m2_env"]
    for c in comparators():
        assert g["a_over_v"] > c["a_over_v"], (g["a_over_v"], c)

    # The leakage law must be aporte_aire's, not a second one.
    vol = {"volume_m3": g["volume_m3"]}
    assert abs(leakage_m3h(N50_LIMIT, 10.0, g["volume_m3"]) - aa.leakage_m3h(10.0, vol)) < 0.01, (
        leakage_m3h(N50_LIMIT, 10.0, g["volume_m3"]), aa.leakage_m3h(10.0, vol))
    assert abs(leakage_m3h(N50_LIMIT, REFERENCE_PA, g["volume_m3"]) - f["q50_m3h"]) < 0.1

    # One fan is enough: the highest test point must be well inside a small set's range.
    assert f["max_test_flow_m3h"] < 150.0, f["max_test_flow_m3h"]

    # Acceptance falls as uncertainty rises, and never exceeds the limit.
    for label, u in U_REL.items():
        assert acc[label]["n50_accept"] < N50_LIMIT, (label, acc[label])
    assert acc["favourable"]["n50_accept"] > acc["typical"]["n50_accept"] > acc["poor"]["n50_accept"]

    # §6's floor: the sealed case must be monotone in n50, must cross the fan ceiling
    # inside the swept band, and the floor must be below 1.5 but above 1.0.
    pressures = [r["pressure_pa"] for r in sc["rows"]]
    assert pressures == sorted(pressures), pressures
    assert any(r["deliverable"] for r in sc["rows"]) and not all(r["deliverable"] for r in sc["rows"])
    assert 1.0 < sc["n50_floor"] < N50_LIMIT, sc["n50_floor"]

    # The target must sit inside the band the document claims: above the floor, and
    # low enough that a typical measurement still clears the limit.
    target = screen()["target_n50"]
    assert target > sc["n50_floor"], (target, sc["n50_floor"])
    assert target * (1.0 + U_REL["typical"]) <= N50_LIMIT, target
    assert target < N50_LIMIT

    # §7: the inlet grows as the envelope tightens — a tighter envelope leaks less, so
    # the inlet must pass more — but only slightly. Both halves matter: the direction is
    # the physics, the smallness is the procurement point. The band runs 1.50 → 1.20, so
    # the diameters must ascend.
    band = inlet_band(g)
    dias = [r["diameter_mm"] for r in band]
    assert dias == sorted(dias), dias
    assert dias[0] - dias[-1] < 10.0, dias
    assert abs(dias[0] - 113.0) < 2.0, dias[0]

    # §8: the exponent matters, and its sign is not obvious — a lower exponent means
    # a *higher* pressure for the same flow, so the ordering must be checked, not assumed.
    ex = exponent_band(g)
    assert ex[0]["pressure_pa"] > ex[1]["pressure_pa"] > ex[2]["pressure_pa"], ex

    # The rendered document must carry the three claims that make it worth writing.
    text = markdown()
    assert "NO MEASUREMENT EXISTS" in text
    assert f"{sc['n50_floor']:.2f}" in text
    assert "not held" in text
    for s in ("§14-3", "§13-1(1)", "§2-4", "§4-2"):
        assert s in text, s
    # Typographic minus must survive, as everywhere in this project.
    assert "−22" in text

    print(f"Tetthet test self-test OK: Q50 {f['q50_m3h']:.1f} m³/h, "
          f"q50 {f['q50_per_m2_env']:.2f} m³/(h·m²), A/V {g['a_over_v']:.2f}, "
          f"target {target:.2f} inside [{sc['n50_floor']:.2f}, "
          f"{acc['typical']['n50_accept']:.2f}], one fan at "
          f"{f['max_test_flow_m3h']:.0f} m³/h, inlet "
          f"{band[0]['diameter_mm']:.0f}→{band[-1]['diameter_mm']:.0f} mm, no measurement")


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

    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(screen(), indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(json.dumps(screen(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
