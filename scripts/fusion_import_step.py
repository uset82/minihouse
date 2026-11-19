"""Import the scaled MiniHouse frame STEP into Autodesk Fusion.

Run only through FluidBridge/2.0 `run_project_script`: the bridge injects
`app`, `adsk`, `args` and `RESULT` on Fusion's main thread. It uses
ImportManager.importToNewDocument so Fusion 2706 does not raise the blocking
"What do you want to create?" chooser that documents.add() opens.

CONCEPTUAL model, not a fabrication release. The imported geometry is the
1:40 frame layout with an exaggerated section, not a specified steel section.
"""
import os

step_path = args.get("step") or (
    "C:/Users/carlos/PROYECTOS/minihouse/fase1/prototipo/marco-R0/frame.step"
)
doc_name = args.get("name") or "MiniHouse_frame_R0"

try:
    if not os.path.isfile(step_path):
        raise FileNotFoundError(step_path)
    options = app.importManager.createSTEPImportOptions(step_path)
    if options is None:
        raise RuntimeError("createSTEPImportOptions returned null")
    doc = app.importManager.importToNewDocument(options)
    if doc is None:
        raise RuntimeError("importToNewDocument failed")
    try:
        doc.name = doc_name
    except Exception:
        pass
    RESULT.update(
        ok=True,
        document=doc.name,
        step=step_path,
        is_saved=bool(doc.isSaved),
    )
except Exception as exc:  # returned to the bridge caller, not raised into Fusion
    RESULT.update(ok=False, error=f"{type(exc).__name__}: {exc}", step=step_path)
