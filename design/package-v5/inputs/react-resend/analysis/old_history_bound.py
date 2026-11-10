#!/usr/bin/env python3
"""Upper bound for P4-type clearing: the bill share spent re-reading history tokens that are older than K steps.
At request i the prompt = prefix + sum_{j<i} g_j, g_j = prompt[j+1]-prompt[j] (assistant output + tool results of step j).
Tokens from steps j < i-K are 'old'. They are charged at the cached rate if the request's cache covers them
(cache fills front-to-back), else at the fresh rate. Ignores: cache rewrite caused by clearing, accuracy loss.
Usage: python3 -I old_history_bound.py PIN,POUT,PCR LABEL RUNDIR[,RUNDIR2] K [K...]"""
import json, glob, sys
pin, pout, pcr = [float(x)/1e6 for x in sys.argv[1].split(',')]; label = sys.argv[2]; dirs = sys.argv[3].split(','); Ks = [int(k) for k in sys.argv[4:]]
seen = {}
for d in reversed(dirs):
    for f in glob.glob(d+'/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'): seen.setdefault(f.split('/')[-3], f)
tot = 0; old = {K: 0.0 for K in Ks}
for f in seen.values():
    us = [json.loads(l)['output']['usage'] for l in open(f)]
    P = [u['prompt_tokens'] for u in us]; C = [(u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0 for u in us]
    g = [P[j+1]-P[j] for j in range(len(P)-1)]
    for i, u in enumerate(us):
        tot += ((P[i]-C[i])*pin + C[i]*pcr + u['completion_tokens']*pout)
        for K in Ks:
            old_tok = max(0, sum(g[:max(0, i-K)]))          # tokens from steps older than K
            start = P[0]                                     # old tokens occupy positions [P0, P0+old_tok)
            cached_in_old = max(0, min(C[i], start+old_tok) - start)
            old[K] += cached_in_old*pcr + (old_tok-cached_in_old)*pin
print(f"{label}: bill=${tot/1e0:.3f}  " + "  ".join(f"K={K}: ${old[K]:.3f} ({100*old[K]/tot:.0f}%)" for K in Ks))
