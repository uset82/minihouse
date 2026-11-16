#!/usr/bin/env python3
"""MiniHouse · Comparativa conceptual de chasis R0 (ILUSTRATIVA — NO ES CALCULO DEL MODULO).

AVISO: seccion provisional inventada para demostrar el flujo, masa del archivo
EJEMPLO (2200 kg, 100% estimado). Ningun resultado sirve para dimensionar,
seleccionar eslingas ni liberar planos. Estado: CONCEPTUAL — NOT FOR FABRICATION.

Geometria: fase1/geometria-R0.md (ejes, origen). Chasis: 2 largueros x=0..6 en
y=0.15/2.85, 6 travesanos CANONICOS @1200 (x=0,1.2,...,6.0; reconciliacion-R0).
Largueros discretizados en segmentos de 0.6 m para carga y precision.
Seccion provisional larguero RHS 150x100x5 (h=150 vertical), travesano RHS 100x100x5.
Columnas de izaje SHS 100x100x5 hasta z=3.0 (candidatos esquina alta).

Casos (todos gravedad, sin dinamica — la dinamica se anade en Fase 2 real):
  A instalado-extremos: 4 apoyos z=0 en esquinas de chasis
  B instalado-retranqueado: apoyos x=1.2/4.8 (posicion NO optima, solo comparacion)
  C izaje-bajo: 4 esquinas de chasis suspendidas (ramal vertical ideal)
  D izaje-alto: 4 nudos altos z=3.0 suspendidos, carga baja por columnas
  E izaje-alto excentrico: D + carga puntual bano 250 kg en x=0.6 (asimetria)
  F izaje-bajo 2 puntos diagonales: sensibilidad torsional (caso de ensayo)

Metricas: flecha max |uz| del chasis, diferencial z entre esquinas (torsion),
momento max en largueros, reacciones por punto. Ramales verticales ideales =
spreader perfecto; H de eslingas reales NO incluido (ver hoja de condiciones).

Salida: tabla por consola + fase2/comparativa-izaje-R0-resultados.csv
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from barras3d import Modelo

E, G = 210e9, 81e9


def rhs(b, h, t):
    """Propiedades RHS: b ancho, h alto (vertical), t espesor. Devuelve A, Iz(flexion vertical), Iy, J(aprox pared fina)."""
    A = b * h - (b - 2 * t) * (h - 2 * t)
    Iz = (b * h**3 - (b - 2 * t) * (h - 2 * t)**3) / 12
    Iy = (h * b**3 - (h - 2 * t) * (b - 2 * t)**3) / 12
    Am = (b - t) * (h - t)
    J = 4 * Am**2 * t / (2 * (b - t) + 2 * (h - t))
    return A, Iy, Iz, J


# masa EJEMPLO (no del proyecto)
M_EJ = 2200.0
g = 9.81
W = M_EJ * g
P_BANO = 250.0 * g  # subconjunto ya incluido en M_EJ; en E se REDISTRIBUYE, no se suma


def construir(caso):
    m = Modelo()
    AL, IyL, IzL, JL = rhs(0.100, 0.150, 0.005)
    AT, IyT, IzT, JT = rhs(0.100, 0.100, 0.005)
    ys = [0.15, 2.85]
    # malla CANONICA: travesanos @1200 (x=0,1.2,...,6.0); nudos cada 0.6 m
    xs = [round(0.6 * i, 1) for i in range(11)]          # 0,0.6,...,6.0
    xs_t = [round(1.2 * i, 1) for i in range(6)]         # 0,1.2,...,6.0

    def n(x, yi):
        return f"C{int(round(x*10))}_{yi}"

    for yi, y in enumerate(ys):
        for x in xs:
            m.nudo(n(x, yi), x, y, 0.0)
    # largueros (segmentos de 0.6 m)
    for yi, y in enumerate(ys):
        for i in range(len(xs) - 1):
            m.barra(f"L{i}_{yi}", n(xs[i], yi), n(xs[i+1], yi), AL, E, IyL, IzL, G, JL, vec_y=(0, 1, 0))
    # travesanos canonicos @1200
    for x in xs_t:
        m.barra(f"T{int(round(x*10))}", n(x, 0), n(x, 1), AT, E, IyT, IzT, G, JT, vec_y=(0, 0, 1))
    # gravedad: UDL simetrica; en E se sustituye por UDL de (W-P) + P puntual (redistribucion exacta)
    nseg = len(xs) - 1
    q_larg = -(W / 2 / 6)
    if caso != "E":
        for yi in range(2):
            for i in range(nseg):
                m.carga_distribuida(f"L{i}_{yi}", q_larg, "global_z")
    else:
        q_base = -((W - P_BANO) / 2 / 6)
        for yi in range(2):
            for i in range(nseg):
                m.carga_distribuida(f"L{i}_{yi}", q_base, "global_z")
        # bano en x=0.6 (nudo exacto de la malla)
        m.carga_nodal(n(0.6, 0), fz=-P_BANO / 2)
        m.carga_nodal(n(0.6, 1), fz=-P_BANO / 2)
    # columnas y nudos altos para izaje alto
    if caso in ("D", "E"):
        for cx in (0.0, 6.0):
            for yi in (0, 1):
                top = f"H{int(cx*10)}_{yi}"
                m.nudo(top, cx, ys[yi], 3.0)
                m.barra(f"COL{int(cx*10)}_{yi}", n(cx, yi), top, AT, E, IyT, IzT, G, JT, vec_y=(0, 1, 0))
    # apoyos / suspensiones (ramal vertical ideal: z fijo; un punto fija x,y; otro y)
    def colgar(nudos):
        m.apoyo(nudos[0], (1, 1, 1, 0, 0, 0))
        m.apoyo(nudos[1], (0, 1, 1, 0, 0, 0))
        for nn in nudos[2:]:
            m.apoyo(nn, (0, 0, 1, 0, 0, 0))
    if caso == "A":
        colgar([n(0, 0), n(0, 1), n(6, 0), n(6, 1)])
    elif caso == "B":
        # malla canonica: x=1.2/4.8 son nudos exactos (ya no hay aproximacion)
        colgar([n(1.2, 0), n(1.2, 1), n(4.8, 0), n(4.8, 1)])
    elif caso in ("C", "F"):
        if caso == "C":
            colgar([n(0, 0), n(0, 1), n(6, 0), n(6, 1)])
        else:
            # 2 puntos diagonales: mecanismo contenido minimamente
            m.apoyo(n(0, 0), (1, 1, 1, 0, 0, 0))
            m.apoyo(n(6, 1), (1, 1, 1, 0, 0, 0))
            m.apoyo(n(0, 1), (0, 0, 1, 0, 0, 0))  # 3er punto: sin el, giro rigido libre
    elif caso in ("D", "E"):
        colgar(["H0_0", "H0_1", "H60_0", "H60_1"])
    return m


def metricas(m, r):
    idx = r["idx"]
    chasis = [n for n in idx if n.startswith("C")]
    uz = {n: r["u"][idx[n] * 6 + 2] for n in chasis}
    flecha = max(abs(v) for v in uz.values())
    esquinas = ["C0_0", "C0_1", "C60_0", "C60_1"]
    zc = [uz[n] for n in esquinas]
    # torsion diferencial: (z00+z61)/2 - (z01+z60)/2 (alabeo del rectangulo)
    tors = (zc[0] + zc[3]) / 2 - (zc[1] + zc[2]) / 2
    Mmax = 0.0
    for bid, fl in r["fuerzas"].items():
        if bid.startswith("L"):
            Mmax = max(Mmax, abs(fl[4]), abs(fl[10]))
    # reacciones verticales por punto
    reac = {}
    for n in m.apoyos:
        rz = r["R"][idx[n] * 6 + 2]
        if abs(rz) > 1e-6:
            reac[n] = rz
    equilibrio = sum(reac.values())
    return flecha, tors, Mmax, reac, equilibrio


def main():
    filas = []
    print("=== MiniHouse · comparativa CONCEPTUAL chasis R0 (masa EJEMPLO 2200 kg) ===")
    print("CONCEPTUAL — NOT FOR FABRICATION. Seccion provisional RHS150x100x5 / RHS100x100x5.")
    print("Ramales verticales ideales (spreader perfecto), sin dinamica, sin H de eslinga.\n")
    casos = {
        "A": "apoyos 4 esquinas chasis (instalado)",
        "B": "apoyos retranqueados x=1.2/4.8 (nudos exactos, malla canonica @1200)",
        "C": "izaje bajo, 4 esquinas chasis",
        "D": "izaje alto, 4 nudos z=3.0 por columnas",
        "E": "izaje alto + bano 250 kg redistribuido (excentrico)",
        "F": "izaje bajo 2 puntos diagonales + 1 (torsion)",
    }
    for c, desc in casos.items():
        m = construir(c)
        r = m.resolver()
        flecha, tors, Mmax, reac, eq = metricas(m, r)
        ok = abs(eq - W) < 1e-3
        print(f"[{c}] {desc}")
        print(f"    flecha max chasis = {flecha*1000:8.3f} mm | torsion diferencial = {tors*1000:8.3f} mm | M_max larguero = {Mmax/1000:7.3f} kNm")
        print(f"    reacciones: " + ", ".join(f"{n}={v/1000:.2f} kN" for n, v in sorted(reac.items())) + f" | equilibrio {'OK' if ok else 'FALLO'} (suma={eq/1000:.3f} vs W={W/1000:.3f} kN)")
        assert ok, f"equilibrio falla en caso {c}"
        filas.append(dict(caso=c, descripcion=desc, flecha_mm=round(flecha*1000, 3),
                          torsion_mm=round(tors*1000, 3), Mmax_kNm=round(Mmax/1000, 3),
                          reacciones_kN=";".join(f"{n}:{v/1000:.3f}" for n, v in sorted(reac.items())),
                          W_kN=round(W/1000, 3)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fase2", "comparativa-izaje-R0-resultados.csv")
    # la carpeta fase2/ la crea el agente (el sandbox bloquea mkdir de procesos Python)
    if not os.path.isdir(os.path.dirname(out)):
        raise SystemExit("falta la carpeta fase2/; creala antes de ejecutar")
    try:
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0]))
            w.writeheader()
            w.writerows(filas)
        print(f"\nResultados -> {os.path.normpath(out)}")
    except PermissionError:
        print("\nAVISO: sin permiso de escritura para el CSV; resultados solo por consola.")
    print("NOTA: C vs A dan la misma estructura de apoyo (comparar D vs C es el objetivo);")
    print("F es el caso de sensibilidad torsional para el protocolo de ensayo.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()