#!/usr/bin/env python3
"""Read-only audit of AppWorld ReAct traces (R3 runs). Usage: python3 -I trace_audit.py RUNDIR... [--json OUT]
Measures batching of tool calls per request, tool-result sizes, prefix-vs-history share of prompt tokens,
and a crude data-dependency proxy between consecutive steps. Reads only; never reads .env."""
import json, re, sys, glob, os, statistics as st
TOK = re.compile(r'[A-Za-z0-9_@.\-]{3,}')
def toks(s): return set(TOK.findall(s)) if s else set()
def msg_text(m):
    c = m.get('content')
    if isinstance(c, list): c = ' '.join(x.get('text', '') for x in c if isinstance(x, dict))
    return c or ''
def analyse_task(path):
    rows = [json.loads(l) for l in open(path)]
    if not rows: return None
    usage = [r['output']['usage'] for r in rows]
    msgs = list(rows[-1]['input']['messages']) + [rows[-1]['output']['choices'][0]['message']]
    steps, i = [], 0
    while i < len(msgs):
        m = msgs[i]
        if m['role'] == 'assistant':
            tcs = m.get('tool_calls') or []
            res, j = [], i + 1
            while j < len(msgs) and msgs[j]['role'] == 'tool':
                res.append(msg_text(msgs[j])); j += 1
            steps.append({'n_calls': len(tcs), 'args': [t['function']['arguments'] for t in tcs],
                          'names': [t['function']['name'] for t in tcs], 'res': res})
            i = j
        else: i += 1
    nreal = len(rows)
    first_real = len(steps) - nreal
    # message index where first real assistant step starts
    idx, cnt, i2 = 0, 0, 0
    starts = []
    while i2 < len(msgs):
        if msgs[i2]['role'] == 'assistant':
            starts.append(i2)
            j2 = i2 + 1
            while j2 < len(msgs) and msgs[j2]['role'] == 'tool': j2 += 1
            i2 = j2
        else: i2 += 1
    known = toks(' '.join(msg_text(m) for m in msgs[:starts[first_real]])) if first_real >= 0 else set()
    steps = steps[first_real:] if first_real >= 0 else steps
    dep, prev_res, kbp = [], set(), set()
    for k, s in enumerate(steps):
        a = set().union(*[toks(x) for x in s['args']]) if s['args'] else set()
        if k > 0 and s['n_calls'] > 0: dep.append(bool(a & (prev_res - kbp)))
        kbp = set(known); known |= a
        prev_res = set().union(*[toks(r) for r in s['res']]) if s['res'] else set()
        known |= prev_res
    return {'lm_calls': len(rows), 'prompt': [u['prompt_tokens'] for u in usage],
            'cached': [((u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0) for u in usage],
            'completion': [u['completion_tokens'] for u in usage],
            'n_tool_calls_per_step': [s['n_calls'] for s in steps],
            'res_chars_per_step': [sum(len(r) for r in s['res']) for s in steps], 'dep_on_prev': dep,
            'growth': [usage[k+1]['prompt_tokens']-usage[k]['prompt_tokens'] for k in range(len(usage)-1)]}
def summarize(rundir):
    T = []
    for f in sorted(glob.glob(os.path.join(rundir, 'experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'))):
        try: r = analyse_task(f)
        except Exception as e: print('  skip', f.split('/')[-3], repr(e)[:80]); continue
        if r: r['task'] = f.split('/')[-3]; T.append(r)
    if not T: return None
    N = [t['lm_calls'] for t in T]; sw = [n for t in T for n in t['n_tool_calls_per_step'] if n > 0]
    tot = sum(N); sp = sum(sum(t['prompt']) for t in T); sf = sum(t['prompt'][0]*len(t['prompt']) for t in T)
    dt = dc = 0
    for t in T:
        for k in range(len(t['prompt'])-1):
            dt += t['prompt'][k+1]-t['prompt'][k]; dc += t['res_chars_per_step'][k]
    tpc = dt/dc if dc else float('nan')
    deps = [d for t in T for d in t['dep_on_prev']]
    rt = sorted(g for t in T for g in t['growth'])
    return {'run': os.path.basename(rundir.rstrip('/')), 'tasks': len(T), 'requests': tot,
        'requests_per_task_median': st.median(N), 'requests_per_task_mean': round(tot/len(T), 2),
        'tool_calls_per_request': round(sum(sw)/max(1, len(sw)), 2),
        'share_requests_with_ge2_tool_calls': round(sum(1 for n in sw if n >= 2)/max(1, len(sw)), 3),
        'median_first_prompt': int(st.median(t['prompt'][0] for t in T)), 'mean_prompt_per_request': int(sp/tot),
        'history_growth_share_of_prompt_tokens': round(1-sf/sp, 3),
        'cached_share_of_prompt': round(sum(sum(t['cached']) for t in T)/sp, 3),
        'tokens_per_result_char': round(tpc, 3),
        'share_steps_data_dependent_on_prev': round(sum(deps)/max(1, len(deps)), 3), 'step_pairs': len(deps),
        'median_growth_tokens_per_step': int(rt[len(rt)//2]) if rt else None,
        'p90_growth_tokens_per_step': int(rt[int(0.9*len(rt))]) if rt else None,
        'share_steps_growth_gt_1k': round(sum(1 for x in rt if x > 1000)/max(1, len(rt)), 3),
        'share_steps_growth_gt_2k': round(sum(1 for x in rt if x > 2000)/max(1, len(rt)), 3)}
if __name__ == '__main__':
    a = sys.argv[1:]; out = None
    if '--json' in a: k = a.index('--json'); out = a[k+1]; del a[k:k+2]
    res = []
    for d in a:
        r = summarize(d)
        if r: print(json.dumps(r)); res.append(r)
    if out: json.dump(res, open(out, 'w'), indent=1)
