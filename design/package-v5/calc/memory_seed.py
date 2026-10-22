"""When does memory-informed offering pay in bill terms? And what does 'negligible' caching cost (REQ-O21-04)?
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Units: fresh-input-token equivalents.
Same inputs and assumptions as regime_bill.py (DPR-0006 section 2; w = 1.25, r = 0.1 / 0.05 / 0.025, o = 5,
H = 5,000, q = 150, d = 250 tokens per definition).
Revision 2 (2026-10-22, after RV-0021 CH-0075): a needed seed is read on T-1 requests where a tool discovered in the
middle of the session is read on about T/2, so a needed seed saves the search but costs the longer carry; the search
it saves is priced in both discovery modes ('client' = an extra request, 'server' = output tokens only).

Revision 3 (2026-10-22, after RV-0023 R1): a search appends K matches (K = 3 in regime_bill.py), of which one is the
needed tool; an avoided search therefore also avoids writing and carrying the K-1 other matches. Results are shown
for K = 1 (the revision-2 case) and K = 3.

Part 1. A returning user's session of T requests. m tools are seeded from memory at the first user turn that names a
task (appended after the shared prefix, written once). h = the fraction of seeded non-core tools that are called in the
session (precision of the seed set; core tools are offered anyway and are not counted).
  saving per needed seed  = S + (K-1)*d*(w + (T/2)*r) - d*r*((T-1) - T/2)
                            with S = H*r + o*q (client) or o*q (server)
  cost per unneeded seed  = d*(w + (T-1)*r)
  seeding pays when h*saving > (1-h)*cost; h* = cost / (saving + cost); 'never' when saving <= 0.
Part 2. 'Negligible' cost of keeping K added tokens in a cached prefix for T requests, against re-sending them
uncached and against not adding them at all.
Run: python design/package-v5/calc/memory_seed.py
"""
W, O, H, Q, D = 1.25, 5.0, 5000, 150, 250


def hstar(t, r, mode, k):
    s = (H * r if mode == "client" else 0) + O * Q
    saving = s + (k - 1) * D * (W + (t / 2) * r) - D * r * ((t - 1) - t / 2)
    cost = D * (W + (t - 1) * r)
    return None if saving <= 0 else cost / (saving + cost)


print("Part 1: break-even h* = share of seeded non-core tools that must be called for seeding to pay")
for k in (1, 3):
    for mode in ("client", "server"):
        print(f"  K = {k} matches per search, discovery mode {mode}")
        print(f"  {'r':>6} " + " ".join(f"T={t:<6}" for t in (3, 10, 30, 100)))
        for r in (0.1, 0.05, 0.025):
            print(f"  {r:>6} " + " ".join(f"{(f'{h:.2f}' if h is not None else 'never'):<8}" for h in (hstar(t, r, mode, k) for t in (3, 10, 30, 100))))
print("Reading: the break-even depends on how many matches a search appends (K) as much as on session length. With")
print("K = 1, seeding needs a third to a half of seeds used in short sessions and may never pay in long ones at r = 0.1;")
print("with K = 3 it needs about a fifth to a half. The arithmetic does not settle whether seeding pays: it gives the")
print("threshold that P1 must compare the measured precision h with, using the observed K, T, history size and mode.")

print("\nPart 2: K = 10,000 added tokens kept for T requests (r = 0.1, w = 1.25)")
print(f"{'T':>5} {'cached':>9} {'uncached':>9} {'cached/uncached':>16} {'cached / one fresh send':>24}")
for t in (1, 3, 10, 30, 100):
    k = 10000
    cached, unc = k * (W + (t - 1) * 0.1), k * t
    print(f"{t:>5} {cached:>9.0f} {unc:>9.0f} {cached/unc:>16.2f} {cached/k:>24.2f}")
print("Reading: against re-sending, caching saves most of the cost after a few requests; against not adding the")
print("tokens at all, the cost grows with every request (0.1 of a fresh send each) and is paid again after a gap.")
