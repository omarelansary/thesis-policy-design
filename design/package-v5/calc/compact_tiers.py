"""D-03: how much does shrinking the APPENDED definitions (the exposé's compact-interface idea, EX-2) change the tool-block bill?
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Same inputs and assumptions as regime_bill.py
(see its header): w = 1.25, r = 0.1, o = 5, H = 5,000, q = 150, K = 3 matches per search, core = 5 tools + a 300-token search tool,
d = 250 tokens per full definition, T = 10 requests.
The ONLY new assumption is the compact size of an appended entry: 0.4 of the full definition. The exposé gives no figure for
its L0-L3 levels (design/package-v5/inputs/expose/Omar_ElAnsary_Master_Thesis_Expose_050626.pdf, page 4), so 0.4 is a
placeholder to show the order of magnitude, not a result; vary FRACTION to see the sensitivity.
Only the appended K definitions per discovery are shrunk; the core prefix keeps full definitions.
Run: python design/package-v5/calc/compact_tiers.py
"""
W, O, H, Q, K, CORE, SEARCH, D_FULL, T, R = 1.25, 5.0, 5000, 150, 3, 5, 300, 250, 10, 0.1


def expose_all(n):
    return n * D_FULL * (W + (T - 1) * R)


def deferral(disc, mode, d_app):
    p = CORE * D_FULL + SEARCH
    reqs = T + (disc if mode == "client" else 0)
    prefix = p * (W + (reqs - 1) * R)
    per = (H * R if mode == "client" else 0) + O * Q + K * d_app * (W + (T / 2) * R)
    return prefix + disc * per


print("Ratio deferral / expose-all for the tool block; appended entries at FRACTION of the full size (core stays full)")
print(f"{'FRACTION':>9} {'tools':>6} {'D':>3} {'mode':>7} {'ratio':>7}")
for frac in (1.0, 0.7, 0.4, 0.2):
    for n in (100, 400):
        for disc in (3, 10):
            for mode in ("client", "server"):
                print(f"{frac:>9} {n:>6} {disc:>3} {mode:>7} {deferral(disc, mode, D_FULL * frac) / expose_all(n):>7.3f}")
print("\nReading: with K = 3 matches per search, the appended definitions are about half of the per-discovery cost,")
print("so tiering them cuts the deferral bill of the tool block by roughly a fifth to a third at FRACTION 0.4; the saving")
print("grows with searches per session D and with K. It does not change which regime is cheapest. Whether tiered entries keep")
print("accuracy (the model may need the full schema to call correctly) is not shown here (05 P2/P3).")
