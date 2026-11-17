#!/usr/bin/env python3
"""MiniHouse · TEK17 chapter 7 natural-hazard screening (flood and landslide).

Chapters 1 to 7 of TEK17 apply in full on the mikrohus route (§1-2(2)(a)),
so §7-2 and §7-3 bind. Neither section constrains the cabin; both constrain
the plot. This script does the arithmetic that can be done before a site is
chosen, and nothing else:

  1. Turns the safety classes into probabilities a person can reason about
     (annual, and "at least once" over 25/50/75 years).
  2. Builds the flood datum a finished floor has to clear: mapped level +
     sea-level-rise allowance over the service life + an explicit margin.
  3. Screens a soil slope with the infinite-slope model, so an obviously
     marginal plot can be rejected before anyone pays for a geotechnical
     report.
  4. Puts the §7-3 guidance ceiling of ~50 kPa into physical terms.

The screen has no pass state. It can say "this plot needs a geotechnical
report" and it can say "this plot needs one urgently". It cannot say "this
plot is safe", and the code is written so that it never pretends to.

Usage:
  python natural_hazard_screen.py --out-md fase1/cribado-riesgos-naturales.md \
      --out-json knowledge/comparisons/natural-hazard-screen.json
  python natural_hazard_screen.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

# Safety classes and their largest nominal annual probability, as return periods.
# TEK17 §7-2 Table 1 (flood) and §7-3 Table 1 (landslide); see S026.
FLOOD_CLASSES = {"F1": 20, "F2": 200, "F3": 1000}
LANDSLIDE_CLASSES = {"S1": 100, "S2": 1000, "S3": 5000}

# MiniHouse assignment. Both lists name the dwelling and the holiday home, so
# this does not depend on C-01.
MINIHOUSE_FLOOD = "F2"
MINIHOUSE_LANDSLIDE = "S2"

LIVES = (25, 50, 75)

# Sea-level-rise sensitivity sweep, mm/year. Not a projection: the local value
# has to come from Kartverket for the actual site.
SLR_RATES = (0.0, 2.0, 4.0, 6.0, 8.0)

# Flood margin above the mapped level. NOT a TEK17 figure — no freeboard number
# was retrieved. It is a project choice and is labelled as one everywhere.
DEFAULT_MARGIN_MM = 300.0
EXAMPLE_FLOOD_LEVEL_MM = 1250.0  # hypothetical, above chart datum

# Infinite-slope sweep.
SLOPE_ANGLES = (20.0, 25.0, 30.0, 35.0, 40.0)
FRICTION_ANGLES = (30.0, 32.0, 34.0, 36.0)
SOIL_UNIT_WEIGHT = 18.0   # kN/m3, a working value, not site data
SLAB_DEPTH = 2.0          # m, depth of the sliding plane in the model
MATERIAL_FACTOR = 1.4     # gamma_m for field-assessed friction, unverified (S014)

# §7-3 guidance: practical ceiling for designing a building to withstand
# landslide forces, above which siting or protective works are the only routes.
PRESSURE_CEILING_KPA = 50.0


def annual_probability(return_period_years):
    """Largest nominal annual probability for a return period."""
    if return_period_years <= 0:
        raise ValueError("return period must be positive")
    return 1.0 / return_period_years


def probability_within(years, return_period_years):
    """Probability of at least one exceedance in `years`, assuming independence."""
    p = annual_probability(return_period_years)
    return 1.0 - (1.0 - p) ** years


def slr_allowance(rate_mm_per_year, years):
    """Linear sea-level-rise allowance. Deliberately linear and deliberately simple."""
    return rate_mm_per_year * years


def required_ffl(flood_level_mm, slr_rate_mm_per_year, years, margin_mm=DEFAULT_MARGIN_MM):
    """Finished floor level above the same datum as `flood_level_mm`."""
    return flood_level_mm + slr_allowance(slr_rate_mm_per_year, years) + margin_mm


def infinite_slope_fs(beta_deg, phi_deg, c_kpa=0.0, gamma=SOIL_UNIT_WEIGHT,
                      z_m=SLAB_DEPTH, ru=0.0):
    """Drained infinite-slope factor of safety for a planar soil slope.

    FS = [c' + gamma*z*cos^2(beta)*(1-ru)*tan(phi')] / [gamma*z*sin(beta)*cos(beta)]

    `ru` is the pore-pressure ratio (0 = dry, 1 = hydrostatic). Textbook model:
    planar, homogeneous, infinite, no vegetation, no structure, no anchors,
    no three-dimensional effects. It is a screening indicator, not an analysis.
    """
    beta = math.radians(beta_deg)
    phi = math.radians(phi_deg)
    # At a vertical face the model degenerates: cos(beta) -> 0, so the driving
    # term vanishes and FS would diverge. Return infinity explicitly rather than
    # letting floating-point noise produce a meaningless finite number.
    if math.cos(beta) < 1e-12:
        return float("inf")
    driving = gamma * z_m * math.sin(beta) * math.cos(beta)
    resisting = c_kpa + gamma * z_m * math.cos(beta) ** 2 * (1.0 - ru) * math.tan(phi)
    return resisting / driving


def fs_verdict(fs, factor=MATERIAL_FACTOR):
    """The screen can only escalate. There is no 'pass'."""
    if fs < 1.0:
        return "fails in the model"
    if fs < factor:
        return "below material-factor practice"
    return "above material-factor practice — still needs geotechnical confirmation"


def pressure_depth(p_kpa, gamma=SOIL_UNIT_WEIGHT):
    """Equivalent depth of soil weighing the same as the pressure."""
    return p_kpa / gamma


def pressure_mass(p_kpa):
    """Equivalent mass per square metre."""
    return p_kpa * 1000.0 / 9.80665


def screen(flood_level_mm=EXAMPLE_FLOOD_LEVEL_MM, margin_mm=DEFAULT_MARGIN_MM,
           lives=LIVES, slr_rates=SLR_RATES):
    classes = []
    for name, period in FLOOD_CLASSES.items():
        classes.append({
            "class": name, "hazard": "flood / storm surge", "return_period_years": period,
            "annual": annual_probability(period),
            "within": {str(y): probability_within(y, period) for y in lives},
            "minihouse": name == MINIHOUSE_FLOOD,
        })
    for name, period in LANDSLIDE_CLASSES.items():
        classes.append({
            "class": name, "hazard": "landslide", "return_period_years": period,
            "annual": annual_probability(period),
            "within": {str(y): probability_within(y, period) for y in lives},
            "minihouse": name == MINIHOUSE_LANDSLIDE,
        })

    flood = []
    for rate in slr_rates:
        row = {"slr_mm_per_year": rate,
               "allowance": {str(y): slr_allowance(rate, y) for y in lives}}
        row["ffl"] = {str(y): required_ffl(flood_level_mm, rate, y, margin_mm) for y in lives}
        flood.append(row)

    slopes = []
    for beta in SLOPE_ANGLES:
        for phi in FRICTION_ANGLES:
            fs = infinite_slope_fs(beta, phi)
            slopes.append({
                "beta_deg": beta, "phi_deg": phi,
                "fs": round(fs, 3), "verdict": fs_verdict(fs),
            })

    return {
        "state": "SCREENING — NO SITE, NO HAZARD MAP, NO GEOTECHNICAL ASSESSMENT",
        "minihouse_flood_class": MINIHOUSE_FLOOD,
        "minihouse_landslide_class": MINIHOUSE_LANDSLIDE,
        "outdoor_reduction": "S2 outdoor area may be assessed at the S1 level (1/100)",
        "classes": classes,
        "flood_level_mm": flood_level_mm,
        "margin_mm": margin_mm,
        "flood": flood,
        "slopes": slopes,
        "material_factor": MATERIAL_FACTOR,
        "pressure_ceiling_kpa": PRESSURE_CEILING_KPA,
        "pressure_ceiling_depth_m": round(pressure_depth(PRESSURE_CEILING_KPA), 2),
        "pressure_ceiling_mass_kg_m2": round(pressure_mass(PRESSURE_CEILING_KPA), 0),
    }


def markdown(result):
    f2 = next(c for c in result["classes"] if c["class"] == "F2")
    s2 = next(c for c in result["classes"] if c["class"] == "S2")
    lines = [
        "# MiniHouse · TEK17 chapter 7 natural-hazard screening",
        "",
        "**State:** PROCEDURE — NO SITE, NO HAZARD MAP, NO GEOTECHNICAL ASSESSMENT. "
        "This is a screening method and the arithmetic that can be done before a plot is chosen. "
        "It is not a siting approval, not a flood assessment and not a geotechnical report.",
        "",
        "- Governing route: TEK17 §1-2(2)(a) admits **chapters 1–7 in full** on the mikrohus route.",
        "- Requirements source: S026 (DIBK, TEK17 chapter 7).",
        f"- Assigned classes: **{result['minihouse_flood_class']}** for flood and "
        f"**{result['minihouse_landslide_class']}** for landslide.",
        "- Both classes hold for a dwelling *and* for a holiday home, because both appear in the "
        "§7-2 and §7-3 lists — so the hazard route does **not** wait on C-01.",
        "",
        "## 1. What the safety classes actually mean",
        "",
        "The classes are expressed as a largest nominal annual probability of a damaging event. "
        "An annual probability is hard to feel; the same number over a service life is not.",
        "",
        "| Class | Hazard | Return period | Annual | At least once in 25 y | 50 y | 75 y | MiniHouse |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for c in result["classes"]:
        w = c["within"]
        mark = "**yes**" if c["minihouse"] else "—"
        lines.append(
            f"| {c['class']} | {c['hazard']} | 1/{c['return_period_years']} | "
            f"{c['annual']:.2%} | {w['25']:.1%} | {w['50']:.1%} | {w['75']:.1%} | {mark} |"
        )
    lines += [
        "",
        f"The headline is uncomfortable and worth stating plainly: **{result['minihouse_flood_class']} "
        f"at 1/{f2['return_period_years']} is a {f2['within']['50']:.0%} chance of being exceeded at least "
        "once in 50 years.** That is not a defect in the requirement — it is what a 1/200 target means "
        "when the building is expected to stand for decades. The requirement is met by *placing* the "
        "building where that event does not reach it, which is why chapter 7 is a siting chapter.",
        "",
        "Two refinements that soften the numbers for a small building:",
        "",
        f"- **Outdoor area:** for {result['minihouse_landslide_class']} buildings the associated "
        "outdoor area may be assessed at the **S1 level (1/100)**, because exposure time outdoors "
        "is shorter. It does not change the class for the building itself.",
        "- **The classes are nominal annual probabilities of a damaging event, not predictions.** "
        "They are a design target set by the regulation, not a statement about a particular slope.",
        "",
        "## 2. The gate sequence",
        "",
        "The order matters, because each gate can stop the plot and each one is cheaper than the next.",
        "",
        "| Gate | Question | Evidence | Can stop the plot? |",
        "|---|---|---|---|",
        "| **A** | Where exactly is the plot, and what finished floor level is intended? | coordinates, boundary, access, planned FFL | yes — without these nothing below can be answered |",
        "| **B** | Does the plot intersect a mapped hazard zone? | NVE hazard maps (flood, avalanche, rockfall, debris flow, quick clay), municipal plan hazard zones | yes |",
        "| **C** | Is the plot below the **marine limit**? | NGU loose-material maps, marine-limit line | no, but it forces gate D |",
        "| **D** | Does a special regime apply (quick clay, great depth or strong current)? | NVE quick-clay database, flood-depth/velocity data | yes |",
        "| **E** | Can the hazard be avoided, secured against, or designed for? | §7-2/§7-3 mitigation routes | yes |",
        "| **F** | What does the specialist report say? | geotechnical report, flood assessment, municipal confirmation | yes |",
        "",
        "Gate B is a desk exercise and takes an afternoon. Gate F costs money. The whole point of the "
        "sequence is to spend the afternoon before spending the money.",
        "",
        "## 3. Flood: what the finished floor has to clear",
        "",
        "§7-2 can be met by placing the building outside the area, by securing it against flooding, "
        "or by designing it to withstand inundation without danger to people or major material damage. "
        "Whichever route is taken, the number that matters is the finished floor level.",
        "",
        "Three things add to the mapped flood level, and only one of them is in the regulation:",
        "",
        "1. **The mapped 1/200 level** for the site.",
        "2. **Sea-level rise over the service life.** §7-2's guidance explicitly requires expected "
        "climate change and sea-level rise to be taken into account for storm surge. A cabin near the "
        "Bergen shoreline cannot be assessed against today's sea level.",
        "3. **A margin.** No freeboard figure was retrieved from TEK17, so the value below is a "
        "**project choice, not a regulatory number**, and it is labelled as such in every row.",
        "",
        f"Worked sensitivity with a hypothetical mapped level of **{result['flood_level_mm']:.0f} mm** "
        f"above chart datum and a **{result['margin_mm']:.0f} mm** margin. The mapped level is an "
        "example, not a Bergen value:",
        "",
        "| Sea-level rise | 25 y allowance | 50 y | 75 y | FFL for 25 y | 50 y | 75 y |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["flood"]:
        a, f = row["allowance"], row["ffl"]
        lines.append(
            f"| {row['slr_mm_per_year']:.0f} mm/yr | {a['25']:.0f} | {a['50']:.0f} | {a['75']:.0f} | "
            f"{f['25']:.0f} mm | {f['50']:.0f} mm | {f['75']:.0f} mm |"
        )
    lines += [
        "",
        "Read the table as a rate, not a prediction: **every 1 mm/yr of local sea-level rise adds "
        "50 mm over a 50-year life.** The rate itself has to come from Kartverket for the actual site, "
        "and the service life is a project decision that has not been taken.",
        "",
        "**A light building is not a protected building.** The §7-2 guidance says that where a flood "
        "area would have **great depth or strong current**, the **F3 level (1/1000) should be used** "
        "instead of F2. A cabin is light relative to its volume and can float or be pushed before it is "
        "submerged, so this escalation is a real consideration for this project, not a technicality.",
        "",
        "## 4. Landslide: when a plot is obviously marginal",
        "",
        "§7-3 requires the building **and its outdoor area** to be placed, designed or secured so that "
        "the class probability is not exceeded. For soil slopes the cheapest first question is whether "
        "the slope is anywhere near stable at all.",
        "",
        "The infinite-slope model below is the standard textbook screen. It assumes a planar, "
        "homogeneous, infinitely long slope with no vegetation, no structure and no anchors — none of "
        "which is true of a real Bergen hillside. It is included because it is **conservative enough to "
        "reject a plot** and because it makes the dependence on slope angle and friction explicit.",
        "",
        f"Dry slope, no cohesion, unit weight {SOIL_UNIT_WEIGHT:.0f} kN/m³, sliding plane at "
        f"{SLAB_DEPTH:.1f} m. FS = tan φ / tan β. Required FS is taken as **{MATERIAL_FACTOR:.1f}** "
        "(material factor for field-assessed friction); the Norwegian National Annex is not available "
        "(S014), so **that factor is unverified** and is flagged rather than trusted.",
        "",
        "| Slope β | φ = 30° | 32° | 34° | 36° |",
        "|---:|---:|---:|---:|---:|",
    ]
    for beta in SLOPE_ANGLES:
        cells = []
        for phi in FRICTION_ANGLES:
            row = next(s for s in result["slopes"]
                       if s["beta_deg"] == beta and s["phi_deg"] == phi)
            fs = row["fs"]
            mark = ""
            if fs < 1.0:
                mark = " ✗"
            elif fs < MATERIAL_FACTOR:
                mark = " !"
            cells.append(f"{fs:.2f}{mark}")
        lines.append(f"| {beta:.0f}° | " + " | ".join(cells) + " |")
    lines += [
        "",
        "`✗` fails in the model · `!` below the material factor · unmarked is still not a pass.",
        "",
        "- **At β = 30° and φ = 32° the factor is about 1.08.** A 30° soil slope is already marginal "
        "before any water is added, and pore pressure only makes it worse: the `(1 − ru)` term cuts the "
        "resisting side directly.",
        "- **At 35° every friction angle in the table is at or below the material factor, and at 40° "
        "every one fails outright.** That is not a reason to reject every steep Bergen plot — much "
        "steep terrain there is **rock**, where this model does not apply at all and the hazard is "
        "rockfall, assessed differently. It is a reason to know which one the plot is on.",
        "- **Cohesion and suction are what hold real slopes**, and both are lost when a slope saturates. "
        "A dry-season factor of safety is not a factor of safety.",
        "",
        "## 5. What the ~50 kPa ceiling means",
        "",
        "§7-3 allows a building to be **designed to withstand** landslide forces where the loads are "
        "not too large, and the guidance puts the practical ceiling at approximately "
        f"**{result['pressure_ceiling_kpa']:.0f} kPa**. In physical terms that is:",
        "",
        f"- about **{result['pressure_ceiling_mass_kg_m2']:.0f} kg/m²** — roughly "
        f"{result['pressure_ceiling_mass_kg_m2'] / 1000:.1f} tonnes pressing on every square metre;",
        f"- equivalent to the weight of about **{result['pressure_ceiling_depth_m']:.1f} m of soil** "
        f"at {SOIL_UNIT_WEIGHT:.0f} kN/m³.",
        "",
        "That is a real load, but it is a **small-event** load. A cabin designed for 50 kPa is designed "
        "for the edge of the acceptable range, not for a debris flow that carries boulders. Above that "
        "ceiling the only routes left are siting and protective works — which is why the ceiling is a "
        "siting criterion in disguise.",
        "",
        "## 6. Quick clay: the gate that has no arithmetic",
        "",
        "Quick clay is not screened by a factor of safety on a slope. §7-3 requires an equivalent safety "
        "level for **kvikkleireskred**, and the guidance expands this into *områdeskred* — area "
        "landslides in quick clay and other soils with brittle failure — following NVE guide 1/2019.",
        "",
        "Three properties make it unlike the rest of chapter 7:",
        "",
        "- **The landslide can be far larger than the project.** A hazard zone can extend well beyond "
        "the plot, so a stable-looking site can sit inside an unstable area.",
        "- **Below the marine limit the ground must be investigated even outside identified hazard "
        "zones.** Bergen has marine-limit terrain, so this is a live requirement for this project, "
        "not a formality.",
        "- **The investigation scope is set by a tiltakskategori** (K0–K3) derived from the consequence "
        "for the project. The guidance's K0 examples are small interventions with very limited ground "
        "works and no influx of people — garages, boat houses, extensions, detached outhouses, tool "
        "sheds. **A new dwelling is not on that list**, so a cabin placed as a dwelling cannot be "
        "assumed to be K0.",
        "",
        "There is no calculation here because there is nothing to calculate: the answer is a "
        "geotechnical report by a qualified person, and the only project decision is whether to pay "
        "for it on this plot.",
        "",
        "## 7. Decision rules",
        "",
        "Short forms for the site search. Each one is a stop, not a preference:",
        "",
        "| Finding | Consequence |",
        "|---|---|",
        "| Plot intersects a mapped 1/1000 landslide zone | Not buildable as S2 without protective works or a documented equivalent safety level |",
        "| Plot intersects a mapped 1/200 flood zone | Place outside, raise, secure, or design to withstand; otherwise the plot fails |",
        "| Flood area with great depth or strong current | Escalate to **F3 (1/1000)**, not F2 |",
        "| Plot below the marine limit | Geotechnical investigation required **regardless of mapping** |",
        "| Plot in a quick-clay zone or an area-landslide zone | Siting question first; NVE 1/2019 and a tiltakskategori apply |",
        "| Slope steeper than ~35° in soil | Treat as marginal until a geotechnical report says otherwise |",
        "| Slope steeper than ~35° in rock | Different hazard (rockfall); the soil model in §4 does not apply |",
        "",
        "## 8. What transportability does and does not change",
        "",
        "- **It does not reduce the requirement.** TEK17 assesses the building where it stands. The "
        "fact that the cabin *can* be moved does not lower the class at the site it occupies.",
        "- **It does change the paperwork.** The hazard assessment is not a one-time document for the "
        "cabin; it is a **per-deployment check** that has to be repeated for every new site over the "
        "cabin's life. That is a genuine operational burden of the concept and belongs in the "
        "deployment procedure, not only in the design file.",
        "- **It changes the mitigation economics.** Raising a floor or adding a flood-resistant plinth "
        "is cheaper on a 18 m² module than on a house, and a cabin that is designed for F3 from the "
        "start does not need a new assessment when it moves to a worse plot.",
        "",
        "## 9. Limits",
        "",
        "- **The screen has no pass state.** It can escalate a plot to \"needs a geotechnical report\" "
        "and it can escalate it to \"needs one urgently\". It cannot clear a plot, and nothing below "
        "should be read as if it could.",
        "- **No hazard map has been consulted.** This document records requirements and a method, not "
        "a finding about any plot.",
        "- **No geotechnical, flood or storm-surge assessment has been made** and none can be made by "
        "the agent. Those are specialist reports by qualified people.",
        "- The infinite-slope model in §4 ignores cohesion, suction, vegetation, structure, anchors and "
        "three-dimensional effects, and does not apply to rock slopes.",
        f"- The material factor {MATERIAL_FACTOR:.1f} is unverified against the Norwegian National Annex "
        "(S014).",
        f"- The {result['margin_mm']:.0f} mm flood margin is a **project choice**, not a TEK17 figure.",
        "- Nothing here is a siting approval, a building permit input or a compliance certificate.",
        "",
        "## 10. Source and status",
        "",
        "- TEK17 §§7-1…7-4: S026 (DIBK, retrieved 2026-11-17).",
        "- Class assignment F2/S2: S026, §7-2 and §7-3 pre-accepted lists.",
        "- Generated by `scripts/natural_hazard_screen.py`; JSON companion: "
        "`knowledge/comparisons/natural-hazard-screen.json`.",
        "- SCREENING ONLY — no plot accepted, no plot rejected, no design released.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # F2 is 1/200, and 50 years of it is a 22.2 % chance of at least one event.
    assert abs(annual_probability(200) - 0.005) < 1e-12
    assert abs(probability_within(50, 200) - 0.2217) < 5e-4
    assert abs(probability_within(50, 1000) - 0.0488) < 5e-4
    assert abs(probability_within(50, 100) - 0.3949) < 5e-4
    # A longer life can only increase the probability, and a rarer event decrease it.
    assert probability_within(75, 200) > probability_within(25, 200)
    assert probability_within(50, 1000) < probability_within(50, 200)
    # Flood datum: the three terms add, and the margin is not hidden.
    assert abs(required_ffl(1250.0, 4.0, 50, 300.0) - 1750.0) < 1e-9
    assert abs(required_ffl(1250.0, 0.0, 50, 0.0) - 1250.0) < 1e-9
    # Infinite slope with no cohesion: FS collapses to tan(phi)/tan(beta).
    assert abs(infinite_slope_fs(30.0, 30.0) - 1.0) < 1e-9
    assert abs(infinite_slope_fs(30.0, 32.0) - math.tan(math.radians(32.0))
               / math.tan(math.radians(30.0))) < 1e-9
    assert abs(infinite_slope_fs(30.0, 32.0) - 1.0824) < 5e-4
    # Monotonic in both directions.
    assert infinite_slope_fs(35.0, 32.0) < infinite_slope_fs(30.0, 32.0)
    assert infinite_slope_fs(30.0, 36.0) > infinite_slope_fs(30.0, 32.0)
    # Cohesion raises FS; pore pressure lowers it.
    assert infinite_slope_fs(35.0, 32.0, c_kpa=5.0) > infinite_slope_fs(35.0, 32.0)
    assert infinite_slope_fs(30.0, 32.0, ru=0.5) < infinite_slope_fs(30.0, 32.0)
    # A vertical slope has no driving term in this formulation only at beta=90.
    assert infinite_slope_fs(90.0, 32.0) == float("inf")
    # The verdict can escalate but never clear a plot.
    assert fs_verdict(0.9) == "fails in the model"
    assert fs_verdict(1.2) == "below material-factor practice"
    assert "still needs" in fs_verdict(2.0)
    # 50 kPa in physical terms.
    assert abs(pressure_mass(50.0) - 5099.0) < 2.0
    assert abs(pressure_depth(50.0) - 2.7778) < 1e-3
    result = screen()
    assert len(result["classes"]) == 6
    assert sum(1 for c in result["classes"] if c["minihouse"]) == 2
    assert len(result["slopes"]) == len(SLOPE_ANGLES) * len(FRICTION_ANGLES)
    assert all("still needs" in s["verdict"] or s["fs"] < MATERIAL_FACTOR
               for s in result["slopes"])
    print("Natural-hazard self-test OK: class probabilities, flood datum, "
          "infinite-slope limits and monotonicity, pressure ceiling all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--flood-level", type=float, default=EXAMPLE_FLOOD_LEVEL_MM)
    ap.add_argument("--margin", type=float, default=DEFAULT_MARGIN_MM)
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    result = screen(flood_level_mm=args.flood_level, margin_mm=args.margin)
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
