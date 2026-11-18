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
3. "Casita de emergencia" necesita precisión jurídica: ¿vivienda habitual, alojamiento temporal o unidad de emergencia? Esto decide la clase de uso TEK17, el conjunto aplicable del capítulo 13 (S023) y las excepciones energéticas (S020/S021). Hasta entonces no se aplica una ruta por defecto: la matriz mantiene separadas mikrohus, edificio temporal y vivienda ordinaria.
4. El mercado Bergen (costero, húmedo, ventoso) refuerza: fachada ventilada, barrera de vapor en lado caliente Sd ≥ 10 m (S012), y verificación de carga de nieve/viento con NA noruego y datos de emplazamiento (pendiente).

**Estado:** intención documentada; geometría y masas siguen conceptuales.

## G. Instrumentos de trabajo añadidos (2026-11-16)

| Archivo | Función | Estado |
|---|---|---|
| [solicitud-datos.md](solicitud-datos.md) | Cuestionario priorizado P0/P1/P2 para responder C-01…C-09 sin inventar datos | Abierto; no sustituye este registro |
| [r1-opciones-techo.md](r1-opciones-techo.md) | Sensibilidad de tejado a dos aguas para 5°/10°/15°/20°: cumbrera, superficie, gálibo, envolvente inversa de alero para 4,00 m y área de viento | Generado; **ninguna pendiente seleccionada** |
| [../scripts/r1_gable_options.py](../scripts/r1_gable_options.py) | Generador reproducible de las opciones R1 y su JSON companion | Selftest OK; concepto, no fabricación |
| [../scripts/lift_geometry_screen.py](../scripts/lift_geometry_screen.py) | Pantalla de geometría de eslingas I-1/I-2 con esquinas y 20 % inset, normalizada por W | Selftest OK; **ninguna variante ni eslinga seleccionada** |
| [../knowledge/comparisons/lift-geometry-screen.md](../knowledge/comparisons/lift-geometry-screen.md) | Ángulos, longitudes y ratios T/W, H/W para 3000/4000/5000 mm verticales | Generado; no autoriza izaje |
| [../scripts/mass_sensitivity.py](../scripts/mass_sensitivity.py) | Comprobación de procedencia de masas y ranking de sensibilidad del CG y reacciones ante incertidumbre de posición | Selftest OK; espera inventario real C-07; marca filas `EJ-` como ejemplo |
| [../scripts/r1_frame_skeleton.py](../scripts/r1_frame_skeleton.py) | Generador de nudos/barras del esqueleto R1 para 5°/10°/15°/20° | Selftest OK; 32 nudos y 59 barras por opción; sin secciones ni masas |
| [../fase2/miembros-R1-opciones.csv](../fase2/miembros-R1-opciones.csv) | Tabla de barras R1 para CAD/IFC y preparación de modelo estructural | Generada; **ninguna pendiente seleccionada** |
| [../scripts/daylight_check.py](../scripts/daylight_check.py) | Comprobación de §13-7 con la tabla de aberturas R0, área de vidrio ≥0,8 m, LT y factor de marco | Selftest OK; **screening condicional a C-01**, no certificado |
| [verificacion-luz-diurna.md](verificacion-luz-diurna.md) | Resultado: 2,47 m² de vidrio; LT mínimo 0,510–0,638 según marco | Generado; puerta excluida por falta de vidrio documentado |
| [../knowledge/comparisons/r1-gable-options.json](../knowledge/comparisons/r1-gable-options.json) | Modelo paramétrico de las opciones para CAD/IFC posterior | Conceptual |
| [clasificacion-uso-decision.md](clasificacion-uso-decision.md) | Árbol de decisión mikrohus / fritidsbolig / edificio temporal y modelos de consulta municipal y transporte | Propuesta; la clasificación la decide el municipio |
| S020/S021/S022 en [knowledge/INDEX.md](../knowledge/INDEX.md) | Base verificada de TEK17 §1-2, §14-5/§14-4 y altura 4,00 m ( Statens vegvesen ) | Verificada; corrige el uso del marco §14-2 |
| [S023](../knowledge/sources/S023.md) | Conjunto aplicable del capítulo 13 para mikrohus: §13-1(1), §§13-4/5/7 y 13-9…13-16; §§13-2/3/6/8 no aplican | Verificada; corrige la ventilación de §13-2 y añade límites de radón, luz, humedad y humedad construida |

La solicitud de datos y el estudio R1 son apoyos para cerrar C-01/C-02/C-06; no congelan geometría, no validan masa y no autorizan izaje. La corrección energética de S021 impide usar `100+1600/A ≈ 188.9` como objetivo de MiniHouse en las rutas probables. La corrección de S023 impide usar `1,2 m³/h·m²` o `21,6 m³/h` como objetivo de ventilación mientras la ruta mikrohus siga abierta: allí rige §13-1(1) con cantidades de aire documentadas.

## H. Corrección de ámbito: TEK17 capítulo 13 (S023, 2026-11-16)

| Punto | Regla verificada | Consecuencia para MiniHouse |
|---|---|---|
| Conjunto aplicable en mikrohus | §13-1 **párrafo primero**, §13-4, §13-5, §13-7 y §13-9…§13-16 | Es el conjunto que debe usarse si C-01 confirma vivienda independiente ≤30 m² BRA |
| Ventilación | §13-1(1): calidad de aire satisfactoria según uso, contaminación y humedad; cantidades alternativas **documentadas** | No trasladar `1,2 m³/h·m²` ni `21,6 m³/h` desde §13-2; esas tasas vuelven sólo si la clasificación final es vivienda ordinaria |
| No aplicables en mikrohus | §13-2, §13-3, §13-6 y §13-8 | No diseñar contra tasas de vivienda, ventilación de edificios públicos, acústica obligatoria ni vistas obligatorias sin reclasificación |
| Límites numéricos útiles | Radón ≤200 Bq/m³ (preparación >100 Bq/m³); luz diurna ≥2,0 % o vía simplificada; pendiente terreno ≥1:50 en ≥3 m; cubierta membrane/foil ≥1:40; madera <20 wt% y <15 wt% en estructuras de secado lento; duchas 1:50/1:100 con resaltes 25/15 mm | Entradas para detalle de envolvente en Bergen; **no** son resultados de rendimiento calculados |
| Edificio temporal | Si C-01 resulta §1-2(5), el capítulo 13 aplica “så langt de passer” | Confirmar con municipio antes de fijar requisitos |

**Estado:** ámbito registrado; la clasificación legal sigue siendo C-01 y ningún valor de esta tabla congela geometría, masa o autorización de izaje.

## I. Capítulo 11 de TEK17: ruta de incendio (S024, 2026-11-17)

| Punto | Regla verificada | Consecuencia para MiniHouse |
|---|---|---|
| Clase de riesgo | §11-2 Tabla 1: **Bolig** y **Fritidsbolig** → clase de riesgo **4**; *arbeidsbrakke* y *skur* → clase 1 | La ruta de incendio **no depende de C-01** entre vivienda y fritidsbolig; sólo cambiaría si la casita se clasificara como cobertizo o barracón |
| Clase de incendio | §11-3 Tabla 1: clase de riesgo 4 en una planta → **BKL 1** | Una planta sin sótano se mantiene en BKL 1 |
| Resistencia portante | §11-4(3) nº 4: BKL 1 + clase de riesgo 4 → **R 15** en sistema principal **y** secundario | Rige R 15, no el R 30 de la Tabla 1; no sobredimensionar contra R 30 |
| Cubierta | §11-4(3) nº 6: sin resistencia especificada sólo si no es decisiva para la estabilidad en la fase de escape, y con 6.1 elemento separador a dos caras, 6.2 **todos** los materiales de cubierta incluido aislamiento A2-s1,d0, o 6.3 revestimiento inferior K210 B-s1,d0 (**K210 D-s2,d0 admitido en clase de riesgo 4**) con aislamiento A2-s1,d0 | Condiciona el techo: 6.2 excluye madera y fibra de madera; 6.3 obliga a lana mineral. Confirmar antes de congelar la composición |
| Celdas de incendio | §11-8: la *boenhet* es siempre celda propia, sin excepción por superficie; EI 30 general en BKL 1 | Una sola *boenhet* sin vecinos: la frontera es la propia envolvente; el armario técnico no es celda automáticamente |
| Separación entre edificios | §11-6: edificio bajo (≤9,0 m) → **8,0 m** mínimo; exento si los edificios forman una sola *bruksenhet*; unidades de camping 4,0 m si ≤75 m² y ≤4,0 m | Pregunta de parcela en Bergen, no de detalle |
| Secciones | §11-7: umbral más bajo 800 m² frente a 18 m² | No es un condicionante de diseño |
| Detección | §11-12(2)(b) y nº 3: detectores de humo interconectados a red con batería, ≥1 por planta, cubriendo cocina, estar, zona fuera de dormitorios y locales técnicos, **≥60 dB** a puertas cerradas | No se requiere sistema NS 3960 ni plano de orientación en clase de riesgo 4 |
| Escape | §11-13(4): una sola dirección admitida en edificios bajos si cada celda tiene ventanas de escape; alto ≥600 mm, ancho ≥500 mm, alto+ancho ≥1 500 mm, antepecho ≤1 000 mm; no aptas en faldón inclinado | Con la tabla actual **sólo V-01 cumple**; V-02 falla antepecho (1 100 mm) y V-03 falla alto, suma y antepecho |
| Ancho de escape | §11-14: clases 1/2/4 → **0,86 m** libres | Una hoja de 900 mm deja sólo 40 mm para marco y herrajes |
| Extinción manual | §11-16: extintor o manguera que alcance todos los locales; en vivienda manguera formoestable **≥10 mm**, ≤30 m; señalización exenta si sirve a una sola vivienda | Un extintor o una manguera de 10 mm bastan |
| Acceso de bomberos | §11-17: edificio pequeño en clase 4/BKL 1 → hasta **50 m**; **1 200 l/min** en zona de viviendas unifamiliares; boca de incendio a 25–50 m | Pregunta de parcela; puede decidir el emplazamiento |
| Clases de superficie | §11-9 Tabla 1A, BKL 1: paredes y techo **D-s2,d0** en celda ≤200 m²; revestimiento exterior **D-s3,d0**; cubierta **BROOF(t2)** (chapa asumida); superficies de cámara sin clasificar admitidas en BKL 1 | La madera recuperada vista **sí es admisible** con D-s2,d0 documentado; si la casita entera se considera *rømningsvei*, sube a **B-s1,d0** y deja de serlo sin tratamiento |
| Aislamiento | §11-9 D: regla general **A2-s1,d0**; nº 7 exige soporte portante **A2-s1,d0**, que un par de madera no cumple; nº 9 admite celulosa o fibra textil en BKL 1 y viviendas de hasta tres plantas | Converge con §11-4(3) nº 6: el aislamiento de cubierta apunta a **lana mineral** salvo análisis de incendio documentado |
| Instalaciones técnicas | §11-10: conducto de extracción de cocina propio con filtro de grasas, **A2-s1,d0**, y **EI 15 A2-s1,d0** si no va en patinillo; penetraciones no rebajan la resistencia; **≥30 min** de continuidad de cable en clase de incendio 1 | Condiciona la cocina y el paso de instalaciones por la envolvente |

**Estado:** requisitos registrados. Quedan abiertos, para el ingeniero de incendio y el municipio: si la cubierta pertenece al sistema portante principal (R 15) o puede acogerse al nº 6; si **una** ventana de escape basta en una casita de una estancia; si el armario técnico necesita EI 30; si la casita entera cuenta como *rømningsvei* para clases de superficie; y si cabe justificar fibra de madera en cubierta. Nada de esta tabla constituye una estrategia de incendio ni una liberación.

## J. Capítulo 12 de TEK17: conjunto aplicable y altura libre (S025, 2026-11-17)

| Punto | Regla verificada | Consecuencia para MiniHouse |
|---|---|---|
| Conjunto aplicable | §1-2(2)(d) admite sólo **ocho** preceptos: §12-1(1), §12-5, §12-7(1)+(2)(c)+(2)(d), §12-11(1)+(2), §12-13(1)+(2)(d), §12-14(1)(a–d)+(5)(b), §12-15 y §12-17 | Todo el resto del capítulo 12 queda exento |
| Accesibilidad | §12-2 (vivienda accesible), círculos de giro de 1,5 m, pasos de 0,9 m: **no aplican** | Libertad de planta para 18 m²; no hay que reservar 1,5 m de maniobra |
| Entrada, comunicación, baño, almacén, residuos, rampa | §12-4, §12-6, §12-9, §12-10, §12-12, §12-16, §12-18: **no aplican** | Sin mínimo de baño ni de almacén por el capítulo 12; **§13-15 de cuartos húmedos sigue aplicando** |
| Altura libre | §12-7(2)(c): **2,2 m** para la ruta ≤30 m²; §12-7(2)(a) exigiría **2,4 m** y está exenta | Una sola cifra para toda la casita, no 2,4 m en salas |
| Altura en partes del local | §12-7(2)(d): partes pueden ser más bajas; el techo inclinado puede bajar de 2,2 m | El alero **no** es el plano de referencia de la altura libre |
| Altura a ancho completo | Con 20° y pila de 1 100 mm, el límite es **20,1°** para un suelo de 150 mm; con 200 mm baja a 18,4° | 20° queda **justo en el límite**; 5–15° tienen margen amplio. Cifras en [altura libre](verificacion-altura-libre.md) |
| Puertas | §12-13(2)(a) y (2)(e) exentas: **no hay 0,86 m ni 2,0 m de altura por capítulo 12** | El 0,86 m viene de **§11-14** (ruta de escape); la altura es funcional |
| Escaleras | §12-14(1)(a–d): pasamanos a dos caras, 0,8–0,9 m, contrahuella uniforme, huella ≥0,25 m; **sin ancho ni altura libre** del capítulo 12 | Si hay altillo, la escalera se rige por esos cuatro puntos; (5)(b) exime la de servicio **salvo que sea ruta de escape** |
| Protección contra caídas | §12-5 y §12-11(2): desniveles **>0,5 m** asegurados; §12-15: barandilla **1,0 m** hasta 10 m, huecos ≤0,10 m | Afecta a la terraza y a la ventana de escape si el suelo queda a más de 0,5 m del terreno |
| Vidrio | §12-17: asegurado hasta **0,8 m** sobre el suelo; antepechos actuales ≥900 mm → **sin vidrio de seguridad** por esa regla; balconera siempre asegurada; marcado 0,9/1,5 m | Sin conflicto con la ventana de escape: antepecho entre 0,8 y 1,0 m cumple ambas |

**Estado:** conjunto aplicable y cifras registrados. Quedan abiertos: qué fracción de la planta debe alcanzar 2,2 m (§12-7(1)/(2)(d) no fija porcentaje); el espesor real del suelo (C-02), que consume los 154 mm de margen a 20°; y si la ventana de escape necesita barandilla o limitador con el suelo a más de 0,5 m. El **capítulo 7 de riesgos naturales** ya está consultado: ver sección K.

## K. Capítulo 7 de TEK17: riesgos naturales (S026, 2026-11-17)

| Punto | Regla verificada | Consecuencia para MiniHouse |
|---|---|---|
| Frontera del capítulo | §7-1: nieve, viento y sismo **no** son capítulo 7, sino **§10-2** y los Eurocódigos | No se cuenta dos veces: una parcela puede fallar §7-3 por deslizamiento mientras el viento y la nieve se dimensionan con normalidad |
| Deber del §7-1(2) | El edificio no puede **crear ni agravar** el peligro para sí mismo, para el terreno ni para el terreno vecino | Aplica a una casita sobre pendiente o sobre relleno aunque la parcela parezca aceptable |
| Clase de inundación | §7-2: **F1 = 1/20**, **F2 = 1/200**, **F3 = 1/1000**; F2 nombra «bolig, fritidsbolig og campinghytte» | **MiniHouse es F2**, y no depende de C-01 porque la lista nombra vivienda y fritidsbolig |
| Escalada a F3 | Si el área de inundación tiene **gran profundidad o corriente fuerte**, la guía indica usar el nivel **F3** | Una casita es ligera respecto a su volumen: flota o es empujada antes de quedar sumergida. Es criterio real, no tecnicismo |
| Nivel del mar | §7-2 cubre **flom og stormflo** y exige considerar el cambio climático y la subida del nivel del mar | La cota de suelo acabado no puede compararse con el nivel del mar actual; cada 1 mm/año añade 50 mm en 50 años |
| Clase de deslizamiento | §7-3: **S1 = 1/100**, **S2 = 1/1000**, **S3 = 1/5000**; S2 nombra «enebolig … fritidsbolig med maksimum 10 boenheter» | **MiniHouse es S2** |
| Uso exterior | En edificios S2 el requisito del **área exterior** puede rebajarse al nivel **S1 (1/100)** | La terraza no exige 1/1000; el edificio sí |
| Diseñar contra el deslizamiento | Se admite dimensionar el edificio para resistir la acción si las cargas no son grandes; techo práctico ≈**50 kPa** | 50 kPa ≈ 5,1 t/m² ≈ 2,8 m de suelo a 18 kN/m³: es un evento pequeño, no un flujo de derrubios con bloques |
| Arcilla rápida | §7-3 exige nivel equivalente para **kvikkleireskred**; la guía lo amplía a *områdeskred* según NVE 1/2019 | No se criba con un factor de seguridad: la zona de peligro puede ser mayor que la parcela |
| Límite marino | **Bajo el límite marino el terreno debe investigarse aunque esté fuera de zonas mapeadas** | Bergen tiene terreno bajo el límite marino: es requisito vivo, no formalidad |
| Categoría de medida | El alcance lo fija una **tiltakskategori** K0–K3; los ejemplos K0 son garajes, casetas de bote, ampliaciones, cobertizos | **Una vivienda nueva no está en la lista K0**: la casita colocada como vivienda no puede suponerse K0 |
| §7-4 | Excepción para **fjellskred** y su ola, con aviso ≥**72 h** y evacuación ≤**12 h**, y plan de área que acredite ausencia de alternativa | Es un instrumento de planificación regional y de zonas monitorizadas por NVE; **no es una ruta para una casita privada** |
| Transportabilidad | TEK17 evalúa el edificio **en su posición** | Mover la casita no rebaja la clase, pero obliga a **repetir el cribado en cada emplazamiento** durante su vida útil |

**Estado:** requisitos y clases registrados. La clase no depende de C-01, pero **no se ha consultado ningún mapa, ni el límite marino, ni una cota de inundación**. El capítulo condiciona la parcela, no la casita, y por eso es la primera puerta del emplazamiento — antes de las 8,0 m de separación (§11-6) y de los 50 m de acceso de bomberos (§11-17). Nada de esta tabla es una evaluación geotécnica, una evaluación de inundación ni una aprobación de emplazamiento. Procedimiento: [cribado de riesgos naturales](cribado-riesgos-naturales.md).

## L. Envolvente: U y humedad con números (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Regla de la cámara ventilada | Una cámara **bien ventilada** y todo lo que queda por fuera **no cuentan** en la U (ISO 6946); la resistencia superficial exterior se toma en la cara que limita la cámara | Contar la cámara y el revestimiento como aislamiento rebaja la U en ~0,02 W/m²K: suficiente para convertir un fallo en un aprobado. El revestimiento de madera recuperada **no aporta aislamiento** |
| U de campo limpio | Pared **0,209**, cubierta **0,164**, suelo **0,160** W/m²K frente a 0,22 / 0,18 / 0,18 de §14-3 | Los tres pasan… |
| Fracción de montantes | Con 15 % de madera en la capa aislada: pared **0,267**, cubierta **0,218**, suelo **0,209** | …y **los tres fallan**. La penalización es del 20–30 % y es invisible en un cálculo por capas |
| Espesor necesario | Pared ~**189 mm** de lana mineral (141 en campo limpio), cubierta ~247 mm, suelo ~238 mm | El espesor deja de ser una preferencia: compite con los 2,2 m de §12-7(2)(c) y con los 4,00 m de transporte |
| Aislamiento continuo | Basta una capa continua, un rastrelado cruzado o un tablero aislante para volver a cumplir | Deja de ser un refinamiento: es la diferencia entre cumplir y no cumplir |
| Humedad con barrera Sd ≥ 10 m | Seco a 40 % y a 55 % de HR interior | Cumple §13-13 con margen en el modelo |
| Humedad con barrera débil o sin barrera | También **seco**, porque el tablero de viento de fibra de madera es difusivamente abierto | La difusión sola **no** condena una barrera débil; el sentido común «más barrera = mejor» es falso en este modelo |
| Humedad con tablero de viento cerrado | **0,41 kg/m² en 90 días** a 40 % HR y **1,09 kg/m²** a 55 % | El fallo dominante es una **trampa en el lado frío**, no la falta de barrera en el lado cálido. El tablero de viento es una decisión de proyecto, no un consumible |
| Lectura de §13-13 | Sd ≥ 10 m no es un cálculo de difusión: es un requisito de **robustez** | Cubre fugas de aire, humedad interior alta, función de barrera de aire y ejecución por terceros. Glaser no ve fugas de aire, que transportan mucho más vapor que la difusión |
| Puente térmico del chasis | **No cuantificado** | Un perfil de acero que cruza el aislamiento del suelo puede dominar el perímetro; hace falta detalle de rotura y, si se exige, un valor Ψ |

**Estado:** cifras registradas con datos de material **genéricos**, sin producto elegido y sin simulación higrotérmica. El cribado es estacionario y unidimensional: no ve convección, capilaridad, puentes 2D ni lluvia. Informe: [verificación de envolvente](verificacion-envolvente.md).

## M. Sección integrada: altura, pendiente, envolvente y gálibo (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Por qué hacía falta | La comprobación de altura libre trataba la cubierta como una **línea sin espesor** y el suelo desde 100 mm | Las dos omisiones favorecían el resultado. Había que resolverlo todo junto |
| Coste vertical de la cubierta | El espesor es perpendicular a la pendiente, así que cuesta **t/cos θ** en vertical, además de la subida de cumbrera | Subir la pendiente cuesta **dos veces**: más cumbrera y más espesor en pie |
| Presupuesto de altura | `cumbrera = t_suelo + h_muro + 1500·tan θ + t_cubierta/cos θ`, y `transporte = cumbrera + pila` | Suelo, muro, cubierta, pendiente y pila compiten por los mismos 4,00 m |
| Caso de referencia | 20°, pila 1 100 mm, suelo 250 mm, cubierta 300 mm → muro máximo **1785 mm** y cobertura **24 %** | El alero **no llega** a 2,2 m: sólo una franja de ~**720 mm** junto a la cumbrera cumple |
| Rango de pendiente | La pendiente máxima con 2,2 m a ancho completo va de **16,3°** (900/200/250) a **1,9°** (1 100/300/350) | Una cubierta a dos aguas de 20° y 2,2 m a ancho completo son incompatibles bajo 4,00 m con envolvente realista |
| Palancas cerradas | En el caso de referencia, el suelo y la cubierta tendrían que ser **negativos** para recuperar la cobertura completa | No son restricciones ajustadas: son puertas cerradas. La envolvente ya está en el mínimo de §14-3 |
| Palancas abiertas | Pila hasta **685 mm**; límite de transporte hasta **4 415 mm**; pendiente hasta **5,7°** | Sólo tres salidas: menos pila, dispensa o menos pendiente |
| Coste en superficie | Un muro de 264 mm quita **528 mm** por dimensión: 18,0 → **13,53 m²** útiles, un **25 %** | Sigue cabiendo en la ruta ≤30 m², pero es un coste de habitabilidad, no de cumplimiento |
| Ambigüedad a cerrar | La «pila» se toma como todo lo que hay bajo la cara superior del chasis (chasis + plataforma + apoyos) | Si el transportista cotiza sólo la plataforma, la pila real es ~250 mm mayor y todo empeora (C-06) |

**Estado:** cribado paramétrico, **sin pendiente elegida y sin geometría congelada**. No hay holguras de salientes, aleros, chimenea, orejetas de izaje ni estructura del remolque; ninguna de ellas está modelada y todas consumen altura. Informe: [verificación de sección](verificacion-seccion.md). La comprobación anterior de altura libre queda **superada en alcance, no en aritmética**.

## N. Opciones R2 de sección (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Para qué | El conflicto de altura ya está establecido; lo que faltaba era poner configuraciones coherentes sobre la mesa | Cuatro opciones resueltas con el mismo modelo, para decidir con cifras y no con preferencia |
| **R2-A** cubierta tendida 8° | Pila 900, muro **2336 mm**, **2,2 m a ancho completo**, transporte 4000 | Cierra la altura libre; la cubierta se lee casi plana y la dos aguas de las referencias queda en una línea de cumbrera |
| **R2-B** 20° con zonas bajas | Pila 1 100, muro **1785 mm**, franja de **718 mm**, zona baja de **1141 mm por lado** | Mantiene los 20° sin permiso ni plataforma especial; exige llevar baño, cocina y almacén a los bordes |
| **R2-C** 15° sobre plataforma baja | Pila **700**, muro **2337 mm**, **2,2 m a ancho completo** | Cierra la altura libre conservando algo de pendiente; depende de encontrar plataforma de 700 mm (C-06) |
| **R2-D** 20° con dispensa | Límite **4 400**, muro **2185 mm**, franja **2916 mm** | Casi ancho completo sin cambiar el diseño; convierte cada traslado en una solicitud VegSak |
| Zona baja de R2-B | **1141 mm de fondo × 5,47 m = 6,24 m² por lado**, techo de 1785 a 2200 mm | No es desperdicio: cabe un baño de ~1,1 × 2,0 m, una cocina de 600 mm y almacén a altura completa. Es la lógica de un ático |
| Tolerancia | Las cuatro opciones se resuelven **exactamente** en el límite; con **100 mm** de reserva R2-B cae a **6 %** y R2-D a **79 %**; R2-A y R2-C aguantan | Una opción que sólo funciona con tolerancia cero es un cálculo, no una opción robusta |
| Altillo | Altura libre en cumbrera **2331 mm** a 20° | **Ninguna opción admite altillo**: no hay 1 600 mm sobre un forjado a 2,2 m |

**Estado:** opciones calculadas, **ninguna seleccionada**. La elección es de Carlos y depende de cuánto valga la cubierta a dos aguas de las referencias, de qué plataforma exista (C-06) y de qué fracción de planta deba alcanzar 2,2 m. Informe: [opciones de sección R2](opciones-seccion-R2.md).

## O. Capítulo 9 de TEK17: medio exterior (S027, 2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Qué es realmente el capítulo | **No** es ruido ni agua: es sustancias peligrosas, suelo, hábitats y **residuos de obra** | El ruido es §13-6 (exento) y el agua es el capítulo 15. Se admite **íntegro** por §1-2(2) |
| **§9-2** sustancias peligrosas | Exige productos «uten eller med lavt innhold»; la guía ofrece Svanemerket, ECOproduct, SINTEF TG, ficha de datos, EPD, declaración CE o confirmación del fabricante | **Todos los peldaños suponen un fabricante.** La madera recuperada no tiene ninguno, así que la ruta predocumentada **no existe** |
| SCIP | El deber de notificar a **>0,1 % en peso** de SVHC recae en el *proveedor de artículos* | Quien recupera madera de un derribo no es proveedor. No hay instrumento |
| Qué queda para C-08 | Sólo el **dictamen pericial y comparación** que la propia guía contempla | Es una pregunta de **ensayo**: pintura con plomo, CCA u otro protector, sellante con PCB, polvo con amianto. Coste y plazo, y debe ir al principio de C-08, no al final |
| **§9-3** suelo contaminado | Investigar **antes de solicitar** licencia; la forurensningsforskriften cap. 2 impone un deber independiente; si hay contaminación, **plan de actuación** aprobado antes de excavar | Segunda puerta de emplazamiento, **independiente del capítulo 7**: el 7 pregunta si la naturaleza amenaza al edificio, el 9-3 si el suelo amenaza a las personas. El municipio puede **prohibir** |
| **§9-4** hábitats seleccionados | Sólo si hay reglamento de la ley de biodiversidad, la especie está en el municipio y el plan no lo resuelve | **Sin exención por tamaño.** El análisis de consecuencias de la letra b) **no es dispensable** |
| **§9-6** plan de residuos | Umbrales: **>300 m²** obra nueva, **>100 m²** reforma o derribo, o **>10 t** de residuos | A 18 m² los umbrales de superficie son inalcanzables y **ninguna masa plausible de la casita cruza las 10 t** |
| Masa necesaria para cruzar 10 t | 33 t con 30 % de merma, 50 t con 20 %, 100 t con 10 %, 200 t con 5 % | Construir la casita **no puede** activar el deber. Sólo lo activa la **agregación de §9-6(2)** con un derribo |
| **§9-7/§9-8/§9-9** | §9-7 es **sólo edificios existentes**; §9-8 (70 % en peso, en obra) y §9-9 (informe final con ferdigattest) siguen el interruptor de §9-6 | La casita nueva queda **fuera** de §9-7. Pero el edificio de origen, si se derriba, **sí** entra, con declaración de residuos peligrosos |
| **§9-5** residuos y reutilización | (1) vida útil prevista; (2) productos aptos para reutilización y reciclaje, **diseño para desmontaje documentado en el proyecto**, y **la sujeción es decisiva** | Es el capítulo que **premia** el concepto: MiniHouse ya se levanta entero. Pero un chasis soldado al bastidor o una membrana pegada son «difíciles de separar» y por tanto **poco aptos** |
| **§9-10** estufa de leña | **5 g/kg** con catalizador, **10 g/kg** sin él (NS 3059:1994, ensayo NS 3058:1994); estufas de acumulación exentas | Casi seguro habrá estufa. La emisión, la clase de humos y las distancias se eligen **juntas** |

**Estado:** requisitos verificados, **ninguna parcela comprobada**. §9-2 convierte C-08 en una pregunta de ensayo; §9-3 añade una puerta de emplazamiento que no existía en el registro. Informe: [verificación de instalaciones](verificacion-instalaciones.md).

## P. Capítulos 15, 16 y 17 de TEK17: instalaciones (S028, 2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Exención por tamaño | **No existe en ningún punto del capítulo 15**; §15-5, §15-6, §15-7 y §15-8 se comprobaron uno a uno | La casita está **plenamente** en alcance. El supuesto contrario es falso |
| Grupos del capítulo | Bajan a la casita §15-1/15-3/15-4/15-5/15-6; al **sitio** §15-7/15-8; nunca se activan §15-2 y §15-9…15-15 | Tres resultados distintos en un mismo capítulo |
| **§15-1** calefacción | Superficie con riesgo de quemadura por encima de **~45 °C**; protección de suelo no combustible o **B-s1,d0 (In1)**; **T400** de chimenea; sin sala de calderas si sólo hay electricidad | En 18 m² la estufa queda cerca de todo: los 45 °C son una restricción de **planta**, no del aparato |
| **§15-3** humos y chimenea | **T400** mínimo (NS-EN 1443:2019), sección constante, fábrica sobre soporte no combustible, **≥2 caras libres** para ver fisuras, acceso de **feiing** | Las dos caras libres compiten con la estufa, sus distancias y el límite de 45 °C en la misma pared |
| **§15-5** agua interior | **38 °C** (usuarios vulnerables) / **55 °C** en grifo, ACS en circulación **65 °C**, cámaras de aire **20/50 mm**, reductor sobre **0,6 MPa**, prueba a **1 MPa**, **cortagotas** y **llave de paso** antes de la primera derivación | La llave de paso sirve a la vez para §15-5(3)(c) y para **vaciar el sistema antes de cada traslado** |
| **§15-6** desagüe interior | Sifón obligatorio; **0,90 m** entre el nivel del sifón más bajo y la parte superior interior del colector | Reordenado: `d_crown ≥ 900 + d_trap − h_ffl`. Es una **profundidad mínima de zanja**, no un detalle de fontanería |
| Cuánto exige | Con suelo a **400 mm** y sifón a **60 mm**, unos **560 mm** de tapada | Choca con la premisa de tocar poco el suelo, con §7-1(2) y con §9-3 a la vez |
| Red municipal frente a depósito | Colector municipal a 1 500 mm: **+940 mm** de margen. Depósito sellado a 400 mm: **falla por 160 mm** | No es un problema general, es **específico del concepto de desagüe**. La salida es suelo elevado, depósito con bomba u otro receptor |
| **§15-7/§15-8** redes exteriores | **2,5 bar** en acometida, reductor sobre **6,0 bar**, **1,0 bar** en boca de incendio, **4 m** del edificio; pluviales a **100 años climatizados**, **0,90 m** otra vez | Son requisitos del **sitio**, no del módulo, y dependen de si hay red o depósito |
| Dos frecuencias | Los **100 años** de §15-8(1) son capacidad de diseño; el **1/200** de §7-2 es clase de seguridad | No confundirlos: o se sobredimensiona el drenaje o se subprotege la cota de suelo |
| Cuatro determinaciones | **§15-2** sin sistema de distribución; **§15-9…15-15** sin ascensor ni plataforma; **capítulo 16** control de ascensores; **§17-1** sólo boligblokk y yrkesbygning | Cierran limpias y **con base escrita**. Una determinación no es un olvido |
| Capítulo 16 | **No es documentación**: es control de seguridad de ascensores | La documentación es el **capítulo 2** (cumplimiento) y el **capítulo 4** (FDV), ambos admitidos y **sin consultar** |
| **§17-1** huella de carbono | Sólo boligblokk y yrkesbygning; un småhus queda exento **por definición**, no por superficie; NS 3720 **excluye el carbono biogénico** | Un proyecto de reutilización queda fuera del único requisito de contabilidad climática, y el método ignora justo su mejor argumento |

**Estado:** requisitos verificados, **ningún producto elegido**. Cuatro no-aplicabilidades quedan como determinaciones. El capítulo 2 y el 4 siguen sin consultar y son el hueco real que queda en el alcance admitido. Informe: [verificación de instalaciones](verificacion-instalaciones.md).
## Q. Capítulos 2 y 4 de TEK17: documentación y FDV (S029, 2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Qué añaden | Ni un solo número al edificio. Añaden **el criterio que decide si el análisis del proyecto cuenta** | Hasta ahora ese criterio se aplicaba por costumbre. §2-2(3) lo escribe |
| **§2-2(1) frente a (2)** | Si la norma da una **ytelse**, se cumple y el análisis **no sustituye**. Sólo donde da **función y ningún número** cabe preaceptada o **análisis** | Es una puerta, no un permiso: se puede analizar **hasta** un requisito funcional, no **más allá** de una ytelse dada |
| Qué es analizable | §12-7(2)(d) (fracción de cobertura) y §13-1(1) (calidad de aire) | El solucionador de sección no es una comprobación informal: es el **instrumento formal**, y §2-2(3) lo gobierna |
| Qué no lo es | Si la cubierta es sistema principal; si una ventana de escape basta; si la casita es ruta de evacuación | No son análisis sino **clasificación**: preguntan qué ytelse aplica. Las resuelve una determinación, no un cálculo |
| **§2-2(3)** | Método **idóneo y válido**, supuestos **descritos**, supuestos **justificados**, **márgenes de seguridad declarados** | Las secciones **Límites** de los informes pasan de cortesía a trabajo normativo |
| Márgenes hoy | Sólo **3 de 9** informes declaraban un margen numérico, y en tres monedas: 4,00 m de cribado (S022), 100 mm de reserva (R2), 1,4 de factor de material (sin verificar) | Resuelto con la [declaración de márgenes](declaracion-de-margenes.md), sección **S**: una moneda por tipo de análisis, doce filas con signo, y la conclusión de que el proyecto **carece de margen**, no de declaración |
| **§2-2(4)** | Las ytelses fijadas deben dar **base suficiente para el proyecto de detalle** | La sección no cierra a 20° bajo 4,00 m, así que la base **no existe todavía**. Eso no es un fallo del trabajo: es §2-2(4) haciendo su función. R2 es el paso que la produce |
| **§2-3 / §2-4** | Base de producción y ejecución | **No alcanzadas.** Una U con λ genérica demuestra que un **espesor** podría servir, no que una **especificación de producto** sirva: ésa es toda la diferencia |
| **§4-1(2)** exención | Ejemplos: garajes pequeños, naust, uthus — todos **sin calefacción, sin instalaciones y no residenciales** | **Considerada y rechazada.** La casita tiene **6 de 6** categorías FDV, con estufa de combustión y cuarto húmedo. Determinación, no omisión |
| Contenido FDV de vivienda | Productos y superficies a limpiar y mantener; necesidades de operación y servicio; instrucciones de uso; sobre seis categorías de instalación | Es la única parte del cuadro que está **cerrada en alcance** y sólo necesita rellenarse |
| FDV en edificio trasladable | Debe estar **ajour** y corresponder al edificio **tal como se construyó**, declarando premisas y limitaciones | Cada traslado cambia terreno, cota, viento, nieve, cimentación y acometidas: exige **archivo versionado con sección por emplazamiento**, decidido antes del primer traslado |
| **§4-2** | Se entrega al **propietario** y él lo conserva | Sin plazo ni ubicación en el precepto. No se inventa ninguno |
| **§2-1** y los anexos nacionales | La guía exige **aplicar** los NA para cumplir las reglas noruegas | S014 registraba los NA como bloqueo de **diseño**; también lo son de **documentación**. Una barrera de pago, dos bloqueos |

**Estado:** requisitos verificados, **veiledning de §§2-2/2-3/2-4/4-2 no obtenida** (cuatro páginas de DIBK devolvieron sólo navegación; el texto vinculante vino de Lovdata). No se reconstruye ninguna guía de memoria. El alcance admitido por §1-2(2) queda **completamente cardado**. Informe: [verificación de documentación](verificacion-documentacion.md).

## R. Puentes térmicos y el encuentro del chasis (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| ¿Limita §14-3 los puentes térmicos? | **No.** La ruta que aplica fija U de elemento y estanqueidad y calla sobre puentes lineales | Se puede cumplir **todos** los números de §14-3 y perder una fracción grande del calor en los encuentros. Cumplir no es ser eficiente |
| ¿De dónde sale el 0,05 W/m²K? | De **§14-2**, la ruta alternativa de medidas de energía, que §14-5(1) **exime** en edificio suelto ≤70 m² | La única cifra disponible **no obliga** aquí. Se usa como referencia **voluntaria**, etiquetada así |
| Inventario de encuentros | **61,10 m** lineales: perímetro de suelo 18,00 + alero 18,00 + esquinas 8,80 + jambas 16,30 | **3,39 m por m² de suelo.** El perímetro del suelo solo ya es tan largo como el edificio entero |
| Coste del detalle corriente | Ψ″ **0,210 W/m²K**, **4,2×** la referencia y **16 %** de la pérdida de calor. Bueno 0,117 (2,3×), malo 0,397 (7,9×) | Ningún escenario alcanza 0,05. Los encuentros no son una nota al pie en ningún caso |
| ¿Se compensa con aislamiento? | **Sí aritméticamente, no geométricamente.** Escalar las U por f = (H_elementos − H_puentes)/H_elementos cuesta +53 mm de pared, +65 de cubierta y +65 de suelo | La cubierta cuesta su espesor entre cos θ: **69 mm de alero** contra un déficit de 415 mm, ~17 %. La palanca existe y no hay sitio para moverla |
| Corrección de este informe | La primera versión afirmaba que los puentes **no** se pueden compensar. Era falso; lo detectó el autotest del propio guion | Se corrige el texto, no el número. La conclusión honesta es más estrecha y más fuerte |
| El objetivo 0,05 W/m²K | A 18 m² y 61,10 m implica un Ψ medio de **0,0147 W/mK**, menos de la **mitad** de buena práctica. En 150 m² la misma cifra implica 0,075 W/mK | **No adoptarlo como objetivo.** Está normalizado por área, que es justo lo que a esta casita le falta. Si se fija objetivo, **por metro** |
| Escala con el tamaño | A detalle constante Ψ″ cae de 0,199 a 0,066 entre 18 y 150 m² | El conjunto de requisitos es más débil justo donde este tipo de edificio está más expuesto, y §14-5(1) retira el único límite que lo habría notado |
| Planta 6:2 | ~**6 %** más perímetro que un cuadrado de la misma área | Una planta más cuadrada sería térmicamente más barata; los 6 m son una decisión de transporte, no de arquitectura |
| Consecuencia de diseño | El **perfil del chasis** y el **detalle térmico** son el mismo dibujo: el aislamiento de suelo debe pasar **por fuera** del acero, no quedar interrumpido por él | Es la mayor decisión térmica del edificio y no está dibujada. Depende de Fase 2 |

**Estado:** cribado, **ningún Ψ calculado** y ningún encuentro dibujado; los Ψ son rangos genéricos de práctica corriente, no datos de proyecto. Un valor real exige cálculo 2D según NS-EN ISO 10211 sobre un detalle que no existe. Informe: [verificación de puentes térmicos](verificacion-puentes-termicas.md).

## S. Declaración de márgenes de §2-2(3) (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Qué pide §2-2(3) | Método idóneo, supuestos descritos, supuestos justificados y **márgenes de seguridad necesarios declarados** | Los tres primeros se cumplían en los nueve informes; el cuarto se declaraba en tres monedas distintas. Ahora hay **una** declaración |
| Qué es un margen | **valor disponible − valor exigido**, en las unidades de la magnitud que gobierna, **con signo**, y acompañado de la incertidumbre del modelo | Definición operativa: se puede comprobar. Un margen sin signo no es un margen |
| Moneda por tipo | mm para lo dimensional; W/m²K para la U; **Ψ medio por metro** para los puentes; probabilidad anual para lo probabilístico; factor adimensional para lo resistente; **indefinido** si falta producto o masa | Deja de haber tres monedas sueltas. La moneda de los puentes **no** es la normalizada, porque depende del área |
| Recuento | **4 filas positivas, 5 negativas, 3 indefinidas, 1 nula por construcción** | De las cuatro positivas, **tres** son sub-márgenes dentro del capítulo 11 y la cuarta es una **elección de proyecto**, no una cifra normativa |
| Margen más fino | **+40 mm** de ancho libre de puerta: una hoja de 900 mm deja 40 mm para marco, bisagra y tope antes de perder los 0,86 m de §11-14 | No dar por hecho que la hoja nominal cumple: hay que confirmar el ancho libre en el listado de puertas |
| Margen que gobierna | La sección: **−415 mm** de alero a 20° con pila de 1 100 mm | Es el mínimo del vector de márgenes, y nada más del proyecto está tan lejos de su límite |
| Por qué no hay margen | Cada opción R2 se resolvió **hasta** los 4 000 mm exactos: el margen se gastó antes de dibujar | **R2 deja de ser preferencia y pasa a ser requisito de §2-2(3)**: elegir una opción que devuelva holgura es lo que produce un margen positivo. Decisión de **Carlos** |
| Los márgenes no son aditivos | El margen de envolvente (+0,011 W/m²K) y el de sección (−415 mm) están en magnitudes distintas, y además están acoplados al revés: recuperar U pide más aislamiento, y el aislamiento cuesta altura | El objeto correcto es un **vector** de márgenes, no un número, y lo gobierna su componente mínimo |
| **Error a evitar** | El **1,4** de riesgos naturales **no** es un margen sobre la clase: F2 = 1/200 y S2 = 1/1000 **ya son** el margen normativo. El 1,4 es un factor parcial sobre los parámetros resistentes de un modelo de ladera | Sumarlos cuenta dos veces. La pantalla debe decir cuál usa; hoy el factor de parámetro está sin verificar y por eso **no se declara** |
| «Indefinido» es una entrada válida | Tres filas lo son porque falta un producto (vidrio), una fracción (§12-7(2)(d)) y una masa (C-07) | Rellenarlas con valores plausibles haría la declaración **parecer** completa y ser inútil. Deben sobrevivir a la siguiente revisión |

**Estado:** declaración emitida y **vigente sólo hasta que se elija R2**, porque la geometría se mueve. Se reemite con la geometría, igual que el FDV y por la misma razón. No es una declaración de cumplimiento. Documento: [declaración de márgenes](declaracion-de-margenes.md).

## T. Condensación en el encuentro del chasis (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Quién cubre esto | **Nadie.** §14-3 limita calor y §13-13 limita vapor; ninguno dice nada de la **temperatura del acero que cruza el aislamiento**, que es lo que decide si el encuentro condensa | Es el hueco entre los dos capítulos que gobiernan la envolvente, y cae justo donde está el chasis |
| El factor de temperatura | ISO 13788: f_Rsi = (θ_si − θ_e)/(θ_i − θ_e), que en 1D es f = 1 − R_si/R_total. Tiende a **0** con una película y a **1** con resistencia infinita | Criterio de moho al **80 %** de HR superficial, no de condensación al 100 % |
| Cuánto aporta el acero | Una placa de 10 mm a λ 50 aporta **0,0002 m²K/W** | No es una resistencia pequeña: es nada. La superficie interior queda a una película del aire exterior |
| El caso desnudo | **f_Rsi 0,236** frente a **0,754** exigido; superficie a **−2,9 °C** con −10 °C fuera — mojada y helada | **No es marginal, es catastrófico.** No es un problema de energía |
| Cuándo condensa | Con acero desnudo, siempre que fuera baje de **5,9 °C**: casi toda la temporada de calefacción en Bergen, no una ola de frío | Un encuentro así pudre la madera que toca, y ninguna cantidad de aislamiento en otra parte de la pared lo cambia |
| La solución tiene tamaño | **0,358 m²K/W** de rotura térmica: ~**9 mm** de espuma rígida, ~**47 mm** de madera, ~**54 mm** de neopreno | Es un número que un detallista puede usar, a diferencia de un valor Ψ |
| Lo que no basta | Un entablado de 22 mm llega solo a **0,617** y **falla** el criterio de moho | «Poner madera encima» no es una rotura térmica |
| Moho frente a condensación | Moho exige 0,358; condensación solo 0,193 | **Dimensionar para moho.** Dimensionar para condensación deja una superficie mojada el tiempo suficiente para crecer |
| Dónde gobierna | La **esquina suelo-pared** exige 0,726 frente a 0,358 de la pared plana, porque su resistencia superficial es mayor | Es exactamente donde va el perímetro del chasis. Una rotura dimensionada en pared plana se dimensiona en el caso fácil |
| Qué mueve el requisito | 40→60 % de HR interior lo multiplica por **3,5×**; −5→−20 °C fuera solo por **2,0×** | La humedad interior manda más que el clima. Ventilación (§13-1(1)) y cuarto húmedo dejan de ser confort y pasan a ser parte del diseño del encuentro |
| El límite honesto | La red 1D ignora el flujo lateral que un puente lineal concentra, así que todo f_Rsi es una **cota superior** | El cribado puede demostrar que un detalle **falla**; no puede demostrar que pasa con margen. Los que pasan lo hacen por 0,022–0,070, que es el orden del error del término 2D ausente |
| Consecuencia | **0,358 m²K/W es un suelo, no un valor de proyecto** | Cualquier detalle adoptado debe superarlo, y cuánto es una pregunta 2D sobre un detalle dibujado que no existe |
| Lo que no se ve | La **perforación de la barrera de vapor**: un miembro del chasis que atraviesa la pared la interrumpe, y el Sd ≥ 10 m de §13-13 solo se cumple si esa interrupción está sellada | La fuga convectiva por un defecto de barrera lleva mucho más vapor que la difusión y es invisible a cualquier modelo 1D |

**Estado:** cribado con **cota superior 1D**, sin cálculo 2D, sin detalle dibujado y sin producto elegido; la temperatura exterior de diseño es un valor de cribado (faltan el NA y C-01). No es un diseño de encuentro ni una declaración de cumplimiento. Informe: [verificación de condensación](verificacion-condensacion-union.md).

## U. La cubierta bajo el capítulo 11: la duda no bloquea, la carbonización sí (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| Qué decía la ficha | Que si la cubierta forma parte del **sistema portante principal** hay que resolverlo antes de congelar el paquete constructivo (S024) | Correcto, pero no es la pregunta que decide el paquete |
| Las cuatro ramas | no. 4 (R 15 si es sistema principal), no. 6.1 (elemento separador), no. 6.2 (todo A2-s1,d0) y no. 6.3 (protección inferior) | Se tabulan con lo que cada una pide de rastrel, aislamiento y revestimiento |
| **El hallazgo** | La columna del aislamiento es **idéntica en las cuatro**: A2-s1,d0 | La duda de interpretación gobierna el **rastrel** y el **revestimiento**, y **no** el aislamiento |
| Por qué | §11-9 D es cláusula independiente: su regla principal exige A2-s1,d0, y la única excepción que alcanzaría una cubierta de madera (no. 7) exige **soporte portante A2-s1,d0 con clase R documentada**. Un rastrel de madera no lo es | El aislamiento es A2-s1,d0 sea o no sistema principal. Y 6.2 y 6.3 lo dicen con sus propias palabras |
| **Consecuencia** | **La cubierta se puede congelar ya**, como lana mineral | La duda no bloquea el paquete constructivo; bloquea la sección del rastrel y la clase del revestimiento |
| no. 6.2 | Exige que **todos** los materiales de la cubierta, aislamiento incluido, sean A2-s1,d0 | **Cerrada.** Describe una cubierta incombustible, que no es este edificio |
| no. 6.1 | Disponible pero es una decisión arquitectónica: un techo con resistencia al fuego | Cambia la sección, no la estrategia |
| no. 6.3 | La ruta realista: revestimiento **K210 B-s1,d0**, o **D-s2,d0** en clase de riesgo 4, con aislamiento A2-s1,d0 | Es la rama que hay que desarrollar |
| Si aplica R 15 | Es un problema de **carbonización**, no de espesor: 0,65 mm/min más k₀·d₀ da **15,0 mm** efectivos por cara a 15 min | La velocidad de carbonización ataca la dimensión estrecha **dos veces** |
| Cuánto cuesta | **48 × 198 conserva el 32 %** de su módulo de sección; 48 × 223 el 33 % (más profundo no ayuda); 73 × 198 el 50 %; 98 × 198 el 59 % | La paridad pide **78 mm** de ancho, es decir **98 mm** comercial: el rastrel **duplica su ancho**, no su canto |
| Con carga desconocida | No hay modelo estructural ni C-07, así que el momento accidental se **barre** como fracción de la capacidad en frío, no se supone | El rastrel de 48 mm **falla en todos los barridos**. El patrón importa más que una celda |
| Las dos salidas | Revestimiento inferior que retrase la carbonización, o rastrel más ancho | **Convergen:** el revestimiento es lo que ya pide no. 6.3. Tres cláusulas, un dibujo |
| **La fracción de madera** | **No es una propiedad del material: es ancho ÷ separación.** El 15 % uniforme implica montantes de **90 mm** | A 48 mm y 600 mm la cubierta necesita **214 mm**, no 245. Pero placas, riostras y refuerzos suben la fracción efectiva: el alivio real es **13–31 mm** |
| Coste del ramal R 15 | Con rastrel de 98 mm la fracción sube al 16,3 % y la cubierta necesita **251 mm**: **+37 mm**, o **+40 mm de alero** | Es el mayor acoplamiento entre el capítulo 11 y la sección, y es mayor que el que cuesta la elección de aislamiento (**25 mm**) |

**Estado:** determinación de las ramas y cribado de la carbonización; **no es un informe de ingeniería de incendio ni una comprobación estructural**, y las cargas se barren porque no existen. Documento: [determinación de la cubierta](determinacion-cubierta-incendio.md).

## V. El bucle cerrado: los espesores de R2 y la solicitud de dispensa (2026-11-17)

| Punto | Resultado | Consecuencia para MiniHouse |
|---|---|---|
| De dónde venían los espesores | Las cuatro opciones R2 se resolvieron con **suelo 250 mm y cubierta 300 mm**, atribuidos al [cribado de envolvente](verificacion-envolvente.md) | **No vienen de ahí:** son números redondos. El solucionador devuelve otra cosa |
| Qué devuelve de verdad | Con 15 % de madera: suelo **281 mm** (241 de aislamiento), cubierta **278 mm** (245) | El suelo es **31 mm más grueso** y la cubierta **22 mm más fina** |
| Cuánto se equivocaba lo publicado | Los dos errores **casi se cancelan**: el alero publicado es optimista en unos **7 mm** | El caso de referencia era **cercano, no falso**, y el déficit es robusto: **−422 mm**, no −415 |
| Qué **no** era cercano | La **fracción de madera**. Es **ancho ÷ separación**, no una propiedad del material | El 15 % uniforme era una **elección**, no un resultado. Re-resolver era obligatorio |
| Al re-resolver | 15 % → 12 % → 8 %: R2-B pasa de **23 % a 34 %** de cobertura; R2-D de **96 % a 100 %** | Es la **única palanca de sección que no cuesta nada** en el límite de transporte, y vale **28–64 mm** de alero |
| **La corrección que importa** | La dispensa de R2-D a **4 400 mm** **no basta**: la cobertura total a 20° con pila de 1 100 exige **4 415 mm** con los espesores publicados y **4 422 mm** al 15 % | Los 4 400 mm nunca fueron el umbral de cobertura total: eran un número redondo que cayó en el 97 % |
| A qué fracción sí basta | 12 % → **4 394 mm**; 8 % → **4 358 mm** | Con madera esbelta, 4 400 mm sobra. Pero hay que **saberlo antes de escribir la solicitud** |
| Por qué importa el número | **El número que se escribe en la solicitud es el que se evalúa** | Pedir 4 400 cuando hacen falta 4 422 invita a un rechazo que un bastidor algo más esbelto habría evitado |
| La lección, otra vez | Es la misma que produjo la determinación de cubierta: **declarar ancho y separación, no una fracción** | Una fracción escrita como si fuera una propiedad convierte una elección de cribado en una base falsa |

**Estado:** opciones re-resueltas contra los espesores reales; **sigue sin haber selección** y la geometría sigue sin congelar. La corrección no cambia qué opción es preferible, cambia **qué hay que pedir** y cuánto margen queda. Documento: [opciones de sección R2](opciones-seccion-R2.md).

## W. Las ventanas: tres lecturas de §11-13, y la que hay que construir (2026-11-17)

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Cuántas ventanas de escape exige §11-13? | Depende de una lectura que **no es análisis**. §11-13(1) pide *una salida a lugar seguro* y la puerta P-01 da a ras de suelo; §11-13(4) sólo relaja la regla de las dos direcciones, y lo hace «forutsatt at hver branncelle har **vinduer**» — en plural | Tres lecturas: **A** la puerta basta (no exige nada), **B** la celda necesita dos ventanas cualificadas, **C** cada cuarto sin salida directa necesita la suya |
| ¿Cuál es el cuarto que decide? | El **baño**: no tiene salida directa y su única abertura, V-03, falla por tres motivos (alto 500, suma 1 000, antepecho 1 500) | B y C discrepan justo ahí, y por eso la lectura no se puede resolver mirando la tabla |
| ¿Cuánto cuesta cada lectura? | **A** 0 m². **B** **100 mm** de antepecho en V-02 y **cero** vidrio extra (falla sólo el antepecho). **C** **0,29 m²** en V-03 | Construir la unión de las tres cuesta **0,29 m²** y una decisión de antepecho. Es más barato que discutir la lectura |
| ¿Y la frase que hace parecer que la tabla cumple? | «one accessible escape window is sufficient in a dwelling unit» está en la tabla de **acceso del servicio de bomberos** y habla de §11-17 | Leída como relajación de §11-13(4) hace pasar la tabla R0 con V-01 sola. **No lo es**, y la duda se pregunta al municipio en la misma carta que C-01 |
| ¿Qué tamaño tiene la ventana mínima? | El área cualificada tiene **dos mínimos iguales** en la recta de la suma: 600 × 900 y 900 × 600, ambos **0,54 m²**; entre ellos **sube** a 0,5625 (750 × 750), así que la ventana cuadrada es la peor de la banda. El mínimo absoluto es una ranura de 500 × 1 000, **0,50 m²** | Se elige **900 × 600**: el más ancho de los dos mínimos, y módulo comercial. La ranura ahorra 0,04 m² y cuesta la única propiedad que importa, que es poder salir por ella |
| ¿Dónde va la del baño? | La pared trasera del baño mide **1 200 mm**: a 900 de ancho quedan **150 mm** de jamba, insuficiente para una esquina estanca. El **hastial en x=0 mide 3 000 mm** | V-03 se **mueve al hastial**. No cuesta nada en luz diurna porque §13-7 no distingue orientación |
| ¿Se cruzan §11-13 y §13-7? | **Sí, y por eso este es el único sitio donde una decisión arregla dos cribados.** El vidrio cualificante pasa de **2,47 a 2,76 m²** y el LT mínimo de **0,600 a 0,537** a ff 0,85 | Antes el §13-7 exigía 0,600–0,638, en el techo de lo disponible; después, 0,537–0,571. No demuestra que se cumpla —no hay acristalamiento elegido— pero **baja el listón 0,06** |
| ¿Qué cuesta en calor? | +0,284 W/K por el vidrio **y** +0,050 W/K por el perímetro de hueco que se alarga (Ψ 0,05 W/mK, detalle corriente) | Los dos efectos **suman**, no se cancelan: el vidrio desplaza pared pero alarga la junta. Total **+0,334 W/K**, 1,7 % de la envolvente |
| ¿Qué cambia en la declaración de márgenes? | Las filas 3 y 4 estaban escritas sobre **V-01**, la única que cumple, y daban +100 mm de antepecho y +500/+700/+800 de tamaño | Estaban **bien de V-01 y mal del requisito**. Reescritas sobre la peor ventana: **−500 mm** de suma y antepecho en V-03, **−100 mm** de antepecho en V-02. El recuento pasa de 4/5/3/1 a **2/7/3/1** |
| ¿Cuál es ahora el mínimo del vector? | Por **magnitud**, la ventana de escape a **−500 mm**, por delante de la sección a −422. Por **consecuencia**, la sección: la ventana se cierra agrandando un hueco y la sección no | Las dos afirmaciones son ciertas y ninguna sustituye a la otra. El recuento de la declaración se **parsea** ahora de la tabla, así que no puede resumir una versión vieja |
| ¿Qué queda abierto? | Qué hay **bajo** la ventana del baño (§11-13 admite antepecho 1,0 m «unless measures ease escape»; un WC o un plato de ducha lo suben), el antepecho de la ventana de cocina contra la encimera, y la lectura municipal | Son tres preguntas de **Carlos** y del municipio, no de cálculo |

**Estado:** las tres lecturas están valoradas y la tabla de aberturas **sigue sin cambiar** — la revisión es una propuesta, no una decisión. Documento: [ventanas](verificacion-ventanas.md).

## X. ¿Son adecuados los márgenes? Ninguna fila pasa el test (2026-11-17)

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Qué pedía la declaración y no hacía? | §2-2(3) pide márgenes *necesarios*, y la declaración define adecuado como **positivo y mayor que la incertidumbre** del modelo que lo produjo. La columna de incertidumbre estaba vacía | Se llena, y el resultado es **0 adecuadas, 8 no adecuadas, 5 no comprobables** |
| ¿Cuántas clases de incertidumbre hay? | **Cuatro**: modelo (error de la idealización), dato (parámetro sin medir), interpretación (qué ytelse aplica) y ejecución (tolerancia) | Sólo la segunda se reduce tomando datos. La primera pide mejor modelo, la tercera una decisión, la cuarta un detalle |
| ¿Qué filas se pueden barrer? | Tres: U del muro frente a la fracción de bastidor, sección frente a la fracción de madera, Ψ″ frente al nivel de detalle | Las demás se declaran por su clase, no con un número inventado |
| ¿Qué pasa con el **+40 mm** de la puerta? | Es el margen positivo más fino y **no está demostrado**. Son 40 mm porque una hoja de 900 supera en 40 el requisito de 860 — pero el requisito es sobre el **ancho libre**, que es la hoja menos bastidor, bisagra y tope | Un juego de puerta corriente se lleva 30–60 mm. El margen está entre +10 y −20 mm y **el signo es desconocido**. No es que la puerta falle: es que **todavía no hay margen, hay una hoja nominal** |
| ¿Y la U del muro? | A 189 mm y 15 % da **0,2202** frente a 0,2200: está **sobre** el límite porque 189 mm es el espesor que se **resolvió** para llegar ahí | Es **nula por construcción**, igual que la fila del transporte. La declaración sólo admitía una de las dos. Los valores 0,267 / 0,209 que llevaba son del **espesor por defecto de 150 mm** — diagnóstico de que la penalización de montantes es lo que rompe el muro, no margen de proyecto |
| ¿La sección sobrevive a su incertidumbre? | Sí en signo, no en magnitud: de **−358 mm** (8 %) a **−498 mm** (23 %), todo negativo | Pero **−422 mm es el valor del 15 %**, y la tabla de sensibilidad de R2 baja a 8 % y nunca sube. Se está citando un valor de banda media donde corresponde el caso peor |
| ¿Y los puentes térmicos? | De **−0,067** (buen detalle) a **−0,347** (malo): negativo en los tres niveles, pero la magnitud se mueve por un factor de tres | El signo es robusto y la fila no es accionable, porque la referencia de 0,05 W/m²K no vincula |
| ¿La condensación? | **+0,051 m²K/W es un techo, no un valor**: un campo 1D no captura el reparto 2D alrededor de un acero que atraviesa el aislamiento, y repartir **sube** f_Rsi | El requisito de 0,358 es un suelo y el margen un techo — al revés de lo que hace falta para proyectar. Pide cálculo 2D sobre un detalle dibujado. **Corregido en §Y**: el 2D no estrecha el margen, le **cambia el signo** |
| ¿Qué falta por completo? | La **tolerancia de ejecución**, en todas las filas | No hay detalle ni especificación que la soporte. Se registra la ausencia en vez de rellenarla |
| ¿Qué cambia en la declaración? | Recuento **2/6/3/2** (antes 2/7/3/1), §8 nueva con el test de adecuación, y la fila 7 reescrita | El recuento se sigue **parseando** de la tabla, así que no puede resumir una versión vieja |

**Estado:** la declaración ya no dice sólo «faltan márgenes», dice **«ninguno de los declarados es adecuado, por el criterio que ella misma fija»**. Documento: [adecuación](verificacion-incertidumbre.md).

## Y. El encuentro resuelto en 2D: el acero no es el punto frío, y envolverlo gana por 3 W/K (2026-11-17)

Todo f_Rsi del repositorio era un número **1D**, y la pantalla de condensación lo decía con
honradez: un camino 1D no tiene resistencia de reparto, así que el valor es una cota y el
requisito un suelo. Lo que también decía —y no era cierto— es que la cota iba **en la dirección
conservadora**. `scripts/puente_2d.py` resuelve ∇·(λ∇T) = 0 en volúmenes finitos con las
películas superficiales como condiciones de Robin, y devuelve el punto interior más frío, su
posición y el Ψ del encuentro según ISO 10211.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Se puede usar un solver 2D sin validarlo? | No. Cuatro pruebas corren antes: una losa 1D debe reproducir su f_Rsi analítico (**0,9207** modelado frente a **0,9823** analítico), las capas en serie su resistencia exacta a 1e-12, el flujo se conserva a **1e-6**, y el resultado debe ser estable al refinar | La malla de 2 mm converge a **±0,005**. Las de 3 y 4 mm **no se usan**: la placa de 10 mm queda a dos o tres celdas de ancho y la respuesta dispersa ±0,02. Esa dispersión es la incertidumbre de modelo del cribado y se declara |
| ¿Qué da el acero en 2D? | **0,377**, frente a los 0,236 del 1D | El 1D era **pesimista** con el acero: asumía que toda la superficie era acero, sin aporte lateral del suelo que lo rodea. La conclusión seguía siendo válida —era una cota— pero **la dirección de error declarada estaba al revés** |
| ¿Y el requisito de 0,358 m²K/W? | Es correcto **para la superficie donde se calculó** y falso para el edificio. El acero deja de ser el punto más frío **al primer milímetro de separación**; desde 3 mm **la esquina de madera gobierna** en todo espesor | En 2D, 9 mm da **0,693** —por debajo del criterio— y **20 mm llega a 0,754**. El requisito es **0,80 m²K/W**, no 0,358: el 1D se queda **0,44 corto**, no 0,05 largo. La fila 13 de la declaración pasa de +0,051 a **−0,39**, y el signo se **invierte**, no se estrecha |
| ¿Suplementar el acero o moverlo? | Moverlo. La misma placa **por debajo del suelo, fuera del aislamiento**, da **0,921** y **Ψ +0,027** — idéntico a la esquina desnuda hasta tres decimales, sin suplemento, sin material y sin espesor | Suplementar nunca llega: 60 mm de espuma dan 0,863 y sigue subiendo hacia una asíntota por debajo del valor envuelto. La respuesta de proyecto es **pasar el aislamiento por fuera del acero** |
| ¿Cuánto cuesta equivocarse? | Con el acero dentro, **3,50 W/K** sobre 18 m de perímetro; envuelto, **0,49 W/K**. Diferencia **3,01 W/K**, ~**16 %** de la pérdida por elementos (19,4 W/K en los límites de §14-3) | Una decisión de dibujo mueve el balance térmico más que **todas las elecciones de aislamiento del proyecto juntas** |
| ¿Qué pasa con la tabla genérica de puentes? | Asumía **0,10 W/mK** para el perímetro del suelo; el 2D da **0,027** envuelto y **0,195** sin envolver | El valor genérico cae **entre** los dos, lo que confirma la conclusión de aquella pantalla —los puentes hay que **diseñarlos**, no estimarlos— y explica por qué su número no se podía mejorar sin un detalle |
| ¿Y el rastrel perimetral? | En bruto parece sumar **+0,014 W/mK** al encuentro en toda posición dentro de la ventana modelada. No lo hace: la U del suelo sube de **0,1363** a **0,1716** con la fracción del 12 % que contiene la ventana, y eso explica todo el desplazamiento. Referido a la U del suelo con rastrel, el encuentro lee **+0,028** — la esquina sin rastrel | **Un modelo 2D de unión y una U de elemento por vía paralela no pueden contar el mismo rastrel dos veces.** Es la misma familia de error que la fracción de montantes. Lo que el rastrel cuesta en la unión es poco (f_Rsi 0,921 → **0,906**), porque el entablado de 22 mm reparte. El rastrel **perpendicular** cruza el perímetro como un **punto** y es un efecto 3D que esta sección no ve |
| ¿Esto es un valor de proyecto? | **No.** Una placa de 10 mm no es un perfil: no hay A, W, I, J, espesor ni grado (C-07). Un perfil real tiene ala superior en contacto con el suelo en todo su ancho, y leerá mejor que la placa y peor que el caso envuelto | La esquina 3D, el varenga perimetral y el campo de vapor quedan fuera. El 2D es un **instrumento**, no un detalle de encuentro |

**Estado:** el proyecto ya no tiene «un requisito de rotura térmica de 0,358 m²K/W» sino **una
decisión de posición**: el acero va **por fuera** del aislamiento, y entonces no hace falta
rotura. Documentos: [conducción 2D](verificacion-puente-2d.md),
[condensación](verificacion-condensacion-union.md), [declaración](declaracion-de-margenes.md).

## Z. Las ventanas y la puerta son una sola pregunta (2026-11-17)

El proyecto llevaba la ventana de escape, el ancho de la puerta y la clase de superficie
como tres preguntas con tres precios. Dos de ellas son la misma, y la tercera no lo es.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Qué dice §11-13(4) exactamente? | Está escrito como **alternativa**: la salida va a **lugar seguro**, *o* a una **rømningsvei** con una sola dirección y entonces hacen falta ventanas | No es un permiso que se sume a una salida a lugar seguro. Es una cosa o la otra |
| ¿Y §11-14? | Gobierna la **rømningsvei** y las puertas en o hacia ella | Si no hay rømningsvei, no hay nada que gobernar: los 0,86 m no se exigen |
| ¿Qué filas de la declaración se mueven? | **2, 3 y 4** — ancho libre de puerta y las dos de ventana de escape | Con lugar seguro las tres dejan de ser requisito y el recuento cae a **1 positiva / 4 negativas / 3 indefinidas / 2 nulas** sobre diez filas. La única positiva que queda es la del resguardo de inundación, que es elección de proyecto |
| ¿Y con rømningsvei? | Las tres son obligatorias, y se construyen por **0,29 m²** de vidrio (V-03 a 900 × 600) y **100 mm** de antepecho en V-02 | Es la respuesta conservadora y es edificable. La favorable no la puede adjudicar el proyecto a sí mismo |
| ¿§11-9 se mueve con esto? | **No.** Una celda que no contiene rømningsvei sigue siendo una celda, así que la fila de ≤200 m² (**D-s2,d0**) aplica decida lo que decida §11-13 | Acoplar las dos habría condenado el interior de madera recuperada por una lectura que no lo alcanza. Y al revés: una respuesta favorable en ventanas tampoco convierte el interior en superficie de rømningsvei |
| ¿Cuánto se anda por dentro? | **5,04 m** desde la esquina del baño hasta la jamba más próxima, en línea recta | Frente a los 15 m que el texto recuperado contiene, el margen es +10 m. Pero la fila de la tabla 1 de §11-13 para clase de riesgo 4 **no se ha leído nunca**, y la cifra de §11-14 es de puerta de celda a salida, no de recorrido interior |
| ¿Qué superficie hay en juego si la respuesta fuese B-s1,d0? | **48,5 m²** de madera interior expuesta en la sección de referencia (alero 1778 mm, cumbrera 2324 mm) | No se le pone precio porque no hay producto elegido. Se da el área para poder ponerlo |

**Estado:** la pregunta al municipio es **una**, no tres: *¿la salida de la casita va
directamente a un lugar seguro, o a una rømningsvei con una sola dirección de escape?*
Documento: [determinación](determinacion-estrategia-incendio.md).

## AA. La ventilación que seca el encuentro es la que ahoga la estufa (2026-11-17)

§13-1(1) pide caudales de aire alternativos **documentados**. El proyecto llevaba cuatro
registros de esa frase y ningún caudal. Ya los hay — y al producirlos aparece algo que el
capítulo 13 no había mirado, porque es un problema de **presión**, no de caudal.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Qué caudales hay que documentar? | §13-2 no vincula en esta ruta, así que se adoptan sus tarifas **voluntariamente**: **21,6 m³/h** por vivienda, **52 m³/h** por plazas de cama, y una extracción de **90 m³/h** básica (cocina 36 + baño 54) y **108–216 m³/h** forzada | Adoptar una cifra verificada y decir que no vincula es más defendible que inventar una. La extracción gobierna, no la impulsión |
| ¿Por qué 108–216 y no una cifra? | La fuente da el forzado **por local** y no dice si los dos locales fuerzan a la vez | Se llevan las dos lecturas. La segunda es la cota superior y es la que destapa el problema |
| ¿Qué pasa si no hay reposición? | Un ventilador en una caja sellada **no mueve aire**: baja la presión hasta que la fuga de la envolvente lo aporta. Con 36,9 m³ a 1,5 h⁻¹@50 Pa, la extracción básica sostiene **106 Pa** y la forzada de un local **140 Pa** | Son presiones grandes, no pequeñas. La de los dos locales a la vez pide 406 Pa, que **ningún ventilador da**: ese caudal no se entrega y el déficit es de ventilación, no de selección de ventilador |
| ¿Y la estufa? | Un tiro de chimenea es de **10–20 Pa**. Contra 140 Pa de depresión el tiro **se invierte** | Margen **−130 Pa**, medido contra la mayor presión que el ventilador **puede sostener**. Es el único margen de **seguridad** de la declaración (fila 14) y es negativo |
| ¿Por qué no se cita el caso de 406 Pa? | Porque no es una presión a la que la casita esté: es un caudal que el ventilador no alcanza | Citarlo contra el tiro habría dado −396 Pa y **exagerado** el caso. El margen se calcula sólo con presiones alcanzables |
| ¿Cómo se arregla? | **Aire de reposición dedicado** dimensionado con la extracción, y **aire de combustión propio** para la estufa, directo de fuera y por debajo del hogar | Ninguna de las dos es opcional, y cada una es un agujero en la barrera de vapor: **las filas 13 y 14 son el mismo dibujo** |
| ¿Cierra el lazo con la humedad? | **No, y se dice.** Un balance estacionario sin el amortiguamiento de la madera da una concentración por encima de la saturación a cualquier caudal plausible, que es obviamente falso en un interior de 48,5 m² de madera | Cerrarlo pide un modelo dinámico de sorción y datos de material que el proyecto no tiene. Lo que sí se afirma es la **dirección**: el 50 % de HR es conservador, así que la fila 13 sólo puede mejorar |
| ¿Toca §13-5? | Sí, y no se evalúa: la depresión sostenida es justamente el mecanismo que arrastra radón del suelo y anula una barrera por hermética que sea | Se registra el mecanismo; no se afirma nada sobre la concentración |

**Estado:** la fila 14 entra en la declaración con **−130 Pa**. Documento:
[ventilación](verificacion-ventilacion.md).

## AB. El aire de reposición tiene tamaño, y no compra el tiro (2026-11-17)

La §AA terminó en una decisión sin número: el aire de reposición tiene que venir de algún
sitio. Ya tiene tamaño — y al calcularlo aparece que **el agujero resuelve la ventilación y
no resuelve la estufa**, que son dos problemas que la §AA había dejado juntos.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Cuánto mide el agujero? | Una entrada de área A pasa `Q = 3600·Cd·A·√(2Δp/ρ)`. Sostener una depresión elegida con los 108 m³/h de diseño fija A: **113 mm a 10 Pa**, o 89 mm a 20 Pa | Es una válvula de fachada, no un sistema. La ventilación se resuelve con una pieza |
| ¿Qué depresión se elige? | La **más baja** que siga siendo tamaño estándar y sostenible con viento: 10 Pa. Elegir el agujero más pequeño sería elegir la presión más alta y llamarlo eficiencia | A 10 Pa la extracción básica cae a 7 Pa: quita **98 Pa** de los 106 que llevaría |
| ¿Y el tiro? | A 10 Pa el margen contra 10–20 Pa de tiro es **0 a +10 Pa**. La única depresión que pasa el test de §2-2(3) —positivo **y** mayor que su incertidumbre— es **2 Pa**, que pide **181 mm** | 2 Pa está por debajo de la presión que un viento de 3 m/s ejerce sobre el mismo muro: **una entrada pasiva no puede sostener una presión fijada**. El viento la fija |
| ¿Depende del límite de 125 mm? | **No.** Aflójalo y la fila de 2 Pa pasa a ser tamaño estándar, pero sigue por debajo del viento | El límite decide cuánto de la tabla es construible; el viento decide que ninguna fila adecuada lo sea |
| ¿Entonces? | La fila 14 **se retira, no se mejora**: una estufa **estanca** toma el aire de combustión de fuera y equilibra su tiro contra el exterior, así que la presión de la cabina no entra en el tiro | Es un requisito de especificación sin coste dimensional, y la **única fila negativa con una salida gratis**. Hasta que se adopte, la fila sigue en **−130 Pa** |
| ¿Cuánto cuesta el aire? | **905 W** a 30 K sin recuperación, **181 W** con el 80 %. La pérdida del cerramiento es **18,3 W/K** → 550 W | El aire de reposición cuesta **1,65× el cerramiento**: la recuperación de calor es precondición, no mejora. En 18 m² eso no es una partida, es el diseño |
| ¿Y la barrera de vapor? | Por difusión el agujero lleva el **0,8 %** de la conductancia de la barrera (Sd 10 m sobre 48,5 m² contra 264 mm de aire: factor 38) | Por difusión no es el problema. El riesgo es **convectivo**, y ninguna cuenta de Sd lo alcanza: la entrada es un **problema de control** —válvula cerrable y estanca—, no de difusión |
| ¿Y §13-5? | La depresión baja de 106 a 7 Pa, un factor de **14,9** | Es una mitigación real y no evalúa radón. Lo que cambia es que la mitigación tiene tamaño |

**Estado:** la fila 14 no cambia de valor; cambia de naturaleza. Documento:
[aporte de aire](verificacion-aporte-aire.md).

## AC. §13-5 pide una barrera «contra el terreno», y este piso no está sobre el terreno (2026-11-18)

La §AA registró que la depresión sostenida activa el mecanismo de §13-5 y que no se evaluaba.
Lo que sí se puede evaluar sin emplazamiento es la forma del problema — y la forma resulta que
no es la que el capítulo describe.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Qué pide exactamente §13-5? | Dos cosas distintas: un **rendimiento** (media anual ≤ **200 Bq/m³**) y una **ruta prescriptiva** (barrera **contra el terreno** + preparación para reducir presión por encima de **100 Bq/m³**, salvo que se documente innecesaria) | No son la misma pregunta y este edificio las responde de forma distinta |
| ¿Cuál es la frase que decide? | **«contra el terreno»**. El piso está sobre un hueco ventilado sobre el chasis — `envelope_check` ya lo modela como capa ventilada | La ruta prescriptiva describe un detalle que el edificio no contiene. La pregunta es si el hueco **es** la medida o si la barrera hay que construirla igual |
| ¿Se puede cerrar sin emplazamiento? | **No**, y se dice. Lo que sí se cierra es cuánto margen deja la aritmética | Si el margen es enorme, el emplazamiento importa poco; si es estrecho, lo decide todo |
| ¿Hay una cota? | Sí: **C ≤ E/Q**. Incluso en el caso patológico en que **cada átomo exhalado bajo la huella llega al interior**, la concentración no pasa de E dividido por el caudal de ventilación | Es independiente del hueco, de la estanqueidad del piso y del detalle del encuentro. Es la cota que hace argumentable la ruta de «documentado innecesario» |
| ¿Cuánto vale? | **3,6–36 Bq/m³** en terreno ordinario, con 90 m³/h sobre 18 m² de huella | **5,6× por dentro** del límite en el extremo alto de la horquilla. El margen no es un resultado del modelo: es que 90 m³/h pasan por 18 m² |
| ¿Y el hueco? | Es un volumen tampón, y un hueco abierto no es un tampón: es aire exterior (864 renovaciones/h a 150 mm). Uno **con faldón** renueva 19–32 veces por hora, porque el volumen es pequeño y el perímetro no | El tampón es robusto por geometría. Y hay que **no destruirlo**: un faldón sellado o rellenar el hueco con aislante lo eliminan, y entonces queda la cota |
| ¿Dónde se acaba? | **Esquisto de alumbre**: a 300 mBq/(m²·s) la cota es **216 Bq/m³**, por encima del límite | El signo es un hecho del emplazamiento, no del modelo. **C-01 decide esto y la aritmética no** |
| ¿Dónde va la barrera, si se construye? | La ruta prescriptiva **no se descarga**: hasta que haya medición, la barrera se queda. Pero es un requisito de **estanqueidad**, no de Sd — y el Sd ≥ 10 m de la barrera de vapor **no lo satisface por construcción** | Su continuidad es el **encuentro piso-pared**, 18 m del mismo rincón que resolvió el cálculo 2D. Un dibujo contesta calor, vapor y radón, o no contesta ninguno |
| ¿Y los agujeros? | La entrada de aire de reposición va en el muro, **por encima del piso**: está en la *otra* membrana. El desagüe es la penetración húmeda que pide collarín sellado | El aire de combustión de la estufa se vuelve pregunta de barrera en cuanto se toma de debajo del tablero en vez del muro |

**Estado:** fila 15 de la declaración, **indefinida**, +164 a −16 Bq/m³. No se declara el caso de
esquisto de alumbre como margen: sería el mismo error que citar los 406 Pa contra el tiro, que
exageró el problema en 266 Pa. Documento: [radón](verificacion-radon.md).

## AD. El encuentro tiene dibujo, y lo genera el solver (2026-11-18)

Cinco pantallas aterrizan en la misma esquina y ninguna la había dibujado. Los planos de
`fase1/planos/` están escritos a mano, que es justo el modo de fallo que este proyecto ya ha
pagado cuatro veces. Así que el detalle se **genera**.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Qué dibuja? | El encuentro piso-pared del sector de referencia: pared de **264 mm** en 5 capas, piso de **280 mm** en 3, la viga perimetral arropada por debajo, el hueco ventilado y el terreno | Cada cota sale de `puente_2d.WALL_LAYERS` y `FLOOR_LAYERS`. El autotest falla si el dibujo deja de coincidir con ellas |
| ¿Qué resuelve que la prosa no? | **Si el acero cruza la barrera de vapor.** La barrera gira en **(13, −22)** — detrás del forro, por encima del aislante. La placa ocupa el espesor del piso en la cara interior, así que **cruza ese plano** cuando no va arropada | Arropar no es un grosor de aislante: es una instrucción de dibujo. Quita el puente (0,377 → **0,921**) y deja la barrera continua **de una vez** |
| ¿Y el hueco? | Se dibuja a 300 mm nominales, marcado **C-05 sin definir** | Es el tampón de radón que §13-5 no puede perder: el dibujo lo deja a la vista para que no se cierre por descuido |
| ¿Y el desagüe? | Es la única penetración húmeda a través del piso | La entrada de aire de reposición va en el muro, en la otra membrana |
| ¿Qué NO es? | **Conceptual, no para fabricación.** Perfil del chasis sin definir, R2 sin elegir, nada liberado | El dibujo muestra dónde chocan las exigencias, no un detalle constructivo cerrado |

**Estado:** `fase1/planos/detalle-encuentro-R0.svg`, generado por `scripts/detalle_encuentro.py`,
check 32. La guarda prohíbe que vuelva a existir un plano del encuentro sin su línea de estado.

## AE. La guía de §2-2 acota la prueba de márgenes, y no la alivia (2026-11-18)

El hueco de procedencia más antiguo del proyecto queda cerrado: la **veiledning** de
§§2-2/2-3/2-4/4-2 y la introducción del capítulo 2, en [S030](../knowledge/sources/S030.md). Las
cuatro páginas se renderizan en cliente y cuatro intentos devolvieron sólo navegación; el texto
estaba en el DOM, colapsado tras un control que no aceptaba clic, y leer el `textContent` de
`<main>` lo devolvió entero — 50 kB donde `inner_text` daba 2,6 kB.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿La prueba de márgenes se aplica a las quince filas? | **No.** La guía dice «Hvilke sikkerhetsmarginer er lagt til grunn (**nødvendig ved mer omfattende analyse**)», y admite que «en enkel faglig vurdering eller et logisk resonnement» baste | La declaración aplicaba la prueba a quince filas sin clasificarlas nunca. **Nueve** son análisis, **cuatro** ytelser declaradas (2, 3, 4, 10) y **dos** determinaciones (6, 9) |
| ¿Sacarlas de la prueba las alivia? | **No, al contrario.** Una ytelse declarada se cumple o no se cumple, y §2-2(1) sólo permite desviarse por **dispensación** municipal (PBL cap. 19), con la prueba «klart større fordeler enn ulemper» | Las filas 3 y 4 no son dos márgenes negativos finos: son **dos desviaciones de −500 mm que necesitan dispensación**, que es más difícil de obtener que un margen positivo. La fila 2 tampoco era el margen más fino: es un ancho libre sin acotar |
| ¿Un margen y una tolerancia son lo mismo? | **No.** La introducción del capítulo 2: «skal disse forstås som **absolutte krav**, så fremt det ikke i forskrift eller i vedtak […] er gitt konkrete toleranser». NS 3420 rige la ejecución **medida**, no el proyecto | Resolver *a* 4000 mm y *a* 0,2202 gasta una tolerancia que nadie ha concedido. Es la versión normativa de la conclusión que la pantalla de adecuación ya había alcanzado por los números |
| ¿Y §2-2(4)? | La guía prescribe la **ytelsesoversikt** en tres categorías: ytelser dadas en la norma, preaksepterte brukt, y documentadas por análisis; y admite que haga falta **suppleres con planos**, «for eksempel for sikkerhet ved brann» | El objeto **no existe**. §2-2(4) estaba registrado como insatisfecho-hasta-R2, que es cierto del *contenido*, pero la clasificación que necesita es la misma que la del alcance de los márgenes |
| ¿Qué no cambia? | **Nada del texto vinculante.** S029 sigue siendo la fuente de los requisitos; S030 sólo dice qué significan | Ningún requisito se mueve, ningún margen mejora: **0 adecuados, 5 no adecuados, 4 intesteables** sobre nueve filas |

**Estado:** `CLASS` en `scripts/incertidumbre.py` es la única autoridad de la clasificación, porque
decide dos cosas a la vez — el alcance de §2-2(3) y las tres categorías de §2-2(4). El autotest
falla si una fila queda sin clase o si una ytelse sale de la prueba sin decir qué la gobierna.

## AF. La ytelsesoversikt existe, y dice que el edificio no descarga nada (2026-11-18)

§2-2(4) estaba registrado como insatisfecho-hasta-R2. Eso es cierto del **fundamento** —la sección no
cierra, así que la base no puede ser suficiente— y nunca lo fue del **objeto**, que es lo primero que
pide un tramitador. El material llevaba quince informes ahí; lo que faltaba era ensamblarlo.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Cuántas categorías? | Tres, las de la guía: ytelser dadas en la norma, preaksepterte usadas, documentadas por análisis. Más una **cuarta explícita** para lo que no es ytelse | **38 filas**: 27 / **0** / 4 / 7. La cuarta no es un cajón: es lo que impide que la tabla se lea como una promesa de prestaciones que el edificio no debe dar |
| ¿Por qué no hay ninguna preakseptert? | Porque el edificio no tiene cimentación, ni envolvente montada en obra, ni cubierta convencional | **§2-2(2)(b) no es una opción entre dos: es la única ruta.** Eso sube el listón de §2-2(3) en vez de bajarlo — no hay respaldo en el que una lista sustituya a un argumento |
| ¿Cuántas ytelser se cumplen? | **Ninguna de las 31.** 9 incumplidas por el cribado, 20 indeterminadas, 2 no aplican | Es lo que significa R0. Un cribado no es una verificación, y las dos filas que se leerían como «cumple» —detección de humo y clase de superficie— son especificaciones que nadie ha escrito |
| ¿Cuatro decisiones desbloquean el edificio? | **No.** 21 decisiones distintas cierran las filas y **17 cierran exactamente una** | C-01 cierra 4, un producto 3, R2 3, el resto son individuales. El trabajo que queda es mayormente **uno a uno**, con dos palancas reales: el emplazamiento y la sección |
| ¿Y las que no esperan a una decisión? | Dos esperan a **trabajo**: la estanqueidad de §14-3 nunca se ha medido (§2-4 nombra `tetthetsmåling`) y §15-5 no tiene proyecto de instalación | Se cierran en una tarde, no en una reunión — **corregido en AG**: la estanqueidad es barata en dinero y no en tiempo |
| ¿Qué garantiza que no derive? | Cada valor se lee de la constante del script que lo posee (`ec.U_LIMITS`, `rc.RADON_LIMIT_BQ`, `fc.R_MAIN_MIN`, `vc.N50_PER_H`, `ic.BACKFLOW_HEAD_MM`) | Una constante no puede moverse sin que la tabla la siga, y el autotest falla si una fila de la declaración deja de estar citada: las dos piezas son un conjunto, no dos listas |

**Estado:** `fase1/ytelsesoversikt.md`, generado por `scripts/ytelsesoversikt.py`, check 33. El
objeto sigue sin ser el **fundamento** de §2-2(4): es el inventario del que saldrá, y R2 sigue
siendo el paso que lo produce.

## AG. El ensayo de estanqueidad está especificado, y especificarlo giró la fila (2026-11-18)

La ytelsesoversikt llamó a la fila 14.5 la más barata del documento: n50 ≤ 1,5 h⁻¹ a 50 Pa, un
ventilador, una tarde. Es cierto en dinero. **No lo es en tiempo**: no se puede presurizar un
edificio que no existe, así que la tarde no es esta semana sino el final de la fabricación y otra vez
la entrega. La fila sigue `undetermined`, y lo único que cambia es que el trabajo está especificado
en vez de nombrado. **Una especificación es a una medición lo que un cribado a una verificación.**

Escribirla cambió tres cosas que la tabla agregada no podía ver.

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Es difícil el límite? | En caudal absoluto no: **55,4 m³/h** son un extractor de baño. En relativo sí: la envolvente son **66,48 m²** sobre **36,92 m³**, A/V **1,80 m⁻¹** contra ~0,77 de una casa compacta de dos plantas | El mismo 1,5 h⁻¹ exige q50 **0,83 m³/(h·m²)**, **2,3×** más bajo, sobre **61,10 m** de detalle lineal: **0,91 m³/h por metro de junta**. Se alcanza fácil y se falla fácil, y los planos no dicen cuál pasó |
| ¿Más estanco es siempre mejor? | **No.** §14-3 premia la estanqueidad; el extractor necesita que lo alimenten. En cabina sellada la depresión sube al bajar la fuga: 106 Pa a 1,50, **149 Pa a 1,20**, 151 Pa a 1,19 | Por debajo de **1,19 h⁻¹** el extractor básico de 90 m³/h no se puede entregar con un ventilador de 150 Pa. No es un requisito —con la entrada funcionando se sostienen 10 Pa— es el **caso de fallo**, y por eso la entrada va enclavada y no al criterio del ocupante |
| Entonces, ¿cuál es el objetivo? | **1,30 h⁻¹**, y es una banda, no un mínimo | Ni el límite ni «tan estanco como se pueda». Con la entrada cerrada, 1,50 deja la cabina a 106 Pa y 1,20 a 149 Pa, que es el techo del ventilador y la inversión del tiro |
| ¿Aceptar es 1,5? | **No.** La regla de la declaración —un margen es adecuado sólo si es positivo **y mayor que su propia incertidumbre**— aplicada a una medición baja el umbral de aceptación a **1,36** con un ensayo al 10 %, y a 1,43 con uno al 5 % | **La calidad de la medición forma parte de la aceptación**: un ensayo malo puede suspender una cabina construida al objetivo. Se compra un buen ensayo, no una cabina más estanca |
| ¿Y la entrada de aire? | **113 → 116 mm** en toda la banda | Se dimensiona por el extractor de diseño, no por la fuga, así que **se puede pedir antes de medir**. Es el componente que parecía depender del ensayo y no depende |
| ¿Qué más mide? | El exponente de fuga que los cribados suponen, n = 0,65 | Entre 0,50 y 0,80 hay **40 Pa** de diferencia en la cifra titular de ventilación. El ensayo sustituye el supuesto en tres cribados a la vez |
| ¿Y la norma? | **NS-EN ISO 9972:2015**, que sustituyó a NS-EN 13829, **no se tiene** (S031) | No se cita ni un apartado, ni un número de puntos, ni un rango de presión, ni una regla de incertidumbre. Reconstruirlos de memoria es el fallo que las reglas de conocimiento existen para impedir |

**Estado:** `fase1/especificacion-ensayo-tetthet.md`, generado por `scripts/tetthet_test.py`, check 34.
La fila 14.5 **no se cierra**: sigue `undetermined` por dos motivos independientes — el edificio no
existe para medirlo y la norma que define el método no se tiene. Nada de esto es una declaración de
conformidad ni una autorización de fabricación.
