"""P3 harness: do models search for a deferred tool when nobody tells them to? (HYP-0019; design/package-v5/05 P3; INT-T-028,
INT-T-029). Standard library only. Route: OpenRouter chat completions with one provider pinned and fallbacks off.

Tasks: about 20 single-need tasks written by the lead over AppWorld's real function-calling definitions (task file and catalogue
stay in the git-excluded folder design/package-v5/inputs/p3/local/, because AppWorld asks that public copies be encrypted). Each
task names one target tool and one similar but wrong tool (the distractor); the prompt gives every required value. Tool calls
are answered with a fixed stub result, so the measure is which tools the model calls, not whether an app changed.

Catalogue: every app file in --catalogue except api_docs.json (AppWorld's own documentation app is a discovery route of its own
and would confound the search measure). The core (always visible) is the supervisor app's five tools other than complete_task.

Cells (one session = one user turn, at most --turn-cap model requests)
  E  expose-all      tools = core + every app tool; no search tool                      (control)
  D  deferred        tools = core + search_tools + call_tool; target searchable
  A  absent          as D, target removed from the searchable catalogue                 (the right answer is to say so)
  W  wrong visible   as D, plus the distractor's definition visible in tools
D, A and W each run in variants: plain; index (one line naming the apps reachable beyond the listed tools, without saying how to
reach them; run 1); rule (run 2, INT-T-031: the NO-MATCH RULE below, system text as plain).
NO-MATCH RULE (deterministic, no count of turns or searches and no score threshold): the client remembers every tool a search has
shown in the session. A search whose top --k results were all shown before has found nothing new. The first time that happens, the
search result is the complete list of the tools (name and first sentence of the description) of the app(s) those results belong
to, with a note that if none of them fits, the catalogue has no such tool; any later search that again finds nothing new (or a
search with no match at all) gets a note that the catalogue has no further tool for this need. The note states a fact about the
catalogue; the system text does not change, and what the model does next is what is measured. --turn-cap stays as a safety
backstop only (run 2: 12), reported separately, never the rule. The system text never tells the model to search; search_tools and call_tool carry their own short
descriptions, as a vendor's search tool does. search_tools returns the top --k definitions by BM25 over name, description and
parameter names (the harness's ranker, not a V5 choice); call_tool runs any catalogue tool by name.

Per session the harness records: searches, the target's rank in each search result, every tool called (name), whether the target
was called (directly or through call_tool), whether it was called without having appeared in a search result, the distractor and
other catalogue calls, and the usage of each request (prompt, cached, completion, reasoning tokens, cost). Outcome classes, from
`05`: zero searches, search then correct call, wrong-tool call, answer without a tool.

A session that reaches --turn-cap while still calling tools is complete with the outcome 'turn cap reached' (unless the
target or another catalogue tool was already called, which then decides its class).

Stops: HTTP 401, 402 or 403; two failed requests in a row; --max-requests; spend (--prior-spend plus this run's reported cost)
reaching --max-spend (INT-T-029: $10 in total across all P3 runs). Keys only from the environment variable --key-env; never
printed or written. Logs (local folder only): requests.jsonl, sessions.jsonl, run-meta.json. --analyze writes a summary with
counts per cell and variant and task ids only (no AppWorld text), which is what may be committed.

Examples (Linux):
  python3 design/package-v5/tools/p3_uninstructed_search.py --catalogue ~/r3-work/aw-root/data/api_docs/function_calling \
      --tasks design/package-v5/inputs/p3/local/tasks.json --model z-ai/glm-x --provider some/provider --dry-run \
      --out design/package-v5/inputs/p3/local/dry
  set -a; . ~/r3-work/.env; set +a
  python3 design/package-v5/tools/p3_uninstructed_search.py ... --max-spend 10 --prior-spend 0 --out design/package-v5/inputs/p3/local/<run>
  python3 design/package-v5/tools/p3_uninstructed_search.py --analyze design/package-v5/inputs/p3/local/<run> \
      --summary design/package-v5/inputs/p3/<run>-summary.json
"""
import argparse, glob, hashlib, json, math, os, re, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--catalogue")
ap.add_argument("--tasks")
ap.add_argument("--model")
ap.add_argument("--provider", help="OpenRouter provider slug to pin (order, no fallbacks)")
ap.add_argument("--base", default="https://openrouter.ai/api/v1")
ap.add_argument("--key-env", default="OPENROUTER_API_KEY")
ap.add_argument("--cells", default="E,D,A,W")
ap.add_argument("--variants", default="plain,index")
ap.add_argument("--task-ids", default="", help="comma-separated subset, default all")
ap.add_argument("--k", type=int, default=3)
ap.add_argument("--turn-cap", type=int, default=6)
ap.add_argument("--max-requests", type=int, default=600)
ap.add_argument("--max-spend", type=float, default=0.0, help="dollars, required for a live run")
ap.add_argument("--prior-spend", type=float, default=0.0, help="dollars already spent by earlier P3 runs")
ap.add_argument("--max-output", type=int, default=4096)
ap.add_argument("--temperature", type=float, default=0.0)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--timeout", type=float, default=300.0)
ap.add_argument("--pause", type=float, default=0.0)
ap.add_argument("--out")
ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--analyze", metavar="RUN_DIR")
ap.add_argument("--summary", help="with --analyze: where to write the committable summary JSON")
a = ap.parse_args()

CORE_NAMES = ["supervisor__show_active_task", "supervisor__show_profile", "supervisor__show_addresses",
              "supervisor__show_payment_cards", "supervisor__show_account_passwords"]
APPS_SKIPPED = {"api_docs.json", "supervisor.json"}
SYSTEM = ("You are a personal assistant for one user and act in the user's apps on their behalf. The user is signed in to every app: "
          "wherever a tool asks for an access_token, pass \"tok-demo\". Carry out the request, then reply in one or two sentences.")
INDEX_LINE = " Tool categories beyond the tools listed: {apps}."
SEARCH_DEF = {"type": "function", "function": {"name": "search_tools", "description": "Search the catalogue of further tools by "
              "keywords. Returns the full definitions of the best matches.", "parameters": {"type": "object", "properties": {
              "query": {"type": "string", "description": "keywords describing the tool you need"}}, "required": ["query"]}}}
CALL_DEF = {"type": "function", "function": {"name": "call_tool", "description": "Run a tool from the catalogue by its exact name.",
            "parameters": {"type": "object", "properties": {"name": {"type": "string", "description": "exact tool name"},
            "arguments": {"type": "object", "description": "the tool's arguments"}}, "required": ["name", "arguments"]}}}
STUB = json.dumps({"status": "ok", "message": "Done."})


def summarize(run_dir, out_path):
    """counts per cell and variant from sessions.jsonl; task ids only, no tool names or AppWorld text"""
    ss = [json.loads(l) for l in open(os.path.join(run_dir, "sessions.jsonl"), encoding="utf-8")]
    rq = [json.loads(l) for l in open(os.path.join(run_dir, "requests.jsonl"), encoding="utf-8")]
    meta = json.load(open(os.path.join(run_dir, "run-meta.json"), encoding="utf-8"))
    cells = {}
    for s in ss:
        c = cells.setdefault(f"{s['cell']}-{s['variant']}", dict(sessions=0, complete=0, outcome={}, searched=0, target_called=0,
                             target_in_search_results=0, target_called_unseen=0, distractor_called=0, other_catalogue_called=0,
                             requests=0, failed_tasks=[]))
        c["sessions"] += 1
        c["requests"] += s["requests"]
        if not s["complete"]:
            c["failed_tasks"].append(s["task"])
            continue
        c["complete"] += 1
        c["outcome"][s["outcome"]] = c["outcome"].get(s["outcome"], 0) + 1
        c["searched"] += s["searches"] > 0
        c["target_called"] += s["target_called"]
        c["target_in_search_results"] += s["target_best_rank"] is not None
        c["target_called_unseen"] += s["target_called_unseen"]
        c["distractor_called"] += s["distractor_called"]
        c["other_catalogue_called"] += s["other_catalogue_calls"] > 0
    per_task = {}
    for s in ss:
        per_task.setdefault(s["task"], {})[f"{s['cell']}-{s['variant']}"] = s["outcome"] if s["complete"] else "incomplete"
    ok = [r for r in rq if r["status"] == 200]
    out = dict(run=os.path.basename(run_dir.rstrip("/")), model=meta["model"], provider=meta["provider"],
               harness_sha256=meta["harness_sha256"], tasks_sha256=meta["tasks_sha256"], catalogue_sha256=meta["catalogue_sha256"],
               catalogue_tools=meta["catalogue_tools"], k=meta["k"], temperature=meta["temperature"],
               served=sorted({f"{r.get('provider')}|{r.get('served_model')}" for r in ok}),
               requests=len(rq), requests_ok=len(ok), cost=round(sum((r.get("cost") or 0) for r in ok), 5),
               prompt_tokens=sum(r.get("prompt") or 0 for r in ok), cached_tokens=sum(r.get("cached") or 0 for r in ok),
               completion_tokens=sum(r.get("completion") or 0 for r in ok), cells=cells, per_task=per_task)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
    print(f"{out['model']} via {out['provider']}: {out['requests_ok']}/{out['requests']} requests ok, ${out['cost']}")
    print(f"{'cell':12} {'done':>4} {'srch':>4} {'tgt':>4} {'inres':>5} {'unseen':>6} {'distr':>5} {'other':>5}  outcomes")
    for k in sorted(cells):
        c = cells[k]
        print(f"{k:12} {c['complete']:>4} {c['searched']:>4} {c['target_called']:>4} {c['target_in_search_results']:>5} "
              f"{c['target_called_unseen']:>6} {c['distractor_called']:>5} {c['other_catalogue_called']:>5}  {c['outcome']}")


if a.analyze:
    summarize(a.analyze, a.summary or os.path.join(a.analyze, "summary.json"))
    sys.exit(0)

for need in ("catalogue", "tasks", "model", "provider", "out"):
    if not getattr(a, need):
        sys.exit(f"--{need} is required")

# ---------------------------------------------------------------- catalogue and tasks
files = sorted(glob.glob(os.path.join(os.path.expanduser(a.catalogue), "*.json")))
cat_hash = hashlib.sha256()
defs, apps = {}, []
for f in files:
    raw = open(f, "rb").read()
    cat_hash.update(os.path.basename(f).encode() + b"\0" + raw)
    base = os.path.basename(f)
    items = json.loads(raw)
    if base not in APPS_SKIPPED:
        apps.append(base[:-5])
    for x in items:
        if base == "api_docs.json":
            continue
        fn = x["function"]
        defs[fn["name"]] = {"type": "function", "function": {"name": fn["name"], "description": fn.get("description", ""),
                                                             "parameters": fn.get("parameters", {"type": "object", "properties": {}})}}
CORE = [defs[n] for n in CORE_NAMES]
APP_TOOLS = [d for n, d in defs.items() if not n.startswith("supervisor__")]
tasks_raw = open(a.tasks, "rb").read()
TASKS = json.loads(tasks_raw)
if a.task_ids:
    keep = set(a.task_ids.split(","))
    TASKS = [t for t in TASKS if t["id"] in keep]
for t in TASKS:
    for k in ("target", "distractor"):
        if t[k] not in defs:
            sys.exit(f"{t['id']}: {k} {t[k]} not in the catalogue")


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", s.lower().replace("__", " ").replace("_", " ")) if w]


def doc_text(d):
    fn = d["function"]
    props = fn.get("parameters", {}).get("properties", {})
    return " ".join([fn["name"], fn.get("description", "")] + list(props) + [str(v.get("description", "")) for v in props.values()])


class BM25:
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


def setup(task, cell, variant):
    """tools array, system text and searchable catalogue for one session"""
    system = SYSTEM + (INDEX_LINE.format(apps=", ".join(sorted(apps))) if variant == "index" else "")
    if cell == "E":
        return CORE + APP_TOOLS, system, None
    searchable = [d for d in APP_TOOLS if not (cell == "A" and d["function"]["name"] == task["target"])]
    tools = CORE + ([defs[task["distractor"]]] if cell == "W" else []) + [SEARCH_DEF, CALL_DEF]
    return tools, system, searchable


SESSIONS = []
for t in TASKS:
    for cell in a.cells.split(","):
        for v in (["plain"] if cell == "E" else a.variants.split(",")):
            SESSIONS.append((t, cell, v))

meta = dict(model=a.model, provider=a.provider, base=a.base, cells=a.cells, variants=a.variants, k=a.k, turn_cap=a.turn_cap,
            temperature=a.temperature, seed=a.seed, max_output=a.max_output, max_spend=a.max_spend, prior_spend=a.prior_spend,
            harness_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), tasks_sha256=hashlib.sha256(tasks_raw).hexdigest(),
            catalogue_sha256=cat_hash.hexdigest(), catalogue_tools=len(APP_TOOLS), core=CORE_NAMES, apps=sorted(apps),
            tasks=[t["id"] for t in TASKS], sessions_planned=len(SESSIONS), started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
os.makedirs(a.out, exist_ok=True)

if a.dry_run:
    tot = 0
    for t, cell, v in SESSIONS[: len(SESSIONS) // len(TASKS)]:
        tools, system, searchable = setup(t, cell, v)
        ch = len(json.dumps(tools)) + len(system)
        tot += ch
        print(f"{cell}-{v:6} tools {len(tools):>4}  prefix about {ch // 4:>6} tokens (chars/4)  searchable {len(searchable or [])}")
    print(f"{len(TASKS)} tasks, {len(SESSIONS)} sessions; first-request prefix per task about {tot // 4} tokens; catalogue "
          f"{len(APP_TOOLS)} app tools + {len(CORE)} core; catalogue sha256 {cat_hash.hexdigest()[:12]}")
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
for si, (task, cell, variant) in enumerate(SESSIONS, 1):
    if stop:
        break
    tools, system, searchable = setup(task, cell, variant)
    index = BM25(searchable) if searchable is not None else None
    names_visible = {d["function"]["name"] for d in tools}
    names_searchable = {d["function"]["name"] for d in searchable or []}
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": task["prompt"]}]
    called, seen, ranks, searches, complete, nreq, capped = [], set(), [], 0, False, 0, False
    listed, rule_stage = False, None
    for step in range(1, a.turn_cap + 1):
        if n_req >= a.max_requests:
            stop = "max-requests"
            break
        if a.prior_spend + spent >= a.max_spend:
            stop = "max-spend"
            break
        body = dict(model=a.model, messages=msgs, tools=tools, tool_choice="auto", temperature=a.temperature, seed=a.seed,
                    max_tokens=a.max_output)
        status, j, secs = post(body)
        if status in (429, 500, 502, 503, 504, None):
            time.sleep(20)
            status, j, secs = post(body)
        n_req += 1
        nreq += 1
        rec = dict(session=si, task=task["id"], cell=cell, variant=variant, step=step, status=status, seconds=secs)
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
                   tool_calls=[], search_queries=[], search_target_rank=[])
        if not tcs:
            rec["reply_head"] = scrub(msg.get("content") or "")[:240]  # local log only, for adjudicating 'answer without a tool'
            req_log.write(json.dumps(rec) + "\n"); req_log.flush()
            complete = True
            break
        amsg = {"role": "assistant", "content": msg.get("content") or "", "tool_calls": tcs}
        if msg.get("reasoning_details"):
            amsg["reasoning_details"] = msg["reasoning_details"]
        msgs.append(amsg)
        for tc in tcs:
            fn = tc.get("function") or {}
            name = fn.get("name") or ""
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = None
            if name == "search_tools" and index is not None:
                searches += 1
                q = (args or {}).get("query", "") if isinstance(args, dict) else ""
                hits = index.rank(str(q))
                top = hits[: a.k]
                fresh = [n for n in top if n not in seen]
                seen.update(top)
                rank = hits.index(task["target"]) + 1 if task["target"] in hits else None
                ranks.append(rank)
                rec["tool_calls"].append("search_tools")
                rec["search_queries"].append(scrub(str(q))[:200])
                rec["search_target_rank"].append(rank)
                result = json.dumps([defs[n]["function"] for n in top]) if top else json.dumps({"result": "no matching tools"})
                if variant == "rule" and not fresh:  # NO-MATCH RULE (run 2): this search brought nothing not already shown
                    if top and not listed:
                        hit_apps = sorted({n.split("__")[0] for n in top})
                        listing = [{"name": d["function"]["name"], "description": d["function"]["description"].split(". ")[0]}
                                   for d in searchable if d["function"]["name"].split("__")[0] in hit_apps]
                        seen.update(x["name"] for x in listing)
                        listed, rule_stage = True, "listing"
                        result = json.dumps({"note": "Nothing new: every match was already shown. Below is every tool of " +
                                             ", ".join(hit_apps) + ". If none of them does what is needed, the catalogue has no "
                                             "such tool.", "tools": listing})
                    else:
                        rule_stage = "exhausted"
                        result = json.dumps({"note": "Nothing new: no tool beyond those already shown matches. The catalogue "
                                             "has no further tool for this need."})
                rec.setdefault("rule_stage", []).append(rule_stage)
            elif name == "call_tool" and index is not None:
                inner = str((args or {}).get("name", "")) if isinstance(args, dict) else ""
                rec["tool_calls"].append("call_tool:" + inner)
                if inner in names_searchable or inner in names_visible:
                    called.append((inner, inner in seen or inner in names_visible))
                    result = STUB
                else:
                    called.append((inner, False))
                    result = json.dumps({"error": f"unknown tool: {inner}"})
            else:
                rec["tool_calls"].append(name)
                if name in names_visible:
                    called.append((name, True))
                    result = STUB
                else:
                    called.append((name, False))
                    result = json.dumps({"error": f"unknown tool: {name}"})
            msgs.append({"role": "tool", "tool_call_id": tc.get("id") or "", "content": result})
        req_log.write(json.dumps(rec) + "\n"); req_log.flush()
        if a.pause:
            time.sleep(a.pause)
    else:
        capped = complete = True  # the turn cap ended the session while the model was still calling tools
    target = task["target"]
    cat_calls = [(n, v) for n, v in called if n not in CORE_NAMES and n in defs]
    target_called = any(n == target for n, _ in cat_calls)
    others = [n for n, _ in cat_calls if n != target]
    if not complete:
        outcome = "incomplete"
    elif capped and not target_called and not others:
        outcome = "turn cap reached, searched" if searches else "turn cap reached, zero searches"
    elif cell == "A":
        outcome = ("wrong-tool call" if others else "called the absent tool by name" if target_called else "searched, no call" if searches else "answer without a tool, zero searches")
    elif target_called:
        first_other = others and [n for n, _ in cat_calls].index(others[0]) < [n for n, _ in cat_calls].index(target)
        outcome = ("correct after a wrong call" if first_other else "search then correct call" if searches else
                   "correct call, zero searches")
    elif others:
        outcome = "wrong-tool call"
    else:
        outcome = "answer without a tool, searched" if searches else "answer without a tool, zero searches"
    srec = dict(session=si, task=task["id"], cell=cell, variant=variant, complete=complete, capped=capped, requests=nreq, searches=searches,
                target_best_rank=min([r for r in ranks if r], default=None), target_called=target_called,
                target_called_unseen=any(n == target and not v for n, v in cat_calls),
                distractor_called=any(n == task["distractor"] for n, _ in cat_calls), other_catalogue_calls=len(others),
                core_calls=sum(1 for n, _ in called if n in CORE_NAMES), rule_stage=rule_stage, outcome=outcome)
    ses_log.write(json.dumps(srec) + "\n"); ses_log.flush()
    print(f"[{si}/{len(SESSIONS)}] {task['id']} {cell}-{variant:5} {outcome}; searches {searches}; requests {n_req}; "
          f"spent ${spent:.4f}", flush=True)

meta.update(ended_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), requests=n_req, spent=round(spent, 5),
            stop=stop or "done")
with open(os.path.join(a.out, "run-meta.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(meta, f, indent=1)
print(f"stop: {stop or 'done'}; requests {n_req}; spent ${spent:.4f} (P3 total ${a.prior_spend + spent:.4f} of ${a.max_spend})")
