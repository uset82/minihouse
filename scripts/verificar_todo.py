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
  9. alcance normativo TEK17 §13/§14 (guard de regresiones S020-S023)
 10. lift_geometry_screen.py --selftest (geometría de eslingas I-1/I-2 y paso a toneladas)
 11. mass_sensitivity.py --selftest (preparación y sensibilidad de C-07)
 12. r1_frame_skeleton.py --selftest (nudos/barras R1, sin secciones)
 13. daylight_check.py --selftest (TEK17 §13-7, luz diurna)
 14. fire_check.py --selftest (TEK17 capítulo 11, ventanas de escape y R 15)
 15. room_height_check.py --selftest (TEK17 §12-7, altura libre y cobertura)
 16. natural_hazard_screen.py --selftest (TEK17 capítulo 7, inundación y deslizamiento)
 17. envelope_check.py --selftest (TEK17 §14-3 U-values y §13-13 humedad)
 18. section_feasibility.py --selftest (sección integrada: altura, pendiente, envolvente, gálibo)
 19. section_options.py --selftest (opciones R2 de sección y su tolerancia)
 20. instalaciones_check.py --selftest (TEK17 caps. 9/15/16/17: residuos, desagüe, estufa)
 21. documentacion_check.py --selftest (TEK17 caps. 2 y 4: audit §2-2(3) de los informes)
 22. puentes_termicas.py --selftest (puentes térmicos del chasis; §14-3 no los limita)
 23. condensacion_union.py --selftest (condensación en el encuentro; factor f_Rsi ISO 13788)
 24. cubierta_incendio.py --selftest (cubierta bajo cap. 11: ramas, R 15 por carbonización)
 25. ventanas_check.py --selftest (ventanas de rømning §11-13 contra luz diurna §13-7)
 26. incertidumbre.py --selftest (¿son adecuados los márgenes declarados? §2-2(3), 4.º)
 27. puente_2d.py --selftest (conducción 2D en el encuentro; f_Rsi, Ψ, y la malla)
 28. estrategia_incendio.py --selftest (cap. 11: qué cláusulas dependen de la misma decisión)
 29. ventilacion_check.py --selftest (§13-1(1): caudales documentados y la presión que imponen)
 30. aporte_aire.py --selftest (el aire de reposición: su tamaño, y el tiro que no rescata)
 31. radon_check.py --selftest (§13-5 con el piso elevado: la cota E/Q y el esquisto de alumbre)
 32. detalle_encuentro.py --selftest (el detalle del encuentro, generado desde el solver)
 33. ytelsesoversikt.py --selftest (§2-2(4): las tres categorías y lo que queda fuera)
 34. tetthet_test.py --selftest (§14-3 medido: la especificación del ensayo de estanqueidad)
 35. bolted_lap_prototype.py --selftest (unión trenzada atornillada: malla, STEP y acceso a la llave)
 36. frame_model.py --selftest (marco 6 × 3 m a escala 1:40, canales U y travesaños)
 37. combined_joint_prototype.py --selftest (unión combinada: M6 real + aletas + unión dividida)

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
                # file:/// es una ruta absoluta del sistema, no un enlace relativo
                # al repositorio: comprobarla aqui daria falsos positivos.
                if t.startswith(("http:", "https:", "mailto:", "file:", "#")):
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
    resultados.append(run("alcance normativo §13/§14", [r"scripts\verificar_alcance_normativo.py"]))
    resultados.append(run("lift geometry screen", [r"scripts\lift_geometry_screen.py", "--selftest"]))
    resultados.append(run("mass sensitivity screen", [r"scripts\mass_sensitivity.py", "--selftest"]))
    resultados.append(run("R1 frame skeleton", [r"scripts\r1_frame_skeleton.py", "--selftest"]))
    resultados.append(run("daylight check §13-7", [r"scripts\daylight_check.py", "--selftest"]))
    resultados.append(run("fire check capítulo 11", [r"scripts\fire_check.py", "--selftest"]))
    resultados.append(run("room height §12-7", [r"scripts\room_height_check.py", "--selftest"]))
    resultados.append(run("natural hazard capítulo 7", [r"scripts\natural_hazard_screen.py", "--selftest"]))
    resultados.append(run("envelope §14-3 / §13-13", [r"scripts\envelope_check.py", "--selftest"]))
    resultados.append(run("sección integrada", [r"scripts\section_feasibility.py", "--selftest"]))
    resultados.append(run("opciones de sección R2", [r"scripts\section_options.py", "--selftest"]))
    resultados.append(run("instalaciones caps. 9/15/16/17", [r"scripts\instalaciones_check.py", "--selftest"]))
    resultados.append(run("documentación caps. 2/4", [r"scripts\documentacion_check.py", "--selftest"]))
    resultados.append(run("puentes térmicos chasis", [r"scripts\puentes_termicas.py", "--selftest"]))
    resultados.append(run("condensación del encuentro", [r"scripts\condensacion_union.py", "--selftest"]))
    resultados.append(run("cubierta bajo cap. 11", [r"scripts\cubierta_incendio.py", "--selftest"]))
    resultados.append(run("ventanas §11-13 / §13-7", [r"scripts\ventanas_check.py", "--selftest"]))
    resultados.append(run("adecuación de márgenes", [r"scripts\incertidumbre.py", "--selftest"]))
    resultados.append(run("conducción 2D del encuentro", [r"scripts\puente_2d.py", "--selftest"]))
    resultados.append(run("estrategia de incendio cap. 11", [r"scripts\estrategia_incendio.py", "--selftest"]))
    resultados.append(run("ventilación §13-1(1)", [r"scripts\ventilacion_check.py", "--selftest"]))
    resultados.append(run("aire de reposición", [r"scripts\aporte_aire.py", "--selftest"]))
    resultados.append(run("radón §13-5", [r"scripts\radon_check.py", "--selftest"]))
    resultados.append(run("detalle del encuentro", [r"scripts\detalle_encuentro.py", "--selftest"]))
    resultados.append(run("ytelsesoversikt §2-2(4)", [r"scripts\ytelsesoversikt.py", "--selftest"]))
    resultados.append(run("tetthet §14-3 especificado", [r"scripts\tetthet_test.py", "--selftest"]))
    resultados.append(run("prototipo unión atornillada", [r"scripts\bolted_lap_prototype.py", "--selftest"]))
    resultados.append(run("modelo del marco 6x3 a escala", [r"scripts\frame_model.py", "--selftest"]))
    resultados.append(run("unión combinada M6 + aletas", [r"scripts\combined_joint_prototype.py", "--selftest"]))
    print("=" * 40)
    if all(resultados):
        print("SUITE COMPLETA: TODO PASA")
        return 0
    print("SUITE COMPLETA: HAY FALLOS")
    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())