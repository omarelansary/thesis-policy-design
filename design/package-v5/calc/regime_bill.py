"""First-order bill of the tool block: expose-all with prompt caching versus deferral with a small core and search.
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Units: fresh-input-token equivalents
(multiply by the model's input price to get money). Terms follow DPR-0006 section 2 (C_r = F + w*W + r*R + o*O).
Revision 2 (2026-10-22, after RV-0021 CH-0076..CH-0080): discovery priced in two modes; a deferral prefix below the
model's minimum cacheable length is priced uncached; sensitivity over D and d; the cold/warm session difference is
shown as a difference only (every session here already starts with a write, so it must not be added again).

Inputs and where they come from:
  w = 1.25   5-minute cache write multiplier (Anthropic price page; OpenAI GPT-5.6+): FND-0039, EXT-0085, EXT-0086
  r          cache read multiplier 0.1 / 0.05 / 0.025 (Anthropic by model; OpenAI 0.1): FND-0039
  o = 5      output price / input price, stored Anthropic and OpenAI standard rows (DPR-0006 section 2, O_r row)
  d          tokens per tool definition 100 / 250 / 1000 (design/package-v4/01-supervisor-brief.md:8, three sources)
Assumptions [I] (parameters of this sketch, not values chosen for the policy; none has an empirical source here):
  core = 5 non-deferred tools plus a search tool of 300 tokens (vendor advice of 3-5 core tools, EXT-0012)
  D = discoveries per session (1, 3, 10); T = requests per session; every session starts cold (one write)
  discovery mode 'client': one extra request re-reading the cached prefix and H = 5,000 history tokens at r, plus
    q = 150 output tokens at o; mode 'server': the search runs inside the same request (Anthropic server-side tool
    search, L/v5-anthropic-tool-search-20261022.md:601-652; DPR-0006 section 1), so only q output tokens are added
  each discovery appends K = 3 definitions, written once (w) and read on about half the remaining requests
  'uncached core': the deferral prefix is below the model's minimum cacheable length (512-4,096 tokens, FND-0037 Q8;
    the minimum applies to the whole prefix including the system prompt, which this sketch leaves out) and is paid
    fresh on every request
Run: python design/package-v5/calc/regime_bill.py
"""
W, O, H, Q, K, CORE, SEARCH = 1.25, 5.0, 5000, 150, 3, 5, 300


def expose_all(n, d, t, r):
    return n * d * (W + (t - 1) * r)


def deferral(n, d, t, r, disc, mode="client", core_cached=True):
    p = CORE * d + SEARCH
    reqs = t + (disc if mode == "client" else 0)
    prefix = p * (W + (reqs - 1) * r) if core_cached else p * reqs
    per_disc = (H * r if mode == "client" else 0) + O * Q + K * d * (W + (t / 2) * r)
    return prefix + disc * per_disc


def nstar(d, t, r, disc, mode, core_cached):
    return next((m for m in range(1, 20001) if deferral(m, d, t, r, disc, mode, core_cached) < expose_all(m, d, t, r)), None)


print("A. Ratio deferral / expose-all for the tool block per session (<1: deferral cheaper); r = 0.1, T = 10")
print(f"{'tools':>6} {'d':>5} " + " ".join(f"{m[:3]}{'/unc' if not c else ''} D={x:<3}" for m, c in (('client', True), ('server', True), ('client', False)) for x in (1, 3, 10)))
for n in (20, 50, 100, 400, 1000):
    for d in (100, 250, 1000):
        a = expose_all(n, d, 10, 0.1)
        cells = [deferral(n, d, 10, 0.1, x, m, c) / a for m, c in (('client', True), ('server', True), ('client', False)) for x in (1, 3, 10)]
        print(f"{n:>6} {d:>5} " + " ".join(f"{v:>12.2f}" for v in cells))

print("\nB. Break-even catalogue size n* (deferral cheaper above it), d = 250")
print(f"{'r':>6} {'T':>4} " + " ".join(f"{m[:3]}{'/unc' if not c else ''} D={x:<3}" for m, c in (('client', True), ('server', True), ('client', False)) for x in (1, 3, 10)))
for r in (0.1, 0.025):
    for t in (3, 10, 30):
        cells = [nstar(250, t, r, x, m, c) for m, c in (('client', True), ('server', True), ('client', False)) for x in (1, 3, 10)]
        print(f"{r:>6} {t:>4} " + " ".join(f"{str(v):>12}" for v in cells))

print("\nC. Break-even n* by definition length, client mode, cached core, r = 0.1, T = 10")
for d in (100, 250, 1000):
    print(f"  d={d:<5} " + "  ".join(f"D={x}: {nstar(d, 10, 0.1, x, 'client', True)}" for x in (1, 3, 10)))

print("\nD. Window: tool block n*d against 200,000 and 1,000,000 tokens (expose-all infeasible above)")
for d in (100, 250, 1000):
    print(f"  d={d:<5} max tools in 200k: {200000 // d:>6}   in 1M: {1000000 // d:>6}")

print("\nE. Cold versus warm session start, d = 250, r = 0.1 (a DIFFERENCE, already inside every row above; do not add)")
print("   A session that starts warm (another session of the same deployment wrote the prefix within the lifetime)")
print("   saves P*(w - r) on its first request:")
for n in (20, 100, 400, 1000):
    pa, pb = n * 250, CORE * 250 + SEARCH
    print(f"  {n:>5} tools: expose-all {pa*(W-0.1):>9.0f}   deferral core {pb*(W-0.1):>7.0f}")
