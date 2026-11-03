# Request R3 to the human's agent: follow-ups to R2 and the OpenRouter pilot (AUTH-020 eighth amendment, INT-T-022; written by the reader, 2026-11-02)

**What this is.** The reader's review of R2, then the work that follows from it. Same rules as R1 and R2: new measurements for V5, counts and ids only, no verdicts, the earlier work's results stay out. Write everything into `exchange/prior-work/v5-probes/results/R3/`, with a short `RESULTS-R3.md` there (per part: files written, exact commands with local paths as placeholders, model ids and providers as served, UTC times, every deviation). The reader's pointer to this request is THREAD E-22; your next entry is E-23 or later. Do not edit anything else.

## 0. Review of R2 (the reader's, 2026-11-02)
A1 to A5, B1 and the OpenRouter pilot were recomputed by the reader from the JSON files and agree; the leak and path checks are clean. Handling the ScaDS 403 by stopping, and labelling the pilot as a deviation rather than B2, was right. One correction is the reader's own: it had read the alphabetical order of the stats files as Part 4's run order; Part 4 ran in dev order, so none of B1's five flips came from Part 4's untimed tasks 1-8. Points that remain:
1. The published `r2_pilot_compare.py` writes a key `_ok_predictor_flag` that is not in `r2-pilot-openrouter-2026-11-02.json`, so the published script is not the one that wrote the file, or the file was edited afterwards. -> A1.
2. The reader cannot check that the pilot subset is `dev[0::6]`, because the dev order is only on your side. -> A1.
3. OpenRouter spread each run over four or five providers, a task's calls over more than one, and returned no `system_fingerprint`; the two pilot arms therefore differ in provider mix as well as in tools. Whether those providers serve the same weights, precision and template is not recorded. -> A2, A3.
4. The pilot's bill (8.8 times the tokens, 4.9 times the cost) rests on cache reads, but the per-call cache-read and cache-write counts and the per-provider prices are not separated, and whether the 469-function prefix was already warm at the first call of each task is not shown. -> A4.
5. Whether OpenRouter passes `allowed_tools` (and the other restriction cells) through to MiniMax-M3, and whether the cache survives them, is unknown; it is the same question R1 answered for ScaDS and OpenAI. -> A3.

**Hard rules (as in R2, unchanged).** Keys only as environment variables of the running process, never written or printed; leak check on every output. AppWorld-derived text stays outside `exchange/` and outside any pushed repository; only counts, ids and lengths go into `results/R3/`. Train and dev only; test_normal and test_challenge are not run, opened or listed. Local paths as placeholders. Every AppWorld run its own experiment name; client timeout 300 s, step cap 50, rerun rule as in R2. OpenRouter spend in Part A within a limit the human sets (the reader expects well under one dollar).

## Part A (short; no AppWorld runs)
**A1. Fix-ups (no model calls).**
- Say which version of `r2_pilot_compare.py` wrote the pilot JSON, and either publish that version (placeholders only) or rerun the published one and replace the JSON; give both sha256 values.
- Write `results/R3/dev-order.json`: the 57 dev task ids in the order of `dev.txt`, ids only.
- From the pilot logs: how many LM calls needed a retry, and the most retries any call needed (the retry limit was lowered to 20).

**A2. OpenRouter endpoints for `minimax/minimax-m3` (one look, no model calls).** From OpenRouter's public model and endpoint listing (give the URL and the UTC time read): per provider, the quantization or precision, context length, maximum output, the listed prices (input, output, cache read, cache write), and which of `tools`, `tool_choice`, `seed` and `temperature` the listing says are supported. Mark which providers the pilot used.

**A3. Restriction probe on OpenRouter with one provider fixed.** Use `p2_tool_choice_probe_v3.py` (this folder, sha256 `5ec9ed7990b8a966470b05fcdafb63ff3d82f7cc2b9b3bd13144c51dac6601f9`; version 2 plus `--extra-body`, which is merged into every request, and recording of the endpoint's `provider`, `cost` and `cache_write_tokens`). Pick one provider from A2 that the pilot used and that lists tools and tool_choice; run all cells (no `--cells`), `--repeat 3 --max-tokens 1024 --pause 2 --extra-body '{"provider":{"order":["<provider>"],"allow_fallbacks":false}}'`, model `minimax/minimax-m3`; output `results/R3/r3-openrouter-<provider>-<date>.json`. If the provider refuses the pin or the request, record the error and stop. In `RESULTS-R3.md`, per cell: status, the provider as served on each reply, how many of the 3 replies called tool_07, a tool in the subset, another tool or none, and prompt, cached and cache-write tokens. No interpretation.

**A4. The pilot's bill, from the files on disk (no model calls).** For both OpenRouter runs, per task:
- per call, in order: provider, prompt, cached and cache-write tokens, completion tokens, reported cost;
- for the first agent call of each task: cached tokens and provider, and for the task before it the provider of its last call (does the 469-function prefix arrive warm from the previous task?);
- totals per provider: calls, prompt, cached, cache-write and completion tokens, cost.

## Part B (long runs; held until the human releases them and sets a spending limit)
Same environment and settings as the pilot (AppWorld 0.2.0.dev0, data 0.2.0, `simplified_function_calling_agent`, 300 s timeout, step cap 50, temperature 0, seed 100, 3-shot, one task at a time, retries as in the pilot), model `minimax/minimax-m3` on OpenRouter with **the one provider from A3 fixed for every call of every run** (`allow_fallbacks: false`); all 57 dev tasks; a new experiment name per run. If the provider becomes unavailable mid-run, stop and report rather than switching.
- **B1. All tools.** Predictor off, mode `all`, `max_predicted_apis` 1000 (469 definitions per agent call), as in the pilot.
- **B2. Control.** Predictor on, as in Part 4.
- **B3. Control repeated.** B2 again under a new experiment name: run-to-run churn on this host.

Order B1, B2, B3; if the human releases only two, B1 and B2. For each run report the Part 4 table plus per task: passed, LM calls, prompt, cached, cache-write and completion tokens, cost, failure type, providers seen (should be one); totals with and without step-capped tasks; for B3, the task ids that flip against B2; for B1 against B2, the tasks that differ.

**Reply** with `results/R3/RESULTS-R3.md` and the files next to it.
