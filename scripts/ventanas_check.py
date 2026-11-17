#!/usr/bin/env python3
"""MiniHouse · escape windows (§11-13) priced against daylight (§13-7).

§11-13 admits three readings for a one-room transportable cabin, and the R0
aperture table passes one of them while failing the other two. Rather than pick
a reading, this screen prices all three against the same table and then runs
each resulting aperture set through the §13-7 daylight requirement, so the
escape decision and the daylight decision are read off one set of numbers.

The definitions of "qualifies as an escape window" and "qualifying glass area"
are imported from fire_check and daylight_check rather than restated, so the
three screens cannot drift apart.

This is a screening tool. It does not decide the interpretation, does not
certify compliance and is not a fire strategy.

Usage:
  python ventanas_check.py fase1/tabla-aberturas.csv \
      --out-md fase1/verificacion-ventanas.md \
      --out-json knowledge/comparisons/ventanas.json
  python ventanas_check.py --selftest
"""
import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from daylight_check import COEFFICIENT, FRAME_FACTORS, LT_SCENARIOS, qualifying_area_m2
from fire_check import (
    ESCAPE_MAX_SILL_MM,
    ESCAPE_MIN_HEIGHT_MM,
    ESCAPE_MIN_SUM_MM,
    ESCAPE_MIN_WIDTH_MM,
    escape_window,
)
from envelope_check import U_LIMITS
from puentes_termicas import PSI_SCENARIOS

# --- plan -------------------------------------------------------------------
# x is longitudinal; the bathroom occupies x 0..1200 (geometria-R0.md, S-04).
ROOMS = (
    {"id": "BATH", "name": "bathroom", "x_min": 0.0, "x_max": 1200.0,
     "direct_exit": False, "back_wall_mm": 1200.0, "gable_wall_mm": 3000.0},
    {"id": "MAIN", "name": "main room", "x_min": 1200.0, "x_max": 6000.0,
     "direct_exit": True, "back_wall_mm": 3000.0, "gable_wall_mm": 3000.0},
)
ABRA_M2 = 18.0
ROOM_HEIGHT_MM = 2200.0
PERIMETER_M = 18.0

# --- the three readings ------------------------------------------------------
READINGS = (
    {
        "id": "R-A",
        "name": "minimal",
        "short": "the door to grade is a safe place; (4) not engaged",
        "needs": (),
        "basis": "§11-13(1) needs one exit to a safe place, and the door discharges to "
                 "grade. §11-13(4) relaxes the two-direction rule; if the exit already "
                 "reaches a safe place, (4) is not engaged.",
        "weakness": "the safe place is a site condition, not a property of the module. "
                    "A transportable cabin cannot carry its escape strategy in its siting.",
    },
    {
        "id": "R-B",
        "name": "fire cell",
        "short": "the cell needs «vinduer», plural",
        "needs": ("two_in_cell",),
        "basis": "§11-13(4) engaged: «hver branncelle har vinduer» — the cell needs at "
                 "least two qualifying windows.",
        "weakness": "turns on whether the plural in «vinduer» binds for a one-room cell.",
    },
    {
        "id": "R-C",
        "name": "room by room",
        "short": "the bathroom has no direct exit",
        "needs": ("room_without_exit",),
        "basis": "every room without a direct exit needs its own qualifying window; here "
                 "that is the bathroom, whose only opening is V-03.",
        "weakness": "not stated in §11-13 as retrieved; it is guidance practice.",
    },
)

# --- preferred enlargement ---------------------------------------------------
USABLE_MIN_WIDTH_MM = 900.0   # see §3 of the report: 600..900 all cost the same area


def room_of(x_centre_mm):
    for room in ROOMS:
        if room["x_min"] <= x_centre_mm < room["x_max"]:
            return room["id"]
    raise ValueError(f"opening at x={x_centre_mm} mm is outside the plan")


def read_openings(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    openings = []
    for row in rows:
        ident = row["id"].strip()
        if not ident.upper().startswith("V-"):
            continue
        width = float(row["ancho_mm"])
        height = float(row["alto_mm"])
        sill = float(row["z_antepecho_mm"])
        x_centre = float(row["x_centro_mm"])
        verdict = escape_window(width, height, sill)
        openings.append({
            "id": ident,
            "room": room_of(x_centre),
            "facade": row["fachada"].strip(),
            "x_centre_mm": x_centre,
            "width_mm": width,
            "height_mm": height,
            "sill_mm": sill,
            "gross_m2": round(width * height / 1e6, 4),
            "qualifying_m2": round(qualifying_area_m2(width, height, sill), 4),
            "escape_qualifies": verdict["qualifies"],
            "escape_fails": verdict["fails"],
        })
    if not openings:
        raise SystemExit("ERROR: no window rows (V-*) found")
    return openings


def smallest_qualifying(width_mm, height_mm, sill_mm,
                        min_width_mm=ESCAPE_MIN_WIDTH_MM):
    """Smallest enlargement of one opening that satisfies §11-13(4).

    Never shrinks a dimension. Raises the height until the sum rule is met and
    lowers the sill to the limit, so the returned triple always qualifies.
    """
    w = max(width_mm, min_width_mm)
    h = max(height_mm, ESCAPE_MIN_HEIGHT_MM, ESCAPE_MIN_SUM_MM - w)
    s = min(sill_mm, ESCAPE_MAX_SILL_MM)
    return w, h, s


def enlarge(opening, min_width_mm=ESCAPE_MIN_WIDTH_MM):
    w, h, s = smallest_qualifying(opening["width_mm"], opening["height_mm"],
                                  opening["sill_mm"], min_width_mm)
    return {
        **opening,
        "width_mm": w,
        "height_mm": h,
        "sill_mm": s,
        "gross_m2": round(w * h / 1e6, 4),
        "qualifying_m2": round(qualifying_area_m2(w, h, s), 4),
        "escape_qualifies": True,
        "escape_fails": [],
    }


def change_record(before, after):
    return {
        "id": before["id"],
        "room": before["room"],
        "from_mm": f"{before['width_mm']:.0f} × {before['height_mm']:.0f} @ sill "
                   f"{before['sill_mm']:.0f}",
        "to_mm": f"{after['width_mm']:.0f} × {after['height_mm']:.0f} @ sill "
                 f"{after['sill_mm']:.0f}",
        "added_glass_m2": round(after["gross_m2"] - before["gross_m2"], 4),
        "added_qualifying_m2": round(after["qualifying_m2"] - before["qualifying_m2"], 4),
    }


def solve(reading, openings, min_width_mm=ESCAPE_MIN_WIDTH_MM):
    """Cheapest modification set that satisfies one reading."""
    mods = [dict(o) for o in openings]
    changes = []
    if "two_in_cell" in reading["needs"]:
        while sum(1 for o in mods if o["escape_qualifies"]) < 2:
            candidates = [o for o in mods if not o["escape_qualifies"]]
            if not candidates:
                raise SystemExit("ERROR: cannot reach two qualifying windows")
            cheapest = min(
                candidates,
                key=lambda o: enlarge(o, min_width_mm)["gross_m2"] - o["gross_m2"])
            idx = mods.index(cheapest)
            after = enlarge(cheapest, min_width_mm)
            mods[idx] = after
            changes.append(change_record(cheapest, after))
    if "room_without_exit" in reading["needs"]:
        for room in ROOMS:
            if room["direct_exit"]:
                continue
            if any(o["room"] == room["id"] and o["escape_qualifies"] for o in mods):
                continue
            in_room = [o for o in mods if o["room"] == room["id"]]
            if not in_room:
                raise SystemExit(f"ERROR: room {room['id']} has no opening to enlarge")
            cheapest = min(
                in_room,
                key=lambda o: enlarge(o, min_width_mm)["gross_m2"] - o["gross_m2"])
            idx = mods.index(cheapest)
            after = enlarge(cheapest, min_width_mm)
            mods[idx] = after
            changes.append(change_record(cheapest, after))
    return mods, changes


def solve_union(openings, min_width_mm=ESCAPE_MIN_WIDTH_MM):
    """The set that satisfies every reading at once."""
    mods = [dict(o) for o in openings]
    changes = []
    for reading in READINGS:
        mods, reading_changes = solve(reading, mods, min_width_mm)
        changes.extend(reading_changes)
    return mods, changes


def daylight(openings):
    qualifying = sum(o["qualifying_m2"] for o in openings)
    gross = sum(o["gross_m2"] for o in openings)
    minimum_lt = {
        f"{ff:.2f}": round(COEFFICIENT * ABRA_M2 / (qualifying * ff), 4)
        for ff in FRAME_FACTORS
    }
    grid = []
    for lt in LT_SCENARIOS:
        required = COEFFICIENT * ABRA_M2 / lt
        row = {"LT": lt, "required_m2": round(required, 4), "by_frame_factor": {}}
        for ff in FRAME_FACTORS:
            effective = qualifying * ff
            row["by_frame_factor"][f"{ff:.2f}"] = {
                "effective_m2": round(effective, 4),
                "pass": effective >= required,
                "margin_m2": round(effective - required, 4),
            }
        grid.append(row)
    return {
        "gross_m2": round(gross, 4),
        "qualifying_m2": round(qualifying, 4),
        "minimum_lt": minimum_lt,
        "grid": grid,
    }


def heat_loss(openings, door_m2=0.900 * 2.050, door_perimeter_m=2 * (0.900 + 2.050)):
    """Marginal heat loss of the added glazing, at the §14-3 element limits.

    Adding glass displaces wall but lengthens the opening perimeter, so the two
    effects have opposite signs on the element loss and the same sign on the
    bridge loss. Both are computed, because they do not cancel.
    """
    area = sum(o["gross_m2"] for o in openings)
    perimeter = sum(2.0 * (o["width_mm"] + o["height_mm"]) for o in openings) / 1000.0
    u_wall = U_LIMITS["wall"]
    u_window = U_LIMITS["window"]
    opaque = PERIMETER_M * ROOM_HEIGHT_MM / 1000.0 - area - door_m2
    elements = (
        opaque * u_wall
        + ABRA_M2 * U_LIMITS["roof"]
        + ABRA_M2 * U_LIMITS["floor"]
        + area * u_window
        + door_m2 * u_window
    )
    return {
        "u_wall": u_wall,
        "u_window": u_window,
        "opaque_wall_m2": round(opaque, 4),
        "elements_w_per_k": round(elements, 4),
        "delta_per_m2_w_per_k": round(u_window - u_wall, 4),
        "opening_perimeter_m": round(perimeter + door_perimeter_m, 4),
        "reveal_psi_w_per_mk": PSI_SCENARIOS["ordinary"]["reveal"],
    }


def screen(openings):
    current = [dict(o) for o in openings]
    readings = []
    for reading in READINGS:
        mods, changes = solve(reading, current)
        readings.append({
            "id": reading["id"],
            "name": reading["name"],
            "short": reading["short"],
            "basis": reading["basis"],
            "weakness": reading["weakness"],
            "changes": changes,
            "qualifying_windows": [o["id"] for o in mods if o["escape_qualifies"]],
            "qualifying_count": sum(1 for o in mods if o["escape_qualifies"]),
            "added_glass_m2": round(sum(c["added_glass_m2"] for c in changes), 4),
            "daylight": daylight(mods),
        })

    minimum, minimum_changes = solve_union(current)
    recommended, recommended_changes = solve_union(current, USABLE_MIN_WIDTH_MM)
    current_daylight = daylight(current)
    recommended_daylight = daylight(recommended)

    convergence = {}
    for ff in FRAME_FACTORS:
        key = f"{ff:.2f}"
        before = current_daylight["minimum_lt"][key]
        after = recommended_daylight["minimum_lt"][key]
        convergence[key] = {
            "min_lt_before": before,
            "min_lt_after": after,
            "relief": round(before - after, 4),
        }

    loss = heat_loss(current)
    loss_after = heat_loss(recommended)
    loss["delta_glass_w_per_k"] = round(
        sum(c["added_glass_m2"] for c in recommended_changes)
        * loss["delta_per_m2_w_per_k"], 4)
    loss["delta_reveal_w_per_k"] = round(
        (loss_after["opening_perimeter_m"] - loss["opening_perimeter_m"])
        * loss["reveal_psi_w_per_mk"], 4)
    loss["delta_w_per_k"] = round(
        loss["delta_glass_w_per_k"] + loss["delta_reveal_w_per_k"], 4)
    loss["share_of_elements"] = round(loss["delta_w_per_k"] / loss["elements_w_per_k"], 4)
    loss["added_glass_m2"] = round(
        sum(c["added_glass_m2"] for c in recommended_changes), 4)
    loss["added_perimeter_m"] = round(
        loss_after["opening_perimeter_m"] - loss["opening_perimeter_m"], 4)

    return {
        "state": "SCREENING — CONDITIONAL ON C-01",
        "current": {
            "openings": current,
            "qualifying_windows": [o["id"] for o in current if o["escape_qualifies"]],
            "qualifying_count": sum(1 for o in current if o["escape_qualifies"]),
            "daylight": current_daylight,
        },
        "readings": readings,
        "minimum": {
            "changes": minimum_changes,
            "openings": minimum,
            "qualifying_windows": [o["id"] for o in minimum if o["escape_qualifies"]],
            "qualifying_count": sum(1 for o in minimum if o["escape_qualifies"]),
            "added_glass_m2": round(sum(c["added_glass_m2"] for c in minimum_changes), 4),
            "daylight": daylight(minimum),
        },
        "recommended": {
            "min_width_mm": USABLE_MIN_WIDTH_MM,
            "changes": recommended_changes,
            "openings": recommended,
            "qualifying_windows": [o["id"] for o in recommended if o["escape_qualifies"]],
            "qualifying_count": sum(1 for o in recommended if o["escape_qualifies"]),
            "added_glass_m2": round(
                sum(c["added_glass_m2"] for c in recommended_changes), 4),
            "daylight": recommended_daylight,
        },
        "convergence": convergence,
        "heat_loss": loss,
    }


def markdown(result, source_path):
    cur = result["current"]
    minimum = result["minimum"]
    recommended = result["recommended"]
    loss = result["heat_loss"]

    lines = [
        "# MiniHouse · escape windows (§11-13) against daylight (§13-7)",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a fire strategy, not a daylight "
        "simulation, not a compliance certificate.",
        "",
        f"- Aperture table: `{source_path}` (R0 conceptual, unchanged by this screen).",
        "- §11-13 from S024; §13-7 simplified dwelling route from S023.",
        "- Escape-window and qualifying-glass definitions are imported from `fire_check.py` "
        "and `daylight_check.py`, so the three screens share one definition each.",
        "",
        "## 1. What §11-13 requires, and the sentence that is easy to misread",
        "",
        "§11-13(1) asks for **one exit to a safe place**, or exits to two independent escape "
        "routes, or one exit to an escape route with two directions. §11-13(4) then allows "
        "the exit from a fire cell to lead to a **single-direction** escape route, "
        "«forutsatt at hver branncelle har **vinduer** som er utformet og tilrettelagt for "
        "sikker rømning».",
        "",
        "The dimensions table in S024 also carries the line **«one accessible escape window "
        "is sufficient in a dwelling unit»**. That sentence sits under *fire-service access*, "
        "and it is about the window the fire service can reach under §11-17 — it is **not** a "
        "relaxation of «vinduer» in §11-13(4). Reading it as one would make the current table "
        "pass. It should not be read that way.",
        "",
        "So the requirement attaches to the **fire cell**, and whether the cabin's single "
        "door to grade already satisfies §11-13(1) decides whether §11-13(4) is engaged at "
        "all. That is a determination, not a calculation. What this screen can do is price "
        "each answer.",
        "",
        "## 2. The room model",
        "",
        "| Room | x range mm | Direct exit | Openings |",
        "|---|---|---|---|",
    ]
    for room in ROOMS:
        in_room = [o["id"] for o in cur["openings"] if o["room"] == room["id"]]
        lines.append(
            f"| {room['name']} | {room['x_min']:.0f}–{room['x_max']:.0f} | "
            f"{'yes — P-01' if room['direct_exit'] else '**no**'} | "
            f"{', '.join(in_room) if in_room else '—'} |")
    lines += [
        "",
        "The bathroom has **no direct exit** and one opening, V-03, which does not qualify. "
        "That is the structural fact the three readings disagree about.",
        "",
        "## 3. The current table",
        "",
        "| ID | Room | Size mm | Sill mm | h+w mm | Qualifies | Fails | Qualifying glass m² |",
        "|---|---|---|---:|---:|---|---|---:|",
    ]
    room_name = {r["id"]: r["name"] for r in ROOMS}
    for o in cur["openings"]:
        lines.append(
            f"| {o['id']} | {room_name[o['room']]} | {o['width_mm']:.0f} × {o['height_mm']:.0f} | "
            f"{o['sill_mm']:.0f} | {o['width_mm'] + o['height_mm']:.0f} | "
            f"{'yes' if o['escape_qualifies'] else '**no**'} | "
            f"{', '.join(o['escape_fails']) if o['escape_fails'] else '—'} | "
            f"{o['qualifying_m2']:.3f} |")
    lines += [
        "",
        f"**{cur['qualifying_count']} qualifying escape window** "
        f"({', '.join(cur['qualifying_windows'])}). V-02 fails **only** on the sill — "
        "100 mm too high. V-03 fails on three counts.",
        "",
        "## 4. The three readings, priced",
        "",
        "| Reading | What it requires | Changes needed | Added glass m² | Resulting qualifying windows |",
        "|---|---|---|---:|---|",
    ]
    for r in result["readings"]:
        change_text = "; ".join(
            f"{c['id']} {c['from_mm']} → {c['to_mm']}" for c in r["changes"]) or "none"
        lines.append(
            f"| **{r['id']}** {r['name']} | {r['short']} | {change_text} | "
            f"{r['added_glass_m2']:.2f} | {r['qualifying_count']} "
            f"({', '.join(r['qualifying_windows'])}) |")
    lines += [
        "",
        "Reading by reading:",
        "",
    ]
    for r in result["readings"]:
        lines.append(f"### {r['id']} — {r['name']}")
        lines.append("")
        lines.append(r["basis"])
        lines.append("")
        if r["changes"]:
            for c in r["changes"]:
                lines.append(
                    f"- **{c['id']}** ({room_name[c['room']]}): {c['from_mm']} → {c['to_mm']}, "
                    f"+{c['added_glass_m2']:.2f} m² gross, "
                    f"+{c['added_qualifying_m2']:.2f} m² qualifying.")
        else:
            lines.append("- No change to the aperture table.")
        lines.append(f"- Weakness: {r['weakness']}")
        lines.append("")

    lines += [
        "## 5. The set that satisfies all three",
        "",
        "Designing to the strictest reading means the interpretation stops mattering — the "
        "municipality's answer to C-01 cannot then break the design. The union of R-A, R-B "
        "and R-C is:",
        "",
        "| ID | Room | Now | Proposed | Added glass m² |",
        "|---|---|---|---|---:|",
    ]
    for c in recommended["changes"]:
        lines.append(
            f"| {c['id']} | {c['room']} | {c['from_mm']} | **{c['to_mm']}** | "
            f"+{c['added_glass_m2']:.2f} |")
    lines += [
        f"| | | | **Total** | **+{recommended['added_glass_m2']:.2f}** |",
        "",
        f"That yields **{recommended['qualifying_count']} qualifying windows** "
        f"({', '.join(recommended['qualifying_windows'])}) — not three openings on one wall, "
        "which would be a weaker claim: V-01 and V-02 sit on opposite façades, 3000 mm "
        "apart.",
        "",
        "### Why 900 mm and not the literal minimum",
        "",
        "The area of a qualifying aperture has **two equal minima** on the sum-rule line: "
        "600 × 900 and 900 × 600, both **0.54 m²**. Between them it bulges to 0.5625 m² at "
        "the 45° point (750 × 750), so a square window is the *worst* choice in that band. "
        "The absolute minimum is a 500 × 1000 slot at **0.50 m²**.",
        "",
        "So the 500 mm slot saves 0.04 m² of glass and 0.008 of LT, and costs the one thing "
        "that matters here: a 500 mm aperture is a slot to climb through sideways. "
        "**900 × 600 is the widest aperture at the equal-minimum area**, and it is a "
        "standard Norwegian module. Take it.",
        "",
        "### The bathroom window has a placement problem",
        "",
        "V-03 sits on the y=0 wall, and the bathroom's back wall is only **1200 mm** long. "
        "At 900 mm wide the piers are 150 mm each side — too thin for a weathertight corner "
        "return and for the frame fixings.",
        "",
        "The bathroom's **gable wall at x=0 is 3000 mm** and takes a 900 × 600 opening "
        "comfortably. Moving V-03 there costs nothing in daylight — the §13-7 count is "
        "orientation-blind — and it is the difference between a window that satisfies the "
        "letter and one a person can actually leave through.",
        "",
        "## 6. Daylight before and after",
        "",
        "| Set | Qualifying glass m² | Min LT, ff 1.00 | ff 0.90 | ff 0.85 | ff 0.80 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, block in (("Current", cur), ("Literal minimum (500 mm slot)", minimum),
                         ("Recommended (900 mm)", recommended)):
        d = block["daylight"]
        lines.append(
            f"| {label} | {d['qualifying_m2']:.2f} | {d['minimum_lt']['1.00']:.3f} | "
            f"{d['minimum_lt']['0.90']:.3f} | {d['minimum_lt']['0.85']:.3f} | "
            f"{d['minimum_lt']['0.80']:.3f} |")
    lines += [
        "",
        "The two bathroom-window options differ by 0.04 m² of glass, which is 0.008 of LT. "
        "**The wall geometry decides, not the daylight.**",
        "",
        "### Where the two requirements actually converge",
        "",
        "| Frame factor | Min LT now | Min LT after the escape fix | Relief |",
        "|---:|---:|---:|---:|",
    ]
    for ff in FRAME_FACTORS:
        c = result["convergence"][f"{ff:.2f}"]
        lines.append(
            f"| {ff:.2f} | {c['min_lt_before']:.3f} | {c['min_lt_after']:.3f} | "
            f"−{c['relief']:.3f} |")
    lines += [
        "",
        "The escape fix is **also** the daylight fix. At a frame factor of 0.85 the current "
        "table needs a light transmittance of "
        f"**{result['convergence']['0.85']['min_lt_before']:.3f}**; after the fix it needs "
        f"**{result['convergence']['0.85']['min_lt_after']:.3f}**. The same change relieves "
        "the daylight screen by 0.06 of LT at no extra cost, and it is the only lever that "
        "does so without adding a fourth opening.",
        "",
        "Whether either figure is achievable is a **product question** — no glazing is "
        "specified yet — so this screen does not claim the daylight requirement is met. It "
        "claims the requirement is now 0.06 lower than it was.",
        "",
        "## 7. What the fix costs in heat",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Added glass | {loss['added_glass_m2']:.2f} m² |",
        f"| U window − U wall at the §14-3 limits | "
        f"{loss['delta_per_m2_w_per_k']:.2f} W/m²K |",
        f"| Element loss from the added glass | +{loss['delta_glass_w_per_k']:.3f} W/K |",
        f"| Added opening perimeter | +{loss['added_perimeter_m']:.2f} m |",
        f"| Reveal bridges at Ψ {loss['reveal_psi_w_per_mk']:.2f} W/mK (ordinary) | "
        f"+{loss['delta_reveal_w_per_k']:.3f} W/K |",
        f"| **Total marginal heat loss** | **+{loss['delta_w_per_k']:.3f} W/K** |",
        f"| Share of the element loss ({loss['elements_w_per_k']:.1f} W/K) | "
        f"{loss['share_of_elements'] * 100:.1f} % |",
        "",
        "The two effects **add**, they do not cancel: the glass displaces wall, which "
        "saves heat, but it also lengthens the opening perimeter, which costs heat at the "
        "reveal detail. The reveal is about a sixth of the glass figure, and both together "
        "are under two per cent of the envelope.",
        "",
        "That is small enough not to move the R2 choice, and it is the second time the "
        "reveal has appeared as a real cost rather than a rounding term. The first was the "
        "16.3 m reveal inventory in the bridge screen.",
        "",
        "## 8. What this screen does not settle",
        "",
        "1. **Which reading applies.** That is a municipal / fire-engineer determination. "
        "The screen prices the three so the question can be asked with numbers attached.",
        "2. **Whether V-02 may drop its sill to 1000 mm.** It is the kitchen window; a "
        "900 mm worktop plus a splashback normally puts the sill at about 1050 mm. The "
        "100 mm drop is a joinery decision, not a free move.",
        "3. **What sits under the bathroom window.** §11-13 allows a 1.0 m sill «unless "
        "measures ease escape»; a WC or a shower tray under the opening raises the effective "
        "sill. The sanitary layout is not drawn.",
        "4. **The §11-13 Table 1 travel distance for risk class 4**, still absent from the "
        "retrieved table. Moot by geometry at 18 m².",
        "5. **Whether the whole cabin is a rømningsvei** for §11-9 surface classes. That "
        "question is unchanged by this screen and still governs whether reclaimed timber may "
        "stay exposed.",
        "6. **Whether the bathroom door gives 0.86 m free width.** A 1200 mm bathroom with a "
        "900 mm leaf leaves 150 mm each side; not checked here.",
        "",
        "## 9. Source and status",
        "",
        "- TEK17 §11-13 and §11-14: S024. §13-7: S023.",
        "- Plan and aperture geometry: `fase1/geometria-R0.md`, "
        "`fase1/tabla-aberturas.csv` (R0 conceptual).",
        "- Generated by `scripts/ventanas_check.py`; JSON companion: "
        "`knowledge/comparisons/ventanas.json`.",
        "- SCREENING ONLY — no fire strategy, no compliance certificate, no fabrication "
        "release.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    # The absolute minimum qualifying aperture is a 500 x 1000 slot at 0.50 m2.
    assert smallest_qualifying(500, 500, 1500) == (500.0, 1000.0, 1000.0)
    # On the sum-rule line the area has two equal minima, 600 x 900 and 900 x 600,
    # both 0.54 m2, with a bulge to 0.5625 at the 45-degree point between them.
    areas = {w: smallest_qualifying(500, 500, 1500, float(w))[0] *
                 smallest_qualifying(500, 500, 1500, float(w))[1]
             for w in (600, 750, 900)}
    assert abs(areas[600] - areas[900]) < 1e-9, areas
    assert areas[750] > areas[900], areas
    assert abs(areas[900] / 1e6 - 0.54) < 1e-9
    # Beyond 900 the height floor binds and the area grows again.
    assert smallest_qualifying(500, 500, 1500, 1000) == (1000.0, 600.0, 1000.0)
    assert (1000.0 * 600.0) > areas[900]

    # A window that already qualifies is never shrunk.
    assert smallest_qualifying(1200, 1100, 900) == (1200.0, 1100.0, 900.0)
    # A qualifying window with a low sill keeps its sill.
    assert smallest_qualifying(1200, 1100, 300) == (1200.0, 1100.0, 300.0)

    openings = [
        {"id": "V-01", "room": "MAIN", "facade": "y=3000", "x_centre_mm": 2400,
         "width_mm": 1200, "height_mm": 1100, "sill_mm": 900,
         "gross_m2": 1.32, "qualifying_m2": 1.32,
         "escape_qualifies": True, "escape_fails": []},
        {"id": "V-02", "room": "MAIN", "facade": "y=0", "x_centre_mm": 2400,
         "width_mm": 1000, "height_mm": 900, "sill_mm": 1100,
         "gross_m2": 0.90, "qualifying_m2": 0.90,
         "escape_qualifies": False, "escape_fails": ["sill"]},
        {"id": "V-03", "room": "BATH", "facade": "y=0", "x_centre_mm": 600,
         "width_mm": 500, "height_mm": 500, "sill_mm": 1500,
         "gross_m2": 0.25, "qualifying_m2": 0.25,
         "escape_qualifies": False, "escape_fails": ["height", "sum", "sill"]},
    ]
    result = screen(openings)

    # R-A needs nothing, and its set is the current table.
    r_a = next(r for r in result["readings"] if r["id"] == "R-A")
    assert r_a["changes"] == [] and r_a["qualifying_count"] == 1

    # R-B adds V-02 only, and adds no glass: the sill is the only thing wrong with it.
    r_b = next(r for r in result["readings"] if r["id"] == "R-B")
    assert [c["id"] for c in r_b["changes"]] == ["V-02"], r_b["changes"]
    assert r_b["added_glass_m2"] == 0.0
    assert r_b["qualifying_count"] == 2

    # R-C must fix the bathroom, which has no direct exit.
    r_c = next(r for r in result["readings"] if r["id"] == "R-C")
    assert [c["id"] for c in r_c["changes"]] == ["V-03"], r_c["changes"]
    assert abs(r_c["added_glass_m2"] - 0.25) < 1e-9

    # The union of the three readings carries both changes and three qualifying windows.
    assert [c["id"] for c in result["minimum"]["changes"]] == ["V-02", "V-03"]
    assert result["minimum"]["qualifying_count"] == 3
    assert abs(result["minimum"]["added_glass_m2"] - 0.25) < 1e-9
    assert abs(result["minimum"]["daylight"]["qualifying_m2"] - 2.72) < 1e-9

    # The recommended 900 mm option costs 0.04 m2 more and is the wider aperture.
    assert abs(result["recommended"]["added_glass_m2"] - 0.29) < 1e-9
    assert result["recommended"]["added_glass_m2"] > result["minimum"]["added_glass_m2"]
    assert result["recommended"]["qualifying_count"] == 3

    # Daylight: 2.47 -> 2.76 m2 for the recommended set, and the requirement falls.
    assert abs(result["current"]["daylight"]["qualifying_m2"] - 2.47) < 1e-9
    assert abs(result["recommended"]["daylight"]["qualifying_m2"] - 2.76) < 1e-9
    for ff in FRAME_FACTORS:
        c = result["convergence"][f"{ff:.2f}"]
        assert c["relief"] > 0, c
        assert c["min_lt_after"] < c["min_lt_before"]

    # A reading that needs nothing must never report a change.
    assert solve({"id": "X", "needs": ()}, openings)[1] == []

    # Room assignment is a partition, not a guess: x=1200 belongs to MAIN.
    assert room_of(1199.0) == "BATH"
    assert room_of(1200.0) == "MAIN"
    assert room_of(600.0) == "BATH"

    # Heat loss is positive and small.
    assert result["heat_loss"]["delta_w_per_k"] > 0
    assert result["heat_loss"]["share_of_elements"] < 0.05

    print("Window self-test OK: smallest qualifying aperture, the equal-minimum "
          "600/900 band, three readings priced, union set, daylight relief and heat "
          "cost all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aperturas", nargs="?")
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return
    if not args.aperturas:
        ap.error("falta el CSV de aberturas (o use --selftest)")

    openings = read_openings(args.aperturas)
    result = screen(openings)
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(result, args.aperturas), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(markdown(result, args.aperturas))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
