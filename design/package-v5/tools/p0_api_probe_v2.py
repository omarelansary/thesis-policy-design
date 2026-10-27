"""P0 part 3 (design/package-v5/10): the second probe of the university API. RUN BY THE HUMAN, not by the lead.
Same rules as p0_api_probe.py: the key is read from the environment and never printed or written; only usage records, status
codes and short checks are printed; standard library only.

What changed since revision 1 (design/package-v5/10 explains why):
  - max_tokens default 400 (revision 1 used 16, which reasoning models spend entirely on thinking, so no tool call was ever reached);
  - tool calling is tested directly (T1-T4);
  - the cache is tested against CHANGES OF THE TOOLS ARRAY (C3, C4), the thing V5-R02 says never to do;
  - a 429 (rate limit) is retried once after a wait, and --pause spaces the requests (GLM-5.3 allowed 2 requests per minute).
  - the allowed_tools test is dropped: it was rejected with HTTP 400 on every model in revision 1.

PowerShell (use the SAME terminal; the file is written as UTF-8 by the script itself, so there is no redirect and no UTF-16):
    $env:SCADS_API_KEY = "<your key>"
    python design/package-v5/tools/p0_api_probe_v2.py --model "openai/gpt-oss-120b" --model "MiniMaxAI/MiniMax-M3" --out design/package-v5/inputs/p0-api-probe2-output.json
    Remove-Item Env:SCADS_API_KEY
For zai-org/GLM-5.3 add --pause 35 (or run it alone). Add --model for any other chat model you want covered.

Requests per model (10 small chat requests plus one model-list request):
  C1 prime       20 tools, a stable system prompt of a few thousand tokens           -> cached / created counters
  C2 identical   the same request again                                              -> expect a cache hit
  C3 extra tool  the same request with a 21st tool appended at the END of tools      -> does the cache survive a changed tools array?
  C4 edited tool the same request with the FIRST tool's description edited           -> does the cache survive an edit at the front?
  C5 tools back  the original request again                                          -> is the original prefix still cached?
  T1 auto        "Call tool_07 now with note 'x'", tool_choice auto                  -> is a tool call made?
  T2 required    the same, tool_choice required                                      -> is it honoured?
  T3 named       the same, tool_choice naming tool_07                                -> is it honoured?
  T4 absent      asks for "tool_99", which does not exist, tool_choice auto          -> does the model call a wrong tool, invent one, or answer?
Nothing here measures accuracy or makes a claim about a bill; it reads what the API reports.
"""
import argparse, copy, json, os, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--model", action="append", required=True)
ap.add_argument("--base", default="https://llm.scads.ai/v1")
ap.add_argument("--max-tokens", type=int, default=400)
ap.add_argument("--pause", type=float, default=0.0, help="seconds to wait between requests")
ap.add_argument("--out", default=None, help="write the report as UTF-8 JSON to this path instead of printing it")
a = ap.parse_args()
KEY = os.environ.get("SCADS_API_KEY")
if not KEY:
    sys.exit("Set SCADS_API_KEY in this terminal first (see the docstring). Nothing was sent.")


def req(path, body=None, retry=True):
    data = None if body is None else json.dumps(body).encode("utf-8")
    r = urllib.request.Request(a.base.rstrip("/") + path, data=data, method="GET" if body is None else "POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")
        if e.code == 429 and retry:
            time.sleep(65)
            return req(path, body, retry=False)
        return e.code, {"error_body": scrub(txt)[:500]}, round(time.time() - t0, 2)
    except Exception as e:
        return None, {"error": type(e).__name__}, round(time.time() - t0, 2)


def scrub(s):
    import re
    return re.sub(r"[0-9a-f]{40,}", "<hex-redacted>", s)  # LiteLLM prints a hash of the key in rate-limit messages


SYSTEM = ("You are a test assistant for a cache probe. " + " ".join(
    f"Rule {i}: answer briefly, use tools only when the user asks for a tool by name, and never invent tool names." for i in range(1, 121)))
TOOLS = [{"type": "function", "function": {"name": f"tool_{i:02d}", "description": f"Test tool number {i}. Returns the string 'ok {i}'. " * 3,
          "parameters": {"type": "object", "properties": {"note": {"type": "string", "description": "free text"}}, "required": []}}}
         for i in range(1, 21)]
TOOLS_PLUS = TOOLS + [{"type": "function", "function": {"name": "tool_21", "description": "Test tool number 21. Returns the string 'ok 21'. " * 3,
                       "parameters": {"type": "object", "properties": {"note": {"type": "string", "description": "free text"}}, "required": []}}}]
TOOLS_EDIT = copy.deepcopy(TOOLS)
TOOLS_EDIT[0]["function"]["description"] = "Edited description of tool number 1. Returns the string 'ok 1'. " * 3


def body(model, tools, user, **kw):
    return {"model": model, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            "tools": tools, "max_tokens": a.max_tokens, "temperature": 0, **kw}


def summary(status, js, secs):
    out = {"http": status, "seconds": secs}
    if isinstance(js, dict):
        out["usage"] = js.get("usage")
        ch = (js.get("choices") or [{}])[0]
        msg = ch.get("message") or {}
        out["finish_reason"] = ch.get("finish_reason")
        out["tool_calls"] = [{"name": tc.get("function", {}).get("name"), "arguments": (tc.get("function", {}).get("arguments") or "")[:80]} for tc in (msg.get("tool_calls") or [])]
        out["text"] = (msg.get("content") or "")[:120]
        for k in ("error_body", "error"):
            if k in js:
                out[k] = js[k]
    return out


def run(model, tools, user, **kw):
    if a.pause:
        time.sleep(a.pause)
    return summary(*req("/chat/completions", body(model, tools, user, **kw)))


READY = "Reply with the single word: ready."
CALL7 = "Call tool_07 now with note 'x'."
report = {"script": "p0_api_probe_v2", "base": a.base, "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "max_tokens": a.max_tokens}
s, js, t = req("/models")
report["models_endpoint"] = {"http": s, "count": len(js.get("data", [])) if isinstance(js, dict) else None}
for m in a.model:
    r = {}
    r["C1_prime"] = run(m, TOOLS, READY)
    r["C2_identical"] = run(m, TOOLS, READY)
    r["C3_extra_tool_at_end"] = run(m, TOOLS_PLUS, READY)
    r["C4_first_tool_edited"] = run(m, TOOLS_EDIT, READY)
    r["C5_original_again"] = run(m, TOOLS, READY)
    r["T1_auto_call_tool_07"] = run(m, TOOLS, CALL7, tool_choice="auto")
    r["T2_required_call_tool_07"] = run(m, TOOLS, CALL7, tool_choice="required")
    r["T3_named_tool_07"] = run(m, TOOLS, CALL7, tool_choice={"type": "function", "function": {"name": "tool_07"}})
    r["T4_absent_tool_99"] = run(m, TOOLS, "Call tool_99 now with note 'x'.", tool_choice="auto")
    report[m] = r
text = json.dumps(report, indent=1, ensure_ascii=False)
if a.out:
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    print("written", a.out)
else:
    print(text)
