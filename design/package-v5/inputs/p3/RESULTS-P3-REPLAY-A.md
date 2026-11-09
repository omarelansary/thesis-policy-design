# P3 option (a): candidate per-need stop rules replayed on run 4's logs (2026-11-08)

Status: done by the lead with **no model requests and no cost**; **provisional, for the human**. No V5 rule changed. Covered
by INT-T-036.
- **Scripts:** `tools/p3_replay_stop.py` (part 1) and `tools/p3_replay_end_rules.py` (part 2).
- **Counts:** `replay-a-analysis.json` and `replay-a-end-rules.json`.
- **Inputs:** run 4's local logs; search results recomputed with the harness's BM25.

## Why a replay is valid, and where it stops being valid
A rule changes nothing before it first acts. So the no-rule sessions show what a rule session would have seen up to that point
(part 1). The search-withdrawn sessions show what a model does once search is gone, up to a rule's own end point (part 2).
- **Check:** the replayed first NULL equals the logged one in all 180 note sessions (60 per model).
- **Not replayable:** what a model would do after a call that a rule refuses, because the log shows "Done" there. Those sessions
  are counted as "approximate".

## 1. Part 1: the doable need at the moment the rule first fires [O]
No-rule sessions (plain + plainB) of the kinds with a missing tool, 80 per model. State of the doable need Y at the first NULL:

| | MiniMax | DeepSeek | GLM |
|---|---|---|---|
| Y already done | 12 | 13 | 2 |
| **Y's tool already shown, not yet called** | **51** | **51** | **67** |
| Y's tool not yet shown | 1 | 1 | 0 |
| rule never fires | 16 | 15 | 11 |

Waiting for a later NULL changes little: at the second NULL Y is still "shown, not called" in 36, 30 and 52 sessions.

**Reading [I].** Models search for both needs first and act afterwards. So when the rule fires, the doable tool has already been
found but not used. Any stop that ends the session at that point loses Y, and run 4's forced reply did exactly that. Keeping
search open for Y is not needed. What is needed is to let the model call tools it has already found.

## 2. Part 2: end rules after search is withdrawn [O]
Logged stopsearch sessions, kinds with a missing tool, 40 per model.

| Rule | Y kept (M / D / G) | X substitute ran | ended by the rule | requests saved | still at the backstop |
|---|---|---|---|---|---|
| logged stopsearch (no end rule) | 32 / 38 / 34 | 14 / 9 / 9 | 0 | 0 | 22 / 5 / 14 |
| end at the 1st misstep | 20 / 15 / 10 | 8 / 2 / 4 | 28 / 32 / 31 | 210 / 199 / 183 | 1 / 0 / 1 |
| end at the 2nd misstep | 23 / 21 / 17 | 8 / 2 / 4 | 26 / 31 / 23 | 186 / 173 / 144 | 3 / 0 / 2 |
| end at the 3rd misstep | 27 / 27 / 23 | 9 / 3 / 5 | 23 / 24 / 19 | 161 / 138 / 108 | 3 / 0 / 2 |
| end at the 4th misstep | 30 / 28 / 27 | 10 / 3 / 6 | 21 / 23 / 16 | 134 / 125 / 84 | 3 / 0 / 3 |
| **DRY (no count)** | **30 / 36 / 33** | **5 / 2 / 4** | 14 / 20 / 8 | 82 / 96 / 37 | 15 / 2 / 9 |

- A "misstep" is any action after the stop other than a call of an already-shown tool: a guessed name, or an attempt to search.
- **DRY:** a "dry app" is the best-match app of a NULL search. After the first NULL:
  - search is withdrawn;
  - a call of a shown tool in a dry app is refused;
  - at a misstep or a refused call, the session ends only if nothing is pending. Pending means a best match of an earlier search,
    outside the dry apps, state-changing, and not yet called.
- **Both tools present (P, 20 per model):** no rule changed anything (DRY ended 0 sessions; Y kept 17 / 19 / 20, as logged).
- **Approximate part:** in 12, 7 and 3 of the 40 DRY sessions, logged actions follow a call the rule would have refused.

**Reading [I].**
1. **Ending at the m-th misstep is a dial, not a solution.** Each extra misstep tolerated keeps more Y and saves fewer requests.
   Even at four, Y is lower than with no end rule. It is also a count, which the human ruled out.
2. **DRY is the one candidate that survives.**
   - It keeps Y within 1 to 2 sessions of the no-end-rule baseline (plain and plainB disagree on up to 5).
   - It does no harm where both tools exist.
   - It blocks most substitute actions in the missing need's app (14 to 5, 9 to 2, 9 to 4) without knowing the gold answer: the
     dry app is simply where the search found nothing new.
   - It ends 8 to 20 of 40 sessions early and saves 10 to 29% of their requests.
3. **DRY does not end every loop.** MiniMax and GLM still reach the backstop in 15 and 9 of 40, because earlier searches leave
   best matches outside the dry app that the model never calls. That is a known gap, not hidden.
4. **DRY needs a live test.** Part of its effect on substitutes is mechanical: those calls are refused. What a model does after a
   refusal (another substitute, a false claim, or an honest reply) is not in the logs.

## 3. Proposal for the human (not made): run 5
- **Variants:** plain and DRY, on the same 20 two-need tasks in kinds P, AF and AS, with the same three models. When DRY ends a
  session, the client sends one request with no tools for the final reply; if tool calls still come back, the session ends there,
  as in run 4.
- **Measured:** Y kept; substitutes; false claims (replies classed as in run 4); backstop hits; requests.
- **Cost:** two of run 4's five variants, so about $1.40 (run 4: $3.51 for five). That is within the $2.21 left.
- **Not run before the human's approval** (INT-T-036).

## Corrections of 2026-11-09 (lead, AUTH-032 as amended by INT-T-053)
Found while building the results deck (`design/package-v5/deck/CLAIM-LEDGER.md`). The text above is left as it was; each point names the line it corrects.
- Line 61: "10 to 29% of their requests" reproduces with the requests of all 40 sessions as denominator (82, 96, 37 saved of 382, 332, 379), not only of the 8 to 20 sessions ended early.
