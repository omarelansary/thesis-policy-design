"""P4 condition check (2026-11-09): per task-run sizes from P2 main logs (API prompt counts; tool-result text tokenized with o200k_base).
Usage: ~/r3-work/venv/bin/python -I design/package-v5/tools/p4_condition_sizes.py design/package-v5/inputs/p2/local/runs (counts only printed)."""
import json, glob, sys, collections, os
import tiktoken
enc = tiktoken.get_encoding("o200k_base")
tok = lambda s: len(enc.encode(s if isinstance(s, str) else json.dumps(s)))
root = sys.argv[1]
q = lambda v, p: sorted(v)[min(len(v)-1, int(p*len(v)))]
res = []; missing = 0
for run in sorted(glob.glob(f"{root}/p2-main-*")):
    tr = [json.loads(l) for l in open(f"{run}/trace/calls.jsonl")]
    by = collections.defaultdict(list)
    for r in tr:
        if r["status"] == "ok": by[r["task"]].append(r)
    for task, calls in by.items():
        f = glob.glob(f"{run}/experiments/outputs/*/tasks/{task}/logs/lm_calls.jsonl")
        obs = []
        if f:
            L = [json.loads(l) for l in open(f[0])]
            pre = len(L[0]["input"]["messages"]); last = L[-1]["input"]["messages"][pre:]
            obs = [tok(m.get("content") or "") for m in last if m.get("role") == "tool"]
        else:
            missing += 1
        p = [c["prompt"] for c in calls]
        res.append(dict(run=os.path.basename(run), task=task, calls=len(calls), first=p[0], last=max(p), growth=max(p)-p[0],
                        billed=sum(p), obs=sum(obs), has_log=bool(f)))
print("task-runs with ok calls", len(res), "without lm_calls log", missing)
for k in ("calls", "first", "last", "growth", "billed", "obs"):
    v = [r[k] for r in res if r["has_log"] or k != "obs"]; print(f"{k}: median {q(v,.5)} p90 {q(v,.9)} max {max(v)}")
R = [r for r in res if r["has_log"]]
print("tool results / last prompt: median %.3f p90 %.3f max %.3f" % tuple(q([r['obs']/r['last'] for r in R], p) for p in (.5,.9,.999)))
print("tool results / growth: median %.3f p90 %.3f" % tuple(q([r['obs']/max(r['growth'],1) for r in R], p) for p in (.5,.9)))
print("task-runs whose last prompt >= 32k:", sum(r['last']>=32000 for r in res), "of", len(res))
