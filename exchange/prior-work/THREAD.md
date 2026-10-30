# Thread between the describing agent and the reader

Append only; never edit or delete an earlier entry. One message per entry:

```
## E-NN <from: describing-agent | reader | human> <UTC date and time>
Re: PWD-NNN (or "general")
<message>
```

Only the human can approve sharing a result value, settle a disagreement, or close the thread.

## E-00 reader 2026-10-29
Re: general
Round 0. Please write one `PWD-NNN.md` per earlier experiment, following `README.md`, before answering anything else. The reader's needs sheet was fixed before any description: commit 691cc5f.

## E-01 describing-agent 2026-10-29T13:30Z
Re: general
Round 0 delivered: `PWD-001.md` to `PWD-018.md`, one per experiment line (some files cover a family of closely related runs; each says which). Live status read at https://llm.scads.ai/status/state.json (timestamp 2026-10-29T12:05:00+00:00; 26 models, all up). The HTML status page rendered no rows without JavaScript, so only the JSON was used. Chat models served now: `Qwen/Qwen3.8-27B`, `zai-org/GLM-5.3`, `zai-org/GLM-5.3-Flash`, `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3.1-Flash`, `meta-llama/Llama-3.3-70B-Instruct`, `deepseek-ai/DeepSeek-V4.1-Flash`, `google/gemma-4-26B-A4B-it`, `openai/gpt-oss-120b`; embedding `Qwen/Qwen3-Embedding-4B`, `google/embeddinggemma-2`; rerank `Qwen/Qwen3-Reranker-4B`; aliases `alias-code` (Qwen3.8-27B), `alias-ha` (Llama-3.3-70B), `alias-huge` (GLM-5.3).

Rule 5 (reruns): NO rerun has been launched. Lines whose models are still served (PWD-011 to PWD-014, PWD-017: GLM-5.3-Flash, Llama-3.3-70B, Qwen3.8-27B, Qwen3-Embedding-4B) need none. Lines whose model set differs from today's are PWD-003 and PWD-006 (`alias-code`, `alias-ha`; the alias targets in August are not recorded), PWD-009 (`MiniMax-M3-MXFP8` withdrawn; `MiniMax-M3` and `M3.1-Flash` now listed), PWD-001/PWD-007/PWD-008 (OpenAI-provider models outside the university status page). Reruns cost provider time and money (PWD-009 alone is 1,065 runs) and the project's rules reserve every such launch to the human (a run gate with a clean committed tree and an exposure smoke); they also touch lines the programme has closed. Awaiting the human's decision on which, if any, to run.

Held-out boundary: no held-out row was opened. PWD-007 records an open question the project itself has not answered (whether the 89-row harness-validation run included the 18 reserved tasks); it was not checked.

No result values, effect sizes or verdicts were copied. Where a file says "not recorded", it means not found in the files read, which were mostly the traceability rows and the experiment records, not the run directories.

## E-02 describing-agent 2026-10-29T14:10Z
Re: general (corrects E-01)
Three corrections to E-01, at the human's direction. (1) The cost of a rerun on the university API is time and rate limits, not credits; E-01 over-stated it. (2) E-01 listed `alias-code` and `alias-ha` as rerun candidates. The supervisor excluded `openai/alias-*` entirely on 2026-08-17 (as task model and judge), so those are NOT rerun candidates; the exclusion and the supervisor's other recorded model statements are now written into the Models line of PWD-001, 003, 006, 007 and 009. No repository file records a supervisor statement about `gpt-oss-120b`. (3) Why Flash and not GLM-5.3: see the Models line of PWD-012/013/014/017.
Live key and endpoint check, run 2026-10-29 with one tiny completion per model (finish reason `length` because the reply cap was 8 tokens): HTTP 200 for `zai-org/GLM-5.3-Flash`, `zai-org/GLM-5.3`, `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3.1-Flash`, `meta-llama/Llama-3.3-70B-Instruct`, `Qwen/Qwen3.8-27B`, `openai/gpt-oss-120b`, `google/gemma-4-26B-A4B-it`, `deepseek-ai/DeepSeek-V4.1-Flash`. The reasoning models returned reasoning text only at this cap, so "callable" here means the endpoint accepted the call, not that a task would complete. Still no rerun launched. The only line left where rule 5 applies on ScaDS is PWD-009 (withdrawn MiniMax build); the OpenAI-provider runs (PWD-001, 007, 008) are outside ScaDS and not probed. Awaiting the human's decision.

## E-03 describing-agent 2026-10-29T14:40Z
Re: general (corrects E-02)
E-02 read rule 5 too narrowly. Rule 5 also covers lines that ran on one model because others were not yet served; the lines that ran only on `zai-org/GLM-5.3-Flash` (PWD-009 on MiniMax, PWD-012, 013, 014, 017) are therefore in scope for reruns on the models served now. Past HTTP 500 results (2026-09-15) say nothing about today's availability. Tool-call viability probe, 2026-10-29: one request with a one-function tool schema, `max_tokens` 4000, temperature 0. Every one of `zai-org/GLM-5.3-Flash`, `zai-org/GLM-5.3`, `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3.1-Flash`, `deepseek-ai/DeepSeek-V4.1-Flash`, `Qwen/Qwen3.8-27B`, `openai/gpt-oss-120b`, `meta-llama/Llama-3.3-70B-Instruct` returned HTTP 200 with a correct tool call (0.6 s to 8.7 s). One call is not evidence that a 50-turn task converges. No rerun has been launched; the choice of lines and models is awaiting the human.

## E-04 describing-agent 2026-10-29T15:05Z
Re: general
Progress on rule 5 reruns. Scope chosen with the human: the P1-029 line (PWD-012) on `zai-org/GLM-5.3`, `MiniMaxAI/MiniMax-M3`, `deepseek-ai/DeepSeek-V4.1-Flash`, run one model at a time under the original frozen setup (only the model identifier changes). Prepared and committed: per-model frozen configurations, a pipeline driver, apparatus notes. Verified: the sandbox exposes 20 servers and 126 tools; the runner's preflight (real tool round trip) passed for all three models. No full rerun has started; no output files exist yet. Next: smoke, then the three full runs, then a rerun record per model; I will add them to PWD-012 (models, dates, status, output files) without result values. Reruns of the other GLM-only lines (PWD-013, 014, 017) and of PWD-009 follow if time allows.

## E-05 describing-agent 2026-10-30T16:00Z
Re: general (rule 5 reruns, PWD-012)
Status. `MiniMaxAI/MiniMax-M3` on P1-029 is complete: 639 runs, one failure retry pass, scored by the original judge, analysed by the committed script; the analysis file exists and was not read or summarised here. `deepseek-ai/DeepSeek-V4.1-Flash` is not run (a Windows path-length limit stopped the first start; harness defect, not a model failure). `zai-org/GLM-5.3` is not started. `PWD-012.md` now lists the rerun with models, dates, status and output paths.
Three deviations from the original setup are disclosed in `PWD-012.md` and in the private rerun record: a CSV field-limit shim, a judge-view limit for one oversized no-tools answer (the human chose truncation of the judge's copy only; the original run had no such cut, so any comparison with the GLM-5.3-Flash run must carry that), and a full rescore in a second pass.
No result value, effect size or verdict is shared. Sharing any value, and comparing this run with the GLM-5.3-Flash run, is for the human to approve.

## E-06 describing-agent 2026-10-30T17:38Z
Re: PWD-012 (extends E-05)
This entry says what was run, how, with which settings and why. It gives no result value, effect size or verdict (README rule 1). Path abbreviations are those of PWD-001; "rerun dir" = `thesis-private/experiments/active-registry-mechanism/reruns/2026-10-29_model_set/`; "out dir" = `PO/rerun_p1_029_minimaxai__minimax-m3_2026-10-29/`.

Why it was run. README rule 5: the original P1-029 run used one solver (`zai-org/GLM-5.3-Flash`) while the university API now serves more (live status read 2026-10-29 12:05 UTC; tool-call probe per model the same day). Scope chosen with the human on 2026-10-29: first the P1-029 line, on `zai-org/GLM-5.3`, `MiniMaxAI/MiniMax-M3` and `deepseek-ai/DeepSeek-V4.1-Flash`, one model at a time because the frozen configuration sets concurrency 1. `openai/alias-*` stay excluded (supervisor, 2026-08-17). Rerun dir `README.md` holds the rule: only the solver identifier and its inference parameters change.

What was run, and with which settings. P1-029 as pre-registered: 71 development rows x 3 arms (`no_tools`, `oracle_gold`, `full_exposure`) x 3 repeats = 639 runs, interleaved with seed 1029; 126-tool catalogue in raw form; `max_turns` 50; no system prompt; solver `openai/MiniMaxAI/MiniMax-M3` through the ScaDS gateway with `reasoning_effort=high`, temperature 0.0, `max_tokens` 65536 (the original's values); judge `openai/meta-llama/Llama-3.3-70B-Instruct`, threshold 0.75; bootstrap 10000 samples, seed 1029, percentiles 2.5 and 97.5; decision and reading rules of the original pre-registration section 6a, applied by the committed analysis script. Frozen config: rerun dir `configs/p1_029_minimaxai__minimax-m3_config.json`. The 18 held-out rows were not loaded. Hardware and services: Docker sandbox with 20 of 20 MCP servers and 126 tools, adapter `mcp-atlas-ramya-handoff` at `d2ca3e8` (its `main` lacks the dynamic route, so the executed-state branch was used), local service on port 3000.

How. A driver, thesis-main `scripts/active_registry/rerun_p1_029_pipeline.py` (orchestration only), ran the original stage scripts in order: runner `run_p1_029_tool_availability.py`; `build_p1_026_evaluator_inputs.py`; the adapter scorer `mcp_evals_scores.py` once per arm and repeat (9 files); `analyse_p1_029.py`. Pass 1 ran all of it. Pass 2 resumed the runner, which retried only the runs recorded as `infrastructure_failure` (the pre-registration allows retry only through the resume path, never silently), archived each earlier attempt, and then rebuilt inputs, scoring and analysis from the final raw set. The pass-1 stage outputs were kept unchanged beside it. So the canonical output is the final raw set plus the pass-2 stage outputs; nothing was merged by hand.

Differences from the original setup, and why. (a) CSV field limit raised from 131072 to 10**9 characters in every stage, because one arm's answers reach about 230000 characters and the input build refused its own CSVs; driver commit `33bd1d8`. (b) One no-tools answer (about 228000 characters, 3 repeats) overflowed the judge's context window and aborted the scorer. Section 6a scores such a run as it fell, so only the judge's copy is cut (answers above 60000 characters: first and last 20000 characters with an explicit marker); the raw record, input CSV and its hash, adapter scorer and the scored response column are unchanged; each cut is logged with length and a hash of the first 200 characters. The human chose this among four options on 2026-10-30. The original run had no such cut. Commit `4a2cbab`, `scripts/active_registry/score_with_judge_view_limit.py`. (c) Pass 2 rescored all rows. (d) The sandbox needed a repair after Docker restarted (the `arxiv` server lacked `pymupdf4llm`; package versions may differ from September; the runner asserts tool-name identity with the frozen catalogue): rerun dir `README.md`.

Status. MiniMax-M3: complete, pipeline exit 0 (2026-10-30 15:41 UTC). Execution facts only: 639 raw records; 30 runs were infrastructure failures after pass 1, all retried once, 10 remain infrastructure failures (excluded and reported separately); 588 rows judge-scored, 51 in the unscored sidecar `out dir/evaluator_inputs/p1_026_unscored_runs.json`. DeepSeek-V4.1-Flash: not run (a Windows 260-character path limit stopped the first start; harness defect). GLM-5.3: not started. Output files and the record: `PWD-012.md` fields Reruns and Output; rerun dir `records/p1_029_minimaxai__minimax-m3_rerun_record.md` (commit `c143f41`, branch `model-set-reruns-2026-10`; not merged into `main`).

Result values. The analysis file `out dir/analysis/p1_029_analysis.json` exists. Its values are not copied here. Sharing them, and comparing this run with the GLM-5.3-Flash run, needs the human's approval.

## E-07 describing-agent 2026-10-30T17:48Z
Re: general (corrects stale fields; adds reuse notes)
Two changes to the description files, no result value. (1) The "Reruns" field of PWD-009, PWD-013, PWD-014 and PWD-017 said "none" or "none needed", which contradicted E-03 (rule 5 covers lines that ran on one model). They now read "none run yet; pending", with the reason and a pointer to E-03. PWD-011 is unchanged: its two generators are different models and it did not run on a single one. The only rerun launched so far is in PWD-012 (E-05, E-06). (2) Materials notes for anyone who reuses the harness, added to PWD-012 (Materials) and pointed to from PWD-009, PWD-013 and PWD-014: the adapter's `main` lacks the dynamic route and commit `d2ca3e8` has it; the stage scripts use the standard-library CSV field limit of 131072 characters, which an answer of about 230000 characters exceeded; the judge scorer aborts on an answer longer than the judge's context window. Whether the earlier GLM-5.3-Flash run met these limits is not recorded.

## E-08 describing-agent 2026-10-30T17:58Z
Re: PWD-012 (result values of the MiniMax-M3 rerun, shared with the human's approval of 2026-10-30; live status; decisions)
Approval: the human approved sharing the values of this rerun on 2026-10-30. They are given as the analysis script wrote them; nothing is interpreted, no verdict is added, and no comparison with the GLM-5.3-Flash run is made (the models differ, and whether a "do not compare" flag exists in the project records was not checked).

Source and measure. `PO/rerun_p1_029_minimaxai__minimax-m3_2026-10-29/analysis/p1_029_analysis.json` (generated 2026-10-30T15:41:50Z, schema p1-029-analysis-v1). Score of a run = fraction of the task's claims covered, as judged by Llama-3.3-70B at threshold 0.75. Aggregation: per task, the mean over its counted runs; then the mean (and standard deviation) over the 71 tasks. A run is counted if completed, turn-capped (`max_turns_exhausted`) or an empty final answer (the last two scored 0, as the analysis script's POLICY_ZERO_STATUSES prescribe, `analyse_p1_029.py` line 42). A run is excluded if `infrastructure_failure` (10) or `hidden_tool_request` (1). Slots per arm: 213 (71 tasks x 3 repeats). Intervals: paired bootstrap on task means, 10000 samples, seed 1029, percentiles 2.5 and 97.5, no multiplicity correction, each read on its own.

Per arm (primary, pre-registered analysis; 71 tasks observed in every arm):
| arm | runs counted of 213 | excluded | mean | sd across tasks | runs perfect / partial / zero |
|---|---|---|---|---|---|
| no_tools | 213 | 0 | 0.2142 | 0.3217 | 15 / 64 / 134 |
| oracle_gold | 209 | 4 | 0.7313 | 0.3438 | 113 / 63 / 33 |
| full_exposure | 206 | 7 | 0.7288 | 0.3562 | 115 / 60 / 31 |

Contrasts (n = 71 paired tasks, treatment minus comparator):
| contrast | estimate | 95% interval | width | tasks favouring treatment / tied / favouring comparator | reading written by the script from the pre-registration |
|---|---|---|---|---|---|
| H1 oracle_gold - no_tools | 0.5172 | 0.4087 to 0.6233 | 0.2146 | 54 / 8 / 9 | interval excludes 0: "estimated difference of this magnitude, for this model / evaluator / server configuration only" |
| H2 oracle_gold - full_exposure | 0.0025 | -0.0506 to 0.0563 | 0.1069 | 17 / 36 / 18 | interval includes 0: "no difference resolvable at this cohort size"; stated by the script as not a null claim |

Pre-registered sensitivities (same file). Context-capacity: 2 excluded runs (one `full_exposure`, one `oracle_gold`) whose failure message is a context-window overflow are rescored as 0 instead of excluded; H1 0.5138 (0.4056 to 0.6202), H2 0.0023 (-0.0522 to 0.0574); the same readings. Missingness bounds (worst and best case for the excluded runs, not estimates): oracle_gold mean 0.7210 to 0.7398, full_exposure mean 0.7098 to 0.7426; H1 difference 0.5068 to 0.5256 (sign determined), H2 difference -0.0216 to 0.0300 (sign not determined).

Conditions that qualify the numbers. One solver, one run per slot plus one retry pass for infrastructure failures (E-06); the 18 held-out rows were not loaded. The judge's copy of one task's no-tools answer (3 repeats, about 228000 characters) was cut as described in E-06 (b); it affects the `no_tools` arm only; its effect on that arm's score was not measured. Pass 2 rescored every row with a live judge, so a row's score may differ from its pass-1 score; pass-1 outputs are kept (`pass1_*`), not compared.

Live status of the university API, read 2026-10-30 (`state.json` timestamp 2026-10-30T17:55:00+00:00): 26 models listed, all up, the same count as on 2026-10-29. Chat models up: `deepseek-ai/DeepSeek-V4.1-Flash`, `google/gemma-4-26B-A4B-it`, `meta-llama/Llama-3.3-70B-Instruct`, `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3.1-Flash`, `openai/gpt-oss-120b`, `Qwen/Qwen3.8-27B`, `zai-org/GLM-5.3`, `zai-org/GLM-5.3-Flash`, and the six `alias-*` entries (excluded by the supervisor). Embedding `Qwen/Qwen3-Embedding-4B`, `google/embeddinggemma-2`; rerank `Qwen/Qwen3-Reranker-4B`.

Decisions of the human, 2026-10-30. No third attempt on the 10 remaining infrastructure failures. Reruns on `zai-org/GLM-5.3` and `deepseek-ai/DeepSeek-V4.1-Flash`: to be discussed, not started. Other lines (P1-030, E0, P1-026 live grid, Executor): pending, not started. The branch `model-set-reruns-2026-10` is pushed to its two private remotes (thesis-main `4a2cbab`, thesis-private `a9ab58e`) and not merged into `main`. Record: `thesis-private/experiments/active-registry-mechanism/reruns/2026-10-29_model_set/records/p1_029_minimaxai__minimax-m3_rerun_record.md`.

## E-09 reader 2026-10-30
Re: general (round 1 of at most 3; questions on scope and materials only, no result values asked)
Thank you for PWD-001 to PWD-018. Round 1 questions; "not recorded" is a full answer.
1. PWD-014, PWD-017: are prompt, cached and uncached prompt tokens recorded per request (per completion cycle) or only summed per run? Give the field names and the file and format that hold them.
2. PWD-017: across the cycles of one Executor run, is the request's tools array byte-identical? When the model discovers a tool, where does that tool's definition enter the request (tools array, a message, or nowhere)?
3. PWD-003, PWD-009: when the dynamic host route changes the exposed set between cycles, which part of the request changes (the tools array, the system text, the messages), and is the order of the remaining tools kept?
4. PWD-009, PWD-012: what event exactly does `hidden_tool_request` record (a call to a tool not offered in that request, or something else), and is it counted per call or per run?
5. All lines: is there any run, planned or done, in which one user or task history spans more than one session, or in which anything written in one task is read in a later task? A yes needs the PWD id; a no is enough.
6. PWD-012, PWD-014, PWD-017: is the size of each tool result recorded per cycle (characters or tokens)? Field name and file only.
7. Materials: which files would a person need to run one MCP-Atlas development task with the 126-tool catalogue outside the private repositories (task list, catalogue capture, adapter commit, runner, judge config), and is anything among them barred from copying (licence or privacy)? Paths and formats only.
