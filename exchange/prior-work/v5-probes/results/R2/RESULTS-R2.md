# RESULTS-R2 (reply to REQUEST-R2.md; written by the human's agent, 2026-11-02)

Scope of this reply: Part A (A1–A5) is done. **B1 (repeat run) was released by the human and has been run; B2 (all tools) has not been run and is held until the human releases it.** Environment for everything below: the Part 4 environment unchanged (AppWorld 0.2.0.dev0 at commit `42b5bcf3…`, data 0.2.0). No test split was run, opened or listed. No AppWorld text is in this folder: only counts, ids and lengths. Times are UTC. The human's agent ran everything; no verdicts are given.

Fixed before any Part B run (as the request asks; recorded before B1 started and applied to it): client timeout 300 s from the first task (the `openai` client patch in `run_part4.py`), step cap 50, rerun rule = a task whose process hangs is rerun once from scratch and logged with the reason, no other reruns, and a new experiment name per run (open issue #203).

## A1. Repeats with the version-2 probe

- Script: `../../p2_tool_choice_probe_v2.py` run unmodified, sha256 `ef04642730107b60265be006084267f0a01565d59e070a39f3cd733e2abcc0dd`. Runner: `run_r2_a1.ps1` (paths replaced by placeholders; the version that ran has sha256 `aac841028f6d0a07d562853b1a8d44f49a7cd83ad00150ae7792120c41fe8419`), which reads the keys inside its own process from the adapter service `.env` and never prints them.
- Command per model (ScaDS): `python p2_tool_choice_probe_v2.py --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model <id> --cells C2 C4 C6 C8 C9 --repeat 5 --max-tokens 1024 --pause 15 --out raw/r2-scads-<id with / as __>-2026-11-02.json`; OpenAI: the same with `--base https://api.openai.com/v1 --key-env OPENAI_API_KEY --pause 2`, and `--token-param max_completion_tokens` for `gpt-5-mini` (no copy of the script). Models: the nine ScaDS tool models of R1 (no alias) and `gpt-4.1-mini`, `gpt-5-mini`.
- Start times of each model's file (UTC):
- `raw/r2-openai-gpt-4.1-mini-2026-11-02.json` started 2026-11-02T10:55:15Z
- `raw/r2-openai-gpt-5-mini-2026-11-02.json` started 2026-11-02T10:56:31Z
- `raw/r2-scads-MiniMaxAI__MiniMax-M3-2026-11-02.json` started 2026-11-02T11:19:17Z
- `raw/r2-scads-MiniMaxAI__MiniMax-M3.1-Flash-2026-11-02.json` started 2026-11-02T11:25:47Z
- `raw/r2-scads-Qwen__Qwen3.8-27B-2026-11-02.json` started 2026-11-02T11:38:58Z
- `raw/r2-scads-deepseek-ai__DeepSeek-V4.1-Flash-2026-11-02.json` started 2026-11-02T10:59:33Z
- `raw/r2-scads-google__gemma-4-26B-A4B-it-2026-11-02.json` started 2026-11-02T11:06:15Z
- `raw/r2-scads-meta-llama__Llama-3.3-70B-Instruct-2026-11-02.json` started 2026-11-02T11:12:43Z
- `raw/r2-scads-openai__gpt-oss-120b-2026-11-02.json` started 2026-11-02T11:32:17Z
- `raw/r2-scads-zai-org__GLM-5.3-2026-11-02.json` started 2026-11-02T11:45:32Z
- `raw/r2-scads-zai-org__GLM-5.3-Flash-2026-11-02.json` started 2026-11-02T12:06:22Z
- Deviation: the script writes its file only at the end, so each model was run as its own call and its own file in `raw/`; `merge_r2_a1.py` joined them without changes into the files named in the request, `r2-scads-2026-11-02.json` and `r2-openai-2026-11-02.json` (each row keeps its `cell`, `rep`, status, usage, tools called, finish reason, `meta`). The merged files carry a `merged_from` list instead of a single start time. Cell C0/C1/C3/C5/C7 were not run (the request lists C2 C4 C6 C8 C9).
- Counts of the 5 replies per model and cell (`requested tool_07` = the reply called tool_07, the tool the user asked for; `subset` = only tool_03/04/05; `other tool` = another tool; `no tool` = HTTP 200 with no tool call; `errors` = replies that were not HTTP 200). In C6 the named tool is tool_03, which is in the subset column. In C9 the "tool" is a `function_call` output item. Also in `A1_summary_tables.md`:

| model | cell | requested tool_07 | subset (tool_03/04/05) | other tool | no tool | errors |
|---|---|---|---|---|---|---|
| MiniMaxAI/MiniMax-M3 | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| MiniMaxAI/MiniMax-M3 | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| MiniMaxAI/MiniMax-M3 | C6 | 5 | 0 | 0 | 0 | 0 |
| MiniMaxAI/MiniMax-M3 | C8 | 0 | 0 | 0 | 5 | 0 |
| MiniMaxAI/MiniMax-M3 | C9 | 0 | 0 | 0 | 5 | 0 |
| MiniMaxAI/MiniMax-M3.1-Flash | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| MiniMaxAI/MiniMax-M3.1-Flash | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| MiniMaxAI/MiniMax-M3.1-Flash | C6 | 5 | 0 | 0 | 0 | 0 |
| MiniMaxAI/MiniMax-M3.1-Flash | C8 | 0 | 0 | 0 | 5 | 0 |
| MiniMaxAI/MiniMax-M3.1-Flash | C9 | 0 | 0 | 0 | 5 | 0 |
| Qwen/Qwen3.8-27B | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| Qwen/Qwen3.8-27B | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| Qwen/Qwen3.8-27B | C6 | 0 | 5 | 0 | 0 | 0 |
| Qwen/Qwen3.8-27B | C8 | 0 | 0 | 0 | 5 | 0 |
| Qwen/Qwen3.8-27B | C9 | 0 | 0 | 0 | 5 | 0 |
| deepseek-ai/DeepSeek-V4.1-Flash | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| deepseek-ai/DeepSeek-V4.1-Flash | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| deepseek-ai/DeepSeek-V4.1-Flash | C6 | 0 | 5 | 0 | 0 | 0 |
| deepseek-ai/DeepSeek-V4.1-Flash | C8 | 0 | 0 | 0 | 5 | 0 |
| deepseek-ai/DeepSeek-V4.1-Flash | C9 | 0 | 0 | 0 | 5 | 0 |
| google/gemma-4-26B-A4B-it | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| google/gemma-4-26B-A4B-it | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| google/gemma-4-26B-A4B-it | C6 | 5 | 0 | 0 | 0 | 0 |
| google/gemma-4-26B-A4B-it | C8 | 0 | 0 | 0 | 5 | 0 |
| google/gemma-4-26B-A4B-it | C9 | 0 | 0 | 0 | 5 | 0 |
| meta-llama/Llama-3.3-70B-Instruct | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| meta-llama/Llama-3.3-70B-Instruct | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| meta-llama/Llama-3.3-70B-Instruct | C6 | 0 | 5 | 0 | 0 | 0 |
| meta-llama/Llama-3.3-70B-Instruct | C8 | 5 | 0 | 0 | 0 | 0 |
| meta-llama/Llama-3.3-70B-Instruct | C9 | 0 | 0 | 0 | 5 | 0 |
| openai/gpt-oss-120b | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| openai/gpt-oss-120b | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| openai/gpt-oss-120b | C6 | 0 | 5 | 0 | 0 | 0 |
| openai/gpt-oss-120b | C8 | 1 | 0 | 0 | 4 | 0 |
| openai/gpt-oss-120b | C9 | 5 | 0 | 0 | 0 | 0 |
| zai-org/GLM-5.3 | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| zai-org/GLM-5.3 | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| zai-org/GLM-5.3 | C6 | 0 | 5 | 0 | 0 | 0 |
| zai-org/GLM-5.3 | C8 | 0 | 0 | 0 | 5 | 0 |
| zai-org/GLM-5.3 | C9 | 0 | 0 | 0 | 5 | 0 |
| zai-org/GLM-5.3-Flash | C2 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| zai-org/GLM-5.3-Flash | C4 | 0 | 0 | 0 | 0 | HTTP 400 5 |
| zai-org/GLM-5.3-Flash | C6 | 0 | 5 | 0 | 0 | 0 |
| zai-org/GLM-5.3-Flash | C8 | 0 | 0 | 0 | 5 | 0 |
| zai-org/GLM-5.3-Flash | C9 | 0 | 0 | 0 | 5 | 0 |
| gpt-4.1-mini | C2 | 0 | 5 | 0 | 0 | 0 |
| gpt-4.1-mini | C4 | 0 | 5 | 0 | 0 | 0 |
| gpt-4.1-mini | C6 | 0 | 5 | 0 | 0 | 0 |
| gpt-4.1-mini | C8 | 0 | 0 | 0 | 5 | 0 |
| gpt-4.1-mini | C9 | 0 | 5 | 0 | 0 | 0 |
| gpt-5-mini | C2 | 0 | 5 | 0 | 0 | 0 |
| gpt-5-mini | C4 | 0 | 5 | 0 | 0 | 0 |
| gpt-5-mini | C6 | 0 | 0 | 0 | 5 | 0 |
| gpt-5-mini | C8 | 0 | 0 | 0 | 5 | 0 |
| gpt-5-mini | C9 | 0 | 5 | 0 | 0 | 0 |

- `x-litellm-version`: the value was `1.106.0` on all 135 HTTP-200 replies of the nine ScaDS models; the header is absent on the two OpenAI models (columns for all `x-litellm-*` header names, served model ids and `system_fingerprint` per model are in `A1_summary_tables.md`). Served model id equals the requested id for every ScaDS model; OpenAI served `gpt-4.1-mini-2025-04-14` and `gpt-5-mini-2025-08-07`. `system_fingerprint` (vLLM build strings for ScaDS, chat replies only; `None` in the C9 rows because `/responses` replies carry none): MiniMaxAI/MiniMax-M3: vllm-0.32.0-tp4-7a90bd24; MiniMaxAI/MiniMax-M3.1-Flash: vllm-0.1.dev23341+g8744dd2fb.d20261022-tp4-91773519; Qwen/Qwen3.8-27B: vllm-0.32.0-fd9309b2; deepseek-ai/DeepSeek-V4.1-Flash: vllm-0.32.0-tp4-ep-a70cb2c6; google/gemma-4-26B-A4B-it: vllm-0.31.0-f0427dc5; meta-llama/Llama-3.3-70B-Instruct: vllm-0.31.0-803ebedb; openai/gpt-oss-120b: vllm-0.31.0-0c81045a; zai-org/GLM-5.3: vllm-0.32.0-tp4-pp2-5c819679; zai-org/GLM-5.3-Flash: vllm-0.32.0-tp4-ep-10c5df41.
- Facts to read before the table: (a) C2 and C4 returned HTTP 400 on all 5 repeats for all nine ScaDS models, as in R1; both OpenAI models accepted them. (b) C9 returned HTTP 200 for all nine ScaDS models, with output item types `message` or `reasoning,message` (no `function_call`) except `openai/gpt-oss-120b`, whose five replies were `reasoning,function_call`; the reply text length and first 160 characters of each are in the JSON (`meta.text_len`, `meta.text_head`; these are text of the probe's own prompt, not of AppWorld). (c) `gpt-5-mini` in C6: 5 of 5 replies have `finish_reason` `length` with 1024 completion tokens and no tool call, so the `no tool` entries there are token-limit stops, not refusals. (d) `no tool` replies in C8 and in ScaDS C9 have `finish_reason` `stop` (C8) or none recorded (C9); counts only, no reading of the text was done for this table.

## A2. LiteLLM version and `allowed_tools` on `/responses`

One look: `https://llm.scads.ai/status/state.json` (timestamp 2026-11-02T10:55:00+00:00; keys `timestamp`, `models`, `all_up`; no mention of LiteLLM, a version, or `allowed_tools`) and the page `https://llm.scads.ai/` (sections: TUD:AI, How Can I Chat With an LLM?, Get in Touch; no version, no tool-choice text). Nothing found there. The LiteLLM version is known from the response header instead: see A1 (`x-litellm-version` above). The proxy's handling of `allowed_tools` on `/responses` is not documented in those two places; what was observed is in A1 (C9).

## A3. OpenAI spend

Billing page: not read (it needs a login). Computed from the usage records in the output files and OpenAI's list prices: `https://developers.openai.com/api/docs/pricing` (the old URL `platform.openai.com/docs/pricing` redirects there), Standard tier, read 2026-11-02: gpt-4.1-mini $0.40 / $0.10 (cached) / $1.60 per 1M tokens input / cached input / output; gpt-5-mini $0.25 / $0.025 / $2.00. Method and counts in `r2-a3-openai-spend-2026-11-02.json`. HTTP-200 requests only (failed requests counted as free); gpt-5-mini completion tokens include reasoning tokens.

| | gpt-4.1-mini | gpt-5-mini | total |
|---|---|---|---|
| R1 (Parts 1 and 3, 26 priced requests) | $0.0108 | $0.0105 | $0.0213 |
| A1 (50 requests) | $0.0170 | $0.0247 | $0.0417 |
| both | $0.0278 | $0.0352 | **$0.0630** |

These are estimates from list prices; the invoice was not read. Calls that were not recorded in an output file (authentication checks against `/v1/models`) are free.

## A4. Part 4 files on disk, predictor call separated (no new model calls)

Files: `r2-a4-predictor-and-turns-2026-11-02.json` (per task and model: predictor prompt/cached/completion tokens, number of functions offered to the agent after the predictor, number of required APIs, how many of them were among those offered, whether all were, agent turns and agent tokens, failure type, and the per-call `[prompt, cached]` pairs in order, entry 0 being the predictor call) and `r2_a4_a5.py` (the script; the version that ran has sha256 `79e1f9154fe30cfa36b55d18dae1c9b7e66ad61b7d5d71cc604de10f88a1d5e8`). Source: `logs/lm_calls.jsonl` of each Part 4 task; the first call of every task was asserted to be the predictor (no tools declared) and the number of calls per task to equal the `llm_calls` of the Part 4 stats. Tokens are parsed with AppWorld's own `Tokens.from_response`, as in Part 4. Required APIs = `required_apis` of the dev ground truth (full mode, loaded outside any model run). "Offered" = the function definitions declared in the agent's first call after the predictor (this is the list the agent filters from the predictor's output; it always includes `supervisor__complete_task`).

| | MiniMaxAI/MiniMax-M3 | deepseek-ai/DeepSeek-V4.1-Flash |
|---|---|---|
| predictor calls: prompt tokens total (cached) | 437,675 (423,424) | 446,732 (437,888) |
| predictor calls: prompt tokens per task min / median / max | 7,664 / 7,672 / 7,713 | 7,822 / 7,831 / 7,872 |
| predictor calls: completion tokens total (per task median / max) | 19,344 (308 / 742) | 25,900 (388 / 2197) |
| functions offered per task min / median / max | 5 / 10 / 17 | 6 / 10 / 13 |
| required APIs per task min / median / max (total over 57) | 6 / 8 / 10 (459) | 6 / 8 / 10 (459) |
| required APIs among those offered (total over 57) | 422 | 422 |
| tasks with all required APIs offered (of 57) | 38 | 30 |
| … of those, passed | 37 | 25 |
| tasks with not all required APIs offered, passed | 13 | 23 |

The two totals of required APIs among those offered are equal (422 and 422) by sum only: per task the two models agree in 33 of 57 tasks and offered the same number of functions in 18 of 57.

**Part 4 table without the predictor calls** (agent turns only; passed counts and failure types are unchanged from Part 4):

| | MiniMaxAI/MiniMax-M3 | deepseek-ai/DeepSeek-V4.1-Flash |
|---|---|---|
| tasks passed (of 57) | 50 | 48 |
| agent LM calls total | 601 | 523 |
| agent turns per task median / mean / max | 8 / 10.54 / 49 | 8 / 9.18 / 49 |
| prompt tokens total (cached) | 13,560,768 (12,597,120) | 7,486,287 (6,576,000) |
| completion tokens total | 377,222 | 479,052 |
| prompt tokens per task median / mean / max | 69,364 / 237,908 / 3,745,656 | 68,336 / 131,338 / 1,391,558 |
| completion tokens per task median / mean / max | 4,101 / 6,618 / 45,849 | 4,297 / 8,404 / 54,985 |
| step-capped tasks (ids) | 3 (0d8a4ee_2, 383cbac_1, 383cbac_3) | 2 (df61dc5_1, 4fab96f_2) |
| step-capped tasks: share of all prompt tokens incl. predictor | 8,219,836 of 13,998,443 (58.7%) | 2,693,037 of 7,933,019 (33.9%) |
| without step-capped tasks: tasks / passed | 54 / 50 | 55 / 48 |
| without step-capped tasks: agent LM calls / prompt tokens / completion tokens | 454 / 5,364,038 / 347,286 | 425 / 4,808,915 / 392,097 |

Check: predictor + agent totals equal the Part 4 totals (MiniMax-M3 prompt 437,675 + 13,560,768 = 13,998,443 and completion 19,344 + 377,222 = 396,566; DeepSeek-V4.1-Flash prompt 446,732 + 7,486,287 = 7,933,019 and completion 25,900 + 479,052 = 504,952). Step-capped tasks are those with failure type `step_cap_reached` in Part 4; their cap of 50 steps includes the predictor step.

## A5. AppWorld agent options (0.2.0.dev0, data 0.2.0)

Read from `experiments/code/common/api_predictor.py` and `experiments/code/simplified/function_calling_agent.py` of the Part 4 clone, and counted from the loaded dev task. Counts: `r2-a5-appworld-agent-options-2026-11-02.json`.

- **Predictor modes accepted:** `ground_truth`, `predicted` (the Part 4 setting, `max_predicted_apis` 20), `all`. Any other value raises. In `ground_truth` and `all` no predictor LM call is made (usage is empty).
- **A mode that offers every API (`all`): number of definitions per turn.** `all` builds the list of every API of every app except the `api_docs` app: **469** definitions (supervisor 6, amazon 75, phone 30, file_system 26, spotify 92, venmo 54, gmail 48, splitwise 65, simple_note 17, todoist 56); `api_docs` has 4 more (473 in `api_docs.function_calling()`). **But the code cuts that list to `max_predicted_apis` in every mode** (`predicted_apis[: self.max_predicted_apis]`, with a code comment saying so), and the Part 4 configuration has `max_predicted_apis` 20. With the Part 4 settings and `mode: all` the agent would therefore be offered **20** definitions (the first 20 in app order), not 469; offering all of them needs `max_predicted_apis` set to at least 469. This is the code as read; `mode: all` was not run.
- **Not comparable with Part 3:** Part 3 counted 457 definitions (data 0.1.0: amazon 66, gmail 42, spotify 91, other apps as above, `api_docs` 4 included). Data 0.2.0 has 473 including `api_docs` (amazon 75, gmail 48, spotify 92), so the token sizes measured in Part 3 do not apply to the Part 4/Part B environment; they were not re-measured for R2.
- **Are the 3-shot demonstrations inside the prompt counted above?** For the agent's calls: yes. The agent's messages are `header + demo_messages + test_input` (`demo_messages` read from `prompts/function_calling_agent/demos.json`, the Part 4 `demo_messages_file_path`), and every agent call sends these messages, so the demonstrations are inside the per-call prompt tokens. For the predictor call: its own prompt (`prompts/api_predictor.txt`) contains three demonstrations built from the train tasks `82e2fac_1`, `29caf6f_1`, `d0b1f43_1` (each with its required APIs) after the API descriptions, so they are inside the predictor's prompt tokens (about 7.7k per task, the cached part about 7.4k).

## B1. Repeat run (MiniMaxAI/MiniMax-M3, identical settings to Part 4, predictor on)

**Released by the human on 2026-11-02; B2 is still held.** Command: `run_part4.ps1 -Model MiniMaxAI/MiniMax-M3 -Tag minimax-m3-b1` (one task at a time, all 57 dev tasks in the Part 4 order, new experiment name and a new AppWorld root for this run, so nothing is shared with the Part 4 run; issue #203 cannot apply). Same runner, agent code, configuration and environment as Part 4 (AppWorld 0.2.0.dev0, data 0.2.0, `max_steps` 50, temperature 0, seed 100, `tool_choice` auto, 3-shot demonstrations, predictor mode `predicted` with at most 20 APIs). Model id as served: `MiniMaxAI/MiniMax-M3` on all 605 LM calls of B1 (and on all 658 of Part 4); `system_fingerprint` `vllm-0.32.0-tp4-7a90bd24` on all calls of both runs. Started 2026-11-02T13:58Z (launch), first task finished 13:59Z, last 14:53Z, process exited about 14:54Z; the sum of the task durations is 3,290 s.

**Differences from the Part 4 MiniMax-M3 run, for the record:** (1) B1 ran as one process from start to end with the 300 s client timeout from the first task; no task hung, no rerun was needed or done (57 of 57 tasks have exactly one record, 0 exceptions). Part 4's tasks 1–8 ran in a first process without that timeout, and its tasks 9–57 in a second (resumed) process. (2) Nothing else was changed; ScaDS accepted `seed` and temperature 0 (no error) but whether it makes the output deterministic is exactly what this comparison measures.

**Part 4 table, both runs:**

| | Part 4 run (`minimax-m3`) | B1 run (`minimax-m3-b1`) |
|---|---|---|
| tasks run / passed (TGC) | 57 / 50 (0.8772) | 57 / 53 (0.9298) |
| scenarios all 3 passed (SGC) | 14 of 19 (0.7368) | 16 of 19 (0.8421) |
| failures by type | evaluation_failed 4, step_cap_reached 3 | step_cap_reached 2, evaluation_failed 2 |
| LM calls (incl. 1 predictor call per task) | 658 | 605 |
| prompt tokens total (cached) | 13,998,443 (13,020,544) | 13,196,358 (12,205,952) |
| completion tokens total | 396,566 | 359,557 |
| … prompt / completion tokens without the predictor calls | 13,560,768 / 377,222 | 12,758,683 / 340,043 |
| step-capped tasks (ids) | 3 (0d8a4ee_2, 383cbac_1, 383cbac_3) | 2 (383cbac_1, 383cbac_2) |
| step-capped tasks: prompt tokens (share of total) | 8,219,836 (58.7%) | 7,477,838 (56.7%) |
| **without step-capped tasks:** tasks / passed | 54 / 50 | 55 / 53 |
| … LM calls / prompt tokens / completion tokens | 508 / 5,778,607 / 365,311 | 505 / 5,718,520 / 339,443 |

**Tasks that flipped between the Part 4 run and B1** (task passed in one run and failed in the other): 5 of 57. Both passed: 49. Both failed: 3.

| task | Part 4 run | B1 run |
|---|---|---|
| `0d8a4ee_1` | failed (evaluation_failed), 7 turns | passed, 7 turns |
| `0d8a4ee_2` | failed (step_cap_reached), 49 turns | passed, 8 turns |
| `383cbac_2` | passed, 10 turns | failed (step_cap_reached), 49 turns |
| `383cbac_3` | failed (step_cap_reached), 49 turns | passed, 9 turns |
| `4fab96f_2` | failed (evaluation_failed), 7 turns | passed, 9 turns |

Passed in Part 4, failed in B1: `383cbac_2`. Failed in Part 4, passed in B1: `0d8a4ee_1`, `0d8a4ee_2`, `383cbac_3`, `4fab96f_2`. Scenarios whose all-3-passed outcome differs: `0d8a4ee`, `4fab96f`. Step-capped in both runs: `383cbac_1`.

**Paired differences, B1 minus Part 4 run** (57 tasks; per-task values are in `r2-b1-compare-with-part4-2026-11-02.json`):

- TGC: +0.0526 (+3 tasks net: 4 tasks gained, 1 lost). SGC: +0.1053.
- Total prompt tokens: -802,085 (13,196,358 against 13,998,443); total completion tokens: -37,009; total LM calls: -53.
- Per task prompt tokens: median -467, mean -14,072, min -3,637,746, max +3,636,733; B1 higher in 22 tasks, lower in 35, equal in 0. The largest differences are the tasks that hit the step cap in one run and not the other.
- Per task turns: equal in 30 of 57 tasks, B1 more turns in 8, fewer in 19. Predictor prompt tokens: identical in all 57 tasks (the predictor's prompt does not depend on the run). Number of functions offered after the predictor: equal in 20 of 57 tasks, B1 higher in 17, lower in 20 (the predictor's choice differs between the two runs in 37 tasks by count; names were not compared).

Not computed: any test or interval for these differences (one pair of runs). Files: `r2-b1-stats-minimax-m3-b1-2026-11-02.json` (per-task stats, same format as the Part 4 stats files), `r2-b1-compare-with-part4-2026-11-02.json` (flips, paired differences, per-task rows for both runs, totals with and without step-capped tasks), `r2_b1_compare.py`, `r2_pilot_compare.py` (placeholders for local paths; the version that ran has sha256 `098ffb52822f2971b247d4c23a7dcac49b922d4bfabbb3608fd660d045120012`).

## B2 (not run)

B2 (predictor off, every API offered) waits for the human's release. Note A5: `max_predicted_apis` must be raised for `mode: all` to offer every API, and the request size with all definitions has not been measured in this environment.

## B2 pilot on OpenRouter (deviation from the request; the full B2 was NOT run)

**What this is.** The full B2 (57 tasks, MiniMaxAI/MiniMax-M3 on ScaDS) could not be started: after B1 finished (about 14:54Z) the ScaDS endpoint answered HTTP 403 for `MiniMaxAI/MiniMax-M3` ("not available for this API key, or the model name is invalid") and the model was absent from `/v1/models` (26 models listed; `MiniMaxAI/MiniMax-M3.1-Flash` present). A one-task attempt ended with that error after the runner's retries; it produced no data. The human then supplied an OpenRouter key and asked for a cheaper test with fewer calls.

**Differences from B2 as requested:** (1) host: OpenRouter, model id `minimax/minimax-m3`, not the ScaDS deployment; OpenRouter routed calls to several providers (below). (2) Only 10 of the 57 dev tasks: every 6th task in dev order starting at the first (`dev[0::6]`; the rule was fixed before any outcome was read). (3) The AppWorld client's retry setting was lowered to 20 tries, 15 s apart (default 100). Unchanged: 300 s client timeout, step cap 50, temperature 0, seed 100, `tool_choice` auto, 3-shot demonstrations, AppWorld 0.2.0.dev0, data 0.2.0. No task needed a rerun.

**Runs** (each its own experiment name and AppWorld root; dev tasks only; one task at a time): `or-b2-pilot` = predictor off, mode `all`, `max_predicted_apis` raised to 1000 (the default 20 would truncate, see A5). `or-ctrl-pilot` = predictor on, as in Part 4 (control for the change of host). Runner changes: `run_part4.py` gained `--predictor-mode` and `--max-predicted-apis` (defaults reproduce Part 4); `run_part4.ps1` gained `-PredictorMode`, `-MaxPredictedApis`, `-KeyEnvVar`; `part4_stats.py` counts `turns` as all LM calls when the predictor is off (there is no predictor call then). The key was read inside the runner process and never printed.

**Table** (same 10 tasks in every row; the two ScaDS rows are the existing full runs restricted to these tasks; prompt tokens with the cached part in brackets; cost = `usage.cost` as reported by the endpoint, summed over calls; ScaDS cost was not recorded):

| run | passed | failed (failure type) | LM calls | prompt tokens (cached) | completion tokens | functions offered per agent call | cost |
|---|---|---|---|---|---|---|---|
| or_b2_pilot (`or-b2-pilot`) | 7 of 10 | `530b157_1` (evaluation_failed), `3ab5b8b_1` (evaluation_failed), `6c2c621_1` (evaluation_failed) | 130 | 11,899,694 (11,062,305) | 100,489 | 469 | $0.964 |
| or_control (`or-ctrl-pilot`) | 7 of 10 | `3ab5b8b_1` (evaluation_failed), `6c2c621_1` (evaluation_failed), `4fab96f_1` (evaluation_failed) | 110 | 1,357,750 (1,121,186) | 66,225 | 7, 8, 9, 10, 11, 13 | $0.198 |
| scads_part4 (`minimax-m3`) | 8 of 10 | `0d8a4ee_1` (evaluation_failed), `383cbac_1` (step_cap_reached) | 131 | 4,548,310 (4,294,016) | 61,701 | 6, 8, 9, 10, 11, 12, 13 | not recorded |
| scads_b1 (`minimax-m3-b1`) | 9 of 10 | `383cbac_1` (step_cap_reached) | 126 | 4,439,858 (4,168,192) | 63,049 | 7, 8, 9, 10, 11, 13 | not recorded |

**Per task** (result, LM calls, prompt tokens):

| task | B2 pilot: result, LM calls, prompt tokens | control: result, LM calls, prompt tokens | ScaDS Part 4 | ScaDS B1 |
|---|---|---|---|---|
| `50e1ac9_1` | passed, 9, 754,894 | passed, 10, 148,392 | passed | passed |
| `530b157_1` | failed (evaluation_failed), 36, 3,776,919 | passed, 16, 141,775 | passed | passed |
| `b119b1f_1` | passed, 9, 701,206 | passed, 10, 63,615 | passed | passed |
| `0d8a4ee_1` | passed, 8, 642,651 | passed, 12, 225,068 | failed (evaluation_failed) | passed |
| `3ab5b8b_1` | failed (evaluation_failed), 11, 926,416 | failed (evaluation_failed), 10, 105,145 | passed | passed |
| `383cbac_1` | passed, 9, 784,548 | passed, 9, 99,706 | failed (step_cap_reached) | failed (step_cap_reached) |
| `57c3486_1` | passed, 20, 1,947,878 | passed, 16, 266,932 | passed | passed |
| `6bdbc26_1` | passed, 5, 380,654 | passed, 6, 31,402 | passed | passed |
| `6c2c621_1` | failed (evaluation_failed), 16, 1,432,481 | failed (evaluation_failed), 14, 224,333 | passed | passed |
| `4fab96f_1` | passed, 7, 552,047 | failed (evaluation_failed), 7, 51,382 | passed | passed |

**Observations (counts; no inference drawn).**
- The request with all 469 function definitions was accepted on every call (469 definitions on each of the 130 agent calls of the pilot; no size error). The pilot averaged 91,536 prompt tokens per call; the control averaged 12,343 (its calls include the predictor calls).
- Pilot against control: 7 and 7 of 10 tasks passed. The counts are equal but the sets differ: failed only in the pilot: `530b157_1`; failed only in the control: `4fab96f_1`; failed in both: `3ab5b8b_1`, `6c2c621_1`. No task hit the step cap in either OpenRouter run (in both ScaDS runs `383cbac_1` did).
- Total prompt tokens: pilot 11,899,694 against control 1,357,750 (8.8 times). Reported cost: $0.96 against $0.20 (4.9 times), because 93% of the pilot's prompt tokens were served from cache (control: 83%). `530b157_1` alone took 36 LM calls in the pilot against 16 in the control.
- Providers (calls): `or-b2-pilot`: Minimax 45, GMICloud 40, Novita 25, StreamLake 20 (one task spans more than one provider). `or-ctrl-pilot`: GMICloud 34, Novita 25, Minimax 24, StreamLake 17, CoreWeave 10 (all 10 tasks span more than one provider, because the predictor call and the agent calls were routed separately). The served model id was `minimax/minimax-m3` on every call; `system_fingerprint` is absent. Whether the providers differ in precision, chat template or tool handling is not recorded.
- The OpenRouter control (7 of 10) and the ScaDS runs (8 and 9 of 10, same tasks) differ by 1-2 tasks; B1 flipped 5 of 57 tasks between two identical ScaDS runs. With 10 tasks and no repeat, none of the differences above can be told apart from run-to-run variation.

**Not done.** The full 57-task B2 on ScaDS; a repeat of either OpenRouter run; any test or interval. Files: `r2-pilot-openrouter-2026-11-02.json` (per-task rows for all four runs), `r2_pilot_compare.py` (local paths replaced by placeholders; the version that ran has sha256 `f6daa7dcd991c4bdc128a95a02753fe6aff7f741b213db1a3f85924b02ccf0b2`).

## Files in this folder

`RESULTS-R2.md` (this file); `A1_summary_tables.md`; `r2-scads-2026-11-02.json`, `r2-openai-2026-11-02.json` (merged A1 output) and `raw/` (the per-model files they were merged from); `r2-a3-openai-spend-2026-11-02.json`; `r2-a4-predictor-and-turns-2026-11-02.json`; `r2-a5-appworld-agent-options-2026-11-02.json`; `r2-b1-stats-minimax-m3-b1-2026-11-02.json`, `r2-b1-compare-with-part4-2026-11-02.json`; `r2-pilot-openrouter-2026-11-02.json`; scripts `run_r2_a1.ps1`, `merge_r2_a1.py`, `r2_a4_a5.py`, `r2_b1_compare.py` (local paths replaced by placeholders). Hard rules kept: keys only as environment variables of the running process; leak check on every output file (ScaDS key present: False; OpenAI key present: False); a scan of this folder for local paths found none; no AppWorld definitions, tasks, solutions or model messages about tasks are in it.
