#!/usr/bin/env python
"""R3 Part B runner (lead, AUTH-024, 2026-11-05). Rebuilt from RESULTS-R1 (Part 4) and RESULTS-R2 (pilot):
AppWorld's own agent code and prompts unchanged (commit 42b5bcf3, data 0.2.0, dev split only); `simplified_function_calling` agent
through the `openai` client on OpenRouter; model minimax/minimax-m3; provider pinned (order [provider], allow_fallbacks false);
temperature 0, seed 100, tool_choice auto, parallel_tool_calls true, 3-shot, step cap 50, client timeout 300 s,
retry 20 x 15 s; one task at a time; a new experiment name and a new AppWorld root per run.

Differences from the describing agent's (unpublished) run_part4.py are listed in RESULTS-R3-B.md. Counts and ids only are written
to <run>/trace/ and <run>/stats.json; AppWorld task text goes only to <run>/console.log and AppWorld's own output folders.

Usage: python run_partb.py --tag b1 --predictor-mode all --max-predicted-apis 1000 --max-spend 7.0 [--ids a_1 b_2] [--limit N]
The key is read from the environment or ~/r3-work/.env (OPENROUTER_API_KEY) and is never printed or written.
"""
import argparse, datetime, json, os, pathlib, sys, time, traceback

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--tag", required=True, help="run name; becomes the experiment name and the folder runs/<tag>")
ap.add_argument("--predictor-mode", choices=["predicted", "all"], required=True)
ap.add_argument("--max-predicted-apis", type=int, required=True)
ap.add_argument("--model", default="minimax/minimax-m3")
ap.add_argument("--provider", default="gmicloud/fp8", help="OpenRouter provider tag to pin")
ap.add_argument("--host", choices=["openrouter", "scads"], default="openrouter", help="AUTH-026: scads = https://llm.scads.ai/v1 with SCADS_API_KEY, no provider pin, reasoning as served")
ap.add_argument("--max-spend", type=float, required=True, help="stop the run when the summed reported cost reaches this many dollars")
ap.add_argument("--ids", nargs="*", help="task ids (must be in dev.txt); default all 57 in dev.txt order")
ap.add_argument("--limit", type=int, help="only the first N of the selected ids (smoke tests)")
ap.add_argument("--dry-run", action="store_true", help="build everything, call nothing")
ap.add_argument("--reasoning", action="store_true", help="AUTH-025: send OpenRouter's reasoning {enabled: true} (reasoning is optional for this model there and off unless asked)")
args = ap.parse_args()

# ---- environment (before any appworld import)
def load_env():
    f = HERE / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if v and k not in os.environ:
                    os.environ[k] = v
load_env()
KEYVAR = "SCADS_API_KEY" if args.host == "scads" else "OPENROUTER_API_KEY"
BASE = (os.environ.get("SCADS_BASE_URL") or "https://llm.scads.ai/v1") if args.host == "scads" else "https://openrouter.ai/api/v1"
if args.host == "scads" and args.reasoning:
    sys.exit("--reasoning is an OpenRouter request field; on ScaDS reasoning is as served; nothing was run")
key = os.environ.get(KEYVAR, "")
if not key and not args.dry_run:
    sys.exit(f"{KEYVAR} is not set (put it in ~/r3-work/.env or export it); nothing was run")
RUN = HERE / "runs" / args.tag
if RUN.exists():
    sys.exit(f"{RUN} already exists: every run needs a new tag (AppWorld issue #203); nothing was run")
(RUN / "trace").mkdir(parents=True)
os.symlink(HERE / "aw-root" / "data", RUN / "data")
os.environ.update({
    "APPWORLD_ROOT": str(RUN), "PYTHON_DOTENV_DISABLED": "1", "MODEL_SERVER_URL": BASE,
    "OPENAI_API_BASE": BASE, "OPENAI_BASE_URL": BASE,
    "APPWORLD_EXPERIMENT_PROMPTS_PATH": str(HERE / "appworld-src/experiments/prompts"),
})
if key:
    os.environ["OPENAI_API_KEY"] = key  # in this process only, as in Part 4
elif args.dry_run:
    os.environ["OPENAI_API_KEY"] = "dry-run-no-key"  # the client object needs some value; no call is made
del key

def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # real clock; only used outside tasks
def now():
    # AppWorld freezes the clock inside a task (time and datetime); os.times().elapsed is a real elapsed-seconds counter
    return os.times().elapsed
def log(msg):
    with open(RUN / "progress.log", "a") as f:
        f.write(f"{utc()} {msg}\n")
    print(f"{utc()} {msg}", file=sys.__stderr__, flush=True)

# console output of the agent contains task text: keep it in a local file only
sys.stdout = open(RUN / "console.log", "a", buffering=1)

import appworld_agents.code.simplified.language_model as lmm
from appworld import AppWorld
from appworld.evaluator import evaluate_tasks
from appworld.task import load_task_ids
from appworld_agents.code.simplified.agent import Agent
import appworld_agents.code.simplified.function_calling_agent  # registers the agent type

class SpendLimit(BaseException):
    pass

CUR = {"task": None, "spend": 0.0, "calls": 0}
TRACE = RUN / "trace" / "calls.jsonl"

# ---- patch 1: 300 s client timeout on every OpenAI client the agent creates
_OpenAI = lmm.OpenAI
lmm.OpenAI = lambda **kw: _OpenAI(timeout=300.0, **kw)

# ---- patch 2: provider pin + counts-only trace of every raw call (including failed ones)
_orig_get = lmm.get_raw_lm_caller
EXTRA = {"provider": {"order": [args.provider], "allow_fallbacks": False}} if args.host == "openrouter" else None
if args.reasoning:
    EXTRA["reasoning"] = {"enabled": True}

def _get(*a, **kw):
    caller = _orig_get(*a, **kw)
    def wrapped(**ckw):
        if CUR["spend"] >= args.max_spend:
            raise SpendLimit(f"spend {CUR['spend']:.4f} reached --max-spend {args.max_spend}")
        if EXTRA is not None:
            ckw["extra_body"] = EXTRA
        rec = {"t_elapsed_s": round(now(), 1), "task": CUR["task"], "predictor_call": "tools" not in ckw, "n_messages": len(ckw.get("messages", [])), "n_tools": len(ckw.get("tools") or [])}
        t0 = now()
        try:
            r = caller(**ckw)
        except Exception as e:
            rec.update(status="error", error=type(e).__name__, http=getattr(e, "status_code", None), latency_s=round(now() - t0, 2))
            with open(TRACE, "a") as f:
                f.write(json.dumps(rec) + "\n")
            if getattr(e, "status_code", None) in (401, 402, 403):  # key, credit or key-limit refusal: retrying cannot help, stop the run
                raise SpendLimit(f"endpoint refused with HTTP {e.status_code} ({type(e).__name__}); run stopped") from None
            raise
        d = r.model_dump() if hasattr(r, "model_dump") else dict(r)
        u = d.get("usage") or {}
        det = u.get("prompt_tokens_details") or {}
        ch = (d.get("choices") or [{}])[0]
        msg = ch.get("message") or {}
        cost = u.get("cost") or 0.0
        CUR["spend"] += float(cost); CUR["calls"] += 1
        rec.update(status="ok", provider=d.get("provider"), model=d.get("model"), system_fingerprint=d.get("system_fingerprint"),
                   prompt=u.get("prompt_tokens"), cached=det.get("cached_tokens"), cache_write=det.get("cache_write_tokens"),
                   completion=u.get("completion_tokens"), reasoning_tokens=(u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                   reasoning_chars=len(msg.get("reasoning") or msg.get("reasoning_content") or ""), history_msgs_with_reasoning=sum(bool(m.get("reasoning") or m.get("reasoning_details") or m.get("reasoning_content")) for m in ckw.get("messages", []) if isinstance(m, dict)), cost=cost, finish=ch.get("finish_reason"),
                   n_tool_calls=len(msg.get("tool_calls") or []), latency_s=round(now() - t0, 2))
        with open(TRACE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return r
    return wrapped
lmm.get_raw_lm_caller = _get

# ---- configuration: the rendered template for simplified_function_calling_agent with this run's changes
P = args.max_predicted_apis
model_config = {
    "client_name": "openai", "api_type": "chat_completions", "name": args.model, "base_url": BASE,
    "temperature": 0.0, "seed": 100, "drop_reasoning_content": False,
    # AppWorld's own cost caps only; the real cost is the endpoint's usage.cost in the trace. GMICloud fp8 prices per token.
    "cost_per_token": ({"input_cache_hit": 4.8e-08, "input_cache_miss": 2.4e-07, "input_cache_write": 0.0, "output": 9.6e-07} if args.host == "openrouter"
                       else {"input_cache_hit": 0.0, "input_cache_miss": 0.0, "input_cache_write": 0.0, "output": 0.0}),  # ScaDS reports no cost
    "retry_after_n_seconds": 15, "use_cache": False, "max_retries": 20,
}
agent_config = {
    "type": "simplified_function_calling",
    "model_config": {**model_config, "tool_choice": "auto", "parallel_tool_calls": True},
    "api_predictor_config": {
        "mode": args.predictor_mode, "model_config": dict(model_config),
        "prompt_file_path": os.environ["APPWORLD_EXPERIMENT_PROMPTS_PATH"] + "/api_predictor.txt",
        "demo_task_ids": ["82e2fac_1", "29caf6f_1", "d0b1f43_1"], "max_predicted_apis": P,
    },
    "appworld_config": {"random_seed": 100, "raise_on_extra_parameters": True, "include_direct_functions": True, "direct_function_separator": "__"},
    "logger_config": {"color": False, "verbose": True},
    "usage_tracker_config": {"max_cost_overall": 1000, "max_cost_per_task": 10, "max_output_tokens_per_task": 100000},
    "prompt_file_path": os.environ["APPWORLD_EXPERIMENT_PROMPTS_PATH"] + "/function_calling_agent/instructions.txt",
    "demo_messages_file_path": os.environ["APPWORLD_EXPERIMENT_PROMPTS_PATH"] + "/function_calling_agent/demos.json",
    "max_steps": 50, "log_lm_calls": True, "skip_if_finished": False,
}

# ---- tasks: dev only
dev = load_task_ids("dev")
ids = args.ids or dev
bad = [t for t in ids if t not in dev]
if bad:
    sys.exit(f"not dev task ids: {bad}; nothing was run")
if args.limit:
    ids = ids[: args.limit]
log(f"run {args.tag}: host {args.host}, model {args.model}, {len(ids)} dev tasks, mode {args.predictor_mode}, max_predicted_apis {P}, provider {args.provider}, reasoning {args.reasoning}, max-spend {args.max_spend}, appworld {__import__('appworld').__version__}")
agent = Agent.from_dict(agent_config)
if args.dry_run:
    log("dry run: agent built, no call made")
    sys.exit(0)

stats = {"tag": args.tag, "reasoning": args.reasoning, "predictor_mode": args.predictor_mode, "max_predicted_apis": P, "model": args.model, "provider_pinned": args.provider,
         "started": utc(), "tasks": {}}
def save_stats():
    (RUN / "stats.json").write_text(json.dumps(stats, indent=1))

exp = args.tag
agent.logger.initialize(experiment_name=exp, num_tasks=len(ids), num_processes=1, process_index=0)
exit_code = 0
with AppWorld.initializer(update_defaults=True, experiment_name=exp, **agent.appworld_config):
    for i, tid in enumerate(ids, 1):
        CUR["task"] = tid
        t0 = now()
        calls0 = CUR["calls"]
        rec = {"index": i, "exception": None}
        try:
            agent.solve_task(tid)
        except SpendLimit as e:
            log(f"STOP at task {i} ({tid}): {e}")
            rec["exception"] = "SpendLimit"; stats["tasks"][tid] = rec; stats["stopped_by_spend_limit"] = True
            save_stats(); exit_code = 3
            break
        except Exception as e:
            rec["exception"] = type(e).__name__
            print(traceback.format_exc())
            CUR["consecutive_exceptions"] = CUR.get("consecutive_exceptions", 0) + 1
        else:
            CUR["consecutive_exceptions"] = 0
        rec["steps"] = agent.step_number
        rec["seconds"] = round(now() - t0, 1)
        rec["lm_calls_ok"] = CUR["calls"] - calls0
        stats["tasks"][tid] = rec
        save_stats()
        log(f"task {i}/{len(ids)} {tid}: steps {rec['steps']}, ok-calls {rec['lm_calls_ok']}, {rec['seconds']} s, exception {rec['exception']}, spend so far ${CUR['spend']:.4f}")
        if CUR.get("consecutive_exceptions", 0) >= 2:  # added 2026-11-06 after a key limit made every call fail for 16 tasks
            log(f"STOP after task {i} ({tid}): two tasks in a row ended with an exception"); stats["stopped_by_consecutive_exceptions"] = True
            save_stats(); exit_code = 4
            break

# ---- evaluation with AppWorld's own evaluator, then merge with the trace (counts only)
done = [t for t in ids if t in stats["tasks"] and stats["tasks"][t].get("exception") is None]
try:
    AppWorld.close_all() if hasattr(AppWorld, "close_all") else None
    ev = evaluate_tasks(task_ids=done, experiment_name=exp, suppress_errors=True, include_details=True, save_reports=True)
except Exception as e:
    ev = {"evaluation_error": f"{type(e).__name__}: {e}"}
stats["evaluation_raw_keys"] = list(ev.keys())
(RUN / "evaluation.json").write_text(json.dumps(ev, indent=1, default=str))
calls = [json.loads(l) for l in open(TRACE)] if TRACE.exists() else []
stats["totals"] = {
    "calls_ok": sum(c["status"] == "ok" for c in calls), "calls_error": sum(c["status"] != "ok" for c in calls),
    "prompt": sum(c.get("prompt") or 0 for c in calls), "cached": sum(c.get("cached") or 0 for c in calls),
    "cache_write": sum(c.get("cache_write") or 0 for c in calls), "completion": sum(c.get("completion") or 0 for c in calls),
    "cost": round(sum(c.get("cost") or 0 for c in calls), 6), "reasoning_tokens": sum(c.get("reasoning_tokens") or 0 for c in calls),
    "replies_with_reasoning": sum(bool(c.get("reasoning_chars")) for c in calls),
    "providers": sorted({str(c.get("provider")) for c in calls if c["status"] == "ok"}),
}
stats["finished"] = utc()
save_stats()
log(f"run {args.tag} finished, exit {exit_code}; totals {json.dumps(stats['totals'])}")
sys.exit(exit_code)
