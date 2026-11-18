---
name: minihouse-frontend-design
description: Diseñar, construir o revisar la web de MiniHouse, tanto la web promocional (fase4/promo, web/promo) como el sitio documental. Cubre dirección visual, UI, textos, imágenes, accesibilidad y rendimiento con el método y los tokens de fase4/promo/DESIGN-GUIDE.md.
---

# minihouse-frontend-design

Habilidad del rol [frontend-designer](../../agents/frontend-designer.md). Cárgala antes de diseñar o revisar la interfaz. La web es la Fase 4: primero se aprueba el encargo (audiencia, páginas, contenido y medios).

## Web promocional (desde 2026-11-17): obligatorio

La web principal es ahora promocional. Antes de diseñar, programar, escribir textos o generar imágenes para ella:

1. Lee completa la [guía de diseño](../../../fase4/promo/DESIGN-GUIDE.md). Recoge el método de trabajo (adaptado de la habilidad `frontend-design` de Claude Code), los tokens exactos, los componentes, la lista de patrones prohibidos y la definición de terminado.
   - El resumen en formato DESIGN.md (el estilo «/design») está en [web/promo/DESIGN.md](../../../web/promo/DESIGN.md).
   - `/frontend-design:frontend-design` sólo existe en Claude Code. Fuera de él (Grok, DeepSeek), lee directamente el archivo de la habilidad que indica la guía.
2. Lee el [plan](../../../fase4/promo/PLAN.md) y el [reparto entre agentes](../../../fase4/promo/agents/README.md). Están en `fase4/promo/agents/`:
   - el brief de tu cliente (Antigravity, Cursor o DeepSeek);
   - si te unes para una sola tarea (Grok, WorkBuddy), su archivo `task-*.md`.
3. En cada sección: planifica los tokens y la maquetación, y compáralos con la lista de patrones prohibidos (§10 de la guía). Construye sólo con tokens y revisa capturas a 360 y 1280 px. Quita un adorno antes de darla por terminada.
4. Edita sólo los archivos que te asigna tu brief y registra cada tarea en `fase4/promo/status/<agente>.md`.

El procedimiento siguiente sigue vigente para el sitio documental (`fase4/sitio/`).

## Procedimiento

1. **Brief.** Audiencia (propietario, equipo técnico, público curioso), propósito (documentar el proyecto y su avance), páginas propuestas y medios autorizados. Sin aprobación del encargo, sólo exploración conceptual.
2. **Referencias.** Archivos de diseño de uset82/webdesigner: entradas y procedencia en [references/README.md](../../../references/README.md#webdesigner). Revisar licencia antes de reutilizar assets. En Claude Code, `/frontend-design:frontend-design` como complemento si está instalado.
3. **Sistema visual.** Tokens documentados (color, tipografía, espaciado, radios, sombras); identidad coherente con acero + madera recuperada; jerarquía que separe narrativa, datos técnicos y galería.
4. **Contenido trazable.** Cada foto o render con autorización y pie (qué es, cuándo, revisión). Visualizaciones conceptuales etiquetadas como tales. Medidas publicadas con estado (conceptual / calculado / ensayado / liberado) y enlace a su fuente; nunca presentar cifras hipotéticas como aprobadas.
5. **Implementación de partida.** Astro + TypeScript + CSS, sitio estático documental; decidir alcance final al aprobar el encargo. Sin dependencias innecesarias.
6. **Revisión obligatoria.** Móvil (≈360 px) y escritorio (≥1280 px); navegación completa por teclado; contraste WCAG AA; foco visible; texto alternativo; rendimiento (imágenes optimizadas, sin bloqueos de render). Registrar capturas y resultados por pantalla.
7. **Entrega.** Brief aprobado, tokens, maquetas/prototipo, lista de contenido con procedencia y checklist de accesibilidad/rendimiento cumplida antes de publicar en el destino acordado.

## Verificación de cierre

Ningún medio sin autorización; ninguna cifra sin estado y fuente; revisión visual y de teclado hecha en estrecho y ancho; contraste medido, no estimado.