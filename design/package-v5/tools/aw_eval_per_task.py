"""Score an AppWorld run one task at a time (AUTH-033, 2026-11-10). AppWorld's batch evaluate_tasks fails for a whole run when a
stop interrupted a task mid-session (the open DB state of that task), as in the P2b ScaDS attempts and P1 none r1; scored one by
one, every completed task evaluates. Writes <run>/evaluation-per-task.json ({"individual": ..., "per_task_errors": ...}).
Usage: ~/r3-work/venv/bin/python -I design/package-v5/tools/aw_eval_per_task.py RUN_DIR "ID ID ..."
"""
import json, os, sys
run, ids = sys.argv[1], sys.argv[2].split()
os.environ.update({"APPWORLD_ROOT": run, "PYTHON_DOTENV_DISABLED": "1"})
from appworld.evaluator import evaluate_tasks
exp = os.path.basename(run)
res, bad = {}, {}
for t in ids:
    try:
        ev = evaluate_tasks(task_ids=[t], experiment_name=exp, suppress_errors=True, include_details=True, save_reports=False)
        res[t] = ev["individual"][t]
    except Exception as e:
        bad[t] = f"{type(e).__name__}: {str(e)[:160]}"
json.dump({"individual": res, "per_task_errors": bad}, open(os.path.join(run, "evaluation-per-task.json"), "w"), indent=1, default=str)
print("evaluated", len(res), "success", sum(bool(v["success"]) for v in res.values()), "errors", len(bad))
for t, e in bad.items(): print(" ", t, e.replace(run, "<run>"))
