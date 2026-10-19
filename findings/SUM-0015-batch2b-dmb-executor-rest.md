---
id: "FND-0013"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-100
evidence: ["EXT-0157", "EXT-0160", "EXT-0162", "EXT-0165", "EXT-0167", "EXT-0168", "EXT-0170", "EXT-0172"]
---

# Batch 2b: DynamicMCPBench and Executor, remaining ranges (AUTH-016, ledger batch 2)

All quotes are verbatim from the extracts named. Source line = the extract's `line_start` + (body line - 22) (body lines in the EXT files start at 22). Statements marked [O]/[I] are mine. Executor texts are a README and a docs index pinned to commit a54b513e (retrieved 2026-10-11); DynamicMCPBench texts are from `dev`/`HEAD` as retrieved 2026-10-15. Vendor/project self-description, not verified behaviour. Nothing was run.

## Row C-E01/E03 (~292K flat-catalogue figure; what is counted, tokenizer; the 57.3% to 36.7% drop)

| Field | Content |
|---|---|
| Question | Does any range say what is counted (schemas only? names + descriptions? serialised `tools=` block?) and with which tokenizer/counter? What does 57.3% to 36.7% compare? |
| Verdict | **NOT STATED IN THIS TEXT** for the ~292K figure, tokenizer and counting method. **ANSWERED** (in part) for the 57.3% to 36.7% comparison. |
| Quote 1 (EXT-0157, src 32-37) | "When the curated pool is removed and the agent must find its tools in the full 1,168-tool catalog, how much of the measured drop (57.3% → 36.7% for `qwen3.7-max` at top-8) is a property of *the benchmark's difficulty* rather than *that one retrieval configuration*?" |
| Quote 2 (EXT-0157, src 26-30) | "`e8.11` answered the reviewers' objection with a single point: one model (`qwen3.7-max`), one retriever (embedding top-8), one slice, one attempt." |
| Quote 3 (EXT-0160, src ~71-83) | "**Scoring.** Deterministic replay against the released reference traces (`--replay --reference-traces`), Tier-1 effect checkpoints only, no LLM judge ... Budget 12 tool calls per task, as in `e8.11`." |
| Quote 4 (EXT-0160, matrix) | "`flat` \| — \| — \| 36.0 [29–44] \| — \|" (only the minimax-m3 column; the other three are "—"); "Pass rate % with Wilson 95% CI over the 150 pre-registered tasks." Line 23 of EXT-0157: "`flat` partial by design — see H5". |
| What it does NOT show | No token count appears in lines 1-19 or 71-135: the string "292" is absent from both ranges (I read both in full). No tokenizer, counter, or counting surface is named. The 1,168 is a tool count, not a token count. The text does not state which run produced 57.3 and 36.7 beyond "for `qwen3.7-max` at top-8"; the sentence calls e8.11 "a single point ... top-8" so [I] they are probably e8.11 values, but the range does not say so. |
| Arithmetic (mine) | 57.3 - 36.7 = 20.6 percentage points (relative drop 20.6/57.3 = 36.0%). [O] The e9.1 matrix gives for qwen3-7-max curated 54.0 and `rag:8` 30.7 (difference 23.3 points), different from 57.3/36.7; the ranges do not explain the difference (slice/task set? 150 pre-registered tasks vs e8.11 "one slice"). [U] |
| Limits | Metric is pass rate (success), not tokens. The figure being tested by the ledger (~292K tokens) must come from another source or range, not read here. Experiment note says `status: done`, results H1/H2/H3 neutral, H4 positive (EXT-0157 src 2); matrix is "Generated, never transcribed". Only 1 of 4 models has a `flat` cell. |
| [I] effect on ledger row | The row's "not stated" remains true for these ranges; the 57.3% to 36.7% is a success-rate drop from curated pool to embedding top-8 over the 1,168-tool catalog, not a token comparison. |

Extracts: EXT-0157 (lines 1-19), EXT-0160 (lines 71-135).

## Row C-R03/STUB (do distractor tools carry placeholder or stub schemas?)

| Field | Content |
|---|---|
| Question | What do ToolEntry and ToolCatalog contain; do strategies or pool modes build tools with empty, minimal or synthetic schemas? |
| Verdict | **ANSWERED** for the code in the ranges read: yes for rendering the surface (`pool_to_tool_surface`), with a stated exception for tools absent from the reference trace. |
| ToolEntry (EXT-0162, src 57-66) | "class ToolEntry: ... server_id: str / tool_name: str / description: str = \"\" / tags: tuple[str, ...] = ()" with docstring "One pool tool. `tags` carries the server's manifest tags (e.g. domain labels)". No input-schema field. |
| ToolCatalog (EXT-0162, src 72-100) | "The candidate tool universe. Built from observed traces (which carry `tool_specs[server_id]` after every session) and, optionally, a manifest to attach domain tags. Tools are deduplicated by (server_id, tool_name)." `from_traces` copies only `server_id`, `tool_name=ts.name`, `description=(ts.description or "")`, `tags`. |
| Fallback entry (EXT-0162, src 123-127) | "Missing entries fall back to bare-bones ToolEntry(server_id, tool_name) so downstream strategies still have a name/server to work from." (applies to required tools missing from the catalog) |
| Pool modes (EXT-0167, src 66-72, 82-90) | `build_eval_pool(... mode ...)`: "if mode == \"gold\": return req_entries"; "if mode == \"full\": return req_entries + catalog.excluding(required)"; otherwise "target: required + p_alt*pool_size direct alternatives + rest near-misses" (alts via `same_name`, others via `hard_neg`). `build_strategy_pool`: "Required tools + a single-strategy distractor set (for the ablation harness)." Defaults `pool_size: int = 8`, `p_alt: float = 0.5`. |
| Schema rendering (EXT-0167, src 107-123) | "Render a pool into a {server_id: [ToolSpec]} surface for the explorer. Required tools reuse their real ToolSpec (with input schema) from the reference trace so the candidate can call them correctly; distractor tools not present in the reference get a minimal permissive schema — calling one just misses the replay cache." Code: "ts = real.get(e.key) or ToolSpec(name=e.tool_name, description=e.description, input_schema={\"type\": \"object\"})". |
| Strategies (EXT-0162, EXT-0165) | `VALID_STRATEGIES = ("random", "hard_neg", "cross_domain", "same_name", "sibling", "stratified")`. All sampling strategies return ToolEntry lists (name/server/description/tags); none of the sampling code touches a schema. Similarity uses description plus tool name (`_tokens(r.description + " " + r.tool_name)`) or embeddings over "tool-description vectors" (hard_neg docstring, EXT-0162). |
| What it does NOT show | Only lines 41-312 of sampling.py (357 total) and 31-125 of pools.py (125 total, so the file head, lines 1-30, with `POOL_MODES`, was not read) were read. Whether the real specs of distractors that do exist in the reference trace are used (the code says `real.get(e.key) or ...`: any pool tool found in the reference specs gets its real ToolSpec, others get the stub) depends on what `reference_specs` contains; not stated in these ranges. Whether this surface was what the models in the e9.1 / e8.11 runs saw, and whether the `rag:k` and `hier` conditions use `pool_to_tool_surface` at all, is not stated here (they are other scripts). [U] Token counts of the stub schema are not given. |
| Limits | Code at HEAD as retrieved 2026-10-15; may differ from the code used for the paper's runs. |
| [I] effect on ledger row | The unverified item can be restated: in this code, distractors absent from the reference trace get `input_schema={"type": "object"}` with their description kept; required tools keep real schemas. [O] The ToolEntry has no schema field at all, so any catalog-level token count built from ToolEntry would not include input schemas (inference from the structure; no count in these ranges). |

Extracts: EXT-0162 (sampling.py 41-180), EXT-0165 (sampling.py 180-312), EXT-0167 (pools.py 31-125).

## Rows AS-07 and C-D08/EXEC (what a connected agent sees by default in Executor)

| Field | Content |
|---|---|
| Question | What do the remaining README ranges and docs index say about what a connected agent sees by default (listing vs search), about 'details' and 'results' tools, and about connection prefixes? Report only what is stated. |
| Verdict | **NOT STATED IN THIS TEXT** for default agent view, 'details' and 'results' meta-tools and connection prefixes (the ledger's wording is not supported by these ranges). **PARTLY** for adjacent facts (below). |
| Stated: appearance of tools (EXT-0168, src ~79-81) | "Most MCP clients only load servers at startup, so you may need to restart the client or open a new chat before the Executor tools appear." (the text says "the Executor tools" without listing them) |
| Stated: connection (EXT-0168, src ~64-71; EXT-0172) | README: "paste an OpenAPI, GraphQL, or MCP URL, and Executor detects the type, indexes the tools, and handles auth." Docs index: "Integration: anything you add (an MCP server, an OpenAPI spec, a GraphQL API). Connection: one configured instance of an integration. An integration can have many connections, and a connection doesn't have to be authenticated." This defines "connection" as an instance of an integration; no "prefix" is mentioned. |
| Stated: CLI commands for search/details (EXT-0170, src ~167-173) | "executor tools search \"\"     # search tools by intent"; "executor tools integrations         # list configured integrations + tool counts"; "executor tools describe       # show tool TypeScript/JSON schema"; "executor call  --help --match \"\" --limit  # narrow huge namespaces"; "executor resume --execution-id  # resume paused execution"; "executor mcp                        # start MCP endpoint (stdio)". These are CLI commands, not a description of the tool surface an MCP client receives. |
| Stated: SDK (EXT-0170, src ~155-159) | "const tools = await executor.tools.list({ integration: \"inventory\" }); const schema = await executor.tools.schema(tools[0].address);" (SDK listing is per integration, with a separate schema fetch). |
| Stated: policies (EXT-0172) | "Policy: whether each tool is always allowed, requires approval, or is blocked. Policies start from a sensible default derived from the imported spec (for example, GET requests on an OpenAPI spec are allowed by default)." Index also: "one catalog for every tool, shared across every agent you use." |
| Stated: execution runtimes (EXT-0170, src ~192) | "kernel/ execution runtimes (QuickJS, Deno subprocess, dynamic worker)"; "hosts/ host adapters (MCP surface, Cloudflare)" (directory names only). |
| What it does NOT show | Nothing in lines 61-114 and 136-253 of the README or in the docs index (1-64, whole page) states which MCP tools an agent sees by default, whether the MCP endpoint lists every integration tool or exposes a small fixed set of meta-tools, or any tool named "details" or "results". The word "prefix" for connections is absent. The string "tool search" occurs only as the CLI command `executor tools search`. README lines 1-60 and 115-135 and the linked docs pages (concepts/policies, integrations, connections, local/cli) were not read in this batch (lines 115-135 lie between my two README ranges and were not read by me). An earlier batch may have covered lines 1-60; I did not recheck. [U] |
| Limits | README/docs index pinned to commit a54b513e; project self-description, no measured behaviour; this is a README, not an MCP protocol specification. |
| [I] effect on ledger rows | AS-07 and C-D08/EXEC's wording ("connection prefixes and meta-tools (tool search, details, results) instead of listing all tools") is not supported by these ranges; it must rest on other text (if any) or be marked unverified. The README CLI shows a search command and a describe command, which is compatible with, but does not establish, a search-first MCP surface. |

Extracts: EXT-0168 (README 61-114), EXT-0170 (README 136-253), EXT-0172 (docs index 1-64).

## Not read / not run
- Not read: DynamicMCPBench e9.1 lines 20-70 and 136-801 (outside the assigned ranges, so the experiment's other tables, H5 text and any token figures there are unread); sampling.py lines 1-40 and 313-357; pools.py lines 1-30; Executor README lines 1-60 and 115-135.
- The ~292K figure was not located in any range read here.
- Nothing run; no web access used; no `--no-write` extractions needed.
