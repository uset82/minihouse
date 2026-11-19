"""Set up the MiniHouse frame as a clean Fusion data project.

Run through FluidBridge/2.0 `run_project_script` with `root` pointing at this
repository. The active document must be the imported R0 frame STEP.

This only organises and saves the conceptual model. It does not size steel,
approve bolts or welds, or release anything for fabrication.
"""
import adsk.core

project_name = args.get("project") or "MiniHouse Frame R0"
purpose = ("Conceptual 1:40 printable frame mock-up for the MiniHouse cabin; "
           "layout and channel geometry only, not for fabrication.")

doc = app.activeDocument
if doc is None or doc.name != args.get("document", "MiniHouse_Frame_R0_Project"):
    raise RuntimeError("activate the imported MiniHouse frame document first")

# Descriptive metadata only: these parameters document the model and do not
# drive the imported B-rep geometry.
meta = [
    ("FrameLength_mm", "6000 mm", "mm", "Real cabin length; conceptual reference"),
    ("FrameWidth_mm", "3000 mm", "mm", "Real cabin width; conceptual reference"),
    ("PrintScale", "40", "", "1:40 plan scale used by the printable model"),
    ("WallSlot_mm", "5.6 mm", "mm", "Printed channel slot; not a specified wall build-up"),
    ("FrameBodies", "48", "", "Bodies from the R0 STEP import"),
]
added = []
for name, expression, units, comment in meta:
    if design.allParameters.itemByName(name) is None:
        design.userParameters.add(
            name, adsk.core.ValueInput.createByString(expression), units, comment)
        added.append(name)

try:
    root.name = "MiniHouse Frame R0"
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
    saved = bool(doc.saveAs("MiniHouse_Frame_R0", project.rootFolder,
                            "Conceptual R0 frame; not for fabrication", ""))
except Exception as exc:
    save_error = f"{type(exc).__name__}: {exc}"

RESULT.update(
    document=doc.name,
    root_name=getattr(root, "name", None),
    root_renamed=renamed,
    added_parameters=added,
    project=project.name if project else None,
    project_created=created_project,
    project_purpose=purpose,
    saved=saved,
    save_error=save_error,
)
