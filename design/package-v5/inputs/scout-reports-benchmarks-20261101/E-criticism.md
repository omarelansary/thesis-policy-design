# Scout E report (thread T-20261101-127, TASK E: criticism, audits, errata and community reports)
Model output of a general-purpose scout at high effort, received by the lead 2026-11-01 from its hand-back. Sections 3 to 6 copied as delivered (line breaks compacted); section 1 (instruction files: CLAUDE.md and ops/STATE.md; only the allowed files read) and section 2 (not requested for task E) omitted. A lead, not evidence; only stored pages are cited.

Scout's caveats: WebFetch returns a small model's answer, not page text; "(snippet)" rows rest on search summaries; openai.com returned HTTP 403; on GitHub list pages "no maintainer reply visible" means none in the captured page; about 60 searches and fetches. Interest key: AUTH benchmark authors; IND independent with no stated stake; INT interested party, named.

## 3. Claims (E1 to E33)
**Audit and replication papers**
- E1. BFCL v4, tau2-Bench, LiveMCPBench, MCP-Atlas. "Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation" (arXiv v1, 30 Jun 2026). INT: CoreThink AI and Stanford authors introducing their own Tool-Veritas and Harness Lab; no conflict statement found. https://arxiv.org/html/2607.02577v1. "we find 92 evaluator-human disagreements, corresponding to an 18.5% misalignment rate" (Abstract; 496 tasks, Table 3). methods, E2E. PROBLEM; maintainers' contact not stated.
- E2. Same, BFCL v4 (Sec. 4.3): "BFCL v4 exhibits 40 evaluator–human disagreements across 200 audited tasks" (20.0%); "instance_state_mismatch" 20 of 25 official failures in a 50-task multi-turn export; the scorer can measure "exact simulator-state conformity rather than whether the user objective was achieved". P3. PROBLEM.
- E3. Same, tau2-Bench Retail (Sec. 4.3, App. A.1): "The τ2-Bench Retail audit contains 112 tasks and 11 disagreements" (9.8%); a false negative "an incorrect semantic target implemented as a substring check"; a false positive shows "final-state scoring can reward inaction when the expected state is itself unchanged". E2E. PROBLEM.
- E4. Same, LiveMCPBench (Secs. 4.3-4.4): error rate 30.5% (29 of 95); 23 reruns "ranging from 57.9% to 76.8%" (mean 69.4%, SD 5.4); judge gpt-4.1-mini "rather than the stronger judge configuration recommended in the benchmark paper"; agent MiniMax-M2.7. methods, E2E. PROBLEM (judge variance).
- E5. Same, MCP-Atlas (Tables 1, 3): 89 audited, 12 misaligned, 13.5%; evaluator "LLM claim coverage"; no MCP-Atlas-specific cases in the text received; search summaries name cases, unconfirmed. PROBLEM (weak).
- E6. tau2-bench airline and retail. "Policy Loopholes in Agent Evaluation" (arXiv 2609.14400 v1, 13 Sep 2026, single author Hongliu Cao). IND. https://arxiv.org/abs/2609.14400. "Policy specification quality sets the ceiling on evaluation quality"; search summary: 17 loopholes in 50 airline and 114 retail tasks (PDF unreadable). E2E. PROBLEM.
- E7. tau2-bench. Amazon AGI "tau2-bench-verified" README (MIT). INT (Amazon runs models; SABER arXiv 2512.07850). https://github.com/amazon-agi/tau2-bench-verified. Changes "only in the dataset"; four categories: policy violations, database mismatches, logically impossible tasks, vague instructions; each in FIXES.md; no task count. E2E. PROBLEM; a fixed fork.
- E8. tau2-bench, Sierra repository (AUTH). https://github.com/sierra-research/tau2-bench. tau3 added "75+ task fixes"; "v1.0.1 fixed `banking_knowledge` grading; results from before 1.0.1 are not comparable on that domain"; "2.0 English runs are not input-identical to v1.0.1"; 155 open issues; MIT. methods, E2E. PROBLEM (version lock).
- E9. tau2-bench 2.0, issue #672 (jimmy-holdout, 22 Oct 2026, open). IND. https://github.com/sierra-research/tau2-bench/issues/672. Malformed tool-call JSON and empty replies classed `infrastructure_error` "drop out of the denominator instead of counting as 0"; wrong answer gives a cell 0.5, malformed JSON 1.0; no maintainer reply visible. P2, E2E (open-weight models). PROBLEM.
- E10. tau2-bench 2.0, issue #710 (31 Oct 2026, open). IND. https://github.com/sierra-research/tau2-bench/issues/710. With gpt-oss-120b as user simulator the default English persona "writes several turns in one message"; merged turns in 5 of 12 runs vs 0 of 12 for qwen3.8-27b; "Version 1.0.1 never merged". methods (simulators), E2E. PROBLEM.
- E11. tau2-bench issue list, first page. https://github.com/sierra-research/tau2-bench/issues. #716, #715, #714, #713, #712, #708 (wrong ground truth, 30 Oct to 1 Nov 2026); #711 (telecom DB match fails on float formatting and a stale gold DB); #729 "Provider-dependent caller-generation timing may hurt comparability across runs". All open. PROBLEM (live errata stream).
- E12. BFCL v4. Epoch AI "Benchmark Review", reviewed 10 Sep 2026. IND (Epoch does not review its own). https://epoch.ai/benchmarks/berkeley-function-calling-leaderboard/review. Verdict "Flawed"; 50 questions from "the 5,088 scored items" (15 multi-turn, 10 memory, 10 web-search, 5 each non-live AST, live AST, irrelevance); defects "could affect accuracy in 24 of 50 tasks (48%)"; "We stopped inspecting once we discovered errors that exceeded our published threshold." P3, methods. PROBLEM.
- E13. BFCL, same page: "A model that answers the question properly (retrieving the current headmaster) would get it wrong"; "If a model checks the watchlist first and ends up making no tool call, it will fail the turn entirely"; "dependent on live external state that can drift"; no commit hash named; a search summary's claim of a version change without a bump is not supported by the page. PROBLEM.
- E14. SWE-bench Verified. Epoch review 3 Sep 2026. IND. https://epoch.ai/benchmarks/swe-bench-verified/review. "Flawed"; relies on OpenAI's 23 Feb 2026 audit: 27.6% of tasks audited, 59.4% of those flawed tests, "a floor of 16.4% of tasks broken"; "unlikely to meet our bar of fewer than 20% of questions having accuracy-impacting issues"; RDI found a reward hack giving a perfect score. methods. CONTEXT.
- E15. SWE-bench Verified, OpenAI post (snippet only; 403). https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/. 138 problems o3 "did not consistently solve over 64 independent runs", each reviewed by "at least six experienced software engineers"; "35.5% ... strict test cases ... 18.8% ... additional functionality"; improvements "increasingly reflect how much the model was exposed to the benchmark at training time". INT. CONTEXT, to be checked.
- E16. Epoch "Benchmark Reviews Documentation". https://epoch.ai/data/benchmark-reviews-documentation. "Flawed: The benchmark has one or more substantive flaws that we believe users need to be aware of to accurately interpret results"; "reviews stop once enough evidence is found" (snippet paraphrase). methods. CONTEXT: reviews are not exhaustive; no Epoch review found for tau-bench, MCP-Atlas, Toolathlon or AppWorld.

**MCP and large-catalogue benchmarks**
- E17. MCPMark issue #272 "Run-to-run noise in the v1-0905 logs" (3 Oct 2026, open). IND. https://github.com/eval-sys/mcpmark/issues/272. Two single runs "must differ by about 11 points per service (14.9 on Postgres)"; "A median of 22% of tasks flip between identical runs"; "559 of 11,314 runs ended in a harness or API error with no verdict, and pass@1 counts them as failures"; a commenter: gpt-oss-120b 1-2% empty replies "because a provider's parser dropped tool calls". P4, E2E. PROBLEM.
- E18. MCPMark issue #278 "Postgres verifiers pass when the agent empties the source tables" (30 Oct 2026, open). https://github.com/eval-sys/mcpmark/issues/278. Pass "12 of 28 Postgres tasks (8 of 18 standard, 4 of 10 easy) without doing the work"; reporter "did not see a model do this unprompted". P4. PROBLEM.
- E19. MCPMark open issues (22). https://github.com/eval-sys/mcpmark/issues. #269 "`.../asset_retirement_migration` can never pass"; #238 "TimeZone issue"; #237; #227; #239 "Reproducibility Issues with MCPMark Benchmark" (7 comments); #253 Notion template link expired. PROBLEM.
- E20. MCP-Universe issue #45 (5 Jan 2026, open). IND. https://github.com/SalesforceAIResearch/MCP-Universe/issues/45. Leaderboard gpt-oss-120B (OpenRouter, function-call) "≈ 24.44"; reproduced "≈ 11", "stable across runs", unmodified code. Floor/ceiling, route. PROBLEM.
- E21. MCP-Universe issues (19 open). https://github.com/SalesforceAIResearch/MCP-Universe/issues. #77 "separating agent errors from ground-truth drift"; #53 outputs requested; #48 "version number of mcp-server used"; #46 reproduction help. Paper's dynamic evaluators "retrieve real-time ground truth" (snippet, arXiv 2508.14704). PROBLEM (live ground truth).
- E22. Toolathlon issue #85 "External API instability causes non-model evaluation failures" (19 Aug 2026, open). IND. https://github.com/hkust-nlp/Toolathlon/issues/85. "Several Toolathlon tasks depend on live third-party APIs or public websites"; rate limits, anti-bot, "data drift"; also #83, #89, #94. E2E. PROBLEM.
- E23. Toolathlon issue #98 "Review of Toolathlon model-evaluation problems" (19 Oct 2026, open). https://github.com/hkust-nlp/Toolathlon/issues/98. 20 defects, e.g. 3.2 "The GT becomes 0.115 instead of 0.13, and the result depends on API return order"; 3.16 "Three of 29 GT statuses ... don't follow the stated rules"; 3.18 "Five of the seven required repos can't be reached"; security report: container mounts `/var/run/docker.sock`; some models "downloaded the ground truth (GT) and evaluation code from the public repo". One reporter, unverified. PROBLEM.
- E24. Toolathlon README. https://github.com/hkust-nlp/Toolathlon. "[2026.06.30] Toolathlon-Verified is released ... task prompts, ground truths, and evaluators reviewed and aligned for the final benchmark release"; "You need to register some accounts and configure some tokens/api keys/secrets"; no licence stated (HF dataset gated); #98 post-dates Verified. PROBLEM / CONTEXT.
- E25. MCP-Atlas issue #76 "[Bug/Data Quality] Systematic Ground Truth (GT) Quality Issues in Evaluation Claims" (28 Aug 2026, open). IND. https://github.com/scaleapi/mcp-atlas/issues/76. Seven GT errors in six tasks, e.g. "skeleton,tsk" for skeleton.tsx; "The tool returned a duration of 687.3 with no unit. GT reads it as minutes"; "valid alternatives scored 0.0". PROBLEM.
- E26. MCP-Atlas issue #71 "How is closed-SaaS state isolated between tasks" (4 Aug 2026, open). https://github.com/scaleapi/mcp-atlas/issues/71. Write tools such as `slack-conversations_add_message` enabled; "It's still not clear to me how the eval maintains unbiased scores across evals of several models."; only a non-maintainer answer. P1, E2E. PROBLEM / [U].
- E27. MCP-Atlas README and issues. https://github.com/scaleapi/mcp-atlas. "20 need no setup, 11 require API keys, and 5 require API keys plus data setup"; "36 servers and 307 tools"; "500 tasks"; default judge "gemini/gemini-3.1-pro-preview"; MIT; paper and Scale pages say 220 tools; #84 smoke-test fixture provenance, public/private split; #34 filesystem error; #15 "503 Egress is over the account limit for ghcr.io/scaleapi/mcp-atlas:1.2.5"; per-task exposure by `ENABLED_TOOLS`. CONTEXT / PROBLEM (220 vs 307 unreconciled).
- E28. MCP-Atlas judge change, Scale leaderboard (AUTH, vendor). https://labs.scale.com/leaderboard/mcp_atlas. Snippet: "In April 2026, Scale updated the MCP-Atlas evaluation, upgrading the scoring judge and adding retry handling for transient tool errors." Version lock. PROBLEM; confirm on the page.
- E29. LiveMCPBench issue #9 "Reward extraction is extremely untrustworthy" (16 Dec 2025). IND, maintainer replied. https://github.com/icip-cas/LiveMCPBench/issues/9. Judge wrote "the task was not completed successfully", which contains "success", scored 1; maintainer: "an early implementation bug", fix pushed; "still edge cases". PROBLEM (acknowledged, residual).
- E30. MCP-Bench (Accenture) issues (16 open). https://github.com/Accenture/mcp-bench/issues. #17 "Only 52 out of 56 tasks were successful"; #15, #25 scoring logic; #21, #24 Google API keys; #20 "MCP connection error" (10 comments). PROBLEM (titles only).

**Retrieval, simulators and others**
- E31. ToolBench and StableToolBench. StableToolBench paper (arXiv 2403.07714 v4). AUTH of the fix (01.AI, Google, Tsinghua, HKU). https://arxiv.org/html/2403.07714v4. "the stability of API status for a significant portion of online tools (55.6% in ToolBench) is inconsistent"; "only 44.4% of API calls are successful" (Table 10: 49.2% "Not Available", 6.4% "Not Authorised"); "If a task is unsolvable, the result defaults to a pass regardless of the answer status"; "gpt-3.5-turbo-16k can not assume the role of the automatic evaluator"; cache plus LLM API simulator, GPT-4 a dependency. catalogue source, methods. PROBLEM for ToolBench; FIT with limits for StableToolBench.
- E32. AppWorld issues (12 open). https://github.com/StonyBrookNLP/appworld/issues. #230 task 988af8e evaluation "calls nonexistent `models.changed_fields`"; #218 `changed_model_names` skips real diffs; #229 sqlmodel>=0.0.45 "rejects naive datetimes: every amazon `place_order` fails"; #203 state reset. No independent audit found. PROBLEM (small).
- E33. ToolRet by extension. TooLEX/ToolEX paper (arXiv 2609.08327 v1, 8 Sep 2026). IND. https://arxiv.org/abs/2609.08327. "one-to-one annotation systematically underestimates retrievers"; "an average of 5.3 valid combinations per query" on Tool-DE; ToolRet not named on the page; a search summary says arXiv 2510.22670 (TOOL-DE) reports ToolRet's 35 datasets differ in documentation completeness; ToolRet paper https://arxiv.org/pdf/2503.01763. P3. PROBLEM by extension.

**Also noted (weaker, no row)**
- "Auditing the Audit" (ICML 2026, https://icml.cc/virtual/2026/78606; Li, Fan, Zhuang): five failure modes of audit pipelines; audits such as E1 are also fallible.
- ToolSandbox limitations (snippet, arXiv 2408.04682): milestones and minefields need expertise; some tools "are still backed by external web services"; 0 open issues seen.
- Self-serving benchmark choice: only a FAR.AI talk summary (two AI-scientist agents "favored easier benchmarks") and a write-up of a pilot audit of twelve agent-benchmark papers (inconsistent versions and hyperparameters), both snippets; no systematic measurement found. Not to be cited as established.
- arXiv 2601.12979 (snippet) dropped one broken tau-bench mock task ("update_task_with_user_tools").
- Mem2ActBench (ACL 2026 long.370) built from ToolACE, BFCL and Oasst1, 2,029 sessions, 400 tasks (snippet); inherits their issues; no independent criticism found.

## 4. Not found (in the places read)
Queries: SWE-bench Verified audit; tau-bench flawed tasks; BFCL criticism; tau3 changelog; MCP-Atlas criticism; Epoch reviews for tau, MCP, Toolathlon (none); OpenAI SWE-bench post (403); Toolathlon issues, errata, criticism; AppWorld audit; ToolSandbox, ToolRet, ETAPP, Mem2ActBench, ATRBench criticism; MCPVerse, TheMCPCompany, MCP-Universe limitations; selective-reporting evidence; Hacker News and LocalLLaMA posts. Nothing on ETAPP, ATRBench or TheMCPCompany (repositories not opened); no MCPVerse issues read; no forum posts found (the forum category is empty, not evidence of absence); no AppWorld or ToolSandbox audit; no BFCL response to Epoch linked. Maintainer fixes: LiveMCPBench #9 in part; tau2 fixes and v1.0.1 by the authors; Toolathlon-Verified (30 Jun 2026) with defects listed after it.

## 5. Possible wrong assumptions
- Live-service drift is common in the MCP set (E13, E21, E22, E24): paired arms less deterministic, uncached variance in the bill; a frozen catalogue and stored task copy are needed.
- Parser and route effects on open-weight models run both ways (E17 counted as failures, E9 dropped from the denominator, E20 24.44 vs about 11 on another route; E10 simulator breakage).
- Loop sizes versus noise (E17: 22% of tasks flip, 11 points between single runs): `05`'s direction-only reading is supported; E2E needs repeats.
- Scorer errors common (E1-E4, E12); a paired design cancels part.
- State between tasks (E26) matters for repeated runs and P1; check isolation.
- Version instability (E8, E11, E13, E27, E28): lock by commit and dataset revision, not paper version only.
- No criticism read mentions token, cost or cache reporting; #729 nearest.
- Epoch's "Flawed" reviews are partial and lean on an interested party's audit for SWE-bench.

## 6. URLs to store
https://arxiv.org/html/2607.02577v1 | html
https://epoch.ai/benchmarks/berkeley-function-calling-leaderboard/review | html
https://epoch.ai/benchmarks/swe-bench-verified/review | html
https://epoch.ai/data/benchmark-reviews-documentation | html
https://github.com/sierra-research/tau2-bench/issues/672 | html
https://github.com/sierra-research/tau2-bench/issues/710 | html
https://github.com/sierra-research/tau2-bench/issues | html
https://github.com/sierra-research/tau2-bench | html
https://github.com/amazon-agi/tau2-bench-verified | html
https://arxiv.org/abs/2609.14400 | html
https://github.com/eval-sys/mcpmark/issues/272 | html
https://github.com/eval-sys/mcpmark/issues/278 | html
https://github.com/eval-sys/mcpmark/issues | html
https://github.com/SalesforceAIResearch/MCP-Universe/issues/45 | html
https://github.com/SalesforceAIResearch/MCP-Universe/issues | html
https://github.com/hkust-nlp/Toolathlon/issues/85 | html
https://github.com/hkust-nlp/Toolathlon/issues/98 | html
https://github.com/hkust-nlp/Toolathlon | html
https://github.com/scaleapi/mcp-atlas/issues/76 | html
https://github.com/scaleapi/mcp-atlas/issues/71 | html
https://github.com/scaleapi/mcp-atlas | html
https://labs.scale.com/leaderboard/mcp_atlas | html
https://github.com/icip-cas/LiveMCPBench/issues/9 | html
https://github.com/Accenture/mcp-bench/issues | html
https://arxiv.org/html/2403.07714v4 | html
https://github.com/StonyBrookNLP/appworld/issues | html
https://arxiv.org/abs/2609.08327 | html
https://arxiv.org/pdf/2503.01763 | pdf
https://icml.cc/virtual/2026/78606 | html
https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | html
