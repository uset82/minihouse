# Matriz de acciones y combinaciones · plantilla R0

2026-11-16 · Rol: structural-engineer · Estado: **plantilla conceptual**. Archivo de datos: [matriz-acciones.csv](matriz-acciones.csv). Ningún coeficiente está fijado salvo constantes físicas; los valores del Anexo Nacional noruego están bloqueados por acceso de pago (S014 de knowledge/).

## Cómo se usa

1. Cada fila del CSV es una acción sobre un caso (U-1…I-3 de la [hoja de condiciones](../fase1/condiciones-transporte-izaje.md)). La columna `estado_valor` distingue: FIJADO (físico), PENDIENTE_NA (anexo nacional), PENDIENTE_DATO (respuesta de Carlos), PENDIENTE_MEDICION (ensayo E-5), PENDIENTE_INGENIERO (criterio del responsable), PENDIENTE_IZAJE (empresa de maniobra).
2. Cuando llegue un valor, se rellena `valor_na` **con su fuente y condición de aplicación** (tabla del NA, edición, emplazamiento) — nunca un número de memoria o de otro país (el NA del Reino Unido no vale: C002 de knowledge/).
3. Las combinaciones (filas COMB) se cierran sólo cuando todas las acciones del caso tienen valor o cota justificada.
4. Esta matriz es la entrada del "Load takeoff" del stage-gate del informe; alimenta el modelo de Fase 2 y el protocolo de ensayos.

## Actualizaciones incorporadas respecto a la hoja de condiciones

- **Techo a dos aguas** (intención S016): el coeficiente de forma de nieve μ1 cambia respecto al monopendiente; queda pendiente de la pendiente acotada.
- **Bergen costero**: viento y lluvia batiente refuerzan U-1 viento y el detalle de envolvente; el valor básico de viento sigue pendiente del emplazamiento exacto.
- **Clase de uso**: "casita de emergencia" sin clase legal → carga de uso Q_k sin tabla aplicable todavía.

## Lo que esta plantilla NO hace

No calcula combinaciones numéricas, no elige γ/ψ, no sustituye al ingeniero responsable. Es el andamiaje para que el día que lleguen NA + datos, el takeoff sea mecánico y auditable.