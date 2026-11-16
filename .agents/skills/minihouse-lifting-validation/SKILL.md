---
name: minihouse-lifting-validation
description: Comparar enganches, planificar el traslado o preparar y revisar ensayos del módulo MiniHouse. Produce comprobaciones de rigging, transporte y protocolo con registros de medición.
---

# minihouse-lifting-validation

Habilidad del rol [lifting-test-engineer](../../agents/lifting-test-engineer.md). Cargar antes de comparar izajes, planificar transporte o preparar ensayos.

## Procedimiento

1. **Masas y CG verificados.** No planificar con la masa hipotética del informe (3 000 kg). Configuración exacta de transporte: depósitos, baterías, desmontables. CG 3D con incertidumbre declarada; z_G por inventario fiable o procedimiento de inclinación.
2. **Comparar variantes de izaje.** Nudos superiores vs base, misma masa y restricciones. Por variante: recorrido de carga completo, fuerza por punto (con desigualdad de ramales y dinámica), excentricidad respecto al centroide del perfil, deformación de aberturas y torsión del bastidor. Decidir con el análisis estructural, no por precedente.
3. **Geometría del aparejo.** T = V/sen α, H = V·cot α (α desde la horizontal). Ángulos bajos castigan el chasis: cuantificar H. Evaluar spreader/balancín para verticalizar ramales; un accesorio fabricado ad hoc puede caer bajo EN 13155:2020+A1:2025 (resistencia estática, estabilidad, fatiga). Posición del gancho sobre el CG, holguras, viento, radio y capacidad de grúa con la tabla real del equipo.
4. **Transporte.** EN 12195-1 para amarre (bloqueo, amarre directo/fricción, vuelco). Coeficientes del vehículo y ruta reales. Anchura ≈ 3 m: comprobar lista de carreteras de Statens vegvesen y transporte especial si aplica. Apoyos sobre remolque ≠ amarres ≠ puntos de izaje: plano con los tres.
5. **Protocolo de ensayo (criterios ANTES de ensayar).**
   - Probeta de nudo: recorrido de carga completo (oreja + perfil + conexión), F–δ, deformación permanente, modo de fallo; nº de probetas y factores estadísticos fijados a priori.
   - Chasis: flecha en centros/esquinas, diagonales, giro torsional, residual tras descarga; caso simétrico + caso excéntrico.
   - Pesaje: 4 células calibradas → W, x_G, y_G; certificados de calibración vigentes.
   - Izaje instrumentado: células en ramales, inclinómetro; criterios de parada definidos.
   - Recorrido piloto: acelerómetros triaxiales (remolque + módulo), diagonales en paredes y techo/piso, inspección antes/después de puertas, ventanas, sellos y revestimientos.
6. **Registro y correlación.** Cada medición vinculada a caso, configuración y revisión del modelo. Entregar a structural-engineer para el modelo "as-tested"; ajustar rigidez sólo con justificación física.
7. **Autoridad.** El lift plan y la maniobra real los aprueba y ejecuta la empresa competente de izaje bajo normativa noruega (Arbeidstilsynet). Esta habilidad prepara requisitos, comprobaciones y protocolos; no autoriza izajes.

## Verificación de cierre

Cada variante tiene fuerzas con dinámica y desigualdad incluidas; el protocolo fija aceptación y parada antes de medir; los registros ligan medición ↔ caso ↔ revisión; ningún WLL se selecciona con números estáticos ideales.