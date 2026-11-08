"""Evaluate the 21 finished tasks of runs/glm-b2-control (killed by the laptop restart on 2026-11-07 before its own evaluation step)
with AppWorld's own evaluator, as run_partb.py does. Local only, no API call. Lead, 2026-11-08."""
import json, os, pathlib
H = pathlib.Path(__file__).resolve().parent
RUN = H / "runs" / "glm-b2-control"
os.environ.update({"APPWORLD_ROOT": str(RUN), "PYTHON_DOTENV_DISABLED": "1"})
from appworld.evaluator import evaluate_tasks
st = json.load(open(RUN / "stats.json"))
done = [t for t, r in st["tasks"].items() if r.get("exception") is None]
ev = evaluate_tasks(task_ids=done, experiment_name="glm-b2-control", suppress_errors=True, include_details=True, save_reports=True)
(RUN / "evaluation.json").write_text(json.dumps(ev, indent=1, default=str))
print(len(done), "tasks;", sum(bool(v["success"]) for v in ev["individual"].values()), "passed")
