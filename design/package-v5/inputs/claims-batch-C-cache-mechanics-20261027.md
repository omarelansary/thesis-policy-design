# Batch C claims to check: serving-system cache literature against the probe observations (thread T-20261027-119; leads from scout 3, not evidence)

Stored files are in `evidence/literature-20261019/`. The probe observations are in `design/package-v5/10-p0-university-api-reading.md` sections 2, 7 and 9 (they are measurements by the human, not literature).

| # | Claim (scout 3) | Stored file |
|---|---|---|
| C1 | PagedAttention/vLLM: "vLLM sets its default block size as 16" (section 7.2); all-or-nothing eviction (section 4.5); prefix sharing for predefined prefixes (section 4.4) | v5-lit-pagedattention-2309.06180.txt |
| C2 | vLLM automatic prefix caching: each block is hashed by its tokens and the tokens of the prefix before it; "We only cache full blocks."; LRU eviction; `cache_salt` isolates tenants | v5-lit-vllm-prefix-caching-design-20261027.txt |
| C3 | vLLM hybrid KV cache manager: cached prefix is the intersection of the groups; sliding-window layers need only the last window-1 tokens; one LRU queue; for Mamba hybrids block size is raised to match state size | v5-lit-vllm-hybrid-kv-20261027.txt |
| C4 | gpt-oss model card section 2.2: attention blocks alternate between banded window and fully dense patterns, bandwidth 128 tokens; 64 query heads, 8 KV heads | v5-lit-gptoss-modelcard-2508.10925.txt |
| C5 | OpenAI Harmony format: functions are defined "in the developer message in a dedicated `Tools` section"; order system, developer, user; the developer message starts with `# Instructions` then `# Tools` | v5-lit-openai-harmony-20261027.txt |
| C6 | SGLang RadixAttention: radix tree over token sequences, "the size of each page is equivalent to one token", LRU eviction of leaves, cache-aware scheduling | v5-lit-sglang-radixattention-2312.07104.txt |
| C7 | SGLang server arguments: `--page-size` "The number of tokens in a page" default 1; `radix_eviction_policy` lru or lfu; `enable_cache_report` returns the number of cached tokens in `usage.prompt_tokens_details`, default False | v5-lit-sglang-server-args-20261027.txt |
| C8 | LMCache: "a default size of 256 tokens per chunk"; tiers CPU memory, local disk, remote disk, Redis; hit ratios 85% falling to 45% under truncation; no TTL stated | v5-lit-lmcache-2510.09665.txt |
| C9 | CacheBlend: reuses cached chunks "regardless of position" and recomputes a small subset of tokens | v5-lit-cacheblend-2405.16444.txt |
| C10 | Mooncake: block hashes with block size 512, each key combining its tokens with the previous block's key; LRU best on its traces; scheduler assigns a request by prefix match and queue time; hot-block replication | v5-lit-mooncake-2407.00079.txt |
| C11 | "A Year in LLM Serving" (arXiv 2608.13573): most requests see little or nearly full prefix reuse; 99% of reuse arrives within 15 minutes of the previous request; simple eviction is competitive; each instance manages its own KV cache; cache-blind routing scatters turns across replicas | v5-lit-yearinllmserving-2608.13573.txt |
| C12 | CacheRoute (arXiv 2608.19677): served KV-cache hit rate rises from about 64% to about 93% with cache-aware routing; cache-blind balancing scatters reuse | v5-lit-cacheroute-2608.19677.txt |
| C13 | OpenAI prompt caching: `cached_tokens` counts billed reads and excludes tokens charged as writes; earlier models round down to a multiple of 128; minimum 1,024 tokens; in-memory entries last about 5 to 10 minutes up to one hour; "Keys influence routing; they do not pin requests to a machine"; traffic above 15 requests per minute can overflow | v5-openai-prompt-caching-20261022.md |
| C14 | DeepSeek KV cache guide: "best-effort", no guaranteed hit rate; cleared "usually within a few hours to a few days"; matches only the prefix of the input; fields `prompt_cache_hit_tokens` and `prompt_cache_miss_tokens` | v5-lit-deepseek-kvcache-20261027.txt |

## Then, for each of the five probe facts below, say which stored sources predict it, which do not, and what is not predicted by any
1. Cached-token counts are always multiples of a block: 16 tokens on gpt-oss-120b, 64 on GLM-5.3, 128 on MiniMax-M3.
2. On GLM-5.3 and MiniMax-M3 a change invalidates the cache from the change onward (plain prefix cache); the tools sit first on GLM-5.3 and the system text first on MiniMax-M3.
3. On gpt-oss-120b the cached length after nonce-marked edits was not monotonic in the edit position: first tool edited 64, tool_10 edited 3,248, tool_20 edited 3,808, a tool added at the end 64, a marker at the start or end of the system prompt 64, base repeated 4,464.
4. A prefix sent about 75 minutes earlier was still cached on three models; about 5 hours earlier it was gone on gpt-oss-120b and MiniMax-M3 and still present after about 5.5 hours on GLM-5.3.
5. Whether replicas, routing or eviction could produce non-repeatable hit lengths.
