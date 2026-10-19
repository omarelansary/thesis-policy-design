---
id: FND-0010
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-99
evidence: ["EXT-0118", "EXT-0120", "EXT-0124", "EXT-0127", "EXT-0132", "EXT-0133", "EXT-0135", "EXT-0138", "EXT-0140"]
---

# FND-0010: Batch 1c, Executor and DynamicMCPBench (AUTH-016 ledger rows)

Nine extractions, all hash-verified. Statements are labelled [F] fact in source, [O] observation, [I] interpretation, [U] unknown. Nothing here identifies the supervisor's "Executor" (CAVEATS row 6 is for the researchers). Pinned Executor sources: commit `a54b513e...`, retrieved 2026-10-11. DynamicMCPBench dev doc and code retrieved 2026-10-15 (dev branch doc; `HEAD` for code files); paper arXiv 2607.20531 retrieved 2026-10-13.

## Row AS-07 and C-D08/EXEC

Supervisor assertion A7: "'Executor' exposes connection prefixes and meta-tools (tool search, details, results) instead of listing all tools."

- Verdict: **PARTLY** (two different modes are documented; the exact A7 wording is matched in part by each, in full by neither as a single statement).
- [F] `execute` tool description holds integration slugs only. EXT-0127 (r4-executor-src-description, lines 30-35): "Available integrations (the live, per-session inventory): the top-level integration slugs the user has connected, deduped across connections, names only." Lines 92-95: "one bare line per integration slug (deduped across connections, sorted), no per-connection prefixes and no descriptions."
- [F] The description is a short intro plus pointer to a `skills` tool. EXT-0127 lines 50-54: "Execute TypeScript in a sandboxed runtime." / "Before writing code, call `skills({ name: \"execute\" })` for the workflow on how to use this tool." Lines 29-31: the how-to lives behind `skills` "to keep this always-loaded description small".
- [F] The inventory is capped. EXT-0127 line 96: `INVENTORY_LIMIT = 50`; lines 132-134: "- ... N more" marker when over the limit.
- [F] Tool names live under a namespace. EXT-0127 line 129: "Integrations you have connected. Their tools live under `tools.<...>.…`." (angle-bracket text between the dots is missing in the stored text: [U] the exact path template.)
- [F] Search and invoke (passthrough) mode exists, via `?mode=passthrough` or a "Search and invoke" toggle. EXT-0124 (r4-executor-docs-mcp-proxy, lines 81-93): "This mode exposes four discovery and invocation tools: `integrations` ... `skills` ... `search`: find tools and read their JSON input schemas ... `invoke`: call the exact tool ID from search with JSON arguments."
- [F] Schema loading in that mode. EXT-0124 lines 105-106: "The tool list stays small as you add integrations. Input schemas are loaded only for matching search results." Lines 106-107: "Your client handles approval for `invoke`, and workspace block policies still apply. This mode does not expose a general code execution tool."
- [F] Default (non-passthrough) mode: EXT-0124 lines 27-30 and 78-79 describe "one catalog" and "every integration you add to Executor appears in that agent automatically"; the proxy page does not say in the stored range whether tools are listed individually in that mode. [U]
- [F] README names no meta-tools in range except CLI commands: EXT-0120 (r4-executor-readme, lines 30-32): "executor tools search \"send email\"      # find tools by intent", "executor call github issues --help      # browse a namespace"; line 40 `executor resume --execution-id exec_123`. EXT-0118 line 58-59: "Create a connection: one configured (optionally authenticated) instance of that integration. An integration can have many connections."
- Not stated in these texts: a meta-tool called "details" or "results" (no such tool name appears in EXT-0118/0120/0124/0127); `search` returns input schemas, which is the nearest to "details". The passthrough tools are `integrations`, `skills`, `search`, `invoke`. The first tools an agent sees in the default `execute` mode are not enumerated in the stored ranges beyond `execute` and `skills` (the description mentions both). The README range 61-114 was not extracted (not in the nine). [U] whether the README says more about the session start.
- Not shown: token size of any of these tool lists; whether "connection prefixes" (A7) equals the integration slugs (the code says "no per-connection prefixes", the span attribute `executor.connection_addresses` names "callable prefixes" only in a trace comment, EXT-0127 lines 70-72: "names the callable prefixes it resolved without listing tools").
- [I] effect on the ledger row: the stored text supports "integration names, not tools, in the description" and a separate search/invoke mode with `integrations`, `skills`, `search`, `invoke`; it does not show "details" or "results" tools.
- Limits: one repository commit (a54b513e), a source-code comment is a statement of intent, not observed behaviour; vendor documentation; the `.mdx` page is a repo doc, not a deployed page.

## Row C-E01/E03

Ledger wording: "The ~292K-token flat-catalogue figure is not verified (counted surface, tokenizer)."

- Verdict: **PARTLY** (the figure is stated; its counting method is not in the extracted range).
- [F] EXT-0132 (s4f-2a-dmcp-dev-e9-1-exposure-matrix, lines 32-36): "H5 (flat feasibility). The literal flat full-catalog condition is not runnable for most of the pool: the catalog serialises to ~292k tokens of tool schema, which exceeds the context window of `kimi-k2.6` (262,144), `glm-5.1` (204,800) and `claude-haiku-4.5` (200,000). Only the 1M-context models (`qwen3.7-max`, `minimax-m3`) can be offered the whole catalog."
- [F] EXT-0132 lines 38-40: "H5 is registered as a *finding to report*, not a hypothesis to test: it follows from published context limits and the measured catalog size".
- [F] The doc says "serialises" (JSON schema serialisation) and "measured catalog size", but the extracted lines name no tokenizer, no tokenizing model, and no definition of what is counted (names, descriptions, input schemas). [U]
- [F] The catalog in the matrix is the reference-trace catalog: EXT-0132 lines 63-64: "All under `--pool full`, i.e. the entire catalog reconstructed from the reference traces, with no curated distractor pool".
- [F] Paper Table 7 caption, EXT-0140 (s4c-g2-dynamicmcpbench-2607-20531, lines 1028-1033): "Table 7: Single-attempt pass rate (%) on the 150-task subset, four candidate models against six exposure conditions. Each cell is 150 tasks and carries a 95% Wilson interval of roughly ±8 points. flat was run on one model only: 1,168 tool schemas per request is 10-30x the prompt of any other cell." Table row, line 1025: "flat (1,168)                  36.0 —".
- [O] The paper gives a count (1,168 schemas) and a ratio (10-30x the prompt of any other cell); it gives no token figure in this range. The dev doc gives ~292k tokens and no schema count in the range. Neither passage links the two numbers. Division would give about 250 tokens per schema ([I], arithmetic of two unlinked figures, not stated by either source).
- Possible inconsistency, reported plainly: the dev doc says the flat condition is "1M-context models only" and lists `minimax-m3` among the four models and `qwen3.7-max` as 1M-context (two such models); the paper says "flat was run on one model only". [F] both statements; [O] they are not contradictory (one model of the two eligible was run), but the stored text does not say which model or why. The table column layout is ragged (the flat row shows "36.0 —" under four-column text-layer garbling), so which column holds 36.0 is [U].
- Not shown: whether 292k used the same tokenizer for each model, whether 292k includes the 1,168 count's identical catalog (dev doc is of 2026 dev branch, paper later), or the effect of the paper's counted surface. Whether "10-30x the prompt" is consistent with ~292k (rag:4 prompts would then be about 10-29k tokens) is [S].
- [I] effect on the ledger row: the figure's source is now located (EXT-0132) and matches "~292K"; the unverified parts (counted surface, tokenizer) remain unverified in the extracted lines.
- Limits: dev-branch document (not a release), single-document figure, paper text layer with a garbled two-column table.

## Row C-R03/STUB

Ledger wording: "Whether distractor tools carry placeholder or stub schemas, and the effect on the 292k figure, is unverified."

- Verdict: **NOT STATED IN THIS TEXT** (in the extracted ranges; sampler lines 41-312 and pools lines 31-125 were not read).
- [F] The sampler returns catalog entries, not generated schemas. EXT-0135 (s4f-2a-dmcp-dmcp-sampling-py, lines 313-357): "Build an `n`-tool distractor set around `required` using `strategy`. The returned list never contains any required tool." `candidates = catalog.excluding(required)`; `-> list[ToolEntry]`. [O] the distractors are `ToolEntry` objects taken from `ToolCatalog`; what a `ToolEntry` contains is not in the extracted lines.
- [F] Six strategies, EXT-0133 (lines 34-50): "random", "hard_neg" ("Tools whose descriptions are lexically nearest to the required tools"), "cross_domain", "same_name" ("Same tool name on a DIFFERENT server (the SAE primitive)"), "sibling", "stratified" ("Roughly equal mix of all five"). (Docstring says "Six strategies" and lists six; stratified mixes the other five.)
- [F] Pools, EXT-0138 (s4f-2a-dmcp-dmcp-pools-py, lines 22-40): three modes `gold` / `target` / `full`. "target - required tools + a controlled distractor set built by the sampler." "full - required tools + every other tool in the catalog (lower bound)." "The pool is rendered into a tool-surface the explorer offers; calls to distractor tools simply miss the replay cache."
- [F] Dev doc for e9.1 runs "under `--pool full` ... with no curated distractor pool" (EXT-0132 lines 63-64), so the 292k catalog is the `full` mode, not `target`.
- [O] The words "stub" and "placeholder" do not occur in any of the extracted ranges (EXT-0133, 0135, 0138, 0132). The "replay cache" statement implies distractor calls are not executed; it does not say anything about their schema content.
- Not shown: schema content of a `ToolEntry`; whether distractor tools in `full` mode carry full schemas; any effect on the 292k figure. The only relevant claim is that `full` rebuilds the catalog "from the reference traces" (EXT-0132 line 63-64): [U] whether trace-derived schemas are complete; this is a possible source of stub-like schemas but the text does not say so ([S]).
- [I] effect on the ledger row: stays unverified; the stored text read here is silent. Reading `dmcp/sampling.py` lines 41-312 (ToolEntry/ToolCatalog definitions) or `dmcp/trace.py` would be needed (not in this batch).
- Limits: code on `HEAD` as retrieved 2026-10-15, a different state from the dev doc (dev branch).

## Not read in this batch
- r4-executor-readme lines 61-114 and 136-253; sampling.py lines 41-312; pools.py lines 31-125; e9.1 doc outside lines 20-70 (the first 19 lines and 71-801, including any token-count method); paper outside lines 1020-1036.
