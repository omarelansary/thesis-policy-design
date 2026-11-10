"""P4 step A (AUTH-033, 2026-11-10): replay of client-side tool-result clearing on the logged P2 sessions; no model request.
Rule: Anthropic's clear_tool_uses (stored source evidence/literature-20261019/v5-anthropic-context-editing-20261022.md, lines
38-40 and 1724-1732): when a request's input exceeds TRIGGER tokens, the oldest tool results are replaced by a placeholder,
keeping the last KEEP; the clearing happens only if it removes at least CLEAR_AT_LEAST tokens. Settings: the vendor's defaults
(100,000 / 3 / none) and its documented example (30,000 / 3 / 5,000). Cleared results stay cleared.
Bill (counterfactual, same model behaviour assumed): for each request, prompt' = prompt - tokens cleared so far; cached' = cached
- tokens cleared so far, except on a request where new clearing happens: then only the part before the first newly cleared
message stays cached (the rest is written again). Output tokens unchanged. Tool-result text is tokenized with o200k_base.
Upper-bound caveats: the model's later behaviour (and accuracy) may change; this replays only the bill.
Usage: ~/r3-work/venv/bin/python -I design/package-v5/tools/p4_replay.py design/package-v5/inputs/p2/local/runs
"""
import collections, glob, gzip, json, os, sys
import tiktoken

enc = tiktoken.get_encoding("o200k_base")
tok = lambda s: len(enc.encode(s or ""))
PH = "[tool result cleared]"
PRICES = {"gpt-5-mini": (0.25, 0.025, 2.0), "gpt-5.4-mini": (0.75, 0.075, 4.5), "glm-5.3": (0.70, 0.13, 2.2)}
SETTINGS = [("vendor default", 100000, 3, 0), ("vendor example", 30000, 3, 5000)]
root = sys.argv[1]


def opener(p):
    return gzip.open(p, "rt") if p.endswith(".gz") else open(p)


out = collections.defaultdict(lambda: collections.defaultdict(float))
for run in sorted(glob.glob(f"{root}/p2-main-*") + glob.glob(f"{root}/p2b-or-*")):
    model = next(m for m in PRICES if f"-{m}-" in os.path.basename(run))
    pin, pc, po = PRICES[model]
    tr = collections.defaultdict(list)
    for l in open(f"{run}/trace/calls.jsonl"):
        r = json.loads(l)
        if r["status"] == "ok":
            tr[r["task"]].append(r)
    for task, calls in tr.items():
        f = glob.glob(f"{run}/experiments/outputs/*/tasks/{task}/logs/lm_calls.jsonl*")
        if not f:
            continue
        L = [json.loads(l) for l in opener(f[0])]
        if len(L) != len(calls):
            continue
        for name, trig, keep, least in SETTINGS:
            key = (model, name)
            cleared = set(); xcum = 0; base = new = 0.0; fired = 0
            for c, r in zip(L, calls):
                msgs = c["input"]["messages"]
                tool_idx = [i for i, m in enumerate(msgs) if m.get("role") == "tool"]
                first_new = None
                if r["prompt"] - xcum > trig:
                    cand = [i for i in tool_idx[:-keep] if i not in cleared] if keep else [i for i in tool_idx if i not in cleared]
                    x = sum(tok(msgs[i].get("content")) - tok(PH) for i in cand)
                    if cand and x >= max(least, 1):
                        cleared |= set(cand); xcum += x; fired += 1; first_new = min(cand)
                p2 = r["prompt"] - xcum
                if first_new is not None:
                    tail = sum(tok(json.dumps(m)) for m in msgs[first_new:])
                    c2 = max(0, min(r["cached"], p2 - tail))
                else:
                    c2 = max(0, r["cached"] - xcum)
                base += (r["prompt"] - r["cached"]) * pin + r["cached"] * pc + r["completion"] * po
                new += (p2 - c2) * pin + c2 * pc + r["completion"] * po
            o = out[key]
            o["task_runs"] += 1; o["fired_runs"] += fired > 0; o["base"] += base / 1e6; o["new"] += new / 1e6; o["tokens_cleared"] += xcum
for (model, name), o in sorted(out.items()):
    print(f"{model:13} {name:15} task-runs {int(o['task_runs'])}, clearing fired in {int(o['fired_runs'])}, tokens cleared {int(o['tokens_cleared'])}, "
          f"bill ${o['base']:.3f} -> ${o['new']:.3f} ({(o['new'] / o['base'] - 1) * 100:+.1f}%)")
