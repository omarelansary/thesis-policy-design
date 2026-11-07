"""P5 break-even harness (AUTH-028; design/package-v5/05 P5, 12 sections 3 and 5). Standard library only.

Question: on our route, at what catalogue size n does offering every tool definition (expose-all, cached prefix) cost more than a
small core plus search (deferral)? And (OpenAI part) are deferred definitions that were never loaded billed as input?
Measured: provider usage records per request (prompt, cached, cache-write, reasoning, completion tokens). No accuracy claim.

Catalogue: stub tools, generated deterministically from --seed, each about --def-chars characters of JSON (about 250 tokens, short
description, bulk in the parameter schema; the real tokens per definition are measured by the calibration requests). The needed tool `orders_get_shipping_status` is index 7, so it
is in every catalogue of 10 or more tools and is never in the deferral core (indexes 0-4).

Session (one short task, three user turns): (1) shipping status of order 4471; (2) the same for 4472; (3) both in one sentence.
The harness answers every tool call with fixed stub data. Up to --turn-cap model requests per user turn.

Routes and arms
  scads  (chat completions, client-side deferral; the route V5 applies, `04` section 5)
    expose_all  tools = the n stub definitions
    deferral    tools = core (indexes 0-4) + search_tools + call_tool. search_tools returns the top 3 definitions by word match
                as JSON in the tool result (D-01: K = 3, appended, never added to `tools`, V5-R02); call_tool runs one by name.
                The search and call mechanism is this harness's, chosen to keep `tools` fixed; it is not P2's choice.
  openai (Responses API, hosted tool search; only gpt-5.4 and later support it, stored doc L/v5-openai-tool-search-20261022.md:7)
    eager        the n definitions as functions
    deferred_fn  the same with defer_loading true (core 0-4 not deferred) plus {"type": "tool_search"}
    deferred_ns  deferred functions grouped into namespaces of at most 10 (the doc's advice) plus tool_search
Calibration (per route): one request with no tools and one per size and arm with the user message "Reply with OK." gives tokens per
definition, and for the OpenAI deferred arms whether unloaded definitions are billed.

Stops: HTTP 401, 402 or 403; two failed requests in a row; --max-requests; --max-spend (OpenAI, from usage and --price).
Keys only from the environment (SCADS_API_KEY and SCADS_BASE_URL, or OPENAI_API_KEY); never printed or written. Output: one JSON
line per request (counts and tool names only, no message text) and a summary JSON; use --analyze on the JSONL afterwards.

Examples (Linux):
  python3 design/package-v5/tools/p5_break_even.py --route scads --model zai-org/GLM-5.3 --dry-run --out /tmp/x
  set -a; . ~/r3-work/.env; set +a
  python3 design/package-v5/tools/p5_break_even.py --route scads --model zai-org/GLM-5.3 --sizes 10,30,100,300 --sessions 2 \
      --out design/package-v5/inputs/p5/scads-glm53
  python3 design/package-v5/tools/p5_break_even.py --route openai --model gpt-5.4-mini --price 0.75,0.075,0,4.5 \
      --max-spend 1.5 --out design/package-v5/inputs/p5/openai-gpt54mini
  python3 design/package-v5/tools/p5_break_even.py --analyze design/package-v5/inputs/p5/scads-glm53/requests.jsonl
"""
import argparse, hashlib, json, os, random, re, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--route", choices=["scads", "openai"])
ap.add_argument("--model")
ap.add_argument("--sizes", default="10,30,100,300")
ap.add_argument("--arms", default=None, help="default: expose_all,deferral (scads); eager,deferred_fn,deferred_ns (openai)")
ap.add_argument("--sessions", type=int, default=2, help="identical sessions per size and arm; the second shows a warm start")
ap.add_argument("--no-calibration", action="store_true")
ap.add_argument("--turn-cap", type=int, default=6)
ap.add_argument("--max-requests", type=int, default=100)
ap.add_argument("--max-spend", type=float, default=0.0, help="dollars; 0 = no cap (ScaDS is free)")
ap.add_argument("--price", default="", help="input,cached_input,cache_write,output dollars per million tokens (OpenAI)")
ap.add_argument("--reasoning-effort", default="low", help="OpenAI only; ScaDS serves reasoning as configured and it is recorded")
ap.add_argument("--max-output", type=int, default=2048)
ap.add_argument("--timeout", type=float, default=300.0)
ap.add_argument("--pause", type=float, default=0.0)
ap.add_argument("--seed", type=int, default=5)
ap.add_argument("--def-chars", type=int, default=1000)
ap.add_argument("--out")
ap.add_argument("--dry-run", action="store_true", help="build catalogues and print sizes; send nothing")
ap.add_argument("--analyze", metavar="JSONL")
a = ap.parse_args()

TARGET = "orders_get_shipping_status"
ORDERS = {"4471": {"order_id": "4471", "status": "in transit", "carrier": "DHL", "eta": "2026-11-12"},
          "4472": {"order_id": "4472", "status": "delivered", "carrier": "UPS", "delivered_on": "2026-11-05"}}
USER_TURNS = ["What is the shipping status of order 4471?", "And of order 4472?", "Thanks. Put both answers in one sentence."]
SYSTEM = "You are the assistant of an online shop's back office. Answer with the tools; never guess order data."
SYSTEM_DEFER = (" Only some tools are listed. More tools exist: find them with search_tools, then run one with call_tool, giving its"
                " exact name and its arguments.")

# ---------------------------------------------------------------- catalogue
DOMAINS = ["orders", "shipments", "invoices", "payments", "refunds", "customers", "products", "inventory", "warehouses", "suppliers",
           "coupons", "reviews", "returns", "carts", "subscriptions", "tickets", "employees", "shifts", "campaigns", "newsletters",
           "pricing", "taxes", "currencies", "reports", "audits", "contracts", "assets", "fleet", "stores", "kiosks", "gift_cards",
           "loyalty", "bundles", "catalog", "media", "translations", "webhooks", "api_keys", "sessions", "notifications"]
VERBS = ["get", "list", "create", "update", "cancel", "archive", "export", "validate", "count", "search", "merge", "restore",
         "approve", "reject", "schedule", "tag", "assign", "sync", "preview", "recalculate", "lock", "unlock", "duplicate", "rank", "audit"]
NOUNS = ["record", "summary", "history", "status", "details", "batch", "note", "flag", "label", "owner", "schedule", "limit", "rule"]
WORDS = ("account region channel batch period ledger owner partner priority quota segment tier window threshold policy revision "
         "reference identifier draft archive locale timezone currency attachment comment reviewer approver deadline budget forecast "
         "margin discount warehouse carrier parcel route manifest invoice voucher").split()


def _filler(rng, n):
    out = []
    while len(" ".join(out)) < n:
        w = rng.sample(WORDS, 6)
        out.append(f"The {w[0]} and {w[1]} fields follow the {w[2]} rules of the {w[3]}; a missing {w[4]} falls back to the {w[5]}.")
    return " ".join(out)


def make_tool(rng, name, purpose, chars):
    # a short description and the bulk in the parameter schema, as in real catalogues; OpenAI's deferral keeps names and
    # descriptions visible and defers the schema (L/v5-openai-tool-search-20261022.md:22), so where the bulk sits matters
    tool = {"name": name, "description": purpose + " " + _filler(rng, 80),
            "parameters": {"type": "object", "properties": {}, "required": []}}
    while len(json.dumps(tool)) < chars:
        w = rng.sample(WORDS, 2)
        key = f"{w[0]}_{w[1]}"
        if key in tool["parameters"]["properties"]:
            continue
        tool["parameters"]["properties"][key] = {"type": rng.choice(["string", "integer", "boolean"]),
                                                 "description": f"Optional {w[0]} {w[1]} filter. " + _filler(rng, 90)}
    return tool


def catalogue(nmax=1000):
    rng = random.Random(a.seed)
    names, tools = set(), []
    while len(tools) < nmax:
        if len(tools) == 7:
            t = make_tool(random.Random(7), TARGET, "Return the current shipping status and the estimated or actual delivery date of "
                          "one customer order.", a.def_chars)
            t["parameters"]["properties"] = {
                "order_id": {"type": "string", "description": "The order number, for example 1234."},
                "include_history": {"type": "boolean", "description": "Also return earlier status changes."},
                **dict(list(t["parameters"]["properties"].items())[2:])}
            t["parameters"]["required"] = ["order_id"]
            names.add(TARGET); tools.append(t); continue
        d, v, n = rng.choice(DOMAINS), rng.choice(VERBS), rng.choice(NOUNS)
        nm = f"{d}_{v}_{n}"
        if nm in names or nm == TARGET:
            continue
        names.add(nm)
        tools.append(make_tool(rng, nm, f"{v.capitalize()} the {n} of {d.replace('_', ' ')}.", a.def_chars))
    return tools


SEARCH = {"name": "search_tools", "description": "Search the full tool catalogue by keywords. Returns up to 3 matching tool definitions "
          "(name, description, parameters) that can then be run with call_tool.",
          "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "Keywords describing the needed tool."}},
                         "required": ["query"]}}
CALL = {"name": "call_tool", "description": "Run a tool found with search_tools.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string", "description": "Exact tool name."},
                                                         "arguments": {"type": "object", "description": "The tool's arguments."}},
                       "required": ["name", "arguments"]}}


def search(cat, query):
    q = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]
    def score(t):
        text = (t["name"].replace("_", " ") + " " + t["description"]).lower()
        return sum(text.count(w) for w in q) + 3 * sum(w in t["name"] for w in q)
    return sorted(cat, key=lambda t: -score(t))[:3]


def run_tool(cat, name, args):
    if name == TARGET:
        oid = str((args or {}).get("order_id", "")).strip().lstrip("#")
        return ORDERS.get(oid, {"error": f"order {oid} not found"})
    if name == "search_tools":
        return {"tools": search(cat, (args or {}).get("query", ""))}
    if name == "call_tool":
        return run_tool(cat, (args or {}).get("name", ""), (args or {}).get("arguments") or {})
    if any(t["name"] == name for t in cat):
        return {"result": "no data for this request"}
    return {"error": f"unknown tool {name}; use search_tools"}


# ---------------------------------------------------------------- analysis
def analyze(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    ok = [r for r in rows if r.get("status") == 200]
    out = {"file": path, "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "requests": len(rows), "ok": len(ok)}
    cal = [r for r in ok if r["phase"] == "calibration"]
    base = next((r["prompt"] for r in cal if r["n"] == 0), None)
    out["calibration"] = [{"arm": r["arm"], "n": r["n"], "prompt": r["prompt"], "cached": r["cached"],
                           "tokens_per_definition": (round((r["prompt"] - base) / r["n"], 1)
                                                     if base is not None and r["n"] and r["arm"] != "deferral" else None),
                           "note": "deferral: the core prefix (5 tools, search_tools, call_tool), same at every size" if r["arm"] == "deferral" else ""}
                          for r in cal]
    groups = {}
    for r in ok:
        if r["phase"] != "session":
            continue
        g = groups.setdefault((r["arm"], r["n"], r["session"]), {"requests": 0, "prompt": 0, "cached": 0, "cache_write": 0,
                                                                 "completion": 0, "reasoning": 0, "searches": 0, "target_calls": 0,
                                                                 "cost": 0.0, "turns_capped": 0})
        g["requests"] += 1
        for k in ("prompt", "cached", "cache_write", "completion", "reasoning"):
            g[k] += r.get(k) or 0
        g["searches"] += r["tool_calls"].count("search_tools") + r["tool_calls"].count("tool_search")
        g["target_calls"] += sum(1 for t in r["tool_calls"] if t.endswith(TARGET) or t == "call_tool:" + TARGET)
        g["cost"] += r.get("cost") or 0.0
    for r in rows:
        if r.get("phase") == "note" and r.get("turn_capped"):
            k = (r["arm"], r["n"], r["session"])
            if k in groups:
                groups[k]["turns_capped"] += 1
    out["sessions"] = [dict(arm=k[0], n=k[1], session=k[2], **v) for k, v in sorted(groups.items(), key=lambda x: (x[0][1], x[0][0], x[0][2]))]
    # bill in fresh-input-token equivalents (DPR-0006: F + w*W + r*R + o*O) with the D-01 ratios unless --price is given
    r_, w_, o_ = 0.1, 1.25, 5.0
    if a.price:
        p = [float(x) for x in a.price.split(",")]
        r_, w_, o_ = p[1] / p[0], (p[2] / p[0] if p[2] else 1.0), p[3] / p[0]
    out["bill_ratios"] = {"r": r_, "w": w_, "o": o_, "source": "--price" if a.price else "D-01 defaults (r 0.1, w 1.25, o 5), not a price table"}
    for s in out["sessions"]:
        fresh = s["prompt"] - s["cached"] - s["cache_write"]
        s["bill_fresh_equiv"] = round(fresh + w_ * s["cache_write"] + r_ * s["cached"] + o_ * s["completion"], 1)
    arms = sorted({s["arm"] for s in out["sessions"]})
    ref = "expose_all" if "expose_all" in arms else "eager"
    ratios = []
    for s in out["sessions"]:
        if s["arm"] == ref:
            continue
        m = next((x for x in out["sessions"] if x["arm"] == ref and x["n"] == s["n"] and x["session"] == s["session"]), None)
        if m:
            ratios.append({"arm": s["arm"], "n": s["n"], "session": s["session"],
                           "bill_ratio_vs_" + ref: round(s["bill_fresh_equiv"] / m["bill_fresh_equiv"], 3) if m["bill_fresh_equiv"] else None})
    out["ratios"] = ratios
    print(json.dumps(out, indent=1))
    with open(re.sub(r"\.jsonl$", "", path) + "-analysis.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)


if a.analyze:
    analyze(a.analyze); sys.exit(0)
if not (a.route and a.model and a.out):
    sys.exit("--route, --model and --out are required (or --analyze FILE)")

SIZES = [int(x) for x in a.sizes.split(",")]
ARMS = (a.arms.split(",") if a.arms else (["expose_all", "deferral"] if a.route == "scads" else ["eager", "deferred_fn", "deferred_ns"]))
CAT = catalogue(max(SIZES))
CORE = CAT[:5]
PRICE = [float(x) for x in a.price.split(",")] if a.price else None
if a.route == "openai" and a.max_spend and not PRICE:
    sys.exit("--max-spend on the OpenAI route needs --price input,cached,cache_write,output; nothing was sent")


def chat_tools(arm, n):
    defs = CAT[:n] if arm == "expose_all" else CORE + [SEARCH, CALL]
    return [{"type": "function", "function": t} for t in defs]


def resp_tools(arm, n):
    if arm == "eager":
        return [{"type": "function", **t} for t in CAT[:n]]
    core = [{"type": "function", **t} for t in CORE]
    rest = CAT[5:n]
    if arm == "deferred_fn":
        return core + [{"type": "function", "defer_loading": True, **t} for t in rest] + [{"type": "tool_search"}]
    groups = {}
    for t in rest:
        d = next(x for x in DOMAINS if t["name"].startswith(x + "_"))
        groups.setdefault(d, []).append(t)
    ns = []
    for d, ts in groups.items():
        for i in range(0, len(ts), 10):
            ns.append({"type": "namespace", "name": f"{d}_{i // 10}", "description": f"Tools for {d.replace('_', ' ')} in the shop's back office.",
                       "tools": [{"type": "function", "defer_loading": True, **t} for t in ts[i:i + 10]]})
    return core + ns + [{"type": "tool_search"}]


if a.dry_run:
    for arm in ARMS:
        for n in SIZES:
            tl = chat_tools(arm, n) if a.route == "scads" else resp_tools(arm, n)
            s = json.dumps(tl)
            print(f"{arm:12} n={n:5}  tools-json {len(s):9,} chars  (about {len(s) // 4:,} tokens at 4 chars per token)")
    print("target index", [t["name"] for t in CAT].index(TARGET), "| search('shipping status order') ->",
          [t["name"] for t in search(CAT, "shipping status of order")])
    sys.exit(0)

KEY = os.environ.get("SCADS_API_KEY" if a.route == "scads" else "OPENAI_API_KEY")
if not KEY:
    sys.exit("The API key variable is not set in this process; nothing was sent.")
BASE = (os.environ.get("SCADS_BASE_URL") or "https://llm.scads.ai/v1") if a.route == "scads" else "https://api.openai.com/v1"
os.makedirs(a.out, exist_ok=True)
LOG = open(os.path.join(a.out, "requests.jsonl"), "a", encoding="utf-8", newline="\n")
STATE = {"requests": 0, "fails_in_row": 0, "spend": 0.0, "stopped": None}


def scrub(s):
    return re.sub(r"[0-9a-f]{40,}|sk-[A-Za-z0-9_-]{8,}", "<redacted>", s)[:300]


def post(path, body):
    req = urllib.request.Request(BASE.rstrip("/") + path, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=a.timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8")), round(time.time() - t0, 2), None
    except urllib.error.HTTPError as e:
        return e.code, None, round(time.time() - t0, 2), scrub(e.read().decode("utf-8", "replace"))
    except Exception as e:  # timeout, connection reset
        return 0, None, round(time.time() - t0, 2), scrub(type(e).__name__ + ": " + str(e))


def usage_of(j):
    u = (j or {}).get("usage") or {}
    if a.route == "scads":
        pd, cd = u.get("prompt_tokens_details") or {}, u.get("completion_tokens_details") or {}
        return dict(prompt=u.get("prompt_tokens"), cached=pd.get("cached_tokens") or 0,
                    cache_write=u.get("created_cache_tokens") or u.get("cache_creation_input_tokens") or 0,
                    completion=u.get("completion_tokens"), reasoning=cd.get("reasoning_tokens") or u.get("reasoning_tokens") or 0)
    idt, odt = u.get("input_tokens_details") or {}, u.get("output_tokens_details") or {}
    return dict(prompt=u.get("input_tokens"), cached=idt.get("cached_tokens") or 0, cache_write=idt.get("cache_write_tokens") or 0,
                completion=u.get("output_tokens"), reasoning=odt.get("reasoning_tokens") or 0)


def call(phase, arm, n, session, turn, step, body):
    if STATE["stopped"]:
        return None
    if STATE["requests"] >= a.max_requests:
        STATE["stopped"] = f"max-requests {a.max_requests}"; return None
    if a.max_spend and STATE["spend"] >= a.max_spend:
        STATE["stopped"] = f"max-spend ${a.max_spend}"; return None
    STATE["requests"] += 1
    status, j, lat, err = post("/chat/completions" if a.route == "scads" else "/responses", body)
    rec = dict(t=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), route=a.route, model_requested=a.model,
               model_served=(j or {}).get("model"), phase=phase, arm=arm, n=n, session=session, turn=turn, step=step,
               status=status, latency_s=lat, n_tools_array=len(body.get("tools") or []), body_chars=len(json.dumps(body)), error=err)
    rec.update(usage_of(j) if j else dict(prompt=None, cached=None, cache_write=None, completion=None, reasoning=None))
    names = []
    if j and a.route == "scads":
        msg = (j.get("choices") or [{}])[0].get("message") or {}
        rec["finish"] = (j.get("choices") or [{}])[0].get("finish_reason")
        for tc in msg.get("tool_calls") or []:
            nm = (tc.get("function") or {}).get("name", "")
            if nm == "call_tool":
                try:
                    nm = "call_tool:" + json.loads(tc["function"].get("arguments") or "{}").get("name", "")
                except Exception:
                    nm = "call_tool:?"
            names.append(nm)
    elif j:
        rec["finish"] = j.get("status")
        for it in j.get("output") or []:
            if it.get("type") == "function_call":
                names.append((it.get("namespace") + "." if it.get("namespace") else "") + it.get("name", ""))
            elif it.get("type") in ("tool_search_call",):
                names.append("tool_search")
    rec["tool_calls"] = names
    if PRICE and j:
        fresh = (rec["prompt"] or 0) - rec["cached"] - rec["cache_write"]
        rec["cost"] = round((fresh * PRICE[0] + rec["cached"] * PRICE[1] + rec["cache_write"] * (PRICE[2] or PRICE[0])
                             + (rec["completion"] or 0) * PRICE[3]) / 1e6, 6)
        STATE["spend"] += rec["cost"]
    LOG.write(json.dumps(rec) + "\n"); LOG.flush()
    print(f"{rec['t']} {phase:11} {arm:11} n={n:<4} s{session} t{turn} #{step} {status} prompt={rec['prompt']} cached={rec['cached']} "
          f"write={rec['cache_write']} out={rec['completion']} calls={names} {lat}s" + (f" spend=${STATE['spend']:.4f}" if PRICE else ""))
    if status in (401, 402, 403):
        STATE["stopped"] = f"HTTP {status}"
    STATE["fails_in_row"] = 0 if status == 200 else STATE["fails_in_row"] + 1
    if STATE["fails_in_row"] >= 2:
        STATE["stopped"] = "two failed requests in a row"
    if a.pause:
        time.sleep(a.pause)
    return j


def base_body(tools, system, messages):
    if a.route == "scads":
        b = {"model": a.model, "messages": [{"role": "system", "content": system}] + messages, "temperature": 0, "seed": 100,
             "max_tokens": a.max_output}
        if tools:
            b["tools"], b["tool_choice"] = tools, "auto"
        return b
    b = {"model": a.model, "instructions": system, "input": messages, "store": False, "include": ["reasoning.encrypted_content"],
         "reasoning": {"effort": a.reasoning_effort}, "max_output_tokens": a.max_output}
    if tools:
        b["tools"] = tools
    return b


def calibration():
    msg = [{"role": "user", "content": "Reply with OK."}]
    call("calibration", "none", 0, 0, 0, 0, base_body(None, SYSTEM, msg))
    for arm in ARMS:
        for n in (SIZES[:1] if arm == "deferral" else SIZES):  # the deferral core is the same at every size
            tl = chat_tools(arm, n) if a.route == "scads" else resp_tools(arm, n)
            call("calibration", arm, n, 0, 0, 0, base_body(tl, SYSTEM + (SYSTEM_DEFER if arm == "deferral" else ""), msg))


def session_scads(arm, n, s):
    tools, system, msgs = chat_tools(arm, n), SYSTEM + (SYSTEM_DEFER if arm == "deferral" else ""), []
    for ti, u in enumerate(USER_TURNS, 1):
        msgs.append({"role": "user", "content": u})
        for step in range(1, a.turn_cap + 1):
            j = call("session", arm, n, s, ti, step, base_body(tools, system, msgs))
            if not j:
                return
            m = (j.get("choices") or [{}])[0].get("message") or {}
            am = {"role": "assistant", "content": m.get("content") or ""}
            for k in ("tool_calls", "reasoning_content"):
                if m.get(k):
                    am[k] = m[k]
            msgs.append(am)
            if not m.get("tool_calls"):
                break
            for tc in m["tool_calls"]:
                try:
                    args = json.loads(tc["function"].get("arguments") or "{}")
                except Exception:
                    args = {}
                msgs.append({"role": "tool", "tool_call_id": tc.get("id"), "content": json.dumps(run_tool(CAT[:n], tc["function"]["name"], args))})
        else:
            LOG.write(json.dumps({"phase": "note", "arm": arm, "n": n, "session": s, "turn": ti, "turn_capped": True}) + "\n")


def session_openai(arm, n, s):
    tools, items = resp_tools(arm, n), []
    for ti, u in enumerate(USER_TURNS, 1):
        items.append({"role": "user", "content": u})
        for step in range(1, a.turn_cap + 1):
            j = call("session", arm, n, s, ti, step, base_body(tools, SYSTEM, items))
            if not j:
                return
            out = j.get("output") or []
            items.extend(out)
            fcs = [it for it in out if it.get("type") == "function_call"]
            if not fcs:
                break
            for fc in fcs:
                try:
                    args = json.loads(fc.get("arguments") or "{}")
                except Exception:
                    args = {}
                items.append({"type": "function_call_output", "call_id": fc.get("call_id"),
                              "output": json.dumps(run_tool(CAT[:n], fc.get("name", ""), args))})


meta = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), args={k: v for k, v in vars(a).items()},
            started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), base_host=BASE.split("/")[2], sizes=SIZES, arms=ARMS,
            catalogue_sha256=hashlib.sha256(json.dumps(CAT).encode()).hexdigest(), target=TARGET)
if not a.no_calibration:
    calibration()
for s in range(1, a.sessions + 1):  # every first session before any warm repeat, so a request cap cuts repeats first
    for n in SIZES:
        for arm in ARMS:
            (session_scads if a.route == "scads" else session_openai)(arm, n, s)
meta.update(finished=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), requests=STATE["requests"], spend=round(STATE["spend"], 4),
            stopped=STATE["stopped"])
with open(os.path.join(a.out, "run-meta.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(meta, f, indent=1)
print(json.dumps({k: meta[k] for k in ("requests", "spend", "stopped")}))
