# Autodesk exchange procedure · Robot ↔ Advance Steel (SMLX) and IFC

Status: Stage 7. Procedure prepared; **not yet executed** — no Autodesk product access in this environment (rules.md §14: mark pending, do not assume).

## 0. Before any transfer (mandatory gate)

- [ ] Confirm exact product, version installed, file extension, access permission and tool scope.
- [ ] Record what test was run and what data survived.
- [ ] Without access: prepare this manual sequence and leave the interface marked **pendiente de verificar**.

## 1. Bar test (Robot → Advance Steel via SMLX)

1. Create one bar in Robot with a steel profile, material, local orientation and explicit units.
2. Export SMLX; open in Advance Steel.
3. Open the resulting DWG in the agreed tool.
4. Fill the before/after comparison table:

| Field | Robot before | AS/SMLX after | Match? |
|---|---|---|---|
| Member count | | | |
| Node count | | | |
| Coordinates | | | |
| Local axes orientation | | | |
| Section / family | | | |
| Material | | | |
| Offsets | | | |
| Releases | | | |
| Mass | | | |
| Loads | | | |

Known limit (S000, S003 context): certain geometric adjustments made inside Robot are **not** saved in SMLX. Loads must never be trusted to a round-trip without a difference report.

## 2. IFC coordination check

- Export a coordination IFC from the model.
- Run an IfcOpenShell script to extract, per steel member: GUID, length, profile, material, mass.
- Compare against the analytical-model table; detect silent section changes (e.g. RHS 120×60×5 → other).

## 3. Fabrication outputs (Fase 3, only after sign-off)

- DWG + PDF approved drawings, BOM consistent with drawing revision, NC/DSTV for profiles, DXF for plates.
- Confirm the workshop's DSTV/NC1 version and conventions before issuing machine files.
- Keep neutral records (IFC, DSTV, PDF, DWG, parameter table) because Advance Steel is in maintenance mode.

## 4. SolidCraft role

SolidCraft (free open-source Rust parametric CAD, desktop/browser/CLI, STEP/IGES/STL/3MF/DXF) is used for **geometry exploration** of the R0 model via `scripts/r0_parametric.py` → JSON → import/bridge. It is **not** a structural solver and not a fabrication detailing replacement. Export STEP/IGES for geometry coordination; verification stays with Robot + PyNite/Frame3DD.

## 5. Environment status

No live Autodesk or SolidCraft connector is available here. Work proceeds with local files and scripts. If exports are placed in the project, run sections 1–2 and record results.
