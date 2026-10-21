# Blind output, variant A (evidence-led), thread T-20261022-113

Verbatim final reply of the general-purpose Sonnet 5.5 instance spawned with `blind-prompt-20261022.md` (COMMON + VARIANT A), 2026-10-22; 67 tool uses. Model output, not evidence: every citation in it must be re-read before V5 relies on it. Stored by the lead because the guard refuses writes by general-purpose agents.

---

0. Project-instruction files received in my context: CLAUDE.md (thesis-policy-design operating instructions) with its imported ops/STATE.md, plus two system reminders (git attribution; user email). I did not use STATE.md's content. It names earlier packages that are outside the allow-list, and I did not open them. I did read lines 100-189 of the 21 Oct file, which include the machine-written notes (L104-136). I took nothing from them and use only transcript lines.

Citation aliases:
- U = requirements/intake/2026-10-21-user-decisions-after-meetings.md
- S21, S14, S02 = the 21 Oct, 14 Oct and 2 Oct supervisor files in requirements/intake/ (file line numbers)
- LIT = evidence/literature-20261019/
- Origin sources are cited as id:L, and their line numbers are counted from the printed range (about +-3 lines where I give ranges).

## 1. The problem in my words

**Goal.** Minimise the bill averaged over turns and sessions while accuracy stays nearly the same. There is no margin, budget or threshold (U:L28, U:L20). The supervisor's research question is "most optimal way to reduce the count of tools while keeping the accuracy as high as possible" (S14:L178). He treats tool count as the means and tokens as the aim (S02:L242-248, S02:L70-72 as numbered in the file). Scope is memory and tool calls only (S21:L242). Memory should help tool calls (S21:L242, S21:L409). [F]

**Decision points** (my reading of the transcripts [I]):
- **D0, session start or return.** Known: deployment, invoker or role (S14:L267-280, the AI-salesman example), the stored memory, the time since the last call (cache age), and the tool catalogue. Not known: the task.
- **D1, each user turn.** Known: the message, the in-session history, and the memory. Not known: which tools will be needed.
- **D2, each model call inside a turn.** Known: tool results so far and the model's own request for a capability. Not known: whether the offered set was sufficient.
- **D3, end of turn or session.** Known: the outcome and the tool question-and-answer pairs. Decision: what to write to memory and what to drop (S21:L252-262, S21:L388-394).

**Bill terms.** Per model call: uncached input x p_in, plus cache-write tokens x (1.25 or 2) x p_in, plus cache-read tokens x (0.1, 0.05 or 0.025) x p_in, plus output tokens (including reasoning) x p_out, plus any tool-specific charges. Also a hidden system-prompt overhead whenever tools are present (286-675 tokens per request, LIT/price-anthropic-20261019.md:L242-259), and helper-model calls for filtering or summarising (S02:L70-72). [F]
- Anthropic's multipliers are at LIT/price-anthropic-20261019.md:L146-152 and its per-model prices at L17-29.
- Gemini bills thinking tokens as output (LIT/price-gemini-20261019.txt:L140). Its newest model has implicit caching only (L149). Explicit caches are charged per hour of storage (L304).
- OpenAI lists cached-input and cache-write columns (LIT/price-openai-20261019.md:L32-40).
- Task cost = sum of all calls and retries divided by completed tasks (LIT/web-stackone-where-agent-tokens-go.txt:L234-239; LIT/pdf-tokennotcost-2607.12161v5.txt:L140-161).
- Counters such as turns, tool calls and retries are diagnostics, not factors to multiply (stackone L241-247).

**Horizon.** The supervisor wants savings judged on average over many turns, with dearer recovery turns allowed (S21:L317-343). Sessions include one long run and returning users (U:L26). A return after a gap matters because the cache lives only 5 minutes or 1 hour (price-anthropic:L148-150). [F]

**Facts that shape the design.**
1. In Claude Code workloads, the harness base (system prompt plus tool definitions) was 74.7% of billed cost, and cache creation plus reads were about 87% of the reconstructed cost (tokennotcost:L79-85, L201-218, Table 1 L231-279). [F, one vendor-neutral study, 5,500 billed runs, coding agents, Haiku 4.5 prices]
2. Cutting 38.4% of tool-output tokens raised billed cost by 6.8% (tokennotcost:L17-22). Token count is not cost. [F]
3. Cost is also driven by what a change does to the number of turns and to success (tokennotcost:L179-183). [F]

## 2. The policy proposed (in the order it acts on a request)

**P0. Stable cached prefix.** The prefix is system prompt, then a small always-loaded tool set (3-5 tools in Anthropic's guidance, 13 in Copilot's), then a short category index of the deferred tools. It is byte-stable within a session, and caching is on.
- Established: Anthropic documents that modifying tool definitions invalidates the whole cache and that changing tool_choice or thinking parameters invalidates the messages cache (r4-anthropic-tool-use-caching:L43-61). Community and vendor pages say the same: dynamic per-step tool swapping "breaks KV cache" (LIT/web-agentpatterns-dynamic-tool-fetching.txt:L13-25, L47-71, L117), and OpenAI guidance is to change allowed_tools instead of deleting definitions (stackone-tokens:L282-284, secondary). [F]
- Anthropic recommends keeping 3-5 frequent tools non-deferred and describing tool categories in the system prompt (r4-anthropic-tool-search, "Optimization tips", about L805-815).

**P1. Static filter by invoker, role or deployment (supervisor's "stage one").** Tools that this invoker can never need are not in the catalogue for this session at all. It costs zero tokens and is decided once at D0.
- Established as a mechanism: static allowlists and usage-derived core sets. Copilot cut 40 built-in tools to 13 core ones "based on tool usage statistics" (r4-github-copilot-fewer-tools:L415-425). LangChain hard-codes a CORE_TOOLS set (LIT/lit-langchain-progressive-disclosure.txt:L37-38).
- "Invoker-conditioned filtering" itself: nothing established found in the allow-list beyond the supervisor's example (S14:L267-317).

**P2. On-demand discovery of the remaining tools, with expansion as the recovery path.** Deferred definitions are searched by embedding, BM25 or regex and appended inline in the messages, so the prefix is untouched (r4-anthropic-tool-search:L575-590). The model can re-search when the first result misses, which is the supervisor's required way back (S02:L25-33 context, S21:L317-343, S14:L411-425).
- Established: Anthropic tool search, with deferral cutting about 55k tokens to about 8.7k and accuracy rising from 49% to 74% on Opus 4 and from 79.5% to 88.1% on Opus 4.5 (r4-anthropic-advanced-tool-use:L40-70). These are vendor-internal numbers. [F as claim]
- Established: Copilot virtual tool groups plus embedding routing (94.5% coverage, against 87.5% for LLM-based selection and 69.0% for the static list) (github-copilot:L395-415).
- Established: LangChain middleware and langgraph-bigtool (r4-langgraph-bigtool-readme:L1-20), Spring AI (r4-spring-tool-search-blog, measured 34-64% token savings), and MCP-Zero (LIT/pdf-mcpzero-2506.01056-latest.txt:L66-70).
- The supervisor's Executor "search/detail/result" tools (S02:L311-321) are another implementation of P2.

**P3. Memory read (D0 and D1).** Inject a short summary of past interaction and the relevant memory slices (preferences, tool configurations, earlier tool question-and-answer pairs). Give more only when asked (S21:L388-407, S21:L445-447). Memory can also tell P1 and P2 which tools to preload in the always-loaded set for this user (U:L17, combined staged policy and memory).
- Established for the memory part: "shared selective persistent memory" keeps four categories (specs, schemas, tool configurations, output constraints) and drops traces. It completed 12/12 at 3.9K input tokens, against 8/12 at 7.7K for full history and 0/12 for no memory. It is one deployment and small N (LIT/arxiv-2607.09493.txt:L28-61, L127-135). [F]
- Established, as benchmarks only: Mem2ActBench tests memory for choosing tools and grounding parameters (LIT/arxiv-2601.19935.txt:L20-24). MPT found that memory systems "often fail to improve on full-history prompting" (LIT/arxiv-2604.17886.txt:L25-31).
- Memory that decides which tools are offered, per user: nothing established found. The Claude Code issue only proposes lazy loading and eviction (LIT/lit-ccissue-59650-deferred-cache-reads.txt:L44-47, L67). The Copilot post lists memory-informed tool choice as future work (github-copilot:L440-447).

**P4. Large tool results go to a file or code step and only an excerpt or summary enters the context (conditional).**
- Established: Anthropic Programmatic Tool Calling, with average tokens down from 43,588 to 27,297 (r4-anthropic-advanced-tool-use:L168-171, vendor-internal), and the supervisor's files-not-context example (S21:L275-281).
- This part is conditional (see section 3).

**P5. Memory write (D3).** Store the tool question-and-answer pairs and 3-4 lines of summary. Discard reasoning traces and raw tool responses (S21:L388-407; arxiv-2607.09493:L127-135). The traces being "not worth their price" is a measured cost claim in that paper, not a measured harm (L130-135).

**Cut because the evidence does not support them** (the evidence-led pruning Variant A asks for):
- A multi-stage narrowing graph of 1,000 to 800 to 500 to 200 to 10 (S14:L329-337, L407-425). Stored evidence supports a static filter and one on-demand search level. It shows no benefit of extra stages. Each extra stage adds a call and a cache risk. [I]
- LLM-based filtering or clustering. Copilot found it slow, token-expensive and worse than embeddings (github-copilot:L385-395, L413). The supervisor also bars helpers that cost more than they save (S02:L70-72).
- Per-step swapping of definitions in the prefix (agentpatterns:L13-25).
- Name-only and tiered partial-information schemes (S02:L248-268) beyond the P0 category index. No stored evidence tests the tiers. [U]
- Anticipation beyond the role filter in P1 (U:L24, small part).

## 3. For each part: when it fails, when it is unnecessary, simpler alternatives

**P0 (stable prefix).**
- Fails if the provider does not cache or hit rates vary. Artificial Analysis says hit rates "vary significantly by provider routing" (LIT/web-artificialanalysis-coding-agents.txt:L82). Gemini's newest listing is implicit-only (price-gemini:L149). The student's university API is unknown [U].
- Unnecessary when the catalogue is tiny (Anthropic: under 10 tools or under 100 tokens of definitions, tool-search:L805-815).
- Dominating alternative: none cheaper. It is the baseline of every other part.

**P1 (static filter).**
- Fails if roles are mislabelled or the same session crosses roles. A filtered-out tool is then impossible to call without P2.
- Unnecessary if P2 already makes unused tools cost near zero.
- Simpler alternative that could dominate: no role filter, only P0 plus P2. The stored evidence does not isolate the filter's value. [U]

**P2 (deferred discovery).**
- Fails on weak search: "poor search hits miss tools, and that hurts task completion more than cache breaks cost" (agentpatterns:L103-105). It also fails through extra round trips: the Spring benchmark used 4 requests where the baseline used 3, and was preliminary, a few runs, total tokens only (spring-blog, about L282-330). It fails on near-duplicate tools, where a retrieval shortlist of 5 found nothing on hard queries (LIT/arxiv-2605.24660 via s4c-g3-howmanytools-pdf-2605-24660:L16-22).
- Fails if the platform forbids the combination: a tool with defer_loading cannot carry cache_control (tool-search about L795-800; LIT/lit-ccissue-30920-defer-cachecontrol.txt:L33-34).
- Unnecessary when the whole catalogue is small, or when caching works and defs are cheap. My arithmetic [I], with cited prices:
  - At Sonnet 5.5 prices ($2 input, $0.10 cache read, $2.50 5-minute write, $10 output per MTok), 55k tokens of definitions cost $0.0055 per cached call and $0.11 per uncached call.
  - A cold cache costs $0.1375 to write.
  - One search round trip costs about $0.003 or more.
  - So P2 saves clearly on a cold or uncached session. It saves little per call on warm cached sessions, where its main remaining benefit is accuracy.
- Dominating alternatives:
  - All tools plus caching (rival R0 below).
  - A static core set only (no discovery), which Copilot found improved success by 2-5 points (github-copilot:L422-424).
  - Provider-native tool search, instead of a custom one.

**P3 (memory read).**
- Fails by injecting stale, wrong or irrelevant memory. Memora reports frequent reuse of invalid memories and only "marginal" gains from memory agents (LIT/arxiv-2604.20006.txt:L34-39).
- A summary can lose details the tool call needs, and it costs a helper-model call to write.
- The 1.18x session-total difference and tied first-turn tokens in one measured skill-memory system (LIT/lit-memskill-2609.16669.txt:L26-34) suggest memory overhead can cancel the savings.
- Unnecessary for single-session, stateless agents.
- Dominating alternative: no summary, only caching of the full history. Compaction invalidates the messages cache, and the stored text does not price it. [U]

**P4 (result offload).**
- Fails if offloading makes the agent re-read or re-search. Compression of tool output cost +6.8% with a 38.4% token cut (tokennotcost:L17-22). Tool outputs were only 3.3% of cost in those coding workloads (Table 1, L250-254).
- Unnecessary when results are small. Anthropic itself lists "quick lookups with small responses" as a poor case (tool-use advanced, about L205-212).
- Whether the target agents (sales, recruiting) have large tool outputs is unknown. [U]
- Dominating alternative: nothing (do not offload). This is the first part to cut if measurement shows a small addressable share.

**P5 (memory write).**
- Fails if discarded traces were needed (the memory paper tested cost, not harm: arxiv-2607.09493:L130-135).
- Unnecessary if no cross-session return is expected.
- Simple alternative: keep the full history and rely on caching. The same paper found full history gave "no improvement at all despite 9x the input" when users re-specify (L56-61), but on its public-data replication full history moved the result from 0/12 to 8/12 (L86-93).

## 4. The simplest rival and the evidence that decides

**R0: expose every tool, use provider caching, and keep a short rolling conversation summary.** Why it could win:
- Cache reads cost 0.1x, 0.05x or 0.025x of input (price-anthropic:L146-152), and the supervisor himself says cached additions cost "negligible" (S21:L226-228).
- Tool definitions are a fixed cached prefix (tokennotcost Table 1).
- Any change to definitions is a cache-break risk (tool-use-caching:L43-61).

Why it could lose:
- Cold sessions pay the 1.25x write on the whole prefix, and the "hi" session is the supervisor's cost case (S21:L373-379, S21:L216-218). Whether the cache is shared across users is [U] in the allow-list.
- Accuracy falls as the visible tool count grows. Copilot saw 2-5 points; the StackOne summary of the LangChain benchmark shows GPT-4o at 2% across seven domains; ToolMenuBench reports task success of 32.1% under all-tools exposure against 85.7% for its causal filter, with about 98% fewer tokens (r1-toolmenubench:L14-22). These are vendor and benchmark claims on older or synthetic settings. [F as claims, I]

**R1: a static usage-derived core set plus the provider's native tool search, with no custom memory.** This is the likelier practical winner on engineering grounds, because it uses mature mechanisms.

**Evidence that would decide** (nothing here fixes a threshold):
- Paired runs on the same tasks and models, billed or reconstructed by component (uncached, write, read, output, helper calls), reported as cost per completed task, as in tokennotcost:L154-161.
- Arms: R0, R1, the full policy P0-P5, and each part removed one at a time.
- Session shapes: a "hi" bounce, a 7-10 turn sale, a return after a gap longer than the cache lifetime, and a long run.
- Catalogue sizes spanning tiny to several hundred tools, and at least one provider where caching is off or implicit-only.
- Repeated runs for variance (S21:L458-462).
- Process and scope follow U:L19 and the supervisor's "don't engineer it at all" until results (S21:L472).

## 5. What could not be determined from the allow-list

- Whether the prompt cache is shared across users and sessions with an identical prefix. Stored pages describe lifetimes and prices, not sharing. This decides whether cold-start cost is per session or amortised.
- The cache behaviour and billing of the university API and its models.
- OpenAI reasoning-token billing detail and the OpenAI tool-search interaction with caching. The OpenAI tool-search guide exists in the origin as r3-openai-toolsearch and r4-openai-tool-search, but I did not read it.
- An independent replication of Anthropic's tool-search accuracy numbers, or any third-party measurement of billed cost under tool search. Round 3 of the literature README also records that none surfaced (LIT/README.md:L12).
- Current-model results for tool-count degradation. The StackOne figures are early-2025 models (stackone-ceiling, about L240-262), and the same page says newer models may hold up longer.
- Memory-versus-full-history results for tool-calling agents on a billed-cost basis, beyond the single small-N paper (arxiv-2607.09493) and benchmarks.
- The real size of tool outputs, of history and of memory in sales or recruiting agents, and the real distribution of gaps between returns.
- The cost of the helper call that writes a summary, and whether compaction breaks the messages cache.
- Per-role tool usage frequencies, which a P1 filter and a core set both need.
- Not read, so not used: the Executor source, ScaleMCP, LiveMCPBench and ToolRet result tables, the BFCL data file, and the gh-api-langgraph-bigtool .dat file.

## 6. Paths read

requirements/intake/2026-10-21-user-decisions-after-meetings.md, requirements/intake/2026-10-21-supervisor-meeting-2026-10-21-notes-and-transcript.md (L100-519), requirements/intake/2026-10-21-supervisor-meeting-2026-10-14-notes-and-transcript.md (grep, L170-459), requirements/intake/2026-10-21-supervisor-meeting-2026-10-02-excerpts.md (L1-400), requirements/REGISTER.md (L67-126), evidence/literature-20261019/ (directory listing, README.md, MANIFEST.jsonl pattern grep, pages/INDEX.md, price-anthropic-20261019.md, price-openai-20261019.md, price-gemini-20261019.txt, lit-ccissue-59650-deferred-cache-reads.txt, lit-ccissue-30920-defer-cachecontrol.txt, web-agentpatterns-dynamic-tool-fetching.txt, pdf-tokennotcost-2607.12161v5.txt, web-stackone-where-agent-tokens-go.txt, web-artificialanalysis-coding-agents.txt, lit-procmem-2602.01869.txt, lit-memskill-2609.16669.txt, lit-efficientagents-2601.14192.txt, pdf-scaffold-2608.08654v1.txt, arxiv-2604.20006.txt, arxiv-2607.09493.txt, arxiv-2604.17886.txt, arxiv-2601.19935.txt, arxiv-2604.19749.txt, pdf-mcpzero-2506.01056-latest.txt, lit-langchain-progressive-disclosure.txt, pdf-memory-survey-2602.06052.txt via grep, arxiv-2602.11541.txt, web-slite-progressive-tool-loading.txt via grep), origin sources via the extractor (r4-anthropic-advanced-tool-use, r4-anthropic-tool-search, r4-anthropic-tool-use-caching, r4-github-copilot-fewer-tools, s4c-g3-howmanytools-pdf-2605-24660, r4-langgraph-bigtool-readme, r4-spring-tool-search-blog, s4f-2b-tooluse-tax-2605-00136, r1-toolmenubench, s4b-wb-stackone-20261013, plus --list-sources --grep tool; r4-speakeasy-dynamic-toolsets has no stored text).

## Lead's note on the independence check (not part of the reply)
Instance A reports reading lines 100-189 of the 21 Oct file, which include machine-written notes (L104-136); it states it used only transcript lines. Both instances received CLAUDE.md and ops/STATE.md automatically, which name the earlier packages; neither reports opening them. Instance B reports reading `r4-executor-readme` through the extractor (allowed). The tool logs were not inspected line by line (the transcript files are not to be read into the lead's context); the check rests on the instances' own path lists.
