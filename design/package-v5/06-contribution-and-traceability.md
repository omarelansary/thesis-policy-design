# 06. Contribution and traceability (V5, AUTH-020)

Status: provisional, lead, 2026-10-22. Machine check: `python design/package-v5/tools/trace_check.py` (every literature pointer resolves to a stored file and existing lines; every record id exists; every V5-Rnn and D-nn of `04` is listed here).

## 1. New, reused, needs validation
| Part of V5-R | Status | Where searched for prior work |
|---|---|---|
| Cached prefix, invalidation rules, prices | Reused (vendor mechanism) | `03` section 1 |
| Offering at a fixed prefix | Reused mechanism (Anthropic beta, OpenAI); effect in our setting needs validation (HYP-0018) | `03` section 2 |
| Deferral and search, append-only | Reused (vendor mechanism); uninstructed use needs validation (HYP-0019) | `03` section 3 |
| Usage-based core, groups, routing | Reused (Copilot's shipped design, EXT-0228) | `03` section 4 |
| Deployment filter (S1) | Reused mechanism (static allow-lists) | `03` section 4 |
| Regime switch (S2) by D-01 | **Reused**: Claude Code ships a threshold that loads MCP tools upfront below 10% of the window (`03` section 3); DPR-0008 proposes the same switch independently; V5 adds only the bill arithmetic for where to set it (D-01), which needs a reading (P5) (corrected after CH-0081) | `03` section 3; DPR-0008 |
| Memory-informed offering after the shared prefix (M2-M3) | **New as a combination** (personalized tool memory over small tool sets exists, `03` section 5); gated; needs validation (HYP-0017); not established | scout group 3; blind A and B; V4 `04` section 4; steward C; targeted searches (search log section 2) |
| Markdown memory file (M1, W) | Reused (the supervisor's prescription; Anthropic memory tool as carrier) | `03` section 5 |
| Observation masking (H) | Reused result (one study); not in the default; an option for deployments with large tool results (HYP-0021) | `03` section 6 |
| Bill criterion | Reused (DPR-0006) | — |

## 2. Thesis sufficiency against the recorded criteria only
- A negative or not very novel result is still a thesis; a paper needs a systematic study (REQ-O14F-02): V5's admissible outcomes include dropping every new part.
- The novelty is combining approaches and showing what works and what does not (REQ-O14F-03): the only new part is the combination M2-M3 (per-user seeding from a large catalogue after a shared prefix, with the bill as criterion); it is falsifiable in `05` P1; the arithmetic gives its threshold but does not settle whether it pays (D-02 revision 3).
- Success is the quality of the work, nothing missed (REQ-U21-11): the reuse map lists every slot with its sources and its limits; gaps are stated as "not found in a limited search" with the queries logged (`inputs/search-log-20261022.md` section 2), or as not re-searched where that is the case.

## 3. Register of recommendations and derivations
| Id | Pointer |
|---|---|
| V5-R01 | DPR-0006; `04` section 6 |
| V5-R02 | L/v5-anthropic-tool-use-caching-20261022.md:57-63; L/v5-anthropic-midconv-sysmsg-20261022.md:27; L/v5-openai-prompt-caching-20261022.md:440-441; L/v5-ccissue-92033-cachebust-20261022.txt:180-190 |
| V5-R03 | D-01; FND-0037 (minimum length, EXT-0150) |
| V5-R04 | L/v5-anthropic-tool-use-caching-20261022.md:49; L/v5-openai-tool-search-20261022.md:5 |
| V5-R05 | REQ-O21-09; L/v5-anthropic-memory-tool-20261022.md:29 |
| V5-R06 | L/v5-anthropic-midconv-sysmsg-20261022.md:27, :452; L/v5-openai-prompt-caching-20261022.md:441; HYP-0017 |
| V5-R07 | EXT-0228 (a group expansion costs a cache miss and a round trip; an embedding ranker costs an embedding call rather than a model request [I], not stated in EXT-0228); `03` section 7 (no source for a system trigger) |
| V5-R08 | L/v5-complexitytrap-2508.21433.txt:23-25; L/v5-anthropic-context-editing-20261022.md:71; L/pdf-tokennotcost-2607.12161v5.txt:200-224; HYP-0021 |
| V5-R09 | `05` section 1 |
| V5-R10 | `09` EX-2; L/v5-openai-tool-search-20261022.md:22; L/v5-executor-docs-mcp-20261022.md:28-31; L/v5-sciagentskills-2609.00065.txt:131-136; D-03 |
| V5-R11 | `09` EX-9, BR-8, BR-1; L/v5-anthropic-tool-use-caching-20261022.md:57-63 |
| V5-R12 | `15` PL-1, 4.1; L/v5-ls-b05-github-pull-2611.txt; L/v5-ls-f04-claude-blog-lessons-from-building-claude-code-prompt-caching.txt; L/v5-ls-f05-openai-guides-prompt-caching.txt (SUM-0056, SUM-0057); REQ-U28-01 |
| V5-R13 | `15` PL-2, 4.3; L/v5-ls-b06-chatgpt-customization-memories.txt; L/v5-ls-a10-geminicli-cli-auto-memory.txt; L/v5-ls-c04-mem0-blog-mem0-the-token-efficient-memory-algorithm.txt; L/v5-ls-g01-arxiv-pdf-2605.24941.txt (SUM-0058, SUM-0059, SUM-0061); REQ-O21-03; REQ-U28-01 |
| V5-R14 | `15` PL-3, 4.5; L/v5-ls-g07-github-github-copilot-building-an-agentic-memory-system-for.txt; L/v5-ls-g08-github-agents-copilot-memory.txt:149-155; L/v5-ls-e02-arxiv-pdf-2602.11988.txt (SUM-0060, SUM-0063); REQ-U28-01 |
| V5-R15 | `15` PL-8, 4.5; L/v5-ls-g08-github-agents-copilot-memory.txt; L/v5-ls-f25-claude-en-memory.txt (SUM-0056, SUM-0060); REQ-U28-01 |
| V5-R16 | `15` PL-6, 4.6; L/v5-ls-f03-claude-build-with-claude-prompt-caching.txt; L/v5-ls-f05-openai-guides-prompt-caching.txt; L/v5-ls-f12-google-docs-pricing.txt (SUM-0057); REQ-U28-01 |
| D-01 | `calc/regime_bill.py`, `calc/regime_bill.stdout.txt` |
| D-03 | `calc/compact_tiers.py`, `calc/compact_tiers.stdout.txt` |
| D-04 | `calc/price_sensitivity.py`, `calc/price_sensitivity.stdout.txt`; `11` |
| D-05 | `calc/retention_and_write.py`, `calc/retention_and_write.stdout.txt`; `10` sections 9 and 11; `inputs/p0-api-lifetime.jsonl`, `inputs/p0-api-minmax-lifetime.jsonl`, `inputs/p0-api-glm-lifetime.jsonl`; L/v5-ls-f03-claude-build-with-claude-prompt-caching.txt; L/v5-ls-f05-openai-guides-prompt-caching.txt; L/v5-ls-f12-google-docs-pricing.txt:288-305 (SUM-0057); REQ-U28-01 |
| D-02 | `calc/memory_seed.py`, `calc/memory_seed.stdout.txt` |
