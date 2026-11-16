---
name: minihouse-autodesk-bim
description: Coordinar ACS/Forma, modelos, revisiones e integración con APS para MiniHouse. Produce inventario de versiones, mapeo y evidencia de intercambio.
---

# minihouse-autodesk-bim

Habilidad del rol [autodesk-bim-coordinator](../../agents/autodesk-bim-coordinator.md). Cargar antes de transferir archivos entre aplicaciones o cambiar revisiones.

## Procedimiento

1. **Inventario.** Registro por archivo: id, revisión, responsable, estado (conceptual / calculado / ensayado / liberado), formato, fecha, checksum. Originales inalterados; cada cambio con revisión nueva.
2. **Antes de cualquier transferencia Autodesk.** Confirmar producto, versión instalada, extensión, permiso de acceso y alcance real de la herramienta. Sin acceso: secuencia manual documentada y conexión marcada pendiente de verificar.
3. **Prueba de intercambio (una barra).** Perfil, material, orientación y unidades entre Robot y Advance Steel vía SMLX; abrir el DWG en la herramienta acordada. Registrar qué sobrevivió: miembros, nodos, coordenadas, ejes locales, sección, material, offsets, releases, masas, cargas. Ciertos ajustes de Robot no viajan en SMLX: la tabla de diferencias es obligatoria, no opcional.
4. **IFC de coordinación.** Exportar y verificar con IfcOpenShell: GUID, longitud, perfil, material y masa por miembro contra la tabla del modelo analítico. Detectar cambios silenciosos de sección (p. ej. RHS 120×60×5 → otra).
5. **Forma / Autodesk Docs.** Sólo con proyecto autorizado. Primero lectura de una revisión conocida; escritura después de la prueba. APS Data Management API requiere OAuth; las credenciales viven en el entorno o gestor autorizado, nunca en el repo. APS Automation no tiene motores de Robot ni Advance Steel: SDK/API local.
6. **Versiones y ciclo de vida.** Fijar versión de Robot/Revit/Advance Steel y .NET por release (transición .NET 10 en Robot 2026/2027). Advance Steel en maintenance mode: mantener registro neutro (IFC, DSTV, PDF, DWG, tabla de parámetros) además del nativo.
7. **Traspaso.** Al siguiente rol: archivos con revisión, registro actualizado, interfaces confirmadas/pendientes y verificaciones ejecutadas. Antes de retomar un archivo compartido, leer plan, revisión y último traspaso.

## Verificación de cierre

El archivo transferido abre con unidades, puntos de control, ejes, perfiles, huecos y revisión correctos; la tabla de diferencias existe y sus entradas están resueltas o registradas; cada interfaz tiene estado (verificada / pendiente) con fecha y evidencia.