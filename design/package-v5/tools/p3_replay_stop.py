"""P3 option (a) (INT-T-036): replay candidate stop rules on run 4's logged sessions, with no model requests.

Why a replay is valid up to the firing point: a rule changes nothing before it first fires, so the logged no-rule sessions (plain
and plainB) show exactly what a rule session would have seen up to that point. What the model does after the rule fires cannot
be replayed. The script therefore counts, at the moment each candidate would act, the state of the doable need Y:
  done      Y's target already called         (the stop costs nothing)
  shown     Y's target shown by a search, not yet called
  unshown   Y's target not yet shown           (a stop that removes search loses Y, unless search stays open for Y)
Search results are recomputed with the harness's BM25 over the same searchable catalogue (deterministic). Check: on the note
sessions, the replayed first-NULL step must equal the logged null_step.

Candidates (the trigger is always run 3's rule2: a search showing no unseen tool from a scope app is a NULL):
  C0 first-null      act at the first NULL (what stopreply did)
  C1 second-null     act at the second NULL in the session (CGDP-style p = 2 consecutive-evidence form, not a turn count)
  C2 same-scope      act at the second NULL whose best match is in an app that already had a NULL (dry scope)
  C3 pending-shown   at the first NULL withdraw search; then the first action that is not a call of an already-shown tool ends
                     the session. Y is kept if Y's target is called before that action (replayed on the logged actions; a lower
                     bound, because with search really withdrawn the model may call shown tools more readily)
Second part, on the logged stopsearch sessions (search already withdrawn at the first NULL, so the model's later actions are
real for these rules up to their end point):
  C3s pending-shown    after the first NULL, calls of already-shown tools continue; the first other action (a guessed or
                       unknown name, or an attempt to search) ends the session
  C4s dry-scope        as C3s, and a call of a shown tool in a dry app (the best-match app of a NULL search) also ends it
Per session: Y kept (Y's target called before the end point), X substitute after the NULL that the rule would still allow, and
requests that the end point saves against the logged session.
Usage: python3 design/package-v5/tools/p3_replay_stop.py --catalogue AW_FC_DIR --tasks LOCAL/tasks2.json --out SUMMARY.json RUN_DIRS
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
    if os.path.basename(f) == "api_docs.json":
        continue
    for x in json.load(open(f, encoding="utf-8")):
        fn = x["function"]
        defs[fn["name"]] = fn
APP = [n for n in defs if not n.startswith("supervisor__")]
TASKS = {t["id"]: t for t in json.load(open(a.tasks, encoding="utf-8"))}


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", s.lower().replace("__", " ").replace("_", " ")) if w]


def doc(n):
    fn = defs[n]
    props = fn.get("parameters", {}).get("properties", {})
    return " ".join([n, fn.get("description", "")] + list(props) + [str(v.get("description", "")) for v in props.values()])


class BM25:  # same as the harness
    def __init__(self, names, k1=1.2, b=0.75):
        self.names = names
        self.tf = [words(doc(n)) for n in names]
        self.avg = sum(map(len, self.tf)) / len(self.tf)
        df = {}
        for t in self.tf:
            for w in set(t):
                df[w] = df.get(w, 0) + 1
        N = len(names)
        self.idf = {w: math.log(1 + (N - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        self.k1, self.b = k1, b

    def rank(self, q):
        q = words(q)
        sc = []
        for i, t in enumerate(self.tf):
            s = 0.0
            for w in q:
                f = t.count(w)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(t) / self.avg))
            if s > 0:
                sc.append((s, i))
        sc.sort(key=lambda x: (-x[0], x[1]))
        return [self.names[i] for _, i in sc]


INDEX = {}


def index_for(absent):
    if absent not in INDEX:
        INDEX[absent] = BM25([n for n in APP if n != absent])
    return INDEX[absent]


def replay(task, kind, reqs):
    """walk the logged actions in order; return events and Y's state at each candidate's acting point"""
    x, y = task["needs"]["X"], task["needs"]["Y"]
    absent = x["target"] if kind in ("AF", "AS") else None
    idx = index_for(absent)
    seen, scope, dry = set(), set(), set()
    y_called = False
    nulls, events, actions = [], [], []
    for r in sorted(reqs, key=lambda r: r["step"]):
        qi = 0
        for c in r.get("tool_calls") or []:
            if c == "search_tools":
                q = r["search_queries"][qi] if qi < len(r["search_queries"]) else ""
                qi += 1
                top = idx.rank(q)[: a.k]
                fresh = [n for n in top if n not in seen]
                seen.update(top)
                app = top[0].split("__")[0] if top else None
                if app:
                    scope.add(app)
                is_null = not [n for n in fresh if n.split("__")[0] in scope]
                actions.append(("search", is_null, app))
                if is_null:
                    nulls.append(dict(step=r["step"], app=app, y=("done" if y_called else "shown" if y["target"] in seen else "unshown"),
                                      same_scope=app in dry))
                    if app:
                        dry.add(app)
            else:
                n = c.split(":", 1)[1] if c.startswith("call_tool:") else c
                actions.append(("call", n in seen and n in defs, n))
                if n == y["target"]:
                    y_called = True
    out = {"first_null_step": nulls[0]["step"] if nulls else None}
    out["C0"] = nulls[0]["y"] if nulls else "no-fire"
    out["C1"] = nulls[1]["y"] if len(nulls) > 1 else "no-fire"
    same = [e for e in nulls if e["same_scope"]]
    out["C2"] = same[0]["y"] if same else "no-fire"
    if not nulls:
        out["C3"] = "no-fire"
    elif nulls[0]["y"] == "done":
        out["C3"] = "done"
    else:
        # position of the first NULL in the action list, then scan
        k = [i for i, (kind_, flag, _) in enumerate(actions) if kind_ == "search" and flag][0]
        res = "cut"
        for kind_, flag, n in actions[k + 1:]:
            if kind_ == "call" and flag:
                if n == y["target"]:
                    res = "kept"
                    break
                continue
            break
        out["C3"] = res
    out["y_done_in_log"] = y_called
    return out


READ_PREFIX = ("show_", "search_")
READ_NAMES = {"directory_exists", "file_exists", "get_current_date_and_time"}


def state_changing(n):
    api = n.split("__", 1)[-1]
    return not (api.startswith(READ_PREFIX) or api in READ_NAMES)


def simulate_end(task, kind, reqs):
    """C3s and C4s on a logged stopsearch session"""
    x, y = task["needs"]["X"], task["needs"]["Y"]
    absent = x["target"] if kind in ("AF", "AS") else None
    idx = index_for(absent)
    seen, scope, dry = set(), set(), set()
    fired, res = False, {}
    y_before = False
    rs = sorted(reqs, key=lambda r: r["step"])
    nreq = len(rs)
    alive = {"C3s": True, "C4s": True}
    out = {c: dict(y_kept=False, x_sub_allowed=False, end_step=None) for c in alive}
    for r in rs:
        qi = 0
        for c in r.get("tool_calls") or []:
            if not fired:
                if c == "search_tools":
                    q = r["search_queries"][qi] if qi < len(r["search_queries"]) else ""
                    qi += 1
                    top = idx.rank(q)[: a.k]
                    fresh = [n for n in top if n not in seen]
                    seen.update(top)
                    app = top[0].split("__")[0] if top else None
                    if app:
                        scope.add(app)
                    if not [n for n in fresh if n.split("__")[0] in scope]:
                        fired = True
                        if app:
                            dry.add(app)
                else:
                    n = c.split(":", 1)[1] if c.startswith("call_tool:") else c
                    if n == y["target"]:
                        y_before = True
                continue
            n = c.split(":", 1)[1] if c.startswith("call_tool:") else c
            shown_call = c.startswith("call_tool:") and n in seen and n in defs
            for cand in alive:
                if not alive[cand]:
                    continue
                ok = shown_call and not (cand == "C4s" and n.split("__")[0] in dry)
                if not ok:
                    alive[cand] = False
                    out[cand]["end_step"] = r["step"]
                    continue
                if n == y["target"]:
                    out[cand]["y_kept"] = True
                if absent and n.split("__")[0] == x["target"].split("__")[0] and state_changing(n):
                    out[cand]["x_sub_allowed"] = True
    if not fired:
        return None
    for cand in out:
        out[cand]["y_kept"] = out[cand]["y_kept"] or y_before
        end = out[cand]["end_step"]
        out[cand]["saved"] = (nreq - end + 1) if end else 0  # the request whose actions end it is replaced by the stop
    return out


summary = dict(runs=[])
for d in a.runs:
    meta = json.load(open(os.path.join(d, "run-meta.json"), encoding="utf-8"))
    reqs = {}
    for l in open(os.path.join(d, "requests.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if r.get("status") == 200:
            reqs.setdefault(r["session"], []).append(r)
    ss = [json.loads(l) for l in open(os.path.join(d, "sessions.jsonl"), encoding="utf-8")]
    check = dict(note_sessions=0, match=0)
    tab = {}
    for s in ss:
        rp = replay(TASKS[s["task"]], s["kind"], reqs.get(s["session"], []))
        if s["variant"] == "note":
            check["note_sessions"] += 1
            check["match"] += rp["first_null_step"] == s["null_step"]
        if s["variant"] not in ("plain", "plainB"):
            continue
        group = "P" if s["kind"] == "P" else "A"  # A = AF + AS
        t = tab.setdefault(group, {"sessions": 0, "y_done_in_log": 0})
        t["sessions"] += 1
        t["y_done_in_log"] += rp["y_done_in_log"]
        for cand in ("C0", "C1", "C2", "C3"):
            t.setdefault(cand, {})
            t[cand][rp[cand]] = t[cand].get(rp[cand], 0) + 1
    sim = {}
    for s_ in ss:
        if s_["variant"] != "stopsearch":
            continue
        o = simulate_end(TASKS[s_["task"]], s_["kind"], reqs.get(s_["session"], []))
        group = "P" if s_["kind"] == "P" else "A"
        g = sim.setdefault(group, {"sessions": 0, "fired": 0, "y_done_logged": 0, "x_sub_logged": 0, "capped_logged": 0})
        g["sessions"] += 1
        g["y_done_logged"] += s_["need_y"]["target_called"]
        g["x_sub_logged"] += s_["need_x"]["absent"] and s_["need_x"]["state_changing_other_in_app"] > 0
        g["capped_logged"] += s_["capped"]
        if o is None:
            for cand in ("C3s", "C4s"):
                g.setdefault(cand, dict(y_kept=0, x_sub_allowed=0, ended_early=0, requests_saved=0))["y_kept"] += s_["need_y"]["target_called"]
            continue
        g["fired"] += 1
        for cand, v in o.items():
            h = g.setdefault(cand, dict(y_kept=0, x_sub_allowed=0, ended_early=0, requests_saved=0))
            h["y_kept"] += v["y_kept"]
            h["x_sub_allowed"] += v["x_sub_allowed"]
            h["ended_early"] += v["end_step"] is not None
            h["requests_saved"] += v["saved"]
    summary["runs"].append(dict(model=meta["model"], replay_check_note_first_null=check, plain_and_plainB=tab,
                                stopsearch_simulation=sim))
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(summary, f, indent=1)
for r in summary["runs"]:
    print(r["model"], "check (note sessions, replayed first NULL = logged):", r["replay_check_note_first_null"])
    for g, t in r["plain_and_plainB"].items():
        print(f"  {g}: sessions {t['sessions']}, Y done in log {t['y_done_in_log']}")
        for cand in ("C0", "C1", "C2", "C3"):
            print(f"     {cand}: {dict(sorted(t[cand].items()))}")
    for g, t in r["stopsearch_simulation"].items():
        print(f"  stopsearch {g}: {t}")
