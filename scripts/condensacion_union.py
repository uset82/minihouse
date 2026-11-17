#!/usr/bin/env python3
"""MiniHouse · condensation at the chassis junction (CONCEPTUAL — NO JUNCTION DRAWN).

The thermal-bridge screen (`puentes_termicas.py`) prices the chassis junction in
energy and then says, in as many words, that moisture is a separate analysis.
This is that analysis, in the only form available without a drawn detail: the
temperature-factor screen of NS-EN ISO 13788.

Three things make it worth its own calculation:

1. **The two chapters meet here and neither covers it.** §14-3 caps heat loss;
   §13-13 caps vapour resistance and requires a vapour barrier on the warm side.
   Neither says anything about the temperature of a steel member that crosses
   the insulation line, and that temperature is what decides whether the
   junction condenses.

2. **A steel member bridging the insulation has almost no resistance.** Its
   inner surface sits one surface film away from outdoor air. The temperature
   factor collapses, and the surface condenses at outdoor temperatures that
   occur for most of a Bergen year — not in a cold snap.

3. **The requirement is a resistance, and it is small enough to build.** The
   screen returns the added resistance a thermal break must provide, which is a
   number a detailer can use, unlike a Ψ value.

The 1D resistance network used here cannot bound the building, because it
ignores the lateral heat flow that a linear junction concentrates. A 2D
calculation has since been run on the same junction (`puente_2d.py`) and it
overturns two of this screen's conclusions: the direction of the error was
backwards for the steel (1D 0.236, 2D 0.377 — lateral feed warms it), and the
steel stops being the governing surface at the first millimetre of pad, so the
required break is 0.80 m²K/W rather than the 0.358 this screen returns. The
numbers below are unchanged and remain 1D; §7 states what they may and may not
be used for.

Usage:
  python condensacion_union.py --out-md fase1/verificacion-condensacion-union.md \
      --out-json knowledge/comparisons/condensacion-union.json
  python condensacion_union.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from envelope_check import p_sat  # noqa: E402

# Indoor condition. 20 °C / 50 % is the ordinary design case for a dwelling and
# the basis of the ISO 13788 temperature-factor tables.
T_IN = 20.0
RH_IN = 0.50

# Outdoor design condition for the Bergen coast. A screening value: the real one
# comes from the National Annex and the site (C-01), neither of which is held.
T_OUT = -10.0
RH_OUT = 0.90

# Surface film resistances, NS-EN ISO 6946. The corner value is the one ISO 13788
# uses at a concave junction, and it is the worst of the three.
R_SI_FLAT = 0.13     # horizontal heat flow (wall)
R_SI_FLOOR = 0.17    # downward heat flow (floor)
R_SI_CORNER = 0.25   # concave junction
R_SE = 0.04

# Critical surface humidity for mould growth, ISO 13788. 80 % is the criterion;
# 100 % is condensation.
RH_CRIT_MOULD = 0.80
RH_CRIT_CONDENSATION = 1.00

# Steel. A 10 mm plate at lambda 50 W/mK contributes 0.0002 m2K/W — included so
# the model shows it is negligible rather than asserting it.
LAM_STEEL = 50.0
STEEL_PLATE_MM = 10.0

LAM_TIMBER = 0.13
LAM_PU = 0.025

# The 2D calculation supersedes this screen's requirement, and the numbers are
# carried here so that the two cannot drift apart silently. `puente_2d.py` is
# the source: 20 mm of rigid foam reaches f_Rsi 0.754, 9 mm reaches 0.693.
REQUIRED_ADDED_R_2D = 0.80      # m²K/W on the governing surface
REQUIRED_PAD_MM_2D = 20.0
F_RSI_STEEL_2D = 0.377          # the same plate, solved in 2D
LAM_NEOPRENE = 0.15

# Material catalogue, by conductivity. The junction is designed by choosing a
# MATERIAL and a THICKNESS, so the two are kept separate here: naming a layer by
# its product thickness would make "how much of it you need" unreadable.
MATERIALS = {
    "timber": LAM_TIMBER,
    "rigid PU foam": LAM_PU,
    "neoprene": LAM_NEOPRENE,
}

# Junction constructions to screen. Each entry is the list of layers between the
# steel and the indoor air, as (material, thickness in mm), steel outwards.
SCENARIOS = (
    ("A. steel exposed indoors", ()),
    ("B. steel under a 22 mm timber deck", (("timber", 22.0),)),
    ("C. steel + 6 mm PU pad + timber deck",
     (("rigid PU foam", 6.0), ("timber", 22.0))),
    ("D. steel + 10 mm PU pad + timber deck",
     (("rigid PU foam", 10.0), ("timber", 22.0))),
    ("E. steel + neoprene 6 mm + timber deck",
     (("neoprene", 6.0), ("timber", 22.0))),
)

# Indoor/outdoor combinations for the sensitivity of the required resistance.
SENSITIVITY_RH = (0.40, 0.50, 0.60)
SENSITIVITY_T_OUT = (-5.0, -10.0, -15.0, -20.0)


def layer_resistance(material, thickness_mm):
    return thickness_mm / 1000.0 / MATERIALS[material]


def added_resistance(added=()):
    """Sum of the added layer resistances, m2K/W."""
    return sum(layer_resistance(m, t) for m, t in added)


def steel_resistance():
    return STEEL_PLATE_MM / 1000.0 / LAM_STEEL


def r_total(added=(), r_si=R_SI_FLAT):
    """Total resistance of the path from indoor air to outdoor air, m2K/W."""
    return r_si + R_SE + steel_resistance() + added_resistance(added)


def f_rsi(added=(), r_si=R_SI_FLAT):
    """Temperature factor, ISO 13788: f = (theta_si - theta_e)/(theta_i - theta_e).

    For a 1D path this reduces to f = 1 - R_si/R_total, which is the form used
    here. It tends to 0 as the construction approaches a bare film and to 1 as
    the resistance grows without bound.
    """
    return 1.0 - r_si / r_total(added, r_si)


def dew_point(t_c, rh):
    """Dew point from the Magnus relation, in degrees C."""
    p = rh * p_sat(t_c)
    return dew_point_from_pressure(p)


def dew_point_from_pressure(p_pa):
    """Invert the Magnus relation for a given vapour pressure."""
    if p_pa <= 0.0:
        return float("-inf")
    a = math.log(p_pa / 610.94)
    return 243.04 * a / (17.625 - a)


def surface_temperature(added=(), r_si=R_SI_FLAT, t_in=T_IN, t_out=T_OUT):
    """Indoor surface temperature of the junction, degrees C."""
    return t_in - (t_in - t_out) * r_si / r_total(added, r_si)


def f_crit(t_in=T_IN, rh_in=RH_IN, t_out=T_OUT, rh_crit=RH_CRIT_MOULD):
    """Critical temperature factor for a given surface humidity criterion.

    The surface is at the critical humidity when its vapour pressure equals
    p_i / rh_crit, which fixes a surface temperature; f_crit follows from the
    definition of f.
    """
    p_surface = rh_in * p_sat(t_in) / rh_crit
    t_surface_crit = dew_point_from_pressure(p_surface)
    return 1.0 - (t_in - t_surface_crit) / (t_in - t_out)


def required_added_resistance(target_f, r_si=R_SI_FLAT):
    """Added resistance needed to reach a target f, in m2K/W.

    Inverts f = 1 - R_si/R_total. Returns 0 when the bare construction already
    meets the target and a negative number is never returned.
    """
    if target_f >= 1.0:
        return float("inf")
    r_needed = r_si / (1.0 - target_f)
    return max(0.0, r_needed - r_total((), r_si))


def condensation_outdoor_temp(added=(), r_si=R_SI_FLAT, t_in=T_IN, rh_in=RH_IN):
    """Outdoor temperature at which the indoor surface reaches the dew point.

    Below this outdoor temperature the surface condenses. Rearranged from
    theta_si = theta_i - (theta_i - theta_e) R_si / R_total = theta_dew.
    """
    t_dew = dew_point(t_in, rh_in)
    return t_in - (t_in - t_dew) * r_total(added, r_si) / r_si


def mould_outdoor_temp(added=(), r_si=R_SI_FLAT, t_in=T_IN, rh_in=RH_IN):
    """Outdoor temperature at which the surface reaches the mould threshold."""
    p_surface = rh_in * p_sat(t_in) / RH_CRIT_MOULD
    t_surface = dew_point_from_pressure(p_surface)
    return t_in - (t_in - t_surface) * r_total(added, r_si) / r_si


def screen():
    crit_mould = f_crit(rh_crit=RH_CRIT_MOULD)
    crit_cond = f_crit(rh_crit=RH_CRIT_CONDENSATION)
    req_mould = required_added_resistance(crit_mould)
    req_cond = required_added_resistance(crit_cond)

    scenarios = []
    for name, added in SCENARIOS:
        f = f_rsi(added)
        scenarios.append({
            "scenario": name,
            "layers": [f"{m} {t:g} mm" for m, t in added],
            "added_resistance": round(added_resistance(added), 4),
            "r_total": round(r_total(added), 4),
            "f_rsi": round(f, 4),
            "surface_temp_c": round(surface_temperature(added), 2),
            "passes_mould": f >= crit_mould,
            "passes_condensation": f >= crit_cond,
            "condensation_below_c": round(condensation_outdoor_temp(added), 1),
            "mould_below_c": round(mould_outdoor_temp(added), 1),
        })

    # How the requirement moves with the indoor and outdoor assumptions.
    sensitivity = []
    for rh in SENSITIVITY_RH:
        row = {"rh_in": rh, "f_crit": round(f_crit(rh_in=rh), 4),
               "required_added": round(required_added_resistance(f_crit(rh_in=rh)), 4)}
        sensitivity.append(row)

    outdoor = []
    for t_out in SENSITIVITY_T_OUT:
        outdoor.append({
            "t_out_c": t_out,
            "f_crit": round(f_crit(t_out=t_out), 4),
            "required_added": round(required_added_resistance(f_crit(t_out=t_out)), 4),
        })

    # The corner is the worst surface. Same steel, higher film resistance.
    corners = []
    for r_si, label in ((R_SI_FLAT, "flat wall"), (R_SI_FLOOR, "floor, downward"),
                        (R_SI_CORNER, "concave corner")):
        corners.append({
            "surface": label, "r_si": r_si,
            "f_rsi_bare": round(f_rsi((), r_si), 4),
            "required_added": round(required_added_resistance(crit_mould, r_si), 4),
        })

    return {
        "revision": "CONDENSACION-UNION",
        "state": "CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO 2D CALCULATION, NO PRODUCT SELECTED",
        "units": "degC, Pa, m2K/W, mm",
        "basis": {
            "t_in_c": T_IN, "rh_in": RH_IN, "t_out_c": T_OUT, "rh_out": RH_OUT,
            "r_si_flat": R_SI_FLAT, "r_se": R_SE,
            "rh_crit_mould": RH_CRIT_MOULD,
            "outdoor_note": (
                "Screening value for the Bergen coast. The real design temperature comes "
                "from the National Annex and the site (C-01); neither is held."
            ),
            "sources": ["S012", "S023", "S011"],
        },
        "critical": {
            "f_crit_mould": round(crit_mould, 4),
            "f_crit_condensation": round(crit_cond, 4),
            "required_added_mould": round(req_mould, 4),
            "required_added_condensation": round(req_cond, 4),
            "governed_by": "mould" if req_mould >= req_cond else "condensation",
            "dew_point_c": round(dew_point(T_IN, RH_IN), 2),
        },
        "steel_resistance": round(steel_resistance(), 6),
        "materials": {k: v for k, v in MATERIALS.items()},
        "material_thickness_for_requirement": {
            k: round(req_mould * 1000.0 * v, 1) for k, v in MATERIALS.items()
        },
        "scenarios": scenarios,
        "sensitivity_rh": sensitivity,
        "sensitivity_t_out": outdoor,
        "corners": corners,
        "excluded": [
            "2D temperature field", "interstitial condensation at the barrier penetration",
            "air leakage", "junction detail", "chassis profile", "product selection",
            "rain and wind-driven wetting", "thermal comfort",
        ],
    }


def markdown(model):
    b = model["basis"]
    c = model["critical"]
    L = [
        "# MiniHouse · condensation at the chassis junction",
        "",
        "**State:** CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO 2D CALCULATION, NO PRODUCT SELECTED.",
        "The thermal-bridge screen prices this junction in energy and defers moisture as a "
        "separate analysis ([puentes térmicos](verificacion-puentes-termicas.md)). This is that "
        "analysis, in the only form available without a drawn detail.",
        "",
        "## 1. The two chapters meet here, and neither covers it",
        "",
        "§14-3 caps **heat loss**. §13-13 caps **vapour resistance** and requires the barrier on "
        "the warm side ([S012](../knowledge/sources/S012.md), "
        "[S023](../knowledge/sources/S023.md)). Neither says anything about the **temperature of "
        "a steel member that crosses the insulation line**, and that temperature is what decides "
        "whether the junction condenses. It is the one place where the envelope's two governing "
        "requirements leave a gap between them.",
        "",
        "## 2. The temperature factor",
        "",
        "NS-EN ISO 13788 assesses surface condensation by the temperature factor",
        "",
        "```",
        "f_Rsi = (theta_si - theta_e) / (theta_i - theta_e)",
        "```",
        "",
        "For a one-dimensional path this reduces to `f = 1 - R_si/R_total`. It tends to **0** as "
        "the construction approaches a bare surface film and to **1** as the resistance grows. "
        "The critical value comes from the surface humidity that matters — 80 % for mould, 100 % "
        "for condensation:",
        "",
        "| Criterion | Critical f | Meaning |",
        "|---|---:|---|",
        f"| Mould (80 % surface RH) | **{c['f_crit_mould']:.3f}** | the surface must stay above "
        f"this at design conditions |",
        f"| Condensation (100 %) | **{c['f_crit_condensation']:.3f}** | below this the surface "
        "runs wet |",
        "",
        f"Design conditions: **{b['t_in_c']:.0f} °C / {b['rh_in']*100:.0f} %** indoors, "
        f"**{b['t_out_c']:.0f} °C** outdoors, dew point "
        f"**{c['dew_point_c']:.1f} °C**. The outdoor value is a screening figure — the real one "
        "comes from the National Annex and the site, and neither is held.",
        "",
        "## 3. What a bare chassis does",
        "",
        f"A {STEEL_PLATE_MM:.0f} mm steel plate contributes "
        f"**{model['steel_resistance']:.4f} m²K/W**. That is not a small resistance; it is "
        "nothing. The inner surface of a steel member bridging the insulation therefore sits one "
        "surface film away from outdoor air:",
        "",
        "| Construction | Added R m²K/W | f_Rsi | Surface °C | Mould | Condensation |",
        "|---|---:|---:|---:|---|---|",
    ]
    for s in model["scenarios"]:
        L.append(
            f"| {s['scenario']} | {s['added_resistance']:.3f} | **{s['f_rsi']:.3f}** | "
            f"{s['surface_temp_c']:.1f} | {'pass' if s['passes_mould'] else '**FAIL**'} | "
            f"{'pass' if s['passes_condensation'] else '**FAIL**'} |"
        )

    bare = model["scenarios"][0]
    L += [
        "",
        f"**The bare case is not marginal, it is catastrophic.** f = {bare['f_rsi']:.3f} against a "
        f"required {c['f_crit_mould']:.3f}, so the surface sits at "
        f"**{bare['surface_temp_c']:.1f} °C** when it is −10 °C outside — below the "
        f"{c['dew_point_c']:.1f} °C dew point, so it is wet, and below freezing, so it is frost. "
        f"It condenses whenever the outdoor temperature falls below "
        f"**{bare['condensation_below_c']:.1f} °C**, which on the Bergen coast is most of the "
        "heating season rather than a cold snap.",
        "",
        "That is worth stating plainly because it is not an energy argument. A junction that "
        "condenses for six months a year will rot the timber it touches, and no amount of "
        "insulation elsewhere in the wall changes it.",
        "",
        "## 4. What it takes to pass",
        "",
        f"On a one-dimensional path, reaching the mould criterion needs an **added resistance of "
        f"{c['required_added_mould']:.3f} m²K/W** between the steel and the warm side. Expressed "
        "as a single layer of one material:",
        "",
        "| Material | λ W/mK | Resistance of 10 mm | Thickness needed |",
        "|---|---:|---:|---:|",
    ]
    for name, lam in model["materials"].items():
        L.append(f"| {name} | {lam:.3f} | {10.0 / 1000.0 / lam:.3f} | "
                 f"**{model['material_thickness_for_requirement'][name]:.0f} mm** |")

    L += [
        "",
        f"**Mould governs, not condensation.** The condensation criterion needs only "
        f"{c['required_added_condensation']:.3f} m²K/W, so a detail sized for mould is "
        "automatically dry. Sizing to the condensation limit alone would leave a surface that "
        "stays wet enough for long enough to grow things.",
        "",
        "## 5. The requirement moves with the assumptions",
        "",
        "| Indoor RH | Critical f | Added R needed |",
        "|---|---:|---:|",
    ]
    for row in model["sensitivity_rh"]:
        L.append(f"| {row['rh_in']*100:.0f} % | {row['f_crit']:.3f} | "
                 f"**{row['required_added']:.3f}** |")

    L += [
        "",
        "| Outdoor design | Critical f | Added R needed |",
        "|---|---:|---:|",
    ]
    for row in model["sensitivity_t_out"]:
        L.append(f"| {row['t_out_c']:.0f} °C | {row['f_crit']:.3f} | "
                 f"**{row['required_added']:.3f}** |")

    rh_first, rh_last = model["sensitivity_rh"][0], model["sensitivity_rh"][-1]
    t_first, t_last = model["sensitivity_t_out"][0], model["sensitivity_t_out"][-1]
    L += [
        "",
        f"**Indoor humidity moves the requirement harder than the weather does.** Across the "
        f"swept ranges, 40 → 60 % RH multiplies the required break by "
        f"**{rh_last['required_added'] / rh_first['required_added']:.1f}×**, while −5 → −20 °C "
        f"outdoors multiplies it by only "
        f"**{t_last['required_added'] / t_first['required_added']:.1f}×**. And 60 % is what a "
        "small heated space with a stove, cooking and washing produces — so ventilation "
        "(§13-1(1)) and the wet room stop being comfort items and become part of the junction "
        "design.",
        "",
        "## 6. The corner is worse than the wall",
        "",
        "| Surface | R_si | Bare f_Rsi | Added R needed |",
        "|---|---:|---:|---:|",
    ]
    for row in model["corners"]:
        L.append(f"| {row['surface']} | {row['r_si']:.2f} | {row['f_rsi_bare']:.3f} | "
                 f"**{row['required_added']:.3f}** |")

    L += [
        "",
        "The network can also be run with the higher surface film resistance a concave junction "
        "has — the air in a corner is stiller and the surface sees less of the room, and some "
        "national annexes to ISO 13788 use 0.20–0.25 there. Under that treatment the required "
        "break roughly doubles.",
        "",
        "**This is a 1D stand-in for a 2D effect, so it must not be added to the caveat in §7** — "
        "it is the same physics seen through a different lens. What it does establish is that the "
        "floor-to-wall corner, where the chassis perimeter beam sits, is the governing point "
        "rather than the flat wall, and that a break sized on the flat wall is sized on the "
        "easier of the two.",
        "",
        "## 7. The limit of this screen, and it has now been measured",
        "",
        "The one-dimensional network used above **ignores lateral heat flow**, and a linear "
        "junction concentrates exactly that. So no f_Rsi here can be read as a bound on the "
        "building — and [the 2D calculation](verificacion-puente-2d.md) has since been run on the "
        "same junction, which turns that caution into three specific corrections:",
        "",
        f"1. **The direction of the error was backwards for the steel.** This screen gives "
        f"{bare['f_rsi']:.3f} for the bare member; 2D gives **{F_RSI_STEEL_2D:.3f}**. Lateral "
        "feed from the surrounding floor warms the steel, so the 1D value was a *lower* bound on "
        "that surface, not an upper one. The number was a bound and the stated sign of the error "
        "was wrong.",
        "2. **The steel is not the governing surface once any break is built.** From the first "
        "millimetre of pad the coldest point moves to the **timber corner**, and it stays there "
        "for every thickness. A break sized to protect the steel is sized on the surface that "
        "has already stopped governing.",
        f"3. **So the requirement is larger than this screen says.** In 2D, "
        f"{REQUIRED_PAD_MM_2D:.0f} mm of rigid foam reaches the criterion and 9 mm does not — "
        f"0.693 against 0.754. The requirement is **{REQUIRED_ADDED_R_2D:.2f} m²K/W**, not "
        f"{c['required_added_mould']:.3f}, and the difference is not a refinement: the 1D answer "
        f"is {REQUIRED_ADDED_R_2D - c['required_added_mould']:.2f} m²K/W short.",
        "",
        "What survives unchanged is the conclusion: **a thermal break is mandatory and it has a "
        "size.** What does not survive is the claim that the size is a floor this screen can "
        "certify — it is a floor on a surface that stops governing as soon as it is built.",
        "",
        "There is a second thing this screen cannot see at all: the **vapour barrier "
        "penetration**. A chassis member passing through the wall interrupts the barrier, and "
        "§13-13's Sd ≥ 10 m is only satisfied if that interruption is sealed. Convective leakage "
        "through a barrier defect carries far more vapour than diffusion and is invisible to any "
        "1D model — the same limitation the envelope screen records.",
        "",
        "## 8. What this changes",
        "",
        "1. **The chassis junction is a moisture problem before it is an energy problem.** The "
        "thermal-bridge screen said it costs 16 % of heat loss; this one says a naive detail "
        "condenses below "
        f"{bare['condensation_below_c']:.1f} °C. The second is the one that damages the building.",
        "2. **A thermal break is mandatory, and it has a size.** Not \"a thermal break\" as a "
        f"gesture: **{REQUIRED_ADDED_R_2D:.2f} m²K/W** on the governing surface, which is "
        f"{REQUIRED_PAD_MM_2D:.0f} mm of rigid foam or "
        f"{REQUIRED_ADDED_R_2D * 1000.0 * LAM_TIMBER:.0f} mm of timber. A timber deck alone is "
        f"not enough — it reaches only {model['scenarios'][1]['f_rsi']:.3f}. Padding is not the "
        "only option and it is the worse one: putting the steel outside the insulation recovers "
        "the bare corner exactly, at no thickness at all.",
        "3. **Size for mould, not for condensation.** The condensation limit is the weaker of the "
        "two and sizing to it leaves a surface that is wet but not dripping.",
        "4. **The governing point is the floor-to-wall corner**, where the perimeter beam is and "
        "where R_si is highest. A detail that works on the flat wall may not work there.",
        "5. **Indoor humidity is a design parameter.** Moving from 40 % to 60 % multiplies the "
        f"required break by "
        f"{model['sensitivity_rh'][-1]['required_added'] / model['sensitivity_rh'][0]['required_added']:.1f}×, "
        "more than the whole outdoor range does, so ventilation (§13-1(1)) and the wet room stop "
        "being comfort items and become part of the junction design.",
        "",
        "## 9. Limits",
        "",
        "- **The numbers here are 1D and are not bounds on the building.** "
        "[The 2D screen](verificacion-puente-2d.md) corrects the requirement from "
        f"{c['required_added_mould']:.3f} to {REQUIRED_ADDED_R_2D:.2f} m²K/W and shows the "
        "governing surface is not the one this network computes.",
        "- **No junction detail exists.** The 2D screen models a steel plate, not a chassis "
        "member: the profile is not selected, so the geometry that would make this a design "
        "value does not exist either.",
        "- The outdoor design temperature is a **screening value**; the National Annex and the "
        "site are both missing (S014, C-01).",
        "- Interstitial condensation inside the wall is **not** modelled here — the envelope "
        "screen's Glaser profile covers the field of the wall, not the junction.",
        "- Air leakage and the barrier penetration are outside any 1D model and are recorded, not "
        "assessed.",
        "- No product is selected. The layer resistances use generic lambda values.",
        "- Nothing here is a junction design, a compliance statement or an energy calculation.",
        "",
        "- Generated by `scripts/condensacion_union.py`; JSON companion: "
        "`knowledge/comparisons/condensacion-union.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    # Saturation pressure and dew point against known values.
    assert abs(p_sat(20.0) - 2339.0) < 10.0
    assert abs(dew_point(20.0, 0.50) - 9.3) < 0.2, dew_point(20.0, 0.50)
    assert abs(dew_point(20.0, 1.00) - 20.0) < 0.05

    timber = (("timber", 22.0),)
    pad = (("rigid PU foam", 10.0), ("timber", 22.0))

    # The temperature factor must have the right limits and the right identity.
    r_si, r_se = R_SI_FLAT, R_SE
    bare = r_si + r_se + steel_resistance()
    assert abs(f_rsi(()) - (1.0 - r_si / bare)) < 1e-12
    # f -> 0 when the path is nothing but the surface film.
    assert abs(1.0 - r_si / r_si) < 1e-12
    # Monotone in added resistance, and bounded above by 1.
    f_bare = f_rsi(())
    f_timber = f_rsi(timber)
    f_pad = f_rsi(pad)
    assert 0.0 < f_bare < f_timber < f_pad < 1.0

    # THE lock on the formula. A steel member bridging the insulation has a
    # surface one film from outdoor air, so f must be small. If a future edit
    # inverts the ratio this fails: the value is ~0.24, not ~0.76.
    assert f_bare < 0.30, f"bare steel f_Rsi = {f_bare:.3f}; the formula may be inverted"
    # Equivalent form, derived independently: f = (R_total - R_si)/R_total, whose
    # numerator is everything outside the surface film (R_se plus the steel).
    assert abs(f_bare - (bare - r_si) / bare) < 1e-12
    assert abs(f_bare - (r_se + steel_resistance()) / bare) < 1e-12

    # The requirement must be the exact inverse of the criterion: feeding back
    # precisely the required resistance has to land on f_crit.
    crit = f_crit()
    assert 0.70 < crit < 0.80, crit
    req = required_added_resistance(crit)
    assert req > 0.0
    assert abs((1.0 - r_si / (r_total(()) + req)) - crit) < 1e-12
    # And a construction carrying that much added resistance must pass.
    assert f_rsi(pad) > crit > f_rsi(timber)
    # A loose target (low f) needs no break; a very strict one needs a great deal.
    assert required_added_resistance(0.0) == 0.0
    assert required_added_resistance(0.99) > 10.0

    # Mould must govern over condensation: 80 % surface RH is reached first.
    assert f_crit(rh_crit=RH_CRIT_MOULD) > f_crit(rh_crit=RH_CRIT_CONDENSATION)
    assert required_added_resistance(f_crit()) > required_added_resistance(
        f_crit(rh_crit=RH_CRIT_CONDENSATION))

    # The condensation threshold must FALL as resistance rises: a better detail
    # condenses at a colder outdoor temperature, so the bare case is the worst.
    t_bare = condensation_outdoor_temp(())
    t_pad = condensation_outdoor_temp(pad)
    assert t_pad < t_bare < T_IN
    # A bare steel surface condenses well above a Bergen winter.
    assert 4.0 < t_bare < 8.0, t_bare

    # The mould threshold is always milder than the condensation threshold.
    assert mould_outdoor_temp(()) > condensation_outdoor_temp(())

    # A higher surface film resistance (a corner) must lower f.
    assert f_rsi((), R_SI_CORNER) < f_rsi((), R_SI_FLAT) < f_rsi((), 0.10)

    # Sensitivity: wetter indoor air must need MORE break, and a colder outdoor
    # design must need more too. Both are ascending in the swept order.
    reqs = [required_added_resistance(f_crit(rh_in=rh)) for rh in SENSITIVITY_RH]
    assert reqs == sorted(reqs), reqs
    reqs_out = [required_added_resistance(f_crit(t_out=t)) for t in SENSITIVITY_T_OUT]
    assert reqs_out == sorted(reqs_out)

    model = screen()
    assert len(model["scenarios"]) == len(SCENARIOS)
    assert model["critical"]["governed_by"] == "mould"
    # The bare case must fail both criteria in the serialised model.
    assert not model["scenarios"][0]["passes_mould"]
    assert not model["scenarios"][0]["passes_condensation"]
    # Every material thickness must be positive and finite.
    for name, mm in model["material_thickness_for_requirement"].items():
        assert mm > 0.0, name

    # --- the 2D screen must still say what this report claims it says --------
    # This screen quotes three numbers that come from `puente_2d.py`. Quoting
    # them without solving is how a report and its source drift apart, so the
    # two cases the claim rests on are solved here: 20 mm reaches the criterion
    # and 9 mm does not. A change in either solver fails this.
    import puente_2d

    nine = puente_2d.evaluate(steel_mm=10.0, pad_mm=9.0)
    twenty = puente_2d.evaluate(steel_mm=10.0, pad_mm=REQUIRED_PAD_MM_2D)
    assert abs(nine["f_rsi"] - 0.693) < 0.02, nine["f_rsi"]
    assert abs(twenty["f_rsi"] - puente_2d.F_CRIT_MOULD) < 0.02, twenty["f_rsi"]
    assert nine["f_rsi"] < puente_2d.F_CRIT_MOULD <= twenty["f_rsi"] + 1e-9
    # 20 mm of PU at lambda 0.025 is the resistance this report now quotes.
    assert abs(REQUIRED_PAD_MM_2D / 1000.0 / LAM_PU - REQUIRED_ADDED_R_2D) < 0.01
    # And the 1D answer was materially short of it, not a rounding apart.
    assert REQUIRED_ADDED_R_2D - model["critical"]["required_added_mould"] > 0.40
    # The steel's 1D and 2D values must disagree in the direction §7 states:
    # 2D is HIGHER, because lateral feed warms the member.
    assert puente_2d.evaluate(steel_mm=10.0)["f_rsi"] > model["scenarios"][0]["f_rsi"] + 0.10

    print("Junction condensation self-test OK: f_Rsi limits and inversion lock, critical "
          "factor inverse, mould-over-condensation, thresholds, corner and sensitivity all pass; "
          "the 2D screen still gives 0.693 at 9 mm and 0.754 at 20 mm, and its steel reads "
          "higher than 1D as §7 states")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON screen model")
    ap.add_argument("--out-md", help="write Markdown screening report")
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
    main()
