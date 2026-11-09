"""ADOPTED 2026-11-08 as D-01h, a separate mode of D-01 for vendor-hosted search (INT-T-043, after P5 part A showed that D-01 as
written fits the client route, design/package-v5/inputs/p5/RESULTS-P5-A.md). Original header follows.
PROPOSED, not adopted: a vendor-hosted-search variant of D-01 (calc/regime_bill.py), written after P5's OpenAI side check
(design/package-v5/inputs/p5/RESULTS-P5-B.md, repeat with harness revision 2). D-01 stays as it is until the human decides (AUTH-028
stop rule: the as-written predictions were contradicted by 2.2 to 7.9 times at 100-300 tools). The human decided on 2026-11-07
(INT-T-027): D-01 stays the working equation, this stays a proposal, and revision is decided after P5 part A on ScaDS.
Derived arithmetic [D], one party.

What it changes against D-01's server mode, each from the side check's measurements (gpt-5.4-mini, stub catalogue):
  v   share of a deferred definition that stays billed (OpenAI keeps name and description visible): 0.30 for individually deferred
      functions, 0.036 in namespaces (at 300 tools); D-01 assumes 0
  s0  fixed searchable surface besides the core (the search tool's own definition): about 380 tokens; D-01 assumes 300
  A   tokens a search loads, billed fresh in that request and read afterwards: about 310 (one function's schema) to 1,360 (a whole
      namespace); D-01 assumes K*d = 3 definitions written and read on half the requests
  X   the non-tool part of the session (system text, history, tool results, output), the same in both arms: about 2,300
      fresh-token equivalents for the side check's 3-turn, 5-request session; D-01 prices the tool block only (X = 0)
  start  cold (the prefix is written on the first request) or warm (read from the first request); D-01 prices cold only
Session bill (fresh-input-token equivalents, DPR-0006): block(P) = P*(w + (T-1)*r) cold, P*T*r warm;
  expose-all = block(n*d) + X;  hosted deferral = block(core*d + (n-core)*v*d + s0) + D*A*(1 + (T-1)*r) + X
Check against the side check's cold cells: section A (the inputs are the measured ones; agreement here is a fit, not a test).
Run: python3 design/package-v5/calc/regime_bill_hosted.py
"""
R, W, CORE = 0.1, 1.0, 5  # OpenAI gpt-5.4-mini: cached input 0.1 of input, no write charge


def block(p, t, warm, r=R, w=W):
    return p * (t * r if warm else w + (t - 1) * r)


def expose(n, d, t, warm, x, r=R, w=W):
    return block(n * d, t, warm, r, w) + x


def hosted(n, d, t, warm, x, v, s0=380, a=310, disc=1, r=R, w=W):
    surface = CORE * d + max(n - CORE, 0) * v * d + s0
    return block(surface, t, warm, r, w) + disc * a * (1 + (t - 1) * r) + x


def nstar(d, t, warm, x, v, a, r=R, w=W):
    return next((n for n in range(CORE + 1, 20001) if hosted(n, d, t, warm, x, v, a=a, r=r, w=w) < expose(n, d, t, warm, x, r, w)), None)


print("A. Fit to the side check's cold sessions (d 171, T 5, D 1, X 2,300; measured ratio from RESULTS-P5-B revision 2)")
measured = {("fn", 10): 1.19, ("fn", 30): 0.70, ("fn", 100): 0.44, ("fn", 300): 0.35,
            ("ns", 10): 1.12, ("ns", 30): 0.67, ("ns", 100): 0.29, ("ns", 300): 0.11}
for (arm, n), m in measured.items():
    v, a = (0.30, 310) if arm == "fn" else (0.036, 830)
    ratio = hosted(n, 171, 5, False, 2300, v, a=a) / expose(n, 171, 5, False, 2300)
    print(f"  {arm} n={n:<4} model {ratio:5.2f}  measured {m:4.2f}")
print("  (ns uses A = 830, the middle of the measured 320-1,360; its v of 0.036 is the 300-tool value and too low at 10-30 tools,")
print("   where the namespace lines and the search tool weigh more per tool)")

print("\nB. Break-even n* (hosted deferral cheaper above it); r 0.1, w 1, D 1")
print(f"{'d':>5} {'T':>3} {'X':>5} " + " ".join(f"{lab:>13}" for lab in ("fn cold", "fn warm", "ns cold", "ns warm", "D-01-like")))
for d in (100, 171, 250, 1000):
    for t in (3, 5, 10, 30):
        for x in (0, 2300):
            cells = [nstar(d, t, False, x, 0.30, 310), nstar(d, t, True, x, 0.30, 310),
                     nstar(d, t, False, x, 0.036, 830), nstar(d, t, True, x, 0.036, 830),
                     nstar(d, t, False, x, 0.0, 3 * d)]
            print(f"{d:>5} {t:>3} {x:>5} " + " ".join(f"{str(c):>13}" for c in cells))
print("  D-01-like = v 0, A = 3 definitions, cold: close to D-01's server mode. X does not move n* (it is added to both arms);")
print("  it only pulls the ratio towards 1.")

print("\nC. Bill ratio at 300 tools by visible share v (d 171, T 5, X 2,300, A 310): how much of a definition stays billed matters most")
for v in (0.0, 0.036, 0.15, 0.30, 0.60):
    c = hosted(300, 171, 5, False, 2300, v) / expose(300, 171, 5, False, 2300)
    wm = hosted(300, 171, 5, True, 2300, v) / expose(300, 171, 5, True, 2300)
    print(f"  v={v:<5}  cold {c:5.2f}  warm {wm:5.2f}")
