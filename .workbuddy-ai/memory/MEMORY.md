# MiniHouse · long-term notes

**Role.** Lead engineer/designer/CAD (Inge), six AGENTS.md roles. Release, sign-off and lift authority stay with the qualified human (rules.md §5). Never claim code compliance, geotechnical, siting or lift approval.

**Tooling.** Native Fusion MCP endpoint inert; live bridge is FluidBridge/2.0 on 127.0.0.1:7800 (`import_step`, `bodies`, `screenshot`, `export`, `run_project_script` — pass `root` explicitly, default is `drywallcutter`). Fusion data project **MiniHouse Frame R0** holds saved doc `MiniHouse_Frame_R0` (48 bodies, 5 descriptive params). `scripts/ocp_step.py` uses optional cadquery-ocp in `.tmp/ocp` (gitignored) to write Fusion-importable STEP; stdlib writer is fallback only. SolidCraft geometry only; verification: Robot + PyNite/Frame3DD.

**Verification.** `verificar_todo.py` — 37 checks; Fit1 geometry additionally checked in `frame_fit1.py`. `verificar_alcance_normativo.py` is authoritative on scope corrections (**read it, not this file**). documentacion_check.py guards §2-2(3).

**State.** Fase 0 closed, Fase 1 active, all R0 conceptual. C-01…C-09 open (registro-decisiones, solicitud-datos); checklist plan-diseno-construccion. 3,000 kg beam / 2,200 kg CSV = **examples, never project data**.

**Knowledge.** `knowledge/INDEX.md`, S000…S031, primary sources only, paywalled = *to acquire*. **veiledning closed** (S030); **S031 ISO 9972 not held**. Never reconstruct a source from memory.

**The chapter 2 gate.** Analysis only where no number was given; never past a stated performance. §2-2(3) margin only for *extensive analysis*: **9/15 rows**; 4 ytelser, 2 determinations. Adequate = positive **and** larger than its own uncertainty — 0 of 9. A stated ytelse must be met; shortfall needs **dispensation** (PBL ch. 19). **A margin is not a tolerance**: levels are absolute; solving to 4000 mm spends one nobody has. §2-2(4) unmet (R2 basis); ytelsesoversikt: 38 rows, **none discharged**, 0 preaccepted, 21 decisions.

**Open drivers** — derivations live in the daily logs and named scripts:
- **Section**: binding at **−422 mm**; pitch cap 1.9–16.3°; R2-A/C survive a 100 mm reserve, R2-D needs 4422.
- **Envelope**: clear-field U passes, 15 % studs fail; wall needs ~189 mm wool. Element loss **18.3 W/K**, held in `puente_2d.py`.
- **Junction**: 2D steel 0.377 not 0.236; **wrapping** 0.921, Ψ +0.027 — drawing instruction. Barrier turns (13, −22); plate unwrapped.
- **Make-up air**: 113 mm at 10 Pa; passive inlet cannot hold pressure, so **row 14 retired by specification** (room-sealed stove).
- **Radon**: C ≤ E/Q gives 3.6–36 Bq/m³ vs 200; **alum shale breaks it** — C-01 decides. The void is a buffer, do not seal it.
- **Airtightness**: 1.5 h⁻¹ = q50 0.83 at A/V 1.80; target **1.30**, acceptance 1.36; below **1.19** the extract stalls. No measurement.
- **Margins**: **2 positive / 7 negative / 4 undefined / 2 zero** — short of margin, not of a statement.
- **Woven joint**: cycle **1→2→3→4→1**; no rigid order, ply 4 threads. Article **150×150×9.5 mm** (A1 mini), 53 mm wrench spare; STL/3MF/STEP generated, **not printed**; STEP = **32 bodies in Fusion 2706.1.17**; no strength/grade/EXC claim, thermal junction re-opened (check 35).
- **Frame model**: 6×3 m frame, four numbered U-channels with fins for sandwich wall, 4 crossmembers @1200. Plan **1:40** = 150×75 mm (A1 mini), section **not to scale**, 5.6 mm wall slot. `frame_model.py`, check 36; STL/3MF/STEP, **not printed**. STEP = **48 bodies in Fusion**, bbox 150×75×12 mm; `frame.f3d` native archive exported. R0 right rail was misplaced; do not print as proof of fit (§AL). Current rectangular bench model **MiniHouse_Frame_Fit1**, native 8 bodies, four M6 corners, rail 4 slides in without bolts, A1 mini plate in `fase1/prototipo/marco-fit1`; not physically tested. Combined 67-body R0 coupon also superseded for fit (pocket/notch defects).
