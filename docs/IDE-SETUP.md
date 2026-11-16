# Abrir MiniHouse en Windows y en cada IDE

Extrae `MiniHouse.zip` en la carpeta de trabajo. Abre **la carpeta interior `MiniHouse`**, donde se encuentra `AGENTS.md`. Si todavía necesitas Antigravity, elige el instalador oficial correspondiente y abre la carpeta como espacio de trabajo. Puedes usar el mismo directorio con los demás IDEs. [Descarga de Antigravity](https://antigravity.google/download) · [Inicio de Antigravity](https://antigravity.google/docs/getting-started)

```powershell
Expand-Archive -LiteralPath .\MiniHouse.zip -DestinationPath .
Set-Location .\MiniHouse
Get-Item .\AGENTS.md, .\PROJECT.md, .\skills.md, .\rules.md
Get-ChildItem -Force -Name
```

`AGENTS.md` usa la capitalización de la convención. En Windows normalmente puedes abrirlo con cualquier capitalización. Mantén el nombre exacto en Git y en sistemas que distinguen mayúsculas. Las habilidades pueden mantenerse en control de versiones junto con el resto del proyecto. [Especificación abierta de AGENTS.md](https://agents.md/)

| Cliente | Activación del contexto | Dónde encontrar los especialistas |
| --- | --- | --- |
| **Antigravity** | Abre `MiniHouse`. Usa `AGENTS.md` y las habilidades de `.agents/skills/`. En la App puedes probar `/minihouse-structural-analysis`. | App y CLI descubren las definiciones de `.agents/agents/`. [Reglas](https://antigravity.google/docs/rules/) · [Habilidades](https://antigravity.google/docs/skills) · [Agentes](https://antigravity.google/docs/subagents?tab=cli) |
| **Claude Code** | `CLAUDE.md` importa los archivos de contexto. `.claude/skills/` ofrece las habilidades con el mismo nombre. | `.claude/agents/` contiene entradas para cada agente. Revisa `/agents` en una sesión del proyecto. [Memoria](https://code.claude.com/docs/en/memory) · [Habilidades](https://code.claude.com/docs/en/skills) · [Agentes](https://code.claude.com/docs/en/sub-agents) |
| **Cursor** | `AGENTS.md` y `.agents/skills/` se descubren desde la raíz del proyecto. | Cursor documenta compatibilidad con los agentes de `.claude/agents/`. [Reglas](https://cursor.com/docs/rules) · [Habilidades](https://cursor.com/docs/skills) · [Agentes](https://cursor.com/docs/subagents) |
| **ZCode** | Inicia una tarea en `MiniHouse` para cargar `AGENTS.md`. Para el selector de habilidades y agentes, abre **Settings → Plugins → Create → Add marketplace**, selecciona la carpeta MiniHouse o su archivo `marketplace.json` e instala `minihouse-workspace` desde el catálogo `minihouse-local`. Sigue el modo de lectura directa si tu versión requiere otro método de importación. | El paquete local incluye las entradas de especialistas. Verifica sus listas en Settings y comienza una sesión nueva para cargar cambios de definiciones. [ZCode Agent](https://zcode.z.ai/en/docs/agents) · [Plugins](https://zcode.z.ai/en/docs/plugin) · [Subagentes](https://zcode.z.ai/en/docs/subagents) |
| **WorkBuddy** | Abre la carpeta y referencia explícitamente `AGENTS.md` y `rules.md` en el primer mensaje. Comprueba `.agents/skills/` en la lista de habilidades de tu edición. | Cuando el cliente no exponga un selector para estas definiciones, referencia el Markdown del rol en `.agents/agents/`. [Habilidades en WorkBuddy](https://developer.cloud.tencent.com/techpedia/2610/20530) |
| **DeepSeek Harness** | Inicia el Harness con `MiniHouse` como directorio y un perfil basado en `dsh-base`. Comprueba `AGENTS.md` y el catálogo de habilidades de `.agents/skills/`. | Usa el archivo del rol como referencia explícita. Si usas el modelo DeepSeek dentro de otro IDE, aplica las rutas de ese IDE. [Instrucciones del proyecto](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/context/agent-instructions) · [Descubrimiento de habilidades](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) |

## Comprobación inicial

Pega este mensaje en cada cliente con la carpeta abierta:

> Lee AGENTS.md, PROJECT.md, rules.md y skills.md desde la raíz de MiniHouse. Indica la fase activa, nombra los seis especialistas y dime si puedes abrir minihouse-structural-analysis. Explica qué archivos cargaste automáticamente y cuáles abriste por su ruta. Haz esta comprobación en modo de lectura.

Si una habilidad no aparece en el selector, abre el `SKILL.md` canónico indicado en [skills.md](../skills.md). Las entradas de Claude y ZCode apuntan al proyecto abierto. Si ZCode instala una copia del paquete en su caché, las referencias operativas se resuelven desde la carpeta `MiniHouse` abierta en el IDE.

## Frontend Design en Claude Code

En una tarea de diseño web, usa `/frontend-design:frontend-design` si está habilitado en Claude. La habilidad local `/minihouse-frontend-design` contiene el brief y la comprobación visual de MiniHouse. Puedes revisar el complemento oficial desde el gestor de plugins de Claude cuando empiece el trabajo web. [Frontend Design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)

## Prueba de Autodesk

Cuando tengas las aplicaciones disponibles, abre un archivo de prueba en las versiones seleccionadas. Comprueba el intercambio de una barra con perfil, material, orientación y unidades entre Robot y Advance Steel, y abre el DWG en la herramienta acordada. Para Forma, verifica primero acceso de lectura al proyecto autorizado y a una revisión conocida. Registra lo que pudo confirmarse antes de elegir una integración de escritura. [Enlace oficial de Robot y Advance Steel](https://marketplace.autodesk.com/apps/792db896-4333-4681-a4dd-e3bf922f6fc6) · [Autodesk APS Data Management](https://aps.autodesk.com/developer/overview/data-management-api)
