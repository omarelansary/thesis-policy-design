"""V5 probe R1 (AUTH-020 eighth amendment, INT-T-022): why is `allowed_tools` rejected, and what can restrict tools at a fixed cached prefix?
RUN BY THE HUMAN'S AGENT, not by the lead. The key is read from the environment variable named by --key-env and is never printed or written;
only status codes, scrubbed error texts, usage records and the NAMES of tools the model called are written. Standard library only.

Question (design/package-v5/10 line 39: every ScaDS model returned HTTP 400 "litellm.BadRequestError: Invalid tool choice ..." for one request shape).
Is that the model, the request shape (naming), or the API layer (LiteLLM proxy / vLLM)? And does a paid OpenAI model accept it?
Each model gets the same system prompt and 20 tools (a prefix above 1,024 tokens, so prompt caching can apply), then these cells:
  C0  base              tool_choice "auto"; user asks to call tool_07                (warms the cache)
  C1  base again        same request                                                 (cached tokens expected)
  C2  allowed-chat      tool_choice {"type":"allowed_tools","allowed_tools":{"mode":"auto","tools":[{"type":"function","function":{"name":...}}]}}
  C3  allowed-flat      tool_choice {"type":"allowed_tools","mode":"auto","tools":[{"type":"function","name":...}]}   (Responses-API naming)
  C4  allowed-required  as C2 with mode "required"
  C5  required          tool_choice "required"
  C6  named             tool_choice {"type":"function","function":{"name":"tool_03"}}
  C7  none              tool_choice "none"
  C8  instruction-only  tools unchanged, tool_choice "auto", one extra message at the END: "Only tool_03, tool_04 and tool_05 may be used now."
  C9  responses-api     POST /responses with the flat allowed_tools shape (where the endpoint exists)
In C2-C4 and C8 the allowed subset is tool_03, tool_04, tool_05 while the user asks for tool_07: a call to tool_07 means "not enforced".
Every cell records: HTTP status, scrubbed error (first 400 characters), prompt / cached / completion tokens, finish reason, tool names called.

Optional --deftokens FILE: a JSON list of OpenAI-style tool definitions (for example AppWorld's function-calling definitions, kept LOCAL and never
committed). For n in --sizes, one request with the first n definitions, a one-word user message and max_tokens 1: prompt_tokens(n) - prompt_tokens(0)
is the tokens that model bills for n definitions; an error at a size shows the context-window limit. Only counts are written.

Examples (PowerShell):
    $env:SCADS_API_KEY = "<key>"
    python p2_tool_choice_probe.py --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model "zai-org/GLM-5.3" --model "MiniMaxAI/MiniMax-M3" --model "openai/gpt-oss-120b" --pause 35 --out out-scads.json
    $env:OPENAI_API_KEY = "<key>"
    python p2_tool_choice_probe.py --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model "gpt-5-mini" --out out-openai.json
    python p2_tool_choice_probe.py --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model "zai-org/GLM-5.3" --deftokens C:/local/appworld_fc_tools.json --sizes 0 10 50 100 200 457 --out out-deftokens-glm.json
    Remove-Item Env:SCADS_API_KEY; Remove-Item Env:OPENAI_API_KEY
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--key-env", required=True)
ap.add_argument("--model", action="append", required=True)
ap.add_argument("--max-tokens", type=int, default=64)
ap.add_argument("--pause", type=float, default=0.0, help="seconds between requests (rate limits)")
ap.add_argument("--deftokens", default=None)
ap.add_argument("--sizes", type=int, nargs="*", default=[0, 10, 50, 100, 200, 457])
ap.add_argument("--out", required=True)
a = ap.parse_args()
KEY = os.environ.get(a.key_env)
if not KEY:
    sys.exit(f"Set {a.key_env} in this terminal first. Nothing was sent.")


def scrub(s):
    s = re.sub(r"[0-9a-f]{40,}", "<hex-redacted>", s)
    return re.sub(r"sk-[A-Za-z0-9_\-]{10,}", "<key-redacted>", s)


def post(path, body, retry=True):
    r = urllib.request.Request(a.base.rstrip("/") + path, data=json.dumps(body).encode("utf-8"), method="POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")
        if e.code == 429 and retry:
            time.sleep(65)
            return post(path, body, retry=False)
        return e.code, {"error_body": scrub(txt)[:400]}, round(time.time() - t0, 2)
    except Exception as e:
        return None, {"error": type(e).__name__}, round(time.time() - t0, 2)


SYSTEM = ("You are a test assistant for a tool-restriction probe. " + " ".join(
    f"Rule {i}: answer briefly, use tools only when asked, and never invent tool names." for i in range(1, 121)))


def tool(i):
    return {"type": "function", "function": {"name": f"tool_{i:02d}", "description": f"Test tool number {i}. Returns 'ok {i}'. " * 3,
            "parameters": {"type": "object", "properties": {"note": {"type": "string", "description": "free text"}}, "required": []}}}


TOOLS = [tool(i) for i in range(1, 21)]
SUBSET = ["tool_03", "tool_04", "tool_05"]
USER = "Please call tool_07 with note 'probe'."


def usage(j):
    u = j.get("usage") or {}
    det = u.get("prompt_tokens_details") or u.get("input_tokens_details") or {}
    return {"prompt": u.get("prompt_tokens", u.get("input_tokens")), "cached": det.get("cached_tokens"),
            "completion": u.get("completion_tokens", u.get("output_tokens"))}


def called(j):
    names, fin = [], None
    for ch in j.get("choices") or []:
        fin = ch.get("finish_reason")
        for tc in (ch.get("message") or {}).get("tool_calls") or []:
            names.append((tc.get("function") or {}).get("name"))
    for it in j.get("output") or []:  # Responses API
        if it.get("type") == "function_call":
            names.append(it.get("name"))
    return names, fin


def chat(model, tool_choice, extra=None):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}] + (extra or [])
    body = {"model": model, "messages": msgs, "tools": TOOLS, "max_completion_tokens": a.max_tokens}
    if tool_choice is not None:
        body["tool_choice"] = tool_choice
    return post("/chat/completions", body)


def cells(model):
    sub_chat = [{"type": "function", "function": {"name": n}} for n in SUBSET]
    sub_flat = [{"type": "function", "name": n} for n in SUBSET]
    yield "C0 base", lambda: chat(model, "auto")
    yield "C1 base again", lambda: chat(model, "auto")
    yield "C2 allowed-chat", lambda: chat(model, {"type": "allowed_tools", "allowed_tools": {"mode": "auto", "tools": sub_chat}})
    yield "C3 allowed-flat", lambda: chat(model, {"type": "allowed_tools", "mode": "auto", "tools": sub_flat})
    yield "C4 allowed-required", lambda: chat(model, {"type": "allowed_tools", "allowed_tools": {"mode": "required", "tools": sub_chat}})
    yield "C5 required", lambda: chat(model, "required")
    yield "C6 named", lambda: chat(model, {"type": "function", "function": {"name": "tool_03"}})
    yield "C7 none", lambda: chat(model, "none")
    yield "C8 instruction-only", lambda: chat(model, "auto", [{"role": "user", "content": "Only tool_03, tool_04 and tool_05 may be used now."}])
    rtools = [{"type": "function", "name": t["function"]["name"], "description": t["function"]["description"],
               "parameters": t["function"]["parameters"]} for t in TOOLS]
    yield "C9 responses-api", lambda: post("/responses", {"model": model, "instructions": SYSTEM, "input": USER, "tools": rtools,
                                                           "tool_choice": {"type": "allowed_tools", "mode": "auto", "tools": sub_flat},
                                                           "max_output_tokens": max(a.max_tokens, 16)})


report = {"probe": "p2_tool_choice_probe", "base": a.base, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "models": {}}
for m in a.model:
    rows = []
    if a.deftokens:
        defs = json.load(open(a.deftokens, encoding="utf-8"))
        for n in a.sizes:
            body = {"model": m, "messages": [{"role": "user", "content": "ok"}], "max_completion_tokens": 256}
            if n:
                body["tools"] = defs[:n]
            s, j, t = post("/chat/completions", body)
            rows.append({"cell": f"deftokens n={n}", "status": s, "seconds": t, "usage": usage(j) if s == 200 else None,
                         "error": None if s == 200 else j})
            time.sleep(a.pause)
    else:
        for name, fn in cells(m):
            s, j, t = fn()
            names, fin = called(j) if s == 200 else ([], None)
            rows.append({"cell": name, "status": s, "seconds": t, "usage": usage(j) if s == 200 else None,
                         "tools_called": names, "finish_reason": fin, "error": None if s == 200 else j})
            print(m, name, s, rows[-1]["usage"], names, flush=True)
            time.sleep(a.pause)
    report["models"][m] = rows
json.dump(report, open(a.out, "w", encoding="utf-8"), indent=1)
print("written", a.out)
