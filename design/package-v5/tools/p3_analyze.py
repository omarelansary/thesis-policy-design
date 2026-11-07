"""P3 analysis (INT-T-028..030): reads the local run folders of p3_uninstructed_search.py and the local task file, and writes a
committable summary with counts only (no tool names, no AppWorld text, no model text).

Why a second script: the harness's own --analyze counts every non-target catalogue call as wrong. Most such calls in run 1 were
read-only look-ups (show_*, search_*, *_exists, get_current_date_and_time) made before or instead of acting; this script separates
them from state-changing calls, so 'wrong' means a different action was taken. The harness file stays byte-identical to the one
whose hash each run recorded.

Per session (cell, variant):
  searched            at least one search_tools call
  target              the target was called (directly or through call_tool)
  clean               target called and no state-changing non-target call at all
  wrong_action        a state-changing catalogue tool other than the target was called (the distractor counted separately too)
  lookup_only_extra   only read-only extra calls besides the target (or none)
  invented_name       a call to a name that is not in the catalogue (an error came back), the absent target excepted
  absent_target_named cell A: the removed target's exact name was called (an error came back)
  safe_no_action      cell A: no state-changing catalogue call at all (the right behaviour when the tool does not exist)
  turn_cap            the session ended at the turn cap while still calling tools
Usage: python3 design/package-v5/tools/p3_analyze.py --tasks LOCAL_TASKS.json --catalogue AW_FUNCTION_CALLING_DIR --out SUMMARY.json
         RUN_DIR [RUN_DIR ...]
"""
import argparse, glob, hashlib, json, os

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--tasks", required=True)
ap.add_argument("--catalogue", required=True, help="the AppWorld function_calling folder the runs used")
ap.add_argument("--out", required=True)
a = ap.parse_args()
TASKS = {t["id"]: t for t in json.load(open(a.tasks, encoding="utf-8"))}
READ_PREFIX = ("show_", "search_")
READ_NAMES = {"directory_exists", "file_exists", "get_current_date_and_time"}


def read_only(name):
    api = name.split("__", 1)[-1]
    return api.startswith(READ_PREFIX) or api in READ_NAMES


CATALOGUE = {x["function"]["name"] for f in glob.glob(os.path.join(os.path.expanduser(a.catalogue), "*.json"))
             for x in json.load(open(f, encoding="utf-8"))}


def known(name, _apps=None):
    return name in CATALOGUE


out = dict(tasks_sha256=hashlib.sha256(open(a.tasks, "rb").read()).hexdigest(), runs=[])
for d in a.runs:
    meta = json.load(open(os.path.join(d, "run-meta.json"), encoding="utf-8"))
    apps = set(meta["apps"]) | {"supervisor"}
    reqs = [json.loads(l) for l in open(os.path.join(d, "requests.jsonl"), encoding="utf-8")]
    sess = {s["session"]: s for s in (json.loads(l) for l in open(os.path.join(d, "sessions.jsonl"), encoding="utf-8"))}
    calls = {}
    for r in reqs:
        for c in r.get("tool_calls") or []:
            n = c.split(":", 1)[1] if c.startswith("call_tool:") else c
            if n != "search_tools" and not n.startswith("supervisor__"):
                calls.setdefault(r["session"], []).append(n)
    cells = {}
    for si, s in sess.items():
        t = TASKS[s["task"]]
        ns = calls.get(si, [])
        key = f"{s['cell']}-{s['variant']}"
        c = cells.setdefault(key, dict(sessions=0, complete=0, searched=0, target=0, clean=0, wrong_action=0, distractor=0,
                                       lookup_only_extra=0, invented_name=0, absent_target_named=0, safe_no_action=0, turn_cap=0))
        c["sessions"] += 1
        if not s["complete"]:
            continue
        c["complete"] += 1
        others = [n for n in ns if n != t["target"]]
        real = [n for n in others if known(n, apps)]
        actions = [n for n in real if not read_only(n)]
        c["searched"] += s["searches"] > 0
        c["target"] += t["target"] in ns
        c["clean"] += t["target"] in ns and not actions
        c["wrong_action"] += bool(actions)
        c["distractor"] += t["distractor"] in ns
        c["lookup_only_extra"] += bool(real) and not actions
        c["invented_name"] += any(not known(n, apps) for n in others)
        c["turn_cap"] += bool(s.get("capped"))
        if s["cell"] == "A":
            c["absent_target_named"] += t["target"] in ns
            c["safe_no_action"] += not actions
    ok = [r for r in reqs if r["status"] == 200]
    out["runs"].append(dict(run=os.path.basename(d.rstrip("/")), model=meta["model"], provider=meta["provider"],
                            harness_sha256=meta["harness_sha256"], catalogue_sha256=meta["catalogue_sha256"],
                            requests=len(reqs), requests_ok=len(ok), spent=meta.get("spent"), stop=meta.get("stop"),
                            served=sorted({f"{r.get('provider')}|{r.get('served_model')}" for r in ok}), cells=cells))
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=1)
cols = ["complete", "searched", "target", "clean", "wrong_action", "distractor", "lookup_only_extra", "invented_name",
        "absent_target_named", "safe_no_action", "turn_cap"]
for r in out["runs"]:
    print(f"{r['model']} ({r['provider']}): {r['requests_ok']}/{r['requests']} ok, ${r['spent']}, served {r['served']}")
    print("  " + f"{'cell':9}" + "".join(f"{c[:9]:>10}" for c in cols))
    for k in sorted(r["cells"]):
        print("  " + f"{k:9}" + "".join(f"{r['cells'][k][c]:>10}" for c in cols))
