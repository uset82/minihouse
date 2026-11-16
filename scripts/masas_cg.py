#!/usr/bin/env python3
"""MiniHouse · Calculadora reproducible de masas, CG y reacciones (Fase 1).

Estado: herramienta de inventario. NO es un calculo de resistencia ni de izaje.
Lee un inventario CSV (columnas: id,revision,componente,material,masa_kg,x_m,y_m,z_m,
procedencia,condicion,notas) y calcula, por configuracion:

  W = g * sum(m_i);  r_G = sum(m_i r_i) / sum(m_i)

Configuraciones: 'instalado' y 'transporte' incluyen fijo + deposito_lleno o
deposito_vacio segun --depositos; excluyen 'desmontable' si --sin-desmontables.
Reacciones entre dos estaciones A(x_A) y B(x_B) a lo largo de x (viga ideal,
solo componente vertical, sin dinamica): R_B = W (x_G-x_A)/(x_B-x_A).
Con 4 apoyos NO se reparte W/4: se avisa y solo se da el total por eje.

Uso:
  python masas_cg.py inventario.csv [--depositos lleno|vacio] [--sin-desmontables]
                     [--apoyos xA xB] [--g 9.81]

Prueba automatica: python masas_cg.py --selftest
Unidades: m, kg, N, kN. Origen segun fase1/geometria-R0.md.
"""
import argparse
import csv
import sys

COND_FIJA = {"fijo"}
COND_DEP = {"deposito_lleno", "deposito_vacio"}
COND_DESM = {"desmontable"}


def leer_inventario(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    items = []
    for i, r in enumerate(filas, start=2):
        try:
            items.append({
                "id": r["id"].strip(),
                "componente": r["componente"].strip(),
                "m": float(r["masa_kg"]),
                "x": float(r["x_m"]), "y": float(r["y_m"]), "z": float(r["z_m"]),
                "procedencia": r["procedencia"].strip().lower(),
                "condicion": r["condicion"].strip().lower(),
            })
        except (KeyError, ValueError) as e:
            raise SystemExit(f"ERROR fila {i} ({r.get('id','?')}): {e}")
        if items[-1]["m"] < 0:
            raise SystemExit(f"ERROR fila {i}: masa negativa")
        if items[-1]["condicion"] not in COND_FIJA | COND_DEP | COND_DESM:
            raise SystemExit(f"ERROR fila {i}: condicion desconocida "
                             f"'{items[-1]['condicion']}' (use fijo, deposito_lleno, "
                             "deposito_vacio, desmontable)")
        if items[-1]["procedencia"] not in {"medido", "fabricante", "estimado"}:
            raise SystemExit(f"ERROR fila {i}: procedencia debe ser medido, "
                             "fabricante o estimado")
    ids = [it["id"] for it in items]
    if len(set(ids)) != len(ids):
        raise SystemExit("ERROR: ids duplicados en el inventario")
    return items


def seleccionar(items, depositos="lleno", sin_desmontables=False):
    sel = []
    for it in items:
        c = it["condicion"]
        if c in COND_FIJA:
            sel.append(it)
        elif c == f"deposito_{depositos}":
            sel.append(it)
        elif c in COND_DESM and not sin_desmontables:
            sel.append(it)
    return sel


def masas_cg(items, g=9.81):
    M = sum(it["m"] for it in items)
    if M <= 0:
        raise SystemExit("ERROR: masa total nula; inventario vacio o mal filtrado")
    xg = sum(it["m"] * it["x"] for it in items) / M
    yg = sum(it["m"] * it["y"] for it in items) / M
    zg = sum(it["m"] * it["z"] for it in items) / M
    return M, g * M, (xg, yg, zg)


def reacciones_2apoyos(W, xg, xa, xb):
    if xb == xa:
        raise SystemExit("ERROR: apoyos coincidentes")
    rb = W * (xg - xa) / (xb - xa)
    ra = W - rb
    return ra, rb


def informe(items, sel, depositos, sin_desmontables, apoyos, g):
    M, W, (xg, yg, zg) = masas_cg(sel, g)
    n_est = sum(1 for it in sel if it["procedencia"] == "estimado")
    m_est = sum(it["m"] for it in sel if it["procedencia"] == "estimado")
    print("=== MiniHouse · masas y CG (herramienta de inventario, NO verificacion) ===")
    print(f"Configuracion: depositos={depositos}, desmontables incluidos={not sin_desmontables}")
    print(f"Componentes incluidos: {len(sel)} de {len(items)}")
    print(f"Masa total M = {M:.1f} kg   W = {W/1000:.3f} kN (g={g})")
    print(f"CG: x_G={xg:.3f} m  y_G={yg:.3f} m  z_G={zg:.3f} m")
    print(f"Calidad del dato: {n_est} componentes estimados, {m_est:.1f} kg "
          f"({100*m_est/M:.0f}% de la masa) -> CG ESTIMADO hasta pesaje")
    if any(it["procedencia"] == "estimado" for it in sel):
        print("AVISO: resultados ESTIMADOS. No usar para seleccionar eslingas, grua ni WLL.")
    if apoyos:
        xa, xb = apoyos
        ra, rb = reacciones_2apoyos(W, xg, xa, xb)
        print(f"\nReacciones viga ideal 2 estaciones x_A={xa} m, x_B={xb} m (sin dinamica):")
        print(f"  R_A = {ra/1000:.3f} kN   R_B = {rb/1000:.3f} kN   (suma = {(ra+rb)/1000:.3f} kN)")
        if ra < 0 or rb < 0:
            print("  AVISO: reaccion negativa -> vuelco respecto a esa estacion; revisar CG/apoyos.")
        print("  Con 4 apoyos reales el reparto NO es W/4 (hiperestatico):")
        print("  se requiere rigidez del modelo (Fase 2) o pesaje con celulas.")
    return M, W, (xg, yg, zg)


def selftest():
    """Casos cerrados verificables a mano."""
    g = 9.81
    # 1) dos masas puntuales simetricas
    items = [
        dict(id="t1", componente="a", m=100.0, x=1.0, y=1.5, z=0.0, procedencia="medido", condicion="fijo"),
        dict(id="t2", componente="b", m=300.0, x=5.0, y=1.5, z=2.0, procedencia="medido", condicion="fijo"),
    ]
    M, W, (xg, yg, zg) = masas_cg(items, g)
    assert abs(M - 400.0) < 1e-9
    assert abs(W - 3924.0) < 1e-6
    assert abs(xg - 4.0) < 1e-9      # (100*1+300*5)/400
    assert abs(yg - 1.5) < 1e-9
    assert abs(zg - 1.5) < 1e-9      # (300*2)/400
    # 2) reacciones: W=3924 N, xg=4 entre 0 y 6 -> RA=W/3, RB=2W/3
    ra, rb = reacciones_2apoyos(W, xg, 0.0, 6.0)
    assert abs(ra - 1308.0) < 1e-6 and abs(rb - 2616.0) < 1e-6
    # 3) CG fuera de apoyos (xg=4 < xA=4.5) -> R_B negativa (vuelco en A)
    ra2, rb2 = reacciones_2apoyos(W, xg, 4.5, 6.0)
    assert rb2 < 0 < ra2
    assert abs(rb2 + W / 3.0) < 1e-6
    # 4) filtro depositos: lleno vs vacio cambia masa, no ids fijos
    items += [
        dict(id="t3", componente="dep", m=120.0, x=0.6, y=2.6, z=0.3, procedencia="estimado", condicion="deposito_lleno"),
        dict(id="t4", componente="dep", m=20.0, x=0.6, y=2.6, z=0.3, procedencia="estimado", condicion="deposito_vacio"),
        dict(id="t5", componente="silla", m=10.0, x=4.0, y=1.0, z=0.5, procedencia="estimado", condicion="desmontable"),
    ]
    assert len(seleccionar(items, "lleno")) == 4
    assert len(seleccionar(items, "vacio")) == 4
    assert len(seleccionar(items, "vacio", True)) == 3
    Mll, _, _ = masas_cg(seleccionar(items, "lleno"), g)
    Mva, _, _ = masas_cg(seleccionar(items, "vacio"), g)
    assert abs(Mll - Mva - 100.0) < 1e-9
    print("SELFTEST OK: 4 casos cerrados (CG, W, reacciones, vuelco, filtros) verificados.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inventario", nargs="?")
    p.add_argument("--depositos", choices=["lleno", "vacio"], default="lleno")
    p.add_argument("--sin-desmontables", action="store_true")
    p.add_argument("--apoyos", nargs=2, type=float, metavar=("XA", "XB"))
    p.add_argument("--g", type=float, default=9.81)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
        return
    if not a.inventario:
        p.error("falta el CSV de inventario (o use --selftest)")
    items = leer_inventario(a.inventario)
    sel = seleccionar(items, a.depositos, a.sin_desmontables)
    informe(items, sel, a.depositos, a.sin_desmontables, a.apoyos, a.g)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()