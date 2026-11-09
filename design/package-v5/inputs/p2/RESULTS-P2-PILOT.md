# P2 pilot: floor, ceiling and real figures (2026-11-08)

Status: run and read by the lead; **a pilot, not P2's test**. No arm was compared. Covered by INT-T-041: "run P5 and p2 parallel",
read as the pilot of `P2-DESIGN.md` section 8 stage 1 (about $0.50, stop $2).
- **Tasks:** 5 dev tasks, one from each of the first five eligible scenarios: 50e1ac9_1, fac291d_1, 4ec8de5_1, b119b1f_1,
  d4e9306_1.
- **Settings:** arm `all` (128 tools declared and offered), one run each.
- **Counts:** `pilot-analysis.json` (`tools/p2_analyze.py`). Logs are local and git-excluded.

## Runs
| Run | Model (served id) | API | Success (AppWorld evaluator) | Tests passed | Calls | Prompt tokens per call | Cached share | Output tokens per call | Cost per task |
|---|---|---|---|---|---|---|---|---|---|
| p2-pilot-gpt5mini-all | gpt-5-mini-2025-08-07 | chat_completions | 3 of 5 | 16 of 18 | 40 | 16,843 | 0.86 | 456 | $0.0149 |
| p2-pilot-gpt5mini-all-resp | gpt-5-mini-2025-08-07 | responses | 3 of 5 | 15 of 18 | 47 | 17,156 | 0.78 | 283 | $0.0175 |
| p2-pilot-gpt54mini-all-resp | gpt-5.4-mini-2026-03-17 | responses | 3 of 5 | 16 of 18 | 34 | 16,929 | 0.84 | 321 | $0.0308 |
| p2-pilot-gpt54mini-all (failed) | gpt-5.4-mini | chat_completions | not run | — | 0 (5 rejected) | — | — | — | $0 |

**Pilot spend: $0.316**, inside the $2 stop. Prices from `P2-DESIGN.md` E2, computed from the reported tokens.

## Findings [O]
1. **No floor and no ceiling.** Every working run solved 3 of 5, so P2 can show a loss or a gain (`17` CH-0140).
2. **The run-to-run spread is visible already.** The two gpt-5-mini runs both solved 3 of 5, but not the same 3: one task each
   way. Temperature 1.0 is the models' fixed default, so P2 needs its repeats.
3. **The real figures are below the estimate** of section 7.
   - About 8 calls per task (7 to 9.4), against 10 assumed.
   - About 17,000 prompt tokens per call, against 22,500.
   - Cached share 0.78 to 0.86, against 0.85.
   - Cost per task: $0.015-0.018 (gpt-5-mini) and $0.031 (gpt-5.4-mini), against $0.025 and $0.067.
   - The first call of each run was uncached and the second already cached about 98%, so the 128-tool prefix caches as
     expected.
4. **gpt-5.4-mini rejects function tools with reasoning on Chat Completions.** Every call returned HTTP 400: "Function tools
   with reasoning_effort are not supported for gpt-5.4-mini in /v1/chat/completions. To use function tools, use /v1/responses
   or set reasoning_effort to 'none'."
   - AppWorld's agent absorbed the errors, so that run ended with no calls and no spend.
   - The harness now stops after two failed model calls in a row, and supports the Responses API, AppWorld's own setting for
     the gpt-5 family.
   - **P2's main run uses the Responses API for both models**, so the API is the same across models.
5. **In arm `all`, gpt-5.4-mini made 2 calls to tools outside the oracle subset.** That is allowed in `all`, and it shows the
   oracle list is not the only working path.

## Revised cost for P2's main run (from the measured figures)
**Main A:** `all`, `enf` and `instr`; 30 tasks; 2 repeats; Responses API.
- gpt-5-mini: about **$3.2** (180 task-runs x $0.0175).
- gpt-5.4-mini: about **$5.5** (180 x $0.031).
- **Together about $8.7**; stop at 1.5 times, $13.

**Main B** adds `drop`: about $11.6, stop $17.4.

## Limits
Five tasks, one run per cell. The arms `enf`, `instr` and `drop` have not yet run live; `enf`'s `allowed_tools` field on the
Responses API is still untested from this harness (R1 tested it with its own probe). Prices were read on 2026-11-08.
