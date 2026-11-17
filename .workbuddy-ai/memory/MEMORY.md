# MiniHouse · long-term project notes

## Role and boundary

Agent = lead engineer / designer / CAD expert (Inge), covering the six AGENTS.md roles. Assigned by Carlos 2026-11-16. Fabrication release, structural sign-off and authorisation of real lifts stay with the qualified human authority (rules.md §5). Never claim code compliance, geotechnical assessment, siting approval or lift authorisation.

## Tooling reality

Autodesk (Robot, Revit, Advance Steel, AutoCAD, Forma) and SolidCraft have no live connector. Work is via local files, scripts, documented exchange. SolidCraft is geometry only; verification stays with Robot + PyNite/Frame3DD. Python available; vendored pypdf at `.tmp/pylibs`.

## Verification

`python scripts/verificar_todo.py` is the single entry point (30 checks). Run before any handoff or batch document edit. `verificar_alcance_normativo.py` is a regression guard on the verified scope corrections; `documentacion_check.py` enforces the §2-2(3) margin rule across all screening reports.

## State

Fase 0 closed, Fase 1 active, everything R0 conceptual. C-01…C-09 open in `fase1/registro-decisiones.md` and block phase close; collect via `fase1/solicitud-datos.md`. Checklist: `docs/plan-diseno-construccion.md`. The 3,000 kg / 1.2 m beam and the 2,200 kg CSV are **examples, never project data**.

## Knowledge acquisition

Plan `docs/knowledge-acquisition-plan.md`, index `knowledge/INDEX.md`, cards `knowledge/sources/` (S000…S029). Primary sources only; paywalled works recorded as *to acquire*, never copied. **The §1-2(2) admitted scope is fully carded.** One gap: the veiledning for §§2-2, 2-3, 2-4 and 4-2 was never retrieved — never reconstruct it from memory.

## Corrections that must not be lost

All of them are enforced by `verificar_alcance_normativo.py`, which fails if any is lost — read that file rather than this list: §13-1(1) not §13-2; §14-2 not a target (188.9 is not a MiniHouse number); **R 15** not R 30; room height **2.2 m**; **F2 1/200**, **S2 1/1000**; chapter 9 is not noise/water; chapter 15 has no small-building exemption; chapter 16 is lift safety control; §17-1 exempts a småhus by definition.

## The chapter 2 gate

§2-2(1)+(2) read together: **analysis is available only where no number was given.** You can analyse up to a functional requirement, never past a stated performance. Given ytelser are simply met. Analysable: §12-7(2)(d) coverage, §13-1(1) air quality — so the section solver is the formal instrument. Neither: whether the roof is main-system, whether one escape window suffices — those are determinations, and the escape-window one is now **priced** in three readings rather than open (A 0 m², B a 100 mm sill, C 0.29 m²). §2-2(3) demands four things; the margin declaration is the fourth, and **no declared margin is adequate** by its own test (positive *and* larger than its uncertainty) — 0 of 14, with three rows where the uncertainty is wider than the margin and two zero by construction. §2-2(4) is unsatisfied until R2 is chosen.

## Design drivers still open

- **Section**: roof build-up costs t/cos θ, so at 20°/1100 mm stack the eave tops out ~1785 mm and only ~24 % of width reaches 2.2 m. Pitch cap 1.9°–16.3°. Needs C-02 + C-06 together → R2-A/B/C/D undecided.
- **Envelope**: clear-field U passes; at 15 % studs all fail, so the wall needs ~189 mm wool, competing with room height and the 4.00 m transport limit.
- **Thermal bridges**: §14-3 sets **no** limit; the 0.05 W/m²K figure belongs to §14-2's exempt route. Junction inventory **61.10 m** for 18 m² (3.39 m/m²). Ordinary detailing reads 0.210 W/m²K = 4.2× the benchmark and 16 % of heat loss. Compensation is arithmetically open and **geometrically shut** (+53 mm wall, +65 mm roof; the roof share is 69 mm of eave height against a 415 mm deficit). The 0.05 benchmark is **not adoptable at 18 m²** — it implies a mean Ψ of 0.0147 W/mK, under half of good practice. State targets **per metre**. No Ψ calculated; no junction drawn.
- **The junction has now been solved in 2D** (`puente_2d.py`, ISO 10211): the 1D value was
  pessimistic about the steel (0.236 → **0.377**), but the steel stops being the coldest point
  at the **first millimetre of pad** — from 3 mm the timber corner governs, so the requirement
  is **0.80 m²K/W (20 mm), not 0.358 (9 mm)**. **Wrapping** the steel outside the insulation
  gives 0.921 and Ψ +0.027, identical to the bare corner, worth **3.01 W/K** over 18 m (~16 % of
  element loss). Declaration row 13 is **−0.39, sign inverted**, not merely narrowed. A plate is
  not a chassis member, so it is an instrument, not a design value. A parallel perimeter joist
  adds nothing to Ψ once the reference U carries the same timber fraction (0.028 vs 0.027) —
  **a 2D junction model and a parallel-path element U must not count the same joist twice**.
  Full text in the daily log.
- **Condensation at the junction (1D)**: §14-3 caps heat, §13-13 caps vapour, neither covers the
  steel temperature. Bare steel gives f_Rsi **0.236** vs 0.754 required, condensing below
  **5.9 °C** outdoor. Fix has a size: **0.358 m²K/W** of break (~9 mm rigid foam); a 22 mm deck
  alone reaches 0.617. **Mould governs**; the **floor-wall corner** governs. All f_Rsi are
  **1D upper bounds**, so the requirement is a floor.
- **The roof is not blocked**: all four §11-4(3) branches force **A2-s1,d0** insulation, so it is
  mineral wool whatever the scheme — freeze it. **6.2 closed.** Open: rafter + lining; one lining
  answers both. R 15 is **charring**: **48×198 keeps 32 %** of its modulus, parity needs 98 mm
  stock. **The stud fraction is width ÷ centres, not a property** — state width and centres.
- **R2 build-ups corrected**: the options were solved with floor 250 / roof 300, which are round
  numbers — the envelope solver returns **281 / 278** at 15 %. They nearly cancel, so published
  wall heights are ~7 mm optimistic and the real deficit is **−422 mm**. **R2-D's 4400 mm
  dispensation is 22 mm short** (4415 needed at the published build-ups, 4422 at 15 %; 4358 at
  8 %). The timber fraction is the only free lever: R2-B 23→34 %, R2-D 96→100 %.
- **Margins (§2-2(3))**: declared in `fase1/declaracion-de-margenes.md` — one currency per analysis type, thirteen rows with signs: **4 positive, 5 negative, 3 undefined, 1 zero by construction**. Binding component is the section at **−415 mm**; thinnest positive is the **+40 mm** door free width. The project is **short of margin, not of a statement**, because every R2 option was solved *to* 4000 mm — so choosing an option that gives some back is a **regulatory requirement**. The natural-hazard 1.4 factor is **not** a margin on F2/S2 and must not be double-counted.
- **Reclaimed timber (C-08)**: §9-2 has no manufacturer-free route — it is a **testing** question (lead paint, CCA, PCB, asbestos), scoped before purchase. §9-6's 10 t limb is unreachable by the cabin alone; only §9-6(2) aggregation with a **demolition** engages it, so the waste duties apply iff the project includes dismantling a source building.
- **Drainage**: 0.90 m backflow head is a minimum burial depth (≈560 mm at 400 mm floor); shallow sealed-tank fails by 160 mm. Never conflate §15-8(1) 100-year (capacity) with §7-2 1/200 (safety class).
- **Chapter 11 coupling**: §11-13(4) and §11-14 are engaged by the **same** question — safe place
  or rømningsvei — so declaration rows 2/3/4 move together. §11-9 is **not** coupled: a cell with
  no rømningsvei is still a cell, so D-s2,d0 governs and the reclaimed timber stays exposed. Travel
  5.04 m against 15 m, but the risk-class-4 Table 1 row was never retrieved.
- **FDV**: §4-1(2) exemption considered and **rejected** (6 of 6 categories). Must be a versioned file with a site-specific section re-issued per deployment.
- **National Annexes (S014)** are a documentation blocker as well as a design one.
- **Make-up air (`aporte_aire.py`, check 30)**: the hole has a size and does not buy the flue. Orifice law fixes A: **113 mm at 10 Pa** removes 98 Pa of the 106. Row 14 is **retired, not improved** — the only depression passing the §2-2(3) test is 2 Pa, which needs 181 mm and is below a 3 m/s wind's own pressure, so **a passive inlet cannot hold a set pressure**; the conclusion survives dropping the 125 mm limit. A **room-sealed stove** removes the coupling, a specification with no dimensional cost. The make-up air costs **905 W** at 30 K, **1.65×** the fabric loss (18.3 W/K), so heat recovery is a precondition; by diffusion the hole is **0.8 %** of the barrier, so the risk is convective — a **control problem** (closable vapour-tight valve), not a diffusion one. §13-5 driving force falls 106 → 7 Pa (14.9×), which is mitigation, not an assessment.
- **One number, one place**: the envelope element loss is **18.3 W/K**, derived in `aporte_aire.py` from `U_LIMITS` and the reference areas. `puente_2d.py` carried a hand-typed **19.4** (6 % high); it now holds the constant and `aporte_aire`'s self-test crosses the two, because `puente_2d` stays free of project imports on purpose.
