"""P2 main-run driver (INT-T-042): runs p2_offering.py for one model over the arms and repeats, in the order repeat 1 of every arm,
then repeat 2, so that a stop leaves complete repeats. Keeps a running total of the computed cost and passes each run only the
budget left under --cap; stops when the cap is reached or a run stops on its own (spend, two failed calls, HTTP 401/402/403).
Writes a counts-only progress line per run to design/package-v5/inputs/p2/local/main-<model>.progress (local).
Usage (with the AppWorld environment's Python, keys in the environment):
  ~/r3-work/venv/bin/python design/package-v5/tools/p2_main_driver.py --model gpt-5-mini --price 0.25,0.025,2.0 --cap 6
"""
import argparse, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
WS = HERE.parents[2]
ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--price", required=True)
ap.add_argument("--cap", type=float, required=True)
ap.add_argument("--arms", default="all,enf,instr,drop")
ap.add_argument("--repeats", type=int, default=2)
ap.add_argument("--api", default="responses")
a = ap.parse_args()
RUNS = WS / "design/package-v5/inputs/p2/local/runs"
PROG = WS / f"design/package-v5/inputs/p2/local/main-{a.model}.progress"
spent = 0.0
for rep in range(1, a.repeats + 1):
    for arm in a.arms.split(","):
        left = round(a.cap - spent, 4)
        if left <= 0.01:
            open(PROG, "a").write(f"{time.strftime('%FT%TZ', time.gmtime())} STOP cap ${a.cap} reached (spent ${spent:.4f})\n")
            sys.exit(3)
        tag = f"p2-main-{a.model}-{arm}-r{rep}"
        rc = subprocess.call([sys.executable, str(HERE / "p2_offering.py"), "--tag", tag, "--arm", arm, "--api", a.api, "--model", a.model,
                              "--price", a.price, "--max-spend", str(left)])
        st = json.load(open(RUNS / tag / "stats.json")) if (RUNS / tag / "stats.json").exists() else {}
        s = float(st.get("spend") or 0.0)
        spent += s
        line = (f"{time.strftime('%FT%TZ', time.gmtime())} {tag}: exit {rc}, tasks {len(st.get('tasks', {}))}, run ${s:.4f}, "
                f"model total ${spent:.4f} of cap ${a.cap}, stopped {st.get('stopped')}\n")
        open(PROG, "a").write(line)
        if rc != 0:
            open(PROG, "a").write(f"STOP: run {tag} exited {rc}\n")
            sys.exit(rc)
open(PROG, "a").write(f"{time.strftime('%FT%TZ', time.gmtime())} DONE model total ${spent:.4f}\n")
