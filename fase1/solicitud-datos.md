# MiniHouse · Solicitud priorizada de datos (Fase 1)

Estado: **abierta** · 2026-11-16 · Complemento de [registro-decisiones.md](registro-decisiones.md). Sirve para recibir las respuestas C-01…C-09 sin mezclarlas con supuestos. No cierra ninguna casilla por sí sola: cada respuesta se verifica y se registra con fuente.

## Cómo responder

- Puedes responder sólo lo que tengas a mano. Escribe **"no lo sé"** o **"pendiente"** donde corresponda; no inventes valores.
- Para cotas y masas, da el valor y su origen: **medido**, **ficha de fabricante**, **estimación** o **decisión**.
- Si un dato es preliminar, indícalo. Lo guardaremos como provisional y no lo usaremos para liberar fabricación.
- Una respuesta puede desbloquear varias tareas; por eso van ordenadas por prioridad.

## P0 · Necesario para cerrar Fase 1

### C-01 · Uso y clasificación legal

| Pregunta | Por qué lo necesitamos |
|---|---|
| ¿La casita será vivienda habitual, alojamiento temporal de emergencia, o un uso distinto? | Define TEK17/SAK, nieve, viento, energía, conjunto del capítulo 13 y documentación. |
| Si se clasifica como mikrohus, ¿qué ventilación se prevé y pueden documentarse las cantidades de aire alternativas de §13-1(1)? | En esa ruta no aplican las tasas de §13-2; hay que justificar calidad de aire, humedad y olores ([S023](../knowledge/sources/S023.md)). |
| Emplazamiento exacto previsto en Bergen: dirección, coordenadas o zona; y si es terreno propio, alquilado o municipal. | Define datos de nieve/viento, accesos, servicios y restricciones municipales. |
| ¿Se prevé ocupación continua o estancias cortas? ¿Cuántas personas y cuántas duermen dentro? | Define ventilación, baño, cocina, masa de equipos y clasificación. |
| ¿El solar está ya edificado? ¿Hay casa existente en la parcela? | El régimen simplificado mikrohus depende de que se coloque en propiedad edificada; no elimina planificación municipal. |
| ¿A qué distancia está el edificio más cercano de otra propiedad? | §11-6 exige **8,0 m** entre edificios bajos salvo medidas equivalentes, y no aplica si ambos forman una sola *bruksenhet*. Puede decidir la parcela ([S024](../knowledge/sources/S024.md)). |
| ¿Hay acceso rodado hasta la puerta principal y boca de incendio o hidrante en la parcela o cerca? | §11-17 admite hasta **50 m** para un edificio pequeño en clase de riesgo 4/BKL 1, con **1 200 l/min** en zona de viviendas unifamiliares y boca a 25–50 m ([S024](../knowledge/sources/S024.md)). |
| ¿Habrá chimenea o estufa con chimenea? | Es excepción conocida al régimen simplificado de responsabilidad. |
| ¿La parcela está en zona marcada en los mapas del NVE (inundación, avalancha, desprendimiento, flujo de derrubios, arcilla rápida)? ¿Y el planeamiento municipal la marca como zona de peligro? | El capítulo 7 aplica íntegro: **F2 = 1/200** y **S2 = 1/1000**. Una zona mapeada puede descartar la parcela antes que cualquier otro requisito ([S026](../knowledge/sources/S026.md), [cribado](cribado-riesgos-naturales.md)). |
| ¿La parcela está **bajo el límite marino**? ¿Hay arcilla rápida conocida en la zona? | Bajo el límite marino la investigación geotécnica es obligatoria **aunque no haya zona mapeada**; el alcance lo fija una *tiltakskategori* K0–K3 y una vivienda nueva no puede suponerse K0 ([S026](../knowledge/sources/S026.md)). |
| ¿Hay una cota de inundación 1/200 del sitio, o datos del municipio/NVE? ¿Y una cota de suelo acabado prevista? | La cota de suelo acabado debe superar nivel 1/200 + subida del nivel del mar en la vida útil + margen. El margen es decisión de proyecto, no cifra de TEK17. |
| ¿El plan municipal resuelve el **hábitat seleccionado** en la parcela, o hay que hacer análisis de consecuencias? | §9-4 no exime por tamaño y la letra b) **no es dispensable**. Se responde con el registro de naturabase y el estado del plan ([S027](../knowledge/sources/S027.md)). |
| ¿Hay sospecha de **suelo contaminado** (centro urbano, antiguo vertedero o industria)? | §9-3 obliga a investigar antes de solicitar licencia, y si hay contaminación el plan de actuación municipal debe aprobarse **antes de excavar**. El municipio puede prohibir la obra. |
| ¿La casita se conecta a **red municipal**, o va con **depósito sellado**? | Decide si el 0,90 m de §15-6/§15-8 se cumple con 940 mm de sobra o falla por 160 mm ([S028](../knowledge/sources/S028.md), [cribado](verificacion-instalaciones.md)). |
| ¿Hay **estufa de leña**? ¿Y chimenea con dos caras libres posibles? | Dispara §9-10 (5 o 10 g/kg), §15-1 (45 °C, protección de suelo) y §15-3 (T400, dos caras, feiing) a la vez. |
| ¿La parcela tiene pendiente? ¿Sabes si el terreno es suelo o roca? | En suelo, una pendiente ≥30° ya es marginal con φ≈32°; en roca el riesgo es otro (desprendimiento) y se evalúa de otra forma ([cribado, §4](cribado-riesgos-naturales.md)). |

**Nota verificada:** DIBK define mikrohus como vivienda independiente de hasta 30 m² BRA, una vivienda, una planta sin sótano, altura máxima 4,5 m y altura libre reducida a 2,2 m. Aplica sólo si el uso se clasifica como vivienda; ahora mismo es **condicional**, no decidido. En esa ruta rige §13-1(1), no §13-2 ([S023](../knowledge/sources/S023.md)). Para decidir entre mikrohus, fritidsbolig, edificio temporal u otro, usa la [ayuda de decisión y consulta municipal](clasificacion-uso-decision.md).

**Lo que C-01 ya no bloquea:** el capítulo 11 de incendio da la misma respuesta para vivienda y para fritidsbolig — clase de riesgo 4 y BKL 1 en una planta, con **R 15** ([S024](../knowledge/sources/S024.md)). Sólo cambiaría si la casita acabara clasificada como *arbeidsbrakke* o *skur* (clase de riesgo 1, sin clase de incendio). El capítulo 7 tampoco espera a C-01: **F2** y **S2** nombran vivienda y fritidsbolig en sus listas ([S026](../knowledge/sources/S026.md)).

### C-02 · Geometría final y transporte

| Pregunta | Formato útil |
|---|---|
| Largo y ancho exteriores finales, en mm | `6000 × 3000` o valor real |
| Salientes reales por lado: aleros, herrajes, cubierta, escalera, terraza | Lista por elemento y mm |
| Pendiente deseada del tejado a dos aguas | Grados o relación altura/horizontal; **no** la tomaremos de las imágenes |
| Altura al alero y altura total de cumbrera sobre chasis, en mm | Dos valores |
| Altura libre interior mínima aceptable | mm |
| Vidrio previsto: transmitancia luminosa LT y fracción de marco | `LT 0,6`, `marco 0,85` o ficha del fabricante |
| Altura de antepecho de cada ventana, en mm | Lista por ventana; **≤1 000 mm** si la ventana debe servir de escape |
| ¿Qué elementos viajan montados y cuáles se desmontan? | Lista |

**Por qué importa:** la pendiente y la altura de cumbrera controlan el gálibo, el área de viento, la masa de cubierta y la altura de aparejo. El borrador R0 usa 3 200 mm y monopendiente; ya no es la intención visual. La LT y el factor de marco deciden si los 2,47 m² de vidrio actuales cumplen §13-7. La altura de antepecho decide si una ventana sirve además como **ventana de escape** §11-13(4): alto ≥600 mm, ancho ≥500 mm, alto+ancho ≥1 500 mm y antepecho ≤1 000 mm. Con la tabla actual sólo V-01 cumple ([cribado de incendio](verificacion-incendio.md)).

### C-07 · Masas y configuración de carga

| Dato | Ejemplo de respuesta |
|---|---|
| Baño completo: inodoro, ducha, lavabo, calentador, depósito | `sí/no`, masa o ficha, posición aproximada |
| Cocina: fregadero, placa, frigorífico, armarios | `sí/no`, masa o ficha, posición aproximada |
| Baterías, inversor, paneles, generador | cantidad, masa cada una, posición |
| Depósitos de agua: litros y si viajan llenos o vacíos | `2 × 100 L`, `viajan vacíos` |
| Calefacción, ventilación, bomba, caldera | modelo o masa aproximada |
| Mobiliario que viaja dentro | lista o masa total estimada |
| Masa total objetivo o límite que dio transportista/grúa | kg o NOK por peso |

**Por qué importa:** masa y CG reales son entrada obligatoria de cualquier plan de izaje. La calculadora y el [analizador de sensibilidad](../scripts/mass_sensitivity.py) están listos: necesitan masa **y posición X/Y/Z** de cada componente para clasificar qué datos conviene medir primero. El inventario de ejemplo de 2 200 kg **no** es dato del proyecto y la herramienta lo marca automáticamente como `EJ-`.

## P1 · Necesario para elegir variante y presupuestar

### C-03 · Ruta y frecuencia

- Taller de origen y destino aproximado.
- Distancia y tipo de carretera; si conoces tramos estrechos, puentes bajos o curvas, indícalos.
- Número previsto de traslados al año y vida útil esperada.
- ¿Se traslada con equipos instalados o vacía?

### C-04 · Grúa

- Empresa prevista o tipo de grúa.
- Radio de trabajo disponible y capacidad en ese radio.
- Altura libre sobre el punto de colocación.
- ¿Se acepta spreader o se prefiere izaje directo?

### C-05 · Apoyos finales

- Pilotes, losa, gatos niveladores, zapatas u otro.
- Tipo de suelo y si hay pendiente.
- ¿Se ancla la casita contra viento? ¿Con qué sistema?

### C-06 · Transporte

- Camión/remolque propio o contratado.
- Altura de plataforma y altura de los apoyos de transporte.
- Puntos de apoyo y amarre que el transportista proponga.
- Límites de peso, ancho y altura que haya indicado el transportista.

### C-08 · Madera recuperada

- Cantidad disponible por especie y sección.
- Origen y uso anterior.
- Estado: defectos, humedad medida, tratamientos previos.
- ¿Se quiere utilizar sólo como revestimiento o también como elemento portante?
- **¿El proyecto incluye el derribo del edificio de origen?** Es la pregunta que decide si el plan de residuos de §9-6 aplica: construir la casita no cruza el umbral de 10 t, pero la **agregación de §9-6(2)** con un derribo sí puede ([S027](../knowledge/sources/S027.md), [cribado](verificacion-instalaciones.md)).
- **¿Hay ensayos de la madera?** §9-2 no tiene ruta documental sin fabricante, así que sólo queda el dictamen pericial: pintura con plomo, CCA u otro protector, sellante con PCB, polvo con amianto. Conviene presupuestarlo **antes** de comprar la madera.
- **¿Cómo se sujeta?** §9-5(2) documenta el diseño para desmontaje y la guía dice que **la sujeción es decisiva**: un chasis soldado al bastidor o una membrana pegada hacen el conjunto «difícil de separar» y por tanto poco apto para reutilización.

## P2 · Referencias y decisiones complementarias

- C-09: las dos imágenes ya están registradas como intención. Si hay más vistas, planos o croquis, indícalos; no se tomarán cotas de renders.
- Web: audiencia, idiomas, páginas y si las imágenes pueden publicarse. Esto pertenece a Fase 4 y no bloquea la estructura.

## Plantilla rápida de respuesta

| ID | Respuesta |
|---|---|
| C-01 uso/clasificación | |
| C-01 ubicación | |
| C-01 distancia al edificio más cercano | |
| C-01 acceso de bomberos y agua | |
| C-01 zona de peligro NVE / planeamiento | |
| C-01 bajo el límite marino / arcilla rápida | |
| C-01 hábitat seleccionado en el plan (§9-4) | |
| C-01 sospecha de suelo contaminado (§9-3) | |
| C-01 red municipal o depósito sellado (§15-6) | |
| C-01 estufa de leña y chimenea (§9-10/§15-3) | |
| C-01 cota de inundación 1/200 y cota de suelo | |
| C-01 pendiente y tipo de terreno (suelo/roca) | |
| C-02 largo × ancho | |
| C-02 salientes | |
| C-02 pendiente/altura cumbrera | |
| C-02 antepechos de ventana | |
| C-07 masa total o límite | |
| C-07 equipos pesados | |
| C-03 ruta y traslados | |
| C-04 grúa | |
| C-05 apoyos | |
| C-06 vehículo | |
| C-08 madera | |
| C-08 ¿incluye derribo del origen? (§9-6) | |
| C-08 ¿hay ensayos de la madera? (§9-2) | |
| C-08 ¿cómo se sujeta? (§9-5) | |

## Plantilla de equipos y masas

| id | componente | masa kg | x mm | y mm | z mm | viaja montado | fuente | estado |
|---|---|---:|---:|---:|---:|---|---|---|
| | | | | | | sí/no | medido/ficha/estimado | confirmado/provisional |

## Plantilla de lotes de madera recuperada

| lote | especie | sección mm | longitud mm | cantidad | humedad % | origen | defectos | uso previsto |
|---|---|---|---|---:|---:|---|---|---|
| | | | | | | | | |

## Qué ocurre después de cada respuesta

1. Se registra en [registro-decisiones.md](registro-decisiones.md) con fecha y fuente.
2. Se actualiza el estado del dato: declarado → provisional → medido/confirmado.
3. Se propaga a geometría, inventario de masas, matriz de casos y ficha de transporte.
4. Solo entonces se puede cerrar la casilla correspondiente de Fase 1.
