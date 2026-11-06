"""Environment check (lead, AUTH-024; corrected 2026-11-06): run the published reference solutions of all 57 dev tasks and evaluate them, with the call Part 4 recorded (r1-appworld-summary, solution_execution): AppWorld(task_id, experiment_name, raise_on_failure=False, ground_truth_mode="full", timeout_seconds=None).
The first version (2026-11-05) left raise_on_failure at AppWorld's default (True), so a solution that expects an HTTP 422 and checks for it stopped with an exception: 46 of 57."""
import os, sys, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
RUN = pathlib.Path(sys.argv[1]); RUN.mkdir(parents=True, exist_ok=True)  # a new AppWorld root (usage: python envcheck.py runs/<new-name>)
if not (RUN/"data").exists(): os.symlink(HERE/"aw-root/data", RUN/"data")
os.environ["APPWORLD_ROOT"] = str(RUN)
from appworld import AppWorld
from appworld.task import load_task_ids
ids = load_task_ids("dev"); res = {}; errs = {}
for t in ids:
    try:
        with AppWorld(task_id=t, experiment_name="envcheck2", raise_on_failure=False, ground_truth_mode="full", timeout_seconds=None) as w:
            out = w.execute(w.task.ground_truth.compiled_solution_code + "\nsolution(apis, requester)")
            if "Execution failed" in str(out): errs[t] = str(out)[-150:]
            res[t] = bool(w.evaluate().success)
    except Exception as e: errs[t] = f"{type(e).__name__}: {str(e)[:120]}"
print(json.dumps({"tasks": len(ids), "passed": sum(res.values()), "failed": [t for t in ids if not res.get(t)], "execution_errors": errs}))
