# Weave-closure options for the MiniHouse base frame — R0 research note

**Status:** CONCEPTUAL — NOT FOR FABRICATION. Date: 2026-11-19.
**Question:** four numbered perimeter members interlace 1→2→3→4→1. Four rigid
members cannot be lowered into that closed cycle (`vertical_order()` returns
`None`). Which closure lets a bolted, printed joint article be assembled while
still looking like the sketches?

The folded-paper sketch proves the *shape*, not the assembly: paper bends. The
existing flat-bar coupon relies on ply 4 flexing last (`THREAD_PLY = 4`). Adding
two upstanding fins to each member makes that strip much stiffer, so the
combined article should not depend on flex alone.

## Criteria

| Criterion | Test applied here |
|---|---|
| Assembly feasibility | Can rigid steel members be placed without bending? Does the printed article need only a small elastic deflection? |
| Bolt / wrench access | Ø6.4 hole and Ø20 × 5.5 mm nut seat at every lap; Ø24 × 18 mm wrench keep-out must stay clear, fins included. |
| Parts and hardware | Extra bodies beyond the four numbered members; extra bolts or plates. |
| Thermal bridge | State the consequence only. The woven base **re-opens** the junction; the earlier wrapped-steel Ψ +0.027 is **not** inherited. |
| Fidelity to sketch | Four numbered members, visible over/under at corners, two fins with the wall between them. |
| Printability | Fits 180³ A1 mini; no printed M6 threads, no support-dependent features, no sub-nozzle tiny fins. |

## Options compared

| Option | Assembly | Wrench / bolts | Extra parts | Thermal | Sketch fidelity | Printability | R0 verdict |
|---|---|---|---|---|---|---|---|
| **Split lap** — one member split at one corner into two overlapping tongues, bolted through the crossing member | Opens the cycle; other three stay rigid; small deflection at the split only | Four corner bolts kept; keep-out can be reserved on the flat pad before fins resume | None beyond the four numbered members (two tongues are one member in the print file) | Steel-to-steel lap remains; not resolved here | Highest: still four numbered members and four visible laps | Good: split is a geometry change, no new hardware | **Chosen** |
| **Removable closure plate** — one corner closed by a fifth bolted plate | Opens the cycle with rigid bars | Plate adds a stack and may need a second wrench side | One plate (+ bolts) | Extra steel at the corner; not resolved | Visible extra plate at one corner | Good, but more bodies and alignment | Runner-up |
| **Slotted joint** — one member has a long bolt slot that lets it slide into place | Opens the cycle by translation | Bolt can be tightened after sliding; slot weakens the member and invites movement | None | Same lap steel | Over/under still visible but slot changes the sketch line | Long slot may print oval and loose at 0.4 mm nozzle | Not chosen |
| **Welded corner** | Removes the bolted-lap question entirely | No bolt access issue | Adds weld/execution-class decisions | Different junction; still not qualified | Loses the "bolted like hands" intent | Not a printed-joint test | **Excluded from R0 scope**, not judged on engineering merit |

## Decision

Adopt the **split lap** for the combined R0 test article. It is the only option
that opens the closed precedence cycle without adding a fifth body, without
weakening a member with a long slot, and without abandoning the bolted-lap
question the sketch asks about. It does **not** prove steel assembly: the real
steel split, bolt class, preload and execution class remain undefined and are
outside this project's authority.

## Sources and limits

- Project derivation only: `scripts/bolted_lap_prototype.py` and
  `scripts/frame_model.py` both return no topological order for the cycle
  `[1, 2, 3, 4, 1]`. This is mathematics of the chosen graph, not a code claim.
- S030 (DIBK veiledning, held, explicitly guidance and not binding) supports
  treating testing as a legitimate documentation route; it gives no connection
  detail and no numbers used here.
- S014 (National Annex), S019 (NS-EN 1090-2), S006 (EC3 joint guide) and S031
  (ISO 9972) are **not held**. No clause number, bolt class, EXC, weld procedure
  or capacity is quoted. The comparisons above are design heuristics for a
  printed mock-up, not sourced engineering rules.
- No printed measurement exists yet. The article tests assembly sequence, fit,
  wrench access and the visible weave — and only after it is actually printed.
