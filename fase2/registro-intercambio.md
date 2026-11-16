# Registro de intercambio y herramientas · Fase 2 preparación

2026-11-17 · Rol: autodesk-bim-coordinator · Estado: evidencia de pruebas locales.

## Inventario de software verificado en esta máquina (2026-11-16)

| Producto | Estado |
| --- | --- |
| Robot Structural Analysis | **No instalado** |
| Advance Steel / AutoCAD / Revit | **No instalados** |
| Autodesk Desktop Connector 2027.3.1, CER, Access, Interoperability Engine | Instalados (sin aplicaciones de autoría) |
| FreeCAD 1.1.3 (con IfcOpenShell embebido) | Instalado y operativo |
| VS Code, Cursor 3.30.14, Claude Code 2.1.319, Antigravity | Instalados (Claude Code sin login: comprobación de segundo cliente pendiente de credenciales) |

## Prueba de intercambio ejecutada (sustituta de SMLX, NO equivalente)

- **Archivo**: [chasis-R0.ifc](chasis-R0.ifc) — IFC4, unidades mm, 12 IfcMember (2 largueros, 6 travesaños canónicos @1200, 4 columnas de izaje candidatas) — regenerado tras la reconciliación de malla, perfiles provisionales marcados CONCEPTUAL.
- **Generación**: [scripts/export_ifc_r0.py](../scripts/export_ifc_r0.py) con IfcOpenShell (Python de FreeCAD).
- **Verificación**: relectura del archivo escrito; 12 miembros, nombres y longitudes (Depth) coinciden con la tabla de entrada, unidades MILLI confirmadas. Tabla resultante: [miembros-R0.csv](miembros-R0.csv) con GUID por miembro.
- **Qué sobrevivió**: identidad, nombre, longitud, unidades, jerarquía espacial. **Qué no se probó**: sección como perfil paramétrico (va como extrusión arbitraria + Tag textual), material, cargas, releases — el enlace Robot↔Advance Steel (SMLX) sigue **pendiente de verificar** hasta instalar las aplicaciones.
- Nota técnica: `Import.export` de FreeCAD falla silenciosamente en este entorno (no escribe el archivo); la vía IfcOpenShell directa funciona y es la prescrita por la habilidad BIM.

## Registro de archivos Fase 2 (revisión R0)

| Archivo | Formato | Estado | Verificación |
| --- | --- | --- | --- |
| chasis-R0.ifc | IFC4 | conceptual | round-trip IfcOpenShell OK |
| miembros-R0.csv | CSV | conceptual | generado por el script verificado |
| comparativa-izaje-R0-resultados.csv | CSV | conceptual (masa EJEMPLO) | equilibrio ΣR=W en 6 casos |

## Pendientes

Instalación/licencia de Robot + Advance Steel (o decisión de pila alternativa con FreeCAD/CalculiX), acceso a proyecto Forma autorizado, segundo cliente IDE con credenciales.