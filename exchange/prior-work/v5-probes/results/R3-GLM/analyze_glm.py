"""Counts-only analysis of GLM-5.3 on ScaDS (AUTH-026, lead, 2026-11-08): B1 = all tools (runs/glm-b1-all-tools) against
B2 = predictor subset of at most 20 (runs/glm-b2-control: the 21 tasks finished before the laptop restart of 2026-11-07,
plus runs/glm-b2-control-rest: the other 36). Calls of the task cut off by the restart are left out; that task was rerun
from scratch in the second part. Descriptive only, no statistical test (INT-T-022). ScaDS bills nothing: the bill is
computed from the token counts and a stored price listing. AppWorld's own logs (lm_calls.jsonl) are read locally to check
which functions the predictor offered; only names of functions and counts are written out, no task text.
Usage: venv/bin/python analyze_glm.py <price listing json> <out.json> [MiniMax B2 run tags for the predictor comparison ...]"""
import collections, json, os, pathlib, re, statistics, sys
H = pathlib.Path(__file__).resolve().parent
dev = [l.strip() for l in open(H / "aw-root/data/datasets/dev.txt") if l.strip()]
PW = "supervisor__show_account_passwords"

def part(tag):
    R = H / "runs" / tag
    st = json.load(open(R / "stats.json"))
    ev = {t: bool(v["success"]) for t, v in json.load(open(R / "evaluation.json"))["individual"].items()}
    allcalls = [json.loads(l) for l in open(R / "trace/calls.jsonl")]
    fin = set(st["tasks"])
    excluded = collections.Counter(c["task"] for c in allcalls if c["task"] not in fin)
    return st, ev, [c for c in allcalls if c["task"] in fin], dict(excluded)

def offered(tag, t):
    """Functions offered on the first agent call, and whether the predictor's reply had any parseable 'app.api' line."""
    p = H / "runs" / tag / "experiments/outputs" / tag / "tasks" / t / "logs/lm_calls.jsonl"
    if not p.exists():
        return None, None
    L = [json.loads(l) for l in open(p)]
    agent = [x for x in L if isinstance(x.get("input"), dict) and x["input"].get("tools")]
    names = sorted(x["function"]["name"] for x in agent[0]["input"]["tools"]) if agent else []
    pred = [x for x in L if not (isinstance(x.get("input"), dict) and x["input"].get("tools"))]
    parse = None
    if pred:
        content = pred[0]["output"]["choices"][0]["message"].get("content") or ""
        parse = sum(bool(re.fullmatch(r"\s*[a-z_]+\.[a-z_0-9]+\s*", l)) for l in content.splitlines())
    return names, parse

def arm(tags, predictor):
    tasks, ev, calls, per, excl = {}, {}, [], {}, {}
    for tag in tags:
        st, e, c, x = part(tag)
        dup = set(st["tasks"]) & set(tasks)
        assert not dup, f"task in two parts: {dup}"
        tasks.update(st["tasks"]); ev.update(e); calls += c
        if x:
            excl[tag] = x
        for t, r in st["tasks"].items():
            tc = [k for k in c if k["task"] == t]
            row = {"part": tag, "passed": int(e.get(t, False)), "steps": r.get("steps"), "seconds": r.get("seconds"),
                   "lm_calls_ok": sum(k["status"] == "ok" for k in tc), "timeouts": sum(k.get("error") == "APITimeoutError" for k in tc),
                   "prompt": sum(k.get("prompt") or 0 for k in tc), "completion": sum(k.get("completion") or 0 for k in tc)}
            if predictor:
                names, parse = offered(tag, t)
                row.update(n_functions_offered=len(names), credentials_offered=int(PW in names), predictor_lines_parsed=parse)
            per[t] = row
    ok = [c for c in calls if c["status"] == "ok"]
    agent_ok = [c for c in ok if not c["predictor_call"]]
    sc = collections.defaultdict(list)
    for t in dev:
        sc[t.split("_")[0]].append(ev.get(t, False))
    tot = {"parts": tags, "tasks_finished": len(tasks), "tasks_evaluated": len(ev), "passed": sum(ev.values()),
           "TGC": round(100 * sum(ev.values()) / len(dev), 1), "SGC": round(100 * sum(all(v) for v in sc.values()) / len(sc), 1),
           "scenarios_fully_passed": sum(all(v) for v in sc.values()), "scenarios": len(sc),
           "lm_calls_ok": len(ok), "predictor_calls_ok": len(ok) - len(agent_ok), "lm_calls_error": len(calls) - len(ok),
           "errors_by_kind": dict(collections.Counter(c.get("error") for c in calls if c["status"] != "ok")),
           "prompt": sum(c["prompt"] for c in ok), "cached": sum(c["cached"] or 0 for c in ok), "cache_write": sum(c.get("cache_write") or 0 for c in ok),
           "completion": sum(c["completion"] for c in ok), "reasoning_tokens": sum(c.get("reasoning_tokens") or 0 for c in ok),
           "replies_with_reasoning": sum(bool(c.get("reasoning_chars")) for c in ok),
           "mean_prompt_per_ok_call": round(sum(c["prompt"] for c in ok) / len(ok)),
           "mean_functions_per_agent_call": round(sum(c["n_tools"] for c in agent_ok) / len(agent_ok), 1),
           "median_latency_s_ok_calls": round(statistics.median(c["latency_s"] for c in ok), 1),
           "served_model_ids": sorted({str(c.get("model")) for c in ok}), "system_fingerprints": sorted({str(c.get("system_fingerprint")) for c in ok}),
           "step_capped": sorted(t for t, r in tasks.items() if (r.get("steps") or 0) >= 50),
           "ended_within_3_steps": sorted(t for t, r in tasks.items() if (r.get("steps") or 99) <= 3),
           "tasks_with_timeouts": {t: r["timeouts"] for t, r in sorted(per.items()) if r["timeouts"]},
           "exceptions": {t: r["exception"] for t, r in tasks.items() if r.get("exception")},
           "agent_hours": round(sum(r.get("seconds") or 0 for r in tasks.values()) / 3600, 1),
           "excluded_calls_of_unfinished_tasks": excl}
    tot["uncached_prompt"] = tot["prompt"] - tot["cached"]
    tot["cached_share"] = round(tot["cached"] / tot["prompt"], 4)
    return ev, tot, per

def bills(listing, t1, t2):
    eps = json.load(open(listing))["response"]["data"]["endpoints"]
    rows = []
    for e in eps:
        p = e["pricing"]; pi, po = float(p["prompt"]), float(p["completion"]); pc = float(p.get("input_cache_read") or p["prompt"])
        f = lambda t: t["uncached_prompt"] * pi + t["cached"] * pc + t["completion"] * po
        g = lambda t: t["prompt"] * pi + t["completion"] * po
        rows.append({"endpoint": e.get("tag"), "usd_per_M_in": round(pi * 1e6, 4), "usd_per_M_cache_read": round(pc * 1e6, 4), "usd_per_M_out": round(po * 1e6, 4),
                     "B1_usd": round(f(t1), 2), "B2_usd": round(f(t2), 2), "ratio": round(f(t1) / f(t2), 2), "ratio_without_cache_price": round(g(t1) / g(t2), 2)})
    rs = [r["ratio"] for r in rows]; r0 = [r["ratio_without_cache_price"] for r in rows]
    return {"listing": pathlib.Path(listing).name, "endpoints": len(rows), "ratio_min": min(rs), "ratio_median": statistics.median(rs), "ratio_max": max(rs),
            "ratio_without_cache_price_min": min(r0), "ratio_without_cache_price_max": max(r0),
            "gmicloud_fp8": next((r for r in rows if r["endpoint"] == "gmicloud/fp8"), None), "per_endpoint": rows}

listing, outp, mm_tags = sys.argv[1], sys.argv[2], sys.argv[3:]
rest = sorted(p.name for p in (H / "runs").glob("glm-b2-control-rest*") if p.is_dir())
e1, t1, p1 = arm(["glm-b1-all-tools"], False)
e2, t2, p2 = arm(["glm-b2-control"] + rest, True)
r = lambda k: round(t1[k] / t2[k], 2) if t2[k] else None
cred = [t for t in dev if p2[t]["credentials_offered"]]; nocred = [t for t in dev if not p2[t]["credentials_offered"]]
pred = {"credentials_function": PW,
        "B2_tasks_credentials_offered": len(cred), "B2_passed_with_credentials_offered": sum(e2[t] for t in cred), "B1_passed_on_those_tasks": sum(e1[t] for t in cred),
        "B2_tasks_credentials_not_offered": len(nocred), "B2_passed_without_credentials_offered": sum(e2[t] for t in nocred), "B1_passed_on_the_tasks_without": sum(e1[t] for t in nocred),
        "B2_not_offered_and_ended_within_3_steps": sum((p2[t]["steps"] or 99) <= 3 for t in nocred),
        "B2_ended_within_3_steps_with_credentials_offered": sum((p2[t]["steps"] or 99) <= 3 for t in cred),
        "B2_predictor_replies_without_any_parseable_line": sorted(t for t in dev if p2[t]["predictor_lines_parsed"] == 0),
        "tasks_not_offered": sorted(nocred)}
mm = {}
for tag in mm_tags:
    st = json.load(open(H / "runs" / tag / "stats.json"))["tasks"]
    ev = {t: bool(v["success"]) for t, v in json.load(open(H / "runs" / tag / "evaluation.json"))["individual"].items()}
    o = {t: PW in (offered(tag, t)[0] or []) for t in st}
    mm[tag] = {"tasks": len(o), "credentials_offered": sum(o.values()), "passed_with": sum(ev[t] for t in o if o[t]), "passed_without": sum(ev[t] for t in o if not o[t])}
pred["MiniMax_M3_B2_runs_for_comparison"] = mm
out = {"note": "Counts only; descriptive, no test (INT-T-022). GLM-5.3 on ScaDS (vLLM), reasoning as served (on by default), temperature 0, seed 100, step cap 50, client timeout 300 s with the client's own 2 retries (so a timed-out request is about 900 s), up to 20 AppWorld retries 15 s apart. ScaDS bills nothing; the bill is computed.",
       "B1_all_tools": t1, "B2_control": t2, "dev_tasks_missing": {"B1": [t for t in dev if t not in e1], "B2": [t for t in dev if t not in e2]},
       "ratios_B1_over_B2": {k: r(k) for k in ["prompt", "uncached_prompt", "cached", "completion", "reasoning_tokens", "lm_calls_ok", "mean_prompt_per_ok_call"]},
       "bill_computed": bills(listing, t1, t2),
       "tasks_with_different_result": sum(e1.get(t, False) != e2.get(t, False) for t in dev),
       "B1_only_passed": sorted(t for t in dev if e1.get(t) and not e2.get(t)),
       "B2_only_passed": sorted(t for t in dev if e2.get(t) and not e1.get(t)),
       "both_passed": sum(e1.get(t, False) and e2.get(t, False) for t in dev), "both_failed": sum(not e1.get(t, False) and not e2.get(t, False) for t in dev),
       "predictor_check": pred,
       "per_task": {t: {"B1": p1[t], "B2": p2[t]} for t in dev}}
pathlib.Path(outp).write_text(json.dumps(out, indent=1))
show = {k: v for k, v in out.items() if k not in ("per_task",)}
show["bill_computed"] = {k: v for k, v in out["bill_computed"].items() if k != "per_endpoint"}
print(json.dumps(show, indent=1))
