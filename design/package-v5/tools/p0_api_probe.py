"""P0 part 2 (design/package-v5/05): what the university API reports and honours. RUN BY THE HUMAN, not by the lead.
The key is read from the environment and is never printed or written anywhere; only usage records, HTTP status
codes and short checks are printed. Standard library only.

PowerShell (one line each):
    $env:SCADS_API_KEY = "<your key>"
    python design/package-v5/tools/p0_api_probe.py --model "openai/gpt-oss-120b" > design/package-v5/inputs/p0-api-probe-output.txt
Then remove the key from the session:  Remove-Item Env:SCADS_API_KEY
Optional: --model can be given several times; --base defaults to https://llm.scads.ai/v1 (L/v5-tud-selfservice-scads-llm-20261022.txt:46).

Requests per model: 5 small chat requests (max 16 output tokens each) plus one GET of the model list.
  R1, R2  the same request twice: a stable system prompt of a few thousand tokens and 20 tool definitions.
          Question: does the usage record show cached prompt tokens on R2 (prefix caching reported)?
  R3      the same prefix plus one more user message appended. Question: are the earlier tokens still cached?
  R4      R1 with tool_choice set to OpenAI's allowed_tools form, allowing only tool_01..tool_03, while the user
          message asks for tool_07. Question: is the parameter accepted, rejected, or ignored (tool_07 called)?
  R5      R1 with tool_choice "required". Question: does tool calling work at all on this model?
Nothing here measures accuracy or makes a claim about the bill; it reads what the API reports.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--model", action="append", required=True)
ap.add_argument("--base", default="https://llm.scads.ai/v1")
a = ap.parse_args()
KEY = os.environ.get("SCADS_API_KEY")
if not KEY:
    sys.exit("Set SCADS_API_KEY in this terminal first (see the docstring). Nothing was sent.")


def req(path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    r = urllib.request.Request(a.base.rstrip("/") + path, data=data, method="GET" if body is None else "POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        return e.code, {"error_body": e.read().decode("utf-8", "replace")[:500]}, round(time.time() - t0, 2)
    except Exception as e:  # network errors: report the type only
        return None, {"error": type(e).__name__}, round(time.time() - t0, 2)


SYSTEM = ("You are a test assistant for a cache probe. " + " ".join(
    f"Rule {i}: answer briefly, use tools only when the user asks for a tool by name, and never invent tool names." for i in range(1, 121)))
TOOLS = [{"type": "function", "function": {"name": f"tool_{i:02d}", "description": f"Test tool number {i}. Returns the string 'ok {i}'. " * 3,
          "parameters": {"type": "object", "properties": {"note": {"type": "string", "description": "free text"}}, "required": []}}}
         for i in range(1, 21)]
USER = "Reply with the single word: ready."


def body(model, extra_msgs=(), **kw):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}] + list(extra_msgs)
    return {"model": model, "messages": msgs, "tools": TOOLS, "max_tokens": 16, "temperature": 0, **kw}


def summary(status, js, secs):
    out = {"http": status, "seconds": secs}
    if isinstance(js, dict):
        out["usage"] = js.get("usage")
        ch = (js.get("choices") or [{}])[0]
        msg = ch.get("message") or {}
        out["finish_reason"] = ch.get("finish_reason")
        out["tool_calls"] = [tc.get("function", {}).get("name") for tc in (msg.get("tool_calls") or [])]
        out["text"] = (msg.get("content") or "")[:80]
        for k in ("error_body", "error"):
            if k in js:
                out[k] = js[k]
    return out


report = {"base": a.base, "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
s, js, t = req("/models")
report["models_endpoint"] = {"http": s, "count": len(js.get("data", [])) if isinstance(js, dict) else None}
for m in a.model:
    r = {}
    r["R1_first"] = summary(*req("/chat/completions", body(m)))
    r["R2_same_again"] = summary(*req("/chat/completions", body(m)))
    r["R3_appended_turn"] = summary(*req("/chat/completions", body(m, extra_msgs=[{"role": "assistant", "content": "ready"}, {"role": "user", "content": "Again: reply with the single word: ready."}])))
    allowed = {"type": "allowed_tools", "allowed_tools": {"mode": "auto", "tools": [{"type": "function", "function": {"name": f"tool_{i:02d}"}} for i in (1, 2, 3)]}}
    r["R4_allowed_tools_asks_for_tool_07"] = summary(*req("/chat/completions", body(m, extra_msgs=[{"role": "assistant", "content": "ready"}, {"role": "user", "content": "Call tool_07 now with note 'x'."}], tool_choice=allowed)))
    r["R5_tool_choice_required"] = summary(*req("/chat/completions", body(m, tool_choice="required")))
    report[m] = r
print(json.dumps(report, indent=1))
