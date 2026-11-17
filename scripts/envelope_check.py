#!/usr/bin/env python3
"""MiniHouse · envelope thermal and moisture screening (TEK17 §14-3 and §13-13).

The project has had moisture *principles* (S010) and TEK17 *limits* (S011, S023)
since the beginning, but no numbers that connect them. This script connects them:

  1. U-value of a layered construction, series resistances, with the correct
     surface resistances for wall, roof and floor — and with the **ventilated
     layer rule**: for a well-ventilated cavity, ISO 6946 says to ignore the
     cavity and everything outside it and to take the external surface
     resistance at the face bounding the cavity.
  2. The **parallel-path penalty** of timber studs, because §14-3's U-value is a
     whole-element value and a clear-field calculation flatters a stud wall.
  3. The insulation thickness actually needed to meet §14-3 once studs count.
  4. A steady-state **Glaser** moisture check: interface temperatures, saturation
     and actual vapour pressures, and where condensation would form.

The Glaser model is the textbook one: steady state, one-dimensional diffusion,
no convection, no capillary transport, no hygroscopic buffering. It is a screen
for "is this build-up obviously wrong", not a hygrothermal simulation. Every
number it produces depends on assumed material properties, which are generic
values, not manufacturer data.

Usage:
  python envelope_check.py --out-md fase1/verificacion-envolvente.md \
      --out-json knowledge/comparisons/envelope-check.json
  python envelope_check.py --selftest
"""
import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# TEK17 §14-3 absolute minimums (S011). Whole-element values, W/m2K.
U_LIMITS = {"wall": 0.22, "roof": 0.18, "floor": 0.18, "window": 1.20}

# Surface resistances, NS-EN ISO 6946 conventions, m2K/W.
SURFACES = {
    "wall": (0.13, 0.04),    # horizontal heat flow
    "roof": (0.10, 0.04),    # upward heat flow
    "floor": (0.17, 0.04),   # downward heat flow, ventilated underside
}

# Water vapour permeability of still air, kg/(m s Pa).
DELTA_0 = 2.0e-10

# Generic material properties. NOT manufacturer data; replace before use.
LAM_TIMBER = 0.13
LAM_MINERAL_WOOL = 0.035
LAM_WOOD_FIBRE = 0.050
MU_TIMBER = 50.0
MU_MINERAL_WOOL = 1.0
MU_WOOD_FIBRE = 5.0

# Stud fraction of the insulated layer, area basis. 45 mm studs at 600 c/c is
# 0.075; plates, lintels, noggings and junctions push the effective figure up.
STUD_FRACTIONS = (0.10, 0.15, 0.20)

# Design conditions for the diffusion check. Bergen winter, not a cold inland site.
T_IN, RH_IN = 20.0, 0.40
T_OUT, RH_OUT = 0.0, 0.85

# Alternative indoor humidity, to show how fast the margin disappears.
RH_IN_WET = 0.55

DAYS = 90.0


@dataclass
class Layer:
    """One layer of a construction, inside to outside."""
    name: str
    d_mm: float = 0.0
    lam: float | None = None      # W/(m K)
    r: float | None = None        # m2K/W, fixed (air layers)
    sd: float | None = None       # m, explicit vapour diffusion resistance
    mu: float | None = None       # -, sd = mu * d
    ventilated: bool = False      # well-ventilated cavity: truncates the build-up

    @property
    def r_value(self):
        if self.r is not None:
            return self.r
        if self.lam is None:
            raise ValueError(f"layer {self.name!r} has neither r nor lam")
        return (self.d_mm / 1000.0) / self.lam

    @property
    def sd_value(self):
        if self.sd is not None:
            return self.sd
        if self.mu is not None:
            return self.mu * self.d_mm / 1000.0
        return 0.0


def effective_layers(layers):
    """Layers up to, but not including, the first well-ventilated cavity.

    ISO 6946: for a well-ventilated air layer the thermal resistance of the
    layer and of all layers outside it is ignored, and the external surface
    resistance is taken at the face bounding the cavity. Getting this wrong
    counts the cladding and the cavity as insulation, which flatters the wall
    by roughly 0.02 W/m2K — enough to turn a marginal pass into a real one.
    """
    out = []
    for l in layers:
        if l.ventilated:
            break
        out.append(l)
    return out


def r_total(layers, r_si, r_se):
    return r_si + sum(l.r_value for l in effective_layers(layers)) + r_se


def u_value(layers, r_si, r_se):
    return 1.0 / r_total(layers, r_si, r_se)


def u_parallel_path(layers, idx, stud_fraction, lam_stud=LAM_TIMBER, r_si=0.13, r_se=0.04):
    """Whole-element U with a fraction of the insulated layer replaced by studs."""
    insulated = u_value(layers, r_si, r_se)
    alt = list(layers)
    ins = layers[idx]
    alt[idx] = Layer(f"{ins.name} (stud)", ins.d_mm, lam=lam_stud,
                     sd=ins.sd, mu=ins.mu)
    through_stud = u_value(alt, r_si, r_se)
    return stud_fraction * through_stud + (1.0 - stud_fraction) * insulated, through_stud


def min_insulation_thickness(target_u, layers, idx, lam_ins=LAM_MINERAL_WOOL,
                             r_si=0.13, r_se=0.04):
    """Insulation thickness needed to reach `target_u` in the clear field."""
    base = list(layers)
    ins = layers[idx]
    base[idx] = Layer(ins.name, 0.0, lam=lam_ins, sd=ins.sd, mu=ins.mu)
    r_other = r_total(base, r_si, r_se)
    r_needed = 1.0 / target_u - r_other
    if r_needed <= 0:
        return 0.0
    return r_needed * lam_ins * 1000.0


def min_thickness_with_studs(target_u, layers, idx, stud_fraction,
                             lam_ins=LAM_MINERAL_WOOL, lam_stud=LAM_TIMBER,
                             r_si=0.13, r_se=0.04, hi=600.0):
    """Bisection on thickness until the parallel-path U meets the target."""
    lo = 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        trial = list(layers)
        ins = layers[idx]
        trial[idx] = Layer(ins.name, mid, lam=lam_ins, sd=ins.sd, mu=ins.mu)
        u, _ = u_parallel_path(trial, idx, stud_fraction, lam_stud, r_si, r_se)
        if u > target_u:
            lo = mid
        else:
            hi = mid
    return hi


def p_sat(t_c):
    """Saturation vapour pressure, Magnus formula, Pa."""
    return 610.94 * math.exp(17.625 * t_c / (t_c + 243.04))


def glaser(layers, t_in=T_IN, rh_in=RH_IN, t_out=T_OUT, rh_out=RH_OUT,
           r_si=0.13, r_se=0.04):
    """Steady-state interface temperature and vapour pressure profile."""
    eff = effective_layers(layers)
    rt = r_si + sum(l.r_value for l in eff) + r_se
    p_in = rh_in * p_sat(t_in)
    p_out = rh_out * p_sat(t_out)
    sd_total = sum(l.sd_value for l in eff)

    nodes = []
    r_cum = r_si
    sd_cum = 0.0
    nodes.append({
        "name": "inner surface",
        "t_c": round(t_in - (r_cum / rt) * (t_in - t_out), 2),
        "sd_cum": 0.0,
        "p_pa": round(p_in, 1),
    })
    for l in eff:
        r_cum += l.r_value
        sd_cum += l.sd_value
        t = t_in - (r_cum / rt) * (t_in - t_out)
        p = p_in - (p_in - p_out) * (sd_cum / sd_total) if sd_total > 0 else p_in
        nodes.append({
            "name": f"after {l.name}",
            "t_c": round(t, 2),
            "sd_cum": round(sd_cum, 3),
            "p_pa": round(p, 1),
        })

    for n in nodes:
        n["p_sat_pa"] = round(p_sat(n["t_c"]), 1)
        n["ratio"] = round(n["p_pa"] / p_sat(n["t_c"]), 3) if p_sat(n["t_c"]) > 0 else None
        n["condensing"] = n["p_pa"] > p_sat(n["t_c"])

    first = next((n for n in nodes if n["condensing"]), None)
    result = {
        "t_in": t_in, "rh_in": rh_in, "t_out": t_out, "rh_out": rh_out,
        "p_in": round(p_in, 1), "p_out": round(p_out, 1),
        "sd_total_m": round(sd_total, 3),
        "r_total": round(rt, 3),
        "nodes": nodes,
        "condensation_at": first["name"] if first else None,
        "excess_pa": round(first["p_pa"] - first["p_sat_pa"], 1) if first else 0.0,
        "rate_kg_m2_90d": None,
    }
    if first:
        # Glaser condensation rate at the plane: inflow from inside minus
        # outflow to outside, both taken at the saturation pressure there.
        z_in = first["sd_cum"] / DELTA_0
        z_out = (sd_total - first["sd_cum"]) / DELTA_0
        g_in = (p_in - first["p_sat_pa"]) / z_in if z_in > 0 else 0.0
        g_out = (first["p_sat_pa"] - p_out) / z_out if z_out > 0 else 0.0
        rate = max(0.0, g_in - g_out)
        result["rate_kg_m2_s"] = rate
        result["rate_kg_m2_90d"] = round(rate * 86400.0 * DAYS, 3)
    return result


# --- constructions -----------------------------------------------------------

def wall(ins_mm=150.0, barrier_sd=10.0, wind_barrier_sd=None):
    """Reclaimed-timber rainscreen on a timber-stud wall, inside to outside."""
    wb = (Layer("wind barrier board", 12.0, lam=LAM_WOOD_FIBRE, mu=MU_WOOD_FIBRE)
          if wind_barrier_sd is None
          else Layer("wind barrier board", 12.0, lam=LAM_WOOD_FIBRE, sd=wind_barrier_sd))
    return [
        Layer("timber lining", 13.0, lam=LAM_TIMBER, mu=MU_TIMBER),
        Layer("vapour barrier", 0.2, r=0.0, sd=barrier_sd),
        Layer("mineral wool between studs", ins_mm, lam=LAM_MINERAL_WOOL, mu=MU_MINERAL_WOOL),
        wb,
        Layer("ventilated cavity", r=0.17, sd=0.0, ventilated=True),
        Layer("reclaimed timber cladding", 25.0, lam=LAM_TIMBER, mu=MU_TIMBER),
    ]


def roof(ins_mm=200.0, barrier_sd=10.0):
    return [
        Layer("timber ceiling lining", 13.0, lam=LAM_TIMBER, mu=MU_TIMBER),
        Layer("vapour barrier", 0.2, r=0.0, sd=barrier_sd),
        Layer("mineral wool between rafters", ins_mm, lam=LAM_MINERAL_WOOL, mu=MU_MINERAL_WOOL),
        Layer("roof board", 18.0, lam=LAM_TIMBER, mu=MU_TIMBER),
        Layer("underlay", 0.5, r=0.0, sd=0.5),
        Layer("ventilated cavity", r=0.20, sd=0.0, ventilated=True),
        Layer("standing-seam metal", 0.6, r=0.0, sd=0.0),
    ]


def floor(ins_mm=200.0):
    return [
        Layer("timber floor deck", 22.0, lam=LAM_TIMBER, mu=MU_TIMBER),
        Layer("mineral wool between joists", ins_mm, lam=LAM_MINERAL_WOOL, mu=MU_MINERAL_WOOL),
        Layer("structural board", 18.0, lam=LAM_TIMBER, mu=MU_TIMBER),
        Layer("ventilated void over chassis", r=0.17, sd=0.0, ventilated=True),
    ]


def screen():
    results = {"state": "SCREENING — GENERIC MATERIAL DATA, NO PRODUCTS SELECTED",
               "u_limits": U_LIMITS, "elements": {}}

    for kind, builder, idx, surf in (
        ("wall", wall, 2, "wall"),
        ("roof", roof, 2, "roof"),
        ("floor", floor, 1, "floor"),
    ):
        r_si, r_se = SURFACES[surf]
        base = builder()
        u_clear = u_value(base, r_si, r_se)
        entry = {
            "insulation_mm": base[idx].d_mm,
            "r_total": round(r_total(base, r_si, r_se), 3),
            "u_clear": round(u_clear, 3),
            "u_limit": U_LIMITS[kind],
            "clear_field_ok": u_clear <= U_LIMITS[kind],
            "layers": [{"name": l.name, "d_mm": l.d_mm, "r": round(l.r_value, 3),
                        "sd_m": round(l.sd_value, 3), "counted": not l.ventilated}
                       for l in base],
            "stud_cases": [],
            "min_clear_mm": round(min_insulation_thickness(U_LIMITS[kind], base, idx,
                                                           r_si=r_si, r_se=r_se), 1),
            "min_with_studs_mm": {},
        }
        for f in STUD_FRACTIONS:
            u_par, u_stud = u_parallel_path(base, idx, f, r_si=r_si, r_se=r_se)
            entry["stud_cases"].append({
                "stud_fraction": f,
                "u_stud_path": round(u_stud, 3),
                "u_parallel": round(u_par, 3),
                "ok": u_par <= U_LIMITS[kind],
                "penalty_pct": round((u_par / u_clear - 1.0) * 100.0, 1),
            })
            entry["min_with_studs_mm"][f"{f:.2f}"] = round(
                min_thickness_with_studs(U_LIMITS[kind], base, idx, f,
                                         r_si=r_si, r_se=r_se), 0)
        results["elements"][kind] = entry

    # Moisture: four build-ups that differ only in where the vapour resistance sits.
    scenarios = {
        "Sd 10 m barrier (TEK17 §13-13)": wall(barrier_sd=10.0),
        "Sd 2 m barrier (a weak retarder)": wall(barrier_sd=2.0),
        "no barrier, vapour-open wind barrier": wall(barrier_sd=0.0),
        "no barrier, tight sheathing Sd 2 m": wall(barrier_sd=0.0, wind_barrier_sd=2.0),
    }
    results["moisture"] = {}
    for label, layers in scenarios.items():
        dry = glaser(layers, rh_in=RH_IN)
        wet = glaser(layers, rh_in=RH_IN_WET)
        results["moisture"][label] = {
            "rh_in_40": {k: dry[k] for k in
                         ("sd_total_m", "condensation_at", "excess_pa", "rate_kg_m2_90d")},
            "rh_in_55": {k: wet[k] for k in
                         ("sd_total_m", "condensation_at", "excess_pa", "rate_kg_m2_90d")},
            "profile_rh40": dry["nodes"],
            "profile_rh55": wet["nodes"],
        }
    return results


def markdown(result):
    w = result["elements"]["wall"]
    r = result["elements"]["roof"]
    f = result["elements"]["floor"]
    lines = [
        "# MiniHouse · envelope thermal and moisture screening",
        "",
        "**State:** SCREENING — GENERIC MATERIAL DATA, NO PRODUCTS SELECTED. Not a thermal "
        "calculation of the built element, not a hygrothermal simulation and not a compliance "
        "certificate.",
        "",
        "- Limits: TEK17 **§14-3** (S011) — U wall ≤0.22, roof ≤0.18, floor ≤0.18, glazing ≤1.2 W/m²K.",
        "- Moisture requirement: TEK17 **§13-13** (S012/S023) — vapour barrier on the warm side, "
        "**Sd ≥ 10 m**, vapour-open wind barrier behind a ventilated cavity.",
        "- Physics: the four-condition moisture test from S010.",
        "- All λ and μ values are **generic**, not manufacturer data. They are good enough to size "
        "an envelope and not good enough to buy one.",
        "",
        "## 1. The build-ups as modelled",
        "",
        "Inside to outside. `R` is the layer resistance, `Sd` the vapour diffusion resistance. "
        "Rows marked *not counted* sit outside a well-ventilated cavity and are excluded from the "
        "U-value, as ISO 6946 requires.",
        "",
    ]
    for kind, entry in (("Wall", w), ("Roof", r), ("Floor", f)):
        lines += [
            f"**{kind}** — {entry['insulation_mm']:.0f} mm insulation, "
            f"R total {entry['r_total']:.2f} m²K/W",
            "",
            "| Layer | d mm | R m²K/W | Sd m | Counted |",
            "|---|---:|---:|---:|---|",
        ]
        for l in entry["layers"]:
            mark = "yes" if l["counted"] else "not counted"
            lines.append(f"| {l['name']} | {l['d_mm']:.1f} | {l['r']:.3f} | {l['sd_m']:.2f} | {mark} |")
        lines += ["", f"Clear-field U = **{entry['u_clear']:.3f}** W/m²K "
                      f"against a limit of **{entry['u_limit']:.2f}** "
                      f"({'PASS' if entry['clear_field_ok'] else 'FAIL'}).", ""]

    lines += [
        "## 2. The stud penalty — and why the clear-field number is a trap",
        "",
        "§14-3's U-value is a **whole-element** value. A timber-stud wall is a parallel path: the "
        "studs short-circuit the insulation, and the area they occupy is not small. The table below "
        "is the same element with a fraction of the insulated layer replaced by timber "
        f"(λ {LAM_TIMBER:.2f} W/mK against {LAM_MINERAL_WOOL:.3f} for mineral wool).",
        "",
        "| Element | Clear field | 10 % studs | 15 % | 20 % | Limit |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for kind, entry in (("Wall", w), ("Roof", r), ("Floor", f)):
        cells = []
        for case in entry["stud_cases"]:
            mark = "" if case["ok"] else " **FAIL**"
            cells.append(f"{case['u_parallel']:.3f}{mark}")
        lines.append(
            f"| {kind} | {entry['u_clear']:.3f} | " + " | ".join(cells) +
            f" | {entry['u_limit']:.2f} |"
        )
    lines += [
        "",
        f"**This is the finding that matters.** All three elements pass §14-3 on the clear field — "
        f"wall {w['u_clear']:.3f}, roof {r['u_clear']:.3f}, floor {f['u_clear']:.3f} W/m²K — and "
        f"**all three fail once the studs are counted**: at a 15 % stud fraction the wall goes to "
        f"{w['stud_cases'][1]['u_parallel']:.3f} (+{w['stud_cases'][1]['penalty_pct']:.0f} %), the "
        f"roof to {r['stud_cases'][1]['u_parallel']:.3f} and the floor to "
        f"{f['stud_cases'][1]['u_parallel']:.3f}. The penalty is 20–30 % for a detail that is "
        "invisible in a layer-by-layer calculation. Continuous insulation, a cross-battened service "
        "zone or an insulating sheathing board is not a refinement here — it is the difference "
        "between passing and failing.",
        "",
        "Insulation thickness needed to meet §14-3, clear field versus with studs:",
        "",
        "| Element | Clear field | 10 % studs | 15 % | 20 % |",
        "|---|---:|---:|---:|---:|",
    ]
    for kind, entry in (("Wall", w), ("Roof", r), ("Floor", f)):
        s = entry["min_with_studs_mm"]
        lines.append(
            f"| {kind} | {entry['min_clear_mm']:.0f} mm | {s['0.10']:.0f} mm | "
            f"{s['0.15']:.0f} mm | {s['0.20']:.0f} mm |"
        )
    lines += [
        "",
        f"The wall needs about **{w['min_with_studs_mm']['0.15']:.0f} mm** of mineral wool at a "
        f"15 % stud fraction, against **{w['min_clear_mm']:.0f} mm** in the clear field. That "
        "difference lands directly on the two constraints already identified elsewhere: the "
        "**2.2 m** room height of §12-7(2)(c) and the **4.00 m** transport screening value. "
        "**Envelope thickness is not a free parameter — it competes with both.** See "
        "[verificación de altura libre](verificacion-altura-libre.md).",
        "",
        "## 3. Moisture: where the vapour resistance sits decides everything",
        "",
        f"Steady state, {T_IN:.0f} °C indoors, {T_OUT:.0f} °C outdoors at {RH_OUT:.0%} RH — a "
        "Bergen winter, not a cold inland site. The diffusion path stops at the ventilated cavity, "
        "so the cladding and the cavity are outside it. A row is only dry if **no** interface "
        "reaches saturation.",
        "",
        "| Build-up | Total Sd | At RH 40 % | Rate, 90 d | At RH 55 % | Rate, 90 d |",
        "|---|---:|---|---:|---|---:|",
    ]
    for label, m in result["moisture"].items():
        a, b = m["rh_in_40"], m["rh_in_55"]
        a_where = a["condensation_at"] or "**dry**"
        b_where = b["condensation_at"] or "**dry**"
        a_rate = f"{a['rate_kg_m2_90d']:.2f} kg/m²" if a["rate_kg_m2_90d"] else "—"
        b_rate = f"{b['rate_kg_m2_90d']:.2f} kg/m²" if b["rate_kg_m2_90d"] else "—"
        lines.append(f"| {label} | {a['sd_total_m']:.2f} m | {a_where} | {a_rate} | {b_where} | {b_rate} |")

    keys = list(result["moisture"].keys())
    ref = result["moisture"][keys[0]]
    weak = result["moisture"][keys[1]]
    open_wb = result["moisture"][keys[2]]
    tight = result["moisture"][keys[3]]

    lines += [
        "",
        "The result is not the one the usual rule of thumb predicts, and it is worth reading "
        "carefully:",
        "",
        f"- **The §13-13 wall stays dry at both humidities.** With Sd 10 m almost the whole vapour "
        "pressure drop happens across the barrier, so the insulation and the wind barrier never see "
        f"a partial pressure above saturation. Total Sd {ref['rh_in_40']['sd_total_m']:.1f} m, "
        "condensation: none.",
        f"- **Weakening the barrier to Sd 2 m does not, on its own, cause condensation here** "
        f"(total Sd {weak['rh_in_40']['sd_total_m']:.2f} m, dry at 40 % and 55 %). Diffusion alone "
        "does not condemn a weak barrier when the cold side is open.",
        f"- **Removing the barrier entirely also stays dry** (total Sd "
        f"{open_wb['rh_in_40']['sd_total_m']:.2f} m), for the same reason: with a vapour-open "
        "wood-fibre wind barrier nothing traps the vapour, so nothing accumulates.",
        f"- **But the same barrier-free wall with a tight sheathing board (Sd 2 m) is the worst case "
        f"in the table** — {tight['rh_in_40']['rate_kg_m2_90d']:.2f} kg/m² over 90 days at 40 % RH "
        f"and {tight['rh_in_55']['rate_kg_m2_90d']:.2f} kg/m² at 55 %. That is the classic "
        "cold-climate error: a vapour-tight layer on the **cold** side. It is worse than having no "
        "barrier at all, because the vapour gets in and cannot get out.",
        "",
        "**So the four rows do not say that the vapour barrier is unnecessary.** They say that the "
        "dominant failure mode in this build-up is a **cold-side trap**, not a missing warm-side "
        "barrier — and that the wind barrier board, which nobody photographs and nobody specifies "
        "carefully, is the component that decides the answer.",
        "",
        "That distinction matters because **Glaser cannot see the other three moisture paths**. "
        "S010's four-condition test asks for moisture, a path, a force and a susceptible material; "
        "steady-state diffusion is only one path. Air leakage carries far more vapour than "
        "diffusion, and it is invisible to this model. A barrier-free wall that is dry in a Glaser "
        "calculation can still be wet in service because of a single unsealed penetration.",
        "",
        "Read §13-13 in that light and its Sd ≥ 10 m is not a diffusion calculation. It is a "
        "**robustness requirement**: it keeps the wall dry when the cold side is not as open as "
        "designed, when indoor humidity runs above the assumption, when the barrier is also doing "
        "air-barrier duty, and when the build-up is repeated by someone who has not read this "
        "report. The regulation is buying tolerance, not a number.",
        "",
        "Two corollaries the model does make visible:",
        "",
        "- **A service cavity between the barrier and the lining moves the barrier deeper and "
        "colder**, where the same Sd holds less margin. If a service zone is wanted, the barrier "
        "belongs in front of it, not behind.",
        "- **The wind barrier board is a design decision, not a commodity.** Swapping a vapour-open "
        "board for a foil-faced one converts a tolerable wall into the worst row of the table "
        "without changing anything visible.",
        "",
        "## 4. What this changes in the design",
        "",
        "1. **The wall thickness is now a number.** ~"
        f"{w['min_with_studs_mm']['0.15']:.0f} mm of mineral wool at 15 % studs, plus lining, "
        "barrier, wind barrier, cavity and cladding — of the order of 250–270 mm total. Two walls "
        "of that thickness take 500–540 mm out of a 3000 mm floor width.",
        "2. **The room-height and transport constraints tighten accordingly.** Floor and roof "
        "build-ups grow for the same reason, and the eave allowance at 20° with a 1100 mm stack is "
        "only 154 mm. This is the same collision from a different direction.",
        "3. **Continuous insulation or a cross-battened zone stops being optional** if the element "
        "is to stay under 0.22 W/m²K at a realistic stud fraction.",
        "4. **The steel chassis is a linear thermal bridge this script does not model.** A steel "
        "member crossing the floor insulation can dominate the junction. It needs a thermal-break "
        "detail; no Ψ value is claimed here.",
        "5. **The reclaimed timber is thermally almost irrelevant** — 25 mm of cladding is "
        "R ≈ 0.19 m²K/W, and outside the ventilated cavity it is not counted at all. Its role is "
        "weather, not insulation, which matches the brief's decision to keep it non-structural and "
        "reversible.",
        "",
        "## 5. Limits",
        "",
        "- **Generic λ and μ values.** No product has been selected; manufacturer data would move "
        "the U-values by a few percent — not the conclusions, but the exact thicknesses.",
        "- **Steady-state Glaser only.** No convection, no capillary redistribution, no hygroscopic "
        "buffering, no solar-driven inward diffusion, no rain penetration. A real hygrothermal "
        "assessment (WUFI or equivalent) is a specialist deliverable.",
        "- **One-dimensional.** Junctions, corners, the chassis and window reveals are where "
        "buildings actually fail, and none of them is in this model.",
        f"- **The design conditions are assumptions**: {T_IN:.0f} °C / {RH_IN:.0%} indoors and "
        f"{T_OUT:.0f} °C / {RH_OUT:.0%} outdoors. A Bergen winter mean is not the same as a "
        "diffusion design case.",
        "- **No energy-frame calculation.** §14-2 does not apply on the likely routes (S020/S021), "
        "so this is an element-level check against §14-3, not an energy performance result.",
        "- Nothing here is a compliance certificate, a product specification or a fabrication release.",
        "",
        "## 6. Source and status",
        "",
        "- TEK17 §14-3 U-values: S011. §13-13 vapour barrier and cavity: S012, S023.",
        "- Moisture mechanisms: S010.",
        "- Ventilated-layer treatment: ISO 6946 convention, applied here as a modelling rule.",
        "- Generated by `scripts/envelope_check.py`; JSON companion: "
        "`knowledge/comparisons/envelope-check.json`.",
        "- SCREENING ONLY — no construction fixed, no product approved.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # A single 100 mm layer of lambda 0.04 has R = 2.5.
    one = [Layer("x", 100.0, lam=0.04)]
    assert abs(r_total(one, 0.0, 0.0) - 2.5) < 1e-9
    assert abs(u_value(one, 0.0, 0.0) - 0.4) < 1e-9
    # Doubling the thickness halves U when surfaces are ignored.
    two = [Layer("x", 200.0, lam=0.04)]
    assert abs(u_value(two, 0.0, 0.0) - 0.2) < 1e-9
    # Surface resistances only ever lower U.
    assert u_value(one, 0.13, 0.04) < u_value(one, 0.0, 0.0)
    # Sd from mu and thickness.
    assert abs(Layer("y", 25.0, lam=0.13, mu=50).sd_value - 1.25) < 1e-12
    # The ventilated layer truncates the build-up: layers outside it are dropped.
    stack = [Layer("a", 100.0, lam=0.04),
             Layer("cavity", r=0.17, sd=0.0, ventilated=True),
             Layer("b", 100.0, lam=0.04)]
    assert len(effective_layers(stack)) == 1
    assert abs(u_value(stack, 0.0, 0.0) - 0.4) < 1e-9
    # Ignoring the ventilated rule would have counted the outer layer and the
    # cavity, giving a lower U. Confirm the direction of the correction.
    naive = [Layer("a", 100.0, lam=0.04), Layer("cavity", r=0.17), Layer("b", 100.0, lam=0.04)]
    assert u_value(naive, 0.0, 0.0) < u_value(stack, 0.0, 0.0)
    # Parallel path lies between the clear-field and the all-stud value.
    layers = wall(150.0)
    u_clear = u_value(layers, 0.13, 0.04)
    u_par, u_stud = u_parallel_path(layers, 2, 0.15)
    assert u_clear < u_par < u_stud
    # A larger stud fraction is always worse.
    assert u_parallel_path(layers, 2, 0.20)[0] > u_parallel_path(layers, 2, 0.10)[0]
    # Minimum thickness rises with the stud fraction, and the solver meets the target.
    t10 = min_thickness_with_studs(0.22, layers, 2, 0.10)
    t20 = min_thickness_with_studs(0.22, layers, 2, 0.20)
    assert t20 > t10 > 0.0
    assert u_parallel_path(wall(round(t20)), 2, 0.20)[0] <= 0.22 + 1e-3
    # Magnus formula anchors. The 17.625/243.04 coefficient set gives 2333.4 Pa
    # at 20 C against the tabulated 2339 Pa; a 0.25 % difference, irrelevant here.
    assert abs(p_sat(0.0) - 611.0) < 2.0
    assert abs(p_sat(20.0) - 2339.0) < 10.0
    assert p_sat(-10.0) < p_sat(0.0) < p_sat(10.0)
    # Profiles are monotone from inside to outside.
    prof = glaser(wall(150.0))["nodes"]
    ps = [n["p_pa"] for n in prof]
    ts = [n["t_c"] for n in prof]
    assert all(ps[i] >= ps[i + 1] - 1e-9 for i in range(len(ps) - 1))
    assert all(ts[i] >= ts[i + 1] - 1e-9 for i in range(len(ts) - 1))
    # The diffusion path stops at the ventilated cavity: the cladding is not a node.
    assert not any("cladding" in n["name"] for n in prof)
    # The §13-13 wall is dry at 40 %; a tight cold-side sheathing is not.
    assert glaser(wall(150.0, barrier_sd=10.0), rh_in=0.40)["condensation_at"] is None
    assert glaser(wall(150.0, barrier_sd=0.0, wind_barrier_sd=2.0),
                  rh_in=0.55)["condensation_at"] is not None
    # A wetter interior can only make things worse or equal.
    wet = glaser(wall(150.0, barrier_sd=10.0), rh_in=0.55)
    dry = glaser(wall(150.0, barrier_sd=10.0), rh_in=0.40)
    assert wet["excess_pa"] >= dry["excess_pa"]
    result = screen()
    assert set(result["elements"]) == {"wall", "roof", "floor"}
    assert len(result["moisture"]) == 4
    print("Envelope self-test OK: layered R/U, ventilated-layer truncation, parallel-path "
          "penalty, thickness solver, Magnus anchors, monotone profiles and the "
          "barrier comparison all pass")


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
