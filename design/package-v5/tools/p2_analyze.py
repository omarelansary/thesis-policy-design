"""P2 analysis (INT-T-040): reads local run folders of p2_offering.py and writes a committable summary with counts only (task ids,
no tool names, no AppWorld text).

Per run (one model x arm x repeat): tasks, success (AppWorld's evaluator, task goal completion), passes and tests, calls,
steps, prompt / cached / completion / reasoning tokens, cached share, computed cost, calls outside the offered subset, model calls
that failed, served model ids.
Paired comparisons (same model and repeat index, or pooled over repeats): for each arm against `all`, tasks where only `all`
succeeded (b) and only the arm succeeded (c), with the exact two-sided McNemar p; and `all` against itself across repeats (flips),
the run-to-run noise against which arm differences are read.
Usage: python3 design/package-v5/tools/p2_analyze.py --out SUMMARY.json RUN_DIR [RUN_DIR ...]
"""
import argparse, json, math, os

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--out", required=True)
a = ap.parse_args()


def mcnemar(b, c):
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


runs = []
for d in a.runs:
    meta = json.load(open(os.path.join(d, "run-meta.json")))
    st = json.load(open(os.path.join(d, "stats.json")))
    ev = json.load(open(os.path.join(d, "evaluation.json")))
    ind = ev.get("individual", {})
    tr = [json.loads(l) for l in open(os.path.join(d, "trace", "calls.jsonl"))] if os.path.exists(os.path.join(d, "trace", "calls.jsonl")) else []
    ok = [r for r in tr if r.get("status") == "ok"]
    succ = {t: bool(ind.get(t, {}).get("success")) for t in st["tasks"]}
    r = dict(run=os.path.basename(d.rstrip("/")), model=meta["model"], arm=meta["arm"], reasoning_effort=meta["reasoning_effort"],
             harness_sha256=meta["harness_sha256"], tasks=len(st["tasks"]),
             exceptions=sum(1 for v in st["tasks"].values() if v.get("exception")), success=sum(succ.values()),
             tests_passed=sum(len(ind.get(t, {}).get("passes", [])) for t in st["tasks"]),
             tests_total=sum(ind.get(t, {}).get("num_tests", 0) for t in st["tasks"]),
             steps=sum(v.get("steps") or 0 for v in st["tasks"].values()), calls=len(ok), calls_failed=len(tr) - len(ok),
             prompt=sum(x.get("prompt") or 0 for x in ok), cached=sum(x.get("cached") or 0 for x in ok),
             completion=sum(x.get("completion") or 0 for x in ok), reasoning=sum(x.get("reasoning") or 0 for x in ok),
             cost=round(sum(x.get("cost") or 0 for x in ok), 4), outside_subset=sum(x.get("outside_subset") or 0 for x in ok),
             served=sorted({str(x.get("model")) for x in ok}), per_task_success=succ, stopped=st.get("stopped"))
    r["cached_share"] = round(r["cached"] / r["prompt"], 3) if r["prompt"] else None
    runs.append(r)
pairs = []
for x in runs:
    for y in runs:
        if x is y or x["model"] != y["model"] or y["arm"] != "all":
            continue
        common = sorted(set(x["per_task_success"]) & set(y["per_task_success"]))
        b = sum(1 for t in common if y["per_task_success"][t] and not x["per_task_success"][t])
        c = sum(1 for t in common if x["per_task_success"][t] and not y["per_task_success"][t])
        pairs.append(dict(model=x["model"], arm=x["run"], against=y["run"], tasks=len(common), all_only=b, arm_only=c,
                          exact_mcnemar_p=round(mcnemar(b, c), 4)))
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(dict(runs=runs, paired_against_all=pairs), f, indent=1)
for r in runs:
    print(f"{r['run']:28} {r['model']:14} {r['arm']:5} success {r['success']}/{r['tasks']}  calls {r['calls']}  cached {r['cached_share']}  "
          f"outside {r['outside_subset']}  ${r['cost']}")
for p in pairs:
    print(f"  {p['arm']} vs {p['against']}: all-only {p['all_only']}, arm-only {p['arm_only']}, p {p['exact_mcnemar_p']}")
