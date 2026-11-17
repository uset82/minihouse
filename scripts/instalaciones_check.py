#!/usr/bin/env python3
"""MiniHouse · installations and external-environment screen (CONCEPTUAL).

Turns TEK17 chapters 9, 15, 16 and 17 into arithmetic where arithmetic exists.
Four questions, in the order they can actually hurt the project:

  1. Does the waste-plan duty engage?  (§9-6)
     The area limbs are unreachable at 18 m2, so the whole duty hangs on the
     10-tonne limb. This script shows that the limb cannot be crossed by
     building the cabin at any plausible mass, and can only be crossed by
     aggregation with a demolition under §9-6(2) -- which is exactly what a
     reclaimed-timber supply chain does.

  2. Does the drain satisfy the 0.90 m backflow head?  (§15-6(2), §15-8(3))
     Written as an inequality, the pre-accepted performance becomes a MINIMUM
     BURIAL DEPTH for the drain. On a low chassis that depth is not free.

  3. Is the stove/chimney chain closed?  (§9-10, §15-1(5)(d), §15-3)
     Particle limit, flue-gas class and free-side access bind together, and
     the stove choice fixes all three.

  4. What does not apply, and on what basis?  (§15-2, §15-9..15-15, ch.16, §17-1)
     Recorded as determinations, not as omissions.

Nothing here selects a product, a drainage concept or a stove, and nothing is
an installation approval.

Usage:
  python instalaciones_check.py --out-md fase1/verificacion-instalaciones.md \
      --out-json knowledge/comparisons/instalaciones-check.json
  python instalaciones_check.py --selftest
"""
import argparse
import json
from pathlib import Path

# --- §9-6 avfallsplan thresholds -------------------------------------------------
WASTE_PLAN_AREA_NEW_BUILD_M2 = 300.0      # ">300 m2 BRA"
WASTE_PLAN_AREA_ALTERATION_M2 = 100.0     # ">100 m2 BRA"
WASTE_PLAN_AREA_DEMOLITION_M2 = 100.0     # ">100 m2 BRA"
WASTE_PLAN_TONNES = 10.0                  # ">10 tonn bygg- og rivningsavfall"
SORTING_FRACTION = 0.70                   # §9-8, 70 vektprosent
MINIHOUSE_BRA_M2 = 18.0                   # R0 gross footprint

# --- §9-10 stove emissions -------------------------------------------------------
STOVE_LIMIT_CATALYST_G_PER_KG = 5.0
STOVE_LIMIT_OTHER_G_PER_KG = 10.0

# --- §15-3 / §15-1(5)(d) chimney -------------------------------------------------
CHIMNEY_MIN_CLASS_C = 400                 # T400 for solid fuel, NS-EN 1443:2019
CHIMNEY_MIN_FREE_SIDES = 2                # element chimney, crack visibility

# --- §15-6(2) / §15-8(3) backflow head -------------------------------------------
BACKFLOW_HEAD_MM = 900.0

# Screening scenarios: finished floor level above ground, trap water level below FFL.
FFL_SCENARIOS_MM = (250.0, 300.0, 350.0, 400.0, 450.0, 500.0)
TRAP_DEPTHS_MM = (50.0, 60.0, 75.0)

# Crown depth of the receiving pipe. A municipal main is deep by frost
# requirement; a sealed tank connection is shallow to keep gravity fall.
CROWN_SCENARIOS_MM = {
    "municipal main (frost depth)": 1500.0,
    "shallow sealed-tank connection": 400.0,
}

# Cabin mass sweep for §9-6(d). Example values only -- C-07 is unanswered.
MASS_SWEEP_T = (2.0, 3.0, 4.0, 5.0, 6.0, 8.0)
WASTE_FRACTIONS = (0.05, 0.10, 0.20, 0.30)


def backflow_head_mm(h_ffl_mm, d_trap_mm, d_crown_mm):
    """§15-6(2): trap water level minus the main pipe's internal top, in mm.

    Datum is ground level, positive up.
      trap water level = h_ffl - d_trap
      main pipe crown  = -d_crown
    """
    return h_ffl_mm - d_trap_mm + d_crown_mm


def min_crown_depth_mm(h_ffl_mm, d_trap_mm, head_mm=BACKFLOW_HEAD_MM):
    """Shallowest crown depth that still satisfies the 0.90 m head."""
    return head_mm + d_trap_mm - h_ffl_mm


def backflow_verdict(head_mm, head_required=BACKFLOW_HEAD_MM):
    if head_mm < head_required:
        return "fails", head_mm - head_required
    return "passes", head_mm - head_required


def waste_plan_limbs(bra_m2, tonnes, measure="new_build"):
    """Return the §9-6 limbs that engage, as (letter, description, engaged)."""
    limbs = []
    if measure == "new_build":
        limbs.append(("a", f"new build > {WASTE_PLAN_AREA_NEW_BUILD_M2:.0f} m2 BRA",
                      bra_m2 > WASTE_PLAN_AREA_NEW_BUILD_M2))
    elif measure == "alteration":
        limbs.append(("b", f"alteration/repair > {WASTE_PLAN_AREA_ALTERATION_M2:.0f} m2 BRA",
                      bra_m2 > WASTE_PLAN_AREA_ALTERATION_M2))
    elif measure == "demolition":
        limbs.append(("c", f"demolition > {WASTE_PLAN_AREA_DEMOLITION_M2:.0f} m2 BRA",
                      bra_m2 > WASTE_PLAN_AREA_DEMOLITION_M2))
    limbs.append(("d", f"waste > {WASTE_PLAN_TONNES:.0f} tonnes",
                  tonnes > WASTE_PLAN_TONNES))
    return limbs


def waste_plan_required(bra_m2, tonnes, measure="new_build"):
    limbs = waste_plan_limbs(bra_m2, tonnes, measure)
    return any(engaged for _, _, engaged in limbs), limbs


def mass_to_cross_tonnage(fraction, limit_t=WASTE_PLAN_TONNES):
    """Cabin mass that would generate `limit_t` of waste at `fraction`."""
    if fraction <= 0.0:
        return float("inf")
    return limit_t / fraction


def stove_limit_g_per_kg(has_catalyst):
    return STOVE_LIMIT_CATALYST_G_PER_KG if has_catalyst else STOVE_LIMIT_OTHER_G_PER_KG


def stove_verdict(g_per_kg, has_catalyst):
    limit = stove_limit_g_per_kg(has_catalyst)
    return g_per_kg <= limit, limit


def chimney_verdict(flue_class_c, free_sides, constant_section=True, feiing_access=True):
    """§15-3: T400 minimum, >=2 free sides, constant cross-section, feiing access."""
    reasons = []
    if flue_class_c < CHIMNEY_MIN_CLASS_C:
        reasons.append(f"flue class {flue_class_c:.0f} < T{CHIMNEY_MIN_CLASS_C:.0f}")
    if free_sides < CHIMNEY_MIN_FREE_SIDES:
        reasons.append(f"{free_sides} free side(s) < {CHIMNEY_MIN_FREE_SIDES}")
    if not constant_section:
        reasons.append("cross-section varies")
    if not feiing_access:
        reasons.append("no feiing access")
    return not reasons, reasons


APPLICABILITY = (
    ("§9-1", "general external environment", "applies", "qualitative; NS 3466:2009 programme and follow-up plan"),
    ("§9-2", "hazardous substances in products", "applies — no documented route for reclaimed timber", "manufacturer instruments only"),
    ("§9-3", "contaminated ground", "applies — siting gate", "investigation before permit; municipal tiltaksplan"),
    ("§9-4", "selected nature types", "applies — siting gate", "only if designated type present and plan silent"),
    ("§9-5", "construction waste and reuse", "applies — rewards the concept", "design for disassembly must be documented"),
    ("§9-6", "waste plan", "conditional on the 10-tonne limb", "area limbs unreachable at 18 m2"),
    ("§9-7", "hazardous-waste mapping", "NOT applicable — new build", "existing buildings only"),
    ("§9-8", "waste sorting 70 wt%", "follows §9-6", "same switch as the waste plan"),
    ("§9-9", "final waste report", "follows §9-6", "submitted with ferdigattest"),
    ("§9-10", "wood-stove emissions", "applies if a stove is fitted", "5 g/kg catalyst, 10 g/kg other"),
    ("§15-1", "general heating and cooling", "applies", "45 °C, T400, B-s1,d0 floor protection"),
    ("§15-2", "central heating", "not triggered", "no distribution system"),
    ("§15-3", "flue and chimney", "applies if a stove is fitted", "T400, two free sides, feiing access"),
    ("§15-4", "heat pump and refrigeration", "applies if a heat pump is fitted", "30 kg sectioning thresholds not reached"),
    ("§15-5", "internal water", "applies", "38/55 °C, 20/50 mm air gaps, leak stopper"),
    ("§15-6", "internal drainage", "applies", "0.90 m head sets a minimum burial depth"),
    ("§15-7", "external water supply", "applies to the site", "2.5/6.0/1.0 bar, 4 m"),
    ("§15-8", "external drainage and stormwater", "applies to the site", "100-year climate-adjusted; 0.90 m"),
    ("§15-9…15-15", "lifts, platforms, escalators", "NOT applicable", "no lifting device for persons"),
    ("Chapter 16", "lift safety control", "NOT applicable", "no lift in the building"),
    ("§17-1", "greenhouse gas account", "NOT applicable", "boligblokk and yrkesbygning only; småhus exempt"),
)


def screen():
    # 1. Waste plan switch
    cabin_waste = []
    for mass in MASS_SWEEP_T:
        for frac in WASTE_FRACTIONS:
            tonnes = mass * frac
            required, _ = waste_plan_required(MINIHOUSE_BRA_M2, tonnes)
            cabin_waste.append({
                "mass_t": mass,
                "waste_fraction": frac,
                "waste_t": round(tonnes, 2),
                "waste_plan_required": required,
            })
    crossing_mass = [
        {"waste_fraction": frac,
         "cabin_mass_to_cross_t": (None if mass_to_cross_tonnage(frac) == float("inf")
                                   else round(mass_to_cross_tonnage(frac), 1))}
        for frac in WASTE_FRACTIONS
    ]

    # 2. Backflow head
    backflow = []
    for crown_label, crown in CROWN_SCENARIOS_MM.items():
        for h_ffl in FFL_SCENARIOS_MM:
            for d_trap in TRAP_DEPTHS_MM:
                head = backflow_head_mm(h_ffl, d_trap, crown)
                verdict, margin = backflow_verdict(head)
                backflow.append({
                    "receiving_pipe": crown_label,
                    "d_crown_mm": crown,
                    "h_ffl_mm": h_ffl,
                    "d_trap_mm": d_trap,
                    "head_mm": round(head, 1),
                    "verdict": verdict,
                    "margin_mm": round(margin, 1),
                    "min_crown_mm": round(min_crown_depth_mm(h_ffl, d_trap), 1),
                })

    return {
        "revision": "INSTALACIONES-CHECK",
        "state": "CONCEPTUAL — NO PRODUCT, DRAINAGE CONCEPT OR STOVE SELECTED",
        "units": "mm, m2, tonnes, g/kg, °C",
        "basis": {
            "bra_m2": MINIHOUSE_BRA_M2,
            "waste_plan_area_new_build_m2": WASTE_PLAN_AREA_NEW_BUILD_M2,
            "waste_plan_tonnes": WASTE_PLAN_TONNES,
            "sorting_fraction": SORTING_FRACTION,
            "backflow_head_mm": BACKFLOW_HEAD_MM,
            "chimney_min_class_c": CHIMNEY_MIN_CLASS_C,
            "chimney_min_free_sides": CHIMNEY_MIN_FREE_SIDES,
            "stove_limit_catalyst_g_per_kg": STOVE_LIMIT_CATALYST_G_PER_KG,
            "stove_limit_other_g_per_kg": STOVE_LIMIT_OTHER_G_PER_KG,
            "sources": ["S027", "S028"],
        },
        "applicability": [
            {"provision": p, "subject": s, "status": st, "basis": b}
            for p, s, st, b in APPLICABILITY
        ],
        "cabin_waste": cabin_waste,
        "crossing_mass": crossing_mass,
        "backflow": backflow,
        "excluded": [
            "product selection", "drainage concept", "stove or chimney selection",
            "installation approval", "waste tonnage measurement", "site connection type",
        ],
    }


def markdown(model):
    b = model["basis"]
    L = [
        "# MiniHouse · installations and external environment",
        "",
        "**State:** SCREENING — CONCEPTUAL, NO PRODUCT SELECTED, NOT AN INSTALLATION APPROVAL.",
        "Covers TEK17 chapters 9, 15, 16 and 17 as admitted by §1-2(2) "
        "([S020](../knowledge/sources/S020.md)). Requirements from "
        "[S027](../knowledge/sources/S027.md) and [S028](../knowledge/sources/S028.md).",
        "",
        "## 1. Applicability map",
        "",
        "The point of this table is that four items are **not applicable** and now have a "
        "stated basis. A determination is not the same thing as an omission.",
        "",
        "| Provision | Subject | Status | Basis |",
        "|---|---|---|---|",
    ]
    for row in model["applicability"]:
        L.append(f"| {row['provision']} | {row['subject']} | {row['status']} | {row['basis']} |")

    L += [
        "",
        "## 2. The waste-plan duty hangs on one limb",
        "",
        f"§9-6 triggers on **>300 m² BRA** for a new build, **>100 m²** for alteration or "
        f"demolition, or **>10 tonnes** of construction and demolition waste. At "
        f"{b['bra_m2']:.0f} m² the area limbs are not close. The tonnage limb is the only "
        "live question, and it is a **mass** question.",
        "",
        "Waste generated by building the cabin, at plausible cabin masses:",
        "",
        "| Cabin mass t | Waste 5 % | Waste 10 % | Waste 20 % | Waste 30 % |",
        "|---:|---:|---:|---:|---:|",
    ]
    by_mass = {}
    for row in model["cabin_waste"]:
        by_mass.setdefault(row["mass_t"], {})[row["waste_fraction"]] = row["waste_t"]
    for mass in sorted(by_mass):
        cells = [f"{by_mass[mass][f]:.2f} t" for f in WASTE_FRACTIONS]
        L.append(f"| {mass:.0f} | " + " | ".join(cells) + " |")

    L += [
        "",
        "**No cell in that table crosses 10 tonnes, and no plausible cabin mass could.** "
        "The mass needed to cross the limb at a given waste fraction:",
        "",
        "| Waste fraction | Cabin mass needed |",
        "|---:|---:|",
    ]
    for row in model["crossing_mass"]:
        value = row["cabin_mass_to_cross_t"]
        L.append(f"| {row['waste_fraction']*100:.0f} % | "
                 f"{'—' if value is None else f'{value:.0f} t'} |")

    L += [
        "",
        f"An 18 m² cabin weighing 33 t at a 30 % waste fraction is not a building, it is a "
        "barge. So:",
        "",
        "> **The 10-tonne limb cannot be crossed by building the cabin. It can only be "
        "crossed by aggregation.**",
        "",
        "§9-6(2) requires that a project comprising several buildings, constructions or "
        "installations be assessed **as a whole**. A reclaimed-timber supply chain that "
        "dismantles a source building adds that demolition waste to the same assessment. "
        "That is how limb (d) engages — not through the cabin, but through where its "
        "material came from. §9-8 (70 wt % sorting) and §9-9 (final report) inherit exactly "
        "the same switch, so all three stand or fall together.",
        "",
        "**Consequence for the project definition.** Whether chapter 9's waste duties apply "
        "is decided before the first drawing, by the choice of whether the project includes "
        "a demolition. That choice is part of C-08 and should be recorded with it.",
        "",
        "## 3. §9-2 and the reclaimed-timber documentation gap",
        "",
        "§9-2 requires products «uten eller med lavt innhold av helse- eller miljøfarlige "
        "stoffer». Its guidance offers a ladder of compliance instruments, and **every rung "
        "requires a manufacturer**:",
        "",
        "| Rung | Instrument | Available for reclaimed timber? |",
        "|---|---|---|",
        "| 1 | Svanemerket / EU Ecolabel, ECOproduct, SINTEF Teknisk Godkjenning | **no** — no product to look up |",
        "| 2 | Sikkerhetsdatablad, EPD, CE declaration of conformity | **no** — none exist |",
        "| 3 | Written confirmation from the manufacturer's legally responsible person | **no** — there is no manufacturer |",
        "| 4 | Professional assessment and comparison of hazardous-substance content | **yes** — the only route left |",
        "",
        "The **SCIP** duty (produktforskriften §2-32, >**0.1 weight percent** SVHC) falls on "
        "*suppliers of articles*; a private party harvesting timber from a demolished "
        "building is not one.",
        "",
        "This is not a finding that reclaimed timber is non-compliant. It is a finding that "
        "**the pre-accepted documentation route is structurally unavailable**, so rung 4 is "
        "the whole strategy. For old timber that means answering, element by element, "
        "whether the material carries lead paint, CCA or other preservative treatment, "
        "PCB-bearing sealant or asbestos-contaminated dust — which is a **testing** question, "
        "and should be scoped before the timber is bought.",
        "",
        "## 4. The 0.90 m backflow head is a burial depth",
        "",
        "§15-6(2) requires the water level in the **lowest water trap** to sit at least "
        f"**{b['backflow_head_mm']:.0f} mm** above the internal top of the main pipe. §15-8(3) "
        "repeats the same figure for stormwater and combined sewers. With ground level as "
        "datum:",
        "",
        "```",
        "h_ffl − d_trap + d_crown ≥ 900 mm",
        "```",
        "",
        "Rearranged, it is a **minimum burial depth**:",
        "",
        "```",
        "d_crown ≥ 900 + d_trap − h_ffl",
        "```",
        "",
        "A chassis cabin has a low `h_ffl`. The shallowest crown depth that still complies:",
        "",
        "| FFL above ground mm | Trap 50 mm | Trap 60 mm | Trap 75 mm |",
        "|---:|---:|---:|---:|",
    ]
    by_ffl = {}
    for row in model["backflow"]:
        key = (row["h_ffl_mm"], row["d_trap_mm"])
        by_ffl[key] = row["min_crown_mm"]
    for h in FFL_SCENARIOS_MM:
        cells = [f"{by_ffl[(h, d)]:.0f}" for d in TRAP_DEPTHS_MM]
        L.append(f"| {h:.0f} | " + " | ".join(cells) + " |")

    L += [
        "",
        "Whether that is a problem depends entirely on what the drain connects to:",
        "",
        "| Receiving pipe | Crown depth mm | FFL 400 / trap 60 | Verdict |",
        "|---|---:|---:|---|",
    ]
    for label, crown in CROWN_SCENARIOS_MM.items():
        head = backflow_head_mm(400.0, 60.0, crown)
        verdict, margin = backflow_verdict(head)
        L.append(f"| {label} | {crown:.0f} | {head:.0f} | **{verdict}**, "
                 f"{margin:+.0f} mm |")

    L += [
        "",
        "**So the rule is not a general problem — it is a specific one.** A municipal main "
        "sits deep for frost reasons and the head is satisfied with a wide margin. A shallow "
        "sealed-tank connection is where it fails, and then it demands roughly **560 mm** of "
        "crown depth at a 400 mm floor and a 60 mm trap.",
        "",
        "That matters because it is not a plumbing detail but an **earthwork** floor. It "
        "pulls against three other requirements at once: the light-touch siting premise of a "
        "transportable cabin, §7-1(2) (do not create or worsen a hazard by the works) and "
        "§9-3 (do not disturb contaminated ground). The only ways out change the drainage "
        "**concept** — a raised floor, a pumped tank, or a different receiving pipe — and "
        "that decision has not been taken.",
        "",
        "## 5. The stove fixes three things at once",
        "",
        "For an emergency cabin in Norway a wood stove is close to certain, and choosing one "
        "closes a chain rather than a line item:",
        "",
        "| Criterion | Requirement | Source |",
        "|---|---|---|",
        f"| Particle emission | **{b['stove_limit_catalyst_g_per_kg']:.0f} g/kg** with catalyst, "
        f"**{b['stove_limit_other_g_per_kg']:.0f} g/kg** otherwise | §9-10 |",
        f"| Flue-gas temperature class | **T{b['chimney_min_class_c']:.0f}** minimum | §15-1(5)(d), §15-3(2) |",
        f"| Chimney crack visibility | **{b['chimney_min_free_sides']} free sides** minimum | §15-3(5)(b) |",
        "| Surface temperature | burn risk above **~45 °C** | §15-1(3)(c) |",
        "| Floor protection | non-combustible slab or **B-s1,d0 (In1)** | §15-1(3)(b) |",
        "| Cleaning | access for **feiing** and soot removal | §15-3(5)(d) |",
        "",
        "The **two free sides** rule is the one that reaches the floor plan. An element "
        "chimney boxed into a wall or a cupboard on three sides does not comply, because a "
        "crack could not be seen. On an 18 m² plan that is a positional constraint competing "
        "with the stove's own clearances and with the 45 °C surface limit — three constraints "
        "on one small area of wall.",
        "",
        "## 6. Two frequencies that must not be conflated",
        "",
        "§15-8(1) requires stormwater to be dimensioned for **climate-adjusted 100-year** "
        "rainfall. §7-2 assigns MiniHouse safety class **F2 = 1/200**. These are different "
        "instruments and the ordering is coherent:",
        "",
        "- the **drain** is sized for the 1/100 rain (design capacity);",
        "- the **building** must be safe at the 1/200 flood (safety class).",
        "",
        "Collapsing them produces either an over-sized drain or an under-protected floor "
        "level. Where the two meet is the finished floor level: §7-2 pushes it up and "
        "§15-8(3) pushes backflow protection onto the drain. Combined with §15-6's 0.90 m "
        "rule pushing the pipe down, the three requirements pull the same geometry in "
        "opposite directions, and the space between them is the design space.",
        "",
        "## 7. What is not applicable, and why that is a result",
        "",
        "| Item | Why not |",
        "|---|---|",
        "| §15-2 central heating | a single stove or panel heaters are not a distribution system |",
        "| §15-9…15-15 lifts and platforms | no lifting device for persons; a one-storey cabin has none |",
        "| Chapter 16 lift safety control | no lift; the chapter is an operational-safety regime, not documentation |",
        "| §17-1 greenhouse gas account | *boligblokk* and *yrkesbygning* only; a småhus is exempt **by definition**, not by area |",
        "",
        "The §17-1 exemption is worth one sentence of honesty. A project built on material "
        "efficiency and reuse sits outside the only climate-accounting requirement in the "
        "regulation, and the NS 3720 method **excludes biogenic carbon** — which is precisely "
        "the argument reclaimed timber would want to make. If the account is ever produced "
        "voluntarily, that limitation has to be stated with it.",
        "",
        "## 8. Limits",
        "",
        "- No stove, chimney, heat pump, pipe or drainage concept has been selected.",
        "- The 0.90 m inequality restates the pre-accepted performance; it is not a plumbing "
        "design, and branch geometry on a real main may differ.",
        "- Waste tonnages are not measured and cabin mass is unknown (C-07); the mass sweep "
        "uses example values and claims nothing about the real module.",
        "- Whether the plot connects to municipal mains or runs a sealed tank is unknown "
        "until C-01 and C-06, and it decides which column of §4 applies.",
        "- TEK17 chapters **2 and 4** (documentation and FDV) are admitted by §1-2(2) and are "
        "**not covered here**; they remain an open retrieval item.",
        "- Nothing here is an installation approval, a fire approval or a completion certificate.",
        "",
        "- Generated by `scripts/instalaciones_check.py`; JSON companion: "
        "`knowledge/comparisons/instalaciones-check.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    # Backflow identity: the boundary case must sit exactly on the requirement.
    assert backflow_head_mm(400.0, 60.0, 560.0) == 900.0
    assert min_crown_depth_mm(400.0, 60.0) == 560.0
    # min_crown_depth is the inverse of backflow_head at the requirement.
    for h in FFL_SCENARIOS_MM:
        for d in TRAP_DEPTHS_MM:
            crown = min_crown_depth_mm(h, d)
            assert abs(backflow_head_mm(h, d, crown) - BACKFLOW_HEAD_MM) < 1e-9
    # Monotonicity: higher floor helps, deeper trap hurts, deeper crown helps.
    assert backflow_head_mm(450.0, 60.0, 560.0) > backflow_head_mm(400.0, 60.0, 560.0)
    assert backflow_head_mm(400.0, 75.0, 560.0) < backflow_head_mm(400.0, 60.0, 560.0)
    assert backflow_head_mm(400.0, 60.0, 600.0) > backflow_head_mm(400.0, 60.0, 560.0)
    verdict, margin = backflow_verdict(900.0)
    assert verdict == "passes" and margin == 0.0
    assert backflow_verdict(899.0)[0] == "fails"

    # §9-6: area limbs unreachable at 18 m2, tonnage limb engages above 10 t.
    required, limbs = waste_plan_required(MINIHOUSE_BRA_M2, 1.8)
    assert required is False
    assert not any(e for _, _, e in limbs)
    required, limbs = waste_plan_required(MINIHOUSE_BRA_M2, 12.0)
    assert required is True
    assert [letter for letter, _, e in limbs if e] == ["d"]
    required, _ = waste_plan_required(320.0, 1.0)
    assert required is True
    # Strict inequality: exactly 10 t does not trigger ">10".
    required, _ = waste_plan_required(MINIHOUSE_BRA_M2, WASTE_PLAN_TONNES)
    assert required is False
    # No plausible cabin mass crosses the limb.
    for frac in WASTE_FRACTIONS:
        assert mass_to_cross_tonnage(frac) >= WASTE_PLAN_TONNES
        assert mass_to_cross_tonnage(frac) > max(MASS_SWEEP_T)
    assert mass_to_cross_tonnage(0.0) == float("inf")

    # §9-10 stove limits.
    assert stove_verdict(4.9, True)[0] is True
    assert stove_verdict(5.1, True)[0] is False
    assert stove_verdict(9.9, False)[0] is True
    assert stove_verdict(10.1, False)[0] is False
    # A stove passing the non-catalyst limit may fail the catalyst limit.
    assert stove_verdict(8.0, True)[0] is False and stove_verdict(8.0, False)[0] is True

    # §15-3 chimney chain.
    assert chimney_verdict(400.0, 2)[0] is True
    assert chimney_verdict(350.0, 2)[0] is False
    assert chimney_verdict(600.0, 1)[0] is False
    assert "free side" in chimney_verdict(600.0, 1)[1][0]
    assert chimney_verdict(600.0, 2, constant_section=False)[0] is False
    assert chimney_verdict(600.0, 2, feiing_access=False)[0] is False

    # Applicability map must carry every chapter the scope admits, with a status.
    provisions = [row["provision"] for row in screen()["applicability"]]
    for needle in ("§9-1", "§9-10", "§15-3", "§15-6", "Chapter 16", "§17-1"):
        assert needle in provisions, needle
    # Four determinations: §9-7 (new build), §15-9..15-15, chapter 16, §17-1.
    assert sum(1 for r in screen()["applicability"] if "NOT applicable" in r["status"]) == 4

    print("Installations self-test OK: waste-plan switch, backflow inversion, stove limits, "
          "chimney chain and applicability map all pass")


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
