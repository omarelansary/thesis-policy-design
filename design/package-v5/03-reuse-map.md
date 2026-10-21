# 03. Reuse map: established components per policy slot (V5, AUTH-020)

Status: provisional, written by the lead 2026-10-22; checked by three stewards in thread T-20261022-115 (results in `findings/SUM-0042..0044`, reconciled in section 11). Nothing here is validated, approved or final. The principle applied is the human's (REQ-U21-03): what research, large companies or widely used open-source projects have already built and tested is reused, not re-invented or re-tested; only the remainder goes to the proof-of-concept loop (`05`).

**How to read a row.** "L/" = `evidence/literature-20261019/`, stored with URL, date and hashes in `MANIFEST.jsonl` (fetched 2026-10-22 under AUTH-020 unless older). Labels: [F] the stored source says it (a vendor statement of its own mechanism or price counts as established; a vendor performance number does not); [O] observed by the lead in the stored text; [I] interpretation; [U] unknown. A row marked *scout-reported* comes from a scout's discovery report and has not been re-read at the source by anyone yet; it is a lead, not evidence. Star counts are from the GitHub API on the retrieval date and say nothing about quality. "Not found" means not found in the places listed in `inputs/search-log-20261022.md`.

**Verdict vocabulary.** REUSE = established mechanism, adopt as is; REUSE+CHANGE = adopt with a stated change; OURS = the effect in our combination is untested anywhere we looked, so it goes to `05`; NONE FOUND = nothing established in the places searched.

## 1. Slot 1: cached full exposure (all definitions in a stable cached prefix)

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Provider prompt caching (Anthropic, OpenAI) | Prefix order tools, system, messages; a change at one level invalidates it and everything after; changing `tool_choice` invalidates only the messages cache [F] | L/v5-anthropic-tool-use-caching-20261022.md:57-63 | REUSE |
| Prices and lifetimes | Write 1.25x (5 min) or 2x (1 h), read 0.1x / 0.05x / 0.025x by model; OpenAI 5.6+ write 1.25x, read 0.1x, 30 min [F] | FND-0039 (`findings/SUM-0041`), DPR-0006 section 2 | REUSE (inside DPR-0006) |
| Minimum cacheable length | 512 to 4,096 tokens by model; a prefix below it is not cached [F] | FND-0037 Q8 (EXT-0150, EXT-0142) | REUSE as a design constraint |
| Measured caching in a multi-turn agent | Caching cut API cost 41-80% across providers on one benchmark (DeepResearch Bench, 40 sessions per condition, 10,000-token system prompt); caching only the system prompt or excluding tool results beat full-context caching [F, one study] | L/v5-dontbreakcache-2601.06007v2.txt:33, :108, :304-306, :422 | REUSE as prior result; it does not vary the tool catalogue |
| Tool-set change breaks the cache | "any change to the available tool set invalidates the cached prefix" [F] | L/v5-dontbreakcache-2601.06007v2.txt:525-527; L/v5-anthropic-tool-use-caching-20261022.md:57-63 | REUSE as a constraint |
| Measured tool-block caching | One practitioner: caching the last tool cut the carried tool-block cost about 90% on Claude; a 2-tool block (about 655 tokens) fell below the minimum and could not cache; one added tool re-wrote a 4,082-token block; Gemini implicit cache gave zero hits in three probes [F as a self-reported measurement, small n, vendor-adjacent] | L/v5-synthorai-mcp-overhead-20261022.txt:174, :176 | REUSE as a magnitude check, not as a result |
| Cost of mid-session tool-list changes in production | One issue with community data: two rewrites of 857,710 and 782,873 tokens a minute apart; 506 local session logs with 2,766 cache-bust events, 224.4M re-billed input tokens, 13.5% of spend, in 38% of sessions [F as a user report, not controlled] | L/v5-ccissue-92033-cachebust-20261022.txt:64, :89, :180-190 | REUSE as the failure mode to design against |
| Cache diagnostics | Anthropic reports where a prefix diverged (`tools_changed`, `system_changed`, `messages_changed` and others) per request *scout-reported*; the stored page is L/v5-anthropic-cache-diagnostics-20261022.md | stored, not yet re-read | REUSE as the measurement instrument for `05` |
| Keep-alive or 1 h lifetime for returning users | Provider prices fix the arithmetic (DPR-0006 section 3, gap cost). Open-source keep-alive schedulers exist (OpenClaw docs) *scout-reported* | DPR-0006; scout report group 1 | REUSE the arithmetic; the gap distribution of our sessions is OURS |

## 2. Slot 2: restriction or offering without changing the cached definitions

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| OpenAI `allowed_tools`, `tool_choice: none` | The vendor's guidance: restrict callable tools with `allowed_tools` "while keeping the supplied `tools` list stable"; disable tools with `tool_choice: none` instead of removing definitions [F] | L/v5-openai-prompt-caching-20261022.md:440-441 | REUSE (OpenAI) |
| Anthropic mid-conversation tool changes (`tool_addition`, `tool_removal`) | Declare the full tool set in `tools` once, then offer or withdraw tools per turn with system-message blocks; "The `tools` array itself never changes, so the cached prefix stays intact"; a tool can also be defined by value mid-conversation and "the prompt cache still hits", except when `tools` holds no non-deferred tool [F] | L/v5-anthropic-midconv-sysmsg-20261022.md:27, :31, :452 | REUSE+CHANGE: beta (`inline-tools-2026-09-15`); by-reference changes also on Bedrock and Google Cloud, by-value on the Claude API only (:20); listed models only (:18) |
| Anthropic `tool_choice` | Changing it invalidates the messages cache, not tools or system [F] | L/v5-anthropic-tool-use-caching-20261022.md:63, :70 | REUSE as a constraint (not a cache-free restriction) |
| Logit masking (Manus) | Mask instead of removing tools, to keep the cache; needs decode-time control [F as a practitioner account, no data] | L/v5-manus-context-eng-20261022.txt (stored, not yet re-read at line level) | Not available on hosted APIs; recorded, not adopted |

[I] This slot changes the design question. With per-turn offering at a fixed prefix available from two providers, a staged policy no longer has to choose between "small prefix" and "warm cache" on those providers: definitions can sit cached in `tools` while the stage decides what is *offered*. What it saves then is not the tool-block read (still paid at the read price on every request) but wrong-tool risk and, where tools are deferred, the definitions themselves. Whether offering fewer tools raises accuracy at a fixed prefix is OURS.

## 3. Slot 3: deferred loading and tool search

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Anthropic tool search with `defer_loading` | Deferred tools are not in the prefix; a discovered definition is appended inline as `tool_reference`; "The prefix is untouched, so prompt caching is preserved" [F] | L/v5-anthropic-tool-use-caching-20261022.md:49 | REUSE |
| Anthropic tool search limits and billing | Up to 10,000 deferred tools; search not metered separately; loaded definitions count as input; at least one non-deferred tool; `defer_loading` with `cache_control` on one tool returns 400 [F] (earlier extracts) | FND-0037 Q1, EXT-0131; stored current page L/v5-anthropic-tool-search-20261022.md, not yet re-read for changes | REUSE; steward re-check of the current page |
| Anthropic tool search performance | 49% to 74% (Opus 4) and 79.5% to 88.1% (Opus 4.5), "internal testing", no method [vendor performance claim, not established] | L/v5-anthropic-advanced-tool-use-20261022.txt (stored, line not yet cited) | Not established |
| OpenAI tool search | Discovered tools "are injected at the end of the context window" to preserve the cache; only gpt-5.4 and later; an individually deferred function still shows its name and description, so namespaces or MCP servers save more; keep namespaces under 10 functions; changing the loaded tool set "will break the model's cache from that point forward"; mixing eager and deferred functions "generally not recommended" [F] | L/v5-openai-tool-search-20261022.md:5, :7, :22, :24, :860, :1134 | REUSE (OpenAI) with its own constraints |
| Claude Code MCP tool search | A production client that defers MCP tools by default with thresholds and per-server always-load *scout-reported*; threshold bugs reported in mirrored issues *scout-reported* | L/v5-claudecode-mcp-20261022.md (stored, not yet re-read) | REUSE as a reference client |
| Open-source retrievers (langgraph-bigtool, Spring AI advisor, LlamaIndex) | Client-side retrieval of tools; no cost or cache evidence of their own; Spring AI's own test is one task, 28 tools, manual runs, "preliminary" *scout-reported* | L/gh-api-langgraph-bigtool-20261022.dat (557 stars, MIT); others scout-reported | REUSE as implementations only |
| Research on model-requested retrieval (MCP-Zero, RAG-MCP, ScaleMCP) | Prompt-token reductions of about 50-98% with mixed accuracy effects; counted prompt tokens, not a bill with caching *scout-reported*; stored texts L/pdf-mcpzero-*, L/v5-ragmcp-2505.03275v1.txt, L/v5-scalemcp-2505.06416.txt | stored, not yet re-read | Prior results on tokens, not on the bill |
| First-stage retrieval quality (ToolRet) | Best nDCG@10 about 35 without instructions, about 47.5 with *scout-reported*; stored L/pdf-toolret-2503.01763v2.txt | stored earlier, not re-read here | REUSE as the reason not to rely on one embedding step |
| Small catalogues | A vendor's preliminary test: at 40 tools a simple task cost $0.072 progressive against $0.045 static, a complex one $0.051 against $0.146; static at 200 and 400 tools exceeded the 200k window [F as a vendor's "preliminary" test] | L/v5-speakeasy-dynamic-toolsets-20261022.txt:67, :75-77, :92 | REUSE as a magnitude check |

## 4. Slot 4: staged narrowing, hierarchies and gateways

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Executor (the supervisor's named baseline) | An open-source integration layer: one catalogue of MCP, OpenAPI and GraphQL integrations shared by any MCP agent, per-tool policy (allowed, approval, blocked), and tool search by intent [F]; repository now `UsefulSoftwareCo/executor`, 4,235 stars, MIT, pushed 2026-10-21 [O]. How it exposes tools to the model (one code-executing tool with in-sandbox discovery) is *scout-reported* from a third-party docs mirror | L/v5-executor-readme-20261022.md:5-7, :28-32, :123; L/v5-gh-api-executor-20261022.dat | REUSE as the required baseline (REQ-O02-06); the MCP surface it presents must be read from its own docs before the arm is defined |
| GitHub MCP server dynamic toolsets, Docker MCP gateway (`mcp-find`, `mcp-add`) | Model-navigated groups: list groups, enable one; server-level staging; both beta or experimental [F for Docker's docs page, *scout-reported* for GitHub] | L/v5-docker-dynamic-mcp-20261022.txt (stored); L/v5-gh-api-docker-mcp-gateway-20261022.dat; L/v5-gh-api-github-mcp-server-20261022.dat | REUSE as implementations; enabling a group changes the tool list, so on Anthropic it must go through slot 2 to keep the cache |
| Invoker or role filter (supervisor's stage one, REQ-O14F-04) | Static per-deployment allow-lists are standard practice (Copilot's usage-based core, LangChain's CORE_TOOLS) per the blind instances, from stored sources | `inputs/blind-output-A-20261022.md` P1 (r4-github-copilot-fewer-tools, lit-langchain-progressive-disclosure.txt:37-38), not re-read by the lead | REUSE as a mechanism; its value in our setting is OURS |
| Multi-step semantic narrowing (1,000 to 10 in several steps, REQ-O14F-05) | NONE FOUND as a measured multi-stage policy; one two-stage router in an earlier benchmark scored within noise of single-stage retrieval (V4 `01` section 4) | V4 `01` section 4 row "Not found"; scout group 2 queries | NONE FOUND; each extra stage adds a request and, without slot 2, a cache break |
| AWS AgentCore semantic tool search | A hosted search endpoint over gateway tools *scout-reported* | scout report group 2 | Recorded; AWS-only |

## 5. Slot 5: memory that informs which tools are offered

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Within-session tool memory (MemTool) | Agents add and remove tools across 100 consecutive turns; reasoning models removed unneeded tools 90-94% of the time, medium models 0-60% *scout-reported*, consistent with the earlier steward reading in `findings/SUM-0005` | L/v5-memtool-2507.21428.txt (stored, not yet re-read); SUM-0005 | REUSE as prior result; removal mid-session breaks the cache unless done through slot 2 [I] |
| Tool-experience memory (ToolMem, MemToolAgent, ReMe) | Memory of how tools performed, used to pick among tools; gains reported relative, no token or cost figures *scout-reported* | L/v5-toolmem-2510.06664.txt, L/arxiv-2606.07909.txt (stored, not yet re-read) | Prior results on accuracy only |
| Selective persistent memory across sessions | One deployment keeping four categories (including tool configurations) completed 12/12 at 3.9K input tokens against 8/12 at 7.7K for full history; small N | L/arxiv-2607.09493.txt:28-61 per both blind instances, not re-read by the lead | Prior result, small N |
| Memory frameworks and tool parameters | Seven memory frameworks inadequate at grounding tool parameters (Mem2ActBench) per blind B | L/arxiv-2601.19935.txt:41-45 per blind B | REUSE as a known failure |
| Anthropic memory tool | Client-side `/memories` directory, read at the start of a task and in later conversations; a documented multi-session pattern [F] | L/v5-anthropic-memory-tool-20261022.md:29, :983 | REUSE as the memory carrier option |
| Memory that chooses or pre-loads tool definitions across sessions, with a bill measured | NONE FOUND (scout group 3 queries; blind instances A and B; V4 `04` section 4) | search log | NONE FOUND: the core of REQ-U21-04 is OURS |

## 6. Slot 6: tool results and history kept out of the context

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Observation masking (JetBrains and TUM) | Replacing old tool observations by a placeholder (window of 10 turns) more than halved cost against the raw agent and matched LLM summarisation on solve rate; a hybrid saved a further 7% and 11% [F, one study, coding agents]. Cost was API-reported for Gemini; for Qwen it was priced post hoc without a cache-hit distinction, which inflates those costs [F] | L/v5-complexitytrap-2508.21433.txt:24, :96-100, :325, :820-827 | REUSE as the simple default for long single runs; its interaction with prompt caching is not reported in the passages read [U] |
| Anthropic context editing (clearing tool results) | Clearing "Invalidates cached prompt prefixes"; "clear enough tokens to make the cache invalidation worthwhile"; `clear_at_least` exists for that; each clear incurs a cache write [F] | L/v5-anthropic-context-editing-20261022.md:71 | REUSE with the documented trade-off; the break-even is DPR-0006 arithmetic |
| OpenAI compaction | Server-side compaction returning an opaque item *scout-reported*; stored L/v5-openai-compaction-20261022.md | stored, not yet re-read | REUSE as an option on OpenAI |
| Programmatic tool calling and code mode | Results of programmatic calls are not added to the context; vendor's own results: -38% billed input on one benchmark, about +8% cost on tau2-bench [F, EXT-0183 via FND-0038] | FND-0038 row N-29; L/v5-anthropic-ptc-20261022.md, L/v5-cloudflare-codemode-mcp-20261022.txt (stored) | REUSE as a conditional option; the supervisor's "80%" (REQ-O21-05) is an illustration (REQ-U21-12) |
| Files plus search instead of context | Cursor writes long outputs and tool descriptions to files; -46.9% total agent tokens in runs that called an MCP tool, no sample size [vendor claim] *scout-reported* | L/v5-cursor-dynamic-context-20261022.txt (stored) | Recorded as a vendor claim |
| Share of cost in tool outputs versus the fixed base | In one coding-agent study the harness base (system prompt and tool definitions) was 74.7% of billed cost and tool outputs 3.3%; compressing outputs cut tokens 38.4% and raised cost 6.8% [F per both blind instances and FND-0038 for the 6.8%] | L/pdf-tokennotcost-2607.12161v5.txt:200-222 per blind A and B; EXT-0016 | REUSE as a warning: in coding agents the tool block, not the results, dominates |

## 7. Slot 7: discovery control and recovery

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Recovery channel | The tool-search call itself is the documented recovery path; a search with no match returns an empty list *scout-reported* from the current Anthropic page | L/v5-anthropic-tool-search-20261022.md (stored, not yet re-read) | REUSE |
| Held-back-then-released benchmark | BFCL `multi_turn_miss_func`: needed functions withheld, then supplied in a later turn *scout-reported*; stored L/v5-bfcl-test-categories-20261022.md | stored, not yet re-read | REUSE as an evaluation vehicle for recovery |
| Abstention and stopping | AgentAbstain (stored earlier as L/arxiv-2607.10059.txt) and CONVOLVE (L/v5-convolve-2606.28733.txt): models abstain poorly; CONVOLVE learns stopping rules from earlier trajectories *scout-reported* | stored, not yet re-read | Prior results |
| A cap on discovery calls or a stop-after-N-failures rule | NONE FOUND as a recommended value; BFCL force-terminates after 20 steps per turn *scout-reported* | scout group 4 | NONE FOUND; a cap stays a symbol, never a value |
| Uninstructed search initiation | NONE FOUND (FND-0037 row C-S08/UNINSTR) | FND-0037 | OURS |

## 8. Slot 8: security and robustness

| Component | What it establishes | Source | Verdict |
|---|---|---|---|
| Ranker and selection attacks (ToolHijacker) | One injected tool document can win retrieval and selection; defences tested were insufficient [prior record; numbers not re-read here] | origin `s3-shi-toolhijacker-2504-19793-20261012` (steward probe found the id) | REUSE as a risk of any retrieve-then-select stage |
| Tool-metadata poisoning (MCPTox) | 45 servers, 353 tools, 20 agents; attack success up to 72.8% *scout-reported* | not stored | Recorded only |
| `tools/list` caching and `list_changed` | MCP SEP-2549 adds `ttlMs` and `cacheScope` to list results; it is client-side (latency, gateway load), not provider tokens *scout-reported* | L/v5-mcp-sep2549-20261022.txt (stored, not yet re-read) | REUSE as a client-side detail; a tool-list change reaching the provider prefix is the slot-1 failure |

## 9. Slot 9: evaluation vehicles (reuse instead of building)

| Vehicle | Fit | Source | Verdict |
|---|---|---|---|
| tau2-bench | Multi-turn with a user simulator; records `agent_cost` and `user_cost` floats; any LiteLLM provider *scout-reported*; small tool sets; no sessions | L/v5-tau2-simulation-py-20261022.py:1117-1120, :50; L/v5-gh-api-tau2-20261022.dat | Candidate for the PoC loop (cost recorded; cache fields to verify) |
| BFCL (multi-turn, missing function, memory categories) | OpenAI-compatible endpoint supported; score only, no bill *scout-reported* | L/v5-bfcl-test-categories-20261022.md; L/v5-gh-api-gorilla-20261022.dat | Candidate for recovery and memory checks; the bill must come from provider usage records |
| MCPMark | 127 tasks, 5 servers, a built-in compaction option *scout-reported* | L/v5-mcpmark-readme-20261022.md; L/v5-mcpmark-2509.24002.txt | Candidate for long single runs |
| MCPVerse, LiveMCPBench, TheMCPCompany, MCP-Universe | Large catalogues (218-18,505 tools); no sessions; token or cost recording partial *scout-reported* | API metadata stored for each (L/v5-gh-api-*.dat) | Candidates for the catalogue-size axis |
| A vehicle with sessions, a gap, a large catalogue and cache fields | NONE FOUND (scout group 4) | search log | NONE FOUND: the session axis needs our own thin harness over provider usage records (REQ-O21-09: plain Markdown memory first) |

## 10. What the map leaves for the proof-of-concept loop (feeds `05`)
1. **Offering at a fixed prefix** (slot 2): does offering fewer tools per turn, through `tool_addition`/`tool_removal` or `allowed_tools`, keep accuracy nearly the same while the bill stays at the cached-prefix level? The mechanism is the vendors'; the effect in our setting is OURS.
2. **Memory-informed offering across sessions** (slot 5): NONE FOUND; the combined decision REQ-U21-04 rests here.
3. **Uninstructed recovery** (slot 7): OURS.
4. **Session-gap economics** for returning users (slot 1): the arithmetic is DPR-0006; the gap distribution and the share of cold starts of our sessions are OURS.
5. **Whether the university API exposes cache fields at all** (REQ-U21-01): a one-request check, not an experiment (both blind instances flag it).
Everything else in sections 1-9 is reused as stated, with its source's limits.

## 11. Steward check (T-20261022-115) — corrections received, NOT YET APPLIED to the rows above
All three batches are in: A (`findings/SUM-0042`, FND-0040, sections 1, 2, 6), B (`findings/SUM-0043`, FND-0041), C (`findings/SUM-0044`, FND-0042). Corrections to apply on resume:
- s1 caching study: "system prompt only / exclude tool results beat full context" is about time to first token; on cost the three strategies are within 2-4 points (L/v5-dontbreakcache-2601.06007v2.txt:414-423).
- s1 issue 92033: 38% is the share of sessions with tool-list mutations (191 of 506), not of cache-bust events (:186-188). synthorai: the 90% is on Opus 4.8, the 4,082-token rewrite on Opus 5; drop "vendor-adjacent" (not in the lines read).
- s6 cost share: 74.7% is at L/pdf-tokennotcost-2607.12161v5.txt:243, :298 and covers system prompt plus tool definitions together, so "the tool block dominates" is NOT supported (also fix `01` C7 pointer); the 38.4% is of tool-output tokens only (about 1.3% of cost).
- s6 masking: the paper does discuss KV-cache and cache-hit pricing (L/v5-complexitytrap-2508.21433.txt:317, :531-533, :603, :826-827, :1178); replace the [U].
- s2 mid-conversation changes: add the `mid-conversation-tool-changes-2026-07-01` header (by reference, Bedrock and Google Cloud) and `mcp-client-2026-09-15`; the "never changes" quote is :27 (:31 is about `defer_loading`); Manus "not available on hosted APIs" is the lead's inference; the s1 "(Anthropic, OpenAI)" prefix claim is cited to Anthropic only.
- s6 OpenAI compaction: add that compaction can prevent reuse from the first changed token (L/v5-openai-prompt-caching-20261022.md:59).
- Not verified by steward A: OpenClaw keep-alive (no stored text), price pages (FND-0039 quotes relied on).
- s3 ToolRet: best nDCG@10 without instructions is 33.83 (L/pdf-toolret-2503.01763v2.txt:139-142, :1489), not "about 35"; no "47.5 with instructions" figure found.
- s4 multi-step narrowing: V4 `01`:77 says the two-stage router scored 0.7-4.0 points below rag:32 on every model; keep the direction. Check that this benchmark is not the student's earlier retrieval work (contamination rule) before keeping the sentence.
- Not in any stored text (keep as scout-reported or drop): GitHub MCP dynamic toolsets, AWS AgentCore, MCPTox, Spring AI 28-tool test, LlamaIndex, Claude Code threshold bugs, Executor's MCP surface, Copilot 40-to-13.
- Confirmed: tool-search limits and billing (L/v5-anthropic-tool-search-20261022.md:73, :790, :821, :849); vendor 49/74 and 79.5/88.1 at L/v5-anthropic-advanced-tool-use-20261022.txt:60 (claim); Executor, bigtool, Speakeasy (Sonnet 4, a handful of runs), ToolHijacker, SEP-2549 fields. OpenAI's "fewer than 10 functions" is a best practice. Docker's units are MCP servers; experimental. "Mixed accuracy" for MCP-Zero and RAG-MCP is not in their abstracts; ScaleMCP numbers not located; SEP-2549 "not provider tokens" is the lead's reading.
- s5: MemToolAgent has a cost analysis and token table (L/arxiv-2606.07909.txt:515-516, :765-799); "ReMe" is not stored (only "ReMem", :176); 2607.09493 lines are 20-36, it is a controlled replication plus a platform, selective versus full memory not significant (p = 0.125), and its "tool configurations" are specification context, not tool offering. MemTool 90-94% / 0-60% is a removal ratio, not accuracy.
- s7: the "recovery path" is the lead's reading; the page documents the empty result (:658). BFCL withheld-then-supplied and the 20-step stop are in L/web-bfcl-v3-multi-turn-blog.txt:235-238, :690-691, not in the test-categories file (:41).
- s9: tau2 `:50` is an import line; "any LiteLLM provider" not stored; `agent_usage` populated only for audio-native runs, so cache fields in text runs are unknown; BFCL "OpenAI-compatible" not found in the cited files; 18,505 at L/arxiv-2510.19286.txt:374; 218 not found in the MCPVerse text.
- NONE FOUND rows: nothing in the files read contradicts them; the check ran no new searches.
