"""P1 analysis (AUTH-033): reads the local P1 runs of tools/p1_memory.py and prints a committable summary (counts and AppWorld task
ids only; no user identity, task text or API name).
Per run: sessions, success (AppWorld's evaluator), billed cost, calls, searches, seeds called (measured h = seeds called / seeds),
seeds called that the task does not need (over-calling), needed APIs called.
Paired (same session, averaged over repeats): pop6 minus none, for success and for billed cost per session. 95% interval: bootstrap
over users (the unit of analysis, `05` P1), 4,000 resamples, seed 0. Also by recurrence band of the session (precision of seeding
everything the user needed before, `tools/p1_recurrence.py`): zero, low (above 0 and below 0.25), high (0.25 or more).
Run-to-run noise: none r1 against none r2 (sessions whose success differs).
Usage: python3 -I design/package-v5/tools/p1_analyze.py RUNS_DIR DATA_DIR --out SUMMARY.json
"""
import argparse, json, os, random, re, statistics

ap = argparse.ArgumentParser()
ap.add_argument("runs")
ap.add_argument("data")
ap.add_argument("--out", required=True)
ap.add_argument("--prefix", default="p1-main-glm-5.3")
a = ap.parse_args()
DATA = os.path.expanduser(a.data)


def is_core(api):
    app, name = re.split(r"\.|__", api, maxsplit=1)
    return app == "supervisor" or name == "login"


ids = []
for split in ("train", "dev"):
    ids += [l.strip() for l in open(os.path.join(DATA, "datasets", f"{split}.txt")) if l.strip()]
users = {}
for t in ids:
    s = json.load(open(os.path.join(DATA, "tasks", t, "specs.json")))
    need = {x for x in json.load(open(os.path.join(DATA, "tasks", t, "ground_truth", "required_apis.json"))) if not is_core(x)}
    users.setdefault(s["supervisor"]["email"], {}).setdefault(t.split("_")[0], (s["datetime"], t, need))
OWNER, BAND = {}, {}
for k, (u, sc) in enumerate(users.items()):
    ss = sorted(sc.values())
    for i in range(1, len(ss)):
        prev = set().union(*(x[2] for x in ss[:i])); h = len(prev & ss[i][2]) / len(prev) if prev else 0.0
        OWNER[ss[i][1]] = f"u{k}"
        BAND[ss[i][1]] = "zero" if h == 0 else ("low" if h < 0.25 else "high")


def load(arm, rep):
    d = os.path.join(a.runs, f"{a.prefix}-{arm}-r{rep}")
    evf = next((os.path.join(d, f) for f in ("evaluation-per-task.json", "evaluation.json") if os.path.exists(os.path.join(d, f))), None)
    if not (os.path.exists(os.path.join(d, "stats.json")) and evf):
        return None  # missing or still running
    st = json.load(open(os.path.join(d, "stats.json")))
    ev = json.load(open(evf)).get("individual", {})  # per-task scoring preferred (tools/aw_eval_per_task.py)
    tasks = st.get("tasks", {})
    per = {t: {"success": int(bool(ev.get(t, {}).get("success"))), "spend": r.get("spend", 0.0), "calls": r.get("calls", 0),
               "searches": r.get("searches", 0), "seeds": r.get("seeds", 0), "seeds_called": r.get("seeds_called", 0),
               "over": r.get("seeds_called_not_needed", 0), "exception": r.get("exception")} for t, r in tasks.items()}
    return {"per": per, "spend": st.get("spend"), "stopped": st.get("stopped")}


runs = {(arm, rep): load(arm, rep) for arm in ("none", "pop6") for rep in (1, 2)}
out = {"runs": {}, "paired": {}}
for (arm, rep), r in runs.items():
    if not r:
        continue
    p = r["per"].values()
    seeds = sum(x["seeds"] for x in p)
    out["runs"][f"{arm}-r{rep}"] = {"sessions": len(r["per"]), "success": sum(x["success"] for x in p),
                                    "exceptions": sum(1 for x in p if x["exception"]), "billed": round(r["spend"] or 0, 4),
                                    "calls": sum(x["calls"] for x in p), "searches": sum(x["searches"] for x in p),
                                    "seeds": seeds, "seeds_called": sum(x["seeds_called"] for x in p),
                                    "measured_h": round(sum(x["seeds_called"] for x in p) / seeds, 3) if seeds else None,
                                    "seeds_called_not_needed": sum(x["over"] for x in p), "stopped": r["stopped"]}
reps = [rep for rep in (1, 2) if runs[("none", rep)] and runs[("pop6", rep)]]
if reps:
    common = sorted(set.intersection(*[set(runs[(arm, rep)]["per"]) for arm in ("none", "pop6") for rep in reps]))
    diff = {k: {t: statistics.mean(runs[("pop6", rep)]["per"][t][k] - runs[("none", rep)]["per"][t][k] for rep in reps) for t in common}
            for k in ("success", "spend", "calls", "searches")}
    us = sorted({OWNER[t] for t in common})

    def boot(vals):
        rng = random.Random(0); bs = []
        for _ in range(4000):
            pick = [rng.choice(us) for _ in us]
            v = [vals[t] for u in pick for t in common if OWNER[t] == u]
            bs.append(sum(v) / len(v))
        bs.sort()
        return [round(bs[99], 4), round(bs[3899], 4)]

    for k in ("success", "spend", "calls", "searches"):
        out["paired"][k] = {"mean_diff_per_session": round(statistics.mean(diff[k].values()), 4), "ci95_user_cluster": boot(diff[k])}
    base_spend = statistics.mean(statistics.mean(runs[("none", rep)]["per"][t]["spend"] for rep in reps) for t in common)
    out["paired"]["spend"]["none_mean_per_session"] = round(base_spend, 4)
    out["paired"]["spend"]["relative"] = round(out["paired"]["spend"]["mean_diff_per_session"] / base_spend, 3)
    out["paired"]["by_band"] = {b: {"sessions": sum(BAND[t] == b for t in common),
                                    "success_diff": round(statistics.mean([diff["success"][t] for t in common if BAND[t] == b] or [0]), 3),
                                    "spend_diff": round(statistics.mean([diff["spend"][t] for t in common if BAND[t] == b] or [0]), 4)}
                                for b in ("zero", "low", "high")}
    out["paired"]["sessions"], out["paired"]["users"], out["paired"]["repeats"] = len(common), len(us), reps
if runs[("none", 1)] and runs[("none", 2)]:
    c = set(runs[("none", 1)]["per"]) & set(runs[("none", 2)]["per"])
    out["none_flips_r1_vs_r2"] = sum(runs[("none", 1)]["per"][t]["success"] != runs[("none", 2)]["per"][t]["success"] for t in c)
    out["pop6_flips_r1_vs_r2"] = (sum(runs[("pop6", 1)]["per"][t]["success"] != runs[("pop6", 2)]["per"][t]["success"]
                                      for t in set(runs[("pop6", 1)]["per"]) & set(runs[("pop6", 2)]["per"]))
                                  if runs[("pop6", 1)] and runs[("pop6", 2)] else None)
out["per_session"] = {f"{arm}-r{rep}": {t: [x["success"], round(x["spend"], 5), x["calls"], x["searches"], x["seeds_called"]]
                                        for t, x in r["per"].items()} for (arm, rep), r in runs.items() if r}
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "per_session"}, indent=1))
