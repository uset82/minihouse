"""Set up the combined MiniHouse joint as a clean Fusion data project.

Run through FluidBridge/2.0 `run_project_script` with `root` pointing at this
repository. The active document must be the imported combined-joint STEP.

This only organises and saves the conceptual model. It does not size steel,
approve bolts or welds, resolve the thermal bridge, or release anything for
fabrication. The body count is recorded as an exchange check, not a strength
or compliance claim.
"""
import adsk.core

project_name = args.get("project") or "MiniHouse Combined Joint R0"
purpose = ("Conceptual combined printable joint article for the MiniHouse "
           "cabin; fit, access and weave-closure only, not for fabrication.")

doc = app.activeDocument
if doc is None or doc.name != args.get("document", "MiniHouse_Combined_Joint_R0"):
    raise RuntimeError("activate the imported MiniHouse combined joint document first")

# Descriptive metadata only: these parameters document the model and do not
# drive the imported B-rep geometry.
meta = [
    ("JointFootprint_mm", "150 mm", "mm", "Printed joint-region footprint"),
    ("PrinterBed_mm", "180 mm", "mm", "Bambu A1 mini printable envelope"),
    ("BoltNominal_mm", "6 mm", "mm", "Full-size M6 hardware reference"),
    ("HoleDiameter_mm", "6.4 mm", "mm", "Printed hole; 0.4 mm diametral clearance"),
    ("ClearSlot_mm", "47.6 mm", "mm", "Locating gap only; C-02 wall build-up OPEN"),
    ("Closure", "split lap", "", "Opens the closed 1 -> 2 -> 3 -> 4 -> 1 cycle"),
    ("StepBodies", "67", "", "Bodies from the combined-joint STEP import; exchange check"),
]
added = []
for name, expression, units, comment in meta:
    if design.allParameters.itemByName(name) is None:
        design.userParameters.add(
            name, adsk.core.ValueInput.createByString(expression), units, comment)
        added.append(name)

body_count = None
try:
    body_count = design.rootComponent.bRepBodies.count
except Exception:
    pass

try:
    root.name = "MiniHouse_Combined_Joint_R0"
    renamed = True
except Exception:
    renamed = False

projects = app.data.dataProjects
project = None
for i in range(projects.count):
    candidate = projects.item(i)
    if candidate.name == project_name:
        project = candidate
        break
created_project = project is None
if project is None:
    project = projects.add(project_name, purpose, "")

saved = False
save_error = ""
try:
    saved = bool(doc.saveAs("MiniHouse_Combined_Joint_R0", project.rootFolder,
                            "Conceptual R0 combined joint; not for fabrication", ""))
except Exception as exc:
    save_error = f"{type(exc).__name__}: {exc}"

RESULT.update(
    document=doc.name,
    root_name=getattr(root, "name", None),
    root_renamed=renamed,
    added_parameters=added,
    body_count=body_count,
    project=project.name if project else None,
    project_created=created_project,
    project_purpose=purpose,
    saved=saved,
    save_error=save_error,
)
