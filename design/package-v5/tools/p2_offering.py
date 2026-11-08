#!/usr/bin/env python
"""P2 harness (INT-T-040, preparation only): does offering a subset of the declared tools at a fixed cached prefix keep task accuracy
nearly the same? (`design/package-v5/05` P2, HYP-0018; design in `design/package-v5/inputs/p2/P2-DESIGN.md`.)

Run with the AppWorld environment's Python (AppWorld 0.2.0 data and its experiments package), for example
  ~/r3-work/venv/bin/python design/package-v5/tools/p2_offering.py --tag p2-dry --arm all --model gpt-5-mini --dry-run
Modeled on the other agent's AppWorld driver ~/r3-work/run_partb.py (AUTH-024..027): AppWorld's own `simplified_function_calling`
agent, its prompts (function_calling_agent/instructions.txt and demos.json, 3-shot), step cap 50, AppWorld's own evaluator,
a new AppWorld root and experiment name per run (AppWorld issue #203). Two hooks only, everything else is AppWorld's code:
  1. Declared tools. The agent's first step normally picks the predicted APIs. Here the declared list is the FIXED catalogue:
     the function-calling definitions of supervisor (6), spotify (92) and phone (30) = 128 tools, in a fixed order, the same for
     every task (OpenAI accepts at most 128 tools per request, `17` section 5, R1 part 3). Arm `drop` declares only the subset.
  2. What is offered. SUBSET = the task's ground-truth required APIs (AppWorld ground truth, dev split) plus
     supervisor__complete_task: an oracle subset, so P2 tests the mechanism, not a predictor.
Arms (one per run):
  all     128 declared, tool_choice "auto"                                   (reference: everything offered)
  enf     128 declared, tool_choice allowed_tools(mode auto, SUBSET)         (server-enforced offering; OpenAI)
  instr   128 declared, tool_choice "auto", one sentence appended to the task message naming SUBSET (no enforcement; portable)
  drop    only SUBSET declared, tool_choice "auto"                           (removal; the prefix differs per task)
Recorded per model call (local trace, counts and tool names): prompt, cached, completion and reasoning tokens, served model id,
number of tools declared, tool calls and how many fell outside SUBSET, cost from --price. Per task: steps, exception, and
AppWorld's evaluation (success, pass and fail counts). AppWorld text and tool names stay in the git-excluded run folder
design/package-v5/inputs/p2/local/runs/<tag>/; `tools/p2_analyze.py` writes the committable counts.
Stops: --max-spend (summed computed cost), --max-calls, HTTP 401/402/403, two tasks in a row with an exception.
Keys only from the environment variable named by --key-env (default OPENAI_API_KEY); never printed or written.
No model request is sent with --dry-run. A live run needs the human's authorization with its cost (INT-T-040).
"""
import argparse, datetime, json, os, pathlib, sys, time, traceback

WS = pathlib.Path(__file__).resolve().parents[3]
AW = pathlib.Path(os.path.expanduser("~/r3-work"))
ap = argparse.ArgumentParser()
ap.add_argument("--tag", required=True, help="run name: experiment name and folder local/runs/<tag> (must be new)")
ap.add_argument("--arm", choices=["all", "enf", "instr", "drop"], required=True)
ap.add_argument("--model", required=True, help="OpenAI model id, e.g. gpt-5-mini or gpt-5.4-mini")
ap.add_argument("--base", default="https://api.openai.com/v1")
ap.add_argument("--api", choices=["chat_completions", "responses"], default="responses",
                help="responses is AppWorld's own setting for the gpt-5 family; gpt-5.4-mini refuses function tools with reasoning on chat")
ap.add_argument("--key-env", default="OPENAI_API_KEY")
ap.add_argument("--reasoning-effort", default="low", choices=["minimal", "low", "medium", "high"])
ap.add_argument("--temperature", type=float, default=1.0, help="gpt-5 family accepts only the default 1.0")
ap.add_argument("--seed", type=int, default=None, help="sent as the request seed when given (P2b on ScaDS: 100, as R3 Part B)")
ap.add_argument("--no-reasoning-param", action="store_true", help="send no reasoning field (ScaDS: reasoning as served)")
ap.add_argument("--min-interval", type=float, default=0.0, help="seconds between model calls (ScaDS GLM-5.3: 2 per minute, use 31)")
ap.add_argument("--retry-429", type=int, default=0, help="retry a rate-limited call this many times after --min-interval + 5 s")
ap.add_argument("--price", default="", help="input,cached_input,output dollars per million tokens (required for a live run)")
ap.add_argument("--max-spend", type=float, default=0.0)
ap.add_argument("--max-calls", type=int, default=3000)
ap.add_argument("--ids", nargs="*", help="task ids (dev split, apps within the catalogue); default all eligible")
ap.add_argument("--limit", type=int)
ap.add_argument("--apps", default="supervisor,spotify,phone", help="catalogue apps, in this order")
ap.add_argument("--dry-run", action="store_true", help="build agent, catalogue and subsets; print sizes; call nothing")
args = ap.parse_args()

APPS = args.apps.split(",")
RUN = WS / "design/package-v5/inputs/p2/local/runs" / args.tag
if RUN.exists():
    sys.exit(f"{RUN} already exists: every run needs a new tag (AppWorld issue #203); nothing was run")
(RUN / "trace").mkdir(parents=True)
os.symlink(AW / "aw-root" / "data", RUN / "data")
os.environ.update({"APPWORLD_ROOT": str(RUN), "PYTHON_DOTENV_DISABLED": "1", "OPENAI_BASE_URL": args.base, "MODEL_SERVER_URL": args.base, "OPENAI_API_BASE": args.base,
                   "APPWORLD_EXPERIMENT_PROMPTS_PATH": str(AW / "appworld-src/experiments/prompts")})
key = os.environ.get(args.key_env, "")
if not key and not args.dry_run:
    sys.exit(f"{args.key_env} is not set; nothing was run")
if not args.dry_run and (args.max_spend <= 0 or not args.price):
    sys.exit("a live run needs --max-spend and --price (INT-T-040: a run needs its own authorization with its cost); nothing was run")
os.environ["OPENAI_API_KEY"] = key or "dry-run-no-key"
del key
PRICE = [float(x) / 1e6 for x in args.price.split(",")] if args.price else [0.0, 0.0, 0.0]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now():
    return os.times().elapsed  # AppWorld freezes the clock inside a task


def log(msg):
    with open(RUN / "progress.log", "a") as f:
        f.write(f"{utc()} {msg}\n")
    print(f"{utc()} {msg}", file=sys.__stderr__, flush=True)


sys.stdout = open(RUN / "console.log", "a", buffering=1)  # agent output holds task text: local file only

import appworld_agents.code.simplified.language_model as lmm  # noqa: E402
from appworld import AppWorld  # noqa: E402
from appworld.evaluator import evaluate_tasks  # noqa: E402
from appworld.task import load_task_ids  # noqa: E402
from appworld_agents.code.simplified.agent import Agent, Status  # noqa: E402
from appworld_agents.code.common.usage_tracker import Usage  # noqa: E402
from appworld_agents.code.simplified.function_calling_agent import SimplifiedFunctionCallingAgent  # noqa: E402


class Stop(BaseException):
    pass


CUR = {"task": None, "subset": [], "spend": 0.0, "calls": 0, "fail_streak": 0, "last_call": 0.0}
TRACE = RUN / "trace" / "calls.jsonl"
GT = AW / "aw-root/data/tasks"


def subset_for(task_id):
    apis = json.load(open(GT / task_id / "ground_truth" / "required_apis.json"))
    names = [a.replace(".", "__") for a in apis]
    if "supervisor__complete_task" not in names:
        names.insert(0, "supervisor__complete_task")
    return list(dict.fromkeys(names))


INSTR = ("For this task, call only these tools: {names}. Do not call any other tool.")


@Agent.register("p2_function_calling")
class P2Agent(SimplifiedFunctionCallingAgent):  # type: ignore[misc]
    """AppWorld's agent; only the declared tools (hook 1) and, for arm instr, one sentence in the task message change."""

    def initialize(self, world):
        super().initialize(world)
        if args.arm == "instr":
            last = self.messages[-1]
            assert last.get("role") == "user", "the task input is expected to be the last user message"
            last["content"] = (last.get("content") or "") + "\n\n" + INSTR.format(names=", ".join(CUR["subset"]))

    def first_execution_inputs_usage_and_status(self):
        docs = self.world.task.api_docs.function_calling()
        by_app = {a: [d for d in docs if d["function"]["name"].split("__", 1)[0] == a] for a in APPS}
        catalogue = [d for a in APPS for d in by_app[a]]
        if args.arm == "drop":
            catalogue = [d for d in catalogue if d["function"]["name"] in set(CUR["subset"])]
        self.functions = catalogue
        CUR["declared"] = len(catalogue)
        missing = [n for n in CUR["subset"] if n not in {d["function"]["name"] for d in catalogue}]
        if missing:
            return [], Usage(), Status(failed=True, message=f"subset outside the catalogue: {missing}")
        return [], Usage(), Status(failed=False)


_OpenAI = lmm.OpenAI
lmm.OpenAI = lambda **kw: _OpenAI(timeout=300.0, **kw)
_orig_get = lmm.get_raw_lm_caller


def _get(*a, **kw):
    caller = _orig_get(*a, **kw)

    def wrapped(**ckw):
        if args.max_spend and CUR["spend"] >= args.max_spend:
            raise Stop(f"spend {CUR['spend']:.4f} reached --max-spend {args.max_spend}")
        if CUR["calls"] >= args.max_calls:
            raise Stop(f"calls reached --max-calls {args.max_calls}")
        if args.arm == "enf" and ckw.get("tools"):
            if args.api == "chat_completions":  # the shape R1 tested on Chat Completions
                ckw["tool_choice"] = {"type": "allowed_tools", "allowed_tools": {"mode": "auto", "tools": [
                    {"type": "function", "function": {"name": n}} for n in CUR["subset"]]}}
            else:  # the flat Responses shape (R1: also accepted and enforced on OpenAI)
                ckw["tool_choice"] = {"type": "allowed_tools", "mode": "auto",
                                      "tools": [{"type": "function", "name": n} for n in CUR["subset"]]}
        rec = {"task": CUR["task"], "arm": args.arm, "api": args.api, "n_tools": len(ckw.get("tools") or []),
               "n_items": len(ckw.get("messages") or ckw.get("input") or [])}
        r, attempt = None, 0
        while True:
            if args.min_interval:
                wait = CUR["last_call"] + args.min_interval - time.time()
                if wait > 0:
                    time.sleep(wait)
            CUR["last_call"] = time.time()
            t0 = now()
            try:
                r = caller(**ckw)
                break
            except Exception as e:
                if getattr(e, "status_code", None) == 429 and attempt < args.retry_429:
                    attempt += 1
                    with open(TRACE, "a") as f:
                        f.write(json.dumps({**rec, "status": "rate_limited_retry", "attempt": attempt}) + "\n")
                    time.sleep(args.min_interval + 5)
                    continue
                err = e
                break
        if r is None:
            e = err
            rec.update(status="error", error=type(e).__name__, http=getattr(e, "status_code", None), latency_s=round(now() - t0, 2))
            with open(TRACE, "a") as f:
                f.write(json.dumps(rec) + "\n")
            if getattr(e, "status_code", None) in (401, 402, 403):
                raise Stop(f"endpoint refused with HTTP {e.status_code}") from None
            CUR["fail_streak"] += 1
            if CUR["fail_streak"] >= 2:  # added after the first gpt-5.4-mini pilot: AppWorld's agent absorbs failed calls
                raise Stop(f"two failed model calls in a row ({type(e).__name__}, HTTP {getattr(e, 'status_code', None)})") from None
            raise e
        CUR["fail_streak"] = 0
        d = r.model_dump() if hasattr(r, "model_dump") else dict(r)
        u = d.get("usage") or {}
        if "input_tokens" in u:  # Responses API
            det, cdet = u.get("input_tokens_details") or {}, u.get("output_tokens_details") or {}
            prompt, cached, completion = u.get("input_tokens") or 0, det.get("cached_tokens") or 0, u.get("output_tokens") or 0
        else:
            det, cdet = u.get("prompt_tokens_details") or {}, u.get("completion_tokens_details") or {}
            prompt, cached, completion = u.get("prompt_tokens") or 0, det.get("cached_tokens") or 0, u.get("completion_tokens") or 0
        cost = (prompt - cached) * PRICE[0] + cached * PRICE[1] + completion * PRICE[2]
        CUR["spend"] += cost
        CUR["calls"] += 1
        if "output" in d:  # Responses API: function calls are output items
            names = [(o.get("name") or "") for o in (d.get("output") or []) if o.get("type") == "function_call"]
        else:
            msg = ((d.get("choices") or [{}])[0].get("message")) or {}
            names = [((tc.get("function") or {}).get("name") or "") for tc in (msg.get("tool_calls") or [])]
        rec.update(status="ok", model=d.get("model"), system_fingerprint=d.get("system_fingerprint"), prompt=prompt, cached=cached,
                   completion=completion, reasoning=cdet.get("reasoning_tokens"), cost=round(cost, 6), tool_calls=names,
                   outside_subset=sum(1 for n in names if n not in set(CUR["subset"])), latency_s=round(now() - t0, 2))
        with open(TRACE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return r
    return wrapped


lmm.get_raw_lm_caller = _get

model_config = {"client_name": "openai", "api_type": args.api, "name": args.model, "base_url": args.base,
                "temperature": args.temperature, "drop_reasoning_content": False,
                **({} if args.no_reasoning_param else {"reasoning_effort": args.reasoning_effort} if args.api == "chat_completions"
                   else {"reasoning": {"effort": args.reasoning_effort}}),
                **({"seed": args.seed} if args.seed is not None else {}),
                "cost_per_token": {"input_cache_hit": PRICE[1], "input_cache_miss": PRICE[0], "input_cache_write": 0.0, "output": PRICE[2]},
                "retry_after_n_seconds": 15, "use_cache": False, "max_retries": 20}
P = os.environ["APPWORLD_EXPERIMENT_PROMPTS_PATH"]
agent_config = {
    "type": "p2_function_calling",
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

dev = load_task_ids("dev")
eligible = [t for t in dev if set(json.load(open(GT / t / "ground_truth" / "required_apps.json"))) <= set(APPS) - {"supervisor"}]
ids = args.ids or eligible
bad = [t for t in ids if t not in eligible]
if bad:
    sys.exit(f"not eligible dev task ids: {bad}; nothing was run")
if args.limit:
    ids = ids[: args.limit]
meta = dict(tag=args.tag, arm=args.arm, model=args.model, api=args.api, base=args.base, seed=args.seed,
            no_reasoning_param=args.no_reasoning_param, min_interval=args.min_interval, reasoning_effort=args.reasoning_effort, temperature=args.temperature,
            price=args.price, max_spend=args.max_spend, apps=APPS, tasks=ids, started=utc(),
            harness_sha256=__import__("hashlib").sha256(open(__file__, "rb").read()).hexdigest())
(RUN / "run-meta.json").write_text(json.dumps(meta, indent=1))
log(f"run {args.tag}: arm {args.arm}, model {args.model}, {len(ids)} eligible dev tasks, apps {APPS}, dry_run {args.dry_run}")
agent = Agent.from_dict(agent_config)
if args.dry_run:
    from appworld.task import Task
    t = Task.load(ids[0])
    docs = t.api_docs.function_calling()
    cat = [d for a in APPS for d in docs if d["function"]["name"].split("__", 1)[0] == a]
    sizes = [len(subset_for(i)) for i in ids]
    log(f"dry run: catalogue {len(cat)} tools, {len(json.dumps(cat))} chars (about {len(json.dumps(cat)) // 4} tokens at 4 chars/token); "
        f"subset sizes min {min(sizes)} max {max(sizes)}; {len(ids)} tasks; no call made")
    sys.exit(0)

stats = {"meta": meta, "tasks": {}}
exp = args.tag
agent.logger.initialize(experiment_name=exp, num_tasks=len(ids), num_processes=1, process_index=0)
code, streak = 0, 0
with AppWorld.initializer(update_defaults=True, experiment_name=exp, **agent.appworld_config):
    for i, tid in enumerate(ids, 1):
        CUR.update(task=tid, subset=subset_for(tid))
        t0, c0, s0 = now(), CUR["calls"], CUR["spend"]
        rec = {"index": i, "exception": None, "subset_size": len(CUR["subset"])}
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
        rec.update(steps=agent.step_number, seconds=round(now() - t0, 1), calls=CUR["calls"] - c0, cost=round(CUR["spend"] - s0, 6),
                   declared=CUR.get("declared"))
        stats["tasks"][tid] = rec
        (RUN / "stats.json").write_text(json.dumps(stats, indent=1))
        log(f"task {i}/{len(ids)} {tid}: steps {rec['steps']}, calls {rec['calls']}, ${rec['cost']:.4f}, exception {rec['exception']}, "
            f"spend ${CUR['spend']:.4f}")
        if streak >= 2:
            log("STOP: two tasks in a row ended with an exception")
            stats["stopped"] = "two exceptions"
            code = 4
            break
done = [t for t in ids if stats["tasks"].get(t, {}).get("exception") is None]
try:
    AppWorld.close_all() if hasattr(AppWorld, "close_all") else None
    ev = evaluate_tasks(task_ids=done, experiment_name=exp, suppress_errors=True, include_details=True, save_reports=True)
except Exception as e:
    ev = {"evaluation_error": f"{type(e).__name__}: {e}"}
(RUN / "evaluation.json").write_text(json.dumps(ev, indent=1, default=str))
stats["finished"] = utc()
stats["spend"] = round(CUR["spend"], 6)
(RUN / "stats.json").write_text(json.dumps(stats, indent=1))
log(f"run {args.tag} finished, exit {code}; spend ${CUR['spend']:.4f}; calls {CUR['calls']}")
sys.exit(code)
