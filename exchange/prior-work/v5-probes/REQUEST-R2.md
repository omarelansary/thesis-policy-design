# Request R2 to the human's agent: follow-ups to R1 (AUTH-020 eighth amendment, INT-T-022; written by the reader, 2026-11-02)

**What this is.** The reader's review of R1, then new work that follows from it. As in R1: new measurements for V5, not descriptions of earlier work; report what was run and what came back, no verdicts; the earlier work's results stay out. Organise the work as you see fit. Write everything into `exchange/prior-work/v5-probes/results/R2/`, with a short `RESULTS-R2.md` there (per part: files written, exact commands with local paths as placeholders, model ids as served, UTC times, every deviation). You may add a THREAD entry as before. Do not edit anything else.

## 0. Review of R1 (the reader's, 2026-11-01 and 2026-11-02)
Every table in `RESULTS-R1.md` was recomputed by the reader from the JSON files and agrees. The responses to the five review comments were checked: the three probe hashes match, no local path or folder name is left in `results/`, pip freezes are recorded, the canary field is absent. Thank you. Points that remain, and that the parts below address:
1. Part 1 has one sample per cell, and the script recorded neither the reply text nor the model snapshot, so the nine ScaDS models with no call in C9 (`/responses`) cannot be read (the reader's script's fault). -> Part A1.
2. The LiteLLM version of the ScaDS proxy is not known. -> Part A1 (response headers).
3. The OpenAI spend was not recorded. -> Part A3.
4. Part 4 mixes AppWorld's "API predictor" call (at most 20 APIs per task) with the agent's turns, so the cost and the recall of AppWorld's own tool selection are not separable, and the score is the score *with* that selection, not with all tools declared. -> Parts A4, A5 and B2.
5. One run per model, two runs that were interrupted and resumed, temperature 0 and seed untested: run-to-run variation (how many tasks flip between two identical runs) is unknown, and it sets the smallest difference any later comparison can detect. -> Part B1.
6. Step-cap failures carried 59% (MiniMax-M3) and 34% (DeepSeek-V4.1-Flash) of the prompt tokens. Keep the cap at 50 in every run and report bills with and without capped tasks. -> Parts B1, B2.
7. Parts 2 and 4 used different AppWorld versions (0.1.3.post1 with data 0.1.0; main `42b5bcf3` with data 0.2.0). Use the Part 4 environment, unchanged, for everything in R2.

**Hard rules (as in R1, plus two).** Keys only as environment variables, never written or printed; leak check on every output. AppWorld-derived text (definitions, tasks, solutions, tool outputs, model messages about tasks) stays outside `exchange/` and outside any pushed repository; only counts, ids and lengths go into `results/R2/`. Train and dev only; test_normal and test_challenge are not run, opened or listed. Local paths in published files as placeholders. **New:** every AppWorld run uses its own experiment name (open issue #203: state does not reset when a task id and experiment name are reused). **New:** fix before starting, and report: the client timeout (300 s from the first task), the step cap (50), and the rerun rule (a task whose process hangs is rerun once from scratch, logged with the reason; no other reruns).

## Part A (short; no long runs; within the spending limit the human set for R1)
**A1. Repeats with a probe that records more.** Use `p2_tool_choice_probe_v2.py` (this folder; same prompt, tools and cells as version 1; adds `--repeat`, `--cells`, `--token-param`, and records the served model id, `system_fingerprint`, `x-litellm-*` response headers, reply text length and first 160 characters, and `/responses` output item types). Run `--cells C2 C4 C6 C8 C9 --repeat 5 --max-tokens 1024`:
- on the nine ScaDS tool models (no alias), `--pause 15`; output `results/R2/r2-scads-<date>.json`;
- on `gpt-4.1-mini` and `gpt-5-mini` (`--token-param max_completion_tokens` for gpt-5-mini, so no copy is needed), `--pause 2`; output `results/R2/r2-openai-<date>.json`.

In `RESULTS-R2.md` give per model and cell the number of the 5 replies that called the requested tool_07, a tool in the subset, another tool, or no tool, and the `x-litellm-version` header if present. No interpretation.

**A2.** If ScaDS's status page or docs show the LiteLLM version, or the proxy's handling of `allowed_tools` on `/responses`, give the URL and the line. One look only; no wider search.

**A3. Spend.** The OpenAI cost of R1 and of A1, from the billing page (with date and time read) or, if not available, from the usage records and OpenAI's list prices (give the price page URL and the date read).

**A4. From the Part 4 files already on disk (no new model calls),** per task and model, counts only:
- the predictor call's prompt, cached and completion tokens, separately from the agent's turns;
- the number of APIs the predictor picked;
- how many of the task's required APIs (from the dev ground truth, `required_apis` or the APIs in the reference solution's calls) were among them, and whether all were;
- the per-call sequence of prompt and cached tokens (one pair per call, in order).

Then the same totals as the Part 4 table, without the predictor calls.

**A5. AppWorld agent options (names and counts only):**
- the API predictor modes the 0.2.0.dev0 configuration accepts;
- for a mode that offers every API of every app, how many function definitions the agent would send per turn;
- whether the 3-shot demonstrations are inside the prompt counted above.

## Part B (long runs; held until the human releases them, as Part 4 was)
Same environment, model `MiniMaxAI/MiniMax-M3`, dev 57 tasks, `simplified_function_calling_agent` with the Part 4 settings except as stated, one task at a time, new experiment name per run, the fixed timeout, cap and rerun rule above. Keep the per-call usage records (counts only).
- **B1. Repeat run.** Identical settings to Part 4 (predictor on). It gives run-to-run churn: tasks that flip between the two runs, and the paired difference of TGC and of tokens between them.
- **B2. All tools.** Predictor off, every API of every app offered (the mode from A5). If the request is too large for the model, record the error and stop. This is AppWorld's agent with all tools declared, a baseline, not a V5 arm.

For each run, report the Part 4 table plus:
- per task: passed, turns, prompt, cached and completion tokens, failure type;
- the totals with and without step-capped tasks;
- for B1, the list of task ids that flipped relative to Part 4's MiniMax-M3 run.

**Order and stopping.** A1-A5 first. B1 before B2. If the human releases only one, B1 is the one the reader needs most: without it no later difference can be told apart from noise.

**Reply** with `results/R2/RESULTS-R2.md` and the files next to it.
