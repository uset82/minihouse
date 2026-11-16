# MiniHouse · Reglas de trabajo

## Fases y evidencia

1. Trabaja sobre el encargo activo y su criterio de cierre en [PROJECT.md](PROJECT.md). Marca las casillas conforme se cumplan. Registra cada resultado con fecha, archivos, revisión, método y limitaciones.
2. Mantén identificados los datos medidos, los datos de fabricante y los supuestos. Usa milímetros para los dibujos de taller y un sistema de unidades explícito y consistente en cada ecuación y modelo. Declara ejes, origen, unidades, signos y versión del software.
3. Todo valor de referencia necesita procedencia y condición de aplicación. El ejemplo de 3.000 kg del informe es un caso numérico hipotético. Usa la masa y el centro de gravedad verificados para resolver el izaje real.
4. Antes de emitir una recomendación estructural, documenta el recorrido de las cargas, las reacciones, la rigidez y los modos de falla. Revisa instalación, izaje y transporte como casos independientes. Contrasta el modelo con cálculos simples y después con mediciones del prototipo.
5. Distingue estado **conceptual**, **calculado**, **ensayado** y **liberado para fabricación**. La liberación de los planos y la ejecución de maniobras reales requieren el criterio del ingeniero estructural responsable y, para el izaje, la planificación de la empresa competente. Usa los requisitos de aplicación confirmados para el emplazamiento y la ruta.

## Archivos e integración

- Conserva los originales y utiliza una revisión identificable para cada cambio en geometría, masas, apoyos o uniones. Usa identificadores estables entre arquitectura, cálculo, taller y ensayos. Mantén la correspondencia entre el modelo nativo, el archivo de intercambio y las salidas.
- Antes de una transferencia Autodesk, confirma el producto, la versión, la extensión de archivo, el permiso de acceso y el alcance de la herramienta disponible. Registra qué prueba se ejecutó y qué datos sobrevivieron. Cuando falte acceso, prepara la secuencia manual y deja la conexión como pendiente de verificar.
- Mantén credenciales y datos privados en el entorno o gestor autorizado. Para las referencias de GitHub, conserva la procedencia y revisa licencias, dependencias y efectos de un instalador antes de usarlo. Conserva el alcance de cada cuenta, carpeta y servicio.
- Coordina el trabajo de los IDEs sobre archivos distintos cuando corran a la vez. Antes de retomar un archivo, lee el plan, la revisión y el último traspaso para evitar sobrescribir cambios.
- Para la futura web, usa contenido y medios autorizados. Identifica las visualizaciones conceptuales y conserva la trazabilidad de las medidas publicadas. Aplica revisión visual en móvil y escritorio, navegación por teclado y contraste adecuado.

`rules.md` contiene instrucciones de proyecto. En Codex, las reglas de ejecución de comandos usan archivos `.rules` en los niveles de configuración habilitados. Este proyecto delega los permisos al cliente y a su configuración vigente. [OpenAI Codex Rules](https://developers.openai.com/codex/rules) · [Guía de AGENTS.md](https://developers.openai.com/codex/guides/agents-md) · [Repositorio de AGENTS.md](https://github.com/agentsmd/agents.md)
