"""P0 part 4: the third probe of the university API: cache behaviour after changes to the tools array, with NONCE-marked variants, and the cache lifetime.
RUN BY THE HUMAN, not by the lead. Same rules as the earlier probes: the key is read from the environment and never printed or written; only
usage records and status codes are printed; standard library only; the report is written as UTF-8 JSON by the script (no redirect).

Why (design/package-v5/10, section 7): in the second probe, GLM-5.3 behaved like a plain prefix cache (an edit at the front rewrote 99% of the
prompt), but gpt-oss-120b and MiniMax-M3 kept almost the whole cache after the tools array changed, and gpt-oss reported more cached tokens
(4,528) than the original prompt had (4,479). Either those variants had been primed by an earlier run, or these deployments do not cache as a
plain prefix. Each variant below carries a fresh random NONCE inside the edited text, so no earlier run can have cached it.

MODE 1 (default, "variants"): 8 requests per model
  V0 base          the original request (the base prefix; expect a hit if it was primed earlier)
  V1 end-add       a 21st tool appended at the END of tools, its description carrying the nonce
  V2 first-edit    the FIRST tool's description carries the nonce
  V3 middle-edit   the tool_10 description carries the nonce
  V4 last-edit     the tool_20 description carries the nonce
  V5 system-tail   the NONCE appended to the END of the system prompt (tools unchanged)
  V6 system-head   the NONCE at the START of the system prompt
  V7 base again    the original request again (is the base prefix still cached after all the variants?)
MODE 2 ("lifetime"): one request, the base request. Run it again after 2 hours, 6 hours, a day; it shows whether the base prefix is still cached.

PowerShell:
    $env:SCADS_API_KEY = "<your key>"
    python design/package-v5/tools/p0_api_probe_v3.py --model "openai/gpt-oss-120b" --model "MiniMaxAI/MiniMax-M3" --out design/package-v5/inputs/p0-api-probe3-output.json
    python design/package-v5/tools/p0_api_probe_v3.py --model "zai-org/GLM-5.3" --pause 35 --out design/package-v5/inputs/p0-api-probe3-glm-output.json
    # lifetime (later, any model; appends one line per run):
    python design/package-v5/tools/p0_api_probe_v3.py --mode lifetime --model "openai/gpt-oss-120b" --out design/package-v5/inputs/p0-api-lifetime.jsonl
    Remove-Item Env:SCADS_API_KEY
"""
import argparse, copy, json, os, secrets, sys, time, re, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--model", action="append", required=True)
ap.add_argument("--base", default="https://llm.scads.ai/v1")
ap.add_argument("--mode", choices=["variants", "lifetime"], default="variants")
ap.add_argument("--max-tokens", type=int, default=64)
ap.add_argument("--pause", type=float, default=0.0)
ap.add_argument("--out", required=True)
a = ap.parse_args()
KEY = os.environ.get("SCADS_API_KEY")
if not KEY:
    sys.exit("Set SCADS_API_KEY in this terminal first (see the docstring). Nothing was sent.")


def scrub(s):
    return re.sub(r"[0-9a-f]{40,}", "<hex-redacted>", s)  # LiteLLM prints a hash of the key in rate-limit messages


def req(path, body=None, retry=True):
    data = None if body is None else json.dumps(body).encode("utf-8")
    r = urllib.request.Request(a.base.rstrip("/") + path, data=data, method="GET" if body is None else "POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), round(time.time() - t0, 2), 0
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")
        if e.code == 429 and retry:
            time.sleep(65)
            s, j, t, n = req(path, body, retry=False)
            return s, j, t, n + 1
        return e.code, {"error_body": scrub(txt)[:400]}, round(time.time() - t0, 2), 0
    except Exception as e:
        return None, {"error": type(e).__name__}, round(time.time() - t0, 2), 0


SYSTEM = ("You are a test assistant for a cache probe. " + " ".join(
    f"Rule {i}: answer briefly, use tools only when the user asks for a tool by name, and never invent tool names." for i in range(1, 121)))


def tool(i, text=None):
    desc = text if text is not None else f"Test tool number {i}. Returns the string 'ok {i}'. " * 3
    return {"type": "function", "function": {"name": f"tool_{i:02d}", "description": desc,
            "parameters": {"type": "object", "properties": {"note": {"type": "string", "description": "free text"}}, "required": []}}}


BASE_TOOLS = [tool(i) for i in range(1, 21)]
NONCE = secrets.token_hex(6)


def variant_tools(kind):
    t = copy.deepcopy(BASE_TOOLS)
    mark = f" [nonce {NONCE}-{kind}]"
    if kind == "end-add":
        t.append(tool(21, f"Test tool number 21. Returns the string 'ok 21'. " * 3 + mark))
    elif kind in ("first-edit", "middle-edit", "last-edit"):
        idx = {"first-edit": 0, "middle-edit": 9, "last-edit": 19}[kind]
        t[idx] = tool(idx + 1, f"Test tool number {idx + 1}. Returns the string 'ok {idx + 1}'. " * 3 + mark)
    return t


def call(model, tools, system, user="Reply with the single word: ready."):
    if a.pause:
        time.sleep(a.pause)
    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "tools": tools,
            "max_tokens": a.max_tokens, "temperature": 0}
    st, js, secs, retries = req("/chat/completions", body)
    out = {"http": st, "seconds": secs, "retries_after_429": retries}
    if isinstance(js, dict):
        out["usage"] = js.get("usage")
        for k in ("error_body", "error"):
            if k in js:
                out[k] = js[k]
    return out


report = {"script": "p0_api_probe_v3", "mode": a.mode, "base": a.base, "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "nonce": NONCE}
for m in a.model:
    if a.mode == "lifetime":
        report[m] = {"V0_base": call(m, BASE_TOOLS, SYSTEM)}
        continue
    r = {}
    r["V0_base"] = call(m, BASE_TOOLS, SYSTEM)
    r["V1_end_add"] = call(m, variant_tools("end-add"), SYSTEM)
    r["V2_first_edit"] = call(m, variant_tools("first-edit"), SYSTEM)
    r["V3_middle_edit"] = call(m, variant_tools("middle-edit"), SYSTEM)
    r["V4_last_edit"] = call(m, variant_tools("last-edit"), SYSTEM)
    r["V5_system_tail"] = call(m, BASE_TOOLS, SYSTEM + f" [nonce {NONCE}-sys-tail]")
    r["V6_system_head"] = call(m, BASE_TOOLS, f"[nonce {NONCE}-sys-head] " + SYSTEM)
    r["V7_base_again"] = call(m, BASE_TOOLS, SYSTEM)
    report[m] = r
if a.mode == "lifetime":
    with open(a.out, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")
else:
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
print("written", a.out)
