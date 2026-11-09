# P2b results: the instruction-only offering on an open-weight model (2026-11-09; AUTH-031, INT-T-044, INT-T-046 to INT-T-051)

- **Question (HYP-0018, `P2-DESIGN.md` section 8):** on a route without enforcement, does naming the subset in one sentence keep an
  open-weight model inside it, at the same accuracy and without breaking the cache?
- **Counts:** `p2b-or-analysis.json` (`tools/p2_analyze.py`) and `p2b-or-paired-summary.json` (`tools/p2_paired.py`, the method
  of RESULTS-P2-MAIN, which it reproduces exactly). Logs and AppWorld outputs are local and git-excluded.

## Route: why OpenRouter and not the university API [O]
- Planned on ScaDS (free). Three attempts stopped themselves after 6, 7 and 5 tasks of their first run (190 calls, 10 failed):
  1. two calls in a row timed out after 3 x 300 s (client timeout);
  2. the same, by night;
  3. with a 1200 s client timeout (INT-T-049): ScaDS itself answered HTTP 408 after about 900 s per try.
  ScaDS runs GLM-5.3 as an HPC job (`gpustack/GLM-5.3-W4A8`, thinking at maximum by default; stored page
  `evidence/literature-20261019/p2b-scads-glm53-model-page-20261109.txt`). The attempts are kept locally and are not pooled or
  scored (each stop left an unfinished task, which AppWorld's evaluator rejects).
- Run instead on OpenRouter, `z-ai/glm-5.3` pinned to GMICloud fp8 with fallbacks off (INT-T-050, INT-T-051; `--provider`,
  commit ad0383d). Every one of the 855 calls was served by GMICloud.
- **Effort as served** (INT-T-048: not lowered). On GMICloud "as served" behaves like effort high (reasoning tokens for one short
  question: none sent 236 and 421, high 224 and 172, low 50 and 73; `tools/p2b_effort_probe.py`). ScaDS's default is max. So
  this is not the university route: 8-bit against 4-bit weights, and a lower default effort.

## Run [O]
- 30 AppWorld dev tasks (10 scenarios), 128 tools declared, oracle subsets of 6-10; Chat Completions; temperature 0, seed 100;
  arms `all` and `instr` (`all` plus one sentence naming the subset), 2 repeats each, in the order all, instr, all, instr.
- 4 runs, 120 task-runs, 855 calls, 0 failed calls. Billed by OpenRouter: $1.707, $1.297, $1.499, $1.278 = **$5.781**
  (estimate was about $18, range $13-28). P2 total with P2 main and the pilot: $18.474.

| Run | Success | Calls | Calls outside the oracle subset | Cached share | Billed |
|---|---|---|---|---|---|
| all r1 | 27/30 | 215 | 48 | 0.819 | $1.707 |
| instr r1 | 29/30 | 205 | 0 | 0.917 | $1.297 |
| all r2 | 28/30 | 228 | 108 | 0.935 | $1.499 |
| instr r2 | 30/30 | 207 | 0 | 0.922 | $1.278 |

- Per call (means over runs): prompt 25,615-27,271 tokens, completion 791-918, reasoning 423-580.

## Paired estimates [O]
- `instr` against `all`, per task, averaged over the repeats: **+0.067 (95% scenario-bootstrap interval −0.033 to +0.217)**;
  59 of 60 against 55 of 60.
- Run-to-run noise: `all` repeat 1 against repeat 2 differ on **1 of 30** tasks (P2 main: 6 and 8).
- Calls x0.93 and billed cost x0.80 against `all`. Part of the cost gap is the first run's lower cached share (0.819, the cache
  was still cold); on repeat 2 alone the ratio is x0.85.
- **0 calls outside the subset in 412 `instr` calls (60 task-runs).** In `all`, 48 and 108 calls went to tools outside the oracle
  list.

## Reading [I]
- On this route GLM-5.3 followed the instruction completely: it stayed inside the named subset, kept the cache, used slightly
  fewer calls and was not less accurate (the interval allows at most a 3-point loss). This is the opposite of gpt-5-mini in P2
  main (5 and 14 calls outside, calls doubled) and like gpt-5.4-mini.
- So "the instruction form depends on the model" stands, now with one open-weight model on the side that follows it. It is not
  shown for the university route itself (other weights and effort), nor for subsets that miss a needed tool.
- GLM-5.3 succeeded far more often than the two OpenAI models (55 of 60 in `all`, against 38 and 40). Near that ceiling a gain is
  hard to see; a loss would still have shown.

## Limits
- One model, one provider, 30 tasks in 10 scenarios (the interval is rough), oracle subsets, catalogue of 128.
- Not the university route (see above). The ScaDS attempts give no scored comparison.
- Accuracy differences of a few points cannot be shown by a loop item (`05` section 1).
