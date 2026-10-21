# Blind output, variant B (simplest-first), thread T-20261022-113

Verbatim final reply of the general-purpose Sonnet 5.5 instance spawned with `blind-prompt-20261022.md` (COMMON + VARIANT B), 2026-10-22; 66 tool uses. Model output, not evidence: every citation in it must be re-read before V5 relies on it. Stored by the lead because the guard refuses writes by general-purpose agents.

---

0. Project-instruction files received in my context: CLAUDE.md (with ops/STATE.md imported through its @-line). I used neither as evidence.

Abbreviations: T21 / T14 = the 21 / 14 Oct transcript files in requirements/intake/ (file line numbers); X02 = the 2 Oct excerpts file; DEC = 2026-10-21-user-decisions-after-meetings.md; REG = REQUIREMENTS REGISTER H; LIT = evidence/literature-20261019/. Extractor sources are cited as id:Lstart-Lend. Ranges marked "~" are coarse because the extractor view printed no per-line numbers.

## 1. The problem in my words

[F] The research question is to reduce the count of tools while keeping accuracy as high as possible (T14:178). The supervisor says the real aim is saving tokens, not filtering as such (X02:230-232). Filtering must not cost more than it saves (X02:70-72).
[F] The student's decisions are to minimise the bill on average over turns and sessions with accuracy nearly the same, with no margin or budget (DEC:20, DEC:28). The equation must be model-agnostic (input, reasoning, output, tools, prompt cache) (DEC:20, REG REQ-U21-07). Sessions can be one long run or returning users (DEC:26). Scope is memory and tool calls only (T21:242, T21:409).

**Decision points and what is known at each**
- D0, session start or return after a gap. Known: the invoker or role (T14:267-317), the account, the prior-session record, and the elapsed gap.
- D1, each model call. Known: the history, the cached prefix and its remaining lifetime.
- D2, after a tool result. Known: the result size.
- D3, session end. Known: the whole trajectory.
- D4, failure. Known: that a tool the model needed was not offered.

**Cost terms (my reading; sources below)**
- Per model call: uncached input × p_in + cache-write tokens × p_w + cache-read tokens × p_r + output tokens (including reasoning) × p_out, plus any helper-model and tool fees.
- [F] This is the structure used by StackOne (LIT/web-stackone-where-agent-tokens-go.txt:232-239), by the PointFive tokens-vs-cost paper (LIT/pdf-tokennotcost-2607.12161v5.txt:139-150) and by the Alier et al. scaffolding paper (LIT/pdf-scaffold-2608.08654v1.txt:227,254-255).
- The bill is summed over all calls, retries and failed attempts, and divided by completed tasks (stackone:234-239; tokennotcost:132-135).
- [F] Price multipliers: Anthropic 5-minute write 1.25x, 1-hour write 2x, read 0.1x (0.05x on Sonnet 5.5 / Opus 5.5) (LIT/price-anthropic-20261019.md:148-152). OpenAI GPT-5.6 and later: write 1.25x, read 0.1x, 30-minute lifetime (r4-openai-prompt-caching:~L1-L120). Gemini: implicit-only caching on some models and an hourly storage price on others (LIT/price-gemini-20261019.txt:149,304-305).
- [F] Two further wrinkles for a model-agnostic equation. Haiku 5.5 prices change above 100k prompt tokens (price-anthropic:34-35). Claude 4.7 and later tokenise about 30% more tokens for the same text (price-anthropic:54).

**Horizon**
- [F] The supervisor wants savings judged on average over many turns, with an occasional dearer recovery turn accepted (X02:474-488; T21:317-343). He also wants the return-after-gap case, where a summary replaces replaying a 20k-token history (T21:388-403).
- [I] In bill terms, three situations matter: the cold first call of a session, calls after the cache lifetime lapses, and warm calls.

**Worked numbers (my arithmetic)**
- Anthropic says a typical multi-server catalogue is about 55k tokens of definitions (r4-anthropic-tool-search:~L10-L12). Sonnet 5.5 rates are $2 in, $2.50 5-minute write, $0.10 read, $10 out per million tokens (price-anthropic:29).
- [I] On Sonnet 5.5, that catalogue costs about $0.11 uncached, $0.1375 to write for 5 minutes, and $0.0055 per warm read. That is about 25 warm reads per write, and about half the price of 1,000 output tokens.
- [I] A unused catalogue therefore costs little while the cache is warm. It costs a lot at cold starts and after expiry. This matches the supervisor's "hello, 10,000 tokens" complaint (T21:216-218) but not his "negligible cost" claim (T21:226-228). REG H.2 flags that tension as untested.

## 2. The policy, simplest-first (Variant B)

**S0, the starting point (not an addition).**
- Expose every tool in a byte-stable prefix, ordered tools, then system, then memory summary, then messages.
- Turn provider caching on and keep a short summary for returning users.
- Evidence it works: caching cut cost by 41-80% over 500 agent sessions at 10k-token system prompts (r4-dont-break-cache:L1-L70, abstract). The cache carried 97.1% of input in the Alier et al. sessions (scaffold:408-413). Prefix order and invalidation rules: r4-anthropic-tool-use-caching:L1-L99 ("What invalidates your cache"; changing tool definitions invalidates everything).

Parts in the order they act on a request. For each: what forced it, and the established mechanism.

**P1. Session-start filter by invoker, role or permission (static, not per turn).**
- Forced by: [I] price arithmetic above, since each removed definition is smaller in the write and in every read, and a role is constant within a session so the prefix stays stable. Also [F] hard caps: Cursor 40 (LIT/lit-cursor-forum-40-tool-limit.txt:25-29), Copilot 128 (LIT/web-slite-progressive-tool-loading.txt:41-43), Gemini 512 (LIT/pdf-mcpverse-2508.16260v2.txt:573).
- Established: the supervisor's stage one (T14:267-317). LangChain says static filtering by role or phase is a standard option (LIT/lit-langchain-progressive-disclosure.txt:92). A gateway vendor scopes tools per key so the model never sees them (LIT/web-maxim-cutting-mcp-92.txt:49, vendor claim).
- The size of the saving was not measured in the allow-list [U].

**P2. Memory: a short summary written once after a session ends and injected at the start of the next one, in the stable part of the prefix.**
- Forced by: replaying history on return is a full cold write (T21:388-403).
- Established: the supervisor's description (T21:388-403) and a plain Markdown file as the first test (T21:445-451). For the mechanism: nothing established found that measures the bill effect of summaries. I did see MemGPT-style stores named only in surveys (LIT/lit-efficientagents-2601.14192.txt:984).
- [F] Mem2ActBench reports that seven memory frameworks are inadequate at using memory to ground tool parameters (LIT/arxiv-2601.19935.txt:41-45).
- Deliberately not added: mid-session compaction. [F] OpenAI says compaction can stop prefix reuse from the first changed token (r4-openai-prompt-caching:~L1-L120, settings table). [F] Query-aware prompt rewriting invalidated the cache on every call in one study (s4-cacheaware-compress-2607-15516-20261013:L1-L60).

**P3. Deferred loading: a small core set plus a search tool, with discovered tools appended inline, never edited into the prefix.**
- Forced by: catalogue size where P1 is not enough (caps above), and cold-start cost. Not by warm per-turn cost, which is small.
- Established:
  - Anthropic tool search, with `defer_loading`. Discovered tools arrive as `tool_reference` blocks and the prefix cache is preserved (r4-anthropic-tool-use-caching:L1-L99). The docs claim over 85% fewer definition tokens and note selection accuracy degrading beyond 30-50 tools (r4-anthropic-tool-search:~L10-L16, vendor claim).
  - OpenAI `tool_search`, which injects discovered tools at the end of context (r4-openai-tool-search:L1-L70).
  - Spring AI tool-search (named in the source list; not read).
  - LangChain progressive disclosure (LIT/lit-langchain-progressive-disclosure.txt:24-27,77-86).
  - Slite reports 17 tools upfront, 65+ on demand, and 23% lower cost per question on 63 questions (LIT/web-slite-progressive-tool-loading.txt:154-159, own benchmark).
- Negative evidence the part must respect: per-step dynamic fetching that edits the tool list breaks the cache (LIT/web-agentpatterns-dynamic-tool-fetching.txt:15-25,37-45; Slite:45-62). Treat this as a secondary source; the numbers it attributes to Anthropic (55K to 8.7K tokens, 49% to 74% accuracy, lines 59-69) are not traceable here.

**P4. Cache lifetime choice, 5 minutes versus 1 hour, or periodic keep-alive reads.**
- Forced by: returning sessions and the 5-minute / 30-minute lifetimes (price-anthropic:146-152; OpenAI lifetime above). The student himself raised the one-hour idle case (T21:344-357).
- [I] The break-even is expected inter-turn gaps against the 1.25x versus 2x write price. It cannot be set without the gap distribution [U].
- Established: provider pricing and the "cache pays after one read for 5 minutes, two reads for 1 hour" statement (price-anthropic:152). Nothing established found on automatic keep-alive.

**P5. Recovery: the model can ask for held-back tools; failure escalates to a wider search, and finally to the full catalogue.**
- Forced by: the supervisor's requirement that the policy can recover when filtering was wrong (X02:470-472) and by [F] evidence that retrieval error is a main failure source (LIT/pdf-livemcpbench-2508.01780v2.txt:171,1753).
- Established: the tool-search call itself is the recovery path (P3 sources).
- [F] Accuracy risk reported by MCPVerse: most models degrade as the toolset grows, but agentic models can improve with a larger toolset (pdf-mcpverse:19-24,638-642,648-650). So accuracy forcing is model-dependent.

**Parts I considered and did not add, with the trigger that would add them**
- Tool-output offload to files ("MCP brain without notepad", T21:275-281; the 80% claim at T21:294 is an assertion).
  - Evidence against forcing it: for Claude Code runs, accessible content (tool outputs, history) was about 6% of cost, tool outputs 3.3%, and the harness base (system prompt plus tool definitions) 74.7% (LIT/pdf-tokennotcost-2607.12161v5.txt:200-222,231-278). Aggressive output compression cut delivered tool tokens by 38.4% but raised billed cost by 6.8% (tokennotcost:14-25).
  - Evidence for: stale tool results were 21.8% structural waste across 857 production sessions, and eviction cut context by up to 93% in live use (r4-missing-memory-hierarchy:L1-L45). Anthropic-reported code-mode figures (150k to 2k tokens) are secondary (web-maxim:27).
  - Trigger: tool results that are large and re-read many times.
- Helper-model or semantic multi-stage narrowing and query expansion (T14:322-337; X02:256-276). Trigger: a catalogue still too large after P1 and P3, with filtering cost measured against savings (X02:70-72).
- Memory-conditioned preloading of tools (the "both combined" decision, REG REQ-U21-04).
  - Nothing established found for memory choosing the tool set, other than LangChain's middleware that re-activates tools found by earlier `search_tools` calls from message history (lit-langchain:57-70).
  - Trigger: measured search-round-trip cost on returning sessions.

## 3. Failure, unnecessary, and the simpler alternative

**P1**
- Fails when the role or context is mis-detected, or the "never needed" assumption is false, so P5 must catch it.
- Unnecessary when the catalogue is small or every role uses everything.
- Dominated by S0, plus allowed-tools masking. OpenAI's `allowed_tools` / `tool_choice` change what is callable without deleting definitions, but the definitions still cost tokens (stackone:282-284).

**P2**
- Fails when the summary drops a fact the next task needs (Mem2ActBench, above).
- Unnecessary for single long runs with no return.
- Dominated by "no memory, start fresh", or by a plain stored last-N-turns replay. [S] Whether a summary beats replay at long gaps depends on whether the cache is already lapsed; replay would then be a cold write anyway.
- Note the memory-as-skill paper found only a 1.18x session-total difference between conditions and no detected behaviour difference between carriers in small comparisons (LIT/lit-memskill-2609.16669.txt:23-35).

**P3**
- Fails when search misses the tool (LiveMCPBench, above), when the search round trip costs more than the deferred definitions (agentpatterns:95-105: small libraries, always-needed tools, latency limits), and for providers or models without tool search. There, a client-side search must stay append-only.
- [F] A reported deferred-schema cache problem: a user says deferred MCP schemas are re-read in every call (LIT/lit-ccissue-59650-deferred-cache-reads.txt:21-41). Whether that contradicts Anthropic's "prefix untouched" statement is [U]; the issue was closed "not planned". A separate issue shows the API rejecting `defer_loading` combined with `cache_control` on one tool (LIT/lit-ccissue-30920-defer-cachecontrol.txt:31-34).
- Unnecessary under the catalogue size where S0 plus caching is cheap and accurate.
- Dominated by S0 on warm sessions with a small catalogue.

**P4**
- Fails when gaps are unpredictable (write cost wasted) or the provider's lifetime is fixed (OpenAI GPT-5.6: 30 minutes only).
- Unnecessary for single short sessions.
- Dominated by the default 5-minute tier.

**P5**
- Fails when the model is unaware it is missing a tool. Unnecessary if filtering is so loose that nothing is held back. Dominated by "always provide the full catalogue on first failure".

## 4. The simplest rival that could beat the whole policy

Rival A is S0 itself: all tools, stable prefix, caching, short summary.
- Evidence for it:
  - Warm-cache definition cost is about 5% of a fresh write (my arithmetic, section 1).
  - The harness-base cost in the PointFive study was already mostly cache reads, and compressing the accessible 6% did not reliably help (tokennotcost:200-222).
  - Selection quality is model-dependent (MCPVerse).
- It loses where caps bind, catalogues are large, sessions are short or cold, or gaps exceed the cache lifetime.

Rival B changes the interface rather than the policy: a shell and filesystem instead of a tool catalogue.
- [F] Two scaffoldings without MCP support were 5.0x to 28x cheaper than the five with MCP (scaffold:21-25). But thirteen strictly paired MCP-versus-CLI ratios ran 0.43 to 29 and were judged inconclusive (scaffold:745-756), so the cross-scaffolding gap is confounded.
- [F] A terminal-and-filesystem agent matched or beat complex architectures on enterprise tasks (LIT/arxiv-2604.00073.txt:36-40).

Rival C (outside policy scope) is a cheaper model: Haiku 5.5 input is $0.10 per million against $2 for Sonnet 5.5 (price-anthropic:29,34).

**Evidence that would decide**
- Paired arms on the same tasks: S0, S0+P1, S0+P1+P3, the full policy, and (optionally) the shell-only arm.
- Metric: billed cost per completed task (with cache-write, cache-read, uncached and output tokens separate, retries included), plus success rate against the all-tools baseline.
- Condition grid: catalogue sizes, single long run versus returning users, and gaps shorter and longer than the cache lifetime.
- Method: the PointFive-style decomposition (tokennotcost:79-85) and the supervisor's "global lens" averaging (X02:486-488).
- This follows the human's "test parts in a loop, then end to end" order (REG REQ-U21-06).

## 5. What I could not determine from the allow-list

- Independent third-party measurement of vendor tool search on bill and accuracy together. The literature README records none surfaced in three queries (LIT/README.md:12).
- The distribution of gaps and the share of cold starts in the student's target agents.
- Whether the free university API (REG REQ-U21-01) bills, caches, or exposes cache fields at all. This decides how the bill must be computed.
- Per-provider handling of reasoning tokens and of tool-definition caching for Gemini (explicit versus implicit) and for non-Claude, non-OpenAI models.
- Summary quality and cost for returning users on a tool-using benchmark. Mem2ActBench is a candidate, untested here.
- The BFCL v4 CSV, BFCL multi-turn blog, Artificial Analysis page, memory survey, MCP-Universe, ToolRet and several other stored files were not read (budget). They may contain relevant numbers.
- Unverified secondary claims: the agentpatterns accuracy table, the Maxim 92% benchmark (vendor), the supervisor's 80% saving (T21:294).
- The effect size of P1 (static filtering) in any stored source.

## 6. Paths read

design/package-v5/inputs/blind-prompt-20261022.md, requirements/intake/2026-10-21-user-decisions-after-meetings.md, requirements/intake/2026-10-21-supervisor-meeting-2026-10-21-notes-and-transcript.md (lines 150-531), requirements/intake/2026-10-21-supervisor-meeting-2026-10-14-notes-and-transcript.md (grep, lines 170-460), requirements/intake/2026-10-21-supervisor-meeting-2026-10-02-excerpts.md, requirements/REGISTER.md (lines 67-126), evidence/literature-20261019/ (directory listing, README.md, MANIFEST.jsonl, price-anthropic-20261019.md, price-openai-20261019.md (grep), price-gemini-20261019.txt (grep), web-agentpatterns-dynamic-tool-fetching.txt, web-stackone-where-agent-tokens-go.txt, web-maxim-cutting-mcp-92.txt, web-slite-progressive-tool-loading.txt, lit-langchain-progressive-disclosure.txt, lit-ccissue-59650-deferred-cache-reads.txt, lit-ccissue-30920-defer-cachecontrol.txt, lit-cursor-forum-40-tool-limit.txt (grep), pdf-tokennotcost-2607.12161v5.txt, pdf-scaffold-2608.08654v1.txt, pdf-mcpverse-2508.16260v2.txt, pdf-mcpzero-2506.01056-latest.txt, pdf-livemcpbench-2508.01780v2.txt (grep), arxiv-2508.01780.txt (grep), arxiv-2510.19286.txt, arxiv-2601.19935.txt, arxiv-2504.18851.txt (grep), lit-procmem-2602.01869.txt, lit-memskill-2609.16669.txt, arxiv-2604.00073.txt, arxiv-2511.02734.txt, lit-efficientagents-2601.14192.txt (head and grep), directory-wide greps for summarisation/cache, memory papers and tool search); origin sources via the extractor: r4-dont-break-cache, r4-anthropic-tool-use-caching, r4-openai-prompt-caching, r4-executor-readme, r4-anthropic-tool-search, r4-openai-tool-search, s4-cacheaware-compress-2607-15516-20261013, r4-missing-memory-hierarchy (plus list-sources greps for executor, cach, tool-search, compact, memory-tool, memory).
