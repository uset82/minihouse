"""Optional OCCT-backed STEP export for the conceptual frame and joint models.

Why this exists
---------------
The repository's stdlib STEP writer emits valid-looking B-rep entities, but
Fusion 2706 creates only empty components from it (bodies: 0). A real OCCT
STEP writer produces a file that Fusion imports as actual solids. This module
isolates that optional dependency: STL/3MF and all checks stay stdlib-only.

Install (local, does not touch the global environment):

    python -m pip install --target .tmp/ocp cadquery-ocp==7.9.3.1.1

Or make OCP available normally in Python. `MINIHOUSE_OCP_DIR` can point to an
alternative directory. Nothing here claims structural validity of the model.
"""

import datetime
import os
import re
import sys
import tempfile
from pathlib import Path

DEFAULT_LOCAL_OCP = Path(__file__).resolve().parent.parent / ".tmp" / "ocp"


def ocp():
    """Import and return the OCP module namespace, with a local fallback."""
    try:
        import OCP  # noqa: F401
    except ImportError:
        extra = os.environ.get("MINIHOUSE_OCP_DIR") or str(DEFAULT_LOCAL_OCP)
        if extra and Path(extra).is_dir():
            sys.path.insert(0, str(extra))
        else:
            raise ImportError(
                "OCCT STEP export needs cadquery-ocp. Install with "
                "`python -m pip install --target .tmp/ocp cadquery-ocp==7.9.3.1.1` "
                "or set MINIHOUSE_OCP_DIR."
            )
        import OCP  # noqa: F811
    return OCP


def available():
    """True when an OCCT STEP writer can be imported."""
    try:
        ocp()
        return True
    except ImportError:
        return False


def shell_to_solid(sh, tol=1e-6):
    """Sew one triangulated Shell into a single OCCT solid."""
    ocp()
    from OCP.gp import gp_Pnt
    from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon,
                                    BRepBuilderAPI_MakeFace,
                                    BRepBuilderAPI_Sewing,
                                    BRepBuilderAPI_MakeSolid)
    from OCP.TopoDS import TopoDS
    from OCP.BRepCheck import BRepCheck_Analyzer

    sewing = BRepBuilderAPI_Sewing(tol)

    faces = []
    for a, b, c in sh.oriented_triangles():
        p = BRepBuilderAPI_MakePolygon(gp_Pnt(*sh.verts[a]),
                                       gp_Pnt(*sh.verts[b]),
                                       gp_Pnt(*sh.verts[c]))
        p.Close()
        faces.append(BRepBuilderAPI_MakeFace(p.Wire()).Face())
    if not faces:
        raise ValueError(f"empty shell: {sh.name}")
    for face in faces:
        sewing.Add(face)
    sewing.Perform()
    shell = TopoDS.Shell_s(sewing.SewedShape())
    solid = BRepBuilderAPI_MakeSolid(shell).Solid()
    if not BRepCheck_Analyzer(solid).IsValid():
        raise ValueError(f"OCCT rejected shell: {sh.name}")
    return solid


def write_step(path, shells, *, exact_shapes=None, product_name="MiniHouse R0"):
    """Write a Fusion-importable STEP; return the number of solids.

    OCCT emits one ADVANCED_BREP_SHAPE_REPRESENTATION per solid. Fusion imports
    that as empty components. The valid OCCT B-rep entities are therefore kept,
    but wrapped in one product with one representation listing every solid —
    the same shape Fusion's own exporter uses for a multi-body design.
    """
    ocp()
    from OCP.TopoDS import TopoDS_Compound
    from OCP.BRep import BRep_Builder
    from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs

    path = Path(path)
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "occt-raw.step"
        compound = TopoDS_Compound()
        builder = BRep_Builder()
        builder.MakeCompound(compound)
        if exact_shapes is not None and len(exact_shapes) != len(shells):
            raise ValueError('exact shapes and labels must have matching counts')
        for idx, sh in enumerate(shells):
            builder.Add(compound, shell_to_solid(sh) if exact_shapes is None else exact_shapes[idx])
        writer = STEPControl_Writer()
        transfer = writer.Transfer(compound, STEPControl_AsIs)
        if int(getattr(transfer, "value", transfer)) != 1:
            raise RuntimeError("OCCT STEP transfer failed")
        written = writer.Write(str(raw))
        if int(getattr(written, "value", written)) != 1:
            raise RuntimeError("OCCT STEP write failed")
        raw_text = raw.read_text(encoding="utf-8", errors="replace")

    _, data = raw_text.split("DATA;", 1)
    ents = {int(m.group(1)): m.group(2)
            for m in re.finditer(r"#(\d+)\s*=\s*(.*?);", data, re.S)}
    breps = sorted(i for i, v in ents.items() if "MANIFOLD_SOLID_BREP(" in v)
    if len(breps) != len(shells):
        raise RuntimeError(f"OCCT wrote {len(breps)} solids, expected {len(shells)}")
    for brep, sh in zip(breps, shells):
        label = str(sh.name).replace("'", "")
        ents[brep] = re.sub(r"MANIFOLD_SOLID_BREP\('[^']*'",
                            f"MANIFOLD_SOLID_BREP('{label}'", ents[brep], count=1)

    geom = set(breps)
    queue = list(breps)
    while queue:
        i = queue.pop()
        for ref in re.findall(r"#(\d+)", ents[i]):
            ref = int(ref)
            if ref not in geom and ref in ents:
                geom.add(ref)
                queue.append(ref)
    ents = {i: v for i, v in ents.items() if i in geom}

    nid = max(ents) + 1

    def add(entity):
        nonlocal nid
        ident = nid
        nid += 1
        ents[ident] = entity
        return ident

    app = add("APPLICATION_CONTEXT('Core Data for Automotive Mechanical Design Process')")
    proto = add("APPLICATION_PROTOCOL_DEFINITION('international standard',"
                f"'automotive_design',2009,#{app})")
    product_ctx = add(f"PRODUCT_CONTEXT('part definition',#{app},'mechanical')")
    def_ctx = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{proto},'design')")
    length = add("(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))")
    angle = add("(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))")
    solid_angle = add("(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())")
    uncertainty = add(
        f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-07),#{length},"
        "'distance_accuracy_value','')")
    geom_ctx = add(
        f"(GEOMETRIC_REPRESENTATION_CONTEXT(3) "
        f"GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{uncertainty})) "
        f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{length},#{angle},{solid_angle})) "
        "REPRESENTATION_CONTEXT('','3D'))")
    prod = product_name.replace("'", "''")
    product = add(f"PRODUCT('{prod}','{prod}',$,(#{product_ctx}))")
    formation = add(f"PRODUCT_DEFINITION_FORMATION('',$,#{product})")
    definition = add(
        f"PRODUCT_DEFINITION('{prod}','{prod}',#{formation},#{def_ctx})")
    shape = add(f"PRODUCT_DEFINITION_SHAPE('',$,#{definition})")
    items = ",".join(f"#{b}" for b in breps)
    rep = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('',({items}),#{geom_ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{shape},#{rep})")

    stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    head = [
        "ISO-10303-21;", "HEADER;",
        "FILE_DESCRIPTION(('MiniHouse conceptual frame'),'2;1');",
        f"FILE_NAME('{path.name}','{stamp}',('Inge'),('MiniHouse'),"
        "'OCCT B-rep with minimal product layer',"
        "'conceptual - not for fabrication','');",
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 3 1 1 }'));",
        "ENDSEC;", "DATA;"
    ]
    out = "\n".join(head) + "\n" + "\n".join(
        f"#{i} = {ents[i]};" for i in sorted(ents)) + "\nENDSEC;\nEND-ISO-10303-21;\n"
    if out.count("MANIFOLD_SOLID_BREP(") != len(shells):
        raise RuntimeError("STEP rebuild lost solids")
    path.write_text(out, encoding="utf-8")
    return len(shells)
