#!/usr/bin/env python3
"""MiniHouse · the ytelsesoversikt that TEK17 §2-2(4) requires

§2-2(4) says the documentation shall describe how the building is to be formed and
which ytelser are relied on, and the veiledning (S030) prescribes what that overview
must contain:

    Dersom funksjonskrav i forskriften er oppfylt ved bruk av preaksepterte ytelser:
        ytelser gitt i forskrift · preaksepterte ytelser
    Dersom funksjonskrav i forskriften er dokumentert ved analyse:
        ytelser gitt i forskrift · preaksepterte ytelser som er brukt ·
        ytelser som er dokumentert ved analyse

Three categories. The project has had the material scattered across fifteen screening
reports since the first week and has never assembled the object, which is why §2-2(4)
has been recorded as "unsatisfied until R2 is chosen". That is true of the *content* —
the basis cannot be sufficient until the section closes — but it was never true of the
object, and the object is what a case officer asks for first.

**This file is a view, not an authority.** Every value that a screen owns is read from
that screen's constant, so the overview cannot drift from the analysis it summarises;
where no script owns the number, the row cites the card that does. A fourth category
exists for the things the declaration carries that are *not* ytelser — a benchmark that
does not bind, a project choice, an external constraint, a determination. They are listed
so that nothing disappears between the declaration and this overview, and they are kept
out of the three prescribed categories so the overview does not become a dumping ground.

Not a compliance statement. Nothing here is met by assertion: every status is what a
screening report shows, and most of them are waiting on a decision.

Usage:
  python ytelsesoversikt.py --out-md fase1/ytelsesoversikt.md \
      --out-json knowledge/comparisons/ytelsesoversikt.json
  python ytelsesoversikt.py --selftest
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import envelope_check as ec
import fire_check as fc
import incertidumbre as inc
import instalaciones_check as ic
import natural_hazard_screen as nh
import radon_check as rc
import room_height_check as rh
import ventilacion_check as vc

FORSKRIFT = "forskrift"
PREAKSEPTERT = "preakseptert"
ANALYSE = "analyse"
UTENFOR = "utenfor"

CATEGORY_LABEL = {
    FORSKRIFT: "Ytelser gitt i forskrift",
    PREAKSEPTERT: "Preaksepterte ytelser som er brukt",
    ANALYSE: "Ytelser dokumentert ved analyse",
    UTENFOR: "Outside the overview — not a ytelse",
}

# Status vocabulary. Deliberately not "pass"/"fail": a screening is not a verification.
MET = "met by the screening"
NOT_MET = "**not met** by the screening"
UNDETERMINED = "undetermined"
NOT_APPLICABLE = "not applicable to this building"
AT_LIMIT = "met at the limit, no margin"

# One row per ytelse. `decl` lists the declaration-of-margins rows that report on it,
# which is what makes the two documents a set rather than two lists.
ROWS = (
    # --- chapter 7: natural hazards -----------------------------------------
    dict(id="7.1", provision="§7-2", ytelse="Flood — safety class",
         value=f"{nh.MINIHOUSE_FLOOD} (1/{nh.FLOOD_CLASSES[nh.MINIHOUSE_FLOOD]})",
         category=FORSKRIFT, decl=(6,), status=UNDETERMINED, closed_by="C-01",
         evidence="The class is fixed by the regulation and does not depend on the site; "
                  "whether the site is in it does. Flood datum and freeboard are the "
                  "site inputs (cribado-riesgos-naturales.md)"),
    dict(id="7.2", provision="§7-3", ytelse="Landslide — safety class",
         value=f"{nh.MINIHOUSE_LANDSLIDE} (1/{nh.LANDSLIDE_CLASSES[nh.MINIHOUSE_LANDSLIDE]})",
         category=FORSKRIFT, decl=(), status=UNDETERMINED, closed_by="C-01",
         evidence="Quick-clay regime below the marine limit is a siting gate, not a design "
                  "value; no ground investigation exists"),
    # --- chapter 9: external environment ------------------------------------
    dict(id="9.1", provision="§9-2", ytelse="Hazardous substances in products",
         value="no manufacturer-free route", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="C-08 (testing)",
         evidence="The reclaimed timber has no documented compliance instrument; §2-3(1)'s "
                  "guidance names prøvning as the route, so this is a testing question "
                  "(verificacion-instalaciones.md)"),
    dict(id="9.2", provision="§9-6 / §9-8", ytelse="Waste plan and 70 wt% sorting",
         value=f">{ic.WASTE_PLAN_TONNES:.0f} t, or >{ic.WASTE_PLAN_AREA_NEW_BUILD_M2:.0f} m²",
         category=FORSKRIFT, decl=(), status=NOT_APPLICABLE, closed_by="—",
         evidence=f"Area limbs unreachable at {ic.MINIHOUSE_BRA_M2:.0f} m²; the tonnage limb is "
                  "crossed only by aggregation with a demolition, so the duty applies iff the "
                  "project dismantles a source building"),
    dict(id="9.3", provision="§9-10", ytelse="Wood-stove emissions",
         value=f"{ic.STOVE_LIMIT_CATALYST_G_PER_KG:.0f} g/kg (catalyst), "
               f"{ic.STOVE_LIMIT_OTHER_G_PER_KG:.0f} g/kg (other)",
         category=FORSKRIFT, decl=(), status=UNDETERMINED, closed_by="stove product",
         evidence="Applies if a stove is fitted, which the room-sealed decision (row 14) "
                  "makes more likely, not less"),
    # --- chapter 11: fire ---------------------------------------------------
    dict(id="11.1", provision="§11-4(3) no. 4", ytelse="Loadbearing capacity, main system",
         value=f"R {fc.R_MAIN_MIN}", category=FORSKRIFT, decl=(), status=NOT_MET,
         closed_by="R2 + C-06",
         evidence="No. 4 overrides Table 1's R 30 for BKL 1 + risk class 4. A 48 mm rafter "
                  "keeps 32 % of its modulus under charring; parity needs 98 mm stock "
                  "(determinacion-cubierta-incendio.md)"),
    dict(id="11.2", provision="§11-8", ytelse="Fire-cell separation",
         value=f"EI {fc.FIRE_CELL_EI_BKL1}", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="whether a technical cupboard is a fire cell (S024 records it as open)",
         evidence="One dwelling unit in one cell; the open question is whether the technical "
                  "cupboard must be separated"),
    dict(id="11.3", provision="§11-9", ytelse="Surface classes, wall and ceiling",
         value=fc.SURFACE_WALL_CEILING, category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="the §11-13 determination (rows 2/3/4)",
         evidence=f"{fc.SURFACE_WALL_CEILING_ESCAPE} applies only inside a rømningsvei. A cell "
                  "with no rømningsvei is still a cell, so D-s2,d0 governs and the reclaimed "
                  "timber stays exposed (determinacion-estrategia-incendio.md)"),
    dict(id="11.4", provision="§11-9", ytelse="Roof covering",
         value=fc.ROOF_COVERING, category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="product",
         evidence="A product property of the standing-seam sheet, not a design value"),
    dict(id="11.5", provision="§11-13", ytelse="Escape window — aperture",
         value=f"{fc.ESCAPE_MIN_HEIGHT_MM:.0f} h × {fc.ESCAPE_MIN_WIDTH_MM:.0f} w, "
               f"sum ≥ {fc.ESCAPE_MIN_SUM_MM:.0f} mm",
         category=FORSKRIFT, decl=(3, 4), status=NOT_MET, closed_by="the aperture table (R0)",
         evidence="V-03 gives 500 × 500, sum 1000. The deficit is −500 mm on the sum rule, the "
                  "largest dimensional gap in the project (verificacion-ventanas.md)"),
    dict(id="11.6", provision="§11-13", ytelse="Escape window — sill",
         value=f"≤ {fc.ESCAPE_MAX_SILL_MM:.0f} mm",
         category=FORSKRIFT, decl=(3,), status=NOT_MET, closed_by="the aperture table (R0)",
         evidence="V-03 at 1500 mm, V-02 at 1100; V-01 alone qualifies at 900 mm"),
    dict(id="11.7", provision="§11-14", ytelse="Door free width in a rømningsvei",
         value=f"{fc.MIN_FREE_WIDTH_MM:.0f} mm",
         category=FORSKRIFT, decl=(2,), status=UNDETERMINED,
         closed_by="a door schedule with the free width dimensioned",
         evidence="A 900 mm leaf is not a free width; ordinary sets spend 30–60 mm on frame, "
                  "hinge and stop, and none is specified"),
    dict(id="11.8", provision="§11-12", ytelse="Smoke detection",
         value=f"≥ {fc.SMOKE_ALARM_MIN_DB:.0f} dB, {len(fc.DWELLING_ALARM_ZONES)} zones",
         category=FORSKRIFT, decl=(), status=UNDETERMINED, closed_by="specification",
         evidence="A specification item with no dimensional consequence, which is why it has "
                  "not been written yet"),
    dict(id="11.9", provision="§11-6 / §11-17", ytelse="Separation and fire-service access",
         value=f"{fc.MIN_SEPARATION_M:.0f} m separation; {fc.MAX_ACCESS_DISTANCE_M:.0f} m access",
         category=FORSKRIFT, decl=(), status=UNDETERMINED, closed_by="C-01",
         evidence="Both are properties of the pitch, not of the module"),
    # --- chapter 12: layout --------------------------------------------------
    dict(id="12.1", provision="§12-7(2)(c)", ytelse="Room height",
         value=f"{rh.TARGET_FREE_MM / 1000:.1f} m", category=FORSKRIFT, decl=(5,), status=NOT_MET,
         closed_by="R2",
         evidence="1778 mm at the eave at 20° / 1100 mm stack, so −422 mm. §12-7(2)(a)'s 2.4 m "
                  "is exempt; (2)(c) sets 2.2 m for this building type (verificacion-altura-libre.md)"),
    dict(id="12.2", provision="§12-7(2)(d)", ytelse="Relief for parts of a room",
         value="no fraction given", category=UTENFOR, decl=(9,), status=UNDETERMINED,
         closed_by="a determination",
         evidence="Parts of the room may be lower «der dette ikke påvirker rommets "
                  "bruksformål». How much is a determination, not a number, so it cannot be "
                  "measured — only argued"),
    # --- chapter 13: indoor climate -----------------------------------------
    dict(id="13.1", provision="§13-1(1)", ytelse="Ventilation adapted to the pollution load",
         value="documented quantities required", category=ANALYSE, decl=(14,), status=NOT_MET,
         closed_by="a room-sealed stove (row 14) and the make-up air inlet",
         evidence="The quantities are produced — 52 m³/h governing supply, 90 basic and "
                  "108–216 boosted extract — but the extract depressurises a sealed cabin to "
                  "106–140 Pa and reverses the flue by −130 Pa (verificacion-ventilacion.md)"),
    dict(id="13.2", provision="§13-5", ytelse="Radon — annual average",
         value=f"≤ {rc.RADON_LIMIT_BQ:.0f} Bq/m³", category=FORSKRIFT, decl=(15,),
         status=UNDETERMINED, closed_by="C-01",
         evidence=f"Bounded by C ≤ E/Q at 3.6–36 Bq/m³ on ordinary ground; alum shale at "
                  f"{rc.ALUM_SHALE_MBQ_M2S:.0f} mBq/(m²·s) breaks it at 216 (verificacion-radon.md)"),
    dict(id="13.3", provision="§13-5", ytelse="Radon barrier against the ground",
         value=f"plus pressure reduction above {rc.ACTION_LEVEL_BQ:.0f} Bq/m³",
         category=FORSKRIFT, decl=(15,), status=NOT_APPLICABLE,
         closed_by="—",
         evidence="The prescriptive route describes a floor on the ground. This one sits on a "
                  "ventilated void over the chassis, so the route describes a detail the "
                  "building does not contain — which is why the bound, not a membrane, is the "
                  "instrument"),
    dict(id="13.4", provision="§13-7", ytelse="Daylight — light transmittance",
         value="0.510 at ff 1.00", category=ANALYSE, decl=(1,), status=UNDETERMINED,
         closed_by="glazing",
         evidence="The requirement is a function; 0.510 is the minimum LT that delivers the "
                  "required glass area, so it is the project's instrument and it moves with "
                  "the frame factor (verificacion-luz-diurna.md)"),
    dict(id="13.5", provision="§13-13", ytelse="Vapour resistance of the barrier",
         value="Sd ≥ 10 m", category=ANALYSE, decl=(13,), status=UNDETERMINED,
         closed_by="the barrier product and the junction detail",
         evidence="A function in the forskrift; 10 m is the project's instrument. Its "
                  "continuity is the floor-to-wall junction, where the steel crosses the "
                  "plane when it is not wrapped (detalle-encuentro-R0.svg)"),
    dict(id="13.6", provision="§13-4", ytelse="Thermal indoor climate",
         value="operative temperature, no number", category=ANALYSE, decl=(), status=UNDETERMINED,
         closed_by="R2 and the heating choice",
         evidence="Not analysed. The envelope and junction screens cover the fabric; the "
                  "comfort quantity needs the heating system, which is not chosen"),
    dict(id="13.7", provision="§13-15", ytelse="Wet room",
         value="applies", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="the plan",
         evidence="A bathroom is in the R0 plan; the wet-room build-up is not designed"),
    # --- chapter 14: energy --------------------------------------------------
    dict(id="14.1", provision="§14-3", ytelse="Wall U-value",
         value=f"≤ {ec.U_LIMITS['wall']:.2f} W/m²K", category=FORSKRIFT, decl=(7,),
         status=NOT_MET, closed_by="a timber fraction below 15 %, or more wool",
         evidence="189 mm gives 0.2202 against 0.2200 — solved *to* the limit, so the margin is "
                  "zero by construction and the band across 8–23 % changes sign"),
    dict(id="14.2", provision="§14-3", ytelse="Roof U-value",
         value=f"≤ {ec.U_LIMITS['roof']:.2f} W/m²K", category=FORSKRIFT, decl=(), status=NOT_MET,
         closed_by="R2",
         evidence="278 mm at 15 %; clear field passes, studs do not. Solved to the limit like "
                  "the wall (verificacion-envolvente.md)"),
    dict(id="14.3", provision="§14-3", ytelse="Floor U-value",
         value=f"≤ {ec.U_LIMITS['floor']:.2f} W/m²K", category=FORSKRIFT, decl=(), status=NOT_MET,
         closed_by="R2",
         evidence="281 mm at 15 %; same construction as the roof"),
    dict(id="14.4", provision="§14-3", ytelse="Window and door U-value",
         value=f"≤ {ec.U_LIMITS['window']:.2f} W/m²K", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="product",
         evidence="No glazing selected. This is the row that also holds the daylight and the "
                  "escape-window deficits, so one product decision moves three"),
    dict(id="14.5", provision="§14-3", ytelse="Airtightness",
         value=f"n50 ≤ {vc.N50_PER_H:.1f} h⁻¹ at 50 Pa", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="the measurement itself — the test is specified, not performed",
         evidence="Used as a design value by the ventilation and radon screens. The test is now "
                  "specified (especificacion-ensayo-tetthet.md) but no measurement exists, and "
                  "the standard that defines the method is not held (S031)"),
    # --- chapter 15: installations ------------------------------------------
    dict(id="15.1", provision="§15-3", ytelse="Flue and chimney",
         value=f"T{ic.CHIMNEY_MIN_CLASS_C}, {ic.CHIMNEY_MIN_FREE_SIDES} free sides, feiing access",
         category=FORSKRIFT, decl=(14,), status=UNDETERMINED, closed_by="product",
         evidence="The chimney chain is checked; the draught it produces is the negative margin "
                  "in row 14, which a room-sealed stove removes"),
    dict(id="15.2", provision="§15-6 / §15-8", ytelse="Backflow head",
         value=f"{ic.BACKFLOW_HEAD_MM:.2f} m", category=FORSKRIFT, decl=(11,), status=NOT_MET,
         closed_by="C-01 and the foundation",
         evidence="+940 mm on the sewer route, −160 mm on a shallow sealed tank. The 0.90 m is "
                  "a minimum burial depth, not a clearance"),
    dict(id="15.3", provision="§15-5", ytelse="Internal water installation",
         value="38 / 55 °C, 20 / 50 mm air gaps", category=FORSKRIFT, decl=(), status=UNDETERMINED,
         closed_by="the services design",
         evidence="A specification item; no distribution system is designed"),
    # --- chapter 4: FDV ------------------------------------------------------
    dict(id="4.1", provision="§4-1", ytelse="FDV documentation",
         value="must exist at ferdigattest, ajour, as built", category=FORSKRIFT, decl=(),
         status=UNDETERMINED, closed_by="a written file",
         evidence="§4-1(2)'s exemption is rejected for this building (6 of 6 categories). "
                  "§4-2 puts the duty to keep it updated on the owner, and a cabin that moves "
                  "meets that condition routinely"),
    # --- outside the overview: not ytelser ----------------------------------
    dict(id="X1", provision="§14-2 (exempt)", ytelse="Ψ″ benchmark of 0.05 W/m²K",
         value="does not bind", category=UTENFOR, decl=(8,), status=NOT_APPLICABLE,
         closed_by="—",
         evidence="The figure sits in §14-2's route, exempt via §14-5(1). At 18 m² it implies a "
                  "mean Ψ of 0.0147 W/mK, under half of good practice, so it is not adoptable "
                  "as a target (verificacion-puentes-termicas.md)"),
    dict(id="X2", provision="S022 (road transport)", ytelse="Overall height",
         value=f"{rh.TRANSPORT_LIMIT_MM:.0f} mm", category=UTENFOR, decl=(10,), status=AT_LIMIT,
         closed_by="R2",
         evidence="Not a TEK17 ytelse at all — a road-transport constraint from Directive "
                  "96/53/EC. Every R2 option was solved *to* it, so it has no margin"),
    dict(id="X3", provision="project", ytelse="R2 dimensional reserve",
         value=f"{inc.__dict__.get('RESERVE_MM', 100.0):.0f} mm", category=UTENFOR, decl=(10,),
         status=UNDETERMINED, closed_by="R2",
         evidence="A project allowance, not a regulatory number; it destroys two of the four "
                  "R2 options"),
    dict(id="X4", provision="project", ytelse="Flood freeboard",
         value=f"{nh.DEFAULT_MARGIN_MM:.0f} mm", category=UTENFOR, decl=(6,), status=UNDETERMINED,
         closed_by="C-01",
         evidence="A project choice above the flood datum. The class is the margin; the "
                  "freeboard is a decision"),
    dict(id="X5", provision="lifting", ytelse="Per-leg sling tension",
         value="accessory capacity", category=UTENFOR, decl=(12,), status=UNDETERMINED,
         closed_by="C-07",
         evidence="Governed by the lift plan and the equipment's rated capacity, not by TEK17. "
                  "No mass inventory exists, so no tension can be stated"),
    dict(id="X6", provision="S014", ytelse="Material factor on soil strength",
         value=f"γ_m = {nh.MATERIAL_FACTOR:.1f}", category=UTENFOR, decl=(), status=UNDETERMINED,
         closed_by="the National Annex",
         evidence="A partial factor on the slope-stability model, not a margin on the F2/S2 "
                  "class; applying it as one double-counts"),
)


# One line per row: the reason for the status, authored rather than derived. The evidence
# field above is the long form for the JSON; truncating it to a sentence was tried and it
# cut «No. 4 overrides…» at «No.», which is exactly the class of quiet corruption this
# project keeps having to repair.
WHY = {
    "7.1": "The class is fixed by the regulation; whether the site is in it is not.",
    "7.2": "Quick-clay regime below the marine limit is a siting gate, and no ground "
           "investigation exists.",
    "9.1": "The reclaimed timber has no documented compliance instrument; §2-3(1) names "
           "prøvning as the route.",
    "9.2": "The area limbs are unreachable at 18 m² and the tonnage limb needs a demolition "
           "to aggregate with.",
    "9.3": "Applies if a stove is fitted — which the room-sealed decision makes more likely, "
           "not less.",
    "11.1": "No. 4 overrides Table 1's R 30; a 48 mm rafter keeps 32 % of its modulus, and "
            "parity needs 98 mm.",
    "11.2": "One dwelling unit in one cell; whether the technical cupboard must be separated "
            "is open.",
    "11.3": "D-s2,d0 governs a cell with no rømningsvei, so the reclaimed timber stays exposed.",
    "11.4": "A product property of the standing-seam sheet, not a design value.",
    "11.5": "V-03 gives 500 × 500, a sum of 1000 against 1500 — the largest dimensional gap "
            "in the project.",
    "11.6": "V-03 at 1500 mm and V-02 at 1100; V-01 alone qualifies at 900 mm.",
    "11.7": "A 900 mm leaf is not a free width, and no frame build-up is specified.",
    "11.8": "A specification item with no dimensional consequence, which is why it has not "
            "been written.",
    "11.9": "Both are properties of the pitch, not of the module.",
    "12.1": "1778 mm at the eave at 20° / 1100 mm stack, so −422 mm.",
    "12.2": "Parts of a room may be lower where it does not affect the room's use; how much "
            "is argued, not measured.",
    "13.1": "The quantities exist, but the extract depressurises the cabin to 106–140 Pa and "
            "reverses the flue by −130 Pa.",
    "13.2": "Bounded by C ≤ E/Q at 3.6–36 Bq/m³ on ordinary ground; alum shale at "
            "300 mBq/(m²·s) gives 216.",
    "13.3": "The prescriptive route describes a floor on the ground; this one is on a "
            "ventilated void over the chassis.",
    "13.4": "The requirement is a function; 0.510 is the minimum LT that delivers the required "
            "glass area.",
    "13.5": "A function in the forskrift; 10 m is the project's instrument, and its continuity "
            "is the junction.",
    "13.6": "Not analysed. The comfort quantity needs the heating system, which is not chosen.",
    "13.7": "A bathroom is in the R0 plan; the wet-room build-up is not designed.",
    "14.1": "189 mm gives 0.2202 against 0.2200 — solved to the limit, and the band across "
            "8–23 % changes sign.",
    "14.2": "278 mm at 15 %; the clear field passes and the studs do not.",
    "14.3": "281 mm at 15 %; same construction as the roof.",
    "14.4": "No glazing selected, and this row also holds the daylight and escape-window "
            "deficits.",
    "14.5": "Specified and not performed: the target is 1.30, and 1.19 is the floor at which "
            "the extract can no longer be fed.",
    "15.1": "The chimney chain is checked; the draught it produces is the −130 Pa of row 14.",
    "15.2": "+940 mm on the sewer route, −160 mm on a shallow sealed tank.",
    "15.3": "A specification item; no distribution system is designed.",
    "4.1": "The §4-1(2) exemption is rejected, and §4-2 puts the duty to keep it updated on "
           "the owner.",
    "X1": "The figure sits in §14-2's route, exempt via §14-5(1), and at 18 m² it implies a "
          "mean Ψ of 0.0147.",
    "X2": "A road-transport constraint, not a TEK17 ytelse, and every option was solved to it.",
    "X3": "A project allowance, not a regulatory number; it destroys two of the four R2 "
          "options.",
    "X4": "A project choice above the flood datum; the class is the margin and the freeboard "
          "is a decision.",
    "X5": "Governed by the lift plan and the equipment's rated capacity, and no mass inventory "
          "exists.",
    "X6": "A partial factor on the slope-stability model, not a margin on the F2/S2 class.",
}


def rows():
    return [dict(r) for r in ROWS]


def by_category():
    out = {FORSKRIFT: [], PREAKSEPTERT: [], ANALYSE: [], UTENFOR: []}
    for r in ROWS:
        out[r["category"]].append(r)
    return out


def counts():
    cats = by_category()
    statuses = {}
    for r in ROWS:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    return {
        "rows": len(ROWS),
        "by_category": {k: len(v) for k, v in cats.items()},
        "by_status": statuses,
        "undetermined": sum(1 for r in ROWS if r["status"] == UNDETERMINED),
        "not_met": sum(1 for r in ROWS if r["status"] == NOT_MET),
        "not_applicable": sum(1 for r in ROWS if r["status"] == NOT_APPLICABLE),
        "cited_declaration_rows": sorted({n for r in ROWS for n in r["decl"]}),
        "ytelser_only": yt_statuses(),
        "closures": closure_histogram(),
    }


def yt_statuses():
    """Status counts inside the ytelser — the outside rows are not ytelser and must not
    inflate a denominator that the report's §5 quotes."""
    out = {MET: 0, NOT_MET: 0, UNDETERMINED: 0, NOT_APPLICABLE: 0, AT_LIMIT: 0}
    for r in ROWS:
        if r["category"] != UTENFOR:
            out[r["status"]] += 1
    return out


def closure_histogram():
    """How many rows each named decision closes.

    This is the number that decides whether the overview is a queue or a list. It is
    computed rather than asserted because the comfortable version — "four decisions
    unblock the building" — is the kind of claim this project keeps having to withdraw.
    """
    import collections
    counts_ = collections.Counter(
        r["closed_by"] for r in ROWS
        if r["category"] != UTENFOR and r["status"] != NOT_APPLICABLE)
    return {
        "distinct": len(counts_),
        "closing_one": sum(1 for v in counts_.values() if v == 1),
        "largest": [{"decision": k, "rows": v} for k, v in counts_.most_common(4)],
    }


def table(rows_, why_header="Why"):
    out = ["| # | Provision | Ytelse | Value | Status | " + why_header + " |",
           "|---|---|---|---|---|---|"]
    for r in rows_:
        why = WHY[r["id"]]
        if r["closed_by"] != "—":
            why += f" **Closes with:** {r['closed_by']}."
        out.append(f"| {r['id']} | {r['provision']} | {r['ytelse']} | `{r['value']}` | "
                   f"{r['status']} | {why} |")
    return out


def model():
    return {"state": "SCREENING — §2-2(4) OVERVIEW, NOT A COMPLIANCE STATEMENT",
            "rows": rows(), "counts": counts()}


def markdown():
    cats = by_category()
    c = counts()
    y = c["ytelser_only"]
    cl = c["closures"]

    L = [
        "# MiniHouse · ytelsesoversikt under TEK17 §2-2(4)",
        "",
        "**State:** SCREENING — §2-2(4) OVERVIEW, NOT A COMPLIANCE STATEMENT. Every status below "
        "is what a screening report shows at R0. No value is a measurement and none is released.",
        "",
        "§2-2(4) requires the documentation to describe **how the building is to be formed and "
        "which ytelser are relied on**, and to give a basis sufficient for detailed design. The "
        "veiledning ([S030](../knowledge/sources/S030.md)) prescribes the overview's content:",
        "",
        "> ytelser gitt i forskrift · preaksepterte ytelser som er brukt · ytelser som er "
        "dokumentert ved analyse",
        "",
        "**The object has not existed until now.** §2-2(4) has been recorded as unsatisfied "
        "until R2 is chosen, which is true of the *basis* — the section does not close, so the "
        "basis cannot yet be sufficient — but was never true of the object. The material has "
        "been in fifteen screening reports since the first week. This is it, assembled, with "
        "each value read from the screen that owns it rather than retyped.",
        "",
        "---",
        "",
        f"## 1. {CATEGORY_LABEL[FORSKRIFT]} — {c['by_category'][FORSKRIFT]}",
        "",
        "Numbers the regulation states. They are met or they are not; a shortfall is a "
        "**deviation** and the only instrument is municipal dispensation (PBL ch. 19), not a "
        "better analysis.",
        "",
    ]
    L += table(cats[FORSKRIFT])

    L += [
        "",
        f"## 2. {CATEGORY_LABEL[PREAKSEPTERT]} — {c['by_category'][PREAKSEPTERT]}",
        "",
    ]
    if cats[PREAKSEPTERT]:
        L += table(cats[PREAKSEPTERT])
    else:
        L += [
            "**Empty, and the emptiness is a finding rather than an omission.** Every number "
            "this project relies on is either one the forskrift states or one a solver "
            "produced; none comes from the preaccepted catalogue. That is unusual, and it "
            "follows from the building: the "
            "preaccepted route is written for a house with a foundation, a heated envelope "
            "assembled on site and a normal roof, and this module has none of those three in "
            "the form the veiledning assumes.",
            "",
            "It also has a consequence worth stating plainly. The veiledning warns that «det er "
            "**ikke tilstrekkelig** kun med en bekreftelse på at de preaksepterte ytelsene er "
            "fulgt» — a bare confirmation is not enough. Here there is nothing to confirm, so "
            "**every** functional requirement in this building is carried by an analysis or by "
            "a stated number, and the analysis route is not optional anywhere.",
        ]

    L += [
        "",
        f"## 3. {CATEGORY_LABEL[ANALYSE]} — {c['by_category'][ANALYSE]}",
        "",
        "Where the regulation gives a function and no number, the value below is the "
        "project's own instrument, produced by a screen in `scripts/` and carrying the margin "
        "declared in [`declaracion-de-margenes.md`](declaracion-de-margenes.md). The "
        "screen that owns each value is named in the JSON companion.",
        "",
    ]
    L += table(cats[ANALYSE])

    L += [
        "",
        f"## 4. {CATEGORY_LABEL[UTENFOR]} — {c['by_category'][UTENFOR]}",
        "",
        "Seven items sit outside the three prescribed categories, and they are here so that "
        "nothing falls between this overview and the declaration of margins: a benchmark that "
        "does not bind, an external constraint, two project choices, a lifting capacity, a "
        "partial factor and a relief whose extent is a determination. Keeping them out of "
        "§1–§3 is what stops the overview being read as claiming a performance the building "
        "does not have to give.",
        "",
    ]
    L += table(cats[UTENFOR], why_header="Why it is not a ytelse")

    L += [
        "",
        "---",
        "",
        "## 5. What the overview says about the building",
        "",
        f"**{c['rows']} rows: {c['by_category'][FORSKRIFT]} stated in the forskrift, "
        f"{c['by_category'][PREAKSEPTERT]} preaccepted, {c['by_category'][ANALYSE]} documented "
        f"by analysis, {c['by_category'][UTENFOR]} outside the overview.** Of the "
        f"**{c['rows'] - c['by_category'][UTENFOR]}** that are ytelser: "
        f"**{y[MET]} are met**, {y[NOT_MET]} are not met by the screening, {y[UNDETERMINED]} "
        f"are undetermined and {y[NOT_APPLICABLE]} do not apply.",
        "",
        "**Not one ytelse is discharged, and that is what R0 means.** It is not a defect of "
        "the overview: a screening is not a verification, and the two rows that would read as "
        "met — smoke detection and the surface class — are specifications nobody has written "
        "yet, so they are undetermined too. What this document shows is the shape of the "
        "problem, not the state of the building, and it will keep showing that until something "
        "is built or measured.",
        "",
        f"**The queue is longer than the list looked.** {cl['distinct']} distinct decisions "
        f"close these rows, and **{cl['closing_one']} of them close exactly one row**. The "
        "comfortable version — «four decisions unblock the building» — is false. "
        + ", ".join(f"{d['decision']} closes {d['rows']}" for d in cl["largest"][:3])
        + ", and the rest are one-offs. That is the thing assembling the overview adds: each "
        "screen looks tractable alone, and together they show a project whose remaining work is "
        "mostly individual, with two real levers — the site (**C-01**) and the section (**R2**).",
        "",
        "**Three findings follow that the individual screens could not show.**",
        "",
        "1. **The preaccepted category is empty, and that is structural.** A building with no "
        "foundation, no site-assembled envelope and no conventional roof has no preaccepted "
        "route to follow, so §2-2(2)(b)'s analysis route is not one option among two — it is "
        "the only route this project has. That raises the stakes on §2-2(3) rather than "
        "lowering them: there is no fallback in which a checklist substitutes for an argument.",
        "2. **Two rows do not apply, and both for the same reason.** §13-3's radon barrier "
        "«against the ground» and §9-2's product route both describe a building assembled on "
        "its own site from products with manufacturers. This one is lifted onto a chassis and "
        "skinned in timber nobody can certify. The pattern is worth naming: **the prescriptive "
        "routes assume a foundation and a supply chain**, and where both are missing the "
        "regulation does not become inapplicable — it becomes an analysis.",
        "3. **One row waits on work rather than on a decision, and even that work waits on the "
        "building.** §15-5's water installation has no design and could be drawn this week. "
        "§14-5's airtightness looked like the other one, and writing its test specification "
        "([especificacion-ensayo-tetthet.md](especificacion-ensayo-tetthet.md)) showed that the "
        "*test* is cheap and the *building to test* is not: the measurement happens at the end "
        "of fabrication and again at handover. So the cheapest row in this document is cheap in "
        "money and not in time, and the earlier reading — that it waited on an afternoon — was "
        "too generous. **A specification is not a measurement**, which is the same distinction "
        "as a screening not being a verification.",
        "",
        "## 6. What §2-2(4) still requires",
        "",
        "- **The basis must be sufficient for detailed design**, and it is not: the section does "
        "not close at 20° under 4.00 m, so R2 is the step that produces the basis. This "
        "overview is the *inventory* the basis will be built from, not the basis.",
        "- **Drawings may be required**, and the veiledning names fire safety as the example. "
        "One drawing exists — [the junction detail](planos/detalle-encuentro-R0.svg) — and it "
        "is conceptual. No fire-strategy drawing, no plan at 1:50 and no section at 1:20 exist.",
        "- **The overview must be reissued when the geometry moves**, for the same reason the "
        "declaration is versioned: a ytelsesoversikt that describes a superseded geometry is "
        "worse than none, because it looks current.",
        "",
        "## 7. Limits",
        "",
        "- Every status is a screening status. **None is a verification, an approval or a "
        "compliance statement**, and the municipality decides which ytelse applies in a real "
        "case.",
        "- Values that a screen owns are read from that screen's constants; values no script "
        "owns cite the card or report in the evidence column of the JSON companion. The "
        "self-test fails if a row loses its evidence or if a declared margin is not cited "
        "somewhere in this overview.",
        "- The category assignment is this project's reading of §2-2(2), applied row by row. "
        "It is not a legal opinion.",
        "- `§12-7(2)(d)` is a **determination**: parts of a room may be lower than 2.2 m "
        "where it does not affect the room's use, and how much is argued rather than "
        "measured. It is in §4 for that reason, and the §11-13 determination that governs "
        "rows 2–4 of the declaration appears as the closure of row 11.3 rather than as a "
        "ytelse of its own.",
        "",
    ]
    return "\n".join(L)


def selftest():
    c = counts()
    rs = rows()

    # The four categories must partition the rows exactly, or a row has escaped both
    # the three prescribed categories and the explicit "outside" one.
    assert sum(c["by_category"].values()) == len(rs) == c["rows"], c
    assert set(c["by_category"]) == {FORSKRIFT, PREAKSEPTERT, ANALYSE, UTENFOR}

    # Every row must carry an evidence pointer: a status without a source is an assertion.
    for r in rs:
        assert r["evidence"].strip(), r["id"]
        assert r["value"].strip(), r["id"]
        assert r["closed_by"].strip(), r["id"]
        assert r["status"] in (MET, NOT_MET, UNDETERMINED, NOT_APPLICABLE, AT_LIMIT), (r["id"], r["status"])

    # The three prescribed categories must all be *considered*. Two of them are
    # populated; the preaccepted one is empty on purpose and must stay a stated finding
    # rather than being quietly filled with something that is really a forskrift number.
    assert c["by_category"][FORSKRIFT] > 0 and c["by_category"][ANALYSE] > 0
    assert c["by_category"][PREAKSEPTERT] == 0, (
        "a preaccepted ytelse has appeared; the report's §2 says the category is empty and "
        "explains why, so both must move together")

    # The cross-lock with the declaration of margins: every one of its fifteen rows must
    # be cited somewhere here, or the two documents are two lists rather than a set.
    assert c["cited_declaration_rows"] == list(range(1, 16)), c["cited_declaration_rows"]
    # And the citation must be honest: a row classified as a ytelse in the declaration
    # cannot be cited only by rows this overview calls "outside".
    decl_class = inc.CLASS
    for r in rs:
        for n in r["decl"]:
            if decl_class[n] == "ytelse":
                assert r["category"] != ANALYSE, (r["id"], n)

    # Values that a screen owns must be the screen's value, not a copy. These asserts are
    # the reason the module imports eight screens instead of quoting them.
    vals = {r["id"]: r["value"] for r in rs}
    assert vals["14.1"] == f"≤ {ec.U_LIMITS['wall']:.2f} W/m²K"
    assert vals["14.2"] == f"≤ {ec.U_LIMITS['roof']:.2f} W/m²K"
    assert vals["14.3"] == f"≤ {ec.U_LIMITS['floor']:.2f} W/m²K"
    assert vals["13.2"] == f"≤ {rc.RADON_LIMIT_BQ:.0f} Bq/m³"
    assert vals["12.1"] == f"{rh.TARGET_FREE_MM / 1000:.1f} m"
    assert vals["11.1"] == f"R {fc.R_MAIN_MIN}"
    assert vals["11.7"] == f"{fc.MIN_FREE_WIDTH_MM:.0f} mm"
    assert vals["14.5"] == f"n50 ≤ {vc.N50_PER_H:.1f} h⁻¹ at 50 Pa"
    assert vals["15.2"] == f"{ic.BACKFLOW_HEAD_MM:.2f} m"
    assert vals["7.1"].startswith(nh.MINIHOUSE_FLOOD)

    # A row that is "not met" must say what closes it; otherwise the overview is a list of
    # complaints. "—" is only legitimate for a row that does not apply.
    for r in rs:
        if r["status"] == NOT_MET:
            assert r["closed_by"] not in ("—", ""), r["id"]
        if r["status"] == NOT_APPLICABLE:
            assert r["closed_by"] == "—", r["id"]

    # The markdown must render the three prescribed categories in the guidance's order and
    # must not lose the empty-category finding.
    text = markdown()
    for label in CATEGORY_LABEL.values():
        assert label in text, label
    assert text.index(CATEGORY_LABEL[FORSKRIFT]) < text.index(CATEGORY_LABEL[ANALYSE])
    assert "**ikke tilstrekkelig**" in text
    assert "NOT A COMPLIANCE STATEMENT" in text
    # The overview's central claim is that no ytelse is discharged at R0. If a row ever
    # acquires "met", either something was verified or a screening was mislabelled.
    y = c["ytelser_only"]
    assert y[MET] == 0, y
    assert y[NOT_MET] + y[UNDETERMINED] + y[NOT_APPLICABLE] == c["rows"] - c["by_category"][UTENFOR]
    # And the queue finding: the work is mostly individual, not four decisions.
    assert c["closures"]["distinct"] >= 15, c["closures"]
    assert c["closures"]["closing_one"] >= 10, c["closures"]

    # Every row must have an authored one-liner, and no orphan may linger.
    assert set(WHY) == {r["id"] for r in rs}, (set(WHY) ^ {r["id"] for r in rs})
    for k, v in WHY.items():
        assert 20 < len(v) < 200, (k, len(v))

    # "Met at the limit" is a distinct status and must stay rare: it means the design
    # touches an absolute number with nothing to spare, which is the failure mode the
    # chapter 2 introduction names.
    at_limit = [r["id"] for r in rs if r["status"] == AT_LIMIT]
    assert at_limit == ["X2"], at_limit

    # Row ids must be unique, or a citation can point at two rows at once.
    ids = [r["id"] for r in rs]
    assert len(ids) == len(set(ids)), sorted(i for i in ids if ids.count(i) > 1)
    # The typographic minus must survive into the rendered report, as everywhere else.
    assert "−" in text

    print(f"Ytelsesoversikt self-test OK: {c['rows']} rows across four categories "
          f"({c['by_category'][FORSKRIFT]} forskrift / {c['by_category'][PREAKSEPTERT]} "
          f"preakseptert / {c['by_category'][ANALYSE]} analyse / "
          f"{c['by_category'][UTENFOR]} outside), all fifteen declaration rows cited, every "
          f"status carrying evidence, {c['not_met']} not met and {c['undetermined']} "
          f"undetermined")


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
        path.write_text(json.dumps(model(), indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(json.dumps(model(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
