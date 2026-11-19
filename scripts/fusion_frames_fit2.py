"""FluidBridge run_project_script: organize imported Fit2 STEP solids, then save once.

Activate a never-saved MiniHouse_Frames_Fit2_Work containing the assembled STEP,
 or an empty design of that name to import the 14 step_parts in assembly coordinates.
No documents are opened, activated or closed. On failure no save is retried;
discard a partial work import before trying again. No feature history is rebuilt.
"""
import json
import math
from pathlib import Path
from uuid import uuid4


WORK = 'MiniHouse_Frames_Fit2_Work'
PROJECT = 'MiniHouse Frame R0'
OUTPUT = 'MiniHouse_Frames_Fit2'
SOURCE = Path(__file__).resolve().parents[1] / 'fase1/prototipo/marco-fit2'
VOLUME_REL = 1e-4  # Fusion VeryHighCalculationAccuracy: +/- 0.01 percent.
VOLUME_ABS_MM3 = 0.001
CENTER_TOL_MM = 0.02


def manifest():
    rows = json.loads((SOURCE / 'parts.json').read_text(encoding='utf-8-sig'))
    if not isinstance(rows, list) or len(rows) != 14:
        raise ValueError('parts.json must be an array of 14 part records')
    parts = {}
    expected = {f'{i:02d}' for i in range(1, 15)}
    for row in rows:
        name, volume, center = row['name'], row['volume_mm3'], row['center_mm']
        if (not isinstance(name, str) or name[:2] not in expected or name[2:3] != '_'
                or not name[3:].strip() or name != name.strip()):
            raise ValueError(f'invalid or repeated part number: {name!r}')
        if (not isinstance(center, list) or len(center) != 3 or
                not all(type(v) in (int, float) and math.isfinite(v) for v in [volume, *center])
                or volume <= 0):
            raise ValueError(f'{name}: expected positive volume_mm3 and three finite center_mm coordinates')
        expected.remove(name[:2])
        parts[name] = volume, center
    return parts


def guard(doc):
    if doc is None or not doc.isActive or doc.isSaved or doc.name != WORK:
        raise RuntimeError(f'activate the never-saved isolated Fusion design named exactly {WORK!r}')


def destination():
    if app.isOffLine:
        raise RuntimeError('cannot check for an existing cloud file while offline')
    projects = [p for p in app.data.dataProjects.asArray() if p.name == PROJECT]
    if len(projects) != 1:
        raise RuntimeError(f'expected exactly one existing {PROJECT!r} project; found {len(projects)}')
    folder = projects[0].rootFolder
    pending = [folder]
    while pending:
        current = pending.pop()
        for f in current.dataFiles.asArray():
            if f.name.casefold() in {OUTPUT.casefold(), OUTPUT.casefold() + '.f3d', OUTPUT.casefold() + '.f3z'}:
                raise RuntimeError(f'{PROJECT}/{current.name} already contains {f.name!r}; refusing saveAs')
        pending.extend(current.dataFolders.asArray())
    return folder


def import_parts(doc, root, parts):
    directory = SOURCE / 'step_parts'
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in {'.step', '.stp'})
    if (len(files) != 14 or sorted(p.name[:3] for p in files) != sorted(n[:3] for n in parts)):
        raise ValueError(f'{directory}: expected exactly one STEP file per part prefix, 01_ through 14_')
    for path in files:
        guard(doc)
        options = app.importManager.createSTEPImportOptions(str(path))
        if not options or not app.importManager.importToTarget(options, root):
            raise RuntimeError(f'import failed for {path.name}; discard the partial work document')


def measurements(root):
    measured = []
    seen = set()

    def visit(component, transforms):
        if component.id in seen:
            raise RuntimeError(f'{component.name}: shared component cannot have independent native body names')
        seen.add(component.id)
        if component.meshBodies.count:
            raise RuntimeError(f'{component.name}: unexpected mesh in the STEP work design')
        for body in component.bRepBodies:
            if not body.isSolid or body.lumps.count != 1:
                raise RuntimeError(f'{component.name}/{body.name}: expected one connected solid')
            props = body.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy)
            center = props.centerOfMass
            # All handles are native. Map the local centroid outward through each parent.
            for matrix in reversed(transforms):
                if not center.transformBy(matrix):
                    raise RuntimeError(f'{body.name}: cannot transform centroid into assembly coordinates')
            measured.append((body, props.volume * 1000, tuple(v * 10 for v in center.asArray())))
        for occurrence in component.occurrences:
            if occurrence.isReferencedComponent:
                raise RuntimeError(f'{occurrence.name}: refusing to touch externally linked geometry')
            visit(occurrence.component, transforms + (occurrence.transform2,))

    visit(root, ())
    return measured


def match(parts, measured):
    if len(measured) != len(parts):
        raise RuntimeError(f'expected {len(parts)} solid bodies, found {len(measured)}')
    matches = {}
    for body, volume, center in measured:
        names = [n for n, (v, c) in parts.items()
                 if math.isclose(volume, v, rel_tol=VOLUME_REL, abs_tol=VOLUME_ABS_MM3)
                 and math.dist(center, c) <= CENTER_TOL_MM]
        if len(names) != 1 or names[0] in matches:
            raise RuntimeError(f'{body.name}: no unique unused match; volume_mm3={volume:.9g}, '
                               f'assembly_center_mm={center}, candidates={names}')
        matches[names[0]] = body
    return matches


def run():
    doc = app.activeDocument
    guard(doc)
    design = adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
    if design is None:
        raise RuntimeError('work document is not a Fusion design')
    root = design.rootComponent
    parts = manifest()
    folder = destination()  # Reject a rerun before any local import or rename.
    source = 'assembled STEP'
    if not root.bRepBodies.count and not root.occurrences.count:
        if root.meshBodies.count or root.sketches.count or root.features.count or root.constructionPlanes.count:
            raise RuntimeError('step_parts import requires an empty work design')
        import_parts(doc, root, parts)
        source = 'step_parts'

    matches = match(parts, measurements(root))  # Complete geometric preflight before renaming anything.
    guard(doc)
    changes = [(n, b) for n, b in matches.items() if b.name != n]
    # Stage changed names so an existing, incorrect 01_/02_ label cannot block a swap.
    prefix = 'Fit2_work_' + uuid4().hex + '_'
    for i, (_, body) in enumerate(changes):
        body.name = f'{prefix}{i}'
    for name, body in changes:
        body.name = name
    if any(body.name != name for name, body in matches.items()):
        raise RuntimeError('Fusion did not retain the exact assigned names; refusing saveAs')

    if destination().id != folder.id:
        raise RuntimeError('cloud destination changed during validation; refusing saveAs')
    guard(doc)
    if not doc.saveAs(OUTPUT, folder, 'Imported Fit2 STEP solids for tabletop fit checks.', ''):
        raise RuntimeError(f'saveAs failed for {PROJECT}/{OUTPUT}; inspect the destination before retrying')
    RESULT.update(ok=True, saved=True, project=PROJECT, document=doc.name, source=source,
                  body_count=len(matches), bodies=sorted(matches))


run()
