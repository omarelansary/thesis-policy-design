# RESULTS-R3-B (2026-11-05/06): R3 Part B, run by the lead on Linux (AUTH-024)

**What this is.** REQUEST-R3 Part B (B1 all tools, B2 control, B3 control repeated; 57 dev tasks each; `minimax/minimax-m3` on OpenRouter; provider fixed to `gmicloud/fp8`, `allow_fallbacks` false) run by the lead because the describing agent was unavailable. Counts and ids only; the key was read from a local file outside the repository and never printed or written here; no test split was run, opened or listed (the full data download was deleted unopened; only train and dev task folders were kept). UTC times. **The runner is a rebuild, not the describing agent's `run_part4.py`** (not in the repository): it is published here as `run_partb.py` and its differences are listed under *Deviations*. Hard result first: **an environment check shows this Linux environment does not reproduce Part 4's environment (reference solutions: 46 of 57 pass here, 57 of 57 in Part 4), and the pass rates below are far under Part 4's; the cause is not found.** Treat the accuracy figures as unreadable until that is resolved; token, cache and cost figures are measured as stated.

## Environment
AppWorld `0.2.0.dev0` at commit `42b5bcf3cd334fee33f0c37c02070a9f5807add5` (source archive from GitHub; the four Git LFS bundles fetched from GitHub's LFS media URL and checked against the SHA-256 in each pointer), data 0.2.0, Python 3.12.16 (uv), Linux, packages pinned to Part 4's `pip freeze` (differences: Windows-only `colorama`, `winloop`, `opentelemetry-api` absent here; `pexpect`, `ptyprocess`, `uvloop` present here). Agent code, prompts and demonstrations are AppWorld's own, unchanged. Settings as in the pilot: `simplified_function_calling` agent through the `openai` client, base URL OpenRouter, temperature 0, seed 100, `tool_choice` auto, `parallel_tool_calls` true, 3-shot, step cap 50 (includes the predictor step), client timeout 300 s, retry 20 times 15 s apart, no cache, one task at a time, a new AppWorld root and experiment name per run. B1: predictor mode `all`, `max_predicted_apis` 1000 (469 definitions per agent call). B2 and B3: predictor `predicted`, `max_predicted_apis` 20 (as Part 4).

## Part 4-style table (all 57 dev tasks)
| run | passed | failure types | LM calls | prompt tokens (cached; share) | completion tokens | cache-write tokens | cost (endpoint-reported) | UTC |
|---|---|---|---|---|---|---|---|---|
| B1 all tools (`b1-all-tools`) | 28 of 57 (TGC 49.1, SGC 21.1) | {'evaluation_failed': 29, 'passed': 28} | 475 (0 predictor) | 39,173,891 (37,725,511; 96.3%) | 266,291 | 0 | $2.4141 | 20:38-21:30 |
| B2 control (`b2-control`) | 28 of 57 (TGC 49.1, SGC 21.1) | {'passed': 28, 'evaluation_failed': 28, 'step_cap_reached': 1} | 602 (57 predictor) | 10,159,408 (9,148,997; 90.1%) | 305,502 | 0 | $0.9749 | 21:30-22:30 |
| B3 control repeated (`b3-control-repeat`) | 24 of 57 (TGC 42.1, SGC 26.3) | {'evaluation_failed': 33, 'passed': 24} | 560 (57 predictor) | 7,352,721 (6,343,522; 86.3%) | 334,715 | 0 | $0.8680 | 22:31-23:30 |

- Provider on every call of every run: GMICloud (one provider per task and per run: **0** tasks with more than one provider); served model id `minimax/minimax-m3`; `system_fingerprint` absent on every call; **0** failed or retried calls (the trace records failed calls and there are none); cache-write tokens 0 on every call.
- Totals without step-capped tasks: B1 had none; B2 without its 1 step-capped task: 56 tasks, prompt 6,556,919, cost $0.7657; B3 had none.
- Cost of the whole of Part B: $4.2570; the three one-task smoke runs before it (tags `smoke-ctrl`, `smoke-ctrl2`, `smoke-ctrl3`, task `50e1ac9_1`, not part of the results) cost $0.0121, $0.0396 and $0.0108. The approved estimate was about $6.7; B1 cost less than half of its estimate ($4.7).
- B1 against B2 on cost: 2.48 times; on prompt tokens: 3.86 times (the 10-task pilot, mixed providers: 4.9 and 8.8). Cold start (first agent call of a task with under half its prompt cached): B1 2 of 57 tasks, B2 57, B3 57.
- Failures by kind (AppWorld's evaluation report): in B1, B2, B3 the failed tasks fail the *answers match* test in 18, 19 and 22 cases and only a state test in 11, 10 and 11.

## Which tasks differ
| pair | pass/fail differs in | passed only in the first | passed only in the second |
|---|---|---|---|
| B3 against B2 | 12 tasks: `0d8a4ee_1`, `0d8a4ee_2`, `23cf851_3`, `37a8675_3`, `4fab96f_1`, `50e1ac9_1`, `57c3486_1`, `6171bbc_1`, `6c2c621_1`, `6c2c621_2`, `df61dc5_1`, `df61dc5_3` | 4 | 8 |
| B1 against B2 | 12 tasks: `0d8a4ee_2`, `37a8675_1`, `383cbac_1`, `3ab5b8b_2`, `4fab96f_1`, `50e1ac9_1`, `50e1ac9_3`, `57c3486_1`, `57c3486_2`, `6c2c621_1`, `df61dc5_1`, `df61dc5_3` | 6 | 6 |
| B1 against B3 | 10 tasks: `0d8a4ee_1`, `23cf851_3`, `37a8675_1`, `37a8675_3`, `383cbac_1`, `3ab5b8b_2`, `50e1ac9_3`, `57c3486_2`, `6171bbc_1`, `6c2c621_2` | 7 | 3 |

(Part 4 and its repeat on ScaDS: 5 of 57 flipped between identical runs.)

## Environment check: reference solutions (no model call)
`envcheck.py` executes each dev task's published reference solution (`compiled_solution_code` followed by `solution(apis, requester)`, as AppWorld's own `verify.py` does) and evaluates it. **Result here: 46 of 57 pass; 11 fail** (`0d8a4ee_1/_2/_3`, `37a8675_1/_2/_3`, `3ab5b8b_1/_2/_3`, `57c3486_1`, `57c3486_3`): the solution's own API call returns HTTP 422 (a Venmo account that does not exist, a payment card without enough money, a Spotify song already liked), i.e. the initial world state differs from the one the solution was written for. Part 4's check on Windows: 57 of 57 (`r1-part4-envcheck-dev-solutions-2026-11-01.json`). The same failure occurs on a freshly downloaded, unpruned data folder and with `TZ=UTC`, `PYTHONHASHSEED=0` and `LC_ALL=C`, so it is neither my data pruning nor those settings. Not found: the cause (package versions equal apart from the platform extras above; the data folder differs from the first download only in `__pycache__`).
Agents did pass some of these 11 tasks (B1: 6 passes among them, B2: 4, B3: 4), so a failing reference solution does not make a task unsolvable.

## Against Part 4 (ScaDS, same model name, predictor on)
Part 4: 50 of 57. Here (B2, B3): 28 and 24. **17 tasks passed in Part 4 and in none of B1, B2, B3.** Per scenario (3 tasks; Part 4 passed a of 3, the three B runs together b of 9, so compare a/3 with b/9): lower here: `4ec8de5` 3/3 against 0/9, `fac291d` 3/3 against 0/9, `3ab5b8b` 2/3 against 1/9, `4fab96f` 2/3 against 1/9, `50e1ac9` 3/3 against 2/9, `6c2c621` 3/3 against 2/9, `37a8675` 3/3 against 3/9, `383cbac` 1/3 against 1/9, `b119b1f` 3/3 against 3/9, `df61dc5` 2/3 against 3/9, `23cf851` 3/3 against 5/9, `6171bbc` 3/3 against 5/9, `396c5a2` 3/3 against 6/9, `57c3486` 3/3 against 7/9; equal: `530b157`, `68ee2c9`, `6bdbc26`, `d4e9306`; higher here: `0d8a4ee`. Mean agent steps per task: Part 4 10.5 turns; here B1 9.3, B2 10.6, B3 9.8 (these include the predictor step), so the agents stop at a similar point and then fail the check, mostly on the returned answer. Candidates, not tested: the provider (`gmicloud/fp8` is a quantised build; the pilot's mixed providers passed 7 of 10 in both arms against 8 and 9 on ScaDS), the Linux environment (the failing reference solutions), or a difference between this rebuilt runner and `run_part4.py`. On the 10 pilot tasks (dev[0::6]) this run passed 5 (B1), 6 (B2) and 5 (B3) of 10, against 7 and 7 in the pilot.

## Deviations from REQUEST-R3 Part B and from the pilot
1. Run by the lead with a rebuilt runner on Linux instead of by the describing agent with `run_part4.py` on Windows; the runner changes nothing in AppWorld's agent code and adds: the 300 s client timeout, the provider pin through `extra_body`, a counts-only trace of every raw call (`r3-b-*-calls.jsonl`: task id, whether a predictor call, tokens, cost, provider, finish reason, number of tool calls, elapsed seconds), a dev-only guard, per-task exception handling and a spend cap.
2. The rerun rule (a hung task is rerun once) was never needed: no task hung, none raised, no call failed.
3. Elapsed seconds in the trace come from a real-time counter because AppWorld freezes the clock inside a task (found in the first smoke run; fixed before Part B).
4. AppWorld's own cost caps use `cost_per_token` set to GMICloud's listed prices; the cost column is the endpoint's reported `usage.cost`.
5. The data folder holds the train and dev tasks only (147 task folders); `appworld install` also unpacked a tests bundle to `~/.cache/appworld/tests` outside the working folder.
6. Accuracy is not comparable with Part 4 (see above); this report gives no verdict on tool offering.

## Files
`RESULTS-R3-B.md` (this file); `r3-b-b1-stats.json`, `r3-b-b2-stats.json`, `r3-b-b3-stats.json` (per task: result, failure type, steps, LM calls, prompt, cached, cache-write, completion, cost, providers, first agent call's cached and prompt tokens; totals); `r3-b-b1-calls.jsonl`, `r3-b-b2-calls.jsonl`, `r3-b-b3-calls.jsonl` (per call); `r3-b-comparison.json`; `envcheck-result.json`; `run_partb.py`, `run_all.sh`, `analyze_partb.py`, `envcheck.py` (local paths are relative to the working folder).

## Per task (result, LM calls, cost in US cents)
| task | Part 4 (ScaDS) | B1 | B2 | B3 |
|---|---|---|---|---|
| `50e1ac9_1` | P | F 11 6.8 | P 8 1.2 | F 10 4.1 |
| `50e1ac9_2` | P | F 8 3.9 | F 11 1.5 | F 8 1.3 |
| `50e1ac9_3` | P | P 9 4.0 | F 22 6.0 | F 7 0.9 |
| `fac291d_1` | P | F 5 2.1 | F 6 0.5 | F 8 0.9 |
| `fac291d_2` | P | F 4 1.7 | F 6 0.7 | F 6 0.5 |
| `fac291d_3` | P | F 5 2.1 | F 6 0.5 | F 11 1.5 |
| `530b157_1` | P | P 7 2.9 | P 7 0.7 | P 8 0.8 |
| `530b157_2` | P | P 10 7.0 | P 9 0.7 | P 10 0.8 |
| `530b157_3` | P | P 7 2.9 | P 9 0.9 | P 10 0.8 |
| `4ec8de5_1` | P | F 8 3.9 | F 9 1.0 | F 8 0.7 |
| `4ec8de5_2` | P | F 7 3.2 | F 8 0.8 | F 8 0.8 |
| `4ec8de5_3` | P | F 10 5.0 | F 7 0.7 | F 8 1.1 |
| `b119b1f_1` | P | P 9 3.5 | P 13 0.7 | P 10 0.5 |
| `b119b1f_2` | P | F 12 6.3 | F 13 0.7 | F 13 0.7 |
| `b119b1f_3` | P | F 10 5.4 | F 10 0.6 | F 13 0.8 |
| `d4e9306_1` | P | P 6 2.7 | P 6 0.7 | P 7 0.8 |
| `d4e9306_2` | P | P 8 3.7 | P 7 0.8 | P 7 0.8 |
| `d4e9306_3` | P | P 8 3.6 | P 10 1.3 | P 10 1.2 |
| `0d8a4ee_1`* | F | F 8 3.3 | F 7 0.7 | P 8 0.7 |
| `0d8a4ee_2`* | F | F 7 3.1 | P 8 0.8 | F 10 0.9 |
| `0d8a4ee_3`* | P | P 7 3.0 | P 7 1.1 | P 12 2.3 |
| `37a8675_1`* | P | P 11 4.5 | F 10 0.7 | F 5 0.3 |
| `37a8675_2`* | P | F 11 4.5 | F 10 0.7 | F 10 0.7 |
| `37a8675_3`* | P | P 8 3.2 | P 9 0.8 | F 5 0.3 |
| `3ab5b8b_1`* | P | F 13 7.6 | F 13 1.6 | F 7 0.5 |
| `3ab5b8b_2`* | P | P 10 5.8 | F 8 0.7 | F 16 1.9 |
| `3ab5b8b_3`* | F | F 6 2.4 | F 6 0.4 | F 6 0.4 |
| `df61dc5_1` | P | P 12 5.5 | F 8 0.7 | P 9 0.8 |
| `df61dc5_2` | F | F 17 10.2 | F 16 2.6 | F 27 5.4 |
| `df61dc5_3` | P | F 8 4.0 | P 15 2.3 | F 15 3.9 |
| `383cbac_1` | F | P 5 2.1 | F 10 1.2 | F 7 0.6 |
| `383cbac_2` | P | F 6 2.6 | F 50 20.9 | F 7 0.7 |
| `383cbac_3` | F | F 5 2.1 | F 10 1.1 | F 7 0.7 |
| `23cf851_1` | P | P 5 2.0 | P 6 0.4 | P 6 0.4 |
| `23cf851_2` | P | F 7 3.0 | F 16 1.3 | F 7 0.6 |
| `23cf851_3` | P | P 6 2.5 | P 12 0.8 | F 12 1.2 |
| `57c3486_1`* | P | P 9 5.5 | F 10 2.4 | P 13 3.0 |
| `57c3486_2` | P | F 6 3.3 | P 7 1.7 | P 8 1.7 |
| `57c3486_3`* | P | P 9 5.3 | P 11 2.6 | P 9 2.6 |
| `68ee2c9_1` | P | P 16 11.2 | P 18 5.9 | P 20 7.4 |
| `68ee2c9_2` | P | P 14 9.5 | P 9 3.3 | P 10 4.0 |
| `68ee2c9_3` | P | P 12 9.7 | P 15 4.1 | P 22 5.0 |
| `6bdbc26_1` | P | P 5 1.9 | P 6 0.3 | P 6 0.3 |
| `6bdbc26_2` | P | P 5 1.9 | P 6 0.3 | P 6 0.3 |
| `6bdbc26_3` | P | P 5 1.9 | P 6 0.3 | P 6 0.3 |
| `6171bbc_1` | P | P 8 3.6 | P 9 1.0 | F 13 2.3 |
| `6171bbc_2` | P | P 9 4.0 | P 9 1.0 | P 9 0.9 |
| `6171bbc_3` | P | F 9 4.2 | F 23 2.8 | F 13 2.4 |
| `6c2c621_1` | P | F 8 5.1 | P 11 2.8 | F 11 2.8 |
| `6c2c621_2` | P | F 8 4.8 | F 12 2.6 | P 9 2.3 |
| `6c2c621_3` | P | F 10 6.7 | F 12 3.3 | F 12 3.4 |
| `396c5a2_1` | P | P 8 3.1 | P 8 0.6 | P 5 0.3 |
| `396c5a2_2` | P | F 9 5.1 | F 8 0.5 | F 8 0.5 |
| `396c5a2_3` | P | P 7 2.7 | P 8 0.4 | P 17 2.9 |
| `4fab96f_1` | P | F 6 2.6 | P 9 1.0 | F 7 0.5 |
| `4fab96f_2` | F | F 9 4.0 | F 10 1.5 | F 8 1.8 |
| `4fab96f_3` | P | F 7 3.0 | F 7 0.5 | F 10 1.0 |

`*` = the reference solution fails in this environment.
