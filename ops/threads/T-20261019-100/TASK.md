# Thread T-20261019-100: TASK (lead; AUTH-016, ledger batch 2: remaining stored-text reads)

- Authorization: **AUTH-016**. Second wave of reads of source texts already stored in the repo (the stewards of batch 1, T-20261019-99, left specific ranges unread; findings FND-0008..0011 in `findings/SUM-0010..0013`). No web access (agents have none). No design proposals, no ranking, no thesis-question or parameter choices.
- Four stewards in parallel on **disjoint files**. **No SendMessage.** **Do not write any file under `ops/threads/`** (the guard blocks everything except `ops/threads/*/evidence-steward.md`; the lead writes the per-steward logs from your final answer). Write only your findings file (and the extracts the tool creates).
- Method for every row: `python tools/origin_extract.py --source ID --lines A-B --note "<ledger id>"` (one command per Bash call; no `cd`, pipes, `;`, `&&`, redirection; at most 9 extractions per steward). The pointer ranges were located by the lead with keyword greps; they are starting points, not conclusions. If a range does not contain what the row asks, use an adjacent range with `--no-write` (viewing only, not citable) and then extract the relevant lines (counting against the 9), and say so. Governing copies: `python tools/origin_extract.py --governing PATH --lines A-B`.
- For each row write one table row: `Ledger ID | question | verdict | verbatim quote with EXT id and source lines | what the passage does NOT show | limits (version, date, vendor claim, ragged table)`. Verdicts: **ANSWERED**, **PARTLY**, **NOT STATED IN THIS TEXT**, **CONTRADICTS current wording**, **CANNOT DETERMINE** (say why). Add a one-line `[I] effect on the ledger row` as an observation only. Labels: [F] fact in source, [O] observation, [I] interpretation, [U] unknown, [S] speculation. Report arithmetic you do yourself as yours and show it. Keep what you did not read stated honestly.
- Create your findings file FIRST with front matter and an empty table skeleton, then fill it. Front matter, with **quoted** ids: `id: FND-00xx`, `type: finding`, `status: unverified-until-human-checks`, `created_by: evidence-steward`, `created_utc: 2026-10-19`, `thread: T-20261019-100`, `evidence: ["EXT-....", ...]` (update at the end).
- Final answer to the lead: files written, EXT ids created, per row the verdict in one line, anything you could not read or run, anything that contradicts the lead's current wording, and unresolved items verbatim. (Also include the text you would have put in a thread log, in 4-6 lines.)

## Steward 2a: Anthropic pages and vendor figures (writes `findings/SUM-0014-batch2a-anthropic-vendor.md`, id FND-0012)
Extract (6):
1. `r4-anthropic-prompt-caching` lines 585-600 (minimum cacheable prompt length by model).
2. `r4-anthropic-prompt-caching` lines 476-486 and 786-800 as one or two extractions (1-hour TTL and "1-hour cache duration").
3. `r4-anthropic-tool-use-caching` lines 1-99 (the whole page: defer_loading and cache preservation; what invalidates the cache).
4. `r4-anthropic-advanced-tool-use` lines 30-60 (the 55K, 72K, 77K, 8.7K and "85% reduction" statements).
5. `r4-github-copilot-fewer-tools` lines 365-425 (embedding-guided routing; coverage figures).
Rows (current wording in quotes):
- **C-S03/MINCACHE**: "Anthropic minimum is not in the ranges read." Question: what minimum cacheable length does each Anthropic model class have?
- **C-S03/EXCEPTIONS** and **C-S03/DEFUSAGE**: Question: what does the 'tool use with prompt caching' page add on defer_loading, cache breakpoints on tools, what invalidates the cache, and whether discovered/deferred tools appear in usage? "The claim that a tool-search tool counts as non-deferred appears in none of the ranges read" (check the page for it).
- **N-5**: Question: what does Anthropic state about the 1-hour option (price multiplier, how it is set, interaction with the 5-minute default)?
- **C-E01/E04**: "The denominator and component arithmetic behind the Anthropic '85%' reduction are ambiguous." Question: which two quantities does the page compare (list them with the page's numbers), and does 85% follow from them? Show the arithmetic for (72K to 8.7K) and (77K to 8.7K) and say which, if either, gives 85%.
- **C-E03/O7-26**: "Vendor figures unreplicated/inconsistent (GitHub 27.5 vs 25.5; Anthropic 85% vs ~89%)." Question: what does the Copilot page state about 27.5% and 94.5/87.5/69.0 coverage (what is measured: coverage, success?), and does 25.5 appear in the range read? State the Anthropic ~89% only if you find or compute it (show the arithmetic).

## Steward 2b: DynamicMCPBench and Executor, remaining ranges (writes `findings/SUM-0015-batch2b-dmb-executor-rest.md`, id FND-0013)
Extract (8):
1. `s4f-2a-dmcp-dev-e9-1-exposure-matrix` lines 1-19.
2. `s4f-2a-dmcp-dev-e9-1-exposure-matrix` lines 71-135.
3. `s4f-2a-dmcp-dmcp-sampling-py` lines 41-180.
4. `s4f-2a-dmcp-dmcp-sampling-py` lines 180-312.
5. `s4f-2a-dmcp-dmcp-pools-py` lines 31-125.
6. `r4-executor-readme` lines 61-114.
7. `r4-executor-readme` lines 136-253.
8. `r4-executor-docs-index` lines 1-64.
Rows:
- **C-E01/E03**: "The ~292K-token flat-catalogue figure: counted surface, tokenizer, counting method not stated." Question: does any range say what is counted (schemas only? names + descriptions? the serialised tools= block?) and with which tokenizer or counter? Also what the 57.3% to 36.7% drop in lines 1-19 compares.
- **C-R03/STUB**: "Whether distractor tools carry placeholder or stub schemas is unverified." Question: what do ToolEntry and ToolCatalog contain (name, description, input schema, ...); do any strategies or pool modes build tools with an empty, minimal or synthetic schema? Quote the definitions.
- **AS-07** and **C-D08/EXEC**: "Executor exposes connection prefixes and meta-tools (tool search, details, results) instead of listing all tools." Question: what do the remaining README ranges and the docs index say about what a connected agent sees by default (tool listing vs search), about 'details' and 'results' tools, and about connection prefixes? Report only what is stated.

## Steward 2c: scaffolding paper, ToolMenuBench, GIST-CMTF (writes `findings/SUM-0016-batch2c-scaffolding-toolmenubench.md`, id FND-0014)
Extract (7):
1. `r4-scaffolding-mcp-vs-cli` lines 296-330 (two corrections to the measurement).
2. `r4-scaffolding-mcp-vs-cli` lines 560-620 (a table with a "Cache" column: median share of input tokens billed at the reduced cached rate).
3. `r4-scaffolding-mcp-vs-cli` lines 700-735 (Table 4: the same completed runs priced twice).
4. `r3-toolmenubench` lines 364-425 (experimental setup).
5. `r3-toolmenubench` lines 426-520 (results; Tables I and II).
6. `r2-gist-cmtf-2606-16813-20261011` lines 100-220 (method).
7. `r2-gist-cmtf-2606-16813-20261011` lines 40-100 (introduction, assumptions) if lines 100-220 do not already cover how goal state and contracts are obtained.
Rows:
- **C-E01/E07**: Question: what cache-share figures and Table 4 results does the paper report (per scaffolding / delivery method; conditions); what exactly are the two pricings in Table 4; what are the two corrections to the measurement? Add [O] on which figures bear on cache behaviour of tool definitions (ledger C-S03) or on the share of tokens due to schemas (C-S01), as observations only.
- **C-R03/CMTF**: "How CMTF obtains its causal path is unverified; it may use information a deployed policy would not have." Question: in the experiments, where do the symbolic state, goal condition and tool contracts come from (benchmark annotations, gold trajectories, inferred)? For GIST-CMTF: how is the goal state inferred, and what does it receive as input? Quote.

## Steward 2d: MCPVerse, validity audit, cache papers, version report (writes `findings/SUM-0017-batch2d-mcpverse-cache-papers.md`, id FND-0015)
Extract (9):
1. `r3-mcpverse` lines 276-292 (mode definitions: Oracle, Standard, Max-Scale).
2. `r3-mcpverse` lines 520-545 (retrieve mode; Table 4).
3. `r3-validityaudit` lines 10-30 (abstract; 18.5%).
4. `r3-validityaudit` lines 60-85 (contributions and the 92 disagreements).
5. `s4-cacheaware-compress-2607-15516-20261013` lines 10-40 (abstract).
6. `s4-cacheaware-compress-2607-15516-20261013` lines 648-720 (section 6.3: enterprise tool-using assistant, 94k-token tools= prefix).
7. `s4-cacherouter-2608-22708-20261013` lines 30-60 (abstract).
8. `s4-cacherouter-2608-22708-20261013` lines 1636-1660 (gateway restarts and tool evolution; the aggregate hit rate).
9. governing copy `audit-s4h-20261015/B1-source-version-report.md` lines 1-40 (`python tools/origin_extract.py --governing audit-s4h-20261015/B1-source-version-report.md --lines 1-40`).
Rows:
- **C-S19/S43**: "Retrieve pool (32/65) and retrieve-mode judge behaviour unknown." Question: what does the paper say about the retrieve mode (how many MCPs are retrieved, from which pool) and about the judge in that mode? Quote Table 4's caption and mode text.
- **C-E03/O7-27**: "Evaluator-human disagreement (18.5% in one audit)." Question: what exactly was audited (which benchmarks, how many tasks, how 'disagreement' is defined) and what is the 92 / 18.5% denominator?
- **C-E02/CACHEPAPERS**: Question: what do the cache-aware compression paper (CAPC) and CacheRouter measure about tool-definition prefixes, cache hit rate and price (conditions: provider, model, price ratio used, baseline, computed vs billed); and what is the 51.7% on the 94k-token tools= prefix compared with? Report limits the authors state.
- **C-E03/E40**: "MCPVerse, MCP-Atlas and LiveMCPBench numbers are version-sensitive." Question: what does the version report conclude per paper (which versions differ, which numbers changed)? Quote the report's rows.
