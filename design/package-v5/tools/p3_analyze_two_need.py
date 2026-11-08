"""P3 run 4 analysis (INT-T-035): reads local run folders of p3_two_need.py and writes a committable summary with counts only
(no tool names, no AppWorld text, no model text).

Per (kind, variant), sessions of 20:
  x_done / y_done   the need's target was called (X is the need whose tool is removed in kinds AF and AS; Y is always present)
  both_done         kind P: both targets called
  y_cut             Y not done in a session where the rule changed the offered tools (stopreply or stopsearch fired)
  x_substitute      X absent: a state-changing tool of X's app (other than X's target) was called
  x_distractor      X absent: X's pre-set near-miss tool (the 'minefield') was called
  x_named           X absent: X's removed target was called by its exact name (an error came back)
  other_app_action  a state-changing call outside the two needs' apps
  null_fired        the rule's NULL result was returned at least once
  stop_ignored      stopreply: the model returned tool calls with no tools offered, so the client ended the session
  capped            the session reached the 12-request backstop
  requests, requests_after_null
Paired per task against plain (same kind): y_done discordant pairs b (plain done, variant not) and c (plain not, variant done),
with the exact two-sided McNemar p; and plain against plainB (run-to-run flips).
Usage: python3 design/package-v5/tools/p3_analyze_two_need.py --out SUMMARY.json RUN_DIR [RUN_DIR ...]
"""
import argparse, json, math, os

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--out", required=True)
a = ap.parse_args()


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


out = dict(runs=[])
for d in a.runs:
    meta = json.load(open(os.path.join(d, "run-meta.json"), encoding="utf-8"))
    ss = [json.loads(l) for l in open(os.path.join(d, "sessions.jsonl"), encoding="utf-8")]
    cells, by = {}, {}
    for s in ss:
        key = f"{s['kind']}-{s['variant']}"
        c = cells.setdefault(key, dict(sessions=0, complete=0, x_done=0, y_done=0, both_done=0, y_cut=0, x_substitute=0,
                                       x_distractor=0, x_named=0, other_app_action=0, null_fired=0, stop_ignored=0, capped=0, requests=0,
                                       requests_after_null=0))
        c["sessions"] += 1
        c["requests"] += s["requests"]
        if not s["complete"]:
            continue
        c["complete"] += 1
        x, y = s["need_x"], s["need_y"]
        c["x_done"] += x["target_called"]
        c["y_done"] += y["target_called"]
        c["both_done"] += s["kind"] == "P" and x["target_called"] and y["target_called"]
        c["y_cut"] += (not y["target_called"]) and s["final_mode"] != "full"
        if x["absent"]:
            c["x_substitute"] += x["state_changing_other_in_app"] > 0
            c["x_distractor"] += x["distractor_called"]
            c["x_named"] += x["target_named_unknown"]
        c["other_app_action"] += s["state_changing_other_apps"] > 0
        c["null_fired"] += s["null_step"] is not None
        c["capped"] += s["capped"]
        c["stop_ignored"] += bool(s.get("stop_ignored"))
        if s["null_step"] is not None:
            c["requests_after_null"] += s["requests"] - s["null_step"]
        by[(s["task"], s["kind"], s["variant"])] = s
    paired = {}
    kinds = sorted({k for _, k, _ in by})
    variants = sorted({v for _, _, v in by})
    for kind in kinds:
        for v in variants:
            if v == "plain":
                continue
            b = c_ = 0
            for (t, k, vv), s in by.items():
                if k != kind or vv != "plain":
                    continue
                o = by.get((t, kind, v))
                if not o:
                    continue
                p_done, v_done = s["need_y"]["target_called"], o["need_y"]["target_called"]
                b += p_done and not v_done
                c_ += v_done and not p_done
            paired[f"{kind}-{v}"] = dict(y_done_plain_only=b, y_done_variant_only=c_, exact_mcnemar_p=round(mcnemar(b, c_), 4))
    out["runs"].append(dict(run=os.path.basename(d.rstrip("/")), model=meta["model"], provider=meta["provider"],
                            harness_sha256=meta["harness_sha256"], tasks_sha256=meta["tasks_sha256"],
                            catalogue_sha256=meta["catalogue_sha256"], requests=meta.get("requests"), spent=meta.get("spent"),
                            stop=meta.get("stop"), cells=cells, paired_vs_plain=paired))
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=1)
cols = ["complete", "x_done", "y_done", "both_done", "y_cut", "x_substitute", "x_distractor", "x_named", "other_app_action",
        "null_fired", "stop_ignored", "capped", "requests", "requests_after_null"]
for r in out["runs"]:
    print(f"{r['model']}: {r['requests']} requests, ${r['spent']}, stop {r['stop']}")
    print("  " + f"{'cell':14}" + "".join(f"{c[:8]:>9}" for c in cols))
    for k in sorted(r["cells"]):
        print("  " + f"{k:14}" + "".join(f"{r['cells'][k][c]:>9}" for c in cols))
    print("  paired y_done vs plain (plain-only / variant-only / p): " +
          "; ".join(f"{k} {v['y_done_plain_only']}/{v['y_done_variant_only']}/{v['exact_mcnemar_p']}" for k, v in sorted(r["paired_vs_plain"].items())))
