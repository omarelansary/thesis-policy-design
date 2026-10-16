# Stage 2 final integrated landscape report

- Date (UTC): 2026-10-12. Authority: `decisions/D2-stage2-closure-contract.md`. Supersedes `stage-reports/STAGE2_INTEGRATED_LANDSCAPE_DRAFT-20261012.md` (pre-challenge; preserved unchanged). Challenger reports: `audits/A45`, `A46`, `A47`; disposition: `audits/A48-challenger-objection-disposition-20261012.md`. Closure audit and gate verdict: `stage-reports/STAGE2_CLOSURE_AUDIT-20261012.md`.
- Scope and labels as in the draft. Research target (brief §0): reduce model-visible input tokens for accessing large tool catalogues while maintaining end-to-end task performance and counting all discovery, selection and execution overhead; the target's validity is itself under investigation; no architecture is favoured. **[F]** finding reported by a source at the stated verification level; **[O]** coordinator observation; **[I]** interpretation; **[U]** uncertainty; **[S]** speculation. "None found" means under the stated providers, queries, caps, window (2023-01-01 to the search date, bounded pre-2023 prior art) and English only. Identity or metadata matches are not claim support.
- This is a landscape report, not a recommendation. Stage 2 is INCONCLUSIVE (see the closure audit).

## 1. What the evidence supports (bounded)

1. **[F] The mechanism space is broad; every pre-specified family has sources.** 208 included mechanism-family source groups exist; 75 have a full-text or official-documentation basis and 68 of those a recorded locator (L2 table). Most remaining sources are abstract-, snippet- or metadata-level.
2. **[F][I] No retrieval method wins universally, and expansion is not uniformly beneficial.** On ToolRet, no-instruction averages show BM25 (22.32 N@10) close to several dense baselines (16.30–23.02) while specialised embedders/rerankers score higher (33.83–35.51); the "<35% completeness" statement holds for those averages only, and the paper also says "<45%". Re-Invoke shows dense retrieval beating BM25 on all five of its datasets, HyDE hurting both sparse and dense retrieval on most datasets, and Re-Invoke's own method improving both (pass rate 56.07 vs 52.13/52.63 end-to-end). Weller et al. report expansion gains shrinking as retriever strength rises. A1 ("dense always beats keyword") and A5 ("expansion helps, established") are supported only conditionally.
3. **[F] Deferred / on-demand / progressive tool exposure is a shipped, documented provider and client feature** (Anthropic, OpenAI, Claude Code, MCP client guidance, AgentCore, Spring AI). Documentation itself states that discovery adds a step and that changing the loaded tool set invalidates the cache. Independent measurements of these products' end-to-end effects are not in the stored evidence. Prior-art dates are not established.
4. **[F] Token-reduction numbers measure different things.** Examples: a constructed synthetic-harness schema count (Tool Attention; success/latency/cost projected, and the paper claims "in our experiments" observations although no live run was made); definition-footprint calculations in vendor posts (Cloudflare 99.9% against a hypothetical server; Speakeasy example, whose own table shows static cheaper at 40 tools for a simple task); an observed 38.4% cut of estimated tool-output tokens that coincided with +6.8% billed cost and +5.1% cost per success in one 103-task campaign, concentrated in few tasks, with a nine-gate treatment and possible cache carryover.
5. **[F] In the tested filters and settings, reduced exposure lowered task success relative to full or oracle exposure** (ComplexMCP −16 to −42 points depending on model and retrieval condition, one MiniLM retriever; ToolMenuBench keyword top-5 −10 points on 30 tasks per condition with no uncertainty; LiveMCPBench k=1 vs k=5). But a different filter in ToolMenuBench raised success by 53.6 points, Re-Invoke's retrieved tools beat the reference toolset, and tool count does not harm monotonically (small related-tool additions −1 to −8% relative; MCPVerse Standard ≈ Oracle but Max-Scale −18 points for one model). A6 ("~50% cut is free in most production systems") and A13 ("100→60 is safe; names-only keeps accuracy") are not supported as general. No evidence in the stored set establishes production prevalence.
6. **[F][I] Evaluation noise and validity are large relative to many reported effects.** 18.5% of audited benchmark tasks showed evaluator–human disagreement; 23 LiveMCPBench reruns spanned 57.9–76.8% (SD 5.4 points). Single-gold-path scoring can mis-score valid alternatives. Cost is rarely reported; where reported it is inconsistent in places. Cross-benchmark pooling is not supported.
7. **[F][I] Caching changes the relation between exposed tokens and billed cost, and the schema/prefix block can dominate cost.** Provider documentation prices cache reads far below uncached input; a multi-provider study reports 41–80% cost reductions from cache-aware strategies (with an internally inconsistent 500-token passage and no quality outcome); in a 1,212-session corpus the harness base (system prompt + tool definitions, not separated) carries 74.7% of cost. One bill-based study found prefix caching removing about 61% of the bill with the Claude Code fixed prefix at roughly 16–20k tokens, confounded by turns. Decode-time shares from self-hosted serving are latency evidence, not billing evidence, and are not used as cost evidence here.
8. **[O][I] None found under bounds: a controlled study combining catalogue filtering or disclosure with both task success and provider-billed cost per successful task.** Nearest stored work and why each falls short: Tool Attention (projected success and cost, synthetic harness); Token Reduction Is Not Cost Reduction (tool-output compression, billed cost and cost per success, no schema filtering); ProMCP (profiling, uncontrolled deferred-loading topology with a quality audit, no billed cost); the scaffolding study (on-demand delivery 70,836 vs full-catalogue 216,986 median input tokens over completed runs, a factor of 3.1, one task, confounded by scaffolding and model, modelled prices); ToolMenuBench/GIST-CMTF (success and tokens in synthetic mocked environments, no cost); Speakeasy (vendor tokens and cost, handful of runs, no accuracy validation). Because F1, F2 and F6 stopped at their caps, this negative is INCONCLUSIVE and says nothing about novelty.

## 2. L1 mechanism taxonomy (summary)

The full table with sources and levels is draft §2; challenger-driven corrections: Tool-DC is a selection method with extra calls, not a long-context alternative; categories c (schema compression) and h (deduplication) remain abstract-level; DADL's 142× is a computed counterfactual with no task evaluation (vendor author); the Missing Memory Hierarchy result is one task; ToolTree's scale test sits behind a retriever shortlist and its model labelling is inconsistent in the source.

| Cat. | Mechanism | Evidence level | Key limit |
|---|---|---|---|
| a Retrieval/filtering | lexical, dense, hybrid, rerankers, LLM-based, learned retrievers | full text for ToolRet, Re-Invoke, RAG-MCP, ToolMenuBench; leads at abstract | success loss vs full exposure in tested filters; gold-label incompleteness |
| b Tiered/lazy exposure, meta-tools | defer schemas, search/describe/execute | official docs, vendor posts | added step; accuracy for complex workflows unvalidated; efficacy unmeasured independently |
| c Description/schema compression | rewrite or re-encode | abstract | unverified |
| d Query expansion | intents, synthetic queries, HyDE, bridges | full text | conditional benefit; extra LLM calls |
| e Hierarchical routing/sub-agents | trees, clusters, delegation | full text (ToolTree, DTDR, ReDel background) | scale confounded; token metric undefined |
| f Training-based selection | virtual tokens, trained selectors | full text (ToolGen) | no full cost accounting; maintenance |
| g Code execution/programmatic | search/execute, generated code | full text (CE-MCP, vendor) | synthetic; security tested 4/16 classes; vendor numbers |
| h Dedup/merge/curation | merging, curated sets | abstract | unverified |
| i Caching/provider features | prefix reuse, ordering, demand paging | official docs, full text | tool changes invalidate cache; no quality outcome |
| j No intervention/long context | pay for larger context | official docs | not tested as an arm |
| k Workload accounting (emerged) | billed cost, cache, turns, success | full text | single harness/provider; no filtering arm |

## 3. L2, L3 (criteria 4, 5)
L2 extraction table: `evidence/stage2/L2-extraction-table-20261012.md` (generated; 68 of 208 mechanism-family rows meet full-text-basis plus locator; others marked). L3 benchmark table: `audits/A12-F6-benchmark-evidence-table-20261011.md` (11 stored F6 sources), with these challenger-driven corrections: MCPVerse reports only definition sizes (its Table 4 conflict is in success rates), and the MCPVerse Table 2 has duplicated cells; LiveMCPBench tokens 6.07M (table) vs 6.70M (prose) stay unresolved; benchmark realism: 48.8% is a single-probe lower bound on a 30.7% transport slice of the registry. Outcome definitions differ across benchmarks and are not pooled.

## 4. L4 assertion map (criterion 6), revised

| Assertion | Disposition after challenge | Notes |
|---|---|---|
| A1 dense always beats keyword | Not supported in the "always" form | ToolRet, Re-Invoke (dense > BM25 on its 5 datasets), SkillSeek (skills, not tools) |
| A3 keyword fails on vague queries; semantic insufficient | Qualified | vagueness degrades retrieval; universal forms unsupported |
| A4 agents rely on and can be misled by names/descriptions | Direction supported; magnitude and mechanism unverified | Tool Preferences (17 models, preference not accuracy, ordering bias; full text now read), MCPTox and MSB (include rows better supported; selection steering vs invocation of alternative legitimate tools differs), 34 abstract-level rows. Coverage gap: Shi et al. (NDSS 2026) and four security-flagged excludes without include rows not examined |
| A5 expansion helps and is established | Conditionally supported | see §1.2 |
| A6 ~50% tool-token cut costs no accuracy in most production systems | Not supported as general; prevalence not established | §1.5 |
| A7 "Executor" is the described product | Candidate match; referent unresolved | source code confirms integrations listing, search and invoke and a default code-execution mode; no measured savings |
| A9 partial disclosure exists in someone's documentation | Prior-art examples exist; source unidentified | vendor docs; dates not established |
| A12 selection does not transfer across models | Mixed | scaffolding study is one task, not a full crossing |
| A13 100→60 safe; names-only keeps accuracy | Not established | SkillRouter does not test model-visible names-only; one n=1 stub task; GIST-CMTF has no names-only tier |

## 5. L5–L6 industry and economics (criterion 7)
Documented behaviour: provider tool search/deferred loading, MCP client guidance, AgentCore semantic search, Claude Code behaviour, Spring AI (official docs, first-party). Claims: Speakeasy, Cloudflare, GitHub Copilot (the blog's own arithmetic is inconsistent: "27.5% absolute improvement" vs 94.5 − 69.0 = 25.5; Stable vs Insiders populations; vendor self-report). Economics per §1.7. Adoption prevalence, independent efficacy and break-even are not established; F11 had five searches.

## 6. L7 identities (criterion 8)
Resolved from primary artifacts: MCP-Atlas (arXiv 2602.00933v3), Re-Invoke (2408.01875), FitText (2605.02411v4), GLM-5.3-Flash (publisher card; context window not stated in the card text). Candidate only: Executor → UsefulSoftwareCo/executor. Unresolved: the Claude paper-writing skill; the A9 source.

## 7. L8 disconfirming questions (criterion 9)
(a) Tool-definition share of tokens: workload-dependent; the harness base (system prompt + definitions) is the dominant cost component in two stored workloads but is not separated; planning-plus-schema is 52–63% of tokens for MCP-Bench custom clients while a deferred-loading topology shows 2.1% and tool results dominate in MCP-Universe; no single answer. (b) Do many tools harm accuracy so filtering helps: mixed (§1.5). (c) Solved by vendor features: the mechanism is productised; independent end-to-end measurement not found; "solved" is not established. (d) Do lazy/meta-tool designs lose more than they save once turns are counted: mixed with no break-even; vendor statements that discovery adds a step; one confounded study favouring on-demand delivery; one vendor table where static is cheaper at small catalogue size. None found under bounds for a controlled answer.

## 8. L9 validity of the target (criterion 13)
Operational measures supported by the sources: keep model-visible exposure, provider usage (uncached/cache-write/cache-read/output), local-tokenizer estimates, reconstructed components, billed dollars, success, turns, latency and cost per success in separate columns; precedents for counting auxiliary overhead exist (compressor cost in LLMLingua; recommender per-query tokens in PTR; a survey's selection/formatting/verification decomposition, unverified). **[I]** Token reduction is worthwhile where static or repeated schema/prefix context is a large measured component of cost (two stored workloads) and is weakened where caching, added turns, output/tool-result volume or gateway behaviour dominate. No universal break-even; no architecture choice is justified.

## 9. Inclusion/exclusion accounting (criterion 10)
669 rows → 506 groups; frozen classes A 217, B 42, C 223, D 24 (freeze manifest). Challenger-informed derived view (logs unchanged): MSB, MCPTox and PTR are treated as included; S2-0117, S2-0125 and S2-0024 are treated as maybe-equivalent for counting; six title-only includes noted. 28 exclusion groups: reasons are mostly snippet/abstract/metadata level; four class-D "F9 scope" excludes (ShareLock, two bundled benchmark leads, MCP-SafetyBench) have no include row anywhere and are an A4 coverage question; S2-0380, S2-0304 and S2-0476 are INCONCLUSIVE. 223 unresolved maybes and 42 contested groups remain unadjudicated.

## 10. Coverage limits (criterion 14)
Per-family status table as in the draft §11 (F1, F2, F6 capped without the two-provider stopping condition). Five signals: (1) A5 known-item identity recall 40/40, 39 include signals, LLMLingua excluded (full text now read: no tool content; reason confirmed); (2) author–challenger overlap: A5 replicated F1, F2, F8 but no systematic overlap analysis; (3) chaining incomplete across categories; (4) grey/production check: three first-party artifacts and weak leads; (5) global 90-day recency incomplete. Saturation is not completeness. Publication bias (positive vendor claims, preprint dominance, English only), provider limits (OpenAlex lag, Semantic Scholar 429s, undisclosed WebSearch backend) and extraction quality (garbled tables in several PDFs) apply.

## 11. Contradictions and unresolved items
Preserved as in the draft §12, plus: SKILL-USE Tables 6 and 7 disagree; the MCP characterization's "2–30×" may conflict with its Table 3; ToolTree's model labelling; MCPVerse duplicated cells; Copilot arithmetic; Tool Attention seeds and claimed observations; page numbers in A37 and A39 differ from stored-text page markers.

## 12. Revised pivotal-statement register (25 statements; assessment after challenge)

| ID | Statement (bounded) | After challenge |
|---|---|---|
| PS-01 | No retrieval primitive wins universally; ceiling ~35% completeness | qualifies; ceiling holds for no-instruction averages; Re-Invoke contradicts the BM25 clause |
| PS-02 | Expansion helps conditionally | qualifies; weak/strong asymmetry not shown by Re-Invoke |
| PS-03 | Deferred/progressive exposure is documented | supports as a provider feature; dates and "protocol" status unestablished |
| PS-04 | Code execution is a competing mechanism | qualifies; controlled study synthetic; vendor claims footprint only |
| PS-05 | Training-based selection exists | qualifies; outside the 20-source set (unreviewed) |
| PS-06 | Hierarchical routing at large catalogue | qualifies; shortlist confound; model label inconsistency |
| PS-07 | Schema context material in specified settings | qualifies; cost shares assumption-based or synthetic |
| PS-08 | Token-component reduction need not lower the bill | qualifies; concentrated, confounded, tool-output scope |
| PS-09 | Caching changes cost relation | qualifies; self-hosted serving and list-price reconstruction |
| PS-10 | Vendor savings are claims | qualifies; footprint claims, some cells contradict framing |
| PS-11 | Filtering lowered success in tested settings | qualifies; filter-specific, no uncertainty, one weak retriever |
| PS-12 | More tools do not monotonically harm | qualifies (mixed) |
| PS-13 | Names-only tiers thinly evidenced | fails to establish; one n=1 task; GIST-CMTF removed |
| PS-14 | Discovery overhead vs savings | mixed; fails to establish a net result |
| PS-15 | Evaluator/run variance large | numbers supported; link to method differences inferential |
| PS-16 | Gold-path scoring can mis-score alternatives | supports; risk acknowledged more than measured in ToolRet |
| PS-17 | Cost reporting rare and inconsistent | supports after correction (MCPVerse has no token data) |
| PS-18 | Benchmark realism bounded | narrowed to the registry slice; drift clause removed |
| PS-19 | No joint success-and-billed-cost study found | bounded negative, near-misses listed; INCONCLUSIVE |
| PS-20 | Cross-model transfer mixed | qualifies; one task, modelled cost |
| PS-21 | Description reliance/misleading metadata | direction supported by Tool Preferences (full text) and MCPTox/MSB (selection vs alternative-tool invocation differ); abstract-level otherwise |
| PS-22 | Nearby pre-2023 prior art | upgraded for one source (full text: reformulation boosts, best-query caveat); mapping to LLM-token objectives unestablished |
| PS-23 | Executor candidate | partly supported; referent unresolved |
| PS-24 | Worth of the token objective is workload-dependent | qualifies; decode share removed |
| PS-25 | Landscape is bounded | coverage statement stands |

## 13. Research opportunities (candidates, not selections; no architecture favoured)

| # | Opportunity | Evidence basis | Competing explanations | Uncertainty |
|---|---|---|---|---|
| O1 | Controlled joint measurement of catalogue filtering/disclosure on task success and provider-billed cost per success under realistic caching | §1.8 near-miss list; PS-19 | Closed or unseen work (F1, F2, F6 capped; F11 thin; Shi et al. and other A4 sources unchecked); vendors' undisclosed internal evaluations; the effect may be workload- and provider-specific so no general result exists | high; novelty not assessed |
| O2 | Break-even accounting for discovery turns versus saved schema tokens, with gateway and cache-invalidation costs counted | PS-14, PS-08, scaffolding Table 5, Speakeasy cells | May be solved by provider cache features; sign may depend on catalogue size (Speakeasy static cheaper at small size) | medium |
| O3 | Cache-aware dynamic discovery evaluated for billed cost and accuracy together | PS-09; doc statements on cache invalidation; DBC no quality outcome | May be provider-specific | medium |
| O4 | Benchmark with valid-alternative scoring, controlled evaluator variance, standard token and cost reporting | PS-15–PS-17 | Reporting practice alone might suffice | medium |
| O5 | Independent replication of vendor-reported savings with accuracy | PS-10 | Vendors may hold unpublished evidence | medium |
| O6 | Effects of exposure choices on description reliance and selection bias | PS-21, Tool Preferences, MCPTox | Security framing may dominate; coverage gap | low–medium |

## 14. What this report does not establish
Completeness of any family, final inclusion, novelty or the absence of a gap, source quality beyond the checks above, the correctness of any figure shown only in figures or garbled tables, or that any mechanism or architecture should be adopted. Interpretation of many statements rests on source-level audits that only the sampled and pivotal subsets were challenged against; unreviewed pivotal sources and abstract-level evidence are listed in `audits/A43-pivotal-inventory-20261012.md` and the closure audit.
