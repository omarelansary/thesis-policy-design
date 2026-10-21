"""When does memory-informed offering pay in bill terms? And what does 'negligible' caching cost (REQ-O21-04)?
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Units: fresh-input-token equivalents.
Same inputs and assumptions as regime_bill.py (DPR-0006 section 2; w = 1.25, r = 0.1 / 0.025, o = 5, H = 5,000,
q = 150, d = 250 tokens per definition).

Part 1. A returning user's session of T requests. Without memory, the model discovers each needed non-core tool by
one search (one extra request: re-read prefix and history at r, q output tokens at o, the definition appended and
written once). With memory, m tools the user needed before are offered at session start (appended after the shared
prefix, written once, read on every later request); a fraction h of them is actually needed this session, and each
needed one saves a search. Seeded-but-unneeded tools cost their write and reads for nothing.
  saving = h*m * (H*r + o*q)               (searches avoided; the appended definition is paid in both cases)
  cost   = (1-h)*m * d*(w + (T-1)*r)       (unneeded seeded definitions carried through the session)
  memory pays when saving > cost; h* = break-even hit rate.
Part 2. 'Negligible' cost of keeping K added tokens in a cached prefix for T requests, against re-sending them
uncached and against not adding them at all.
Run: python design/package-v5/calc/memory_seed.py
"""
W, O, H, Q, D = 1.25, 5.0, 5000, 150, 250


def hstar(t, r):
    per_search = H * r + O * Q
    carry = D * (W + (t - 1) * r)
    # h*per_search = (1-h)*carry  ->  h = carry / (per_search + carry)
    return carry / (per_search + carry)


print("Part 1: break-even hit rate h* of memory-seeded tools (seeding pays when more than h* of them are needed)")
print(f"{'r':>6} " + " ".join(f"T={t:<4}" for t in (3, 10, 30, 100)))
for r in (0.1, 0.05, 0.025):
    print(f"{r:>6} " + " ".join(f"{hstar(t, r):<6.2f}" for t in (3, 10, 30, 100)))
print("Reading: in a returning session of 3-10 requests a seeded tool pays if it is needed about a quarter to a")
print("third of the time; in a long session the carried definition costs more, so the needed share must be higher.")

print("\nPart 2: K = 10,000 added tokens kept for T requests (r = 0.1, w = 1.25)")
print(f"{'T':>5} {'cached':>9} {'uncached':>9} {'cached/uncached':>16} {'cached / one fresh send':>24}")
for t in (1, 3, 10, 30, 100):
    k = 10000
    cached, unc = k * (W + (t - 1) * 0.1), k * t
    print(f"{t:>5} {cached:>9.0f} {unc:>9.0f} {cached/unc:>16.2f} {cached/k:>24.2f}")
print("Reading: against re-sending, caching saves most of the cost after a few requests; against not adding the")
print("tokens at all, the cost grows with every request (0.1 of a fresh send each) and is paid again after a gap.")
