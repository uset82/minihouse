---
name: minihouse-structural-analysis
description: Dimensionar o comparar la base, esquinas, apoyos, torsión o flecha del módulo MiniHouse. Produce casos de carga, cálculo reproducible, modelo de Robot y comprobación independiente.
---

# minihouse-structural-analysis

Habilidad del rol [structural-engineer](../../agents/structural-engineer.md). Cargar antes de cualquier cálculo del módulo. Referencia: [investigación estructural](../../../references/investigacion-estructural-casita-6x3.md).

## Procedimiento

1. **Congelar entradas.** Geometría y revisión, inventario de masas con procedencia (medido / fabricante / supuesto), apoyos y configuración exacta (instalado / suspendido / sobre remolque). Si falta un dato, registrar el supuesto con su rango y continuar sólo lo verificable.
2. **Declarar el marco.** Unidades SI explícitas, ejes, origen, signos, versión del software. Milímetros en dibujos; metros y newtons en el modelo, o la combinación declarada.
3. **Matriz de acciones y combinaciones.** Permanente, uso, nieve, viento (emplazamiento por confirmar), apoyo diferencial, transporte (vertical dinámico, frenado, lateral), izaje, tolerancias de montaje y amarre. EN 1990 con anexos nacionales noruegos; izaje y montaje como situaciones transitorias. Coeficientes sólo tras fijar situación y anexo.
4. **Cálculo manual primero.**
   - CG: r_G = Σ m_i r_i / Σ m_i; W = g Σ m_i.
   - Reacciones entre dos estaciones: R_B = W (x_G − x_A)/(x_B − x_A); R_A = W − R_B. Con cuatro apoyos, declarar la hiperestaticidad (3 ecuaciones, 4 incógnitas) y acotar el reparto por rigidez.
   - Viga con voladizos simétricos: M_A = −q a²/2; M_med = qL(L−4a)/8; δ_med = (q/EI)[5(L−2a)⁴/384 − a²(L−2a)²/16].
   - Eslingas: T = V/sen α, H = V·cot α (α desde la horizontal). Incluir dinámica y desigualdad de ramales antes de dimensionar.
   - Torsión: dφ/dx = T/(GJ); alabeo en perfiles abiertos (SCI P385).
   - Excentricidad en orejas: M_e = F·e.
5. **Modelo global en Robot.** Chasis 3D con travesaños; paredes sólo si colaboran de verdad y está documentado. Releases, offsets, masas puntuales (baño, cocina, depósitos lleno/vacío, baterías), casos de apoyo/izaje/transporte. Extraer deformadas, reacciones, N, V, M, T y modos propios.
6. **Verificación independiente.** Repetir casos gobernantes en PyNite (MIT) o Frame3DD; submodelos de placa/oreja en CalculiX o Code_Aster. Tolerancias de comparación fijadas antes. Tabla Robot vs solver independiente con diferencias y causa.
7. **Comprobaciones Eurocode 3.** Clase de sección; M_Ed ≤ M_Rd; N_Ed ≤ N_b,Rd = χ A f_y/γ_M1; interacción N–M; pandeo lateral/torsional; uniones por EN 1993-1-8 (tracción neta, aplastamiento, block tearing, flexión de placa, pared del RHS, rigidizadores, soldaduras sobre garganta efectiva con distribución de fuerza + momento).
8. **Límites de deformación por función.** Flecha de piso, cambio de diagonal de huecos, torsión diferencial entre esquinas, deformación local del punto de izaje. El criterio de puertas/cristales/sellos puede gobernar sobre el del acero.
9. **Registrar y entregar.** Memoria reproducible (script o hoja paso a paso), fecha, archivos, revisión, método, limitaciones y supuestos. Estado: conceptual o calculado. Entregar fuerzas por unión y límites a detallista y a izaje.

## Prohibiciones

- No usar el ejemplo de 3 000 kg como masa real ni "1,2 m" como posición óptima de apoyos: es un caso de viga ideal.
- No dimensionar WLL de eslingas/grúa con números estáticos sin dinámica ni reparto desigual.
- No usar EN 1993-1-2 (fuego) para uniones; la parte correcta es EN 1993-1-8.
- No liberar planos ni autorizar maniobras: eso exige ingeniero responsable y empresa de izaje competente.

## Verificación de cierre

La memoria se reproduce desde cero con los mismos números; el solver independiente coincide dentro de tolerancia o la diferencia está explicada; cada valor de referencia tiene procedencia y condición de aplicación.