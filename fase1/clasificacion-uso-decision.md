# MiniHouse · Ayuda de decisión de uso y consulta municipal

Estado: **propuesta técnica para cerrar C-01** · 2026-11-16 · No decide la clasificación legal: la decide el municipio. Complemento de [solicitud-datos.md](solicitud-datos.md) y [registro-decisiones.md](registro-decisiones.md).

## 1. Punto clave

**"Casita de emergencia" no es una categoría TEK17.** La misma unidad física puede caer en regímenes distintos según su uso real, duración y lugar:

- vivienda independiente pequeña (*mikrohus* / detached residential building ≤30 m² BRA),
- casa de vacaciones (*fritidsbolig*),
- edificio temporal (*midlertidig bygning* / brakke-modul), u
- otro uso con requisitos más amplios.

La clasificación decide qué capítulos de TEK17 aplican, qué documentación hace falta y si puede tramitarse con el procedimiento simplificado. Ver [S020](../knowledge/sources/S020.md).

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

Fuentes: [S020](../knowledge/sources/S020.md), [S021](../knowledge/sources/S021.md), [S018](../knowledge/sources/S018.md).

### Corrección importante sobre energía

El cálculo `100 + 1600/A ≈ 188.9 kWh/m²·año` para 18 m² es aritmética válida de §14-2, pero **no es un objetivo de cumplimiento para MiniHouse** en las rutas A, B o C. La ruta A exige todavía §14-3 (U-values y estanqueidad) y §14-4(1) (sin calefacción de combustible fósil). La Ruta B con ≤70 m² no aplica el capítulo 14. La Ruta C sólo aplica §14-3 dentro del capítulo 14.

## 4. Altura de transporte: aviso previo

La [sensibilidad R1](r1-opciones-techo.md) usa un alero de 3 000 mm como dato de pantalla, no como diseño. Con esa referencia, todas las pendientes evaluadas superan 4,00 m cuando se añade una pila de remolque/apoyos de 900 mm:

| Pendiente | Cumbrera | Pila máxima para 4,00 m |
|---:|---:|---:|
| 5° | 3 131 mm | 869 mm |
| 10° | 3 265 mm | 735 mm |
| 15° | 3 402 mm | 598 mm |
| 20° | 3 546 mm | 454 mm |

El valor 4,00 m procede del resumen oficial de Statens vegvesen sobre la directiva 96/53/CE ([S022](../knowledge/sources/S022.md)). Es un valor de detección temprana, **no un permiso de ruta**. Una pendiente menor, un remolque más bajo, un alero reducido o transporte especial pueden cambiar el resultado.

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

## 6. Modelo de consulta al transportista / Statens vegvesen

> La unidad terminada tendrá una altura estimada de 3,1–3,5 m sobre la cara superior del chasis, según pendiente. Solicito confirmar:
>
> 1. Altura real de plataforma y apoyos de transporte previstos.
> 2. Altura total cargada resultante y límite aplicable en la ruta Bergen–[destino].
> 3. Si se requiere transporte especial, dispensación o vegliste por altura, además del control de ancho de 3,0–3,1 m.
> 4. Restricciones de puentes, túneles, cables y accesos.
> 5. Posición de apoyos y amarres y masa máxima permitida.

## 7. Evidencia a archivar

- Respuesta municipal con fecha, número de caso y clasificación literal.
- Respuesta del transportista con altura de plataforma, altura cargada y permisos.
- Actualización de C-01 y del registro de decisiones.
- Si la respuesta contradice la ruta preliminar, actualizar matriz de cumplimiento y plan antes de seguir.

**Estado:** ayuda de decisión, no resolución administrativa. Ninguna ruta se marca como aplicable hasta recibir la respuesta municipal.
