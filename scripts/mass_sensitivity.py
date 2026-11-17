#!/usr/bin/env python3
"""MiniHouse · inventory readiness and CG sensitivity screen.

Prepares C-07 data collection. It does NOT invent project masses: it reads the
inventory you supply and reports which values are measured/manufacturer versus
estimated, then ranks components by how much their position uncertainty moves
the CG and the ideal two-support reactions.

Uses the already verified masas_cg.py functions. No strength, lift or
fabrication claim is made.

Usage:
  python mass_sensitivity.py fase1/inventario-masas.csv \
      --depositos lleno --apoyos 0 6 --out-md fase1/sensibilidad-masas.md
  python mass_sensitivity.py --selftest
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from masas_cg import leer_inventario, seleccionar, masas_cg, reacciones_2apoyos  # noqa: E402


def readiness(items, selected):
    estimated = [it for it in selected if it["procedencia"] == "estimado"]
    mass_total = sum(it["m"] for it in selected)
    mass_est = sum(it["m"] for it in estimated)
    return {
        "items_total": len(items),
        "items_selected": len(selected),
        "items_estimated": len(estimated),
        "mass_estimated_kg": round(mass_est, 2),
        "mass_estimated_pct": round(100.0 * mass_est / mass_total, 1) if mass_total else 0.0,
        "example_rows": [it["id"] for it in items if it["id"].upper().startswith("EJ-")],
        "fixed": sum(1 for it in selected if it["condicion"] == "fijo"),
        "tank_related": sum(1 for it in selected if it["condicion"].startswith("deposito_")),
        "removable": sum(1 for it in selected if it["condicion"] == "desmontable"),
    }


def shifted(items, item_id, axis, delta_m):
    out = []
    for it in items:
        row = dict(it)
        if row["id"] == item_id:
            row[axis] += delta_m
        out.append(row)
    return out


def sensitivity(items, g, xa, xb, delta_m):
    M, W, cg = masas_cg(items, g)
    span = xb - xa
    if span == 0:
        raise SystemExit("ERROR: apoyos coincidentes")
    _, rb0 = reacciones_2apoyos(W, cg[0], xa, xb)

    rows = []
    for it in items:
        per_axis = {}
        for axis in ("x", "y", "z"):
            _, _, cg2 = masas_cg(shifted(items, it["id"], axis, delta_m), g)
            per_axis[axis] = cg2[("x", "y", "z").index(axis)] - cg[("x", "y", "z").index(axis)]
        _, rb_x = reacciones_2apoyos(W, cg[0] + per_axis["x"], xa, xb)
        magnitude = math.sqrt(sum(v * v for v in per_axis.values()))
        rows.append({
            "id": it["id"],
            "componente": it["componente"],
            "masa_kg": it["m"],
            "procedencia": it["procedencia"],
            "dxG_m": round(per_axis["x"], 5),
            "dyG_m": round(per_axis["y"], 5),
            "dzG_m": round(per_axis["z"], 5),
            "CG_shift_m": round(magnitude, 5),
            "dRB_N": round(rb_x - rb0, 2),
            "expected_dxG_m": round(it["m"] / M * delta_m, 5),
        })
    rows.sort(key=lambda r: r["CG_shift_m"], reverse=True)
    return {"M_kg": M, "W_N": W, "cg_m": cg, "Rb0_N": rb0, "rows": rows}


def markdown(items, selected, report, meta, delta_mm):
    rd = readiness(items, selected)
    cg = report["cg_m"]
    lines = [
        "# MiniHouse · inventory readiness and CG sensitivity",
        "",
        "**State:** TOOL OUTPUT — NOT PROJECT DATA unless the supplied inventory is real. "
        "No lift, structure or fabrication claim is made.",
        "",
        f"- Inventory: `{meta['inventory']}`",
        f"- Configuration: tanks `{meta['depositos']}`, removable items included: "
        f"{not meta['sin_desmontables']}",
        f"- Support stations for reaction sensitivity: x={meta['xa']:.1f} m and x={meta['xb']:.1f} m "
        "(ideal two-support beam only)",
        f"- Position perturbation: +{delta_mm:.0f} mm in one axis at a time",
        "",
        "## 1. Data readiness",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Rows in inventory | {rd['items_total']} |",
        f"| Rows in selected configuration | {rd['items_selected']} |",
        f"| Fixed / tank-related / removable | {rd['fixed']} / {rd['tank_related']} / {rd['removable']} |",
        f"| Estimated-provenance rows | {rd['items_estimated']} |",
        f"| Estimated mass share | {rd['mass_estimated_pct']:.1f} % ({rd['mass_estimated_kg']:.1f} kg) |",
    ]
    if rd["example_rows"]:
        lines += [
            "",
            f"**WARNING: example rows detected** ({', '.join(rd['example_rows'])}). "
            "This output is a tool demonstration, not MiniHouse project data.",
        ]
    lines += [
        "",
        "## 2. Base case",
        "",
        f"M = {report['M_kg']:.2f} kg; W = {report['W_N']/1000:.3f} kN; "
        f"CG = ({cg[0]:.4f}, {cg[1]:.4f}, {cg[2]:.4f}) m; "
        f"R_B = {report['Rb0_N']/1000:.3f} kN at x_B={meta['xb']:.1f} m.",
        "",
        "## 3. Position sensitivity ranking",
        "",
        "Each row shows the effect of moving that component +delta in x, y or z alone. "
        "The analytic check is `dxG = (m_i/M)·delta`; `dRB = W·dxG/(x_B-x_A)`. "
        "A large value means the component's position must be measured, not guessed.",
        "",
        "| Rank | ID | Component | m kg | Source | dxG m | dyG m | dzG m | CG shift m | dR_B kN | Check dxG m |",
        "|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for idx, r in enumerate(report["rows"], 1):
        lines.append(
            f"| {idx} | {r['id']} | {r['componente']} | {r['masa_kg']:.1f} | {r['procedencia']} | "
            f"{r['dxG_m']:+.4f} | {r['dyG_m']:+.4f} | {r['dzG_m']:+.4f} | "
            f"{r['CG_shift_m']:.4f} | {r['dRB_N']/1000:+.3f} | {r['expected_dxG_m']:+.4f} |"
        )
    lines += [
        "",
        "## 4. Interpretation",
        "",
        "- Reaction sensitivity is an ideal two-support static screen. Four supports are "
        "statically indeterminate; do not read `dR_B` as a four-point lift distribution.",
        "- Reduce estimated mass share before using any result for sling or crane selection. "
        "The existing masas_cg.py report already flags estimated configurations.",
        "- Prioritise field measurement of high-ranking components: mass and 3D position both matter.",
        "- CONCEPTUAL TOOL OUTPUT. No fabrication release, no lift authorisation.",
        "",
    ]
    return "\n".join(lines)


def selftest():
    g = 9.81
    items = [
        dict(id="a", componente="light", m=100.0, x=1.0, y=1.5, z=0.0,
             procedencia="medido", condicion="fijo"),
        dict(id="b", componente="heavy", m=300.0, x=5.0, y=1.5, z=2.0,
             procedencia="estimado", condicion="fijo"),
        dict(id="EJ-001", componente="example", m=100.0, x=0.5, y=0.5, z=0.5,
             procedencia="estimado", condicion="fijo"),
    ]
    selected = [it for it in items if it["id"] != "EJ-001"]
    rep = sensitivity(selected, g, 0.0, 6.0, 0.3)
    assert abs(rep["M_kg"] - 400.0) < 1e-9
    assert abs(rep["cg_m"][0] - 4.0) < 1e-9
    heavy = next(r for r in rep["rows"] if r["id"] == "b")
    light = next(r for r in rep["rows"] if r["id"] == "a")
    assert abs(heavy["dxG_m"] - 0.225) < 1e-9      # (300/400)*0.3
    assert abs(light["dxG_m"] - 0.075) < 1e-9      # (100/400)*0.3
    assert abs(heavy["dRB_N"] - 3924.0 * 0.225 / 6.0) < 0.02
    assert rep["rows"][0]["id"] == "b"
    rd = readiness(items, selected)
    assert rd["example_rows"] == ["EJ-001"]
    assert abs(rd["mass_estimated_pct"] - 75.0) < 1e-9
    print("Mass readiness/sensitivity self-test OK: analytic CG, reaction, ranking and example flags pass")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inventario", nargs="?")
    ap.add_argument("--depositos", choices=["lleno", "vacio"], default="lleno")
    ap.add_argument("--sin-desmontables", action="store_true")
    ap.add_argument("--apoyos", nargs=2, type=float, metavar=("XA", "XB"), default=(0.0, 6.0))
    ap.add_argument("--g", type=float, default=9.81)
    ap.add_argument("--delta-mm", type=float, default=300.0)
    ap.add_argument("--out-md", help="write Markdown report")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()
        return
    if not a.inventario:
        ap.error("falta el CSV de inventario (o use --selftest)")

    items = leer_inventario(a.inventario)
    selected = seleccionar(items, a.depositos, a.sin_desmontables)
    rep = sensitivity(selected, a.g, a.apoyos[0], a.apoyos[1], a.delta_mm / 1000.0)
    meta = {
        "inventory": a.inventario,
        "depositos": a.depositos,
        "sin_desmontables": a.sin_desmontables,
        "xa": a.apoyos[0],
        "xb": a.apoyos[1],
    }
    text = markdown(items, selected, rep, meta, a.delta_mm)
    if a.out_md:
        path = Path(a.out_md)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path}")
    else:
        print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
