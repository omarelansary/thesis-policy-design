"""Environment check (lead, AUTH-024): run the published reference solutions of all 57 dev tasks and evaluate them, as Part 4 did. No model call."""
import os, sys, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
RUN = HERE / "runs" / "envcheck"; RUN.mkdir(parents=True); os.symlink(HERE / "aw-root/data", RUN / "data")
os.environ["APPWORLD_ROOT"] = str(RUN)
from appworld import AppWorld
from appworld.task import load_task_ids
ids = load_task_ids("dev"); errs = {}; res = {}
for t in ids:
    try:
        with AppWorld(task_id=t, experiment_name="envcheck", ground_truth_mode="full") as w:
            w.execute(w.task.ground_truth.compiled_solution_code + "\nsolution(apis, requester)")  # as AppWorld's own verify.py does
            tracker = w.evaluate(); res[t] = bool(tracker.success)
    except Exception as e:
        errs[t] = f"{type(e).__name__}: {str(e)[:120]}"
print(json.dumps({"tasks": len(ids), "execution_errors": errs, "passed": sum(res.values()), "failed": [t for t in ids if not res.get(t)]}))
