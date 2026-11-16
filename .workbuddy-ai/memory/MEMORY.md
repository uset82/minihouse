# MiniHouse · long-term project notes

## Agent role

Agent acts as the single lead responsible engineer / designer / CAD expert (name: Inge), covering all six specialist roles in AGENTS.md. Assigned by Carlos 2026-11-16. Engineering deliverables are produced by the agent; fabrication release, structural sign-off and authorisation of real lifts stay with the qualified human authority (rules.md §5).

## Tooling reality

- Autodesk (Robot, Revit, Advance Steel, AutoCAD, Forma) and SolidCraft have no live connector here. Work is via local files, scripts, and documented exchange procedures.
- SolidCraft = open-source Rust parametric 3D CAD, browser/desktop/CLI, AI/MCP-control, STEP/IGES/STL/3MF/DXF. For geometry only; verification stays with Robot + PyNite/Frame3DD, fabrication with Advance Steel.
- Python available; vendored pypdf at `.tmp/pylibs` for PDF extraction.

## Knowledge acquisition

Long-term plan at `docs/knowledge-acquisition-plan.md`; living index at `knowledge/INDEX.md`. PhD-level defined as 5 abilities with pass gates (derive, navigate codes, critique sources, verify numerically, synthesise decisions). Execute stages in order: foundations → EC3/codes → modular+connections → lifting/transport → architecture/building physics → Norwegian regulation → tooling → synthesis. Sources are captured as cards in `knowledge/sources/`. Primary sources only; paywalled works recorded as *to acquire*, never copied unlawfully. Baseline report registered as S000.

## State

Fase 0 closed; Fase 1 active. Everything to date is R0 conceptual. Open questions C-01…C-09 (fase1/registro-decisiones.md) block phase close. Never treat the 3,000 kg / 1.2 m beam example as real module data. Detailed operational checklist is `docs/plan-diseno-construccion.md`; it maps ChatGPT's six design/construction phases into canonical Fase 0–4 and preserves the Bergen/emergency-cabin and gable-roof intent. Use `fase1/solicitud-datos.md` to collect C-01…C-09. `fase1/r1-opciones-techo.md` + `knowledge/comparisons/r1-gable-options.json` are non-selecting gable-pitch sensitivity outputs; R0 remains the historical coordinate frame.
