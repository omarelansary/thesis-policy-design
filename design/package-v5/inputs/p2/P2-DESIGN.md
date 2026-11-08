# P2 design: offering a subset at a fixed cached prefix (preparation, 2026-11-08)

Status: **preparation only** (INT-T-040). No model request has been sent, and a run needs the human's authorization with its cost.
Written by the lead; nothing here is validated, approved or final. No V5 rule changed.
- **Harness:** `design/package-v5/tools/p2_offering.py`. **Analysis:** `design/package-v5/tools/p2_analyze.py`.
- **Tested** with a dry run and a local mock server (section 9).
- **Labels:** [F] fact in a cited source, [O] observation in this workspace, [I] interpretation, [U] unknown.

## 1. Question and falsifier
- **Question** (`05` P2; HYP-0018): when all tool definitions stay declared and cached, and only a subset is offered per task,
  does task accuracy stay nearly the same as when everything is offered?
- **HYP-0018 falsifier** (`hypotheses/HYP-0018.md`): offering a subset at an unchanged cached prefix gives lower task accuracy
  than offering all declared tools, beyond run-to-run variation, on the same tasks and model.
- **What a loop item can end** (`05` section 1 and its P2 row): only a mechanism failure (a cache break) or a large accuracy loss.
  A small difference goes to the end-to-end study.
- **Why it matters for V5:**
  - V5's offering stages (S1 deployment filter, M2 memory-informed seeds) change what is offered. Under V5-R02 they may not
    change the `tools` array within a session.
  - So V5 needs a way to offer a subset without breaking the cached prefix, and evidence that this does not cost accuracy.
  - HYP-0018 claims no bill saving: the definitions are still read at the cache price (HYP-0018, "Not claimed").

## 2. Evidence base
| # | Source | What it says | Label | Bearing on P2 |
|---|---|---|---|---|
| E1 | OpenAI function-calling guide, https://developers.openai.com/api/docs/guides/function-calling (fetched 2026-11-08; moved from platform.openai.com) | "Allowed tools: Restrict the tool calls the model can make to a subset of the tools available to the model." It lets you restrict calls "but not modify the list of tools you pass in, so you can maximize savings from prompt caching". It also says: "Aim for fewer than 20 functions available at the start of a turn at any one time, though this is just a soft suggestion." Callable definitions "are billed as input tokens". | [F] vendor, read through WebFetch | The mechanism exists and is documented as cache-preserving. The vendor itself recommends small offered sets |
| E2 | OpenAI pricing, https://developers.openai.com/api/docs/pricing (fetched 2026-11-08) | Per million tokens (input / cached input / output): gpt-5-mini $0.25 / $0.025 / $2.00; gpt-5.4-mini $0.75 / $0.075 / $4.50; gpt-5-nano $0.05 / $0.005 / $0.40; gpt-4.1-mini $0.40 / $0.10 / $1.60. Page undated | [F] vendor, read through WebFetch; re-read on the run day | Cost estimate (section 7) |
| E3 | `10` section 12, R1 part 1 and R2 A1 (stored probe results) | On OpenAI, `allowed_tools` (Chat Completions shape) was accepted and enforced: both models stayed inside the subset in 20 of 20. It kept the cache: 3,328 of 3,426 prompt tokens cached, as in the plain repeat. The ScaDS LiteLLM proxy refuses it on all ten models. The instruction-only restriction was followed by most ScaDS models in the adversarial cell, not by Llama-3.3-70B | [O] | The enforced arm runs on OpenAI. The instruction arm is the portable form |
| E4 | `10` section 12, R3 A3 | OpenRouter with GMICloud pinned accepts `allowed_tools` but does not enforce it (the excluded tool was called in 9 of 9). Only `auto` works there | [O] | Not a route for the enforced arm: a run would look enforced and not be |
| E5 | `17` section 5 (R1 part 3) and section 7 (P2 note) | OpenAI accepts at most 128 tools per request, so AppWorld's 457 definitions cannot be declared at once. AppWorld is the first-ranked P2 benchmark (provisional), with unit tests and dev and train splits for the loop | [O] | The catalogue is limited to 128 (section 4) |
| E6 | Manus, "Context Engineering for AI Agents" (stored `L/v5-manus-context-eng-20261022.txt:53-63`; `03` line 34) | "Mask, Don't Remove": tools are masked during decoding instead of removed, because "any change will invalidate the KV-cache" | [F] practitioner | The design principle P2 tests, in its vendor form |
| E7 | HYP-0018's basis EXT-0228 (Copilot) | A large visible toolset cost 2-5 points of resolution rate | [F] vendor | A small effect: below what a loop item can detect (`05` section 1) |
| E8 | LongFuncEval, arXiv 2505.10570 (abstract fetched 2026-11-08) | Function-calling performance fell 7% to 85% as the number of tools increased, across several long-context models | [F] paper, abstract only | Offering fewer tools may help, not only stay equal. HYP-0018 allows that |
| E9 | "How Many Tools Should an LLM Agent See?", arXiv 2605.24660 (abstract fetched 2026-11-08) | Downstream, Claude Sonnet 4.6 reached 93.1% with adaptive shorter lists against 87.1% with 5 tools always shown. It concerns which tools are shown, not restricting calls while definitions stay visible | [F] paper, abstract only | The literature found tests removal, not masking. P2's `enf` against `drop` contrast is what it lacks |
| E10 | R3 Part B (`17` section 5; RESULTS-R3-B on `v5-r3-part-b-results`) | AppWorld's own predictor subset against all 469 definitions on MiniMax-M3: no visible accuracy difference (means 47.5 and 46 of 57); 9 to 12 tasks changed between identical runs | [O] | Removal had no large effect on a similar task set. The run-to-run spread is large, so P2 needs repeats |

**Searches and fetches for this file** (INT-T-040; all on 2026-11-08):
1. Search "LLM function calling accuracy decreases with number of tools in prompt distractor tools study" (extended). It led to
   E8 and E9; a Linköping thesis and arXiv 2411.15399 were not fetched.
2. Search "allowed_tools tool_choice OpenAI restrict callable tools prompt caching keep tools list stable accuracy". It found SDK
   reference pages for the shape; a secondary blog on caching was not used, because E1 says the same first-hand.
3. Search "AppWorld leaderboard function calling agent gpt-5-mini test_normal task goal completion". No gpt-5-mini score was
   found, which is why section 8 has a pilot.
4. Fetches: E1 (after a redirect), E2 (after a redirect), E8, E9, and two redirect notices.

**Gap [I].** No source found measures accuracy when a subset is offered by masking (definitions visible, calls restricted)
against offering everything. The sources measure removal (E8, E9, E10) or the mechanism alone (E3). P2's contrast is new in the
places searched.

## 3. Route and models
- **Route: OpenAI Chat Completions.** It is the only route where the offering mechanism is enforced and keeps the cache (E3, E4).
  The `allowed_tools` shape is the Chat Completions one that R1 tested: `{"type":"allowed_tools","allowed_tools":{"mode":"auto","tools":[{"type":"function","function":{"name":...}}]}}`.
- **Models: two OpenAI models of different generations**, so a result is a range, not one model's (REQ-U22-14):
  - `gpt-5-mini`: AppWorld ships a config for it, `experiments/configs/simplified_function_calling_agent/openai/gpt-5-mini-2025-08-07-medium-reasoning/`;
  - `gpt-5.4-mini`: used in P5 part B.

  The served model id is recorded per call.
- **Settings:**
  - temperature 1.0 (the gpt-5 family's default, as AppWorld's own config uses);
  - reasoning effort `low` (AppWorld's config uses `medium`; `low` is chosen for cost and recorded);
  - `parallel_tool_calls` true; step cap 50; AppWorld's random seed 100; `raise_on_extra_parameters` true. All as AppWorld's
    template `simplified_function_calling_agent.jsonnet.j2`.
- **The open-weight route** (ScaDS, no enforcement) can carry only the `instr` arm against `all`. It is a free follow-on (P2b,
  section 10), not part of this design's cost.

## 4. Tasks, catalogue and subset [O]
- **Tasks:** AppWorld 0.2.0, dev split.
  - **Eligible:** the 30 dev tasks whose required apps all lie within the catalogue's apps. All 30 need Spotify only, in 10
    scenarios of 3 tasks each.
  - The test splits stay untouched (`17` section 7).
- **Catalogue:** the function-calling definitions of supervisor (6), spotify (92) and phone (30) = **128 tools**, OpenAI's
  maximum.
  - It is the same for every task and in a fixed order, so the prefix is shared across tasks.
  - Phone is a realistic app the tasks do not need.
  - 128 tools lies in R-mid on this route (D-01's break-even range, `04` section 1).
  - Size, as served through AppWorld's task API: 76,763 characters, about 19,200 tokens at 4 characters per token. R1 part 3's
    measured 80 to 145 billed tokens per AppWorld definition gives about 10,300 to 18,500 billed tokens.
- **Subset:** each task's ground-truth required APIs plus `supervisor__complete_task`: 6 to 10 tools (median 7).
  - It is an **oracle** subset, so P2 tests the mechanism at its best case, not a predictor (V5-R11's oracle ablation).
  - Realistic subsets, such as memory seeds that miss or over-include, belong to P1 and the end-to-end study.

## 5. Arms
| Arm | Declared `tools` | Offered | Prefix across tasks | Purpose |
|---|---|---|---|---|
| `all` | 128 | all (`tool_choice: auto`) | fixed | reference |
| `enf` | 128 | subset by `allowed_tools` (server-enforced) | fixed | HYP-0018 in its vendor form (E1, E6) |
| `instr` | 128 | all, with one sentence appended to the task message naming the subset (no enforcement) | fixed up to the task message | the portable form, for routes without enforcement (E3) |
| `drop` | subset only | subset | changes per task | removal, as AppWorld's predictor does: separates "fewer tools visible" from "fewer tools callable" (E9, E10) |

- **The instruction sentence:** "For this task, call only these tools: <names>. Do not call any other tool." It is appended to
  the task's user message, after the cached prefix of tools, system text and demos.
- **Everything else is AppWorld's own agent, prompt, demos and evaluator.** The harness changes only the declared list and the
  offer.

## 6. Measures and analysis
- **Primary: task success** from AppWorld's state-based evaluator (`world.evaluate()`, unit tests on the database; collateral
  changes fail a task). Paired by task, against `all`, per model and repeat.
- **Mechanism checks**, each of which could end P2 on its own (`05` P2):
  - cached share of prompt tokens per call, `enf` and `instr` against `all`; a clear drop is a cache break;
  - calls outside the subset: 0 expected in `enf`, counted in `instr` (compliance).
- **Secondary:** tests passed of total; steps and calls per task; tokens by class; cost per task (DPR-0006's components:
  uncached, cached and output tokens).
- **Run-to-run noise:** every arm runs twice. `all` against `all` gives the flip rate, against which an arm's difference is read
  (R2 B1: 5 of 57 flipped at temperature 0; E10: 9 to 12 of 57).
- **Statistics** (estimation-only reporting, INT-T-022):
  - the paired difference in successes with exact McNemar counts (all-only / arm-only) per repeat;
  - a 95% interval clustered by scenario (10 clusters of 3);
  - the lead adds no threshold.
- **What 30 tasks can show:** about 6 or more one-directional discordant tasks for p < 0.05. Only large effects show (`05`
  section 1).
- **Results committed:** counts per task id only (`p2_analyze.py`). AppWorld text, tool names and logs stay in the git-excluded
  `inputs/p2/local/` (AppWorld's licence requires encrypted public copies).

## 7. Cost estimate (assumptions stated; to be replaced by the pilot's numbers)
**Per task-run** (one task, one arm, one repeat):
- **Calls:** about 10 calls (range 6 to 20). AppWorld's agent took a median of 8 turns on dev in R1 part 4 (`17` section 5),
  with a cap of 50.
- **Prompt per call:** about 22,500 tokens (range 18,000 to 27,000): the 128 definitions (10,300-19,200), AppWorld's
  instructions and demos (about 4,200), and a growing history.
- **Cached share:** about 85% (range 60 to 95%). P5 part B measured 60-99.6% on warm OpenAI sessions; the tools and system
  header are shared across tasks.
- **Output including reasoning (effort low):** about 600 tokens per call (range 300 to 1,000).

| Model | per task-run, central (range) | Pilot: 5 tasks x `all` x 1 | Main A: 30 x 3 arms x 2 | Main B: 30 x 4 arms x 2 |
|---|---|---|---|---|
| gpt-5-mini | $0.025 ($0.008-0.10) | $0.13 | $4.5 ($1.4-18) | $6.0 ($1.8-24) |
| gpt-5.4-mini | $0.067 ($0.02-0.29) | $0.34 | $12 ($3.6-52) | $16 ($4.8-70) |

- Main A is `all`, `enf` and `instr`; Main B adds `drop`.
- **The ranges are wide** because steps and the cached share are not yet measured for these models on these tasks. So the lead
  proposes the pilot first.

## 8. Staged plan (each stage needs the human's word)
1. **Pilot** (about $0.50, stop $2):
   - 5 tasks from 5 different scenarios, arm `all`, both models, one run each.
   - It gives the floor and ceiling (`17` CH-0140: if `all` solves nearly every task, a gain cannot show; if it solves almost
     none, a loss cannot show) and the real tokens, steps and cached share.
   - Then the lead replaces section 7 with measured figures.
2. **Main A** (`all`, `enf`, `instr`; 30 tasks; 2 repeats; both models):
   - cost from the pilot's figures, with a stop at 1.5 times the estimate (as AUTH-028);
   - `drop` is added (Main B) only if the human wants the removal contrast.
3. **Report and revise** (`05` section 2: after each item the policy is revised before the next).

## 9. Harness and tests [O]
- **`p2_offering.py`:** standard library plus AppWorld's own package, run with `~/r3-work/venv/bin/python`.
  - It is modeled on the other agent's AppWorld driver (`~/r3-work/run_partb.py`), with a new AppWorld root and experiment name
    per run.
  - **Hook 1:** the declared list. **Hook 2:** the offer, `allowed_tools` for `enf` and the sentence for `instr`.
  - A live run refuses to start without `--max-spend` and `--price`. Stops: spend, call cap, HTTP 401/402/403, two task
    exceptions in a row.
- **Dry run:** 128 tools, 30 eligible dev tasks, subsets of 6 to 10. No call made.
- **Mock test:** a local fake OpenAI server, 2 tasks per arm, AppWorld executing and evaluating for real.
  - Recorded per arm: `all` sent 128 tools with `auto`; `enf` sent 128 tools with `allowed_tools` (10 names); `instr` sent 128
    tools with the sentence in the task message; `drop` sent 10 tools.
  - AppWorld executed the calls and its evaluator wrote its report (success, tests).
  - The cost formula reproduced the mock's token counts.
  - `p2_analyze.py` read all four runs.
- **Not yet tested:** a real OpenAI reply to the `allowed_tools` field from this harness. R1 tested the same shape with its own
  probe. The pilot will show it.

## 10. Limits and follow-ons
- **Oracle subsets only.** Spotify-only tasks, so phone is the only unneeded app. 128 tools is a single size. One benchmark.
- **Temperature 1.0 is the models' fixed default,** so the repeats matter.
- **P2b (free, our route):** `all` against `instr` on ScaDS GLM-5.3 with the same tasks. It needs a ScaDS flag in the harness (no
  reasoning-effort field) and is slow (B2 took 1 to 15 minutes per task). It is the open-weight half of HYP-0018.
- **Not covered:**
  - offering that changes during a session (V5's M2 seeds after a search; Anthropic's `tool_addition`/`tool_removal` are not on
    this route);
  - the bill (HYP-0018 claims none; it follows from the cached share).
