LEAD RANKING, frozen 2026-11-01 before the independent design-proposer ranking (register 17, section 7 draft)

P5 billing mechanics
1. Real definitions: AppWorld api_docs/function_calling (457, OpenAI format, offline files) plus MCP definitions captured once from the MCP-Atlas sandbox /list-tools (220-307), sampled to each catalogue size; one short task with a stub tool result. Size distribution measured per model tokenizer before any run.
2. Size-matched synthetic definitions (constructed tools) drawn from the measured real distribution, to extend beyond the real pool (R-large) and to separate count from tokens per definition (causal control). Not a substitute for 1.
Rejected: MCP-Zero (LLM-extracted from READMEs, not real schemas), ToolRet (mostly non-MCP, short, card licence unclear), PolicyLayer (vendor, no download; size reference only), MCP registry (no tool lists), TheMCPCompany (no licence; size reference only).

P3 uninstructed search
1. MCP-Atlas subset (extension): tasks whose called tools are keyless (about 18% in sample), union catalogue declared, target deferred/withheld per cell; primary measure a deterministic tool-call check against TRAJECTORY allowing equivalents (our scorer, judge not needed); tool outputs recorded once and replayed for paired cells.
2. AppWorld train+dev (165 tasks with gold programs): offline, deterministic, 457 APIs; second family.
3. Constructed absent-target cell (ToolMATH-style distractors-only) as control.
Rejected as vehicle: BFCL missing-function (native protocol appends to tools array; small catalogue; Epoch flaws) - kept as design precedent; LiveMCPBench (no gold tools per task, live); MCPVerse (no definitions file, live); TheMCPCompany (no licence, OpenHands, Azure).

P1 returning users
1. Declared extension: returning-user sequences built from the same single-session benchmark as P3 (real tools, real tasks), recurrence of needed tools as a controlled variable, gaps from the route's measured cache lifetime, DolphinBench-style with/without-history check. Internal validity; no real-world claim.
2. VitaBench 2.0 (56 users x about 14 subtasks over time, 66 tools, MIT, OpenAI-compatible) with modifications (fixed array, memory placement, judge replaced and re-validated) as external-validity complement.
3. Momento (161 human-annotated tasks, open-weight simulator) as a small check.
Rejected as vehicle: ATRBench (pinned GPT/Gemini simulator and router; memory is preferences, not tools) - reuse its cost reporting; MPT (no environment, 13 functions, NC licence); ETAPP (no licence, single query); DolphinBench (vendor-authored, licence not stated) - reuse its validation check.

P2 subset at fixed cached prefix
1. AppWorld: all 457 declared, subset offered; deterministic unit tests; offline.
2. MCP-Atlas: union declared, ENABLED_TOOLS as the offered subset; judge-scored, validated on a pilot.
3. Toolathlon local-only (31 tasks) pending licence.

P4 masking long outputs
1. MCPMark local services (Filesystem, Postgres: 51 tasks; long inputs; Apache-2.0; deterministic verifiers, Postgres exploit known).
2. AppWorld (measure tool-output sizes first).
3. Toolathlon local-only pending licence (native large outputs measured 15-35%).

E2E
1. AppWorld as the primary accuracy vehicle (deterministic, offline), R-mid native, R-large by declared padding with real captured MCP definitions plus size-matched synthetic; sessions by the P1 extension.
2. MCP-Atlas keyless subset as a second family (real MCP), judge validated on a pilot with human labels.
3. tau2-bench for R-small multi-turn (12-15 tools), simulator replaced and reported.
Rejected: Toolathlon and TheMCPCompany (no licence), MCP-Universe, MCP-Bench, LiveMCP-101, MCPVerse (live services, keys, or no release).

Flags for V5: F1 margin or estimation-only; F2 P3's BFCL design appends to tools array; F3 P1 needs a catalogue extension (no multi-session benchmark above 74 tools); F5 regimes by tokens rather than count if defined by count; F6 scorer check on the subset used; F7 floor screening only in exploration; F8 licence decisions; F9 memory placement differs in all multi-session benchmarks (no change).
