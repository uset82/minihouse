# MiniHouse · Plan detallado de diseño y construcción (revisado)

Estado: **propuesta operativa reconciliada con el proyecto**, 2026-11-16. Este documento mejora el borrador generado por ChatGPT; **no sustituye** a [PROJECT.md](../PROJECT.md), que conserva la numeración oficial de fases. La fase canónica activa sigue siendo **Fase 1 · Datos y viabilidad**.

**Estado técnico general:** CONCEPTUAL — NO PARA FABRICACIÓN NI PARA AUTORIZAR IZAJE. Ninguna casilla se marca como cerrada sin evidencia guardada.

## 0. Qué se cambió frente al borrador de ChatGPT

| Punto | Borrador ChatGPT | Revisión aplicada |
|---|---|---|
| Numeración de fases | Crea Fases 1–6 de diseño/construcción | Se conservan las Fases 0–4 de `PROJECT.md`; las seis fases del borrador se mapean como subflujos. La web sigue siendo Fase 4. |
| Uso y mercado | "Pendientes de definir" | Ya declarado por Carlos: **Noruega, principalmente Bergen**; **casita de emergencia**, con clase legal aún por precisar. |
| Techo | "Dos aguas en la maqueta, pendiente de comparar" | Intención confirmada por imágenes: **techo a dos aguas**, acabado metálico oscuro; **pendiente sin acotar**. El monopendiente +200 mm de R0 queda sólo como marco de coordenadas. |
| Normativa | Enlaces generales | Se distinguen requisitos verificados (TEK17, Lovdata, DIBK mikrohus) de bloqueos reales: National Annex y texto de NS-EN 1090-2. El capítulo 13 se aplica por ruta: en mikrohus rige §13-1(1), no §13-2 (S023); NS 3031 sólo si la documentación térmica lo exige. |
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
| Coeficientes del National Annex | Bloqueados | [S014](../knowledge/sources/S014.md); impiden cerrar el dimensionamiento de miembros |
| NS 3031:2014 | No necesario para el marco §14-2 en las rutas probables | [S021](../knowledge/sources/S021.md); puede hacer falta para documentación de pérdidas térmicas/pontees térmicos; no obtenido |
| TEK17 capítulo 13 por ruta | Mikrohus: §13-1(1), §§13-4/5/7 y 13-9…13-16; §13-2 no aplica | [S023](../knowledge/sources/S023.md); si la clasificación final es vivienda ordinaria, vuelven las tasas de §13-2 |
| TEK17 capítulo 11 por ruta | Vivienda y fritidsbolig comparten **clase de riesgo 4 / clase de incendio BKL 1** en una planta; **R 15** rige, no R 30 | [S024](../knowledge/sources/S024.md); la ruta de incendio **no depende** de resolver C-01 entre vivienda y fritidsbolig |
| TEK17 capítulo 12 por ruta | Sólo **ocho** preceptos aplican; accesibilidad y los 2,4 m de altura libre quedan exentos; rige **2,2 m** | [S025](../knowledge/sources/S025.md); el 0,86 m de puerta viene de §11-14, no de §12-13 |
| TEK17 capítulo 7 riesgos naturales | Aplica **íntegro** (capítulos 1–7). Clases fijadas: **F2 = 1/200** (flood) y **S2 = 1/1000** (deslizamiento); no dependen de C-01 | [S026](../knowledge/sources/S026.md); el capítulo condiciona la **parcela**, no la casita. Bajo el límite marino exige investigación geotécnica aunque no haya zona mapeada |
| TEK17 capítulo 9 medio exterior | Aplica **íntegro**, y no es el capítulo de ruido ni de agua: es sustancias peligrosas, suelo, hábitats y **residuos de obra** | [S027](../knowledge/sources/S027.md); **§9-2 no tiene ruta documental sin fabricante**, así que la madera recuperada sólo puede defenderse con un dictamen pericial. **§9-3** es una segunda puerta de emplazamiento |
| TEK17 capítulos 2 y 4 documentación y FDV | Admitidos **íntegros**. Deciden si el análisis del proyecto es **admisible**: §2-2(2) sólo permite análisis donde la norma da función y **no** número; §2-2(3) exige método válido, supuestos descritos y justificados y **márgenes declarados** | [S029](../knowledge/sources/S029.md) y su **veiledning**, ya recuperada en [S030](../knowledge/sources/S030.md); §4-1(2) «medida pequeña y simple» **considerada y rechazada**; el FDV debe ser un archivo versionado, no un archivador |
| TEK17 capítulos 15, 16 y 17 instalaciones | El capítulo 15 **no exime a los edificios pequeños**: §15-1/15-3/15-5/15-6 aplican a la casita. Cuatro determinaciones cierran limpias | [S028](../knowledge/sources/S028.md); el **0,90 m** de §15-6/§15-8 es una profundidad mínima de zanja, y el capítulo 16 es control de ascensores, no documentación |
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

- [ ] Confirmar la clasificación jurídica de "casita de emergencia": vivienda independiente pequeña, fritidsbolig, edificio temporal u otro. Usar la [ayuda de decisión y consulta municipal](../fase1/clasificacion-uso-decision.md). (C-01; bloquea clase de uso, capítulo 13, nieve/viento, energía y documentación.)
- [ ] Si resulta aplicable el régimen de **mikrohus**, comprobar condiciones oficiales: hasta **30 m² BRA**, una vivienda, una planta sin sótano, altura máxima **4,5 m**, altura libre reducida a **2,2 m**, funciones de aseo, dormir, cocina, baño y estar, energía mínima y documentación. Fuente: [DIBK, regler for mikrohus](../knowledge/sources/S018.md). No aplicar el régimen por el tamaño sin antes cerrar C-01.
- [ ] Confirmar con el municipio de Bergen planeamiento, ubicación permitida, acceso, aparcamiento, agua, alcantarillado, residuos, distancia a linderos y condición del terreno. El régimen mikrohus no elimina la plan- og bygningsloven.
- [ ] Aplicar el **cribado de riesgos naturales del capítulo 7** en el orden de puertas A–F ([procedimiento](../fase1/cribado-riesgos-naturales.md)): primero la parcela concreta, después los mapas del NVE (inundación, avalancha, desprendimiento, flujo de derrubios, arcilla rápida), después el **límite marino** y la base de arcilla rápida, y sólo entonces el informe especialista. Clases ya fijadas: **F2 = 1/200** y **S2 = 1/1000** ([S026](../knowledge/sources/S026.md)). Tres reglas que pueden descartar la parcela: si el área de inundación tiene **gran profundidad o corriente fuerte**, el objetivo sube a **F3 = 1/1000**; bajo el límite marino la investigación geotécnica es obligatoria **aunque no haya zona mapeada**; y el techo de ~**50 kPa** limita el diseño *contra* el deslizamiento a eventos pequeños. **Ningún mapa consultado todavía.**
- [ ] Cerrar las **dos puertas de emplazamiento del capítulo 9**, que son independientes del capítulo 7 y no tienen exención por tamaño ([S027](../knowledge/sources/S027.md)). **§9-3 suelo contaminado**: hay que investigar antes de solicitar licencia, y si hay contaminación el **plan de actuación** municipal debe aprobarse **antes de cualquier excavación**; el municipio puede prohibir la obra. **§9-4 hábitats seleccionados**: sólo aplica si existe el reglamento de la ley de biodiversidad, la especie está en el municipio y el plan no lo resuelve — pero entonces el análisis de consecuencias **no es dispensable**. Consultar también el registro de naturabase y el estado del plan. El procedimiento completo está en la [verificación de instalaciones](../fase1/verificacion-instalaciones.md).
- [ ] Decidir si el **proyecto incluye un derribo** que aporte la madera recuperada, porque eso decide si §9-6/§9-8/§9-9 aplican. Construir la casita **no** cruza el umbral de 10 toneladas a ninguna masa plausible (harían falta 33–200 t); lo cruza la **agregación** de §9-6(2) con el derribo de origen. Es una decisión de definición de proyecto y pertenece a C-08.
- [ ] Fijar la **cota de suelo acabado** frente a la inundación: nivel mapeado 1/200 + subida del nivel del mar durante la vida útil + margen explícito. El margen es **decisión de proyecto, no cifra de TEK17**; cada 1 mm/año de subida añade 50 mm en 50 años ([cribado, §3](../fase1/cribado-riesgos-naturales.md)).
- [ ] Comprobar en el sitio los dos requisitos de incendio que dependen de la parcela: **8,0 m** de separación a otros edificios bajos (§11-6) y **50 m** máximos de acceso rodado al ataque del servicio de bomberos, con **1 200 l/min** de capacidad de agua en zona de viviendas unifamiliares y boca de incendio a 25–50 m (§11-17). Pueden decidir la parcela antes que la casita ([S024](../knowledge/sources/S024.md)).
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
- [ ] Redibujar R0 como R1 con tejado a dos aguas una vez acotada la pendiente. No extraer la pendiente de las imágenes. El [esqueleto geométrico R1](../fase2/miembros-R1-opciones.md) ya tiene nudos y barras para 5°/10°/15°/20°, sin secciones ni masas; sirve como base de coordinación, no como modelo estructural.
- [ ] Definir secciones constructivas de piso, muro y cubierta: estructura, aislamiento, barreras, cámara ventilada y acabados, conforme a clima de Bergen.
- [ ] Resolver encuentros chasis–piso–pared–cubierta: drenaje, protección del acero, ventilación de fachada, acceso para inspección y sustitución de madera exterior.
- [ ] Aplicar la estrategia húmeda ya verificada: fachada ventilada, barrera de vapor en lado caliente `Sd ≥ 10 m`, barrera de viento vapour-open y secado por ventilación ([module brief](../knowledge/comparisons/module-brief.md)).
- [ ] Verificar luz diurna §13-7 con la [comprobación actual](../fase1/verificacion-luz-diurna.md): 2,47 m² de vidrio dan LT mínimo 0,510 con marco 1,00 y 0,600 con marco 0,85. Confirmar LT real, factor de marco y BRA final; si no alcanza, añadir vidrio o pasar a simulación de factor de luz diurna ≥2,0 %.
- [ ] Verificar las **ventanas de escape** §11-13(4) con la [comprobación de incendio](../fase1/verificacion-incendio.md) y el [cribado de ventanas](../fase1/verificacion-ventanas.md): alto ≥600 mm, ancho ≥500 mm, alto+ancho ≥1 500 mm, antepecho ≤1 000 mm. Con la tabla actual **sólo V-01 cumple**; V-02 falla por antepecho de 1 100 mm y V-03 falla alto, suma y antepecho. Las **tres lecturas** de §11-13 están valoradas: la unión cuesta **0,29 m²** de vidrio y un antepecho **100 mm** más bajo, y de paso baja el LT mínimo exigido por §13-7 de **0,600 a 0,537**. Ojo con la frase «one accessible escape window is sufficient»: es acceso del **servicio de bomberos** (§11-17), **no** una relajación de «vinduer» en §11-13(4) ([S024](../knowledge/sources/S024.md)).
- [ ] Fijar la **composición de cubierta** contra §11-4(3) nº 6: sin resistencia especificada sólo si la cubierta no es decisiva para la estabilidad en la fase de escape, y mediante 6.1 elemento separador a dos caras, 6.2 todos los materiales de cubierta **incluido aislamiento** A2-s1,d0, o 6.3 revestimiento inferior K210 B-s1,d0 —**K210 D-s2,d0 admitido en clase de riesgo 4**— con aislamiento A2-s1,d0. La opción 6.2 excluye madera y fibra de madera; la 6.3 obliga a lana mineral, y §11-9 D nº 7 exige además un soporte portante **A2-s1,d0** que un par de madera no cumple. Confirmar antes de congelar el techo ([S024](../knowledge/sources/S024.md)).
- [ ] Pasar la **adecuación de los márgenes** por el test que la propia declaración define —positivo **y** mayor que la incertidumbre del modelo— con [el cribado de adecuación](../fase1/verificacion-incertidumbre.md): **ninguna fila pasa**. El margen de **+40 mm** de la puerta no está demostrado (es hoja nominal, no ancho libre: el bastidor y las bisagras se llevan 30–60 mm); dos filas son **nulas por construcción** porque la dimensión se resolvió *hasta* el límite (transporte y U del muro); y la sección es **−498 mm** en el caso peor, no −422. Declarar ancho y separación de bastidor es lo que convierte las filas 5 y 7 en legibles.
- [ ] Confirmar las **clases de superficie** del interior: §11-9 Tabla 1A pide **D-s2,d0** en paredes y techo para una celda de hasta 200 m² en BKL 1, lo que la madera suele cumplir; si el municipio considera toda la casita como *rømningsvei*, sube a **B-s1,d0** y la madera recuperada vista deja de ser aceptable sin tratamiento o documentación ([S024](../knowledge/sources/S024.md)).
- [ ] Fijar la **altura libre** contra §12-7(2)(c) (**2,2 m**; los 2,4 m de §12-7(2)(a) no aplican) y decidir qué fracción de la planta debe alcanzarla, porque §12-7(2)(d) permite partes más bajas y techo inclinado por debajo de 2,2 m. La [comprobación de altura libre](../fase1/verificacion-altura-libre.md) muestra que a 20° con pila de 1 100 mm el ancho completo sólo aguanta un suelo de ~150 mm, y que 5–15° dejan margen amplio. Decidir con el espesor real de suelo (C-02), no con un valor supuesto ([S025](../knowledge/sources/S025.md)).
- [ ] Dimensionar la **envolvente contra §14-3** con el [cribado de envolvente](../fase1/verificacion-envolvente.md): U de pared 0,22 / cubierta 0,18 / suelo 0,18 W/m²K. Dos reglas cambian el resultado: la cámara **ventilada** y todo lo que queda por fuera **no cuentan** en la U (ISO 6946), y la U de §14-3 es de **elemento completo**, así que la fracción de madera cuenta. Con 15 % de montantes la pared necesita ~**189 mm** de lana mineral y la cubierta ~247 mm — espesores que compiten con los 2,2 m de altura libre y con los 4,00 m de transporte. Fijar además el **tablero de viento**: si es difusivamente cerrado (Sd 2 m) la pared pasa de seca a condensar 0,41 kg/m² en 90 días. Datos de material genéricos, sin producto elegido.
- [ ] Dibujar el **encuentro chasis-pared** como detalle térmico, no sólo estructural: §14-3 **no limita** los puentes térmicos lineales —la única cifra, ≤**0,05 W/m²K** normalizada, está en §14-2, exenta por §14-5(1)— y la planta de 18 m² arrastra **61,10 m** de detalle lineal (3,39 m/m²). Con detalle corriente eso son **0,210 W/m²K**, 4,2× la referencia y ~**16 %** de la pérdida de calor. Compensarlo con aislamiento es aritméticamente posible y geométricamente imposible: +53 mm de pared y +65 mm de cubierta, y sólo la parte de cubierta cuesta **69 mm de alero** contra un déficit de 422 mm. El perfil del chasis y el detalle térmico son **el mismo dibujo** ([cribado de puentes térmicos](../fase1/verificacion-puentes-termicas.md)). Ojo: no adoptar 0,05 W/m²K como objetivo, porque a 18 m² implica un Ψ medio de 0,0147 W/mK, menos de la mitad de buena práctica — si se fija objetivo, que sea **por metro**.
- [ ] Documentar los **caudales de aire alternativos** que §13-1(1) exige y que el proyecto nunca produjo: [cribado de ventilación](../fase1/verificacion-ventilacion.md) da **52 m³/h** de impulsión frente a **90 m³/h** básico y **108–216 m³/h** forzado de extracción. Lo que decide no es el caudal sino la **presión**: un ventilador en una casita sellada de 36,9 m³ sólo mueve lo que la envolvente fuga, así que con la estanqueidad de §14-3 la extracción sostiene **106–140 Pa** de depresión, contra un tiro de chimenea de **10–20 Pa**. **El tiro se invierte: −130 Pa.** Y la extracción con los dos baños forzados pide 406 Pa, que ningún ventilador da, así que ese caudal no se entrega. La salida es una **entrada de aire de reposición** dedicada, más aire de combustión propio para la estufa — y cada una es un agujero en la barrera de vapor de la que depende la fila 13: **las filas 13 y 14 son el mismo dibujo**. Ese agujero ya tiene tamaño y no compra el tiro: [cribado de aporte de aire](../fase1/verificacion-aporte-aire.md) da **113 mm** a **10 Pa** de depresión de diseño, que quita **98 Pa** con una sola válvula de fachada. La única depresión que pasa el test de adecuación de §2-2(3) pide **181 mm** a 2 Pa, y 2 Pa está por debajo de la presión que un viento de 3 m/s ejerce sobre el mismo muro: **una entrada pasiva no puede sostener una presión fijada**. Así que la fila 14 no mejora con un agujero, **se retira con una estufa estanca**, que es un requisito de especificación sin coste dimensional. Y el aire de reposición cuesta **905 W** a 30 K, **1,65×** la pérdida del cerramiento (18,3 W/K): la recuperación de calor es una precondición, no una mejora. Y §13-5 tiene la misma forma: [cribado de radón](../fase1/verificacion-radon.md) — el piso **no está sobre el terreno** (hueco ventilado sobre el chasis), así que la barrera «contra el terreno» describe un detalle que el edificio no tiene. La concentración está acotada por `E/Q`: **36 Bq/m³** en terreno ordinario frente a 200, **216** en esquisto de alumbre. El signo lo fija el emplazamiento (C-01), no el modelo. Y la barrera de radón es un requisito de **estanqueidad**, no de Sd: su continuidad es el encuentro piso-pared, el mismo rincón del cálculo 2D. Ese rincón ya tiene [detalle generado](../fase1/planos/detalle-encuentro-R0.svg): sale de las constantes de `puente_2d`, muestra la barrera girando en (13, −22) y muestra la placa cruzando ese plano cuando la viga no va arropada — así que arropar resuelve puente térmico y continuidad de barrera a la vez.
- [ ] Poner al municipio **una sola pregunta de incendio** en lugar de tres: las **ventanas de escape** (§11-13(4)) y el **ancho libre de la puerta** (§11-14) dependen de la misma decisión —si la salida va a **lugar seguro** o a una **rømningsvei** de una sola dirección—, así que las filas 2, 3 y 4 de la declaración se mueven juntas ([determinación](../fase1/determinacion-estrategia-incendio.md)). Con lugar seguro no se exige ninguna de las dos y el recuento cae a 1 positiva / 4 negativas; con rømningsvei las tres son obligatorias y se construyen por **0,29 m²** de vidrio y 100 mm de antepecho. **Lo que NO está acoplado es §11-9**: una celda que no contiene rømningsvei sigue siendo celda, así que **D-s2,d0** gobierna paredes y techo decida lo que decida §11-13 — y ésa es la respuesta que deja la madera recuperada a la vista. La distancia de recorrido interior es **5,04 m** frente a los 15 m que el texto recuperado contiene, pero la fila de la tabla 1 para clase de riesgo 4 sigue sin leerse.
- [ ] Resolver la **condensación en ese mismo encuentro**, que es un problema de humedad antes que de energía: §14-3 limita calor y §13-13 limita vapor, pero ninguno dice nada de la **temperatura del acero que cruza el aislamiento**. En 1D el acero desnudo da **f_Rsi 0,236** frente al **0,754** que exige el criterio de moho, y condensa siempre que fuera baja de **5,9 °C**. **El cálculo 2D ya está hecho y corrige dos cosas** ([conducción 2D](../fase1/verificacion-puente-2d.md), ISO 10211): la misma placa lee **0,377**, no 0,236 —el flujo lateral del suelo la calienta, así que el 1D era *pesimista* con el acero y su dirección de error estaba al revés—; y el acero **deja de ser el punto más frío al primer milímetro de separación**, porque desde 3 mm **la esquina de madera gobierna** en todo espesor. Por eso el requisito es **0,80 m²K/W — 20 mm de espuma, no 9** (9 mm da 0,693). Y el arreglo bueno no es un espesor: **pasar el acero por debajo del suelo, fuera del aislamiento**, devuelve **0,921** y **Ψ +0,027**, idéntico a la esquina desnuda, sin suplemento ni material; 60 mm de suplemento sólo llegan a 0,863. Sobre 18 m de perímetro la diferencia entre las dos posiciones es **3,01 W/K**, ~**16 %** de la pérdida por elementos de la envolvente. Dimensionar **para moho, no para condensación** ([cribado de condensación](../fase1/verificacion-condensacion-union.md)).
- [ ] **Congelar la cubierta** sin esperar al esquema estructural: las cuatro ramas de §11-4(3) —no. 4 R 15, y no. 6.1/6.2/6.3— exigen aislamiento **A2-s1,d0**, porque la regla principal de §11-9 D aplica por sí sola y la vía de escape de no. 7 exige soporte portante A2-s1,d0, que un rastrel de madera no es. Así que el aislamiento es **lana mineral** en toda lectura, y **no. 6.2 queda cerrada** (describe una cubierta totalmente incombustible). Lo que sigue abierto es el **rastrel** y el **revestimiento inferior**. Si aplica R 15 es un problema de **carbonización**: a 15 min la pérdida efectiva es 15,0 mm por cara, y un rastrel expuesto por tres lados la pierde dos veces en su ancho — **48 × 198 conserva sólo el 32 %** de su módulo; la paridad pide 78 mm, o sea **98 mm** comercial. La salida es un revestimiento inferior, que es justo lo que pide no. 6.3: tres cláusulas, un dibujo ([determinación de la cubierta](../fase1/determinacion-cubierta-incendio.md)).
- [ ] Declarar **ancho y separación** de los montantes, no una fracción: la fracción de madera es **ancho ÷ separación**, no una propiedad del material. El 15 % uniforme implica montantes de 90 mm; a 48 mm y 600 mm la cubierta necesita **214 mm** en vez de 245 mm, pero placas, riostras y montantes de refuerzo suben la fracción efectiva, así que el alivio real es de **13–31 mm**, no un valor fijo. Es el alivio más barato que hay para la sección, y no es gratis.
- [ ] Resolver la **sección completa** con [verificación de sección](../fase1/verificacion-seccion.md), porque suelo, pared, cubierta, pendiente y pila de remolque consumen el mismo presupuesto de 4,00 m. A 20° con pila de 1 100 mm, suelo de 250 mm y cubierta de 300 mm el muro sólo llega a **1785 mm** y únicamente ~**720 mm** de ancho alcanzan 2,2 m. Decidir entre bajar la **pila** (el único factor externo a la casita), aceptar cobertura parcial, reducir la pendiente o pedir dispensa. La decisión necesita **C-02 y C-06 juntos**.
- [ ] Elegir entre las **[opciones R2](../fase1/opciones-seccion-R2.md)** — cubierta tendida a 8°, 20° con zonas laterales bajas, 15° sobre plataforma de 700 mm, o 20° con dispensa a 4,40 m — sabiendo que **ninguna tiene tolerancia**: 100 mm de reserva para cumbrera, aleros u orejetas dejan la opción de 20° en **6 %** de cobertura y la de dispensa en 79 %. Ninguna admite altillo. La elección es de **Carlos** y depende de cuánto valga la cubierta a dos aguas de las referencias. **Corrección:** los 4 400 mm de R2-D **no bastan** — la cobertura total a 20° con pila de 1 100 exige **4 415 mm** con los espesores publicados y **4 422 mm** con un 15 % de madera; a un 12 % efectivo sí bastan, y a un 8 % sólo hacen falta **4 358 mm**. El número que se escribe en la solicitud es el que se evalúa.
- [ ] Decidir el **concepto de desagüe** antes de dibujar la planta baja, porque el **0,90 m** de §15-6(2)/§15-8(3) se reordena como `d_crown ≥ 900 + d_trap − h_ffl` y en una casita sobre chasis exige unos **560 mm** de tapada ([S028](../knowledge/sources/S028.md), [cribado](../fase1/verificacion-instalaciones.md)). Una conexión a red municipal lo cumple con ~940 mm de sobra; un depósito sellado poco profundo **falla por 160 mm**. La salida no es una pieza, es otro concepto: suelo elevado, depósito con bomba u otro tubo receptor. Tira en contra de la premisa de tocar poco el suelo, de §7-1(2) y de §9-3 a la vez.
- [ ] Fijar la **estufa** sabiendo que decide tres cosas a la vez: emisión de partículas (**5 g/kg** con catalizador, **10 g/kg** sin él, §9-10), clase de temperatura de humos (**T400** mínima, §15-1(5)(d) y §15-3(2)) y **dos caras libres** de chimenea para poder ver fisuras (§15-3(5)(b)), más las distancias a combustible y el límite de **~45 °C** de superficie (§15-1(3)). En 18 m² las dos caras libres son una restricción de planta, no un detalle.
- [x] Declarar **un solo margen coherente** por análisis, como exige §2-2(3) ([S029](../knowledge/sources/S029.md)) → [declaración de márgenes](../fase1/declaracion-de-margenes.md). Fija **una moneda por tipo de análisis** (mm para lo dimensional, W/m²K para la U, **Ψ medio por metro** para los puentes, probabilidad anual para lo probabilístico, factor adimensional para lo resistente, y **«indefinido»** cuando falta producto o masa). Tabula **quince** filas: **2 positivas, 7 negativas, 4 indefinidas y 2 nulas por construcción** — y una de las dos positivas es una elección de proyecto, no un número reglamentario. Conclusión: el proyecto **no carece de declaración de margen, carece de margen**. La veiledning ([S030](../knowledge/sources/S030.md)) precisa además el **alcance** de la prueba: los márgenes son «nødvendig ved mer omfattende analyse», así que **nueve** filas son análisis y **seis** no lo son — cuatro ytelser declaradas y dos determinaciones. Sacarlas de la prueba no las alivia: una ytelse incumplida exige **dispensación** (PBL cap. 19), que es más estricta, y un margen **no** es una tolerancia.
- [ ] **Comprar margen donde se pueda**, que es la consecuencia de la declaración: el mínimo del vector de márgenes es la sección (**−422 mm**) porque cada opción R2 se resolvió *hasta* los 4 000 mm exactos. Elegir una opción que devuelva holgura — menos pendiente, menos pila o dispensa — deja de ser preferencia y pasa a ser requisito de §2-2(3). Decisión de **Carlos**.
- [x] **Ensamblar la ytelsesoversikt de §2-2(4)**, que la veiledning prescribe en tres categorías —ytelser dadas en la norma, preaksepterte brukt y documentadas por análisis— y que el proyecto nunca tuvo como objeto: los datos estaban repartidos en quince informes. [El resultado](../fase1/ytelsesoversikt.md) son **38 filas**: 27 dadas en la norma, **0 preaksepterte**, 4 por análisis y 7 explícitamente fuera porque no son ytelser. Cada valor se lee del script que lo posee, así que una constante no puede moverse sin que la tabla la siga. Tres hallazgos: la categoría preakseptert está **vacía por estructura** (sin cimentación, sin envolvente montada en obra y sin cubierta convencional no hay ruta preaceptada, así que §2-2(3) carga con todo); **ninguna de las 31 ytelser queda descargada** (9 incumplidas, 20 indeterminadas, 2 no aplican), que es lo que significa R0; y la cola es más larga de lo que parecía — **21 decisiones distintas** cierran las filas y **17 cierran exactamente una**, así que «cuatro decisiones desbloquean el edificio» es falso.
- [ ] No confundir el **1,4** de riesgos naturales con un margen sobre la clase: F2 = 1/200 y S2 = 1/1000 **ya son** el margen normativo, y el 1,4 es un factor parcial sobre los parámetros resistentes del modelo de ladera. Sumarlos sería contar dos veces.
- [x] **Especificar el ensayo de estanqueidad de §14-3**, la fila que la ytelsesoversikt llamó la más barata y que resultó barata en dinero y no en tiempo: no se puede presurizar un edificio que no existe. [La especificación](../fase1/especificacion-ensayo-tetthet.md) fija objetivo **1,30 h⁻¹** y aceptación **1,36** con un ensayo al 10 % —porque la regla de la declaración, aplicada a una medición, baja el umbral por debajo del límite— y encuentra que **la envolvente tiene suelo además de techo**: por debajo de **1,19 h⁻¹** el extractor básico de 90 m³/h no se puede alimentar con un ventilador de 150 Pa. q50 **0,83 m³/(h·m²)** con A/V **1,80** sobre 61,10 m de junta. La entrada de aire, **113→116 mm**, se puede pedir antes de medir. La norma del método, **NS-EN ISO 9972:2015**, **no se tiene** ([S031](../knowledge/sources/S031.md)): no se cita ni un apartado.
- [ ] **Ejecutar el ensayo de estanqueidad** en dos momentos —T1 con la barrera vista y antes de los tableros interiores, para **localizar** fugas, y T2 en la entrega, para **contarlas**— con el método nombrado en el certificado y el exponente de fuga registrado. Bloqueado por: el edificio no existe y la norma no se tiene. La fila 14.5 sigue `undetermined` hasta que haya una medición.
- [ ] Separar las preguntas de **clasificación** de las de **análisis**: si la cubierta es sistema principal y si una ventana de escape basta no se resuelven analizando, porque preguntan **qué ytelse aplica**; se resuelven con una determinación del proyectista responsable acordada con el municipio. La fracción de cobertura de §12-7(2)(d) sí es análisis, y es el instrumento formal.
- [ ] Diseñar el **FDV como archivo versionado con sección por emplazamiento**, no como archivador único: §4-1 exige que esté **ajour** y que corresponda al edificio **tal como se construyó**, y cada traslado cambia terreno, cota de inundación, viento, nieve, cimentación y acometidas ([S029](../knowledge/sources/S029.md)). La lista de contenido para vivienda es corta y está cerrada: productos y superficies, necesidades de operación y servicio de las instalaciones, e instrucciones de uso, sobre seis categorías.
- [ ] No confundir las **dos frecuencias**: los **100 años** de §15-8(1) son capacidad de diseño del drenaje y el **1/200** de §7-2 es clase de seguridad del edificio. Se cruzan en la cota de suelo acabado, que §7-2 empuja hacia arriba mientras §15-8(3) empuja la protección antirretorno hacia el tubo.

**Evidencia:** plantas y corte acotados, ficha de configuración de transporte y secciones de envolvente con revisión.

### 1C. Materiales, instalaciones y masa

- [ ] Inventariar madera recuperada por lote, dimensión, especie si se conoce, origen, estado, humedad y uso propuesto. Registrar idoneidad; si es portante, documentar propiedades o dejarla fuera del modelo estructural.
- [ ] Coordinar ventilación, calefacción, electricidad, agua y desagüe según la clasificación de uso; reservar espacio y acceso de mantenimiento. Para mikrohus aplican [§13-1(1), §§13-4/5/7 y 13-9…13-16 (S023)](../knowledge/sources/S023.md); **§13-2 no aplica** salvo que la clasificación final sea vivienda ordinaria. Documentar las cantidades de aire alternativas de §13-1(1).
- [ ] Fijar los medios de incendio pasivos y activos: **detectores de humo** interconectados a red con batería de reserva, al menos uno por planta, cubriendo cocina, estar, zona fuera de dormitorios y locales técnicos, con **≥60 dB** a puertas cerradas; y **un extintor o una manguera de diámetro interior ≥10 mm** (≤30 m) que alcance todos los locales. No se requiere sistema de alarma NS 3960 ni plano de orientación en clase de riesgo 4 ([S024](../knowledge/sources/S024.md)).
- [ ] Resolver la **extracción de cocina** según §11-10: conducto propio con filtro de grasas, material **A2-s1,d0** (en småhus se admite clase E y conducto flexible de aluminio), y **EI 15 A2-s1,d0** si no va en patinillo. Comprobar que ningún conducto ni cable que atraviese la envolvente rebaje su resistencia, y si algo debe funcionar durante un incendio, **≥30 min** de continuidad en clase de incendio 1 ([S024](../knowledge/sources/S024.md)).
- [ ] Definir conexión/desconexión de servicios y configuración de viaje de depósitos, baterías, muebles y equipos.
- [ ] Crear hoja de masas por componente con cantidad, masa unitaria, masa total, posición X/Y/Z, fuente y estado del dato. Usar la plantilla [inventario-masas.csv](../fase1/inventario-masas.csv), no el archivo de ejemplo como dato del proyecto.
- [ ] Incluir acero, piso, paredes, cubierta, puertas, ventanas, baño, cocina, equipamiento y contenido previsto durante el traslado. (C-07.)
- [ ] Calcular masa total y CG preliminares con [masas_cg.py](../scripts/masas_cg.py); estudiar sensibilidad al mover baterías, depósitos u otros elementos pesados con [mass_sensitivity.py](../scripts/mass_sensitivity.py), que también marca datos estimados y filas `EJ-` de ejemplo. No usar el inventario de ejemplo como dato del proyecto.
- [ ] Comparar masa estimada con el presupuesto de peso acordado con transportista y empresa de grúa; registrar margen y componentes de mayor incertidumbre.
- [ ] Verificar la ruta energética según [§14-5/§14-4 (S021)](../knowledge/sources/S021.md): para vivienda independiente ≤70 m² de BRA calentada no aplica §14-2; para fritidsbolig ≤70 m² no aplica el capítulo 14; para edificio temporal sólo aplica §14-3 dentro del capítulo 14. Registrar la ruta, no un resultado de cálculo.

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
- [ ] Calcular eslingas con `T = V/sin α` y `H = V·cot α`, con α medido desde la horizontal; incluir longitudes desiguales, pretensado y factor dinámico fijado por el especialista. La [pantalla geométrica](../knowledge/comparisons/lift-geometry-screen.md) ya da ángulos, longitudes y ratios T/W, H/W para esquinas y 20 % inset en I-1/I-2; **no selecciona variante ni eslinga**.
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
- [ ] No afirmar cumplimiento del marco §14-2: §14-5(1) lo excluye para la ruta probable de vivienda independiente ≤70 m². Obtener NS 3031:2014 sólo si se requiere documentación de pérdidas térmicas/pontees térmicos. Estado actual: **no obtenido**.
- [ ] Cerrar la ruta del capítulo 13 con C-01: en mikrohus, justificar ventilación conforme a §13-1(1) con cantidades de aire documentadas; no usar `1,2 m³/h·m²` ni `21,6 m³/h` como objetivo sin confirmar la ruta de vivienda ordinaria ([S023](../knowledge/sources/S023.md)).
- [ ] Cerrar la **estrategia de incendio** con el ingeniero de incendio y el municipio: si la cubierta pertenece al sistema portante principal (R 15) o puede acogerse a §11-4(3) nº 6; si **una** ventana de escape basta para una casita de una sola estancia según §11-13(4); si el armario técnico necesita separación EI 30; y si la casita entera cuenta como *rømningsvei* a efectos de clases de superficie, lo que llevaría el interior de D-s2,d0 a B-s1,d0 ([S024](../knowledge/sources/S024.md)).
- [ ] Obtener texto autorizado de NS-EN 1090-2 antes de fijar clase de ejecución, soldaduras, tolerancias e inspección. Estado actual: **bloqueado** (S019).
- [ ] Confirmar si se requiere fatiga EN 1993-1-9 según número real de traslados (C-03).
- [ ] Elegir y registrar la alternativa estructural y de izaje que pasa a prototipo, con sus hipótesis y revisiones.

**Evidencia:** modelo, memoria de cálculo, comparativa I-1/I-2, plano de interfaces y matriz de cumplimiento actualizada.

**Cierre de Fase 2:** configuración elegida con cargas y verificaciones documentadas; posiciones de enganche, apoyo y amarre coincidentes entre cálculo y plano. Sin National Annex y NS-EN 1090-2 no se emite liberación de fabricación; NS 3031 depende de la documentación térmica que exija la ruta final.

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
| 1 | C-01: clasificación legal y emplazamiento exacto en Bergen | Define TEK17/SAK, ámbito del capítulo 13, nieve, viento, energía y documentación |
| 2 | C-02: cotas exteriores finales, salientes, pendiente del tejado y altura de transporte | Define geometría R1 y gálibo |
| 3 | C-07: equipos, baterías, depósitos en litros y contenido durante traslado | Define masa y CG; sin ello no hay plan de izaje |
| 4 | National Annex noruegos; NS 3031 sólo si aplica | Impiden coeficientes de código; NS 3031 depende de la documentación térmica de la ruta final |
| 5 | NS-EN 1090-2 autorizado y alcance de clase de ejecución | Impiden emitir detalles de soldadura/inspección |
| 6 | C-03/C-04/C-06: ruta, grúa y vehículo | Cierran variante de izaje, amarre, permisos, fatiga y si la altura cargada cabe en 4,00 m o requiere transporte especial (S022) |

Para responder de forma ordenada usa la [solicitud priorizada de datos](../fase1/solicitud-datos.md). Mientras llega C-02, la [sensibilidad R1 de tejado a dos aguas](../fase1/r1-opciones-techo.md) cuantifica 5°/10°/15°/20° sin seleccionar pendiente ni congelar geometría. La envolvente inversa muestra, por ejemplo, que con pila de 1 100 mm y pendiente 20° el alero máximo sería 2 354 mm. Con la altura libre de **2,2 m** de §12-7(2)(c), esos 154 mm son el margen para el **espesor de suelo** —no para «estructura y cubierta», que quedan por encima del alero— y la [comprobación de altura libre](../fase1/verificacion-altura-libre.md) confirma que a 20° el ancho completo se agota en un suelo de ~150 mm ([S025](../knowledge/sources/S025.md)).

## 5. Fuentes bases

- [PROJECT.md](../PROJECT.md) y [registro de decisiones Fase 1](../fase1/registro-decisiones.md)
- [DIBK mikrohus (S018)](../knowledge/sources/S018.md); [TEK17 §10-2 (S005)](../knowledge/sources/S005.md); [Lovdata izaje (S013)](../knowledge/sources/S013.md)
- [ESTA GD25001-EN (S017, PDF local)](../knowledge/sources/S017.md); [SCI P272 (S008)](../knowledge/sources/S008.md)
- [National Annex status (S014)](../knowledge/sources/S014.md); [NS-EN 1090-2 status (S019)](../knowledge/sources/S019.md)
- [Matriz de cumplimiento](../knowledge/comparisons/compliance-matrix.md); [checklist de izaje](../knowledge/comparisons/lift-plan-checklist.md); [pantalla geométrica de izaje](../knowledge/comparisons/lift-geometry-screen.md); [brief arquitectónico](../knowledge/comparisons/module-brief.md); [luz diurna §13-7](../fase1/verificacion-luz-diurna.md); [incendio capítulo 11](../fase1/verificacion-incendio.md); [TEK17 capítulo 13 por ruta (S023)](../knowledge/sources/S023.md); [TEK17 capítulo 11 por ruta (S024)](../knowledge/sources/S024.md)
