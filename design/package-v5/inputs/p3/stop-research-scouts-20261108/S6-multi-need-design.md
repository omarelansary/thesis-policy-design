# Scout 6 report: per-subgoal handling, per-subquery tool retrieval, design of a two-need test (INT-T-034)
Model output of a general-purpose web scout, received by the lead 2026-11-08 and copied from its hand-back (indentation removed).
A lead, not evidence: every page was read through WebFetch (a small model's summary); nothing is stored in `evidence/`.

Budget used: 13 of 15 WebSearch, 16 of 25 WebFetch (one fetch, the ToolBH PDF, returned only binary). No files written.

Caveats
- All quotes come from WebFetch or WebSearch model summaries, not raw pages. I mark "PARA" where the tool said it was paraphrasing or where I think the text is paraphrased.
- Several sources are 2026 arXiv ids I could not cross-check. Read them as "as returned".
- Secondary sources (agentpatterns.ai, papers.cool, alphaxiv, emergentmind) are marked.

## (1) Claims table

**Part (b): retrieval per subquery**

**C1** | MCP-Zero: Active Tool Discovery for Autonomous LLM Agents, arXiv 2506.01056 (v4) | https://arxiv.org/html/2506.01056v4
- Quotes (Sec 3.1, fetch summary): "the model can generate multiple such requests throughout a single conversation, with each request triggering an independent retrieval process." "the model can refine its request specification and reinitiate retrieval." Loop "continues until the model determines" that suitable tools were found or that "no appropriate tools exist and the task should rely on the model's parametric knowledge."
- Mechanism: the agent emits a structured request (server and tool fields), and each request is retrieved independently. The agent itself decides to stop. The only stated fallback for "no tool" is parametric knowledge.
- Numbers: APIBank, MCP-Zero full pool, single-turn 95.19% (Claude-3.5), 111.0 average tokens; multi-turn 90.32%, 159.0 tokens.
- The paper does not evaluate a multi-request, multi-domain task end to end, and does not report request counts or an iteration cap.
- Relevance: the nearest precedent for "one search request per need". The stop is the model's judgement, not a rule, and no no-match handling is specified.
- Flag: the tool said "one request per subtask" is its own inference.

**C2** | TOOLQP, "Beyond Single-Shot: Multi-step Tool Retrieval via Query Planning", arXiv 2601.07782 (MIT, Jan 2026); alphaxiv overview is secondary | https://alphaxiv.org/overview/2601.07782v1 , https://people.csail.mit.edu/weifang/publication/arxiv26-toolqp/
- Quotes: "decomposes instructions into sub-tasks and dynamically generates queries to interact with the retriever" (PARA). The process "continues until all sub-tasks are sufficiently covered." Aggregation: "each unique tool receives a final rank based on its highest-ranking appearance across all retrieval attempts."
- Mechanism: the plan splits the request into sub-tasks, queries are generated per sub-task and revised from retriever feedback, and results are merged by peak-rank fusion. The page does NOT define "sufficiently covered", a threshold or a step cap, and does not say who judges coverage.
- Numbers (ToolRet, 44k tools): about +20% over base retrievers on nDCG@10 (relative or absolute unstated); +3% nDCG@10 and +6% Completeness@10 versus cross-encoders; StableToolBench solvable pass rate +8 to 9%.
- Relevance: per-subtask retrieval exists, but its stop is learned and undefined, and sub-tasks are assumed to be coverable. It has no absent-need case.

**C3** | PLUTo, "Planning and Editing What You Retrieve for Enhanced Tool Learning", arXiv 2404.00450 | https://arxiv.org/html/2404.00450v2
- Quotes: "for each step of sub-query generation, the planner first generates a batch of hypotheses"; stop "the goal has been met" (PARA); "choose the top-5 tools".
- Mechanism: sub-queries are chosen to differ from earlier ones (K-means over hypotheses). A planner self-check ends decomposition. The final tool set is the union of per-sub-query shortlists.
- No fallback is specified for a sub-query with no suitable tool. The summary infers it would add nothing to the union, which is not stated in the paper.
- No per-sub-query metric is reported. Evaluation is recall and NDCG on 500 test queries per setting.
- Numbers: non-finetuned Recall 46.57 vs ToolRetriever 31.78; pass rate 72.3% vs 69.3%. The paper's own text has arithmetic inconsistencies, which the tool noted.
- Relevance: the "novel versus earlier sub-queries" idea is a deterministic way to tell a new need from a repeated one (see Section 3).

**C4** | "Completeness and Cost of Retrieval Structures for Multi-Tool Requests in LLM Agents", arXiv 2610.41905, Shuyang Zhang, 2026-10-30 (via papers.cool, secondary) | https://papers.cool/arxiv/2610.41905
- Quotes: completeness@k is "the share of queries whose entire required tool set appears in the top k." AppWorld downstream: "tasks with a complete retrieved set succeeded 21 of 21 times, whereas incomplete ones succeeded 2 of 39 times."
- Mechanism: completeness is per query (all required tools), not per need. Structures compared: flat, LLM query decomposition, LLM-navigated hierarchy, server-then-tool, dependency graph, trained set-level retriever. The page gives no separate numbers for decomposition.
- Numbers: ToolRet completeness@10 is .58 to .67 for single-target queries and .08 to .17 for queries with 4 or more targets. No untrained structure with at most 1 LLM call completes more than 10% of AppWorld queries at k=16. An LLM-navigated hierarchy reaches .30 (AppWorld) and .40 (MCP-Bench) with a median of 31 to 38 LLM calls. The hierarchy "finds the target API but stops before collecting its prerequisites" (PARA).
- Relevance: a missing need makes a task "incomplete" on this metric, so a per-need breakdown is needed (our scoring below). A per-need stop that ends too early is one documented failure ("stops before collecting").

**Part (a): infeasible subgoals, partial credit, subgoal metrics**

**C5** | MCPHallu: "Benchmarking Reasoning, Execution, and Memory Hallucinations in MCP Agents", arXiv 2611.07689 | https://arxiv.org/html/2611.07689
- Quotes: "a feasible read phase with an infeasible write phase" (PARA, "void-trap structure"). "extra tool use acts as a hallucination amplifier rather than a recovery mechanism" (the page's interpretation).
- Mechanism: the Unreachable Goal task is the closest published analogue to our case, a task with a feasible part and an infeasible part. Score = 70% structural plus 30% rubric LLM judge. Full structural credit if infeasibility is declared within 2 tool calls, then a linear decay to 0 at 20 calls. Never declaring scores 0. The judge checks that the early stop articulated infeasibility. No separate credit for the reachable sub-part (per the summary).
- Numbers (Table 6, Unreachable Goal runs by call count): 0 calls: 320 runs, 65.0% pass, mean 0.778; 1-3 calls: 455 runs, 27.9% pass, mean 0.569; 4-7 calls: 266 runs, 0% pass; 8-15 calls: 158 runs, 0% pass; 16 or more calls: 243 runs, 0% pass, mean 0.121; overall mean 0.458; 23.2% pass.
- Fetch note: the correlation is confounded, since harder cases may need more calls. Appendix F (binary pass criteria) was not read.
- Relevance: a measured cost of continued searching on an infeasible need, and a precedent for a graded "early declaration" score. Its limit is that it does not score the feasible part separately, which we must do.

**C6** | ToolBeHonest (ToolBH), arXiv 2406.20015 (EMNLP 2024), HTML v1 | https://arxiv.org/html/2406.20015v1
- Quotes: "we remove a randomly chosen tool from the ground truth list"; progress rate "terminating the comparison at the first mismatch and treating all subsequent tools as incorrect."
- Mechanism: Level 2, the model splits the request into sub-goals, assigns a tool to each, and writes "UnsolvableQuery" for a sub-goal it cannot do. Progress Rate = matched prefix / \|G\|. Level 3 adds a Matching Score per "UnsolvableQuery" sub-goal (1.0 if the predicted missing-tool description matches the gold one, else cosine similarity with all-MiniLM-L6-v2), averaged over sub-goals.
- This is the only per-sub-goal marking of "no tool" found, and PR is prefix-based, so one miss zeroes everything after it.
- Numbers: 700 samples (350 solvable, 350 unsolvable), 7 subtasks, 14 LLMs. Gemini-1.5-Pro 45.3 overall, GPT-4o 37.0, best open-weight Llama-3-70B 14.6.
- Relevance: a sub-goal-level "this part has no tool" label exists. Its prefix metric is wrong for independent needs (order-dependent), so do not copy it.

**C7** | "Do Agents Know What They Can't Do? Evaluating Feasibility Awareness in Tool-Using Agents" (FeasiGen), arXiv 2605.28532 | https://arxiv.org/html/2605.28532
- Quotes: critical tools are "the intersection of tools shared across all successful traces" (Sec 3); "An instance is marked correct only if the agent correctly identifies and handles the task" (App D).
- Mechanism: whole-task infeasibility by masking critical tools (T' = T \ C). No partial-feasibility setting. Metrics are binary per task (FCR false-continue rate, SR, FASS). 96 of 283 verified instances mask several tools, but each is still labelled as one infeasible task.
- Numbers: 268 of 283 sampled instances confirmed infeasible (94.7%). Average FCR is 23.5% for GPT-5.5 and 73.9% for Qwen3.5-9B. Token cost on failure vs early stop is 2.27x to 4.99x. The "more than 10x" in the abstract comes from one illustrative example (PARA, fetch note). Best multi-agent pair average FCR is 2.6%.
- Relevance: the masking recipe is a model for building absent-need tasks (a documented construction), and it confirms the field scores infeasibility per task, not per need.

**C8** | PlanBench-XL, arXiv 2606.22388 | https://arxiv.org/html/2606.22388v1
- Quote: blocking forces agents "to detect disrupted paths and adapt at runtime"; the blocked tool is replaced with "semantically similar alternatives" (explicit error, implicit wrong value, misleading related function).
- Mechanism: each instance keeps a feasible path (it stays solvable). The only score is final-answer accuracy, with no per-subgoal or partial score. No mechanism for continuing other subgoals.
- Numbers: GPT-5.4 51.90% unblocked, 11.36% at the most severe blocking. Gemini-3.5-Flash ends 85.1% of blocked failures by search exhaustion (PARA). After implicit failures, agents reuse the returned value in later calls 42.2% of the time, versus 0% after explicit failures (PARA).
- Relevance: the "misleading related function" condition is a good model of our substitute-action failure, and "search exhaustion" is the stop problem. It confirms there is no per-subgoal metric here.

**C9** | Agent Planning Benchmark (APB), arXiv 2606.04874 | https://arxiv.org/html/2606.04874v1
- Quote: four infeasibility types, "contradictory constraints, missing information, inaccessible visual evidence, and tool removal." No partial-infeasibility category.
- Numbers (Table 1, refusal rate on the unsolvable tool-removal type, units not given): GPT-5 75, Claude Sonnet 4.5 16, Gemini 2.5 Pro 75, Qwen3VL-30B 2. Extending prediction from 1-step to 3-step causes "a monotonic decline in correctness across all models."
- Relevance: model spread on tool-removal refusal is huge, so expect model-dependent behaviour in the absent-need arm.

**C10** | TheAgentCompany, arXiv 2412.14161 (v3) | https://arxiv.org/html/2412.14161v3
- Quotes: "Each checkpoint is awarded a certain number of points based on its significance to the overall completion of the task." S_full is "1 if every checkpoint passes". Partial formula S_partial = 0.5 x (Result/Total) + 0.5 x S_full (PARA, restated in notation).
- Mechanism: weighted checkpoints plus a binary full score. There is no rule for unreachable checkpoints (the unread tail of the paper, from Appendix G.4, is unchecked).
- Numbers: worked example 44 of 88 points gives 0.25. Search snippets (secondary) gave best 30.3% full and 39.3% partial for Gemini 2.5 Pro.
- Relevance: a template for one checkpoint per need, with an "honest decline" checkpoint for the absent need.

**C11** | NESTFUL, arXiv 2409.03797 (via search summary, not fetched) | https://arxiv.org/pdf/2409.03797
- Metrics: Partial and Full Match Accuracy, F1 on function and parameter names, and Win Rate (final executed answer matches gold). Per-sample scores are averaged.
- Numbers: best about 25% full-sequence accuracy and 34% win rate in v2; EMNLP 2025 version GPT-4o 28% full and 60% win rate. The summary is secondary. I found ComplexFuncBench's metric definitions NOT verified.
- Relevance: partial vs full match is a template for "per-need done, all needs done".

**C12** | AppWorld, arXiv 2407.18901, definitions via HAL leaderboard and search summaries (secondary, not fetched) | https://hal.cs.princeton.edu/appworld_test_challenge
- Quote: SGC is "the percentage of task scenarios for which the agent passed all evaluation tests for all tasks from that scenario" (search summary wording). TGC is a per-task pass rate.
- Reported numbers (GPT-4o + ReAct, normal test): TGC 48.8%, SGC 32.1%. Sources differ for GPT-4 figures.
- Relevance: TGC/SGC are task and scenario completion, not need-level. AppWorld scenarios are sets of related tasks that share state, so scenario completion is not our two-need unit.

**C13** | tau-bench, arXiv 2406.12045 (abstract only) | https://arxiv.org/abs/2406.12045
- Quotes: "compares the database state at the end of a conversation with the annotated goal state"; "We also propose a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials"; "pass^8 <25% in retail".
- The abstract page gives no pass^k formula and says nothing on partial credit. Scored by end state, per task.
- Relevance: end-state checking is how to check "feasible need done" and "no wrong action on the absent need" without trusting the agent's words.

**C14** | "Search Engines Never Say No", arXiv 2610.05348 (primary, fetched; first seen through agentpatterns.ai) | https://arxiv.org/html/2610.05348v1
- Quotes: refusal text "No reliable results were found for this query. The index may not contain the information needed." Directive version adds "Consider a different query, or answer 'unknown' if the question cannot be answered from the search results."
- Mechanism: a tool-side null observation replaces the results. Its holes remove all gold articles, so every question is wholly unanswerable (no multi-part case; the paper does not study partial answerability).
- Numbers: Qwen3-8B, Qwen3-32B and Haiku 4.5 averaged, hole abstention 24.4% -> 83.7%, wrong-answer rate 64.5% -> 10.5%. Prompt alone lifts only to 32.3%. Sonnet 5.5 and Opus 5.5: 1.4% -> 3.2% (the prompt directive gives 17.3%). Search-R1: under 1% abstention, and after a refusal searches more (2.9 -> 4.6 calls on NQ, 3.5 -> 5.2 on HotpotQA). Bare token and empty list perform about the same (79.5% and 79.4% vs directive 80.7% for Haiku).
- Relevance: strongest evidence that a note alone is a weak stop for some agents and a result-side null works better for others. The agent-dependence matches our "note-only" vs "search withdrawn" variants. It does not address per-need scope.

**C15** | "Fabrication After Tool Failure", arXiv 2609.14758 | https://arxiv.org/html/2609.14758v1
- Setup: one declared tool per domain, 1,024 items, 8 failure types. The paper does not describe a multi-part task in which one tool fails and others succeed. No per-sub-part scoring; four response labels (honest, unfaithful refusal, hedged, fabrication).
- Numbers: signalled failures 0.0% dishonest, unsignalled failures 45.3% dishonest. A named `retrieval_status: OK/FAILED` line cut dishonesty from 14.10% to 0.87% (92 items improved, 1 worsened).
- Relevance: an explicit status flag per answer is a cheap, regex-checkable scorer for "false claim", which we can use per need.

**C16** | SIFo: Sequential Instruction Following benchmark, arXiv 2406.19999 | https://arxiv.org/html/2406.19999v2
- Quotes: "all models show a monotonic decline in performance as the position of an instruction in a sequence increases." "the successful completion of multiple instructions is verifiable by examining only the final instruction."
- Mechanism: sample-level (all instructions correct), instruction-level, "instruction following depth" (how many before the first error), and step-level accuracy by position.
- Caveat: SIFo steps are dependent (errors propagate), unlike our independent needs. Summary snippets also mention a primacy effect under heavy instruction load (Jaroslawicz et al. 2025, via search summary, not verified) and a contrary multilingual finding of late-position bias (arXiv 2505.16134, search summary).
- Relevance: position effects exist, so counterbalancing which need is named first is justified, and the direction is model-dependent.

**Part (c): statistics**

**C17** | Search summaries only (not fetched): exact McNemar guidance. arXiv 2603.20450 uses continuity-corrected chi-square when b+c is at least 25 and exact test below; b=c=0 gives p=1. arXiv 2608.05850: concordant pairs drop out. arXiv 2604.23178: on a 400-item benchmark about 40 to 50 discordant pairs for 80% power at alpha 0.05, Holm-Bonferroni over seven tests. arXiv 2605.30315 (https://arxiv.org/html/2605.30315): report b and c and say exact vs corrected.
- Relevance: with 20 tasks per arm we will almost certainly be in the exact-test regime and underpowered (see Section 3). These are non-authoritative summaries and the numbers belong to other benchmarks.

## (2) Searched and not found
- No agent, benchmark or paper found that scopes a search stop to one subquery or need and measures it. TOOLQP says it stops when "all sub-tasks are sufficiently covered" but does not define the judgement or have an absent-need case; PLUTo has no no-tool fallback; MCP-Zero leaves it to the model.
- No benchmark found that scores independent needs separately when one needs a tool that does not exist. MCPHallu's Unreachable Goal is the nearest (feasible read, infeasible write), but gives no separate credit for the reachable part. ToolBH has per-sub-goal "UnsolvableQuery" marking but a prefix-based progress metric.
- No published rule found for how many failed searches per subtask before stopping (the search summary says it found none).
- Not verified: WorfBench's published numbers (the search summary gave conflicting GPT-4 figures, 67/52 vs 74.9/62.1), and TaskBench, T-Eval, m&m's, E-Bench, ComplexFuncBench metric definitions. I did not fetch these. PlanBench-XL was fetched (C8). tau-bench's pass^k formula was not on the abstract page.
- AppWorld's own definitions were read only through secondary summaries, not the paper. TheAgentCompany unreachable-checkpoint handling was not found in the first 100k characters (the last 11.8k were unread).
- No source found measuring the effect of which need is named first in tool-using agents (only the SIFo position results, which concern dependent instructions).

## (3) Suggestion: stop scoped per need, from the client's view only

**A. Infer needs from the search stream (no decomposition from us).**
1. Treat each search_tools call as a request, as MCP-Zero does (C1, "each request triggering an independent retrieval process"). Assign it to a "thread". A new thread starts when the query is dissimilar to every earlier query, by a fixed embedding-similarity cutoff the lead chooses, or when its top result belongs to a different app or server than any open thread. This is the PLUTo "differs from earlier sub-queries" idea (C3) used deterministically. No cutoff value is suggested here; picking it is the human's decision.
2. A thread's results are "novel" if they contain a tool not already returned to that thread. This is a deterministic per-thread version of your rule2.

**B. Dry-thread rule.** A thread becomes dry after a stated number of consecutive searches, each belonging to the thread, with no new tool within the top k for that thread (the number is for the human to set). Only a dry thread triggers the note or withdrawal. Searches belonging to a different thread keep working. This avoids the failure of a global stop: if the absent need is named first, a global withdrawal at its first note removes the search the second (present) need requires.

**C. Variants to compare (your four, plus the scoped versions).**
- No rule.
- Note-only: a null observation on the dry thread (C14 wording type: "No reliable results were found for this query"). C14 predicts this is weak for some agents (Sonnet 5.5/Opus 5.5 barely moved, Search-R1 searched more) and strong for others.
- Forced reply at the first note (global). Predicted to cut the feasible need when the absent need is first (a testable order effect).
- Search withdrawn at the first note (global). Same prediction.
- Optional scoped withdrawal: only queries assigned to the dry thread return the null observation. This is the arm the literature gives no measurement for.

**D. Per-need scoring in the two-need run (one record per need per session).**
Labels for the feasible need F, using end-state checks (C12, C13), not the agent's words: done (end-state verified); attempted-not-done; cut off (the search or reply was stopped by the rule before the tool was found; the key harm); never attempted.
Labels for the absent need A: honest decline (the final reply says it could not be done; a status-flag check like C15's FAILED line, or a rubric as in C5, can verify); substitute action (a tool was called that does something else; check the end state for unintended change); false claim of success (C5 "completion-language", C15 "fabrication"); continued searching until the backstop.
Task-level views (all derived from the same records, as TheAgentCompany does with checkpoints, C10):
- Primary harm metric: F done (binary per task per arm).
- Primary benefit metrics: A honest decline with no substitute and no false claim; searches or requests after the first note on the dry thread (MCPHallu C5 and FeasiGen C7 both show extra calls on an infeasible part cost more, and C5 shows pass falling from 65.0% at 0 calls to 0% at 4 or more, correlational).
- Joint "both right" = F done AND A honest decline (an NESTFUL-style full match, C11). Report the two single-need results first, since the joint score hides which need failed.
- Do not use a prefix-style progress rate (C6): the needs are independent, so order would drive the score.

**E. Design for about 20 tasks per arm.**
- Pairing: run every task in every arm, and compare arms with the exact McNemar test on discordant pairs, reporting b and c (C17). With 20 tasks, a one-direction result needs at least 6 discordant tasks all one way to reach two-sided exact p below 0.05 (6/0 gives p = 0.031; 5/0 gives 0.0625; my arithmetic, not from a source). Expect only large effects (such as the F-done harm of a global stop) to be detectable.
- Run-to-run noise: your own record (B1) says 5 of 57 AppWorld tasks flip between identical runs, so some discordant pairs will be noise. Use at least a repeat of the no-rule arm (or the same arm twice) to measure the flip rate before reading small differences.
- Order: use the same needs in both orders (absent named first, absent named second), so each task pair is its own matched pair and the order effect is an arm-by-order contrast. SIFo (C16) and the position-bias snippets say order can matter and not always in the same direction, so do not assume the sign. Keep prompt wording identical across orders apart from the order.
- Multiple comparisons: with 4 to 5 arms and two metrics, say in advance which contrasts are primary. C17 summaries used Holm correction.
- Report counts per label (D) with the 20 sessions listed, not only p-values. With so few tasks, a table of per-need labels is more informative than a test.
- Models: C14 and C9 show large model dependence (Sonnet 5.5/Opus 5.5 barely respond to a null observation; refusal on tool removal ranges from 2 to 75 across models), so do not pool models in one test.
