# P1 results: memory-informed offering for returning users (2026-11-10; AUTH-033, INT-T-054)

- **Question (HYP-0017, `05` P1):** for returning users, does offering at session start the tools that memory says this user or
  role needed before lower the session bill against discovery from scratch, with accuracy nearly the same?
- **Before the run:** `P1-PREP.md` sections 6 and 7 (desk, no model request). Seeding everything a user needed before reaches
  the break-even in at most 7 to 22 of 64 returning sessions, and its mean precision (0.14) is below every h*. On gold all
  per-user rules lose on the bill except "used in 2+ earlier sessions" (+88 and +10 fresh-token equivalents at T = 8, over the
  15 of 64 sessions it seeds at all; negative at T = 30). A role memory (pop6: the six non-core APIs other users need most,
  outside the current scenario) gains about 2% of a short session at three matches per search.
- **Counts:** `p1-analysis.json` (`tools/p1_analyze.py`; task ids and counts only). Logs local and git-excluded.
- Revised the same day after one review round (AUTH-033); the corrections are listed in WD-086's addendum.

## Run [O]
- **Harness** `tools/p1_memory.py`: AppWorld's own function-calling agent and prompts; declared at start the core (15: every
  supervisor API and every login) + `tools__search` (BM25, top 3 over the 458 other APIs; matches appended to the declared tools)
  + the arm's seeds. No stop rule. GLM-5.3 on OpenRouter pinned to GMICloud fp8, effort as served, temperature 0, seed 100.
- **Arms:** none (no seeds) and pop6 (role memory). The oracle arm was dropped before any run because the projection exceeded
  the lead's P1 limit of $12 (AUTH-033's limits are the lead's; `P1-PREP.md` section 8).
- **Sessions:** AppWorld's 64 returning sessions in fixed order. `P1-PREP.md` section 9 fixed, after the first run, a common set
  of the 44 sessions none r1 completed before its $3 cap. The 35 and then 33 followed when pop6 r1 and pop6 r2 reached their own
  caps (the lead's rule, applied after pop6 r1's cost was seen), so **the set length depends on pop6's spending**, and pop6 r2's
  cut fell in an expensive pop6 session. **33 sessions of 16 users** were completed in all four runs.
- **Spend:** smoke $0.110, none r1 $3.002, pop6 r1 $3.008, an aborted start $0.021, none r2 $2.317, pop6 r2 $2.935 =
  **$11.394** (the lead's limit $12).
- **Scoring:** AppWorld's batch scoring fails after a stop mid-session; every run was rescored one session at a time
  (`tools/aw_eval_per_task.py`), with no errors.

| Run | Sessions completed | Success | Billed | Calls | Searches | Mean prompt | Cached share | Seeds called / seeded (measured h) | Seeds called, not needed |
|---|---|---|---|---|---|---|---|---|---|
| none r1 | 44 | 39 | $3.002 | 535 | 171 | 14,489 | 0.692 | - | - |
| none r2 | 35 | 34 | $2.317 | 405 | 134 | 13,936 | 0.644 | - | - |
| pop6 r1 | 35 | 32 | $3.008 | 424 | 106 | 16,209 | 0.634 | 57 / 210 (0.271) | 7 |
| pop6 r2 | 33 | 30 | $2.935 | 380 | 91 | 18,114 | 0.738 | 53 / 198 (0.268) | 7 |

Billed, calls, mean prompt and cached share are whole-run values: they include the session each capped run stopped in (from the local call traces; the
calls of completed sessions only, as in `p1-analysis.json`, are 534, 405, 400 and 358). Searches and seeds are completed
sessions only. Mean prompt and cached share are not in `p1-analysis.json`.

## Paired, pop6 minus none, per session (averaged over the 2 repeats; 95% bootstrap over users, 4,000 resamples, seed 0)
| | Completed in all runs (33 sessions, 16 users) | Sensitivity: the session cut by a run's cap counted as a failure with its spend so far (34, 17) |
|---|---|---|
| Success | +0.015 (−0.081 to +0.121) | −0.015 (−0.135 to +0.097) |
| Billed | −$0.011 (−$0.039 to +$0.008), −16% | +$0.011 (−$0.031 to +$0.074), +16% |
| Calls | −1.35 (−3.23 to −0.09) | −0.84 |
| Searches | −1.14 (−1.72 to −0.63) | −0.99 |

- **Single sessions decide the bill estimate, in both directions:**
  - The −16% rests on one **no-memory** runaway, `76f2c72_3` (none r1: 49 calls, $0.584, failed; the other three runs: 8 calls,
    $0.025, success). Without it the 32-session difference is −$0.003, **−4.6%**.
  - The +16% comes from adding `7d7fbf6_1`: without memory 10 and 7 calls ($0.027, $0.019); with pop6 49 calls ($0.618) in
    repeat 1 (AppWorld's 50-step cap) and 22 calls ($0.923) before the run's cap cut it in repeat 2.
  - Other expensive pop6 sessions: `7d7fbf6_2` (the same user's next session, a sibling of the same scenario, so not independent)
    was cut by pop6 r1's cap after about 24 calls ($0.459); `3c13f5a_3` took 26 calls ($0.368) in pop6 r2 against 13 to 14
    calls ($0.053 to $0.061) without memory and in pop6 r1.
- **By recurrence band** (main set; the band is the precision of seeding everything the user needed before): zero 17 sessions,
  billed −$0.020; low 7, +$0.035; high 9, −$0.031; success differences 0, +0.07, 0. No intervals.
- **Run-to-run flips** (sessions whose success differs between repeats): none 6, pop6 3.

## Reading [I]
- **Role memory saves searches** (about one per session; the interval excludes zero in the main set), and the measured share of
  seeds the model called (0.27) is close to the desk's 0.24 from gold. Over-calling is small (7 seeds called but not needed per
  run).
- **On the bill, P1 shows no effect that can be relied on:** the estimate is −16%, −5% or +16% depending on one or two
  expensive sessions in either arm, and every interval includes zero. The table's mean prompt is higher with pop6
  (+12% and +30%), but those whole-run means include the sessions cut by caps and the runaways; on the 33 sessions completed in
  all four runs the mean prompt per call was 12,985 and 14,305 with pop6 against 15,430 and 14,164 without memory, so larger
  requests are **not shown** (corrected 2026-11-10 after a verifier; an earlier version of this file said "+16% on matched
  35-session sets", which was not a matched comparison).
- **Success:** no difference detected (within about ±0.1 per session on 33 sessions); the sign flips between the two views.
- **Per-user memory** (HYP-0017's main form) was not run live; on gold it loses except the 2+-sessions rule, which seeds almost
  nothing. For role memory the measured h (0.27) is above the break-even at three matches per search in 8-request sessions (h*
  0.18), equal to it at one match per search (0.27) and below it in 30-request sessions at three matches (0.30) (`P1-PREP.md`
  section 6, r = 0.1). Whether the expensive pop6 sessions are caused by the seeds is suggested by `7d7fbf6_1` (both repeats),
  not shown.
- **Step C** (synthetic users) was not run. The lead judged the high-recurrence band (9 sessions, no interval) readable, roughly,
  and the lead's P1 limit was nearly spent. `P1-PREP.md` section 5 made step C conditional on that band proving too thin; **the
  human should confirm** that judgement.
- HYP-0017 stays `proposed`.

## Limits
- One model and provider; 33 sessions of 16 users (half the planned 64; the user-level interval is rough); oracle arm not run.
- **pop6 looks ahead:** it counts every other user's sessions, including later-dated ones (`tools/p1_seed_rules.py`, `pop6`),
  so it is benchmark-wide popularity, not history available at that date.
- The memory is built from gold, not from what the model did in earlier sessions; first sessions were not run.
- Discovery appends to the tools array, which ends the cached prefix there (cached share 0.63 to 0.74 against about 0.9 in P2):
  the bill of discovery itself is high on this route, which affects both arms (V5-R02).
- The users are a construction: AppWorld's tasks ordered by date (`P1-PREP.md` section 4).
