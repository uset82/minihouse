# MiniHouse · Plan detallado de diseño y construcción (revisado)

Estado: **propuesta operativa reconciliada con el proyecto**, 2026-11-16. Este documento mejora el borrador generado por ChatGPT; **no sustituye** a [PROJECT.md](../PROJECT.md), que conserva la numeración oficial de fases. La fase canónica activa sigue siendo **Fase 1 · Datos y viabilidad**.

**Estado técnico general:** CONCEPTUAL — NO PARA FABRICACIÓN NI PARA AUTORIZAR IZAJE. Ninguna casilla se marca como cerrada sin evidencia guardada.

## 0. Qué se cambió frente al borrador de ChatGPT

| Punto | Borrador ChatGPT | Revisión aplicada |
|---|---|---|
| Numeración de fases | Crea Fases 1–6 de diseño/construcción | Se conservan las Fases 0–4 de `PROJECT.md`; las seis fases del borrador se mapean como subflujos. La web sigue siendo Fase 4. |
| Uso y mercado | "Pendientes de definir" | Ya declarado por Carlos: **Noruega, principalmente Bergen**; **casita de emergencia**, con clase legal aún por precisar. |
| Techo | "Dos aguas en la maqueta, pendiente de comparar" | Intención confirmada por imágenes: **techo a dos aguas**, acabado metálico oscuro; **pendiente sin acotar**. El monopendiente +200 mm de R0 queda sólo como marco de coordenadas. |
| Normativa | Enlaces generales | Se distinguen requisitos verificados (TEK17, Lovdata, DIBK mikrohus) de bloqueos reales: National Annex, NS 3031 y texto de NS-EN 1090-2. |
| Izaje | Checklist amplio pero sin estatus legal | Se separan puntos de apoyo, amarre e izaje; se añaden requisitos verificables de ESTA y se mantiene que el plan real lo firma la empresa competente. |
| Datos | Mezcla datos provisionales y tareas | Cada dato se etiqueta como **declarado**, **confirmado**, **supuesto R0**, **medido** o **pendiente**, con fuente y revisión. |

## 1. Reglas de trabajo

1. Lee [PROJECT.md](../PROJECT.md), [AGENTS.md](../AGENTS.md), [rules.md](../rules.md) y [skills.md](../skills.md) antes de ejecutar tareas.
2. Registra cada dato como **declarado**, **confirmado**, **provisional**, **medido** o **pendiente**. Indica fuente, fecha y revisión del modelo que lo consume.
3. Marca una casilla sólo cuando exista evidencia: plano acotado, cálculo verificable, medición, acta o decisión registrada.
4. Si falta un dato, anota qué decisión bloquea y continúa con las tareas verificables de la fase.
5. No uses las imágenes de referencia para sacar cotas. Son intención visual, no geometría.
6. Un resultado de cálculo no autoriza fabricación ni maniobra; la liberación corresponde al ingeniero responsable y a la empresa de izaje competente.

## 2. Datos ya registrados y supuestos activos

| Dato | Estado | Fuente / consecuencia |
|---|---|---|
| Un módulo transportable entero | Declarado | [PROJECT.md](../PROJECT.md); define U/T/I como una sola unidad |
| 6 000 × 3 000 mm exteriores aproximados | Declarado/provisional | Huella exterior declarada en el encargo; salientes y cota final abiertas (C-02) |
| Estructura primaria de acero; madera recuperada en envolvente | Declarado | La madera recuperada no entra como portante sin propiedades documentadas |
| Mercado Noruega, principalmente Bergen | Declarado por Carlos, 2026-11-16 | C-01 parcial; define clima, ruta y marco normativo |
| Uso: casita de emergencia | Declarado por Carlos, 2026-11-16 | C-01 parcial; clasificación TEK17/SAK aún pendiente |
| Techo a dos aguas, chapa metálica oscura | Declarado por referencias visuales | [S016](../knowledge/sources/S016.md); pendiente y altura transporte sin acotar |
| R0: H total 3 200 mm, libre 2 400 mm, monopendiente +200 mm | Supuesto R0 | Sólo marco de ejes; S-03 revisado en [registro de decisiones](../fase1/registro-decisiones.md) |
| Ancho ≈3 m como carga indivisible | Hallazgo verificado | Banda noruega 2,55–3,25 m; exige comprobar vegliste/veggruppe y transportista |
| Coeficientes del National Annex y NS 3031 | Bloqueados | [S014](../knowledge/sources/S014.md); impiden cerrar el dimensionamiento de miembros y la energía del proyecto final |
| Texto NS-EN 1090-2 | No disponible | [S019](../knowledge/sources/S019.md); no se hacen afirmaciones de EXC, soldadura o inspección |

## 3. Mapa entre el borrador de ChatGPT y el plan canónico

| Fase del borrador | Contenido útil | Destino en `PROJECT.md` |
|---|---|---|
| Fase 1 · Uso, terreno y presupuesto | Uso, ocupación, espacios, parcela, traslados, presupuesto | **Fase 1** · Datos y viabilidad |
| Fase 2 · Planta y dimensiones de transporte | Dos plantas, alzados/corte, configuración de viaje, ruta y grúa | **Fase 1** para datos de partida; **Fase 2** para verificación |
| Fase 3 · Materiales, instalaciones y peso | Secciones, encuentros, inventario recuperado, instalaciones, masa y CG | **Fase 1** para inventario; **Fase 2** para cálculo |
| Fase 4 · Chasis, esquinas, apoyos e izaje | Casos U/T/I, dos variantes, rigidez, plan de puntos | **Fase 2** · Cálculo y modelo |
| Fase 5 · Planos de taller y construcción | Modelo coordinado, detalles, BOM, secuencia, revisión | **Fase 3** · Prototipo, ensayos y taller |
| Fase 6 · Ensayo y primer traslado | Pesaje, izaje de prueba, primer viaje, as-built | **Fase 3** · Prototipo, ensayos y taller |
| No incluida en el borrador | Sitio documental y asistente web | **Fase 4** · Web, según `PROJECT.md` |

---

## Fase 1 · Datos y viabilidad

### 1A. Uso, ocupación y clasificación legal

- [ ] Confirmar la clasificación jurídica de "casita de emergencia": vivienda habitual, alojamiento temporal o unidad de emergencia a efectos TEK17/SAK. (C-01; bloquea clase de uso, nieve/viento, energía y documentación.)
- [ ] Si resulta aplicable el régimen de **mikrohus**, comprobar condiciones oficiales: hasta **30 m² BRA**, una vivienda, una planta sin sótano, altura máxima **4,5 m**, altura libre reducida a **2,2 m**, funciones de aseo, dormir, cocina, baño y estar, energía mínima y documentación. Fuente: [DIBK, regler for mikrohus](../knowledge/sources/S018.md). No aplicar el régimen por el tamaño sin antes cerrar C-01.
- [ ] Confirmar con el municipio de Bergen planeamiento, ubicación permitida, acceso, aparcamiento, agua, alcantarillado, residuos, distancia a linderos y condición del terreno. El régimen mikrohus no elimina la plan- og bygningsloven.
- [ ] Definir ocupación simultánea y número de plazas para dormir.
- [ ] Escribir los espacios y equipos imprescindibles: cama, aseo, cocina, mesa, almacenamiento, espacio técnico y almacenamiento de agua si aplica.
- [ ] Fijar frecuencia prevista de traslados y qué elementos se desmontan antes de mover la casita: escalera, terraza, paneles, depósitos o conexiones.
- [ ] Definir presupuesto objetivo en NOK separando materiales, taller, instalaciones, revisión técnica, transporte, grúa, permisos y contingencia.

**Evidencia:** ficha de uso y viabilidad con clasificación legal, ocupación, programa, lugar, frecuencia de traslados y presupuesto. Fuente de cada dato y C-01…C-09 actualizados.

**Cierre de fase parcial:** uso y capacidad definidos; condiciones del sitio que afectan la planta confirmadas o registradas como pendientes.

### 1B. Planta, alzados y envolvente de referencia

- [ ] Dibujar dos plantas acotadas dentro de la envolvente preliminar, con puertas, ventanas, mobiliario, instalaciones y circulación.
- [ ] Calcular el espacio interior descontando espesores preliminares de muros y revestimientos; acotar anchos libres en los pasos principales.
- [ ] Dibujar dos elevaciones y un corte con chasis, nivel de piso terminado, cubierta, pendiente del tejado a dos aguas y elementos más salientes.
- [ ] Comparar las dos plantas por espacio útil, comodidad, luz natural, recorrido de instalaciones, posición de masas pesadas y posibilidad de arriostrar muros.
- [ ] Elegir una planta y justificar la decisión; reservar espacio para estructura y acceso a instalaciones.
- [ ] Acotar longitud, ancho y altura máximos en configuración de traslado, incluyendo cubierta, aleros, herrajes y todo lo que viaje montado. (C-02.)
- [ ] Redibujar R0 como R1 con tejado a dos aguas una vez acotada la pendiente. No extraer la pendiente de las imágenes.
- [ ] Definir secciones constructivas de piso, muro y cubierta: estructura, aislamiento, barreras, cámara ventilada y acabados, conforme a clima de Bergen.
- [ ] Resolver encuentros chasis–piso–pared–cubierta: drenaje, protección del acero, ventilación de fachada, acceso para inspección y sustitución de madera exterior.
- [ ] Aplicar la estrategia húmeda ya verificada: fachada ventilada, barrera de vapor en lado caliente `Sd ≥ 10 m`, barrera de viento vapour-open y secado por ventilación ([module brief](../knowledge/comparisons/module-brief.md)).

**Evidencia:** plantas y corte acotados, ficha de configuración de transporte y secciones de envolvente con revisión.

### 1C. Materiales, instalaciones y masa

- [ ] Inventariar madera recuperada por lote, dimensión, especie si se conoce, origen, estado, humedad y uso propuesto. Registrar idoneidad; si es portante, documentar propiedades o dejarla fuera del modelo estructural.
- [ ] Coordinar ventilación, calefacción, electricidad, agua y desagüe según la clasificación de uso; reservar espacio y acceso de mantenimiento. Verificar requisitos TEK17 §13-2, §13-9 y §13-13 ya registrados.
- [ ] Definir conexión/desconexión de servicios y configuración de viaje de depósitos, baterías, muebles y equipos.
- [ ] Crear hoja de masas por componente con cantidad, masa unitaria, masa total, posición X/Y/Z, fuente y estado del dato. Usar la plantilla [inventario-masas.csv](../fase1/inventario-masas.csv), no el archivo de ejemplo como dato del proyecto.
- [ ] Incluir acero, piso, paredes, cubierta, puertas, ventanas, baño, cocina, equipamiento y contenido previsto durante el traslado. (C-07.)
- [ ] Calcular masa total y CG preliminares con [masas_cg.py](../scripts/masas_cg.py); estudiar sensibilidad al mover baterías, depósitos u otros elementos pesados.
- [ ] Comparar masa estimada con el presupuesto de peso acordado con transportista y empresa de grúa; registrar margen y componentes de mayor incertidumbre.
- [ ] Verificar la compatibilidad energética sólo cuando exista clasificación y acceso a NS 3031. Hasta entonces registrar la obligación, no un resultado.

**Evidencia:** inventario con procedencia, hoja de masas, cálculo reproducible de CG y ficha de configuración de carga.

**Cierre de Fase 1:** uso, clasificación de trabajo, planta preliminar, configuración de transporte y masa/CG preliminares registrados. La clasificación legal completamente incierta se mantiene como bloqueo explícito, no como supuesto oculto.

---

## Fase 2 · Cálculo y modelo

### 2A. Casos, carga y estructura

- [ ] Dibujar el recorrido de cargas desde cubierta, paredes y piso hacia postes, largueros, travesaños y apoyos. Mostrar cómo se mantiene la escuadra alrededor de puertas y ventanas.
- [ ] Definir los casos **U** (instalada), **T** (transporte) e **I** (izaje) con acciones y combinaciones correspondientes, según [condiciones-transporte-izaje.md](../fase1/condiciones-transporte-izaje.md).
- [ ] No aplicar `W/4` a cuatro apoyos o cuatro eslingas sin demostrar reparto: cuatro puntos no implica determinación estática ni igualdad de fuerzas.
- [ ] Modelar dos configuraciones con las mismas masas y CG: **I-1 nudos altos** e **I-2 base**. Evaluar también spreader si la geometría o la estabilidad lo requieren.
- [ ] Para cada variante comprobar recorrido de eslingas, reacciones, reparto con CG excéntrico, estabilidad y deformación relativa de huecos.
- [ ] Verificar flexión y torsión del conjunto, uniones de esquina, puntos de izaje y marcos de puertas/ventanas frente a límites acordados **a priori** por el ingeniero responsable.
- [ ] Contrastar el modelo con equilibrio, reacciones y flexión independientes; documentar unidades, cargas, hipótesis, solver, revisión y diferencias.
- [ ] Comprobar el intercambio de un archivo de prueba en la versión instalada de Autodesk. Si no está disponible, mantener la ruta IFC/SMLX documentada en [autodesk-exchange.md](../knowledge/comparisons/autodesk-exchange.md) y no afirmar que el enlace fue probado.

### 2B. Requisitos de izaje y transporte — checklist, no plan autorizado

Basado en [lift-plan-checklist.md](../knowledge/comparisons/lift-plan-checklist.md), [D003](../knowledge/derivations/D003.md), SCI P272 (S008) y ESTA GD25001-EN (S017).

- [ ] Obtener masa real y CG 3D de la configuración de viaje; verificar con pesaje acordado. Sin este dato no hay plan de izaje válido.
- [ ] Entregar a la empresa de izaje: masa, CG, dimensiones, número/capacidad/posición de puntos de izaje y coeficiente/área de viento de la carga. ESTA §3.2 lo exige como entrada del plan.
- [ ] Calcular eslingas con `T = V/sin α` y `H = V·cot α`, con α medido desde la horizontal; incluir longitudes desiguales, pretensado y factor dinámico fijado por el especialista.
- [ ] Comprobar el triángulo de estabilidad de eslingas en todas direcciones. Si los puntos quedan por debajo del CG, tratar la operación como **crítica** (ESTA §3.4.1).
- [ ] Calcular el área expuesta al viento y aplicar el límite de velocidad definido por la empresa de izaje. ESTA advierte que sobre ~1,2 m²/t los valores de la ficha de la grúa dejan de bastar.
- [ ] Evaluar daño en esquinas superiores si se elige I-2, posibilidad de retirar las eslingas después de apoyar y uso de spreader.
- [ ] Dibujar en un único plano revisado los tres tipos de punto: **apoyo**, **amarre** y **izaje**. No suponer que coinciden.
- [ ] Confirmar con transportista: apoyos, amarres, vehículo, plataforma, ruta, vegliste/veggruppe y VegSak si hace falta dispensación.
- [ ] Confirmar con empresa de izaje: grúa, tabla de carga, radio, altura de gancho, aparejo, condiciones de viento, suelo, señalización y competencias conforme a Lovdata §§10 y 13.
- [ ] Exigir como entregable real los tres dibujos de ESTA §5.3: **lifting arrangement**, **rigging arrangement** y **(dis)assembly arrangement**, con estado, revisión, carga, CG, dimensiones, viento máximo, presión de suelo, materiales y estabilidad del aparejo.
- [ ] Registrar evaluación de riesgos, method statement, toolbox talk y gestión de cambios. Cualquier cambio después de la aprobación vuelve a revisión antes de reanudar.
- [ ] Mantener cuatro límites de deformación acordados antes del ensayo: piso, diagonal de hueco, torsión diferencial de esquina y deformación local del punto de izaje.

### 2C. Bloqueos de cálculo y cumplimiento

- [ ] Obtener acceso autorizado a los National Annex noruegos antes de usar coeficientes `γ`, `ψ`, `α`, curvas de pandeo o parámetros de nieve/viento. Estado actual: **bloqueado** (S014).
- [ ] Obtener NS 3031:2014 antes de afirmar cumplimiento energético TEK17 §14-2. Estado actual: **bloqueado**.
- [ ] Obtener texto autorizado de NS-EN 1090-2 antes de fijar clase de ejecución, soldaduras, tolerancias e inspección. Estado actual: **bloqueado** (S019).
- [ ] Confirmar si se requiere fatiga EN 1993-1-9 según número real de traslados (C-03).
- [ ] Elegir y registrar la alternativa estructural y de izaje que pasa a prototipo, con sus hipótesis y revisiones.

**Evidencia:** modelo, memoria de cálculo, comparativa I-1/I-2, plano de interfaces y matriz de cumplimiento actualizada.

**Cierre de Fase 2:** configuración elegida con cargas y verificaciones documentadas; posiciones de enganche, apoyo y amarre coincidentes entre cálculo y plano. Sin NA, NS 3031 y NS-EN 1090-2 no se emite liberación de fabricación.

---

## Fase 3 · Prototipo, ensayos, taller y primer traslado

### 3A. Detalle y fabricación

- [ ] Completar modelo 3D coordinado: dimensiones, huecos, instalaciones y geometría estructural en la **misma revisión**.
- [ ] Preparar planos de conjunto, despiece del chasis, detalles de esquina, uniones, enganches, apoyos, amarres y encuentros de envolvente.
- [ ] Indicar materiales, dimensiones, tolerancias, uniones, soldaduras y protección anticorrosiva **sólo después** de definir la clase de ejecución con texto autorizado y revisión del ingeniero.
- [ ] Separar la lista de materiales en compra, recuperación y fabricación; actualizar coste y masa estimados.
- [ ] Definir secuencia de montaje con el taller: control de diagonales, nivelación, posición de huecos y acceso a uniones que quedarán cubiertas.
- [ ] Preparar el plan de ensayo con ingeniero y empresa de grúa: configuración de carga, puntos de medición, instrumentación, cargas, criterios de parada y aceptación fijados antes del ensayo.
- [ ] Obtener revisión del ingeniero estructural responsable y resolver observaciones antes de emitir planos de chasis para fabricación.
- [ ] Fabricar e inspeccionar el chasis; registrar medidas reales y diferencias respecto al plano.
- [ ] Montar envolvente, carpintería, instalaciones y equipamiento; actualizar planos según lo construido y registrar cambios que afecten masa, geometría o uniones.

### 3B. Ensayo y primer traslado

- [ ] Verificar dimensiones finales en configuración de traslado; comparar con ficha y registrar salientes.
- [ ] Pesar el módulo terminado; verificar CG con el método acordado; actualizar cálculo y ficha de izaje con datos reales.
- [ ] Inspeccionar chasis, enganches y uniones; registrar estado de puertas, ventanas, acabados y diagonales antes de la maniobra.
- [ ] Ejecutar izaje de prueba con equipo competente y según su plan aprobado; registrar cargas y deformaciones en los puntos acordados.
- [ ] Comparar mediciones con modelo y criterios de aceptación; corregir desviaciones y repetir verificaciones correspondientes.
- [ ] Confirmar ruta, plataforma, apoyos, amarres y acceso a destino con el transportista antes de salir.
- [ ] Realizar primer traslado y colocación sobre apoyos preparados; registrar daños, deformaciones y cambios en uniones, puertas y ventanas.
- [ ] Guardar planos as-built, peso y CG verificados, resultados de ensayo y ficha de preparación para futuros traslados.

**Evidencia:** modelo revisado, planos de taller, acta de fabricación, informe de pesaje/izaje y registro del primer traslado.

**Cierre de Fase 3:** casita documentada según lo construido; maniobra evaluada con criterios acordados; correcciones resueltas. Nada se considera autorizado por este documento.

---

## Fase 4 · Web

La Fase 4 permanece según [PROJECT.md](../PROJECT.md): audiencia y medios autorizados, diseño responsive, navegación, contraste, accesibilidad y rendimiento antes de publicar. Los avances de ingeniería pueden publicarse sólo con estado y revisión; no exponer planos, pesos o detalles de izaje no aprobados.

## 4. Bloqueos activos y próximas decisiones

| Prioridad | Bloqueo o decisión | Por qué importa |
|---|---|---|
| 1 | C-01: clasificación legal y emplazamiento exacto en Bergen | Define TEK17/SAK, nieve, viento, energía y documentación |
| 2 | C-02: cotas exteriores finales, salientes, pendiente del tejado y altura de transporte | Define geometría R1 y gálibo |
| 3 | C-07: equipos, baterías, depósitos en litros y contenido durante traslado | Define masa y CG; sin ello no hay plan de izaje |
| 4 | National Annex noruegos y NS 3031 | Impiden coeficientes de código y verificación energética |
| 5 | NS-EN 1090-2 autorizado y alcance de clase de ejecución | Impiden emitir detalles de soldadura/inspección |
| 6 | C-03/C-04/C-06: ruta, grúa y vehículo | Cierran variante de izaje, amarre, permisos y fatiga |

Para responder de forma ordenada usa la [solicitud priorizada de datos](../fase1/solicitud-datos.md). Mientras llega C-02, la [sensibilidad R1 de tejado a dos aguas](../fase1/r1-opciones-techo.md) cuantifica 5°/10°/15°/20° sin seleccionar pendiente ni congelar geometría.

## 5. Fuentes bases

- [PROJECT.md](../PROJECT.md) y [registro de decisiones Fase 1](../fase1/registro-decisiones.md)
- [DIBK mikrohus (S018)](../knowledge/sources/S018.md); [TEK17 §10-2 (S005)](../knowledge/sources/S005.md); [Lovdata izaje (S013)](../knowledge/sources/S013.md)
- [ESTA GD25001-EN (S017, PDF local)](../knowledge/sources/S017.md); [SCI P272 (S008)](../knowledge/sources/S008.md)
- [National Annex status (S014)](../knowledge/sources/S014.md); [NS-EN 1090-2 status (S019)](../knowledge/sources/S019.md)
- [Matriz de cumplimiento](../knowledge/comparisons/compliance-matrix.md); [checklist de izaje](../knowledge/comparisons/lift-plan-checklist.md); [brief arquitectónico](../knowledge/comparisons/module-brief.md)
