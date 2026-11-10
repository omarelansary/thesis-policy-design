#!/usr/bin/env python
"""P1 harness (AUTH-033, INT-T-054): does memory-informed offering help returning users, on the bill and on accuracy?
(`design/package-v5/05` P1, HYP-0017; plan in `design/package-v5/inputs/p1/P1-PREP.md` sections 7 and 8.)

AppWorld's own `simplified_function_calling` agent, its prompts as shipped (instructions.txt, demos.json), step cap 50, its
evaluator, a new AppWorld root and experiment per run (AppWorld issue #203), as in `p2_offering.py`. Changes, and only these:
  1. Declared tools at the start: CORE (every supervisor API and every app's login API) + the search tool `tools__search` + the
     arm's SEEDS. The name has exactly one `__` because AppWorld's agent skips any other name.
  2. Search: a `tools__search` call's code is replaced by a `print` of the top --k BM25 matches (P3's ranker) over all non-core
     APIs of all apps, as full definitions; matches not yet declared are appended to the declared tools from the next request
     (V5's discovery after the prefix). Nothing tells the model to search; the tool's description says what it does.
  3. No stop rule (every task is doable; P1-PREP section 8).
Arms (one per run): none (no seeds); pop6 (the six non-core APIs most often needed by other users' sessions outside this
session's scenario, from AppWorld's gold; P1-PREP section 7); oracle (this session's own gold non-core APIs, an upper bound).
Sessions: the returning sessions of AppWorld's 34 returning users (train and dev; the second session onward, in date order).
Recorded per model call (local trace): tokens, billed cost, provider, tools declared, tool calls; per task: searches, seeds
called, seeds called that the task does not need, discovered tools. Stops: --max-spend (billed), --max-calls, HTTP 401/402/403,
two failed calls in a row, two tasks in a row with an exception, a provider other than the pinned one.
Keys only from the environment variable named by --key-env; never printed or written. --dry-run sends no request.
Usage: ~/r3-work/venv/bin/python design/package-v5/tools/p1_memory.py --tag p1-smoke --arm none --model z-ai/glm-5.3 \
  --base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --provider GMICloud --price 0.70,0.13,2.2 --max-spend 1 --limit 3
"""
import argparse, collections, datetime, json, math, os, pathlib, re, sys, time, traceback

WS = pathlib.Path(__file__).resolve().parents[3]
AW = pathlib.Path(os.path.expanduser("~/r3-work"))
ap = argparse.ArgumentParser()
ap.add_argument("--tag", required=True)
ap.add_argument("--arm", choices=["none", "pop6", "oracle"], required=True)
ap.add_argument("--model", required=True)
ap.add_argument("--base", default="https://openrouter.ai/api/v1")
ap.add_argument("--key-env", default="OPENROUTER_API_KEY")
ap.add_argument("--provider", default="GMICloud")
ap.add_argument("--temperature", type=float, default=0.0)
ap.add_argument("--seed", type=int, default=100)
ap.add_argument("--timeout", type=float, default=600.0)
ap.add_argument("--k", type=int, default=3, help="matches per search")
ap.add_argument("--price", default="", help="input,cached_input,output dollars per million tokens (computed cost beside the billed one)")
ap.add_argument("--max-spend", type=float, default=0.0)
ap.add_argument("--max-calls", type=int, default=5000)
ap.add_argument("--ids", nargs="*")
ap.add_argument("--limit", type=int)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

RUN = WS / "design/package-v5/inputs/p1/local/runs" / args.tag
if RUN.exists():
    sys.exit(f"{RUN} already exists: every run needs a new tag; nothing was run")
(RUN / "trace").mkdir(parents=True)
os.symlink(AW / "aw-root" / "data", RUN / "data")
os.environ.update({"APPWORLD_ROOT": str(RUN), "PYTHON_DOTENV_DISABLED": "1", "OPENAI_BASE_URL": args.base,
                   "MODEL_SERVER_URL": args.base, "OPENAI_API_BASE": args.base,
                   "APPWORLD_EXPERIMENT_PROMPTS_PATH": str(AW / "appworld-src/experiments/prompts")})
key = os.environ.get(args.key_env, "")
if not key and not args.dry_run:
    sys.exit(f"{args.key_env} is not set; nothing was run")
if not args.dry_run and args.max_spend <= 0:
    sys.exit("a live run needs --max-spend (AUTH-033 limits); nothing was run")
os.environ["OPENAI_API_KEY"] = key or "dry-run-no-key"
del key
PRICE = [float(x) / 1e6 for x in args.price.split(",")] if args.price else [0.0, 0.0, 0.0]
DATA = AW / "aw-root" / "data"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now():
    return os.times().elapsed  # AppWorld freezes the clock inside a task


def log(msg):
    with open(RUN / "progress.log", "a") as f:
        f.write(f"{utc()} {msg}\n")
    print(f"{utc()} {msg}", file=sys.__stderr__, flush=True)


# ---- returning sessions and seeds (the same construction as tools/p1_recurrence.py and tools/p1_seed_rules.py)
def is_core(api):  # "app.api" or "app__api"
    app, name = re.split(r"\.|__", api, maxsplit=1)
    return app == "supervisor" or name == "login"


task_ids = []
for split in ("train", "dev"):
    task_ids += [l.strip() for l in open(DATA / "datasets" / f"{split}.txt") if l.strip()]
users = {}
for t in task_ids:
    s = json.load(open(DATA / "tasks" / t / "specs.json"))
    need = {a.replace(".", "__") for a in json.load(open(DATA / "tasks" / t / "ground_truth" / "required_apis.json")) if not is_core(a)}
    users.setdefault(s["supervisor"]["email"], {}).setdefault(t.split("_")[0], (s["datetime"], t, need))
sessions = {u: sorted(sc.values()) for u, sc in users.items()}
NEED = {t: need for ss in sessions.values() for _, t, need in ss}
RETURNING = [ss[i][1] for ss in sessions.values() for i in range(1, len(ss))]
OWNER = {t: u for u, ss in sessions.items() for _, t, _ in ss}


def seeds_for(tid):
    if args.arm == "none":
        return []
    if args.arm == "oracle":
        return sorted(NEED[tid])
    scen, u = tid.split("_")[0], OWNER[tid]
    c = collections.Counter(a for v, ss in sessions.items() if v != u for _, t, need in ss if t.split("_")[0] != scen for a in need)
    return [a for a, _ in c.most_common(6)]


ids = args.ids or RETURNING
bad = [t for t in ids if t not in set(RETURNING)]
if bad:
    sys.exit(f"not returning sessions: {bad}; nothing was run")
if args.limit:
    ids = ids[: args.limit]

sys.stdout = open(RUN / "console.log", "a", buffering=1)  # agent output holds task text: local file only

import appworld_agents.code.simplified.language_model as lmm  # noqa: E402
from appworld import AppWorld  # noqa: E402
from appworld.evaluator import evaluate_tasks  # noqa: E402
from appworld_agents.code.simplified.agent import Agent, Status  # noqa: E402
from appworld_agents.code.common.usage_tracker import Usage  # noqa: E402
from appworld_agents.code.simplified.function_calling_agent import SimplifiedFunctionCallingAgent  # noqa: E402


class Stop(BaseException):
    pass


CUR = {"task": None, "spend": 0.0, "calls": 0, "fail_streak": 0, "seeds": [], "searches": 0, "discovered": set(), "called": []}
TRACE = RUN / "trace" / "calls.jsonl"
SEARCH_NAME = "tools__search"
SEARCH_DEF = {"type": "function", "function": {"name": SEARCH_NAME, "description": "Search the catalogue of further tools by "
              "keywords. Returns the full definitions of the best matches; they can be called directly afterwards.",
              "parameters": {"type": "object", "properties": {"query": {"type": "string",
                             "description": "keywords describing the tool you need"}}, "required": ["query"]}}}


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", s.lower().replace("__", " ").replace("_", " ")) if w]


def doc_text(d):
    fn = d["function"]
    props = fn.get("parameters", {}).get("properties", {})
    return " ".join([fn["name"], fn.get("description", "")] + list(props) + [str(v.get("description", "")) for v in props.values()])


class BM25:  # the ranker of p3_uninstructed_search.py and p3_two_need.py
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
        return [self.docs[i] for _, i in scores]


@Agent.register("p1_memory_function_calling")
class P1Agent(SimplifiedFunctionCallingAgent):  # type: ignore[misc]
    def _clean(self, d):
        d = json.loads(json.dumps(d))
        for _, info in d["function"].get("parameters", {}).get("properties", {}).items():
            for k in self.remove_function_property_keys:
                info.pop(k, None)
        return d

    def first_execution_inputs_usage_and_status(self):
        docs = self.world.task.api_docs.function_calling()
        byname = {d["function"]["name"]: d for d in docs}
        core = [self._clean(d) for d in docs if is_core(d["function"]["name"])]
        self.index = BM25([self._clean(d) for d in docs if not is_core(d["function"]["name"])])
        missing = [n for n in CUR["seeds"] if n not in byname]
        if missing:
            return [], Usage(), Status(failed=True, message=f"seeds outside the catalogue: {missing}")
        seeds = [self._clean(byname[n]) for n in CUR["seeds"]]
        self.functions = core + [SEARCH_DEF] + seeds
        CUR.update(declared_start=len(self.functions), core=len(core), catalogue=len(self.index.docs))
        return [], Usage(), Status(failed=False)

    def second_onwards_execution_inputs_usage_and_status(self, last_execution_outputs):
        inputs, usage, status = super().second_onwards_execution_inputs_usage_and_status(last_execution_outputs)
        calls = {tc.get("call_id", tc.get("id")): tc for tc in (self.messages[-1].get("tool_calls") or [])} if self.messages else {}
        declared = {d["function"]["name"] for d in self.functions}
        for ei in inputs:
            name = ei.metadata["function_name"]
            CUR["called"].append(name)
            if name != SEARCH_NAME:
                continue
            CUR["searches"] += 1
            try:
                query = str(json.loads(calls[ei.metadata["id"]]["function"]["arguments"]).get("query", ""))
            except Exception:
                query = ""
            top = self.index.rank(query)[: args.k]
            for d in top:
                if d["function"]["name"] not in declared:
                    self.functions.append(d)
                    declared.add(d["function"]["name"])
                    CUR["discovered"].add(d["function"]["name"])
            text = json.dumps({"matches": [d["function"] for d in top]} if top else {"matches": [], "note": "No tool matches."})
            ei.content = f"print({text!r})"
        return inputs, usage, status


_OpenAI = lmm.OpenAI
lmm.OpenAI = lambda **kw: _OpenAI(timeout=args.timeout, **kw)
_orig_get = lmm.get_raw_lm_caller


def _get(*a, **kw):
    caller = _orig_get(*a, **kw)

    def wrapped(**ckw):
        if args.max_spend and CUR["spend"] >= args.max_spend:
            raise Stop(f"spend {CUR['spend']:.4f} reached --max-spend {args.max_spend}")
        if CUR["calls"] >= args.max_calls:
            raise Stop(f"calls reached --max-calls {args.max_calls}")
        ckw["extra_body"] = {**(ckw.get("extra_body") or {}),
                             "provider": {"order": [args.provider], "allow_fallbacks": False}, "usage": {"include": True}}
        rec = {"task": CUR["task"], "arm": args.arm, "n_tools": len(ckw.get("tools") or []), "n_items": len(ckw.get("messages") or [])}
        t0 = now()
        try:
            r = caller(**ckw)
        except Exception as e:
            rec.update(status="error", error=type(e).__name__, http=getattr(e, "status_code", None), latency_s=round(now() - t0, 2))
            with open(TRACE, "a") as f:
                f.write(json.dumps(rec) + "\n")
            if getattr(e, "status_code", None) in (401, 402, 403):
                raise Stop(f"endpoint refused with HTTP {e.status_code}") from None
            CUR["fail_streak"] += 1
            if CUR["fail_streak"] >= 2:
                raise Stop(f"two failed model calls in a row ({type(e).__name__}, HTTP {getattr(e, 'status_code', None)})") from None
            raise
        CUR["fail_streak"] = 0
        d = r.model_dump() if hasattr(r, "model_dump") else dict(r)
        u = d.get("usage") or {}
        det, cdet = u.get("prompt_tokens_details") or {}, u.get("completion_tokens_details") or {}
        prompt, cached, completion = u.get("prompt_tokens") or 0, det.get("cached_tokens") or 0, u.get("completion_tokens") or 0
        cost = (prompt - cached) * PRICE[0] + cached * PRICE[1] + completion * PRICE[2]
        or_cost = u.get("cost")
        if d.get("provider") and d.get("provider") != args.provider:
            raise Stop(f"served by {d.get('provider')}, not the pinned {args.provider}")
        CUR["spend"] += or_cost if or_cost is not None else cost
        CUR["calls"] += 1
        msg = ((d.get("choices") or [{}])[0].get("message")) or {}
        names = [((tc.get("function") or {}).get("name") or "") for tc in (msg.get("tool_calls") or [])]
        rec.update(status="ok", model=d.get("model"), provider=d.get("provider"), prompt=prompt, cached=cached, completion=completion,
                   reasoning=cdet.get("reasoning_tokens"), cost=round(cost, 6), or_cost=or_cost, tool_calls=names,
                   latency_s=round(now() - t0, 2))
        with open(TRACE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return r
    return wrapped


lmm.get_raw_lm_caller = _get

model_config = {"client_name": "openai", "api_type": "chat_completions", "name": args.model, "base_url": args.base,
                "temperature": args.temperature, "drop_reasoning_content": False, "seed": args.seed,
                "cost_per_token": {"input_cache_hit": PRICE[1], "input_cache_miss": PRICE[0], "input_cache_write": 0.0, "output": PRICE[2]},
                "retry_after_n_seconds": 15, "use_cache": False, "max_retries": 20}
P = os.environ["APPWORLD_EXPERIMENT_PROMPTS_PATH"]
agent_config = {
    "type": "p1_memory_function_calling",
    "model_config": {**model_config, "tool_choice": "auto", "parallel_tool_calls": True},
    "api_predictor_config": {"mode": "all", "model_config": dict(model_config), "prompt_file_path": P + "/api_predictor.txt",
                             "demo_task_ids": ["82e2fac_1", "29caf6f_1", "d0b1f43_1"], "max_predicted_apis": 1000},
    "appworld_config": {"random_seed": 100, "raise_on_extra_parameters": True, "include_direct_functions": True,
                        "direct_function_separator": "__"},
    "logger_config": {"color": False, "verbose": True},
    "usage_tracker_config": {"max_cost_overall": 1000, "max_cost_per_task": 10, "max_output_tokens_per_task": 100000},
    "prompt_file_path": P + "/function_calling_agent/instructions.txt",
    "demo_messages_file_path": P + "/function_calling_agent/demos.json",
    "max_steps": 50, "log_lm_calls": True, "skip_if_finished": False,
}
meta = dict(tag=args.tag, arm=args.arm, model=args.model, base=args.base, provider=args.provider, seed=args.seed,
            temperature=args.temperature, timeout=args.timeout, k=args.k, price=args.price, max_spend=args.max_spend, tasks=ids,
            effort="as served (no reasoning field)", started=utc(),
            harness_sha256=__import__("hashlib").sha256(open(__file__, "rb").read()).hexdigest())
(RUN / "run-meta.json").write_text(json.dumps(meta, indent=1))
log(f"run {args.tag}: arm {args.arm}, model {args.model}, {len(ids)} returning sessions, dry_run {args.dry_run}")
agent = Agent.from_dict(agent_config)
if args.dry_run:
    from appworld.task import Task
    t = Task.load(ids[0])
    docs = t.api_docs.function_calling()
    core = [d for d in docs if is_core(d["function"]["name"])]
    log(f"dry run: {len(docs)} APIs, core {len(core)}, searchable {len(docs) - len(core)}; seeds of the first session "
        f"{len(seeds_for(ids[0]))}, all in catalogue {all(n in {d['function']['name'] for d in docs} for n in seeds_for(ids[0]))}; "
        f"{len(ids)} sessions; no call made")
    sys.exit(0)

stats = {"meta": meta, "tasks": {}}
exp = args.tag
agent.logger.initialize(experiment_name=exp, num_tasks=len(ids), num_processes=1, process_index=0)
code, streak = 0, 0
with AppWorld.initializer(update_defaults=True, experiment_name=exp, **agent.appworld_config):
    for i, tid in enumerate(ids, 1):
        CUR.update(task=tid, seeds=seeds_for(tid), searches=0, discovered=set(), called=[])
        t0, c0, s0 = now(), CUR["calls"], CUR["spend"]
        rec = {"index": i, "exception": None, "seeds": len(CUR["seeds"])}
        try:
            agent.solve_task(tid)
        except Stop as e:
            log(f"STOP at task {i} ({tid}): {e}")
            rec["exception"] = "Stop"
            stats["tasks"][tid] = rec
            stats["stopped"] = str(e)
            code = 3
            break
        except Exception as e:
            rec["exception"] = type(e).__name__
            print(traceback.format_exc())
            streak += 1
        else:
            streak = 0
        called = [n for n in CUR["called"] if n != SEARCH_NAME]
        rec.update(steps=agent.step_number, seconds=round(now() - t0, 1), calls=CUR["calls"] - c0, spend=round(CUR["spend"] - s0, 6),
                   searches=CUR["searches"], discovered=len(CUR["discovered"]), declared_start=CUR.get("declared_start"),
                   seeds_called=len(set(CUR["seeds"]) & set(called)),
                   seeds_called_not_needed=len((set(CUR["seeds"]) & set(called)) - NEED[tid]),
                   needed=len(NEED[tid]), needed_called=len(NEED[tid] & set(called)))
        stats["tasks"][tid] = rec
        (RUN / "stats.json").write_text(json.dumps(stats, indent=1))
        log(f"task {i}/{len(ids)} {tid}: steps {rec['steps']}, calls {rec['calls']}, searches {rec['searches']}, seeds called "
            f"{rec['seeds_called']}/{rec['seeds']}, ${rec['spend']:.4f}, exception {rec['exception']}, spend ${CUR['spend']:.4f}")
        if streak >= 2:
            log("STOP: two tasks in a row ended with an exception")
            stats["stopped"] = "two exceptions"
            code = 4
            break
done = [t for t in ids if stats["tasks"].get(t, {}).get("exception") is None]
try:
    ev = evaluate_tasks(task_ids=done, experiment_name=exp, suppress_errors=True, include_details=True, save_reports=True)
except Exception as e:
    ev = {"evaluation_error": f"{type(e).__name__}: {e}"}
(RUN / "evaluation.json").write_text(json.dumps(ev, indent=1, default=str))
stats["finished"] = utc()
stats["spend"] = round(CUR["spend"], 6)
(RUN / "stats.json").write_text(json.dumps(stats, indent=1))
log(f"run {args.tag} finished, exit {code}; spend ${CUR['spend']:.4f}; calls {CUR['calls']}")
sys.exit(code)
