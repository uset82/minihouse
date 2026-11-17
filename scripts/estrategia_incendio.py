#!/usr/bin/env python3
"""MiniHouse · the chapter 11 determinations, and which clauses move together.

Chapter 11 is the one chapter whose answer is independent of the C-01
dwelling/holiday-home ambiguity: both land in risk class 4, brannklasse 1. The
clauses themselves are verified in S024. What has never been done is to ask
which of the open determinations decide *the same thing* — and the answer is
that two of them do, which matters because the project has been treating them
as three separate questions with three separate prices.

The specific coupling this screen tests:

    §11-13(1)  one exit to a safe place, or exits to two independent routes
    §11-13(4)  the single-direction allowance: exit to a safe place OR to a
               rømningsvei with one direction, provided each fire cell has
               windows arranged for safe escape
    §11-14     free width 0.86 m in the rømningsvei, and in doors in or to it

If the exit from the fire cell leads to a **safe place**, then (4) is not
engaged — it is the alternative that applies when the exit leads to a
rømningsvei — and there is no rømningsvei for §11-14 to govern. So the escape
windows and the 0.86 m door width are the *same* determination, and declaration
rows 2, 3 and 4 are one row wearing three hats.

What is **not** coupled is §11-9's surface class. A fire cell that contains no
rømningsvei is still a fire cell, and the D-s2,d0 row for a cell up to 200 m²
applies to it whatever §11-13 decides. The two questions are separate, and the
obvious misreading — that a strict answer on windows also raises the interior
to B-s1,d0 — is wrong in both directions. It is worth saying so, because the
consequence if it were true (reclaimed timber could not stay exposed) would
drive the concept.

Usage:
  python estrategia_incendio.py --out-md fase1/determinacion-estrategia-incendio.md \
      --out-json knowledge/comparisons/estrategia-incendio.json
  python estrategia_incendio.py --selftest
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fire_check as fc            # noqa: E402
import section_options as so       # noqa: E402
import ventanas_check as vc        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
APERTURAS = ROOT / "fase1" / "tabla-aberturas.csv"

# --- plan geometry, from the R0 layout ---------------------------------------
PLAN_L_MM = 6000.0
PLAN_W_MM = 3000.0
BATHROOM_X_MM = 1200.0        # the bathroom occupies x 0..1200 across the width
DOOR = {"x_min": 4050.0, "x_max": 4950.0, "y": 3000.0}
DOOR_AREA_M2 = 0.900 * 2.050  # the P-01 leaf, from the aperture table

# --- §11-14's distance figures, verbatim from S024 ---------------------------
# The retrieved text gives these for the *door of the fire cell to the nearest
# stair or exit*, not for the travel inside the cell. They are the loosest
# figures the source contains, which is why they bound the check rather than
# decide it.
DOOR_TO_EXIT_ONE_STAIR_M = 15.0
DOOR_TO_EXIT_SEVERAL_M = 30.0


def travel_distance_m():
    """Furthest point of the bathroom from the nearest door jamb.

    Straight line, so it is a **lower bound** on the walking path: furniture,
    the bathroom door and any change of direction all lengthen it. The margin
    computed from it is therefore an upper bound.
    """
    best = 0.0
    worst = None
    for x in (0.0, BATHROOM_X_MM):
        for y in (0.0, PLAN_W_MM):
            # a person leaves by the NEAREST part of the opening, not the far one
            jamb, d = min(((j, math.hypot(x - j, y - DOOR["y"]))
                           for j in (DOOR["x_min"], DOOR["x_max"])), key=lambda p: p[1])
            if d > best:
                best, worst = d, (x, y, jamb)
    return best / 1000.0, worst


def interior_timber_m2(stud_fraction=0.15):
    """Exposed interior timber area at the R0 reference section.

    Walls plus ceiling, with the gable triangles, minus the openings. It moves
    with whichever R2 option is chosen, because the eave height moves; the
    reference case is the only section the project has solved.
    """
    depths = so.build_up_depths(stud_fraction)
    h_eave = so.max_wall_height(so.REFERENCE["pitch"], so.REFERENCE["stack"],
                                depths["floor_mm"], depths["roof_mm"],
                                so.REFERENCE["limit"])
    rise = (PLAN_W_MM / 2.0) * math.tan(math.radians(so.REFERENCE["pitch"]))
    long_walls = 2.0 * PLAN_L_MM * h_eave
    gables = 2.0 * (PLAN_W_MM * h_eave + 0.5 * PLAN_W_MM * rise)
    ceiling = (PLAN_L_MM * PLAN_W_MM) / math.cos(math.radians(so.REFERENCE["pitch"]))
    gross = (long_walls + gables + ceiling) / 1e6

    openings = vc.read_openings(APERTURAS)
    holes = sum(o["gross_m2"] for o in openings) + DOOR_AREA_M2
    return {
        "eave_mm": round(h_eave, 1),
        "ridge_mm": round(h_eave + rise, 1),
        "long_walls_m2": round(long_walls / 1e6, 2),
        "gables_m2": round(gables / 1e6, 2),
        "ceiling_m2": round(ceiling / 1e6, 2),
        "gross_m2": round(gross, 2),
        "openings_m2": round(holes, 2),
        "net_m2": round(gross - holes, 2),
    }


# --- the two coherent packages ----------------------------------------------
PACKAGES = (
    {
        "id": "P1",
        "name": "the door discharges to a safe place",
        "basis": "§11-13(1) satisfied directly — one exit to a safe place",
        "engaged": {"§11-13(1)": True, "§11-13(4)": False,
                    "§11-14": False, "§11-17": True},
        "windows": "none required as escape windows",
        "width": "§11-14 does not apply: there is no rømningsvei to be in or to",
        "rows": {2: "not required", 3: "not required", 4: "not required"},
        "cost": "nothing",
        "risk": "the municipality may not accept grade outside the door as a safe place",
    },
    {
        "id": "P2",
        "name": "the exit leads to a rømningsvei with one direction",
        "basis": "§11-13(4) engaged — the allowance needs qualifying windows in every cell",
        "engaged": {"§11-13(1)": True, "§11-13(4)": True,
                    "§11-14": True, "§11-17": True},
        "windows": "a qualifying window in every room without a direct exit",
        "width": "§11-14 applies: 0.86 m free width in the door",
        "rows": {2: "mandatory", 3: "mandatory", 4: "mandatory"},
        "cost": "0.29 m² of glass and a 100 mm sill drop",
        "risk": "none — this is the conservative answer, and it is buildable",
    },
)

# §11-9 is a separate determination. The reason is stated, not asserted.
NOT_COUPLED = (
    ("§11-9 surfaces", "D-s2,d0 walls and ceiling (cell ≤200 m²)",
     "a fire cell that contains no rømningsvei is still a fire cell, and the "
     "≤200 m² row applies to it whatever §11-13 decides"),
    ("§11-9 cladding", "K210 D-s2,d0", "the cladding is metal, so it meets either row without a product choice"),
    ("§11-9 insulation", "A2-s1,d0", "already forced by §11-4(3) no. 6 as well; the roof is mineral wool either way"),
    ("§11-17 fire service", "one accessible window", "applies on both packages, and V-01 already satisfies it"),
)


def screen():
    distance, worst = travel_distance_m()
    timber = interior_timber_m2()
    openings = vc.read_openings(APERTURAS)
    win = vc.screen(openings)
    # The union at a usable width, not one reading's minimum: P2 has to satisfy
    # every reading, so its price is the recommended set.
    union = win["recommended"]

    return {
        "state": "DETERMINATION — NOT A FIRE-ENGINEERING ANALYSIS, NOT A COMPLIANCE STATEMENT",
        "basis": {"sources": ["S024"], "risk_class": fc.RISIKOKLASSE,
                  "fire_class": fc.BRANNKLASSE},
        "coupling": {
            "clauses": ["§11-13(4)", "§11-14"],
            "rows": [2, 3, 4],
            "reason": "both are engaged by whether the exit leads to a safe place "
                      "or to a rømningsvei, which is one question",
        },
        "packages": [
            {**p, "window_cost": {
                "added_glass_m2": round(sum(c["added_glass_m2"] for c in union["changes"]), 4),
                "changes": union["changes"],
                "min_lt_after": win["convergence"]["0.85"]["min_lt_after"],
            } if p["id"] == "P2" else None}
            for p in PACKAGES
        ],
        "not_coupled": [{"clause": c, "value": v, "why": w} for c, v, w in NOT_COUPLED],
        "travel": {
            "max_internal_m": round(distance, 2),
            "from": {"x_mm": worst[0], "y_mm": worst[1], "jamb_mm": worst[2]},
            "door_to_exit_one_stair_m": DOOR_TO_EXIT_ONE_STAIR_M,
            "door_to_exit_several_m": DOOR_TO_EXIT_SEVERAL_M,
            "margin_vs_loosest_m": round(DOOR_TO_EXIT_ONE_STAIR_M - distance, 2),
            "note": "straight line, so a lower bound on the path and an upper bound on the margin",
        },
        "timber": timber,
        "door": {"leaf_mm": 900.0, "required_mm": fc.MIN_FREE_WIDTH_MM,
                 "nominal_margin_mm": 40.0},
        "excluded": ["fire-engineering analysis", "municipal decision",
                     "product documentation for B-s1,d0 timber", "compliance statement"],
    }


def markdown(model):
    c = model["coupling"]
    t = model["travel"]
    timber = model["timber"]
    p1, p2 = model["packages"]

    L = [
        "# MiniHouse · the chapter 11 determinations, and which clauses move together",
        "",
        "**State:** DETERMINATION — NOT A FIRE-ENGINEERING ANALYSIS, NOT A COMPLIANCE "
        "STATEMENT. Nothing here decides what the municipality will accept; it decides "
        "which question to put to it, and prices both answers.",
        "",
        "- Basis: the verified clause texts in S024 read against the **R0 layout**. Risk class "
        f"{model['basis']['risk_class']}, brannklasse {model['basis']['fire_class']}.",
        "- The window cost is imported from the window screen and the door figures from the "
        "fire screen, so this report cannot drift from either.",
        "- **Screening values**, not measurements: the travel distance is a straight line and "
        "the timber area is computed at the reference section.",
        "",
        "## 1. What this adds",
        "",
        "Chapter 11's clauses are verified in [S024](../knowledge/sources/S024.md), and the "
        "project has priced several of its open questions separately: the escape windows in "
        "[the window screen](verificacion-ventanas.md), the roof branch in "
        "[the roof determination](determinacion-cubierta-incendio.md), the door width in "
        "[the fire screen](verificacion-incendio.md). What nobody has asked is whether two of "
        "those questions are the same question — and two of them are.",
        "",
        "## 2. The coupling",
        "",
        "> §11-13(4): «… kan utgangen fra branncelle enten føre til **sikkert sted**, eller "
        "til **rømningsvei** som bare har én rømningsretning, forutsatt at hver branncelle har "
        "vinduer …»",
        "",
        "The allowance is written as an **alternative**: either the exit leads to a safe place, "
        "*or* it leads to a rømningsvei with one direction and then the windows are required. "
        "It is not a permission that applies on top of a safe-place exit.",
        "",
        "§11-14 then governs the **rømningsvei** — its free width, and the width of doors in or "
        "to it. If there is no rømningsvei, §11-14 has nothing to govern.",
        "",
        "So one answer decides both, and with them three rows of the declaration of margins:",
        "",
        "| Clause | Engaged when the exit reaches a safe place | Engaged when it reaches a rømningsvei |",
        "|---|---|---|",
        "| §11-13(1) | yes — that is how it is satisfied | yes — via the (4) allowance |",
        "| §11-13(4) windows | **no** | **yes** |",
        "| §11-14 free width | **no** | **yes** |",
        "| §11-17 fire service | yes | yes |",
        "",
        f"Declaration rows **{', '.join(str(r) for r in c['rows'])}** are therefore not three "
        "margins. They are one determination read three ways, and the table has been carrying "
        "them as if they were independent.",
        "",
        "## 3. The two packages, priced",
        "",
        "| | **P1** — safe place | **P2** — rømningsvei |",
        "|---|---|---|",
    ]
    for key, label in (("name", "Reading"), ("basis", "Basis"), ("windows", "Windows"),
                       ("width", "Door width"), ("cost", "Cost"), ("risk", "Risk")):
        L.append(f"| {label} | {p1[key]} | {p2[key]} |")
    L += [
        "",
        f"**P2's window cost is the one already measured**: "
        f"{p2['window_cost']['added_glass_m2']:.2f} m² of added glass, a 100 mm sill drop on "
        f"V-02, and the minimum light transmittance requirement falls to "
        f"{p2['window_cost']['min_lt_after']:.3f} — the only lever in the project that closes "
        "two screens at once.",
        "",
        "**P1's cost is nothing, and that is the whole difficulty.** It is the answer the "
        "design wants, it is available on the text, and it is the answer a project is least "
        "entitled to award itself.",
        "",
        "## 4. What is *not* coupled, and why it matters",
        "",
        "The obvious next step is to say that a strict answer on windows also raises the "
        "interior surfaces to **B-s1,d0** under §11-9, and that reclaimed timber therefore "
        "cannot stay exposed. **That is wrong, and it is wrong in both directions.**",
        "",
        "§11-9 Table 1A separates fire cells that *are* an escape route from those that are "
        "not. In the ordinary reading a rømningsvei is a route **outside** the fire cell — the "
        "cell's exit leads to it — so a cell that contains none is not one. "
        "A cell that contains no rømningsvei is still a cell, so the ≤200 m² row applies to it "
        "whatever §11-13 decides. The two questions are independent:",
        "",
        "| Clause | Value either way | Why it does not move |",
        "|---|---|---|",
    ]
    for row in model["not_coupled"]:
        L.append(f"| {row['clause']} | **{row['value']}** | {row['why']} |")

    L += [
        "",
        "This cuts both ways and both are worth stating. A strict answer on windows does **not** "
        "condemn the timber interior. And a favourable answer on windows does **not** entitle "
        "the project to call the interior an escape route's surface either — the D-s2,d0 row "
        "applies on its own terms.",
        "",
        "## 5. Travel distance: satisfied, and the table row is still missing",
        "",
        f"The furthest point of the bathroom from the nearest door jamb is "
        f"**{t['max_internal_m']:.2f} m** — from ({t['from']['x_mm']:.0f}, "
        f"{t['from']['y_mm']:.0f}) mm to the jamb at {t['from']['jamb_mm']:.0f} mm. That is a "
        "**straight line**, so it is a lower bound on the walking path and the margin below is "
        "an upper bound.",
        "",
        "| Figure | Value | Source |",
        "|---|---:|---|",
        f"| Maximum internal distance | **{t['max_internal_m']:.2f} m** | plan geometry, straight line |",
        f"| Door of the fire cell to the nearest exit, one stair | {t['door_to_exit_one_stair_m']:.0f} m | §11-14, S024 |",
        f"| Same, several stairs or exits | {t['door_to_exit_several_m']:.0f} m | §11-14, S024 |",
        "",
        f"So the margin against the loosest figure the retrieved text contains is "
        f"**+{t['margin_vs_loosest_m']:.1f} m**. But §11-14's figures are for the distance from "
        "the **door of the fire cell** to the nearest stair or exit — not for travel inside the "
        "cell — and the §11-13 Table 1 row for risk class 4 is **not in the retrieved text**. "
        "The honest statement is therefore: the cabin's internal distance is small, it is "
        "comfortably inside every figure the source does contain, and the applicable row has "
        "never been read.",
        "",
        "This is the one place in chapter 11 where the answer is very unlikely to be the "
        "constraint. It should still be confirmed rather than assumed, because the number is "
        "cheap to check and the assumption would be invisible in the drawing.",
        "",
        "## 6. The door, under each package",
        "",
        f"§11-14 asks for **{model['door']['required_mm']:.0f} mm** free width in risk class 4. "
        f"A {model['door']['leaf_mm']:.0f} mm leaf is "
        f"**{model['door']['nominal_margin_mm']:.0f} mm** wider than that, which is where "
        "declaration row 2's +40 mm comes from — and the declaration already says it is not a "
        "margin, because the free width is the leaf minus a frame and hinge build-up nobody has "
        "specified.",
        "",
        "Under **P1** the clause does not apply at all, so the 900 mm leaf stops being a "
        "requirement and becomes a choice. That does not make the door better; it means the "
        "project would be choosing 900 mm for reasons of its own, and should say so rather than "
        "book it as a margin.",
        "",
        "Under **P2** the clause applies and the +40 mm is a real margin on a real requirement — "
        "still undemonstrated, for the reason the adequacy screen gives.",
        "",
        "## 7. The question to put, and it is one question",
        "",
        "The project has been carrying the window question and the door-width question as "
        "separate items. They are one. The technical cupboard, the escape-route classification "
        "and the travel distance are genuinely separate, and none of them is decided here. Put "
        "the coupled pair as one question with two priced answers:",
        "",
        "> **Does the exit from the cabin lead directly to a safe place, or to a rømningsvei "
        "with a single escape direction?**",
        "",
        "If a safe place: no escape windows are required, §11-14 does not apply, and the "
        "aperture table stands as drawn.",
        "",
        "If a rømningsvei: every room without a direct exit needs a qualifying window, the door "
        "needs 0.86 m free width, and both are buildable for 0.29 m² of glass and a 100 mm sill.",
        "",
        "Either way, the interior surfaces stay **D-s2,d0** unless the municipality separately "
        "decides the cabin *is* an escape route — which is the one answer that would put the "
        "reclaimed timber in question, and it is a different question from this one.",
        "",
        "## 8. Limits",
        "",
        "- The determinations here are readings of S024 against the R0 layout. They are **not** "
        "a fire-engineering analysis and **not** a municipal decision.",
        "- The travel distance is a straight line from a room corner to a door jamb. The real "
        "path is longer, and the bathroom door is not modelled.",
        f"- The interior timber area, **{timber['net_m2']:.1f} m²**, is computed at the R0 "
        f"reference section (eave {timber['eave_mm']:.0f} mm, ridge {timber['ridge_mm']:.0f} mm) "
        "and moves with whichever R2 option is chosen.",
        "- No B-s1,d0 product is specified, so no cost is attached to the surface class. The "
        "area is given so that the cost can be priced when a product exists.",
        "- Nothing here is a compliance statement, a fire strategy or a design release.",
        "",
        "- Generated by `scripts/estrategia_incendio.py`; JSON companion: "
        "`knowledge/comparisons/estrategia-incendio.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    model = screen()

    # The coupling must name both clauses and all three rows, or the screen's
    # whole point is lost.
    assert set(model["coupling"]["clauses"]) == {"§11-13(4)", "§11-14"}
    assert model["coupling"]["rows"] == [2, 3, 4]

    # P1 must switch (4) and §11-14 off; P2 must switch both on. If either
    # package stops being internally consistent this fails.
    p1, p2 = model["packages"]
    assert p1["engaged"]["§11-13(4)"] is False and p1["engaged"]["§11-14"] is False
    assert p2["engaged"]["§11-13(4)"] is True and p2["engaged"]["§11-14"] is True
    # §11-17 applies on both — it is not part of the coupling.
    assert p1["engaged"]["§11-17"] and p2["engaged"]["§11-17"]
    # and the rows must follow the engagement, not be listed independently
    assert p1["rows"] == {2: "not required", 3: "not required", 4: "not required"}
    assert all(v == "mandatory" for v in p2["rows"].values())

    # §11-9 must be declared NOT coupled, with all four rows present.
    assert len(model["not_coupled"]) == 4
    assert any(r["clause"] == "§11-9 surfaces" for r in model["not_coupled"])

    # Travel distance: inside the plan diagonal, and well inside the loosest
    # figure in the source. Both bounds, not just the convenient one.
    t = model["travel"]
    diagonal = math.hypot(PLAN_L_MM, PLAN_W_MM) / 1000.0
    assert 0.0 < t["max_internal_m"] < diagonal, (t["max_internal_m"], diagonal)
    assert t["margin_vs_loosest_m"] > 5.0, t["margin_vs_loosest_m"]

    # The timber area must be physically plausible for an 18 m² plan: bigger
    # than the floor, smaller than twice it plus the walls.
    timber = model["timber"]
    assert 18.0 < timber["net_m2"] < 70.0, timber["net_m2"]
    assert timber["gross_m2"] - timber["openings_m2"] == timber["net_m2"] or \
        abs((timber["gross_m2"] - timber["openings_m2"]) - timber["net_m2"]) < 0.05

    # P2's window cost must come from the window screen, not be retyped — and it
    # must be the UNION at a usable width (0.29 m2 over two windows), not one
    # reading's minimum, because P2 has to satisfy every reading.
    assert abs(p2["window_cost"]["added_glass_m2"] - 0.29) < 0.01, p2["window_cost"]
    assert len(p2["window_cost"]["changes"]) == 2, p2["window_cost"]["changes"]
    assert {c["id"] for c in p2["window_cost"]["changes"]} == {"V-02", "V-03"}
    assert 0.4 < p2["window_cost"]["min_lt_after"] < 0.7

    # The door figures must be the fire screen's, not this file's.
    assert model["door"]["required_mm"] == fc.MIN_FREE_WIDTH_MM
    assert abs(model["door"]["leaf_mm"] - model["door"]["required_mm"]
               - model["door"]["nominal_margin_mm"]) < 1e-9

    print(f"Chapter 11 determination self-test OK: §11-13(4) and §11-14 coupled to one "
          f"question and to rows 2/3/4, both packages internally consistent, §11-9 declared "
          f"independent, travel {t['max_internal_m']:.2f} m against a "
          f"{t['door_to_exit_one_stair_m']:.0f} m figure, and "
          f"{timber['net_m2']:.1f} m² of interior timber")


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
