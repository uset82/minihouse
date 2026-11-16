# Nota de coordinación · trabajo paralelo en la raíz

2026-11-16 23:15, ampliada 23:30 · Rol: autodesk-bim-coordinator (registro).

## Elementos de otras sesiones detectados (no creados por esta sesión)

| Elemento | Timestamps | Contenido | Decisión de esta sesión |
| --- | --- | --- | --- |
| `web/` | 22:37–23:10 | chat-demo + deepseek-harness vendorizados, adaptados a OpenRouter free, node_modules instalados | Intacto. No es la web de Fase 4 (es un cliente de chat LLM). Origen y alcance: preguntar a Carlos |
| `knowledge/` + `docs/knowledge-acquisition-plan.md` | 22:47–22:53 | Base de conocimiento con fuentes S000–S015, derivaciones D001–D003 verificadas, PDFs oficiales (QUB, SCI P272, Straube), matriz de cumplimiento TEK17 | Intacto y **referenciado**: es trabajo válido y complementario (fuentes oficiales que esta sesión no había recuperado). El brief de Fase 4 cita su brief arquitectónico |
| `images/` (2 PNG) | 22:27 | Renders/imágenes de la casita, origen por confirmar | Registradas en references/README.md como pendientes de revisión visual y autorización; no publicadas |
| `.workbuddy-ai/` | 22:36 | Memoria de otro agente ("Inge", WorkBuddy) con los seis roles | Intacto; confirma trabajo multi-agente autorizado por Carlos |
| `scripts/r0_parametric.py` | 22:52 | Geometría paramétrica R0 de la otra sesión (genera knowledge/comparisons/r0-model.json) | Intacto; no duplicado por esta sesión |

## Verificación de enlaces

La comprobación de enlaces del proyecto excluye `web/`, `node_modules/` y `.tmp/`: los ~340 enlaces rotos detectados ahí pertenecen a READMEs de paquetes de terceros. En archivos del proyecto (incluidos knowledge/ y fase4/): todos resuelven.

## Pendiente de Carlos

Confirmar origen y alcance de `web/` (¿forma parte del plan o es experimento aparte?) y autorizar/revisar las imágenes de `images/`.