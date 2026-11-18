# MiniHouse · documentation audit (TEK17 chapters 2 and 4)

**State:** AUDIT — NOT A COMPLIANCE STATEMENT, NOT A HANDBOOK.
Chapter 2 adds no numbers to the building. It adds the test that decides whether the project's own analysis counts ([S029](../knowledge/sources/S029.md)). This audit applies that test to every screening report in the repository.

## 1. Why chapter 2 outranks the chapters it follows

§2-2(1) requires the performance requirements **given** in the regulation to be met. §2-2(2) allows a **functional** requirement to be documented by pre-accepted performance or by **analysis**. The structure is a gate, not a permission:

```
Is a performance requirement (ytelse) given in the regulation?
  YES -> §2-2(1): meet it. Analysis is not a substitute.
  NO  -> §2-2(2): document the function, by pre-accepted performance or analysis.
```

So analysis is available only where **no number was given**. You can analyse your way up to a functional requirement; you cannot analyse your way past a stated performance. Applied to this project's requirement list:

| Class | Count | Instrument |
|---|---:|---|
| Given ytelse (number, class, basis or formula) | **10** | meet it — analysis unavailable |
| Function without a quantity | **3** | analysis is the instrument |
| Scope interpretation | **2** | determination, not analysis |

| Requirement | Class | Instrument |
|---|---|---|
| §14-3 U wall 0.22 / roof 0.18 / floor 0.18 / 1.5 h-1 | given number | meet it |
| §11-4(3) no. 4 R 15 | given number | meet it |
| §12-7(2)(c) 2.2 m room height | given number | meet it |
| §11-14 0.86 m free width | given number | meet it |
| §15-6(2) 0.90 m backflow head | given number | meet it |
| §9-6 10 tonnes waste | given number | meet it |
| §7-2 F2 = 1/200 | given class | meet it |
| §7-3 S2 = 1/1000 | given class | meet it |
| §15-8(1) 100-year climate-adjusted stormwater | given basis | meet it |
| §13-7 Ag >= 0.07*ABRA/LT | given formula | meet it |
| §12-7(2)(d) parts of a room may be lower | function, no fraction | analysis |
| §13-1(1) satisfactory air quality | function, no quantity | analysis |
| §11-4(3) no. 6 whether the roof is decisive for stability | function | analysis |
| §11-13(4) whether one escape window suffices | scope interpretation | determination |
| §11-9 whether the cabin is an escape route | scope interpretation | determination |

**Two consequences.** The room-height fraction in §12-7(2)(d) is a **function with no number**, so the section solver is not an informal sanity check — it is the formal instrument, and §2-2(3) governs it. Conversely the fire questions (is the roof main-system; does one escape window suffice) are **scope interpretations**: analysis cannot answer them, and a determination by the responsible designer can.

## 2. §2-2(3): the admissibility test, applied

An analysis must show the method is **suitable and valid**, the assumptions **described**, the assumptions **justified**, and the **necessary safety margins** stated. The first three can be checked mechanically; the fourth is reported as an observation, because the project states margins in three different currencies and a pass/fail would encode that problem rather than expose it.

| Screening report | State declared | Limits / exclusions | Basis / assumptions | Numeric margin stated |
|---|---|---|---|---|
| daylight §13-7 | yes | yes | yes | *none stated* |
| fire chapter 11 | yes | yes | yes | *none stated* |
| escape windows §11-13 vs daylight §13-7 | yes | yes | yes | *none stated* |
| room height §12-7 | yes | yes | yes | 200 mm |
| natural hazards chapter 7 | yes | yes | yes | 300 mm |
| envelope §14-3 / §13-13 | yes | yes | yes | *none stated* |
| integrated section | yes | yes | yes | *none stated* |
| R2 section options | yes | yes | yes | 100 mm |
| installations chapters 9/15/16/17 | yes | yes | yes | *none stated* |
| condensation at the junction | yes | yes | yes | *none stated* |
| 2D conduction at the floor-edge junction | yes | yes | yes | *none stated* |
| chapter 11 determinations and coupling | yes | yes | yes | 4 |
| ventilation §13-1(1) and envelope pressure | yes | yes | yes | *none stated* |
| make-up air sizing and the flue | yes | yes | yes | 14 t |
| radon §13-5 for a floor off the ground | yes | yes | yes | 3 |
| lift geometry | yes | yes | yes | *none stated* |

The **Limits** sections these reports already carry are therefore not good manners — they are §2-2(3) work. The weakest column is the last one. Three different kinds of margin are in use and none is presented as *the* margin the analysis relies on:

- **screening value** — the 4.00 m transport height (S022), a general value, not a route permit;
- **project reserve** — the 100 mm allowance in the R2 options, a project choice;
- **material factor** — the 1.4 in the natural-hazard screen, flagged unverified because the NA is paywalled.

§2-2(3) asks for one coherent statement of what margin is being relied on and why it is enough. **That statement now exists**: [declaración de márgenes](../fase1/declaracion-de-margenes.md) fixes one currency per analysis type and states every margin with its sign.

It does not deliver the answer the project wanted. Of the 15 rows it tabulates, **2 are positive, 7 negative, 4 undefined and 2 zero by construction** — and one of the positive rows is a project choice rather than a regulatory number. So §2-2(3)'s fourth demand cannot be satisfied by writing a number down: the project is not short of a margin statement, it is **short of margin**.

Two consequences follow, and they are why the declaration is gated rather than merely filed:

1. **R2 stops being a preference.** Every R2 option was solved *to* 4000 mm, so the governing dimension has zero margin by construction. Choosing an option that gives some back is what produces a positive margin, which makes the choice a regulatory requirement rather than a taste.
2. **"Undefined" must survive.** Three rows are undefined because a product, a fraction and a mass are missing. Filling them with plausible values would make the declaration look complete and be worthless.

## 3. §2-2(4): why the basis does not exist yet

> «De fastsatte ytelsene skal gi et tilstrekkelig underlag for detaljprosjekteringen.»

The assumed performances must give a **sufficient basis for detailed design**. This is the cleanest description of where Fase 1 stands: the screens have produced a great deal of §2-2(3)-quality analysis and one conclusion that the basis does **not** yet exist — at 20° with a realistic envelope the section does not close under 4.00 m. That is not a failure of the work; it is §2-2(4) doing its job. R2 is the step that produces the missing basis, and until one option is chosen §2-2(4) is unsatisfied by construction.

## 4. §2-3 and §2-4: the stages not reached

| Stage | Duty | Status |
|---|---|---|
| §2-3(1) | document that designed solutions and **product specifications** meet the ytelser | **not reached** — no product specified |
| §2-3(2) | produce a **produksjonsunderlag** sufficient for execution | **not reached** |
| §2-4 | document that execution and chosen products match the produksjonsunderlag | **not reached** |

§2-3(1) is why the envelope screen's «generic λ, no products selected» caveat matters. A U-value demonstrated with generic conductivity shows that a **thickness** could work; it does not show that a **product specification** does. That distinction is the whole of §2-3(1), and it is the difference between a screen and a specification.

§2-4 has a wrinkle worth naming early. It compares execution against the produksjonsunderlag, and a **transportable** building is executed once but *installed* many times. Each installation has its own foundation, connections and site conditions that are not in the module's produksjonsunderlag. That gap is not covered by §2-4 as written, and §4-1 runs into it from the other side.

## 5. §4-1: FDV, and the exemption that does not fit

The residential FDV list is short and achievable — and it is the one part of the whole compliance picture that is **finished in scope** and merely needs filling:

| §4-1 category | In the current design |
|---|---|
| building products and surfaces to clean and maintain | yes |
| sanitary installations | yes |
| heating installations | yes |
| ventilation installations | yes |
| electrical installations | yes |
| fire alarm and extinguishing installations | yes |

**6 of 6.** §4-1(2) drops the duty where documentation is «åpenbart overflødig», with examples: smaller garage, boathouse (naust), outhouse (uthus).

Every one of those examples is an **unheated, unserviced, non-dwelling** structure. A cabin with a wood stove, a water installation, a drainage installation, ventilation and fire detection has six of six categories. The exemption is therefore **considered and rejected** — which is a determination, not an omission, and this project has been careful about that distinction elsewhere.

**FDV is a living document here, not a handover file.** The guidance requires it to be *ajour*, to match the building **as actually built**, and to state the **premises, conditions and limitations** of the design. For a building designed to be re-sited, every move changes the premises: ground, flood level, wind and snow exposure, foundation, service connections. A single binder cannot stay *ajour* across that. The obligation argues for a **structured, versioned file with a site-specific section re-issued at every deployment** — a documentation-architecture decision that is cheap now and expensive later.

## 6. §2-1: the National Annex is a documentation blocker too

§2-1's guidance requires **National Annexes to be applied** to meet Norwegian building rules, including where a pre-accepted performance is tied to a standard. S014 records that the Norwegian NA texts are paywalled, which was filed as a *design* blocker — no γ or ψ values may be used. It is also a **documentation** blocker: without the NAs the structural route cannot be documented as compliant. One paywall, two blockers.

## 7. Limits

- The **veiledning for §§2-2, 2-3, 2-4 and 4-2 was not retrieved**; four DIBK pages returned navigation only and the Lovdata consolidation supplies binding text without guidance.
- The ytelse/function classification in §1 is this audit's reading of the provisions against the project's requirement list. It is **not** a legal opinion, and the responsible designer and the municipality decide which ytelse applies in a real case.
- The §4-1(2) rejection is a reasoned determination, not a municipal ruling.
- The margin column detects a stated numeric margin; it does not judge whether the margin is adequate, and its absence is not a finding of inadequacy.
- No produksjonsunderlag, execution documentation or FDV file exists. Nothing here is a completion certificate or a compliance statement.

- Generated by `scripts/documentacion_check.py`; JSON companion: `knowledge/comparisons/documentacion-check.json`.
