"""Paired estimates for P2 and P2b (counts only): per task, the arm's success minus `all`'s, averaged over repeats; the 95% interval
is a bootstrap over scenarios (the task id before "_"), 4,000 resamples, seed 0. Also calls and cost ratios against `all`, and
`all`'s flips between repeat 1 and 2. Written 2026-11-09 to reproduce RESULTS-P2-MAIN's table (whose script was not kept).
Usage: python3 design/package-v5/tools/p2_paired.py RUNS_DIR TAG_PREFIX MODEL ARM [ARM ...]
  e.g. ... design/package-v5/inputs/p2/local/runs p2-main gpt-5-mini enf instr drop
"""
import json, os, random, sys

root, prefix, model, arms = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]


def load(arm, rep):
    d = os.path.join(root, f"{prefix}-{model}-{arm}-r{rep}")
    ev = json.load(open(os.path.join(d, "evaluation.json"))).get("individual", {})
    st = json.load(open(os.path.join(d, "stats.json")))
    succ = {t: int(bool(v.get("success"))) for t, v in ev.items()}
    calls = sum((v or {}).get("calls", 0) for v in st.get("tasks", {}).values())
    return succ, calls, float(st.get("spend") or 0)


base = [load("all", r) for r in (1, 2)]
tasks = sorted(base[0][0])
out = {"model": model, "prefix": prefix, "all_successes_of_60": sum(base[0][0][t] + base[1][0][t] for t in tasks),
       "all_flips_r1_vs_r2": sum(base[0][0][t] != base[1][0][t] for t in tasks), "arms": {}}
scen = sorted({t.split("_")[0] for t in tasks})
for arm in arms:
    runs = [load(arm, r) for r in (1, 2)]
    diff = {t: sum(runs[r][0].get(t, 0) - base[r][0][t] for r in (0, 1)) / 2 for t in tasks}
    rng = random.Random(0); boots = []
    for _ in range(4000):
        pick = [rng.choice(scen) for _ in scen]
        v = [diff[t] for s in pick for t in tasks if t.split("_")[0] == s]
        boots.append(sum(v) / len(v))
    boots.sort()
    out["arms"][arm] = {"successes_of_60": sum(runs[r][0].get(t, 0) for r in (0, 1) for t in tasks),
                        "mean_paired_diff_per_task": round(sum(diff.values()) / len(tasks), 3),
                        "ci95_scenario_cluster": [round(boots[99], 3), round(boots[3899], 3)],
                        "calls_ratio_vs_all": round((runs[0][1] + runs[1][1]) / (base[0][1] + base[1][1]), 2),
                        "cost_ratio_vs_all": round((runs[0][2] + runs[1][2]) / (base[0][2] + base[1][2]), 2) if base[0][2] + base[1][2] else None}
print(json.dumps(out))
