#!/usr/bin/env python3
"""MiniHouse · Verificacion de accesibilidad y assets del prototipo fase4/sitio.

Contraste WCAG 2.x calculado (no estimado) para los pares de tokens usados,
enlaces/asset internos existentes, alt en imagenes, skip-link, lang, viewport,
aria-current, y ausencia de peticiones externas. Solo lectura.
"""
import os
import re
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fase4", "sitio")


def lum(hexcolor):
    c = hexcolor.lstrip("#")
    rgb = [int(c[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    fallos = []
    # pares realmente usados en estilo.css / html
    pares = [
        ("tinta/papel (texto)", "#2b2620", "#faf6ef", 4.5),
        ("acero/papel (h1,h2)", "#4a5560", "#faf6ef", 4.5),
        ("madera/papel (enlaces)", "#8a5a33", "#faf6ef", 4.5),
        ("alerta/papel (nota footer)", "#8c2f1b", "#faf6ef", 4.5),
        ("exito/papel", "#2c6e49", "#faf6ef", 4.5),
        ("blanco/alerta (etiqueta)", "#ffffff", "#8c2f1b", 4.5),
        ("blanco/acero (etiqueta)", "#ffffff", "#4a5560", 4.5),
        ("blanco/madera (etiqueta)", "#ffffff", "#8a5a33", 4.5),
        ("blanco/exito (etiqueta)", "#ffffff", "#2c6e49", 4.5),
        ("tinta/aviso-fondo", "#2b2620", "#f3e7d8", 4.5),
        ("tinta/tarjeta", "#2b2620", "#fffdf8", 4.5),
        ("tinta/th-fondo", "#2b2620", "#f0e9dc", 4.5),
        ("blanco/acero (skip-link)", "#ffffff", "#4a5560", 4.5),
        ("alerta/hover-madera? enlace hover alerta/papel", "#8c2f1b", "#faf6ef", 4.5),
    ]
    print("== Contraste WCAG (medido) ==")
    for nombre, fg, bg, minimo in pares:
        r = ratio(fg, bg)
        ok = r >= minimo
        print(f"  {'OK ' if ok else 'FALLO'} {nombre}: {r:.2f}:1 (min {minimo})")
        if not ok:
            fallos.append(nombre)
    # focus outline acero sobre papel: non-text 3:1
    r = ratio("#4a5560", "#faf6ef")
    print(f"  {'OK ' if r >= 3 else 'FALLO'} foco (no-texto): {r:.2f}:1 (min 3.0)")
    if r < 3:
        fallos.append("foco")

    print("\n== HTML ==")
    for fn in sorted(os.listdir(BASE)):
        if not fn.endswith(".html"):
            continue
        p = os.path.join(BASE, fn)
        t = open(p, encoding="utf-8").read()
        checks = {
            'lang="es"': 'lang="es"' in t,
            "viewport": 'name="viewport"' in t,
            "skip-link": 'class="salto"' in t and 'href="#contenido"' in t,
            "main id=contenido": 'id="contenido"' in t,
            "nav aria-label": 'aria-label="Secciones"' in t,
            "aria-current": 'aria-current="page"' in t,
            "sin http externo": not re.search(r'(src|href)="https?://', t),
            "title": "<title>" in t,
            "meta description": 'name="description"' in t,
        }
        for img in re.findall(r"<img[^>]*>", t):
            checks[f"alt en {img[:40]}..."] = 'alt="' in img and len(re.search(r'alt="([^"]*)"', img).group(1)) > 20
        for href in re.findall(r'(?:href|src)="([^"#]+)"', t):
            if href.startswith(("http", "mailto")):
                continue
            checks[f"existe {href}"] = os.path.exists(os.path.join(BASE, href))
        malos = [k for k, v in checks.items() if not v]
        print(f"  {fn}: {'OK' if not malos else 'FALLOS: ' + '; '.join(malos)} ({len(checks)} checks)")
        fallos += [f"{fn}: {m}" for m in malos]

    print("\n== Peso ==")
    total = 0
    for root, _, files in os.walk(BASE):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    print(f"  Sitio completo: {total/1024:.1f} KB (sin fuentes externas, sin JS)")
    if fallos:
        print(f"\nRESULTADO: {len(fallos)} FALLOS")
        sys.exit(1)
    print("\nRESULTADO: TODOS LOS CHECKS PASAN")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()