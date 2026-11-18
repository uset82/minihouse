# MiniHouse · long-term notes

**Role.** Agent = lead engineer / designer / CAD (Inge), the six AGENTS.md roles (Carlos, 2026-11-16). Fabrication release, structural sign-off and lift authorisation stay with the qualified human authority (rules.md §5). Never claim code compliance, geotechnical assessment, siting approval or lift authorisation.

**Tooling.** No live Autodesk/SolidCraft connector: local files and scripts. SolidCraft is geometry only; verification: Robot + PyNite/Frame3DD.

**Verification.** `python scripts/verificar_todo.py` — 34 checks, run before any handoff. `verificar_alcance_normativo.py` is the authoritative record of the scope corrections; **read that file, not this one**. `documentacion_check.py` enforces §2-2(3) across the 15 screening reports.

**State.** Fase 0 closed, Fase 1 active, all R0 conceptual. C-01…C-09 open (`fase1/registro-decisiones.md`, `solicitud-datos.md`); checklist `docs/plan-diseno-construccion.md`. The 3,000 kg beam and 2,200 kg CSV are **examples, never project data**.

**Knowledge.** `knowledge/INDEX.md`, cards S000…S031, primary sources only, paywalled works recorded *to acquire*. The §1-2(2) admitted scope is fully carded, the **veiledning gap is closed** (S030); **S031 (ISO 9972) is not held**. Never reconstruct a source from memory.

**The chapter 2 gate.** Analysis only where no number was given — up to a functional requirement, never past a stated performance. A §2-2(3) margin is required only for a *more extensive analysis*: **9 of 15 rows**; four are stated ytelser, two determinations. Adequate = positive **and** larger than its own uncertainty — 0 of 9. A stated ytelse must be met; a shortfall needs **dispensation** (PBL ch. 19), stricter. **A margin is not a tolerance**: levels are absolute unless granted, so solving to 4000 mm spends one nobody has. §2-2(4) unsatisfied (R2 produces the basis); the **ytelsesoversikt** exists: 38 rows, **none discharged**, 0 preaccepted, 21 decisions, 17 closing one.

**Open drivers** — derivations live in the daily logs and named scripts:
- **Section**: binding at **−422 mm**; pitch cap 1.9–16.3°; R2-A/C survive a 100 mm reserve, R2-D needs 4422.
- **Envelope**: clear-field U passes, 15 % studs fail; wall needs ~189 mm wool. Element loss **18.3 W/K**, held in `puente_2d.py`.
- **Junction**: 2D: steel 0.377 not 0.236; **wrapping** gives 0.921 and Ψ +0.027 — a drawing instruction, not a thickness. Barrier turns at (13, −22); plate crosses it unwrapped.
- **Make-up air**: 113 mm at 10 Pa; a passive inlet cannot hold a pressure, so **row 14 is retired by specification** (room-sealed stove).
- **Radon**: C ≤ E/Q gives 3.6–36 Bq/m³ vs 200; **alum shale breaks it** — C-01 decides. The void is a buffer, do not seal it.
- **Airtightness**: 1.5 h⁻¹ = q50 0.83 at A/V 1.80; target **1.30**, acceptance 1.36; below **1.19** the extract stalls. No measurement.
- **Margins**: **2 positive / 7 negative / 4 undefined / 2 zero** — short of margin, not of a statement.
