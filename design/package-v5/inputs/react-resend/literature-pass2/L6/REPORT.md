# L6 report: provider mechanisms, pricing structure, practitioner evidence (fetched 2026-11-09)

Grades: [DOC] provider documentation (behaviour, not measurement); [V] vendor claim; [M] measured by authors; [E] peer-reviewed/replicated; [T] theory; [U] unverified. Source ids refer to sources.tsv. No source in this lane is [E]; the three arXiv items were read abstract-only.

## 1. Pricing structure today (all [DOC] unless stated)

| Route | Cache read vs input (r) | Cache write | TTL | Notes |
|---|---|---|---|---|
| Anthropic (S01) | 0.1x default; 0.05x Opus 5.5 / Sonnet 5.5; 0.025x Fable 5.1 / Mythos 5.1 | 1.25x (5 min), 2x (1 h) | 5 min, refreshed free on each use; 1 h optional | min 512-4096 tokens by model |
| OpenAI, older models incl. gpt-5-mini (S08, S09) | 0.1x (gpt-5-mini $0.025/$0.25) | none | in_memory ~5-10 min (up to 1 h) or 24h | usage `cached_tokens` |
| OpenAI GPT-5.6+ (S08, S09) | 0.1x; 0.05x GPT-6.1 Sol/Terra | 1.25x (30 min), 2.5x (12 h) | 30m default / 12h | `cache_write_tokens` reported; no breakpoints means no caching |
| Qwen (S19) | explicit 0.1x; implicit 0.2x | explicit 1.25x; implicit 1.0x | 5 min / indeterminate | tool definitions cannot be cached on their own |
| xAI (S20) | 0.25x (Grok 4.7/4.6), 0.15x (4.5) | none | not stated | |
| DeepSeek (S17, S12) | 0.1x (via OpenRouter table) | 1.0x | hours-days, best effort | separate hit/miss fields |
| Z.ai GLM direct (S18) | "usually 50%" on its own page; ~0.19 on its OpenRouter endpoint | none | not stated | official pages disagree |
| MiniMax M3 (S15, S14) | 0.2x on 10 of 11 OpenRouter endpoints | no field | - | direct price page not opened |
| Gemini (S16, S12) | 0.25x per OpenRouter; page gives no price | implicit none; explicit storage fee (third-party: $4.50/MTok/h, [U]) | - | `total_cached_tokens` |

**Finding 1: r is not a constant, and no single trend dominates [DOC, M-listing].** Across the cited first-party pages r spans 0.025 to 0.5. Frontier Anthropic/OpenAI tiers moved from 0.1 towards 0.05 and 0.025 on some newest models (S01, S09). The open-weight market is the opposite: for GLM-5.3 on OpenRouter, 45 endpoints show r from 0.10 (BaseTen, Mistral) to about 1.0 (Relace, AkashML, Wafer, i.e. no cache discount), with 0.186 as the mode (GMICloud fp8 = 0.186) (S14). MiniMax-M3 is tight, 0.167-0.217 (S15). So the project's routes (0.2, 0.1) are typical, not extremes. Decision relevance: the bill equation should keep r (and write multiplier w) as per-route parameters; an open-weight endpoint with r near 1 makes fixed tool prefixes cost almost full input price on every request, so exposure control pays far more there; at r=0.025-0.05 the prefix-read share shrinks and fresh input, cache writes and output dominate. No evidence found that r is converging to one value. Limitation: catalogue snapshot summarised by the fetch tool.

**Finding 2: batch/flex discounts leave r unchanged [DOC].** OpenAI Batch and Flex halve both input and cached input (gpt-5-mini $0.125 / $0.0125); Fast (priority) raises both (S09). So the ratio, and thus exposure-policy break-even, is unchanged; absolute bills move. Kimi batch is 60% of price (S21). Only Anthropic's batch/cache stacking was not verified (pricing page truncated).

**Finding 3: cache write fees and TTL matter at specific places, not inside a short ReAct episode [DOC, M].**
- Within one episode of consecutive requests, every request refreshes the cache (Anthropic: refresh free on use; S01), so the 1.25x write is paid once per new prefix segment. That applies to the project's OpenRouter routes only if the endpoint charges writes; none of the GLM/MiniMax endpoints list a write price except Bedrock for GLM (S14, S15).
- The write fee is new for OpenAI GPT-5.6+ (1.25x or 2.5x) (S08). A study run on gpt-5-mini would not see it; a replication on a newer OpenAI model would. This must be a parameter, not an assumption of zero.
- Across user turns, idle time breaks the cache: in 13M Copilot sessions server KV hit rate was ~90% within a turn and ~55% across turn boundaries, with minutes of idle time [M, abstract-only] (S25). Hence a "returning user" session pays a re-write of the whole fixed prefix once per return, at 1.25-2x on Anthropic. A smaller exposed tool set shrinks this cost too.
- Context editing, compaction and model switches also invalidate prefixes and cost writes (S05, S22, S25).

**Finding 4: nothing found removes the per-request re-read charge [DOC, U].** Managed Agents advertise "built-in prompt caching" but state no flat or free cached-token pricing on the fetched page; the session billing was not found (S06). Coding-plan subscriptions meter cached tokens, at least on GLM (own multiplier in a credit formula) (S32, snippet). The only "free" cases are: promotional free writes (Z.AI listed as limited-time free in S12) and self-hosted/university serving where there is no per-token price (but see Finding 7). Not found in the stated places is not "does not exist".

## 2. Server-side exposure mechanisms and what they do to the bill

**Finding 5: the vendors now ship exactly the two exposure routes under study, and document both as cache-preserving [DOC].**
- Anthropic tool search with `defer_loading`: deferred tools are excluded from the prefix; discovered ones are appended as `tool_reference` blocks; "the prefix is untouched" (S02). But the full definitions are still sent in `tools` on every request ("you still send every tool's full definition") (S03), so this is a context/accuracy device and a billing device only if the server leaves them unbilled; the page says loaded definitions bill as ordinary input and search itself is not metered (S03). Whether deferred, unloaded definitions are billed was not stated: [U]. Deferred tools cannot carry cache_control (S03).
- OpenAI `allowed_tools`: restricts callable tools "without changing the tool list" explicitly to keep caching; definitions are billed as input tokens (S11). OpenAI `tool_search` (gpt-5.4+): loaded tools appended at the end; changing the loaded set "will break the model's cache from that point forward" (S10).
- Inline mid-conversation tool changes without invalidation exist as an Anthropic beta (`inline-tools-2026-09-15`, S01).
- Prefix hierarchy: any tool-definition change invalidates tools, system and messages (S01, S02); `tool_choice` changes invalidate messages only.
Decision relevance: a policy that varies the visible tool set per request on the client route (rewriting `tools`) forfeits the cache on every change; the documented cache-safe patterns are fixed prefix + server-side restriction, or append-only discovery. This is consistent with the project's server-enforced offering result (P2) and its D-01/D-01h split. These are [DOC]; none quantifies the bill effect.

**Finding 6: vendor accuracy/token claims for tool search are [V] and token-based.** Anthropic reports Opus 4 49->74% and Opus 4.5 79.5->88.1% on an MCP evaluation and 77K->8.7K context tokens (S04); no methodology, no billed-cost figure. They support the "accuracy at nearly the same or better" side but cannot be used as bill evidence, and they predate the 0.05x read price that shrinks the dollar value of removing a prefix.

## 3. Practitioner and production evidence

**Finding 7: tool-set stability is a first-order design rule in production harnesses [V/M-practice].** Anthropic's Claude Code team alerts on cache hit rate and "treat[s] them as incidents"; "adding or removing a tool invalidates the cache for the entire conversation"; they keep all tools in every request, implement plan mode as tools, and use `defer_loading` stubs in stable order (S22). Manus: KV-hit rate is "the single most important metric", avoid adding/removing tools mid-iteration, mask logits instead (S23). Neither gives numbers. They say the supervisor's concern ("each request re-sends the same input") is real but handled by caching, and that dynamic exposure is the thing to be careful about.

**Finding 8: token reduction is not bill reduction [M, preprint, abstract-only].** Weinberger and Hozez (S24): the strongest compression removed 38.4% of tool-output tokens and raised billed cost 6.8%; correlation between token and cost reduction r=0.15; cache creation and reads dominate input-side cost; recommend cost per successful task. A secondary blog reports bill composition cache writes 44.3%, reads 35.4%, output 10.4%, and tool definitions plus system prompt ~94% of input attribution (S27, [U]). If correct, it is the closest published analogue of the project's finding (66% cache-read bill). Caveat: single harness (Claude Code), cache-write-heavy because Anthropic charges writes; the project's no-write routes will show a different mix.

**Finding 9: measured cache savings in agent loops are large but conditional [M].** Lumer et al. (S26): 41-80% cost reduction and 13-31% TTFT across OpenAI, Anthropic and Google on 500+ sessions with 10k-token system prompts; benefit scales linearly with prompt size once above the provider minimum; dynamic function calling and dynamic tool results hurt. Community counts of Claude Code sessions: cache reads 66% of one session's cost, ~97% of tokens elsewhere (S31, snippet-only, [U]).

**Finding 10: self-hosted vLLM hit rates can collapse (relevant to the free university server) [V/U].** vLLM project posts: >96% prefix hit on agent traces, but 1.7% hit rate for GPU-only prefix cache on 610 Codex traces vs 92.2% with a shared KV store; when the workload overflows GPU cache the hit rate falls to ~0 (S30, snippets). Therefore a vLLM run's "token" cost has no price, and its latency/throughput reflect load, not exposure policy.

**Verifying hits and what providers do not report.**
- Anthropic: `cache_read_input_tokens`, `cache_creation_input_tokens` with 5m/1h split; total input = input + read + creation; both zero means below minimum (S01). Server-tool loops add unrequested 5-min writes (S02).
- OpenAI: `cached_tokens`, `cache_write_tokens`, TTL breakdown on 5.6+ Responses; older models round cached tokens down to 128; caches are per machine, overflow routing above 15 req/min; keys "influence routing; they do not pin" (S08).
- OpenRouter: `cached_tokens`, `cache_write_tokens`, `cache_discount`; a secondary source warns fields appear on every provider including ones where caching is not native, so zeros and nonzeros are weak evidence of provider behaviour [U] (S12, search snippet). Default routing is price/throughput-weighted random across endpoints, stickiness lasts 60 min and exists only in default routing; manual `order` bypasses it (S12, S13, S33). Session detection hashes first messages, so agents that vary them lose stickiness (S33).
- DeepSeek: "best-effort", no guaranteed hit rate (S17). Qwen implicit: not guaranteed (S19).
- Not reported: why a miss happened (Claude Code added this client-side only, per snippet), cache lifetime remaining, the machine/endpoint that served the hit, and for implicit caches any commitment.

## Contradictory or negative evidence
- OpenRouter's table lists OpenAI reads at 0.25-0.5x (S12) while OpenAI's own pricing shows 0.1x for the models checked (S09): third-party routers lag first-party pages.
- Z.ai's page says hits are "usually 50%" (S18) while its OpenRouter endpoint is ~0.19 (S14).
- Anthropic says deferred tools preserve the cache (S02) but a Hermes doc (search snippet) said deferred schemas get no benefit from the cached prefix, and tool search adds extra turns and ~200-300 tokens of overhead; poor search hits can cost more than a cache break (snippet, [U]). Anthropic's own page recommends tool search only at >=10 tools or >10k definition tokens (S03).
- Compression that cuts tokens can raise bill (S24). Tool search's published gains are in tokens, not bills (S04).
- Cache-bug example: a Claude Code history-clearing bug rebuilt context every turn (S29, secondary, [U]).
- No independent measurement of tool search on billed cost was found.

## What would change a tool-exposure policy or its evaluation
1. Evaluate on bill with route-specific r, write multiplier w and TTL as parameters; report them with the result (S01, S08, S14).
2. Include writes and idle-gap rebuilds in the equation for any Anthropic/OpenAI 5.6+ route; omit them only for routes whose docs say writes are free, and say so.
3. A route with r near 1 (several GLM endpoints) is where client-side or server-side exposure control would pay most; r of 0.025-0.05 shrinks the effect. Report break-even tool counts per r.
4. Policy must be cache-stable: fixed prefix + `allowed_tools`/deferral, or append-only; any per-request rewrite of `tools` is priced as a full miss (S01, S10, S22).
5. Success-adjusted cost (S24) and a hit-rate audit per run (usage fields; single pinned endpoint; set `session_id`) are the evaluation standards practitioners use.
6. If the vLLM server is used, record load-dependent cache behaviour separately (S30).

## Coverage self-assessment and unresolved gaps
Covered with primary pages: Anthropic, OpenAI, OpenRouter, Qwen, DeepSeek, Z.ai, Gemini (no prices), xAI (partly), Kimi (tables missing). Not opened: Mistral and MiniMax first-party pricing (MiniMax only via search snippets and OpenRouter), Anthropic batch/caching stacking and Managed Agents session pricing, Gemini price page, Anthropic April postmortem primary, Aider/Cline/OpenHands/Cursor posts, forum threads on billing surprises. The three arXiv papers were abstract-only; the bill-composition numbers rest on a secondary blog. No [E] sources. Counts from search snippets (S30-S32) are unverified. Nothing here shows the supervisor's concern is mistaken: re-sent input is real and billed; the evidence says caching makes it cheap, not free, and its size varies by route by up to 40x in r.
