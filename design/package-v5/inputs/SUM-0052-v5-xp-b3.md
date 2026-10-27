---
id: SUM-0052
type: summary
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-28
thread: T-20261027-122
evidence_lines:
  - evidence/literature-20261019/v5-xp-arxiv-2603.20313.txt
  - evidence/literature-20261019/v5-xp-arxiv-2602.14878.txt
  - evidence/literature-20261019/v5-xp-arxiv-2602.18914.txt
  - evidence/literature-20261019/v5-xp-speakeasy-dynamic-toolsets.txt
  - evidence/literature-20261019/v5-xp-github-executor.txt
  - evidence/literature-20261019/v5-xp-github-langgraph-bigtool.txt
  - evidence/literature-20261019/v5-xp-cursor-dynamic-context.txt
---

# SUM-0052: check of scout claims X15-X21 (batch X, tiers) against stored files

[O] SUM, not a finding. Line numbers refer to the stored .txt files. Claims source: design/package-v5/inputs/claims-batch-X-tiers-20261027.md.

| Claim | Verdict | Lines | Short exact quote | Note |
|---|---|---|---|---|
| X15 arXiv 2603.20313 | CONFIRMED | 21-23 | "99.6% reduction in tool-related token consumption with a hit rate of 97.1% at K=3, achieving an MRR of 0.91 on our benchmark dataset of 140 queries across 121 tools from 5 different MCP servers. The system maintains sub-100ms retrieval latency" | MRR given as 0.9107 in the table (line 326). |
| X16 arXiv 2602.14878 | CONFIRMED | 22-27 | "improves task success rates by a median of 5.85 percentage points ... increases the number of execution steps by 67.46% and regresses performance in 16.67% of cases"; "compact variants ... often preserve behavioral reliability while reducing unnecessary token overhead" | "5.85 points" is percentage points, as the scout wrote. |
| X17 arXiv 2602.18914 | CONFIRMED | 148, 845-848, 1019, 1040 | "Conciseness (+1.5%, p< 0.05)"; "+11.6% ... +8.8%"; "Information Completeness shows moderate but significant impact (+5.9%, p< 0.01)" | Functionality and accuracy p<0.001. Scout's "+1.5% selection" matches line 1040 (tool selection). |
| X18 Speakeasy blog | PARTLY | 17, 42-43, 46, 53-60, 67, 75, 81, 91, 95 | "Published November 18, 2025"; "40 to 400 tools"; "Claude Sonnet 4.5"; "reduced by an average of 96.7% for simple tasks and 91.2% for complex tasks ... total token usage drops by 96.4% and 90.7% respectively"; "2-3x more tool calls"; "~50% increased execution time" | Three meta-tool names, numbers, date, model all match. Sub-claim "no formal caching": NOT FOUND (no match for "cach" in the file). Sub-claim on the category outline: the text says the outline "increas[es] the likelihood that they would attempt to search" and that semantic search without it had LLMs that "sometimes wouldn't even attempt to search" (lines 39, 43); it does not say it "fixed" cases. Page also states "up to 160x token reduction" (line 29), which the scout row does not mention. |
| X19 Executor repo | CONFIRMED | 38, 346-349, 376, 388, 414-420, 472 | "MIT license"; "executor tools search"; "executor tools describe <path>"; "executor call <path...>"; "a streamable-HTTP endpoint"; "Or over stdio"; "TypeScript SDK" | Repo text contains both an HTTP endpoint and `executor mcp` (stdio). |
| X20 langgraph-bigtool | CONFIRMED | 37, 49, 196, 210, 258-260, 337 | "MIT license"; "559 stars"; "retrieve_tools_function ... expected to return a list of IDs"; `"description": f"{tool.name}: {tool.description}"`; `init_embeddings("openai:text-embedding-3-small")` | Index text format seen at line 210 in example code, not as a stated rule. |
| X21 Cursor blog | CONFIRMED | 10, 71, 91 | "Jan 6, 2026"; "static context, including names of the tools"; "in runs that called an MCP tool, this strategy reduced total agent tokens by 46.9% (statistically significant, with high variance based on the number of MCPs installed)"; "full rg parameters or even jq" | Scout's "descriptions in files" is consistent with the file approach in lines 71-91. |

## Counts

CONFIRMED 6 (X15, X16, X17, X19, X20, X21); PARTLY 1 (X18); NOT FOUND 0 whole claims (one sub-claim of X18, "no formal caching", not found); CONTRADICTED 0.

[U] Not checked beyond the search patterns used; "not found" means not found in the named stored file by those patterns.
