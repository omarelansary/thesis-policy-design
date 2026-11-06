# RESULTS-R3-B (2026-11-05/06): R3 Part B, run by the lead on Linux (AUTH-024)

**What this is.** REQUEST-R3 Part B (B1 all tools, B2 control, B3 control repeated; 57 dev tasks each; `minimax/minimax-m3` on OpenRouter; provider fixed to `gmicloud/fp8`, `allow_fallbacks` false) run by the lead because the describing agent was unavailable. Counts and ids only; the key was read from a local file outside the repository and never printed or written here; no test split was run, opened or listed (the full data download was deleted unopened; only train and dev task folders were kept). UTC times. **The runner is a rebuild, not the describing agent's `run_part4.py`** (not in the repository): it is published here as `run_partb.py` and its differences are listed under *Deviations*. Hard result first (corrected 2026-11-06, see *Diagnosis*): **the pass rates below are far under Part 4's, and they are not comparable with Part 4: on OpenRouter/GMICloud the model returned no reasoning on any of 1,637 replies, while on ScaDS it reasons.** The earlier version of this line said the Linux environment fails 11 of 57 reference solutions; that was an error in the lead's check script, and the corrected check passes 57 of 57, as in Part 4. Token, cache and cost figures are measured as stated; they describe MiniMax-M3 without reasoning.

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
`envcheck.py` executes each dev task's published reference solution (`compiled_solution_code` followed by `solution(apis, requester)`, as AppWorld's own `verify.py` does) and evaluates it, with the call recorded for Part 4 (`r1-appworld-summary-2026-11-01.json`, `solution_execution`: `AppWorld(task_id, experiment_name, raise_on_failure=False, ground_truth_mode="full", timeout_seconds=None)`). **Result here: 57 of 57 pass, 0 execution errors** (2026-11-06), as in Part 4 on Windows (`r1-part4-envcheck-dev-solutions-2026-11-01.json`). The environment is not the cause of the accuracy gap.
**Correction.** The first version of the check (2026-11-05) left `raise_on_failure` at AppWorld's default (`True`) and reported 46 of 57 (failing `0d8a4ee_1/_2/_3`, `37a8675_1/_2/_3`, `3ab5b8b_1/_2/_3`, `57c3486_1`, `57c3486_3`). These 11 solutions expect an HTTP 422 (an account that does not exist, a card without enough money, a song already liked) and test for it; with `raise_on_failure` true the 422 raises an exception instead. R1 recorded 422 responses in exactly 11 tasks whose reference solutions still pass. The same mistake was repeated in the variants with a fresh data folder, `TZ=UTC`, `PYTHONHASHSEED=0` and `LC_ALL=C`, which is why they changed nothing. The agent runs are not affected: their `appworld_config` is the template's (it sets no `raise_on_failure`), as in Part 4. Both results are in `envcheck-result.json`.

## Against Part 4 (ScaDS, same model name, predictor on)
Part 4: 50 of 57. Here (B2, B3): 28 and 24. **17 tasks passed in Part 4 and in none of B1, B2, B3.** Per scenario (3 tasks; Part 4 passed a of 3, the three B runs together b of 9, so compare a/3 with b/9): lower here: `4ec8de5` 3/3 against 0/9, `fac291d` 3/3 against 0/9, `3ab5b8b` 2/3 against 1/9, `4fab96f` 2/3 against 1/9, `50e1ac9` 3/3 against 2/9, `6c2c621` 3/3 against 2/9, `37a8675` 3/3 against 3/9, `383cbac` 1/3 against 1/9, `b119b1f` 3/3 against 3/9, `df61dc5` 2/3 against 3/9, `23cf851` 3/3 against 5/9, `6171bbc` 3/3 against 5/9, `396c5a2` 3/3 against 6/9, `57c3486` 3/3 against 7/9; equal: `530b157`, `68ee2c9`, `6bdbc26`, `d4e9306`; higher here: `0d8a4ee`. Mean agent steps per task: Part 4 10.5 turns; here B1 9.3, B2 10.6, B3 9.8 (these include the predictor step), so the agents stop at a similar point and then fail the check, mostly on the returned answer. On the 10 pilot tasks (dev[0::6]) this run passed 5 (B1), 6 (B2) and 5 (B3) of 10, against 7 and 7 in the Windows pilot on OpenRouter and 8 and 9 on ScaDS. The causes examined are in the next section.

## Diagnosis (2026-11-06, no model call; counts in `r3-b-diagnosis.json`, script `diagnose_partb.py`)
The Windows-side files already in the repository served as the reference, because nothing can be run on Windows now.
1. **Environment: ruled out** [O]. Reference solutions pass 57 of 57 here (section above). The package versions equal Part 4's `pip freeze` apart from the platform extras.
2. **Runner: not shown to matter** [O/I]. The settings match RESULTS-R1's description of Part 4: AppWorld's template, `appworld_config` unchanged, 3-shot, temperature 0, seed 100, `tool_choice` auto, `parallel_tool_calls` true, 50 steps, reasoning content kept in the history. The differences are the provider pin, 20 instead of 100 retries (none used), the trace and the spend cap. On the 10 pilot tasks the Windows pilot, which used `run_part4.py` on OpenRouter, passed 7 and 7; this run passed 5, 6 and 5. That gap is within the B2-against-B3 spread on identical settings (12 of 57 flips). An unknown difference in `run_part4.py` cannot be excluded; THREAD E-25 point 2 asks the describing agent.
3. **API predictor: not the main cause** [O]. In B2, 18 failed tasks were offered every required (non-supervisor) API of the task; in B3 it was 21. B1, which offers all 469 definitions, passed 28 like B2. The number of functions offered in B2 matches Part 4 per task (median difference +1).
4. **Reasoning: the clearest difference** [O for the counts, F for the listing, I for the link to accuracy]. In B1, B2 and B3 not one of the 1,637 replies carries reasoning (`reasoning`, `reasoning_content`, `reasoning_details` empty, no `<think>` in the content, `reasoning_tokens` 0). On ScaDS the model reasons:
   - R2's `/responses` probe on ScaDS returned `reasoning,message` items on 5 of 5 replies; the same cell on GMICloud (R3 A3) returned `message` only.
   - For the same single tool call (`tool_07`), ScaDS replies used 41-77 completion tokens and GMICloud 28 on 12 of 15 replies (at most 39).
   - For a text-only reply (C8), ScaDS used 96-144 completion tokens for 72-129 characters of text, GMICloud 30-40 tokens for 97-145 characters. That is roughly the text alone, about 3.6 characters per token.
   - In the AppWorld runs, completion tokens per LM call (median over tasks) were 445 in Part 4 and 451 in its ScaDS repeat, against 236, 238 and 220 in B1, B2 and B3.
   - RESULTS-R1 records that Part 4 kept reasoning content in the message history.
   - OpenRouter's public model listing gives `"reasoning": {"mandatory": false}` for `minimax/minimax-m3` (`r3-b-openrouter-model-minimax-m3-2026-11-06.json`, fetched 2026-11-06). Its endpoint listing (R3 A2) shows `reasoning` and `include_reasoning` among GMICloud's supported parameters.
   - Neither the Windows pilot nor this run sent a `reasoning` parameter. Most likely, therefore, every OpenRouter run of R2 and R3 used MiniMax-M3 without thinking, while ScaDS served it with thinking.
5. **Not separable from 4 without a run** [U]. The fp8 quantisation of `gmicloud/fp8`, and GMICloud's run-to-run variation (12 of 57 flips between B2 and B3, against 5 of 57 on ScaDS).

Consequence. Within Part B, B1 against B2 is a like-for-like comparison: same host, same settings, both without reasoning. Its token, cache and cost ratios stand for that setting. Its accuracy figures (28 and 28, with B3 at 24) do not separate the arms from run-to-run variation. Part B against Part 4 compares a model without thinking with one with thinking, so it says nothing about the host or about tool offering. Testing point 4 needs model calls with reasoning switched on, which is a new probe under AUTH-024 and waits for the human.

## Deviations from REQUEST-R3 Part B and from the pilot
1. Run by the lead with a rebuilt runner on Linux instead of by the describing agent with `run_part4.py` on Windows; the runner changes nothing in AppWorld's agent code and adds: the 300 s client timeout, the provider pin through `extra_body`, a counts-only trace of every raw call (`r3-b-*-calls.jsonl`: task id, whether a predictor call, tokens, cost, provider, finish reason, number of tool calls, elapsed seconds), a dev-only guard, per-task exception handling and a spend cap.
2. The rerun rule (a hung task is rerun once) was never needed: no task hung, none raised, no call failed.
3. Elapsed seconds in the trace come from a real-time counter because AppWorld freezes the clock inside a task (found in the first smoke run; fixed before Part B).
4. AppWorld's own cost caps use `cost_per_token` set to GMICloud's listed prices; the cost column is the endpoint's reported `usage.cost`.
5. The data folder holds the train and dev tasks only (147 task folders); `appworld install` also unpacked a tests bundle to `~/.cache/appworld/tests` outside the working folder.
6. Accuracy is not comparable with Part 4 (see *Diagnosis*); this report gives no verdict on tool offering.
7. No `reasoning` parameter was sent, as in the pilot. Reasoning output is optional for this model on OpenRouter, and none was returned (see *Diagnosis* point 4).

## Files
`RESULTS-R3-B.md` (this file); `r3-b-b1-stats.json`, `r3-b-b2-stats.json`, `r3-b-b3-stats.json` (per task: result, failure type, steps, LM calls, prompt, cached, cache-write, completion, cost, providers, first agent call's cached and prompt tokens; totals); `r3-b-b1-calls.jsonl`, `r3-b-b2-calls.jsonl`, `r3-b-b3-calls.jsonl` (per call); `r3-b-comparison.json`; `envcheck-result.json` (corrected result and the superseded first one); `r3-b-diagnosis.json` (counts for *Diagnosis*); `r3-b-openrouter-model-minimax-m3-2026-11-06.json` (OpenRouter's public listing entry); `run_partb.py`, `run_all.sh`, `analyze_partb.py`, `envcheck.py` (corrected 2026-11-06), `diagnose_partb.py` (local paths are relative to the working folder).

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

`*` = one of the 11 tasks whose reference solution meets an HTTP 422 it expects (the first, faulty check reported these as failing; the corrected check passes all 57).
