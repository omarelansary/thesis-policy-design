# L7 report: benchmarks and interactive-agent evidence (2026-11-09)

Grades: [E] peer-reviewed/replicated with released code or data; [M] measured by authors; [V] vendor; [T] theory; [U] unverified. Source ids (S#) are in sources.tsv. "Read" status is stated per source there; most arXiv items were read partly or abstract-only, and the AppWorld paper itself could not be opened (PDF unreadable, HTML 404), so the task brief's GPT-4o numbers are NOT independently re-verified here.

## 1. Findings by decision relevance

**F1. An independent cross-architecture AppWorld study with cost exists and bears directly on the supervisor's concern. [M, S1]**
Exgentic / Open Agent Leaderboard (arXiv 2602.22953; 100 random AppWorld test_normal tasks, 5 agents x 5 models). Success rates on AppWorld, Claude Opus 4.5: code-action Smolagent 0.70, tool-calling ReAct 0.61, ReAct with tool shortlisting ("ReAct Short") 0.64, OpenAI Solo (MCP) 0.68, Claude Code 0.66. With Gemini 3 the order reverses (ReAct Short .55, ReAct .50, OpenAI Solo .57, Smolagent .13); with DeepSeek-V3.2 and Kimi-K2.5 all agents sit at 0.03-0.13. So "code agents are better" is model-dependent, not an architecture law: it holds for the strongest model and fails for Gemini 3. Cost is reported only as average per task across all six benchmarks (Opus: Smolagent $4.4, ReAct $5.8, ReAct Short $3.8, OpenAI Solo $8.5, Claude Code $8.0). Conditions: one 100-task sample, per-cell Wilson 95% CI about +-7 to +-13 pp, apparently one run per cell, caching not described. Consequence: the thesis cannot assume either architecture dominates; any architecture claim needs the model it was measured on.

**F2. The one published AppWorld shortlisting contrast is small and mixed. [M, S1]**
ReAct Short minus ReAct on AppWorld: Opus +3 pp, Gemini 3 +5, Kimi +1, DeepSeek -5, GPT-5.2 +22 (because plain ReAct scores 0.00: the OpenAI API caps tools at 128 versus about 468 AppWorld actions). Cost per task (all-benchmark average): Opus $5.75 to $3.78; others change by $0.07-0.15. Aggregate effect on accuracy is within CI for 4 of 5 models. Implication: outside a hard tool-count limit, the accuracy effect of shortlisting in a mature tool-calling harness is near zero and the cost effect depends on the model; this supports "nearly the same accuracy" being plausible but also shows effects of 3-5 pp are below detectability at n=100. The shortlister's own cost (model, k) is not disclosed.

**F3. Tool exposure by retrieval can lose accuracy versus an oracle set and its cost is rarely cache-adjusted. [M, S5]**
TheMCPCompany (18,505 tools, 175 tasks): GPT-5-mini 38.9% at $0.17 with the oracle set, 22.9% at $0.26 with retrieval over all tools (about 20 tools surfaced), 24.6% at $0.41 with the browser agent. Retrieval beat the browser baseline for stronger models and lost for GPT-5-mini. Costs are token x list price; caching and run count not mentioned. This is the nearest published design to the thesis and one of its models appears in it. It warns that a predicted subset is only as good as its recall.

**F4. Token reduction is not billed-cost reduction; the evidence is paired, cache-aware, and recent. [M, S6]**
PointFive (arXiv 2607.12161, preprint, coding agents in Claude Code, 2,848 paired runs): a 38.4% cut in tool-output tokens produced +6.8% billed cost (95% CI +2.8 to +11.3); cache reads/creation were about 80% of the actual bill; they price writes 1.25x and reads 0.1x. Per-task correlation between token reduction and cost change r=0.15. Limits: coding domain, one provider, cache carryover between arms not excluded. Direct relevance: a tool-definition change alters the cached prefix; evaluate on billed cost with cache pricing, not token counts. Caveat: this is tool OUTPUT compression, not tool-definition exposure, so transfer is by mechanism, not by measurement.

**F5. Cost-reporting practice in benchmarks is thin. [M/V, S11, S22, S26]**
HAL shows dollar cost per entry but its page does not say how cost is computed or how cached tokens are handled, and HAL does not include AppWorld (home page lists nine other benchmarks; updates paused). MCPMark's legacy board lists cost per run (e.g. gpt-5-medium $127.46, Opus 4.5 $466.18 per run) without a caching explanation. A secondary blog [U] states no public tool-calling leaderboard other than MCPMark reports cost, and that none varies tool count as a controlled variable. The AppWorld leaderboard submission format described in the repo contains no cost field. So a bill-versus-accuracy study on AppWorld has no external cost baseline to be compared against; the thesis's own billing equation is the contribution, not a reproduction.

**F6. Variance and repeats: n=57 tasks / 19 scenarios is a low-power paired design. [M, S8, S9, S4]**
Single-run pass@1 on SWE-bench Verified varied 2.2-6.0 pp across selected runs, SD >1.5 pp even at T=0 (arXiv 2602.07150); ICC converged by 8-16 trials for structured tasks and needed >=32 for complex reasoning (arXiv 2512.06710, GAIA/FRAMES). TabAgent's in-loop AppWorld test (24 tasks, <=3 seeds) gives a paired difference of -2.1 pp with CI [-18.8,+16.7]. My own back-of-envelope [I]: for 57 binary tasks with ~25% discordant pairs the 95% CI half-width is about +-13 pp before clustering by scenario; this agrees with the CI the thesis already reports for P2b (+0.067, -0.033 to +0.217). Therefore "nearly the same accuracy" can only be asserted as a non-inferiority margin of roughly 10-15 pp unless more tasks or repeats are added; cost ratios are far more precisely estimable than accuracy. Exgentic's Wilson CIs (+-7-13 pp at n=100) show that even a published 100-task study cannot resolve 3-5 pp.

**F7. AppWorld validity and contamination. [E/O, S13, S15; gaps]**
Facts [F] from the repo: 457 APIs / 9 apps; train and dev are released with full ground truth, test sets hidden; a canary string is embedded; the authors say state checkpointing gives an unrealistic advantage and test tasks must not be inspected for tuning. So the dev split is public and could be in training corpora; the thesis uses it as intended for development but cannot claim uncontaminated results. Open GitHub issues (titles only, not verified [O]): sqlmodel>=0.0.45 rejects naive datetimes so Amazon place_order fails (#229, Sep 2026); evaluator calls a nonexistent attribute on tasks 988af8e_{1,2,3} (#230); changed_model_names can skip diffs (#218). These imply pinning package versions and checking whether any dev task is affected; I did not check which scenario ids are dev. I found no published audit of AppWorld task labels (Epoch AI reviewed BFCL v4 as Flawed and others, but AppWorld/tau2/Toolathlon were not named in what I could read). TabAgent notes AppWorld has no oracle tool labels; reference tool sets are derived from successful runs, so "oracle subset" definitions are one valid route, not unique truth.

**F8. Saturation and what AppWorld measures in 2026. [U/M, S16, S17, S1]**
Aggregators list test-normal TGC of 86.8-89.3 for ACE/RCL context-optimisation methods with small models (Opus used as optimiser over 30 iterations) [U: aggregator, optimiser sees feedback]. Plain agents in Exgentic are far lower (Opus 0.61-0.70; other models 0-0.57). For MiniMax-M3 / GLM-5.3 / gpt-5-mini on dev, the benchmark is not saturated, but the top of the public leaderboard is dominated by learned-context methods, not by exposure policies; a reviewer may ask why exposure rather than context learning is studied. AppWorld-UL (516 tasks, ICML 2026) adds ambiguity/user interaction; Opus 4.7 gets 48.6% [M]: a complementary variant, not a replacement.

**F9. Code-action versus JSON function calling elsewhere: mildly favourable to code, mostly not cost-measured. [M, S19, S20]**
CaveAgent (the proposers' own method) on tau2 airline/retail, 3 runs: code beat JSON FC in 11 of 12 cells (+1.3 to +13.5 pp; airline gains within noise); no tau2 cost. "Bitter Lesson of Tool Calling" (abstract only): programmatic tool calling >= JSON in 11 of 14 models on a 309-entry BFCL v4 subset. Neither measures billed cost with caching. Exgentic (F1) is the only cost-bearing independent comparison and shows reversal for Gemini 3.

## 2. Candidate complementary benchmarks (for the sceptical reviewer)

| Benchmark | Tools / size | Cost reported? | Concerns |
|---|---|---|---|
| tau2-bench (retail/airline/telecom) | small tool sets (count not found); 50-115 tasks/domain | no public cost | pass^k standard; audit: 9.8% evaluator misalignment on retail (S7); simulator errors reported by secondary sources |
| BFCL v4 | 5,088 scored items | no | Epoch rates Flawed; 20% misalignment on 200-item sample (S7); mostly single/multi-turn call correctness |
| Toolathlon | 108 tasks, 32 apps, 604 tools | not in paper abstract | best fit for large tool counts; reported repair of 83/108 artefacts (secondary, U) |
| MCPMark | 127 tasks; pass@1 and pass^4 | cost per run on legacy board | tool count not found; cost method undocumented |
| MCP-Universe | 11 servers; 231 tasks (secondary) | no | live ground truth drifts |
| LiveMCPBench | 95 tasks, 70 servers, 527 tools | no | LLM judge: 30.5% misaligned; 23 reruns spread 57.9-76.8% (S7) |
| TheMCPCompany | 18,505 tools; 175+17 tasks | token x list price | retrieval-quality confound; one embedding model |
| MCP-Bench | 28 servers, 250 tools | unknown | LLM-judge based (abstract only) |
ToolSandbox, NESTFUL, ATRBench, OSWorld-style: not investigated in depth (budget); not found = not searched beyond one query. The most defensible complement for a tool-exposure claim is a many-tool, state-verified benchmark (Toolathlon or TheMCPCompany, or MCPMark for cost), plus tau2 if the policy is conversational. No benchmark I found varies tool count as a controlled variable, so the thesis's own manipulation is novel in that sense [I].

## 3. Contradictory or negative evidence
- Shortlisting hurt DeepSeek-V3.2 on AppWorld (-5 pp) and gave only +1 to +5 pp for the rest; the large +22 pp for GPT-5.2 is an API tool-cap artefact (S1). GPT-5-mini under retrieval in TheMCPCompany scored below the browser baseline (S5).
- Code-action is not uniformly better: Smolagent with Gemini 3 scored 0.13 against 0.50-0.57 for tool-calling agents (S1).
- Token savings can raise billed cost (+6.8% despite -38.4% tokens, S6).
- TabAgent: the learned shortlister's 82% of failures also occurred with the LLM shortlister, so shortlist quality was not the main bottleneck (S4).
- Benchmark validity: tau2 retail 9.8%, BFCL 20.0%, MCP-Atlas 13.5%, LiveMCPBench 30.5% official-vs-expert misalignment (S7).
- The supervisor's "you pay twice" concern is not tested by any source I found as a ReAct-code input-resending effect under caching; S1 reports no token split, and S6 shows cache reads dominate bills in agent loops (suggesting repeated input is cheap per token but not free). [I]

## 4. What would change a tool-exposure policy or its evaluation
1. Report cost per architecture with the same pricing/caching model; Exgentic-style architecture comparisons exist, so a reviewer will ask why only function calling was used. A single code-agent arm on the same 57 tasks would answer the question the supervisor raised; it is not needed for the exposure result itself unless the thesis claims generality beyond function calling.
2. Treat accuracy equivalence as a CI-bounded claim (about +-13 pp at n=57) and place the weight on the cost ratio, which is measurable.
3. Pin AppWorld and dependency versions; check dev tasks against open issues; state that dev is public.
4. Disclose the 128-tool cap for OpenAI models: any "all tools" arm for gpt-5-mini cannot be the full 469 set via API (S1 documents this for GPT-5.2); the thesis already uses 128-tool subsets in P2 per its workspace state, so this is consistent, but the contrast should be named.
5. A second benchmark with many tools and state-based grading (Toolathlon or TheMCPCompany; MCPMark for cost conventions) would pre-empt "single benchmark" objections.
6. Report run-to-run noise of cost and accuracy separately (HAL: token usage varies widely between runs, S12).

## 5. Coverage self-assessment and unresolved gaps
- Strong: Exgentic study, TheMCPCompany, validity audits, variance literature, cost conventions of HAL/MCPMark.
- Weak: I could not open the AppWorld paper, appworld.dev leaderboard, or any submitted-agent designs; AppWorld leaderboard entries are known only through an unverified aggregator. Best AppWorld agents' costs and token counts: not found. Whether any submitted agent uses tool exposure/subsetting: not found.
- Exgentic: per-AppWorld cost, token split, caching, repeats, shortlister identity not obtained (160k-char paper read partly; appendices tables may hold more).
- Many sources read abstract-only (Toolathlon, MCPMark, MCP-Universe, Bitter Lesson, 2602.07150, 2512.06710).
- tau2 tool counts, ToolSandbox, NESTFUL, ATRBench, OSWorld, Artificial Analysis agentic indices: not investigated or not found within budget. Tool-count degradation primary papers (RAG-MCP, LongFuncEval, etc.) belong to other lanes; here only blogs were seen and are excluded.
- Several 2026 items (2607.*, 2608.*, Epoch Sep 2026 reviews) appear only in my fetched pages; none were cross-checked against a second independent copy.
