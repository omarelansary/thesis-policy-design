# NOTE: local paths replaced by placeholders in this published copy.
"""R2 OpenRouter pilot: counts only. Compares or-b2-pilot (predictor off, all APIs) and or-ctrl-pilot (predictor on) with the two ScaDS MiniMax-M3 runs (minimax-m3, minimax-m3-b1) on the same 10 dev tasks.
Writes task ids, pass/fail, failure types, token counts, cost reported by the endpoint, provider names."""
import json, os, sys, statistics
P = r"<local>/appworld-local/part4"
OUT = sys.argv[1]
SUB = ["50e1ac9_1","530b157_1","b119b1f_1","0d8a4ee_1","3ab5b8b_1","383cbac_1","57c3486_1","6bdbc26_1","6c2c621_1","4fab96f_1"]
dev = [l.strip() for l in open(os.path.join(P, "root", "data", "datasets", "dev.txt"), encoding="utf-8") if l.strip()]
assert all(t in dev for t in SUB) and SUB == dev[0::6] and len(SUB) == 10

def load(tag):
    st = json.load(open(os.path.join(P, f"stats_{tag}.json"), encoding="utf-8"))
    rows = {r["task_id"]: r for r in st["tasks"]}
    exp = os.path.join(P, "runs", tag, "appworld_root", "experiments", "outputs", tag, "tasks")
    extra = {}
    for t in SUB:
        calls = [json.loads(l) for l in open(os.path.join(exp, t, "logs", "lm_calls.jsonl"), encoding="utf-8") if l.strip()]
        assert len(calls) == rows[t]["llm_calls"], (tag, t)
        us = [(c["output"].get("usage") or {}) for c in calls]
        tools = [len(c["input"].get("tools") or []) for c in calls]
        extra[t] = {
            "cost": round(sum(u.get("cost", 0) or 0 for u in us), 6) if any("cost" in u for u in us) else None,
            "providers": sorted({str(c["output"].get("provider")) for c in calls}),
            "tools_first_agent_call": next((n for n in tools if n), None),
            "predictor_call_present": calls[0]["input"].get("tools") is None,
        }
    return st, rows, extra

runs = {}
for key, tag in (("or_b2_pilot", "or-b2-pilot"), ("or_control", "or-ctrl-pilot"), ("scads_part4", "minimax-m3"), ("scads_b1", "minimax-m3-b1")):
    st, rows, extra = load(tag)
    sub = {t: rows[t] for t in SUB}
    cap = [t for t in SUB if sub[t]["failure_type"] == "step_cap_reached"]
    tot = lambda k: sum(sub[t][k] for t in SUB)
    runs[key] = {
        "tag": tag, "model": st["model"], "tasks": 10, "passed": sum(1 for t in SUB if sub[t]["passed"]),
        "passed_ids": [t for t in SUB if sub[t]["passed"]], "failed": {t: sub[t]["failure_type"] for t in SUB if not sub[t]["passed"]},
        "llm_calls": tot("llm_calls"), "turns": tot("turns"), "prompt_tokens": tot("prompt_tokens"),
        "cached_prompt_tokens": tot("cached_prompt_tokens"), "completion_tokens": tot("completion_tokens"),
        "step_capped": cap,
        "cost_reported_usd": round(sum(e["cost"] for e in extra.values()), 4) if all(e["cost"] is not None for e in extra.values()) else None,
        "providers": sorted({p for e in extra.values() for p in e["providers"]}),
        "functions_offered_first_agent_call": sorted({e["tools_first_agent_call"] for e in extra.values()}),
        "per_task": {t: {"passed": sub[t]["passed"], "failure_type": sub[t]["failure_type"], "turns": sub[t]["turns"], "llm_calls": sub[t]["llm_calls"],
                         "prompt_tokens": sub[t]["prompt_tokens"], "cached_prompt_tokens": sub[t]["cached_prompt_tokens"],
                         "completion_tokens": sub[t]["completion_tokens"], "cost_usd": extra[t]["cost"], "functions_offered": extra[t]["tools_first_agent_call"]} for t in SUB},
    }
    runs[key]["_ok_predictor_flag"] = sorted({e["predictor_call_present"] for e in extra.values()})
json.dump({"note": "Counts only. Subset = every 6th dev task from #1 (rule fixed before any outcome was read).", "subset": SUB, "runs": runs}, open(OUT, "w", encoding="utf-8"), indent=1)
for k, r in runs.items():
    print(k, "passed", r["passed"], "/10 failed", r["failed"], "calls", r["llm_calls"], "prompt", r["prompt_tokens"], "cached", r["cached_prompt_tokens"],
          "compl", r["completion_tokens"], "cost", r["cost_reported_usd"], "providers", r["providers"], "fns", r["functions_offered_first_agent_call"], "capped", r["step_capped"], "predictor_first", r["_ok_predictor_flag"])
