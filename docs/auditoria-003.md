# Auditoría cruzada nº 3 · S023 (capítulo 13), build web de raíz, estado de hallazgos

2026-11-17 00:05 · Auditor: sesión lead (DSH). Solo lectura sobre archivos ajenos. Continuación de [auditoria-001](auditoria-001.md) y [auditoria-002](auditoria-002.md).

## A. S023 · corrección del capítulo 13 para la ruta mikrohus — VERIFICADA ✅

WorkBuddy recuperó el conjunto aplicable real de TEK17 cap. 13 para mikrohus (§1-2(2)(e)): **§13-1(1), §13-4, §13-5, §13-7, §13-9…13-16**; quedan fuera §13-2/3/6/8. Consecuencia: las tasas de ventilación de §13-2 (1,2 m³/h·m² → 21,6 m³/h para 18 m²) **no son el requisito** en la ruta probable; rige ventilación funcional §13-1(1) con cantidades alternativas documentadas.

Comprobaciones del auditor:
- La corrección está **propagada coherentemente** en los 9 archivos que citaban las tasas (INDEX, S012 con nota de corrección, compliance-matrix, module-brief, known-assumed-unknown, registro-decisiones, solicitud-datos, clasificacion, plan). Grep exhaustivo: ningún archivo del auditor (fase2/, fase4/, references/) usaba esas tasas — nada que retirar.
- §13-5 (radón) existe en DIBK con la URL citada (fetch directo; límites 200/100 Bq/m³ son los valores conocidos de la norma).
- Números nuevos útiles para el diseño ya registrados: radón ≤200 Bq/m³ (preparación >100), luz ≥2,0% DF o ruta simplificada Ag≥0,07·BRA/LT, terreno ≥1:50 en 3 m, membranas de cubierta ≥1:40, madera <20% humedad (<15% antes de cerrar), baños 1:50/1:100 con rebordes 25/15 mm.
- **Implicación de diseño registrada**: la barrera de radón y la capa capilar-rotura van contra el suelo → afectan al detalle del chasis/apoyos (C-05), no sólo a la envolvente. Y §13-14 exige **medir** la humedad de la madera recuperada antes de instalar: refuerza C-08 con un requisito legal concreto.

## B. Build web de raíz (Antigravity): scripts/build-web.mjs + dist/ + serve.mjs

- El build de producción existe en `dist/` (raíz) y el bundle `main.a4f3054c.js` fue inspeccionado directamente.
- **W-1 SIGUE en el bundle publicado**: hero pill `1.49 mm (a=1.2m)` con `[CALCULADO · 3t REF]` — el ejemplo hipotético sigue badgeado como calculado del módulo.
- **W-2 SIGUE**: `5 × 3000 mm Crossmembers (S355)` literal en el bundle (malla canónica: 6 @1200, ≈2700 mm, grado sin definir).
- **W-3 SIGUE**: "Documented Batch" en el bundle.
- W-4 (altura 3200) sigue en el código fuente.
- El simulador mantiene sus etiquetas correctas ("Hypothetical", "3000 KG REF") ✅.
- **Riesgo de publicación**: con `dist/` en la raíz y `serve.mjs` listo, el sitio puede servirse/publicarse con los hallazgos abiertos. **Recomendación: no publicar hasta cerrar W-1…W-4** (las correcciones concretas están en auditoria-001 §B). Nota: el auditor no arranca servidores sin petición explícita de Carlos.
- `build-web.mjs` borra `dist/` de raíz con `rmSync` antes de copiar: aceptable porque es salida de build; `.gitignore` ya cubre `dist/`, `node_modules/` y `.tmp/` ✅ (verificado).

## C. CSV del auditor reescrito de nuevo (00:02)

Re-verificado: **6/6 filas se reproducen exactamente** desde chasis_r0.py. Sigue siendo benigno. Reiteración de la nota de coordinación: regenerar ejecutando el script, no editando la salida.

## D. Resumen de estado de hallazgos

| Hallazgo | Estado | Dueño |
| --- | --- | --- |
| W-1 hero CALCULADO sobre ejemplo hipotético | **ABIERTO** (también en dist) | Antigravity |
| W-2 5 crossmembers S355 | **ABIERTO** (también en dist) | Antigravity |
| W-3 Documented Batch | **ABIERTO** (también en dist) | Antigravity |
| W-4 altura 3200 sin nota | **ABIERTO** | Antigravity |
| r0-model.json monopendiente | Resuelto por declaración de histórico | WorkBuddy ✅ |
| Corrección §14-2 energía | Propagada y verificada | WorkBuddy ✅ |
| Corrección §13-2 ventilación | Propagada y verificada (S023) | WorkBuddy ✅ |
| Imágenes concepts/*.jpg sin autorización | ABIERTO | Carlos |
| Altura transporte ~4 m | Registrado como restricción C-02 | los 3 agentes |

## E. Suite

verificar_todo.py sigue pasando; CSV↔solver 6/6; enlaces del proyecto sin rotos.