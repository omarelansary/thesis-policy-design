"""P4 condition check (2026-11-09): share of billed input that is old tool results (before the latest model turn), and its price if cached.
An upper bound on what masking could save in P2: ignores cache rewrites, output and accuracy. Same usage as p4_condition_sizes.py."""
import json, glob, sys, collections, os
import tiktoken
enc = tiktoken.get_encoding("o200k_base"); tok = lambda s: len(enc.encode(s or ""))
root = sys.argv[1]; q = lambda v, p: sorted(v)[min(len(v)-1, int(p*len(v)))]
out = []
for run in sorted(glob.glob(f"{root}/p2-main-*")):
    tr = collections.defaultdict(list)
    for l in open(f"{run}/trace/calls.jsonl"):
        r = json.loads(l)
        if r["status"] == "ok": tr[r["task"]].append(r)
    for task, calls in tr.items():
        f = glob.glob(f"{run}/experiments/outputs/*/tasks/{task}/logs/lm_calls.jsonl")
        if not f: continue
        L = [json.loads(l) for l in open(f[0])]
        pre = len(L[0]["input"]["messages"])
        old = 0
        for c in L:
            m = c["input"]["messages"][pre:]
            last_asst = max([i for i, x in enumerate(m) if x.get("role") == "assistant"], default=-1)
            old += sum(tok(x.get("content")) for i, x in enumerate(m) if x.get("role") == "tool" and i < last_asst)
        billed = sum(c["prompt"] for c in calls); cached = sum(c.get("cached") or 0 for c in calls)
        out.append(dict(old=old, billed=billed, cached=cached, run=os.path.basename(run)))
tot_old = sum(r["old"] for r in out); tot_b = sum(r["billed"] for r in out); tot_c = sum(r["cached"] for r in out)
print("task-runs", len(out))
print("old tool results carried / billed input tokens: overall %.3f; per task-run median %.3f p90 %.3f max %.3f" %
      (tot_old/tot_b, q([r['old']/r['billed'] for r in out], .5), q([r['old']/r['billed'] for r in out], .9), max(r['old']/r['billed'] for r in out)))
print("cached share of billed input: %.3f" % (tot_c/tot_b))
# dollar upper bound for gpt-5-mini prices (0.25 in, 0.025 cached): old tokens assumed cached
for m, pin, pc, pout in (("gpt-5-mini", .25, .025, 2.0), ("gpt-5.4-mini", .75, .075, 4.5)):
    R = [r for r in out if f"p2-main-{m}-" in r["run"]]
    inp = sum((r["billed"]-r["cached"])*pin + r["cached"]*pc for r in R)/1e6
    save = sum(r["old"]*pc for r in R)/1e6
    print(f"{m}: input bill ${inp:.3f}; old results priced as cached ${save:.3f} = {save/inp:.3f} of the input bill (upper bound, before rewrites and output)")
