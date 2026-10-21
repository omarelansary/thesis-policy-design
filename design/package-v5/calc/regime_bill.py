"""First-order bill of the tool block: expose-all with prompt caching versus deferral with a small core and search.
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Units: fresh-input-token equivalents
(multiply by the model's input price to get money). Terms follow DPR-0006 section 2 (C_r = F + w*W + r*R + o*O).

Inputs and where they come from:
  w = 1.25   5-minute cache write multiplier (Anthropic price page; OpenAI GPT-5.6+): FND-0039, EXT-0085, EXT-0086
  r          cache read multiplier 0.1 / 0.05 / 0.025 (Anthropic by model; OpenAI 0.1): EXT-0085, price-anthropic-20261019.md:146-152
  o = 5      output price / input price, stored Anthropic and OpenAI standard rows (DPR-0006 section 2, O_r row)
  d          tokens per tool definition 100 / 250 / 1000 (design/package-v4/01-supervisor-brief.md:8, three sources of different quality)
  window     200,000 and 1,000,000 tokens (same line)
Assumptions [I] (parameters of this sketch, not values chosen for the policy):
  core = 5 tools non-deferred plus a search tool of 300 tokens (vendor advice of 3-5 core tools, EXT-0012)
  each discovery = one extra request that re-reads the cached prefix and H = 5,000 history tokens, writes q = 150 output
  tokens, and appends k = 3 definitions written once (w) and read on about half the remaining requests
  the conversation history itself is common to both policies and left out, except the extra requests' re-read
Run: python design/package-v5/calc/regime_bill.py
"""
W, O, H, Q, K, CORE, SEARCH = 1.25, 5.0, 5000, 150, 3, 5, 300


def expose_all(n, d, t, r):
    p = n * d
    return p * (W + (t - 1) * r)


def deferral(n, d, t, r, disc):
    p = CORE * d + SEARCH
    prefix = p * (W + (t + disc - 1) * r)
    per_disc = H * r + O * Q + K * d * (W + (t / 2) * r)
    return prefix + disc * per_disc


def fits(n, d, window):
    return n * d <= window


print("Tool-block bill per session in fresh-input-token equivalents; ratio = deferral / expose-all (<1: deferral cheaper)")
for r in (0.1, 0.025):
    for t in (3, 10, 30):
        print(f"\nr={r}  requests per warm session T={t}")
        print(f"{'tools':>6} {'d':>5} {'P=n*d':>9} {'fits 200k':>9} {'expose-all':>11} {'defer D=1':>10} {'ratio':>6} {'defer D=3':>10} {'ratio':>6}")
        for n in (20, 100, 400, 1000, 10000):
            for d in (100, 250, 1000):
                a = expose_all(n, d, t, r)
                b1, b3 = deferral(n, d, t, r, 1), deferral(n, d, t, r, 3)
                print(f"{n:>6} {d:>5} {n*d:>9} {'yes' if fits(n, d, 200000) else 'NO':>9} {a:>11.0f} {b1:>10.0f} {b1/a:>6.2f} {b3:>10.0f} {b3/a:>6.2f}")

print("\nCold start per returning session (gap longer than the cache lifetime): the first request writes the prefix again.")
print("Extra cost per return = P*(w - r); expose-all vs deferral prefix, d=250, r=0.1:")
for n in (20, 100, 400, 1000):
    pa, pb = n * 250, CORE * 250 + SEARCH
    print(f"  {n:>5} tools: expose-all {pa*(W-0.1):>9.0f}   deferral {pb*(W-0.1):>7.0f}")

print("\nBreak-even catalogue size n* (deferral cheaper above it), d=250, D discoveries per session:")
for r in (0.1, 0.05, 0.025):
    for t in (3, 10, 30):
        row = []
        for disc in (1, 3, 10):
            n = next((m for m in range(1, 20001) if deferral(m, 250, t, r, disc) < expose_all(m, 250, t, r)), None)
            row.append(f"D={disc}: {n}")
        print(f"  r={r:<5} T={t:<3} " + "  ".join(row))
