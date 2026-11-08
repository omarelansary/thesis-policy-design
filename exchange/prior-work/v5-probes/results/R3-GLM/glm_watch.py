"""Status of the GLM-5.3 B2 run (lead, 2026-11-07). Read-only: prints one summary; makes no API call.
Usage: venv/bin/python glm_watch.py [tag]"""
import json, pathlib, subprocess, sys, time, collections, datetime as dt
H = pathlib.Path(__file__).resolve().parent
tag = sys.argv[1] if len(sys.argv) > 1 else "glm-b2-control-rest"
R = H / "runs" / tag
st = json.load(open(R / "stats.json"))
cs = [json.loads(l) for l in open(R / "trace/calls.jsonl")] if (R / "trace/calls.jsonl").exists() else []
alive = subprocess.run(["pgrep", "-f", f"run_partb.py .*--tag {tag} "], capture_output=True, text=True).stdout.split()
done = st["tasks"]; ids = (H / "runs/glm-b2-remaining-ids.txt").read_text().split() if tag == "glm-b2-control-rest" else []
cur = cs[-1]["task"] if cs else None
calls_cur = [c for c in cs if c["task"] == cur and cur not in done]
age = time.time() - (R / "trace/calls.jsonl").stat().st_mtime if cs else None
logl = [l for l in open(R / "progress.log")] if (R / "progress.log").exists() else []
last_task_line = next((l for l in reversed(logl) if " task " in l), logl[0] if logl else "")
since = dt.datetime.fromisoformat(last_task_line[:20].replace("Z", "+00:00")) if last_task_line else None
out = {"now_utc": dt.datetime.now(dt.timezone.utc).strftime("%H:%M"), "process_alive": bool(alive), "finished": st.get("finished"),
       "tasks_done": f"{len(done)} of {len(ids) or '?'}", "exceptions": {t: r["exception"] for t, r in done.items() if r["exception"]},
       "step_capped": [t for t, r in done.items() if r.get("steps", 0) >= 50],
       "current_task": None if st.get("finished") else cur, "hours_on_current": round((dt.datetime.now(dt.timezone.utc) - since).total_seconds() / 3600, 2) if since else None,
       "current_calls": len(calls_cur), "current_timeouts": sum(c["status"] != "ok" for c in calls_cur),
       "current_msgs": calls_cur[-1]["n_messages"] if calls_cur else None, "minutes_since_last_call": round(age / 60, 1) if age else None,
       "total_calls": len(cs), "total_errors": sum(c["status"] != "ok" for c in cs), "stops": [l.strip() for l in logl if "STOP" in l or "finished, exit" in l]}
print(json.dumps(out, indent=1))
