---
id: "FND-0014"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-100
evidence: ["EXT-0149", "EXT-0154", "EXT-0164", "EXT-0166", "EXT-0173", "EXT-0175", "EXT-0178", "EXT-0179"]
---

# Batch 2c: scaffolding paper, ToolMenuBench, GIST-CMTF (AUTH-016 ledger batch 2)

Extractions used: 8 of 9 (EXT-0179 is lines 262-330, chosen after a view-only look, `--no-write`, at lines 220-330). Line numbers below are source lines as given in the extract headers; for EXT-0179 and EXT-0178 I cite the passage text, not an exact line, where I could not compute it. Source texts are PDF-to-text conversions (two-column text interleaved; tables ragged). All statements about papers are [F] "the source says", not verified truth.

## Row C-E01/E07: scaffolding paper (r4-scaffolding-mcp-vs-cli, arXiv 2608.08654v1, retrieved 2026-10-11)

**Verdict: ANSWERED for the three asked items; cache-share is given only for the command-line arm (Table 2), not per MCP delivery method in the ranges read.**

1. Two corrections (EXT-0149, source lines 296-330).
   - [F] Correction 1: "Our verification originally checked five conditions rather than four. The fifth compared each pull request against a particular issue number, but the routine that reset the repository between runs assigned a new issue number every time, so no run could ever satisfy it. All completion figures in this paper are computed over the four conditions that are actually satisfiable."
   - [F] Correction 2: "The second correction was a configuration error of our own. In one scaffolding's configuration file the MCP server's credential was written as a variable name that the scaffolding expands only in a bracketed form, so the server started with the name of the credential in place of its value and was refused by the API on every call it made." Effect: "which stood above forty per cent before this correction and stands at 12.9 with the cell measured properly" (wasted-cost share, Section 4.4; the unit after 12.9 is not printed in the extract, presumably per cent [U]). The affected cell was repeated three times and "completes on all three".
2. Cache-share figures (EXT-0154, source lines 560-620). Condition: Table 2, **command-line arm only, "No MCP catalogue was attached in any of these runs"**; "Runs" counts completed runs; "'Cache' is the median share of input tokens billed at the reduced cached rate"; cost is a median over each row's own model mix; "Claude Code's rests on two completed runs".

| Scaffolding | MCP client | Runs | Tokens | vs pi | Cache | Cost |
|---|---|---|---|---|---|---|
| pi | no | 4 | 14,660 | x1.0 | 88% | $0.0124 |
| Tau | no | 4 | 16,459 | x1.1 | 77% | $0.0149 |
| Codex | yes | 4 | 82,378 | x5.6 | 80% | $0.0352 |
| Hermes | yes | 3 | 83,954 | x5.7 | 93% | $0.0922 |
| opencode | yes | 3 | 137,800 | x9.4 | 93% | $0.0909 |
| qwen-code | yes | 4 | 297,649 | x20.3 | 88% | $0.1666 |
| Claude Code | yes | 2 | 410,797 | x28.0 | 98% | $0.7251 |

   (The Tokens column is described in the same section as input tokens: "the analysis is expressed in input tokens"; the exact column heading text is just "Tokens".) Other figures in the same range: "Output ... varies from 824 to 1,367 tokens across the seven scaffoldings ... while input varies by a factor of 20"; output share of modelled cost "24 per cent for pi and 25 per cent for Tau down to 2.9 per cent for qwen-code and 2.6 per cent for Claude Code"; a 27B open-weight model "consumed 17,416 tokens" under Tau vs "2,418,828 tokens across 108 tool calls — 139 times as much" under Codex with the MCP server attached. My check: 2,418,828 / 17,416 = 138.9, consistent with "139".
3. Table 4, the two pricings (EXT-0164, source lines 700-735). [F] "Table 4 prices the same completed runs twice: once at list rates, and once applying a ninety per cent discount to cached input, which is close to what the hosted providers in this study charge."

| Arm | Runs | Tokens | Cost, list price | Cost, cached discounted |
|---|---|---|---|---|
| Command line | 16 | 119,916 | $0.0934 | $0.0287 |
| MCP | 16 | 187,954 | $0.1044 | $0.0345 |

   Caption: "Cost of the two arms under two billing assumptions, completed runs only, across the five MCP-capable scaffoldings. Local models are priced counterfactually throughout." Paper's reading: "the MCP arm consumed twice the tokens and cost about ten per cent more at list price, or half as much again once cached input is discounted. Neither margin means much, because the completed runs in the two arms are not drawn from the same mix of models, and the per-token prices of those models differ by a factor of twenty."
   - My arithmetic [mine, not the paper's]: tokens 187,954 / 119,916 = 1.567; list cost 0.1044 / 0.0934 = 1.118; discounted cost 0.0345 / 0.0287 = 1.202. So from the table as extracted: tokens x1.57 (paper text: "twice"), list +12% (paper: "about ten per cent"), discounted +20% (paper: "half as much again", which would be +50%). The prose and the table do not match closely. Possible causes (not determinable here): the text refers to a different aggregate, the table is median-based, or an extraction error [U]. Implied discounted/list ratio: 0.0287/0.0934 = 0.31 and 0.0345/0.1044 = 0.33 (my arithmetic).
   - Preceding text (same range): the MCP-vs-CLI difference is described as a bimodal distribution; "The quantity is not stable enough to have a single value."

**What the passages do NOT show:** how Table 4 splits input into cached/uncached; the cache share of the MCP arm (Table 2 is CLI-only); whether cached share is attributable to tool definitions specifically; the model mix per row; any statement of provider-side minimum cacheable length or TTL in these ranges. The preceding sentence of the Table 4 section says "an MCP catalogue is identical on every request, so it should cache well" ([F] expectation stated by authors, not tested in the ranges read).
**Limits:** one preprint (v1); single task (pull-request task, per context lines); small run counts (2 to 4 per row, 16 per arm); local models priced counterfactually; medians over different model mixes; 90% discount is an assumption "close to" provider pricing.
**[O] relevance to ledger C-S03 (cache of tool definitions):** Table 2 cache shares (77% to 98%) are shares of all input tokens in CLI-arm runs; they say nothing specific about tool-definition caching. Table 4 is a computed re-pricing under an assumed 90% discount on cached input, not billed cost. **[O] relevance to C-S01 (share of tokens due to schemas):** the only schema-related statement in these ranges is the lead-in to Section 4.3 ("The proxy recorded how many tool schemas each scaffolding included in each request"), whose figures lie beyond the range read. **[I] effect on ledger row:** can cite both corrections and Table 2/4 numbers with the conditions above; should flag the prose/table mismatch in Table 4 discussion as reported by the steward.

## Row C-R03/CMTF: ToolMenuBench and GIST-CMTF provenance of state, goal, contracts

**Verdict: PARTLY.** Both papers describe the task structure; neither range read says how the contracts were produced; for GIST-CMTF the goal-inference method is described but its implementation (what model/prompt, what inputs in the experiments) is not in the ranges read.

### ToolMenuBench (r3-toolmenubench; EXT-0166 lines 364-425, EXT-0173 lines 426-520)
- [F] "Each task is defined by a user request, an initial symbolic state, a goal state, and a gold tool trajectory." (EXT-0166). "The gold trajectory is held fixed while distractor tools are added to increase menu size." Registry sizes 25, 100, 250.
- [F] "At each decision step, the model receives the user task, the current symbolic state, and the schemas and descriptions for the tools exposed by the filtering method."
- [F] "We use a deterministic mocked tool environment. Each selected tool either updates the symbolic state according to its defined effects or produces a failure observation when its requirements are not satisfied."
- [F] Design: "26,460 end-to-end agent executions: seven evaluation settings, seven model backends, three tool-menu sizes, six filtering methods, and thirty tasks for each condition." My check: 7x7x3x6x30 = 26,460.
- [F] Methods: all-tools, keyword top-5, keyword top-10, state-aware, full causal path, CMTF. "learned-contract CMTF" is listed as an extension left "to future work" (EXT-0166), implying the reported CMTF uses non-learned contracts [I]. The extract does not say who wrote the contracts.
- [O] In this benchmark the goal state and gold trajectory are part of the task definition, so CMTF as evaluated receives the task's goal state; the text read does not say whether CMTF receives the annotated goal state directly [U].
- Results (EXT-0173), conditions: main mixed-distractor setting, "success is reported in percent, average visible tools are measured per decision step, and the remaining metrics are averaged per task execution". Table I: All tools 32.1% success, 125.00 avg visible, 56,062 tokens; Keyword top-5 22.1 / 4.80 / 3,200; Keyword top-10 22.4 / 9.54 / 5,356; State-aware 24.0 / 25.95 / 13,522; Full causal path 24.0 / 26.24 / 13,697; CMTF 85.7 / 0.99 / 1,125. Text: "a 53.6 percentage-point absolute improvement in success and roughly a 98% reduction in token usage". My checks: 85.7 - 32.1 = 53.6; 1 - 1,125/56,062 = 0.980. Table II (ragged in extraction): CMTF best in all six targeted settings, success 84.4% (premature) to 90.6% (text says near-duplicate; table rows are misaligned in the extract, so the row-to-value assignment cannot be read reliably), about one thousand tokens.
- [O] The "tokens" figure counts tokens "per task execution" with menus of schemas and descriptions; the tokenizer and what is counted beyond that are not stated in these ranges. Also bears on C-S01: all-tools 56,062 tokens at 125.00 visible tools averaged per step is a per-task figure, not a per-request figure (division not attempted, step counts not given).

### GIST-CMTF (r2-gist-cmtf-2606-16813-20261011; EXT-0175 lines 100-220, EXT-0178 lines 40-100, EXT-0179 lines 262-330)
- [F] Tool contracts (EXT-0175): "ti = (di, Ri, Ei, ci, ρi), where di is a natural-language description, Ri is the set of required state variables, Ei is the set of produced state variables, ci is an optional cost, and ρi is an optional risk label." "Recent contract-learning work studies how these preconditions, effects, and risk annotations can be inferred from tool names, descriptions, schemas, documentation, and execution traces [8]." This is a pointer to other work; the text read does not say the paper's own experiments use inferred contracts.
- [F] Standard CMTF assumption (EXT-0175): "Existing causal filtering methods typically assume that the user's request has already been mapped to a symbolic goal state." "Standard CMTF assumes that the target goal state g ⊆ X is known."
- [F] Goal inference (EXT-0175): "We therefore define a goal-state inference module H that maps the user request, current state, and tool-contract context to a ranked set of candidate goals: H(q, st, T) = {(g1,p1),...,(gk,pk)}". Inputs: user request q, current symbolic state st, tool library T (with contracts). "The candidate goals are drawn from the same symbolic vocabulary used by downstream causal filtering" (view-only lines 220-330, same text as the start of source range; also EXT-0178: GIST-CMTF "predicts candidate symbolic goal states" given "a natural-language request, current task state, and tool contract graph"). Ambiguity rule, simplest implementation: A = I[p* < tau or (p* - p(2)) < delta], with thresholds tau (confidence) and delta (margin) unspecified in the ranges read.
- [F] Evaluation tasks (EXT-0179): "Each task consists of a natural-language user request, an initial symbolic state, a set of candidate symbolic goals, an intended goal when one is specified, and a downstream gold tool path after the goal is known." Suite: 120 tasks (40 explicit, 40 ambiguous, 30 missing-variable, 10 clarification-required), "evaluated under six filtering methods and seven model backends, yielding 5,040 total runs" (my check: 120x6x7 = 5,040). "We build on the controlled multi-step tool-use setting used in prior causal tool-filtering work, where tools have precondition-effect contracts, execution is deterministic, and task state is represented symbolically [7]." "Gold-goal CMTF: applies CMTF using the annotated intended goal. This serves as an upper-bound causal filtering baseline." Metric: "Wrong-tool calls: number of selected tools that differ from the gold next tool for the intended goal."
- Abstract numbers (EXT-0178): GIST-CMTF 97.0% task success vs 80.1% top-goal CMTF and 82.9% semantic-goal CMTF; wrong-goal execution 19.4% (top-goal) and 16.7% (semantic-goal) down to 2.5%; seven models, six methods, 120 tasks.

**What the passages do NOT show:** (a) who or what authored the tool contracts in either benchmark, and whether they are derived from the same annotations as the gold trajectories; (b) in ToolMenuBench, whether CMTF receives the annotated goal state at run time; (c) in GIST-CMTF, how H is implemented in the experiments (LLM, prompt, or rule-based) and whether "candidate symbolic goals" in the task record are given to H or only used for scoring; these lie in ranges after source line ~330 (GIST) and before line 364 (ToolMenuBench), which I did not read. **[U]** whether a deployed policy would have access to what the benchmark supplies.
**Limits:** controlled mocked environments with deterministic execution and symbolic state; both are preprints; the benchmark tasks and the GIST suite are small and author-built; seven model backends include models whose names are not independently checked here.
**[I] effect on ledger row:** statement "How CMTF obtains its causal path is unverified" stays partly open. Narrowed: in both papers the evaluation tasks come with an initial symbolic state, gold trajectory and (GIST) annotated intended goals plus a "Gold-goal CMTF" upper-bound baseline; tool contracts are precondition/effect specifications whose origin in the experiments is not stated in the ranges read.

## Not read
- r4-scaffolding-mcp-vs-cli Section 4.3 onward (catalogue delivery method, schema counts per request) and Section 2.5/2.8.
- r3-toolmenubench lines before 364 (contract/state generation, if described) and after 520.
- r2-gist-cmtf lines 330-667 (metrics definitions, results, any statement on H implementation) and lines 1-40.
- No 9th extraction used.
