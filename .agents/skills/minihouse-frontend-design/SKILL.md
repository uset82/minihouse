---
name: minihouse-frontend-design
description: Diseñar la web documental de MiniHouse o revisar UI, contenido visual, accesibilidad y rendimiento. Produce dirección visual, jerarquía y criterios para la futura implementación.
---

# minihouse-frontend-design

Habilidad del rol [frontend-designer](../../agents/frontend-designer.md). Cargar antes de diseñar o revisar la interfaz. La web es Fase 4: primero se aprueba el encargo (audiencia, páginas, contenido y medios).

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