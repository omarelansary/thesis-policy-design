#!/usr/bin/env python
"""R3 Part B diagnosis (lead, AUTH-024, 2026-11-06). No model call. Counts only: reads the local AppWorld logs of B1-B3 (task text is
not copied), the counts-only traces, and the Windows-side reference files already in the repository (Part 4, ScaDS repeat, pilot, probes).
Usage: python diagnose_partb.py <repo>/exchange/prior-work/v5-probes/results <out.json>"""
import collections, glob, json, os, pathlib, statistics as st, sys

RES = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
HERE = pathlib.Path(__file__).resolve().parent
RUNS = {"B1": "b1-all-tools", "B2": "b2-control", "B3": "b3-control-repeat"}
out = {"note": "Counts only; no task text, no model output. Produced by diagnose_partb.py; inputs are the local AppWorld logs of B1-B3 and the Windows-side files in v5-probes/results."}

# 1. reasoning in the replies of B1-B3 (AppWorld's own lm_calls.jsonl per task)
rs = {}
for k, tag in RUNS.items():
    c = collections.Counter()
    for f in glob.glob(str(HERE / f"runs/{tag}/experiments/outputs/{tag}/tasks/*/logs/lm_calls.jsonl")):
        for line in open(f):
            o = json.loads(line)["output"]
            if not o.get("choices"):
                continue
            m = o["choices"][0]["message"]
            u = o.get("usage") or {}
            c["replies"] += 1
            c["reasoning_field_nonempty"] += bool(m.get("reasoning"))
            c["reasoning_content_nonempty"] += bool(m.get("reasoning_content"))
            c["reasoning_details_nonempty"] += bool(m.get("reasoning_details"))
            c["think_tag_in_content"] += "<think" in (m.get("content") or "")
            c["reasoning_tokens_sum"] += (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
            c["completion_tokens_sum"] += u.get("completion_tokens") or 0
    rs[k] = dict(c)
out["reasoning_in_replies"] = rs

# 2. completion tokens per LM call, per task (median over tasks): ScaDS (Part 4, its repeat) vs GMICloud (B1-B3)
def per_task_ratio(pairs):
    r = [c / n for c, n in pairs if n]
    return {"tasks": len(r), "median_completion_per_call": round(st.median(r), 1), "mean_completion_per_call": round(st.mean(r), 1)}
p4 = json.load(open(RES / "r1-part4-stats-minimax-m3-2026-11-01.json"))["tasks"]
sb1 = json.load(open(RES / "R2/r2-b1-stats-minimax-m3-b1-2026-11-02.json"))["tasks"]
cpc = {"part4_scads": per_task_ratio([(t["completion_tokens"], t["llm_calls"]) for t in p4]),
       "repeat_scads": per_task_ratio([(t["completion_tokens"], t["llm_calls"]) for t in sb1])}
for k, tag in RUNS.items():
    d = collections.defaultdict(lambda: [0, 0])
    for line in open(HERE / f"runs/{tag}/trace/calls.jsonl"):
        c = json.loads(line)
        if c["status"] == "ok":
            d[c["task"]][0] += c["completion"]; d[c["task"]][1] += 1
    cpc[k + "_gmicloud"] = per_task_ratio(d.values())
out["completion_tokens_per_call"] = cpc

# 3. the same probe cells on ScaDS (R1, R2) and on GMICloud (R3 A3): completion tokens and visible text length per reply
probe = {}
for name, f in [("scads_r1", "raw/r1-scads-MiniMaxAI__MiniMax-M3-2026-11-01.json"), ("scads_r2", "R2/raw/r2-scads-MiniMaxAI__MiniMax-M3-2026-11-02.json"),
                ("gmicloud_r3a3", "R3/r3-openrouter-gmicloud-2026-11-02.json")]:
    d = json.load(open(RES / f)); rows = next(iter(d["models"].values())); by = collections.defaultdict(list)
    for r in rows:
        if r["status"] == 200 and r["usage"]:
            by[r["cell"]].append({"completion": r["usage"]["completion"], "text_len": (r.get("meta") or {}).get("text_len"),
                                  "output_types": (r.get("meta") or {}).get("output_types"), "tools_called": r["tools_called"]})
    probe[name] = {"probe": d.get("probe"), "cells": dict(by)}
out["probe_cells"] = probe

# 4. API predictor coverage in B2/B3: are all required (non-supervisor) APIs of the task among the functions offered?
ev = {k: json.load(open(HERE / f"runs/{tag}/evaluation.json"))["individual"] for k, tag in RUNS.items()}
cov = {}
for k in ("B2", "B3"):
    tag = RUNS[k]; cnt = collections.Counter()
    for f in glob.glob(str(HERE / f"runs/{tag}/experiments/outputs/{tag}/tasks/*/logs/lm_calls.jsonl")):
        t = f.split(os.sep)[-3]
        agent = [x for x in map(json.loads, open(f)) if x["input"].get("tools")]
        offered = {tl["function"]["name"].replace("__", ".") for tl in agent[0]["input"]["tools"]} if agent else set()
        req = {r for r in json.load(open(HERE / f"aw-root/data/tasks/{t}/ground_truth/required_apis.json")) if not r.startswith("supervisor.")}
        cnt[("all_required_offered" if req <= offered else "some_required_missing") + ("_passed" if ev[k][t]["success"] else "_failed")] += 1
    cov[k] = dict(cnt)
out["predictor_coverage"] = cov

# 5. the 10 pilot tasks (dev[0::6]) in every run
pil = json.load(open(RES / "R2/r2-pilot-openrouter-2026-11-02.json"))
sub = pil["subset"]
tab = {r: sum(bool(pil["runs"][r]["per_task"][t]["passed"]) for t in sub) for r in pil["runs"]}
for k in RUNS:
    tab["linux_" + k] = sum(bool(ev[k][t]["success"]) for t in sub)
out["pilot_subset_passed_of_10"] = tab
OUT.write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("reasoning_in_replies", "completion_tokens_per_call", "predictor_coverage", "pilot_subset_passed_of_10")}, indent=1))
