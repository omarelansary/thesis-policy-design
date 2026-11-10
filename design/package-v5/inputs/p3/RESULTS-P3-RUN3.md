# P3 run 3: the revised no-match rule (2026-11-08)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-028 to INT-T-032. Design:
`README.md` section "Run 3" (variant `rule2`: no app listing; the scope is the apps of each search's best match; a search that
shows no unseen tool of a scope app gets only the note that the catalogue has no further tool for this need; no count, no
threshold). Counts: `run3-analysis.json` (`tools/p3_analyze.py`). Raw logs local and git-excluded. Harness hash `281b8f217991...`.

## Run
| Model (OpenRouter, GMICloud fp8, no fallbacks) | Requests | Failed | Spend |
|---|---|---|---|
| minimax/minimax-m3 | 647 | 0 | $0.162 |
| deepseek/deepseek-v4.1-flash | 607 | 0 | $0.158 |
| z-ai/glm-5.3 | 644 | 0 | $0.407 |
| **Run 3** | 1,898 | 0 | $0.726 |
**P3 total (smoke tests, runs 1 to 3): $4.156 of the $10 stop.** Cells D, A, W, each as `plain` and `rule2` (no expose-all cell,
which is why this run cost less than half of run 2); turn cap 12 as a safety backstop only. Same 20 tasks, temperature 0, one run each.

## 1. Where the tool exists [O]: the rule does no harm
| Target called (of 20), plain / rule2 | MiniMax-M3 | DeepSeek | GLM-5.3 |
|---|---|---|---|
| D deferred | 20 / 20 | 19 / 19 | 20 / 20 |
| W distractor visible | 20 / 20 | 20 / 19 | 20 / 20 |
Every session searched. The note fired in 2, 3 and 0 D or W sessions, and the target was called in each of them; DeepSeek's one
W-rule2 miss is in a session where the rule did not fire.

## 2. Target absent: plain against rule2 [O] (sessions of 20; requests summed over the 20)
| | MiniMax plain / rule2 | DeepSeek plain / rule2 | GLM plain / rule2 |
|---|---|---|---|
| still searching at the 12-request backstop | 11 / 6 | 4 / 3 | 7 / 7 |
| requests | 190 / 168 (-12%) | 159 / 145 (-9%) | 185 / 171 (-8%) |
| a substitute action taken | 6 / 7 | 2 / 3 | 4 / 5 |
| final reply: said it cannot be done | 4 / 7 | 14 / 15 | 10 / 8 |
| final reply: a workaround, disclosed or equivalent | 3 / 6 | 2 / 2 | 2 / 5 |
| **final reply: claimed the requested action without a tool that does it** | **2** / 1 | 0 / 0 | **1** / 0 |
| no final reply (backstop) | 11 / 6 | 4 / 3 | 7 / 7 |
The lead classed the final replies from their first 400 characters and the tools called, as in run 2 [I, one reader]. One
borderline case was classed as a disclosed workaround: MiniMax rule2 recorded a $0 payment for a settle-up and said so. The
false claims:
- **plain:** MiniMax and GLM each updated an existing alarm and said a new one was set; MiniMax said a promo code was applied
  after only reading the cart.
- **rule2:** MiniMax used the send-money tool when asked to request $25 and said a request was sent. This is the same error GLM
  made in run 2 under the listing; this time there was no listing, and the model reached that tool through its own searches.

**What models did after the note** (A-rule2): the note reached 15, 18 and 17 of the 20 sessions. Only 3, 3 and 4 of those ended
with no further search. The median was 3, 4 and 2 further searches, and 6, 3 and 6 sessions still reached the backstop.

**Run-to-run spread** (A-plain is now a second repeat): from run 2 to run 3, backstop hits went 10 to 11, 5 to 4 and 8 to 7;
substitute actions 5 to 6, 2 to 2 and 2 to 4; false claims 0 to 2, 0 to 0 and 0 to 1.

## 3. Against run 2's rule [O]
| A cell, sessions of 20 | MiniMax rule / rule2 | DeepSeek rule / rule2 | GLM rule / rule2 |
|---|---|---|---|
| substitute action | 10 / 7 | 4 / 3 | 6 / 5 |
| false claim | 2 / 1 | 0 / 0 | 2 / 0 |
| backstop | 5 / 6 | 3 / 3 | 2 / 7 |
(The two runs are different runs, so the comparison is looser than plain against rule2 within one run.)

## 4. Reading [I]
1. **Dropping the listing removed run 2's harm.** Against plain in the same run, rule2 added one substitute action per model,
   which is inside the spread plain itself shows between runs (0 to 2). False claims were 1 against plain's 3. In run 2, the rule
   added 2 to 5 substitutes per model. Rule2 did no harm where the tool exists.
2. **As a stop, rule2 is weak.** The note reached 50 of 60 sessions, but only 10 of those 50 ended without another search, and
   requests fell by only 8 to 12%. GLM reached the backstop as often as without the rule. A note from the search tool tells the
   model that nothing is left, but the model still decides when to stop. Each reworded query whose best match lands in a new app
   also widens the scope. Run 2's listing ended sessions sooner (backstop 5, 3, 2), but only by giving models something to act on.
3. **Correction to run 2's reading.** Run 2 tied all four false claims to the listing. Run 3 shows the same kind of claim without
   any rule (3 in plain). The listing raised substitute actions, but false claims also arise without it. Run 2's file carries a
   note pointing here.
4. **What follows for the human's requirement (a dynamic, deterministic stop):** a rule in the tool's result does not end the
   session on its own. Two ways remain that keep the system text free of instructions:
   - **(a) Withdraw search_tools when the note is returned.** The client removes search_tools from the rest of the session, so
     the model can only reply or call a tool it has already seen. This is deterministic and has no count. It costs one change to
     the tools array near the end of a session; the second probe showed the cache stays clean after such a change on GLM-5.3, and
     the other two models are unexplained (`10`).
   - **(b) Keep rule2 and treat the backstop as the bound,** reporting the extra requests as a cost.

   The lead's recommendation: test (a) as a variant on the same 20 tasks. **Proposal for the human, not made.** Cell A, as plain
   and (a), would cost about $0.40; the A cells made 54% of this run's requests. Adding D and W, to check that (a) does no harm
   where the tool exists, brings it to about $0.75.

## Limits
As runs 1 and 2: 20 single-need tasks by the lead, stub results ("Done" for every call, which makes workarounds and claims
easier than real results would), one provider, one run per cell, temperature 0, one reader for the final replies.

## Correction of 2026-11-10 (lead, AUTH-034, found by a verifier of the P1-P4 analysis)
- Line 73 says the second probe "showed the cache stays clean after such a change on GLM-5.3". That contradicts
  `design/package-v5/10-p0-university-api-reading.md` section 7: on GLM-5.3 one tool added at the end of the list left 1,728 of
  5,116 prompt tokens cached (3,328 rewritten, 65%), and an edit of the first tool rewrote 99%; gpt-oss-120b and MiniMax-M3 kept
  95-100% cached in that probe, and the third probe (`10` section 9) explains MiniMax-M3's result by earlier priming (gpt-oss-120b
  stays unexplained). `10` section 7 concludes that this supports V5-R02 on this route.
- P1's traces agree (GLM-5.3 on GMICloud): the cached share of calls made right after the tools array changed was 0.17, 0.18,
  0.17 and 0.20 in the four runs, against 0.77 to 0.86 for calls with an unchanged array.
- So withdrawing `search_tools` mid-session (option (a) above) has a cache cost on a plain prefix-cache route; this matters for
  V5-R17's open item (b). The measured V5-R17 results (runs 4 to 6) are unaffected: they count requests and actions, not the bill.
