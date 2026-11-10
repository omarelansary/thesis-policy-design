#!/usr/bin/env python3
"""Final robustness checks on the stored R3 runs (read-only). Usage (from ~/r3-work/runs): python3 -I final_checks.py
Computes per arm: share of the bill from step-capped runs (>=48 agent requests), ratio of mean per-task bills
with/without those runs, cold-start counterfactual (first agent request of each task billed with no cache),
and the anatomy of the bill. Predictor requests have input.tools == None (test 'is not None', not key presence)."""
import json, glob
ARMS = [('MiniMax all-tools', 'mm3-b1r-repeat', (0.24, 0.96, 0.048)), ('MiniMax subset', 'mm3-b2r-repeat', (0.24, 0.96, 0.048)),
        ('GLM all-tools', 'glm-b1-all-tools', (0.70, 2.20, 0.13)), ('GLM subset', 'glm-b2-control,glm-b2-control-rest', (0.70, 2.20, 0.13))]
def load(dirs):
    seen = {}
    for d in reversed(dirs.split(',')):          # later directories win for duplicate task ids
        for f in glob.glob(d + '/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'): seen.setdefault(f.split('/')[-3], f)
    return seen
def task_stats(path, pin, pout, pcr):
    rows = [json.loads(l) for l in open(path)]
    agent = [r for r in rows if r['input'].get('tools') is not None]
    cost = tok = 0.0
    for r in rows:
        u = r['output']['usage']; p = u['prompt_tokens']; c = (u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
        cost += ((p - c) * pin + c * pcr + u['completion_tokens'] * pout) / 1e6; tok += p
    first = agent[0]['output']['usage']; fc = (first.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
    cold_extra = fc * (pin - pcr) / 1e6
    return dict(cost=cost, tokens=tok, n_agent=len(agent), cold_extra=cold_extra)
res = {}
for label, dirs, (pin, pout, pcr) in ARMS:
    T = [task_stats(f, pin, pout, pcr) for f in load(dirs).values()]
    capped = [t for t in T if t['n_agent'] >= 48]; rest = [t for t in T if t['n_agent'] < 48]
    tot = sum(t['cost'] for t in T)
    res[label] = (tot / len(T), sum(t['cost'] for t in rest) / len(rest))
    print(f"{label:18s} tasks={len(T)} bill=${tot:7.3f} capped={len(capped)} ({100*sum(t['cost'] for t in capped)/tot:4.1f}% of bill, "
          f"{100*sum(t['tokens'] for t in capped)/sum(t['tokens'] for t in T):4.1f}% of prompt tokens)  cold-start +{100*sum(t['cold_extra'] for t in T)/tot:4.1f}%")
for m in ('MiniMax', 'GLM'):
    A, S = res[m + ' all-tools'], res[m + ' subset']
    print(f"{m}: ratio of mean per-task bills all/subset = {A[0]/S[0]:.2f} (all tasks), {A[1]/S[1]:.2f} (capped runs removed from each arm)")
