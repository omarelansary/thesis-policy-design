"""P4 analysis (AUTH-033): masking (p2_offering.py --mask 30000,3,5000) against keep-everything (P2b's `all` runs), GLM-5.3 on
OpenRouter GMICloud, on the tasks the masking runs share. Counts and AppWorld task ids only.
Per arm and repeat: success (per-task scoring preferred), billed cost, calls, prompt and cached tokens, clearing events and tokens
cleared. Paired per task (mask minus keep, averaged over repeats): success, billed cost, calls; 95% interval by bootstrap over
scenarios (task id before "_"), 4,000 resamples, seed 0, as tools/p2_paired.py. Run-to-run flips within each arm.
Usage: python3 -I design/package-v5/tools/p4_analyze.py RUNS_DIR --out SUMMARY.json
"""
import argparse, json, os, random, statistics

ap = argparse.ArgumentParser()
ap.add_argument("runs")
ap.add_argument("--out", required=True)
a = ap.parse_args()
TAGS = {"keep": ["p2b-or-glm-5.3-all-r1", "p2b-or-glm-5.3-all-r2"], "mask": ["p4-mask-glm-5.3-r1", "p4-mask-glm-5.3-r2"]}


def load(tag):
    d = os.path.join(a.runs, tag)
    evf = next(os.path.join(d, f) for f in ("evaluation-per-task.json", "evaluation.json") if os.path.exists(os.path.join(d, f)))
    ev = json.load(open(evf)).get("individual", {})
    st = json.load(open(os.path.join(d, "stats.json")))["tasks"]
    calls = {}
    for l in open(os.path.join(d, "trace", "calls.jsonl")):
        r = json.loads(l)
        if r.get("status") != "ok":
            continue
        c = calls.setdefault(r["task"], {"prompt": 0, "cached": 0, "billed": 0.0, "clears": 0, "cleared": 0})
        c["prompt"] += r.get("prompt") or 0
        c["cached"] += r.get("cached") or 0
        c["billed"] += r.get("or_cost") or 0
        c["clears"] += 1 if (r.get("mask_cleared_now") or 0) > 0 else 0
        c["cleared"] = max(c["cleared"], r.get("mask_cleared_total") or 0)
    return {t: {"success": int(bool(ev[t]["success"])), "calls": st[t]["calls"], **calls.get(t, {})}
            for t in ev if t in st and st[t].get("exception") is None}


R = {arm: [load(t) for t in tags] for arm, tags in TAGS.items()}
tasks = sorted(set.intersection(*[set(r) for rs in R.values() for r in rs]))
out = {"tasks": len(tasks), "runs": {}, "paired": {}}
for arm, rs in R.items():
    for i, r in enumerate(rs, 1):
        v = [r[t] for t in tasks]
        out["runs"][f"{arm}-r{i}"] = {"success": sum(x["success"] for x in v), "billed": round(sum(x["billed"] for x in v), 4),
                                     "calls": sum(x["calls"] for x in v), "prompt_tokens": sum(x["prompt"] for x in v),
                                     "cached_share": round(sum(x["cached"] for x in v) / max(sum(x["prompt"] for x in v), 1), 3),
                                     "tasks_with_clearing": sum(1 for x in v if x["clears"]), "clearing_events": sum(x["clears"] for x in v),
                                     "tokens_cleared": sum(x["cleared"] for x in v)}
    out[f"{arm}_flips_r1_vs_r2"] = sum(rs[0][t]["success"] != rs[1][t]["success"] for t in tasks)
scen = sorted({t.split("_")[0] for t in tasks})
for k in ("success", "billed", "calls"):
    diff = {t: statistics.mean(R["mask"][i][t][k] - R["keep"][i][t][k] for i in (0, 1)) for t in tasks}
    rng = random.Random(0); bs = []
    for _ in range(4000):
        pick = [rng.choice(scen) for _ in scen]
        v = [diff[t] for s in pick for t in tasks if t.split("_")[0] == s]
        bs.append(sum(v) / len(v))
    bs.sort()
    out["paired"][k] = {"mean_diff_per_task": round(statistics.mean(diff.values()), 4), "ci95_scenario_cluster": [round(bs[99], 4), round(bs[3899], 4)]}
keep_b = sum(out["runs"][f"keep-r{i}"]["billed"] for i in (1, 2)); mask_b = sum(out["runs"][f"mask-r{i}"]["billed"] for i in (1, 2))
keep_c = sum(out["runs"][f"keep-r{i}"]["calls"] for i in (1, 2)); mask_c = sum(out["runs"][f"mask-r{i}"]["calls"] for i in (1, 2))
out["ratios_mask_vs_keep"] = {"billed": round(mask_b / keep_b, 2), "calls": round(mask_c / keep_c, 2)}
out["per_task"] = {f"{arm}-r{i + 1}": {t: [r[t]["success"], round(r[t]["billed"], 5), r[t]["calls"], r[t]["clears"]] for t in tasks}
                   for arm, rs in R.items() for i, r in enumerate(rs)}
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "per_task"}, indent=1))
