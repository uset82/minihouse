# Estado del plan · puerta por puerta

2026-11-16 23:35 · Generado por la sesión lead (DSH). Verificación completa: `python scripts/verificar_todo.py` → **TODO PASA** (8 comprobaciones, exit 0). Este documento es el mapa honesto de qué está hecho, qué falta y quién lo desbloquea. No marca casillas de PROJECT.md: eso exige cumplir el criterio completo.

## Fase 0 · Contexto — CERRADA ✅

| Criterio | Evidencia |
| --- | --- |
| Guía, habilidades, reglas, roles, IDE | Estructura reconstruida y verificada: [verificacion-fase-0.md](verificacion-fase-0.md) |
| Carga en primer IDE | DSH: 6 habilidades descubiertas en vivo; 87→199 enlaces verificados |
| Repetir en otro cliente | Pendiente menor: Claude Code instalado sin login; Cursor/Antigravity disponibles |

## Fase 1 · Datos y viabilidad — EN FRONTERA HUMANA

| Casilla | Hecho | Falta (dueño) |
| --- | --- | --- |
| Confirmar destino/uso/cotas/ruta/grúa/apoyo | Bergen + casita de emergencia + intención dos aguas ([registro §F](../fase1/registro-decisiones.md)); ancho ≤3,25 m verificado con fuentes | Clase legal de uso, emplazamiento exacto, C-02…C-06 (**Carlos**) |
| Planta/elevaciones + masas con procedencia | R0 completo + [alzado R1 dos aguas](../fase1/planos/alzado-trans-R1.svg); plantillas + calculadora probada | Inventario real con masas medidas/fabricante (**Carlos** C-07/C-08); pendiente de techo acotada (**Carlos** + ingeniero) |
| Condiciones transporte/montaje/uso | [Hoja de casos U/T/I](../fase1/condiciones-transporte-izaje.md) + [matriz de 16 acciones](../fase2/matriz-acciones.csv) | Validación con ingeniero y proveedor de izaje (**profesionales**) |

## Fase 2 · Cálculo y modelo — HERRAMIENTAS LISTAS, CÁLCULO REAL BLOQUEADO

| Casilla | Hecho | Falta (dueño) |
| --- | --- | --- |
| Intercambio Autodesk de prueba | Autodesk NO instalado (verificado); sustituto IFC ejecutado: [12 miembros round-trip OK](../fase2/registro-intercambio.md) | Robot + Advance Steel (**licencia/Carlos**) |
| Cálculo + verificación independiente | [barras3d.py](../scripts/barras3d.py) reproduce el informe; [D001 simbólico](../knowledge/derivations/D001.md) coincide — doble método cruzado entre sesiones | Masas reales, NA noruego (**compra**), geometría congelada |
| Alternativas izaje arriba/abajo | [A–F en malla canónica @1200](../fase2/comparativa-izaje-R0-resultados.csv), equilibrio verificado; candidato inset 20% P272 registrado | Modelo real con uniones, H de eslingas, dinámica |
| Revisión con ingeniero responsable | — | **Ingeniero responsable** (p. ej. candidatos Bergen del informe) |

## Fase 3 · Prototipo y ensayos — PROTOCOLO A PRIORI LISTO

| Casilla | Hecho | Falta |
| --- | --- | --- |
| Unión piloto + planos | — | Fase 2 real completa |
| Instrumentación/criterios | [Protocolo E-1…E-5](../fase3/protocolo-ensayos-R0.md) con estructura de aceptación previa | Valores de aceptación (**ingeniero**), empresa de ensayo (**contratación**) |
| Ejecutar pruebas | — | Prototipo físico + taller + izaje competente |
| Archivos de taller liberados | — | Liberación del RIB (rules.md §5) |

## Fase 4 · Web — PROTOTIPO LISTO, ENCARGO SIN APROBAR

| Casilla | Hecho | Falta |
| --- | --- | --- |
| Aprobar audiencia/páginas/medios | [Brief completo](../fase4/brief-web.md) con 5 decisiones para Carlos | **Carlos** |
| Diseñar/revisar estrecho y ancho | [Sitio 4 páginas](../fase4/sitio/index.html), tokens, R1 incorporado; checks medidos pasan | Revisión visual humana (modelo sin visión) |
| Verificar antes de publicar | Contraste 15 pares medido, teclado estructural, 0 externas, ~37 KB | Teclado manual, capturas, destino de publicación (**Carlos**) |

## Bloqueos transversales (orden de impacto)

1. **C-02…C-08 de Carlos** → desbloquea geometría R1 congelada, inventario real y todo el cálculo.
2. **Clase legal de "casita de emergencia"** → TEK17 uso, nieve/viento, energía.
3. **NA noruego + NS 3031** (de pago, S014) → coeficientes γ/ψ y verificación de código.
4. **Robot/Advance Steel** → gate SMLX y detallado.
5. **Ingeniero responsable + empresa de izaje** → límites, aceptación, lift plan, liberación.
6. **Aprobación web** → publicación.

## Trabajo paralelo coordinado

Sesión WorkBuddy ("Inge"): knowledge/ (19 fuentes, 3 derivaciones, 4 PDFs primarios), r0_parametric.py, respuestas parciales de Carlos registradas. Verificación cruzada mutua completada: [reconciliacion-R0.md](reconciliacion-R0.md). `r0-model.json` sigue siendo el histórico monopendiente R0; la intención a dos aguas se explora sin selección en [r1-opciones-techo.md](../fase1/r1-opciones-techo.md) y en [r1-gable-options.json](../knowledge/comparisons/r1-gable-options.json). Para cerrar los datos pendientes hay una [solicitud priorizada](../fase1/solicitud-datos.md). `web/` (cliente chat OpenRouter) fuera del plan hasta decisión de Carlos: [nota-coordinacion-web.md](nota-coordinacion-web.md).