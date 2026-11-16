# MiniHouse

Casita modular de unos **6 m de largo por 3 m de ancho**, construida con estructura de acero y madera recuperada. La idea es mover el módulo entero en camión, colocarlo con grúa y volver a apoyarlo sin deformar de forma permanente el chasis, las esquinas o los marcos de puertas y ventanas.

## Qué hay que resolver

La base, los nudos de esquina y los apoyos cambian de función cuando la casita está instalada, suspendida o sobre un remolque. Hay que calcular la resistencia de las uniones, la flexión y torsión del conjunto y la estabilidad de la maniobra. La comparación inicial incluye izaje por nudos altos e izaje desde la base.

| Quién lo usa | Qué necesita |
| --- | --- |
| Propietario y equipo de diseño | Explorar distribución, materiales recuperados, coste y facilidad de traslado |
| Ingeniero estructural y equipo de grúa | Definir masas, centro de gravedad, cargas, apoyos y aparejo. Revisar resultados y ensayos |
| Modelador y taller | Compartir geometría, uniones, tolerancias, planos y revisiones verificables |
| Diseñador web | Explicar el proyecto y su avance con contenido, fotos y visualizaciones trazables |

## Base de diseño

| Dato | Estado inicial |
| --- | --- |
| Planta | Aproximadamente 6 × 3 m exteriores. Confirmar salientes, ancho de transporte y ruta antes de fijar cotas |
| Altura y techo | Por definir. Registrar altura total sobre la plataforma y distancia libre para aparejos |
| Acero y madera | Acero en chasis y estructura primaria. Madera recuperada en la envolvente o en otros usos según sus propiedades documentadas |
| Masa de traslado | Por determinar con un inventario y pesaje. Registrar accesorios, baño, equipos y estado de depósitos |
| Izaje | Comparar nudos superiores e inferiores con las mismas masas y restricciones. La cantidad y posición de enganches se deciden con el análisis |
| Apoyos | Registrar suelo, nivelación, anclajes y posiciones reales sobre el camión. Distinguir apoyo, punto de amarre y punto de izaje |
| Entorno | Windows es la plataforma prevista para Autodesk y los IDEs. Noruega es el marco de referencia inicial. Confirmar lugar de instalación, uso, ruta y requisitos aplicables |
| Web | Alcance provisional de sitio documental, con presentación del proyecto, materiales y avance. El alcance final se decide al aprobar el encargo web |

El informe de referencia reúne precedentes, fuentes, fórmulas y un cálculo reproducible de una viga ideal. Las imágenes originales registran la intención inicial de Carlos. [Investigación estructural](references/investigacion-estructural-casita-6x3.md) · [Croquis y referencias](references/README.md)

## Herramientas y entregables previstos

| Función | Herramienta de partida | Qué se intercambia |
| --- | --- | --- |
| Estructura y comprobación independiente | Robot Structural Analysis Professional y Python con NumPy o PyNite cuando aporten verificación | Hipótesis, curvas, reacciones, fuerzas de nudo y revisión del solver |
| Modelado arquitectónico | Autodesk Revit si está disponible. AutoCAD para planta, elevaciones y coordinación de geometría | Cotas, huecos, acabados, interferencias y relación de masas |
| Detallado estructural y taller | Autodesk Advance Steel y AutoCAD. Probar el enlace Robot–Advance Steel si las versiones coinciden | SMLX si el enlace lo soporta, DWG/PDF, lista de materiales y NC/DSTV o DXF según el taller |
| Coordinación y control documental | Archivos locales al inicio. Autodesk Forma Data Management, antes Autodesk Docs, cuando exista un proyecto autorizado | Versiones, responsables, estado, trazabilidad y formatos de intercambio acordados |
| Automatización futura | Python para verificaciones y C#/.NET o AutoLISP para tareas CAD según SDK y versión confirmados | Elegir interfaces después del intercambio manual en un archivo de prueba |
| Web futura | Sitio documental y asistente interactivo basado en `deepseek-ai/chat-demo` y `deepseek-ai/deepseek-harness` modificados para usar `@openrouter/sdk` (API gratuita de OpenRouter: `openrouter/free` y modelos `:free`), con diseño guiado por WebDesigner | Contenido y medios autorizados, asistente técnico con trazabilidad de estados, diseño responsivo y revisión de accesibilidad |

Mantén por componente su identificador, revisión, material, masa, posición y procedencia. Vincula cada caso de carga con la revisión analizada y cada medición con el caso y la configuración ensayada. La web puede usar los datos autorizados del proyecto con su estado y revisión. [Referencias de Autodesk](references/README.md#autodesk)

## Puesta en marcha

1. Extrae la carpeta y abre `MiniHouse` como raíz en el IDE.
2. Completa la verificación del cliente y de sus detectores de agentes y habilidades. La conexión con Autodesk se verifica con un archivo de prueba cuando haya acceso a las aplicaciones correspondientes.
3. Selecciona la primera tarea aplicable de la fase activa y el especialista que entrega la evidencia requerida. [Guía para Windows y los IDEs](docs/IDE-SETUP.md)

## Plan secuencial

Marca cada casilla al cumplir su criterio de cierre. El desglose operativo del borrador de ChatGPT, con sus tareas de uso, planta, masas, izaje, taller y primer traslado, está reconciliado con esta numeración en [plan detallado de diseño y construcción](docs/plan-diseno-construccion.md); no cambia las fases oficiales.

### Fase 0 · Contexto

- [x] Crear la guía de agentes, el índice de habilidades y las reglas en la raíz.
- [x] Definir las seis funciones, las habilidades y las entradas de IDE con sus rutas documentadas.
- [x] Adjuntar el informe estructural y los croquis originales, y fijar los enlaces a WebDesigner.
- [x] Verificar estructura de archivos, metadatos y referencias internas del paquete.
- [x] Verificar la carga en el primer IDE de trabajo con la comprobación inicial. Repetir al abrir MiniHouse en otro cliente. (DeepSeek Harness, 2026-11-16: [registro](docs/verificacion-fase-0.md); estructura `.agents/`, `references/` y `docs/` reconstruida y enlaces verificados; croquis originales y prueba en otros clientes pendientes.)

### Fase 1 · Datos y viabilidad

- [ ] Confirmar destino, uso, dimensiones exteriores, ruta, limitaciones de la grúa, frecuencia de traslado y tipo de apoyo. (Parcialmente respondido 2026-11-16: mercado Bergen, uso casita de emergencia —clase legal por precisar—, intención de techo a dos aguas registrada en [sección F](fase1/registro-decisiones.md) y propagada a planos R1. Siguen abiertas: cotas definitivas, ruta, grúa, apoyos, remolque, equipos, madera. Hallazgo verificado: ancho ≈3 m viaja como carga indivisible ≤3,25 m según veggruppe.)
- [ ] Hacer la planta y elevaciones de referencia. Registrar aberturas, equipos y cada masa con su ubicación y procedencia. (Avance R0 conceptual 2026-11-16: [geometría y planos](fase1/geometria-R0.md), [aberturas](fase1/tabla-aberturas.csv), plantillas de masas y [calculadora probada](scripts/masas_cg.py). Falta: datos reales de equipos y masas — no marcar hasta inventario con procedencia real.)
- [ ] Definir las condiciones de transporte, montaje y uso con el ingeniero estructural y el proveedor de izaje. (Estructura de casos U/T/I y fórmulas preparadas: [hoja de condiciones](fase1/condiciones-transporte-izaje.md). Falta: validación con ingeniero y proveedor — no marcar.)

### Fase 2 · Cálculo y modelo

- [ ] Comprobar el intercambio de un archivo de prueba en la versión instalada de Autodesk. Registrar el resultado. (Verificado 2026-11-16: Robot/Advance Steel/AutoCAD/Revit NO instalados; sólo Desktop Connector y FreeCAD 1.1.3. Prueba alternativa ejecutada: IFC R0 generado y reimportado con IfcOpenShell, 13 miembros verificados — [fase2/README.md](fase2/README.md). El enlace SMLX sigue pendiente de instalación.)
- [ ] Calcular peso, centro de gravedad, reacciones, flechas, torsión y reparto de fuerzas. Verificar con un cálculo independiente. (Herramientas listas y probadas 2026-11-16: [masas_cg.py](scripts/masas_cg.py) y [barras3d.py](scripts/barras3d.py) —selftest OK, reproduce los casos del informe. Verificación cruzada entre sesiones completada: [reconciliacion-R0.md](docs/reconciliacion-R0.md) — derivaciones simbólicas y solver FEM independientes coinciden; geometría R0 unificada. Falta: masas y geometría reales C-01…C-09.)
- [ ] Modelar las alternativas de izaje por arriba y por la base. Comparar nudo de esquina, larguero, travesaño y deformación de las aberturas. (Demostración conceptual A–F ejecutada 2026-11-16 con masa EJEMPLO y sección provisional, regenerada sobre malla canónica @1200: [chasis_r0.py](scripts/chasis_r0.py), [resultados](fase2/comparativa-izaje-R0-resultados.csv). Matriz de acciones preparada: [matriz-acciones.csv](fase2/matriz-acciones.csv) — 16 acciones, coeficientes NA bloqueados por acceso. No es el cálculo del módulo; faltan datos reales y uniones.)
- [ ] Revisar casos de suelo, transporte e izaje con el ingeniero responsable. Elegir la variante que pasa al prototipo.

### Fase 3 · Prototipo, ensayos y taller

- [ ] Detallar la unión piloto y preparar los planos de prototipo con la revisión acordada.
- [ ] Definir instrumentación, cargas de ensayo, criterios de parada y aceptación con los responsables del ensayo. (Borrador R0 con estructura a priori: [fase3/protocolo-ensayos-R0.md](fase3/protocolo-ensayos-R0.md). Valores de aceptación pendientes del ingeniero responsable.)
- [ ] Ejecutar y documentar las pruebas acordadas de la unión, chasis, izaje y transporte. Comparar mediciones con el modelo.
- [ ] Incorporar los resultados y emitir los archivos de taller revisados según la liberación del ingeniero responsable.

### Fase 4 · Web

- [ ] Aprobar audiencia, páginas, contenido y medios utilizables. (Propuesta completa para decisión de Carlos: [fase4/brief-web.md](fase4/brief-web.md) §8. Imágenes de `images/` registradas como NO autorizadas hasta revisión visual humana.)
- [ ] Usar la habilidad de frontend para diseñar y revisar la interfaz en pantallas estrechas y anchas. (Prototipo estático de 4 páginas con tokens documentados: [fase4/sitio/](fase4/sitio/index.html). Revisión automatizada OK: contraste medido 15 pares, skip-link, alt, 0 peticiones externas, 32,5 KB — [check_web.py](scripts/check_web.py). Revisión VISUAL estrecho/ancho pendiente: requiere humano o modelo con visión.)
- [ ] Verificar navegación, contraste, accesibilidad y rendimiento antes de publicar en el destino acordado. (Checks automatizados pasan 2026-11-16; faltan teclado manual, capturas visuales y destino de publicación — checklist en el brief §7.)

## Verificación y riesgos

| Punto de control | Evidencia de aceptación |
| --- | --- |
| Intercambio CAD | Abrir el archivo transferido y contrastar unidades, puntos de control, ejes, perfiles, huecos y revisión |
| Desplazamientos, torsión y estabilidad | Comparar cálculos simples, resultados del solver y mediciones dentro de los límites fijados por el responsable |
| Desgaste y durabilidad | Especificar drenaje, protección anticorrosiva e inspección de uniones. Documentar trazabilidad de las piezas estructurales recuperadas |
| Producción y coordinación | Revisar números de pieza, tolerancias, soldaduras, secuencia de fabricación y revisión de dibujo coincidente con la lista de materiales |
| Uso por varios IDEs | Confirmar descubrimiento y acceso a las rutas. Registrar versión, adaptador y cualquier dependencia pendiente |

Estado a 2026-11-16: Fase 0 cerrada; Fases 1–4 avanzadas hasta su frontera humana (datos de Carlos, licencias Autodesk, NA de pago, ingeniero responsable y empresa de izaje). Mapa puerta por puerta: [docs/estado-del-plan.md](docs/estado-del-plan.md). Suite de verificación completa: `python scripts/verificar_todo.py` (8 comprobaciones, todas pasan). El plano, el modelo real y las pruebas físicas se desarrollan a partir de los datos pendientes.
