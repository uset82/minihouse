# Fase 4 · Brief del sitio documental · BORRADOR para aprobación de Carlos

2026-11-16 · Rol: frontend-designer · Estado: **borrador — el encargo NO está aprobado**. La primera casilla de Fase 4 exige que Carlos apruebe audiencia, páginas, contenido y medios. Este documento es la propuesta sobre la que decidir; el prototipo en [sitio/](sitio/) es exploración conceptual, no publicación.

## 1. Propósito

Sitio estático documental que explique MiniHouse (casita transportable 6 × 3 m, acero + madera recuperada), muestre su avance real con trazabilidad y separe con claridad lo conceptual de lo verificado. No es una web comercial ni un configurador.

## 2. Audiencia propuesta

| Audiencia | Necesidad | Prioridad |
| --- | --- | --- |
| Carlos (propietario) | Ver el estado real del proyecto y qué falta | 1 |
| Ingeniero / taller / izaje | Datos con revisión, estado y fuente descargable | 2 |
| Público curioso | Historia, fotos, por qué es difícil mover una casa | 3 |

## 3. Páginas propuestas (mínimo viable)

1. **Inicio** — qué es MiniHouse, estado de fases, aviso permanente de estado conceptual.
2. **Diseño** — geometría R0 con planos SVG, supuestos visibles, aberturas.
3. **Ingeniería** — método de tres niveles, casos de carga, resultados con etiqueta de estado y enlace al archivo fuente; el ejemplo de 3 000 kg jamás como dato del módulo.
4. **Diario** — hitos con fecha y evidencia (Fase 0 cerrada, R0, pruebas de herramientas…).
5. **Materiales** — madera recuperada: fichas de trazabilidad cuando existan.

## 4. Contenido y medios (lista de autorización)

| Medio | Procedencia | Estado de autorización |
| --- | --- | --- |
| Planos SVG R0/R1 (planta, alzados) | Generados en este proyecto, fase1/planos/ | Autoría propia; uso interno seguro; publicar = aprobar encargo |
| images/MiniHouse cabin on a Norwegian slope-2.png | Renders conceptuales ChatGPT aportados por Carlos (S016, 2026-11-16) | **Aportadas por el propietario como referencia de intención**; revisar calidad/pie antes de publicar; no medirlas |
| images/MiniHouse_ From Base to Roof-1.png | Ídem (S016) | Ídem |
| Cifras de la comparativa A–F | Masa EJEMPLO + sección provisional | Publicable sólo etiquetado "demostración de herramienta, no cálculo del módulo" |
| Datos TEK17/normativa | knowledge/ (fuentes oficiales citadas) | Publicable con cita y fecha de consulta |

## 5. Sistema visual (tokens del prototipo)

Acero + madera recuperada, sobrio, legible:

| Token | Valor | Uso |
| --- | --- | --- |
| --tinta | #2b2620 | texto principal (sobre papel: contraste **medido** 13.92:1) |
| --papel | #faf6ef | fondo |
| --acero | #4a5560 | encabezados técnicos, bordes (7.06:1) |
| --madera | #8a5a33 | acentos cálidos / enlaces (5.43:1) |
| --alerta | #8c2f1b | etiquetas CONCEPTUAL (7.68:1; blanco sobre alerta 8.28:1) |
| --exito | #2c6e49 | estados verificados (5.68:1; blanco sobre éxito 6.12:1) |
| Tipografía | system-ui / Georgia para narrativa | sin fuentes externas (rendimiento, privacidad) |
| Espaciado | escala 4/8/16/24/40 px | consistente |
| Ancho máx. | 72ch texto, 1100px página | legibilidad |

Etiquetas de estado obligatorias en toda cifra: `CONCEPTUAL` / `CALCULADO` / `ENSAYADO` / `LIBERADO`, con enlace a la fuente y revisión.

## 6. Implementación

Prototipo actual: **HTML+CSS estático sin dependencias** (fase4/sitio/), fiel a los tokens. La propuesta Astro+TS del plan se decide al aprobar el encargo: para 5 páginas documentales, HTML plano puede ser el alcance final (menos mantenimiento, cero build). Migrar a Astro sólo si el diario crece o se quieren componentes.

## 7. Criterios de revisión (checklist de publicación)

- [ ] Encargo aprobado por Carlos (audiencia, páginas, contenido, medios)
- [ ] Cada imagen con autorización y pie (qué, cuándo, revisión)
- [x] Cada cifra con estado + fuente + revisión (verificado por scripts/check_web.py y revisión de contenido, 2026-11-16)
- [x] Contraste AA **medido** en los 15 pares usados: mínimo 5.43:1 (scripts/check_web.py, 2026-11-16)
- [x] Navegación por teclado estructural: skip-link, foco visible 3:1+, aria-current, landmarks (check automatizado); revisión manual de teclado pendiente de humano
- [ ] Revisión visual a 360px y ≥1280px con capturas archivadas — **pendiente**: el modelo de esta sesión no puede ver imágenes; CSS responsive escrito (breakpoint 480px, clamp tipográfico) pero sin verificación visual
- [x] Sin peticiones externas en carga: 0 (verificado); sitio completo 32,5 KB sin JS
- [ ] Destino de publicación acordado

## 8. Decisiones que Carlos debe tomar

1. ¿Aprueba audiencia/páginas/medios de §2–4? ¿Qué falta o sobra?
2. Las dos imágenes ya están identificadas (S016: renders ChatGPT aportados por Carlos). ¿Autoriza publicarlas con pie "imagen conceptual, no acotada"?
3. ¿HTML estático simple o Astro?
4. ¿Dónde se publica (dominio, hosting)? ¿Idioma(s): español, noruego, inglés?
5. Nuevo (2026-11-16, sección F del registro): ¿la "casita de emergencia" es vivienda habitual, alojamiento temporal o unidad de emergencia? Decide la clase TEK17.