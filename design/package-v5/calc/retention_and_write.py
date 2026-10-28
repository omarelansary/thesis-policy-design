"""D-05 (V5-R16, REQ-U28-01): what keeping a returning user's cache warm costs, and what the memory write W costs.
Derived arithmetic [D], recomputed by one party (the lead); no measurement. Extends D-04 (price_sensitivity.py), whose
output is unchanged. Units: fresh-input-token equivalents per cached token (Parts 1-2) or per session (Part 3).
Same session model as regime_bill.py / memory_seed.py: core prefix P = 5 tools x 250 + a 300-token search tool = 1,550,
history H = 5,000, a model turn q = 150, output ratio o = 5, client-side search.

Part 1. Paid retention on closed providers (sensitivity only; `11` covers hosted open-weight models). A user-specific
block is written once per session. If the user returns after the short lifetime but within a long one, the long
write turns a cold rewrite (w_short) into a read (r). The premium dw = w_long - w_short is paid on every write.
  pays when the expected number of such returns per write N > N* = dw / (w_short - r)
  Prices (stored pages, checked in SUM-0057): Anthropic 5 min 1.25x, 1 h 2.0x, read 0.1x (0.05x, 0.025x on some
  models) [F2]; OpenAI 30 min 1.25x, 12 h 2.5x, read 0.1x or 0.05x [F11].
Part 1b. Keep-alive pings instead (one ping per short lifetime re-reads the block at r; the ping's own few tokens are
  ignored). Assumption [A]: a read renews the lifetime; stated for Anthropic (F2), not checked for OpenAI.
  pings pay over a gap g when (g / lifetime) * r < w_short - r, i.e. g < lifetime * (w_short - r) / r.
Part 1c. An explicit cache priced per token-hour (Gemini, F14; v5-ls-f12 lines 288-305 and 2074-2087). sigma = storage
  price per hour / input price. Assumption [A]: creating the cache and a cold rewrite both cost the input price (w = 1.0).
  holding pays over a gap g when sigma * g + r < 1.0, i.e. g < (1.0 - r) / sigma hours.
Part 2. The university route (no prices, no retention options): nothing to buy; the lifetime is what the server gives.
  Observed by the human's probes (`10` section 9, single runs): warm about 75 minutes later on all three models;
  after about 5 hours gone on gpt-oss-120b and MiniMax-M3, still warm on GLM-5.3 (over 5.5 h).
Part 3. The memory write W and the memory block (V5-R13): the rule-based tool record costs no tokens. The summary is
  one extra request appended to the session: it re-reads (H + P) at r, adds an instruction of I = 100 fresh tokens and
  writes S summary tokens at o. Next session, the memory block of B tokens (summary plus index) sits after the shared
  prefix: written once (w) and read on T - 1 requests (r).
  C_W = (H + P) * r + I + o * S          C_M(T) = B * (w + (T - 1) * r)
  One avoided client-side search is worth (H + P) * r + o * q (memory_seed.py, revision 4).
Run: python design/package-v5/calc/retention_and_write.py
"""
H, P, Q, O, I = 5000, 1550, 150, 5.0, 100

print("Part 1. Paid retention: returns per write (each after the short lifetime, within the long one) needed to pay the premium")
print(f"  {'provider':<34} {'w_short':>7} {'w_long':>6} {'r':>6} {'N*':>6}")
for name, ws, wl, rs in (("Anthropic 5 min -> 1 h", 1.25, 2.0, (0.1, 0.05, 0.025)), ("OpenAI 30 min -> 12 h", 1.25, 2.5, (0.1, 0.05))):
    for r in rs:
        print(f"  {name:<34} {ws:>7} {wl:>6} {r:>6} {(wl - ws) / (ws - r):>6.2f}")
print("  Reading: on Anthropic one such return in about two of three sessions (N* 0.61-0.65) pays for the 1 h write; on OpenAI")
print("  a single return never pays for the 12 h write (N* 1.04-1.09); the user must come back more than once within 12 hours.")

print("\nPart 1b. Keep-alive pings: longest gap over which pinging is cheaper than a cold rewrite (minutes)")
print(f"  {'lifetime':<22} {'w_short':>7} {'r':>6} {'g_max':>8}")
for name, life, ws, rs in (("Anthropic 5 min", 5, 1.25, (0.1, 0.05, 0.025)), ("OpenAI 30 min [A]", 30, 1.25, (0.1, 0.05))):
    for r in rs:
        print(f"  {name:<22} {ws:>7} {r:>6} {life * (ws - r) / r:>8.0f}")
print("  Reading: at r = 0.1 pinging pays for gaps up to about an hour on Anthropic; cheaper reads stretch it to two or four hours.")

print("\nPart 1c. Explicit cache priced per hour: longest gap over which holding is cheaper than rewriting [A: w = 1.0]")
print(f"  {'model':<18} {'input $':>8} {'read $':>7} {'store $/h':>10} {'r':>5} {'sigma/h':>8} {'g_max (h)':>10}")
for name, inp, rd, st in (("Gemini 3.8 Flash", 0.75, 0.075, 0.50), ("Gemini 2.5 Flash", 0.30, 0.03, 1.00)):
    r, sigma = rd / inp, st / inp
    print(f"  {name:<18} {inp:>8.2f} {rd:>7.3f} {st:>10.2f} {r:>5.2f} {sigma:>8.2f} {(1.0 - r) / sigma:>10.2f}")
print("  Reading: holding a cache pays only for short gaps: about 1.35 h (3.8 Flash, 2026 price) and about 16 minutes (2.5 Flash).")
print("  Prices per token-hour make storage, not the gap distribution alone, decide; these are list prices of one provider.")

print("\nPart 2. University route: no paid retention; observed lifetime brackets (single runs, `10` section 9)")
print("  warm at ~75 min (all three models); cold at ~5 h on gpt-oss-120b and MiniMax-M3; warm at >5.5 h on GLM-5.3.")
print("  A returning session within ~75 min may start warm; after ~5 h it starts cold on two of three models. Narrower")
print("  brackets need the probe's lifetime mode (`p0_api_probe_v3.py --mode lifetime`, not yet run).")

print("\nPart 3. Cost of the memory write and of carrying the memory block, against one avoided client-side search")
print(f"  {'r':>5} {'S':>5} {'C_W':>7} {'search':>7} {'C_W/search':>11}   C_M(T) for B = 500, w = 1.25: T=3 / 10 / 30")
for r in (0.02, 0.1, 0.5):
    search = (H + P) * r + O * Q
    for s in (100, 200, 400):
        cw = (H + P) * r + I + O * s
        cm = [500 * (1.25 + (t - 1) * r) for t in (3, 10, 30)]
        print(f"  {r:>5} {s:>5} {cw:>7.0f} {search:>7.0f} {cw / search:>11.2f}   {cm[0]:.0f} / {cm[1]:.0f} / {cm[2]:.0f}")
print("  Reading: a summary call of 100-400 output tokens costs about 0.8 to 2.5 avoided searches (output dominates at low r);")
print("  carrying a 500-token memory block costs about 0.7 to 0.8 searches' worth in a 10-request session (all three r).")
print("  In P1, V5-R's arm carries C_W + C_M on every returning session; the rule-based tool record adds nothing; whether")
print("  memory pays is then: avoided searches (from seeds) minus unneeded-seed carry minus C_W minus C_M, all measured.")
print("  NOT varied: H, P, q, I, B; the minimum cacheable length (a 500-token block may fall below it and not cache).")
