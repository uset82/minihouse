"""Import the frame STEP into the active Fusion design and report what arrived.

Run through FluidBridge/2.0 `run_project_script`, which injects `app`, `root`,
`args` and `RESULT`. Unlike importToNewDocument this returns imported objects,
so a silent failure cannot be mistaken for a success.
"""
import os

step_path = args.get("step") or (
    "C:/Users/carlos/PROYECTOS/minihouse/fase1/prototipo/marco-R0/frame.step"
)

try:
    if not os.path.isfile(step_path):
        raise FileNotFoundError(step_path)
    options = app.importManager.createSTEPImportOptions(step_path)
    if options is None:
        raise RuntimeError("createSTEPImportOptions returned null")
    imported = app.importManager.importToTarget2(options, root)
    count = 0 if imported is None else imported.count
    RESULT.update(ok=count > 0, imported_objects=count, step=step_path)
except Exception as exc:
    RESULT.update(ok=False, error=f"{type(exc).__name__}: {exc}", step=step_path)
