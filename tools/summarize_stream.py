#!/usr/bin/env python3
"""Summarise a `claude -p --output-format stream-json --verbose` log for the operational tests.

Prints: session init (cwd, model, tools, agents, mcp servers, skills), every tool call with its result (truncated),
the model that produced each assistant message (lead vs subagent via parent_tool_use_id), and the final results.
Used only to document tests (ops/tests/); it interprets nothing.
usage: python tools/summarize_stream.py LOG.jsonl [--max 400]
"""
import json, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 400
uses, results, models, order = {}, {}, collections.Counter(), []
init = None
finals = []
for l in open(path, encoding="utf-8-sig"):
    try:
        o = json.loads(l)
    except Exception:
        continue
    t = o.get("type")
    if t == "system" and o.get("subtype") == "init":
        init = o if init is None else init
    elif t == "assistant":
        m = o["message"]
        models[(m.get("model"), "subagent" if o.get("parent_tool_use_id") else "lead")] += 1
        for c in m.get("content", []):
            if c.get("type") == "tool_use":
                uses[c["id"]] = (c["name"], c["input"], o.get("parent_tool_use_id"), m.get("model"))
                order.append(c["id"])
    elif t == "user":
        for c in (o.get("message", {}).get("content") or []):
            if isinstance(c, dict) and c.get("type") == "tool_result":
                cont = c.get("content")
                if isinstance(cont, list):
                    cont = " ".join(x.get("text", "") for x in cont if isinstance(x, dict))
                results[c["tool_use_id"]] = (bool(c.get("is_error")), str(cont))
    elif t == "result":
        finals.append(o)
if init:
    print("INIT cwd:", init.get("cwd"), "| model:", init.get("model"), "| permissionMode:", init.get("permissionMode"), "| version:", init.get("claude_code_version"))
    print("  agents:", init.get("agents"))
    print("  mcp_servers:", init.get("mcp_servers"))
    print("  skills:", init.get("skills"))
    tools = init.get("tools", [])
    print("  tools:", [x for x in tools if not x.startswith("mcp__")], "| mcp tools:", sum(1 for x in tools if x.startswith("mcp__")))
print("MODELS (model, role) -> assistant messages:", dict(models))
for i in order:
    n, inp, parent, model = uses[i]
    r = results.get(i)
    who = "SUBAGENT" if parent else "LEAD"
    s = json.dumps(inp, ensure_ascii=False)
    print(f"[{who} {model}] {n} {s[:mx]}")
    if r:
        print(f"    -> {'ERROR ' if r[0] else ''}{r[1][:mx].replace(chr(10), ' ')}")
for f in finals:
    print("RESULT:", (f.get("result") or "")[:3000])
    mu = f.get("modelUsage")
    if mu:
        print("modelUsage:", {k: round(v.get("costUSD", 0), 3) for k, v in mu.items()})
