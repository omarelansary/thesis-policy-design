# Thread T-20261019-99: TASK (lead; AUTH-016, ledger batch 1: stored-text reads)

- Authorization: **AUTH-016** (open-items ledger, `design/ledger/PROJECT_A_OPEN_ITEMS_LEDGER.xlsx`; evidence only; repo evidence first). This batch reads source texts that are already stored in the repo (`evidence/sources.json`); no web access (agents have none). No design proposals, no ranking of mechanisms, no thesis-question or parameter choices.
- Four stewards work in parallel on **disjoint files** (one writer per file). **No SendMessage** (no ACTIVE.json exists; do not message anyone). Each steward ends with a final answer to the lead.
- Method for every row below: read the passage with `python tools/origin_extract.py --source ID --lines A-B --note "<ledger id>"` (one command per Bash call, no `cd`, pipes, `;`, `&&` or redirection; at most 9 extractions per steward, so spend them on the pointer ranges given; each creates an EXT file). The lead located the pointer ranges by keyword; they are starting points, not conclusions. If a range does not contain what the row asks, read an adjacent range (stay within the 9) and say so. Report what the text says even where it contradicts the "current ledger wording".
- For each row write one table row: `Ledger ID | question | verdict | verbatim quote with EXT id and source lines | what the passage does NOT show | limits (version, date, vendor claim, ragged table)`. Verdicts: **ANSWERED** (the text answers the exact question), **PARTLY**, **NOT STATED IN THIS TEXT**, **CONTRADICTS current wording**, **CANNOT DETERMINE** (say why). Add a one-line `[I] effect on the ledger row` only as an observation of what the evidence supports (never a design recommendation). Label statements [F] fact in source, [O] observation, [I] interpretation, [U] unknown, [S] speculation. Keep what you did not read stated honestly.
- Create your findings file FIRST with the front matter and an empty table skeleton, then fill it as you read. Front matter: `id: FND-00xx`, `type: finding`, `status: unverified-until-human-checks`, `created_by: evidence-steward`, `created_utc: 2026-10-19`, `thread: T-20261019-99`, `evidence: [EXT ids...]` (update at the end). Also append a short block to your own thread log file.
- Final answer: files written, EXT ids created, per row the verdict in one line, anything you could not read or run, anything that contradicts the lead's current wording, and unresolved items verbatim.

## Steward 1a: provider caching and billing pages (writes `findings/SUM-0010-batch1a-provider-docs.md`, id FND-0008; log `ops/threads/T-20261019-99/evidence-steward-1a.md`)
Prices were already extracted earlier (EXT-0085..0089); do not repeat them. Extract these (9):
1. `r4-anthropic-prompt-caching` lines 606-656 (cache hierarchy; what invalidates the cache; the table, row "Tool definitions").
2. `r4-anthropic-prompt-caching` lines 1770-1806 (caching tool definitions; which usage fields carry their tokens).
3. `r4-anthropic-tool-search` lines 760-840 (a deferred tool and `cache_control`; the Usage section).
4. `r4-bedrock-prompt-caching` lines 55-85 (checkpoints, minimum tokens, TTL).
5. `r4-gemini-caching` lines 340-380 (implicit caching, minimum input tokens).
6. `r4-openai-prompt-caching` lines 48-116 (minimum cacheable length, explicit vs implicit breakpoints, TTL/retention).
7. `r4-mcp-caching-2026-07-28` lines 1-177 (what MCP results are cacheable; `ttlMs`, `cacheScope`; whether tool lists are covered).
8. `r4-anthropic-ptc` lines 30-60 (programmatic tool calling intro).
9. `r4-openai-tool-search` lines 60-80 (mixing deferred and non-deferred functions; any statement on caching).
Rows (current ledger wording in quotes):
- **N-5** and **N-5/UNREAD**: "Stored pages show: Anthropic and OpenAI price cache writes and reads (cache lifetimes of minutes to 24 hours); Gemini explicit caching adds an hourly storage price." Question: what does each page state about cache lifetime/retention and about any time-based charge? Is there an hourly storage statement outside the Gemini pricing page (r4-gemini-caching does not hold prices)?
- **C-S03/MINCACHE**: "Minimum cacheable length 1,024-4,096 tokens by provider; a small restricted prefix can fall under it and lose caching." Question: what minimum does each page state and what happens to a prefix below it?
- **C-S03/EXCEPTIONS**: "Vendor-documented exceptions (a tools array with no non-deferred tool pays one full miss; a tool-search tool counts as non-deferred) have not been tested." Question: list every documented case in these pages where tool definitions, deferral or tool_choice break or restrict the cache.
- **C-S03/DEFUSAGE**: "Whether provider usage counts deferred or withdrawn definitions is not stated." Question: does any page state whether deferred / tool-search-loaded definitions appear in usage fields or the bill?
- **N-26**: Question: which caching mechanisms (implicit/automatic, explicit breakpoints, retention options) does each page document, and which of them can the API caller control?
- **C-E02/E22**: "Anthropic programmatic docs partial; prompt-cache tail, pricing and MCP pages not read in full." Question: what do the programmatic-tool-calling and MCP caching pages say that bears on tool-definition tokens or caching?

## Steward 1b: BFCL and fcrobust (writes `findings/SUM-0011-batch1b-bfcl-fcrobust.md`, id FND-0009; log `evidence-steward-1b.md`)
Extract these (6):
1. `r3-bfcl` lines 115-155 (dataset description; irrelevance; missing parameters).
2. `r3-bfcl` lines 178-200 (multi-turn categories).
3. `r3-bfcl` lines 885-910 (irrelevance category construction).
4. `r3-bfcl` lines 950-970 (category definitions list).
5. `r3-fcrobust` lines 140-215 (toolkit expansion; where the drops occur).
6. `r3-fcrobust` lines 214-245 (results table).
Rows:
- **C-S08/BFCLDEF**: "v4-05 states the definitions of irrelevance and relevance detection from background knowledge: irrelevance = no provided function is relevant and the correct behaviour is to make no call; relevance = a relevant function exists and the model must call it." Question: how does the BFCL paper itself define irrelevance and relevance detection, and the multi-turn categories (base, missing functions, missing parameters, long context)? Quote.
- **C-E02/E20**: "BFCL ICML 2025 paper seen only as a snippet." Question: confirm the stored text is the full paper (page count, appendices) and which categories' results it reports (the table header near line 310), and whether per-model irrelevance and relevance numbers appear in the text layer.
- **C-E01/E01**: "fcrobust BFCL range disputed; original table not rendered." Question: what exact performance changes does the paper report (which models, which perturbation, which measure; the parenthesised percentages in the table), and what do lines 145-146 and 171 say? Report every number and its condition without summarising into a single range.

## Steward 1c: Executor and DynamicMCPBench (writes `findings/SUM-0012-batch1c-executor-dmb.md`, id FND-0010; log `evidence-steward-1c.md`)
Extract these (9):
1. `r4-executor-readme` lines 1-60.
2. `r4-executor-readme` lines 115-135.
3. `r4-executor-docs-mcp-proxy` lines 1-89.
4. `r4-executor-src-description` lines 1-115.
5. `s4f-2a-dmcp-dev-e9-1-exposure-matrix` lines 20-70 (hypotheses H1-H5; the flat condition).
6. `s4f-2a-dmcp-dmcp-sampling-py` lines 1-40.
7. `s4f-2a-dmcp-dmcp-sampling-py` lines 313-357 (distractor strategies).
8. `s4f-2a-dmcp-dmcp-pools-py` lines 1-30.
9. `s4c-g2-dynamicmcpbench-2607-20531` lines 1020-1036 (Table 7 caption: "1,168 tool schemas per request").
Rows:
- **AS-07** and **C-D08/EXEC**: the supervisor's assertion A7: "'Executor' exposes connection prefixes and meta-tools (tool search, details, results) instead of listing all tools." Question: what does the stored Executor README, proxy doc and `execute` tool description say about what an agent sees at the start of a session (integration/connection names? meta-tools? tool search? describe? results?), and is there a "Search and invoke" / passthrough mode? Report what is and is not stated; do not judge whether it is "the" project the supervisor meant (that identification is the researchers', CAVEATS row 6).
- **C-E01/E03**: "The ~292K-token flat-catalogue figure is not verified (counted surface, tokenizer)." Question: what exactly does the development document state about the 292k figure (what is counted, how, which models), and what does the paper's Table 7 caption say about the flat condition?
- **C-R03/STUB**: "Whether distractor tools carry placeholder or stub schemas, and the effect on the 292k figure, is unverified." Question: do the stored sampler/pool sources or the dev document say anything about distractor tools' schemas (full, stub, placeholder), and which pools use them? Say plainly if none of the stored text states it.

## Steward 1d: scaffolding paper and CMTF (writes `findings/SUM-0013-batch1d-scaffolding-cmtf.md`, id FND-0011; log `evidence-steward-1d.md`)
Extract these (8):
1. `r4-scaffolding-mcp-vs-cli` lines 18-45 (abstract).
2. `r4-scaffolding-mcp-vs-cli` lines 251-296 (measures: input, cached tokens, schemas per request; proxy; corrections).
3. `r4-scaffolding-mcp-vs-cli` lines 740-800 (Table 5, cost of the MCP arm by delivery method; schemas per request).
4. `r4-scaffolding-mcp-vs-cli` lines 388-420 (how cost is reported).
5. `r3-toolmenubench` lines 15-35 and 84-90 (abstract; released artifacts).
6. `r3-toolmenubench` lines 118-135 (state-aware and causal filtering).
7. `r2-gist-cmtf-2606-16813-20261011` lines 10-40 (GIST-CMTF abstract and the assumption on CMTF's input).
8. one further range of your choice from `r3-toolmenubench` that describes how CMTF's "next causally necessary frontier" is computed in the experiments (find it with adjacent reads; say which lines).
Rows:
- **C-E01/E07**: "Scaffolding paper body unavailable; cited token/schema figures unverified." Question: what token, cached-token and schemas-per-request figures does the paper report for MCP vs CLI arms (state conditions: scaffolding, model, task, completed runs only), and how were they measured? Quote numbers with their conditions. Add an [O] on which of these bear on tool-definition token share (ledger C-S01) or cache behaviour (C-S03), as observations only.
- **C-R03/CMTF**: "How CMTF obtains its causal path is unverified; it may use information a deployed policy would not have." Question: what inputs does CMTF use in ToolMenuBench (gold trajectories? tool contracts? task state? the goal?), and what does GIST-CMTF say CMTF assumes about the user request? Quote, and state which of those inputs the texts say are available to the agent at runtime and which are benchmark artifacts.
