---
type: summary
status: draft v3 = the analyser's text corrected after verification round 1 (28 problems) and round 2 (23 problems) by four independent verifiers; every correction was checked by the lead against the files; round 3 pending (AUTH-034, INT-T-055)
---
# Analysis of experiments P3, P2 (with P2b), P1 and P4 of the V5 tool-access policy

Written by an independent analyser from the committed evidence files only. The analyser wrote no file in the workspace. No model, API, web or git commit action was taken.

The analyser recomputed the key numbers with read-only `python3 -I` scripts:
- the per-run JSON files for P1, P2, P2b, P3 and P4;
- `calc/memory_seed.py`;
- `tools/p1_recurrence.py` and `tools/p1_seed_rules.py`, which read AppWorld's local data and print counts only.

Path shorthand: `p1/`, `p2/`, `p3/`, `p4/` mean `design/package-v5/inputs/p1/` and so on. `04` means `design/package-v5/04-design.md`.

Labels:
- [O] observed in a file.
- [D] derived by me from numbers in a file; the calculation is shown.
- [I] my interpretation.
- [U] unknown, or not shown.

---

## A. Summary

- **P3 (do models search uninstructed, and what stops a search for a tool that does not exist):**
  - Three open-weight models searched for a deferred tool in 20 of 20 sessions each without being told to, and called the target in 19 to 20 of 20.
  - For a missing tool, no client-side rule stopped the searching without also losing the doable need.
  - The best combination (the DRY rule plus one system sentence, which became V5-R17) kept the doable need at 40/39/37 of 40, cut requests by 32 to 48%, and cut guessed-name loops.
  - The tasks are lead-written, results are stubs, and the rule was developed on the same 20 tasks it was tested on.
- **P2 (offering a subset while all definitions stay cached):**
  - OpenAI `allowed_tools` kept the cache and was enforced (0 calls outside the subset in 120 task-runs). No accuracy difference was detectable. The two OpenAI models gave opposite signs (+11.7 and -5.0 points), and the intervals allow losses of up to 17 points.
  - The instruction-only form worked for two of three models; gpt-5-mini broke it.
  - Declaring only the subset was 20% (gpt-5-mini) and 10% (gpt-5.4-mini) cheaper, for a subset fixed per session on one stream; sharing across users is not priced.
  - The university route itself was not tested.
- **P1 (seeding tools from memory for returning users):**
  - Role memory saved about 1.1 searches per session (interval -1.7 to -0.6).
  - The bill effect is -16%, -5% or +16% depending on one or two sessions, and every interval includes zero. This is one model, 33 sessions of 16 users.
  - Per-user memory was not run live. On gold data it loses on the bill, except one rule that seeds almost nothing. The rule actually tested live was a role memory with look-ahead (see C3).
- **P4 (clearing old tool results):**
  - On short tasks, the vendor's documented example setting roughly doubled the bill (x2.06; x2.66 where clearing fired) and raised calls (x1.37).
  - Long tasks, where clearing is meant to pay, were not tested.
- **Overall picture:**
  - What the four tests support is at the level of mechanism: the cache survives enforced offering, and models search uninstructed.
  - None of the four demonstrates a bill saving from a V5 add-on against run-to-run variation. Point estimates down exist: removal of unoffered definitions (P2 `drop`, x0.80 and x0.90, one stream, sharing not priced), P2b `instr` (x0.80 or x0.85, no interval for the cost) and P3's requests (-32 to -48%, which is requests, not bill, on stub tasks). Enforced offering (x1.02, x1.15) and masking (x2.06) point up, and the sign of P1's bill effect is unresolved. Role memory saves searches. (The large saving of deferral over showing everything is another result: P3 run 1 side observation and P5, see C1 and D.)
  - Every test is one benchmark (AppWorld), short tasks and one to three models. Three of the four (P3, P1, P4) ran only on OpenRouter, not on the university API.

---

## B. How to read this

**Terms.**
- **Cache:** a repeated, identical start of the prompt is billed at a lower "cached" price.
- **Deferral:** tool definitions are not shown; the model gets a search tool and finds definitions on demand.
- **Seeding (memory-informed offering):** at session start, offer tools that memory says were needed before.
- **Masking (clearing):** replace old tool results in the history by a placeholder.
- **Oracle subset:** the tools the gold solution needs plus `complete_task`. This is a best case, because the subset is correct by construction.
- **Enforced vs instructed offering:** enforced means the server refuses calls outside the subset (`allowed_tools`). Instructed means one sentence in the prompt names the subset.
- **Break-even:** the catalogue size above which deferral costs less than showing everything.
- **Backstop:** a cap on requests per session, used in P3 only as a safety net (6 requests in run 1, 12 in later runs).

**"The bill"** is the cost computed from the provider's usage records and a price table (billing equation DPR-0006). The goal is to minimise it on average over turns and sessions, with accuracy nearly the same (`ops/STATE.md` B; `requirements/REGISTER.md` H). No margin or threshold exists. Reporting is estimation-only: paired differences with intervals, no pass or fail (`04` and `p1/RESULTS-P1.md`).

**Models and routes.**

| Test | Models | Route and settings | Data |
|---|---|---|---|
| P3 | MiniMax-M3, DeepSeek-V4.1-Flash, GLM-5.3 | OpenRouter, GMICloud fp8 pinned, temperature 0, seed 7, one run per cell | 20 lead-written tasks over 463 AppWorld tool definitions; tool results are stubs ("Done") (`p3/README.md`) |
| P2 | gpt-5-mini, gpt-5.4-mini | OpenAI Responses API, effort low, temperature 1.0 | 30 AppWorld dev tasks (10 scenarios, Spotify), 128 tools declared, 2 repeats |
| P2b | GLM-5.3 | OpenRouter, GMICloud fp8, Chat Completions, temperature 0, "effort as served" | Same tasks, 2 repeats |
| P1 | GLM-5.3 | Same route as P2b | 33 sessions of 16 users, 2 repeats |
| P4 | GLM-5.3 | Same route as P2b | 20 tasks in 7 scenarios, 2 repeats |

- [O] None of P1 to P4 produced a scored result on the university API (ScaDS). P2b's three ScaDS attempts timed out or returned HTTP 408 and were not scored (`p2/RESULTS-P2B.md`). The university route appears here only as context (P5 part A, P0).
- [O] Who decided what: the lead proposed the P3 models and the human confirmed them (INT-T-030), authorized each run and closed P3 (INT-T-039), and kept HYP-0018 open (INT-T-044). The lead wrote the tasks, harnesses and the classification of replies (one reader). The human set the $10 stop for P3 (INT-T-029) and accepted exceeding it for run 6 (INT-T-038; the $10.60 ceiling was the lead's). The lead set the $12 (P1) and $8 (P4) limits: during P1 and P4 the human was away and "stated none" (AUTH-033, `ops/AUTHORIZATIONS.md`).

---

## C. The four experiments (order by dependency: P3, P2, P1, P4)

### C1. P3: do models search for a deferred tool uninstructed, and what ends a search for a missing tool? (HYP-0019, V5-R17)

**Idea.** If most tools are deferred, the model must decide to search for the one it needs, without being told. The second question was added by the human (INT-T-031): when the tool does not exist, what makes the model stop? The stop had to be dynamic and deterministic, not a count of turns.

**Setup** [O, `p3/README.md`, `p3/P3-LOG.md`].
- Cells:
  - E: all 468 tools shown.
  - D: target deferred.
  - A: target absent.
  - W: a similar wrong tool visible.
- Runs 1 to 3 used single-need tasks. Runs 4 to 6 used 20 two-need tasks in three kinds: both tools present (P), or one tool missing and named first (AF) or second (AS).
- "Substitute" means a state-changing call of another tool in the missing tool's app. "False claim" means saying the missing action was done.
- Total spend $9.953. The per-run sums match the log [D: 1.675 + 1.755 + 0.726 + 3.630 + 1.618 + 0.549].

**Result 1: uninstructed search** [O, `p3/RESULTS-P3-RUN1.md`, recomputed from `run1-analysis.json`]. Sessions out of 20, MiniMax / DeepSeek / GLM; the `plain` prompt variant (an `index` variant made no difference that 20 tasks can show, same file, Reading 2):

| Cell | Measure | Result |
|---|---|---|
| E | target called | 20 / 20 / 20 |
| D | searched, no instruction | 20 / 20 / 20 |
| D | target called | 20 / 19 / 20 |
| W | target called | 19 / 19 / 20 |
| A | substitute action | 3 / 2 / 2 |
| A | still searching at the 6-request cap | 15 / 14 / 15 |

- The repeats in runs 2 and 3 held: D target called 20/20/20 (run 2) and 20/19/20 (run 3) (`p3/RESULTS-P3-RUN2.md`, `p3/RESULTS-P3-RUN3.md`).
- [O, not P3's question] Bill side observation of run 1: per session, expose-all cost 4.6 times (DeepSeek) to 30 times (MiniMax) deferral, on one-turn single-need tasks (`p3/RESULTS-P3-RUN1.md`).
- [I] HYP-0019's falsifier (a large failure rate) is not met on this set.

**Result 2: the missing tool.**
- [O] Run 2's rule listed the matched app's tools once. Substitutes doubled or tripled, for example MiniMax 5 to 10.
- [O] Run 3's note-only rule `rule2` did little. The note reached 50 of 60 sessions and only 10 then ended. Requests fell 8 to 12%.
- [O] Run 4 (kinds P/AF/AS, 40 sessions per model): a session-wide forced reply lost the doable need. Y done was 14/19/9 of 40, against 37 to 40 / 36 to 40 / 30 to 33 with no rule. Withdrawing only search kept Y but made guessed-name calls rise (3 to 12, 12 to 19, 13 to 15).
- [O] The log replay (`p3/RESULTS-P3-REPLAY-A.md`, no model call): at the first no-match, the doable tool was already shown but not yet called in 51, 51 and 67 of 80 sessions. [I, the replay file's reading] Models search for both needs before acting, which is why any stop that ends the session at that point loses the doable need.

**Result 3: runs 4 to 6, AF+AS, 40 sessions per model** (recomputed from `run4/5/6-analysis.json` and the adjudicated-replies files):

| MiniMax / DeepSeek / GLM | No rule (3 copies: range) | DRY (run 5) | DRY + one sentence (run 6) |
|---|---|---|---|
| Doable need done | 37-40 / 36-40 / 30-33 | 34 / 34 / 27 | **40 / 39 / 37** |
| Substitute in the missing app | 12-16 / 4-5 / 5-8 | 5 / 1 / 3 | 7 / 1 / 2 |
| False claim | 5-8 / 0 / 0-1 | 2 / 0 / 0 | 3 / 0 / 0 |
| At the 12-request backstop | 13-15 / 2-8 / 15-17 | 11 / 8 / 11 | **3 / 0 / 1** |
| Missing tool called by guessed name | 3-4 / 10-19 / 10-13 | 11 / 18 / 17 | 2 / 1 / 0 |
| Requests | 375-400 / 321-354 / 380-390 | 323 / 320 / 350 | **254 / 185 / 217** |
| Both tools present, both done (of 20) | 18-20 / 18 / 20 | 18 / 18 / 20 | 20 / 17 / 19 |

- [D] Requests under DRY + sentence against the no-rule range: MiniMax 254/375 to 254/400 gives -32 to -37%. DeepSeek 185/321 to 185/354 gives -42 to -48%. GLM 217/380 to 217/390 gives -43 to -44%. So the file's "32 to 48%" is the span across models.
- [O] With both tools present, DRY plus the sentence gave 20 / 17 / 19 of 20 against a no-rule 18-20 / 18 / 20: DeepSeek's 17 and GLM's 19 are one session below the no-rule range; "no harm" is not shown (`p3/RESULTS-P3-RUN6.md`; `04` corrections).
- **DRY** is the V5-R17 stop. Search is withdrawn after a no-match. Calls into the dry app are refused. The session ends only when no best match outside the dry apps is still uncalled. It has no counter and no threshold.
- [O] The sentence is, exactly: "If a tool search reports that the catalogue has no tool for a need, do not try other tools for that need: tell the user that this part cannot be done, and carry out the rest of the request." (`p3/RESULTS-P3-RUN6.md`)
- [O] The rule fired less with the sentence (24/21/15 sessions against 33/36/34). [O] The file reads this as most of the gain over DRY seeming to come from the sentence, and says the run cannot separate the two parts (`p3/RESULTS-P3-RUN6.md` section 2).
- A footnote on counts: one DeepSeek DRY session did not complete, so its 34 is of 39 complete sessions.

**Strength of evidence.**
- Samples are 20 tasks per cell and 40 sessions per two-need cell. These are small. Only large effects show (`05` section 1).
- [O] Plain and plainB disagree on up to 5 of 20 tasks, so run-to-run spread is large. The route is not deterministic even at temperature 0.
- [O] Only the forced reply in run 4 reached significance (p at most 0.016). No cell of DRY did (`p3/RESULTS-P3-RUN5.md` section 1a). The file reads both DRY effects, fewer substitutes (a gain) and fewer doable needs (a cost), as "very probably real" because DRY lies below the whole no-rule range on both.
- [I] DRY + sentence is compared with no-rule runs made earlier the same day. The comparison is across runs.
- [I] The DRY rule was designed from run 4's logs on the same 20 tasks that runs 5 and 6 then used. The sentence was added after seeing run 5's failure mode. So these results are in-sample.
- [I] Run 6's wording "at or above the no-rule range" holds for MiniMax (40 equals the top of its range 37-40) and GLM (37, above 30-33). DeepSeek's 39 lies inside its range 36-40.
- [O] Replies were classed by one reader (the lead), with a keyword pre-filter (`p3/RESULTS-P3-RUN4.md`).
- [O] The tool results are stubs that always say "Done". [I] The research note reads this as the high-dishonesty condition for false claims (`p3/STOP-RULE-RESEARCH-20261108.md`, point 6, from arXiv 2609.14758). I spot-checked five of the nine stored sources for their quoted phrases and found them. The note otherwise remains a summary.
- [O] Tasks give every value in the prompt, and the harness's BM25 search put the target in the top 3 for 17 of 20 whole-prompt queries. The models' own queries found the target every time. So search quality (recall on a hard ranker) was not tested.

**What P3 does not show.**
- [U] The effect of the sentence alone. There is no instruction-only arm (moved to the end-to-end study).
- [U] The effect on real AppWorld tasks with real results.
- [U] Whether DRY plus the sentence works if `search_tools` stays and answers `no_match` instead of being withdrawn (`04` V5-R17 open item b). A note alone (search left in place) was weak in run 3 (the note reached 50 of 60 sessions and 10 of those then ended; requests fell 8 to 12%) and showed no measurable effect in run 4.
- [U] Other models. MiniMax kept 7 substitutes and 3 false claims of 40 even with the rule, so this is model-dependent.
- [I] V5-R17 withdraws `search_tools`. V5-R02 forbids changing the tools array within a session; `04` V5-R17 item (b) says that on routes with an offering mechanism (Anthropic tool removal, OpenAI `allowed_tools`) the withdrawal needs no array change, and on routes without one it does. This is open item (b).

---

### C2. P2 and P2b: offering a subset while all definitions stay declared and cached (HYP-0018)

**Idea.** If all 128 definitions stay declared (so the cached prefix does not change) and only a subset is offered per task, does accuracy stay nearly the same? Offering fewer tools might help, because the model sees fewer options. HYP-0018 claims no bill saving: the definitions are still read at the cache price.

**Setup** [O, `p2/P2-DESIGN.md`].
- Arms:
  - `all`: everything offered.
  - `enf`: the subset enforced by `allowed_tools`.
  - `instr`: all offered, plus one sentence naming the subset.
  - `drop`: only the subset declared.
- The subsets are oracle subsets of 6 to 10 tools. 30 dev tasks, 2 repeats each. Spend $12.693 in all. The cost matches `main-analysis.json` [D: 12.3777 main + 0.316 pilot].
- P2b ran only `all` and `instr` on GLM-5.3. Its spend was $5.781.

**Results** (recomputed from `main-analysis.json`; the paired intervals reproduce `main-paired-summary.json`). Differences are per task, averaged over the two repeats, with a 95% bootstrap interval over the 10 scenarios.

| Model, arm | Successes of 60 | Difference [interval] | Calls vs all | Cost vs all | Calls outside the subset |
|---|---|---|---|---|---|
| gpt-5-mini `all` | 38 | - | - | - | 12 and 17 (allowed) |
| `enf` | 45 | +0.117 [+0.033, +0.217] | x1.08 | x1.02 | 0 |
| `instr` | 36 | -0.033 [-0.283, +0.183] | x2.03 | x1.37 | 5 and 14 |
| `drop` | 36 | -0.033 [-0.167, +0.083] | x0.97 | x0.80 | 0 |
| gpt-5.4-mini `all` | 40 | - | - | - | 18 and 26 (allowed) |
| `enf` | 37 | -0.050 [-0.167, +0.050] | x1.32 | x1.15 | 0 |
| `instr` | 40 | 0.000 [-0.133, +0.117] | x0.98 | x0.87 | 0 |
| `drop` | 45 | +0.083 [-0.067, +0.233] | x1.14 | x0.90 | 0 |
| GLM-5.3 `all` (P2b) | 55 | - | - | - | 48 and 108 (allowed) |
| `instr` | 59 | +0.067 [-0.033, +0.217] | x0.93 | x0.80 (x0.85 on repeat 2 alone; the first `all` run began with a cold cache, cached share 0.819) | 0 of 412 calls |

- **The cache** [D, `main-analysis.json`]: `enf` cached share was 0.929/0.934 against `all` 0.913/0.915 (gpt-5-mini), and 0.891/0.904 against 0.858/0.897 (gpt-5.4-mini). The cache was not broken.
- **Cost of `drop`:** declaring only the subset gave a prefix of about 8,000 to 12,000 tokens against about 19,500. Cost was 20% lower (gpt-5-mini) and 10% lower (gpt-5.4-mini; that is smaller than the 21% gap between that model's two single `all` runs; the noise of pooled sums is not estimated). The prefix differs per task and per user, so the sharing across users (V5-R06) is lost; which form is cheaper over many users depends on the request rate and is not priced (`p2/RESULTS-P2-MAIN.md` section 3.4, [U]).
- **Cost of `enf`:** no saving (x1.02 and x1.15). [D] The two identical `all` runs of gpt-5.4-mini differ in cost by 21% ($1.172 against $0.967), so the x1.15 is within that single-run gap; the noise of pooled sums is not estimated.
- **Noise:** the two identical `all` runs disagree on 6 and 8 of 30 tasks at temperature 1.0 for the two OpenAI models. In P2b (temperature 0) they disagree on 1 of 30.
- **Per-repeat McNemar tests** [D, recomputed]: none is below 0.05. The smallest p is 0.062 (gpt-5-mini `enf`, repeat 2: 0 `all`-only against 5 `enf`-only).

**Strength of evidence.**
- [O] The file's own corrections (`04` Corrections, `p2/RESULTS-P2-MAIN.md` Corrections) say the supported wording is "no detectable difference, small effects not excluded". The intervals allow losses of up to 17 points (gpt-5.4-mini `enf`) and 28 points (gpt-5-mini `instr`). Six contrasts were made without correction. The scenario bootstrap has only 10 clusters and is called "rough".
- [O] The +11.7 points for gpt-5-mini has the opposite sign to gpt-5.4-mini's -5.0. I would treat this as model-dependent or noise, not as a general gain.
- [I] The oracle subset includes exactly the tools the task needs. In `instr`, the sentence names them. That is a hint as much as a restriction. In `all`, GLM made 22% and 47% of its calls outside the oracle list (48 of 215 and 108 of 228 [D]) and still succeeded 55 times in 60. So the oracle list is not the only working path.
- [U] The jump from 22% (repeat 1) to 47% (repeat 2) at temperature 0 is unexplained in the files.
- [O] `enf` is a server mechanism. [I] The vendor text (it does not modify the list of tools passed in) implies that the unoffered definitions stay visible under `allowed_tools`; no P2 arm checks it.

**Where results conflict.**
- The same instruction form was broken by gpt-5-mini and followed by gpt-5.4-mini and GLM-5.3.
- `enf` was +11.7 points (interval excludes 0) on gpt-5-mini and -5.0 (interval includes 0) on gpt-5.4-mini.
- `drop` was -3.3 on gpt-5-mini and +8.3 on gpt-5.4-mini; both intervals include 0, and the Corrections warn that none of the six contrasts supports an effect.
- P2b's "effort as served" differs from main P2's effort low. `p2b-or-analysis.json` records `reasoning_effort: low`, but the local stats show `no_reasoning_param: true`. [I] The JSON field is probably the harness default (the run's `stats.json` also records `reasoning_effort: low` beside `no_reasoning_param: true`). The files say GMICloud "as served" behaves like effort high (`p2/RESULTS-P2B.md`).

**What P2 and P2b do not show.**
- Realistic subsets that miss a needed tool.
- Offering that changes within a session (the M2 case, where the problem would show).
- Catalogue sizes other than 128, other benchmarks, and Anthropic's mechanism.
- The university route, which has 4-bit weights, maximum effort and no `allowed_tools` (the proxy refuses it).
- Accuracy differences of a few points.

---

### C3. P1: seeding tools from memory for returning users (HYP-0017)

**Idea.** For a returning user, offer at session start the tools that memory says were needed before. If enough seeded tools are actually used, they replace searches and save money. If too few are used, they only add tokens to carry. `calc/memory_seed.py` gives a break-even precision h* (the share of seeds that must be called).

**Setup** [O, `p1/P1-PREP.md`, `p1/RESULTS-P1.md`].
- AppWorld has 34 users who own tasks in 2 to 5 scenarios. Sorted by date, that gives 64 "returning sessions". The ordering is a construction, not a recorded history.
- **Desk check** (no model; I re-ran `p1_recurrence.py` and `p1_seed_rules.py` and reproduced the tables):
  - Seeding "everything used before" has mean precision 0.14. Zero precision occurs in 36 of 64 sessions.
  - All per-user rules lose on the bill, except "used in 2+ earlier sessions", which seeds only 0.3 tools on average (net +88 at K=3, T=8, and about zero or negative otherwise).
  - A "pop6" role memory (the six non-core APIs other users need most, outside the current scenario) has precision 0.24 and net +956 fresh-token equivalents at K=3, T=8. Against a session of about 50,000 [O, approximate] that is about 2% [D: 956/50,000].
  - At K=1 the net is -256. At T=30 it is negative.
- **Live run:** `none` against `pop6`, GLM-5.3, client-side BM25 search returning the top 3, 2 repeats. The oracle arm was dropped by the lead before any run, because the projection exceeded the lead's $12 limit. The run spent $11.394.
- Runs hit their cost caps. The common session set became 33 sessions of 16 users.

**Results** [O, recomputed from `p1-analysis.json`; I reproduced the paired values]:

| Run | Sessions | Success | Billed | Searches | Seeds called / seeded |
|---|---|---|---|---|---|
| none r1 | 44 | 39 | $3.002 | 171 | - |
| none r2 | 35 | 34 | $2.317 | 134 | - |
| pop6 r1 | 35 | 32 | $3.008 | 106 | 57/210 (0.271) |
| pop6 r2 | 33 | 30 | $2.935 | 91 | 53/198 (0.268) |

Paired, pop6 minus none, per session, 33 sessions of 16 users (95% bootstrap over users):

| Measure | Completed in all runs | Sensitivity: the cap-cut session counted as a failure with its spend so far (34 sessions) |
|---|---|---|
| Success | +0.015 (-0.081, +0.121) | -0.015 (-0.135, +0.097) |
| Billed | -$0.011 (-$0.039, +$0.008) = -16% | +$0.011 (-$0.031, +$0.074) = +16% |
| Searches | -1.14 (-1.72, -0.63) | -0.99 |
| Calls | -1.35 (-3.23, -0.09) | -0.84 |

- Only the success and billed cells of the sensitivity column are clean: `tools/p1_analyze.py` enters the cut session with 0 calls and 0 searches, so that column's calls and searches count it as zero and are not comparable with the main column.
- In the run table, Billed includes the session each capped run stopped in, while Sessions count completed sessions only, and the rows cover unequal session sets (44, 35, 35, 33).

- [D] Dropping the single no-memory session `76f2c72_3` (49 calls, $0.584, failed in none r1; 8 calls and $0.025 in the three other runs) gives -$0.0029 per session, -4.6% (32 sessions). I recomputed this.
- [O] The +16% comes from adding `7d7fbf6_1`: with pop6 it took 49 calls ($0.618) and then 22 calls ($0.923, cut by the cap); without memory it took 10 and 7 calls ($0.027, $0.019). It was expensive with pop6 in both repeats, so a seed effect is suggested by this session, not shown. The -16% estimate, by contrast, rests on a no-memory runaway in one repeat only.
- [O] Seeds make requests larger. Mean prompt rises 12 to 30% across unequal session sets [D: 16,209/14,489; 18,114/13,936], and about 16% on the matched 35-session sets (16,209 against 13,936; the mean prompt figures come from the local logs, not from `p1-analysis.json`).
- [O] By recurrence band (main set: zero 17 sessions, low 7, high 9): billed -$0.020, +$0.035, -$0.031 per session; success differences 0, +0.07, 0; no intervals. Run-to-run flips (sessions whose success differs between repeats): none 6, pop6 3.

**Strength of evidence.**
- [O] One model, one provider, 33 sessions of 16 users (half the planned 64). The user-level interval is rough.
- [I] The average session length was about 11 to 12 requests [D, completed sessions only: 534/44 = 12.1, 405/35 = 11.6, 400/35 = 11.4, 358/33 = 10.8]. At K=3, client search and T 11 to 12, the break-even h* is 0.19 to 0.21 at the project's cache-read ratios (r = 0.1, 0.05, 0.025) and up to 0.22 at GLM-5.3's list ratio 0.186 [D, via `memory_seed.py`'s `hstar`, recomputed by the lead]. The measured 0.27 is above that, so by D-02 role memory should pay a little (pop6's net per session at T = 11 to 12 is +580 to +670 fresh-token equivalents at the three ratios, about 1% of a session of roughly 50,000, recomputed by the lead with `tools/p1_seed_rules.py`'s functions). At T = 30 (K=3) h* is 0.30 at r = 0.1 (0.23 to 0.26 at lower r), above the measured 0.27, so the sign depends on session length (`P1-PREP.md` section 6; some sessions ran 49 calls).
- [I] The expected saving (about 1% at T = 11 to 12, about 2% at T = 8) is far smaller than the interval half-width. The paired bill interval is about ±$0.024 on a mean of $0.071 per session, about ±34% [D]. P1 could not have detected a 2% effect either way.
- [O] **Selection effects.** The session set depends on pop6's own spending. The lead's cap rule fixed the set after pop6 r1's cost was seen (`P1-PREP.md` section 9, corrected after review). Sessions that cost pop6 more were cut. [I] That may bias the main set in pop6's favour. The sensitivity view is the file's attempt to show the other side.
- [O] **pop6 looks ahead.** It counts later-dated sessions of other users (`RESULTS-P1.md` Limits). It is not memory a deployed system would have at that date. [I] It also does not depend on the user, so it is closer to a larger core chosen by usage (S1) than to personal memory (`P1-PREP.md` section 7's reading).
- [O] The memory is built from gold, not from what the model did earlier.
- [O] **Route.** Discovered tools were appended to the tools array (docstring of `tools/p1_memory.py`, point 2), which V5-R02 allows ("appended discoveries", `04` line 87). Seeds were declared at session start. Cached share was 0.63 to 0.74 against about 0.9 in P2. [I] On this route, appended discoveries ended the cached prefix, so V5-R02's "appended discoveries" is not cache-safe here (`P1-PREP.md` section 9 calls this V5-R02's question). The effect falls on both arms; its effect on the trade between seeds and searches is [U].
- [O] No stop rule (V5-R17) was used in P1, although the AUTH-033 text mentions it. The harness note says every task is doable.

**What P1 does not show.**
- Per-user memory run live (HYP-0017's main form).
- The oracle arm.
- Memory written from the model's own earlier sessions.
- Other models, or longer sessions.
- A route where discovery keeps the cached prefix.
- Over-calling is small (7 seeds called but not needed per run), but only for pop6.
- A decision on step C (synthetic users). The lead judged the high-recurrence band (9 sessions, no interval) readable, roughly, and the lead's P1 limit was nearly spent. The file asks the human to confirm; the human's condition was "only if the high-recurrence band proves too thin" (`P1-PREP.md` section 5).

---

### C4. P4: clearing old tool results (HYP-0021)

**Idea.** Old tool results sit in the history and are re-read on every request. Replace them by a placeholder, and the prompt is shorter. But a change in the middle of the history makes the cached part after it cost more to re-write. HYP-0021's claim is for long single runs.

**Setup** [O, `p4/P4-CONDITION-CHECK.md`, `p4/P4-REPLAY-A.md`, `p4/RESULTS-P4.md`].
- **Condition check.** In P2's logs, old tool results were 13.1% of billed input. An upper bound of removing them for free was 6.3% and 6.9% of the input bill, or 2.4% and 4.3% of the total bill.
- **Reading:** "P4's condition is not met by our results" (`05` section 2: P4 runs "only if P0-P5 show deployments with large tool results"). The human's AUTH-033 message asked for P4 "if possible"; the lead read that as covering a run despite the condition check. The human has not ruled on the condition (`RESULTS-P4.md`), and the `WD-086` addendum records it as the lead's decision.
- **Step A: replay on the P2 logs.** No new model call, and behaviour held fixed. The vendor's defaults (trigger 100,000 tokens) never fire. The documented example (30,000 / keep 3 / at least 5,000) raised the bill by +1.2% (gpt-5-mini), +1.0% (gpt-5.4-mini) and +7.5% (GLM-5.3).
- **Step B: live.** The client applies the vendor example on GLM-5.3. 20 tasks in 7 scenarios, 2 repeats. The keep arm is P2b's two `all` runs on the same 20 tasks, made a day earlier with the harness version before `--mask` was added (same code path when masking is off). Intervals are 95% scenario bootstraps over 7 scenarios. Spend $5.385.

**Results** (recomputed from `p4-analysis.json`):

| | Success of 20 | Billed | Calls | Cached share | Tasks where clearing fired |
|---|---|---|---|---|---|
| keep r1 / r2 | 18 / 18 | $1.220 / $1.177 | 145 / 157 | 0.820 / 0.922 | - |
| mask r1 / r2 | 17 / 18 | $2.463 / $2.483 | 212 / 201 | 0.835 / 0.743 | 11 / 10 |

- **Paired, mask minus keep, per task:**
  - success -0.025 (-0.175, +0.125);
  - billed +$0.064 (+$0.024, +$0.107), x2.06;
  - calls +2.8 (+0.7, +5.2), x1.37.
- [D, recomputed] Where clearing fired in either repeat (11 tasks): billed x2.66, calls x1.72. Where it never fired (9 tasks): billed x1.00, calls x0.95.
- [D] Mean prompt per call was larger in the mask arm: 33.5k and 32.0k tokens, against 26.7k and 28.2k [7,108,479/212; 6,439,311/201; 3,866,157/145; 4,430,152/157]. Sessions were longer (more calls), so this is not a clean comparison.

**Strength of evidence.**
- [O] One model and provider, 20 tasks, 7 scenarios, one rule setting. There was no cache-write premium on this provider.
- [O] Short tasks: the keep arm's median is about 7 calls. The 20 tasks are P2b's first 20 in fixed order, because repeat 1 hit its $2.50 cap. The lead fixed the rule for repeat 2 after seeing the first 7 tasks' costs and before accuracy. [I] The number of tasks (a prefix of a fixed order) was therefore set by the mask arm's cap.
- [O] The "never fired" check is weak. The groups are defined after the fact by the mask arm, and the never-fired nine are all short (at most 12 calls). It is consistent with no day drift for those tasks.
- [I] The files say the model "called tools again" after a clear. That is suggested, not shown. Repeat 1's cached share equals keep's, so cache rewrites are not shown as the cause there. Repeat 2's was lower (0.743 against 0.922).
- [O] Step A (behaviour held fixed) predicted +1 to 7.5%, step B gave x2.06. [I] Changed behaviour (calls x1.72 where clearing fired) is the suggested reason for the gap; it is not decomposed, and the two measurements differ in tasks (replay: all 30 tasks) and day.

**Correction already made.** The original WD-086 text said "HYP-0021 falsifier met on this setting" (also in the commit 9caf9e9 subject). The addendum and the current `HYP-0021.md` say it is neither met nor refuted, because the falsifier's domain is long single runs.

**What P4 does not show.**
- Long tasks, where clearing is meant to pay.
- Other models or other rule settings.
- Providers with a cache-write premium (which would make clearing costlier).
- Accuracy unchanged (the interval spans -17.5 to +12.5 points).
- AUTH-033 said "the longest available tasks, if feasible". These were not the longest.

---

## D. Across the four

**What fits together.**
- [I] Enforced offering at a fixed prefix does not by itself lower the bill (x1.02 to x1.15). Uninstructed search is what lets deferral lower it (P3 run 1 side observation; P5).
- [I] Where it was tried as a bill reducer on our route: seeds, bill effect not resolved; clearing, cost more.
- [O] P2 `enf` costs x1.02 to x1.15 of `all`. Declaring only the subset saves 20% and 10% (one model each; the 10% is smaller than the 21% gap between that model's two single `all` runs).
- [O] P1 seeds saved searches but not a demonstrable bill.
- [O] P4 doubled the bill.
- [I] For a subset fixed per session on a single stream, declaring only it looks cheaper (P2's own text says so); sharing across users (V5-R06) is not priced.
- [I] The P5 context (as reported; the lead rechecked the figures) is where the largest bill effect was computed (token counts from the university API run, priced by a price table, stub tools). Break-even lies between 10 and 30 tools, and deferral costs about 14 to 15% of expose-all at 100 tools on a cold start (20% warm) (`p5/RESULTS-P5-A.md`).

**What conflicts or depends on the model.**
- P2: the instruction form was followed by two models and broken by one; `enf` was +11.7 points (interval excludes 0) on one OpenAI model and -5.0 (includes 0) on the other.
- P3: MiniMax made far more false claims than DeepSeek and GLM (5-8 against 0 and 0-1 with no rule; 3 against 0 and 0 with DRY plus the sentence), and more substitutes without a rule (12-16 against 4-5 and 5-8) and with DRY plus the sentence (7 against 1 and 2).
- P1 and P2b: P2b (30 Spotify tasks) succeeded 55 of 60; P1's no-memory runs succeeded 39 of 44 and 34 of 35 on other tasks. The difference is a few 49-call sessions, not a success gap; no contradiction is shown.
- P4 step A against step B: the replay and the live result disagree by an order of magnitude on how much clearing costs. Changed behaviour (calls x1.72 where clearing fired) is the suggested reason; it is not decomposed, and the two measurements differ in tasks and day.
- P1 and P3 against V5-R02: P1's appended discoveries are allowed by V5-R02 and were followed by a lower cached share on this route ([I] mechanism, not tested by an arm); P3's V5-R17 withdrawal of search needs no array change on routes with an offering mechanism and does on routes without one.

**V5 stages.** These are statements about evidence, not recommendations.

| V5 stage | Verdict | Basis |
|---|---|---|
| Offering at a fixed prefix (S1, M2 mechanism), enforced, OpenAI | Falsifier not met on this set (HYP-0018 stays `proposed`): mechanism observed (cache kept, 0 of 120 calls outside); accuracy: no detectable difference, small effects not excluded; oracle subsets, 128 tools, 2 OpenAI models, AppWorld Spotify tasks | C2 |
| Offering by instruction on routes without enforcement | **Suggested** for two of three models; **not shown** for the university route | C2 |
| Memory seeding (M2) | **Observed** for pop6 on one model that it saves searches (interval excludes 0); **not shown** on the bill; per-user live **not shown**. The rule tested live was pop6: benchmark-wide popularity from gold with look-ahead, not per-user M2 | C3 |
| Tool search/deferral, uninstructed search | Falsifier not met on 3 models with easy stub tasks (HYP-0019 stays open); ranker quality **not shown** | C1 |
| Stop rule V5-R17 | **Suggested** (provisional); sentence-alone effect and real-task effect **not shown** | C1 |
| Masking | **Not supported on short tasks** (bill x2.06, one model, one setting); the hypothesis's domain (long runs) not tested; falsifier neither met nor refuted | C4 |

**Common weaknesses.**
- **One benchmark:** all on AppWorld, with simulated apps (P3 tasks are lead-written over AppWorld definitions).
- **Short tasks:** median 6 to 8 calls per task in the `all` arms of P2, P2b and P4 (mean 7 to 12), about 11 in P1 (mean 11.5).
- **One to three models per test, and routes unlike the university API.** OpenRouter's GMICloud fp8 was used for P3, P2b, P1 and P4. P2 used OpenAI. P2b's route has 8-bit weights against the university's 4-bit weights.
- **Selection by cost caps:**
  - P1's 33 sessions depend on pop6's spending.
  - P4's number of tasks (a prefix of a fixed order) was set by the mask arm's cap.
  - Both rules were set by the lead, not the human.
- **Lead-chosen limits:** the $12 and $8 limits, the dropped P1 oracle arm and the P4 decision are the lead's, not the human's.
- **In-sample development in P3**, and a single reader of the final replies.
- **Wide intervals:** 7 to 16 clusters (P4 7 scenarios, P2 10, P1 16 users), and bootstrap intervals the files call rough.
- **Multiple contrasts without correction.**

---

## E. Claims table

| # | Claim | Label | Evidence pointer | Status |
|---|---|---|---|---|
| 1 | Three models searched in 20/20 D sessions uninstructed; target called 20/19/20 | O | `p3/RESULTS-P3-RUN1.md`, `run1-analysis.json` | Recomputed |
| 2 | HYP-0019 falsifier not met on this set | I | Same | Interpretation; set is easy |
| 3 | No client-side rule stopped searching for a missing tool without also losing the doable need | O/I | Runs 2 to 5 | Reported; run 4/5 recomputed |
| 4 | Forced reply lost the doable need (14/19/9 of 40) | O | Run 4, `run4-analysis.json` | Recomputed |
| 5 | DRY + sentence: Y 40/39/37, backstop 3/0/1, requests -32 to -48% | O/D | Runs 5 and 6 | Recomputed |
| 6 | Most of the gain over DRY seems to come from the sentence (the file's wording; the run cannot separate the two parts) | I | `RESULTS-P3-RUN6.md` s2 | No instruction-only arm |
| 7 | P3 results are in-sample (rule designed on run 4's tasks) | I | `P3-LOG.md`, replay file | My reading |
| 8 | `enf` kept the cache and was enforced | O | `main-analysis.json` | Recomputed |
| 9 | `enf` accuracy: +0.117 and -0.050, intervals include zero for 5.4-mini | O | `main-paired-summary.json` | Recomputed |
| 10 | No per-repeat McNemar below 0.05 | D | `main-analysis.json` | My recomputation |
| 11 | Instruction form is model-dependent | I (the file's reading) | C2 table; `RESULTS-P2-MAIN.md` s3.3 | 3 models |
| 12 | `drop` costs 20% (gpt-5-mini) and 10% (gpt-5.4-mini) less, on a single stream | O/D | Cost ratios 0.80, 0.90 | Recomputed; sharing across users not priced |
| 13 | P2b: 0 calls outside in 412; calls x0.93, cost x0.80 (x0.85 on repeat 2 alone) | O | `p2b-or-paired-summary.json`; `RESULTS-P2B.md` | Reproduced |
| 14 | Oracle sentence is also a hint | I | (none; the analyser's reading) | Not in the files |
| 15 | pop6 measured h 0.27 vs h* 0.19 to 0.21 (up to 0.22 at r = 0.186) at actual T | D/I | `p1-analysis.json`; `memory_seed.py` | Derived and recomputed by the lead |
| 16 | Searches -1.14 per session (-1.72, -0.63) | O | `p1-analysis.json` | Recomputed |
| 17 | Bill -16% / -4.6% / +16%, all uncertain | O/D | `p1-analysis.json` | Recomputed |
| 18 | P1 could not detect a 2% effect | I | CI half-width about ±34% | My reading |
| 19 | P1 session set depends on pop6's spending | O | `P1-PREP.md` s9 | Stated in file |
| 20 | P1 appended discoveries (allowed by V5-R02) and the cached share fell to 0.63-0.74 | O | `tools/p1_memory.py` docstring; `04` line 87 | Corrected after verification |
| 21 | Per-user rules lose on gold, except "used in 2+ earlier sessions" (seeds 0.3 tools on average; +88 at T=8) | O | `p1_seed_rules.py` (reproduced) | Not tested live |
| 22 | Clearing: billed x2.06, calls x1.37 | O | `p4-analysis.json` | Recomputed |
| 23 | Where fired x2.66; never fired x1.00 | D | Same | Recomputed |
| 24 | Re-fetch after clearing is the mechanism | I | `RESULTS-P4.md` | Suggested only |
| 25 | Falsifier of HYP-0021 neither met nor refuted | O | `HYP-0021.md` | After correction |
| 26 | Replay (+1 to 7.5%) vs live (x2.06) differ | O/D | `P4-REPLAY-A.md` | Reported |
| 27 | Masking not supported on short tasks; domain (long runs) not tested | I | C4 | Single model/setting |
| 28 | Role memory is closer to S1 (core by usage) than to M2 | I | `P1-PREP.md` s7 | The file's reading |

---

## F. Things I could not verify, or that look inconsistent between files

1. **`ops/STATE.md` said P2 had "no accuracy loss beyond run-to-run variation".** The corrections in `04` and in `p2/RESULTS-P2-MAIN.md` say that is too strong ("no detectable difference, small effects not excluded"). Confirmed by the lead; STATE.md is corrected in the same commit as this analysis.
2. **WD-086's original P1 and P4 bullets are superseded by its addendum but remain.** They say:
   - "HYP-0021 falsifier met on this setting";
   - "accuracy unchanged";
   - "rules fixed before any arm comparison".

   The commit subject of 9caf9e9 also says "falsifier met" (history is not rewritten). `ops/STATE.md` and `RESULTS-P4.md`'s Reading say clearing "doubled" the bill; the measured ratio where it fired is x2.66 (x2.06 over all 20 tasks). "Accuracy unchanged" is in WD-086's P4 bullet; its P1 bullet says "success unchanged".
3. **`P1-PREP.md` section 2's "all APIs" column is not reproduced.** I re-ran `p1_recurrence.py`: it gives recall 0.55 and precision 0.44 against the file's 0.49 and 0.38. The file already says so. The non-core column reproduces exactly. M2 depends only on the non-core column.
4. **P2b cost field.**
   - `p2b-or-analysis.json` gives `instr` repeat 2 cost as $1.2939. The local `stats.json` and `RESULTS-P2B.md` say $1.278.
   - The JSON's four costs sum to $5.797, against $5.781 stated.
   - The cost ratio x0.80 is unaffected: 0.808 from the JSON and 0.803 from the billed spend [D].
5. **P2b effort field.** `p2b-or-analysis.json` says `reasoning_effort: low`. The local run metadata show no reasoning parameter was sent (`no_reasoning_param: true`). The JSON field is a harness default.
6. **P3 run 6 paired fields.** `run6-analysis.json` has `paired_vs_plain` entries that are all 0/0 with p=1.0. Run 6 has no plain cell, so these entries compare nothing. The comparison with the no-rule runs is made by range only.
7. **P3 counts corrected in the files.**
   - Run 5: the number of DRY sessions without Y is 25, not 24 (DeepSeek's AS cell has 19 complete sessions).
   - Run 1: MiniMax searched in 19 of 20 W sessions, not "every session".

   Both are noted in the "Corrections of 2026-11-09" sections. I confirmed the 40-session counts from the JSON.
8. **Run 6's "at or above the no-rule range" wording.** It holds for MiniMax (40 equals the top of 37-40) and GLM (37 above 30-33); DeepSeek's 39 lies inside 36-40.
9. **AUTH-033 text against what was done.**
   - The text lists an oracle arm; the lead dropped it.
   - It names V5-R17's stop; P1 ran without a stop.
   - It says P4 would use "the longest available tasks, if feasible"; the 20 tasks were short.
   - The files record these as the lead's decisions.
10. **P1 session length.** The session length T that D-02 assumes was never measured as a target. I derived about 11 to 12 requests per session [D] from the run table. No file states the h* at T = 11 to 12; `P1-PREP.md` section 6 gives h* at T = 10 (0.19 to 0.20).
11. **P3 literature.** I spot-checked five of the nine stored `p3stop-*` sources for their quoted phrases and found them. I did not check the other four. The note itself (`STOP-RULE-RESEARCH-20261108.md`) remains a summary. The Guardrails Redirect source is only a listing page abstract.
12. **P5 and P0.** Used as context and taken from the files. I did not recompute them.
13. **Whether the model sees the unoffered definitions under `allowed_tools`.** [I] the vendor text implies they stay visible; no P2 arm checks it.
14. **Why P2b's `all` arm made 48 and 108 calls outside the oracle subset in two identical settings.** Not explained.
15. **`P4-REPLAY-A.md` stated, under an observed label, that "after a clear the model calls tools again".** `RESULTS-P4.md` and `HYP-0021.md` say suggested, not shown. Found by a verifier, confirmed by the lead; `P4-REPLAY-A.md` is corrected in the same commit as this analysis.

---

## G. Questions for the human

1. **Is P4 to be tested on long tasks, parked, or dropped?** The condition check says P2's tool results are small (old results 13% of billed input; bound 2 to 4% of the total). The human's AUTH-033 message asked for P4 "if possible"; the lead read it as covering a run despite the condition check, and the human has not ruled on the condition (`RESULTS-P4.md`). Options:
   - Park masking and keep it out of the default.
   - Run a long-task benchmark, with the benchmark and the meaning of "large tool results" chosen by the human.
   - Drop masking from the plan.

   This decides whether history clearing is offered as an option for deployments with large tool results (`04` keeps it out of the default).
2. **Do you accept the lead's P1 choices, or do you want per-user memory run live and synthetic users added (step C)?**
   - The choices were pop6 as the tested seed rule, the oracle arm dropped, a 33-session set, and step C skipped (the lead's own call, which the file asks you to confirm).
   - The result also depends on whether V5's M2 means role memory (a core chosen from usage, close to S1) or per-user memory (which the desk check says loses).
   - Options: accept; run per-user live; add synthetic users at controlled recurrence.
3. **Which discovery form should the end-to-end study use: appending discovered tools to the tools array, or placing them in the message history?**
   - P1 appended to the array and cached share fell to 0.63 to 0.74.
   - V5-R02 allows appended discoveries but forbids other changes to the array; appending was followed by a lower cached share on this route ([I] mechanism, not tested by an arm).
   - V5-R17's search withdrawal needs no array change on routes with an offering mechanism and does on routes without one; the files say the end-to-end study decides (`04` V5-R17 open item b).
4. **Do thesis claims need to hold on the university API?** Only the human knows the thesis constraint.
   - If yes, P2b's failure on ScaDS (timeouts, HTTP 408) means a new route test.
   - If an OpenRouter route is acceptable, the model-and-route differences (8-bit against 4-bit, effort) need to be stated as limits.
5. **Which models for the end-to-end study?** P2 shows the instruction form is model-dependent, and P3 shows MiniMax-M3 with more false claims. `05` section 3 plans at least two models (citing REQ-U21-08, which itself only says that models and providers are chosen when implementing). The files record MiniMax's behaviour as "an input to model choice".
6. **Do you want HYP-0019 closed?** P3's falsifier was not met. HYP-0018 was kept open on your instruction (INT-T-044); HYP-0019's file says "closing it is the human's decision".
7. **Do you accept the lead's cost limits and selection rules as they were, or should P1 and P4 be re-run under limits you set?** The $12, $8 and per-run caps shaped which sessions and tasks were measured, and you stated none.
