# Geometría de referencia R0 · CONCEPTUAL — NOT FOR FABRICATION

Revisión R0 · 2026-11-16 · Rol: architectural-modeler. Geometría de trabajo construida sobre los supuestos S-01…S-08 del [registro de decisiones](registro-decisiones.md). **No es un diseño aprobado**: existe para acotar el volumen, colocar masas y aberturas y dar al cálculo un marco de coordenadas único. Cambia en cuanto Carlos responda C-01…C-09.

## Sistema de referencia (obligatorio para todo modelo)

- Unidades: **mm** en planos y tablas de geometría; **m, kg, N** en el inventario de masas y la calculadora.
- Origen: esquina exterior del chasis, cara superior del larguero de piso, en (x=0, y=0, z=0).
- Ejes: +x longitudinal (6 000 mm hacia el extremo del baño→estar según S-04, aquí baño en x∈[0; 1 200]); +y transversal (3 000 mm); +z vertical hacia arriba.
- Cotas exteriores R0: L = 6 000, B = 3 000, H total sobre chasis = 3 200 (S-01). Altura libre interior 2 400 (S-02). ~~Techo monopendiente con cumbrera +200 mm sobre el borde bajo (≈3,8°, S-03), cumbrera en y=0. Pared: 3 000 mm en el borde bajo.~~ **S-03 SUPERSEDIDO el 2026-11-16 por intención de Carlos** (sección F del [registro](registro-decisiones.md), fuente S016): **tejado a dos aguas** de chapa metálica oscura, cumbrera centrada; pendiente, aleros y altura de cumbrera **sin acotar** (no se miden los renders). S-01 (H=3200) queda pendiente de revisión con la nueva forma de techo.
- Salientes de envolvente ≤ 50 mm/lado (S-06) → ancho de transporte ≤ 3 100 mm.
- Chasis conceptual: 2 largueros longitudinales en y ≈ 150 y y ≈ 2 850 (ejes de perfil), travesaños cada ≈ 1 200 mm (4 intermedios en x=1200/2400/3600/4800 + 2 de extremo = 6). **Sección sin definir**: no se dibuja ningún perfil porque EI del informe no identifica sección (falta A, W, I, J, espesores, grado). Los ejes de chasis son líneas de referencia, no perfiles elegidos.
- Nota de discretización (2026-11-16, reconciliación entre sesiones): la malla de 1 m con 7 travesaños usada en [scripts/chasis_r0.py](../scripts/chasis_r0.py) y [fase2/chasis-R0.ifc](../fase2/chasis-R0.ifc) es una **discretización de demostración**, no la geometría de referencia; la referencia canónica es la de 6 travesaños @1200 de este documento y de [knowledge/comparisons/r0-model.json](../knowledge/comparisons/r0-model.json). Ver [docs/reconciliacion-R0.md](../docs/reconciliacion-R0.md).
- Puntos de izaje candidatos: 4 esquinas altas (nudos de pórtico en x=0/6 000, y=0/3 000, z≈3 000) y 4 bajos (esquinas de chasis, z≈0). Posiciones **candidatas** para comparar variantes; la decisión sale del análisis (Fase 2).

## Aberturas R0

Ver [tabla-aberturas.csv](tabla-aberturas.csv). P-01 puerta en fachada larga y=3 000; V-01…V-03 ventanas. Todas marcadas como gobernantes de deformación (cambio de diagonal) hasta que el cálculo fije límites.

## Planos conceptuales

Escala gráfica, cotas en mm, sin perfiles ni espesores constructivos:

- [Planta R0](planos/planta-R0.svg) — volumen, ejes de chasis, travesaños, aberturas, zona de baño, candidatos de izaje.
- [Alzado longitudinal R0](planos/alzado-long-R0.svg) — fachada y=3 000, alturas S-01/S-02. **Nota**: la línea de cumbrera proyectada corresponde al techo monopendiente superado; con dos aguas la fachada larga muestra el alero (altura pendiente de acotar). Aberturas y longitud siguen válidas.
- [Alzado transversal R1-intención](planos/alzado-trans-R1.svg) — **vigente para la forma de techo** (dos aguas, sin acotar). El [alzado-trans-R0](planos/alzado-trans-R0.svg) monopendiente se conserva como histórico superado.

## Qué NO contiene R0

Secciones de acero, espesores de placa, soldaduras, orejas de izaje, anclajes, detalles de madera, instalaciones. Todo eso entra en Fase 2–3 con datos y cálculo. Cualquier uso de R0 para fabricar viola rules.md §5.

## Traspaso

A structural-engineer: este marco de ejes/unidades, tabla de aberturas, plantilla de masas y la propuesta S-07 (sin paredes colaborantes inicialmente). A lifting-test-engineer: candidatos de izaje y ancho de transporte (hallazgo D del registro). A autodesk-bim-coordinator: R0 como primera revisión registrada; nativo CAD/IFC pendiente de las herramientas (Fase 2).