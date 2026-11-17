# Auditoría cruzada nº 2 · nuevas entregas de WorkBuddy + estado de hallazgos nº 1

2026-11-16 23:58 · Auditor: sesión lead (DSH). Solo lectura sobre archivos ajenos. Continuación de [auditoria-001.md](auditoria-001.md).

## A. Nuevas entregas de WorkBuddy verificadas

### A.1 · clasificacion-uso-decision.md (árbol TEK17 §1-2 + cartas al municipio)

**Veredicto: CORRECTO Y VALIOSO ✅** — es la pieza que convierte "casita de emergencia" en una pregunta respondible.

- Aritmética de la tabla de altura (§4): verificada independientemente contra r1-gable-options.json — pilas máximas 869/735/598/454 mm para 4,00 m coinciden en las 4 pendientes; rango cargado 4031–4846 mm coincide con S022.
- Fuentes primarias comprobadas por el auditor: TEK17 §1-2 y §14-5 existen en DIBK con las URLs citadas (fetch directo; el texto completo queda tras la navegación, pero S020/S021 citan los párrafos literales en noruego y son coherentes entre sí y con la guía mikrohus de DIBK).
- La **corrección energética es real y importante**: §14-5(1) exime del marco §14-2 (100+1600/A) a edificios independientes ≤70 m² BRA calentada; el 188,9 kWh/m²·año que circulaba en notas anteriores NO es un requisito aplicable en las rutas probables. El auditor buscó restos del 188,9 en sus propios archivos (fase2/, fase4/, references/): **ninguno** — la corrección no invalida nada publicado por esta sesión.
- La carta al municipio (ES/NO) y la consulta al transportista son accionables tal cual. **Carlos puede enviarlas hoy.**
- Límite bien declarado: la clasificación la decide el municipio, no el documento.

### A.2 · Reescritura de fase2/comparativa-izaje-R0-resultados.csv (archivo del auditor)

WorkBuddy regeneró el CSV del auditor (23:53) con más decimales en reacciones. **Verificado: las 6 filas se reproducen exactamente desde scripts/chasis_r0.py** (flechas, torsiones, momentos y cada reacción dentro de 0,0006 kN). Cambio benigno, aceptado. Nota de coordinación: el archivo es salida del script del auditor; futuras regeneraciones deberían ejecutando el script, no editando la salida — queda registrado para evitar divergencias script↔CSV.

### A.3 · Edición de docs/estado-del-plan.md (archivo del auditor)

Actualización coherente (19 fuentes, NS 3031 matizado, r0-model.json declarado histórico). Aceptada; el documento sigue siendo el mapa del plan.

### A.4 · r0-model.json

Sigue monopendiente pero ahora **declarado histórico** en estado-del-plan y apuntando a las opciones R1. La divergencia de auditoria-001 §A queda resuelta por declaración (no por edición). Aceptable.

## B. Estado de los hallazgos de auditoria-001 (web de Antigravity)

Revisado el código a las 23:55: **W-1…W-4 siguen abiertos** (hero "1.49 mm [CALCULADO]", BOM "5 crossmembers S355", "Documented Batch", altura 3200). Antigravity hizo cambios en App.tsx/index.html a las 23:50 pero no en MiniHouseFrontPage/3DSimulator. Los hallazgos siguen pendientes de su acción; el informe nº 1 §B tiene las correcciones concretas.

## C. Nuevo riesgo transversal detectado (para los tres agentes)

**Altura de transporte ≈4,0–4,9 m cargado** (S022 + opciones R1): incluso la pendiente más baja (5°) con plataforma de 900 mm supera los 4,00 m generales. Esto puede gobernar el diseño del techo **más que la nieve o la estética**: una cumbrera alta puede forzar transporte especial en cada traslado, o exigir alero más bajo/plataforma más baja/techo desmontable. Debe entrar como restricción de C-02 cuando Carlos decida la pendiente. Registrado aquí para que ningún agente optimice la pendiente sólo por nieve.

## D. Reproducibilidad

- `.tmp/audit_clasificacion.py` (aritmética de alturas) — promover si se quiere continuo.
- Verificación CSV↔solver: ejecutada inline (6/6 filas).
- Suite del proyecto: sigue pasando (verificar_todo.py).

## E. Nota posterior (2026-11-17 00:03, sin reescribir el registro histórico)

Las secciones A y A.3 reflejan el estado a las 23:58 del 2026-11-16. Después de esa auditoría se incorporó **S023** (conjunto aplicable del capítulo 13 TEK17 para mikrohus), por lo que:

- el recuento de fuentes ya no es 19 sino **23**;
- §13-2 no gobierna la ruta mikrohus: rige §13-1(1) con cantidades de aire documentadas;
- el estado del plan y la matriz de cumplimiento quedaron actualizados en consecuencia.

Esta nota existe para evitar que el "19 fuentes" histórico se lea como estado actual; el cuerpo de la auditoría se conserva tal cual.