# P4 results: clearing old tool results on our route (2026-11-10; AUTH-033, INT-T-054)

- **Question (HYP-0021, `05` P4):** does masking old tool observations lower the bill of a session, once the cache rewrites it
  causes are counted, without lowering accuracy beyond run-to-run variation?
- **Condition check first** (`P4-CONDITION-CHECK.md`): in P2's logs old tool results were 13% of billed input; P4 went ahead
  under AUTH-033 ("if possible ... finish p4 fully") although its condition was not met.
- **Step A** (`P4-REPLAY-A.md`, no model request): with the vendor's defaults clearing never fires on our tasks; with its
  documented example it raises the replayed bill by 1.0-7.5%.
- **Counts:** `p4-analysis.json` (`tools/p4_analyze.py`). Logs local and git-excluded.

## Run [O]
- **Rule:** Anthropic's `clear_tool_uses` applied by the client, with the vendor's documented example (trigger 30,000 input
  tokens, keep the last 3 tool results, clear only if at least 5,000 tokens go; stored source
  `v5-anthropic-context-editing-20261022.md` lines 38-40, 395-410, 1724-1732). Cleared results stay cleared. `p2_offering.py
  --mask 30000,3,5000` (commits 759de31 and its predecessor).
- **Setting:** GLM-5.3 on OpenRouter pinned to GMICloud fp8, effort as served, temperature 0, seed 100; AppWorld dev, 128 tools
  declared; the keep-everything arm is P2b's two `all` runs (same model, provider and settings, 2026-11-09).
- **Tasks:** mask repeat 1 stopped at its $2.50 cap after 20 of P2b's 30 tasks; repeat 2 ran exactly those 20 (rule fixed in
  `P4-REPLAY-A.md` before any accuracy was seen). The keep arm is read on the same 20.
- **Spend:** smoke $0.400, repeat 1 $2.502, repeat 2 $2.483 = **$5.385** (AUTH-033 limit $8).

| Arm, repeat | Success of 20 | Billed | Calls | Cached share | Tasks with clearing | Clearing events | Tokens cleared |
|---|---|---|---|---|---|---|---|
| keep r1 | 18 | $1.220 | 145 | 0.820 | - | - | - |
| keep r2 | 18 | $1.177 | 157 | 0.922 | - | - | - |
| mask r1 | 17 | $2.463 | 212 | 0.835 | 11 | 33 | 268,784 |
| mask r2 | 18 | $2.483 | 201 | 0.743 | 10 | 28 | 225,103 |

- **Paired, mask minus keep, per task** (averaged over repeats; 95% scenario-bootstrap interval, 4,000 resamples, seed 0):
  success **−0.025 (−0.175 to +0.125)**; billed **+$0.064 (+$0.024 to +$0.107)**; calls **+2.8 (+0.7 to +5.2)**.
  Billed x2.06, calls x1.37.
- **Run-to-run flips:** keep 0 of 20, mask 1 of 20.
- **Control for the different day:** on the 9 tasks where clearing never fired, mask and keep agree (billed x1.00, calls x0.95).
  On the 11 where it fired: billed **x2.66**, calls **x1.72**.

## Reading [I]
- Clearing old tool results, as the vendor documents it, **doubled the bill** on the tasks where it fired and did not change
  accuracy within the interval. The model called tools again after its earlier results were cleared, so the saving in carried
  tokens was outweighed by extra calls and by the cache rewrites. Step A, which held the behaviour fixed, already showed a small
  loss; the live run shows the larger cause, the re-fetching.
- HYP-0021's falsifier ("a higher session bill than keeping them, once the cache rewrites caused by the masking are counted")
  is **met on this setting**. Its status stays `proposed`: one model, one rule setting, AppWorld's short tasks.
- With the vendor's defaults (100,000 tokens) clearing would not have fired at all on these tasks.

## Limits
- One model and provider, 20 tasks in 7 scenarios (the interval is rough), one rule setting, no cache-write premium (GMICloud);
  with Anthropic's write premium the rewrites would cost more.
- AppWorld's tasks are short. Long tasks, where clearing is meant to pay, were not run (`05` P4 named MCPMark).
- The keep arm ran a day earlier; the never-cleared tasks show no drift, but the comparison is not simultaneous.
