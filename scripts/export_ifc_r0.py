#!/usr/bin/env python3
"""MiniHouse · IFC de coordinacion R0 con IfcOpenShell (dentro de FreeCAD).

Ejecutar:
  "C:\\Program Files\\FreeCAD 1.1\\bin\\python.exe" scripts\\export_ifc_r0.py

CONCEPTUAL — NOT FOR FABRICATION. Genera fase2/chasis-R0.ifc (IFC4, mm) con
13 miembros extruidos + tabla fase2/miembros-R0.csv, y VERIFICA releyendo el
archivo: GUID, nombre, longitud, bbox y volumen por miembro.
"""
import os
import sys
import time
import uuid

sys.path.insert(0, r"C:\Program Files\FreeCAD 1.1\lib")
sys.path.insert(0, r"C:\Program Files\FreeCAD 1.1\bin\Lib\site-packages")
import ifcopenshell
import ifcopenshell.api

BASE = r"C:\Users\carlos\PROYECTOS\minihouse\fase2"
OUT = os.path.join(BASE, "chasis-R0.ifc")
CSV = os.path.join(BASE, "miembros-R0.csv")

# miembros R0 canonicos (@1200, reconciliacion-R0): (nombre, perfil provisional, largo_mm, seccion b,h, origen_mm, dir_extrusion)
MIEMBROS = []
for i, y in enumerate((150, 2850), start=1):
    MIEMBROS.append((f"Larguero_{i}", "RHS150x100x5(PROV)", 6000, (100, 150), (0, y - 50, -150), (1, 0, 0)))
for x in range(0, 6001, 1200):
    MIEMBROS.append((f"Travesano_x{x}", "RHS100x100x5(PROV)", 2700, (100, 100), (x - 50, 150, -100), (0, 1, 0)))
for x in (50, 5950):
    for y in (150, 2850):
        MIEMBROS.append((f"Columna_x{x}_y{y}", "SHS100x100x5(PROV)", 3000, (100, 100), (x - 50, y - 50, 0), (0, 0, 1)))


def guid():
    return ifcopenshell.guid.compress(uuid.uuid4().hex)


def main():
    f = ifcopenshell.api.run("project.create_file", version="IFC4")
    project = ifcopenshell.api.run("root.create_entity", f, ifc_class="IfcProject", name="MiniHouse R0 CONCEPTUAL")
    ifcopenshell.api.run("unit.assign_unit", f, length={"is_metric": True, "raw": "MILLI METRE"})
    ctx = ifcopenshell.api.run("context.add_context", f, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", f, context_type="Model",
                                context_identifier="Body", target_view="MODEL_VIEW", parent=ctx)
    site = ifcopenshell.api.run("root.create_entity", f, ifc_class="IfcSite", name="Sitio R0")
    building = ifcopenshell.api.run("root.create_entity", f, ifc_class="IfcBuilding", name="MiniHouse")
    storey = ifcopenshell.api.run("root.create_entity", f, ifc_class="IfcBuildingStorey", name="Chasis z=0")
    ifcopenshell.api.run("aggregate.assign_object", f, relating_object=project, products=[site])
    ifcopenshell.api.run("aggregate.assign_object", f, relating_object=site, products=[building])
    ifcopenshell.api.run("aggregate.assign_object", f, relating_object=building, products=[storey])

    for nombre, perfil, L, (b, h), origen, direccion in MIEMBROS:
        el = ifcopenshell.api.run("root.create_entity", f, ifc_class="IfcMember", name=nombre)
        el.Tag = perfil
        el.Description = "CONCEPTUAL - NOT FOR FABRICATION - perfil provisional"
        # perfil rectangular centrado en el plano perpendicular a la extrusion
        if direccion == (1, 0, 0):   # extruye en x: perfil en y-z
            pts = [(0, -b / 2, -h / 2), (0, b / 2, -h / 2), (0, b / 2, h / 2), (0, -b / 2, h / 2), (0, -b / 2, -h / 2)]
            pos = (origen[0], origen[1] + b / 2, origen[2] + h / 2)
        elif direccion == (0, 1, 0):  # extruye en y: perfil en x-z
            pts = [(-b / 2, 0, -h / 2), (b / 2, 0, -h / 2), (b / 2, 0, h / 2), (-b / 2, 0, h / 2), (-b / 2, 0, -h / 2)]
            pos = (origen[0] + b / 2, origen[1], origen[2] + h / 2)
        else:                          # extruye en z: perfil en x-y
            pts = [(-b / 2, -h / 2, 0), (b / 2, -h / 2, 0), (b / 2, h / 2, 0), (-b / 2, h / 2, 0), (-b / 2, -h / 2, 0)]
            pos = (origen[0] + b / 2, origen[1] + h / 2, origen[2])
        polyline = f.createIfcPolyline([f.createIfcCartesianPoint(tuple(float(v) for v in p)) for p in pts])
        profile = f.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        placement = f.createIfcAxis2Placement3D(
            f.createIfcCartesianPoint(tuple(float(v) for v in pos)),
            f.createIfcDirection(tuple(float(v) for v in direccion)),
            f.createIfcDirection((0.0, 0.0, 1.0)) if direccion != (0, 0, 1) else f.createIfcDirection((1.0, 0.0, 0.0)),
        )
        solid = f.createIfcExtrudedAreaSolid(profile, placement, f.createIfcDirection(tuple(float(v) for v in direccion)), float(L))
        shape = f.createIfcShapeRepresentation(body, "Body", "SweptSolid", [solid])
        prod = f.createIfcProductDefinitionShape(None, None, [shape])
        el.Representation = prod
        loc = f.createIfcLocalPlacement(None, f.createIfcAxis2Placement3D(f.createIfcCartesianPoint((0.0, 0.0, 0.0))))
        el.ObjectPlacement = loc
        ifcopenshell.api.run("spatial.assign_container", f, relating_structure=storey, products=[el])

    f.write(OUT)
    print(f"IFC escrito: {OUT} ({os.path.getsize(OUT)} bytes)")

    # ---- verificacion: releer y contrastar ----
    g = ifcopenshell.open(OUT)
    els = g.by_type("IfcMember")
    assert len(els) == len(MIEMBROS), f"esperaba {len(MIEMBROS)} miembros, hay {len(els)}"
    filas = ["nombre,guid,perfil,largo_mm,bbox_mm,volumen_m3"]
    for el, (nombre, perfil, L, (b, h), origen, d) in zip(els, MIEMBROS):
        assert el.Name == nombre
        solid = el.Representation.Representations[0].Items[0]
        assert abs(solid.Depth - L) < 1e-6, (nombre, solid.Depth, L)
        vol = b * h * L / 1e9
        filas.append(f"{el.Name},{el.GlobalId},{perfil},{L:.0f},\"{origen} dir {d}\",{vol:.6f}")
    # unidades
    units = g.by_type("IfcUnitAssignment")[0]
    ok_mm = any(getattr(u, "Prefix", None) == "MILLI" for u in units.Units if u.is_a("IfcSIUnit"))
    assert ok_mm, "unidades mm no encontradas"
    print(f"VERIFICACION OK: {len(els)} miembros, longitudes y nombres coinciden, unidades mm.")
    with open(CSV, "w", encoding="utf-8") as fh:
        fh.write("\n".join(filas) + "\n")
    print(f"Tabla: {CSV}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()