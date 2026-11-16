# MiniHouse · Habilidades del proyecto

Las habilidades editables están en `.agents/skills/<nombre>/SKILL.md`. Cada carpeta declara su nombre y una descripción de cuándo aplicarla. Claude Code carga entradas en `.claude/skills/` que apuntan a esta misma documentación. Consulta [la guía de IDEs](docs/IDE-SETUP.md) para la activación por cliente.

| Habilidad | Cuándo cargarla | Resultado |
| --- | --- | --- |
| [minihouse-structural-analysis](.agents/skills/minihouse-structural-analysis/SKILL.md) | Dimensionar o comparar base, esquinas, apoyos, torsión o flecha | Casos de carga, cálculo reproducible, modelo de Robot y comprobación independiente |
| [minihouse-architectural-modeling](.agents/skills/minihouse-architectural-modeling/SKILL.md) | Modelar volumen, distribuciones, madera, aberturas o interferencias | Modelo paramétrico, cotas y fichas de masa e interfaces |
| [minihouse-autodesk-steel-detailing](.agents/skills/minihouse-autodesk-steel-detailing/SKILL.md) | Intercambiar perfiles en SMLX o producir planos y archivos de taller | Modelo de detalle, DWG/PDF, lista de materiales y salida de máquina acordada |
| [minihouse-lifting-validation](.agents/skills/minihouse-lifting-validation/SKILL.md) | Comparar enganches, planificar traslado o preparar y revisar ensayos | Comprobaciones de rigging, transporte y protocolo con registros de medición |
| [minihouse-autodesk-bim](.agents/skills/minihouse-autodesk-bim/SKILL.md) | Coordinar ACS/Forma, modelos, revisiones e integración con APS | Inventario de versiones, mapeo y evidencia de intercambio |
| [minihouse-frontend-design](.agents/skills/minihouse-frontend-design/SKILL.md) | Diseñar una web o revisar UI, contenido visual, accesibilidad y rendimiento | Dirección visual, jerarquía y criterios para la futura implementación |

Para la web, `/frontend-design:frontend-design` es una opción cuando está instalado el plugin oficial en Claude Code. La habilidad de MiniHouse contiene el flujo específico del proyecto y se puede abrir desde cualquier cliente. Su enfoque se basa en los archivos de diseño de [uset82/webdesigner](references/README.md#webdesigner).

El formato se basa en la especificación de Agent Skills y en la documentación de Codex. [Agent Skills](https://agentskills.io/home) · [Especificación](https://agentskills.io/specification) · [Repositorio](https://github.com/agentskills/agentskills) · [Habilidades de Codex](https://developers.openai.com/codex/skills)
