# Auditoría cruzada nº 1 · Antigravity (web) + WorkBuddy (cálculo)

2026-11-16 23:50 · Auditor: sesión lead (DSH), rol verificador independiente. Solo lectura sobre archivos ajenos: **nada de `web/` ni de los scripts de WorkBuddy fue modificado**. Los hallazgos son accionables por cada agente sobre sus propios archivos.

## A. WorkBuddy · scripts/r1_gable_options.py + r1-gable-options.json

**Veredicto: MATEMÁTICA CORRECTA ✅**

- `--selftest` ejecutado: pasa.
- Verificación independiente (reimplementación de rise/slope/áreas/alturas cargadas/masa mínima ESTA desde cero): **las 4 opciones de pendiente (5/10/15/20°) coinciden en los 8 campos comprobados**, incluidas cumbreras 3131,2 / 3264,5 / 3401,9 / 3546,0 mm y masas mínimas 15,66–17,73 t.
- Las alturas cargadas (ridge + stack) suman correctamente en los 12 ejemplos.
- Buenas prácticas observadas: no selecciona pendiente, stack declarado ilustrativo, ESTA marcado como guidance no ley noruega, límite legal de altura no reclamado.

**Observación menor (no error):** el datum de alero 3000 mm se hereda del borde bajo del monopendiente R0; está declarado como screening, correcto. Cuando C-02 fije alero/cumbrera, regenerar.

**Hallazgo de coherencia (medio):** `knowledge/comparisons/r0-model.json` sigue con techo monopendiente (S-03 superado). Ya declarado en [reconciliacion-R0.md](reconciliacion-R0.md) §5; WorkBuddy debe actualizar su JSON canónico o marcarlo histórico.

## B. Antigravity · web/chat-demo (MiniHouseFrontPage + 3DSimulator)

**Veredicto: MATEMÁTICA CORRECTA ✅ · TRAZABILIDAD CON 4 HALLAZGOS ⚠️**

Matemática:
- `vitest run` de sus 3 tests: **pasan** (ejecutado aquí).
- Auditoría independiente EXACTA de `computeBeamDeflectionMm`: reimplementación TS→Python contrastada contra doble integración analítica propia en **601 puntos × 7 retranqueos (0–1,8 m): error máximo ~1e-14 mm**. La fórmula del perfil completo (tramo central + voladizo, continuidad de pendiente) es exacta, no sólo los dos puntos del test. (Un primer intento con integrador Euler propio dio falsa divergencia; descartado — el error era del auditor, no del código.)

Hallazgos de contenido (ordenados por gravedad):

| # | Gravedad | Dónde | Problema | Acción sugerida (Antigravity) |
| --- | --- | --- | --- | --- |
| W-1 | **Alta** | FrontPage hero pill "INSET DEFLECTION 1.49 mm (a=1.2m) [CALCULADO · 3t REF]" y Concept 2 badge "[CALCULADO · EULER-BERNOULLI]" con 24,63/1,49 mm | El estado **CALCULADO** del proyecto significa "calculado para el módulo". Estos números son del **caso hipotético de 3 000 kg del informe** (rules.md §3: nunca como dato real). "3t REF" es críptico; un visitante lee "la casita se flexa 1,49 mm". El simulador sí lo etiqueta ("Hypothetical test case", "3000 KG REF") pero el hero no | Cambiar badge a `[CONCEPTUAL · EJEMPLO HIPOTÉTICO 3 t]` o añadir "ejemplo del informe, no del módulo" visible junto a la cifra. Mantener CALCULADO sólo para resultados del módulo real |
| W-2 | Media | BOM MH-STR-001: "2 × 6000 mm + **5 × 3000 mm** Crossmembers (S355)" | (a) La malla canónica reconciliada es **6 travesaños @1200** (no 5); (b) longitud de travesaño ≈2700 mm entre ejes de largueros, no 3000; (c) **S355 no está decidido** — la sección y el grado están SIN DEFINIR en geometria-R0 | Alinear con r0-model.json canónico; marcar material "acero (grado por definir)" o [CONCEPTUAL] explícito en el campo material |
| W-3 | Media | BOM MH-ENV-003 "Documented Batch" / "Weighed per panel batch (Phase 1)"; MH-NOD-002 "EN 13155 Padeyes" | No existe ningún lote documentado ni pesado (C-08 abierta); no hay padeyes diseñados ni cálculo EN 13155. El texto en presente sugiere evidencia que no existe | Redactar en futuro/condicional: "lote por documentar (C-08)", "padeyes por diseñar según EN 13155" |
| W-4 | Baja | FrontPage hero: "6000 × 3000 × **3200** mm" y BOM columnas H=3200; roof layer "6000×3000×450" | 3200 era la altura R0 con monopendiente (S-01 pendiente de revisión con dos aguas; cumbrera R1 provisional 3131–3546 según pendiente). 450 mm de espesor de cubierta no tiene fuente | Marcar altura "por confirmar (techo dos aguas sin acotar)" o citar el rango de r1-gable-options como screening |

Positivos que conviene conservar: etiquetas de estado en las 4 capas BOM, "Hypothetical test case" en massNote, "Pending Phase 1 inventory", roadmap de fases fiel a PROJECT.md, prompts de IA que citan las normas correctas (1993-1-8 para uniones, EN 13155 para aparejo).

**Nota de alcance:** las 3 imágenes `concepts/*.jpg` (hero-nordic, 3d-lifting-sim, exploded-materials) son nuevas, generadas para la web; no están en el registro de medios autorizados del brief. Carlos debe autorizarlas antes de publicar (mismo criterio que images/). El modelo auditor no puede verlas; revisión visual humana pendiente.

## C. Coherencia entre los tres agentes

- Los números de flecha que muestra la web (24,63/1,49) coinciden con D001 (WorkBuddy), barras3d (lead) y el informe: **cuatro fuentes independientes, mismos números** ✅.
- La web usa la malla antigua (5 travesaños) y altura monopendiente; WorkBuddy ya tiene la malla canónica y las opciones R1 de techo. Fuente única sugerida para la web: `knowledge/comparisons/r0-model.json` (cuando WorkBuddy lo actualice a dos aguas) + `r1-gable-options.json`.
- El plan [plan-diseno-construccion.md](plan-diseno-construccion.md) de WorkBuddy respeta la numeración canónica de PROJECT.md ✅ y [solicitud-datos.md](../fase1/solicitud-datos.md) es la vía correcta para las respuestas de Carlos.

## D. Método del auditor (reproducible)

Scripts de auditoría en `.tmp/audit_r1.py` y `.tmp/audit_web_beam2.py` (temporales; se pueden promover a scripts/ si se quiere auditoría continua). Vitest ejecutado con el Node del runtime. Ningún archivo ajeno modificado.