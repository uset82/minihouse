#!/usr/bin/env python3
"""MiniHouse · Suite de verificacion completa del proyecto (un solo comando).

Ejecuta, en orden:
  1. masas_cg.py --selftest          (CG, W, reacciones, filtros)
  2. barras3d.py --selftest          (solver independiente vs casos del informe)
  3. knowledge/derivations/verify_beam.py    (D001, requiere sympy en PYTHONPATH)
  4. knowledge/derivations/verify_rigging.py (D003)
  5. check_web.py                    (contraste medido, HTML, assets del sitio)
  6. chasis_r0.py                    (equilibrio de los 6 casos A-F)
  7. matriz-acciones.csv             (parseable, columnas obligatorias)
  8. enlaces internos Markdown       (excluye web/, node_modules/, .tmp/, dist/)

Uso:  python scripts/verificar_todo.py
Sale con codigo 0 si todo pasa, 1 si algo falla. Pensado para CI local o para
ejecutar antes de cualquier traspaso entre roles/sesiones.

Nota de entorno: si sympy no esta instalado, anadir .tmp/pylibs al PYTHONPATH
(vendorizado) o el paso 3 se marca OMITIDO con aviso (no fallo), porque D001
ya esta cubierto numericamente por el paso 2.
"""
import csv
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def run(nombre, args, obligatorio=True):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    ok = r.returncode == 0
    tail = (r.stdout or r.stderr).strip().splitlines()
    last = tail[-1] if tail else "(sin salida)"
    print(f"[{'OK' if ok else 'FALLO'}] {nombre}: {last[:110]}")
    if not ok and obligatorio:
        return False
    if not ok:
        print(f"       (omitido, no obligatorio: {last[:80]})")
    return True


def enlaces():
    excl = re.compile(r"\\(\.tmp|node_modules|web|dist)\\", re.IGNORECASE)
    broken, checked, nfiles = [], 0, 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".tmp", "node_modules", "web", "dist", ".git")]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            nfiles += 1
            text = open(p, encoding="utf-8").read()
            for m in re.finditer(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
                t = m.group(1)
                if t.startswith(("http:", "https:", "mailto:", "#")):
                    continue
                t2 = t.split("#")[0]
                if not t2:
                    continue
                from urllib.parse import unquote
                t2 = unquote(t2.strip("<>"))
                checked += 1
                if not os.path.exists(os.path.join(dirpath, t2)):
                    broken.append(f"{os.path.relpath(p, ROOT)} -> {t}")
    print(f"[{'OK' if not broken else 'FALLO'}] enlaces: {checked} en {nfiles} archivos")
    for b in broken[:10]:
        print("       ROTO:", b)
    return not broken


def matriz():
    p = os.path.join(ROOT, "fase2", "matriz-acciones.csv")
    cols = {"caso", "situacion_en1990", "accion", "formula_o_fuente", "estado_valor"}
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    ok = bool(rows) and cols.issubset(rows[0].keys())
    print(f"[{'OK' if ok else 'FALLO'}] matriz-acciones: {len(rows)} filas")
    return ok


def main():
    print("=== MiniHouse · verificacion completa ===")
    resultados = []
    resultados.append(run("masas_cg selftest", [r"scripts\masas_cg.py", "--selftest"]))
    resultados.append(run("barras3d selftest", [r"scripts\barras3d.py", "--selftest"]))
    try:
        import sympy  # noqa: F401
        tiene_sympy = True
    except ImportError:
        tiene_sympy = False
    resultados.append(run("D001 verify_beam (sympy)", [r"knowledge\derivations\verify_beam.py"], obligatorio=tiene_sympy))
    resultados.append(run("D003 verify_rigging", [r"knowledge\derivations\verify_rigging.py"]))
    resultados.append(run("check_web", [r"scripts\check_web.py"]))
    resultados.append(run("chasis A-F equilibrio", [r"scripts\chasis_r0.py"]))
    resultados.append(matriz())
    resultados.append(enlaces())
    print("=" * 40)
    if all(resultados):
        print("SUITE COMPLETA: TODO PASA")
        return 0
    print("SUITE COMPLETA: HAY FALLOS")
    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())