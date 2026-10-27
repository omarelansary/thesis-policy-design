# 14. The exposé-derived ideas against literature and open-source projects (V5, AUTH-020 second amendment, INT-T-013)

Status: provisional checkpoint, lead, 2026-10-27. Nothing validated, approved or final. Asked by the human: were the ideas adopted from the June exposé verified against research and open-source projects, "from both sides" (what is already built and reusable, and what research says)? `09` had checked them only against sources already stored. This record adds a wider search and says how far the checking got.

## 1. How far the checking got (read this first)
| Step | Done? | Where |
|---|---|---|
| 4 scouts searched papers, vendor documents and open-source repositories | Done | prompts `inputs/scout-prompts-expose-ideas-20261027.md`; reports in the lead session only (not stored as files) |
| About 58 pages stored | Done | `evidence/literature-20261019/v5-xp-*` (MANIFEST.jsonl) |
| Steward Y compared 17 claims (tool-set maintenance, cache, metrics, oracle) with the stored text | **Done** | `design/package-v5/inputs/SUM-0049-v5-xp-session.md`: 14 confirmed, 3 partly, 0 contradicted |
| Steward X (tiered definitions, reuse) | **Stopped at its turn limit with no output** (no SUM-0048 file). Its 21 claims are scout leads, unchecked | claims `inputs/claims-batch-X-tiers-20261027.md` |
| Steward Z (validation, enrichment, retrieval, cost, reuse) | **Stopped at its turn limit with no output.** The lead checked 3 of its 24 claims only (Z1 Re-Invoke, Z2 Tool-DE, Z15 ToolRet tables: the quoted numbers and the "limited and even negative improvements" sentence are in the stored text). The other 21 are scout leads, unchecked | `inputs/claims-batch-Z-gate-retrieval-20261027.md` |
| Challenger review | **Not run** (checkpoint requested by the human) | thread T-20261027-123 empty |

Everything below that is not marked "checked" is a scout's reading through a summarising tool and must not be cited as evidence yet. Not found in the places searched never means it does not exist.

## 2. Result per idea
### V5-R10 / EX-2: short entries first, full schema on request
- [lead; scout reading, not yet checked against the stored pages] OpenAI's tool search shows an individually deferred function's name and description with the schema deferred; Anthropic's search tool defers the whole definition, and appends it at the end of the context on discovery without touching the prefix (caching preserved). Anthropic's "Code execution with MCP" post suggests a detail-level parameter (name, name and description, full schema), as an unmeasured suggestion.
- Research leads (unchecked): two-stage name-and-description then schema (arXiv 2511.03728, small models: precision up, recall down); schema compression cuts 44-57% of schema tokens but helps accuracy only when the budget binds (2605.26165: at 32K "the difference is minimal"); longer descriptions give +5.85 points success at +67% steps (2602.14878); description content matters more than length (2602.18914).
- Against: tiering moves failures into selection; extra requests (a vendor post reports 2-3x more tool calls and about 50% more time).
- **No stored source defines four fixed levels L0-L3 or measures them.** The 0.4 compact fraction in D-03 still has no source; the closest measured cuts are 44-57% for compressed schemas (leads).
- Reuse (leads): Executor (MIT, TypeScript), langgraph-bigtool (MIT, Python, replaceable retrieval function), TSCG (MIT, TypeScript). Vendor-hosted tool search is tied to Anthropic and OpenAI models; OpenRouter's rejects Chat Completions; LiteLLM's tool search page lists Anthropic-family providers only. So on the university API the pattern can be copied, not the product.

### V5-R11 / BR-8 / EX-9: churn and recall logging, oracle ablation, failure split
- [F, SUM-0049, checked] No stored page defines "churn" or "offered-set recall". The nearest published terms are Recall@K and Completeness@K (ToolRet), Match@k and MRR (Enrich-Retrieve-Rank), and MemTool's removal ratio. So the thesis would define churn itself (1 minus overlap), which is not a problem but should be said.
- [F, SUM-0049] Oracle ablations exist: ToolRet replaces the annotated tool set with retrieved tools and pass rate falls (50.60, down 11.40); MCPVerse has Oracle, Standard and Retrieve modes, but its Table 4 repeats the Qwen row's Oracle and Standard cells in the Claude row (do not cite that row), and for GPT-5 Retrieve beats Standard. ToolEx reports a retrieved set beating the annotated oracle by 3.5-6.5 points, so the oracle is not always an upper bound.
- [F, SUM-0049] Failure splits exist: LiveMCPBench (Retrieve Error 50.00% of one small sample); Enrich-Retrieve-Rank (68% and 70% of failures at retrieval on two large registries, mostly at the reranker on others). None uses the exposé's selection / compression / router / validation split.

### BR-1: evicting appended tools
- [F, SUM-0049] **No stored page shows eviction improving accuracy or cost.** MemTool measures whether models can remove tools (reasoning models 90-94%, some models none) and has no run without removal. Vendor pages say changing tool definitions invalidates the cache from that point (Anthropic, OpenAI) and give cheaper options: Anthropic's `clear_at_least` gate for clearing tool results, and OpenAI's `tool_choice: "none"` instead of removing definitions.
- [I] This supports the current stance in `09` (retention by default, eviction only behind the rewrite arithmetic) and adds the masking alternative, which `05` P4 already names.

### EX-5: validation gate with expansion, no-match rule (all leads, unchecked)
- Reject-only gate exists and is measured (closed-world paper, stored earlier); 15.25% of its fabricated-argument trials are schema-valid and "irreducible". Validate-and-re-ask loops exist in libraries (Instructor, Pydantic AI) and say each retry costs tokens and time. **Validation-triggered expansion of the schema was not found.** A calibrated score threshold for "no tool fits" exists in semantic-router (MIT, needs labelled no-match examples). Models abstain poorly unprompted (AgentAbstain, best 59.5%).

### BR-6: enriched searchable text (leads, 3 of the numbers checked)
- [F, lead-checked] Re-Invoke: nDCG@5 ToolE single 0.6522 to 0.7821 with 10 generated queries per tool; Tool-DE: BM25s 36.41 to 39.35, e5-mistral 40.02 to 38.85 (a loss), mean document length 131.72 to 177.61 tokens, "semantic dilution".
- [U] No tool-specific paper in the stored set reports the cost of generating the enriched text, so "one-time offline cost" in `09` is an assumption.

### EX-4: hybrid retrieval plus reranking, client-side D (leads, ToolRet tables lead-checked)
- [F, lead-checked] ToolRet: generic rerankers give "limited and even negative improvements" (monoT5 33.83 to 28.92); BM25s with instructions 36.46 is competitive.
- Leads: hybrid is not always better than dense alone (ScaleMCP, Dynamic ReAct); on raw tool documentation generic rerankers add about 0.5 points and the large gain needs a trained reranker after expansion (Tool-DE); an industrial gateway uses BM25 plus dense with reciprocal rank fusion (SCOUT). So hybrid weight and reranking are things to measure, not settle.
- Reuse (leads): ToolHive's optimizer accepts an OpenAI-compatible embedding service; LiteLLM proxies rerank in Cohere format (to be confirmed on the live endpoint); the ToolRet and Tool-DE repositories are Apache-2.0.

### Cost of client-side discovery (the bill term)
- [U] No source found that prices the extra request, the appended definitions and the cache effect together. Papers name the extra calls without costing them. A vendor benchmark gives tokens and dollars per task: at 40 tools the semantic arm used far more tokens than static on a complex task and still cost less in dollars on one row, so savings are not monotone in catalogue size (lead; unchecked). A production blog reports cost down 48% while cache-hit rate fell, which fits keep-and-append (unchecked).

## 3. What this changes, and what it does not
- **Nothing in V5-R10, V5-R11 or the loop is changed here** (the amendment forbids it). The searches found no evidence that contradicts keeping them; they found that the supporting evidence is thinner than `09` suggested for R10's levels, for validation-triggered expansion and for enrichment cost.
- Proposals for the human (not applied): (a) state in `04`/`06` that "churn" and "offered-set recall" are the thesis's own definitions; (b) mark the 0.4 compact fraction as having no source; (c) treat hybrid weight and reranking as measured items in `05` P3.
- Corrections to `09` (facts only): none yet; pending steward X and the unchecked Z claims.

## 4. Open
1. Check the 21 unchecked X claims and the 21 unchecked Z claims. Both stewards hit the 40-turn limit with no output because their batches were too large; protocol forbids re-running them past the bounds without the human. A smaller split (about 8 claims per steward) would need the human's say-so.
2. Challenger review (one challenger allowed) not run.
3. The scouts' reports exist only in the lead session; the claim tables carry what matters.
4. Verifier: steward records are `type: summary` with no EXT ids by design.
