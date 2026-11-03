# NOTE: local paths replaced by placeholders in this published copy.
"""R2 Part B1: counts only. Compares runs/minimax-m3-b1 (B1) with runs/minimax-m3 (Part 4) from their stats files and LM-call logs.
Writes only task ids, pass/fail, failure types and token counts."""
import json
import os
import statistics
import sys

PART4 = r"<local>/appworld-local/part4"
OUT = sys.argv[1]
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHON_DOTENV_DISABLED"] = "1"
os.environ["APPWORLD_CACHE"] = os.path.join(PART4, "cache")
os.environ["APPWORLD_ROOT"] = os.path.join(PART4, "root")
from appworld_agents.code.common.usage_tracker import Tokens

with open(os.path.join(PART4, "root", "data", "datasets", "dev.txt"), encoding="utf-8") as fh:
    DEV = [l.strip() for l in fh if l.strip()]
assert len(DEV) == 57


def load(tag):
    st = json.load(open(os.path.join(PART4, f"stats_{tag}.json"), encoding="utf-8"))
    rows = {r["task_id"]: r for r in st["tasks"]}
    exp = os.path.join(PART4, "runs", tag, "appworld_root", "experiments", "outputs", tag, "tasks")
    for tid in DEV:
        assert tid in rows
        calls = [json.loads(l) for l in open(os.path.join(exp, tid, "logs", "lm_calls.jsonl"), encoding="utf-8") if l.strip()]
        assert len(calls) == rows[tid]["llm_calls"]
        assert calls[0]["input"].get("tools") is None
        toks = [Tokens.from_response(c["output"]) for c in calls]
        rows[tid]["predictor_prompt"] = int(toks[0].input_cache_miss + toks[0].input_cache_hit)
        rows[tid]["predictor_completion"] = int(toks[0].output)
        rows[tid]["agent_prompt"] = rows[tid]["prompt_tokens"] - rows[tid]["predictor_prompt"]
        rows[tid]["agent_completion"] = rows[tid]["completion_tokens"] - rows[tid]["predictor_completion"]
        rows[tid]["functions_offered"] = len(calls[1]["input"]["tools"]) if len(calls) > 1 else None
        rows[tid]["model_id_served"] = {c["output"].get("model") for c in calls}
    return st, rows


def summ(rows):
    ids = DEV
    capped = [t for t in ids if rows[t]["failure_type"] == "step_cap_reached"]
    rest = [t for t in ids if t not in capped]
    s = lambda ts, k: sum(rows[t][k] for t in ts)
    def block(ts):
        return {"tasks": len(ts), "passed": sum(1 for t in ts if rows[t]["passed"]), "llm_calls": s(ts, "llm_calls"),
                "prompt_tokens": s(ts, "prompt_tokens"), "cached_prompt_tokens": s(ts, "cached_prompt_tokens"),
                "completion_tokens": s(ts, "completion_tokens"), "agent_prompt_tokens_without_predictor": s(ts, "agent_prompt"),
                "agent_completion_tokens_without_predictor": s(ts, "agent_completion")}
    return {"all": block(ids), "without_step_capped": block(rest), "step_capped_only": block(capped), "step_capped_ids": capped}


a_st, a = load("minimax-m3")
b_st, b = load("minimax-m3-b1")
flips = [t for t in DEV if a[t]["passed"] != b[t]["passed"]]
both_pass = sum(1 for t in DEV if a[t]["passed"] and b[t]["passed"])
both_fail = sum(1 for t in DEV if not a[t]["passed"] and not b[t]["passed"])


def paired(key):
    d = [b[t][key] - a[t][key] for t in DEV]
    return {"sum": sum(d), "median": statistics.median(d), "mean": round(statistics.fmean(d), 2), "min": min(d), "max": max(d),
            "tasks_b1_higher": sum(1 for x in d if x > 0), "tasks_b1_lower": sum(1 for x in d if x < 0), "tasks_equal": sum(1 for x in d if x == 0)}


def scen(rows):
    by = {}
    for t in DEV:
        by.setdefault(rows[t]["scenario_id"], []).append(rows[t]["passed"])
    return {k: all(v) for k, v in by.items()}


sa, sb = scen(a), scen(b)
out = {
    "note": "Counts only. 'part4' = the first MiniMaxAI/MiniMax-M3 run (tag minimax-m3); 'b1' = the repeat run (tag minimax-m3-b1).",
    "runs": {"part4": {"TGC": a_st["TGC"], "SGC": a_st["SGC"], "failure_type_counts": a_st["failure_type_counts"], "totals": a_st["totals"], **summ(a)},
             "b1": {"TGC": b_st["TGC"], "SGC": b_st["SGC"], "failure_type_counts": b_st["failure_type_counts"], "totals": b_st["totals"], **summ(b)}},
    "served_model_ids": {"part4": sorted({x for t in DEV for x in a[t]["model_id_served"]}), "b1": sorted({x for t in DEV for x in b[t]["model_id_served"]})},
    "flips": {
        "n_tasks_with_different_outcome": len(flips), "both_passed": both_pass, "both_failed": both_fail,
        "passed_in_part4_failed_in_b1": [t for t in flips if a[t]["passed"]],
        "failed_in_part4_passed_in_b1": [t for t in flips if b[t]["passed"]],
        "detail": [{"task_id": t, "part4": {"passed": a[t]["passed"], "failure_type": a[t]["failure_type"], "turns": a[t]["turns"]},
                    "b1": {"passed": b[t]["passed"], "failure_type": b[t]["failure_type"], "turns": b[t]["turns"]}} for t in flips],
    },
    "scenario_outcomes_differing": [k for k in sa if sa[k] != sb[k]],
    "paired_differences_b1_minus_part4_per_task": {k: paired(k) for k in ("turns", "llm_calls", "prompt_tokens", "completion_tokens", "predictor_prompt", "agent_prompt", "functions_offered")},
    "paired_difference_TGC_b1_minus_part4": round(b_st["TGC"] - a_st["TGC"], 6),
    "paired_difference_SGC_b1_minus_part4": round(b_st["SGC"] - a_st["SGC"], 6),
    "step_capped_same_tasks": sorted(set(summ(a)["step_capped_ids"]) & set(summ(b)["step_capped_ids"])),
    "tasks": [{"task_id": t, "scenario_id": a[t]["scenario_id"],
               "part4": {k: a[t][k] for k in ("passed", "failure_type", "turns", "llm_calls", "prompt_tokens", "cached_prompt_tokens", "completion_tokens", "predictor_prompt", "functions_offered")},
               "b1": {k: b[t][k] for k in ("passed", "failure_type", "turns", "llm_calls", "prompt_tokens", "cached_prompt_tokens", "completion_tokens", "predictor_prompt", "functions_offered")}} for t in DEV],
}
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
print("written", OUT)
