"""Counts-only analysis of R3 Part B runs (lead, AUTH-024). Reads runs/<tag>/{stats.json,evaluation.json,trace/calls.jsonl}; writes r3-b-<tag>-stats.json and a combined comparison. No AppWorld text is read."""
import json, sys, collections, pathlib
H = pathlib.Path(__file__).resolve().parent
tags = {"B1": "b1-all-tools", "B2": "b2-control", "B3": "b3-control-repeat"}
dev = json.load(open(sys.argv[1]))["task_ids"]
out = {}
for k, tag in tags.items():
    R = H / "runs" / tag
    st = json.load(open(R / "stats.json")); ev = json.load(open(R / "evaluation.json"))
    calls = [json.loads(l) for l in open(R / "trace/calls.jsonl")]
    by = collections.defaultdict(list)
    for c in calls: by[c["task"]].append(c)
    tasks = {}
    for tid in dev:
        cs = by[tid]; ok = [c for c in cs if c["status"] == "ok"]; s = st["tasks"][tid]
        passed = ev["individual"][tid]["success"]
        ftype = "passed" if passed else ("step_cap_reached" if s["steps"] >= 50 else "evaluation_failed")
        tasks[tid] = dict(passed=passed, failure_type=ftype, steps=s["steps"], seconds=s["seconds"], lm_calls_ok=len(ok), lm_calls_error=len(cs) - len(ok),
            predictor_calls=sum(c["predictor_call"] for c in ok), n_tools_first_agent_call=next((c["n_tools"] for c in ok if not c["predictor_call"]), None),
            prompt=sum(c["prompt"] for c in ok), cached=sum(c["cached"] for c in ok), cache_write=sum(c["cache_write"] or 0 for c in ok), completion=sum(c["completion"] for c in ok),
            cost=round(sum(c["cost"] for c in ok), 6), providers=sorted({c["provider"] for c in ok}),
            first_agent_call_cached=next((c["cached"] for c in ok if not c["predictor_call"]), None), first_agent_call_prompt=next((c["prompt"] for c in ok if not c["predictor_call"]), None))
    tot = {f: sum(t[f] for t in tasks.values()) for f in ("lm_calls_ok", "lm_calls_error", "predictor_calls", "prompt", "cached", "cache_write", "completion", "cost", "steps")}
    tot["cost"] = round(tot["cost"], 4)
    sc = {t for t, v in tasks.items() if v["failure_type"] == "step_cap_reached"}
    tot["passed"] = sum(v["passed"] for v in tasks.values()); tot["TGC"] = ev["aggregate"]["task_goal_completion"]; tot["SGC"] = ev["aggregate"]["scenario_goal_completion"]
    tot["failure_types"] = dict(collections.Counter(v["failure_type"] for v in tasks.values()))
    tot["without_step_capped"] = {f: sum(v[f] for t, v in tasks.items() if t not in sc) for f in ("prompt", "cached", "completion", "lm_calls_ok")} | {"cost": round(sum(v["cost"] for t, v in tasks.items() if t not in sc), 4), "tasks": 57 - len(sc)}
    tot["retried_or_errored_calls"] = tot["lm_calls_error"]; tot["providers_seen"] = sorted({p for v in tasks.values() for p in v["providers"]})
    tot["tasks_with_more_than_one_provider"] = sum(len(v["providers"]) > 1 for v in tasks.values())
    tot["cold_start_tasks"] = sum(1 for v in tasks.values() if v["first_agent_call_cached"] is not None and v["first_agent_call_cached"] < v["first_agent_call_prompt"] / 2)
    tot["system_fingerprints"] = sorted({str(c.get("system_fingerprint")) for c in calls if c["status"] == "ok"}); tot["served_models"] = sorted({str(c.get("model")) for c in calls if c["status"] == "ok"})
    tot["started"], tot["finished"] = st["started"], st["finished"]
    out[k] = dict(tag=tag, totals=tot, tasks=tasks)
    json.dump(out[k], open(H / f"r3-b-{k.lower()}-stats.json", "w"), indent=1)
    print(k, json.dumps(tot)[:1500])
def pas(k): return {t for t, v in out[k]["tasks"].items() if v["passed"]}
def diff(a, b): return sorted(pas(a) ^ pas(b)), sorted(pas(a) - pas(b)), sorted(pas(b) - pas(a))
cmp = {}
for a, b in (("B3", "B2"), ("B1", "B2"), ("B1", "B3")):
    x, a_only, b_only = diff(a, b)
    cmp[f"{a}_vs_{b}"] = dict(differ=x, passed_only_in_first=a_only, passed_only_in_second=b_only, n=len(x),
        failure_type_differs=sorted(t for t in dev if out[a]["tasks"][t]["failure_type"] != out[b]["tasks"][t]["failure_type"]))
    print(a, "vs", b, "pass/fail differs in", len(x), "tasks; passed only in", a, len(a_only), ", only in", b, len(b_only))
json.dump(cmp, open(H / "r3-b-comparison.json", "w"), indent=1)
print(json.dumps(cmp, indent=0)[:1800])
