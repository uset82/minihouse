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
| ¿La casita será vivienda habitual, alojamiento temporal de emergencia, o un uso distinto? | Define TEK17/SAK, nieve, viento, energía, ventilación y documentación. |
| Emplazamiento exacto previsto en Bergen: dirección, coordenadas o zona; y si es terreno propio, alquilado o municipal. | Define datos de nieve/viento, accesos, servicios y restricciones municipales. |
| ¿Se prevé ocupación continua o estancias cortas? ¿Cuántas personas y cuántas duermen dentro? | Define ventilación, baño, cocina, masa de equipos y clasificación. |
| ¿El solar está ya edificado? ¿Hay casa existente en la parcela? | El régimen simplificado mikrohus depende de que se coloque en propiedad edificada; no elimina planificación municipal. |
| ¿Habrá chimenea o estufa con chimenea? | Es excepción conocida al régimen simplificado de responsabilidad. |

**Nota verificada:** DIBK define mikrohus como vivienda independiente de hasta 30 m² BRA, una vivienda, una planta sin sótano, altura máxima 4,5 m y altura libre reducida a 2,2 m. Aplica sólo si el uso se clasifica como vivienda; ahora mismo es **condicional**, no decidido.

### C-02 · Geometría final y transporte

| Pregunta | Formato útil |
|---|---|
| Largo y ancho exteriores finales, en mm | `6000 × 3000` o valor real |
| Salientes reales por lado: aleros, herrajes, cubierta, escalera, terraza | Lista por elemento y mm |
| Pendiente deseada del tejado a dos aguas | Grados o relación altura/horizontal; **no** la tomaremos de las imágenes |
| Altura al alero y altura total de cumbrera sobre chasis, en mm | Dos valores |
| Altura libre interior mínima aceptable | mm |
| ¿Qué elementos viajan montados y cuáles se desmontan? | Lista |

**Por qué importa:** la pendiente y la altura de cumbrera controlan el gálibo, el área de viento, la masa de cubierta y la altura de aparejo. El borrador R0 usa 3 200 mm y monopendiente; ya no es la intención visual.

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

**Por qué importa:** masa y CG reales son entrada obligatoria de cualquier plan de izaje. La calculadora está lista; el inventario de ejemplo de 2 200 kg **no** es dato del proyecto.

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

## P2 · Referencias y decisiones complementarias

- C-09: las dos imágenes ya están registradas como intención. Si hay más vistas, planos o croquis, indícalos; no se tomarán cotas de renders.
- Web: audiencia, idiomas, páginas y si las imágenes pueden publicarse. Esto pertenece a Fase 4 y no bloquea la estructura.

## Plantilla rápida de respuesta

| ID | Respuesta |
|---|---|
| C-01 uso/clasificación | |
| C-01 ubicación | |
| C-02 largo × ancho | |
| C-02 salientes | |
| C-02 pendiente/altura cumbrera | |
| C-07 masa total o límite | |
| C-07 equipos pesados | |
| C-03 ruta y traslados | |
| C-04 grúa | |
| C-05 apoyos | |
| C-06 vehículo | |
| C-08 madera | |

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
