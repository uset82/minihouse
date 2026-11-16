# MiniHouse · Referencias

Índice de material de referencia del proyecto. Cada entrada conserva procedencia y condición de aplicación (regla 3 de [rules.md](../rules.md)).

## Investigación estructural

- [investigacion-estructural-casita-6x3.md](investigacion-estructural-casita-6x3.md) — informe de investigación de ingeniería del módulo transportable 6 × 3 m (copia de trabajo del original en `documents/`). Generado con ChatGPT deep research; las citas `citeturn…` son marcadores del generador y las URLs reales están en el PDF original, pp. 13–15.
- Original Markdown: [documents/deep-research-report (14).md](<../documents/deep-research-report (14).md>)
- Original PDF (15 páginas, con lista completa de fuentes): [documents/Informe de investigación…pdf](<../documents/Informe de investigación de ingeniería_ módulo transportable de 6 × 3 m con chasis de acero y madera.pdf>)

Condición de aplicación: el modelo de 3 000 kg, q = 2,4525 kN/m por larguero y EI = 1,68 MN·m² es un **caso numérico hipotético** de viga ideal (flechas 24,63 mm con apoyos en extremos; 1,49 mm retranqueados 1,2 m). No es la masa del módulo ni una posición óptima de apoyos. La masa y el CG reales se determinan por inventario y pesaje (Fase 1–3).

## Croquis y referencias originales

**Incorporadas 2026-11-16.** Carlos aportó dos imágenes conceptuales generadas con ChatGPT como referencia de intención — no son croquis acotados y no deben medirse:

- [`images/MiniHouse_ From Base to Roof-1.png`](../images/MiniHouse_%20From%20Base%20to%20Roof-1.png) — vista explosionada "de la base al techo": chasis metálico tipo escalera, volumen de madera recuperada y tejado a dos aguas separado. Muestra la intención constructiva por capas.
- [`images/MiniHouse cabin on a Norwegian slope-2.png`](../images/MiniHouse%20cabin%20on%20a%20Norwegian%20slope-2.png) — la casita sobre una ladera noruega junto a un fiordo: tablas verticales de madera recuperada, tejado a dos aguas de chapa oscura, hueco grande en fachada larga. Muestra intención de emplazamiento y envolvente.

Condición de aplicación: son referencias visuales, **no** documentación de fabricación ni geometría acotada. La consecuencia registrada es que S-03 (techo) pasa de monopendiente a dos aguas; ver sección F de [`fase1/registro-decisiones.md`](../fase1/registro-decisiones.md). No se extraen cotas de las imágenes.

**Imágenes recibidas 2026-11-16 22:27** (carpeta `images/`, aportadas por otra sesión/agente del proyecto):

- `images/MiniHouse cabin on a Norwegian slope-2.png` (2,3 MB)
- `images/MiniHouse_ From Base to Roof-1.png` (1,9 MB)

Estado: **pendientes de revisión visual y de autorización**. El modelo de esta sesión no puede ver imágenes; no se ha verificado qué muestran, su autoría ni si son renders conceptuales o croquis de Carlos. Hasta revisión humana: no publicar en la web, no derivar cotas de ellas, y tratarlas como visualización conceptual no verificada. Si resultan ser los croquis originales (C-09), mover/copiar a `references/croquis/` con la ficha correspondiente.

## Autodesk

Referencias oficiales citadas por el informe y el plan (verificadas como URLs de documentación; el acceso a productos requiere instalación y licencia propias):

- [Enlace Robot ↔ Advance Steel (Autodesk Marketplace)](https://marketplace.autodesk.com/apps/792db896-4333-4681-a4dd-e3bf922f6fc6)
- [Integration with Robot — RSA Pro User Guide](https://help.autodesk.com/cloudhelp/2026/ENU/RSAPRO-UsersGuide/files/GUID-C284FC96-0577-48D7-AE67-6CB5400333CC.htm)
- [About Advance Steel – Robot Synchronization (SMLX)](https://help.autodesk.com/cloudhelp/2026/ENU/RSAPRO-UsersGuide/files/GUID-46FEC148-5D08-4A75-A9F0-9D462E506E1B.htm)
- [Advance Steel NC Export (DSTV/DXF)](https://help.autodesk.com/cloudhelp/2021/ENU/AdvSteel-Collaboration/files/GUID-4BB649DB-34AA-4CDE-9129-F6785A4E5746.htm)
- [APS Data Management API](https://aps.autodesk.com/data-management-api) · [APS Automation APIs](https://aps.autodesk.com/automation-apis)
- [Robot y la transición a .NET 10 (2026/2027)](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Robot-Structural-Analysis--Requirements-for-products-affected-by-the-Microsoft--NET-10-transition.html)
- [Advancing BIM for Steel Detailing at Autodesk (maintenance mode de Advance Steel)](https://www.autodesk.com/blogs/aec/2023/03/29/advancing-steel-detailing-and-design-at-autodesk/)

Condición: SMLX no conserva todos los ajustes geométricos de Robot; APS Automation no ofrece motores de Robot ni Advance Steel; Data Management requiere OAuth y proyecto autorizado. Ver [minihouse-autodesk-bim](../.agents/skills/minihouse-autodesk-bim/SKILL.md).

## WebDesigner

- [uset82/webdesigner (GitHub)](https://github.com/uset82/webdesigner) — archivos de diseño que sirven de base al enfoque de la futura web documental.

Condición: revisar licencia y procedencia antes de reutilizar assets; el brief y los criterios de MiniHouse están en [minihouse-frontend-design](../.agents/skills/minihouse-frontend-design/SKILL.md). En Claude Code, el plugin oficial [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) es complementario.

## Web interactiva, DeepSeek y OpenRouter (SDK gratuito)

- [deepseek-ai/deepseek-harness (GitHub)](https://github.com/deepseek-ai/deepseek-harness) — framework modular de agentes y plugins (licencia MIT) adaptado en `web/deepseek-harness/` mediante el plugin `@minihouse/dsh-llm-openrouter-free`.
- [deepseek-ai/chat-demo (GitHub)](https://github.com/deepseek-ai/chat-demo) — cliente web de chat en React + TypeScript + Rspack (licencia MIT) adaptado en `web/chat-demo/` para consumir exclusivamente modelos gratuitos de OpenRouter.
- [deepseek-ai/awesome-deepseek-integration (GitHub)](https://github.com/deepseek-ai/awesome-deepseek-integration) — catálogo de integraciones y patrones de referencia del ecosistema DeepSeek.
- [@openrouter/sdk (OpenRouter TypeScript SDK)](https://openrouter.ai/docs) — SDK oficial utilizado para enrutar todas las consultas de la web y del harness hacia el router gratuito `openrouter/free` y variantes `:free` (`pricing.prompt == "0"` y `pricing.completion == "0"`), sustituyendo las llamadas directas a `api.deepseek.com`.

Condición: prohibido activar *fallbacks* hacia modelos de pago; toda respuesta del asistente en la web debe mantener la distinción entre estado **conceptual**, **calculado**, **ensayado** y **liberado para fabricación** según [rules.md](../rules.md).

## Normativa y biblioteca técnica (selección del informe)

TEK17 §10-2 (DIBK) · NS-EN 1990/1991/1993-1-1/-1-8/-1-9/1995 · NS-EN 1090-2:2018+A1:2024 · SN-CEN/TS 1090-201:2024 (acero reutilizado) · EN 13155:2020+A1:2025 (accesorios de izaje) · EN 12195-1 (amarre) · SCI P272 y P385 · JRC *Design of Steel Buildings — Worked Examples* · Jaspart & Weynand · Lawson/Ogden/Goodier · MIT OCW (Roylance). URLs completas en el PDF original, pp. 13–15. Primera generación de Eurocódigos vigente en Noruega; segunda generación prevista 2028.