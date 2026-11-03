# NOTE: local paths replaced by placeholders in this published copy.
"""R2 Parts A4 and A5: counts only, from the Part 4 files on disk (no model call, no AppWorld environment started).
Reads runs/<tag>/.../tasks/<id>/logs/lm_calls.jsonl and the dev ground truth (required_apis). Writes only counts, ids and lengths.
Dev only: a non-dev task id aborts before anything is read.
"""
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

from appworld.common.path_store import path_store
from appworld.task import Task
from appworld_agents.code.common.usage_tracker import Tokens

with open(os.path.join(PART4, "root", "data", "datasets", "dev.txt"), encoding="utf-8") as fh:
    DEV = [l.strip() for l in fh if l.strip()]
assert len(DEV) == 57, len(DEV)


def dist(v):
    v = sorted(v)
    if not v:
        return None
    k = (len(v) - 1) * 0.9
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return {"n": len(v), "min": v[0], "median": statistics.median(v), "mean": round(statistics.fmean(v), 2),
            "p90": round(v[f] + (v[c] - v[f]) * (k - f), 2), "max": v[-1]}


# ---------------- ground truth: required APIs per dev task ----------------
required = {}
req_in_gt = {}
for tid in DEV:
    t = Task.load(tid, load_ground_truth=True, ground_truth_mode="full")
    assert tid in DEV
    required[tid] = [a.lower() for a in t.ground_truth.required_apis]
    req_in_gt[tid] = len(required[tid])

# ---------------- A5: API predictor modes and what "all" offers ----------------
t0 = Task.load(DEV[0], load_ground_truth=False)
apis_by_app = {app: len(docs) for app, docs in t0.api_docs.items()}
fc = t0.api_docs.function_calling()
a5 = {
    "modes_accepted": ["ground_truth", "predicted", "all"],
    "apps_in_api_docs": sorted(apis_by_app),
    "api_count_by_app": apis_by_app,
    "api_count_excluding_api_docs_app": sum(n for app, n in apis_by_app.items() if app != "api_docs"),
    "api_count_including_api_docs_app": sum(apis_by_app.values()),
    "function_calling_definitions_returned_by_api_docs.function_calling()": len(fc),
    "function_calling_names_with_prefix_api_docs__": sum(1 for d in fc if d["function"]["name"].startswith("api_docs__")),
}

# ---------------- A4 per model ----------------
result = {"a5": a5, "models": {}}
for tag in ("minimax-m3", "deepseek-v41-flash"):
    exp = os.path.join(PART4, "runs", tag, "appworld_root", "experiments", "outputs", tag, "tasks")
    stats = json.load(open(os.path.join(PART4, f"stats_{tag}.json"), encoding="utf-8"))
    st = {r["task_id"]: r for r in stats["tasks"]}
    rows = []
    for tid in DEV:
        assert tid in DEV
        calls = []
        with open(os.path.join(exp, tid, "logs", "lm_calls.jsonl"), encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    calls.append(json.loads(line))
        pairs = []
        for c in calls:
            tk = Tokens.from_response(c["output"])
            pairs.append({"prompt": int(tk.input_cache_miss + tk.input_cache_hit), "cached": int(tk.input_cache_hit),
                          "completion": int(tk.output), "tools_declared": None if c["input"].get("tools") is None else len(c["input"]["tools"])})
        assert len(calls) == st[tid]["llm_calls"], (tid, len(calls), st[tid]["llm_calls"])
        assert calls[0]["input"].get("tools") is None, "first call is expected to be the API predictor (no tools)"
        pred = pairs[0]
        agent = pairs[1:]
        offered = None
        found = None
        all_found = None
        n_req = len(required[tid])
        if len(calls) > 1:
            names = [d["function"]["name"].lower().replace("__", ".", 1) for d in calls[1]["input"]["tools"]]
            offered = len(names)
            found = sum(1 for r in required[tid] if r in set(names))
            all_found = found == n_req
        rows.append({
            "task_id": tid, "passed": st[tid]["passed"], "failure_type": st[tid]["failure_type"],
            "predictor_prompt": pred["prompt"], "predictor_cached": pred["cached"], "predictor_completion": pred["completion"],
            "functions_offered_to_agent": offered, "required_apis": n_req, "required_apis_among_offered": found,
            "all_required_among_offered": all_found,
            "agent_turns": len(agent),
            "agent_prompt": sum(p["prompt"] for p in agent), "agent_cached": sum(p["cached"] for p in agent),
            "agent_completion": sum(p["completion"] for p in agent),
            "per_call_prompt_cached": [[p["prompt"], p["cached"]] for p in pairs],
        })
    ran = rows
    tot = lambda k: sum(r[k] for r in ran)
    capped = [r for r in ran if r["failure_type"] == "step_cap_reached"]
    ntot = lambda rs, k: sum(r[k] for r in rs)
    result["models"][tag] = {
        "model": stats["model"],
        "note": "per_call_prompt_cached lists one [prompt, cached] pair per LM call in order; entry 0 is the API-predictor call (no tools declared).",
        "totals_without_predictor": {
            "tasks": len(ran), "passed": sum(1 for r in ran if r["passed"]),
            "agent_llm_calls": tot("agent_turns"), "prompt_tokens": tot("agent_prompt"), "cached_prompt_tokens": tot("agent_cached"),
            "completion_tokens": tot("agent_completion"),
        },
        "totals_predictor_only": {
            "calls": len(ran), "prompt_tokens": tot("predictor_prompt"), "cached_prompt_tokens": tot("predictor_cached"),
            "completion_tokens": tot("predictor_completion"),
        },
        "distributions_without_predictor": {
            "turns": dist([r["agent_turns"] for r in ran]), "prompt_tokens": dist([r["agent_prompt"] for r in ran]),
            "completion_tokens": dist([r["agent_completion"] for r in ran]),
        },
        "distributions_predictor": {
            "prompt_tokens": dist([r["predictor_prompt"] for r in ran]), "cached_prompt_tokens": dist([r["predictor_cached"] for r in ran]),
            "completion_tokens": dist([r["predictor_completion"] for r in ran]),
            "functions_offered": dist([r["functions_offered_to_agent"] for r in ran if r["functions_offered_to_agent"] is not None]),
        },
        "required_apis": {
            "tasks_with_all_required_among_offered": sum(1 for r in ran if r["all_required_among_offered"]),
            "tasks_with_all_required_among_offered_and_passed": sum(1 for r in ran if r["all_required_among_offered"] and r["passed"]),
            "tasks_not_all_required_among_offered_and_passed": sum(1 for r in ran if not r["all_required_among_offered"] and r["passed"]),
            "required_apis_total": tot("required_apis"), "required_apis_among_offered_total": tot("required_apis_among_offered"),
            "required_apis_per_task": dist([r["required_apis"] for r in ran]),
        },
        "step_capped_tasks": {
            "n": len(capped), "task_ids": [r["task_id"] for r in capped],
            "prompt_tokens_incl_predictor": sum(r["predictor_prompt"] + r["agent_prompt"] for r in capped),
            "prompt_tokens_all_tasks_incl_predictor": sum(r["predictor_prompt"] + r["agent_prompt"] for r in ran),
            "prompt_tokens_without_predictor_in_capped": ntot(capped, "agent_prompt"),
        },
        "totals_without_predictor_and_without_capped_tasks": {
            "tasks": len(ran) - len(capped), "passed": sum(1 for r in ran if r["passed"] and r not in capped),
            "agent_llm_calls": ntot([r for r in ran if r not in capped], "agent_turns"),
            "prompt_tokens": ntot([r for r in ran if r not in capped], "agent_prompt"),
            "completion_tokens": ntot([r for r in ran if r not in capped], "agent_completion"),
        },
        "tasks": rows,
    }
json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1)
print("written", OUT)
