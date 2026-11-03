# NOTE: local paths replaced by placeholders in this published copy.
"""R3 Parts A1 (dev order, retries) and A4 (pilot bill per call and per provider). Counts, ids, provider names only; no model call.
Reads runs/or-b2-pilot and runs/or-ctrl-pilot (lm_calls.jsonl usage fields, console.log retry lines are only COUNTED)."""
import collections
import json
import os
import sys

P = r"<local>/appworld-local/part4"
OUT = sys.argv[1]
dev = [l.strip() for l in open(os.path.join(P, "root", "data", "datasets", "dev.txt"), encoding="utf-8") if l.strip()]
assert len(dev) == 57 and len(set(dev)) == 57
SUB = dev[0::6]
assert SUB == json.load(open(os.path.join(P, "r2_pilot_out.json"), encoding="utf-8"))["subset"]
json.dump({"note": "The 57 AppWorld dev task ids in the order of dev.txt (ids only). The OpenRouter pilot subset is dev[0::6] = indices 0, 6, ..., 54.",
           "n": 57, "task_ids": dev, "pilot_subset_indices": list(range(0, 57, 6)), "pilot_subset": SUB},
          open(os.path.join(OUT, "dev-order.json"), "w", encoding="utf-8"), indent=1)

res = {"note": "Counts only. Per call, in order: provider, prompt, cached and cache-write tokens, completion tokens, reported cost (USD).", "runs": {}}
for tag in ("or-b2-pilot", "or-ctrl-pilot"):
    base = os.path.join(P, "runs", tag)
    exp = os.path.join(base, "appworld_root", "experiments", "outputs", tag, "tasks")
    console = open(os.path.join(base, "console.log"), encoding="utf-8", errors="replace").read()
    retry_lines = sum(1 for line in console.splitlines() if "RETRY_ERROR" in line)
    run = {"retry_error_lines_in_console_log": retry_lines, "tasks": {}, "per_provider": {}}
    prov = collections.defaultdict(lambda: collections.Counter())
    prev_last_provider = None
    for t in SUB:
        calls = [json.loads(l) for l in open(os.path.join(exp, t, "logs", "lm_calls.jsonl"), encoding="utf-8") if l.strip()]
        rows = []
        for i, c in enumerate(calls):
            o = c["output"]
            u = o.get("usage") or {}
            d = u.get("prompt_tokens_details") or {}
            r = {"i": i, "predictor_call": c["input"].get("tools") is None, "provider": o.get("provider"), "prompt": u.get("prompt_tokens"),
                 "cached": d.get("cached_tokens"), "cache_write": d.get("cache_write_tokens"), "completion": u.get("completion_tokens"),
                 "cost": u.get("cost")}
            rows.append(r)
            pc = prov[r["provider"]]
            pc["calls"] += 1
            pc["prompt"] += r["prompt"] or 0
            pc["cached"] += r["cached"] or 0
            pc["cache_write"] += r["cache_write"] or 0
            pc["completion"] += r["completion"] or 0
            pc["cost_micro_usd"] += round((r["cost"] or 0) * 1e6)
        first_agent = next(r for r in rows if not r["predictor_call"])
        run["tasks"][t] = {
            "calls": rows,
            "first_agent_call": {"provider": first_agent["provider"], "prompt": first_agent["prompt"], "cached": first_agent["cached"],
                                 "cache_write": first_agent["cache_write"]},
            "provider_of_last_call_of_previous_task": prev_last_provider,
            "providers_seen": sorted({r["provider"] for r in rows}),
        }
        prev_last_provider = rows[-1]["provider"]
    for p, c in prov.items():
        run["per_provider"][p] = {k: (v if k != "cost_micro_usd" else round(v / 1e6, 6)) for k, v in c.items()}
        run["per_provider"][p]["cost_usd"] = run["per_provider"][p].pop("cost_micro_usd")
    run["totals"] = {k: sum(v[k] for v in run["per_provider"].values()) for k in ("calls", "prompt", "cached", "cache_write", "completion", "cost_usd")}
    run["totals"]["cost_usd"] = round(run["totals"]["cost_usd"], 6)
    res["runs"][tag] = run
json.dump(res, open(os.path.join(OUT, "r3-a4-pilot-bill-2026-11-02.json"), "w", encoding="utf-8"), indent=1)
for tag, run in res["runs"].items():
    print(tag, "retry lines", run["retry_error_lines_in_console_log"], "totals", run["totals"])
    for p, c in sorted(run["per_provider"].items(), key=lambda kv: -kv[1]["calls"]):
        print("   ", p, c)
    print("    first agent call (task: provider, cached/prompt, prev task last provider):")
    for t, v in run["tasks"].items():
        f = v["first_agent_call"]
        print("      ", t, f["provider"], f"{f['cached']}/{f['prompt']}", v["provider_of_last_call_of_previous_task"])
