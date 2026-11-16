# Fase 2 · Preparación R0 · CONCEPTUAL — NOT FOR FABRICATION

2026-11-16/17 · Roles: structural-engineer (preparación de herramientas) · Estado: **conceptual/demostración de flujo**, no cálculo del módulo real.

## Qué hay aquí y qué NO es

Esto **no cumple** las casillas de Fase 2: no hay Robot, no hay masas reales, no hay revisión con ingeniero. Es la infraestructura de verificación independiente lista y probada, más una demostración del flujo de comparación con datos EJEMPLO, para que el día que lleguen C-01…C-09 el cálculo real sea cuestión de sustituir entradas.

## Herramientas verificadas

| Herramienta | Qué hace | Evidencia |
| --- | --- | --- |
| [../scripts/barras3d.py](../scripts/barras3d.py) | Solver propio de barras 3D (6 GDL/nudo, Euler-Bernoulli, EA/EIy/EIz/GJ, cargas distribuidas consistentes) | `--selftest` OK: reproduce los dos casos del informe (24,634 mm y 1,490 mm; M_A −1,766 kNm; M_mid 2,207/11,036 kNm), voladizo y torsión exactos, equilibrio de reacciones |
| [../scripts/chasis_r0.py](../scripts/chasis_r0.py) | Chasis conceptual R0 (2 largueros + 7 travesaños + columnas de izaje), 6 casos A–F | Ejecutado; equilibrio verificado en los 6 casos (suma R = W en todos) |
| [../scripts/masas_cg.py](../scripts/masas_cg.py) | Inventario → W, CG, reacciones (Fase 1) | `--selftest` OK |

Limitaciones declaradas del solver: sin alabeo (perfiles abiertos → SCI P385 o 7º GDL), sin rigidez geométrica, sin releases, uniones rígidas. Para el informe, PyNite sigue siendo la opción recomendada como *segundo* solver cuando haya red/instalación; este solver propio es un tercero reproducible sin dependencias externas más allá de NumPy.

## Demostración A–F (masa EJEMPLO 2 200 kg, RHS provisional inventado)

Resultados: [comparativa-izaje-R0-resultados.csv](comparativa-izaje-R0-resultados.csv). Ramales verticales ideales (spreader perfecto), sin dinámica ni H de eslinga. **Regenerado el 2026-11-16 sobre la malla canónica @1200** (6 travesaños, apoyos B en x=1,2/4,8 exactos; ver [reconciliación](../docs/reconciliacion-R0.md)). El IFC de coordinación también se regeneró con 12 miembros canónicos.

Lecturas **cualitativas** transferibles (los números NO):

1. **D vs C (izaje alto vs bajo)**: con ramales verticales y carga simétrica, el chasis ve casi la misma flexión; la diferencia real aparecerá con H de eslingas, excentricidad de orejas y flexibilidad de uniones — exactamente lo que el modelo R0 no tiene. La decisión de variante necesita el modelo real.
2. **B (apoyos retranqueados 1,2/4,8 exactos)**: flecha 1,158 mm vs 19,155 mm en extremos, mismo orden del fenómeno del informe (su viga ideal daba 1,490 mm; la diferencia es la sección provisional y los travesaños). No valida "1,2 m óptimo".
3. **E (excéntrico)**: el reparto por punto se desplaza (5,89 vs 4,90 kN) — confirma que la herramienta captura asimetría; el caso de diseño real debe cubrir además desigualdad de ramales.
4. **F (2 puntos diagonales)**: torsión diferencial de ~58 mm y flecha ~116 mm con la sección provisional: el bastidor sin diafragma es torsionalmente blando. Esto justifica (a) el caso excéntrico obligatorio en el protocolo de ensayo y (b) estudiar diafragmas/paredes colaborantes en el modelo real.

## Bloqueos de Fase 2 (sin cambios)

- Robot/Advance Steel/AutoCAD/Revit **no instalados** en esta máquina (verificado 2026-11-16: sólo Desktop Connector, CER, Access, Interoperability Engine y FreeCAD 1.1.3). La casilla de intercambio SMLX no puede ejecutarse aquí; FreeCAD existe como opción de geometría/submodelo, no como sustituto del enlace.
- Masas y geometría reales: C-01…C-09 del [registro Fase 1](../fase1/registro-decisiones.md).
- Límites de deformación funcionales: fijar con el ingeniero antes del cálculo real.