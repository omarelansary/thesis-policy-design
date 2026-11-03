# NOTE: local paths are replaced by placeholders in this published copy; the version that ran had the real paths (hash in RESULTS-R2.md).
"""Merge the per-model A1 files into r2-scads-<date>.json and r2-openai-<date>.json and write a per-model/per-cell summary (counts only)."""
import glob, json, os, sys
from collections import Counter

R2 = "<exchange>/prior-work/v5-probes/results/R2/"
DATE = "2026-11-02"
REQ, SUBSET = "tool_07", {"tool_03", "tool_04", "tool_05"}
CELLS = ["C2 allowed-chat", "C4 allowed-required", "C6 named", "C8 instruction-only", "C9 responses-api"]


def classify(r):
    if r["status"] != 200:
        return f"HTTP {r['status']}" if r["status"] else "no response"
    t = r["tools_called"]
    if not t:
        return "no tool"
    if REQ in t:
        return "requested tool_07"
    if all(x in SUBSET for x in t):
        return "subset"
    return "other tool"


summary = {}
for kind in ("scads", "openai"):
    files = sorted(glob.glob(R2 + f"raw/r2-{kind}-*-{DATE}.json"))
    merged = None
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        if merged is None:
            merged = {k: v for k, v in d.items() if k != "models"}
            merged["models"] = {}
            merged["started_utc_first_file"] = d["started_utc"]
            merged["merged_from"] = []
        merged["models"].update(d["models"])
        merged["merged_from"].append({"file": "raw/" + os.path.basename(f), "started_utc": d["started_utc"]})
    if merged is None:
        continue
    merged.pop("started_utc", None)
    json.dump(merged, open(R2 + f"r2-{kind}-{DATE}.json", "w", encoding="utf-8"), indent=1)
    for m, rows in merged["models"].items():
        s = {"cells": {}, "served_model": Counter(), "system_fingerprint": Counter(), "x-litellm-version": Counter(), "x-litellm-headers_seen": Counter()}
        for r in rows:
            c = s["cells"].setdefault(r["cell"], {"classes": Counter(), "output_types": Counter(), "finish": Counter()})
            c["classes"][classify(r)] += 1
            if r.get("finish_reason"):
                c["finish"][r["finish_reason"]] += 1
            me = r.get("meta") or {}
            if me:
                s["served_model"][me.get("served_model")] += 1
                s["system_fingerprint"][me.get("system_fingerprint")] += 1
                h = me.get("headers") or {}
                s["x-litellm-version"][h.get("x-litellm-version")] += 1
                for k in h:
                    s["x-litellm-headers_seen"][k] += 1
                if me.get("output_types") is not None:
                    c["output_types"][",".join(x or "?" for x in me["output_types"])] += 1
        summary[m] = s


def fmt(c):
    return ", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: str(kv[0])))


out = ["| model | cell | requested tool_07 | subset (tool_03/04/05) | other tool | no tool | errors |", "|---|---|---|---|---|---|---|"]
for m, s in summary.items():
    for cell in CELLS:
        c = s["cells"].get(cell)
        if not c:
            continue
        cl = c["classes"]
        err = fmt({k: v for k, v in cl.items() if k.startswith("HTTP") or k == "no response"}) or "0"
        out.append(f"| {m} | {cell.split()[0]} | {cl.get('requested tool_07', 0)} | {cl.get('subset', 0)} | {cl.get('other tool', 0)} | {cl.get('no tool', 0)} | {err} |")
out.append("")
out.append("| model | `x-litellm-version` | served model id(s) | system_fingerprint | x-litellm-* headers seen |")
out.append("|---|---|---|---|---|")
for m, s in summary.items():
    out.append(f"| {m} | {fmt(s['x-litellm-version'])} | {fmt(s['served_model'])} | {fmt(s['system_fingerprint'])} | {', '.join(sorted(s['x-litellm-headers_seen'])) or 'none'} |")
out.append("")
out.append("C9 `/responses` output item types per model (replies with HTTP 200):")
for m, s in summary.items():
    c = s["cells"].get("C9 responses-api")
    if c:
        out.append(f"- {m}: {fmt(c['output_types']) or 'no 200 reply'}; finish reasons not applicable")
open(R2 + "A1_summary_tables.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
