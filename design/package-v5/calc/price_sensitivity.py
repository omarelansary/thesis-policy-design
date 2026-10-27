"""D-04: how the V5 break-evens move across the price RANGE of hosted open-weight models (design/package-v5/11-price-ranges.md).
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Same model of the tool block as regime_bill.py and memory_seed.py
(read their headers for the assumptions: core = 5 tools + a 300-token search tool, d = 250, T requests per session, H = 5,000, q = 150,
K matches per search); the ONLY change is that the three price ratios are varied over the ranges seen in the stored price sources:
  r = cache-read price / input price : 0.02 to 0.50 on official pages, 1.0 (no discount) kept as an extreme   [11, section 2]
  w = cache-write multiplier         : 1.0 (no write fee listed) to 1.25 (Alibaba explicit)   [11, section 2]
  o = output price / input price     : 2.1 to 7.5 (grid 2.1 / 5 / 7.5)              [11, section 2]
Run: python design/package-v5/calc/price_sensitivity.py
"""
H, Q, CORE, SEARCH, D_FULL = 5000, 150, 5, 300, 250
RS = (0.02, 0.05, 0.10, 0.14, 0.2, 0.5, 1.0)
OS = (2.1, 5.0, 7.5)


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
    # revision 2: the avoided client-side request also re-reads the core prefix (CORE*D_FULL + SEARCH tokens), as deferral() charges it
    saving = (H + CORE * D_FULL + SEARCH) * r + o * Q + (k - 1) * D_FULL * (w + (t / 2) * r) - D_FULL * r * ((t - 1) - t / 2)
    cost = D_FULL * (w + (t - 1) * r)
    return None if saving <= 0 else cost / (saving + cost)


print("A. Break-even catalogue size n* (deferral cheaper above it); client-side search, T = 10, K = 3, d = 250; cell = n* at o = 2.1 / 5 / 7.5")
print(f"{'r':>5} {'w':>5} | {'D=1':>14} {'D=3':>14} {'D=10':>14}")
for r in RS:
    for w in (1.0, 1.25):
        cells = []
        for disc in (1, 3, 10):
            v = [nstar(10, r, w, o, disc) for o in OS]
            cells.append("/".join(str(x) for x in v))
        print(f"{r:>5} {w:>5} | " + " ".join(f"{c:>14}" for c in cells))

print("\nB. Same, T = 3 (a short returning session)")
print(f"{'r':>5} {'w':>5} | {'D=1':>14} {'D=3':>14} {'D=10':>14}")
for r in RS:
    for w in (1.0, 1.25):
        cells = ["/".join(str(nstar(3, r, w, o, disc)) for o in OS) for disc in (1, 3, 10)]
        print(f"{r:>5} {w:>5} | " + " ".join(f"{c:>14}" for c in cells))

print("\nC. Break-even seed precision h* of memory-seeded tools (seeding pays above it); client-side search, o = 5")
for k in (1, 3):
    print(f"  K = {k}")
    print(f"  {'r':>5} {'w':>5} | " + " ".join(f"T={t:<6}" for t in (3, 10, 30, 100)))
    for r in RS:
        for w in (1.0, 1.25):
            print(f"  {r:>5} {w:>5} | " + " ".join(f"{(f'{h:.2f}' if h is not None else 'never'):<8}" for h in [hstar(t, r, w, 5.0, k) for t in (3, 10, 30, 100)]))

print()
print("Reading (from the tables above; grid r 0.02-1.0, w 1.0/1.25, o 2.1/5/7.5; everything else fixed as in the header):")
print("  1. T = 10: n* is 11-14 tools (D=1), 19-28 (D=3) and 47-77 (D=10). Over r alone (w=1.0, o=5) it moves at most 1.2x (D=10: 65 to 54); over D it moves about 5x (12 to 60).")
print("  2. T = 3: r matters. With w=1.0, o=5, n* rises with r by 1.5x (D=1) to 1.65x (D=3: 26 to 43); at D=10 (more searches than requests, not a plausible session)")
print("     about 2x (50-85 at r=0.02, 97-121 at r=0.5, 117-134 at r=1.0). A weaker discount raises n* because every client-side search is an extra request that re-reads the history at r.")
print("  3. Where D <= T: w (1.0 to 1.25) moves n* by at most 7 tools (T=10) or 3 (T=3); o (2.1 to 7.5) by up to 27 (T=10, D=10, r=0.02) or 9 (T=3, D<=3).")
print("  4. Seed break-even h*: K=3 gives 0.08-0.21 for T <= 10 and 0.21-0.55 for T = 30-100 (little dependence on r). K=1 gives 0.09-0.29 for T <= 10 and 0.33-0.67 at T = 30;")
print("     at T = 100 it is 0.54 (r=0.02), 0.94 (r=0.10) and 'never' for r >= 0.14, so with one match per search and long sessions r decides whether seeding pays.")
print("  Absolute dollar prices do not enter; only the ratios r, w, o do (design/package-v5/11-price-ranges.md). NOT varied: minimum cacheable length, lifetime / cold cache, d, q, H, hit rate.")
