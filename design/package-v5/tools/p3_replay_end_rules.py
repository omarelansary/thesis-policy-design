"""P3 option (a) part 2 (INT-T-036): simulate end rules on run 4's logged stopsearch sessions, with no model requests.

In stopsearch, search_tools was withdrawn at the first NULL (run 3's rule2 trigger) and every later call of a tool that was not
shown got {"error": "unknown tool"}. For a rule that withdraws search at the same point, the logged actions are therefore what the
model would have done, up to the rule's own end point, or up to the first call the rule would refuse while the log shows "Done"
(after that the simulation is approximate and says so).

Rules simulated (actions after the first NULL; "misstep" = any action that is not a call of an already-shown tool, i.e. a
guessed or unknown name or an attempt to search):
  M<m>     end the session at the m-th misstep (m = 1..4; a count, reported only to show the trade-off)
  DRY      no count. A 'dry app' is the best-match app of a NULL search. After the first NULL: (1) search is withdrawn; (2) a call of
           a shown tool in a dry app is refused (it does not run); (3) at a misstep or a refused call, the session ends if no
           'pending' tool remains, where pending = a best match (top 1) of an earlier search, outside the dry apps, state-changing,
           not yet called; otherwise the call just gets the error and the session goes on.
Reported per model and kind group (A = AF + AS, 40 sessions; P = 20 sessions): Y kept, X kept (P), X substitute (state-changing
call in X's app that ran), sessions ended by the rule, requests saved against the log, still at the backstop, and for DRY the
number of sessions in which a refused call is followed by more logged actions (approximate part).
Usage: python3 design/package-v5/tools/p3_replay_end_rules.py --catalogue AW_FC_DIR --tasks LOCAL/tasks2.json --out SUMMARY.json RUN_DIRS
"""
import argparse, glob, json, math, os, re

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--catalogue", required=True)
ap.add_argument("--tasks", required=True)
ap.add_argument("--k", type=int, default=3)
ap.add_argument("--out", required=True)
a = ap.parse_args()

defs = {}
for f in sorted(glob.glob(os.path.join(os.path.expanduser(a.catalogue), "*.json"))):
    if os.path.basename(f) != "api_docs.json":
        for x in json.load(open(f, encoding="utf-8")):
            defs[x["function"]["name"]] = x["function"]
APP = [n for n in defs if not n.startswith("supervisor__")]
TASKS = {t["id"]: t for t in json.load(open(a.tasks, encoding="utf-8"))}
READ_PREFIX, READ_NAMES = ("show_", "search_"), {"directory_exists", "file_exists", "get_current_date_and_time"}


def state_changing(n):
    api = n.split("__", 1)[-1]
    return not (api.startswith(READ_PREFIX) or api in READ_NAMES)


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", s.lower().replace("__", " ").replace("_", " ")) if w]


def doc(n):
    fn = defs[n]
    props = fn.get("parameters", {}).get("properties", {})
    return " ".join([n, fn.get("description", "")] + list(props) + [str(v.get("description", "")) for v in props.values()])


class BM25:  # same as the harness
    def __init__(self, names, k1=1.2, b=0.75):
        self.names, self.tf = names, [words(doc(n)) for n in names]
        self.avg = sum(map(len, self.tf)) / len(self.tf)
        df = {}
        for t in self.tf:
            for w in set(t):
                df[w] = df.get(w, 0) + 1
        self.idf = {w: math.log(1 + (len(names) - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        self.k1, self.b = k1, b

    def rank(self, q):
        q, sc = words(q), []
        for i, t in enumerate(self.tf):
            s = sum(self.idf[w] * t.count(w) * (self.k1 + 1) / (t.count(w) + self.k1 * (1 - self.b + self.b * len(t) / self.avg))
                    for w in q if t.count(w))
            if s > 0:
                sc.append((s, i))
        sc.sort(key=lambda x: (-x[0], x[1]))
        return [self.names[i] for _, i in sc]


IDX = {}


def index_for(absent):
    if absent not in IDX:
        IDX[absent] = BM25([n for n in APP if n != absent])
    return IDX[absent]


def simulate(task, kind, rs, rule):
    x, y = task["needs"]["X"], task["needs"]["Y"]
    absent = x["target"] if kind != "P" else None
    x_app = x["target"].split("__")[0]
    idx = index_for(absent)
    seen, scope, dry, top1, called = set(), set(), set(), set(), set()
    fired, ended, miss, xs, refused_then_more = False, None, 0, False, False
    refused = False
    for r in rs:
        qi = 0
        for c in r.get("tool_calls") or []:
            n = c.split(":", 1)[1] if c.startswith("call_tool:") else c
            if refused:
                refused_then_more = True
            if not fired:
                if c == "search_tools":
                    q = r["search_queries"][qi] if qi < len(r["search_queries"]) else ""
                    qi += 1
                    top = idx.rank(q)[: a.k]
                    fresh = [t for t in top if t not in seen]
                    seen.update(top)
                    if top:
                        scope.add(top[0].split("__")[0])
                        top1.add(top[0])
                    if not [t for t in fresh if t.split("__")[0] in scope]:
                        fired = True
                        if top:
                            dry.add(top[0].split("__")[0])
                else:
                    called.add(n)
                    xs = xs or (absent is not None and n.split("__")[0] == x_app and n in defs and state_changing(n))
                continue
            shown = c.startswith("call_tool:") and n in seen and n in defs
            if rule.startswith("M"):
                if not shown:
                    miss += 1
                    if miss >= int(rule[1:]):
                        ended = r["step"]
                        break
                    continue
            else:  # DRY
                if shown and n.split("__")[0] not in dry:
                    called.add(n)
                    xs = xs or (absent is not None and n.split("__")[0] == x_app and state_changing(n))
                    continue
                if shown:
                    refused = True
                pending = [t for t in top1 if t.split("__")[0] not in dry and state_changing(t) and t not in called]
                if not pending:
                    ended = r["step"]
                    break
                continue
            called.add(n)
            xs = xs or (absent is not None and n.split("__")[0] == x_app and state_changing(n))
        if ended:
            break
    return dict(fired=fired, y=y["target"] in called, x=x["target"] in called, xs=xs, ended=ended,
                saved=(len(rs) - ended + 1) if ended else 0, approx=refused_then_more)


out = dict(runs=[])
for d in a.runs:
    meta = json.load(open(os.path.join(d, "run-meta.json"), encoding="utf-8"))
    reqs = {}
    for l in open(os.path.join(d, "requests.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if r.get("status") == 200:
            reqs.setdefault(r["session"], []).append(r)
    ss = [json.loads(l) for l in open(os.path.join(d, "sessions.jsonl"), encoding="utf-8")]
    res = {}
    for rule in ("M1", "M2", "M3", "M4", "DRY", "LOG"):
        for s in ss:
            if s["variant"] != "stopsearch":
                continue
            g = res.setdefault(rule, {}).setdefault("P" if s["kind"] == "P" else "A", dict(sessions=0, y_kept=0, x_kept=0,
                               x_substitute=0, ended_by_rule=0, requests_saved=0, still_backstop=0, approximate=0))
            g["sessions"] += 1
            if rule == "LOG":  # what the logged stopsearch session did
                g["y_kept"] += s["need_y"]["target_called"]
                g["x_kept"] += s["need_x"]["target_called"]
                g["x_substitute"] += s["need_x"]["absent"] and s["need_x"]["state_changing_other_in_app"] > 0
                g["still_backstop"] += s["capped"]
                continue
            o = simulate(TASKS[s["task"]], s["kind"], sorted(reqs.get(s["session"], []), key=lambda r: r["step"]), rule)
            g["y_kept"] += o["y"]
            g["x_kept"] += o["x"]
            g["x_substitute"] += o["xs"]
            g["ended_by_rule"] += o["ended"] is not None
            g["requests_saved"] += o["saved"]
            g["still_backstop"] += s["capped"] and o["ended"] is None
            g["approximate"] += o["approx"]
    out["runs"].append(dict(model=meta["model"], rules=res))
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=1)
for r in out["runs"]:
    print(r["model"])
    for rule, gs in r["rules"].items():
        print(f"  {rule:4} " + " | ".join(f"{g}: {v}" for g, v in sorted(gs.items())))
