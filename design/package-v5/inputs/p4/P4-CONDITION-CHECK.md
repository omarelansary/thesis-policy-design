# P4: does its condition hold in our results? (lead, 2026-11-09; the human asked "check if P4's condition holds from our results")

**P4's condition** (`05` section 2): it runs "only if P0-P5 show deployments with large tool results". `05` does not define "large";
no threshold is set here (that is the human's). The data below are for the human to judge against.

## Where tool results can be measured
- **P2 main** (AppWorld 0.2.0 dev, 30 Spotify tasks, gpt-5-mini and gpt-5.4-mini, 16 runs, 480 task-runs): real tool results. Used.
- **P3, P5:** stub tools that answer "Done"; their result sizes say nothing about deployments. Not used.
- **P0, R1-R3:** probes with no task-sized tool results. Not used. **P2b** (ScaDS GLM-5.3): running; not included.

## Measurements [O] (`design/package-v5/tools/p4_condition_sizes.py`, `p4_condition_bound.py`; local logs, counts only)
- API prompt tokens per task-run: first request median 14,763 (the fixed prefix: instructions, demonstrations, 128 tool
  definitions); last request median 20,162, p90 32,217, max 49,014; growth over the task median 7,014, p90 19,036, max 34,210.
- Model calls per task-run: median 8, p90 22, max 49.
- Each tool result (tokenized with o200k_base; 12,472 results in the 452 task-runs that have a model-call log): median 146
  tokens, p90 227, p99 1,966, max 3,412.
- Tool results of a task-run, summed: median 3,820, p90 14,174, max 21,392 tokens. They are 62% of the growth (median) and 21% of
  the last request (median; p90 49%, max 72%).
- **AppWorld does not clear the history:** every request repeats the previous one in full (only its cache marker moves).
- **Old tool results** (those before the model's latest turn) carried in all requests: 13.1% of all billed input tokens (per
  task-run median 7.7%, p90 24%, max 56%). 89% of billed input was read from the cache.
- **Upper bound on what masking could save in P2,** if every old result were removed at no cost and were priced as cached input:
  $0.100 of gpt-5-mini's $1.581 input bill (6.3%; 2.4% of its $4.168 total) and $0.364 of gpt-5.4-mini's $5.264 (6.9%; 4.3% of
  its $8.525). The bound ignores the cache rewrite that masking causes, the results the model still needs, and accuracy, each of
  which lowers the saving.

## Reading [I]
- In our tasks the tool results are small next to the fixed prefix of tool definitions, and the possible saving is at most a few
  percent of the bill before the rewrite cost. On this evidence P4's condition is **not met by our results**.
- This is a statement about AppWorld's short Spotify tasks (median 8 calls), not about deployments in general. The long tasks P4
  names (MCPMark's set, `17`) were never run, so our results neither show nor exclude deployments with large tool results.
- 28 of the 480 task-runs have no model-call log; they are in the API counts and not in the tool-result counts.

## For the human
Whether P4 stays parked (condition not met in our results), or is tested on long tasks anyway, is the human's decision.
