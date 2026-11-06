"""Counts-only analysis of AUTH-025 (lead, 2026-11-06): B1 and B2 again with reasoning on (gmicloud/fp8), the 10-task control with reasoning
(stage 2), compared with B1-B3 without reasoning (AUTH-024) and with Part 4 / its repeat on ScaDS (Windows files in the repository).
B1 with reasoning ran in two parts: b1r-all-tools-reasoning (tasks 1-12 finished; task 13 onward refused by an OpenRouter key limit, so
discarded) and b1r2-all-tools-reasoning-rest (the other 45 tasks, task 13 from scratch). No AppWorld text is read.
Usage: python analyze_stage3.py <repo>/exchange/prior-work/v5-probes/results <out.json>"""
import collections, json, pathlib, sys

H = pathlib.Path(__file__).resolve().parent
RES = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
dev = [l.strip() for l in open(H / "aw-root/data/datasets/dev.txt") if l.strip()]

def load(tag, evfile="evaluation.json", only=None):
    R = H / "runs" / tag
    st = json.load(open(R / "stats.json")); ev = json.load(open(R / evfile))["individual"]
    calls = [json.loads(l) for l in open(R / "trace/calls.jsonl")]
    by = collections.defaultdict(list)
    for c in calls:
        by[c["task"]].append(c)
    tasks = {}
    for tid, s in st["tasks"].items():
        if only is not None and tid not in only:
            continue
        ok = [c for c in by[tid] if c["status"] == "ok"]
        passed = bool(ev[tid]["success"])
        tasks[tid] = dict(passed=passed, failure_type="passed" if passed else ("step_cap_reached" if s["steps"] >= 50 else "evaluation_failed"),
                          steps=s["steps"], lm_calls_ok=len(ok), lm_calls_error=len(by[tid]) - len(ok),
                          prompt=sum(c["prompt"] for c in ok), cached=sum(c["cached"] for c in ok), completion=sum(c["completion"] for c in ok),
                          reasoning_tokens=sum(c.get("reasoning_tokens") or 0 for c in ok), replies_with_reasoning=sum(bool(c.get("reasoning_chars")) for c in ok),
                          cost=round(sum(c["cost"] for c in ok), 6), providers=sorted({c["provider"] for c in ok}))
    run_cost = round(sum(c.get("cost") or 0 for c in calls), 6)
    return tasks, run_cost

def totals(tasks, ids):
    t = {f: sum(tasks[i][f] for i in ids) for f in ("lm_calls_ok", "lm_calls_error", "prompt", "cached", "completion", "reasoning_tokens", "replies_with_reasoning", "steps")}
    t["cost"] = round(sum(tasks[i]["cost"] for i in ids), 4)
    t["tasks"] = len(ids); t["passed"] = sum(tasks[i]["passed"] for i in ids)
    t["TGC"] = round(100 * t["passed"] / len(ids), 1)
    sc = collections.defaultdict(list)
    for i in ids:
        sc[i.split("_")[0]].append(tasks[i]["passed"])
    full = {k: v for k, v in sc.items() if len(v) == 3}
    t["SGC"] = round(100 * sum(all(v) for v in full.values()) / len(full), 1) if full else None
    t["failure_types"] = dict(collections.Counter(tasks[i]["failure_type"] for i in ids))
    t["providers"] = sorted({p for i in ids for p in tasks[i]["providers"]})
    return t

out = {"note": "Counts only. TGC/SGC as AppWorld's metric over the tasks listed (SGC over scenarios with all 3 tasks)."}
# B1 with reasoning: part 1 (finished tasks only) + part 2
p1_raw = json.load(open(H / "runs/b1r-all-tools-reasoning/stats.json"))["tasks"]
p1_ok = {t for t, r in p1_raw.items() if r["exception"] is None}
p1, p1_cost = load("b1r-all-tools-reasoning", "evaluation-partial.json", only=p1_ok)
p2, p2_cost = load("b1r2-all-tools-reasoning-rest")
b1r = {**p1, **p2}
assert sorted(b1r) == sorted(dev), "B1 with reasoning does not cover the 57 dev tasks exactly once"
b2r, b2r_cost = load("b2r-control-reasoning")
s2, s2_cost = load("s2-ctrl-reasoning")
old = {k: load(tag)[0] for k, tag in (("B1", "b1-all-tools"), ("B2", "b2-control"), ("B3", "b3-control-repeat"))}
p4 = {t["task_id"]: t["passed"] for t in json.load(open(RES / "r1-part4-stats-minimax-m3-2026-11-01.json"))["tasks"]}
sb1 = {t["task_id"]: t["passed"] for t in json.load(open(RES / "R2/r2-b1-stats-minimax-m3-b1-2026-11-02.json"))["tasks"]}

out["B1_reasoning"] = {"runs": ["b1r-all-tools-reasoning (tasks 1-12)", "b1r2-all-tools-reasoning-rest (45 tasks)"], "totals": totals(b1r, dev),
                       "spend_including_discarded_attempts": round(p1_cost + p2_cost, 4),
                       "discarded": {"tasks": sorted(set(p1_raw) - p1_ok), "cost_of_discarded_calls": round(p1_cost - sum(v["cost"] for v in p1.values()), 4),
                                     "why": "OpenRouter key limit ($10 total) reached during task 13; every later call refused (HTTP 403); rerun in part 2 after the human raised the limit"}}
out["B2_reasoning"] = {"run": "b2r-control-reasoning", "totals": totals(b2r, dev), "spend": b2r_cost}
out["S2_control_reasoning_10_pilot_tasks"] = {"run": "s2-ctrl-reasoning", "totals": totals(s2, list(s2)), "spend": s2_cost}
out["without_reasoning"] = {k: totals(v, dev) for k, v in old.items()}
out["scads"] = {"part4": {"passed": sum(p4.values())}, "repeat": {"passed": sum(sb1.values())}}

def passed(d):
    return {t for t, v in d.items() if (v["passed"] if isinstance(v, dict) else v)}
def flips(a, b):
    A, B = passed(a), passed(b)
    return {"differ": len(A ^ B), "only_first": sorted(A - B), "only_second": sorted(B - A)}
sets = {"B1r": b1r, "B2r": b2r, "B1": old["B1"], "B2": old["B2"], "B3": old["B3"], "P4": p4, "ScRepeat": sb1}
out["flips"] = {f"{a}_vs_{b}": flips(sets[a], sets[b]) for a, b in (("B1r", "B2r"), ("B1r", "B1"), ("B2r", "B2"), ("B2r", "P4"), ("B1r", "P4"), ("P4", "ScRepeat"), ("B2", "B3"))}
r1, r2 = out["B1_reasoning"]["totals"], out["B2_reasoning"]["totals"]
out["ratios_B1r_over_B2r"] = {"prompt": round(r1["prompt"] / r2["prompt"], 2), "cost": round(r1["cost"] / r2["cost"], 2),
                              "cached_share_B1r": round(r1["cached"] / r1["prompt"], 3), "cached_share_B2r": round(r2["cached"] / r2["prompt"], 3)}
w1, w2 = out["without_reasoning"]["B1"], out["without_reasoning"]["B2"]
out["ratios_B1_over_B2_without_reasoning"] = {"prompt": round(w1["prompt"] / w2["prompt"], 2), "cost": round(w1["cost"] / w2["cost"], 2)}
out["per_task"] = {t: {"P4": int(p4[t]), "ScRepeat": int(sb1[t]), "B1": int(old["B1"][t]["passed"]), "B2": int(old["B2"][t]["passed"]), "B3": int(old["B3"][t]["passed"]),
                       "B1r": int(b1r[t]["passed"]), "B2r": int(b2r[t]["passed"]), "B1r_calls": b1r[t]["lm_calls_ok"], "B2r_calls": b2r[t]["lm_calls_ok"],
                       "B1r_cost": b1r[t]["cost"], "B2r_cost": b2r[t]["cost"]} for t in dev}
OUT.write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in out if k != "per_task"}, indent=1))
