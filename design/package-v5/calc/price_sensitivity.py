"""D-04: how the V5 break-evens move across the price RANGE of hosted open-weight models (design/package-v5/11-price-ranges.md).
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Same model of the tool block as regime_bill.py and memory_seed.py
(read their headers for the assumptions: core = 5 tools + a 300-token search tool, d = 250, T requests per session, H = 5,000, q = 150,
K matches per search); the ONLY change is that the three price ratios are varied over the ranges seen in the stored price sources:
  r = cache-read price / input price : 0.14 to 1.0 (1.0 = no cache discount)        [11, section 2]
  w = cache-write multiplier         : 1.0 (no write fee listed by any host) to 1.25   [11, section 2]
  o = output price / input price     : 3.1 to 7.5                                    [11, section 2]
Run: python design/package-v5/calc/price_sensitivity.py
"""
H, Q, CORE, SEARCH, D_FULL = 5000, 150, 5, 300, 250


def expose_all(n, t, r, w):
    return n * D_FULL * (w + (t - 1) * r)


def deferral(n, t, r, w, o, disc, k):
    p = CORE * D_FULL + SEARCH
    prefix = p * (w + (t + disc - 1) * r)              # client-side search: one extra request per discovery
    per = H * r + o * Q + k * D_FULL * (w + (t / 2) * r)
    return prefix + disc * per


def nstar(t, r, w, o, disc, k=3):
    return next((m for m in range(1, 30001) if deferral(m, t, r, w, o, disc, k) < expose_all(m, t, r, w)), None)


def hstar(t, r, w, o, k):
    saving = H * r + o * Q + (k - 1) * D_FULL * (w + (t / 2) * r) - D_FULL * r * ((t - 1) - t / 2)
    cost = D_FULL * (w + (t - 1) * r)
    return None if saving <= 0 else cost / (saving + cost)


print("A. Break-even catalogue size n* (deferral cheaper above it); client-side search, T = 10, K = 3, d = 250; cell = n* at o = 3.1 / 5 / 7.5")
print(f"{'r':>5} {'w':>5} | {'D=1':>14} {'D=3':>14} {'D=10':>14}")
for r in (0.14, 0.2, 0.5, 1.0):
    for w in (1.0, 1.25):
        cells = []
        for disc in (1, 3, 10):
            v = [nstar(10, r, w, o, disc) for o in (3.1, 5.0, 7.5)]
            cells.append("/".join(str(x) for x in v))
        print(f"{r:>5} {w:>5} | " + " ".join(f"{c:>14}" for c in cells))

print("\nB. Same, T = 3 (a short returning session)")
print(f"{'r':>5} {'w':>5} | {'D=1':>14} {'D=3':>14} {'D=10':>14}")
for r in (0.14, 0.2, 0.5, 1.0):
    for w in (1.0, 1.25):
        cells = ["/".join(str(nstar(3, r, w, o, disc)) for o in (3.1, 5.0, 7.5)) for disc in (1, 3, 10)]
        print(f"{r:>5} {w:>5} | " + " ".join(f"{c:>14}" for c in cells))

print("\nC. Break-even seed precision h* of memory-seeded tools (seeding pays above it); client-side search, o = 5")
for k in (1, 3):
    print(f"  K = {k}")
    print(f"  {'r':>5} {'w':>5} | " + " ".join(f"T={t:<6}" for t in (3, 10, 30, 100)))
    for r in (0.14, 0.2, 0.5, 1.0):
        for w in (1.0, 1.25):
            print(f"  {r:>5} {w:>5} | " + " ".join(f"{(f'{h:.2f}' if h is not None else 'never'):<8}" for h in [hstar(t, r, w, 5.0, k) for t in (3, 10, 30, 100)]))

print()
print("Reading (from the tables above):")
print("  1. Over the whole observed price range, n* at T = 10 stays within 11-13 (D=1), 20-24 (D=3) and 52-65 (D=10): the break-even depends on")
print("     how many searches a session makes, not on which price ratios apply.")
print("  2. At T = 3 the direction reverses: a weaker cache discount (higher r) RAISES n* (D=10: about 71-99 at r=0.14, 118-134 at r=1.0), because")
print("     every client-side search is an extra request that re-reads the history at r.")
print("  3. The write premium w (1.0 to 1.25) moves n* by up to about 8 tools and the output ratio o (3.1 to 7.5) by up to about 20 (both at T=3, D=10); at T=10 by at most about 11.")
print("  4. The seed break-even h* is likewise driven by session length and matches per search K, not by prices: K=3 gives 0.10-0.25 for T <= 10 and")
print("     0.34-0.57 for T = 30-100; K=1 gives 0.12-0.35 for T <= 10, 0.57-0.77 at T = 30 and 'never' at T = 100, at every price in the range.")
print("  Absolute dollar prices do not enter; only the ratios r, w, o do (design/package-v5/11-price-ranges.md). The arithmetic does not depend on the model.")
