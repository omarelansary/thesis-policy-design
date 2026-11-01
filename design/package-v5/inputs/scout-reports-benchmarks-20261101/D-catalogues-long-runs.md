# Scout D report (thread T-20261101-127, TASK D: catalogue sources, tool retrieval, long runs and cost reporting)
Model output of a general-purpose scout at high effort, received by the lead 2026-11-01 from its hand-back. Claims (section 3) and sections 4-5 copied as delivered (compacted); property cards condensed by the lead; section 1: CLAUDE.md and ops/STATE.md in context. A lead, not evidence. Scout's note: about 48 searches and fetches; quotes are the fetch tool's rendering ("tool-rendered" = not verbatim).

## 2. Property cards (condensed by the lead)
**D1 tool-definition sources.**
- Official MCP Registry: Terms effective 2025-09-02, "in preview"; server.json examples show $schema, name, description, title, websiteUrl, repository, version, packages, remotes, _meta, no tools array (scout's inference); tools come from `tools/list` at runtime; metadata CC0 1.0, "only to Registry Data and not to packages in third party registries"; "Breaking changes or data resets may occur".
- PolicyLayer (vendor of MCP governance tooling): 13,230 servers, 265,284 tool schemas ("Computed 31-10-2026"); tiktoken o200k_base; median 1,864 tokens per server, P90 13,636, P99 40,135, maximum 448,698 (754 tools); earlier snapshots 3.1-3.4k servers, median about 1,860-1,905; no download or licence; GitHub page 86 tools, 14,406 tokens (snippet).
- MCP-Zero dataset: 308 servers, 2,797 tools from the official MCP repository (tag 2025.4.28, commit ad2d4e6); GitHub server "over 4,600 tokens for 26 tools"; one tool 143 tokens; "comprehensive tool ecosystems can exceed 248k tokens"; repo xfey/MCP-Zero, licence not stated.
- ToolRet (arXiv 2503.01763 v2, ACL 2025): 7.6k tasks (queries card 7,961 rows, 35 subsets); 43k tools (tools card 44,453: code 3.79k, customized 3.37k, web 37.3k); average document 174.56 tokens; non-MCP JSON-like text; NDCG, Recall, Precision, Completeness@K; code Apache-2.0; HF cards no licence; "licensed under their respective data licenses".
- ToolBench/RapidAPI: 16,464 REST APIs, 3,451 tools, 126,486 instances; Apache 2.0, "intended solely for research and educational purposes"; hosted backend needs a maintainer key; StableToolBench separate.
- MetaTool (arXiv 2310.03128 v6): ToolE; arXiv licence CC BY-NC-SA 4.0 (coverage of data unclear).
- COLT/ToolLens (arXiv 2405.16089): release not found.
- Tool-description studies: arXiv 2602.18914 (10,831 servers from GitHub, MCP.so, Glama, PulseMCP, Smithery; no token statistics); arXiv 2602.14878 (856 tools, 103 servers; package SAILResearch/mcp-tool-description-augmentation). Smithery and Glama terms not found.

**D2 tool retrieval.** ToolRet (static single gold); Tool-DE/ToolEQ (arXiv 2609.08327 v1, CC BY 4.0): 7,360 queries, 67.9% of sub-queries with equivalents, 5.3 valid combinations, 30-47% of fine-tuning gain an artifact; ToolRet not named. Seen only: AgentSearchBench (2604.22436), TRAJECT-Bench (2510.04550), arXiv 2601.07782.

**D3 long-horizon and large-output.**
- MCPMark (arXiv 2509.24002 v1): 127 tasks; 16.2 turns, 17.4 tool calls; Notion and GitHub remote APIs; reset; verification script 209.8 lines on average; cap 100 turns, 3,600 s; pass@1 over 4 runs. Table 9 input K tokens and cost: kimi-k2 931.5, $0.57; qwen3-coder-plus 1,421.5, $0.29; deepseek-v3.1 493, $0.28; glm-4.5 419.7, $0.14; gpt-oss-120b 64.5, $0.01. Tool-result sizes not given.
- Toolathlon (arXiv 2510.25726 v2): 108 tasks, 32 apps, 604 tools (32 servers plus 7 local toolkits with 16 tools); 69.9 tools per task; 26.8 turns; 100K-character truncation with 10K paging; overlong outputs 15-35%; history cleared to last 10 turns (App. B); cost "with prompt caching enabled", under $1 per task; real remote services plus containers; scripts, some against live data; pass@1 over 3, pass@3, pass^3.
- TheAgentCompany (arXiv 2412.14161 v3): 175 tasks (App. B sums to 167); self-hosted GitLab, OwnCloud, Plane, RocketChat; 51 tasks (29%) LLM-evaluated; cost "assuming no prompt caching"; Gemini-2.5-Pro 27.2 steps, $4.2; 3 interfaces only.
- TheMCPCompany (arXiv 2510.19286 v1, v2 11 Dec 2025): over 18,000 tools; retrieval and ground-truth tool conditions.
- Terminal-Bench 2.0 (arXiv 2601.11868): 89 tasks (secondary); Harbor and Terminus 2; ABC self-assessment (App. B.5); costs not read.
- SWE-bench Verified: see scout E.

**D4 tokens, cost, cache.**
- HAL (arXiv 2510.11977 v1): 21,730 rollouts, 9 models, 9 benchmarks (Online Mind2Web, AssistantBench, GAIA, CORE-Bench Hard, ScienceAgentBench, SciCode, SWE-bench Verified Mini, USACO, TAU-bench Airline), about $40,000; prices as of 24 Sep 2025; "Token counting methods vary across providers"; caching not mentioned in text read.
- ATRBench (arXiv 2605.28108 v3, EMNLP 2026; BUPT-GAMMA): 20 personas, 284 rules, 568 learning sessions, 6 domains, 74 tools (73 plus confirmation); no elapsed time; transcript appended to a cross-session context block; frozen test phase; simulator gpt-5.4; App. F no-cache and with-cache views, hit read from runner's per-cell token accounting; Apache-2.0; personas CC BY 4.0; deterministic evaluator; adapters in `lib/`.
- SWE-ContextBench (arXiv 2602.08316): 1,476 tasks (abstract v1 300 + 99); settings no context, free or oracle trajectory, free or oracle summary; baseline $0.79; cache-read "more than 97%"; no prices; no human annotators.
- Claw-SWE-Bench (arXiv 2606.12344 v1): 350 instances, 43 repos, 8 languages; cache hit rate = CacheReadTokens / (InputTokens + CacheReadTokens); recommends cost and cache hit rate beside Pass@1 and raw token traces.
- Ndzomga (arXiv 2603.23749): see scout M; the author is also a HAL author.
- Benchmarking the Benchmarks (arXiv 2607.02577; Bhat, Vaghasiya, Mohsin, Aali): see scouts A, E.

## 3. Claims table
D1 | PolicyLayer token cost | vendor (interested) | https://policylayer.com/token-cost | "Computed 31-10-2026" | 13,230 servers, 265,284 tool schemas; median 1,864 tokens per server, P90 13,636, P99 40,135 | P5, methods | CONTEXT, moving vendor snapshot
D2 | PolicyLayer | same | same | same | tokenizer `o200k_base`; "Anthropic's current tokeniser isn't published, so Claude's exact counts will differ"; "treat counts as close estimates rather than exact invoices" | P5 | PROBLEM (self-stated)
D3 | PolicyLayer glossary | vendor | https://policylayer.com/glossary/mcp-token-cost | 11 Jun 2026 | "Measured across 13,230 MCP servers (265,284 tools)"; largest 448,698 tokens | P5 | CONTEXT
D4 | PolicyLayer GitHub page (snippet) | vendor | https://policylayer.com/token-cost/github | not read | 86 tools, 14,406 tokens; a DEV post gives 93 tools / about 55,000 tokens (https://dev.to/rudratosh/your-github-mcp-server-costs-55000-tokens-before-your-agent-reads-a-single-word-4eah) | P5 | CONTEXT; sources disagree
D5 | MCP-Zero | authors | https://arxiv.org/html/2506.01056 | 2025 | "308 MCP servers and 2,797 tools from the official Model-Context-Protocol repository"; GitHub server "over 4,600 tokens for 26 tools"; one tool 143 tokens | P5 | FIT small real set
D6 | MCP Registry terms | maintainers | https://modelcontextprotocol.io/registry/terms-of-service | 2025-09-02 | metadata "dedicated to the public domain under CC0 1.0 Universal"; "applies only to Registry Data and not to packages in third party registries"; "in preview ... data resets may occur" | P5 | FIT metadata / PROBLEM packages excluded
D7 | Registry docs | maintainers | https://raw.githubusercontent.com/modelcontextprotocol/registry/main/docs/reference/server-json/generic-server-json.md | not dated | fields in examples, no tools list | P5 | PROBLEM: no tool definitions in the registry (scout's reading)
D8 | ToolRet | authors | https://arxiv.org/abs/2503.01763 | v2 | "7.6k diverse retrieval tasks"; "43k tools"; "174.56 tokens" average (tool-rendered) | P5, D | FIT / PROBLEM non-MCP, short
D9 | ToolRet card | authors | https://huggingface.co/datasets/mangopy/ToolRet-Tools | 2026-11-01 | "44,453 rows ... code (3.79k), customized (3.37k), web (37.3k)"; 128 to about 4.26k characters; no licence field | P5 | PROBLEM licence
D10 | ToolRet | authors | https://arxiv.org/abs/2503.01763 | v2 | "NV-Embed-v1 ... nDCG@10 of only 33.83"; instructions 42.71; best reranker 47.52 | D | CONTEXT
D11 | ToolRet end-to-end | authors | same | v2 | §7.1 GPT-3.5 with bge-large drops 11.40 points on ToolBench-G1 vs oracle | D, P3 | CONTEXT
D12 | Tool-DE | independent | https://arxiv.org/abs/2609.08327 | v1 | "67.9% of sub-queries have functionally equivalent alternatives"; "an average of 5.3 valid combinations"; "30-47% of the reported fine-tuning gain" | D | PROBLEM for single-gold scoring
D13 | ToolBench | authors | https://github.com/OpenBMB/ToolBench | 2026-11-01 | "16464" APIs, 3,451 tools; "distributed under Apache License 2.0"; "intended solely for research and educational purposes"; backend key | D, P5 | PROBLEM / FIT schema source
D14 | MetaTool | authors | https://arxiv.org/abs/2310.03128 | v6 | CC BY-NC-SA 4.0 (arXiv page) | D | PROBLEM
D15 | MCPMark | authors | https://arxiv.org/abs/2509.24002 | v1 | "127 high-quality tasks"; "16.2 execution turns"; "17.4 tool calls per task" | P4 | FIT
D16 | MCPMark Table 9 | authors | https://arxiv.org/html/2509.24002 | v1 | gpt-oss-120b 5.40 turns, 64.50K input; qwen3-coder-plus 23.75 turns, 1,421.47K; kimi-k2 26.95, 931.50K | P4, E2E | CONTEXT
D17 | MCPMark Table 2 | authors | same | v1 | pass@1 gpt-oss-120b 4.72 ±0.96; glm-4.5 15.55 ±1.16; deepseek-v3.1 16.73 ±1.41; qwen3-coder-plus 24.80 ±2.05 | P4, E2E | PROBLEM floor
D18 | MCPMark environment | authors | same | v1 | "Notion and GitHub use official remote APIs"; reset "to its original state" | P4 | PROBLEM
D19 | Toolathlon | authors | https://arxiv.org/html/2510.25726 | v2 | "32 software applications and 604 tools"; 108 tasks; 26.8 turns; 69.9 tools per task | catalogue, P4 | FIT
D20 | Toolathlon outputs | authors | same | v2 | truncation 100K characters, 10K paging; "approximately 15% to 35%" overlong | P4 | FIT
D21 | Toolathlon scores | authors | same | v2 | DeepSeek-V3.2-Exp 20.1%, GLM-4.6 18.8%, Qwen-3-Coder 14.5%, Kimi-K2-0905 13.0% | E2E | PROBLEM floor
D22 | Toolathlon environment | authors | same | v2 | real remote services plus containers; some checks against live data | P4, E2E | PROBLEM
D23 | Toolathlon cost | authors | same | v2 | "with prompt caching enabled"; "most other models remain under $1 per task" | methods, P4 | CONTEXT
D24 | TheAgentCompany | authors | https://arxiv.org/html/2412.14161v3 | v3 | 175 tasks; Gemini-2.5-Pro "average of almost 27 steps and more than $4"; "assuming no prompt caching" | P4, methods | PROBLEM
D25 | HAL | authors | https://arxiv.org/abs/2510.11977 | v1 | 21,730 rollouts, 9 models, 9 benchmarks, about $40,000; "unified cost tracking"; "Token counting methods vary across providers" | methods | CONTEXT
D26 | HAL caveats | authors | https://arxiv.org/html/2510.11977v1 | v1 | providers may "swap model weights behind the same endpoint without notice"; "o3's price has dropped by 80%" (Sec. 4.1) | methods | PROBLEM: re-price from stored usage
D27 | ATRBench cost | authors | https://arxiv.org/html/2605.28108v3 | v3 | "cache-hit rates are read from per-cell token accounting written by the runner"; 36% to 92%, about 64%; "about $3,550 at posted list price and about $1,730 after applying cache-hit discounts" | P1, methods | FIT
D28 | ATRBench design | authors | same | v3 | "20 personas, 284 standing rules, 568 learning sessions, 6 domains, and 74 tools"; "After the learning phase, ATRBench freezes the accumulated cross-session context"; simulator gpt-5.4 | P1 | PROBLEM 74 tools, order not time / FIT scaffold
D29 | ATRBench repo | authors | https://github.com/BUPT-GAMMA/ATRBench | 2026-11-01 | "The code is released under the Apache License 2.0"; personas "CC BY 4.0"; `evaluator/` "Deterministic trajectory scoring"; variants default, atr, always_ask, oracle_target | P1 | FIT
D30 | SWE-ContextBench | authors | https://arxiv.org/html/2602.08316 | v2 | "cache-read tokens, which account for more than 97% of total consumption across all settings"; summary 217.1 vs 25,633.7 tokens; no prices | P1, methods | FIT arms / PROBLEM no price basis
D31 | Claw-SWE-Bench | authors | https://arxiv.org/html/2606.12344v1 | v1 | "Cache hit rate ... CacheReadTokens / (InputTokens + CacheReadTokens)"; "is not a coding-capability metric"; "should report total API cost and cache hit rate alongside Pass@1" | methods | FIT convention
D32 | Ndzomga | single author (HAL co-author) | https://arxiv.org/abs/2603.23749 | 2026-03-24 | "30-70%" filter cuts tasks 44-70%, rank fidelity | E2E, methods | CONTEXT
D33 | Benchmarking the Benchmarks | audit, rival tool | https://arxiv.org/abs/2607.02577 | v1 | "92 disagreements ... 18.5% misalignment rate"; LiveMCPBench 57.9% to 76.8% | E2E, methods | PROBLEM
D34 | SWE-bench Verified | OpenAI (interested), Epoch (independent) | https://epoch.ai/benchmarks/swe-bench-verified/review | 3 Sep 2026 | "Flawed"; "over 20% of questions have scoring-based issues"; OpenAI 27.6% audited, 59.4% "flawed test cases"; floor 16.4% | P4, E2E | PROBLEM

## 4. Not found
Smithery, Glama, mcp.so terms; ToolRet card licence; ToolLens release; MetaTool tool count; Terminal-Bench cost and tokens; PolicyLayer per-tool averages; MCPMark per-task tool-result sizes; Toolathlon cache-read counts; HAL caching and runs per task; ToolRet-specific criticism; OpenAI's SWE-bench page (403); ATRBench elapsed-time gaps and OpenAI-compatible endpoint.

## 5. Possible wrong assumptions
- "Definitions from public catalogues without running tasks" holds for datasets (MCP-Zero, ToolRet, ToolBench), not the official registry (no tools list; CC0 covers metadata only).
- P5 size: ToolRet 174.56 tokens per document (mostly web docs) vs PolicyLayer median 1,864 tokens per server with a long tail; per-tool sizes disagree across sources; the size distribution matters more than the count; tokenizers differ from the route's models.
- Cache fields: TheAgentCompany assumes none; HAL silent; SWE-ContextBench 97% cache-read share without prices; only ATRBench and Claw-SWE-Bench state cache accounting; V5 must log its own usage records.
- Floors: gpt-oss-120b 4.72% on MCPMark; Toolathlon open-weight 13-20%.
- Live services in MCPMark and Toolathlon.
- ToolRet-style retrieval is static single-shot; no benchmark found measures the model's own search initiation (P3).
- ATRBench has no time gap.
- Audits suggest scorer errors of 18.5% and over 20%; floor and scorer noise could look like "nearly the same".

## 6. URLs to store
(as delivered; stored by the lead, see `inputs/benchmark-url-map.tsv`, letter D)
