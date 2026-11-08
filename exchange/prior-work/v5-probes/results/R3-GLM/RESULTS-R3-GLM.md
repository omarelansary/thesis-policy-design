# RESULTS-R3-GLM (2026-11-06 to 11-08): R3 Part B on a second model, GLM-5.3 on ScaDS, run by the lead on Linux (AUTH-026)

## Summary
- **Setup.** The R3 Part B design of `RESULTS-R3-B.md` (on output branch `v5-r3-part-b-results`), with `zai-org/GLM-5.3` on ScaDS (`https://llm.scads.ai/v1`, vLLM, free). Reasoning as served: on by default, with no reasoning parameter sent. 57 AppWorld dev tasks per arm. B1 = all 469 definitions on every call (predictor off). B2 = AppWorld's predictor subset, at most 20 functions, with GLM-5.3 itself as the predictor. One run per arm: the repeats were dropped by the human on 2026-11-07 ("i choose option 2 Finish GLM B2, then stop").
- **Accuracy.** B1 passed 23 of 57 (TGC 40.4, SGC 15.8). B2 passed 24 of 57 (TGC 42.1, SGC 10.5). The arms disagree on 27 tasks: 13 passed only under B1, 14 only under B2.
- **The equal totals hide a predictor failure** [O for the counts, I for the reading].
  - In 22 of the 57 B2 tasks, GLM-5.3's predictor did not offer `supervisor.show_account_passwords`. That function is how the agent gets the app passwords it needs to log in. All 22 of those tasks failed, and 19 of them ended within 3 steps, the agent calling `complete_task` at its first step.
  - On the 35 tasks where the function was offered, B2 passed 24, against 13 for B1 on the same tasks.
  - MiniMax-M3's predictor offered the function in 57, 55 and 53 of 57 tasks in its three B2 runs.
  - So B2's result here measures GLM-5.3 as a predictor as much as it measures a smaller offer.
- **Bill, B1 over B2** (ScaDS bills nothing, so the bill is computed from the token counts and OpenRouter's GLM-5.3 price listing of 2026-11-07, 47 endpoints).
  - Prompt tokens: 2.17 times (65.3 M against 30.2 M).
  - Uncached prompt tokens: 0.83 times. Completion tokens: 0.65 times (B2 wrote 1.20 M, 90% of it reasoning; B1 wrote 0.78 M, 77% reasoning).
  - Computed bill: 1.51 times at `gmicloud/fp8` ($10.58 against $7.02), and 1.08 to 1.80 times across the 47 endpoints (median 1.51). With no cache discount the range is 1.08 to 2.00.
  - That is smaller than MiniMax-M3's 2.2 to 2.6 (`RESULTS-R3-B`). Two reasons are visible in the counts: B2's prompts still average 43,571 tokens per call, and B2 wrote more completion tokens, the most expensive class.
  - ScaDS served 99.0% (B1) and 97.3% (B2) of the prompt tokens from cache, with 0 cache-write tokens. Whether a paid endpoint would cache as much was not measured.
- **Speed.** B2 had 75 timed-out requests against B1's 2, and 7 step-capped tasks against 3. One task, `37a8675_2`, ran 14.6 hours. Long reasoning replies on long prompts often ran past the 300 s client timeout. Wall time mixes server load with behaviour, because the arms ran at different times on a shared server.
- **Spend:** none (ScaDS is free to the human).

**What this is.** AUTH-026: the human's "So them" (2026-11-06), read as "Do them", in reply to the lead's proposal of a one-task smoke, B1 and B2, and a repeat of both, on ScaDS. Narrowed on 2026-11-07 to finish B2 and stop. Counts and ids only. The key was read from a local file outside the repository and never printed or written here. Only dev tasks were run. No AppWorld task text, model output or evaluation report is copied here: AppWorld's own logs were read locally to check which functions were offered, and only function names and counts are written out. UTC times. Descriptive only, with no statistical test (INT-T-022).

## Runs
| tag | what | UTC | tasks | ok calls | timeouts | note |
|---|---|---|---|---|---|---|
| `glm-smoke` | smoke, task `50e1ac9_1` | 2026-11-06 14:55 | 0 finished | 12 | 0 | stopped by the lead's own 590 s command limit; not counted |
| `glm-smoke2` | smoke, task `50e1ac9_1` | 2026-11-06 15:05 | 1 (failed) | 2 | 0 | the agent called `complete_task` at its first step (see *Predictor check*) |
| `glm-b1-all-tools` | B1 | 2026-11-06 15:06 to 11-07 03:47 | 57 | 739 | 2 | |
| `glm-b2-control` | B2 part 1 | 2026-11-07 03:47 to about 13:45 (last log write) | 21 | 266 counted | 15 counted | killed by a laptop restart during task 22 (`37a8675_1`, 30 calls, 29 of them successful); never reached its own evaluation step |
| `glm-b2-control-rest` | B2 part 2 | 2026-11-07 13:55 to 11-08 14:28 | 36 | 426 | 60 | the 36 tasks not finished in part 1 (`glm-b2-remaining-ids.txt`), with `37a8675_1` started from scratch |

- **Order.** `run_glm.sh` ran the smoke, B1 and B2, followed by B1 and B2 repeats. On 2026-11-07 at about 09:20 the lead stopped the sequence script, so the repeats never started and the B2 process ran on alone. Part 2 was started by `run_glm_b2_rest.sh` after the restart.
- **Evaluation.** Part 1 was evaluated on 2026-11-08 with AppWorld's own evaluator, called as the runner calls it (`eval_glm_b2_first.py`; local, no model call): 11 of its 21 tasks passed. Part 2 and B1 were evaluated by the runner at the end of each run.
- **Counting.** Each of the 57 dev tasks is counted exactly once per arm. The 30 calls of the interrupted `37a8675_1` in part 1 are left out of every figure.
- **Watching.** From 2026-11-07 22:16 the lead checked the run hourly (`glm_watch.py`, read-only; log `r3-glm-b2-watch.log`). It changed no setting. When the human asked on 2026-11-08 at 07:33 whether to stop the run, the lead advised letting it finish, because it was free and stopping would leave B2 with about half the tasks.

## Settings
- The runner is `run_partb.py`, byte-identical to the one published with R3 Part B (SHA-256 `d7dad6db42276d009d503ac56d01896f795f21914c46ccb64ada80caa7e27d56`). It was last changed on 2026-11-06 at 14:55 UTC, before the first GLM run.
- With `--host scads` the base URL is ScaDS and the key is `SCADS_API_KEY`. No `extra_body` is sent, so there is no provider pin and no reasoning field, and `cost_per_token` is zero. **The `provider gmicloud/fp8` printed in the progress logs, and `provider_pinned` in the run-stats files, are the argument's unused default; nothing about a provider was sent to ScaDS.**
- Everything else as in R3 Part B: AppWorld 0.2.0.dev0 at commit 42b5bcf3, data 0.2.0, `simplified_function_calling` agent, temperature 0, seed 100, `tool_choice` auto, `parallel_tool_calls` true, 3-shot, step cap 50 (including the predictor step), no cache, one task at a time, a new AppWorld root and experiment name per run.
- Timeout and retries: the client timeout is 300 s, and the `openai` client retries twice by itself, so a request recorded as timed out took about 900 s. AppWorld then retries up to 20 times, 15 s apart. No task reached the retry limit, and no task ended with an exception.
- The served model id was `zai-org/GLM-5.3` and the `system_fingerprint` `vllm-0.32.0-tp4-pp2-5c819679` on every successful call of every run.
- B1 is predictor mode `all` with `max_predicted_apis` 1000: 469 functions per agent call, and the predictor step makes no model call. B2 is predictor mode `predicted` with `max_predicted_apis` 20: one predictor call per task (57), and 8.5 functions per agent call on average.

## Results
| | B1 all tools | B2 predictor subset |
|---|---|---|
| Tasks passed (of 57) | 23 (TGC 40.4) | 24 (TGC 42.1) |
| Scenarios fully passed (of 19) | 3 (SGC 15.8) | 2 (SGC 10.5) |
| Successful model calls (predictor calls) | 739 (0) | 692 (57) |
| Timed-out requests | 2 | 75 |
| Tasks that hit the 50-step cap | 3: `3ab5b8b_1`, `68ee2c9_2`, `df61dc5_3` | 7: `37a8675_2`, `4ec8de5_3`, `57c3486_1`, `68ee2c9_1`, `68ee2c9_2`, `b119b1f_2`, `df61dc5_1` |
| Tasks that ended within 3 steps | 0 | 19 |
| Functions offered per agent call (mean) | 469 | 8.5 |
| Prompt tokens per successful call (mean) | 88,403 | 43,571 |
| Prompt tokens: all (cached; share) | 65,330,095 (64,662,400; 99.0%) | 30,151,324 (29,350,144; 97.3%) |
| Uncached prompt tokens | 667,695 | 801,180 |
| Cache-write tokens | 0 | 0 |
| Completion tokens (of it reasoning) | 776,941 (597,082) | 1,202,454 (1,078,554) |
| Completion tokens per successful call (mean) | 1,051 | 1,738 |
| Replies carrying reasoning | 619 of 739 | 683 of 692 |
| Median latency of a successful call | 58.3 s | 61.3 s |
| Median steps / seconds per task | 12 / 454 | 8 / 352 |
| Agent wall time, sum over tasks | 12.7 h | 33.6 h |

- **Ratios, B1 over B2:** prompt 2.17, cached 2.20, uncached prompt 0.83, completion 0.65, reasoning 0.55, successful calls 1.07, mean prompt per call 2.03.
- **Pass/fail by task:** both passed 10 tasks, both failed 20. Passed only under B1 (13): `23cf851_1`, `383cbac_1`, `396c5a2_1`, `50e1ac9_2`, `50e1ac9_3`, `6171bbc_2`, `68ee2c9_3`, `6bdbc26_1`, `6bdbc26_2`, `6bdbc26_3`, `b119b1f_2`, `df61dc5_1`, `fac291d_1`. Passed only under B2 (14): `0d8a4ee_1`, `23cf851_2`, `23cf851_3`, `383cbac_2`, `3ab5b8b_1`, `3ab5b8b_2`, `4fab96f_1`, `4fab96f_3`, `50e1ac9_1`, `530b157_1`, `6171bbc_3`, `d4e9306_1`, `d4e9306_2`, `df61dc5_3`.
- **Timeouts by task.** B1: `50e1ac9_2` 1, `df61dc5_3` 1. B2: `37a8675_2` 46, `4ec8de5_1` 10, `68ee2c9_2` 5, `57c3486_1` 3, `4ec8de5_3` 2, `68ee2c9_3` 2, and 1 each in `0d8a4ee_3`, `383cbac_1`, `50e1ac9_2`, `6171bbc_2`, `df61dc5_1`, `df61dc5_3`, `fac291d_2`.
- **GLM's run-to-run variation was not measured,** because there was no repeat. MiniMax-M3's was 5 of 57 tasks on ScaDS and 9 to 12 of 57 on GMICloud, against the 27 tasks that differ between the GLM arms here.

## Predictor check (2026-11-08; counts in `r3-glm-stats.json`, `predictor_check` and `per_task`)
What was seen. Under B2, 19 tasks ended within 3 steps and all failed; under B1, none did. AppWorld's logs show that in each of them the agent's first or second action was `supervisor.complete_task`. In each, `supervisor.show_account_passwords` was missing from the functions offered. In the logs read, the agent's reasoning says it needs credentials it cannot get, or that the functions it needs are not offered (read locally, not copied).

| B2 tasks | count | B2 passed | B1 passed on the same tasks |
|---|---|---|---|
| credentials function offered | 35 | 24 | 13 |
| credentials function not offered | 22 | 0 | 10 |

- **Not offered in 22 tasks:** `23cf851_1`, `37a8675_1`, `383cbac_1`, `396c5a2_1`, `3ab5b8b_3`, `4ec8de5_2`, `4fab96f_2`, `57c3486_1`, `57c3486_3`, `6171bbc_1`, `6171bbc_2`, `68ee2c9_1`, `68ee2c9_3`, `6bdbc26_1`, `6bdbc26_2`, `6bdbc26_3`, `6c2c621_1`, `6c2c621_2`, `6c2c621_3`, `b119b1f_2`, `fac291d_1`, `fac291d_3`. Of these, 19 ended within 3 steps and the other 3 (`57c3486_1`, `68ee2c9_1`, `b119b1f_2`) hit the step cap. No task with the function offered ended within 3 steps.
- **Reply format.** In 56 of 57 tasks the predictor's reply has lines in AppWorld's `app.api` format, and the omission is a choice of functions. In one task (`6bdbc26_1`), the reply used another markup that AppWorld's parser does not read, so only `complete_task` was offered.
- **The predictor varies on the same task.** In the first smoke, the predictor offered `spotify.login`, `supervisor.show_profile` and `supervisor.show_account_passwords` for `50e1ac9_1`, and the agent began by calling the last two. In the second smoke, on the same task, it offered none of them, and the agent ended at its first step. In B2 the same task was offered the function and passed.
- **MiniMax-M3, for comparison** (same predictor code, same 20 cap; run folders of R3 Part B): offered in 57 of 57 tasks (B2 without reasoning), 55 (B2 with reasoning) and 53 (its repeat). Of those runs' tasks without it, 0 of 0, 2 of 2 and 3 of 4 passed.

**Reading** [I].
- **B2 against B1 for GLM-5.3 is two effects of opposite sign** that roughly cancel in the totals:
  - The predictor removed a function the agent needed in 22 tasks, which cost every one of them.
  - Where it did not, the smaller offer passed 24 of 35, against 13 of 35 with all 469 functions.
- **Neither part is a clean estimate.**
  - The 22 tasks are not a random set: they cluster in scenarios, with all three tasks of `6bdbc26` and of `6c2c621` among them.
  - There is one run per arm, and the run-to-run variation of GLM is unknown.
- **For V5.** A selection step run by the same model can fail in a way that the accuracy total hides. A deployment filter or an always-offered core (for example the credentials and profile functions) would remove this failure. That is a design question for P2 and V5-R, not something tested here.

## Bill (computed; `r3-glm-stats.json`, `bill_computed`)
- **How the bill is computed:** uncached prompt tokens at the endpoint's input price, cached tokens at its cache-read price (the input price where none is listed), and completion tokens at its output price. Prices come from `r3-b-openrouter-glm-5.3-endpoints-2026-11-07.json`: a copy of the listing stored with R3 Part B, fetched on 2026-11-07 at 09:57 UTC, with the same bytes and SHA-256 `d7f18cb771bfda50068c991a99ffff56a18e9d993bf5c2ab13001ed172fbb84e`.
- **At `gmicloud/fp8`** ($0.70 input, $0.13 cache read and $2.20 output per million tokens; the endpoint used for MiniMax-M3): B1 $10.58, B2 $7.02, ratio 1.51.
- **Across all 47 endpoints:** the ratio runs from 1.08 to 1.80, with median 1.51. Without cache prices it runs from 1.08 to 2.00.
- **The lowest ratios are on endpoints with a high output price relative to input**, where B2's extra completion tokens weigh most. Examples: `relace/fp4` 1.08 ($4.38 output against $0.07 input) and `inference-net` 1.17.
- **Caveat.** The bill assumes the endpoint caches as much as ScaDS did (97 to 99%). A paid endpoint that cached less would raise both bills, and B1's more.

## Against MiniMax-M3 (R3 Part B, reasoning on, OpenRouter `gmicloud/fp8`)
| | MiniMax-M3 B1 | MiniMax-M3 B2 | GLM-5.3 B1 | GLM-5.3 B2 |
|---|---|---|---|---|
| passed of 57 | 50, 45 | 46, 46 | 23 | 24 |
| B1 over B2: prompt tokens | 4.44, 4.02 | | 2.17 | |
| B1 over B2: bill | 2.58, 2.19 (reported) | | 1.51 at the same endpoint's prices; 1.08 to 1.80 over 47 (computed) | |
| B2 tasks offered the credentials function | | 55, 53 | | 35 |

- The two models ran on different hosts (OpenRouter for MiniMax-M3, ScaDS for GLM-5.3), so their pass rates are not a comparison of the models alone.
- On ScaDS, MiniMax-M3 passed 50 in R1 Part 4 and 53 in its repeat.
- No earlier GLM-5.3 AppWorld agent run is in the repository; R1 and R2 used GLM-5.3 only in API probes.

## Deviations
1. **Repeat dropped.** AUTH-026 included a repeat of both arms. The human narrowed it on 2026-11-07 to finishing B2. So no run-to-run variation is measured for GLM-5.3.
2. **B2 ran in two parts** because a laptop restart killed part 1 during task 22. The interrupted task was rerun from scratch in part 2, and its 30 part-1 calls are excluded. Part 1 was evaluated afterwards with the runner's own evaluator call (`eval_glm_b2_first.py`).
3. **No provider pin or reasoning field on ScaDS** (see *Settings*). The provider value printed in the logs is an unused default.
4. **Timeouts were frequent in B2, and the settings were kept as they were.** Raising the 300 s timeout during the run was considered on 2026-11-07 and not done, so that both arms and both parts ran under the same settings. A request recorded as timed out still counts toward the task's retries, not toward its steps.
5. **The bill is computed,** because ScaDS reports no cost. It uses OpenRouter's listing, not a price of ScaDS, and assumes ScaDS's cache share.
6. **AppWorld's local logs were read** for the predictor check (functions offered, the predictor's reply format, and the reasoning of a few short tasks). Only function names and counts are written here.

## Files
- `RESULTS-R3-GLM.md` (this file).
- `r3-glm-stats.json`: totals of both arms, ratios, the computed bill per endpoint, the predictor check, and per task (result, steps, seconds, successful calls, timeouts, prompt and completion tokens, and for B2 the number of functions offered, whether the credentials function was among them, and how many predictor lines parsed). Written by `analyze_glm.py`.
- Per call, counts only (task id, predictor call or not, messages, functions offered, status, error kind, served model id, fingerprint, prompt, cached, cache-write, completion and reasoning tokens, reasoning characters, finish reason, number of tool calls, latency):
  - `r3-glm-b1-calls.jsonl`
  - `r3-glm-b2-part1-calls.jsonl`, which includes the 30 excluded calls of `37a8675_1`
  - `r3-glm-b2-part2-calls.jsonl`
  - `r3-glm-smoke-calls.jsonl`
  - `r3-glm-smoke2-calls.jsonl`
- Each run's own log and stats, as written by the runner:
  - `r3-glm-*-progress.log` (one line per task)
  - `r3-glm-*-run-stats.json` (per task steps, seconds and successful calls; totals where the run finished; none for `glm-smoke`, which was stopped)
- `r3-glm-b2-watch.log`: the lead's hourly checks of part 2.
- Price listing: `r3-b-openrouter-glm-5.3-endpoints-2026-11-07.json`.
- Scripts:
  - `run_partb.py`: the runner, identical to R3 Part B's.
  - `run_glm.sh`: smoke, B1 and B2; its repeat lines never ran.
  - `run_glm_b2_rest.sh` with `glm-b2-remaining-ids.txt`.
  - `eval_glm_b2_first.py`
  - `analyze_glm.py`: run as `analyze_glm.py r3-b-openrouter-glm-5.3-endpoints-2026-11-07.json r3-glm-stats.json b2-control b2r-control-reasoning mm3-b2r-repeat`, where the last three are MiniMax-M3 B2 run folders, read for the comparison only.
  - `glm_watch.py`
- Paths in the scripts are relative to the working folder (`runs/<tag>/`). The AppWorld run folders themselves (experiment outputs, console logs, evaluation reports) hold task text and stay outside the repository.

## Per task
Result (P passed, F failed), steps (B1's include the predictor step, which makes no call there), successful calls, timed-out requests; for B2 also the number of functions offered on the first agent call, and whether `supervisor.show_account_passwords` was among them.

| task | B1: result, steps, ok calls, timeouts | B2: result, steps, ok calls, timeouts | B2: functions offered, credentials offered | B2 part |
|---|---|---|---|---|
| `50e1ac9_1` | F 16 15 0 | P 9 9 0 | 15 yes | 1 |
| `50e1ac9_2` | P 18 17 1 | F 12 12 1 | 13 yes | 1 |
| `50e1ac9_3` | P 15 14 0 | F 18 18 0 | 7 yes | 1 |
| `fac291d_1` | P 8 7 0 | F 2 2 0 | 7 **no** | 1 |
| `fac291d_2` | F 11 10 0 | F 12 12 1 | 10 yes | 1 |
| `fac291d_3` | F 6 5 0 | F 2 2 0 | 8 **no** | 1 |
| `530b157_1` | F 8 7 0 | P 10 10 0 | 13 yes | 1 |
| `530b157_2` | P 12 11 0 | P 8 8 0 | 9 yes | 1 |
| `530b157_3` | P 11 10 0 | P 10 10 0 | 10 yes | 1 |
| `4ec8de5_1` | F 9 8 0 | F 8 8 10 | 8 yes | 1 |
| `4ec8de5_2` | F 18 17 0 | F 2 2 0 | 6 **no** | 1 |
| `4ec8de5_3` | F 8 7 0 | F 50 50 2 | 9 yes | 1 |
| `b119b1f_1` | P 12 11 0 | P 10 10 0 | 9 yes | 1 |
| `b119b1f_2` | P 12 11 0 | F 50 50 0 | 5 **no** | 1 |
| `b119b1f_3` | P 10 9 0 | P 13 13 0 | 7 yes | 1 |
| `d4e9306_1` | F 6 5 0 | P 7 7 0 | 10 yes | 1 |
| `d4e9306_2` | F 14 13 0 | P 6 6 0 | 10 yes | 1 |
| `d4e9306_3` | P 13 12 0 | P 9 9 0 | 8 yes | 1 |
| `0d8a4ee_1` | F 17 16 0 | P 9 9 0 | 8 yes | 1 |
| `0d8a4ee_2` | P 16 15 0 | P 11 11 0 | 9 yes | 1 |
| `0d8a4ee_3` | F 16 15 0 | F 8 8 1 | 9 yes | 1 |
| `37a8675_1` | F 18 17 0 | F 3 3 0 | 6 **no** | 2 |
| `37a8675_2` | F 12 11 0 | F 50 50 46 | 6 yes | 2 |
| `37a8675_3` | P 12 11 0 | P 11 11 0 | 9 yes | 2 |
| `3ab5b8b_1` | F 50 49 0 | P 8 8 0 | 8 yes | 2 |
| `3ab5b8b_2` | F 7 6 0 | P 8 8 0 | 7 yes | 2 |
| `3ab5b8b_3` | F 9 8 0 | F 2 2 0 | 7 **no** | 2 |
| `df61dc5_1` | P 10 9 0 | F 50 50 1 | 8 yes | 2 |
| `df61dc5_2` | F 12 11 0 | F 11 11 0 | 10 yes | 2 |
| `df61dc5_3` | F 50 49 1 | P 13 13 1 | 9 yes | 2 |
| `383cbac_1` | P 19 18 0 | F 2 2 1 | 4 **no** | 2 |
| `383cbac_2` | F 20 19 0 | P 13 13 0 | 7 yes | 2 |
| `383cbac_3` | P 9 8 0 | P 7 7 0 | 7 yes | 2 |
| `23cf851_1` | P 7 6 0 | F 2 2 0 | 5 **no** | 2 |
| `23cf851_2` | F 9 8 0 | P 10 10 0 | 7 yes | 2 |
| `23cf851_3` | F 6 5 0 | P 7 7 0 | 7 yes | 2 |
| `57c3486_1` | F 11 10 0 | F 50 50 3 | 8 **no** | 2 |
| `57c3486_2` | F 14 13 0 | F 7 7 0 | 7 yes | 2 |
| `57c3486_3` | F 8 7 0 | F 2 2 0 | 5 **no** | 2 |
| `68ee2c9_1` | F 27 26 0 | F 50 50 0 | 8 **no** | 2 |
| `68ee2c9_2` | F 50 49 0 | F 50 50 5 | 13 yes | 2 |
| `68ee2c9_3` | P 28 27 0 | F 2 2 2 | 4 **no** | 2 |
| `6bdbc26_1` | P 6 5 0 | F 2 2 0 | 1 **no** | 2 |
| `6bdbc26_2` | P 6 5 0 | F 2 2 0 | 3 **no** | 2 |
| `6bdbc26_3` | P 6 5 0 | F 2 2 0 | 4 **no** | 2 |
| `6171bbc_1` | F 9 8 0 | F 2 2 0 | 7 **no** | 2 |
| `6171bbc_2` | P 10 9 0 | F 2 2 1 | 7 **no** | 2 |
| `6171bbc_3` | F 10 9 0 | P 8 8 0 | 11 yes | 2 |
| `6c2c621_1` | F 16 15 0 | F 2 2 0 | 8 **no** | 2 |
| `6c2c621_2` | F 15 14 0 | F 2 2 0 | 6 **no** | 2 |
| `6c2c621_3` | F 13 12 0 | F 2 2 0 | 7 **no** | 2 |
| `396c5a2_1` | P 8 7 0 | F 2 2 0 | 5 **no** | 2 |
| `396c5a2_2` | P 7 6 0 | P 7 7 0 | 11 yes | 2 |
| `396c5a2_3` | P 11 10 0 | P 10 10 0 | 11 yes | 2 |
| `4fab96f_1` | F 13 12 0 | P 11 11 0 | 9 yes | 2 |
| `4fab96f_2` | F 6 5 0 | F 2 2 0 | 4 **no** | 2 |
| `4fab96f_3` | F 16 15 0 | P 12 12 0 | 9 yes | 2 |
