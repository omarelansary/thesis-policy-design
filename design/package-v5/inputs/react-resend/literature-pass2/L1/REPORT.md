# Lane L1 report: inference serving and KV-cache systems for agentic workloads

Date 2026-11-09. About 40 tool calls. Ledgers: queries.tsv, sources.tsv (S1-S25), excluded.tsv. Grades: E peer-reviewed/replicated with artefacts, M measured by authors, V vendor, T theory/proposal, U unverified. "Read" means opened with WebFetch; the fetch tool returns a small-model summary, so "full" below really means "full page via summary", and numbers should be re-checked against the paper before they go into the thesis.

## Bottom line
Nothing found overturns the thesis setup. The serving and trace literature mostly confirms it: (a) cache reads of the re-sent prefix dominating the bill is the normal regime of agent traffic, so our ~66% is typical; (b) the supervisor's "you pay twice" is right about tokens but wrong about price, because the re-sent part is billed at 0.1x-0.25x; (c) the "Claude Code makes the LLM wait" idea has no support (what exists is server-side KV retention with a TTL; the client resends everything). What does matter for design and evaluation: tool-array changes break the prefix (documented, one measured study), hit rates on hosted open-weight providers are provider-specific, and no study we found evaluates tool-subset exposure under cache accounting.

## Findings ordered by decision relevance

**1. Cache-read dominance is the generic regime, not an artefact of 469 tools. [M, several independent]**
- TraceLab (S1, 4,265 Claude Code/Codex sessions, 43 users, 2025-26): 95.7% of 54.9B input tokens were cache-read prefix; at list prices prefix tokens were 59.5% of cost, new input 29.2% (includes Claude cache writes), output 11.2%. Tool-result steps hit 97.5%; user-initiated steps 84.4%. Read: first 100k of 133k characters.
- OpenRouter's own traffic (S10, [V]): cached share of agentic prompt tokens rose from ~60% (Jan 2026) to just under 90% (Sep 2026); median provider cache rate 44% to 85%. Worked example: ~87% of tokens cached but about a third of the bill.
- OpenHands/SWE-bench Verified, 8 models (S9, [M]): cache reads are the largest token and dollar category in every phase; the text gives no numeric split.
- Conditions: list prices (Claude, GPT-5.x), coding agents, long human-paced sessions. None of these reports how much of the prefix is tool definitions (S1, S2, S9, CacheWise all say "not reported"), so our 66% for tool definitions is not directly comparable and nothing here tells us the typical tool-definition share.
- Implication: the lever is prefix size x number of requests x read price. Reducing the prefix is a real but second-order saving per token (0.1x-0.2x); cold starts, cache writes and output/reasoning tokens can offset it.

**2. The "makes the LLM wait" claim is unsupported; what exists is KV retention with a TTL. [M/V]**
- Agent traffic is a stream of independent requests whose prefix is almost entirely a repeat: 96% of Claude Code requests reuse >=90% of their input as a verbatim prefix, median 99.6%, median request only 632 tokens longer than the previous (S16, [V], Red Hat/IBM, 219 sessions). Gaps between main-agent turns: p50 2 s, p90 24 s.
- Tool latency is short but heavy-tailed: median 0.3 s, p99 3.6 min, calls >1 min are ~4% of calls but 85% of tool time (S1). Human pauses are 92% of wall-clock in interactive sessions and cause most misses.
- Continuum (S3, ICLR 2026, [M]) is the closest thing to "waiting": the engine pins a request's KV for a TTL during the tool call (1.12-3.66x lower delay, up to 8.18x, vs vLLM/InferCept/Autellix, Llama-3.1 8B/70B, SWE-bench/BFCL traces). It is an operator-side engine feature, needs engine control, was not evaluated on hosted APIs, and reports no hit rates. It is not something a customer of OpenRouter can invoke.
- So the factual description for the thesis: each ReAct step is a new request; cost is controlled by prefix cache hits (TTL minutes), which the provider decides.

**3. Changing the tool array breaks the prefix cache. [V documented; one M study; mechanism confirmed in vLLM design]**
- Anthropic docs (S6): modifying tool definitions invalidates the entire cache; changing tool_choice invalidates the messages cache; tools discovered through tool search are appended in the conversation as tool_reference so the prefix survives.
- OpenAI docs (S20): changes to tool names, descriptions, schemas or ordering break reuse from that point; the guide recommends keeping tools stable and using tool_choice or allowed_tools to restrict. For GPT-5.6 and later, cache writes are billed (1.25x for 30 min); older models have no write fee, so gpt-5-mini economics differ from the newest OpenAI models.
- vLLM (S19): blocks are hashed as a chain over parent hash and tokens, only full blocks are cached, LRU. The chat template normally renders tools before the conversation, so any change to the offered subset invalidates everything after it (inference [I]; the doc says nothing about tools).
- Measured: Lumer et al. (S5, arXiv 2601.06007, DeepResearch Bench, 40 sessions per condition per model, 10k-token system prompt) report cost reductions from caching of 78-81% (GPT-5.2, Sonnet 4.5), 38-41% (Gemini 2.5 Pro), 46-48% (GPT-4o) and state that a changing tool set invalidates the prefix. Cost used cache read/write rates by provider. Single benchmark, small n.
- Practitioner position: Manus (S4, [V], read only through a search summary) says avoid adding or removing tools mid-run and mask logits instead; MCP client guidance (S21, [T]) says a mid-conversation tool change "can cost more tokens than the definitions you removed" and suggests append-after-breakpoint or a stable meta-tool. Both are unmeasured claims.
- Implication: a policy that picks one subset per task at the start and holds it fixed is compatible with all of this; per-step re-selection is the dangerous variant. The P2 result (server-enforced offering at a fixed prefix) matches the OpenAI recommendation.

**4. Cache-hit behaviour on hosted open-weight providers is provider- and config-specific; a bill must be measured per call. [V + U]**
- OpenRouter docs (S7): read price 0.1x (Anthropic, DeepSeek) to ~0.2x (Z.AI/GLM) to 0.25-0.5x; DeepSeek write = input price; Z.AI writes free "limited-time"; MiniMax is not mentioned; sticky routing by conversation hash for 60 min, `session_id` improves hits, and sticky routing is disabled if `provider.order` is set manually.
- DeepSeek (S8): best-effort, no guarantee, TTL hours to days.
- Anecdotes (U, search snippets and S11): the same model name giving 0% to 95% across providers; GLM 5.2 low via OpenRouter vs 85%+ direct. No controlled study found.
- Implication: record `cached_tokens` and write tokens for every call; do not assume the same hit rate across arms or routes.

**5. Serving advances help operators' latency/throughput/GPU cost; none reports a customer price effect. [M, mostly self-reported]**
- Continuum, CacheWise (2.7-3.5x lower session time, 1.64-2x goodput, Qwen2.5-Coder-32B, 2xH200), KVFlow (1.83-2.19x), SAGA (1.64x), AgentServeSim, InferCept (recompute was 37-40% of forward time in 2024 engines; 1.6-2x throughput), Mooncake (115% more requests, FAST'25). All measure delay or throughput. Pass-through to a customer exists only via list prices (cache read 0.1x-0.5x; S7, S10).
- A vendor estimate for self-hosting GLM-5.2 is $0.05-0.08/M input at 24/7 GPU rental versus Z.AI list $1.40/M (S16, [V]); this shows list prices are not marginal costs and that the university vLLM server's "cost" is GPU time, not tokens.
- Not available to an OpenRouter customer: KV pinning, program-level scheduling, offload tiers, disaggregation. Available: prompt layout, session routing keys, provider choice, request count.

**6. With caching, decode dominates time; tool-definition tokens cost through per-token attention and memory, not prefill. [M, self-hosted]**
- S2 (Claude Code harness on Qwen3.6-27B/Gemma4-31B, vLLM 0.20, 5 benchmarks): empirical hit 84.6-99.5%, decode 91-98.6% of LLM time, prefill 1.4-9%; under context thrashing hit fell to 16-26% and throughput fell by up to 66%. Tools were 2-29% of runtime.
- Implication for the self-hosted arm: token savings will show up as KV capacity and hit rate under concurrency, which a single-user run will not reveal. No source isolates the latency added by tool-definition bloat (gap).

**7. Run-to-run variance is large. [M]** S9: same task differs up to 30x in tokens across runs; average most- vs least-expensive run ~2x per model. Paired designs and intervals matter (already in the thesis plan).

**8. Reducing the number of requests is a separate lever from exposure. [T/M, latency-focused]** LLMCompiler (up to 3.7x latency, 6.7x "cost" vs ReAct), AsyncLM (1.6-5.4x), PASTE (-48.5% completion time), MCP "code mode". These cut round trips or hide latency; LLMCompiler's cost is token-based and not cache-aware. Not opened beyond snippets (S14).

## Contradictory or negative evidence
- Caching is not uniformly large: 28-48% cost reduction for Gemini 2.5 Pro and GPT-4o vs ~78-81% for GPT-5.2/Sonnet 4.5; full-context caching raised GPT-4o TTFT by 8.8%; Claude's TTFT benefit fell from 19% at 3 tools to 5% at 50 tools (S5, small n, TTFT noisy).
- Production API traffic (Alibaba, S17, ATC 2025): ideal hit ratio only 54-62%, API (to-B) traffic nearly single-turn. High hit rates (95%+) are specific to agent loops with stable prefixes.
- Secondhand: Copilot coding agent ~55% hit across turn boundaries; teammates 79.4% vs explore subagents 91.3% (S24, U, not opened). Cold starts and idle gaps (a 2-30 s pause can age out a prefix on some deployments) lower real hit rates.
- TTL is provider-controlled and can change: community reports of Anthropic default 1h to 5m in early 2026 (S25, U, disputed by Anthropic).
- No independent measurement supports the Manus or MCP claim that a tool change costs more than it saves; it follows from arithmetic (one write plus reads vs removed tokens x remaining requests) and depends on remaining steps and prices.
- Cache hit does not remove decode cost (S2), so token-count reductions overstate time savings; and "tokens saved" is not "money saved" because 87% of tokens may be 1/3 of the bill (S10).
- Hybrid/linear-attention models make prefix caching harder (Tail-Replay and vLLM Kimi K3 posts, snippet level, S12). MiniMax-M3 and GLM-5.3 architecture and the ScaDS vLLM version/flags were not checked: [U]. llm-d reports ~90-92% GPU prefix hit for GLM-5.2 (MLA + sparse) on Claude Code traces (S16).

## What would change a tool-exposure policy or its evaluation
1. Price-vector sensitivity: report bills under read 0.1x/0.2x/0.5x, write 0/1.25x/2x, and TTL 5 min/30 min/1 h. GPT-5.6+ and Anthropic charge 1.25x for writes; DeepSeek charges input price; Z.AI currently free.
2. Cross-task cache warmth: the all-tools prefix is byte-identical across tasks, so after the first task it can be read from cache (within TTL); a per-task predicted subset differs per task and pays a cold start per task. If tasks run back-to-back this favours the all-tools arm; if gaps exceed the TTL it does not (S1 TTL model, S10). [I] Log cached_tokens on each task's first request and control task order and spacing.
3. Prefix-stable designs form the realistic design space: fixed per-task subset; allowed_tools/tool_choice restriction (not available on the ScaDS proxy per the repo's own notes); append-only discovery (Anthropic tool_reference, MCP guidance); logit masking on self-hosted engines. Per-step changes need a break-even test.
4. Count requests per task, not only tokens; report prefix size x requests as the driver. A policy that adds steps (search tool, re-selection) multiplies the prefix.
5. Self-hosted arms: report GPU-seconds and hit rate under concurrency, not only token counts; check prefix caching is enabled and supports the model architecture.
6. Harness correctness: for MiniMax/GLM, replay reasoning content unchanged (vendor guidance links omission to cache misses and quality loss; unmeasured) and check that serialisation of the tools array is deterministic (ordering changes were fixed in Codex via PR; blog test showed 0% vs ~94% hit, single test, U).
7. Pin the provider and, where possible, send a session id; check sticky-routing behaviour.

## Coverage self-assessment and unresolved gaps
- Searched: Continuum, InferCept, KVFlow, SAGA, AgentServeSim, CacheWise, TraceLab, agentic workload papers, Alibaba KV traces, Mooncake, vLLM APC, CacheBlend, async/speculative tool calling, vendor cache docs (Anthropic, OpenAI, OpenRouter, DeepSeek), Manus, MCP guidance, blog measurements, TTL controversy.
- Not opened (snippet-level or none): Autellix, SGLang RadixAttention, LMCache, Mooncake trace numbers, AsyncLM, PASTE, Tail-Replay, Manus primary text, Anthropic tool-search vendor numbers. Mooncake hit ratios were not retrieved.
- Gaps: (i) no trace study reports the tool-definition share of input; (ii) no study evaluates tool-subset selection with cache-aware billing (the nearest, S5, is about dynamic tool sets only and says invalidation); (iii) no systematic hit-rate data for MiniMax or GLM-5.x on hosted providers; (iv) cache behaviour of university vLLM (version, flags, model architecture) unknown; (v) CacheBlend-style non-prefix reuse could in principle make tool-definition changes cheap on self-hosted engines, but no evidence on tool definitions and none for hosted APIs.
- Method caveat: fetch summaries were produced by a small model; headline numbers (S1, S5, S10, S16) should be rechecked against the PDFs before citation.
