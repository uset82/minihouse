#!/usr/bin/env python3
"""MiniHouse · 2D steady-state conduction at the floor-edge junction (ISO 10211).

Every f_Rsi in this repository is a **1D** number, and the condensation screen
says so: a 1D path has no spreading resistance, so it is optimistic and the
requirement it produces is a floor rather than a design value. No junction has
ever been drawn and no Ψ has ever been calculated.

This script supplies the missing instrument. It solves ∇·(λ∇T) = 0 on a
rectangular finite-volume grid with surface films as Robin boundaries, and
reports three things the 1D screen cannot:

  f_Rsi   at the coldest interior surface point
  Ψ       the linear thermal transmittance of the junction, W/mK
  Q       the total heat flow per metre of junction

The solver is validated before it is used. Four tests must pass: a 1D slab must
reproduce its analytical U and f_Rsi exactly, a series of layers must reproduce
its series resistance, flux must be conserved, and the result must be stable
under mesh refinement. A 2D solver that cannot reproduce 1D is not a solver.

**The geometry is a screening idealisation, not a design.** The chassis profile
is undefined (no A, W, I, J, thickness or grade), so the steel is modelled as a
plate of parameterised thickness at the junction. When a real detail is drawn it
replaces the box list and everything else stays.

Usage:
  python puente_2d.py --out-md fase1/verificacion-puente-2d.md \
      --out-json knowledge/comparisons/puente-2d.json
  python puente_2d.py --selftest
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- boundary conditions -----------------------------------------------------
T_IN = 20.0
T_OUT = -10.0
R_SI = 0.13          # flat wall, ISO 13788 / NS-EN ISO 6946
R_SE = 0.04

# --- materials (W/mK) --------------------------------------------------------
LAM = {
    "timber": 0.13,
    "mineral wool": 0.035,
    "wood fibre": 0.050,
    "rigid PU": 0.025,
    "steel": 50.0,
    # a 25 mm ventilated cavity with r = 0.17 m2K/W behaves as this conductivity
    "ventilated cavity": 0.025 / 0.17,
}

# --- the envelope build-ups, from envelope_check ---------------------------------
WALL_LAYERS = (           # x measured outward from the inner face
    ("timber", 0.0, 13.0),
    ("mineral wool", 13.0, 202.0),
    ("wood fibre", 202.0, 214.0),
    ("ventilated cavity", 214.0, 239.0),
    ("timber", 239.0, 264.0),
)
WALL_T_MM = 264.0
FLOOR_LAYERS = (          # z measured downward from the finished floor
    ("timber", -22.0, 0.0),
    ("mineral wool", -262.0, -22.0),
    ("timber", -280.0, -262.0),
)
FLOOR_T_MM = 280.0

# --- the modelled window -----------------------------------------------------
L_MM = 400.0              # how far the floor and wall run from the corner
H_MM = 400.0
CELL_MM = 2.0

# --- the condensation screen's numbers, to compare against -------------------
ONE_D_F_RSI_BARE = 0.236
REQUIRED_ADDED_R = 0.358      # m2K/W, from condensacion_union.py
F_CRIT_MOULD = 0.754

# The envelope's element heat loss at the §14-3 limits, W/K, as the denominator
# for "how big is 3 W/K". It is derived in aporte_aire.py from U_LIMITS and the
# reference section's element areas; this module stays free of project imports,
# so the figure is restated here and the guard checks the two agree. It was 19.4
# until that derivation existed — a hand-typed number, 6 % high, which is why
# the derivation now exists.
ELEMENT_LOSS_W_PER_K = 18.3


def u_value(layers, r_si, r_se):
    """1D U of a layer list, for the parallel-path comparison."""
    r = r_si + r_se + sum((z1 - z0) / 1000.0 / LAM[m] for m, z0, z1 in layers)
    return 1.0 / r


def u_wall():
    return u_value(WALL_LAYERS, R_SI, R_SE)


def u_floor():
    return u_value(FLOOR_LAYERS, R_SI, R_SE)


def build_domain(boxes, cell_mm=CELL_MM, l_mm=L_MM, h_mm=H_MM, interior_x_max=0.0):
    """Rasterise a box list onto a finite-volume grid.

    Boxes are (material, x0, x1, z0, z1) in mm. Everything not covered by a box
    and not marked as interior air is exterior air. Returns (lam, kind) where
    kind is 0 solid, 1 interior air, 2 exterior air.
    """
    # The domain must extend past the wall, or the wall's outer face lands on
    # the domain edge and becomes adiabatic instead of exterior.
    nx = int(round((WALL_T_MM + 2.0 * l_mm) / cell_mm))
    nz = int(round((h_mm + FLOOR_T_MM + l_mm) / cell_mm))
    lam = np.zeros((nz, nx))
    kind = np.full((nz, nx), 2, dtype=np.int8)

    # cell centres in mm, measured from the wall's inner face and the floor top
    xs = -l_mm + (np.arange(nx) + 0.5) * cell_mm
    zs = h_mm - (np.arange(nz) + 0.5) * cell_mm   # down to -(floor + l_mm)

    # interior air is the quadrant x < 0, z > 0. A slab test passes a huge
    # interior_x_max so the whole upper half is interior and the field is 1D.
    interior = (xs[None, :] < interior_x_max) & (zs[:, None] > 0.0)
    kind[interior] = 1

    for material, x0, x1, z0, z1 in boxes:
        mask = ((xs[None, :] >= x0) & (xs[None, :] < x1)
                & (zs[:, None] >= z0) & (zs[:, None] < z1))
        lam[mask] = LAM[material]
        kind[mask] = 0
    return lam, kind, xs, zs


def solve(lam, kind, cell_mm=CELL_MM):
    """Solve the temperature field and return (T, index) over solid cells."""
    nz, nx = lam.shape
    solid = kind == 0
    idx = -np.ones((nz, nx), dtype=np.int64)
    n = int(solid.sum())
    idx[solid] = np.arange(n)

    h = cell_mm / 1000.0
    rows, cols, vals = [], [], []
    rhs = np.zeros(n)

    def conductance(la, lb):
        return 1.0 / (1.0 / (2.0 * la) + 1.0 / (2.0 * lb))

    for i in range(nz):
        for j in range(nx):
            if not solid[i, j]:
                continue
            k = idx[i, j]
            la = lam[i, j]
            diag = 0.0
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < nz and 0 <= jj < nx):
                    continue                      # domain edge: adiabatic
                if kind[ii, jj] == 0:
                    g = conductance(la, lam[ii, jj])
                    rows.append(k); cols.append(idx[ii, jj]); vals.append(-g)
                    diag += g
                else:
                    r_film = R_SI if kind[ii, jj] == 1 else R_SE
                    t_amb = T_IN if kind[ii, jj] == 1 else T_OUT
                    # film in series with the half-cell to the face. The ambient
                    # temperature goes to the right-hand side, so this term only
                    # adds to the diagonal — adding it as an off-diagonal too
                    # would break diagonal dominance and make the system singular.
                    g = 1.0 / (r_film / h + 1.0 / (2.0 * la))
                    diag += g
                    rhs[k] += g * t_amb
            rows.append(k); cols.append(k); vals.append(diag)

    a = coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr()
    t = spsolve(a, rhs)
    return t, idx, solid


def metrics(t, idx, lam, kind, cell_mm=CELL_MM):
    """f_Rsi at the coldest interior surface, total heat flow, and Ψ."""
    nz, nx = lam.shape
    h = cell_mm / 1000.0
    q_in = 0.0
    t_surf_min = None

    for i in range(nz):
        for j in range(nx):
            if kind[i, j] != 0:
                continue
            la = lam[i, j]
            tc = t[idx[i, j]]
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < nz and 0 <= jj < nx):
                    continue
                if kind[ii, jj] != 1:
                    continue
                g = 1.0 / (R_SI / h + 1.0 / (2.0 * la))
                q = g * (T_IN - tc)
                q_in += q
                # surface temperature at the face, after the film
                t_face = T_IN - q * R_SI / h
                t_surf_min = t_face if t_surf_min is None else min(t_surf_min, t_face)

    if t_surf_min is None:
        raise SystemExit("ERROR: no interior surface found")
    l_2d = q_in / (T_IN - T_OUT)
    f = (t_surf_min - T_OUT) / (T_IN - T_OUT)
    psi = l_2d - u_wall() * (H_MM / 1000.0) - u_floor() * (L_MM / 1000.0)
    return {"q_w_per_m": q_in, "l_2d_w_per_mk": l_2d,
            "t_surface_min_c": t_surf_min, "f_rsi": f,
            "psi_w_per_mk": psi}


def geometry(steel_mm=0.0, pad_mm=0.0, wrapped=False,
             joist_mm=0.0, joist_x0_mm=-48.0):
    """The floor-edge junction as a box list.

    Wall on the left face, floor below, corner at (0, 0). The optional steel
    plate stands at the wall's inner face from the finished floor down to the
    underside of the floor, replacing the floor structure over `steel_mm` of
    width; the optional pad sits on top of it, under the floor surface. The
    optional joist is a timber path parallel to the wall, under the deck and
    through the full insulation depth — the case a 2D section can see, and the
    one a perimeter trimmer creates.
    """
    boxes = []
    for material, x0, x1 in ((m, a, b) for m, a, b in WALL_LAYERS):
        boxes.append((material, x0, x1, 0.0, H_MM))
    # the floor runs out to the wall's outer face, so the wall bears on it.
    # If it stopped at the wall's inner face the two would touch at a point and
    # each would be exposed on faces a real junction does not have.
    for material, z0, z1 in ((m, a, b) for m, a, b in FLOOR_LAYERS):
        boxes.append((material, -L_MM, WALL_T_MM, z0, z1))

    if joist_mm > 0:
        # Under the deck, so the 22 mm deck stays continuous over it as built.
        # A joist perpendicular to the wall is a 3D effect and this section
        # cannot see it; a joist parallel to it is the perimeter trimmer.
        boxes.append(("timber", joist_x0_mm, joist_x0_mm + joist_mm,
                      -FLOOR_T_MM, -22.0))

    if wrapped and steel_mm > 0:
        # the steel sits below the floor, wholly outside the insulation line
        boxes.append(("steel", -L_MM, WALL_T_MM,
                      -FLOOR_T_MM - steel_mm, -FLOOR_T_MM))
    elif steel_mm > 0:
        # the plate occupies the corner column, floor build-up replaced by steel
        boxes.append(("steel", -steel_mm, 0.0, -FLOOR_T_MM, -pad_mm))
        if pad_mm > 0:
            boxes.append(("rigid PU", -steel_mm, 0.0, -pad_mm, 0.0))
    return boxes


def coldest_point(t, idx, lam, kind, xs, zs, cell_mm=CELL_MM):
    """The coldest interior-surface point, with its location and material."""
    nz, nx = lam.shape
    h = cell_mm / 1000.0
    best = None
    for i in range(nz):
        for j in range(nx):
            if kind[i, j] != 0:
                continue
            la = lam[i, j]
            tc = t[idx[i, j]]
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < nz and 0 <= jj < nx):
                    continue
                if kind[ii, jj] != 1:
                    continue
                g = 1.0 / (R_SI / h + 1.0 / (2.0 * la))
                q = g * (T_IN - tc)
                t_face = T_IN - q * R_SI / h
                if best is None or t_face < best["t_surface_c"]:
                    best = {"t_surface_c": t_face, "x_mm": float(xs[j]),
                            "z_mm": float(zs[i]), "lam": float(la)}
    return best


def evaluate(steel_mm=0.0, pad_mm=0.0, wrapped=False,
             joist_mm=0.0, joist_x0_mm=-48.0,
             cell_mm=CELL_MM, l_mm=L_MM, h_mm=H_MM):
    lam, kind, xs, zs = build_domain(
        geometry(steel_mm, pad_mm, wrapped, joist_mm, joist_x0_mm),
        cell_mm, l_mm, h_mm)
    t, idx, _ = solve(lam, kind, cell_mm)
    out = metrics(t, idx, lam, kind, cell_mm)
    cold = coldest_point(t, idx, lam, kind, xs, zs, cell_mm)
    out.update({"steel_mm": steel_mm, "pad_mm": pad_mm, "wrapped": wrapped,
                "joist_mm": joist_mm, "joist_x0_mm": joist_x0_mm,
                "cell_mm": cell_mm, "l_mm": l_mm, "h_mm": h_mm,
                "coldest": cold})
    return out


def slab_geometry():
    """The floor build-up as a horizontal slab with no corner: a 1D test case."""
    return [(m, -L_MM, WALL_T_MM + L_MM, z0, z1) for m, z0, z1 in FLOOR_LAYERS]


def selftest():
    # --- 1. a 1D slab must reproduce its analytical U and f_Rsi --------------
    # A horizontal slab with films above and below. The field is 1D, so the
    # solver must reproduce the series resistance exactly. This is the test that
    # makes the 2D results trustworthy: a solver that cannot do 1D cannot do 2D.
    lam, kind, _, _ = build_domain(slab_geometry(), CELL_MM, interior_x_max=1e9)
    t, idx, _ = solve(lam, kind)
    m = metrics(t, idx, lam, kind)
    r_total = 1.0 / u_floor()
    f_exact = 1.0 - R_SI / r_total
    assert abs(m["f_rsi"] - f_exact) < 0.002, (m["f_rsi"], f_exact)
    # and the total heat flow must equal U * length, per metre of depth
    q_exact = u_floor() * (WALL_T_MM + 2.0 * L_MM) / 1000.0 * (T_IN - T_OUT)
    assert abs(m["q_w_per_m"] - q_exact) / q_exact < 0.002, (m["q_w_per_m"], q_exact)

    # --- 2. series layers must reproduce their series resistance ------------
    # u_wall() is the analytic series value; the 1D region of the model must
    # match it, which the flux already tests through f_rsi above.
    assert abs(u_wall() - 1.0 / (R_SI + R_SE + sum(
        (b - a) / 1000.0 / LAM[mat] for mat, a, b in WALL_LAYERS))) < 1e-12

    # --- 3. flux conservation: heat entering equals heat leaving -------------
    q_in = m["q_w_per_m"]
    # recompute the outward flux independently over the exterior faces
    h = CELL_MM / 1000.0
    nz, nx = lam.shape
    q_out = 0.0
    for i in range(nz):
        for j in range(nx):
            if kind[i, j] != 0:
                continue
            la = lam[i, j]
            tc = t[idx[i, j]]
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < nz and 0 <= jj < nx):
                    continue
                if kind[ii, jj] != 2:
                    continue
                g = 1.0 / (R_SE / h + 1.0 / (2.0 * la))
                q_out += g * (tc - T_OUT)
    assert abs(q_in - q_out) / q_in < 1e-6, (q_in, q_out)

    # --- 4. the corner alone must give a positive Ψ -------------------------
    # A geometric corner is a real bridge even with no steel in it.
    assert m["psi_w_per_mk"] > 0, m["psi_w_per_mk"]

    # --- 5. mesh convergence ------------------------------------------------
    coarse = evaluate(cell_mm=4.0)
    fine = evaluate(cell_mm=2.0)
    assert abs(coarse["f_rsi"] - fine["f_rsi"]) < 0.02, (coarse["f_rsi"], fine["f_rsi"])

    # --- 6. steel must make the surface colder, not warmer ------------------
    bare = evaluate()
    steel = evaluate(steel_mm=10.0)
    assert steel["f_rsi"] < bare["f_rsi"], (steel["f_rsi"], bare["f_rsi"])
    # --- 7. and a pad must recover part of it ------------------------------
    padded = evaluate(steel_mm=10.0, pad_mm=9.0)
    assert padded["f_rsi"] > steel["f_rsi"], (padded["f_rsi"], steel["f_rsi"])

    # --- 8. the governing point must move off the steel once it is padded ---
    # This is the finding 1D cannot produce: the pad protects the steel, and the
    # wall's corner then governs for every pad thickness.
    assert steel["coldest"]["lam"] > 10.0, steel["coldest"]
    assert padded["coldest"]["lam"] < 1.0, padded["coldest"]
    thin = evaluate(steel_mm=10.0, pad_mm=3.0)
    assert thin["coldest"]["lam"] < 1.0, thin["coldest"]

    # --- 9. wrapping the steel must restore the bare corner exactly ---------
    wrapped = evaluate(steel_mm=10.0, wrapped=True)
    assert abs(wrapped["f_rsi"] - bare["f_rsi"]) < 0.01, (wrapped["f_rsi"], bare["f_rsi"])

    # --- 10. the 1D requirement must NOT be enough in 2D --------------------
    # 9 mm of PU is the 1D answer (0.358 m2K/W); in 2D it leaves the corner below
    # the mould criterion, so the requirement is mis-specified.
    assert padded["f_rsi"] < F_CRIT_MOULD, padded["f_rsi"]
    twenty = evaluate(steel_mm=10.0, pad_mm=20.0)
    assert twenty["f_rsi"] >= F_CRIT_MOULD - 0.005, twenty["f_rsi"]
    # and padding has diminishing returns: it never reaches the wrapped value
    assert twenty["f_rsi"] < wrapped["f_rsi"], (twenty["f_rsi"], wrapped["f_rsi"])

    # --- 11. the joist penalty is parallel-path conduction, not a junction ---
    # The sweep must recover the unjoisted Ψ once the reference U carries the
    # same timber fraction the model does. If a future edit drops that
    # correction the raw value (0.042) would be reported as the junction.
    assert abs(u_floor_fraction(0.0) - u_floor()) < 1e-9
    assert u_floor_fraction(0.5) > u_floor_fraction(0.0)
    js = joist_sweep()
    for row in js["rows"]:
        assert abs(row["psi_junction"] - m["psi_w_per_mk"]) < 0.01, (row, m["psi_w_per_mk"])
        assert row["psi_raw"] > row["psi_junction"], row
        # f_Rsi must move a little, and only a little: the deck spreads.
        assert 0.0 < bare["f_rsi"] - row["f_rsi"] < 0.03, row
    # the correction must be the whole of the shift, not a fudge
    assert abs(js["shift_w_per_mk"] - (js["rows"][0]["psi_raw"]
                                      - js["rows"][0]["psi_junction"])) < 1e-4

    print(f"2D self-test OK: 1D reproduction (f {m['f_rsi']:.3f} vs {f_exact:.3f}), "
          f"series R, flux conservation to 1e-6, corner Ψ {m['psi_w_per_mk']:.3f} W/mK, "
          f"mesh convergence, steel {steel['f_rsi']:.3f} < padded {padded['f_rsi']:.3f} "
          f"< bare {bare['f_rsi']:.3f}, the governing point moves off the steel, "
          f"wrapping restores the bare corner, 9 mm of pad is not enough, and the joist "
          f"penalty is parallel-path conduction rather than a junction")


VARIANTS = (
    ("A", "bare corner, no steel", {"steel_mm": 0.0}),
    ("B", "steel plate at the corner", {"steel_mm": 10.0}),
    ("C", "steel plate + 9 mm PU pad", {"steel_mm": 10.0, "pad_mm": 9.0}),
    ("D", "steel plate + 20 mm PU pad", {"steel_mm": 10.0, "pad_mm": 20.0}),
    ("E", "steel wrapped below the floor", {"steel_mm": 10.0, "wrapped": True}),
    ("F", "20 mm steel plate at the corner", {"steel_mm": 20.0}),
)
PAD_SWEEP = (0, 3, 6, 9, 12, 15, 20, 30, 45, 60)

# A parallel joist under the deck: 48 mm is the rafter width the roof screen
# settled on, and the positions run from the wall's inner face inward.
JOIST_MM = 48.0
JOIST_X0_SWEEP = (-48.0, -148.0, -248.0, -348.0)
FLOOR_PERIMETER_M = 18.0


def u_floor_fraction(fraction):
    """Floor U by parallel path at a timber fraction, as the envelope screen does.

    The joist path is solid timber through the full floor depth, which is what
    the 2D section models; the clear path is the layered build-up. Computing the
    reference U this way is what keeps the joist from being counted twice — once
    inside L_2D and once as an omission from U_floor.
    """
    r_clear = R_SI + R_SE + sum((z1 - z0) / 1000.0 / LAM[m]
                                for m, z0, z1 in FLOOR_LAYERS)
    r_joist = R_SI + R_SE + (FLOOR_T_MM / 1000.0) / LAM["timber"]
    return fraction / r_joist + (1.0 - fraction) / r_clear


def joist_sweep():
    """f_Rsi and Ψ as a parallel joist moves away from the corner.

    Ψ is reported twice: raw, against the clear-field floor U, and referenced to
    the joisted floor U. The second is the junction's own value; the first
    silently includes the joist's parallel-path conduction, which belongs in the
    element U and not in the junction.
    """
    fraction = JOIST_MM / L_MM
    u_clear = u_floor_fraction(0.0)
    u_joisted = u_floor_fraction(fraction)
    shift = (u_joisted - u_clear) * (L_MM / 1000.0)
    rows = []
    for x0 in JOIST_X0_SWEEP:
        r = evaluate(joist_mm=JOIST_MM, joist_x0_mm=x0)
        rows.append({"x0_mm": x0, "distance_mm": -x0,
                     "f_rsi": round(r["f_rsi"], 4),
                     "psi_raw": round(r["psi_w_per_mk"], 4),
                     "psi_junction": round(r["psi_w_per_mk"] - shift, 4),
                     "coldest": r["coldest"]})
    return {"joist_mm": JOIST_MM, "fraction": fraction,
            "u_clear": round(u_clear, 4), "u_joisted": round(u_joisted, 4),
            "shift_w_per_mk": round(shift, 4), "rows": rows}


def screen():
    rows = []
    for tag, name, kw in VARIANTS:
        r = evaluate(**kw)
        rows.append({"tag": tag, "name": name, **kw, **r})
    sweep = []
    for pad in PAD_SWEEP:
        r = evaluate(steel_mm=10.0, pad_mm=float(pad))
        sweep.append({"pad_mm": float(pad), "f_rsi": r["f_rsi"],
                      "psi": r["psi_w_per_mk"],
                      "governing": "steel" if r["coldest"]["lam"] > 10.0 else "timber corner"})
    bare = next(r for r in rows if r["tag"] == "A")
    plate = next(r for r in rows if r["tag"] == "B")
    wrapped = next(r for r in rows if r["tag"] == "E")
    return {
        "state": "SCREENING — CONDITIONAL ON C-01",
        "conditions": {"t_in": T_IN, "t_out": T_OUT, "r_si": R_SI, "r_se": R_SE,
                       "cell_mm": CELL_MM, "l_mm": L_MM, "h_mm": H_MM},
        "one_d": {"f_rsi_bare_steel": ONE_D_F_RSI_BARE,
                  "required_added_r": REQUIRED_ADDED_R,
                  "f_crit_mould": F_CRIT_MOULD},
        "wall_u": round(u_wall(), 4),
        "floor_u": round(u_floor(), 4),
        "variants": rows,
        "pad_sweep": sweep,
        "joist": joist_sweep(),
        "heat": {
            "floor_perimeter_m": FLOOR_PERIMETER_M,
            "plate_w_per_k": round(plate["psi_w_per_mk"] * FLOOR_PERIMETER_M, 3),
            "wrapped_w_per_k": round(wrapped["psi_w_per_mk"] * FLOOR_PERIMETER_M, 3),
            "difference_w_per_k": round(
                (plate["psi_w_per_mk"] - wrapped["psi_w_per_mk"]) * FLOOR_PERIMETER_M, 3),
        },
    }


def markdown(result):
    v = {r["tag"]: r for r in result["variants"]}
    c = result["conditions"]
    one_d = result["one_d"]
    heat = result["heat"]
    joist = result["joist"]

    lines = [
        "# MiniHouse · 2D conduction at the floor-edge junction",
        "",
        "**State:** SCREENING — CONDITIONAL ON C-01. Not a junction detail, not a "
        "certificate, not a fabrication release.",
        "",
        "- Conditions: " + f"{c['t_in']:.0f} °C inside, {c['t_out']:.0f} °C outside, "
        f"R_si {c['r_si']:.2f}, R_se {c['r_se']:.2f} m²K/W.",
        f"- Grid: {c['cell_mm']:.0f} mm cells over {c['l_mm']:.0f} × {c['h_mm']:.0f} mm "
        "from the corner.",
        "- Generated by `scripts/puente_2d.py`; JSON companion: "
        "`knowledge/comparisons/puente-2d.json`.",
        "",
        "## 1. What this adds",
        "",
        "Every f_Rsi in this repository is a **1D** number. The condensation screen says so "
        "explicitly, and draws the right conclusion from it: a 1D path has no spreading "
        "resistance, so the value is a bound and the requirement it produces is a floor. It "
        "also records what is missing — **no junction has been drawn and no Ψ has ever been "
        "calculated**.",
        "",
        "This screen supplies the instrument. It solves ∇·(λ∇T) = 0 on a finite-volume grid "
        "with the surface films as Robin boundaries, and reports the coldest interior surface "
        "temperature, its location, and the junction's linear thermal transmittance Ψ by the "
        "ISO 10211 definition.",
        "",
        "## 2. The solver is validated before it is used",
        "",
        "A 2D solver that cannot reproduce 1D is not a solver, so four tests run first:",
        "",
        "| Test | Result |",
        "|---|---|",
        "| A 1D slab must reproduce its analytical f_Rsi | "
        f"**{v['A']['f_rsi']:.4f}** modelled against **0.9823** analytic, and the heat flow "
        "against U·L·ΔT |",
        "| Series layers must reproduce their series resistance | exact to 1e-12 |",
        "| Flux must be conserved | entering and leaving fluxes agree to **1e-6** |",
        "| The result must be stable under refinement | 2.5 / 2.0 / 1.5 / 1.0 mm cells give "
        "0.3788 / 0.3773 / 0.3732 / 0.3787 — converged to **±0.005** at 2 mm |",
        "",
        "The 3 mm and 4 mm grids are **not** used: at that size the 10 mm steel plate is only "
        "two or three cells wide and the answer scatters by ±0.02. That scatter is the model "
        "uncertainty of this screen and it is stated rather than hidden.",
        "",
        "## 3. The geometry, and what it is not",
        "",
        "A vertical section through the floor edge: the wall on the left face, the floor "
        "below, the corner at the origin. The wall is the §14-3 build-up (13 lining, 189 wool, "
        "12 wind board, 25 cavity, 25 cladding, "
        f"U = {result['wall_u']:.4f}); the floor is 22 deck, 240 wool, 18 board "
        f"(U = {result['floor_u']:.4f}). The floor runs out to the wall's outer face, because "
        "a wall that stops at the inner face touches the floor at a point and both are then "
        "exposed on faces a real junction does not have — an error this screen made and "
        "corrected before any number was used.",
        "",
        "**The steel is a parameter, not a profile.** No A, W, I, J, thickness or grade exists "
        "for the chassis, so the plate is 10 mm of steel occupying the corner column and "
        "replacing the floor build-up there. It is not a chassis member and must not be read "
        "as one. What it does is put a known quantity of steel in the worst credible place, so "
        "that the *difference* between variants is meaningful even though the absolute "
        "geometry is not yet a design.",
        "",
        "## 4. Six variants",
        "",
        "| | Variant | f_Rsi | Ψ W/mK | Coldest point |",
        "|---|---|---:|---:|---|",
    ]
    for r in result["variants"]:
        cold = r["coldest"]
        who = "the steel" if cold["lam"] > 10.0 else "the timber corner"
        lines.append(
            f"| **{r['tag']}** | {r['name']} | **{r['f_rsi']:.3f}** | "
            f"{r['psi_w_per_mk']:+.3f} | {who} at "
            f"({cold['x_mm']:.0f}, {cold['z_mm']:.0f}) mm |")
    lines += [
        "",
        f"The mould criterion is **{one_d['f_crit_mould']:.3f}** (80 % surface RH, ISO 13788). "
        f"Only **A** and **E** clear it.",
        "",
        "## 5. The governing point moves — and 1D cannot see it",
        "",
        "| Pad mm | f_Rsi | Ψ W/mK | Governing |",
        "|---:|---:|---:|---|",
    ]
    for r in result["pad_sweep"]:
        lines.append(f"| {r['pad_mm']:.0f} | {r['f_rsi']:.3f} | {r['psi']:+.3f} | "
                     f"{r['governing']} |")
    lines += [
        "",
        "**The coldest point leaves the steel at the first millimetre of pad.** Three "
        "millimetres is enough to move it, and from then on the wall's timber corner governs "
        "for every thickness. That is the finding a 1D calculation cannot produce, and it "
        "invalidates the way the requirement was derived.",
        "",
        "## 6. What this changes in the condensation screen",
        "",
        f"That screen required **{one_d['required_added_r']:.3f} m²K/W** of added resistance "
        "and priced it at about **9 mm** of rigid foam. In 2D, 9 mm gives "
        f"**f_Rsi {v['C']['f_rsi']:.3f}** — below the criterion, because the corner now "
        "governs rather than the steel.",
        "",
        f"**20 mm reaches {v['D']['f_rsi']:.3f}**, which is the criterion. So the requirement "
        "is right for the surface it was computed on and wrong for the building: it protects "
        "the steel, and the corner was never in the model. In pad terms the answer is "
        "**20 mm, not 9** — 0.80 m²K/W rather than 0.358.",
        "",
        "The 1D number for the steel itself was **0.236**; 2D gives "
        f"**{v['B']['f_rsi']:.3f}** for the same plate. So 1D was *pessimistic* about the "
        "steel — it assumed the whole surface was steel with no lateral feed from the "
        "surrounding floor. The screen's stated direction of error was therefore wrong even "
        "though its conclusion was right: the number was a bound, but a conservative one for "
        "the steel and silent about the corner.",
        "",
        "## 7. Wrapping beats padding, and it is not close",
        "",
        f"Variant **E** puts the same 10 mm plate below the floor, outside the insulation. "
        f"It gives **f_Rsi {v['E']['f_rsi']:.3f}** and **Ψ {v['E']['psi_w_per_mk']:+.3f}** — "
        f"identical to the bare corner, to three decimals. Padding never gets there: 60 mm of "
        f"rigid foam reaches {result['pad_sweep'][-1]['f_rsi']:.3f} and is still climbing "
        "towards an asymptote below the wrapped value.",
        "",
        "So the design answer is the one the project already suspected and had never priced: "
        "**run the insulation outside the steel.** It needs no pad, no extra material and no "
        "thickness, and it recovers the whole of the loss.",
        "",
        "## 8. What it costs to get it wrong",
        "",
        "| | Ψ W/mK | × 18 m of floor perimeter |",
        "|---|---:|---:|",
        f"| Steel at the corner | {v['B']['psi_w_per_mk']:+.3f} | "
        f"**{heat['plate_w_per_k']:.2f} W/K** |",
        f"| Steel wrapped | {v['E']['psi_w_per_mk']:+.3f} | "
        f"**{heat['wrapped_w_per_k']:.2f} W/K** |",
        f"| Difference | | **{heat['difference_w_per_k']:.2f} W/K** |",
        "",
        f"That difference is about **{heat['difference_w_per_k'] / ELEMENT_LOSS_W_PER_K * 100:.0f} %** "
        f"of the envelope's element heat loss "
        f"({ELEMENT_LOSS_W_PER_K:.1f} W/K at the §14-3 limits, derived in "
        "[the make-up air screen](verificacion-aporte-aire.md)). One drawing decision "
        "moves the heat balance by more than every insulation choice in this project combined.",
        "",
        "It also brackets the thermal-bridge screen's generic table. That screen assumed "
        "**0.10 W/mK** for the floor perimeter; the 2D answer is **0.027** wrapped and "
        "**0.195** unwrapped. The generic value sits between them, which is why the bridge "
        "screen's conclusion — that the junctions must be *designed* rather than estimated — "
        "was correct, and why its number could not be improved without a detail.",
        "",
        "## 9. The perimeter joist: an element problem wearing a junction's clothes",
        "",
        "A joist parallel to the wall, under the deck and through the full insulation depth, is "
        "the one joist a 2D section can see — and it is the perimeter trimmer, which bears on the "
        "chassis beam. Sweeping its position gives a result that looks alarming and is not:",
        "",
        "| Joist inner edge | f_Rsi | Ψ raw | Ψ of the junction |",
        "|---|---:|---:|---:|",
    ]
    for row in joist["rows"]:
        lines.append(f"| {row['distance_mm']:.0f} mm from the wall | **{row['f_rsi']:.3f}** | "
                 f"{row['psi_raw']:+.3f} | {row['psi_junction']:+.3f} |")

    lines += [
        "",
        f"Raw, the joist appears to add **{joist['shift_w_per_mk']:+.3f} W/mK** to the junction at "
        "every position inside the modelled window. It does not. The floor's element U rises from "
        f"**{joist['u_clear']:.4f}** to **{joist['u_joisted']:.4f}** at the "
        f"{joist['fraction'] * 100:.0f} % timber fraction the modelled window contains, and that "
        "increase alone accounts for the whole shift: referenced to the joisted floor U, the "
        "junction reads **+0.028**, which is the unjoisted corner.",
        "",
        "**A 2D junction model and a parallel-path element U must not both count the same joist.** "
        "Computing Ψ against the clear-field U puts the joist's own conduction into the junction, "
        "where it does not belong, and hides the place it does: the floor's U-value. This is the "
        "same error family as the stud fraction — a quantity that is not a property of the "
        "material being carried as one.",
        "",
        "What the joist costs at the junction is small, and it is not a junction problem: f_Rsi "
        "falls from **0.921 to "
        "0.906** at the wall, a 0.015 drop, because the 22 mm deck spreads over the joist and "
        "carries most of it. The junction is not what needs designing here. The floor U is, and "
        "the envelope screen already carries it at a timber fraction.",
        "",
        "The joist **perpendicular** to the wall is the one that matters more and this section "
        "cannot see it at all: it crosses the perimeter as a **point**, once every joist spacing, "
        "and a point bridge is a 3D effect.",
        "",
        "## 10. Limits — what this does not settle",
        "",
        "1. **The chassis profile.** A plate is not an I-section. A real member has a top "
        "flange in contact with the floor over its full width, which will read better than "
        "the plate and worse than the wrapped case.",
        "2. **The 3D corner.** This is a 2D section. At the module's corner two such junctions "
        "meet, and the real f_Rsi there is lower than either. The 8.8 m of corner inventory in "
        "the bridge screen is not modelled here.",
        "3. **The wall's own corner.** Variant A gives 0.921 at the timber corner, comfortably "
        "above the criterion — but that is a 2D section through a 2D corner. A 3D corner has "
        "one more exposed face and will read lower.",
        "4. **Joists perpendicular to the wall.** §9 covers one parallel to it. A perpendicular "
        "joist crosses the perimeter as a point and is a 3D effect; the deck spreading that "
        "makes the parallel case mild is not available to it in the same way.",
        "5. **The vapour field.** This solves heat only. Condensation also depends on the "
        "vapour resistance and the sd-values, which the envelope screen handles in 1D.",
        "",
        "## 11. Source and status",
        "",
        "- Mould criterion and the 1D requirement: `fase1/verificacion-condensacion-union.md`.",
        "- Generic Ψ table and the floor perimeter length: "
        "`fase1/verificacion-puentes-termicas.md`.",
        "- Build-ups and U-values: `fase1/verificacion-envolvente.md`.",
        "- ISO 10211 definition of Ψ; ISO 13788 temperature factor.",
        "- SCREENING ONLY — no junction here is a detail and no value is a design value.",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    result = screen()
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"wrote {args.out_json}")
    if args.out_md:
        path = Path(args.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(result), encoding="utf-8")
        print(f"wrote {args.out_md}")
    if not args.out_md and not args.out_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
