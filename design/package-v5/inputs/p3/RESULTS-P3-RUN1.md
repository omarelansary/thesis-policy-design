# P3 run 1: do models search for a deferred tool without being told to? (2026-11-07)

Status: run and read by the lead; **the reading is provisional and for the human**. No V5 rule changed. Covered by INT-T-028 to
INT-T-030 (the P3 AUTH row is still to be entered, `ops/OPEN-TASKS.md`). Question: `05` P3, HYP-0019. Method: `README.md` here
and the harness docstring. Counts: `run1-analysis.json` (from `tools/p3_analyze.py`; the harness's own summaries
`run1-*-summary.json` count every extra call as wrong and are kept as the raw view). Raw logs local and git-excluded.

## Run
| Model (OpenRouter, GMICloud fp8 pinned, no fallbacks) | Requests | Failed | Spend |
|---|---|---|---|
| minimax/minimax-m3 | 546 | 0 | $0.514 |
| deepseek/deepseek-v4.1-flash | 575 | 0 | $0.182 |
| z-ai/glm-5.3 | 563 | 0 | $0.864 |
| smoke tests (one task per model, before the runs) | 78 | 0 | $0.115 |
| **P3 total** | 1,762 | 0 | **$1.675 of the $10 stop** |
Every reply was served by GMICloud with the requested model. 20 tasks x 7 sessions per model, temperature 0, seed 7, one run each.

## Results [O] (sessions out of 20 per cell; D, A, W in two prompt variants: plain / index)
| Cell | Measure | MiniMax-M3 | DeepSeek-V4.1-Flash | GLM-5.3 |
|---|---|---|---|---|
| E expose-all (control) | target called | 20 | 20 | 20 |
| | a different action taken as well | 1 | 0 | 1 |
| D target deferred | searched, with no instruction to | 20 / 20 | 20 / 20 | 20 / 20 |
| | target called | 20 / 20 | 19 / 20 | 20 / 20 |
| | a different action taken as well | 1 / 0 | 0 / 0 | 0 / 0 |
| W distractor visible, target deferred | searched | 19 / 19 | 20 / 20 | 20 / 20 |
| | target called | 19 / 19 | 19 / 19 | 20 / 20 |
| | distractor called (mostly a read-only twin) | 2 / 3 | 2 / 4 | 2 / 2 |
| | a different action taken | 1 / 1 | 0 / 0 | 0 / 0 |
| A target absent | searched | 20 / 20 | 20 / 20 | 20 / 20 |
| | no wrong action (the right outcome) | 17 / 17 | 18 / 18 | 18 / 18 |
| | a substitute action taken | 3 / 3 | 2 / 2 | 2 / 2 |
| | the absent tool called by guessing its name | 0 / 0 | 3 / 4 | 1 / 2 |
| | still searching at the 6-request cap | 15 / 12 | 14 / 17 | 15 / 14 |
"A different action" = a state-changing catalogue tool other than the target; read-only look-ups (show_*, search_*, *_exists)
are not counted as wrong. The search ranker put the target in its results in every D and W session where the model searched.

**Bill side observation [O], not P3's question:** per session, expose-all read 171K-189K prompt tokens (the 463-tool prefix on
about 2.4 requests) and deferral 4.3K-5.4K (3.5-3.8 requests); cost per session was 4.6 times (DeepSeek, whose cached price is
about 2% of input) to 30 times (MiniMax) higher for expose-all. One user turn, single-need tasks, one provider.

## Reading [I]
1. **HYP-0019's falsifier is not met on this set.** With the target deferred and no instruction to search, all three models
   searched in every session and called the target in 19-20 of 20, the same as expose-all (20 of 20). A visible wrong tool did
   not pull them away (target 19-20 of 20, different actions 0-1). `05` says a loop item of 20 can show only a large failure
   rate; none was seen, so per `05` the small differences go to the end-to-end study.
2. **The index line made no difference that 20 tasks can show** (target called: plain and index within one session of each other in D and W; DeepSeek called the distractor 2 and 4 times).
3. **The absent-tool case is the weak point.** Models rarely did the wrong thing (2-3 of 20 substitute actions), but most kept
   searching until the cap (12-17 of 20 reached it) instead of telling the user, and DeepSeek and GLM sometimes called the missing
   tool by a guessed name. That costs requests (about 5.7 per session against 3.5-3.8 when the tool exists) and, without a cap,
   would run on. This supports the no-match rule and recovery options `05` already lists for P3 (a stop after an empty or
   unhelpful search; its threshold set by the loop, not here). **Proposal for the human, not a V5 change.**

## Limits
- 20 single-need tasks written by the lead, every value given in the prompt, stub results; real tasks need several tools and
  results that matter. AppWorld's simulated apps, not real services.
- One run per cell at temperature 0; the route is not deterministic (R2: 5 of 57 tasks flipped between identical runs).
- OpenRouter with GMICloud fp8, not ScaDS; quantization and chat templates may differ from ScaDS's deployments.
- "Uninstructed" means no instruction in the system text; search_tools still describes itself in one line, as vendors' search
  tools do. The ranker is the harness's BM25; the models' queries found the target every time, so ranker misses were not tested.
- The cap of 6 requests shapes the absent-cell counts; a longer cap would show how long models keep searching.

## Corrections of 2026-11-09 (lead, AUTH-032 as amended by INT-T-103)
Found while building the results deck (`design/package-v5/deck/CLAIM-LEDGER.md`). The text above is left as it was; each point names the line it corrects.
- Line 44: "searched in every session" holds for the deferred cell D. In the distractor cell W, MiniMax-M3 searched in 19 of 20 sessions in both variants (`run1-analysis.json`; `RESULTS-P3-RUN2.md:85`).
