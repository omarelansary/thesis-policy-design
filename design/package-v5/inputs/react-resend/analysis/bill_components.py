#!/usr/bin/env python3
"""Bill split per arm: fixed prefix (first AGENT request of the task = first request that carries tools),
accumulated history, output, and the separate predictor call (subset arms: request without tools).
A prefix cache fills from the FRONT, so a request's cached tokens are allocated to the prefix first.
Usage: python3 -I bill_components.py PIN,POUT,PCR LABEL RUNDIR[,RUNDIR2]   (prices in $ per million tokens)
Data: <run>/experiments/outputs/*/tasks/<id>/logs/lm_calls.jsonl; later RUNDIRs override earlier ones per task id."""
import json, glob, sys
pin, pout, pcr = [float(x) / 1e6 for x in sys.argv[1].split(',')]
label, dirs = sys.argv[2], sys.argv[3].split(',')
seen = {}
for d in reversed(dirs):
    for f in glob.glob(d + '/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'):
        seen.setdefault(f.split('/')[-3], f)
C = dict(pref_read=0, pref_fresh=0, hist_read=0, hist_fresh=0, output=0, predictor=0)
tok_pref = tok_hist = nagent = npred = 0
for f in seen.values():
    rows = [json.loads(l) for l in open(f)]
    agent = [r for r in rows if r['input'].get('tools')]
    pred = [r for r in rows if not r['input'].get('tools')]
    npred += len(pred)
    for r in pred:
        u = r['output']['usage']; p = u['prompt_tokens']; c = (u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
        C['predictor'] += (p - c) * pin + c * pcr + u['completion_tokens'] * pout
    us = [r['output']['usage'] for r in agent]; pref = us[0]['prompt_tokens']
    for u in us:
        p = u['prompt_tokens']; c = (u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
        pr = min(p, pref); hi = p - pr; cp = min(c, pr); ch = c - cp
        C['pref_read'] += cp * pcr; C['pref_fresh'] += (pr - cp) * pin
        C['hist_read'] += ch * pcr; C['hist_fresh'] += (hi - ch) * pin
        C['output'] += u['completion_tokens'] * pout
        tok_pref += pr; tok_hist += hi; nagent += 1
tot = sum(C.values())
print(f"{label}: tasks={len(seen)} agent requests={nagent} predictor requests={npred} bill=${tot:.3f}")
for k, v in C.items(): print(f"   {k:11s} ${v:7.3f} {100*v/tot:5.1f}%")
print(f"   agent prompt tokens: prefix {100*tok_pref/(tok_pref+tok_hist):.0f}% history {100*tok_hist/(tok_pref+tok_hist):.0f}%")
