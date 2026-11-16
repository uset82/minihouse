---
name: minihouse-autodesk-steel-detailing
description: Intercambiar perfiles en SMLX o producir planos y archivos de taller para MiniHouse. Produce modelo de detalle, DWG/PDF, lista de materiales y salida de máquina acordada.
---

# minihouse-autodesk-steel-detailing

Habilidad del rol [autodesk-steel-detailer](../../agents/autodesk-steel-detailer.md). Cargar antes de detallar acero o emitir archivos de fabricación.

## Procedimiento

1. **Verificar entradas.** Fuerzas y momentos por unión del ingeniero (con excentricidad), secciones verificadas, revisión de geometría. Sin fuerzas aprobadas: todo el detalle se marca CONCEPTUAL — NOT FOR FABRICATION.
2. **Confirmar la cadena.** Versión instalada de Robot y Advance Steel, resultado registrado de la prueba SMLX (ver [minihouse-autodesk-bim](../minihouse-autodesk-bim/SKILL.md)). Si el enlace no está verificado, secuencia manual documentada y conexión pendiente.
3. **Modelo de detalle en Advance Steel.** Largueros, travesaños, nudos de esquina, orejas de izaje con rigidizadores, placas, pernos y soldaduras. Numeración de pieza estable; cada pieza con material, masa y revisión.
4. **Comprobación de transferencia.** Tabla antes/después: miembros, nodos, coordenadas, ejes locales, sección, material, offsets, releases. Diferencias explicadas o corregidas; nunca round-trip a ciegas.
5. **Planos.** GA + planos de pieza y montaje: cotas en mm, tolerancias, símbolos de soldadura, WPS referenciado, secuencia de fabricación. DWG + PDF; la revisión del dibujo coincide con la BOM.
6. **Salidas de máquina.** NC/DSTV para perfiles, DXF para chapas, sólo tras confirmar con el taller versión DSTV/NC1 y convenciones. Verificar una pieza de prueba en el software del taller si es posible.
7. **Paquete de fabricación.** Modelo nativo + PDF aprobado + DWG + NC/DSTV + DXF + BOM + certificados de material + weld map. Registro neutro adicional (IFC, tabla de parámetros) porque Advance Steel está en maintenance mode.
8. **Liberación.** "Approved for Fabrication" lo marca el ingeniero responsable (RIB) en el drawing register; el detallista prepara, no libera. Ejecución NS-EN 1090-2 con clase acordada.

## Verificación de cierre

BOM ↔ dibujos ↔ modelo coinciden en número de pieza y revisión; el archivo de intercambio abre con unidades, ejes y perfiles correctos; ninguna salida de máquina se emite sin confirmación del taller; el estado de liberación está registrado con responsable y fecha.