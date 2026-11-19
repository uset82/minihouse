"""Build the editable Fit1 tabletop mock-up in a fresh .tmp/fit1-seed.step import.

Run via FluidBridge run_project_script. No document is opened, activated or closed.
On failure inspect the named operation in the unsaved work document; do not retry
on a partial build. No existing cloud design is updated.
"""
import json
import math
from pathlib import Path


WORK = 'MiniHouse_Frame_Fit1_Work'
PROJECT = 'MiniHouse Frame R0'
OUTPUT = 'MiniHouse_Frame_Fit1'
GEOMETRY = Path(__file__).resolve().parents[1] / 'fase1/prototipo/marco-fit1/geometry.json'


def load_parts(path):
    parts = json.loads(path.read_text(encoding='utf-8'))['parts']
    if not isinstance(parts, list) or len(parts) != 8:
        raise ValueError('geometry.json must contain exactly eight parts')
    names = set()
    for i, part in enumerate(parts, 1):
        name = part.get('name')
        if not isinstance(name, str) or not name.strip() or name != name.strip() or name.casefold() in names:
            raise ValueError(f'part {i}: missing, blank or duplicate name {name!r}')
        names.add(name.casefold())
        ops = part.get('ops')
        if not isinstance(ops, list) or not ops:
            raise ValueError(f'{name}: expected non-empty ops list')
        for n, op in enumerate(ops, 1):
            try:
                if op['mode'] not in (('new',) if n == 1 else ('cut', 'join')):
                    raise ValueError('first operation must be new; remaining operations must be cut or join')
                keys = {'rect', 'circle'}.intersection(op)
                if len(keys) != 1:
                    raise ValueError('expected exactly one rect or circle')
                key = keys.pop()
                dims = op[key]
                if not isinstance(dims, list) or len(dims) != (4 if key == 'rect' else 3):
                    raise ValueError(f'invalid {key} dimensions')
                if any(type(v) not in (float, int) or not math.isfinite(v) for v in [*dims, op['z'], op['h']]):
                    raise ValueError('dimensions must be finite numbers in mm')
                if op['h'] <= 0 or (key == 'circle' and dims[2] <= 0) or (
                        key == 'rect' and (dims[2] <= dims[0] or dims[3] <= dims[1])):
                    raise ValueError('height, radius, width and length must be positive')
            except (TypeError, KeyError, ValueError, OverflowError) as exc:
                raise ValueError(f'{name} op {n}: {exc}; input={op!r}') from exc
    return parts


def guard_document(doc):
    if doc is None or not doc.isActive or doc.name != WORK or doc.isSaved:
        raise RuntimeError(f'activate the fresh, never-saved STEP import named exactly {WORK!r}')


def verified_seed(root):
    if (root.bRepBodies.count != 1 or root.occurrences.count or root.meshBodies.count
            or root.sketches.count or root.constructionPlanes.count):
        raise RuntimeError('expected one imported root solid, no occurrences, meshes, sketches or user planes')
    body = root.bRepBodies.item(0)
    # Exact fingerprint from scripts/frame_fit1.py, not merely a small body with a plausible name.
    bounds = body.preciseBoundingBox
    actual = (*bounds.minPoint.asArray(), *bounds.maxPoint.asArray())
    expected = (-0.5, -0.5, 0.0, -0.4, -0.4, 0.1)  # cm
    if (not body.isSolid or body.faces.count != 6 or not math.isclose(body.volume, 0.001, rel_tol=1e-5)
            or not all(math.isclose(a, b, abs_tol=1e-5) for a, b in zip(actual, expected))):
        raise RuntimeError(f'not the 1 mm sacrificial cube from .tmp/fit1-seed.step: bounds(cm)={actual}')
    return body


def guard_destination(folder):
    if app.isOffLine:
        raise RuntimeError('Fusion must be online to verify the destination')
    folders = [folder]
    while folders:
        current = folders.pop()
        for file in current.dataFiles.asArray():
            if file.name.casefold() in (OUTPUT.casefold(), OUTPUT.casefold() + '.f3d'):
                raise RuntimeError(f'{file.name!r} already exists in {PROJECT}/{current.name}; refusing saveAs')
        folders.extend(current.dataFolders.asArray())


def check_health(entity):
    if entity is None:
        raise RuntimeError('Fusion returned no timeline entity')
    if entity.healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState:
        raise RuntimeError(f'{entity.name}: health={entity.healthState} {entity.errorOrWarningMessage}')


def add_op(root, planes, name, label, op):
    fusion = adsk.fusion
    core = adsk.core
    mode, z = op['mode'], op['z']
    distance = core.ValueInput.createByReal  # Fusion internal length unit is cm.
    if z not in planes:
        plane_input = root.constructionPlanes.createInput()
        if not plane_input.setByOffset(planes[0], distance(z / 10)):
            raise RuntimeError('could not define XY offset')
        plane = root.constructionPlanes.add(plane_input)
        plane.name = f'Fit1 XY at {z:g} mm'
        plane.isLightBulbOn = False
        planes[z] = plane
    sketch = root.sketches.add(planes[z])
    sketch.name = label + ' profile'

    def point(x, y):
        return sketch.modelToSketchSpace(core.Point3D.create(x / 10, y / 10, z / 10))

    if 'rect' in op:
        x, y, xx, yy = op['rect']
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(point(x, y), point(xx, yy))
    else:
        x, y, r = op['circle']
        sketch.sketchCurves.sketchCircles.addByCenterRadius(point(x, y), r / 10)
    if sketch.profiles.count != 1:
        raise RuntimeError(f'expected one closed profile; found {sketch.profiles.count}')

    operations = fusion.FeatureOperations
    extrudes = root.features.extrudeFeatures
    target = None if mode == 'new' else root.bRepBodies.itemByName(name)
    if mode != 'new' and target is None:
        raise RuntimeError('named target body not found')
    operation = operations.CutFeatureOperation if mode == 'cut' else operations.NewBodyFeatureOperation
    ext_input = extrudes.createInput(sketch.profiles.item(0), operation)
    extent = fusion.DistanceExtentDefinition.create(distance(op['h'] / 10))
    if not ext_input.setOneSideExtent(extent, fusion.ExtentDirections.PositiveExtentDirection):
        raise RuntimeError('could not define positive extrusion extent')
    if mode == 'cut':
        ext_input.participantBodies = [target]
    feature = extrudes.add(ext_input)
    check_health(feature)
    feature.name = label + (' tool' if mode == 'join' else '')
    sketch.isLightBulbOn = False
    if feature.bodies.count != 1:
        raise RuntimeError(f'extrusion produced {feature.bodies.count} bodies instead of one')
    body = feature.bodies.item(0)
    if mode == 'join':
        # Extrude participantBodies does not restrict joins. Explicit Combine cannot absorb a neighbor.
        tools = core.ObjectCollection.create()
        tools.add(body)
        combines = root.features.combineFeatures
        join = combines.createInput(target, tools)
        join.operation = operations.JoinFeatureOperation
        join.isKeepToolBodies = False
        feature = combines.add(join)
        check_health(feature)
        feature.name = label
        if feature.bodies.count != 1:
            raise RuntimeError('combine did not leave a single target body')
        body = feature.bodies.item(0)
    if not body.isSolid or body.lumps.count != 1:
        raise RuntimeError('operation did not leave one connected solid')
    if mode == 'new':
        body.name = name
    elif body.name != name:
        raise RuntimeError(f'expected target {name!r}, got {body.name!r}')


def build():
    doc = app.activeDocument
    guard_document(doc)
    # Bind model handles to the guarded document instead of trusting cached bridge handles.
    design = adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
    if design is None:
        raise RuntimeError('work document is not a Fusion design')
    root = design.rootComponent
    verified_seed(root)
    parts = load_parts(GEOMETRY)
    projects = [p for p in app.data.dataProjects.asArray() if p.name == PROJECT]
    if len(projects) != 1:
        raise RuntimeError(f'expected one existing project named {PROJECT!r}; found {len(projects)}')
    destination = projects[0].rootFolder
    guard_destination(destination)
    guard_document(doc)
    parametric = adsk.fusion.DesignTypes.ParametricDesignType
    if design.designType != parametric:
        design.designType = parametric
    if design.designType != parametric:
        raise RuntimeError('Fusion did not enable parametric history')
    timeline = design.timeline
    if timeline.markerPosition != timeline.count or timeline.count > 1 or any(
            not adsk.fusion.BaseFeature.cast(timeline.item(i).entity) for i in range(timeline.count)):
        raise RuntimeError('work document contains history other than the seed import; refusing to build')
    root = design.rootComponent
    seed = verified_seed(root)
    removed = root.features.removeFeatures.add(seed)
    check_health(removed)
    removed.name = 'Remove sacrificial STEP seed'
    if root.bRepBodies.count != 0:
        raise RuntimeError('seed removal did not leave an empty root')

    planes = {0: root.xYConstructionPlane}
    groups = []
    for part_index, part in enumerate(parts, 1):
        name = part['name']
        start = timeline.count
        for n, op in enumerate(part['ops'], 1):
            label = f'{name} {n:02d} {op["mode"]} {"rect" if "rect" in op else "circle"}'
            try:
                add_op(root, planes, name, label, op)
                if root.bRepBodies.count != part_index:
                    raise RuntimeError(f'expected {part_index} root bodies; found {root.bRepBodies.count}')
            except Exception as exc:
                raise RuntimeError(f'{label}: {exc}; input={op!r}') from exc
        groups.append((start, timeline.count - 1, name))

    if not design.computeAll():
        raise RuntimeError('Fusion failed to complete Compute All')
    for i in range(timeline.count):
        check_health(timeline.item(i))
    bodies = list(root.bRepBodies)
    names = sorted(b.name for b in bodies)
    if (names != sorted(p['name'] for p in parts) or root.occurrences.count
            or not all(b.isSolid and b.lumps.count == 1 and b.volume > 0 for b in bodies)):
        raise RuntimeError(f'final body validation failed: {names}')
    count = sum(len(p['ops']) for p in parts)
    if root.sketches.count != count or root.features.extrudeFeatures.count != count:
        raise RuntimeError(f'expected one editable sketch and extrusion per operation ({count})')
    # Group backwards so a collapsed group cannot shift the ungrouped indices.
    for first, last, name in reversed(groups):
        group = timeline.timelineGroups.add(first, last)
        if group is None:
            raise RuntimeError(f'could not group the timeline for {name}')
        group.name = name

    guard_destination(destination)
    guard_document(doc)
    app.activeViewport.fit()  # The initial view may still be zoomed in on the 1 mm seed.
    if not doc.saveAs(OUTPUT, destination, 'Editable tabletop frame fit test only; not for fabrication.', ''):
        raise RuntimeError(f'saveAs failed for {PROJECT}/{OUTPUT}; inspect the work document before retrying')
    RESULT.update(ok=True, saved=True, project=PROJECT, document=doc.name, body_count=len(names),
                  bodies=names, sketches=count, extrusions=count, offset_planes=len(planes) - 1)


build()
