# MiniHouse · Guía de agentes

MiniHouse es una casita transportable de aproximadamente **6 × 3 m** con estructura de acero y madera recuperada. Abre esta carpeta como raíz del proyecto. Lee [PROJECT.md](PROJECT.md) para el alcance y la fase activa, [rules.md](rules.md) para la forma de trabajar y [skills.md](skills.md) para elegir el procedimiento. Usa [la guía de IDEs](docs/IDE-SETUP.md) para confirmar qué carga tu cliente.

## Especialistas

| Agente | Responsabilidad | Entrega al siguiente rol |
| --- | --- | --- |
| [structural-engineer](.agents/agents/structural-engineer.md) | Cálculo estructural, base, esquinas, apoyos, estabilidad y deformación en Robot | Hipótesis, carga por caso, reacciones y fuerzas en las uniones |
| [architectural-modeler](.agents/agents/architectural-modeler.md) | Implantación del volumen, modelado 3D, huecos, envolvente y madera recuperada | Geometría acotada, inventario de masas y colisiones |
| [autodesk-steel-detailer](.agents/agents/autodesk-steel-detailer.md) | Detallado 3D en Advance Steel, DWG y planos en AutoCAD | Detalles de perfiles y uniones, lista de materiales y archivos de fabricación de la revisión correspondiente |
| [lifting-test-engineer](.agents/agents/lifting-test-engineer.md) | Izaje superior e inferior, transporte y validación física | Requisitos del aparejo y del transporte, plan de ensayo instrumentado y criterios de aceptación |
| [autodesk-bim-coordinator](.agents/agents/autodesk-bim-coordinator.md) | Intercambio entre aplicaciones y control de revisiones en Autodesk Forma | Registro de archivos, versiones, interfaces y pruebas de transferencia |
| [frontend-designer](.agents/agents/frontend-designer.md) | Identidad visual y diseño de la futura web con referencias de WebDesigner | Brief, sistema visual, contenido y criterios de revisión en móvil y escritorio |

El agente principal toma una tarea acotada, elige el rol por su entrega y conserva los hallazgos en el proyecto. En un cliente sin un selector de agentes, lee el archivo del rol y sigue el mismo flujo. Las funciones son independientes de la marca del modelo.

## Secuencia

1. Localiza la primera fase pendiente que corresponda al encargo en [PROJECT.md](PROJECT.md).
2. Lee la definición del rol y la habilidad correspondiente. Entrega al siguiente rol los archivos, la revisión, los datos faltantes y las verificaciones ejecutadas.
3. Marca cada casilla cuando se cumpla su criterio y haya evidencia. Trabaja en orden. Cuando un dato falte, registra el supuesto o la dependencia y continúa las tareas de la fase que puedas verificar.
4. Para esta entrega, cierra la inicialización del contexto. Los cálculos del módulo real, el CAD de la casita, los ensayos y el sitio tienen sus propias fases en el plan.
