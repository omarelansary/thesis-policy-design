#!/usr/bin/env python3
"""Upper bound on bill saving from merging consecutive requests whose tool-call arguments do not use
any value that first appeared in the previous step's results (perfect-foresight batching).
Removed request i loses its INPUT cost (fresh*pin + cached*pcr); its output (completion) is kept
(the work still has to be generated in the earlier request). Ignores added code-writing overhead,
ignores cascades that violate dependencies on older steps -> an UPPER bound.
Usage: python3 -I batching_bound.py PRICES RUNDIR[,RUNDIR2] ...   PRICES = pin,pout,pcr  ($/M)"""
import json, re, sys, glob, os
def mk(minlen_num, minlen_word):
    return re.compile(r'(?<![A-Za-z0-9_])(?:[0-9]{%d,}|[A-Za-z_@.\-][A-Za-z0-9_@.\-]{%d,})' % (minlen_num, minlen_word-1))
def text(m):
    c = m.get('content')
    if isinstance(c, list): c = ' '.join(x.get('text','') for x in c if isinstance(x, dict))
    return c or ''
def per_task(path, TOK):
    rows = [json.loads(l) for l in open(path)]
    if not rows: return None
    use = [r['output']['usage'] for r in rows]
    msgs = list(rows[-1]['input']['messages']) + [rows[-1]['output']['choices'][0]['message']]
    st, i = [], 0
    while i < len(msgs):
        if msgs[i]['role'] == 'assistant':
            j = i+1; res = []
            while j < len(msgs) and msgs[j]['role'] == 'tool': res.append(text(msgs[j])); j += 1
            st.append((i, [t['function']['arguments'] for t in (msgs[i].get('tool_calls') or [])], res)); i = j
        else: i += 1
    real = st[len(st)-len(rows):]
    known = set(TOK.findall(' '.join(text(m) for m in msgs[:real[0][0]])))
    indep = []   # per request i: True if its args use nothing first seen in step i-1 results
    prev_new = set()
    for k, (idx, args, res) in enumerate(real):
        a = set(TOK.findall(' '.join(args))) if args else set()
        indep.append((k > 0) and bool(args) and not (a & prev_new))
        before = set(known); known |= a
        r = set(TOK.findall(' '.join(res))) if res else set()
        prev_new = r - before; known |= r
    return use, indep
def run(rundirs, price, TOK):
    pin, pout, pcr = [p/1e6 for p in price]
    tot = saved = 0; nreq = nrem = 0
    for d in rundirs:
        for f in sorted(glob.glob(os.path.join(d, 'experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'))):
            try: r = per_task(f, TOK)
            except Exception: continue
            if not r: continue
            use, indep = r
            for u, ind in zip(use, indep):
                p = u['prompt_tokens']; c = (u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
                inp = (p-c)*pin + c*pcr; out = u['completion_tokens']*pout
                tot += inp+out; nreq += 1
                if ind: saved += inp; nrem += 1
    return tot, saved, nreq, nrem
if __name__ == '__main__':
    price = [float(x) for x in sys.argv[1].split(',')]
    for spec in sys.argv[2:]:
        dirs = spec.split(',')
        for name, TOK in (('strict(num>=3,word>=3)', mk(3,3)), ('loose(num>=1,word>=3)', mk(1,3))):
            tot, saved, n, nr = run(dirs, price, TOK)
            print(f"{spec:40s} {name:24s} requests={n} removable={nr} ({100*nr/n:.0f}%)  bill=${tot:.3f}  max saving=${saved:.3f} ({100*saved/tot:.0f}% of bill)")
