#!/bin/bash
# Emits: each $5 of OpenRouter spend, each finished run or STOP line of the driver, and each failed call. State kept across re-arms.
cd /home/omar/Documents/thesis-policy-design
S=/home/omar/.claude/jobs/54b71024/tmp/p2bor_watch.state; touch $S
PROG=design/package-v5/inputs/p2/local/p2b-or-glm-5.3.progress
while true; do
  python3 - "$S" <<'PY' || true
import json, glob, sys
S = sys.argv[1]
st = {}
try: st = json.load(open(S))
except Exception: pass
spent = 0.0; errs = 0; calls = 0
for f in glob.glob("design/package-v5/inputs/p2/local/runs/p2b-or-*/trace/calls.jsonl"):
    for l in open(f):
        r = json.loads(l); calls += 1
        if r.get("status") == "ok": spent += r.get("or_cost") or 0
        elif r.get("status") == "error": errs += 1
step = int(spent // 5)
if step > st.get("step", 0):
    print(f"P2b-OR spend passed ${step*5} (now ${spent:.2f}, {calls} calls)", flush=True); st["step"] = step
if errs > st.get("errs", 0):
    print(f"P2b-OR failed calls: {errs} (spend ${spent:.2f})", flush=True); st["errs"] = errs
try: lines = open("design/package-v5/inputs/p2/local/p2b-or-glm-5.3.progress").read().splitlines()
except OSError: lines = []
for l in lines[st.get("nlines", 0):]:
    print("P2b-OR driver:", l[:200], flush=True)
st["nlines"] = len(lines)
json.dump(st, open(S, "w"))
PY
  if grep -qE "STOP|DONE" $PROG 2>/dev/null; then echo "P2b-OR driver ended"; exit 0; fi
  if ! pgrep -f "tag-prefix p2b-or" >/dev/null; then echo "P2b-OR driver process not running"; exit 0; fi
  sleep 60
done
