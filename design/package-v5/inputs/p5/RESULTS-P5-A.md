# RESULTS-P5-A: the break-even on our route, ScaDS GLM-5.3 with client deferral (AUTH-028 part A; lead, 2026-11-08)

**This is P5's test** (`05` P5; `04` section 5): our own route, the university API (ScaDS, free, `zai-org/GLM-5.3`), client-side
deferral (a small core plus `search_tools` and `call_tool`, so the `tools` array never changes, V5-R02), against exposing every
definition.
- **Authorized** by AUTH-028, the cap raised to about 140 by INT-T-026. The run started after GLM B2 ended (2026-11-08 14:28 UTC),
  on the human's word (INT-T-041).
- **Harness:** revision 2 (`87905175...045409`).
- **Analysis:** `tools/p5_analyze.py` (`scads-glm53-analysis.json`). Logs: `scads-glm53-r2/` (the run) and `scads-glm53/` (the
  stopped first attempt).

## Run
- **First attempt** (`scads-glm53/`): stopped after 4 requests by the harness's own rule (two failures in a row). GLM-5.3 on ScaDS
  allows **2 requests per minute** per key (HTTP 429, "model_per_key ... Current limit: 2"; also `10` line 40).
- **Run** (`scads-glm53-r2/`): the same command with `--pause 31`. 138 requests, all HTTP 200 except the very first (one more
  429, from the previous window), 16:59-18:13 UTC. Cost $0 (ScaDS is free).
- **Design:** as revision 2.
  - 4 sizes (10, 30, 100, 300 stub tools of about 230 tokens each), 2 arms.
  - Per size and arm: 2 cold sessions (a fresh marker in tool 0), then 1 warm session; three user turns per session.
  - Calibration requests with markers of their own.
- ScaDS returned no served-model id, so the requested id is recorded. Reasoning as served: 3,530 reasoning tokens in all.
- **Bill units:** DPR-0006 fresh-input-token equivalents, priced by GLM-5.3's official Z.ai table (`11` RC-3: $1.40 input,
  $0.26 cache read, no write charge, $4.40 output; r = 0.186, o = 3.14). ScaDS bills nothing, so the table gives the shape of a
  bill on a priced host of the same model, not a cost to us.

## Results [O]
**Tokens per definition** (calibration, expose-all): 236, 231, 229 and 229 at 10, 30, 100 and 300 tools. D-01 assumed 250. The
deferral prefix is about 1,480 tokens at every size; it does not depend on n.

**Bill ratio, deferral / expose-all, whole session** (D-01 as written: client mode, cached core, its defaults K = 3 and H = 5,000):

| n | cold session 1 | cold session 2 | warm | D-01 as written | D-01, uncached core |
|---|---|---|---|---|---|
| 10 | 1.027 | 1.056 | 1.381 | 1.286 | 2.75 |
| 30 | 0.463 | 0.440 | 0.547 | 0.432 | 0.923 |
| 100 | 0.137 | 0.153 | 0.203 | 0.130 | 0.278 |
| 300 | 0.049 | 0.048 | 0.071 | 0.043 | 0.093 |

- **Cache control:** cold sessions started at 0 cached, warm sessions at 0.95 to 1.00 cached.
- **Requests:** expose-all made 5 requests per session, deferral 6 (one search).

## Reading [I]
1. **The break-even on our route lies between 10 and 30 tools**, close to 10. At 10 tools deferral costs 3-6% more on a cold
   start; at 30 it costs 44-46% of expose-all. This is at the low end of D-01's range for a cached core: 12-57 tools in `README.md`, and "about 10-60 tools"
   in `04` section 1.
2. **D-01 as written fits this route.** At 30, 100 and 300 tools it is within 0.01 to 0.03 of the cold sessions (relative 2-16%).
   The two cold sessions themselves differ by up to 0.02, so the difference is close to the run-to-run spread.
   - At 10 tools D-01 overstates deferral's cost (1.29 against 1.03-1.06): its default search, history and output terms weigh
     most when the tool block is small.
   - The uncached-core variant does not fit (2 to 2.7 times too high): ScaDS caches the small deferral prefix.
3. **A warm start shrinks deferral's advantage** (ratios 0.02 to 0.33 higher), because expose-all's larger prefix gains more
   from the cache. This matches part B (OpenAI) and D-01's table E as a direction.
4. **Against part B** (OpenAI hosted search, `RESULTS-P5-B.md`): D-01 as written missed the vendor route by 2.2 to 7.9 times at
   100-300 tools, but fits our client route. The difference is the vendor's billed deferred part and its loaded namespaces,
   which D-01's client mode does not have.
5. **For the decision the human postponed to after part A (INT-T-027):**
   - D-01 needs no revision for V5's route (client deferral on the university API).
   - The hosted-search variant (`calc/regime_bill_hosted.py`) is needed only for vendor-hosted search (part B's route).
   - **Proposal for the human (not made):** keep D-01 as the working equation for the client route, and add the hosted variant
     as a separate mode for vendor search. **The human decides.**
6. **For V5-R03** (choose by D-01 per deployment): on this route, deferral already pays from about a dozen tools. Below that,
   exposing everything is cheaper.

## Limits
- One model, one route, stub tools (about 230 tokens each), one short three-turn task.
- Two cold sessions and one warm session per cell.
- No accuracy (P5 claims none).
- The price table is the official one for the same model, not ScaDS (free).
- The first request of the run was refused, so it is not in the calibration; the analysis uses the n = 10 deferral calibration
  for every size, because the deferral prefix does not depend on n. That was a fix in `p5_analyze.py` (2026-11-08); part B's arms
  are calibrated per n and unaffected.

## Corrections of 2026-11-09 (lead, AUTH-032 as amended by INT-T-053)
Found while building the results deck (`design/package-v5/deck/CLAIM-LEDGER.md`). The text above is left as it was; each point names the line it corrects.
- Line 46: the largest relative difference at 30 to 300 tools is 17.7% (0.153 against 0.130 at 100 tools), not 16%.
- Line 51: warm minus cold reaches 0.354 at 10 tools (1.381 against 1.027), so the range is 0.02 to 0.35.
