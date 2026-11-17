#!/usr/bin/env python3
"""MiniHouse · thermal-bridge screen (CONCEPTUAL — NO JUNCTION DETAIL DRAWN).

The envelope screen (`envelope_check.py`) establishes that the wall, roof and
floor meet §14-3 once the stud penalty is counted. It then says, in as many
words, that the steel chassis is a linear thermal bridge it does not model.
Four places in the repository flag that junction and none quantifies it. This
script does.

Three things make this worth its own calculation rather than a footnote:

1. **§14-3 sets no thermal-bridge limit.** The only numeric figure in the
   retrieved regulation is the normalised value **≤ 0.05 W/m²K**, and it sits in
   §14-2's alternative "energy measures" route, which §14-5(1) exempts for a
   detached building up to 70 m². So on the applying route the element U-values
   and the airtightness are capped and the junctions are not. A building can
   pass every §14-3 number and still lose a large share of its heat at the
   joints, and the regulation will not object.

2. **A small building is dominated by its perimeter.** Normalised bridge length
   scales roughly as 1/sqrt(area), so an 18 m² cabin carries about three times
   the linear detail per square metre that a 150 m² dwelling does, with
   identical detailing. The requirement set is weakest exactly where the
   building type is most exposed.

3. **Compensating the junctions with insulation is arithmetically possible but
   priced in centimetres.** Holding total heat loss constant scales every
   element U by (H_elements - H_bridges)/H_elements, and the envelope solver
   then says what that scale costs in mineral wool. The answer is a wall that
   grows by tens of millimetres of thickness it does not have room for, which
   collides with the 2.2 m room height and the 4.00 m transport limit already
   binding the section. So the junction has to be *designed*, and the reason is
   geometric, not arithmetic.

The Ψ values below are **generic screening ranges from ordinary practice**, not
project data and not a calculation. Real values require a 2D calculation to
NS-EN ISO 10211 on a drawn detail, which does not exist. Nothing here selects a
junction, a chassis or a build-up.

Usage:
  python puentes_termicas.py --out-md fase1/verificacion-puentes-termicas.md \
      --out-json knowledge/comparisons/puentes-termicas.json
  python puentes_termicas.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from envelope_check import floor, min_thickness_with_studs, roof, wall  # noqa: E402
from section_options import reference_deficit_mm  # noqa: E402

LENGTH_MM = 6000.0
WIDTH_MM = 3000.0
PLAN_AREA_M2 = (LENGTH_MM / 1000.0) * (WIDTH_MM / 1000.0)   # 18.0
PERIMETER_M = 2.0 * (LENGTH_MM + WIDTH_MM) / 1000.0          # 18.0
WALL_HEIGHT_MM = 2200.0   # nominal; the corner length scales with the R2 option
REF_PITCH_DEG = 20.0      # consistent with section_options.py

# Apertures from fase1/tabla-aberturas.csv (R0, conceptual).
OPENINGS = (
    ("P-01 door", 900.0, 2050.0),
    ("V-01 living", 1200.0, 1100.0),
    ("V-02 kitchen", 1000.0, 900.0),
    ("V-03 bathroom", 500.0, 500.0),
)

# Element U-values of the §14-3-COMPLIANT build-ups at a 15 % stud fraction.
# These are the limits themselves: the envelope screen shows that 141 mm of
# mineral wool gives 0.267 and fails, so the wall is built at ~189 mm to reach
# 0.22. Using the failing 141 mm values here would overstate the element loss.
U_WALL_STUD = 0.22
U_ROOF_STUD = 0.18
U_FLOOR_STUD = 0.18
U_GLAZING = 1.2           # §14-3 limit, used as the glazing value
STUD_FRACTION = 0.15

# §14-2 alternative route, NOT applicable here (§14-5(1)). Voluntary benchmark.
BENCHMARK_PSI_PRIME = 0.05  # W/m2K, normalised

# Generic screening ranges — ordinary practice, NOT project data.
PSI_SCENARIOS = {
    "poor":     {"floor": 0.20, "eave": 0.10, "corner": 0.05, "reveal": 0.08},
    "ordinary": {"floor": 0.10, "eave": 0.05, "corner": 0.03, "reveal": 0.05},
    "good":     {"floor": 0.05, "eave": 0.03, "corner": 0.02, "reveal": 0.03},
}

# Reference plan sizes, to isolate the size effect at constant detailing.
REFERENCE_AREAS_M2 = (18.0, 50.0, 100.0, 150.0)


def opening_area_m2():
    return sum(w * h for _, w, h in OPENINGS) / 1e6


def opening_perimeter_m():
    return sum(2.0 * (w + h) for _, w, h in OPENINGS) / 1000.0


def wall_height_m():
    return WALL_HEIGHT_MM / 1000.0


def wall_net_area_m2():
    return PERIMETER_M * wall_height_m() - opening_area_m2()


def roof_area_m2(pitch_deg=REF_PITCH_DEG):
    return PLAN_AREA_M2 / math.cos(math.radians(pitch_deg))


def junction_lengths_m():
    """Linear detail by type, in metres."""
    return {
        "floor / chassis perimeter": PERIMETER_M,
        "eave (wall to roof)": PERIMETER_M,
        "external corner (4 x wall height)": 4.0 * wall_height_m(),
        "opening reveals": opening_perimeter_m(),
    }


def heat_loss_elements_w_per_k():
    """Sum U*A over the envelope, glazing at the §14-3 limit."""
    return (U_WALL_STUD * wall_net_area_m2()
            + U_ROOF_STUD * roof_area_m2()
            + U_FLOOR_STUD * PLAN_AREA_M2
            + U_GLAZING * opening_area_m2())


def psi_prime_w_m2k(psi, lengths=None, area=PLAN_AREA_M2):
    """Normalised thermal bridge value: sum(psi * l) / heated floor area."""
    lengths = lengths or junction_lengths_m()
    total = (psi["floor"] * lengths["floor / chassis perimeter"]
             + psi["eave"] * lengths["eave (wall to roof)"]
             + psi["corner"] * lengths["external corner (4 x wall height)"]
             + psi["reveal"] * lengths["opening reveals"])
    return total / area


def bridge_loss_w_per_k(psi, lengths=None):
    lengths = lengths or junction_lengths_m()
    return (psi["floor"] * lengths["floor / chassis perimeter"]
            + psi["eave"] * lengths["eave (wall to roof)"]
            + psi["corner"] * lengths["external corner (4 x wall height)"]
            + psi["reveal"] * lengths["opening reveals"])


def bridge_share(psi):
    h_el = heat_loss_elements_w_per_k()
    h_br = bridge_loss_w_per_k(psi)
    return h_br / (h_el + h_br)


def square_perimeter_m(area_m2):
    """Perimeter of a square plan of the given area, for the size comparison."""
    return 4.0 * math.sqrt(area_m2)


def square_psi_prime(psi, area_m2, wall_height_m_=None):
    """Normalised bridge value for a square plan of the given area.

    The same detailing, scaled to a different footprint, so the size effect is
    isolated from every other variable.
    """
    h = wall_height_m_ or wall_height_m()
    side = math.sqrt(area_m2)
    perimeter = square_perimeter_m(area_m2)
    reveal = opening_perimeter_m() * (perimeter / PERIMETER_M)
    total = (psi["floor"] * perimeter + psi["eave"] * perimeter
             + psi["corner"] * 4.0 * h + psi["reveal"] * reveal)
    return total / area_m2


def max_mean_psi_for_benchmark(benchmark=BENCHMARK_PSI_PRIME):
    """Average psi the linear detail would have to reach to hit the benchmark."""
    total_length = sum(junction_lengths_m().values())
    return benchmark * PLAN_AREA_M2 / total_length


ELEMENTS = (
    ("wall", U_WALL_STUD, wall, 2),
    ("roof", U_ROOF_STUD, roof, 2),
    ("floor", U_FLOOR_STUD, floor, 1),
)


def baseline_thicknesses():
    """Insulation thickness each element needs at its own §14-3 target, 15 % studs."""
    return {name: min_thickness_with_studs(u, build(), idx, STUD_FRACTION)
            for name, u, build, idx in ELEMENTS}


def compensation_test(psi):
    """Cost of offsetting the bridge loss by insulation, in millimetres.

    Holding the total heat loss constant means scaling every element U by
    f = (H_elements - H_bridges) / H_elements. If f <= 0 no amount of
    insulation can offset the bridges. Otherwise the envelope solver gives the
    thickness that each element would need at its scaled target U, and the
    difference against the baseline is what the junction actually costs.
    """
    h_el = heat_loss_elements_w_per_k()
    h_br = bridge_loss_w_per_k(psi)
    scale = (h_el - h_br) / h_el
    base = baseline_thicknesses()
    out = {
        "bridge": psi_prime_w_m2k(psi),
        "bridge_loss_w_per_k": h_br,
        "element_scale": scale,
        "feasible": scale > 0.0,
        "elements": {},
    }
    for name, u_now, build, idx in ELEMENTS:
        target = u_now * scale if scale > 0.0 else 0.0
        if scale > 0.0:
            thick = min_thickness_with_studs(target, build(), idx, STUD_FRACTION)
        else:
            thick = None
        out["elements"][name] = {
            "u_now": u_now,
            "u_target": target,
            "ins_mm_baseline": base[name],
            "ins_mm_needed": thick,
            "delta_mm": None if thick is None else thick - base[name],
        }
    return out


def round_compensation(comp):
    """Serialise the nested compensation result without rounding dicts."""
    out = {
        "bridge": round(comp["bridge"], 4),
        "bridge_loss_w_per_k": round(comp["bridge_loss_w_per_k"], 3),
        "element_scale": round(comp["element_scale"], 4),
        "feasible": comp["feasible"],
        "elements": {},
    }
    for name, el in comp["elements"].items():
        out["elements"][name] = {
            "u_now": el["u_now"],
            "u_target": round(el["u_target"], 4),
            "ins_mm_baseline": round(el["ins_mm_baseline"], 1),
            "ins_mm_needed": None if el["ins_mm_needed"] is None
            else round(el["ins_mm_needed"], 1),
            "delta_mm": None if el["delta_mm"] is None else round(el["delta_mm"], 1),
        }
    return out


def screen():
    lengths = junction_lengths_m()
    scenarios = []
    for name, psi in PSI_SCENARIOS.items():
        scenarios.append({
            "scenario": name,
            "psi": psi,
            "psi_prime_w_m2k": round(psi_prime_w_m2k(psi), 4),
            "times_benchmark": round(psi_prime_w_m2k(psi) / BENCHMARK_PSI_PRIME, 2),
            "bridge_loss_w_per_k": round(bridge_loss_w_per_k(psi), 3),
            "bridge_share": round(bridge_share(psi), 4),
            "compensation": round_compensation(compensation_test(psi)),
        })

    size_effect = []
    for area in REFERENCE_AREAS_M2:
        size_effect.append({
            "area_m2": area,
            "square_perimeter_m": round(square_perimeter_m(area), 2),
            "perimeter_per_m2": round(square_perimeter_m(area) / area, 4),
            "psi_prime_ordinary": round(square_psi_prime(PSI_SCENARIOS["ordinary"], area), 4),
        })

    return {
        "revision": "PUENTES-TERMICAS",
        "state": "CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO PSI CALCULATED, NO PRODUCT SELECTED",
        "units": "m, m2, W/m2K, W/mK, W/K",
        "basis": {
            "plan_m": [LENGTH_MM / 1000.0, WIDTH_MM / 1000.0],
            "plan_area_m2": PLAN_AREA_M2,
            "perimeter_m": PERIMETER_M,
            "wall_height_mm": WALL_HEIGHT_MM,
            "ref_pitch_deg": REF_PITCH_DEG,
            "benchmark_psi_prime_w_m2k": BENCHMARK_PSI_PRIME,
            "benchmark_note": (
                "§14-2 alternative energy-measures route, exempt for a detached building "
                "up to 70 m2 under §14-5(1). §14-3 sets NO thermal-bridge limit. The "
                "benchmark is therefore voluntary on the applying route."
            ),
            "u_values": {
                "wall_stud_15pct": U_WALL_STUD, "roof_stud_15pct": U_ROOF_STUD,
                "floor_stud_15pct": U_FLOOR_STUD, "glazing": U_GLAZING,
            },
            "sources": ["S011", "S021", "S029"],
        },
        "junctions": {k: round(v, 3) for k, v in lengths.items()},
        "junction_total_m": round(sum(lengths.values()), 3),
        "areas": {
            "wall_net_m2": round(wall_net_area_m2(), 3),
            "roof_m2": round(roof_area_m2(), 3),
            "floor_m2": PLAN_AREA_M2,
            "openings_m2": round(opening_area_m2(), 4),
        },
        "heat_loss_elements_w_per_k": round(heat_loss_elements_w_per_k(), 3),
        "scenarios": scenarios,
        "size_effect": size_effect,
        "max_mean_psi_for_benchmark": round(max_mean_psi_for_benchmark(), 5),
        "excluded": [
            "2D/3D psi calculation", "junction detail", "chassis profile",
            "airtightness", "moisture risk at the junction", "product selection",
        ],
    }


def markdown(model):
    b = model["basis"]
    L = [
        "# MiniHouse · thermal bridges and the chassis junction",
        "",
        "**State:** CONCEPTUAL — NO JUNCTION DETAIL DRAWN, NO Ψ CALCULATED, NO PRODUCT SELECTED.",
        "The envelope screen meets §14-3 on all three elements and then says it does not model "
        "the steel chassis ([S011](../knowledge/sources/S011.md)). This report quantifies what "
        "that omission is worth.",
        "",
        "## 1. The regulation does not cap the junctions on this route",
        "",
        "This is the finding that makes the rest matter. TEK17's only numeric thermal-bridge "
        "figure is the **normalised value ≤ 0.05 W/m²K**, and it appears in **§14-2's** "
        "alternative energy-measures route. **§14-5(1) exempts a detached building up to 70 m² "
        "from §14-2.** **§14-3 sets no thermal-bridge limit** — the route that *does* apply "
        "caps the element U-values and the airtightness and says nothing about linear bridges.",
        "",
        "So on the applying route:",
        "",
        "| Check | Capped? |",
        "|---|---|",
        "| U wall 0.22 / roof 0.18 / floor 0.18 / glazing 1.2 | **yes**, §14-3 |",
        "| Air leakage 1.5 h⁻¹ @50 Pa | **yes**, §14-3 |",
        "| Normalised thermal bridge value | **no** — the 0.05 figure is in the exempt §14-2 route |",
        "",
        "A building can therefore pass every §14-3 number while losing a large share of its heat "
        "at the joints, and the regulation will not object. The 0.05 figure is still the best "
        "benchmark available, and this report uses it — but as a **voluntary target, not a "
        "compliance obligation**, and it is labelled that way throughout.",
        "",
        "## 2. The junction inventory",
        "",
        f"Footprint {b['plan_m'][0]:.1f} × {b['plan_m'][1]:.1f} m, so **{b['perimeter_m']:.1f} m** "
        f"of perimeter against **{b['plan_area_m2']:.1f} m²** of floor. A nominal "
        f"{b['wall_height_mm']:.0f} mm wall height and the R0 aperture table give:",
        "",
        "| Junction | Length m |",
        "|---|---:|",
    ]
    for key, value in model["junctions"].items():
        L.append(f"| {key} | {value:.2f} |")
    L += [
        f"| **total linear detail** | **{model['junction_total_m']:.2f}** |",
        "",
        f"That is **{model['junction_total_m'] / b['plan_area_m2']:.2f} m of linear detail per "
        "square metre of floor**, and it is the quantity that decides whether the junctions "
        "matter. The floor perimeter alone is as long as the whole building.",
        "",
        "## 3. What ordinary detailing costs",
        "",
        "Ψ values below are **generic screening ranges from ordinary practice — not project "
        "data and not a calculation.** Real values need a 2D analysis to NS-EN ISO 10211 on a "
        "drawn detail, and no detail exists.",
        "",
        "| Detailing | Ψ floor / eave / corner / reveal | Ψ″ W/m²K | × benchmark | Bridge loss W/K | Share of heat loss |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for s in model["scenarios"]:
        psi = s["psi"]
        L.append(
            f"| **{s['scenario']}** | {psi['floor']:.2f} / {psi['eave']:.2f} / "
            f"{psi['corner']:.2f} / {psi['reveal']:.2f} | {s['psi_prime_w_m2k']:.3f} | "
            f"**{s['times_benchmark']:.1f}×** | {s['bridge_loss_w_per_k']:.2f} | "
            f"{s['bridge_share']*100:.0f} % |"
        )

    L += [
        "",
        f"Element heat loss for comparison: **{model['heat_loss_elements_w_per_k']:.2f} W/K**, "
        "from the §14-3-compliant build-ups at a 15 % stud fraction.",
        "",
        "**Even the good column is 2.3× the benchmark.** Ordinary detailing lands at just over "
        "four times it and poor detailing at eight. There is no reading of this table in which "
        "the junctions are a footnote.",
        "",
        "## 4. The size effect, isolated",
        "",
        "Normalised bridge length scales roughly as 1/√area. Holding the **same detailing** and "
        "varying only the footprint:",
        "",
        "| Floor area m² | Square perimeter m | Perimeter per m² | Ψ″ at ordinary detailing |",
        "|---:|---:|---:|---:|",
    ]
    for row in model["size_effect"]:
        L.append(f"| {row['area_m2']:.0f} | {row['square_perimeter_m']:.1f} | "
                 f"{row['perimeter_per_m2']:.2f} | {row['psi_prime_ordinary']:.3f} |")

    cabin = model["size_effect"][0]
    big = model["size_effect"][-1]
    L += [
        "",
        f"The 18 m² cabin carries **{cabin['perimeter_per_m2'] / big['perimeter_per_m2']:.1f}×** "
        f"the perimeter per square metre of a 150 m² dwelling, and its Ψ″ is "
        f"**{cabin['psi_prime_ordinary'] / big['psi_prime_ordinary']:.1f}×** as large with "
        "identical detailing. The requirement set is weakest exactly where this building type "
        "is most exposed — and the exemption in §14-5(1) removes the one limit that would have "
        "noticed.",
        "",
        "A second, smaller point: the 6:2 aspect ratio costs about "
        f"**{(b['perimeter_m'] / square_perimeter_m(b['plan_area_m2']) - 1) * 100:.0f} %** more "
        "perimeter than a square of the same area. A squarer plan would be thermally cheaper, "
        "which is worth remembering when the 6 m length is a transport decision rather than an "
        "architectural one.",
        "",
        "## 5. What compensation would cost, in millimetres",
        "",
        "The first version of this section claimed the junctions *cannot* be offset by "
        "insulation. That was wrong, and the self-test in this script is what caught it: "
        "holding total heat loss constant only asks the elements to absorb the bridge loss by "
        "scaling every element U by",
        "",
        "```",
        "f = (H_elements − H_bridges) / H_elements",
        "```",
        "",
        "which stays positive at all three detailing levels. Compensation is therefore "
        "arithmetically open. The envelope solver prices it:",
        "",
        "| Detailing | f | Wall +mm | Roof +mm | Floor +mm |",
        "|---|---:|---:|---:|---:|",
    ]
    for s in model["scenarios"]:
        c = s["compensation"]
        el = c["elements"]
        L.append(f"| **{s['scenario']}** | {c['element_scale']:.3f} | "
                 f"+{el['wall']['delta_mm']:.0f} | +{el['roof']['delta_mm']:.0f} | "
                 f"+{el['floor']['delta_mm']:.0f} |")

    ordinary = next(s for s in model["scenarios"] if s["scenario"] == "ordinary")
    o_el = ordinary["compensation"]["elements"]
    roof_delta = o_el["roof"]["delta_mm"]
    roof_vert = roof_delta / math.cos(math.radians(REF_PITCH_DEG))
    L += [
        "",
        f"At ordinary detailing the wall grows from **{o_el['wall']['ins_mm_baseline']:.0f} to "
        f"{o_el['wall']['ins_mm_needed']:.0f} mm**, the roof from "
        f"{o_el['roof']['ins_mm_baseline']:.0f} to {o_el['roof']['ins_mm_needed']:.0f} mm and "
        f"the floor from {o_el['floor']['ins_mm_baseline']:.0f} to "
        f"{o_el['floor']['ins_mm_needed']:.0f} mm.",
        "",
        "**The roof is the one that closes the door.** A roof build-up costs its thickness "
        "divided by cos θ in the vertical direction, so "
        f"+{roof_delta:.0f} mm of mineral wool costs "
        f"**{roof_vert:.0f} mm of eave height**. The section solver already shows the eave "
        "landing near 1785 mm against a 2200 mm requirement — a deficit of "
        f"**{reference_deficit_mm():.0f} mm**. Compensating the roof alone would consume about "
        f"**{roof_vert / reference_deficit_mm() * 100:.0f} %** of "
        "that deficit, and the wall's extra 53 mm eats into the 18 m² gross area in plan.",
        "",
        "So the honest statement is narrower than the one this report first made, and stronger: "
        "**compensation is arithmetically available and geometrically closed.** Insulation "
        "thickness is not a lever the section has room to pull. **The junction has to be "
        "designed, not offset** — and the reason is the room height and the transport limit, "
        "not the arithmetic.",
        "",
        "## 6. The benchmark is the wrong instrument for this building",
        "",
        f"To reach the voluntary 0.05 W/m²K benchmark across "
        f"**{model['junction_total_m']:.1f} m** of linear detail on an 18 m² plan, the mean Ψ "
        f"would have to be **{model['max_mean_psi_for_benchmark']:.4f} W/mK**.",
        "",
        "That number deserves to be read against what real details achieve. The **good** "
        "scenario in §3 averages "
        f"**{sum(PSI_SCENARIOS['good'].values()) / 4:.4f} W/mK** across its four junction "
        f"types, so the benchmark demands a mean detail at **"
        f"{model['max_mean_psi_for_benchmark'] / (sum(PSI_SCENARIOS['good'].values()) / 4) * 100:.0f} % "
        "of good practice** — on all 61 m, including 16.3 m of window reveals, which are the "
        "hardest linear detail in any wall.",
        "",
        "The same 0.05 applied to a 150 m² dwelling, with roughly 0.67 m of detail per m² "
        "instead of 3.39, implies a mean Ψ of about **0.075 W/mK** — five times looser. The "
        "benchmark is normalised by floor area, and floor area is exactly what a small building "
        "has least of.",
        "",
        "**Conclusion: do not adopt 0.05 W/m²K as a MiniHouse target.** It was calibrated on "
        "dwellings and transplanted here it stops being a target and becomes a different "
        "requirement. If a bridge target is wanted, it should be stated **per metre of linear "
        "detail** — a mean Ψ — where the number means the same thing at any size. The "
        "normalised figure will read high for this building no matter how well it is detailed, "
        "and the report should say that rather than chase it.",
        "",
        "## 7. What this changes",
        "",
        "1. **The chassis junction is a design driver, not a detail.** It is the largest single "
        "thermal decision in the building and it is not drawn.",
        "2. **§14-3 will not catch it.** Element U-values and airtightness pass; the junctions "
        "are unbounded on the applying route. Passing the numbers is not the same as being "
        "efficient, and the gap is where small buildings are weakest.",
        "3. **Compensation is arithmetically open and geometrically shut.** Insulating away "
        "ordinary detailing costs about 53 mm of wall, 65 mm of roof and 65 mm of floor; the "
        f"roof share alone is 69 mm of eave height against a {reference_deficit_mm():.0f} mm "
        "deficit. "
        "The lever exists "
        "and there is no room to pull it.",
        "4. **The 0.05 W/m²K benchmark is not adoptable at 18 m².** It implies a mean Ψ of "
        "0.0147 W/mK — under half of good practice — because it is normalised by an area this "
        "building barely has. State any bridge target per metre, not per m².",
        "5. **The 6:2 plan is thermally expensive.** About 6 % more perimeter than a square of "
        "the same area, on top of an already unfavourable size.",
        "6. **The chassis detail and the thermal detail are one drawing.** Floor insulation "
        "wrapping outside the steel rather than being interrupted by it is the only route to a "
        "low Ψ at the governing junction, and that decision belongs to whoever profiles the "
        "chassis.",
        "",
        "## 8. Limits",
        "",
        "- **No Ψ has been calculated.** The values in §3 are generic screening ranges, not "
        "results, and the real figures require a 2D analysis to NS-EN ISO 10211 on a drawn "
        "detail that does not exist.",
        "- The chassis profile is not selected, so the dominant junction is not even "
        "geometrically defined.",
        "- Moisture risk at the junction is **not** assessed here. A cold steel member crossing "
        "the insulation is a condensation risk as well as a heat-loss one, and §13-13's "
        "vapour-barrier rule interacts with it. That is a separate analysis.",
        "- Wall height is nominal at 2200 mm; the corner length scales with the R2 option and "
        "the numbers move slightly with it.",
        "- No airtightness model. §14-3's 1.5 h⁻¹ is a separate requirement and a separate "
        "failure mode.",
        "- Nothing here is a junction design, a compliance statement or an energy calculation.",
        "",
        "- Generated by `scripts/puentes_termicas.py`; JSON companion: "
        "`knowledge/comparisons/puentes-termicas.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    # Geometry
    assert abs(PLAN_AREA_M2 - 18.0) < 1e-9
    assert abs(PERIMETER_M - 18.0) < 1e-9
    lengths = junction_lengths_m()
    assert abs(lengths["floor / chassis perimeter"] - 18.0) < 1e-9
    assert abs(lengths["eave (wall to roof)"] - 18.0) < 1e-9
    assert abs(lengths["external corner (4 x wall height)"] - 8.8) < 1e-9
    # Opening perimeters from the CSV: 5.9 + 4.6 + 3.8 + 2.0 = 16.3
    assert abs(opening_perimeter_m() - 16.3) < 1e-9
    assert abs(sum(lengths.values()) - 61.1) < 1e-9
    # Opening areas: 1.845 + 1.32 + 0.9 + 0.25 = 4.315
    assert abs(opening_area_m2() - 4.315) < 1e-9

    # Psi'' must be monotone across the scenarios, and proportional to psi scale.
    p_poor = psi_prime_w_m2k(PSI_SCENARIOS["poor"])
    p_ord = psi_prime_w_m2k(PSI_SCENARIOS["ordinary"])
    p_good = psi_prime_w_m2k(PSI_SCENARIOS["good"])
    assert p_poor > p_ord > p_good > 0
    # Doubling every psi doubles the normalised value.
    doubled = {k: 2 * v for k, v in PSI_SCENARIOS["ordinary"].items()}
    assert abs(psi_prime_w_m2k(doubled) - 2 * p_ord) < 1e-9

    # The benchmark is not met by any scenario — that is the finding, so lock it.
    for psi in PSI_SCENARIOS.values():
        assert psi_prime_w_m2k(psi) > BENCHMARK_PSI_PRIME

    # Max mean psi is the exact inverse: mean psi * total length / area = benchmark.
    mean_psi = max_mean_psi_for_benchmark()
    assert abs(mean_psi * sum(lengths.values()) / PLAN_AREA_M2 - BENCHMARK_PSI_PRIME) < 1e-12
    # A uniform psi at that mean must hit the benchmark exactly.
    uniform = {k: mean_psi for k in PSI_SCENARIOS["ordinary"]}
    assert abs(psi_prime_w_m2k(uniform) - BENCHMARK_PSI_PRIME) < 1e-12

    # Compensation: the element scale falls as the detailing gets worse, and
    # stays positive across the swept scenarios (so it is costly, not impossible).
    c_poor = compensation_test(PSI_SCENARIOS["poor"])
    c_ord = compensation_test(PSI_SCENARIOS["ordinary"])
    c_good = compensation_test(PSI_SCENARIOS["good"])
    assert c_poor["element_scale"] < c_ord["element_scale"] < c_good["element_scale"] < 1.0
    assert c_poor["feasible"] and c_good["feasible"]
    # The cost in millimetres must rise with worse detailing.
    assert (c_poor["elements"]["wall"]["delta_mm"]
            > c_ord["elements"]["wall"]["delta_mm"]
            > c_good["elements"]["wall"]["delta_mm"] > 0)
    # The baseline must reproduce the envelope screen's published thicknesses.
    base = baseline_thicknesses()
    assert abs(base["wall"] - 189.0) < 5.0, base["wall"]
    assert abs(base["roof"] - 247.0) < 5.0, base["roof"]
    assert abs(base["floor"] - 238.0) < 5.0, base["floor"]

    # Size effect: smaller plan, larger normalised bridge, same detailing.
    values = [square_psi_prime(PSI_SCENARIOS["ordinary"], a) for a in REFERENCE_AREAS_M2]
    assert values == sorted(values, reverse=True)
    # The 6:2 plan is worse than a square of the same area.
    assert p_ord > square_psi_prime(PSI_SCENARIOS["ordinary"], PLAN_AREA_M2)

    # Bridge share must be a fraction and must rise with worse detailing.
    assert 0.0 < bridge_share(PSI_SCENARIOS["good"]) < bridge_share(PSI_SCENARIOS["poor"]) < 1.0

    model = screen()
    assert len(model["scenarios"]) == len(PSI_SCENARIOS)
    assert len(model["size_effect"]) == len(REFERENCE_AREAS_M2)
    print("Thermal-bridge self-test OK: junction inventory, psi'' scaling, benchmark inverse, "
          "compensation cost in mm, size effect and bridge share all pass")


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
