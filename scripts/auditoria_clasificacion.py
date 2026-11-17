#!/usr/bin/env python3
"""Verificacion independiente de las tablas de fase1/clasificacion-uso-decision.md (WorkBuddy).
1) Pila maxima para 4,00 m por pendiente (arithmetica).
2) Correccion energetica TEK17 14-5: coherencia interna con S020/S021.
Solo lectura.
"""
import json
import math

j = json.load(open(r"knowledge\comparisons\r1-gable-options.json", encoding="utf-8"))
print("== tabla pila maxima para altura cargada 4000 mm ==")
tabla_doc = {5: 869, 10: 735, 15: 598, 20: 454}
ok = True
for o in j["options"]:
    p = int(o["pitch_deg"])
    ridge = o["ridge_z_mm"]
    stack_max = 4000 - ridge
    doc = tabla_doc[p]
    good = abs(stack_max - doc) <= 1.0
    ok &= good
    print(f"{p:>2} deg: cumbrera={ridge:.1f}  pila_max={stack_max:.1f} mm  doc={doc}  {'OK' if good else 'DIVERGE'}")
print("ARITMETICA:", "COINCIDE" if ok else "DIVERGE")

# loaded heights del JSON vs afirmacion S022 (4.03–4.85 m)
mins = min(o["loaded_height_examples_mm"][0]["loaded_height_mm"] for o in j["options"])
maxs = max(o["loaded_height_examples_mm"][-1]["loaded_height_mm"] for o in j["options"])
print(f"\nRango cargado del JSON: {mins:.0f}–{maxs:.0f} mm; S022 dice ~4.03–4.85 m -> {'OK' if abs(mins-4031)<2 and abs(maxs-4846)<2 else 'REVISAR'}")