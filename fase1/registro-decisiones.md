# Fase 1 · Registro de decisiones y datos

Revisión R0 · 2026-11-16 · Estado: **conceptual**. Rol que entrega: architectural-modeler con lifting-test-engineer (transporte). Este registro separa lo fijado, lo supuesto y lo que falta de Carlos (regla 2 y 3 de [rules.md](../rules.md)).

## A. Datos fijados (fuente: PROJECT.md y encargo de Carlos)

| Dato | Valor | Fuente |
| --- | --- | --- |
| Planta exterior aproximada | 6 000 × 3 000 mm | PROJECT.md · Base de diseño |
| Estructura primaria | Acero (chasis y estructura) | PROJECT.md |
| Madera recuperada | Envolvente / acabados; portante sólo con documentación | PROJECT.md + informe, SN-CEN/TS 1090-201 |
| Plataforma de trabajo | Windows + Autodesk | PROJECT.md |
| Marco normativo inicial | Noruega (TEK17 + Eurocódigos 1ª generación + NA) | PROJECT.md + informe |
| Izaje | Comparar nudos superiores vs base, mismas masas | PROJECT.md |
| Mercado y zona principal | Noruega, principalmente **Bergen** | Carlos, 2026-11-16 (C-01) |
| Uso previsto | **Casita de emergencia** — clasificación TEK17 definitiva a confirmar | Carlos, 2026-11-16 (C-01) |

## B. Supuestos de trabajo R0 (no fijados; cada uno con rango y efecto)

| Id | Supuesto | Valor R0 | Rango plausible | Qué bloquea si cambia |
| --- | --- | --- | --- | --- |
| S-01 | Altura total sobre plataforma | 3 200 mm | 2 800–3 600 mm | Gálibo de ruta, CG z_G, aparejo, viento |
| S-02 | Altura libre interior | 2 400 mm | 2 200–2 500 mm | Sección de paredes, masas |
| S-03 | Techo | **REVISAR** — las imágenes de intención (2026-11-16) muestran **tejado a dos aguas** con pendiente notable, no el monopendiente +200 mm asumido aquí. R0 lo mantiene sólo como marco de coordenadas; pendiente real sin acotar. | plano / 2 aguas / 5–15° | Nieve (forma), altura, masas, viento |
| S-04 | Distribución | Baño en extremo x≈0–1,2 m; estar/cocina resto | cualquier otra | CG x_G/y_G, cargas puntuales |
| S-05 | Aberturas | P-01, V-01…V-03 de [tabla-aberturas.csv](tabla-aberturas.csv) | — | Rigidez de paredes, límites de diagonal |
| S-06 | Salientes de envolvente | ≤ 50 mm por lado (ancho transporte ≈ 3 100 mm máx.) | 0–100 mm | Categoría de transporte (ver C-04) |
| S-07 | Paredes colaborantes | Ninguna en el modelo estructural inicial (chasis + pórticos solos) | diafragma documentado | Rigidez torsional, reparto de izaje |
| S-08 | Origen y ejes | Origen en esquina exterior (x=0, y=0) a nivel de cara superior del chasis; +x a lo largo (6 m), +y a lo ancho (3 m), +z hacia arriba | — | Todo modelo debe declarar esto o convertir |

Los supuestos S-01…S-07 se usan **sólo** para la geometría conceptual R0 y las plantillas. Ningún cálculo de resistencia los consume todavía.

## C. Preguntas abiertas a Carlos (bloquean el cierre de Fase 1)

| Id | Pregunta | Por qué importa |
| --- | --- | --- |
| C-01 | **Parcialmente respondida 2026-11-16:** mercado Noruega, principalmente Bergen; uso = casita de emergencia. Falta emplazamiento exacto y si es vivienda habitual, temporal o de emergencia a efectos TEK17. | Nieve, viento, TEK17 clase de uso, aislamiento, masas |
| C-02 | ¿Dimensiones exteriores definitivas y salientes reales? | Ancho legal de transporte, geometría congelada |
| C-03 | ¿Ruta prevista (origen taller → destino) y frecuencia de traslados? | Veggruppe/vegliste, fatiga (EN 1993-1-9), amarre |
| C-04 | ¿Grúa disponible o empresa de izaje prevista? ¿Límites de radio/capacidad? | Variante de izaje, spreader, lift plan |
| C-05 | ¿Tipo de apoyo final (pilotes, losa, gatos niveladores) y suelo? | Reacciones, asentamiento diferencial, anclaje viento |
| C-06 | ¿Remolque/camión previsto (propio o contratado)? | Apoyos de transporte, EN 12195-1, dinámica |
| C-07 | ¿Equipos: baño completo, cocina, baterías, depósitos (litros)? | Masas puntuales dominantes y CG |
| C-08 | ¿Madera recuperada disponible: cantidad, especie, estado? | Masas de envolvente, ficha de trazabilidad |
| C-09 | **Parcialmente respondida 2026-11-16:** dos imágenes conceptuales generadas con ChatGPT en `images/`, aportadas por Carlos como referencia de intención. No son croquis acotados. | Ver sección F y `references/README.md` |

## D. Hallazgo verificado: ancho de transporte en Noruega (2026-11-16)

Fuentes consultadas (contenido externo; confirmar vigencia con el transportista antes de cada traslado):

- Ancho normal máximo con carga: **2,55 m** (forskrift om bruk av kjøretøy cap. 5). Tablas oficiales: [Lovdata 2014-11](http://eksamen.lovdata.no/static/lovtidend/ltavd1/hele-1-2014-11.pdf).
- **Carga indivisible (udelelig gods)** en vogntog N2/N3 + semirremolque o remolque O3/O4: ancho hasta **3,25 m** permitido sin dispensación individual en la mayoría de carreteras, **excepto veggruppe IKKE**, donde se requiere dispensación; el camión tractor debe medir entre 2,30 y 2,55 m de ancho. Resumen del sector: [NLF, seminario spesialtransport (2015)](https://lastebil.no/content/download/28018/579219/version/1/file/NLF%20spesialtransportseminar%2007112015%20med%20tillegg%2009112015.pdf); tabla propuesta/regulación: [Vegdirektoratet, høring udelbart gods (2014)](https://www.vegvesen.no/globalassets/fag/horinger/2014/2010024624-165-udelbart-gods-og-samlasting-frist-20140618/hoeringsnotat.pdf).
- **Husmoduler** tienen reglas propias de dispensación con límite de tiempo (p. ej. dos módulos hasta 4,20 m de ancho combinado); solicitud vía **VegSak**: [Statens vegvesen — søk om dispensasjon for spesialtransport](https://www.vegvesen.no/kjoretoy/yrkestransport/veglister-og-dispensasjoner/sok-om-dispensasjon/dispensasjon-for-spesialtransport-vegsak-elektronisk-soknad).
- Hay una **revisión del reglamento de pesos y dimensiones en consulta en 2026** (§8-3 mantiene el requisito de tractor 2,30–2,55 m): [Vegvesen, høring 2026 — lovspeil](https://www.vegvesen.no/globalassets/fag/horinger/2026/26-183316-horing-om-ny-forskrift-om-vekter-og-dimensjoner-ved-kjoring-pa-offentlig-veg/vedlegg-5.-lovspeil.pdf). Verificar el texto vigente en la fecha del transporte.

**Implicación de diseño:** un módulo de 3,00 m (+ salientes ≤ 3,10 m) cae en la banda 2,55–3,25 m: es transportable como carga indivisible en carreteras aptas sin permiso especial individual, pero **la ruta debe comprobarse contra la vegliste/veggruppe** y el transportista confirma condiciones. Reducir el ancho exterior a ≤ 2,55 m eliminaría la restricción pero cambia el proyecto (18 m² → ~15 m²); no se decide aquí. Esto responde parcialmente C-02/C-03 y no cierra ninguna casilla por sí solo.

## E. Entregables R0 de esta fase (estado conceptual)

- [geometria-R0.md](geometria-R0.md) + planos conceptuales SVG en [planos/](planos/)
- [inventario-masas.csv](inventario-masas.csv) (plantilla vacía) y [inventario-masas-ejemplo.csv](inventario-masas-ejemplo.csv) (sólo prueba de la herramienta)
- [tabla-aberturas.csv](tabla-aberturas.csv)
- [condiciones-transporte-izaje.md](condiciones-transporte-izaje.md)
- Calculadora reproducible: [scripts/masas_cg.py](../scripts/masas_cg.py)

## F. Intención visual declarada (Carlos, 2026-11-16)

Carlos confirma que el mercado es **Noruega, principalmente Bergen**, y que el uso será una **casita de emergencia**. Aporta dos imágenes conceptuales generadas con ChatGPT como **referencia de intención**, no como geometría acotada:

| Imagen | Qué muestra | Consecuencia para el proyecto |
|---|---|---|
| [MiniHouse_ From Base to Roof-1.png](../images/MiniHouse_%20From%20Base%20to%20Roof-1.png) | Vista explosionada "de la base al techo": chasis de acero negro tipo escalera con dos largueros y travesaños, volumen de madera recuperada, **tejado a dos aguas** metálico oscuro separado arriba, puerta y ventana gran en fachada larga, ventana pequeña en testero | El chasis R0 (2 largueros + travesaños @1200) encaja con la intención. **El techo no**: R0 asumió monopendiente. |
| [MiniHouse cabin on a Norwegian slope-2.png](../images/MiniHouse%20cabin%20on%20a%20Norwegian%20slope-2.png) | La misma casita sobre ladera rocosa junto a un fiordo noruego: madera recuperada en tablas verticales, techo a dos aguas de chapa metálica oscura, ventana gran en fachada larga, ventana alta pequeña en testero, zócalo negro | Confirma entorno noruego/costero y la envolvente de madera. Refuerza la estrategia de fachada ventilada por lluvia batiente (S010/S012). |

**Decisiones derivadas:**
1. S-03 pasa a "tejado a dos aguas, pendiente sin acotar". Los planos R0 siguen siendo válidos como marco de ejes, pero `alzado-trans-R0.svg` deberá redibujarse en revisión posterior cuando se acote la pendiente.
2. La imagen no fija cotas: **no** se toman medidas de ellas. C-02 sigue abierta.
3. "Casita de emergencia" necesita precisión jurídica: ¿vivienda habitual, alojamiento temporal o unidad de emergencia? Esto decide la clase de uso TEK17 y si aplican las rampas de §14-2 para småhus (S011). Hasta entonces se aplica el criterio conservador de vivienda.
4. El mercado Bergen (costero, húmedo, ventoso) refuerza: fachada ventilada, barrera de vapor en lado caliente Sd ≥ 10 m (S012), y verificación de carga de nieve/viento con NA noruego y datos de emplazamiento (pendiente).

**Estado:** intención documentada; geometría y masas siguen conceptuales.

## G. Instrumentos de trabajo añadidos (2026-11-16)

| Archivo | Función | Estado |
|---|---|---|
| [solicitud-datos.md](solicitud-datos.md) | Cuestionario priorizado P0/P1/P2 para responder C-01…C-09 sin inventar datos | Abierto; no sustituye este registro |
| [r1-opciones-techo.md](r1-opciones-techo.md) | Sensibilidad de tejado a dos aguas para 5°/10°/15°/20°: altura de cumbrera, superficie, gálibo y área de viento | Generado; **ninguna pendiente seleccionada** |
| [../scripts/r1_gable_options.py](../scripts/r1_gable_options.py) | Generador reproducible de las opciones R1 y su JSON companion | Selftest OK; concepto, no fabricación |
| [../knowledge/comparisons/r1-gable-options.json](../knowledge/comparisons/r1-gable-options.json) | Modelo paramétrico de las opciones para CAD/IFC posterior | Conceptual |

La solicitud de datos y el estudio R1 son apoyos para cerrar C-01/C-02/C-06; no congelan geometría, no validan masa y no autorizan izaje.