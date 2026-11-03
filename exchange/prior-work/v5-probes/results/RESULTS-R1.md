# RESULTS-R1 (2026-11-01): Parts 1-3 done (ScaDS and OpenAI); Part 4 running

Written by the human's agent. No verdicts. AppWorld text (definitions, tasks, solutions, tool outputs) is kept outside this folder; only counts, lengths, ids and public GitHub issue metadata are here.

## Part 1 (tool-choice probe): DONE, ScaDS 2026-11-01T13:31Z to about 14:02Z, OpenAI 14:39Z to 14:41Z
- Command (run by the human's agent through `run_r1_parts_1_and_3.ps1`, a copy of which is in this folder; it loads the key inside the script and never prints it): per model `python p2_tool_choice_probe.py --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model <id> --max-tokens 1024 --pause 15 --out raw/r1-scads-<model-slug>-2026-11-01.json`. The script is the unmodified copy of `../p2_tool_choice_probe.py`. The ten per-model outputs are in `raw/`; `r1-scads-2026-11-01.json` is their `models` objects merged into one file by a one-off script, nothing else changed.
- Models as served (status page of 2026-11-01T13:05Z, all up, `supports_tools: true`): `deepseek-ai/DeepSeek-V4.1-Flash`, `google/gemma-4-26B-A4B-it`, `meta-llama/Llama-3.3-70B-Instruct`, `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3.1-Flash`, `openai/gpt-oss-120b`, `Qwen/Qwen3.8-27B`, `zai-org/GLM-5.3`, `zai-org/GLM-5.3-Flash`; and `alias-code` as a probe only (it is not used anywhere else in the project).
- Where ScaDS documents tool support: the `supports_tools`, `supports_reasoning`, `supports_vision`, `max_tokens` fields per model in `https://llm.scads.ai/status/state.json`; no other way to restrict tools is documented there. Other places (its docs, `/v1/models` metadata, a LiteLLM setting) were not searched.
- Result table: cells C0..C9 as defined in the script header; each entry is the HTTP status, then the last two characters of the name of the tool called (`07` = tool_07, `03` = tool_03; `-` = no tool call). The allowed subset in C2-C4 and C8 is tool_03, tool_04, tool_05; the user asks for tool_07.

| Model | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 |
|---|---|---|---|---|---|---|---|---|---|---|
| `MiniMaxAI/MiniMax-M3` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 07 | 200 - | 200 - | 200 - |
| `MiniMaxAI/MiniMax-M3.1-Flash` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 07 | 200 - | 200 03 | 200 - |
| `Qwen/Qwen3.8-27B` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 - |
| `alias-code` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 - |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 - |
| `google/gemma-4-26B-A4B-it` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 07 | 200 - | 200 - | 200 - |
| `meta-llama/Llama-3.3-70B-Instruct` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 07 | 200 - |
| `openai/gpt-oss-120b` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 07 |
| `zai-org/GLM-5.3` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 - |
| `zai-org/GLM-5.3-Flash` | 200 07 | 200 07 | 400 - | 400 - | 400 - | 200 07 | 200 03 | 200 - | 200 - | 200 - |

- C2, C3 and C4 returned HTTP 400 for all ten models. The scrubbed error text begins `litellm.BadRequestError: Invalid tool choice, tool_choice={'type': 'allowed_tools', ...` in each (see the files).
- Cached prompt tokens on C1 (the repeat of C0): MiniMax-M3 4224, MiniMax-M3.1-Flash 4224, Qwen3.8-27B 1648, alias-code 1648, DeepSeek-V4.1-Flash 4096, gemma 3840, Llama-3.3-70B 4672, gpt-oss-120b 3520, GLM-5.3 3968, GLM-5.3-Flash 2304; prompt sizes were 4,071 to 4,644 tokens.
- OpenAI (run after the ScaDS runs; the first runner pass skipped it because it looked for the variable name `OPENAI_API_KEY` while the service `.env` stores the key as `OPEN_AI_API_KEY`; runner fixed and run again with `-SkipScads`): `gpt-4.1-mini` with the unmodified script, `gpt-5-mini` with `p2_tool_choice_probe_oai.py` (the copy that differs from the original only in using the request field `max_completion_tokens` instead of `max_tokens` on lines 107 and 138, because the `gpt-5` family rejects `max_tokens`), both with `--max-tokens 1024 --pause 2`, base `https://api.openai.com/v1`. Model ids as sent; the snapshot the API resolved them to is not recorded in the outputs. Same cell notation as above (merged file `r1-openai-2026-11-01.json`, per-model files in `raw/`):

| Model | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 |
|---|---|---|---|---|---|---|---|---|---|---|
| `gpt-4.1-mini` | 200 07 | 200 07 | 200 05 | 400 - | 200 05 | 200 07 | 200 03 | 200 - | 200 - | 200 04 |
| `gpt-5-mini` | 200 07 | 200 07 | 200 04 | 400 - | 200 05 | 200 07 | 200 - | 200 - | 200 - | 200 05 |

  - C3 (flat `allowed_tools` shape on Chat Completions) returned HTTP 400 for both: `Missing required parameter: 'tool_choice.function'.` C2 and C4 (the Chat Completions shape) returned 200.
  - `gpt-5-mini` C6 ended with `finish_reason` length and no tool call (1,024 completion tokens used); the other cells ended normally. The OpenAI outputs were searched for both keys by the runner: not present.
- Deviations: `--max-tokens 1024` instead of the default 64 (most of these models reason first); `--pause 15` instead of the suggested 35 (no HTTP 429 appears in any output; the script retries a 429 once after 65 s, which would not show). One sample per cell, no temperature set, as in the script. The runner searched the output files for the ScaDS key string: not present.

## Part 2 (AppWorld statistics): DONE, 2026-11-01T13:09Z to 13:20Z
- Versions: `appworld` 0.1.3.post1; data `version.txt` 0.1.0; Python 3.12; Windows 11, native (no Docker).
- Files in this folder: `r1-appworld-summary-2026-11-01.json` (all aggregates, versions, commands, timestamps, deviations), `r1-appworld-definitions-stats-2026-11-01.json`, `r1-appworld-tasks-2026-11-01.jsonl` (one line per task: ids, split, required apps, call counts, response lengths, status codes, pass), `r1-appworld-issues-2026-11-01.json` (73 issues, titles/state/dates and a short public phrase each).
- Definitions: 457 in function-calling form, 457 distinct names, 11 groups (9 apps plus `api_docs` and `supervisor`): amazon 66, api_docs 4, file_system 26, gmail 42, phone 30, simple_note 17, splitwise 65, spotify 91, supervisor 6, todoist 56, venmo 54); JSON length per definition min 171, median 429, mean 559.6, max 2586, total 255,745 characters. The combined list is local only (`<local>/appworld-local\appworld_fc_tools.json`).
- Reference solutions, executed once each: train 90 tasks, dev 57 tasks (the request expected 60), 147 of 147 evaluation passes, 0 execution failures. API calls per task: median 36, mean 52.6, min 5, max 244 (7,733 calls). Response length per call (characters of the raw HTTP text): median 109, mean 230.4, max 4,719; 24 of 7,733 responses had HTTP 422, in 11 tasks that still pass. Recomputed by the human's agent from the task file: counts, sums, medians and means agree; the 90th percentile of response length is 547 by nearest rank (the summary file gives 548 by its own method).
- Structure: 30 train and 19 dev scenarios, 3 tasks each, no scenario in both splits; tasks use 5 of the 9 apps (the other groups in the definitions are `api_docs` and `supervisor`): spotify, phone, venmo, file_system, simple_note) plus `supervisor`, which every task calls; 96 tasks use 1 app, 45 use 2, 6 use 3. Amazon, gmail, splitwise and todoist appear in no train or dev task.
- Issues: 73 (12 open, 61 closed), pull requests excluded.

Deviations and problems (full list in the summary file): no per-execution timeout (`signal.SIGALRM` absent on Windows); `PYTHONUTF8=1` set because `world.evaluate()` raised `UnicodeEncodeError` under cp1252 (two smoke tasks failed before the fix, output discarded); response lengths were captured by wrapping AppWorld's request function in the runner; `appworld install` also unpacked a tests bundle to `<home>/.appworld\tests` (outside the working folder, left in place); the data folder on disk contains the `test_normal` and `test_challenge` task folders, which were not opened, listed or loaded (only `load_task_ids` for `train` and `dev` was called); the issues file contains public GitHub text that names some `test_challenge` task ids.

## Part 3 (billed tokens of real definitions): DONE, ScaDS 2026-11-01T14:02Z to 14:18Z, OpenAI 14:39Z to 14:43Z
- Command per model: `python p2_tool_choice_probe.py --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model <id> --deftokens <local>/appworld-local/appworld_fc_tools.json --sizes 0 10 50 100 200 457 --pause 15 --out r3-deftokens-<model-slug>-2026-11-01.json` (the nine non-alias models; the per-model files are also in `raw/`). The local file holds the 457 AppWorld definitions and is not in this folder. The script slices the first n definitions of the file; each request is one user message `ok` with `max_tokens` 1.
- Prompt tokens as billed (`usage.prompt_tokens`) for the first n definitions:

| Model | n=0 | 10 | 50 | 100 | 200 | 457 |
|---|---|---|---|---|---|---|
| `MiniMaxAI/MiniMax-M3` | 174 | 1202 | 6806 | 13299 | 28412 | 63922 |
| `MiniMaxAI/MiniMax-M3.1-Flash` | 192 | 1220 | 6824 | 13317 | 28430 | 63940 |
| `Qwen/Qwen3.8-27B` | 41 | 1141 | 6987 | 13694 | 29311 | 66081 |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 31 | 1062 | 6552 | 12939 | 27794 | 62471 |
| `google/gemma-4-26B-A4B-it` | 14 | 735 | 5458 | 11261 | 24703 | 55483 |
| `meta-llama/Llama-3.3-70B-Instruct` | 36 | 1263 | 8478 | 16801 | 36120 | HTTP 400 |
| `openai/gpt-oss-120b` | 68 | 513 | 3640 | 7490 | 16314 | 36786 |
| `zai-org/GLM-5.3` | 13 | 912 | 6311 | 12513 | 27037 | 60995 |
| `zai-org/GLM-5.3-Flash` | 13 | 912 | 6311 | 12513 | 27037 | 60995 |

- Llama-3.3-70B-Instruct at n=457: HTTP 400 `litellm.ContextWindowExceededError ... This model's maximum context length is 65536 tokens. However, you requested 1 output tokens and your prompt contains at least 65536 input tokens` (scrubbed text in the file).
- Observations, not examined further: the two GLM models report identical counts at every size; the two MiniMax models differ by a constant 18 tokens at every size; the n=0 counts differ between models (13 to 192 tokens).
- OpenAI (same runner pass as Part 1; base `https://api.openai.com/v1`, `--pause 2`, same sizes; `gpt-4.1-mini` with the unmodified script, `gpt-5-mini` with `p2_tool_choice_probe_oai.py`, which sends `max_completion_tokens` 1 in this mode):

| Model | n=0 | 10 | 50 | 100 | 200 | 457 |
|---|---|---|---|---|---|---|
| `gpt-4.1-mini` | 8 | 514 | 4068 | 8184 | HTTP 400 | HTTP 400 |
| `gpt-5-mini` | HTTP 400 | HTTP 400 | HTTP 400 | HTTP 400 | HTTP 400 | HTTP 400 |

  - `gpt-4.1-mini` at n=200 and n=457: HTTP 400 `Invalid 'tools': array too long. Expected an array with maximum length 128, but got an array with length 200 [457] instead.` (`array_above_max_length`).
  - `gpt-5-mini` returned HTTP 400 at every size. At n=0..100 the message is `Could not finish the message because max_tokens or model output limit was reached`, i.e. the 1-token output limit made the request fail before any usage was reported; at n=200 and 457 the same tools-array limit of 128 as above.
  - Because of that, `gpt-5-mini` was run again with a second separate copy, `p2_tool_choice_probe_oai256.py` (identical to the first copy except `max_completion_tokens` 256 instead of 1 in the definition-token mode), command `run_oai_deftokens256.ps1`, 2026-11-01T14:42Z, output `r3-deftokens-gpt-5-mini-completion256-2026-11-01.json`: prompt tokens 7 / 595 / 4,149 / 8,265 for n = 0 / 10 / 50 / 100 (cached 0 / 0 / 3,968 / 8,064 for n = 0 / 10 / 50 / 100), HTTP 400 `array_above_max_length` at n = 200 and 457.
  - Cost: not read from the billing page. From the token counts (about 0.1 million tokens in all for OpenAI) it is a small fraction of a dollar.

## Part 4 (floor pilot, AppWorld `simplified_function_calling_agent` on dev): DONE (one run per model), started about 2026-11-01T15:15Z, finished 2026-11-01T21:59Z
Results are in the table below and in `r1-part4-stats-<tag>-2026-11-01.json`.
- Version change, relevant to comparability with Part 2: `simplified_function_calling_agent` is not in the package used for Part 2 (`appworld` 0.1.3.post1, data 0.1.0). It exists on GitHub main (`appworld` 0.2.0.dev0, commit `42b5bcf3cd334fee33f0c37c02070a9f5807add5`), which needs data 0.2.0. Part 4 therefore uses its own environment (Python 3.12; package list in `r1-appworld-pip-freeze-part4-env-2026-11-01.txt`) and data 0.2.0 (dev split, 57 task folders, plus the 3 train tasks the agent's configuration uses as in-context demonstrations). The 57 dev task ids are identical in data 0.1.0 and 0.2.0; the 0.2.0 changelog says it fixed one reported dev-scenario issue, so Part 2 figures (data 0.1.0) may not match exactly. The data download for 0.2.0 temporarily contained the test splits; that temporary folder was deleted unopened.
- Agent and settings: AppWorld's agent code unchanged, configuration rendered from AppWorld's template with its defaults: `max_steps` 50, chat completions through the `openai` client with `base_url` https://llm.scads.ai/v1, `tool_choice` auto, `parallel_tool_calls` true, 3-shot demonstrations, temperature 0, seed 100, up to 100 retries 15 s apart, no cache, `max_output_tokens_per_task` 100000. A runner of our own (`run_part4.py`, a copy of `Agent.solve_tasks`) adds a dev-only guard (a non-dev task id exits before any run starts), per-task exception handling, a progress log and a counts-only trace. `PYTHON_DOTENV_DISABLED=1` and `MODEL_SERVER_URL` set as the agent requires. AppWorld's own `evaluate_task` is used for pass/fail; TGC and SGC follow AppWorld's metric (SGC counts a scenario only if its 3 tasks were requested; tasks not run count as failed).
- Built-in tool selection: the agent makes one extra first call, an "API predictor", that picks at most 20 APIs from the API descriptions (mode `predicted`); the agent then sees only those functions. That call is included in the token totals. In the stats files `llm_calls` includes it and `turns` excludes it.
- Models and order (one run each, one task at a time): `MiniMaxAI/MiniMax-M3` (tag `minimax-m3`), then `deepseek-ai/DeepSeek-V4.1-Flash` (tag `deepseek-v41-flash`). Chosen after a one-task smoke on each (task `50e1ac9_1`, tags `smoke-minimax`, `smoke-deepseek`, about 80 s each, both passed; timing checks only, not part of the results).
- Environment check, because the Part 4 environment has `sqlmodel` 0.0.48 and open AppWorld issue #229 reports that `sqlmodel>=0.0.45` rejects naive datetimes so that every amazon `place_order` fails: the published reference solutions of all 57 dev tasks were executed and evaluated in the Part 4 environment: 57 of 57 pass, 0 execution failures (`r1-part4-envcheck-dev-solutions-2026-11-01.json`). Part 2 (data 0.1.0) ran with `sqlmodel` 0.0.10. No train or dev task uses the amazon app (Part 2).
- Other deviations: the key goes only into `OPENAI_API_KEY`/`OPENAI_API_BASE`/`OPENAI_BASE_URL` for the process (AppWorld's `api_key_env_name` option was not used because it would write the key into `lm_calls.jsonl`), restored afterwards; the agent prints task text, so all console output goes to a local `console.log` outside this folder; reasoning content stays in the message history (no `-DropReasoningContent`); whether ScaDS accepts `seed` and temperature 0 for each model was untested before the run. Usage from an LM call that fails with a breaking error is not counted by the agent.
- Packages installed or left behind outside the working folder: a failed first install attempt of `litellm` created a Rust toolchain cache at `<home>/AppData/Local/puccinialin/` (left in place); Part 2's `appworld install` unpacked a tests bundle to `<home>/.appworld/tests` (left in place).
- Hang and timeout (2026-11-01): the `minimax-m3` run finished tasks 1 to 8 and then made no progress for more than 30 minutes inside task 9 (`530b157_3`, 20 language-model calls logged, then no CPU use and open connections: a request that never returned; the endpoint status page showed the model up). The agent's OpenAI client had no request timeout of its own (SDK default 600 s, 2 retries). At about 16:50 local time (15:50Z) the stuck process was stopped by the human's agent, and `run_part4.py` was changed to give every OpenAI client created by the agent a 300 s read timeout (AppWorld's own retry loop of 100 x 15 s is unchanged). The `minimax-m3` run is resumed after the `deepseek-v41-flash` run; tasks 1 to 8 are kept, task 9 restarts from scratch (the partial attempt is not counted). Tasks 1 to 8 ran without the timeout patch.
- Test-split id lists: one search by the agent compared three train task ids against the dataset id-list files, which include the `test_normal` and `test_challenge` lists, and printed no test content. No test task was run or loaded.

### Part 4 results (counts only; one run per model, 57 dev tasks, 19 scenarios, no interpretation)

| | MiniMaxAI/MiniMax-M3 | deepseek-ai/DeepSeek-V4.1-Flash |
|---|---|---|
| tasks run / requested | 57 / 57 | 57 / 57 |
| tasks passed (TGC) | 50 of 57 (TGC 0.8772) | 48 of 57 (TGC 0.8421) |
| scenarios with all 3 tasks passed (SGC) | 14 of 19 (SGC 0.7368) | 14 of 19 (SGC 0.7368) |
| failures by type | evaluation_failed 4, step_cap_reached 3 | evaluation_failed 7, step_cap_reached 2 |
| exceptions (task not finished) | 0 | 0 |
| LM calls total (incl. 1 API-predictor call per task) | 658 | 580 |
| prompt tokens total (cache hit part) | 13,998,443 (13,020,544) | 7,933,019 (7,013,888) |
| completion tokens total | 396,566 | 504,952 |
| agent turns per task: median / mean / max | 8 / 10.54 / 49 | 8 / 9.18 / 49 |
| prompt tokens per task: median / mean / max | 77,044 / 245,587 / 3,753,369 | 76,198 / 139,176 / 1,399,396 |
| completion tokens per task: median / mean / max | 4,415 / 6,957 / 46,591 | 4,794 / 8,859 / 55,399 |

Files: `r1-part4-stats-minimax-m3-2026-11-01.json`, `r1-part4-stats-deepseek-v41-flash-2026-11-01.json` (per-task pass/fail, turns, token counts and failure type; no task text, no model output, no path; field and failure-type definitions are inside each file). Token counts come from the agent's per-call usage records and equal the sums of the per-task `usage.json` files (cross-check recorded in each stats file: 57 of 57 tasks).

How the runs went (facts about execution, not about the models):
- Command for each model: `run_part4.ps1 -Model <id> -Tag <tag>` (all 57 dev tasks in AppWorld order, one at a time); model ids as given to the endpoint; stats written by `part4_stats.py`. Times below are local time (UTC+1). Correction made 2026-11-02: the `ts` stamps in `progress.jsonl` are local time too, not UTC as an earlier version of this line said.
- Neither run was a single uninterrupted process. MiniMax-M3: tasks 1–8 in a first process, which then hung on task 9 for a long time because the `openai` client had no request timeout; I stopped it and added a 300 s client timeout (`run_part4.py`), after which tasks 9–57 ran in a second process (resumed about 20:35, finished 22:59). The first-process tasks 1–8 ran without the timeout patch. DeepSeek-V4.1-Flash: started 16:50 with the patch; tasks 1–23 completed, task 24 (`37a8675_3`) began about 17:12 local (the previous task's stamp) and kept writing files until 18:34 local, then produced no file writes for 38 minutes (about 1.09 M input tokens already used by then), I stopped the process at 19:12 and resumed with the same tag; task 24 was run again from the start and tasks 24–57 finished at about 20:34. The cause of the stall was not determined. Tokens used by the discarded partial attempts (MiniMax task 9; DeepSeek task 24 before the stop) are not in the totals above.
- A resumed run skips tasks that have a finished record; the stats are computed from the per-task records of the final state, so they cover all 57 tasks of each model once.
- Slowest tasks: DeepSeek `4fab96f_2` 1656 s (step cap reached); several tasks of both models took 300–440 s. Both final records have zero exceptions. Retries of individual LM calls by the agent are not counted in the totals.
- Left as it is: the run was not repeated, so the seed/temperature determinism of either endpoint is untested; no result here should be read as a difference between the two models without repeats.

## Responses to review comments on this run (2026-11-01)
1. **Hard-coded path to the adapter's `.env` in the runner scripts.** The two `.ps1` copies in this folder had the real local paths, including the adapter folder name. Decision (taken by the human's agent): keep the scripts, redact the paths. The published copies now carry placeholders (`<adapter service .env>`, `<exchange>`, `<scratch>`, `<local>`, `<home>`) and a note on their first line; the same replacement was applied to this file and to the Part 2 summary file. The scripts hold no key or result. They cannot be run as published without restoring the paths. The raw output files contain no local path.
2. **Provenance of the probe files.** The unmodified original (`../p2_tool_choice_probe.py`, sha256 `306c7ab9bb1fd15ed3c93c6fe133766fceab6994bdc44d8324d75ad590fea484`, last modified before the first run started) is the file that ran for all ScaDS models and for `gpt-4.1-mini`; it was run from the request folder, not from a scratch copy. Only `gpt-5-mini` used scratch copies: `p2_tool_choice_probe_oai.py` (sha256 `c9580b3fc31823ddde2fb8978bc833907cbb640478e00f0857f0927002150f2d`) and `p2_tool_choice_probe_oai256.py` (sha256 `34049b310f0cb510fe18d84c105f3b04dda588d3487ccfae247e36b5bea76fae`); the copies in this folder were made from them with `cp` and have the same hashes. Run-time hashes of the runners (before redaction): `run_r1_parts_1_and_3.ps1` `cfe59c9f93d0ebf3d39b0f94cde80f3dcadb5c1945fe07d608f9a4e0dae87a4a`, `run_oai_deftokens256.ps1` `732aaef5cb825b9a0fe5e1af538a27fa306d460237a4658a6417e8305ea58fe6`. The runner in this folder is its second version: the ScaDS pass ran the first version, which differs only in not looking for the variable `OPEN_AI_API_KEY` and not having the `-SkipScads` switch; the second version ran the OpenAI pass.
3. **One sample per cell.** Correct: every Part 1 cell was run once, with no temperature set, as in the script. A tool call inside the allowed subset, when the user asked for a tool outside it, is still informative; a call outside it, or no call, is one sample. Repeats were not run; they can be run in a separate copy (cheap for the OpenAI models).
4. **Package versions.** Now recorded: `r1-appworld-pip-freeze-part2-env-2026-11-01.txt` and `r1-appworld-pip-freeze-part4-env-2026-11-01.txt`. Part 2 environment: `appworld` 0.1.3.post1, `sqlmodel` 0.0.10, `SQLAlchemy` 1.4.54, `pydantic` 1.10.27, `fastapi` 0.110.3 (below the 0.0.45 threshold of issue #229). Part 4 environment: AppWorld main 0.2.0.dev0, `sqlmodel` 0.0.48 (above the threshold), `SQLAlchemy` 2.0.55, `pydantic` 2.12.5, `fastapi` 0.119.1, `openai` 1.99.8, `litellm` 1.80.0; the environment check above is the test of whether the issue affects the dev tasks.
5. **Canary field in the definitions.** The local definitions file that was sent in Part 3 has no `canary_string` key and no occurrence of the word "canary" in any of its 457 definitions (checked 2026-11-01); the token counts are therefore not inflated by it. The character-length statistics in `r1-appworld-definitions-stats-2026-11-01.json` are given without the key in the summary file and, separately, with it in the definitions-stats file.
