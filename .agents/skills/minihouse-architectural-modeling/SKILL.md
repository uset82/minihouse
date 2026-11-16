---
name: minihouse-architectural-modeling
description: Modelar el volumen, distribuciones, madera recuperada, aberturas o interferencias del módulo MiniHouse. Produce modelo paramétrico, cotas y fichas de masa e interfaces.
---

# minihouse-architectural-modeling

Habilidad del rol [architectural-modeler](../../agents/architectural-modeler.md). Cargar antes de modelar geometría o masas.

## Procedimiento

1. **Base de partida.** Confirmar en PROJECT.md Fase 1 qué está fijado (destino, uso, ruta, ancho de transporte) y qué es supuesto. Croquis originales e intención de Carlos: [references/README.md](../../../references/README.md).
2. **Volumen y cotas.** Planta ≈ 6 000 × 3 000 mm exteriores como punto de partida; registrar salientes y confirmar ancho legal de transporte antes de congelar. Altura total sobre plataforma y distancia libre para aparejos como datos explícitos. Milímetros, ejes y origen declarados.
3. **Aberturas.** Tabla de puertas y ventanas: identificador, dimensión, posición, revisión. Marcar las que imponen límites de deformación (cambio de diagonal) para el cálculo.
4. **Modelo 3D.** Revit si está disponible; AutoCAD para planta/elevaciones. Parámetros con nombre estable; nada de geometría "muerta" sin identificador. Exportar IFC de coordinación con GUIDs estables.
5. **Madera recuperada.** Ficha por lote/pieza: especie (si se conoce), procedencia, estado, humedad, defectos, uso previsto (revestimiento por defecto). Función portante sólo con documentación resistente específica; si no, queda fuera del modelo estructural.
6. **Inventario de masas.** Tabla: id, revisión, componente, material, masa [kg], x/y/z [m] respecto al origen declarado, procedencia (medido / fabricante / estimado), condición (fijo / desmontable / depósito lleno-vacío). Incluir baño, cocina, baterías, depósitos, mobiliario fijo y envolvente. Sumar W y CG preliminar con la fórmula r_G = Σ m_i r_i / Σ m_i, marcado como estimado hasta pesaje.
7. **Interferencias.** Revisar estructura vs instalaciones vs aberturas vs envolvente; registrar colisiones con revisión y resolución propuesta.
8. **Entrega.** Geometría acotada + inventario de masas + tabla de aberturas + propuesta de paredes colaborantes (no decisión) a structural-engineer; IFC y nativo a autodesk-bim-coordinator. Estado conceptual hasta verificación.

## Verificación de cierre

Cada masa tiene procedencia y coordenadas; cada abertura está acotada; el modelo abre en la herramienta acordada con unidades correctas; los planos llevan "CONCEPTUAL — NOT FOR FABRICATION" mientras no haya liberación.