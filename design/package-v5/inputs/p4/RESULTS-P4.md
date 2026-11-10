# P4 results: clearing old tool results on our route (2026-11-10; AUTH-033, INT-T-054)

- **Question (HYP-0021, `05` P4):** does masking old tool observations lower the bill of a session, once the cache rewrites it
  causes are counted, without lowering accuracy beyond run-to-run variation?
- **Condition check first** (`P4-CONDITION-CHECK.md`): in P2's logs old tool results were 13% of billed input, and its condition
  was not met. **The lead** read AUTH-033's "if possible ... finish p4 fully" as covering a run anyway; `P4-CONDITION-CHECK.md`
  left that decision to the human, who has not ruled on it.
- **Step A** (`P4-REPLAY-A.md`, no model request): with the vendor's defaults clearing never fires on our tasks; with its
  documented example it raises the replayed bill by 1.0-7.5%.
- **Counts:** `p4-analysis.json` (`tools/p4_analyze.py`). Logs local and git-excluded.

## Run [O]
- **Rule:** Anthropic's `clear_tool_uses` applied by the client, with the vendor's documented example (trigger 30,000 input
  tokens, keep the last 3 tool results, clear only if at least 5,000 tokens go; stored source
  `v5-anthropic-context-editing-20261022.md` lines 38-40, 395-410, 1724-1732). Cleared results stay cleared. `p2_offering.py
  --mask 30000,3,5000` (commits 759de31 and its predecessor).
- **Setting:** GLM-5.3 on OpenRouter pinned to GMICloud fp8, no effort setting sent (GMICloud's default; mean 1,369 reasoning tokens per request, median 120, in the masking runs), temperature 0, seed 100; AppWorld dev, 128 tools
  declared; the keep-everything arm is P2b's two `all` runs (same model, provider and settings, 2026-11-09).
- **Tasks:** mask repeat 1 stopped at its $2.50 cap after 20 of P2b's 30 tasks; repeat 2 ran exactly those 20 (rule fixed in
  `P4-REPLAY-A.md` after the first 7 tasks' costs were seen, before any accuracy). The keep arm is read on the same 20. These are
  P2b's first 20 tasks in their fixed order, short tasks (the keep arm's median is about 7 calls), not the longest available.
  The keep runs used the harness before `--mask` was added (the code path is the same when masking is off).
- **Spend:** smoke $0.400, repeat 1 $2.502, repeat 2 $2.483 = **$5.385** (the lead's limit $8, AUTH-033).

| Arm, repeat | Success of 20 | Billed | Calls | Cached share | Tasks with clearing | Clearing events | Tokens cleared |
|---|---|---|---|---|---|---|---|
| keep r1 | 18 | $1.220 | 145 | 0.820 | - | - | - |
| keep r2 | 18 | $1.177 | 157 | 0.922 | - | - | - |
| mask r1 | 17 | $2.463 | 212 | 0.835 | 11 | 33 | 268,784 |
| mask r2 | 18 | $2.483 | 201 | 0.743 | 10 | 28 | 225,103 |

- **Paired, mask minus keep, per task** (averaged over repeats; 95% scenario-bootstrap interval, 4,000 resamples, seed 0):
  success **−0.025 (−0.175 to +0.125; 7 scenarios, so accuracy is not shown unchanged)**; billed **+$0.064 (+$0.024 to
  +$0.107)**; calls **+2.8 (+0.7 to +5.2)**.
  Billed x2.06, calls x1.37.
- **Run-to-run flips:** keep 0 of 20, mask 1 of 20.
- **Check for the different day:** on the 9 tasks where clearing never fired, mask and keep agree (billed x1.00, calls x0.95).
  On the 11 where it fired: billed **x2.66**, calls **x1.72**. The groups are defined by the mask arm's own behaviour after the
  fact, and the never-fired nine are the cheapest tasks (at most 12 calls), so this is a weak check, not a control.

## Reading [I]
- Clearing old tool results, as the vendor documents it, **doubled the bill** on the tasks where it fired; an accuracy
  difference was not detected (the interval is wide). The extra calls (x1.72 where clearing fired) suggest that the model called
  tools again after its results were cleared; this is not decomposed (no check of repeated calls), and repeat 1's cached share
  (0.835) equals keep repeat 1's (0.820), so cache rewrites are not shown as a cause there (repeat 2: 0.743 against 0.922).
  Step A, with the behaviour held fixed, already showed a small loss.
- HYP-0021's falsifier is stated for **long single runs**. Its direction (a higher bill with masking) was observed here on short
  tasks; its stated domain was not tested, so the falsifier is **neither met nor refuted**. Status stays `proposed`.
- With the vendor's defaults (100,000 tokens) clearing would not have fired at all on these tasks.

## Limits
- One model and provider, 20 tasks in 7 scenarios (the interval is rough), one rule setting, no cache-write premium (GMICloud);
  with Anthropic's write premium the rewrites would cost more.
- AppWorld's tasks are short. Long tasks, where clearing is meant to pay, were not run (`05` P4 named MCPMark).
- The keep arm ran a day earlier, with the earlier harness version; the never-cleared tasks show no drift, but the comparison
  is not simultaneous and that check is weak (see above).

## Estimators (added 2026-11-10, AUTH-034; recomputed by the lead from `p4-analysis.json`)
- Ratio of total spend ×2.06; mean of the per-task ratios ×2.12; median per-task ratio ×1.52; without the five tasks with the largest excess (they carry 73% of it) ×1.39. "Doubled" is the total-spend reading; a few tasks carry it.
