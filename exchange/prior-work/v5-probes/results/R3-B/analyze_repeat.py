"""Counts-only analysis of AUTH-027 (lead, 2026-11-06): the repeat of the MiniMax-M3 reasoning-on B1 and B2 (OpenRouter, gmicloud/fp8)
against the first reasoning-on runs (AUTH-025, r3-b-reasoning-stats.json). Descriptive only (estimation-only reporting, INT-T-022): no test.
Usage: python analyze_repeat.py <first-runs stats json> <out.json>"""
import collections, json, pathlib, sys

H = pathlib.Path(__file__).resolve().parent
first = json.load(open(sys.argv[1]))
dev = [l.strip() for l in open(H / "aw-root/data/datasets/dev.txt") if l.strip()]

def run(tag):
    R = H / "runs" / tag
    ev = {t: bool(v["success"]) for t, v in json.load(open(R / "evaluation.json"))["individual"].items()}
    st = json.load(open(R / "stats.json"))
    calls = [json.loads(l) for l in open(R / "trace/calls.jsonl")]
    ok = [c for c in calls if c["status"] == "ok"]
    tot = {"tasks": len(ev), "passed": sum(ev.values()), "lm_calls_ok": len(ok), "lm_calls_error": len(calls) - len(ok),
           "prompt": sum(c["prompt"] for c in ok), "cached": sum(c["cached"] or 0 for c in ok), "completion": sum(c["completion"] for c in ok),
           "reasoning_tokens": sum(c.get("reasoning_tokens") or 0 for c in ok), "cost": round(sum(c.get("cost") or 0 for c in calls), 4),
           "providers": sorted({str(c.get("provider")) for c in ok}),
           "step_capped": sorted(t for t, r in st["tasks"].items() if r["steps"] >= 50), "started": st["started"], "finished": st["finished"]}
    sc = collections.defaultdict(list)
    for t in dev:
        sc[t.split("_")[0]].append(ev[t])
    tot["TGC"] = round(100 * tot["passed"] / len(dev), 1); tot["SGC"] = round(100 * sum(all(v) for v in sc.values()) / len(sc), 1)
    return ev, tot

b1b, t1 = run("mm3-b1r-repeat"); b2b, t2 = run("mm3-b2r-repeat")
b1a = {t: bool(first["per_task"][t]["B1r"]) for t in dev}; b2a = {t: bool(first["per_task"][t]["B2r"]) for t in dev}
flips = lambda a, b: sum(a[t] != b[t] for t in dev)
both = collections.Counter(f"B1 {b1a[t] + b1b[t]} of 2, B2 {b2a[t] + b2b[t]} of 2" for t in dev)
out = {
    "note": "Counts only; descriptive, no test (INT-T-022). 'first' = AUTH-025 runs (B1 in two parts, each task once), 'repeat' = AUTH-027 runs.",
    "repeat_totals": {"B1_all_tools": t1, "B2_control": t2},
    "passed": {"B1_first": sum(b1a.values()), "B1_repeat": t1["passed"], "B2_first": sum(b2a.values()), "B2_repeat": t2["passed"]},
    "mean_passed_of_57": {"B1": (sum(b1a.values()) + t1["passed"]) / 2, "B2": (sum(b2a.values()) + t2["passed"]) / 2},
    "tasks_with_different_result": {"B1_first_vs_repeat": flips(b1a, b1b), "B2_first_vs_repeat": flips(b2a, b2b),
                                    "B1_vs_B2_first": flips(b1a, b2a), "B1_vs_B2_repeat": flips(b1b, b2b)},
    "per_task_passes_of_2": dict(sorted(both.items())),
    "tasks_B1_passed_more_often": sum(b1a[t] + b1b[t] > b2a[t] + b2b[t] for t in dev),
    "tasks_B2_passed_more_often": sum(b1a[t] + b1b[t] < b2a[t] + b2b[t] for t in dev),
    "ratios_B1_over_B2": {"first": {"prompt": first["ratios_B1r_over_B2r"]["prompt"], "cost": first["ratios_B1r_over_B2r"]["cost"]},
                          "repeat": {"prompt": round(t1["prompt"] / t2["prompt"], 2), "cost": round(t1["cost"] / t2["cost"], 2)}},
    "per_task": {t: {"B1_first": int(b1a[t]), "B1_repeat": int(b1b[t]), "B2_first": int(b2a[t]), "B2_repeat": int(b2b[t])} for t in dev},
}
pathlib.Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "per_task"}, indent=1))
