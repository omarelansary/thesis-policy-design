# P1 results: memory-informed offering for returning users (2026-11-10; AUTH-033, INT-T-054)

- **Question (HYP-0017, `05` P1):** for returning users, does offering at session start the tools that memory says this user or
  role needed before lower the session bill against discovery from scratch, with accuracy nearly the same?
- **Before the run:** `P1-PREP.md` sections 6 and 7 (desk, no model request). Seeding everything a user needed before reaches
  the break-even in at most 7 to 22 of 64 returning sessions; every per-user rule loses on the bill; a role memory (pop6: the
  six non-core APIs other users need most, outside the current scenario) gains about 2% of a short session.
- **Counts:** `p1-analysis.json` (`tools/p1_analyze.py`; task ids and counts only). Logs local and git-excluded.

## Run [O]
- **Harness** `tools/p1_memory.py`: AppWorld's own function-calling agent and prompts; declared at start the core (15: every
  supervisor API and every login) + `tools__search` (BM25, top 3 over the 458 other APIs; matches appended to the declared tools)
  + the arm's seeds. No stop rule. GLM-5.3 on OpenRouter pinned to GMICloud fp8, effort as served, temperature 0, seed 100.
- **Arms:** none (no seeds) and pop6 (role memory). The oracle arm was dropped before any run because the projection exceeded
  AUTH-033's $12 (`P1-PREP.md` section 8).
- **Sessions:** AppWorld's 64 returning sessions in fixed order. none r1 stopped at its $3 cap after 44; pop6 r1 after 35; the
  repeat-2 runs used exactly those 35, and pop6 r2 stopped after 33 (rules fixed before any comparison, `P1-PREP.md` section 9).
  **33 sessions of 16 users** were completed in all four runs.
- **Spend:** smoke $0.110, none r1 $3.002, pop6 r1 $3.008, an aborted start $0.021, none r2 $2.317, pop6 r2 $2.935 =
  **$11.394** (limit $12).
- **Scoring:** AppWorld's batch scoring fails after a stop mid-session; every run was rescored one session at a time
  (`tools/aw_eval_per_task.py`), with no errors.

| Run | Sessions | Success | Billed | Calls | Searches | Mean prompt | Cached share | Seeds called / seeded (measured h) | Seeds called, not needed |
|---|---|---|---|---|---|---|---|---|---|
| none r1 | 44 | 39 | $3.002 | 535 | 171 | 14,489 | 0.692 | - | - |
| none r2 | 35 | 34 | $2.317 | 405 | 134 | 13,936 | 0.644 | - | - |
| pop6 r1 | 35 | 32 | $3.008 | 424 | 106 | 16,209 | 0.634 | 57 / 210 (0.271) | 7 |
| pop6 r2 | 33 | 30 | $2.935 | 380 | 91 | 18,114 | 0.738 | 53 / 198 (0.268) | 7 |

(Billed and calls include the session each capped run stopped in.)

## Paired, pop6 minus none, per session (averaged over the 2 repeats; 95% bootstrap over users, 4,000 resamples, seed 0)
| | Completed in all runs (33 sessions, 16 users) | Sensitivity: interrupted session counted as a failure with its spend so far (34, 17) |
|---|---|---|
| Success | +0.015 (−0.081 to +0.121) | −0.015 (−0.135 to +0.097) |
| Billed | −$0.011 (−$0.039 to +$0.008), **−16%** | +$0.011 (−$0.031 to +$0.074), **+16%** |
| Calls | −1.35 (−3.23 to −0.09) | −0.84 |
| Searches | −1.14 (−1.72 to −0.63) | −0.99 |

- **The one session that flips the bill:** `7d7fbf6_1`. Without memory it took 10 and 7 calls ($0.027, $0.019); with pop6 it
  ran to AppWorld's 50-step cap in repeat 1 (49 calls, $0.618) and was cut by the run's cap in repeat 2 ($0.923 spent). The same
  user's next session, `7d7fbf6_2`, also ran away under pop6 (repeat 1), and took 10 calls without memory.
- **By recurrence band** (main set; the band is the precision of seeding everything the user needed before): zero 17 sessions,
  billed −$0.020; low 7, +$0.035; high 9, −$0.031; success differences 0, +0.07, 0.
- **Run-to-run flips** (sessions whose success differs between repeats): none 6, pop6 3.

## Reading [I]
- **Role memory saves searches** (about one per session, in both views), and the measured share of seeds the model called
  (0.27) matches the desk estimate from gold (0.24). Over-calling is small (7 seeds called but not needed per run).
- **On the bill, P1 shows no reliable effect.** The seeds make every request larger (mean prompt +12% to +30%), which offsets
  most of what the avoided searches save, and one user's sessions ran away with the seeds. Runaways (a session running to the
  step cap or until the run's cap) occur in both arms: without memory once (`76f2c72_3`, repeat 1 only, 49 calls), with pop6
  three times, all on one user's two sessions (`7d7fbf6_1` in both repeats, `7d7fbf6_2`). That the seeds cause them there is
  suggested, not shown. Including or excluding that one
  session moves the estimate from −16% to +16%, and both intervals include zero.
- **Per-user memory** (HYP-0017's main form) was not run; the desk check on gold showed it losing in every setting. The falsifier
  ("seed precision below h*") is met for per-user memory on these users by gold; for role memory measured h (0.27) is above the
  break-even at three matches per search in 8-request sessions (h* 0.18), equal to it at one match per search (0.27) and below
  it in 30-request sessions at three matches (0.30) (`P1-PREP.md` section 6, r = 0.1).
- **Step C** (synthetic users) is not run: the high-recurrence band can be read (9 sessions, though roughly), and AUTH-033's
  P1 limit is nearly spent.
- HYP-0017 stays `proposed`.

## Limits
- One model and provider; 33 sessions of 16 users (half the planned 64; the user-level interval is rough); oracle arm not run.
- The memory is built from gold, not from what the model did in earlier sessions; first sessions were not run.
- Discovery appends to the tools array, which ends the cached prefix there (cached share 0.63 to 0.74 against about 0.9 in P2):
  the bill of discovery itself is high on this route, which affects both arms (V5-R02).
- The users are a construction: AppWorld's tasks ordered by date (`P1-PREP.md` section 4).
