# Verificación de Fase 0 · Contexto

Fecha: 2026-11-16 (Europe/Oslo) · Cliente: DeepSeek Harness (Web GUI, perfil local) · Responsable de la comprobación: agente lead de la sesión, a petición de Carlos.

## Comprobación inicial (mensaje de docs/IDE-SETUP.md)

Ejecutada en modo de lectura antes de crear archivos:

- Cargado automáticamente: `AGENTS.md` (instrucciones de workspace). Posteriormente también `CLAUDE.md` al crearse.
- Abiertos por ruta, en orden: `PROJECT.md`, `rules.md`, `skills.md`, `IDE-SETUP.md` (entonces en la raíz), `AGENTS.md`, `documents/deep-research-report (14).md` (279 líneas) y el PDF original (15 páginas, texto extraído con pypdf).
- Fase activa identificada: Fase 0, última casilla (esta verificación).
- Seis especialistas nombrados: structural-engineer, architectural-modeler, autodesk-steel-detailer, lifting-test-engineer, autodesk-bim-coordinator, frontend-designer.
- Hallazgo: el paquete extraído sólo contenía los 5 Markdown de raíz y `documents/`; faltaban `.agents/`, `.claude/`, `CLAUDE.md`, `docs/`, `references/` y `marketplace.json`. `minihouse-structural-analysis` no podía abrirse.

## Reconstrucción (misma fecha, autorizada por Carlos)

Estructura recreada a partir de los enlaces documentados y del contenido del informe:

| Elemento | Estado |
| --- | --- |
| `.agents/agents/` — 6 definiciones de rol | Creados, con responsabilidad, entradas, entregas y habilidad vinculada |
| `.agents/skills/` — 6 `SKILL.md` canónicos | Creados con frontmatter name/description y procedimiento |
| `references/investigacion-estructural-casita-6x3.md` | Copia del informe original (original conservado en `documents/`) |
| `references/README.md` | Índice con procedencia; entradas croquis (pendiente), Autodesk y WebDesigner |
| `docs/IDE-SETUP.md` | Movido desde la raíz a la ruta que enlazan AGENTS/PROJECT/skills |
| `CLAUDE.md`, `.claude/agents/` (6), `.claude/skills/` (6) | Entradas adaptadoras que apuntan a los canónicos |

## Evidencia de descubrimiento

- DeepSeek Harness añadió las 6 habilidades `minihouse-*` a su catálogo de sesión automáticamente al crearse los `SKILL.md` (mensajes de catálogo observados durante la creación, uno por archivo).
- `CLAUDE.md` fue importado como instrucciones adicionales por el cliente al crearse.
- Comprobación de enlaces: 87 enlaces internos en 34 archivos Markdown, todos resuelven (script de verificación ejecutado el 2026-11-16; búsqueda de destinos de enlace Markdown, excluye http/mailto/anclas).

## Limitaciones y pendientes registrados

- **Croquis originales de Carlos: no presentes** en el paquete recibido; entrada marcada como pendiente en `references/README.md`. No se inventó geometría.
- **marketplace.json / catálogo ZCode**: no recreado; el formato exacto del paquete `minihouse-workspace` no está documentado en el material recibido. Pendiente si se usa ZCode.
- **Verificación en otros IDEs** (Antigravity, Claude Code, Cursor, ZCode, WorkBuddy): pendiente; repetir la comprobación inicial al abrir el proyecto en cada cliente.
- **Prueba Autodesk**: pendiente de acceso a las aplicaciones (Fase 2, primera casilla).
- El contenido de roles y habilidades es una reconstrucción coherente con AGENTS.md, PROJECT.md, rules.md y el informe; no es el texto original del paquete perdido.
- Nota de entorno: los procesos Python hijos no podían escribir en el workspace durante la sesión (PermissionError) mientras PowerShell sí; la extracción del PDF se hizo sólo con lecturas. No afectó a esta verificación.

## Cierre

Criterio de la casilla "Verificar la carga en el primer IDE de trabajo con la comprobación inicial": cumplido para DeepSeek Harness con la evidencia anterior. La repetición en otros clientes queda como parte de la misma casilla cuando se abran (no bloquea el avance a Fase 1).