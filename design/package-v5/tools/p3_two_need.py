"""P3 run 4 harness: two-need tasks and client-enforced stop rules (INT-T-033..035; design in
design/package-v5/inputs/p3/STOP-RULE-RESEARCH-20261108.md section 4). Standard library only. Route as in p3_uninstructed_search.py:
OpenRouter chat completions, one provider pinned, fallbacks off. That harness stays unchanged (runs 1 to 3 recorded its hash).

Tasks (local, git-excluded, built by --make-tasks from the run 1-3 single-need task file): 20 two-need tasks. Task m_i joins
single-need task X = t_i and Y = t_(i+10 mod 20), which are always in different apps. X is the need whose tool may be absent.
Kinds (one session each):
  P   both present             prompt "1. X  2. Y"; nothing removed
  AF  absent named first       X's target removed from the searchable catalogue; prompt "1. X  2. Y"
  AS  absent named second      X's target removed; prompt "1. Y  2. X"
Tools offered: core (five supervisor tools) + search_tools + call_tool, as cell D of runs 1 to 3. The system text never tells
the model to search; it is the runs 1-3 text. Every executed call gets the stub result {"status":"ok","message":"Done."}.

Variants (the rule's trigger is the same in all rule variants: run 3's rule2, no count, no threshold)
  plain, plainB  no rule (plainB repeats plain to measure run-to-run flips)
  note           TRIGGER: the scope is the set of apps of the best match (top 1) of every search so far; a search counts as
                 new only if its top --k holds a tool not shown before from a scope app. A search that is not new gets, in place
                 of its results, NULL = {"status":"no_match","note":"Nothing new: no tool beyond those already shown matches.
                 The catalogue has no further tool for this need."}. Nothing else changes.
  stopreply      as note; from the first NULL on, the requests carry no tools at all, so the model can only answer. If it
                 still returns tool calls (GLM-5.3 did in the smoke test), the client ends the session there ('stop_ignored');
                 the calls are logged, not executed.
  stopsearch     as note; from the first NULL on, search_tools is withdrawn; call_tool and the core stay, so tools already shown
                 can still be called.
A call to a tool that is not offered gets {"error":"unknown tool: <name>"}. --turn-cap (12) is a safety backstop only.

Logs (local only): requests.jsonl (per request: usage, tool calls, queries, ranks of both targets, rule stage, tools offered,
final reply head to 600 characters for adjudication), sessions.jsonl (per session and per need: target called, first call step,
state-changing calls in the need's app other than its target, read-only calls, first NULL step), run-meta.json.
Stops: HTTP 401/402/403, two failed requests in a row, --max-requests, P3 spend (--prior-spend + this run) reaching --max-spend.
Keys only from the environment variable --key-env; never printed or written.

  python3 design/package-v5/tools/p3_two_need.py --make-tasks design/package-v5/inputs/p3/local/tasks.json \
      --tasks design/package-v5/inputs/p3/local/tasks2.json
  python3 design/package-v5/tools/p3_two_need.py --catalogue AW_FC_DIR --tasks .../tasks2.json --model M --provider P \
      --max-spend 10 --prior-spend X --out design/package-v5/inputs/p3/local/run4-<model>
"""
import argparse, glob, hashlib, json, math, os, re, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--make-tasks", metavar="SINGLE_NEED_TASKS")
ap.add_argument("--catalogue")
ap.add_argument("--tasks")
ap.add_argument("--model")
ap.add_argument("--provider")
ap.add_argument("--base", default="https://openrouter.ai/api/v1")
ap.add_argument("--key-env", default="OPENROUTER_API_KEY")
ap.add_argument("--kinds", default="P,AF,AS")
ap.add_argument("--variants", default="plain,plainB,note,stopreply,stopsearch")
ap.add_argument("--task-ids", default="")
ap.add_argument("--k", type=int, default=3)
ap.add_argument("--turn-cap", type=int, default=12)
ap.add_argument("--max-requests", type=int, default=2500)
ap.add_argument("--max-spend", type=float, default=0.0)
ap.add_argument("--prior-spend", type=float, default=0.0)
ap.add_argument("--max-output", type=int, default=4096)
ap.add_argument("--temperature", type=float, default=0.0)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--timeout", type=float, default=300.0)
ap.add_argument("--out")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

if a.make_tasks:
    single = json.load(open(a.make_tasks, encoding="utf-8"))
    n = len(single)
    out = []
    for i, x in enumerate(single):
        y = single[(i + n // 2) % n]
        if x["target"].split("__")[0] == y["target"].split("__")[0]:
            sys.exit(f"{x['id']} and {y['id']} share an app")
        out.append(dict(id=f"m{i + 1:02d}", x=x["id"], y=y["id"],
                        needs={"X": {k: x[k] for k in ("target", "distractor", "prompt")},
                               "Y": {k: y[k] for k in ("target", "distractor", "prompt")}}))
    with open(a.tasks, "x", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {len(out)} two-need tasks to {a.tasks}")
    sys.exit(0)

for need in ("catalogue", "tasks", "model", "provider", "out"):
    if not getattr(a, need):
        sys.exit(f"--{need} is required")

CORE_NAMES = ["supervisor__show_active_task", "supervisor__show_profile", "supervisor__show_addresses",
              "supervisor__show_payment_cards", "supervisor__show_account_passwords"]
SYSTEM = ("You are a personal assistant for one user and act in the user's apps on their behalf. The user is signed in to every app: "
          "wherever a tool asks for an access_token, pass \"tok-demo\". Carry out the request, then reply in one or two sentences.")
SEARCH_DEF = {"type": "function", "function": {"name": "search_tools", "description": "Search the catalogue of further tools by "
              "keywords. Returns the full definitions of the best matches.", "parameters": {"type": "object", "properties": {
              "query": {"type": "string", "description": "keywords describing the tool you need"}}, "required": ["query"]}}}
CALL_DEF = {"type": "function", "function": {"name": "call_tool", "description": "Run a tool from the catalogue by its exact name.",
            "parameters": {"type": "object", "properties": {"name": {"type": "string", "description": "exact tool name"},
            "arguments": {"type": "object", "description": "the tool's arguments"}}, "required": ["name", "arguments"]}}}
STUB = json.dumps({"status": "ok", "message": "Done."})
NULL = json.dumps({"status": "no_match", "note": "Nothing new: no tool beyond those already shown matches. The catalogue has no "
                   "further tool for this need."})
RULE_VARIANTS = {"note", "stopreply", "stopsearch"}
READ_PREFIX = ("show_", "search_")
READ_NAMES = {"directory_exists", "file_exists", "get_current_date_and_time"}

files = sorted(glob.glob(os.path.join(os.path.expanduser(a.catalogue), "*.json")))
cat_hash = hashlib.sha256()
defs = {}
for f in files:
    raw = open(f, "rb").read()
    cat_hash.update(os.path.basename(f).encode() + b"\0" + raw)
    if os.path.basename(f) == "api_docs.json":
        continue
    for x in json.loads(raw):
        fn = x["function"]
        defs[fn["name"]] = {"type": "function", "function": {"name": fn["name"], "description": fn.get("description", ""),
                                                             "parameters": fn.get("parameters", {"type": "object", "properties": {}})}}
CORE = [defs[n] for n in CORE_NAMES]
APP_TOOLS = [d for n, d in defs.items() if not n.startswith("supervisor__")]
tasks_raw = open(a.tasks, "rb").read()
TASKS = json.loads(tasks_raw)
if a.task_ids:
    TASKS = [t for t in TASKS if t["id"] in set(a.task_ids.split(","))]
for t in TASKS:
    for nd in t["needs"].values():
        for k in ("target", "distractor"):
            if nd[k] not in defs:
                sys.exit(f"{t['id']}: {nd[k]} not in the catalogue")


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", s.lower().replace("__", " ").replace("_", " ")) if w]


def doc_text(d):
    fn = d["function"]
    props = fn.get("parameters", {}).get("properties", {})
    return " ".join([fn["name"], fn.get("description", "")] + list(props) + [str(v.get("description", "")) for v in props.values()])


class BM25:  # same ranker as p3_uninstructed_search.py
    def __init__(self, docs, k1=1.2, b=0.75):
        self.docs = docs
        self.tf = [words(doc_text(d)) for d in docs]
        self.avg = sum(map(len, self.tf)) / max(len(self.tf), 1)
        df = {}
        for t in self.tf:
            for w in set(t):
                df[w] = df.get(w, 0) + 1
        n = len(docs)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        self.k1, self.b = k1, b

    def rank(self, query):
        q = words(query)
        scores = []
        for i, t in enumerate(self.tf):
            s = 0.0
            for w in q:
                f = t.count(w)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(t) / self.avg))
            if s > 0:
                scores.append((s, i))
        scores.sort(key=lambda x: (-x[0], x[1]))
        return [self.docs[i]["function"]["name"] for _, i in scores]


def read_only(name):
    api = name.split("__", 1)[-1]
    return api.startswith(READ_PREFIX) or api in READ_NAMES


def prompt_for(task, kind):
    x, y = task["needs"]["X"]["prompt"], task["needs"]["Y"]["prompt"]
    first, second = (y, x) if kind == "AS" else (x, y)
    return f"Please do both of these:\n1. {first}\n2. {second}"


SESSIONS = [(t, kind, v) for t in TASKS for kind in a.kinds.split(",") for v in a.variants.split(",")]
meta = dict(model=a.model, provider=a.provider, base=a.base, kinds=a.kinds, variants=a.variants, k=a.k, turn_cap=a.turn_cap,
            temperature=a.temperature, seed=a.seed, max_output=a.max_output, max_spend=a.max_spend, prior_spend=a.prior_spend,
            harness_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), tasks_sha256=hashlib.sha256(tasks_raw).hexdigest(),
            catalogue_sha256=cat_hash.hexdigest(), catalogue_tools=len(APP_TOOLS), core=CORE_NAMES,
            tasks=[t["id"] for t in TASKS], sessions_planned=len(SESSIONS), started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
os.makedirs(a.out, exist_ok=True)
if a.dry_run:
    print(f"{len(TASKS)} tasks x {len(a.kinds.split(','))} kinds x {len(a.variants.split(','))} variants = {len(SESSIONS)} sessions; "
          f"catalogue {len(APP_TOOLS)} app tools; sha256 {cat_hash.hexdigest()[:12]}")
    print(prompt_for(TASKS[0], "AS"))
    sys.exit(0)

KEY = os.environ.get(a.key_env)
if not KEY:
    sys.exit(f"Set {a.key_env} in this terminal first. Nothing was sent.")
if a.max_spend <= 0:
    sys.exit("--max-spend is required for a live run (INT-T-029). Nothing was sent.")
if a.prior_spend >= a.max_spend:
    sys.exit("The P3 spending limit is already reached. Nothing was sent.")


def scrub(s):
    s = re.sub(r"[0-9a-f]{40,}", "<hex-redacted>", s)
    return re.sub(r"sk-[A-Za-z0-9_\-]{10,}", "<key-redacted>", s)


def post(body):
    body = {**body, "provider": {"order": [a.provider], "allow_fallbacks": False}, "usage": {"include": True}}
    r = urllib.request.Request(a.base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"), method="POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(r, timeout=a.timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        return e.code, {"error_body": scrub(e.read().decode("utf-8", "replace"))[:400]}, round(time.time() - t0, 2)
    except Exception as e:
        return None, {"error": type(e).__name__}, round(time.time() - t0, 2)


def usage(j):
    u = j.get("usage") or {}
    det = u.get("prompt_tokens_details") or {}
    cdet = u.get("completion_tokens_details") or {}
    return dict(prompt=u.get("prompt_tokens"), cached=det.get("cached_tokens"), cache_write=det.get("cache_write_tokens"),
                completion=u.get("completion_tokens"), reasoning=cdet.get("reasoning_tokens"), cost=u.get("cost"))


req_log = open(os.path.join(a.out, "requests.jsonl"), "a", encoding="utf-8", newline="\n")
ses_log = open(os.path.join(a.out, "sessions.jsonl"), "a", encoding="utf-8", newline="\n")
with open(os.path.join(a.out, "run-meta.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(meta, f, indent=1)
n_req, spent, fails, stop = 0, 0.0, 0, None
for si, (task, kind, variant) in enumerate(SESSIONS, 1):
    if stop:
        break
    nx, ny = task["needs"]["X"], task["needs"]["Y"]
    absent = nx["target"] if kind in ("AF", "AS") else None
    searchable = [d for d in APP_TOOLS if d["function"]["name"] != absent]
    names_searchable = {d["function"]["name"] for d in searchable}
    index = BM25(searchable)
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt_for(task, kind)}]
    called, seen, scope = [], set(), set()
    searches, nreq, complete, capped, null_step, mode, stop_ignored = 0, 0, False, False, None, "full", False
    for step in range(1, a.turn_cap + 1):
        if n_req >= a.max_requests:
            stop = "max-requests"
            break
        if a.prior_spend + spent >= a.max_spend:
            stop = "max-spend"
            break
        tools = CORE + [SEARCH_DEF, CALL_DEF] if mode == "full" else CORE + [CALL_DEF] if mode == "nosearch" else []
        offered = {d["function"]["name"] for d in tools}
        body = dict(model=a.model, messages=msgs, temperature=a.temperature, seed=a.seed, max_tokens=a.max_output)
        if tools:
            body.update(tools=tools, tool_choice="auto")
        status, j, secs = post(body)
        if status in (429, 500, 502, 503, 504, None):
            time.sleep(20)
            status, j, secs = post(body)
        n_req += 1
        nreq += 1
        rec = dict(session=si, task=task["id"], kind=kind, variant=variant, step=step, status=status, seconds=secs, mode=mode)
        if status != 200 or not j.get("choices"):
            rec["error"] = scrub(json.dumps(j.get("error_body") or j.get("error") or "no choices"))[:400]
            req_log.write(json.dumps(rec) + "\n"); req_log.flush()
            fails += 1
            if status in (401, 402, 403):
                stop = f"http-{status}"
            elif fails >= 2:
                stop = "two-failures"
            break
        fails = 0
        u = usage(j)
        spent += u["cost"] or 0.0
        msg = j["choices"][0].get("message") or {}
        tcs = msg.get("tool_calls") or []
        rec.update(u, provider=j.get("provider"), served_model=j.get("model"), finish=j["choices"][0].get("finish_reason"),
                   tool_calls=[], search_queries=[], rank_x=[], rank_y=[], rule_stage=[])
        if not tcs:
            rec["reply_head"] = scrub(msg.get("content") or "")[:600]  # local log only, for adjudication
            req_log.write(json.dumps(rec) + "\n"); req_log.flush()
            complete = True
            break
        if mode == "notools":  # stopreply: the model answered with tool calls although none were offered; the client ends here
            rec.update(tool_calls=[(tc.get("function") or {}).get("name") or "" for tc in tcs], stop_ignored=True,
                       reply_head=scrub(msg.get("content") or "")[:600])
            req_log.write(json.dumps(rec) + "\n"); req_log.flush()
            complete = stop_ignored = True
            break
        amsg = {"role": "assistant", "content": msg.get("content") or "", "tool_calls": tcs}
        if msg.get("reasoning_details"):
            amsg["reasoning_details"] = msg["reasoning_details"]
        msgs.append(amsg)
        fire = False
        for tc in tcs:
            fn = tc.get("function") or {}
            name = fn.get("name") or ""
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = None
            if name == "search_tools" and name in offered:
                searches += 1
                q = (args or {}).get("query", "") if isinstance(args, dict) else ""
                hits = index.rank(str(q))
                top = hits[: a.k]
                fresh = [n for n in top if n not in seen]
                seen.update(top)
                rec["tool_calls"].append("search_tools")
                rec["search_queries"].append(scrub(str(q))[:200])
                rec["rank_x"].append(hits.index(nx["target"]) + 1 if nx["target"] in hits else None)
                rec["rank_y"].append(hits.index(ny["target"]) + 1 if ny["target"] in hits else None)
                result = json.dumps([defs[n]["function"] for n in top]) if top else json.dumps({"result": "no matching tools"})
                stage = None
                if variant in RULE_VARIANTS:
                    if top:
                        scope.add(top[0].split("__")[0])
                    if not [n for n in fresh if n.split("__")[0] in scope]:
                        stage, result, fire = "null", NULL, True
                        if null_step is None:
                            null_step = step
                rec["rule_stage"].append(stage)
            elif name == "call_tool" and name in offered:
                inner = str((args or {}).get("name", "")) if isinstance(args, dict) else ""
                rec["tool_calls"].append("call_tool:" + inner)
                if inner in names_searchable or inner in CORE_NAMES:
                    called.append((inner, step))
                    result = STUB
                else:
                    called.append((inner + "#unknown", step))
                    result = json.dumps({"error": f"unknown tool: {inner}"})
            else:
                rec["tool_calls"].append(name)
                if name in offered and name in CORE_NAMES:
                    called.append((name, step))
                    result = STUB
                else:
                    called.append((name + "#unknown", step))
                    result = json.dumps({"error": f"unknown tool: {name}"})
            msgs.append({"role": "tool", "tool_call_id": tc.get("id") or "", "content": result})
        if fire and variant == "stopreply":
            mode = "notools"
        elif fire and variant == "stopsearch":
            mode = "nosearch"
        rec["tools_offered_next"] = mode
        req_log.write(json.dumps(rec) + "\n"); req_log.flush()
    else:
        capped = complete = True

    def need_rec(nd, is_absent):
        app = nd["target"].split("__")[0]
        cat = [(n, s) for n, s in called if n in defs and not n.startswith("supervisor__")]
        tgt_steps = [s for n, s in cat if n == nd["target"]]
        other = [n for n, _ in cat if n.split("__")[0] == app and n != nd["target"]]
        return dict(absent=is_absent, target_called=bool(tgt_steps), first_target_step=min(tgt_steps, default=None),
                    distractor_called=any(n == nd["distractor"] for n, _ in cat),
                    state_changing_other_in_app=len({n for n in other if not read_only(n)}),
                    read_only_in_app=sum(1 for n in other if read_only(n)),
                    target_named_unknown=any(n == nd["target"] + "#unknown" for n, _ in called))
    cat_all = [n for n, _ in called if n in defs and not n.startswith("supervisor__")]
    apps_xy = {nx["target"].split("__")[0], ny["target"].split("__")[0]}
    srec = dict(session=si, task=task["id"], kind=kind, variant=variant, complete=complete, capped=capped, requests=nreq,
                searches=searches, null_step=null_step, final_mode=mode, stop_ignored=stop_ignored,
                need_x=need_rec(nx, absent is not None), need_y=need_rec(ny, False),
                state_changing_other_apps=sum(1 for n in cat_all if n.split("__")[0] not in apps_xy and not read_only(n)),
                unknown_calls=sum(1 for n, _ in called if n.endswith("#unknown")))
    ses_log.write(json.dumps(srec) + "\n"); ses_log.flush()
    print(f"[{si}/{len(SESSIONS)}] {task['id']} {kind:2} {variant:10} X {'abs' if absent else 'pre'} "
          f"{'T' if srec['need_x']['target_called'] else '-'} Y {'T' if srec['need_y']['target_called'] else '-'} "
          f"null@{null_step} cap={capped}; requests {n_req}; spent ${spent:.4f}", flush=True)

meta.update(ended_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), requests=n_req, spent=round(spent, 5), stop=stop or "done")
with open(os.path.join(a.out, "run-meta.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(meta, f, indent=1)
print(f"stop: {stop or 'done'}; requests {n_req}; spent ${spent:.4f} (P3 total ${a.prior_spend + spent:.4f} of ${a.max_spend})")
