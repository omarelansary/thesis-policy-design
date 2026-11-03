# Request R1 to the human's agent: V5 measurements (AUTH-020 eighth amendment, INT-T-022; written by the reader, 2026-11-01)

**What this is.** New measurements for the V5 design, not descriptions of earlier work. The rules of `../README.md` about not concluding still apply (report what was run and what came back; no verdicts), and the earlier work's results stay out. You hold the OpenAI and ScaDS keys; the reader never sees them. Organise the work as you see fit (several agents allowed). Write everything into `exchange/prior-work/v5-probes/results/`. Put a short `RESULTS-R1.md` there that lists, per part, the files written, the exact commands, model identifiers as served, dates and times (UTC), and every deviation from this request.

**Hard rules.**
- Keys are only ever environment variables; never write or print them.
- AppWorld asks that its data is not posted in plain text. Keep AppWorld-derived text (definitions, tasks, solutions, tool outputs) **outside** `exchange/prior-work/` and outside any repository that is pushed. Only counts and statistics go into `results/`.
- Use AppWorld's **train and dev** splits only. test_normal and test_challenge are the confirmatory reserve and must not be run or opened.
- Check the live model status (https://llm.scads.ai/status/) and use the tool-calling models served now.

## Part 1. Why is `allowed_tools` rejected? (the human's question: the model, the request naming, or the API?)
Run `p2_tool_choice_probe.py` (in this folder; standard library only):
- **ScaDS:** every chat model with tool support that is served now (`--pause 35` if a model rate-limits). Output: `results/r1-scads-<date>.json`.
- **OpenAI:** one or two current paid models with tool calling (for example `gpt-5-mini`; your choice, model ids recorded). Output: `results/r1-openai-<date>.json`.
- If ScaDS documents another way to restrict tools (its docs, its `/v1/models` metadata, or a LiteLLM setting), note where you saw it. Do not change the script's cells. Add cells only in a separate copy, and say so.

## Part 2. AppWorld inspection (statistics only)
Install AppWorld in an isolated environment on your side (`pip install appworld`, `appworld download data`) and record its version and the data version. Then report, as JSON plus a short summary:
1. **Definitions:** per app, the number of APIs in the function-calling form (`api_docs/function_calling/`), and the character length of each definition serialised as JSON (min, median, mean, max, total). Save the combined list of all function-calling definitions as a LOCAL JSON file for Part 3. Do not put it in `results/`.
2. **Tool-result sizes:** for every train and dev task, execute its published reference solution in AppWorld's offline environment. Record per task:
   - the number of API calls;
   - the character length of each API response (distribution per task and overall);
   - whether the evaluation passes.

   Also record the scenario id of each task, so tasks can be grouped by scenario.
3. **Structure:** tasks per scenario in train and dev, and which apps each task uses (counts only).
4. **Issues:** the AppWorld GitHub issues (open and closed), each with title, state and date, plus a one-line note of what the issue says about evaluation or environment bugs. Quote, do not judge.

## Part 3. Billed tokens of real definitions and the context window
With the local definitions file from Part 2, run the probe's `--deftokens` mode on each ScaDS tool-calling model for `--sizes 0 10 50 100 200 457`. Also run it on one OpenAI model if you can. Output: `results/r3-deftokens-<model>-<date>.json`. An error at a size is a result: it shows the context limit.

## Part 4 (after Parts 1-3, optional). Floor pilot on AppWorld dev
- Run AppWorld's own `simplified_function_calling_agent` on the **dev** split (60 tasks), one run, with one or two ScaDS models through their OpenAI-compatible endpoint.
- Report per model:
  - task and scenario completion (TGC, SGC);
  - prompt, cached and completion tokens per task (from usage records);
  - turns per task and failures by type.
- Dev only. This is a floor check (whether these models score far from 0 and far from 100), not a result about V5.

**Reply** by adding `RESULTS-R1.md` (and the JSON files). Do not edit anything outside `exchange/prior-work/v5-probes/results/`.
