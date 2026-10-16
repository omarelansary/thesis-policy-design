# S4H closure addendum: focused near-neighbour adjudication (evidence packet E5 / E7)

- Date (UTC): 2026-10-16. Coordinator: Sonnet 5.5. Authority: D12 (user instruction of 2026-10-16). Inputs: stored texts only; zero searches, zero fetches, no earlier-thesis material, no 14 October material. No existing record was modified; suggested wording below is **not applied**.
- Labels: **F** stored text at a cited line; **I** interpretation; **Inf** inference; **U** unresolved. Line numbers refer to `text.txt` of the named stored source, or to the named record. This is one model's reading; no independent review was run (as instructed) and it is not human validation.
- Relationship vocabulary: direct prior art / partial prior art / contextual relevance / unrelated / insufficient evidence. A missing citation is not treated as evidence that a conclusion is wrong.

## 1. Result in brief

No current novelty, feasibility or contribution **conclusion** for C3, C5 or C6 needs to be changed. Two statements in the governing records are incomplete and merit a wording qualification (not a change of classification):

1. **C5 (cache axis):** the statements that cache regimes for exposure policies are untested and that prior art lies "in other domains" are too broad. Toollery appendix B.2 measures one full-library versus top-10-retrieval contrast under three cache regimes (single step).
2. **C3 (near-miss list):** the list omits two stored two-class comparisons: Toollery (single-step) and the CE-MCP study (trajectory-level, small catalogue). The literal gap statement still stands.

Dynamic ReAct, Prompt-Induced Waste, Notation Matters, the schema-compression study (TSCG) and CacheRouter are contextual or partial prior art that is consistent with the existing wording.

## 2. Exact current governing assertions (as written)

| Id | Assertion | Location |
|---|---|---|
| G-C3a | "Head-to-head with token categories not found, but near-misses exist (App. N at 150 tasks, Skill Blocks for skills); increment may be a reporting increment" | S4G brief L46; nearest prior art L72 |
| G-C3b | "Residual gap (bounded): independent, controlled head-to-head of at least two classes on one tool-catalogue workload with success, token categories and repeats. Several targeted searches (Stage 4, 4c) found none; near misses are listed." | S4D dossier L113 |
| G-C3c | "Unidentified quantity: comparable token accounting across client, provider-native and code-mediated classes (programmatic results are excluded from usage: r4-anthropic-ptc L1433), which is not an assumption but an open measurement problem." | S4D L111 |
| G-C5a | "Each axis has prior art in other domains (ETC, scaffold effect, token spend, on-device simulators); exposure-specific stability not found (3 queries)" | S4G L48 |
| G-C5b | "What remains untested (I): convention- and evaluator-stability of *tool-exposure policy* conclusions specifically; cache regimes for exposure policies that mutate the prefix; flips at the level of dominance relations." | S4F-PA L52 |
| G-C5c | "each axis has partial prior art in other domains (coding agents, deep search, on-device agents); the exposure-specific stability question was not found, but the existing results make a mixed outcome likely (invariance where cache share is small, divergence where it is large or where evaluators differ)" | S4F-PA L54 |
| G-C6a | "Component ablation exists in three uneven sources (one measured, compound step, F1; one unclear; one projected); controlled deterministic held-out version not found (2 queries)" | S4G L49; S4F-PA L68 |
| G-C6b | "Mechanism novelty is low by construction, so the contribution is controlled component evidence" | S4G L81 |
| G-C6c | "component evidence on which steps pay in tool catalogues is thin: stubs and detail levels exist in practice but are measured on one task or unmeasured" (corrected for skills in the quality addendum §2) | S4D L168 |

## 3. Source adjudication

Depth of reading is stated per source (section 5 lists what was not read).

### 3.1 Toollery (`s4b-wd-toollery-20261013`, arXiv 2609.22218v1, Huawei)
- **Question (F, L9-43):** can document-side query expansion ("manual" of generated user-intent queries) make top-k candidate compression recover the needed capabilities from libraries of hundreds to ~79K capabilities, without losing selection quality.
- **Mechanism:** training-free retrieval layer; final LLM sees only top-10 specifications. Not a staged-disclosure policy and no recovery path.
- **Evidence (F):** retrieval tables 1-3, 5-6 (SkillRouter 75 requests; BFCL-V4 live 1,053 and non-live 200 requests; 3,396 proprietary requests over 220 tools). End-to-end Table 4 (L250-258): BFCL live full-library prompt 457 tools, 84.1K input tokens, accuracy .770; raw top-10 .834; Toollery top-10 .837. **The caption (L260-266) states the full-library rows are DeepSeek V3.2 "scaling references" while the fixed top-10 rows use DeepSeek-V4-Pro**, so the full-library versus retrieval accuracy gap is across selectors. Appendix B.2 and Table 15 (L736-752, L782-791), BFCL replay: natural regime full library AST .787, hit rate .989, billed input cost $0.000749 versus Toollery .840, hit rate .144, $0.000819 ("billed-input-cost difference is inconclusive … $0.000070 per request (95% CI [USD −0.000524, USD 0.000462]) … no billed-input-cost advantage in this regime"); cache-suppressed $0.037879 versus $0.000951 (billed input −97.5%); forced-warm $0.000328 versus $0.000036. Appendix C Tables 16-17 (L861-897): multi-model accuracy against candidate-pool size 10-457, gold tool included by construction (L570).
- **Limitations (F):** single-step selection; "interactive multi-step agent workflows … remains future work" (L390-392); method authors' own baselines; the replay protocol, the selector used in Table 15 and the price basis are not stated in the B.2 text (U).
- **Relationship:** C5 **partial prior art** (in-domain, cache-regime axis only, one contrast, single step). C3 **partial prior art / near-miss** (two classes, success, input tokens, latency, billed input cost, hit rate; not independent, not trajectory-level, one workload family). C6 **contextual** (its ablations in Tables 9-12 concern retrieval components, not exposure steps). C1/C4 (outside this task's scope): Tables 16-17 are a single-step pool-size sweep with the gold tool present; noted, not adjudicated.

### 3.2 Prompt-Induced Waste in Coding Agents (`ch-s2-0176-2608-01347-20261012`, arXiv 2608.01347)
- **Question (F, L22 and §1-2):** what determines cost per successful task in coding agents: prompt wording, inference effort, harness.
- **Mechanism / evidence (F):** preregistered paired design, 4,644 valid runs, 24 deterministic coding tasks, six open-weight models and Claude Sonnet 5, two harnesses plus a DeepSeek-Harness extension (75 runs, five tasks). Harness gap 5-30× cost per success at comparable success; effort control saves about 19% (full stack 27%) in Claude Code but about 75% (82%) in the dsh extension (§6.1, Table 3, L280-320: "the benefit of effort control depends on the harness default and request policy").
- **Limitations (F, L552-596):** small bounded tasks, high success ceilings, one closed model in the extension; "dsh capabilities such as Code Mode … were not factorially varied" (L590-591). Tool-schema exposure is named as a harness factor (L510-511) but is **not manipulated**.
- **Relationship:** C5 **contextual relevance**, equivalent to the other-domain partial prior art already cited for the harness-dependence axis (scaffold effect). C3, C6 **unrelated** (no exposure manipulation). Its §9 list of what an efficiency evaluation must retain (success, cost per success, system-prefix and tool-schema surface, uncached input, cache writes, cache reads, turns) is consistent with C5's token vector.

### 3.3 From Tool Orchestration to Code Execution: A Study of MCP Design Choices (`r2-ce-mcp-2602-15945-20261011`, arXiv 2602.15945v1)
- **Question (F, L12-45):** compare traditional (context-coupled) MCP agents with code-execution MCP (CE-MCP) agents on efficiency, task quality and security; the security analysis (MAESTRO, 16 attack classes) is the paper's main contribution.
- **Evidence (F, L378-480, L828-850):** MCP-Bench, 10 servers (1-26 tools each, Table 3), 34 tasks (two single-server tasks per server, ten two-server, four three-server; L412-415), three GPT models (L387), metrics: token usage "input, output, and total" (L403), turns, end-to-end time, MCP-Bench task fulfilment scored by "three independent GPT-4o-based LLM judges" (L432). Reported direction: CE-MCP reduces tokens, time and turns; task fulfilment "comparable … for most configurations", lower for a subset of three-server tasks (L462-476).
- **Limitations (F, I):** results are in figures only; the extracted text carries no numbers, so magnitudes are **not recoverable here (U)**; catalogue exposure is 1-3 servers per task, not a large catalogue; no repeats or intervals stated; LLM-judged; the paper states it is "neither strictly superior nor inferior" (Conclusion, L744-760); no cache or billed-cost accounting.
- **Relationship:** C3 **partial prior art / near-miss** for the pair (traditional full-schema, code-mediated) on one workload with success, input/output tokens and turns at trajectory level. C5 **contextual** (token and latency, no cost). C6 **contextual** (post-query discovery is one stage of the CE-MCP workflow; no ablation).
- **Bearing on G-C3c (I):** both arms are run in the authors' client harness and token usage covers all model invocations, so for **client-side code mode** token accounting was not an obstacle in this study; the "open measurement problem" in G-C3c is therefore specific to provider-native programmatic calling and server-side mechanisms, as S4G L75 already says. Sandbox compute is not counted.

### 3.4 Dynamic ReAct (`s4-dynreact-2509-20386-20261013`, arXiv 2509.20386v1)
- **Question and mechanism (F, L9-24, L144-360):** how a ReAct agent can use very large MCP tool sets: five designs from direct top-k search, to an LLM-constructed query meta-tool, to `search_tools` + `load_tools`, hierarchical `search_apps`, and a fixed tool set with `get_tool_info` + `call_tool` (L340-362).
- **Evidence (F):** the only quantitative evidence is retrieval Top-5/Top-10 on a "diverse test suite" over a proprietary registry (L476-498, Table 6 L540-547). The percentages (40, 48, 56, 60 Top-5) are consistent with 25 test queries (Inf; the number is not stated). The "50%" is a relative Top-5 improvement from 40% to 60% (L498).
- **Limitations (F):** the abstract's claim that the approach "reduces tool loading by up to 50% while maintaining task completion accuracy" (L21-22) and the conclusion's "improvements in both efficiency and accuracy compared to static tool loading approaches" (L602) have **no corresponding task-completion, tool-loading or static-loading measurement in the text**; architecture pros and cons, including "Caching Efficiency" (L355) and "Performance Degradation" in long conversations for the fixed tool set (L360), are assertions without data; proprietary registry.
- **Relationship:** C3 and C6 **contextual relevance** (mechanism and class descriptions for deferred/hierarchical/fixed-surface designs; consistent with "mechanism novelty is low by construction"). Its qualitative statements must not be cited as evidence of effects. C5 **insufficient evidence**.

### 3.5 Notation Matters (`s4b-wd-notationmatters-20261013`, arXiv 2605.29676v2)
- **Question (F, L12-40):** do token-optimised serialisations of tool schemas, invocations and results (TOON, TRON) keep accuracy inside agentic loops.
- **Evidence (F):** four benchmarks (BFCL, MCPToolBench++, MCP-Universe, StableToolBench), five open-weight 17B-32B models; TRON up to 27% fewer tokens with accuracy within 14 pp, TOON up to 18% at ~9 pp; reasoning configurations lose 27-44 pp on BFCL under TRON (Fig. 5 caption, Table 3-4 L955-1045); effects vary by benchmark more than by format.
- **Limitations (F, L534-560):** schema and result compression were compressed together and "not separately measured"; open-weight models only; no frontier models; single token metric.
- **Relationship:** C6 **partial prior art for the lesson only** (a token-saving component can lower accuracy and the effect is benchmark- and model-dependent), for a content-format step rather than a staged-exposure step. Content-level reduction is already scoped out by D9. C5/C3 **contextual / unrelated**.

### 3.6 Tool-Schema Compression for agentic RAG (`s4b-wa-schemacompress-20261013`)
- **Question and evidence (F, L16-60):** schema compression (all tools kept, schemas compressed) versus JSON schemas when retrieval chunks compete for a fixed context; 14 models, 6,566 calls, 28 synthetic tool definitions, budgets 8K/16K/32K; binary enablement at 8K (average exact-match 2.6% → 23.1%), no effect at 32K; JSON schemas overflow 200K at ~494 tools in a synthetic sweep.
- **Limitations (F, L415-425, L442):** synthetic benchmark, one compression profile, frontier test with synthetic distractors, QA exact match rather than task trajectories.
- **Relationship:** C6 **contextual** (a step's effect depends on the budget regime, which supports the regime factor already in S4G L83). C3, C5 **unrelated**.

### 3.7 CacheRouter (`s4-cacherouter-2608-22708-20261013`, arXiv 2608.22708v1)
- **Question and mechanism (F, L31-46):** how to keep progressive disclosure compatible with prompt caching: a fixed core tool set in the main request and a router sub-model channel for the rest.
- **Evidence (F):** prototype on 55 functional queries and a 30-turn dialogue; token-level cache hit 90.99% and 95.2%, input cost about 12.0% and 8.0% of a no-cache baseline (L36-46).
- **Limitations (F, L1804):** "The scale of this validation is deliberately modest … evidence of feasibility rather than … a performance benchmark"; no comparison arm against other exposure policies and no task-success comparison (STAGE4_PRIOR_ART_COMPARISON §5.2 already says so).
- **Relationship:** C5 **contextual** (a stable-prefix design with measured hit rates; does not test conclusion stability). C6 and C3 **contextual** (a class/mechanism that generalises progressive disclosure). **Insufficient evidence** for any comparative claim.

## 4. Claim-level findings

| # | Governing assertion | Evidence | Finding | Correction needed? |
|---|---|---|---|---|
| F-1 | G-C5b "cache regimes for exposure policies that mutate the prefix" remain untested; G-C5a/G-C5c prior art is "in other domains" | Toollery B.2 / Table 15 (L736-752, L782-791): full library (stable prefix, hit .989) versus top-10 retrieval (changing prefix, hit .144) under natural, suppressed and forced-warm regimes; token −97.5% but billed-cost difference "inconclusive" (natural), −97.5% (suppressed) | One in-domain, single-step, two-policy instance of cache-regime dependence exists. The question as defined for C5 (several policies × conventions × evaluators × horizon, trajectories) is still not covered; the S4F-PA expectation of divergence where cache share is large is supported by this instance | **Wording qualification, not a change of classification:** "untested" should read "untested beyond one single-step replay (Toollery B.2)" and "in other domains" should read "mostly in other domains". Conclusion "exposure-specific stability not found" stands |
| F-2 | G-C3a / G-C3b near-miss list (App. N, Skill Blocks, ToolMenuBench, MemTool, compgateway, vendor claims) | Toollery Table 4 / 15; CE-MCP §6 (L378-480, 34 tasks, 3 models, input/output tokens, turns, judge-scored fulfilment) | Both are two-class comparisons with success and token measures that the list does not name. Neither is independent (Toollery) or at catalogue scale with repeats and token categories (CE-MCP: 1-3 servers, figures only). The literal gap statement stands; "increment may be a reporting increment" is reinforced | **List completeness only:** add the two as near-misses. No change to the novelty classification or contribution |
| F-3 | G-C3c "unidentified quantity … code-mediated classes" | CE-MCP counts input/output/total tokens for both agents in one harness (L403) | Accounting is straightforward for client-side code mode; the open problem is provider-native programmatic calling | **None required** (S4G L75 already scopes it); optional clarification |
| F-4 | G-C6a "three uneven sources" | Notation Matters (token-saving component with accuracy cost; content format), TSCG (budget-dependent effect), CacheRouter (feasibility), Dynamic ReAct (unmeasured designs) | "Three" is a selection among sources that vary a token-saving component; none is a controlled, deterministic, held-out ablation of staged exposure, so the absence claim stands | **None required**; "at least three" would be more exact |
| F-5 | G-C6b / G-C6c mechanism novelty low; component evidence thin | Dynamic ReAct, CacheRouter, Executor-type designs; Dynamic ReAct's claims lack data | Consistent. Dynamic ReAct's abstract-level efficiency and accuracy claims are not supported by its own text and should not be cited | None |
| F-6 | G-C5a harness-dependence prior art in other domains | Prompt-Induced Waste §6 and §9 | Same type as the scaffold effect (interaction of an intervention with the harness); tool-schema exposure not manipulated | None |

No feasibility claim is affected (the vehicle statements in S4F/S4G do not depend on these sources). No candidate-contribution statement requires reconsideration. Nothing here selects, ranks or generates a candidate or question.

## 5. Unresolved limitations

1. **Depth read.** Toollery: main text and appendices A-D read. Dynamic ReAct: whole text. CE-MCP: abstract, §1-4, §6.1-6.2, §8.3, Table 3; the security sections were not read. Prompt-Induced Waste (2,001 lines): abstract, §1-2, §6, §9, §11 and keyword hits; appendices A-P not read. Notation Matters: abstract, limitations, Tables 3-4; methods not read in full. TSCG: abstract, design, limitations; Tables 1-6 not examined cell by cell. CacheRouter: abstract, introduction, evaluation framing and limitation sentences; the eight experiments were not read cell by cell.
2. **CE-MCP magnitudes (U):** the stored text has no figure values; the direction is the authors' statement only.
3. **Toollery B.2 (U):** replay protocol, selector in Table 15 and price basis unstated in the text read; accuracy differences between full-library and retrieved rows in Table 4 are cross-selector.
4. **Layout:** two-column PDF extraction interleaves some tables; values quoted above were matched to prose or to rows I could attribute unambiguously.
5. **Inference flagged:** the 25-query count for Dynamic ReAct.
6. **No independent review and no human validation**, as instructed.

## 6. Closure

S4H is closed for selection purposes. The wording qualifications in F-1 and F-2 are offered for the user's decision; they were not applied to any existing record, and neither changes a candidate's classification, novelty status, feasibility or contribution description.
