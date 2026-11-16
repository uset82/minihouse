# Fase 3 · Protocolo de ensayos · BORRADOR R0 (criterios a priori)

2026-11-17 · Rol: lifting-test-engineer · Estado: **borrador conceptual**. Los valores numéricos de aceptación están PENDIENTES del ingeniero responsable; la estructura y el orden se fijan ahora para que ningún criterio se elija después de ver resultados (regla del informe, método McAvoy/QUB).

## Principio

Cada ensayo mide una predicción del modelo. Antes de ensayar se registran: configuración exacta, revisión del modelo, predicción numérica, instrumentación, criterio de aceptación y criterio de parada. Después se registra medición ↔ caso ↔ revisión y la correlación.

## E-1 · Probeta de nudo de izaje (antes del prototipo)

| Campo | Contenido R0 |
| --- | --- |
| Objeto | Oreja + perfil + rigidizador + soldadura/tornillos: **todo el recorrido de carga**, no la placa aislada |
| Predicción | Fuerza de fallo y modo (a calcular con EN 1993-1-8 cuando exista el detalle) |
| Instrumentación | Máquina de tracción con célula calibrada, extensómetro/desplazamiento, fotos |
| Medidas | Curva F–δ completa, deformación permanente tras descarga, modo de fallo observado |
| Nº probetas | PENDIENTE (mínimo 3 por variante como práctica; el ingeniero fija nº y factores estadísticos ANTES) |
| Aceptación | PENDIENTE: F_fallo ≥ factor × F_diseño con el factor fijado a priori |
| Parada | Deformación permanente > umbral fijado, ruido de fisura, inestabilidad del útil |
| Responsable | Taller certificado + tercera parte (p. ej. tipo Oceaneering/STM del informe) |

## E-2 · Chasis completo (sin envolvente primero, después con ella)

| Campo | Contenido R0 |
| --- | --- |
| Casos | Simétrico (4 puntos) + **excéntrico obligatorio** (2 puntos diagonales o carga asimétrica) — el caso F de la [comparativa conceptual](../fase2/README.md) muestra por qué: la torsión no aparece en el simétrico |
| Instrumentación | Comparadores/LVDT en centros y esquinas, medición de diagonales de huecos (P-01, V-01…V-03), inclinómetros en esquinas |
| Medidas | Flecha vertical, cambio de diagonales, giro torsional diferencial, **deformación residual tras descargar** |
| Aceptación | PENDIENTE: límites funcionales de la [hoja de condiciones](../fase1/condiciones-transporte-izaje.md) §4, fijados antes |
| Parada | Residual creciente entre ciclos, crujido de soldadura, cambio de diagonal fuera de umbral |

## E-3 · Pesaje y CG (antes del primer izaje real)

4 células de carga calibradas bajo los apoyos → W = ΣP_i; x_G = ΣP_i·x_i/W; y_G análogo. z_G por inclinación controlada o inventario validado. Certificados de calibración vigentes archivados. Criterio: discrepancia inventario vs pesaje ≤ umbral fijado (propuesta inicial a discutir: 5% en W, 100 mm en x_G/y_G — NO aprobado).

## E-4 · Izaje instrumentado (empresa competente)

Células en ramales + inclinómetro; verificar reparto real vs predicción y actitud del módulo. Criterios de parada: viento, reparto fuera de envolvente prevista, giro no previsto. **La planificación y ejecución son de la empresa de izaje**; este protocolo es requisito de entrada, no autorización.

## E-5 · Recorrido piloto de transporte

Acelerómetros triaxiales en remolque y módulo; diagonales en una pared longitudinal, una transversal y techo/piso; inspección fotográfica antes/después de puertas, ventanas, sellos y revestimientos. Salida: envolvente real de aceleración/deformación para vehículo y ruta (C-03/C-06), correlación con casos T-1/T-2.

## Registro y correlación

Plantilla por ensayo: `ensayo_id, fecha, configuración, revisión_modelo, predicción, medición, residual, aceptación (pasa/no pasa), firmas`. La rigidez del modelo sólo se ajusta con justificación física documentada ("as-tested").

## Bloqueos

Detalle de unión piloto (Fase 2 real), límites funcionales aprobados, empresa de ensayo/izaje contratada, masas reales. Nada de este borrador se ejecuta hasta entonces.