"""Import the combined MiniHouse joint STEP into Autodesk Fusion.

Run only through FluidBridge/2.0 `run_project_script`: the bridge injects
`app`, `adsk`, `args` and `RESULT` on Fusion's main thread. It uses
ImportManager.importToNewDocument so Fusion 2706 does not raise the blocking
"What do you want to create?" chooser that documents.add() opens.

CONCEPTUAL model, not a fabrication release. The imported geometry combines
four numbered printed shells, full-size M6 reference hardware and wall-strip
references. It tests assembly sequence, fit and wrench access only; it does
not define a steel section, bolt class, capacity or thermal-bridge solution.
"""
import os

step_path = args.get("step") or (
    "C:/Users/carlos/PROYECTOS/minihouse/fase1/prototipo/union-combinada-R0/combined_joint.step"
)
doc_name = args.get("name") or "MiniHouse_Combined_Joint_R0"

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
