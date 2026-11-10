#!/bin/bash
cd /home/omar/Documents/thesis-policy-design
S=/home/omar/.claude/jobs/54b71024/tmp/p1_watch.state; touch $S
while true; do
  python3 - "$S" <<'PY' || true
import json, glob, sys
S = sys.argv[1]
try: st = json.load(open(S))
except Exception: st = {}
spent = 0.0; errs = 0; exc = 0
for f in glob.glob("design/package-v5/inputs/p1/local/runs/p1-main-*/trace/calls.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if r.get("status") == "ok": spent += r.get("or_cost") or 0
        else: errs += 1
for f in glob.glob("design/package-v5/inputs/p1/local/runs/p1-main-*/progress.log"):
    exc += sum(1 for l in open(f) if " task " in l and "exception None" not in l)
step = int(spent // 2)
if step > st.get("step", 0): print(f"P1 spend passed ${step*2} (now ${spent:.2f})", flush=True); st["step"] = step
if errs > st.get("errs", 0): print(f"P1 failed model calls: {errs}", flush=True); st["errs"] = errs
if exc > st.get("exc", 0): print(f"P1 tasks ending with an exception: {exc}", flush=True); st["exc"] = exc
try: lines = open("design/package-v5/inputs/p1/local/p1-main.progress").read().splitlines()
except OSError: lines = []
for l in lines[st.get("n", 0):]: print("P1 driver:", l[:220], flush=True)
st["n"] = len(lines); json.dump(st, open(S, "w"))
PY
  grep -q "DONE3" design/package-v5/inputs/p1/local/p1-main.progress 2>/dev/null && { echo "P1 driver ended"; exit 0; }
  pgrep -f p1_driver3.sh >/dev/null || { echo "P1 driver process not running"; exit 0; }
  sleep 60
done
