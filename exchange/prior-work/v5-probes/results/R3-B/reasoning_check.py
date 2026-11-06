#!/usr/bin/env python
"""Stage 1 of AUTH-025 (lead, 2026-11-06): do MiniMax-M3 replies carry reasoning (a) on ScaDS as served, (b) on OpenRouter gmicloud/fp8
without a reasoning parameter, (c) with reasoning switched on? And is the reasoning sent back on the next turn (prompt tokens of turn 2
with the reasoning kept in the history against stripped)? Counts and field names only are written; the prompt is the lead's own toy task.
Usage: python reasoning_check.py <out.json>"""
import copy, json, os, pathlib, sys, time
from openai import OpenAI

HERE = pathlib.Path(__file__).resolve().parent
for line in (HERE / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TOOLS = [{"type": "function", "function": {"name": "get_price", "description": "Price in cents of one item by name.",
          "parameters": {"type": "object", "properties": {"item": {"type": "string"}}, "required": ["item"]}}},
         {"type": "function", "function": {"name": "submit_answer", "description": "Submit the final answer.",
          "parameters": {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]}}}]
MSGS = [{"role": "system", "content": "You are an agent. Use the tools; do not guess prices."},
        {"role": "user", "content": "I buy 3 apples and 2 pears. Get both prices with get_price, then submit the total in cents with submit_answer."}]
PRICES = {"apple": "45", "pear": "70"}

HOSTS = {
    "scads_as_served": dict(base=os.environ.get("SCADS_BASE_URL", "https://llm.scads.ai/v1"), key="SCADS_API_KEY", model="MiniMaxAI/MiniMax-M3", extra=None),
    "gmicloud_default": dict(base="https://openrouter.ai/api/v1", key="OPENROUTER_API_KEY", model="minimax/minimax-m3",
                             extra={"provider": {"order": ["gmicloud/fp8"], "allow_fallbacks": False}}),
    "gmicloud_reasoning_on": dict(base="https://openrouter.ai/api/v1", key="OPENROUTER_API_KEY", model="minimax/minimax-m3",
                                  extra={"provider": {"order": ["gmicloud/fp8"], "allow_fallbacks": False}, "reasoning": {"enabled": True}}),
}

def summary(r, dt):
    d = r.model_dump()
    m = d["choices"][0]["message"]; u = d.get("usage") or {}
    rd = m.get("reasoning_details") or []
    return {"seconds": round(dt, 2), "provider": d.get("provider"), "finish": d["choices"][0].get("finish_reason"),
            "message_fields_nonempty": sorted(k for k, v in m.items() if v not in (None, "", [], {})),
            "reasoning_chars": len(m.get("reasoning") or ""), "reasoning_content_chars": len(m.get("reasoning_content") or ""),
            "reasoning_details_items": len(rd), "reasoning_details_types": sorted({x.get("type", "?") for x in rd}),
            "think_tag_in_content": "<think" in (m.get("content") or ""), "content_chars": len(m.get("content") or ""),
            "tool_calls": [tc["function"]["name"] for tc in (m.get("tool_calls") or [])],
            "prompt": u.get("prompt_tokens"), "completion": u.get("completion_tokens"),
            "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
            "cached": (u.get("prompt_tokens_details") or {}).get("cached_tokens"), "cost": u.get("cost")}, m

def call(cl, h, msgs):
    kw = dict(model=h["model"], messages=msgs, tools=TOOLS, tool_choice="auto", temperature=0, seed=100)
    if h["extra"]:
        kw["extra_body"] = h["extra"]
    t0 = time.monotonic(); r = cl.chat.completions.create(**kw); return summary(r, time.monotonic() - t0)

out = {}
for name, h in HOSTS.items():
    key = os.environ.get(h["key"])
    if not key:
        out[name] = {"skipped": f"{h['key']} not set"}; continue
    cl = OpenAI(base_url=h["base"], api_key=key, timeout=300.0, max_retries=2)
    try:
        s1, m1 = call(cl, h, MSGS)
        res = {"turn1": s1}
        tcs = m1.get("tool_calls") or []
        if tcs:
            tool_msgs = []
            for tc in tcs:
                try:
                    item = json.loads(tc["function"]["arguments"]).get("item", "").lower().rstrip("s")
                except Exception:
                    item = ""
                tool_msgs.append({"role": "tool", "tool_call_id": tc["id"], "content": PRICES.get(item, "unknown item")})
            # history as AppWorld keeps it: the whole assistant message (reasoning fields included)
            kept = {k: v for k, v in m1.items() if v is not None}
            stripped = {k: v for k, v in kept.items() if k not in ("reasoning", "reasoning_content", "reasoning_details")}
            res["turn2_reasoning_kept"], _ = call(cl, h, MSGS + [kept] + tool_msgs)
            res["turn2_reasoning_stripped"], _ = call(cl, h, MSGS + [stripped] + tool_msgs)
            res["turn2_prompt_difference_kept_minus_stripped"] = (res["turn2_reasoning_kept"]["prompt"] or 0) - (res["turn2_reasoning_stripped"]["prompt"] or 0)
        out[name] = res
    except Exception as e:
        out[name] = {"error": type(e).__name__, "status": getattr(e, "status_code", None), "message": str(e)[:300].replace(key, "<key>")}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
