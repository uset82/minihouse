# Condiciones de transporte, izaje y uso · hoja de trabajo R0

2026-11-16 · Roles: lifting-test-engineer + structural-engineer · Estado: **conceptual**. Esta hoja fija la *estructura* de casos y las fórmulas que se aplicarán; los valores llegan con C-01…C-09 del [registro de decisiones](registro-decisiones.md). Ningún número de aquí selecciona equipos.

## 1. Situaciones de proyecto (EN 1990 — transitorias explícitas)

| Caso | Situación | Configuración de masas | Apoyos/sujeción | Datos que faltan |
| --- | --- | --- | --- | --- |
| U-1 Instalado | Persistente | fijo + uso + nieve + viento | apoyo final (C-05), anclajes | emplazamiento (C-01), suelo, nieve/viento NA |
| U-2 Nivelación/montaje | Transitoria | fijo, depósitos vacíos | gatos/puntos provisionales | procedimiento, tolerancias |
| T-1 Transporte rodadura | Transitoria | configuración de viaje (depósitos vacíos por defecto, a confirmar) | apoyos del remolque (C-06) + amarres EN 12195-1 | vehículo, ruta (C-03), aceleraciones |
| T-2 Frenado/lateral | Accidental/transitoria | igual T-1 | amarres + bloqueo | coeficientes EN 12195-1 del vehículo real |
| I-1 Izaje nudos altos | Transitoria | configuración de izaje (sin desmontables sueltos) | 4 ramales candidatos esquina alta z≈3000 | masa/CG verificados, grúa (C-04), ángulos |
| I-2 Izaje desde base | Transitoria | igual I-1 | 4 puntos bajos z≈0, posible spreader | igual I-1 |
| I-3 Izaje excéntrico/2 puntos | Transitoria (ensayo) | igual I-1 | caso de sensibilidad para torsión | decisión del ingeniero |

Reglas de combinación: coeficientes γ y ψ del anexo nacional noruego **sólo** tras fijar situación y confirmar NA vigente. Izaje nunca dentro del caso permanente.

## 2. Transporte (Noruega)

- Ancho R0 ≤ 3 100 mm → banda 2,55–3,25 m de carga indivisible: ver hallazgo D del [registro](registro-decisiones.md) con fuentes. Ruta contra vegliste/veggruppe; dispensación VegSak si aplica (IKKE u otros excesos).
- Amarre: EN 12195-1 con masas de la configuración T-1 y coeficientes del vehículo real; distinguir carga estable vs susceptible de vuelco; comprobar deslizamiento, vuelco y amarre directo. **Pendiente**: tipo de plataforma, puntos de amarre certificados, STF/LC de las cinchas.
- Plano obligatorio antes del primer viaje: apoyos de remolque ≠ puntos de amarre ≠ puntos de izaje (los tres marcados, con revisión).
- Fatiga: número de traslados previstos (C-03) decide si procede EN 1993-1-9.

## 3. Izaje — geometría y comparativa (a completar con masa verificada)

Fórmulas fijadas (α desde la horizontal): T = V/sen α; H = V·cot α.

Tabla de sensibilidad **puramente geométrica** por ramal, con V unitario (V=1 kN), para ver el castigo del ángulo — no son fuerzas del módulo:

| α | T/V | H/V |
| --- | --- | --- |
| 90° (vertical, con spreader) | 1,000 | 0,000 |
| 60° | 1,155 | 0,577 |
| 45° | 1,414 | 1,000 |
| 30° | 2,000 | 1,732 |

Con 4 ramales, el reparto real es desigual (tolerancias de longitud, rigidez, CG excéntrico): el caso de diseño debe cubrir al menos el patrón 2 ramales efectivos + dinámica, con el factor que fije el especialista de izaje. H en ángulos bajos comprime el chasis y flexiona las paredes: se compara I-1 vs I-2 con el modelo de Fase 2.

Criterios de comparación I-1 vs I-2 (mismas masas): fuerza máxima por punto, H sobre largueros, cambio de diagonal en P-01/V-01…V-03, torsión diferencial de esquinas, excentricidad oreja-perfil (M_e = F·e), accesibilidad de inspección, necesidad y peso del spreader (EN 13155 si es accesorio fabricado).

**Pendiente crítico**: W y CG verificados (inventario real + pesaje), z_G, grúa y radio (C-04), viento admisible de maniobra, altura de gancho disponible.

## 4. Límites de deformación funcionales (propuesta a fijar con el ingeniero)

| Magnitud | Límite propuesto R0 (conceptual) | Justificación |
| --- | --- | --- |
| Flecha de piso en uso | a definir (p. ej. L/300…L/400 como rango de discusión) | confort + acabados |
| Cambio de diagonal de hueco (izaje/transporte) | a definir con fabricante de ventanas/puerta | vidrio y estanqueidad; probable gobernante |
| Torsión diferencial entre esquinas | a definir | marco de puerta y sellos |
| Deformación local en oreja | a definir con el detalle | modo de fallo local |

Estos límites se fijan **antes** del cálculo de Fase 2 y de cualquier ensayo (criterios a priori).

## 5. Traspaso

Cuando lleguen C-01…C-09: congelar configuración de masas por caso → rellenar inventario real → calculadora ([scripts/masas_cg.py](../scripts/masas_cg.py)) → matriz de acciones con NA → cálculos manuales → Fase 2. La liberación de maniobras reales corresponde a la empresa competente de izaje; la del cálculo al ingeniero responsable.