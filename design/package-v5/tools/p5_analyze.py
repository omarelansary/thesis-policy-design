"""P5 analysis (AUTH-028): merge the request logs of p5_break_even.py runs, keep only complete sessions, and compare with D-01.

Usage: python3 design/package-v5/tools/p5_analyze.py --price IN,CACHED,WRITE,OUT --out FILE.json LOG.jsonl [LOG.jsonl ...]
  --price  dollars per million tokens of the model's own price table (WRITE 0 = no write charge, billed as input)
A session (arm, n, session number) counts only if every request in it returned HTTP 200 and its last request ended the user's
third turn; when a later log repeats an incomplete session, the complete one is used. Bill units: dollars from the price table, and
DPR-0006 fresh-input-token equivalents F + w*W + r*R + o*O with r, w, o taken from the same table.
D-01 comparison: calc/regime_bill.py's formulas with the measured tokens per definition d, requests per session T and searches D,
the table's r, w and o, K = 3; server mode for hosted search (OpenAI), client mode with cached and uncached core for ScaDS
(search_tools is a separate request); the measured-parameter variant is computed for hosted search only. D-01 assumes the whole
definition is deferred; OpenAI's individually deferred functions keep name and description visible, so its prediction fits the
namespace arm better. Derived [O] counts and [D] arithmetic only; no accuracy claim.
"""
import argparse, hashlib, json, sys

ap = argparse.ArgumentParser()
ap.add_argument("logs", nargs="+")
ap.add_argument("--price", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
P_IN, P_C, P_W, P_OUT = [float(x) for x in a.price.split(",")]
R, W, O = P_C / P_IN, (P_W / P_IN if P_W else 1.0), P_OUT / P_IN
TARGET = "orders_get_shipping_status"

rows = []
for i, f in enumerate(a.logs):
    for line in open(f, encoding="utf-8"):
        r = json.loads(line)
        r["_file"] = i
        rows.append(r)

cal = {(r["arm"], r["n"]): r for r in rows if r.get("phase") == "calibration" and r.get("status") == 200}
base = cal.get(("none", 0), {}).get("prompt")
calibration = []
for (arm, n), r in sorted(cal.items(), key=lambda x: (x[0][0], x[0][1])):
    if n == 0:
        continue
    tpd = None
    if base is not None:
        tpd = round((r["prompt"] - base) / n, 1)
    calibration.append(dict(arm=arm, n=n, prompt=r["prompt"], cached=r["cached"], tokens_per_tool=tpd))
eager_d = {c["n"]: c["tokens_per_tool"] for c in calibration if c["arm"] in ("eager", "expose_all")}
for c in calibration:  # billed tokens per deferred definition: the core (indexes 0-4) is billed in full at the eager rate
    if c["arm"] in ("deferred_fn", "deferred_ns") and c["n"] > 5 and c["n"] in eager_d and base is not None:
        core = 5 * eager_d[c["n"]]
        c["billed_tokens_per_deferred_tool"] = round((c["prompt"] - base - core) / (c["n"] - 5), 1)
        c["share_of_full_definition"] = round(c["billed_tokens_per_deferred_tool"] / eager_d[c["n"]], 3)

groups = {}
for r in rows:
    if r.get("phase") != "session":
        continue
    groups.setdefault((r["arm"], r["n"], r["session"], r["_file"]), []).append(r)
sessions = {}
for (arm, n, s, fi), rs in groups.items():
    rs.sort(key=lambda r: (r["turn"], r["step"]))
    complete = all(r["status"] == 200 for r in rs) and rs[-1]["turn"] == 3 and not rs[-1]["tool_calls"]
    if not complete:
        continue
    t = dict(arm=arm, n=n, session=s, start=rs[0].get("start") or "unmarked (revision 1)", log=a.logs[fi], requests=len(rs))
    for k in ("prompt", "cached", "cache_write", "completion", "reasoning"):
        t[k] = sum(r.get(k) or 0 for r in rs)
    t["searches"] = sum(r["tool_calls"].count("search_tools") + r["tool_calls"].count("tool_search") for r in rs)
    t["target_calls"] = sum(1 for r in rs for c in r["tool_calls"] if c.split(":")[-1].split(".")[-1] == TARGET)
    t["first_request_cached_share"] = round(rs[0]["cached"] / rs[0]["prompt"], 3) if rs[0]["prompt"] else None
    fresh = t["prompt"] - t["cached"] - t["cache_write"]
    t["fresh"] = fresh
    t["bill_fresh_equiv"] = round(fresh + W * t["cache_write"] + R * t["cached"] + O * t["completion"], 1)
    t["dollars"] = round((fresh * P_IN + t["cached"] * P_C + t["cache_write"] * (P_W or P_IN) + t["completion"] * P_OUT) / 1e6, 6)
    t["served_models"] = sorted({r.get("model_served") for r in rs if r.get("model_served")})
    sessions[(arm, n, s)] = t  # a later log's complete session replaces an earlier one
sessions = [sessions[k] for k in sorted(sessions, key=lambda k: (k[1], k[0], k[2]))]

ref = "eager" if any(s["arm"] == "eager" for s in sessions) else "expose_all"
ratios = []
for s in sessions:
    if s["arm"] == ref:
        continue
    m = next((x for x in sessions if x["arm"] == ref and x["n"] == s["n"] and x["session"] == s["session"]), None)
    if m:
        ratios.append(dict(arm=s["arm"], n=s["n"], session=s["session"], bill_ratio=round(s["bill_fresh_equiv"] / m["bill_fresh_equiv"], 3),
                           dollar_ratio=round(s["dollars"] / m["dollars"], 3)))


def bill_block(tokens, t, warm):
    """a prefix block of `tokens` read on t requests: cold = one write then reads (D-01), warm = reads only"""
    return tokens * (R * t if warm else W + (t - 1) * R)


def d01_as_written(n, d, t, disc, mode="server", core_cached=True, k=3, core=5, search=300, q=150, h=5000):
    """calc/regime_bill.py (revision 2) with this table's r, w, o: tool block only, cold start. mode 'server' = hosted search inside
    the request; 'client' = one extra request per discovery re-reading the prefix and h history tokens at r (D-01's client mode)."""
    ea = bill_block(n * d, t, False)
    p = core * d + search
    reqs = t + (disc if mode == "client" else 0)
    prefix = bill_block(p, reqs, False) if core_cached else p * reqs
    de = prefix + disc * ((h * R if mode == "client" else 0) + O * q + k * d * (W + (t / 2) * R))
    return ea, de


first = {}
for r in rows:
    if r.get("phase") == "session" and r.get("status") == 200 and r["turn"] == 1 and r["step"] == 1:
        first[(r["arm"], r["n"], r["session"])] = r
pred = []
for x in ratios:
    d = eager_d.get(x["n"])
    s = next(v for v in sessions if v["arm"] == x["arm"] and v["n"] == x["n"] and v["session"] == x["session"])
    e = next(v for v in sessions if v["arm"] == ref and v["n"] == x["n"] and v["session"] == x["session"])
    if not d or (x["arm"], x["n"]) not in cal or (ref, x["n"]) not in cal:
        continue
    D = max(s["searches"], 1)
    client = x["arm"] == "deferral"  # ScaDS: search_tools is a separate request
    T = e["requests"] if client else s["requests"]  # D-01's T excludes the discovery requests in client mode
    ea0, de0 = d01_as_written(x["n"], d, T, D, "client" if client else "server")
    unc = d01_as_written(x["n"], d, T, D, "client", core_cached=False)[1] / ea0 if client else None
    # measured parameters: the searchable surface (core in full, deferred names/descriptions or namespace lines, the search tool)
    surface = cal[(x["arm"], x["n"])]["prompt"] - base
    # tokens added by the first search inside the first request: the loaded definitions (hosted search runs in the request)
    fa, fe = first.get((x["arm"], x["n"], x["session"])), first.get((ref, x["n"], x["session"]))
    appended = None
    if fa and fe and not client:
        appended = (fa["prompt"] - cal[(x["arm"], x["n"])]["prompt"]) - (fe["prompt"] - cal[(ref, x["n"])]["prompt"])
    warm_e, warm_s = e["first_request_cached_share"] > 0.5, s["first_request_cached_share"] > 0.5
    eager_block = bill_block(x["n"] * d, T, warm_e)
    non_tool = e["bill_fresh_equiv"] - eager_block  # system text, history, tool results and output, same task in both arms
    de1 = bill_block(surface, T, warm_s) + (appended or 0) * (1 + (T - 1) * R)
    pred.append(dict(arm=x["arm"], n=x["n"], session=x["session"], start=s["start"], measured_session_ratio=x["bill_ratio"],
                     d01_as_written_tool_block_ratio=round(de0 / ea0, 3),
                     d01_as_written_uncached_core_ratio=(round(unc, 3) if unc is not None else None),
                     d01_measured_params_session_ratio=(None if client else round((de1 + non_tool) / e["bill_fresh_equiv"], 3)),
                     measured_params=dict(d=d, T=T, D=D, surface_tokens=surface, appended_tokens_first_search=appended,
                                          warm_start_eager=warm_e, warm_start_deferral=warm_s, non_tool_bill=round(non_tool, 1)),
                     d01_defaults=dict(K=3, search_tool=300, core=5, deferred_part_billed=0, start="cold",
                                       mode="client (H 5,000 history tokens per discovery)" if client else "server")))


out = dict(logs=[dict(file=f, sha256=hashlib.sha256(open(f, "rb").read()).hexdigest()) for f in a.logs],
           price=dict(input=P_IN, cached=P_C, write=P_W, output=P_OUT, r=round(R, 4), w=W, o=round(O, 3)),
           requests_total=len(rows), requests_ok=sum(1 for r in rows if r.get("status") == 200),
           dollars_all_requests=round(sum((((r.get("prompt") or 0) - (r.get("cached") or 0)) * P_IN + (r.get("cached") or 0) * P_C
                                            + (r.get("completion") or 0) * P_OUT) / 1e6 for r in rows), 4),
           calibration=calibration, sessions=sessions, ratios=ratios, d01_comparison=pred)
with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=1)

print(f"price r={R:.3f} w={W} o={O:.2f}; requests {out['requests_ok']} ok of {out['requests_total']}; ${out['dollars_all_requests']} for all logged requests")
print("calibration (no tool needed):")
for c in calibration:
    print("  ", {k: v for k, v in c.items()})
print(f"{'n':>4} {'arm':12} {'s':>2} {'start':>8} {'req':>3} {'prompt':>8} {'cached':>8} {'out':>5} {'srch':>4} {'tgt':>3} {'1st-cached':>10} {'bill-eq':>9} {'$':>8}")
for s in sessions:
    print(f"{s['n']:>4} {s['arm']:12} {s['session']:>2} {s['start'][:8]:>8} {s['requests']:>3} {s['prompt']:>8} {s['cached']:>8} {s['completion']:>5} {s['searches']:>4} {s['target_calls']:>3} "
          f"{s['first_request_cached_share']:>10} {s['bill_fresh_equiv']:>9} {s['dollars']:>8.5f}")
print("deferral / eager (whole session measured; D-01 as written = tool block, cold, its defaults; D-01 measured = its formula with the measured")
print("surface, appended tokens and start state, plus the measured non-tool part of the eager session):")
for p in pred:
    m = p["measured_params"]
    print(f"  n={p['n']:<4} s{p['session']} {p['arm']:12} measured {p['measured_session_ratio']:<6} D-01 as written {p['d01_as_written_tool_block_ratio']:<6} "
          f"uncached-core {p['d01_as_written_uncached_core_ratio']} D-01 measured params {p['d01_measured_params_session_ratio']} surface {m['surface_tokens']:>6} appended {m['appended_tokens_first_search']} "
          f"warm e/d {m['warm_start_eager']}/{m['warm_start_deferral']} non-tool {m['non_tool_bill']}")
