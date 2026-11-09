# 12. Experiment readiness: what can start, what cannot, and what the authorization would need to say

Status: provisional, lead, 2026-10-27; section 5 added 2026-11-07 (what requests R1 to R3 changed). **2026-11-07: the human authorized P5 as drafted in sections 3 and 5 (INT-T-023 lines 12-13, REQ-U1107-03); recorded with its limits as AUTH-028 in `ops/AUTHORIZATIONS.md` on the operations branch. P1 to P4 remain unauthorized. The route and models are still the human's choice before any run.** This is an assessment and a draft scope, not an authorization: no experiment, harness code or API call by the lead is authorized by it (AUTH-020 limits; REQ-U22-16 says the human will extend AUTH-020 when told the lead is ready). The loop rule of `05` stands: small items, read the result, revise, then the next item (REQ-U21-06).

## 1. Readiness by loop item
| Item (`05`) | Question | Ready? | What exists | What is missing |
|---|---|---|---|---|
| P0 part 4 | Is the cache a plain prefix cache? How long does it live? | **Done 2026-10-27 by the human** (REQ-U22-17; `10` section 9) | Outputs for three models | Plain prefix cache on GLM-5.3 and MiniMax-M3, unexplained on gpt-oss-120b; lifetime under 5 hours on two, over 5.5 on one; a longer-gap lifetime run is optional |
| **P5** | Where is the regime break-even on this route, and are deferred definitions billed? | **Yes, once authorized** | D-01 and D-04 (the arithmetic and its price range), the API's usage fields, a stub-tool pattern from the probes | A harness (new code, written by the lead, run by the human): stub catalogues of several sizes, two arms (all tools in the prefix; a small core plus definitions appended after a scripted search), a fixed session length, usage recorded per request. About 80 requests per model, no accuracy measured |
| P3 | Do models search for a deferred tool without being told to? | **Not yet** | The recovery design (`04`), the absent-tool probe (one run per model) | A task set with a ground-truth tool per task, a catalogue with natural descriptions, a client-side search tool, the cells and prompt variants of `05` (desk work, no key; then about 160 requests per model) |
| P1 | Does memory-informed offering help returning users? | **No** | HYP-0017, D-02 (the threshold) | A multi-session benchmark or task set (candidates in `17`) or a thin generator of user histories (none found, `03` section 9), the memory file format, a task set per session; the design decisions of `05` P1 |
| P2 | Does offering a subset keep accuracy nearly the same? | **No** | The mechanism question | `allowed_tools` is rejected (`10`); the route left is instruction text without enforcement, which needs its own design |
| P4 | Does masking lower the bill of long runs? | **Not needed yet** | HYP-0021 | Only if P0-P5 show a deployment with large tool results |

## 2. Model independence
Every harness takes the model as a run-time argument and writes it into each output record; no design conclusion may rest on one model (REQ-U22-14). The first items measure the API and the arithmetic, not a model's accuracy: P5 reads token classes, so any model that reports usage will do, and a result is stated as a range across the models the human runs. The third probe (done) found a plain prefix cache on GLM-5.3 and MiniMax-M3 and an unexplained pattern on gpt-oss-120b, so P5's cached-token readings are easiest to interpret on the first two; this does not choose a model.

## 3. What I would ask AUTH-020 to cover (draft, for the human to change)
1. **Scope:** write the P5 harness (stdlib Python, no installs) and then a P3 task set and harness; the human runs them with the key held in the human's own terminal; outputs are stored under `design/package-v5/inputs/` and read by the lead.
2. **Limits:** P5 first, then stop and report before anything else runs; at most about 100 requests per model for P5; the models are the human's choice at run time; no keys, tokens or key identifiers in the workspace; outputs scanned for key material before commit (UTF-8, no redirect); no accuracy claim from P5.
3. **Not covered:** P1, P2 and P4; any change to the design records beyond adding results; any parameter value for the policy; any push other than to `v5-audit`.
4. **Stop rule:** a result that contradicts the arithmetic (D-01, D-04) by more than the run-to-run spread is reported and the design revised before the next item.

## 4. What I can do now without any authorization
Write the P3 task set and catalogue specification (desk work); regenerate the frontier page and sort the 24 "before any implementation" ledger rows under V5; keep records current. None needs the key.

## 5. Update 2026-11-07: what requests R1 to R3 changed (`17` section 5; results in `exchange/prior-work/v5-probes/results/`)
- **P5.** Still the first loop item, and still unrun as specified (stub catalogues of several sizes). R3 Part B adds one measured point on a real route and benchmark: AppWorld with 469 definitions on every call costs 2.2 to 2.6 times the bill of AppWorld's own predictor subset on MiniMax-M3 (OpenRouter, one provider). About 96% of the all-tools prompt was billed as cache reads, and there were no cache-write charges. A second model (GLM-5.3 on ScaDS, AUTH-026, finished 2026-11-08; `17` section 5) gives a computed ratio of about 1.5 (1.08 to 1.80 over 47 price endpoints), so the point depends on the model. The curve over catalogue size, and so the break-even, still needs P5. The GLM B2 run has ended, so P5's ScaDS part can start.
- **P2.** Partly informed. AppWorld's predictor offers a per-task subset by removing definitions, which is not V5's fixed-prefix offering. In four runs on one model it showed no visible accuracy difference against all tools: means 47.5 and 46 of 57, with 9 to 12 tasks changing between identical runs. The mechanism question of the table above is unchanged.
- **Run settings any authorization must fix and record:** the provider (pinned, no fallback), the reasoning mode (hosts differ in the default; with it off, MiniMax-M3 passed 24 to 28 of 57, with it on 45 to 50), the AppWorld `raise_on_failure` setting for reference-solution checks, a new experiment name per run (AppWorld issue #203), a client timeout, and a stop when the key or endpoint refuses calls.
- **Repeats.** Identical runs differed in 5 (ScaDS) and 9 to 12 (OpenRouter) of 57 tasks. A comparison of arms needs at least two runs per arm, or more tasks, before "nearly the same" accuracy can be read (`17` section 9, item 3).
- **Model availability.** ScaDS stopped serving MiniMax-M3 between 2026-11-02 and 11-06. Served models can disappear without notice, so each harness should record the served model id per call.

## 6. Update 2026-11-08 (INT-T-040; this branch, `v5-p5-break-even`)
This section supersedes the rows of section 1 for P5, P3 and P2. Branch `v5-r3-part-b-results` has its own section 5 (update of
2026-11-07); a merge keeps both sections.
- **P5** (AUTH-028).
  - Part B, the OpenAI side check, is done: $0.594 (`inputs/p5/RESULTS-P5-B.md`).
    - Individually deferred functions still bill 30% of their tokens.
    - The break-even is between 10 and 30 tools on cold starts.
    - D-01 as written misses this route by more than the run-to-run spread. The human keeps D-01 until part A (INT-T-027).
  - Part A (ScaDS GLM-5.3, client deferral, cap about 140 requests, INT-T-026) waits for the GLM B2 run to end.
- **P3: done and closed** (runs 1-6 on OpenRouter, GMICloud fp8, three models, $9.953; INT-T-028..039; `inputs/p3/P3-LOG.md`).
  - The models searched for a deferred tool without being told to, so HYP-0019's falsifier is not met on that set.
  - For a missing tool, V5-R17 adds a deterministic stop plus one sentence in the system text (`04`, provisional).
  - Its open items go to the end-to-end study (`05` section 3).
- **P2: preparation authorized (INT-T-040), no run.** The route question of section 1 ("the route left is instruction text
  without enforcement") is now answered per provider:
  - **OpenAI:** `allowed_tools` is a real server mechanism.
    - It keeps the cache: 3,328 of 3,426 prompt tokens cached, as in the plain repeat.
    - Both models stayed inside the subset in 20 of 20 repeats (`10` section 12, R1 part 1 and R2 A1).
    - Limit: at most 128 tools per request (`17` section 7, P2 note; R1 part 3). So AppWorld's 457 definitions cannot be declared
      at once there.
  - **ScaDS:** the LiteLLM proxy refuses it (HTTP 400 on all ten models, `10` section 12). The instruction-only restriction is
    followed by most models in the adversarial probe cell (seven of nine in 5 of 5), not by Llama-3.3-70B. Named forcing is
    ignored by three models (`10` section 12, R2 A1).
  - **OpenRouter, GMICloud pinned:** accepted and **not enforced** (the excluded tool was called in 9 of 9). Only `auto` works
    for `tool_choice` (`10` section 12, R3 A3). So this route cannot carry a server-enforced arm, and a run there would look
    enforced when it is not.
  - **Consequence for the design [I]:**
    - P2 can test HYP-0018 in two forms: server-enforced on OpenAI, within 128 declared tools; and instruction-only, which is
      portable and has no enforcement, on the open-weight routes.
    - Each form needs an all-offered arm on the same declared prefix and cache diagnostics per request.
    - The design, the harness and a cost estimate are in `inputs/p2/P2-DESIGN.md`. **P2 was run on 2026-11-08** (INT-T-041, INT-T-042; `inputs/p2/RESULTS-P2-MAIN.md`, $12.69): no accuracy loss from server-enforced offering beyond run-to-run variation; the cache was kept. No request is sent before a run is
      authorized with its cost.
- **P1 and P4:** unchanged from section 1.

## Corrections of 2026-11-09 (lead, AUTH-032 as amended by INT-T-103)
Found while building the results deck (`design/package-v5/deck/CLAIM-LEDGER.md`). The text above is left as it was; each point names the line it corrects.
- Line 10: P3 "Not yet" is superseded: P3 ran on 2026-11-07/08 and was closed (line 35; `inputs/p3/P3-LOG.md`).
- Line 42: 3,328 of 3,426 holds for gpt-4.1-mini; gpt-5-mini cached 3,328 of 3,510.
