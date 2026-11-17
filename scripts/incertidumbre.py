#!/usr/bin/env python3
"""MiniHouse · are the declared margins adequate? (§2-2(3), fourth demand, second half)

The declaration of margins defines adequacy as **positive and larger than the
uncertainty of the model that produced it**, and then admits that the
uncertainty column is unpopulated. This screen populates it.

It separates four kinds of uncertainty, because they behave differently:

  model          the idealisation's own error — a 1D temperature field, a
                 generic Ψ table, a uniform framing fraction
  input          a parameter nobody has measured — λ, LT, the timber fraction
  interpretation which requirement applies — a determination, not an error
  construction   what the builder will actually achieve — a tolerance

Only the first two can be swept. The third is priced as alternative readings.
The fourth is stated where the repository has a number for it and left
unquantified where it does not.

This is a screening tool. It does not certify any margin as adequate and it is
not a compliance statement.

Usage:
  python incertidumbre.py --out-md fase1/verificacion-incertidumbre.md \
      --out-json knowledge/comparisons/incertidumbre.json
  python incertidumbre.py --selftest
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import envelope_check as ec
from envelope_check import U_LIMITS
from puentes_termicas import PSI_SCENARIOS, junction_lengths_m, psi_prime_w_m2k
from section_options import reference_deficit_mm

# The framing fraction band. 15 % is the envelope screen's uniform assumption;
# 8 % is the field value for 48 mm members at 600 mm centres; 23 % is what the
# R2 solver reaches when the timber is widened for R 15. The band is the range
# the project has actually considered, not a statistical interval.
STUD_FRACTIONS = (0.08, 0.10, 0.12, 0.15, 0.18, 0.23)
WALL_INS_MM = 189.0          # the §14-3-compliant thickness at 15 %
WALL_INS_IDX = 2             # mineral wool in envelope_check.wall()

# The margin each row declares, taken from the declaration of margins. These are
# quoted, not recomputed: the point of this screen is the uncertainty around
# them, and recomputing them here would create a second authority.
DECLARED = {
    1: None,          # undefined — product not chosen
    2: 40.0,          # mm
    3: -500.0,        # mm, worst window
    4: -500.0,        # mm, worst window
    5: None,          # filled from the sweep
    6: 300.0,         # mm
    7: 0.0,           # W/m²K — zero by construction at the solved 189 mm
    8: None,          # filled from the sweep
    9: None,          # undefined — no limit
    10: 0.0,          # mm by construction
    11: -160.0,       # mm, worst route
    12: None,         # undefined — C-07 missing
    13: -0.80,        # m²K/W — as drawn, with no break, against the 2D requirement
    14: -130.0,       # Pa net draught at the flue, at the achievable pressure
}

ROWS = (
    (1, "Daylight §13-7", "LT", "input", "LT and frame factor are both unselected"),
    (2, "Fire ch. 11 — door", "free width, mm", "construction",
     "the frame, hinge and stop build-up that turns a 900 mm leaf into a free width"),
    (3, "Fire ch. 11 — escape sill", "sill, mm", "interpretation",
     "which of the three §11-13 readings applies"),
    (4, "Fire ch. 11 — escape size", "h+w, mm", "interpretation",
     "which of the three §11-13 readings applies"),
    (5, "Room height §12-7", "eave, mm", "input",
     "the timber fraction, which is width ÷ centres and not yet chosen"),
    (6, "Natural hazards ch. 7", "freeboard, mm", "interpretation",
     "the freeboard is a project choice, not a regulatory figure"),
    (7, "Envelope §14-3 — wall U", "W/m²K", "input",
     "the stud fraction at a fixed insulation thickness"),
    (8, "Thermal bridges", "Ψ″ W/m²K", "model",
     "only one junction has been calculated, and the mean Ψ″ still rests on a generic range"),
    (9, "Integrated section", "% of width", "interpretation",
     "no fraction is specified, so there is no limit to be short of"),
    (10, "R2 options", "transport, mm", "judgement",
     "the 100 mm reserve is a project allowance, not a measurement"),
    (11, "Installations — drain", "cover, mm", "site",
     "ground level, which no survey has fixed"),
    (12, "Lift geometry", "per-leg tension", "input",
     "C-07: the equipment masses and positions"),
    (13, "Condensation at the junction", "m²K/W", "model",
     "the 1D requirement was computed on a surface that stops governing once any break is built"),
    (14, "Ventilation §13-1(1) — flue", "Pa net draught", "model",
     "both the flue's draught and the pressure a fan holds are assumption ranges"),
)


def sweep_wall():
    """U at the compliant thickness as the stud fraction moves."""
    out = []
    for f in STUD_FRACTIONS:
        u, through = ec.u_parallel_path(ec.wall(WALL_INS_MM), WALL_INS_IDX, f)
        out.append({"fraction": f, "u": round(u, 4),
                    "margin": round(U_LIMITS["wall"] - u, 4)})
    return out


def sweep_section():
    """Eave deficit as the timber fraction moves."""
    out = []
    for f in STUD_FRACTIONS:
        deficit = reference_deficit_mm(f)
        out.append({"fraction": f, "deficit_mm": round(deficit, 1),
                    "margin_mm": round(-deficit, 1)})
    return out


def sweep_bridges():
    """Normalised Ψ″ across the three detailing levels."""
    lengths = junction_lengths_m()
    out = []
    for level in ("good", "ordinary", "poor"):
        psi = psi_prime_w_m2k(PSI_SCENARIOS[level], lengths)
        out.append({"level": level, "psi_prime": round(psi, 4),
                    "margin": round(0.05 - psi, 4)})
    return out


def sweep_flue():
    """Net flue draught across the two assumption ranges, worst and best.

    Both inputs are ranges: the flue's own draught, and the pressure the extract
    holds. The band is the product of the two, so it is wide — which is the
    point, because the margin is negative at every corner of it.
    """
    import ventilacion_check as vc

    b = vc.balance()
    deliverable = [r["pressure_pa"] for r in b["rows"] if r["deliverable"]]
    nets = [draught - p for draught in vc.FLUE_DRAUGHT_PA for p in deliverable]
    return [{"draught_pa": d, "worst_net_pa": round(d - max(deliverable), 1),
             "best_net_pa": round(d - min(deliverable), 1)}
            for d in vc.FLUE_DRAUGHT_PA], nets


def span(values):
    return round(max(values) - min(values), 4)


def fmt(value, spec="+.3g"):
    """Format with a typographic minus, so the tables match the prose."""
    return f"{value:{spec}}".replace("-", "−")


def screen():
    wall = sweep_wall()
    section = sweep_section()
    bridges = sweep_bridges()
    flue_rows, flue_nets = sweep_flue()

    wall_margins = [r["margin"] for r in wall]
    section_margins = [r["margin_mm"] for r in section]
    bridge_margins = [r["margin"] for r in bridges]

    declared = dict(DECLARED)
    # The declared values stay as the declaration states them; the sweeps supply the
    # band around them. This screen tests the declared number, it does not replace it.
    declared[5] = -422.0    # mm at the 15 % reference case
    declared[8] = -0.160    # W/m²K at ordinary detailing

    magnitudes = {
        5: {"kind": "input", "span": span(section_margins),
            "from": round(max(section_margins), 1), "to": round(min(section_margins), 1),
            "unit": "mm"},
        7: {"kind": "input", "span": span(wall_margins),
            "from": round(max(wall_margins), 4), "to": round(min(wall_margins), 4),
            "unit": "W/m²K"},
        8: {"kind": "model", "span": span(bridge_margins),
            "from": round(max(bridge_margins), 4), "to": round(min(bridge_margins), 4),
            "unit": "W/m²K"},
        14: {"kind": "model", "span": span(flue_nets),
             "from": round(max(flue_nets), 1), "to": round(min(flue_nets), 1),
             "unit": "Pa"},
    }

    rows = []
    for number, name, quantity, kind, source in ROWS:
        margin = declared[number]
        mag = magnitudes.get(number)
        if margin is None:
            adequate = None
            verdict = "undefined — no adequacy test is possible"
        elif number == 10:
            adequate = False
            verdict = "**zero by construction** — the option was solved *to* the limit"
        elif number == 7:
            adequate = False
            verdict = ("**zero by construction** — the thickness was solved to hit 0.22 at "
                       "15 %, so the margin is zero there and the band across 8–23 % runs "
                       f"{fmt(mag['from'])} to {fmt(mag['to'])}")
        elif number in (3, 4):
            adequate = False
            verdict = ("**sign set by the interpretation** — −500 mm under the strictest "
                       "§11-13 reading, +100 mm on V-01 under the minimal one")
        elif number == 11:
            adequate = None
            verdict = "**sign set by the site** — +940 mm on the sewer route, −160 mm on the shallow tank"
        elif number == 6:
            adequate = None
            verdict = "positive, but the number is a project choice, not a requirement"
        elif number == 13:
            adequate = False
            verdict = ("**sign inverted by 2D** — the 1D requirement of 0.358 m²K/W was computed "
                       "on the steel, which stops governing at the first millimetre of pad; the "
                       "corner needs 0.80, so the margin is −0.80 as drawn, not +0.051")
        elif number == 2:
            adequate = False
            verdict = ("**not demonstrated** — 40 mm is inside the range of ordinary "
                       "frame and hinge build-ups, and none is specified")
        elif number == 14:
            adequate = False
            verdict = (f"**negative across the band** ({fmt(mag['from'])} to "
                       f"{fmt(mag['to'])}) — and the only negative row whose resolution is not "
                       "a number: a room-sealed stove removes the coupling instead of shrinking "
                       "it, so the row is **retired** rather than made positive")
        elif margin <= 0 and mag and mag["from"] < 0 and mag["to"] < 0:
            adequate = False
            verdict = (f"**negative across the band** ({fmt(mag['from'])} to "
                       f"{fmt(mag['to'])}) — sign robust, magnitude not")
        elif margin > 0 and mag:
            adequate = margin > mag["span"]
            verdict = (f"positive and larger than the {mag['span']:.3g} {mag['unit']} the "
                       "band spans" if adequate else
                       f"**not adequate** — the margin is smaller than the "
                       f"{mag['span']:.3g} {mag['unit']} the band spans")
        else:
            adequate = margin > 0
            verdict = "positive" if adequate else "negative"
        rows.append({"number": number, "screen": name, "quantity": quantity,
                     "kind": kind, "source": source,
                     "margin": margin, "magnitude": mag,
                     "adequate": adequate, "verdict": verdict})

    return {
        "state": "SCREENING — CONDITIONAL ON C-01",
        "wall_ins_mm": WALL_INS_MM,
        "stud_fractions": list(STUD_FRACTIONS),
        "sweeps": {"wall_u": wall, "section": section, "bridges": bridges,
                   "flue": flue_rows},
        "rows": rows,
        "counts": {
            "adequate": sum(1 for r in rows if r["adequate"] is True),
            "not_adequate": sum(1 for r in rows if r["adequate"] is False),
            "untestable": sum(1 for r in rows if r["adequate"] is None),
        },
    }


def markdown(result, source_path):
    rows = result["rows"]
    sweeps = result["sweeps"]
    c = result["counts"]

    lines = [
        "# MiniHouse · are the declared margins adequate?",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a compliance statement, not a "
        "margin certificate.",
        "",
        "- Rows and declared values: `fase1/declaracion-de-margenes.md`.",
        "- Sweeps: `envelope_check.py`, `section_options.py`, `puentes_termicas.py`.",
        "- Generated by `scripts/incertidumbre.py`; JSON companion: "
        "`knowledge/comparisons/incertidumbre.json`.",
        "",
        "## 1. What the declaration asked for and did not do",
        "",
        "The declaration defines a margin as *value available − value required*, **accompanied "
        "by the uncertainty of the model that produced it**, and calls a margin adequate only "
        "when it is positive **and larger than that uncertainty**. It then says, in §8, that "
        "the uncertainty column is not populated for most rows.",
        "",
        "That is the last open item of §2-2(3), and it is not decoration. A margin of "
        "−0.047 W/m²K and a margin of −0.047 ± 0.14 are different statements, and only one of "
        "them tells you whether to act. This screen populates the column.",
        "",
        "## 2. Four kinds of uncertainty, because they behave differently",
        "",
        "| Kind | What it is | How it behaves | Can it be swept? |",
        "|---|---|---|---|",
        "| **model** | the idealisation's own error — a 1D temperature field, a generic Ψ "
        "table, a uniform framing fraction | often **one-sided**: the idealisation is "
        "optimistic or pessimistic, not random | no — needs a finer model |",
        "| **input** | a parameter nobody has measured — λ, LT, the timber fraction | roughly "
        "**symmetric**: the margin could be better or worse | yes |",
        "| **interpretation** | which requirement applies | not an error at all — a "
        "determination | priced as alternative readings |",
        "| **construction** | what the builder will actually achieve | a tolerance, and it "
        "consumes the margin from the other side | only with a specification |",
        "",
        "The distinction matters because only the second kind can be reduced by gathering data. "
        "A model uncertainty needs a better model; an interpretation uncertainty needs a "
        "decision; a construction tolerance needs a detail.",
        "",
        "## 3. The three sweeps",
        "",
        f"### Wall U at the compliant {result['wall_ins_mm']:.0f} mm, as the stud fraction moves",
        "",
        "| Stud fraction | U W/m²K | Margin vs 0.22 |",
        "|---:|---:|---:|",
    ]
    for r in sweeps["wall_u"]:
        lines.append(f"| {r['fraction']:.2f} | {r['u']:.4f} | **{fmt(r['margin'], '+.4f')}** |")
    lines += [
        "",
        f"**Span: {span([r['margin'] for r in sweeps['wall_u']]):.4f} W/m²K.** At 15 % the wall "
        "sits **on** the limit — 0.2202 against 0.2200 — because 189 mm is the thickness that "
        "was *solved* to hit it. So this row is **zero by construction**, exactly like the "
        "transport row, and the declaration does not currently say so. The declared "
        "«−0.047 / +0.011» pair belongs to the **150 mm default** (0.267 with studs, 0.209 "
        "clear field), which is a screening default and not a design thickness: it is the "
        "diagnostic that shows the stud penalty is what breaks the wall, and it is worth "
        "keeping for that reason, but it is not the margin.",
        "",
        "### Eave deficit as the timber fraction moves",
        "",
        "| Timber fraction | Deficit mm | Margin mm |",
        "|---:|---:|---:|",
    ]
    for r in sweeps["section"]:
        lines.append(f"| {r['fraction']:.2f} | {r['deficit_mm']:.1f} | "
                     f"**{fmt(r['margin_mm'], '+.1f')}** |")
    lines += [
        "",
        f"**Span: {span([r['margin_mm'] for r in sweeps['section']]):.1f} mm.** Every value is "
        "negative, so the sign is robust and the uncertainty does not threaten the conclusion. "
        "But **the published −422 mm is neither the best nor the worst case** — it is the 15 % "
        "value, and the R2 report's own sensitivity table runs down to 8 % without ever running "
        "up. At 23 % — a 98 mm member at 400 centres, which the R 15 charring fix may force — "
        "the deficit is **−498 mm**. So the number the project quotes is a mid-band value being "
        "read as if it were the worst.",
        "",
        "### Normalised Ψ″ across the three detailing levels",
        "",
        "| Detailing | Ψ″ W/m²K | Margin vs the 0.05 benchmark |",
        "|---|---:|---:|",
    ]
    for r in sweeps["bridges"]:
        lines.append(f"| {r['level']} | {r['psi_prime']:.4f} | **{fmt(r['margin'], '+.4f')}** |")
    lines += [
        "",
        f"**Span: {span([r['margin'] for r in sweeps['bridges']]):.4f} W/m²K.** Negative at every "
        "level, so the sign is robust — but the magnitude moves by a factor of three, and the "
        "benchmark itself does not bind (it sits in §14-2's route, exempt via §14-5(1)). This "
        "row is the clearest case of a margin that is real and not actionable.",
        "",
        "## 4. Every row, tested",
        "",
        "| # | Screen | Quantity | Kind | Margin | Adequate? | Why |",
        "|---|---|---|---|---:|---|---|",
    ]
    for r in rows:
        margin = "undefined" if r["margin"] is None else fmt(r["margin"])
        if r["adequate"] is True:
            mark = "**yes**"
        elif r["adequate"] is False:
            mark = "**no**"
        else:
            mark = "untestable"
        lines.append(
            f"| {r['number']} | {r['screen']} | {r['quantity']} | {r['kind']} | {margin} | "
            f"{mark} | {r['verdict']} |")
    lines += [
        "",
        f"**{c['adequate']} adequate, {c['not_adequate']} not adequate, "
        f"{c['untestable']} untestable.**",
        "",
        "## 5. What this changes",
        "",
        "**The thinnest positive margin in the project is not demonstrated.** Row 2 reads "
        "**+40 mm** of door free width and the declaration calls it the thinnest positive. It "
        "is 40 mm because a 900 mm leaf is 40 mm wider than the 860 mm requirement — but the "
        "requirement is on the **free** width, and the free width is the leaf minus the frame, "
        "hinge and stop build-up. Nothing in the repository says what that build-up is. "
        "Ordinary timber door sets spend 30–60 mm on it. So the margin is somewhere between "
        "+10 mm and −20 mm, and the sign is unknown.",
        "",
        "This does not mean the door fails. It means **the one margin the declaration called "
        "positive and thin is not yet a margin at all** — it is a nominal leaf size. The fix is "
        "a door schedule with the free width dimensioned, which is a line on a drawing, not a "
        "calculation.",
        "",
        "**Two rows are zero by construction, and the declaration only admits one.** The "
        "transport envelope is flagged as «zero by construction» because every R2 option was "
        "solved *to* 4000 mm. The wall U is in the same position and is not: 189 mm is the "
        "thickness that makes 0.2202 against a limit of 0.2200, so the margin is zero because "
        "the design was solved to the limit, not because the wall happens to land there. "
        "**A dimension solved to a limit has no margin by definition**, and the declaration "
        "should name both rows as the same failure mode rather than one as a fact and the "
        "other as a sign flip.",
        "",
        "**Row 13's sign was inverted, not merely uncertain.** The declaration carried it as a "
        "thin positive: +0.051 m²K/W with the break built. [The 2D calculation]"
        "(verificacion-puente-2d.md) shows that the 1D requirement of 0.358 m²K/W was computed "
        "on the steel, and the steel **stops governing at the first millimetre of pad** — the "
        "timber corner takes over and needs **0.80 m²K/W**. So 9 mm of foam, which the 1D screen "
        "priced as sufficient, gives f_Rsi 0.693 against a criterion of 0.754, and the row is "
        "negative as drawn. This is the one row where the model uncertainty did not make the "
        "margin smaller; it made it the wrong sign, which is why a one-sided bound is not a "
        "substitute for a second dimension.",
        "",
        "**Row 5 survives, but the published number is mid-band.** Every value from 8 % to "
        "23 % is negative, so the timber fraction cannot rescue the section — it is a lever on "
        "the *size* of the deficit, not on its sign. But −422 mm is the 15 % value, and at 23 % "
        "the deficit is **−498 mm**. The R2 report's sensitivity table runs down to 8 % and "
        "never up, so the project has been quoting a mid-band figure in the position where a "
        "worst case belongs. The sign is robust; the magnitude is understated by up to 76 mm.",
        "",
        "## 6. What this does not settle",
        "",
        "1. **Row 8's model uncertainty is still unquantified.** One junction has now been "
        "calculated and it brackets the generic 0.10 W/mK the bridge screen assumed — 0.027 "
        "wrapped, 0.195 unwrapped — but the mean Ψ″ rests on 61.10 m of inventory of which one "
        "junction is solved. A bound there is honest; a number would not be. Row 13 is no longer "
        "in this position: it has a 2D answer, and the answer reversed its sign.",
        "2. **Construction tolerance is absent everywhere.** No row carries it, because no "
        "detail and no specification exist. It is the fourth kind and it is entirely missing.",
        "3. **Row 11's site uncertainty is not an interval.** Ground level is a survey result, "
        "not a distribution.",
        "4. **Rows 1, 9 and 12 stay undefined.** A product, a limit and a mass are missing, and "
        "no sweep can substitute for them.",
        "",
        "## 7. Source and status",
        "",
        "- Margins and their declared values: `fase1/declaracion-de-margenes.md`.",
        "- §2-2(3)'s four demands: S029.",
        "- Sweeps generated here from `envelope_check.py`, `section_options.py` and "
        "`puentes_termicas.py`; none is a measurement.",
        "- SCREENING ONLY — no margin here is certified adequate, and the screen does not "
        "release any geometry.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    result = screen()
    wall = result["sweeps"]["wall_u"]
    section = result["sweeps"]["section"]
    bridges = result["sweeps"]["bridges"]

    # The wall U must rise monotonically with the stud fraction.
    assert all(a["u"] < b["u"] for a, b in zip(wall, wall[1:])), wall
    # At 15 % and 189 mm the wall sits on the limit, which is what "compliant
    # thickness" means; anything else would mean the index or the sweep is wrong.
    at15 = next(r for r in wall if abs(r["fraction"] - 0.15) < 1e-9)
    assert abs(at15["u"] - U_LIMITS["wall"]) < 1e-3, at15
    # The sign must actually flip inside the band, or row 7's finding is empty.
    assert min(r["margin"] for r in wall) < 0 < max(r["margin"] for r in wall), wall

    # The section deficit must grow with the timber fraction and stay negative.
    assert all(a["deficit_mm"] < b["deficit_mm"] for a, b in zip(section, section[1:]))
    assert all(r["margin_mm"] < 0 for r in section), section

    # Bridge Ψ″ must fall from poor to good, and stay above the benchmark.
    assert bridges[0]["psi_prime"] < bridges[1]["psi_prime"] < bridges[2]["psi_prime"]
    assert all(r["margin"] < 0 for r in bridges), bridges

    rows = {r["number"]: r for r in result["rows"]}
    assert len(rows) == 14
    # No row may be certified adequate: the declaration's test is positive AND
    # larger than the uncertainty, and no row clears both clauses.
    assert all(r["adequate"] is not True for r in rows.values()), rows
    # The three computed rows must be marked not adequate, and for the right reason.
    for n in (2, 5, 7, 8, 10, 13, 14):
        assert rows[n]["adequate"] is False, (n, rows[n]["verdict"])
    # Row 5 is negative across the band, so it is not adequate but the sign is robust.
    assert "negative across the band" in rows[5]["verdict"], rows[5]["verdict"]
    # Row 7 is zero by construction, and the band around it changes sign.
    assert "zero by construction" in rows[7]["verdict"], rows[7]["verdict"]
    assert "+0.0236" in rows[7]["verdict"] and "−0.0274" in rows[7]["verdict"], rows[7]
    # Two rows are zero by construction — the transport and the wall U. That pattern
    # is the point: any dimension solved *to* a limit has no margin by definition.
    assert sum(1 for r in rows.values() if "zero by construction" in r["verdict"]) == 2
    # Undefined rows must stay undefined rather than acquiring a number.
    for n in (1, 9, 12):
        assert rows[n]["margin"] is None and rows[n]["adequate"] is None, rows[n]

    counts = result["counts"]
    assert counts["adequate"] == 0, counts
    assert counts["adequate"] + counts["not_adequate"] + counts["untestable"] == 14

    print("Uncertainty self-test OK: wall sweep monotone and on the limit at 15 %, sign "
          "changes inside the band, section and bridge margins robustly negative, no row "
          "certified adequate, undefined rows stay undefined")


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
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(result, "fase1/declaracion-de-margenes.md"),
                        encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
