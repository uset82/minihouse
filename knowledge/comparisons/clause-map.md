# EC3 clause-path map for MiniHouse

Status: draft (Stage 2). Sources: S003, S004, S005, S006, S000. Norwegian NA values are **not yet available** — marked PENDING.

## Basis

| Check | Standard | What it governs | NA dependency |
|---|---|---|---|
| Basis of design, combinations | NS-EN 1990 | Persistent / transitory / accidental situations; lifting and assembly as transitory | PENDING — γ, ψ values |
| Actions | NS-EN 1991 | Self-weight, use, snow, wind, transport accelerations | PENDING — snow/wind NA |
| Member resistance | NS-EN 1993-1-1 | Section class, M_Ed ≤ M_Rd, N_Ed ≤ N_b,Rd, N–M interaction | PENDING — γ_M0, γ_M1 |
| Cold-formed members | NS-EN 1993-1-3 | If light-gauge elements used | PENDING |
| Plated elements | NS-EN 1993-1-5 | Plate buckling, stiffeners in ears | PENDING |
| **Joints** | **NS-EN 1993-1-8** | Welds, bolts, bearing, block tearing, plate bending, eccentricity | PENDING |
| Fatigue | NS-EN 1993-1-9 | Only if transport-cycle count justifies it (C-03) | PENDING |
| Timber (if load-bearing) | NS-EN 1995 | Reclaimed wood **only with documented strength** | PENDING |
| Execution | NS-EN 1090-2:2018+A1:2024 | Welding, tolerances, execution class | PENDING — class to agree |
| Reused steel | CEN/TS 1090-201:2024 | Traceability of reclaimed structural steel | guidance document |
| Regulatory frame | TEK17 §10-2 (S005) | Strength, stiffness, stability during execution and final state | direct requirement |

## Key check forms (from S000, to be confirmed against the standards themselves)

- Resistance: M_Ed ≤ M_Rd, with M_Rd built from W · f_y / γ_M depending on section class.
- Buckling: N_Ed ≤ N_b,Rd = χ A f_y / γ_M1, χ from reduced slenderness and buckling curve.
- Joint eccentricity: M_e = F · e.
- Weld groups: distributed force + moment on the actual group geometry; F/(aL) is screening only.
- Torsion: dφ/dx = T/(GJ); warping for open sections (SCI P385, to acquire).

## Deformation limits — four distinct checks (no numeric limit is set yet)

1. Floor deflection
2. Change of aperture diagonal (P-01, V-01…V-03)
3. Differential torsion between corners
4. Local deformation at the lift point

Limits must be fixed **before** Fase 2 calculation and before any test (a-priori criterion, rules.md §5). The controlling limit may be doors/glazing/seals rather than steel stress.

## Gate status

- Clause identification: **done** (S004 part list; S005 TEK17).
- Coefficient values: **BLOCKED** — Norwegian National Annex access pending.
- Clause wording verification: **pending** — need the actual standard texts or authoritative extracts.
