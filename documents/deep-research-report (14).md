# Informe de investigación de ingeniería: módulo transportable de 6 × 3 m con chasis de acero y madera recuperada

## Conclusión técnica y criterio de diseño

La idea es viable, pero no debe avanzar desde “un dibujo que parece estructuralmente razonable” hacia fabricación directa. El objeto debe tratarse simultáneamente como **edificio**, **estructura transportada**, **carga amarrada**, **estructura temporalmente suspendida** y, si se diseña un balancín o accesorio específico, como un sistema de izaje con requisitos propios. En Noruega, TEK17 exige que la estructura tenga resistencia, rigidez y estabilidad suficientes tanto durante ejecución como en su estado final; la vía normal de verificación es NS‑EN 1990 junto con las series NS‑EN 1991–1999 y sus anexos nacionales noruegos. citeturn168234search0turn305957search2

El informe base del proyecto ya identifica correctamente los problemas fundamentales: centro de gravedad, reparto de fuerzas entre eslingas, flexión longitudinal, torsión del chasis, detalle local de orejas y soldaduras, FEM global, vibraciones de transporte y ensayos del prototipo. También contiene un modelo ilustrativo de 3 000 kg, dos largueros de 6 m, \(q=2.4525\ \mathrm{kN/m}\) por larguero y \(EI=1.68\ \mathrm{MN\,m^2}\), con flechas de 24,63 mm y 1,49 mm para apoyos en extremos y apoyos retranqueados 1,2 m respectivamente. Esos resultados son matemáticamente reproducibles, pero no constituyen una aprobación estructural del módulo. fileciteturn0file0

El precedente académico más útil que encontré es el trabajo de Queen’s University Belfast y McAvoy Group sobre un módulo volumétrico de acero ligero. El equipo estudió posiciones de izaje, estabilidad, deformación global y fallos locales, fabricó diferentes soportes y ensayó los nudos a tracción hasta rotura antes de levantar los módulos reales. El prototipo utilizaba seis puntos de elevación y módulos de aproximadamente 9 m de longitud; por metodología, es mucho más relevante para este proyecto que una colección de dibujos de tiny houses sin cálculo. citeturn984735search0turn384745view0turn577476view1

La recomendación central es, por tanto, una arquitectura de verificación de tres niveles: **cálculo manual reproducible → modelo FEM independiente → ensayo físico representativo**. Ningún modelo Autodesk debe ser considerado “verdadero” simplemente porque converge; el modelo debe ser contrastado contra equilibrio, soluciones cerradas de vigas, segundo solver independiente y datos físicos. Esta filosofía coincide con investigaciones de módulos de acero a escala real donde los modelos numéricos se calibran frente a propiedades dinámicas medidas experimentalmente. citeturn984735search2

## Auditoría crítica del informe base

La ecuación de centro de gravedad utilizada en el informe es correcta:

\[
\mathbf r_G=
\frac{\sum_i m_i\mathbf r_i}{\sum_i m_i},
\qquad
W=g\sum_i m_i
\]

y también lo son, para un cuerpo en equilibrio estático idealizado entre dos estaciones de reacción, las relaciones:

\[
R_B=W\frac{x_G-x_A}{x_B-x_A},
\qquad
R_A=W-R_B
\]

La limitación importante es que **cuatro apoyos o cuatro ramales no implican automáticamente \(W/4\)**. Con cuatro reacciones verticales desconocidas, el equilibrio rígido aporta sólo tres ecuaciones independientes —fuerza vertical y dos momentos—, por lo que el reparto individual depende de rigidez estructural, geometría del aparejo, tolerancias de longitud, pretensiones y contacto. El informe menciona correctamente este problema, pero debe convertirse en una condición explícita de diseño y ensayo. fileciteturn0file0

La comprobación independiente del modelo de viga confirma los números del informe. Para \(L=6\,\mathrm m\), \(q=2452.5\,\mathrm{N/m}\), \(EI=1.68\times10^6\,\mathrm{N\,m^2}\) y apoyos simétricos a distancia \(a\) desde los extremos:

\[
M_A=-\frac{qa^2}{2}
\]

\[
M_{L/2}=
\frac{qL(L-4a)}8
\]

y, para esta configuración simétrica específica,

\[
\delta_{L/2}
=
\frac{q}{EI}
\left[
\frac{5(L-2a)^4}{384}
-
\frac{a^2(L-2a)^2}{16}
\right].
\]

Con \(a=0\), resultan \(M_{mid}=11.036\ \mathrm{kN\,m}\) y \(\delta_{mid}=24.634\ \mathrm{mm}\); con \(a=1.2\,\mathrm m\), \(M_A=-1.766\ \mathrm{kN\,m}\), \(M_{mid}=2.207\ \mathrm{kN\,m}\) y \(\delta_{mid}=1.490\ \mathrm{mm}\). El orden de magnitud y las unidades del informe son correctos. La teoría utilizada es Euler–Bernoulli, que relaciona curvatura y momento mediante \(EI\,v''(x)=M(x)\); MIT publica material didáctico de referencia sobre este procedimiento. citeturn671035search2turn671035search37

Sin embargo, este resultado puede inducir a una conclusión demasiado optimista. El descenso de 24,6 a 1,49 mm demuestra que **la posición de los apoyos modifica radicalmente la flexión de un larguero ideal**, no que “1,2 m sea la posición óptima” de una casa real. El modelo omite al menos: torsión del bastidor rectangular; travesaños; flexibilidad de las uniones; deformación local del tubo junto a las orejas; cargas puntuales de baño, cocina, depósitos y baterías; interacción con paredes; grandes aberturas; rigidez del piso; asimetría de masas; deformación del remolque y acción de las eslingas fuera del plano. El SCI específicamente advierte que los módulos deben diseñarse para las fuerzas adicionales de transporte, elevación e instalación, no sólo para las acciones en servicio. citeturn671035search48

Además, \(EI=1.68\ \mathrm{MN\,m^2}\) no identifica por sí solo un perfil. Si se adopta provisionalmente \(E=210\ \mathrm{GPa}\), implica aproximadamente:

\[
I=\frac{EI}{E}
=\frac{1.68\times10^6}{210\times10^9}
\approx8.0\times10^{-6}\,\mathrm{m^4}
\]

pero faltan \(A\), \(W_{el}\), \(W_{pl}\), \(I_y\), \(I_z\), constante torsional \(J\), constante de alabeo cuando corresponda, espesores y clase de sección. Sin ellos no se puede verificar tensión, resistencia plástica, pandeo, torsión ni deformación local. Eurocode 3 distingue explícitamente las verificaciones de resistencia de sección, estabilidad de miembros y uniones. citeturn675713search0turn955640search0

Hay además una corrección documental importante en el precedente McAvoy. Su artículo afirma que el bracket fue diseñado con orientación de **EN 1993‑1‑2:2005**. Esa referencia corresponde a *Structural fire design*, no al diseño normal de uniones. EN 1993‑1‑8 es la parte de Eurocode 3 dedicada a *Design of joints*. Por tanto, no copiaría EN 1993‑1‑2 como norma de dimensionamiento de una oreja de izaje; parece, como mínimo, una referencia inapropiada o un error bibliográfico del paper y debe verificarse con el ingeniero responsable. citeturn384745view0turn675713search0turn675713search6

Para las eslingas, la expresión del informe también es correcta si \(\alpha\) se mide desde la horizontal:

\[
T=\frac{V}{\sin\alpha},
\qquad
H=V\cot\alpha.
\]

Usando el ejemplo de 3 000 kg sólo como chequeo geométrico, si las cuatro esquinas compartieran perfectamente el peso estático, \(V=29.43/4=7.3575\ \mathrm{kN}\). A \(60^\circ\), cada ramal tendría \(T\approx8.50\ \mathrm{kN}\) y una componente horizontal de \(4.25\ \mathrm{kN}\); a \(30^\circ\), \(T\approx14.72\ \mathrm{kN}\) y \(H\approx12.74\ \mathrm{kN}\). Esto muestra por qué los ángulos bajos castigan tanto al chasis. Estos números **no incluyen dinámica ni reparto desigual** y no deben utilizarse para seleccionar WLL de eslingas o grúa. Las operaciones reales deben ser planificadas y ejecutadas con la resistencia y estabilidad requeridas por la normativa de trabajo noruega. citeturn168234search4

## Proyectos comparables y evidencia experimental

La siguiente matriz prioriza proyectos donde existe algo más que una imagen comercial.

| Referencia | Evidencia disponible | Relevancia para 6 × 3 m | Limitación |
|---|---|---|---|
| **McAvoy / Queen’s University Belfast** | Módulos LGS de aprox. 9 m; seis puntos de izaje; varios brackets; excentricidad del eye; ensayos de nudos a tracción hasta fallo; módulo finalmente levantado. citeturn984735search0turn577476view1 | Excelente metodología para diseñar y romper probetas de oreja + perfil + tornillos/soldadura antes del prototipo completo. | Geometría y sistema LGS diferentes; no copiar capacidades. |
| **Ensayo de transporte de módulo de acero, Engineering Structures 2026** | Módulo y remolque instrumentados, acelerómetros, medición de deformación cortante de muros y techo y tres recorridos de ~25 km; inspección posterior de daños. citeturn984735search1 | Modelo directo para un “road test” de tu módulo terminado y para correlacionar vibración con grietas/deformaciones de acabados. | Los espectros y aceleraciones son específicos del vehículo, carretera y módulo ensayados. |
| **Acceleration responses of building modules during road transportation** | Aceleraciones triaxiales de módulos transportados; influencia de vehículo, velocidad y rugosidad; análisis estadístico y PSD. citeturn984735search3 | Útil para construir casos dinámicos de transporte y decidir instrumentación. | No sustituye el recorrido real ni EN 12195 para amarre. |
| **Western Sydney University — módulo volumétrico full scale** | Ensayo dinámico de módulo de acero a tamaño real; acelerómetros; frecuencias naturales, modos y damping; modelos FEM macro y micro comparados con experimento. citeturn984735search2 | Excelente plantilla para validar rigidez global y FEM con ensayo modal simple. | No fue un estudio específico de orejas de izaje. |
| **ACLD 2024 — conexión modular usada también para levantar** | Dispositivo de conexión/izaje ensayado a escala real; evaluación funcional y estructural. El artículo concluye que el concepto puede levantar, aunque el dispositivo concreto no justificó su complejidad. citeturn984735search4 | Demuestra que el punto de izaje debe considerarse parte del diseño de sistema y no una placa añadida al final. | Sistema en estructura ligera de madera y conexión distinta. |
| **CONTAINEX CLASSIC Line XL** | Módulos comerciales de 6 055 × 2 989 mm documentados, prácticamente iguales en huella al objetivo 6 × 3 m. citeturn984735search6 | Precedente dimensional extremadamente cercano para logística, envolvente y manipulación. | La geometría comercial no revela necesariamente todos los cálculos internos ni autoriza copiar conexiones. |

El artículo de Belfast es especialmente útil visualmente: estudia explícitamente levantamiento desde elementos bajos frente a puntos altos, y muestra cómo la fuerza del eye puede quedar excéntrica respecto al centroide del montante. Los brackets experimentales estaban conectados a perfiles delgados con tornillos y el módulo consideró 17,5 kN verticales por punto. Esa cifra pertenece a su módulo y no debe importarse al tuyo; lo transferible es el método: identificar la trayectoria de carga completa, fabricar el detalle y ensayarlo hasta conocer su modo de fallo. citeturn384745view0turn577476view1

El trabajo de carretera de 2026 es probablemente el proyecto más cercano a tu requisito de “physics testing”: instrumentó simultáneamente remolque, módulo y deformación de elementos de cerramiento, y encontró relación entre daño no estructural y amplitud/repetición de deformaciones cortantes. Para una casita con madera recuperada, ventanas y acabados, esto importa tanto como la resistencia última del acero porque una estructura que “no colapsa” puede seguir siendo inaceptable si abre juntas, bloquea puertas o rompe impermeabilización. citeturn984735search1

## Mecánica, normas y verificaciones que deben gobernar el diseño

Para Noruega, TEK17 §10‑2 reconoce NS‑EN 1990 y las series Eurocode como vía de cumplimiento. Standard Norge confirma que, a 12 de noviembre de 2026, la primera generación de Eurocódigos y sus anexos nacionales sigue siendo la normativa aplicable en Noruega hasta la publicación conjunta de la segunda generación en 2028. Los preestándares de segunda generación no sustituyen aún a las normas vigentes. citeturn168234search0turn305957search0

La jerarquía normativa que usaría para un proyecto noruego sería: NS‑EN 1990 para base de diseño y combinaciones; NS‑EN 1991 para acciones; NS‑EN 1993‑1‑1 para miembros de acero; NS‑EN 1993‑1‑8 para uniones; NS‑EN 1993‑1‑9 si los ciclos de transporte/izaje justifican comprobación de fatiga; NS‑EN 1995 para cualquier elemento de madera que realmente sea portante; y NS‑EN 1090‑2 para ejecución del acero. NS‑EN 1090‑2:2018+A1:2024 es la versión consolidada que Standard Norge identifica actualmente para requisitos técnicos de ejecución de estructuras de acero. citeturn168234search2turn675713search6turn675713search12

Para el acero recuperado, existe además SN‑CEN/TS 1090‑201:2024 sobre reutilización de componentes de acero estructural. En tu concepto actual, usar madera recuperada como revestimiento o acabado desmontable es mucho más sencillo que asignarle una función estructural sin trazabilidad. Si alguna madera recuperada va a transmitir cargas, su especie, humedad, defectos, grado resistente y conexiones necesitan documentación específica en lugar de una propiedad “genérica de madera”. citeturn168234search3turn675713search12

Para combinaciones de acciones, una forma básica de ULS de EN 1990 es:

\[
E_d =
E\left\{
\sum \gamma_{G,j}G_{k,j}
+
\gamma_{Q,1}Q_{k,1}
+
\sum_{i>1}\gamma_{Q,i}\psi_{0,i}Q_{k,i}
\right\}.
\]

Los coeficientes concretos no deben fijarse hasta definir la situación de proyecto y el anexo nacional. EN 1990 distingue situaciones persistentes, transitorias, accidentales y sísmicas; el izaje y ciertas etapas de montaje deben tratarse explícitamente como estados temporales en lugar de quedar escondidos dentro del caso permanente del edificio. citeturn955640search11turn955640search12

Para una sección sometida a flexión simple, el chequeo conceptual de una sección de clase apropiada toma la forma:

\[
M_{Ed}\le M_{Rd}
\]

con una resistencia que, según clase y caso, se construye a partir de \(W\,f_y/\gamma_M\). Para compresión global, la forma Eurocode es:

\[
N_{Ed}\le N_{b,Rd}
=
\chi\,A f_y/\gamma_{M1},
\]

donde \(\chi\) depende de la esbeltez reducida y de la curva de pandeo. El proyecto debe comprobar además interacción \(N\)–\(M\), pandeo lateral o torsional cuando proceda, clasificación de sección y efectos de segundo orden. El JRC publica ejemplos completos de estas verificaciones según Eurocode 3. citeturn955640search0turn675713search20

La deformación no puede limitarse a “\(L/xxx\)” sin relacionarla con función. Aquí hay al menos cuatro límites distintos: flecha del piso, cambio de diagonal de huecos, torsión diferencial entre las cuatro esquinas y deformación local alrededor del punto de izaje. La tolerancia que probablemente controle puede ser la compatibilidad de puertas, cristales, membranas y madera, no la tensión del acero. El estudio de carretera de 2026 muestra precisamente que las deformaciones cortantes repetidas de paredes y techos se relacionan con daño no estructural. citeturn984735search1

La torsión debe incluirse deliberadamente. Para un miembro ideal en Saint‑Venant:

\[
\frac{d\phi}{dx}
=
\frac{T}{GJ}
\]

pero perfiles abiertos pueden desarrollar alabeo significativo, por lo que una barra 6‑DOF convencional puede no capturar todos los efectos. SCI P385 está dedicado al diseño de vigas de acero bajo torsión y distingue los mecanismos relevantes. citeturn671035search47

Para la oreja de izaje no basta con comprobar \(A f_y\). El submodelo debe cubrir, según su geometría: tracción neta, sección bruta, aplastamiento alrededor del agujero, desgarro o block tearing, flexión de placa, excentricidad, deformación de pared del RHS/SHS, rigidizadores, soldaduras y camino de carga hacia travesaños y largueros. Para una carga excéntrica:

\[
M_e = F e.
\]

Así, sólo \(10\ \mathrm{kN}\) a 200 mm genera \(2.0\ \mathrm{kN\,m}\) adicional en el detalle. EN 1993‑1‑8 y las guías del JRC sobre uniones, pernos y soldaduras son recursos apropiados para esa etapa. citeturn955640search2turn955640search9

Para soldaduras de filete, el cálculo Eurocode se formula sobre tensiones en la garganta efectiva y resistencia de cálculo del cordón; para un grupo de soldaduras sometido a carga excéntrica hay que distribuir fuerza directa y momento sobre la geometría real del grupo. No reduciría una oreja a la fórmula simplificada \(F/(aL)\) salvo como screening inicial. EN 1993‑1‑8 es la referencia para la comprobación final de uniones soldadas. citeturn675713search6turn955640search2

Un spreader beam o lifting beam fabricado específicamente para la operación puede entrar en el ámbito de EN 13155. La edición vigente de BSI es EN 13155:2020+A1:2025 y cubre, entre otros, lifting beams, así como resistencia estática, estabilidad elástica y fatiga; no cubre las eslingas propiamente dichas. Esto es importante porque “el módulo” y “el accesorio de izaje” pueden tener obligaciones distintas. citeturn988918search0turn988918search6

Para transporte por carretera, EN 12195‑1 aborda el cálculo de fuerzas de aseguramiento mediante bloqueo, amarre o combinaciones y distingue cargas estables de cargas susceptibles de vuelco. El proyecto debe usar los coeficientes y condiciones aplicables al vehículo real, no una aceleración arbitraria de Internet. Además, una anchura exterior próxima a 3 m puede llevar el transporte fuera de los límites ordinarios de determinadas rutas, por lo que Statens vegvesen exige verificar la lista de carreteras y, cuando corresponda, tramitar el transporte especial. citeturn988918search4turn168234search6turn168234search7

## Libros, estándares y software abierto que sí aportan contexto útil

La siguiente selección separa herramientas aptas para cálculo independiente de recursos que sólo sirven como referencia geométrica o de fabricación.

| Recurso | Licencia / estado | Aplicación concreta al proyecto |
|---|---|---|
| **[PyNite](https://github.com/JWock82/Pynite)** | MIT; proyecto activo; la rama actual publica capacidades de análisis elástico 3D y ha tenido releases recientes en 2026. citeturn666225search1turn666225search0 | Mi primera opción para un **solver independiente de barras**: chasis 3D, apoyos, casos de izaje, torsión global, reacciones y comparación con Robot. No usarlo como único verificador de orejas de placa. |
| **[Frame3DD](https://github.com/hpgavin/frame3dd)** | GPL; análisis estático/dinámico de pórticos 2D/3D con rigidez geométrica. citeturn400217search0turn400217search15 | Muy bueno como segundo benchmark de un modelo de barras sencillo porque el input es transparente y la formulación es madura. Menor ecosistema moderno que PyNite. |
| **[FreeCAD](https://github.com/FreeCAD/FreeCAD) + [CalculiX](https://github.com/Dhondtguido/CalculiX)** | FreeCAD LGPL‑2.1; CalculiX GPL‑2.0; el repositorio CalculiX muestra actividad durante 2026. citeturn666225search5turn400217search17turn849312search14 | Adecuado para submodelos de chapa/sólido de una oreja, rigidizador, RHS y soldaduras idealizadas. FreeCAD FEM documenta integración con CalculiX. citeturn666225search18 |
| **[Code_Aster](https://code-aster.org/en)** | Open source, GNU GPL, desarrollado por EDF; dispone de mecánica no lineal, dinámica y una extensa base de casos de verificación. citeturn400217search18turn400217search20turn400217search52 | Alternativa avanzada para contacto, plasticidad, dinámica o validación independiente de un detalle FEM crítico. Mayor curva de aprendizaje. |
| **[OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy)** | Python sobre OpenSees; su licencia impone condiciones adicionales para redistribución comercial. citeturn666225search26turn666225search24 | Útil si posteriormente quieres análisis dinámico/no lineal paramétrico; excesivo para la primera viga estática. |
| **[IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell)** | Ecosistema open source basado principalmente en LGPL; repositorios activos en noviembre de 2026. citeturn666225search8turn666225search35 | No es un solver estructural: úsalo para validar IFC, extraer GUID, secciones, materiales y masas y comparar BIM contra modelo analítico. |
| **[WikiHouse Skylark](https://github.com/wikihouseproject/Skylark)** | Sistema abierto de madera; repo actualizado el 9 de octubre de 2026; contenido de sistema bajo CC BY‑SA. citeturn849312search1turn400217search25 | Útil para estudiar lógica de piezas CNC, documentación, tolerancias y envolvente modular; **no** es una referencia directa para un chasis de acero transportable. El propio proyecto exige un ingeniero estructural local. citeturn400217search26 |

Como biblioteca técnica, priorizaría **SCI P272, Modular Construction using Light Steel Framing**, porque tiene capítulos específicos de requisitos de transporte y fuerzas de izaje y señala que las unidades deben resistir acciones adicionales durante manipulación. citeturn671035search48turn671035search5

Después usaría **Lawson, Ogden & Goodier, *Design in Modular Construction***, que reúne diseño estructural modular y más de 40 casos de estudio; es una referencia de contexto industrial y arquitectónico mucho más amplia que un manual de tiny houses. citeturn671035search0

Para el cálculo metálico, la publicación gratuita **JRC, *Design of Steel Buildings — Worked Examples*** es una de las mejores referencias disponibles porque cubre base de diseño, modelado, miembros, uniones y acero conformado con ejemplos de Eurocode 3. citeturn955640search0

Para las conexiones, **Jaspart & Weynand, *Design of Joints in Steel and Composite Structures*** aborda explícitamente pernos, soldaduras, uniones simples y resistentes a momento bajo EN 1993‑1‑8. citeturn955640search2

Para torsión, usaría **SCI P385, *Design of Steel Beams in Torsion***, especialmente si las orejas o apoyos generan cargas excéntricas sobre RHS, canales o vigas abiertas. citeturn671035search47

Finalmente, para desarrollar y comprobar fórmulas manuales antes del FEM, el material de David Roylance en MIT OCW sobre desplazamiento de vigas es una referencia abierta y apropiada. citeturn671035search2

## Pila de software y plan preciso de interoperabilidad Autodesk

No asumiría que tengo acceso a tu entorno Autodesk hasta que exista realmente una conexión o archivos exportados. El artículo que proporcionaste sobre integraciones de infraestructura describe el ecosistema Autodesk Forma/Construction Cloud y sus integraciones, pero no concede por sí mismo acceso a un proyecto, modelo o API. citeturn818790search26

La pila estable que recomiendo es:

| Función | Herramienta principal | Verificación independiente |
|---|---|---|
| Arquitectura/BIM y coordinación | **Revit** | IFC + IfcOpenShell |
| Análisis global | **Robot Structural Analysis Professional** | Python/PyNite y, para casos seleccionados, Frame3DD |
| Modelo local de chapa/oreja | Robot shell FEM o solver comercial acordado | CalculiX o Code_Aster |
| Detallado de acero | **Advance Steel**, mientras siga siendo apropiado | PDF/DWG/IFC + revisión manual |
| Control de versiones/documentos | Autodesk Forma Data Management / Docs | registro externo de checksums y memorias PDF |
| Automatización reproducible | Python | tests automatizados |
| Plug-in de escritorio Autodesk | C#/.NET | CI y pruebas con modelos pequeños |

Robot y Advance Steel intercambian modelos mediante SMLX, incluyendo sincronización. Autodesk documenta, sin embargo, que ciertos ajustes geométricos realizados dentro de Robot no se guardan necesariamente en el SMLX; por tanto, SMLX no debe tratarse como un gemelo digital perfecto sin comprobación posterior. citeturn818790search3turn818790search7turn818790search9

El flujo que usaría sería **Revit → modelo analítico controlado → Robot → cálculo → SMLX → Advance Steel → taller**. Cada transferencia debe pasar por una tabla automática que compare: número de miembros, nodos, coordenadas, orientación de ejes locales, familia/sección, material, offsets, releases, masa y cargas. Las cargas no deben confiarse a un “round trip” sin informe de diferencias. Autodesk confirma que el enlace Robot–Advance Steel se basa en SMLX y que Advance Steel mantiene su modelo nativo en DWG. citeturn818790search18turn818790search12

Para fabricación, Advance Steel puede generar planos, BOM y archivos NC; Autodesk documenta específicamente la salida NC‑DStV para geometría de piezas destinada a máquinas CNC y salidas DXF para chapas. Eso permite que el paquete de fabricación contenga **modelo nativo + PDF aprobado + DWG + NC/DSTV + DXF de placas**, pero el taller debe confirmar su versión de DSTV/NC1 y convenciones antes de emitir producción. citeturn818790search4turn818790search29

Para IFC, propondría exportar una versión de coordinación y luego ejecutar un script IfcOpenShell que extraiga cada miembro de acero, longitud, perfil, material y GUID. Ese archivo se compara contra la tabla del modelo analítico para detectar, por ejemplo, que un RHS 120×60×5 en Revit no se haya convertido accidentalmente en otra sección en Robot. IfcOpenShell proporciona API de Python y motor geométrico precisamente para manipular y verificar IFC. citeturn666225search8

Para la nube, Autodesk Platform Services Data Management API permite navegar proyectos, carpetas, items y versiones de archivos en Forma Data Management/Autodesk Docs y requiere autenticación OAuth. No conecta automáticamente Robot con la nube ni concede acceso sin autorización de cuenta/proyecto. citeturn818790search0turn818790search1

APS Automation actualmente ofrece motores cloud para AutoCAD, Revit, Inventor, 3ds Max y Fusion. Robot y Advance Steel no aparecen entre esos motores de Automation; por tanto, no basaría la arquitectura en “ejecutar Robot en APS”. Para Robot, utilizaría su SDK/API instalado localmente; Autodesk sigue proporcionando documentación SDK. Advance Steel 2027 dispone igualmente de COM API y .NET API. citeturn551388search3turn551388search2turn551388search1

Hay además un riesgo de ciclo de vida importante: Autodesk puso Advance Steel en **maintenance mode**; seguirá mantenido y disponible, pero Autodesk dejó de desarrollar nuevas funciones y está trasladando la dirección estratégica del detallado de acero hacia Revit y plataformas BIM. Por esa razón, evitaría hacer del formato propietario de Advance Steel el único registro del proyecto. Mantendría IFC, DSTV, PDF, DWG y una base de datos de parámetros independiente. citeturn551388search0turn551388search7

Para un plug‑in interno, C#/.NET es la elección lógica en escritorio Autodesk, mientras Python es mejor para cálculos auditables, procesamiento de resultados y pruebas numéricas. Debe fijarse una versión concreta de Robot/Revit/Advance Steel y de .NET en cada release; Autodesk ya ha publicado requisitos de transición a .NET 10 para Robot 2026/2027. citeturn551388search4

## Servicios de ingeniería, detallado, fabricación e izaje

No existe una empresa que pueda declararse objetivamente “The Best Structural Fabrication Drawing Service” para este proyecto. Lo correcto es separar **responsabilidad de cálculo**, **detallado**, **fabricación** e **inspección/izaje**, y adjudicar cada alcance a una entidad con capacidad verificable.

| Empresa | Zona / rol | Capacidades verificadas | Cómo la consideraría |
|---|---|---|---|
| **H2 Byggeteknikk** | Bergen, RIB | Ingeniería estructural de acero, madera y hormigón; BIM; responsabilidad PRO; aprobación central en clase de medida 3 para diseño/control de seguridad estructural. citeturn368271search1turn368271search2 | Candidato local fuerte para asumir o revisar el cálculo del módulo como edificio y coordinar el expediente noruego. |
| **Dr.techn. Olav Olsen / Artelia** | Bergen, ingeniería estructural/marina | Oficina en Bergen y especialistas en estructuras, transporte, instalaciones industriales, puertos, marine/offshore. citeturn368271search0 | Especialmente interesante si el izaje, transporte o dinámica requieren experiencia más allá de edificio convencional. |
| **BRIAS / Nordic Steel Group** | Ågotnes, ingeniería + fabricación | Cálculo de resistencia, acero S355, plate work, soldadura certificada y fabricación mecánica. citeturn368271search3 | Candidato para orejas, chasis y detalles fabricables, sujeto a confirmar EN 1090/execution class y responsabilidad de diseño en la cotización. |
| **Bergen Mekaniske Group** | Bergen/Hylkje, fabricación | Taller mecánico con fabricación en acero; publica ISO 9001, 45001, 14001, ISO 3834‑2 y NS‑EN 1090‑1. citeturn368271search4 | Buen candidato para fabricar si el paquete de ingeniería y WPS/inspección son compatibles con su alcance certificado. |
| **Oceaneering Crane & Lifting** | Ågotnes, izaje/ensayo | Puntos fijos de prueba, banco de tracción, células de carga calibradas, pruebas, NDT, ingeniería y verificación de equipos y planes de izaje. citeturn368271search6turn368271search8 | Muy relevante para proof load, instrumentación y revisión independiente de la maniobra. |
| **STM Inspection** | Ågotnes, inspección | Ensayos de material/carga, NDT; inspectores ISO 9712; actividad como empresa de inspección ISO 17020 categoría A. citeturn368271search7 | Posible tercera parte para NDT y documentación de aceptación. |
| **TIM Global Engineering** | Global, steel detailing | Detallado 2D/3D con Advance Steel y Tekla; GA, shop drawings, BOM, NC/CAM y coordinación con ingenieros. citeturn368271search9 | Útil para comparar costes de detailing; no sustituye un RIB noruego ni certifica el izaje por sí solo. |
| **Global CAD Services** | Global, detailing | Tekla/Advance Steel, assembly/part drawings, NC1/DSTV, DXF, IFC; su propia página distingue detailing de responsabilidad de ingeniería. citeturn368271search10 | Adecuado como proveedor de dibujo si recibe conexiones y cargas aprobadas por el ingeniero. |

La mejor estrategia de contratación para este módulo sería que un **ingeniero estructural responsable** con conocimiento de Eurocode/Noruega emita la base de diseño y fuerzas en conexiones; el detailer transforme esa información en modelo de fabricación; el taller fabrique bajo el alcance apropiado de EN 1090; y un especialista de izaje prepare la maniobra y, si corresponde, certifique o verifique accesorios y pruebas. Esa separación reduce el riesgo clásico de que cada proveedor suponga que “la oreja la calculó otro”. TEK17 exige propiedades documentadas y seguridad durante ejecución y estado final, mientras Arbeidstilsynet exige planificación adecuada de las operaciones de elevación. citeturn168234search0turn168234search4

## Flujo stage-gate desde concepto hasta liberación de fabricación

El proyecto debería bloquearse mediante gates formales. Ningún gate se supera por “parece bien en FEM”.

| Gate | Trabajo requerido | Evidencia de salida |
|---|---|---|
| **Requisitos congelados** | Geometría 6 × 3 × H; uso; localización; número de traslados; ruta; remolque; grúa; apoyo final; aberturas; sistema de techo; materiales. | Basis of Design firmada, coordenadas y sistema de unidades único. |
| **Mass & CG model** | Pesaje/estimación por componente con \(m_i,x_i,y_i,z_i\). Casos tanque lleno/vacío, baterías, mobiliario fijo y componentes desmontables. | Tabla de masas, \(W,x_G,y_G,z_G\), incertidumbres y configuración exacta de transporte. |
| **Load takeoff** | Permanente, uso, nieve, viento, apoyo diferencial, transporte, frenado/lateral, izaje, tolerancias, montaje. | Matriz de acciones y combinaciones con referencia normativa. |
| **Hand checks** | Vigas, reacciones, torsión simple, estabilidad, sling geometry, sección, pandeo y conexiones principales. | Memoria reproducible; cálculos independientes de FEM. |
| **Global FEM** | Chasis 3D + paredes portantes que realmente colaboren; releases, offsets, masas y casos de apoyo/izaje/transporte. | Deformadas, reacciones, \(N,V,M,T\), modos propios y sensibilidad a rigidez. |
| **Independent FEM** | Repetir casos gobernantes en PyNite/Frame3DD; submodelo de placas en CalculiX/Code_Aster. | Tabla Robot vs solver independiente con tolerancias predefinidas. |
| **Lift engineering** | CG 3D, geometría de eslingas, desigualdad de ramales, spreader, clearance, hook position, viento, radio de grúa, estabilidad. | Lift plan aprobado por especialista competente. |
| **Connection qualification** | Oreja, agujero, placa, RHS, rigidizadores, soldaduras, pernos y accesibilidad de inspección. | Cálculo EN 1993‑1‑8 + planos de detalle + plan NDT. |
| **Prototype tests** | Probeta de nudo; prueba de chasis; pesaje de CG; izaje instrumentado; recorrido piloto. | Resultados fuerza–desplazamiento, aceleración, deformación residual, fotos y modos de fallo. |
| **Model correlation** | Ajustar rigidez sólo con justificación física y comparar predicción/medición. | Informe de validación y modelo “as-tested”. |
| **Fabrication release** | Revisión RIB, IFC/DWG/SMLX, weld map, WPS, material certs, tolerancias, DSTV/DXF. | Drawing register marcado **Approved for Fabrication** por la autoridad correspondiente. |

La estrategia de ensayo del nudo debe copiar la lógica de Belfast: la probeta debe representar **todo el recorrido de carga**, no únicamente una placa aislada. El ensayo debería medir \(F-\delta\), deformación permanente y modo de fallo. Si el proyecto exige demostrar resistencia última por ensayo, el ingeniero debe establecer previamente número de probetas, factores estadísticos y criterio de aceptación; no debe elegirse un “factor de seguridad” después de ver el resultado. citeturn984735search0

En el chasis completo mediría flecha vertical en centros y esquinas, cambio de diagonales, giro torsional entre esquinas y deformación residual después de descargar. La correlación debe cubrir al menos un caso simétrico y uno fuertemente excéntrico, porque un modelo que sólo reproduce el caso simétrico puede esconder errores en rigidez torsional. La investigación full-scale de Western Sydney proporciona un precedente claro para correlacionar un modelo FEM con propiedades medidas en un módulo real. citeturn984735search2

Antes del primer izaje real, pesaría el módulo terminado sobre cuatro células de carga calibradas. Con reacciones \(P_i\) y coordenadas conocidas:

\[
W=\sum_i P_i,
\qquad
x_G=\frac{\sum_i P_i x_i}{W},
\qquad
y_G=\frac{\sum_i P_i y_i}{W}.
\]

Esto permite verificar \(x_G,y_G\) directamente; la altura \(z_G\) requiere un procedimiento adicional —por ejemplo, inclinación controlada o inventario de masas suficientemente fiable— diseñado por el ingeniero. En el izaje instrumentado colocaría celdas de carga en ramales relevantes y un inclinómetro para verificar reparto real y actitud del módulo.

Para el transporte piloto, replicaría la arquitectura del estudio 2026: acelerómetros triaxiales en remolque y módulo, medición de deformación de diagonales en al menos una pared longitudinal, una transversal y techo/piso, más inspección de puertas, ventanas, sellos y revestimientos antes y después. El objetivo es obtener una envolvente real de aceleración y deformación para el vehículo y ruta previstos. citeturn984735search1

Los datos que todavía faltan para convertir este informe en una primera ingeniería cuantitativa son: altura total; geometría exacta del techo; posición y dimensiones de puertas/ventanas; sección tentativa de cada larguero y travesaño; grado y condición del acero; material y espesor de piso; definición de qué paredes participan estructuralmente; masa y coordenadas de baño, cocina, baterías, depósitos y mobiliario fijo; peso de madera recuperada; cuatro posiciones propuestas de izaje; altura del CG estimada; geometría del spreader/eslingas; número esperado de transportes en vida útil; modelo de remolque y apoyos; ruta prevista; condiciones de apoyo final; nieve y viento del emplazamiento; y criterio funcional de deformación para ventanas, puertas y acabados.

Hasta disponer de esos datos, cualquier perfil, espesor de placa, soldadura, tamaño de oreja o WLL que se dibuje debe estar marcado **CONCEPTUAL — NOT FOR FABRICATION**. La arquitectura correcta del proyecto es que Autodesk produzca geometría y documentación a partir de un modelo de ingeniería controlado, no que el software sustituya el razonamiento mecánico. La aprobación final debe recaer en un ingeniero estructural cualificado y la operación de grúa en un especialista competente de izaje bajo la normativa y condiciones de la jurisdicción real. citeturn168234search0turn168234search4