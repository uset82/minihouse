# Despliegue web · minihouse.canner.app

2026-11-17 00:16, **actualizado 00:35** · Rol: frontend-designer + integrador (sesión lead DSH).

## Estado actual (2026-11-17 00:35)

Carlos aclaró que el sitio principal debía ser el **chat-demo + simulador 3D de Antigravity** (walkthrough de su sesión), no el sitio documental. Acción tomada:

1. **Hallazgos W-1…W-4 corregidos en el código fuente** (ediciones mínimas de trazabilidad, con autorización implícita del encargo de Carlos):
   - W-1: hero pill y badge del Concept 2 pasan de `[CALCULADO · 3t REF]` a `[CONCEPTUAL · HYPOTHETICAL EXAMPLE, NOT MODULE]`; la descripción aclara que 24,63/1,49 mm son del caso hipotético del informe.
   - W-2: BOM MH-STR-001 → "2 × 6000 mm beams + **6 crossmembers @1200** (steel grade TBD)", malla canónica R0; estado CONCEPTUAL.
   - W-3: madera → "batch documentation pending (C-08)"; pesaje "to be weighed (pending)".
   - W-4: alturas 3200/450 mm → "TBD with gable roof (R1)" / "build-up thickness TBD"; columnas y padeyes "to be designed per EN 13155 (pending)".
   - Los `CALCULADO` restantes en el bundle son legítimos: textos i18n que explican el sistema de estados y la lógica de renderizado de badges.
2. **Verificado**: 8/8 tests vitest, tsc 0 errores, rspack build OK; los 4 arreglos confirmados en el bundle `main.5ec9da95.js` y **en vivo**.
3. **https://minihouse.canner.app** sirve ahora el chat-demo (Documentary + 3D Lab + AI chat, 3 vistas). Bundle y las 3 imágenes concepts responden 200.
4. **El sitio documental se preservó** en un segundo proyecto: **https://minihouse-docs.canner.app** (mismas 4 páginas, verificado 200).
5. Nota de entorno: el Node del runtime DSH no puede escribir archivos (EPERM, igual que Python); el build se hizo con el **Node del sistema** (v22.22.0, C:\Program Files\nodejs). `build.mjs` falla al borrar dist con el Node del runtime; usar `node node_modules\@rspack\cli\bin\rspack.js build -c rspack.config.ts` con NODE_ENV=production y el Node del sistema.

## Proyectos Canner

| Slug | URL | Contenido | Fuente |
| --- | --- | --- | --- |
| minihouse | https://minihouse.canner.app | chat-demo + 3D lab (Antigravity, con fixes de auditoría) | upload CLI desde web/chat-demo/dist |
| minihouse-docs | https://minihouse-docs.canner.app | sitio documental 4 páginas (fase4/sitio) | upload CLI desde fase4/sitio |

Ambos con `framework_override=static` (PATCH por slug en la API; por id devuelve not_found). El proyecto minihouse sigue conectado al repo GitHub en sus settings, pero **el contenido live viene del upload CLI**; no usar `canner redeploy` ni "Retry" de commits viejos (reconstruiría el monorepo).

## Comandos

```powershell
# chat-demo: rebuild (Node del SISTEMA, no el del runtime DSH)
cd web\chat-demo; $env:NODE_ENV='production'
node node_modules\@rspack\cli\bin\rspack.js build -c rspack.config.ts
cd dist; canner deploy --slug=minihouse --follow
# sitio documental
cd fase4\sitio; canner deploy --slug=minihouse-docs --follow
```

## Pendientes

- Aprobación formal del encargo web (brief §8) y autorización de las imágenes concepts/*.jpg para publicación — Carlos las vio en el walkthrough de Antigravity; confirmar.
- Revisión visual humana del chat-demo en móvil/escritorio (el modelo auditor no ve imágenes).
- El chat-demo requiere API key de OpenRouter del usuario para el chat (se introduce en Settings, no se almacena en el repo).
- Rollback: Canner conserva el bundle anterior (12c43666, el sitio documental) como target del proyecto minihouse.