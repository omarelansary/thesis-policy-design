# P3 run 4: two-need tasks and client-enforced stops (2026-11-08)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-033 to INT-T-035. Design:
`STOP-RULE-RESEARCH-20261108.md` section 4 and the docstring of `tools/p3_two_need.py`.
- **Tasks:** 20 two-need tasks, each joining two single-need tasks of runs 1 to 3 from different apps.
- **Kinds:** P, both tools present; AF, X's tool removed and X named first; AS, X's tool removed and X named second.
- **Variants:** plain and plainB (no rule, run twice); note (run 3's trigger with a typed no_match result); stopreply (from the
  first no_match on, no tools are offered and the session ends if tool calls still come back); stopsearch (from the first
  no_match on, search_tools is withdrawn and call_tool stays).
- No prompt instruction in any variant; turn cap 12 as a backstop only; stub results "Done".

Counts: `run4-analysis.json` (`tools/p3_analyze_two_need.py`) and `run4-replies-adjudicated.json` (classes of the final replies,
counts only). Raw logs are local and git-excluded.

## Run
| Model (OpenRouter, GMICloud fp8, no fallbacks) | Sessions | Requests | Failed | Spend |
|---|---|---|---|---|
| minimax/minimax-m3 | 300 | 2,161 | 0 | $0.749 |
| deepseek/deepseek-v4.1-flash | 300 | 1,924 | 0 | $0.667 |
| z-ai/glm-5.3 | 300 | 2,197 | 0 | $2.094 |
| smoke test (1 task x 15 sessions x 3 models) | 45 | 268 | 0 | $0.120 |
| **Run 4** | 945 | 6,550 | 0 | **$3.630** |

**P3 total (runs 1 to 4 with smoke tests): $7.786 of the $10 stop.** The three models ran in parallel, each with its own spending
cap (GLM $2.60, the others $1.40), so the P3 total could not pass $10.

## 1. Where both tools exist (kind P) [O]: no harm from any rule
Both needs done, of 20 (plain / plainB / note / stopreply / stopsearch):
- MiniMax: 20 / 18 / 20 / 20 / 17
- DeepSeek: 18 / 18 / 19 / 19 / 18
- GLM: 20 / 20 / 20 / 20 / 20

The no_match result fired in 0 to 2 P sessions per variant.

## 2. The doable need when the other tool is missing [O] (Y done, of 20, AF / AS)
| | MiniMax | DeepSeek | GLM |
|---|---|---|---|
| plain | 17 / 20 | 19 / 19 | 16 / 14 |
| plainB (repeat) | 18 / 19 | 20 / 20 | 16 / 15 |
| note | 16 / 20 | 19 / 18 | 15 / 16 |
| **stopreply** | **5 / 9** | **7 / 12** | **5 / 4** |
| stopsearch | 14 / 18 | 19 / 19 | 18 / 16 |

**Paired with plain, task by task** (exact McNemar test on the tasks where only one of the two did Y):
- **stopreply:** plain did Y where stopreply did not in 7 to 12 tasks, the reverse in 0 or 1; p ≤ 0.016 in all six model × kind
  cells.
- **note and stopsearch:** no difference larger than plain against its own repeat. Plain and plainB disagreed on up to 5 of 20
  tasks.

## 3. The missing need [O] (AF + AS, sessions of 40)
| | MiniMax | DeepSeek | GLM |
|---|---|---|---|
| **substitute action in X's app** (plain / plainB / note / stopreply / stopsearch) | 15 / 16 / 14 / 5 / 14 | 5 / 5 / 5 / 4 / 9 | 8 / 5 / 6 / 4 / 9 |
| **called X's removed tool by a guessed name** | 3 / 3 / 2 / 0 / 12 | 12 / 10 / 12 / 2 / 19 | 13 / 10 / 7 / 1 / 15 |
| **still searching at the 12-request backstop** | 15 / 13 / 16 / 0 / 22 | 2 / 4 / 3 / 1 / 5 | 17 / 17 / 13 / 2 / 14 |
| **stopreply: kept calling tools after the stop** (structured, or written out as text) | 21 | 29 | 31 |
| **false claim that X was done** | 6 / 8 / 7 / 0 / 6 | 0 / 0 / 0 / 0 / 1 | 0 / 0 / 0 / 0 / 0 |
| requests (sum) | 375 / 389 / 392 / 207 / 382 | 327 / 321 / 317 / 204 / 332 | 390 / 380 / 345 / 222 / 379 |

**How the final replies were classed** [I, one reader]:
- A keyword filter first sorted out replies that say the action cannot be done, or disclose a workaround.
- The lead read the 45 remaining replies with text (all but those of the two tasks whose workaround is equivalent), including
  the 3 that were cut off in the first pass.
- Workarounds that do what was asked (a wish-list item placed through the cart; a "starred" label) were counted as equivalent.
- The false claims are: an alarm updated and reported as set; volume reported as set with no tool for it; a note reported as
  created; a payment reported as a request; money reported as moved the wrong way; a file reported as copied when a whole folder
  was copied.
- DeepSeek, with no tools offered, wrote its tool calls out as text markup, and GLM did so twice. Those are counted as "kept
  calling tools", not as replies.

## 4. Reading [I]
1. **A session-wide forced reply is not acceptable.** It is the only variant that cut substitutes, backstop hits and requests
   (38 to 45% fewer). But it lost the doable need in 40 to 80% of the tasks, even when that need was named first: models search for both needs before acting on either, so the stop fires before the second tool is called. Most stop
   sessions also did not end with an answer to the user (21, 29 and 31 of 40), because the models kept calling tools that were
   no longer offered.
2. **Withdrawing only the search keeps the doable need, but does not end the loop.**
   - Backstop hits did not fall (MiniMax rose from 15 to 22).
   - Requests did not fall.
   - Guessed calls to the missing tool rose (3 to 12, 12 to 19, 13 to 15): with search gone, models try names through call_tool.
   - Substitute actions did not fall.
3. **The note alone does nothing measurable**, as in run 3.
4. **Substitutes and false claims come from the models, not from the rules.**
   - Substitutes occur without any rule (MiniMax 15 and 16 of 40; DeepSeek 5; GLM 8 and 5).
   - False claims are a MiniMax pattern in every variant but stopreply (6 to 8 of 40). DeepSeek made one, GLM none.
   - This supports the run 3 correction: the claims were not caused by run 2's listing.
   - A search stop cannot prevent a near-miss action. Only removing all tools did, and at the cost in point 1.
5. **What follows for the human's requirement** (a dynamic, deterministic stop):
   - A stop applied to the whole session cannot satisfy it on two-need tasks.
   - Applied only to search, it is not a stop.
   - The rule has to be scoped to the need. No source tests such a rule (research note, point 8), so run 4's logs are the
     development data for one.

## 5. Proposals for the human (not made)
- **(a) Design a per-need rule from run 4's logs, without a new run.** Run 4's local logs show, per session, which tool each
  need's searches surfaced, when the target was called, and what came after the stop. Candidate rules can be replayed against
  these logs to count how often each would have cut a doable need. This costs nothing and spends none of the remaining $2.21.
  One candidate: after no_match, refuse further searches and guessed names for the dry scope only, and force the reply once no
  shown tool from the other scopes is still uncalled. Run only the candidate that survives the replay, as a run 5 within the
  $2.21.
- **(b) Substitutes need their own safeguard.** A request-bound check on state-changing calls (`STOP-RULE-RESEARCH` point 5) is
  not testable in P3, because it would need the gold answer. It belongs to the end-to-end design, where real state checks
  (AppWorld) can score it.
- **(c) Stop P3 here.** Report that no session-level or search-level stop meets the requirement on two-need tasks, and carry the
  per-need rule to the end-to-end study as an open design item.

The lead recommends (a) first, because it costs nothing and decides whether a run 5 is worth its money.

## Limits
- 20 lead-written two-need tasks built from runs 1 to 3; stub results; one provider; one run per cell (plain twice); temperature
  0; one reader for the replies, with a keyword pre-filter.
- "Substitute" counts any state-changing call in the missing need's app other than its own target, so it includes the
  equivalent workarounds.
- With 20 tasks per kind, only large effects show: plain and plainB disagree on up to 5 tasks.
