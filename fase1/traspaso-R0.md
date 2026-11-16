# Traspaso Fase 1 → Fase 2 · R0

Fecha: 2026-11-16 · De: architectural-modeler + lifting-test-engineer (preparación) · A: structural-engineer, autodesk-bim-coordinator · Estado: conceptual.

## Archivos entregados (revisión R0)

| Archivo | Contenido | Verificación ejecutada |
| --- | --- | --- |
| [registro-decisiones.md](registro-decisiones.md) | Datos fijados / supuestos S-01…S-08 / preguntas C-01…C-09 / hallazgo de ancho de transporte con fuentes | Fuentes web citadas; coherencia interna revisada |
| [geometria-R0.md](geometria-R0.md) | Ejes, origen, unidades, cotas, candidatos de izaje | Consistente con S-01…S-08; pendiente de techo corregida a ≈3,8° (+200/3000) |
| [planos/planta-R0.svg](planos/planta-R0.svg), [alzado-long](planos/alzado-long-R0.svg), [alzado-trans](planos/alzado-trans-R0.svg) | Planos conceptuales acotados, CONCEPTUAL — NOT FOR FABRICATION | Cotas derivadas de las mismas cifras R0 |
| [tabla-aberturas.csv](tabla-aberturas.csv) | P-01, V-01…V-03 con posición y gobernancia de diagonal | Posiciones coinciden con planta SVG |
| [inventario-masas.csv](inventario-masas.csv) | Plantilla vacía con columnas obligatorias | La calculadora la rechaza limpiamente (masa nula) |
| [inventario-masas-ejemplo.csv](inventario-masas-ejemplo.csv) | 12 filas de ejemplo, todas marcadas EJEMPLO/estimado | Consumidas por la calculadora en 3 configuraciones |
| [condiciones-transporte-izaje.md](condiciones-transporte-izaje.md) | Casos U-1…I-3, fórmulas, sensibilidad geométrica T/V y H/V, límites funcionales a fijar | Tabla trigonométrica comprobable a mano |
| [../scripts/masas_cg.py](../scripts/masas_cg.py) | CG, W, reacciones 2 estaciones, filtros depósitos/desmontables, avisos de calidad | `--selftest` OK (4 casos cerrados); ejecutado con ejemplo lleno/vacio y apoyos 0–6 / 1,2–4,8; plantilla vacía → error limpio |

## Resultados de la prueba de herramienta (NO son datos del módulo)

Ejemplo 2 200 kg (lleno): CG x=2,545 / y=1,471 / z=0,741 m; R_A=12,429 kN, R_B=9,153 kN con estaciones 0/6. Vacío 2 100 kg: CG x=2,637 m. Todo estimado; la herramienta avisa que no sirve para seleccionar equipos.

## Datos faltantes que bloquean el cierre de Fase 1

C-01…C-09 del registro (destino, uso, cotas definitivas, ruta, grúa, apoyos, remolque, equipos, madera, croquis). Sin ellos no se congela geometría ni masas.

## Pendientes técnicos registrados

- Sección de largueros/travesaños SIN DEFINIR (EI del informe no identifica perfil).
- Sin paredes colaborantes en el modelo inicial (S-07, propuesta).
- Límites de deformación funcionales: propuesta de tabla, valores a fijar con el ingeniero antes de Fase 2.
- Nativo CAD/IFC de R0: pendiente de herramientas Autodesk (primera casilla de Fase 2).
- Repetir comprobación de carga en otros IDEs (Fase 0, mismo criterio).