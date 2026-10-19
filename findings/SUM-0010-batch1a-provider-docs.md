---
id: FND-0008
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-99
evidence: ["EXT-0115", "EXT-0123", "EXT-0131", "EXT-0137", "EXT-0141", "EXT-0142", "EXT-0143", "EXT-0144", "EXT-0145"]
---

# Batch 1a: provider caching and billing pages (AUTH-016)

Scope: nine stored-text ranges, read in full as extracted. Prices EXT-0085..0089 were not repeated. Quote line numbers are source-text lines, computed from the extract body (line 1 of the body = first line of the range). All pages are vendor documentation retrieved 2026-10-11 (see each EXT front matter); statements are vendor claims about their own documented behaviour, not tested behaviour. [F] = fact in source, [O] observation, [I] interpretation, [U] unknown.

Extract map: EXT-0115 anthropic-prompt-caching 606-656; EXT-0123 anthropic-prompt-caching 1770-1806; EXT-0131 anthropic-tool-search 760-840; EXT-0137 bedrock 55-85; EXT-0141 gemini-caching 340-380; EXT-0142 openai-prompt-caching 48-116; EXT-0143 mcp-caching-2026-07-28 1-177 (whole page); EXT-0144 anthropic-ptc 30-60; EXT-0145 openai-tool-search 60-80.

## Rows

### N-5 and N-5/UNREAD (cache lifetime and time-based charges)
Verdict: **PARTLY**. Lifetimes are stated for Anthropic (default only), Bedrock, OpenAI; Gemini explicit-cache lifetime is not in the range read; no hourly storage statement appears in any of the nine ranges.
- [F] Anthropic: "Currently, "ephemeral" is the only supported cache type, which by default has a 5-minute lifetime." (EXT-0115, line 608). The 1-hour option and "24 hours" are not in this range.
- [F] Bedrock: "The cache has a Time To Live (TTL), which resets with each successful cache hit. ... Many models support a 5-minute TTL. Check the model card for your model to see the exact TTL conditions." (EXT-0137, lines 77-80). No price or time-based charge stated.
- [F] OpenAI, GPT-5.6 and later: "Use `prompt_cache_options.ttl` to control the minimum cache lifetime. The only supported value, `30m`, is also the default. A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." (EXT-0142, line 99). Earlier models: "`in_memory`: Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." and "`24h`: Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours." (EXT-0142, lines 105-106). Reuse "refreshes its lifetime without another cache-write charge" (line 95). Charges stated are per-token: "cache writes cost 1.25× the standard, uncached input-token rate. Subsequent reads cost 0.1× ..." (line 56); no per-hour charge appears.
- [F] Gemini, implicit caching: "We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this." (EXT-0141, lines 352-353). No lifetime or storage statement in the range.
- [F] MCP: `ttlMs` is "how long the client MAY consider the result fresh" (EXT-0143, line 43); this is client-side freshness of list/read results, not a model-token cache and has no billing statement.
- [F] Within these ranges, no sentence mentions an hourly or storage charge, for any vendor.
Does NOT show: Anthropic 1-hour/other durations, Gemini explicit-cache storage price or TTL (the explicit-caching part of r4-gemini-caching outside 340-380 was not read; the pricing page holds the hourly statement per the ledger), whether OpenAI "24h" retention carries a price.
Limits: [I] answer to "is there an hourly storage statement outside the Gemini pricing page" is "not found in these nine ranges" only; other parts of the same pages were not read. Vendor docs dated retrieval 2026-10-11.
[I] effect on ledger row: the wording "(cache lifetimes of minutes to 24 hours)" is supported for OpenAI (5 min to 24 h); the Anthropic range read supports only a 5-minute default; the Gemini storage price is not corroborated by r4-gemini-caching 340-380.

### C-S03/MINCACHE
Verdict: **PARTLY** (OpenAI, Bedrock, Gemini implicit stated; Anthropic minimum not in the ranges read). The ledger range "1,024-4,096" is contradicted at the low end by Bedrock.
- [F] Bedrock: "Minimums currently range from 512 to 4,096 tokens per cache checkpoint." (EXT-0137, lines 62-64). "The minimum applies cumulatively to the entire prompt prefix before each checkpoint, including, where applicable, content in the tools, system, and messages fields." (lines 67-69). "If you add a cache checkpoint before the total prompt prefix meets the minimum number of tokens, your inference still succeeds, but your prefix isn't cached." (lines 73-75).
- [F] Gemini implicit: "The minimum input token count for context caching is listed in the following table for each model:" with Gemini 3.8 Flash 4,096; 3.6 Flash 4,096; 3.1 Pro Preview 4,096; 2.5 Flash 2,048; 2.5 Pro 2,048 (EXT-0141, lines 353-372). The page text does not say what happens below it in that range (only implied: not cached).
- [F] OpenAI: "A prompt prefix must meet the model's minimum cacheable token length before it can be cached. Tokens in the OpenAI-provided hidden system content do not count toward this minimum. The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." (EXT-0142, line 50).
Does NOT show: Anthropic per-model minimums (not in 606-656 or 1770-1806); Gemini explicit-cache minimums; whether the Gemini/OpenAI text states a failure behaviour below the minimum (only Bedrock states "inference still succeeds, but your prefix isn't cached").
Limits: models and numbers dated 2026-10-11 retrieval; Gemini table is ragged (one cell per line in the extraction), read as model/limit pairs. [I] a Bedrock minimum of 512 is below the ledger's stated 1,024 floor.

### C-S03/EXCEPTIONS (documented cases where tool definitions, deferral or tool_choice break or restrict the cache)
Verdict: **PARTLY / ANSWERED for Anthropic; ledger wording confirmed**. Cases found, all Anthropic or OpenAI:
1. [F] Tool-definition change: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" (EXT-0115, line 644; table row "Tool definitions": tools ✘, system ✘, messages ✘).
2. [F] Hierarchy: "the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels." (EXT-0115, line 638).
3. [F] tool_choice: "Changes to `tool_choice` parameter only affect message blocks" (EXT-0115, line 648; tools ✓, system ✓, messages ✘).
4. [F] Deferred tool: "A tool with `defer_loading: true` can't also carry `cache_control`: the API returns a 400. Put the cache breakpoint on a non-deferred tool." (EXT-0131, line 769).
5. [F] Mid-conversation tool addition: "The one exception is a `tools` array with no non-deferred tool, where the first tool defined this way costs one full cache miss on that request." (EXT-0115, line 655; applies to the `inline-tools-2026-09-15` beta `tool_addition` mechanism, not to the base `defer_loading` flow).
6. [F] Placement: "Tool definitions can be cached by placing `cache_control` on the last tool in your `tools` array. All tools defined before and including that tool are cached as a single prefix." (EXT-0123, line 1772).
7. [F] OpenAI: "`additional_tools` input items do not currently accept `prompt_cache_breakpoint`." (EXT-0142, line 66). Top-level `instructions` cannot hold an explicit breakpoint (line 68).
8. [F] OpenAI tool search page, 60-80: no caching statement. The sentence there is "Namespaces can have a mix of tools that are deferred and not deferred. Tools without `defer_loading: true` are callable immediately, while deferred tools in the same namespace are loaded through tool search." (EXT-0145, line 60).
9. [F] Anthropic points to a separate page for the deferral/cache interaction: "For detailed interaction between tool definitions, `defer_loading`, and cache invalidation, see [Tool use with prompt caching]..." (EXT-0123, line 1805; and EXT-0131, line 767). That page is not read here.
10. [F] Gemini/Bedrock: Bedrock says the minimum applies "including ... content in the tools, system, and messages fields" (EXT-0137, lines 67-69); no tool-specific invalidation statement in those ranges.
Does NOT show: the claim that "a tool-search tool counts as non-deferred" appears in none of these ranges (it is stated nowhere in the nine extracts); whether withdrawing (removing) a deferred tool invalidates the cache (the page cited in item 9 is unread). The ledger's "have not been tested" is consistent: all items are documentation statements.
Limits: item 5 is a beta header mechanism; vendor claim. The tool-search regex/BM25 tool itself is not mentioned in the cache statements read.
[I] effect: the "tools array with no non-deferred tool pays one full miss" wording is confirmed verbatim (item 5) but in the context of mid-conversation tool definition, not general deferral; the "tool-search tool counts as non-deferred" half is not in these ranges.

### C-S03/DEFUSAGE
Verdict: **PARTLY** (Anthropic states it; the other pages state nothing).
- [F] "Tool search isn't metered as a separate server tool. The response's `usage.server_tool_use` object has no tool search field, and the tool definitions that search loads into context count as input tokens like any other tool definition." (EXT-0131, line 828). So loaded (searched) definitions count as input tokens; this contradicts "is not stated" for Anthropic.
- [F] Cached tool definitions: "On the first request, `cache_creation_input_tokens` reflects the token count of all tool definitions. On subsequent requests within the cache lifetime, those tokens appear under `cache_read_input_tokens` instead." (EXT-0123, line 1803).
- [F] OpenAI "Reported `cached_tokens` is calculated by subtracting the hidden system tokens from the last matched breakpoint, then rounding down to the nearest multiple of 128." (EXT-0142, line 82; earlier models only).
Does NOT show: whether deferred-but-not-loaded definitions are counted in any usage field (the passage speaks of definitions "that search loads into context"; unloaded ones are not addressed); whether OpenAI or Gemini usage counts deferred/tool-search-loaded definitions (nothing in EXT-0145 or EXT-0141); what is billed for "withdrawn" definitions.
Limits: vendor claim; Anthropic only.
[I] effect: the ledger wording "not stated" is partly contradicted for Anthropic (loaded definitions count as input tokens); remains unstated for unloaded deferred definitions and for OpenAI/Gemini within these ranges.

### N-26 (mechanisms documented and who controls them)
Verdict: **ANSWERED** for the ranges read.
- Anthropic: automatic and explicit: "Each of these elements can be cached, either automatically or by marking them with `cache_control`." (EXT-0115, line 620); caller sets `cache_control` (type "ephemeral") including on the last tool (EXT-0123, line 1772); cache type: only "ephemeral", default 5-minute lifetime (EXT-0115, line 608). Deferred tools cannot carry `cache_control` (EXT-0131, line 769).
- Bedrock: explicit checkpoints placed by the caller: "Cache checkpoints are markers that define the contiguous subsection of your prompt that you want to cache." (EXT-0137, lines 57-58); TTL is model-dependent, resets on hit (lines 77-80); "It doesn't guarantee that an eligible request results in a cache hit." (lines 82-84).
- Gemini: implicit, on by default: "Implicit caching is enabled by default for all Gemini 2.5 and newer models." (EXT-0141, line 349); "There is nothing you need to do in order to enable this." Explicit caching exists but the Interactions API does not support it (EXT-0141, lines 342-345: "The Interactions API only supports implicit caching."). Caller-controllable levers stated: ordering and timing only ("Try putting large and common contents at the beginning of your prompt").
- OpenAI GPT-5.6+: explicit and implicit modes selected with `prompt_cache_options.mode`; explicit breakpoints via `prompt_cache_breakpoint`, up to four cache writes per request; TTL via `prompt_cache_options.ttl` (only `30m`) (EXT-0142, lines 60-66, 99). Earlier models: "Only implicit caching is supported." Retention via `prompt_cache_retention` (`in_memory`, `24h`); default depends on Zero Data Retention (EXT-0142, lines 78, 105-113).
- MCP: server-set `ttlMs` and `cacheScope` hints for the client's cache; the client MAY/SHOULD obey; not a model-token cache (EXT-0143, lines 43-44, 171).
Does NOT show: Anthropic 1-hour retention option and automatic caching mode details (other parts of that page); Gemini explicit-cache parameters.
Limits: GPT-5.6-and-later vs earlier-model split is vendor-stated; ragged Gemini table.

### C-E02/E22 (programmatic tool calling and MCP caching pages)
Verdict: **PARTLY** (two pages read in the given ranges only).
Programmatic tool calling (EXT-0144, source lines 30-60):
- [F] "This reduces latency for multi-tool workflows and decreases token consumption by allowing Claude to filter or process data before it reaches the model's context window." (line 35). Vendor-reported figure: "adding programmatic tool calling on top of basic search tools improved performance by an average of 11% while using 24% fewer input tokens" (line 35; on BrowseComp and DeepSearchQA, web-search tools).
- [F] "Adding `allowed_callers: ["code_execution_20260120"]` to a tool definition is what makes that tool callable from within code execution" (line 45); requires the code execution tool version `code_execution_20260120` or later (line 41); Claude Haiku 4.5 "doesn't support programmatic tool calling" (line 32).
- Does NOT show: whether tool definitions with `allowed_callers` count in tokens differently, or any caching statement (none in these lines).
MCP caching spec page (EXT-0143, whole page, source lines 1-177):
- [F] "Servers MUST include caching hints on results with `resultType: "complete"` returned by" `server/discover`, `tools/list`, `prompts/list`, `resources/list`, `resources/templates/list`, `resources/read` (lines 13-21). So tool lists (`tools/list`) are covered.
- [F] Cache key is method plus parameters that affect the result (for example `cursor` for paginated lists) (lines 29-32); each page is separately cacheable with its own `ttlMs` (lines 151-154).
- [F] `cacheScope` is `"public"` or `"private"`; `"public"` "is appropriate for lists of tools, prompts, and resource templates when they are identical for all users"; `"private"` for "filtered list results that vary per user" (lines 103-106). A `tools/list_changed` notification "invalidates the cached response" (lines 118-119).
- [F] Security: "MUST apply appropriate per-primitive access controls, and MUST NOT rely on `cacheScope` alone to prevent unauthorized access to primitives." (line 177).
- Does NOT show: any statement about model token caching, provider prompt cache, or token counts of tool definitions; cache behaviour when a policy restricts which tools are listed per request (only "filtered list results that vary per user" are labelled private); no numeric defaults for `ttlMs` (absent = 0).
Limits: MCP spec page for version 2026-07-28; it concerns client caching of protocol results, not provider KV caches. [I] the two caches are separate layers on the evidence read; the page does not relate them.

## Not read / not run
- Remaining parts of r4-anthropic-prompt-caching (minimum tokens, 1-hour option, pricing), r4-gemini-caching outside 340-380 (explicit caching), r4-bedrock-prompt-caching outside 55-85, r4-openai-prompt-caching outside 48-116 (summary of model differences), r4-anthropic-tool-search outside 760-840, and the Anthropic "Tool use with prompt caching" page (referenced, not stored in the ranges read) were not read in this batch.
- No commands failed.

## Contradictions with current ledger wording (plain)
1. C-S03/MINCACHE: Bedrock states minimums "from 512 to 4,096", not 1,024-4,096 (EXT-0137).
2. C-S03/DEFUSAGE: Anthropic states tool definitions loaded by tool search "count as input tokens like any other tool definition" (EXT-0131), so "not stated" is not correct for Anthropic loaded definitions.
3. C-S03/EXCEPTIONS: the "tool-search tool counts as non-deferred" half of the wording is not present in these nine ranges; the "no non-deferred tool pays one full miss" half is present but attached to the beta mid-conversation tool-addition mechanism (EXT-0115 line 655).
4. N-5: no hourly storage statement appears in any of the nine ranges; Anthropic's range shows only a 5-minute default.
