#!/usr/bin/env python3
"""MiniHouse · the make-up air the extract needs: its size, and what it cannot buy.

ventilacion_check.py ends on a sentence rather than a number — "the design is not
a fan schedule, it is a decision about where the make-up air comes from". That
decision has a size, and this screen computes it.

The arithmetic is an orifice. A deliberate inlet of area A passes

    Q = 3600 · Cd · A · sqrt(2 · dp / rho)

so holding the cabin at a chosen depression while the extract runs fixes A, and A
fixes the diameter. Three things then follow, and only the first is comfortable:

  * The hole is small. A 101 mm inlet holds the cabin at 10 Pa instead of 106 Pa,
    which is 96 Pa of depression removed for the price of one wall valve. For the
    ventilation, and for §13-5's radon mechanism, that is most of the problem
    solved.

  * It does not fix declaration row 14. At 10 Pa the flue margin against a 10-20 Pa
    draught is 0 to +10 Pa — not positive across the band, and not larger than the
    band's own half-width. The only design point that passes the §2-2(3) adequacy
    test needs a 164 mm inlet at 2 Pa, and 2 Pa is below the pressure a 3 m/s wind
    puts on a wall. **A passive inlet cannot hold a set pressure at all**, because
    the wind's own pressure is larger than any design value that would help.

  * So row 14 is not improved by a hole. It is retired by a room-sealed stove,
    which takes the flue out of the cabin-pressure question entirely. That is a
    procurement requirement with no dimensional cost, and it is the only thing in
    this project that closes a negative safety margin for free.

Usage:
  python aporte_aire.py --out-md fase1/verificacion-aporte-aire.md \
      --out-json knowledge/comparisons/aporte-aire.json
  python aporte_aire.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import estrategia_incendio as ei   # noqa: E402
import ventilacion_check as vt     # noqa: E402

# --- the orifice ------------------------------------------------------------
# A sharp-edged opening is 0.6-0.65. A louvred wall valve with a filter and a
# flap is lower, and a lower Cd means a bigger hole for the same flow, so 0.6 is
# the optimistic end. Stated, not measured.
CD = 0.6
RHO_AIR = 1.2               # kg/m3 at 20 C, sea level

# --- what a passive inlet is allowed to be ----------------------------------
# Above 125 mm an inlet stops being a wall valve and becomes a duct with its own
# fire, acoustic and barrier consequences. Stated as a practical ceiling.
MAX_INLET_DIAMETER_MM = 125.0
# A design depression below the pressure a light breeze puts on a wall is not a
# pressure the cabin can be held at — the wind sets it, not the extract.
HOLDABLE_WIND_MS = 3.0

# --- heat ---------------------------------------------------------------
# Volumetric heat capacity of air: rho * cp / 3600 = 1.2 * 1005 / 3600.
AIR_HEAT_CAPACITY = 0.335   # W·h/(m3·K)
DELTA_T_K = 30.0            # 20 C inside, -10 C outside (Bergen winter design)
HEAT_RECOVERY = (0.0, 0.8)  # no recovery / a small residential unit

# --- the barrier the hole interrupts ---------------------------------------
WALL_THICKNESS_MM = 264.0   # the reference build-up, so the hole is a 264 mm air path
SD_BARRIER_M = 10.0         # the project's moisture strategy, §13-13

# --- candidate design depressions ------------------------------------------
DESIGN_PRESSURE_PA = (2.0, 5.0, 10.0, 15.0, 20.0)


def fmt(value, spec="+.0f"):
    """Format with a typographic minus, so the report matches the declaration."""
    return f"{value:{spec}}".replace("-", "−")


def fmt_signed(value, spec="+.0f"):
    """Same, but a true zero prints as 0 rather than +0."""
    if abs(value) < 1e-9:
        return "0"
    return fmt(value, spec)


def wind_pressure_pa(speed_ms):
    """Stagnation pressure of a wind on a wall: 0.5 · rho · v²."""
    return 0.5 * RHO_AIR * speed_ms ** 2


def orifice_area_m2(flow_m3h, dp_pa):
    """Area needed to pass `flow_m3h` at `dp_pa` through a Cd orifice."""
    if dp_pa <= 0.0:
        raise ValueError("an orifice needs a positive pressure difference")
    return (flow_m3h / 3600.0) / (CD * math.sqrt(2.0 * dp_pa / RHO_AIR))


def flow_through_area_m3h(area_m2, dp_pa):
    return 3600.0 * CD * area_m2 * math.sqrt(2.0 * dp_pa / RHO_AIR)


def diameter_mm(area_m2):
    return 2.0 * math.sqrt(area_m2 / math.pi) * 1000.0


def leakage_m3h(dp_pa, vol):
    """Envelope leakage at a depression — the same law the ventilation screen uses."""
    q50 = vt.N50_PER_H * vol["volume_m3"]
    return q50 * (dp_pa / vt.REFERENCE_PRESSURE_PA) ** vt.LEAKAGE_EXPONENT


def pressure_with_inlet(area_m2, extract_m3h, vol):
    """Cabin depression with a deliberate inlet of `area_m2` in parallel with leakage.

    Monotone in dp, so a bisection is exact enough and cannot pick the wrong root.
    """
    def residual(dp):
        return flow_through_area_m3h(area_m2, dp) + leakage_m3h(dp, vol) - extract_m3h

    lo, hi = 0.0, 5000.0
    if residual(hi) < 0.0:      # the inlet alone passes more than the extract
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if residual(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def required_area_m2(extract_m3h, dp_pa, vol):
    """Inlet area that holds the cabin at `dp_pa` while the extract runs."""
    return orifice_area_m2(extract_m3h - leakage_m3h(dp_pa, vol), dp_pa)


def heating_w(flow_m3h, recovery=0.0):
    """Tempering load for outdoor air at DELTA_T_K, net of heat recovery."""
    return AIR_HEAT_CAPACITY * flow_m3h * DELTA_T_K * (1.0 - recovery)


def diffusion_share(area_m2, barrier_m2):
    """The hole's diffusion conductance as a fraction of the barrier's.

    Conductance is area / Sd. The barrier is SD_BARRIER_M over `barrier_m2`; the
    hole is WALL_THICKNESS of plain air over `area_m2`. Only diffusion is counted
    — convective transfer through an opening is not a diffusion calculation and
    is not in this ratio at all.
    """
    sd_hole = WALL_THICKNESS_MM / 1000.0
    return (area_m2 / barrier_m2) * (SD_BARRIER_M / sd_hole)


def element_loss_w_per_k(openings_m2):
    """Sum of U·A over the envelope at the §14-3 limits, W/K.

    The denominator for "does the ventilation cost more than the fabric". It is
    the loss the envelope is *allowed* to have, not the loss of any build-up, so
    it is independent of R2. Areas are internal-face areas at the reference
    section, which understates the wall by roughly the build-up thickness; this
    is a comparison denominator, not an energy-frame calculation, and the energy
    screen should own it when one exists.
    """
    import envelope_check as ec

    a = ei.interior_timber_m2()
    opaque_wall = a["gross_m2"] - a["ceiling_m2"] - a["openings_m2"]
    return (opaque_wall * ec.U_LIMITS["wall"]
            + a["ceiling_m2"] * ec.U_LIMITS["roof"]
            + 18.0 * ec.U_LIMITS["floor"]
            + openings_m2 * ec.U_LIMITS["window"])


def screen():
    vol = vt.volume_m3()
    rates = vt.documented_rates()
    b = vt.balance()
    a = ei.interior_timber_m2()
    barrier_m2 = a["net_m2"]
    holdable_min = wind_pressure_pa(HOLDABLE_WIND_MS)

    # The pressure the cabin sits at today, with no deliberate inlet: the
    # deliverable boosted case is the one a fan can actually hold.
    worst = max((r for r in b["rows"] if r["deliverable"]), key=lambda r: r["pressure_pa"])

    rows = []
    # The inlet is sized for the DESIGN flow, which is the boosted one-room case:
    # that is when the cabin is under the most extract and when the flue matters
    # most. Sizing for the basic flow would leave the boosted case at a higher
    # depression than designed — the wrong way round.
    design_flow = rates["extract_boosted_one_m3h"]
    for dp in DESIGN_PRESSURE_PA:
        area = required_area_m2(design_flow, dp, vol)
        dia = diameter_mm(area)
        flue_worst = min(vt.FLUE_DRAUGHT_PA) - dp
        flue_best = max(vt.FLUE_DRAUGHT_PA) - dp
        band = 0.5 * (max(vt.FLUE_DRAUGHT_PA) - min(vt.FLUE_DRAUGHT_PA))
        rows.append({
            "design_pa": dp,
            "leakage_m3h": round(leakage_m3h(dp, vol), 1),
            "inlet_m3h": round(design_flow - leakage_m3h(dp, vol), 1),
            "area_cm2": round(area * 1e4, 1),
            "diameter_mm": round(dia, 0),
            "standard": dia <= MAX_INLET_DIAMETER_MM,
            "holdable": dp >= holdable_min,
            "flue_worst_pa": round(flue_worst, 1),
            "flue_best_pa": round(flue_best, 1),
            "flue_adequate": flue_worst > 0.0 and flue_worst > band,
        })

    buildable = [r for r in rows if r["standard"] and r["holdable"]]
    adequate = [r for r in rows if r["flue_adequate"]]
    # The design point this screen recommends for the ventilation: the LOWEST
    # depression that is still a standard size and holdable in wind. Lowest
    # pressure means the largest hole, which is the right trade — the hole costs
    # nothing that scales, and the pressure is what harms the flue and the radon
    # barrier. Choosing the smallest hole would pick the highest pressure.
    chosen = min(buildable, key=lambda r: r["design_pa"])
    chosen_area = chosen["area_cm2"] / 1e4

    # What the chosen inlet does to the two pressures that matter, each at its
    # own flow. Mixing the basic and boosted cases is how the first version of
    # this screen quoted a saving against a pressure it was not sized for.
    p_basic = pressure_with_inlet(chosen_area, rates["extract_basic_m3h"], vol)
    p_boost = pressure_with_inlet(chosen_area, rates["extract_boosted_one_m3h"], vol)
    sealed_basic = vt.pressure_for_flow(rates["extract_basic_m3h"], vol)

    heat_none = heating_w(rates["extract_basic_m3h"], HEAT_RECOVERY[0])
    heat_hr = heating_w(rates["extract_basic_m3h"], HEAT_RECOVERY[1])
    openings = a["openings_m2"]
    fabric_w_per_k = element_loss_w_per_k(openings)

    return {
        "state": "SCREENING — CONDITIONAL ON C-01. Not a ventilation design, not a "
                 "product selection, not a compliance statement.",
        "volume_m3": round(vol["volume_m3"], 1),
        "rates": rates,
        "orifice": {"cd": CD, "rho": RHO_AIR,
                    "law": "Q = 3600 · Cd · A · sqrt(2 · dp / rho)"},
        "barrier": {"net_m2": barrier_m2, "sd_m": SD_BARRIER_M,
                    "thickness_mm": WALL_THICKNESS_MM},
        "no_inlet": {"pressure_pa": worst["pressure_pa"], "mode": worst["mode"],
                     "basic_pa": round(sealed_basic, 1)},
        "design_flow_m3h": design_flow,
        "design": rows,
        "chosen": chosen,
        "chosen_pressure": {"basic_pa": round(p_basic, 1),
                            "boosted_one_pa": round(p_boost, 1),
                            "removed_basic_pa": round(sealed_basic - p_basic, 1),
                            "removed_boosted_pa": round(worst["pressure_pa"] - p_boost, 1)},
        # Does the conclusion depend on the 125 mm size limit? It must not: the
        # wind threshold alone has to exclude every adequate row, or the finding
        # is an artefact of a number this screen chose.
        "robust_without_size_limit": not any(r["flue_adequate"] and r["holdable"]
                                             for r in rows),
        "buildable_rows": len(buildable),
        "adequate_rows": len(adequate),
        "wind": {"holdable_min_pa": round(holdable_min, 1),
                 "at": [{"speed_ms": v, "pressure_pa": round(wind_pressure_pa(v), 1)}
                        for v in (3.0, 5.0, 10.0)]},
        "heat": {"basic_m3h": rates["extract_basic_m3h"],
                 "delta_t_k": DELTA_T_K,
                 "w_no_recovery": round(heat_none, 0),
                 "w_with_recovery": round(heat_hr, 0),
                 "recovery": HEAT_RECOVERY[1],
                 "fabric_w_per_k": round(fabric_w_per_k, 2),
                 "fabric_w": round(fabric_w_per_k * DELTA_T_K, 0),
                 "ratio_no_recovery": round(heat_none / (fabric_w_per_k * DELTA_T_K), 2),
                 "ratio_with_recovery": round(heat_hr / (fabric_w_per_k * DELTA_T_K), 2)},
        "diffusion": {"share_pct": round(diffusion_share(chosen_area, barrier_m2) * 100.0, 2),
                      "factor": SD_BARRIER_M / (WALL_THICKNESS_MM / 1000.0)},
        "radon": {"from_pa": round(sealed_basic, 1), "to_pa": round(p_basic, 1),
                  "reduction": round(sealed_basic / p_basic, 1)},
        "stove": {
            "room_sealed": True,
            "retires_row": 14,
            "reason": "a room-sealed appliance takes its combustion air from outside and "
                      "its flue is balanced against the outside, so cabin pressure no "
                      "longer appears in the draught",
            "requirement": "the stove must be room-sealed, or the flue must be balanced; "
                           "no make-up air design substitutes for this",
        },
    }


def markdown(m):
    ch = m["chosen"]
    cp = m["chosen_pressure"]
    h = m["heat"]
    d = m["diffusion"]
    r = m["radon"]
    w = m["wind"]
    no = m["no_inlet"]

    L = [
        "# MiniHouse · the make-up air, its size, and the flue it cannot rescue",
        "",
        f"**State:** {m['state']}",
        "",
        f"- Internal volume **{m['volume_m3']} m³** at the reference section.",
        f"- Extract basic **{m['rates']['extract_basic_m3h']:.0f} m³/h**, boosted one room "
        f"**{m['design_flow_m3h']:.0f} m³/h**. With no deliberate inlet the cabin sits at "
        f"**{no['basic_pa']:.0f} Pa** on the basic rate and **{no['pressure_pa']:.0f} Pa** "
        f"on the boosted one.",
        f"- The inlet is sized for the boosted case, which is when the cabin is under the "
        f"most extract and when the flue matters most.",
        f"- Orifice law {m['orifice']['law']}, Cd **{m['orifice']['cd']}**, air "
        f"**{m['orifice']['rho']} kg/m³**.",
        "- Generated by `scripts/aporte_aire.py`; JSON companion: "
        "`knowledge/comparisons/aporte-aire.json`.",
        "",
        "## 1. What this screen is for",
        "",
        "[The ventilation screen](verificacion-ventilacion.md) established that a fan in a "
        "sealed cabin does not move air, and ended on a decision rather than a number: the "
        "make-up air has to come from somewhere. That decision has a size, and the size is "
        "the whole of the design.",
        "",
        "It also left declaration row 14 at **−130 Pa** with no priced remedy. This screen "
        "prices the remedy, and then tests whether the price buys the row.",
        "",
        "## 2. The hole, sized",
        "",
        f"A deliberate inlet of area A passes `Q = 3600 · Cd · A · sqrt(2 · dp / rho)`. "
        f"Holding the cabin at a chosen depression while the design extract of "
        f"**{m['design_flow_m3h']:.0f} m³/h** runs fixes A, and A fixes the diameter:",
        "",
        "| Design depression Pa | Leakage m³/h | Inlet m³/h | Area cm² | Diameter mm | "
        "Standard size? | Holdable in wind? |",
        "|---:|---:|---:|---:|---:|:--:|:--:|",
    ]
    for row in m["design"]:
        L.append(
            f"| {row['design_pa']:.0f} | {row['leakage_m3h']:.1f} | {row['inlet_m3h']:.1f} | "
            f"{row['area_cm2']:.1f} | {row['diameter_mm']:.0f} | "
            f"{'yes' if row['standard'] else '**no**'} | "
            f"{'yes' if row['holdable'] else '**no**'} |")

    L += [
        "",
        f"\"Standard size\" means an inlet no larger than **{MAX_INLET_DIAMETER_MM:.0f} mm** "
        "across; beyond that it is a duct, with its own fire, acoustic and barrier "
        "consequences. \"Holdable\" means a depression at least as large as the pressure a "
        f"**{HOLDABLE_WIND_MS:.0f} m/s** breeze puts on a wall — "
        f"**{w['holdable_min_pa']:.1f} Pa**. Below that the wind sets the cabin pressure, "
        "not the extract, and the design point is a fiction.",
        "",
        f"The recommended inlet is therefore **{ch['diameter_mm']:.0f} mm** at "
        f"**{ch['design_pa']:.0f} Pa** of design depression: it holds the boosted case at "
        f"**{cp['boosted_one_pa']:.0f} Pa** and lets the basic case fall to "
        f"**{cp['basic_pa']:.0f} Pa**, removing **{cp['removed_basic_pa']:.0f} Pa** of the "
        f"**{no['basic_pa']:.0f} Pa** the basic extract would otherwise carry.",
        "",
        "The lowest buildable depression is the right choice, not the smallest hole: the "
        "hole costs nothing that scales, while the pressure is what harms the flue and the "
        "radon barrier. Choosing the smallest inlet would pick the highest pressure and "
        "call it efficiency.",
        "",
        "That is the ventilation solved, and it is one wall valve.",
        "",
        "## 3. The flue it cannot rescue",
        "",
        "The same table, read against the stove instead of the extract:",
        "",
        "| Design depression Pa | Flue margin, worst Pa | Flue margin, best Pa | "
        "Adequate by §2-2(3)? |",
        "|---:|---:|---:|:--:|",
    ]
    for row in m["design"]:
        L.append(f"| {row['design_pa']:.0f} | {fmt_signed(row['flue_worst_pa'])} | "
                 f"{fmt_signed(row['flue_best_pa'])} | "
                 f"{'yes' if row['flue_adequate'] else '**no**'} |")

    adq = [r for r in m["design"] if r["flue_adequate"]]
    if len(adq) == 1:
        adq_line = (f"The only depression that passes the test is **{adq[0]['design_pa']:.0f} Pa**, "
                    f"which needs a **{adq[0]['diameter_mm']:.0f} mm** inlet — larger than the "
                    f"size limit, and below the pressure a 3 m/s breeze puts on the same wall. "
                    "The inlet cannot hold it, so the row is not a design point, it is "
                    "arithmetic.")
    else:
        adq_line = (f"{len(adq)} depressions pass the test, and none of them is both "
                    "buildable and holdable in wind.")

    L += [
        "",
        "Adequacy here is the declaration's own test, applied to the worst end of the band: "
        "the margin must be **positive and larger than its uncertainty**. The draught is "
        "quoted as 10–20 Pa, so its half-width is 5 Pa, and the worst margin has to beat "
        "both 0 and 5.",
        "",
        f"**{'One of the five' if m['adequate_rows'] == 1 and len(m['design']) == 5 else str(m['adequate_rows']) + ' of ' + str(len(m['design']))} rows "
        f"{'passes' if m['adequate_rows'] == 1 else 'pass'} it, and "
        f"{m['buildable_rows']} rows are buildable.** The two sets do not intersect. "
        + adq_line,
        "",
        f"**That conclusion does not depend on the {MAX_INLET_DIAMETER_MM:.0f} mm size "
        f"limit.** Relax it and the {adq[0]['design_pa']:.0f} Pa row becomes a standard "
        "size, but it is still below the wind's own pressure, so the sets stay disjoint. "
        "The size limit only decides how much of the table is buildable; the wind decides "
        "that none of the adequate rows are.",
        "",
        "The reason is structural rather than numerical. **A passive inlet cannot hold a "
        "set pressure**, because the wind's own pressure is larger than any design value "
        "that would help the flue. The inlet is sized by the extract and the weather does "
        "the rest.",
        "",
        "## 4. Row 14 is retired, not improved",
        "",
        "A **room-sealed** stove takes its combustion air directly from outside and its "
        "flue is balanced against the outside, so the cabin's pressure no longer appears in "
        "the draught at all. That removes the coupling instead of shrinking it, and it is a "
        "procurement requirement with no dimensional cost — which makes it the only thing "
        "in this project that closes a negative safety margin for free.",
        "",
        f"**Row 14 therefore does not become positive; it stops being a margin.** The "
        "declaration must carry it as a requirement on the appliance, not as a number to "
        "be met by the envelope, and no make-up air design substitutes for it. That is a "
        "stronger statement than the screen can make about any other negative row, and it "
        "is worth having: the project's worst number has a fix, and the fix is a "
        "specification.",
        "",
        "## 5. What the hole costs in heat",
        "",
        "The make-up air arrives at outdoor temperature and has to be brought to room "
        "temperature. At the basic extract, over a 30 K design difference:",
        "",
        "| Case | Tempering load W | As a multiple of the fabric loss |",
        "|---|---:|---:|",
        f"| no heat recovery | **{h['w_no_recovery']:.0f}** | {h['ratio_no_recovery']:.2f} × |",
        f"| {h['recovery'] * 100:.0f} % recovery | **{h['w_with_recovery']:.0f}** | "
        f"{h['ratio_with_recovery']:.2f} × |",
        "",
        f"The fabric loss it is compared against is **{h['fabric_w_per_k']:.1f} W/K** — the "
        "§14-3 limits applied to the reference section's element areas — so "
        f"**{h['fabric_w']:.0f} W** over the same 30 K.",
        "",
        f"**The ventilation air costs {h['ratio_no_recovery']:.1f} times the fabric.** In an "
        "18 m² cabin that is not a line item, it is the design: without recovery the "
        "make-up air is the largest heat load in the building, and a heat-recovery unit is "
        "not an upgrade but a precondition for the extract rate being defensible.",
        "",
        "This number belongs to the energy frame, which the project has not built. It is "
        "recorded here because it is a consequence of the ventilation decision, and because "
        f"a **{h['w_no_recovery']:.0f} W** ventilation load in an 18 m² cabin is the kind "
        "of figure that should change a specification before it is discovered later.",
        "",
        "## 6. What the hole does to the barrier",
        "",
        f"The obvious fear is that a hole in the vapour barrier defeats the moisture "
        f"strategy. By diffusion it does not. Conductance is area over Sd, the barrier is "
        f"**Sd {m['barrier']['sd_m']:.0f} m** over **{m['barrier']['net_m2']:.1f} m²**, and "
        f"the hole is **{m['barrier']['thickness_mm']:.0f} mm** of plain air — a factor of "
        f"**{d['factor']:.0f}** in the hole's favour per unit area. The "
        f"**{ch['area_cm2']:.0f} cm²** inlet therefore carries "
        f"**{d['share_pct']:.1f} %** of the barrier's diffusion conductance.",
        "",
        "**A fraction of one per cent is not the problem.** The problem is that this ratio "
        "counts diffusion only. An opening is a convective path, and convective moisture "
        "transport through a defect carries far more vapour than diffusion — the same "
        "sentence [the 2D junction screen](verificacion-puente-2d.md) uses to explain what a "
        "conduction model cannot see. No Sd calculation reaches it, and neither does this "
        "one.",
        "",
        "So the inlet is **a control problem, not a diffusion problem**. It must be open "
        "when the extract runs and closed when it does not, which means a flap and a seal, "
        "not a bigger vapour resistance. The barrier penetration is unavoidable and must be "
        "a designed, closable, vapour-tight valve — and that is a different artefact from "
        "the one the moisture strategy has been assuming.",
        "",
        "## 7. What it does for §13-5",
        "",
        f"Sustained negative pressure is the mechanism that draws soil gas through the "
        f"floor. The inlet reduces it from **{r['from_pa']:.0f} Pa** to "
        f"**{r['to_pa']:.0f} Pa**, a factor of **{r['reduction']:.1f}**.",
        "",
        "That is a real mitigation and it does not assess radon. §13-5 still requires a "
        "concentration, and the barrier and the preparation for pressure reduction are "
        "still unbuilt. What changes is that the mitigation now has a size, and the size is "
        "one wall valve rather than a mechanical supply system.",
        "",
        "## 8. Limits",
        "",
        "- **Not a ventilation design.** No duct is sized, no fan selected, no valve "
        "chosen, no location fixed. This is one opening's area against one pressure.",
        "- Cd 0.6 is the optimistic end. A louvred valve with a filter and a flap is lower, "
        "which makes the hole **larger** than tabulated, not smaller.",
        "- The leakage law is the ventilation screen's: n = 0.65, generic, unmeasured.",
        "- The wind is treated as a static pressure. Real wind is gusty, and a gust on the "
        "intake face pressurises the cabin and reverses the flow through the inlet — which "
        "is a second reason a passive inlet is a control problem.",
        "- The flue draught 10–20 Pa is an assumption range, not a source value, and the "
        "adequacy verdict inherits its uncertainty.",
        "- The fabric loss is the §14-3 limits on internal-face areas. It is a denominator "
        "for comparison, not an energy-frame result.",
        "- Nothing here is a compliance statement, a product selection or a design release.",
        "",
        "## 9. Source and status",
        "",
        "- Extract rates and the leakage law: `scripts/ventilacion_check.py`.",
        "- Barrier area: `scripts/estrategia_incendio.py`, `interior_timber_m2()`.",
        "- U limits: `scripts/envelope_check.py`, §14-3.",
        "- §13-5 and §13-1(1): S023. Flue and stove clauses: S024, `scripts/instalaciones_check.py`.",
        "- Status: **screening**, conditional on C-01. The stove requirement is a "
        "specification input, not a selection.",
        "",
        "- Generated by `scripts/aporte_aire.py`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    m = screen()
    vol = {"volume_m3": m["volume_m3"]}

    # The orifice law must invert exactly, both ways.
    for flow in (30.0, 90.0, 216.0):
        for dp in (2.0, 10.0, 50.0):
            a = orifice_area_m2(flow, dp)
            assert abs(flow_through_area_m3h(a, dp) - flow) < 1e-9, (flow, dp)

    # Area must fall as the allowed depression rises: a bigger hole is a weaker
    # fan, not a stronger one.
    areas = [r["area_cm2"] for r in m["design"]]
    assert all(x > y for x, y in zip(areas, areas[1:])), areas

    # The no-inlet pressure must reproduce the ventilation screen's own figure.
    assert abs(m["no_inlet"]["pressure_pa"] - vt.stove_check()["worst_pressure_pa"]) < 0.2

    # A very large inlet must approach zero depression, and a zero inlet must
    # reproduce the sealed-cabin pressure at the SAME flow. These are the two
    # ends of the bisection, and comparing across flows is how this first failed.
    assert pressure_with_inlet(1.0, 90.0, vol) < 1.0
    basic = m["rates"]["extract_basic_m3h"]
    assert abs(pressure_with_inlet(0.0, basic, vol)
               - vt.pressure_for_flow(basic, vol)) < 0.2

    # The chosen row must be both buildable and holdable, and it must be the
    # LOWEST depression that is — the largest hole the size limit allows. If a
    # future edit flips this back to the smallest hole, it fails.
    ch = m["chosen"]
    assert ch["standard"] is True and ch["holdable"] is True, ch
    lower = [r for r in m["design"]
             if r["standard"] and r["holdable"] and r["design_pa"] < ch["design_pa"]]
    assert not lower, lower
    bigger = [r for r in m["design"]
              if r["standard"] and r["holdable"] and r["diameter_mm"] > ch["diameter_mm"]]
    assert not bigger, f"a larger buildable hole exists: {bigger}"

    # THE finding: the buildable set and the adequate set must not intersect.
    # If they ever do, make-up air has become a flue fix and the report is wrong.
    for row in m["design"]:
        if row["flue_adequate"]:
            assert not (row["standard"] and row["holdable"]), row
    assert m["adequate_rows"] >= 1 and m["buildable_rows"] >= 1

    # And the finding must survive dropping the size limit entirely: the wind,
    # not the 125 mm ceiling, is what excludes every adequate row.
    assert m["robust_without_size_limit"] is True, m["design"]

    # The margin must be reported against the band's half-width, not just zero.
    band = 0.5 * (max(vt.FLUE_DRAUGHT_PA) - min(vt.FLUE_DRAUGHT_PA))
    for row in m["design"]:
        expected = row["flue_worst_pa"] > 0.0 and row["flue_worst_pa"] > band
        assert row["flue_adequate"] is expected, row

    # Heat: recovery must reduce the load, and the ventilation must dominate the
    # fabric at 18 m². That is the claim the report makes in bold.
    h = m["heat"]
    assert h["w_with_recovery"] < h["w_no_recovery"]
    assert abs(h["w_no_recovery"] / h["w_with_recovery"] - 1.0 / (1.0 - h["recovery"])) < 0.02
    assert h["ratio_no_recovery"] > 1.0, h
    assert h["ratio_with_recovery"] < 0.5, h

    # Diffusion share must be small enough that the report's "one per cent" holds,
    # but not so small that the convective warning is unnecessary.
    assert 0.1 < m["diffusion"]["share_pct"] < 5.0, m["diffusion"]

    # The inlet must actually reduce the radon driving force by an order of
    # magnitude, or §7's claim is wrong.
    assert m["radon"]["reduction"] > 5.0, m["radon"]
    assert m["radon"]["to_pa"] < m["radon"]["from_pa"]

    # The stove must be declared room-sealed and tied to row 14 by number.
    assert m["stove"]["room_sealed"] is True
    assert m["stove"]["retires_row"] == 14

    # Wind: the holdable threshold must come from the wind law, not be typed.
    assert abs(m["wind"]["holdable_min_pa"] - wind_pressure_pa(HOLDABLE_WIND_MS)) < 0.05
    assert m["wind"]["at"][1]["pressure_pa"] > m["wind"]["holdable_min_pa"]

    # The fabric loss is the denominator the 2D report quotes, and that report
    # cannot import this one (it stays free of project imports). So the two must
    # be checked against each other here, or they will drift apart — which they
    # already had: the 2D report carried a hand-typed 19.4 against this 18.3.
    import puente_2d
    assert abs(puente_2d.ELEMENT_LOSS_W_PER_K - h["fabric_w_per_k"]) < 0.1, (
        puente_2d.ELEMENT_LOSS_W_PER_K, h["fabric_w_per_k"])

    print(f"Make-up air self-test OK: {m['volume_m3']} m³, no-inlet depression "
          f"{m['no_inlet']['pressure_pa']:.0f} Pa, a {ch['diameter_mm']:.0f} mm inlet at "
          f"{ch['design_pa']:.0f} Pa removes {m['chosen_pressure']['removed_basic_pa']:.0f} Pa, "
          f"{m['buildable_rows']} buildable rows and {m['adequate_rows']} adequate rows do "
          f"not intersect, ventilation heat {h['w_no_recovery']:.0f} W = "
          f"{h['ratio_no_recovery']:.1f} × the fabric, diffusion share "
          f"{m['diffusion']['share_pct']:.1f} %, and row 14 is retired by a room-sealed stove")


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
