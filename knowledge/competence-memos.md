# Competence memos · PhD-level capability check

Date: 2026-11-16; Chapter 13 scope correction 2026-11-17; Chapter 11 fire pass 2026-11-17. One memo per domain: can I derive it, navigate its codes, critique sources, verify numerically, and synthesise a decision? Status reflects **what is now actually in the knowledge base**, not aspirations.

## D1 · Foundations — PASSED
Derive: D001 from equilibrium + Euler-Bernoulli, symbolic and numeric. Critique: sign convention identified and documented; Euler-Bernoulli limits listed. Verify: 24.634 / 1.490 mm reproduced. Synthesis: distinction recorded between ideal-beam support inset and real chassis. Gap: FEM theory (Fish/Belytschko) and dynamics (Chopra) not yet acquired — foundations at undergraduate-proven level, not yet PhD-depth in FEM formulation.

## D2 · Steel design / EC3 — PARTIAL
Navigate: clause-path map built; EN 1993 part identities verified at JRC. Critique: C001 confirmed. Gap: **Norwegian NA coefficients unavailable** — no Eurocode verification can be performed; actual standard clause wording not read. This is the single largest remaining competence gap.

## D3 · Connections / lifting details — PASSED at framework level
Derive: full 10-step load path and 12 failure modes (D002). Evidence: primary QUB tests with F–δ, failure modes, CoV (S007). Critique: 17.5 kN not imported. Synthesis: a-priori test protocol written. Gap: no ear detail designed (blocked on forces).

## D4 · Modular construction / DfMA — PASSED at framework level
SCI P272 read in full (S008); transport/lift design philosophy, robustness and weatherproofing captured; lift-variant comparison written. Gap: Lawson/Ogden/Goodier book still to acquire; UK transport limits explicitly excluded.

## D5 · Lifting, rigging, transport — PASSED at requirements level
Derive: sling math verified (D003) and extended to normalized I-1/I-2 corner/inset geometry at 3000–5000 mm hook-to-point verticals (`lift-geometry-screen.md`, 2026-11-17). Navigate: VegSak/§5 verified at source; EN 13155 identified. Synthesis: lift-plan checklist with three point types, unequal-leg case, a-priori criteria. Gap: no real crane, route or mass — no actual lift plan.

## D6 · Norwegian regulation — SUBSTANTIALLY CLOSED
TEK17 §10-2 (S005), Chapter 13 route map (S023), Chapter 11 fire route (S024) and §14-2/3/5 (S011, S020, S021) verified; Arbeidstilsynet §§10-1/2/3 and 13-1/3 verified at Lovdata (S013). §13-2/9/13 numbers remain valid where their sections apply (S012), but §13-2 is explicitly NOT applicable to the mikrohus route: §13-1(1) functional ventilation with documented alternative air quantities governs instead. Chapter 11 is the first chapter where the answer is **independent of the C-01 dwelling/holiday-home ambiguity** — both are risk class 4 / BKL 1 — and it also produced two checkable design findings: R 15 rather than R 30, and only one of the three current windows qualifies as an escape window. Remaining: Norwegian NA texts confirmed paywalled (S014), NS 3031:2014 not held if thermal documentation is required, §§11-9/11-10 not retrieved, and the specific written-lift-plan paragraph not located. Compliance matrix honest about each.

## D7 · Architecture / building physics — PASSED at requirements level
Moisture physics principles verified (S010) and paired with legal TEK17 limits (S012/S023: Sd ≥ 10 m, vapour-open wind barrier, ventilated cavity; §13-1(1) functional ventilation with documented alternative air quantities on the mikrohus route, not the 1.2 m³/h·m² §13-2 schedule); energy minimums (§14-3) and §14-5 exceptions verified (S011/S021), with the småhus frame arithmetic explicitly not a MiniHouse target; 5 failure mechanisms and controls in module brief; reclaimed-timber traceability stated. Remaining: NS 3031 only if thermal documentation is required (C-01 use classification needed); architecture theory books (Ching, Mallgrave, Maggi) not acquired; no spatial/visual design beyond R0.

## D8 · Tooling — PASSED as prepared
Mass calculator self-test executed; R0 parametric model generated and validated; Autodesk/SMLX/IFC exchange procedure written with mandatory difference table; SolidCraft role correctly scoped; reproducible screens now cover sling geometry, mass sensitivity, R1 skeleton, §13-7 daylight and §11-13 escape windows. Gap: no live application to execute the exchange.

## D9 · Research method — PARTIAL
Provenance, condition-of-application and state labelling applied throughout; critique file maintained. The Turing Way acquired (S015) — the knowledge/ structure already follows its research-compendium principles (separate data/methods/output, README index, executable verification scripts). *The Craft of Research*, ASME V&V and Hevner design-science methodology still to acquire.

One methodological habit worth naming, because the Chapter 11 pass exercised it twice: **the script found the error, not the prose.** The first escape-window self-test failed because V-03 also violates the sill rule, which the hand-written table had missed; and the boundary cases initially asserted a 500 × 600 window passed the sum rule when 1100 < 1500. Both were caught by executable assertions before any document shipped. That is the mechanism working as intended.

## Overall judgement (updated 2026-11-17, Chapter 11 pass)

The plan plus the gap-closing passes produced a **verified engineering and regulatory foundation**: three reproduced calculations, primary-source evidence for the critical lift question, TEK17 numeric requirements with their true route scope (energy §14-3/§14-5, Chapter 13 §13-1(1) vs §13-2, Chapter 11 fire §11-4(3) no. 4 R 15), verified Norwegian work law for lifting competence/control, and honest blockers. D1, D3, D4, D5, D7 and D8 passed their gates; D6 substantially closed; D2 and D9 partial with hard/identified gaps (paywalled NA, NS 3031 only if needed, three method books).

It has NOT produced a fabricated design, a real lift plan, or code-compliant member sizing — all correctly blocked on missing project data (C-01…C-09) and paywalled Norwegian standards. That is the right result at this stage; pretending otherwise would violate rules.md §5. No diploma is claimed or implied.
