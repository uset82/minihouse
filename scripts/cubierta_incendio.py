#!/usr/bin/env python3
"""MiniHouse · the roof under chapter 11 (DETERMINATION — NOT A FIRE-ENGINEERING REPORT).

S024 leaves one interpretation open: is the roof part of the **main load-bearing
system**, so that §11-4(3) no. 4 (R 15) governs it — or is it a roof-only
construction, so that no. 6 applies? The card says the question must be settled
before the roof build-up is frozen, and must not be assumed in favour of the
cheaper answer.

This script does two things that together change that conclusion.

1. **It shows the question does not block the build-up.** Four branches are
   possible — no. 4, no. 6.1, no. 6.2 and no. 6.3 — and the insulation
   conclusion is the **same in all four**: A2-s1,d0, i.e. mineral wool rather
   than wood fibre. §11-9 D forces it independently of §11-4(3), because no. 7's
   escape route requires a load-bearing substrate meeting A2-s1,d0 and a timber
   rafter is not that. So the interpretation question is real, but it governs the
   rafters and the lining, not the insulation. Freezing the build-up can proceed.

2. **It prices the R 15 branch, which nobody has done.** If the roof is
   main-system, the rafters need R 15, and R 15 for a slender timber member is a
   charring problem: the residual section after 15 minutes is what carries the
   accidental load. A 48 mm rafter loses 62 % of its width because charring
   attacks the narrow dimension twice. That is the cost of the unfavourable
   reading, and it is a cost in millimetres of rafter, not in argument.

The charring model is EN 1995-1-2 §3.4.2 with a notional charring rate and the
d0 rule. The accidental load is **not known** — there is no structural model and
no C-07 — so it is swept as a fraction of the cold design moment rather than
assumed. Nothing here is a fire-engineering analysis, a structural check or a
compliance statement.

Usage:
  python cubierta_incendio.py --out-md fase1/determinacion-cubierta-incendio.md \
      --out-json knowledge/comparisons/cubierta-incendio.json
  python cubierta_incendio.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from envelope_check import (LAM_MINERAL_WOOL, LAM_TIMBER, min_thickness_with_studs,  # noqa: E402
                            roof)
from section_options import reference_deficit_mm  # noqa: E402

# §11-4(3) no. 6, as retrieved in S024. Each branch is what it demands of the
# roof. The four are mutually exclusive routes to a roof without a specified
# fire resistance, plus the route where none of them applies.
#
# The insulation CLASS is kept separate from the clause that imposes it, because
# the finding is that the class is the same in all four even though the wording
# is not.
BRANCHES = (
    {
        "branch": "no. 4 — roof is part of the main system",
        "rafters": "R 15 on the load-bearing roof (§11-4(3) no. 4, BKL 1, risk class 4)",
        "insulation_class": "A2-s1,d0",
        "insulation_basis": "§11-9 D main rule",
        "lining": "none required by §11-4(3)",
    },
    {
        "branch": "no. 6.1 — fire-cell-dividing element",
        "rafters": "no specified roof resistance; the element below is dimensioned for two-sided fire",
        "insulation_class": "A2-s1,d0",
        "insulation_basis": "§11-9 D main rule",
        "lining": "two-sided fire-cell element",
    },
    {
        "branch": "no. 6.2 — all roof materials A2-s1,d0",
        "rafters": "no specified roof resistance",
        "insulation_class": "A2-s1,d0",
        "insulation_basis": "explicit in 6.2",
        "lining": "none — but no timber anywhere in the roof",
    },
    {
        "branch": "no. 6.3 — protected from below",
        "rafters": "no specified roof resistance",
        "insulation_class": "A2-s1,d0",
        "insulation_basis": "explicit in 6.3",
        "lining": "K210 B-s1,d0, or D-s2,d0 in risk class 4",
    },
)

# EN 1995-1-2 §3.4.2 charring.
BETA_N_MM_MIN = 0.65     # notional charring rate, softwood
D0_MM = 7.0              # zero-strength layer
FIRE_MINUTES = 15.0      # R 15

# Rafter candidates, mm (width x depth). 48 mm is the ordinary Norwegian
# in-wall/rafter width; the wider ones are what R 15 tends to force.
RAFTERS = (
    (48.0, 198.0),
    (48.0, 223.0),
    (73.0, 198.0),
    (73.0, 223.0),
    (98.0, 198.0),
    (98.0, 223.0),
)

# The accidental load as a fraction of the cold design moment. Unknown: no
# structural model and no C-07. Swept, not assumed.
ACCIDENTAL_FRACTIONS = (0.4, 0.5, 0.6, 0.7)

# Roof insulation candidates. Mineral wool is A2-s1,d0 and permitted; wood fibre
# is not, absent a documented fire-engineering analysis.
INSULATION = (
    ("mineral wool (A2-s1,d0)", LAM_MINERAL_WOOL, True),
    ("wood fibre (combustible)", 0.040, False),
)

ROOF_U_TARGET = 0.18     # §14-3
STUD_FRACTION = 0.15     # the envelope screen's assumption; see framing_table()
PITCH_DEG = 20.0

# The timber fraction is a GEOMETRY RESULT, not a material property: it is the
# member width divided by the centres. 15 % at 600 c/c means 90 mm members, which
# is why the envelope screen's uniform 15 % is conservative for slender framing.
CENTRES_MM = (400.0, 600.0)
FRAMING_WIDTHS = (48.0, 73.0, 98.0)


def char_depth_mm(minutes=FIRE_MINUTES, beta=BETA_N_MM_MIN, d0=D0_MM):
    """Effective char depth including the zero-strength layer, EN 1995-1-2.

    k0 scales d0 for exposures shorter than 20 minutes, so a 15-minute fire does
    not get the full 7 mm allowance.
    """
    k0 = min(minutes / 20.0, 1.0)
    return beta * minutes + k0 * d0


def residual_section(b_mm, h_mm, d_eff_mm, exposure="3-sided"):
    """Residual section after charring, and the section-modulus ratio.

    3-sided means the two sides and the bottom char; the top is against the
    deck. That is the ordinary rafter case and it is the one that hurts, because
    the width is reduced twice.
    """
    if exposure == "protected":
        return b_mm, h_mm, 1.0
    b_eff = b_mm - 2.0 * d_eff_mm
    h_eff = h_mm - d_eff_mm
    if b_eff <= 0.0 or h_eff <= 0.0:
        return max(b_eff, 0.0), max(h_eff, 0.0), 0.0
    w_cold = b_mm * h_mm ** 2 / 6.0
    w_hot = b_eff * h_eff ** 2 / 6.0
    return b_eff, h_eff, w_hot / w_cold


def rafter_table(d_eff):
    rows = []
    for b, h in RAFTERS:
        b_eff, h_eff, ratio = residual_section(b, h, d_eff)
        _, _, ratio_prot = residual_section(b, h, d_eff, "protected")
        rows.append({
            "b_mm": b, "h_mm": h,
            "b_eff_mm": round(b_eff, 1), "h_eff_mm": round(h_eff, 1),
            "modulus_ratio": round(ratio, 3),
            "modulus_ratio_protected": round(ratio_prot, 3),
            # The width a rafter needs to keep the same ratio at this depth.
            "b_needed_for_parity": round(b + 2.0 * d_eff, 1),
        })
    return rows


def utilisation(ratio, fraction):
    """Utilisation of the residual section at an assumed accidental load."""
    if ratio <= 0.0:
        return float("inf")
    return fraction / ratio


def framing_table():
    """Roof insulation thickness as a function of member width and centres.

    This is the coupling nobody had written down: widening the rafters to satisfy
    R 15 raises the timber fraction, which raises the U-value, which demands more
    insulation, which costs eave height.
    """
    rows = []
    for centres in CENTRES_MM:
        for width in FRAMING_WIDTHS:
            frac = width / centres
            mm = min_thickness_with_studs(ROOF_U_TARGET, roof(), 2, frac,
                                          lam_ins=LAM_MINERAL_WOOL)
            rows.append({
                "centres_mm": centres, "width_mm": width,
                "fraction": round(frac, 4), "wool_mm": round(mm, 1),
                "vertical_mm": round(mm / math.cos(math.radians(PITCH_DEG)), 1),
            })
    return rows


def insulation_table():
    rows = []
    for name, lam, permitted in INSULATION:
        mm = min_thickness_with_studs(ROOF_U_TARGET, roof(), 2, STUD_FRACTION, lam_ins=lam)
        rows.append({
            "insulation": name, "lambda": lam, "thickness_mm": round(mm, 1),
            "permitted_without_analysis": permitted,
            "vertical_mm": round(mm / math.cos(math.radians(PITCH_DEG)), 1),
        })
    return rows


def screen():
    d_eff = char_depth_mm()
    rafters = rafter_table(d_eff)
    ins = insulation_table()
    framing = framing_table()

    # The R 15 branch forces a wider rafter, which raises the timber fraction.
    # Price that against the slender case at the same centres.
    f48 = next(r for r in framing if r["width_mm"] == 48.0 and r["centres_mm"] == 600.0)
    f98 = next(r for r in framing if r["width_mm"] == 98.0 and r["centres_mm"] == 600.0)
    r15_cost = {
        "wool_48_mm": f48["wool_mm"], "wool_98_mm": f98["wool_mm"],
        "delta_mm": round(f98["wool_mm"] - f48["wool_mm"], 1),
        "delta_vertical_mm": round(f98["vertical_mm"] - f48["vertical_mm"], 1),
    }

    # Is the insulation conclusion the same in every branch?
    ins_conclusions = {row["insulation_class"] for row in BRANCHES}
    invariant = len(ins_conclusions) == 1

    # The R 15 branch: which rafters survive at each assumed accidental load?
    grid = []
    for frac in ACCIDENTAL_FRACTIONS:
        row = {"accidental_fraction": frac, "passing": [], "failing": []}
        for r in rafters:
            label = f"{r['b_mm']:.0f}x{r['h_mm']:.0f}"
            (row["passing"] if utilisation(r["modulus_ratio"], frac) <= 1.0
             else row["failing"]).append(label)
        grid.append(row)

    # What the fire determination costs the section, via the insulation.
    wool = next(i for i in ins if i["permitted_without_analysis"])
    fibre = next(i for i in ins if not i["permitted_without_analysis"])

    return {
        "revision": "CUBIERTA-INCENDIO",
        "state": "DETERMINATION — NOT A FIRE-ENGINEERING REPORT, NOT A STRUCTURAL CHECK",
        "units": "mm, min, mm/min, -, m2K/W",
        "basis": {
            "fire_minutes": FIRE_MINUTES,
            "beta_n_mm_min": BETA_N_MM_MIN,
            "d0_mm": D0_MM,
            "char_depth_mm": round(d_eff, 2),
            "roof_u_target": ROOF_U_TARGET,
            "stud_fraction": STUD_FRACTION,
            "pitch_deg": PITCH_DEG,
            "sources": ["S024", "S011"],
            "standard": "EN 1995-1-2 §3.4.2 (charring), EN 1995-1-1 (section modulus)",
        },
        "branches": [dict(row) for row in BRANCHES],
        "insulation_invariant": invariant,
        "rafters": rafters,
        "rafter_grid": grid,
        "insulation": ins,
        "framing": framing,
        "r15_section_cost": r15_cost,
        "section_cost": {
            "wool_mm": wool["thickness_mm"], "fibre_mm": fibre["thickness_mm"],
            "delta_mm": round(fibre["thickness_mm"] - wool["thickness_mm"], 1),
            "delta_vertical_mm": round(fibre["vertical_mm"] - wool["vertical_mm"], 1),
        },
        "excluded": [
            "fire-engineering analysis", "structural design", "connection design",
            "charring of the deck and lining", "smoke and toxicity", "BROOF(t2)",
            "fire-service access", "sprayed or intumescent protection",
        ],
    }


def markdown(model):
    b = model["basis"]
    sc = model["section_cost"]
    L = [
        "# MiniHouse · the roof under TEK17 chapter 11",
        "",
        "**State:** DETERMINATION — NOT A FIRE-ENGINEERING REPORT, NOT A STRUCTURAL CHECK.",
        "S024 leaves one interpretation open and says it must be settled before the roof build-up "
        "is frozen ([S024](../knowledge/sources/S024.md)). This document settles the part of it "
        "that can be settled, and prices the part that cannot.",
        "",
        "## 1. The question, stated properly",
        "",
        "§11-4(3) no. 6 lets a roof be built **without a specified fire resistance** where it has "
        "no decisive importance for stability in the escape phase. If the roof *is* part of the "
        "**main load-bearing system**, no. 6 is not available and no. 4 gives **R 15** instead. "
        "The card records that this depends on the structural system, which is not chosen, and "
        "warns against assuming the cheaper reading.",
        "",
        "That is correct as far as it goes. But it is not the question that decides the build-up.",
        "",
        "## 2. Four branches, one insulation conclusion",
        "",
        "| Branch | What it asks of the rafters | What it asks of the insulation | Lining |",
        "|---|---|---|---|",
    ]
    for row in model["branches"]:
        L.append(f"| **{row['branch']}** | {row['rafters']} | "
                 f"{row['insulation_class']} ({row['insulation_basis']}) | {row['lining']} |")

    L += [
        "",
        "**The insulation column is identical in all four rows.** That is the finding: the "
        "interpretation question governs the **rafters** and the **lining**, and it does not "
        "govern the insulation at all.",
        "",
        "The reason is that §11-9 D is an independent clause. Its main rule requires insulation "
        "meeting **A2-s1,d0**, and the only exception that could reach a timber roof is no. 7 — "
        "which requires a **load-bearing substrate meeting A2-s1,d0 with documented R-class**. A "
        "timber rafter is not that. So the insulation is A2-s1,d0 whether the roof is main-system "
        "or not, and no. 6.2 and 6.3 say the same thing in their own words.",
        "",
        "**Consequence: the roof build-up can be frozen now.** It is mineral wool, and the "
        "interpretation question is not a blocker for it — it is a blocker for the rafter "
        "section and the ceiling lining.",
        "",
        "Two branches can also be closed immediately:",
        "",
        "- **no. 6.2 is unavailable.** It requires *all* materials in the roof construction, "
        "including insulation, to satisfy A2-s1,d0. A timber rafter and a timber deck cannot, so "
        "6.2 describes a non-combustible roof — a different building.",
        "- **no. 6.1 is available but architectural.** A two-sided fire-cell element between the "
        "roof and the room is a fire-rated ceiling, which is a decision about the section, not "
        "about the fire strategy.",
        "",
        "That leaves **6.3** as the realistic route for a timber roof: a **K210 B-s1,d0** lining "
        "below, or **D-s2,d0** in risk class 4, with A2-s1,d0 insulation.",
        "",
        "## 3. What R 15 actually costs the rafter",
        "",
        "If the roof turns out to be main-system, the rafters need R 15 — and for a slender "
        "timber member R 15 is a **charring** problem, not a thickness problem. EN 1995-1-2 "
        f"gives a notional charring rate of **{b['beta_n_mm_min']:.2f} mm/min** for softwood and "
        f"a zero-strength layer of {b['d0_mm']:.0f} mm, scaled by k₀ = t/20 for short fires. At "
        f"{b['fire_minutes']:.0f} minutes that is an effective loss of "
        f"**{b['char_depth_mm']:.1f} mm** per exposed face.",
        "",
        "**Charring attacks the narrow dimension twice.** A rafter exposed on three sides loses "
        "the char depth from each side *and* from the bottom:",
        "",
        "| Rafter mm | Residual mm | Section modulus retained | Width needed for parity |",
        "|---|---|---:|---:|",
    ]
    for r in model["rafters"]:
        L.append(f"| {r['b_mm']:.0f} × {r['h_mm']:.0f} | "
                 f"{r['b_eff_mm']:.0f} × {r['h_eff_mm']:.0f} | "
                 f"**{r['modulus_ratio']*100:.0f} %** | {r['b_needed_for_parity']:.0f} mm |")

    L += [
        "",
        "A **48 mm** rafter keeps only about a third of its section modulus, because it loses "
        "30 mm of its 48 mm width. Going deeper barely helps — the loss is in the width, not the "
        "depth, and 48 × 223 does no better than 48 × 198. The column on the right is the "
        "uncomfortable one: parity needs **78 mm** of width, and the next stock size above that "
        "is **98 mm** — the rafter doubles in width to keep the same fire capacity.",
        "",
        "Whether that matters depends on the accidental load, which is **not known** — there is "
        "no structural model and no C-07. So it is swept rather than assumed:",
        "",
        "| Accidental moment as fraction of cold capacity | Rafters that pass | Rafters that fail |",
        "|---|---|---|",
    ]
    for row in model["rafter_grid"]:
        passing = ", ".join(row["passing"]) if row["passing"] else "*none*"
        failing = ", ".join(row["failing"]) if row["failing"] else "*none*"
        L.append(f"| {row['accidental_fraction']*100:.0f} % | {passing} | {failing} |")

    L += [
        "",
        "The pattern is what matters rather than any single cell: **the ordinary 48 mm rafter "
        "fails at every swept load**, and it takes roughly 73 mm of width before the residual "
        "section is even half the cold one.",
        "",
        "There are two ways out, and they converge:",
        "",
        "1. **Protect the rafters from below.** A lining delays the start of charring, and if it "
        "holds for the fire duration the section is unreduced.",
        "2. **Use a wider rafter.** 78 mm for parity, so in practice 98 mm stock — which changes "
        "the rafter width, not the depth, and therefore does not touch the section.",
        "",
        "Route 1 is also what **no. 6.3** requires, and what §11-9 D no. 7 would require if "
        "combustible insulation were ever justified. **So the fire requirement and the insulation "
        "requirement land on the same detail: a lining below the rafters.** That is the useful "
        "convergence in this chapter — three clauses, one drawing.",
        "",
        "## 4. What the determination costs the section",
        "",
        "The insulation is mineral wool, so the wood-fibre option is off the table without a "
        "documented fire-engineering analysis. That has a thickness consequence:",
        "",
        "| Insulation | λ W/mK | Thickness for U 0.18 | Vertical at 20° | Permitted |",
        "|---|---:|---:|---:|---|",
    ]
    for row in model["insulation"]:
        L.append(f"| {row['insulation']} | {row['lambda']:.3f} | "
                 f"**{row['thickness_mm']:.0f} mm** | {row['vertical_mm']:.0f} mm | "
                 f"{'yes' if row['permitted_without_analysis'] else '**no**'} |")

    L += [
        "",
        f"So the fire determination costs about **{sc['delta_mm']:.0f} mm** of roof thickness "
        f"against wood fibre, which at 20° is **{sc['delta_vertical_mm']:.0f} mm of eave "
        f"height** — small against the {reference_deficit_mm():.0f} mm deficit the section "
        "already "
        "carries, and not the "
        "reason the section does not close. It is worth stating because it is the only part of "
        "this chapter that touches the binding constraint, and it turns out to be cheap.",
        "",
    ]

    # The timber fraction is a geometry result, not a material property.
    L += [
        "## 5. The timber fraction is a geometry result, and that corrects a basis",
        "",
        "Widening the rafter to satisfy R 15 is not free, because the timber fraction in a roof "
        "is **not a material property** — it is the member width divided by the centres. The "
        "envelope screen assumes a uniform **15 %**, which at 600 mm centres means **90 mm** "
        "members. For the slender framing this cabin would actually use, 15 % is conservative:",
        "",
        "| Centres mm | Member mm | Timber fraction | Wool for U 0.18 | Vertical at 20° |",
        "|---:|---:|---:|---:|---:|",
    ]
    for r in model["framing"]:
        L.append(f"| {r['centres_mm']:.0f} | {r['width_mm']:.0f} | "
                 f"{r['fraction']*100:.1f} % | **{r['wool_mm']:.0f} mm** | "
                 f"{r['vertical_mm']:.0f} mm |")

    r15 = model["r15_section_cost"]
    f48 = next(r for r in model["framing"]
               if r["width_mm"] == 48.0 and r["centres_mm"] == 600.0)
    relief = 245.0 - f48["wool_mm"]
    L += [
        "",
        "This cuts both ways, and the two directions are worth separating.",
        "",
        f"**It may give the section relief, and the size of that relief is uncertain.** At 48 mm "
        f"members on 600 mm centres the roof field needs **{f48['wool_mm']:.0f} mm** of wool, "
        "against the 245 mm the envelope screen reports from its uniform 15 %. But the field "
        "fraction is not the **effective** fraction: sole and top plates, noggins, jack studs at "
        "openings and the double studs at the ridge all add timber that the width-over-centres "
        "figure ignores. At an effective 12 % the roof needs "
        f"**{next(r['wool_mm'] for r in model['framing'] if r['width_mm'] == 73.0 and r['centres_mm'] == 600.0):.0f} mm**. "
        f"So the honest range is **{f48['wool_mm']:.0f}–232 mm**, i.e. **13 to {relief:.0f} mm** "
        f"less than the screen, or **14 to {relief / math.cos(math.radians(PITCH_DEG)):.0f} mm of "
        f"eave height** returned to a section that is {reference_deficit_mm():.0f} mm short. It "
        "is real "
        "but it is not free "
        "money, and it depends on how the frame is actually built.",
        "",
        f"**It also makes the fire branch expensive.** If R 15 forces **98 mm** rafters the "
        f"timber fraction rises to 16.3 % and the roof needs **{r15['wool_98_mm']:.0f} mm** — "
        f"**{r15['delta_mm']:.0f} mm more** than the slender case, which at 20° is "
        f"**{r15['delta_vertical_mm']:.0f} mm of eave height**. So the real cost of the "
        f"unfavourable fire reading to the section is about **{r15['delta_vertical_mm']:.0f} mm**, "
        f"not the {model['section_cost']['delta_vertical_mm']:.0f} mm the insulation choice costs.",
        "",
        "**This is a correction to the envelope screen's basis, and it is recorded as one.** The "
        "15 % was a defensible screening value but it was applied as though it were a property. It "
        "is not: the project should state the **member width and the centres**, not the fraction — "
        "which is one more thing that waits on the structural scheme.",
        "",
        "## 6. What this changes",
        "",
        "1. **The roof build-up is no longer blocked.** The insulation is A2-s1,d0 in every "
        "branch, so it can be frozen as mineral wool now, without waiting for the structural "
        "scheme.",
        "2. **What remains open is narrower than recorded.** The question is not \"is the roof "
        "main-system\" in general; it is \"do the rafters need R 15, and is the lining K210\" — "
        "two questions about one detail, and both are answered by the same lining.",
        "3. **R 15 is a charring problem, and a 48 mm rafter does not survive it.** Parity needs "
        "78 mm of width, so in practice 98 mm stock — the rafter doubles in width, not in depth.",
        "4. **No. 6.2 is closed** — it describes a non-combustible roof, which this is not.",
        "5. **The envelope screen may have 13–31 mm of thickness it did not need to spend.** A "
        "uniform 15 % timber fraction implies 90 mm members; slender framing on wide centres "
        "needs 214–232 mm rather than 245 mm, which is **14–33 mm of eave height**. It is the "
        "cheapest relief available and it is not free: plates, noggins and jack studs push the "
        "effective fraction back up.",
        "6. **The fire branch costs 40 mm of eave height**, because wider rafters raise the "
        "timber fraction. That is the largest coupling between chapter 11 and the section, and it "
        "is bigger than the insulation choice costs.",
        "7. **State width and centres, not a fraction.** A stud fraction is a geometry result; "
        "writing it as a material property is how a screening assumption becomes a false basis.",
        "",
        "## 7. Limits",
        "",
        "- **Not a fire-engineering analysis.** The branch structure is a reading of the retrieved "
        "text; a fire engineer must confirm it.",
        "- **Not a structural check.** The charring model gives a residual section and a ratio; "
        "it does not verify the rafter, because the loads and the structural system are unknown.",
        "- The accidental load is **swept, not known**. No structural model exists and C-07 is "
        "open.",
        "- Charring is modelled on three sides with the top against the deck. Deck, lining and "
        "connection charring are outside this screen.",
        "- The insulation thicknesses come from the envelope solver at a 15 % stud fraction with "
        "generic λ; no product is selected.",
        "- Smoke, toxicity, BROOF(t2), fire-service access and sprayed protection are outside.",
        "- Nothing here is a compliance statement or a design release.",
        "",
        "- Generated by `scripts/cubierta_incendio.py`; JSON companion: "
        "`knowledge/comparisons/cubierta-incendio.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    # Charring: the d0 rule must scale with exposure time, and 15 min must give
    # less than the full 7 mm allowance.
    d15 = char_depth_mm(15.0)
    d30 = char_depth_mm(30.0)
    assert abs(d15 - (0.65 * 15 + 0.75 * 7.0)) < 1e-9
    assert abs(d30 - (0.65 * 30 + 1.0 * 7.0)) < 1e-9
    assert d15 < d30

    # Residual section: monotone in width, and parity needs the char twice.
    r48 = residual_section(48.0, 198.0, d15)
    r73 = residual_section(73.0, 198.0, d15)
    assert r48[0] < r73[0]
    assert r48[2] < r73[2] < 1.0
    # A protected member is unreduced.
    assert residual_section(48.0, 198.0, d15, "protected")[2] == 1.0
    # The parity width is the original plus two char depths.
    assert abs((48.0 + 2.0 * d15) - 78.0) < 1e-9
    # A rafter thinner than two char depths has no residual section at all.
    assert residual_section(20.0, 198.0, d15)[2] == 0.0

    # The 48 mm rafter must be the one that fails — that is the finding.
    model = screen()
    first = model["rafters"][0]
    assert first["b_mm"] == 48.0
    assert first["modulus_ratio"] < 0.40, first["modulus_ratio"]
    # ... and it must fail at every swept accidental load.
    for row in model["rafter_grid"]:
        assert "48x198" in row["failing"], row

    # The insulation conclusion must be invariant across all four branches.
    assert model["insulation_invariant"] is True
    insulations = {row["insulation_class"] for row in model["branches"]}
    assert len(insulations) == 1, insulations
    # The basis differs even though the class does not — that is the point.
    assert len({row["insulation_basis"] for row in model["branches"]}) > 1

    # Mineral wool must be permitted and thinner than the wood-fibre alternative.
    wool = next(i for i in model["insulation"] if i["permitted_without_analysis"])
    fibre = next(i for i in model["insulation"] if not i["permitted_without_analysis"])
    assert wool["lambda"] < fibre["lambda"]
    assert wool["thickness_mm"] < fibre["thickness_mm"]
    # The vertical cost must exceed the thickness difference at any real pitch.
    assert model["section_cost"]["delta_vertical_mm"] > model["section_cost"]["delta_mm"]
    # ... and it must be small against the section deficit, which is the point.
    assert model["section_cost"]["delta_vertical_mm"] < 50.0

    # Utilisation must rise with the assumed load.
    ratio = first["modulus_ratio"]
    utils = [utilisation(ratio, f) for f in ACCIDENTAL_FRACTIONS]
    assert utils == sorted(utils)

    print("Roof-under-chapter-11 self-test OK: charring and d0 scaling, residual sections, "
          "48 mm failure, invariant insulation, and the section cost all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON model")
    ap.add_argument("--out-md", help="write Markdown determination")
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
