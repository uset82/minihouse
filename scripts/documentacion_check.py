#!/usr/bin/env python3
"""MiniHouse · documentation audit (TEK17 chapter 2 and chapter 4).

Chapter 2 does not add numbers to the building. It adds the test that decides
whether the project's own analysis counts, and until now that test has been
applied by habit rather than stated.

§2-2(3) requires four things of an analysis used to demonstrate a functional
requirement:

    method suitable and valid for the purpose
    assumptions described
    assumptions justified
    necessary safety margins stated

Every screening report in this repository is such an analysis. This script
audits them against those demands, and it separates what can be checked
mechanically from what cannot:

  * PASS/FAIL  state declaration, limits/exclusions, basis/assumptions
  * OBSERVED   whether a numeric margin is stated at all, and which

The margin column is deliberately an observation and not a gate, because the
finding is that the project states margins in three different currencies
(screening value, reserve, material factor) and §2-2(3) asks for one coherent
statement. Turning that into a pass/fail now would encode the problem.

That statement now exists: `fase1/declaracion-de-margenes.md` fixes the
currency per analysis type and states every margin with its sign. So the gate
moves to the declaration itself — it must exist, cover all fourteen screens, and
keep the four positions that make it honest (the operational definition, the
legitimacy of "undefined", the double-counting warning, and R2 as a
requirement rather than a preference). What the declaration then *says* is not
gated, because most of its entries are negative and that is the finding.

It also records two determinations the chapter forces:

  * which requirements are given ytelser (§2-2(1), analysis unavailable) and
    which are functions (§2-2(2), analysis is the instrument);
  * whether §4-1(2)'s "small and simple measure" exemption can apply.

Usage:
  python documentacion_check.py --out-md fase1/verificacion-documentacion.md \
      --out-json knowledge/comparisons/documentacion-check.json
  python documentacion_check.py --selftest
"""
import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Screening reports that are analyses under §2-2(2)(b).
SCREENS = (
    ("fase1/verificacion-luz-diurna.md", "daylight §13-7"),
    ("fase1/verificacion-incendio.md", "fire chapter 11"),
    ("fase1/verificacion-ventanas.md", "escape windows §11-13 vs daylight §13-7"),
    ("fase1/verificacion-altura-libre.md", "room height §12-7"),
    ("fase1/cribado-riesgos-naturales.md", "natural hazards chapter 7"),
    ("fase1/verificacion-envolvente.md", "envelope §14-3 / §13-13"),
    ("fase1/verificacion-seccion.md", "integrated section"),
    ("fase1/opciones-seccion-R2.md", "R2 section options"),
    ("fase1/verificacion-instalaciones.md", "installations chapters 9/15/16/17"),
    ("fase1/verificacion-condensacion-union.md", "condensation at the junction"),
    ("fase1/verificacion-puente-2d.md", "2D conduction at the floor-edge junction"),
    ("fase1/determinacion-estrategia-incendio.md", "chapter 11 determinations and coupling"),
    ("fase1/verificacion-ventilacion.md", "ventilation §13-1(1) and envelope pressure"),
    ("fase1/verificacion-aporte-aire.md", "make-up air sizing and the flue"),
    ("knowledge/comparisons/lift-geometry-screen.md", "lift geometry"),
)

STATE_MARKER = "**State:**"

LIMITS_MARKERS = (
    "not a simulation",
    "not a daylight simulation",
    "not a design decision",
    "not a compliance certificate",
    "not a fire-engineering analysis",
    "not a lift plan",
    "not an installation approval",
    "not a geotechnical assessment",
    "not a thermal calculation",
    "excluded",
)
# Any "## 9. Limits" / "## Exclusions" / "## What this is not" heading counts.
LIMITS_HEADING = re.compile(
    r"^#{2,4}\s*(?:\d+\.\s*)?(limits|exclusions?|what this is not)\b",
    re.IGNORECASE | re.MULTILINE,
)

BASIS_MARKERS = (
    "assumption",
    "conditional on",
    "screening value",
    "screening method",
    "generic",
    "no site",
    "not project data",
    "procedure",
)

# A stated margin is a number sitting next to a word that names a margin.
MARGIN_WORDS = ("reserve", "margin", "material factor", "safety factor")
NUMBER = re.compile(r"(\d+(?:[.,]\d+)?)\s*(mm|%|°|t|kN|m\b)?")

# §2-2(2): given ytelse (analysis unavailable) vs function (analysis is the instrument).
REQUIREMENTS = (
    ("§14-3 U wall 0.22 / roof 0.18 / floor 0.18 / 1.5 h-1", "given number", "meet it"),
    ("§11-4(3) no. 4 R 15", "given number", "meet it"),
    ("§12-7(2)(c) 2.2 m room height", "given number", "meet it"),
    ("§11-14 0.86 m free width", "given number", "meet it"),
    ("§15-6(2) 0.90 m backflow head", "given number", "meet it"),
    ("§9-6 10 tonnes waste", "given number", "meet it"),
    ("§7-2 F2 = 1/200", "given class", "meet it"),
    ("§7-3 S2 = 1/1000", "given class", "meet it"),
    ("§15-8(1) 100-year climate-adjusted stormwater", "given basis", "meet it"),
    ("§13-7 Ag >= 0.07*ABRA/LT", "given formula", "meet it"),
    ("§12-7(2)(d) parts of a room may be lower", "function, no fraction", "analysis"),
    ("§13-1(1) satisfactory air quality", "function, no quantity", "analysis"),
    ("§11-4(3) no. 6 whether the roof is decisive for stability", "function", "analysis"),
    ("§11-13(4) whether one escape window suffices", "scope interpretation", "determination"),
    ("§11-9 whether the cabin is an escape route", "scope interpretation", "determination"),
)

# §4-1 residential FDV categories.
FDV_CATEGORIES = (
    "building products and surfaces to clean and maintain",
    "sanitary installations",
    "heating installations",
    "ventilation installations",
    "electrical installations",
    "fire alarm and extinguishing installations",
)
# §4-1(2) exemption examples: unheated, unserviced, non-dwelling.
EXEMPTION_EXAMPLES = ("smaller garage", "boathouse (naust)", "outhouse (uthus)")


def read(rel):
    path = ROOT / rel
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def margin_on_line(line):
    """First number that precedes a margin word on a line, markdown emphasis removed.

    Reports write "a **100 mm** reserve" and "a 1.4 material factor", so the
    emphasis markers and the unit both have to be handled. The number nearest
    before the margin word is the one being relied on.
    """
    clean = re.sub(r"^\s*(?:\d+\.|[-*+])\s+", "", line)  # drop list markers, or "3." reads as a number
    clean = re.sub(r"[*`_]", "", clean)
    low = clean.lower()
    hits = [low.find(word) for word in MARGIN_WORDS if word in low]
    if not hits:
        return None
    before = clean[:min(hits)]
    numbers = NUMBER.findall(before)
    if not numbers:
        return None
    value, unit = numbers[-1]
    return f"{value} {unit}".strip() if unit else value


DECLARATION = "fase1/declaracion-de-margenes.md"

# The four positions that make the declaration honest rather than decorative.
DECLARATION_MARKERS = {
    "definition": "value available − value required",
    "undefined_allowed": "undefined is a legitimate entry",
    "double_counting": "double-counts",
    "r2_as_requirement": "regulatory requirement",
    "tally": "two rows are positive",
}


def declaration_tally():
    """Count the signs in the declaration's own §2 table.

    Parsing the table rather than restating the tally means the audit fails the
    moment a row changes sign, instead of quietly summarising an old version.
    The verdict cell is read first; where it carries no sign word (rows whose
    verdict is prose), the margin cell decides.
    """
    text = read(DECLARATION)
    if text is None:
        return {"rows": 0, "positive": 0, "negative": 0, "undefined": 0, "zero": 0,
                "unclassified": []}
    counts = {"positive": 0, "negative": 0, "undefined": 0, "zero": 0}
    unclassified, rows = [], 0
    for line in text.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        rows += 1
        verdict, margin = cells[6].lower(), cells[5].lower()
        if "zero by construction" in verdict:
            counts["zero"] += 1
        elif "undefined" in verdict or "undefined" in margin:
            counts["undefined"] += 1
        elif "sign flips" in verdict:
            # counted at the fraction that fails, which is the 15 % case
            counts["negative"] += 1
        elif "positive" in verdict:
            counts["positive"] += 1
        elif "negative" in verdict:
            counts["negative"] += 1
        else:
            unclassified.append(cells[0])
    return {"rows": rows, **counts, "unclassified": unclassified}


def declaration_audit():
    """Check the §2-2(3) declaration exists, covers every screen and keeps its positions."""
    text = read(DECLARATION)
    if text is None:
        return {"file": DECLARATION, "exists": False, "covers_all": False,
                "missing": [rel for rel, _ in SCREENS],
                "markers": {k: False for k in DECLARATION_MARKERS},
                "tally": declaration_tally()}
    missing = [rel for rel, _ in SCREENS if Path(rel).name not in text]
    return {
        "file": DECLARATION,
        "exists": True,
        "covers_all": not missing,
        "missing": missing,
        "markers": {k: v in text for k, v in DECLARATION_MARKERS.items()},
        "tally": declaration_tally(),
    }


def audit_report(rel):
    text = read(rel)
    if text is None:
        return {"file": rel, "exists": False, "state": False, "limits": False,
                "basis": False, "margin": None}
    low = text.lower()
    margin = None
    for line in text.splitlines():
        found = margin_on_line(line)
        if found:
            margin = found
            break
    return {
        "file": rel,
        "exists": True,
        "state": STATE_MARKER in text,
        "limits": bool(LIMITS_HEADING.search(text)) or any(m in low for m in LIMITS_MARKERS),
        "basis": any(marker in low for marker in BASIS_MARKERS),
        "margin": margin,
    }


def screen():
    audits = [audit_report(rel) for rel, _ in SCREENS]
    labels = dict(SCREENS)

    given = [r for r in REQUIREMENTS if r[1] in ("given number", "given class", "given basis", "given formula")]
    analysis = [r for r in REQUIREMENTS if r[2] == "analysis"]
    determination = [r for r in REQUIREMENTS if r[2] == "determination"]

    # §4-1(2): how many of the six FDV categories does this building actually have?
    present = len(FDV_CATEGORIES)  # all six are in the current design
    return {
        "revision": "DOCUMENTACION-CHECK",
        "state": "AUDIT — NOT A COMPLIANCE STATEMENT, NOT A HANDBOOK",
        "basis": {"sources": ["S029"], "state_marker": STATE_MARKER},
        "audits": [{**a, "label": labels[a["file"]]} for a in audits],
        "requirements": [
            {"requirement": r, "kind": kind, "instrument": inst}
            for r, kind, inst in REQUIREMENTS
        ],
        "counts": {
            "given": len(given),
            "analysis": len(analysis),
            "determination": len(determination),
        },
        "fdv": {
            "categories": list(FDV_CATEGORIES),
            "present": present,
            "exemption_examples": list(EXEMPTION_EXAMPLES),
            "exemption_applies": present < len(FDV_CATEGORIES) // 2,
        },
        "declaration": declaration_audit(),
        "excluded": [
            "compliance statement", "produksjonsunderlag", "execution documentation",
            "FDV file", "legal opinion on which ytelse applies",
        ],
    }


def markdown(model):
    a = model["audits"]
    c = model["counts"]
    t = model["declaration"]["tally"]
    L = [
        "# MiniHouse · documentation audit (TEK17 chapters 2 and 4)",
        "",
        "**State:** AUDIT — NOT A COMPLIANCE STATEMENT, NOT A HANDBOOK.",
        "Chapter 2 adds no numbers to the building. It adds the test that decides whether the "
        "project's own analysis counts ([S029](../knowledge/sources/S029.md)). This audit applies "
        "that test to every screening report in the repository.",
        "",
        "## 1. Why chapter 2 outranks the chapters it follows",
        "",
        "§2-2(1) requires the performance requirements **given** in the regulation to be met. "
        "§2-2(2) allows a **functional** requirement to be documented by pre-accepted performance "
        "or by **analysis**. The structure is a gate, not a permission:",
        "",
        "```",
        "Is a performance requirement (ytelse) given in the regulation?",
        "  YES -> §2-2(1): meet it. Analysis is not a substitute.",
        "  NO  -> §2-2(2): document the function, by pre-accepted performance or analysis.",
        "```",
        "",
        "So analysis is available only where **no number was given**. You can analyse your way up "
        "to a functional requirement; you cannot analyse your way past a stated performance. "
        "Applied to this project's requirement list:",
        "",
        f"| Class | Count | Instrument |",
        "|---|---:|---|",
        f"| Given ytelse (number, class, basis or formula) | **{c['given']}** | meet it — analysis unavailable |",
        f"| Function without a quantity | **{c['analysis']}** | analysis is the instrument |",
        f"| Scope interpretation | **{c['determination']}** | determination, not analysis |",
        "",
        "| Requirement | Class | Instrument |",
        "|---|---|---|",
    ]
    for r in model["requirements"]:
        L.append(f"| {r['requirement']} | {r['kind']} | {r['instrument']} |")

    L += [
        "",
        "**Two consequences.** The room-height fraction in §12-7(2)(d) is a **function with no "
        "number**, so the section solver is not an informal sanity check — it is the formal "
        "instrument, and §2-2(3) governs it. Conversely the fire questions (is the roof "
        "main-system; does one escape window suffice) are **scope interpretations**: analysis "
        "cannot answer them, and a determination by the responsible designer can.",
        "",
        "## 2. §2-2(3): the admissibility test, applied",
        "",
        "An analysis must show the method is **suitable and valid**, the assumptions **described**, "
        "the assumptions **justified**, and the **necessary safety margins** stated. The first "
        "three can be checked mechanically; the fourth is reported as an observation, because the "
        "project states margins in three different currencies and a pass/fail would encode that "
        "problem rather than expose it.",
        "",
        "| Screening report | State declared | Limits / exclusions | Basis / assumptions | Numeric margin stated |",
        "|---|---|---|---|---|",
    ]
    for row in a:
        if not row["exists"]:
            L.append(f"| `{row['file']}` | **missing file** | — | — | — |")
            continue
        L.append(
            f"| {row['label']} | {'yes' if row['state'] else '**no**'} | "
            f"{'yes' if row['limits'] else '**no**'} | {'yes' if row['basis'] else '**no**'} | "
            f"{row['margin'] if row['margin'] else '*none stated*'} |"
        )

    L += [
        "",
        "The **Limits** sections these reports already carry are therefore not good manners — they "
        "are §2-2(3) work. The weakest column is the last one. Three different kinds of margin are "
        "in use and none is presented as *the* margin the analysis relies on:",
        "",
        "- **screening value** — the 4.00 m transport height (S022), a general value, not a route permit;",
        "- **project reserve** — the 100 mm allowance in the R2 options, a project choice;",
        "- **material factor** — the 1.4 in the natural-hazard screen, flagged unverified because the NA is paywalled.",
        "",
        "§2-2(3) asks for one coherent statement of what margin is being relied on and why it is "
        "enough. **That statement now exists**: "
        "[declaración de márgenes](../fase1/declaracion-de-margenes.md) fixes one currency per "
        "analysis type and states every margin with its sign.",
        "",
        "It does not deliver the answer the project wanted. Of the "
        f"{t['rows']} rows it tabulates, **{t['positive']} are positive, {t['negative']} "
        f"negative, {t['undefined']} undefined and {t['zero']} zero by construction** — and "
        "one of the positive rows is a project choice rather than a regulatory number. So "
        "§2-2(3)'s fourth demand cannot be satisfied by writing a number down: the project is "
        "not short of a margin statement, it is **short of margin**.",
        "",
        "Two consequences follow, and they are why the declaration is gated rather than merely "
        "filed:",
        "",
        "1. **R2 stops being a preference.** Every R2 option was solved *to* 4000 mm, so the "
        "governing dimension has zero margin by construction. Choosing an option that gives some "
        "back is what produces a positive margin, which makes the choice a regulatory "
        "requirement rather than a taste.",
        "2. **\"Undefined\" must survive.** Three rows are undefined because a product, a fraction "
        "and a mass are missing. Filling them with plausible values would make the declaration "
        "look complete and be worthless.",
        "",
        "## 3. §2-2(4): why the basis does not exist yet",
        "",
        "> «De fastsatte ytelsene skal gi et tilstrekkelig underlag for detaljprosjekteringen.»",
        "",
        "The assumed performances must give a **sufficient basis for detailed design**. This is the "
        "cleanest description of where Fase 1 stands: the screens have produced a great deal of "
        "§2-2(3)-quality analysis and one conclusion that the basis does **not** yet exist — at 20° "
        "with a realistic envelope the section does not close under 4.00 m. That is not a failure "
        "of the work; it is §2-2(4) doing its job. R2 is the step that produces the missing basis, "
        "and until one option is chosen §2-2(4) is unsatisfied by construction.",
        "",
        "## 4. §2-3 and §2-4: the stages not reached",
        "",
        "| Stage | Duty | Status |",
        "|---|---|---|",
        "| §2-3(1) | document that designed solutions and **product specifications** meet the ytelser | **not reached** — no product specified |",
        "| §2-3(2) | produce a **produksjonsunderlag** sufficient for execution | **not reached** |",
        "| §2-4 | document that execution and chosen products match the produksjonsunderlag | **not reached** |",
        "",
        "§2-3(1) is why the envelope screen's «generic λ, no products selected» caveat matters. A "
        "U-value demonstrated with generic conductivity shows that a **thickness** could work; it "
        "does not show that a **product specification** does. That distinction is the whole of "
        "§2-3(1), and it is the difference between a screen and a specification.",
        "",
        "§2-4 has a wrinkle worth naming early. It compares execution against the "
        "produksjonsunderlag, and a **transportable** building is executed once but *installed* "
        "many times. Each installation has its own foundation, connections and site conditions "
        "that are not in the module's produksjonsunderlag. That gap is not covered by §2-4 as "
        "written, and §4-1 runs into it from the other side.",
        "",
        "## 5. §4-1: FDV, and the exemption that does not fit",
        "",
        "The residential FDV list is short and achievable — and it is the one part of the whole "
        "compliance picture that is **finished in scope** and merely needs filling:",
        "",
        "| §4-1 category | In the current design |",
        "|---|---|",
    ]
    for cat in model["fdv"]["categories"]:
        L.append(f"| {cat} | yes |")

    L += [
        "",
        f"**{model['fdv']['present']} of {len(model['fdv']['categories'])}.** §4-1(2) drops the duty "
        "where documentation is «åpenbart overflødig», with examples: "
        + ", ".join(model["fdv"]["exemption_examples"]) + ".",
        "",
        "Every one of those examples is an **unheated, unserviced, non-dwelling** structure. A cabin "
        "with a wood stove, a water installation, a drainage installation, ventilation and fire "
        "detection has six of six categories. The exemption is therefore **considered and "
        "rejected** — which is a determination, not an omission, and this project has been careful "
        "about that distinction elsewhere.",
        "",
        "**FDV is a living document here, not a handover file.** The guidance requires it to be "
        "*ajour*, to match the building **as actually built**, and to state the **premises, "
        "conditions and limitations** of the design. For a building designed to be re-sited, every "
        "move changes the premises: ground, flood level, wind and snow exposure, foundation, "
        "service connections. A single binder cannot stay *ajour* across that. The obligation "
        "argues for a **structured, versioned file with a site-specific section re-issued at every "
        "deployment** — a documentation-architecture decision that is cheap now and expensive later.",
        "",
        "## 6. §2-1: the National Annex is a documentation blocker too",
        "",
        "§2-1's guidance requires **National Annexes to be applied** to meet Norwegian building "
        "rules, including where a pre-accepted performance is tied to a standard. S014 records that "
        "the Norwegian NA texts are paywalled, which was filed as a *design* blocker — no γ or ψ "
        "values may be used. It is also a **documentation** blocker: without the NAs the structural "
        "route cannot be documented as compliant. One paywall, two blockers.",
        "",
        "## 7. Limits",
        "",
        "- The **veiledning for §§2-2, 2-3, 2-4 and 4-2 was not retrieved**; four DIBK pages returned "
        "navigation only and the Lovdata consolidation supplies binding text without guidance.",
        "- The ytelse/function classification in §1 is this audit's reading of the provisions "
        "against the project's requirement list. It is **not** a legal opinion, and the responsible "
        "designer and the municipality decide which ytelse applies in a real case.",
        "- The §4-1(2) rejection is a reasoned determination, not a municipal ruling.",
        "- The margin column detects a stated numeric margin; it does not judge whether the margin "
        "is adequate, and its absence is not a finding of inadequacy.",
        "- No produksjonsunderlag, execution documentation or FDV file exists. Nothing here is a "
        "completion certificate or a compliance statement.",
        "",
        "- Generated by `scripts/documentacion_check.py`; JSON companion: "
        "`knowledge/comparisons/documentacion-check.json`.",
        "",
    ]
    return "\n".join(L)


def selftest():
    model = screen()
    # Every declared screening report must exist and carry a state declaration.
    for row in model["audits"]:
        assert row["exists"], f"missing screening report: {row['file']}"
        assert row["state"], f"no state declaration in {row['file']}"
        # The docstring calls these two PASS/FAIL gates, so they are asserted.
        # They were displayed but unchecked until the 2D report was added with a
        # limits section the heading pattern did not recognise.
        assert row["limits"], f"no limits/exclusions section in {row['file']}"
        assert row["basis"], f"no basis/assumption statement in {row['file']}"
    # §2-2(2) gate: given ytelser must never be classified as analysable.
    for r in model["requirements"]:
        if r["kind"] in ("given number", "given class", "given basis", "given formula"):
            assert r["instrument"] == "meet it", r["requirement"]
        if r["kind"] == "function, no fraction":
            assert r["instrument"] == "analysis", r["requirement"]
    # The classification must be non-trivial in both directions.
    assert model["counts"]["given"] >= 8
    assert model["counts"]["analysis"] >= 2
    assert model["counts"]["determination"] >= 1
    # §4-1(2): a building with all six categories cannot use the exemption.
    assert model["fdv"]["present"] == len(FDV_CATEGORIES)
    assert model["fdv"]["exemption_applies"] is False
    # The margin detector must find a real margin somewhere, or the column is dead.
    assert any(row["margin"] for row in model["audits"]), "margin column found nothing"
    # The §2-2(3) declaration must exist, cover every screen, and keep its four positions.
    decl = model["declaration"]
    assert decl["exists"], f"missing §2-2(3) declaration: {DECLARATION}"
    assert decl["covers_all"], f"declaration omits: {decl['missing']}"
    for name, present in decl["markers"].items():
        assert present, f"declaration lost its '{name}' position"
    # The tally is parsed from the declaration, so it cannot summarise an old version.
    # If a row changes sign this fails and the summary has to be re-read, not re-typed.
    t = decl["tally"]
    assert t["rows"] == 14, t
    assert not t["unclassified"], f"rows with no readable verdict: {t['unclassified']}"
    assert (t["positive"], t["negative"], t["undefined"], t["zero"]) == (2, 7, 3, 2), t
    print("Documentation self-test OK: state declarations, §2-2 gate classification, "
          "§4-1 exemption test, margin detection and a 14-row declaration tally of "
          "2 positive / 7 negative / 3 undefined / 2 zero all pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-json", help="write JSON audit model")
    ap.add_argument("--out-md", help="write Markdown audit report")
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
