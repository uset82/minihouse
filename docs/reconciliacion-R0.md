# Reconciliación R0 entre sesiones · verificación cruzada

2026-11-16 (ronda 3 del plan) · Rol: structural-engineer + autodesk-bim-coordinator. Esta sesión (lead/DSH) verificó el trabajo de la sesión paralela (WorkBuddy/"Inge") y reconcilió las definiciones de geometría. Nada del trabajo ajeno fue modificado.

## 1. Derivaciones de la otra sesión: RE-EJECUTADAS Y CONFIRMADAS

| Script | Resultado al ejecutarlo aquí | Coincidencia con esta sesión |
| --- | --- | --- |
| [knowledge/derivations/verify_beam.py](../knowledge/derivations/verify_beam.py) (D001, SymPy 1.14.0) | **VERIFIED**: suma simbólica derivación+informe = 0; M_A=−1,766, M_mid=2,207/11,036 kNm; δ=24,634/1,490 mm | Idéntico a los selftests de [scripts/barras3d.py](../scripts/barras3d.py) (solver FEM propio): **dos métodos independientes** (integración simbólica vs rigidez directa) reproducen los mismos números |
| [knowledge/derivations/verify_rigging.py](../knowledge/derivations/verify_rigging.py) (D003) | **VERIFIED**: tabla T/V y H/V (90/60/45/30°) coincide con la de [fase1/condiciones-transporte-izaje.md](../fase1/condiciones-transporte-izaje.md); caso 3000 kg reproduce 8,495/14,715 kN; aviso 4 ramales ≠ W/4 con patrón 2 efectivos ×2 | La tabla de la hoja de condiciones queda verificada por script ajeno independiente |

Nota de entorno: SymPy no estaba en el runtime; se vendorizó sympy 1.14.0 + mpmath en `.tmp/pylibs` (igual que pypdf). Los scripts ajenos se ejecutaron sin modificación.

## 2. Geometría R0: diferencias encontradas y resolución

| Aspecto | Esta sesión (geometria-R0.md original) | Otra sesión (r0_parametric.py / r0-model.json) | Resolución |
| --- | --- | --- | --- |
| Travesaños | Texto decía "5 intermedios + 2 de extremo" (=7) pero el plano SVG dibuja 6 (@1200) | 6 @1200 (0,1200,…,6000) — coherente con el SVG | **Error de texto propio corregido** en geometria-R0.md: 4 intermedios + 2 extremos = 6. La referencia canónica es @1200 |
| Malla del solver/IFC | chasis_r0.py y chasis-R0.ifc usan 7 travesaños @1000 | — | Declarado como **discretización de demostración**, no geometría de referencia (nota añadida en geometria-R0.md). No afecta a conclusiones cualitativas A–F; el modelo real usará la malla_canónica |
| Aberturas | tabla-aberturas.csv | r0-model.json | **Comparadas campo a campo: las 4 coinciden** (id, fachada, centro, antepecho, ancho, alto) |
| JSON publicado vs script | — | knowledge/comparisons/r0-model.json | **Regenerado desde r0_parametric.py y comparado: IDÉNTICO** (el "difieren" inicial era artefacto de encoding del pipe de PowerShell, no del contenido) |
| Marco de ejes, cotas, supuestos S-01…S-08 | geometria-R0.md | r0-model.json | Coinciden (6000×3000×3200, libre 2400, +200 techo, salientes ≤50, baño x 0–1200, largueros y=150/2850, sección SIN DEFINIR) |
| Izaje alto | esquinas z≈3000 candidatas | igual + nota SCI P272: 20% inset (~1200) más estable | Complementario: la nota P272 (fuente primaria ahora local en knowledge/refs/) añade un candidato inset a comparar en Fase 2. Registrado, no adoptado |

## 3. Estado de la fuente única de verdad

- **Geometría de referencia canónica R0**: [fase1/geometria-R0.md](../fase1/geometria-R0.md) (texto corregido) ≡ [knowledge/comparisons/r0-model.json](../knowledge/comparisons/r0-model.json) (verificado idéntico a su script generador).
- Las derivaciones D001–D003 de knowledge/ y los selftests de scripts/ de esta sesión son ahora **verificación cruzada mutua**: ningún número de referencia depende de un solo método.
- Cerrado el 2026-11-16 (ronda 5): IFC y comparativa A–F regenerados sobre la malla canónica @1200 (12 miembros IFC verificados; caso B ahora con apoyos exactos 1,2/4,8 → flecha 1,158 mm; F → torsión 57,9 mm). Pendiente para el modelo real: la sección elegida por cálculo.

## 4. Lo que NO se tocó

`knowledge/`, `scripts/r0_parametric.py`, `web/`, `images/`, `.workbuddy-ai/` — trabajo de la otra sesión, intacto (rules.md: coordinación sobre archivos distintos).

## 5. Actualización R1-intención (2026-11-16, ronda 4)

La otra sesión registró respuestas parciales de Carlos (sección F del registro, fuente S016): mercado **Bergen**, uso **casita de emergencia** (clase legal por precisar), y dos renders ChatGPT que muestran **tejado a dos aguas**. Esta sesión propagó la consecuencia a sus propios archivos:

- [fase1/planos/alzado-trans-R1.svg](../fase1/planos/alzado-trans-R1.svg): nuevo alzado transversal esquemático a dos aguas, pendiente/aleros/cumbrera explícitamente SIN ACOTAR; el R0 monopendiente se conserva como histórico.
- [fase1/geometria-R0.md](../fase1/geometria-R0.md): S-03 marcado como superado (tachado, no borrado); nota en el alzado longitudinal sobre la línea de cumbrera obsoleta; S-01 pendiente de revisión.
- Sitio de Fase 4: tabla de cotas, figura transversal (R1) y diario actualizados; checks automatizados pasan de nuevo (37,3 KB).
- Brief web: imágenes identificadas como aportadas por el propietario (S016); pregunta de clase de uso añadida a las decisiones pendientes.

**No propagado aún (deliberado)**: `knowledge/comparisons/r0-model.json` y `scripts/r0_parametric.py` siguen con S-03 monopendiente — son archivos de la otra sesión, que está activa y ya registró la revisión en sus notas; su actualización le corresponde a ella o a una ronda de coordinación posterior. La divergencia queda declarada aquí para que ningún consumidor del JSON use el techo monopendiente como intención vigente.