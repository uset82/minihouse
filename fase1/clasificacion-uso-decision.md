# MiniHouse · Ayuda de decisión de uso y consulta municipal

Estado: **propuesta técnica para cerrar C-01** · 2026-11-16 · No decide la clasificación legal: la decide el municipio. Complemento de [solicitud-datos.md](solicitud-datos.md) y [registro-decisiones.md](registro-decisiones.md).

## 1. Punto clave

**"Casita de emergencia" no es una categoría TEK17.** La misma unidad física puede caer en regímenes distintos según su uso real, duración y lugar:

- vivienda independiente pequeña (*mikrohus* / detached residential building ≤30 m² BRA),
- casa de vacaciones (*fritidsbolig*),
- edificio temporal (*midlertidig bygning* / brakke-modul), u
- otro uso con requisitos más amplios.

La clasificación decide qué capítulos de TEK17 aplican, qué documentación hace falta y si puede tramitarse con el procedimiento simplificado. Ver [S020](../knowledge/sources/S020.md) y [S023](../knowledge/sources/S023.md) para el conjunto del capítulo 13.

## 2. Árbol de decisión

| Paso | Pregunta | Si sí | Si no |
|---|---|---|---|
| 1 | ¿Se usará como vivienda habitual / vivienda de emergencia ocupada de forma continuada? | Ir al paso 2 | Ir al paso 3 |
| 2 | ¿Es una sola vivienda, una planta, sin sótano, ≤30 m² BRA y ≤4,5 m sobre el terreno? | **Ruta A** — mikrohus / vivienda independiente pequeña, TEK17 §1-2(2) | **Ruta D** — requisitos TEK17 completos u otra clasificación municipal |
| 3 | ¿Es uso recreacional / casa de vacaciones con una sola vivienda? | **Ruta B** — fritidsbolig, TEK17 §1-2(2) con rama energética propia | Ir al paso 4 |
| 4 | ¿Es una unidad para una necesidad de duración limitada, tipo brakke/modulo, y no se convertirá en edificio permanente? | **Ruta C** — edificio temporal, TEK17 §1-2(5) | **Ruta D** — consultar municipio; no asumir exención |

**Importante:** la intención de "emergencia" no equivale automáticamente a "temporal". Si se usará de forma permanente, la ruta temporal no debe emplearse para eludir requisitos.

## 3. Consecuencias técnicas de cada ruta

| Ruta | Base | Energía | Responsabilidad / documento |
|---|---|---|---|
| **A · Mikrohus / vivienda independiente ≤30 m²** | TEK17 §1-2(2): capítulos 1–7, 9–11, 14, 15–17; partes listadas de 8, 12, 13 | §14-5(1): sólo §14-1, §14-3 y §14-4(1) aplican. **No aplica el marco §14-2** de 100+1600/A | Régimen SAK simplificado en propiedad edificada, salvo chimenea; se requieren funciones de aseo, dormir, cocina, baño y estar, cumplimiento de seguridad básica y documentación |
| **B · Fritidsbolig una vivienda** | TEK17 §1-2(2), con lista propia de capítulos | §14-5(2): si ≤70 m² de BRA calentada no aplica el capítulo 14; §14-5(3): 70–150 m² aplica §§14-1, 14-3, 14-4(1) | Seguir siendo fritidsbolig en la documentación; no convertir en vivienda sin nueva decisión |
| **C · Edificio temporal / brakke** | TEK17 §1-2(5): capítulos 8, 12, 13 “så langt de passer”; capítulo 14 sólo §14-3 | Orientación §14-5(1) mantiene excepción para unidades reunidas por necesidad de periodo limitado; si pasan a permanentes, energía completa | Confirmar duración y condición temporal por escrito; no elimina seguridad estructural, incendio ni competencia profesional |
| **D · Otro / no clasificado** | TEK17 completo u otro régimen según municipio | No anticipar exenciones | Bloquea Fase 1 hasta respuesta municipal |

Fuentes: [S020](../knowledge/sources/S020.md), [S021](../knowledge/sources/S021.md), [S018](../knowledge/sources/S018.md), [S023](../knowledge/sources/S023.md).

### Corrección importante sobre energía

El cálculo `100 + 1600/A ≈ 188.9 kWh/m²·año` para 18 m² es aritmética válida de §14-2, pero **no es un objetivo de cumplimiento para MiniHouse** en las rutas A, B o C. La ruta A exige todavía §14-3 (U-values y estanqueidad) y §14-4(1) (sin calefacción de combustible fósil). La Ruta B con ≤70 m² no aplica el capítulo 14. La Ruta C sólo aplica §14-3 dentro del capítulo 14.

### Corrección importante sobre ventilación (capítulo 13)

En la **Ruta A (mikrohus)** no se aplica la tabla numérica de §13-2. El conjunto aplicable es §13-1 **párrafo primero**, §13-4, §13-5, §13-7 y §13-9…§13-16; quedan fuera §13-2, §13-3, §13-6 y §13-8 ([S023](../knowledge/sources/S023.md)).

- No usar `1,2 m³/h·m²` ni `21,6 m³/h` para 18 m² como objetivo de MiniHouse mientras la Ruta A siga abierta.
- §13-1(1) exige una ventilación acorde al uso, la contaminación y la humedad, con olor satisfactorio y sin concentraciones nocivas o irritantes. Las cantidades de aire alternativas pueden emplearse, pero **deben documentarse**.
- La Ruta C (edificio temporal) aplica el capítulo 13 “så langt de passer”; confirmar alcance con el municipio. La Ruta D puede hacer volver §13-2 si resulta vivienda ordinaria fuera de §1-2(2).

### Lo que el capítulo 11 no obliga a decidir (incendio)

A diferencia de la energía y de la ventilación, el **capítulo 11 da la misma respuesta para las Rutas A y B**: *bolig* y *fritidsbolig* están ambos en **clase de riesgo 4**, y una planta sin sótano queda en **BKL 1** con **R 15** ([S024](../knowledge/sources/S024.md)).

- La incertidumbre C-01 entre vivienda y fritidsbolig **no bloquea** el diseño de incendio.
- Sólo cambiaría si la casita acabara clasificada como *arbeidsbrakke* o *skur* (clase de riesgo 1, sin clase de incendio asignada). Es poco probable en un edificio con dormir y cocinar, pero es la rama que hay que descartar explícitamente en la consulta municipal.
- Las preguntas de incendio que sí dependen del sitio son la **separación de 8,0 m** a otros edificios (§11-6) y el **acceso de bomberos hasta 50 m** con **1 200 l/min** de agua (§11-17).

## 4. Altura de transporte: aviso previo

La [sensibilidad R1](r1-opciones-techo.md) usa un alero de 3 000 mm como dato de pantalla, no como diseño. Con esa referencia, todas las pendientes evaluadas superan 4,00 m cuando se añade una pila de remolque/apoyos de 900 mm:

| Pendiente | Cumbrera | Pila máxima para 4,00 m |
|---:|---:|---:|
| 5° | 3 131 mm | 869 mm |
| 10° | 3 265 mm | 735 mm |
| 15° | 3 402 mm | 598 mm |
| 20° | 3 546 mm | 454 mm |

El valor 4,00 m procede del resumen oficial de Statens vegvesen sobre la directiva 96/53/CE ([S022](../knowledge/sources/S022.md)). Es un valor de detección temprana, **no un permiso de ruta**. Una pendiente menor, un remolque más bajo, un alero reducido o transporte especial pueden cambiar el resultado.

La [sensibilidad R1](r1-opciones-techo.md) también calcula la envolvente inversa: con pila de 900 mm, el alero máximo sería 2 969 mm a 5° y 2 554 mm a 20°; con pila de 1 100 mm y 20°, sólo 2 354 mm. Ese último caso deja apenas 154 mm sobre la altura libre mínima de 2 200 mm del régimen mikrohus antes de estructura y cubierta. Esto es una advertencia de viabilidad, **no una selección de pendiente ni una cota de diseño**.

## 5. Modelo de consulta al municipio de Bergen

Copiar y adaptar; guardar la respuesta con fecha, número de caso y nombre del interlocutor en C-01.

### Español

> Estimados/as señores/as:
>
> Estamos planificando colocar en Bergen una casita transportable de aproximadamente 6 × 3 m (18 m² BRA), una planta, sin sótano y con una sola vivienda. El uso previsto es [vivienda de emergencia / alojamiento temporal / otro: especificar], con ocupación [continua / ocasional / por periodo limitado de ___ meses].
>
> Agradeceríamos confirmación por escrito sobre:
>
> 1. Cómo clasifica el municipio esta unidad a efectos de plan- og bygningsloven y TEK17 §1-2: vivienda independiente ≤30 m², fritidsbolig, edificio temporal u otra categoría.
> 2. Si puede acogerse a las reglas simplificadas de mikrohus en la parcela prevista [dirección / gnr./bnr.], y si la parcela se considera “bebygd eiendom”.
> 3. Si la clasificación como emergencia implica un uso temporal y, en ese caso, qué duración y documentación se requieren.
> 4. Restricciones de planificación aplicables: ubicación, distancia a linderos, altura, acceso, aparcamiento, agua, alcantarillado, residuos y calidad visual.
> 5. Si se requiere ansvarlig foretak o declaración de responsabilidad para el diseño y la construcción.
> 6. Qué documentación técnica adjuntar para la confirmación.
> 7. Si la unidad se clasifica como mikrohus, qué documentación exige el municipio para acreditar la ventilación funcional de TEK17 §13-1(1) y las cantidades de aire alternativas.
> 8. Confirmación de que la unidad se sitúa en **clase de riesgo 4 / BKL 1** conforme a §11-2 y §11-3, y de que la resistencia portante exigible es **R 15** por §11-4(3) nº 4.
> 9. Si **una sola** ventana de escape conforme a §11-13(4) basta en una unidad de una estancia, o si se exigen dos.
> 10. Distancia mínima exigible a los edificios vecinos según §11-6 y distancia máxima admitida de acceso de bomberos según §11-17 en la parcela prevista.
> 11. Si la parcela está afectada por zonas de peligro del capítulo 7 (inundación, avalancha, desprendimiento, flujo de derrubios, arcilla rápida) y qué clase de seguridad exige el municipio: **F2 = 1/200** y **S2 = 1/1000** son el punto de partida.
> 12. Si la parcela queda **bajo el límite marino** y, por tanto, si se exige investigación geotécnica aunque no haya zona mapeada, y qué *tiltakskategori* se aplica.
> 13. Cota de inundación 1/200 aplicable al sitio y si el municipio exige incluir la subida del nivel del mar en el nivel de stormflo.

### Norwegian draft

> Vi planlegger å plassere en flyttbar modul i Bergen på ca. 6 × 3 m (18 m² BRA), én etasje, uten kjeller, med én boenhet. Tiltenkt bruk er [bolig / beredskapsbolig / midlertidig opphold / annet], med bruk [kontinuerlig / leilighetsvis / tidsbegrenset i ___ måneder].
>
> Vi ber om skriftlig tilbakemelding på:
>
> 1. Hvordan kommunen klassifiserer tiltaket etter plan- og bygningsloven og TEK17 §1-2: frittliggende boligbygning inntil 30 m², fritidsbolig, midlertidig bygning eller annen kategori.
> 2. Om tiltaket kan omfattes av forenklingene for mikrohus på eiendommen [adresse/gnr./bnr.], og om eiendommen anses som bebygd.
> 3. Om beredskapsformålet medfører tidsbegrenset bruk, og hvilken varighet og dokumentasjon som kreves.
> 4. Gjeldende planrestriksjoner for plassering, avstand til nabogrense, høyde, atkomst, parkering, vann, avløp, renovasjon og visuelle kvaliteter.
> 5. Om det kreves ansvarlig foretak for prosjektering og oppføring.
> 6. Hvilken teknisk dokumentasjon som bør vedlegges.
> 7. Dersom enheten klassifiseres som mikrohus, hvilken dokumentasjon kommunen krever for å vise funksjonell ventilasjon etter TEK17 §13-1(1) og eventuelle alternative luftmengder.
> 8. Bekreftelse på at enheten plasseres i **risikoklasse 4 / brannklasse 1** etter §11-2 og §11-3, og at nødvendig bæreevne er **R 15** etter §11-4(3) nr. 4.
> 9. Om **ett** rømningsvindu etter §11-13(4) er tilstrekkelig i en enhet med én oppholdsenhet, eller om det kreves to.
> 10. Minsteavstand til nabobygg etter §11-6 og største tillatte avstand for brannvesenets atkomst etter §11-17 på den aktuelle eiendommen.
> 11. Om eiendommen berøres av faresoner etter kapittel 7 (flom, snøskred, steinsprang, jord- og flomskred, kvikkleire), og hvilken sikkerhetsklasse kommunen krever: **F2 = 1/200** og **S2 = 1/1000** er utgangspunktet.
> 12. Om eiendommen ligger **under marin grense**, og om det dermed kreves geoteknisk undersøkelse selv utenfor kartlagte faresoner, samt hvilken tiltakskategori som gjelder.
> 13. Flomnivå for 1/200 som gjelder for eiendommen, og om kommunen krever at forventet havnivåstigning inngår i stormflonivået.

## 6. Modelo de consulta al transportista / Statens vegvesen

> La unidad terminada tendrá una altura estimada de 3,1–3,5 m sobre la cara superior del chasis, según pendiente. Solicito confirmar:
>
> 1. Altura real de plataforma y apoyos de transporte previstos.
> 2. Altura total cargada resultante y límite aplicable en la ruta Bergen–[destino].
> 3. Si se requiere transporte especial, dispensación o vegliste por altura, además del control de ancho de 3,0–3,1 m.
> 4. Restricciones de puentes, túneles, cables y accesos.
> 5. Posición de apoyos y amarres y masa máxima permitida.

## 7. Evidencia a archivar

- Respuesta municipal con fecha, número de caso y clasificación literal, incluido el alcance del capítulo 13, la documentación de ventilación y la confirmación de clase de riesgo 4 / BKL 1 con R 15.
- Respuesta del transportista con altura de plataforma, altura cargada y permisos.
- Actualización de C-01 y del registro de decisiones.
- Si la respuesta contradice la ruta preliminar, actualizar matriz de cumplimiento y plan antes de seguir.

**Estado:** ayuda de decisión, no resolución administrativa. Ninguna ruta se marca como aplicable hasta recibir la respuesta municipal.
