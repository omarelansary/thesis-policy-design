---
id: "FND-0032"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-20
thread: T-20261020-108
evidence: ["EXT-0004"]
---

# Batch 13: what the agent-memory survey says about the supervisor's memory point (ledger C-E02/UNREADLEADS)

Source (workspace literature copy, not an origin source; cited as `file:line`):
`evidence/literature-20261019/pdf-memory-survey-2602.06052.txt` (below: **S:line**), arXiv 2602.06052, "A Survey of Agent Memory in the Second Half", TMLR 07/2026.
The survey is a secondary source: it describes other papers; no experiment of its own was found in the ranges read. No extract EXT was created (the tool cannot extract it). All quotes are verbatim from the file; labels: [F] fact in source, [O] my observation, [I] interpretation, [U] unknown. Wording rule: the supervisor's statements are proposals that evidence supports, sharpens or narrows.

Ranges read in full: S:340-559, 1015-1114, 1120-1149, 1280-1520, 1556-1645, 1678-1777, 2340-2500, 3005-3064, 3370-3430, 3624-3710, 3800-4000. Located by search only (not read around): S:610-670, 770-840, 976-1012, 1157, 2032, 2174-2182, 2530-2620, 2829-2893, 3482-3500, 4072-4075, 4178, 4276, 4391-4392, 4570, 4645, 4768-4773. Not read: S:560-610, 670-770, 840-1015 (except hits), 1150-1280 (except 1280-1300), 1520-1556, 1645-1678, 1777-2340 (except hits), 2500-3005, 3065-3370, 3430-3624, 3710-3800, 4000-5740 (reference list; searched only).

## Summary table

| # | Question | Verdict |
|---|---|---|
| 1 | Taxonomy of memory kinds and scopes | ANSWERED |
| 2 | Tool-related memory | PARTLY |
| 3 | Cross-session memory, horizon, benchmarks | PARTLY |
| 4 | Cost of memory | PARTLY |
| 5 | Prefix or cache interplay | NOT FOUND IN THIS TEXT (only KV cache as an internal memory substrate) |
| 6 | Deployed-agent scenarios | PARTLY |
| 7 | Anticipation before the first request | NOT FOUND IN THIS TEXT |

## Q1 Taxonomy

The survey uses three orthogonal axes (S:494-500, figure caption): substrate (internal/parametric vs external), cognitive mechanism (sensory, working, episodic, semantic, procedural), subject (user-centric vs agent-centric). Short-term vs long-term is also drawn (S:425-437).

| Kind | Survey's own definition (verbatim, file:line) | Limits | Bearing |
|---|---|---|---|
| Internal/parametric substrate | "Model weight,latent-state,and KV cache are adjusted." (S:372); "Memory stored in model weight,state,or KV cache" (S:394) | caption text of a figure | [F] KV cache is classed as memory substrate, not as a serving optimisation |
| External substrate | "Memory stored in vector store,structural store,text-record, or hierarchical store" (S:399) | | [F] |
| Sensory | "the temporary retention of incoming perceptual signals" (S:1138); "typically not explicitly modeled" in text agents (S:1141) | | [O] not relevant to text tool agents |
| Working | "a short-term memory mechanism that supports the temporary storage and active manipulation of information necessary for complex tasks" (S:1317-1319); "most commonly instantiated through the active context, which includes the prompt context, intermediate reasoning traces, tool outputs, and runtime states such as key-value caches" (S:1328-1330) | | [F] tool outputs are counted as working memory = the context itself. [I] "growing context as the conversation goes" is what the survey calls working memory |
| Episodic | "persistent storage of an agent's interactive experiences across sessions. It records specific events situated in particular temporal and environmental contexts" (S:1369-1372) | | [F] closest to "conversation memory" across sessions |
| Semantic | "storage of abstract facts, general concepts, and structured knowledge" (S:1417-1419) | | [F] |
| Procedural | "dedicated to how to perform tasks. It encodes operational skills, execution strategies, and automated routines" (S:1461-1462); figure: "Stores reusable skills, routines, and workflows that enable consistent tool use and action execution" (S:421-424) | | [F] this is where tool-related memory sits |
| User-centric | "user-specific facts and preferences, including biographical data, historical interactions, and expressed preferences, that could evolve across sessions and domains" (S:1577-1579) | | [F] conversation/profile memory |
| Agent-centric | "the agent's own experiences (trajectories, outcomes, and learned heuristics or skills)" (S:446-449) | | [F] tool-usage memory belongs here |

Scope statement: "Working memory, procedural memory, and sensory memory are predominantly agent-centric ... Semantic and episodic memory appear in both user- and agent-centric settings" (S:1556-1560). The survey says "other memory constructs such as autobiographical ... or prospective memory ... can be understood as compositions" (S:1126-1128) [O]: prospective memory (remembering to do something later) is the nearest named construct to anticipation, and it is not given its own section.
Bearing on Q-J05 (does conversation memory belong in the policy): [F] the survey treats user-centric (conversation/profile) and agent-centric (tool/skill) memory as "conceptual orientations rather than mutually exclusive categories" (S:1563-1564) and says "current benchmarks rarely require both simultaneously" (S:1568). [I] The survey does not decide the scope question; it shows the two are distinct subjects in the literature and are usually evaluated separately. Who decides: the supervisor/human.

## Q2 Tool-related memory

[F] No separate "tool memory" category exists in the taxonomy; it appears under procedural memory, episodic retrieval in tool-use settings, and as a context-growth problem.

| Item | Verbatim (file:line) | Papers cited (as printed) | Limits | Bearing |
|---|---|---|---|---|
| Tool-usage semantic memory | "ToolMem (Xiao et al., 2025) implements semantic memory of tool usage patterns, learning effective tools for specific task types." (S:3643-3644) | ToolMem, arXiv:2510.06664 (S:5391-5392; title "Enhancing multimodal agents with learnable tool capability memory") | one sentence, no numbers; survey puts it under Workflow Automation | [F] the closest named match to "tool-usage memory only" |
| Short-term tool memory | "memory that spans both short-term context and longer-term horizons (Lumer et al., 2025 ...)" (S:619); reference "Memtool: Optimizing short-term memory management for dynamic tool calling in llm agent multi-turn conversations" (S:4771-4773) | MemTool, arXiv:2507.21428 | body only cites it in a list (S:619); I read no description of its method | [U] what MemTool measures is not in this text |
| Episodic retrieval for tools | "In tool-use settings, Li et al. (2025f) retrieves episodic experience by matching the current execution state against structured representations induced from past trajectories." (S:1395-1397) | Li et al. 2025f (no arXiv id read) | | [F] |
| Workflow memory | "AWM (Wang et al., 2025v) induces reusable workflow templates from successful trajectories as parameterized procedural memory." (S:3641-3643) | Agent Workflow Memory (ICML 2025, no arXiv id printed, S:5308-5309); Memp arXiv:2508.06433 (S:4276); ReasoningBank arXiv:2509.25140 (S:4868-4869); Synapse; LEGOMem; MemGen; BREW | | [F] |
| Skill libraries | "Early skill libraries such as Voyager showed that agents can accumulate verified, reusable programs as an ever-growing behavioral repertoire" (S:1490-1492); skills "packaged as composable bundles of instructions, code, and resources that agents load on demand (Anthropic, 2025 ...)" (S:1492-1494) | Voyager (Wang et al., 2025c); Claude Agent Skills (Anthropic, 2025); SkillOps (Song et al. 2026, S:5066); SkillsBench arXiv:2602.12670 (S:4645, "Li et al. 2026") | | [F] "load on demand" is the survey's description of skills |
| Skill library maintenance | "autonomously maintain library health by merging, repairing, or retiring skills to contain accumulated skill-level technical debt (Song et al., 2026)" (S:1498-1499) | | | [O] relevant to the size of a library growing |
| Caveat on skills | "self-generated skills still underperform human-curated ones ... (Li et al., 2026)"; "a substantial fraction of community-contributed skills found to contain vulnerabilities (Liu et al., 2026)" (S:1500-1504) | | conflicting/limiting passage; no figures in the survey | [F] limits for any claim that autonomous tool memory helps |
| Tool-output context growth | "context size can grow rapidly with interaction length and the number or complexity of tool calls." (S:2415-2416); "tool-based agents must retain tool inputs, execution outputs, and intermediate states" (S:2410-2411) | | qualitative | [F] |
| Memory as interface across tool environments | "memory systems are required not merely to log past tool calls, but to maintain structured and separated representations of environment state" (S:2483-2485) | | | [F] |
| Memory and MCP | "Protocol-based interfaces such as the Model Context Protocol (Anthropic, 2024) standardize how agents access external tools and contextual resources, while skill-oriented abstractions such as Claude Agent Skills ... package procedural instructions" (S:2448-2451); "the orchestrator using MCP selects" memory sources (S:2032, located by search, not read around) | | | [F] MCP and memory are discussed together, but no MCP-server-context policy is described |

Measured effect on cost, steps or success: [F] only qualitative claims in what I read: "On WebArena ..., agents that retain episodic memory of web interaction sequences substantially outperform memoryless baselines" (S:3644-3645); "Evaluations on SWE-bench ... report that memory mechanisms improve issue resolution" (S:3661-3663); "dramatically increases robustness and efficiency" (S:3648). [O] No numbers, no cost or step counts, no sizes. Size of the tool or skill library: not stated in the ranges read ([U]); "ever-growing" (S:1491) is the only size statement. Verdict PARTLY: the survey names the papers; effects must be read in those papers.

## Q3 Cross-session memory and horizon

| Statement | Verbatim (file:line) | Limits | Bearing |
|---|---|---|---|
| Need | "foundation agents require memory that supports continuous accumulation, selective reuse, cross-session retention, and user adaptation" (S:510-512) | | [F] supports the supervisor's premise as a stated need in the literature |
| Horizon | "optimizing the experience of a specific user over extended time horizons spanning days, months, or even years" (S:1622-1623) | days appears as part of a range | [F] |
| Episodic cross-session | "recover relevant context that would otherwise be lost between sessions" (S:1377-1378); Sarin et al. (2025) "triggers episodic retrieval using session-level context and user state cues to recall relevant episodic summaries across sessions" (S:1397-1398) | Sarin = "Memoria" (S:4998); no result figures | [F] |
| Substrate persistence | Table 1: external memory "Permanent; entries maintained across sessions"; KV caches "discarded" (S:1054-1059); "unsuitable for cross-session retention" (S:1095) | | [F] cross-session persistence requires external memory, not the KV cache |
| Cold start | No passage found on cold start for agents. Search "cold.start" hit only a reference title about recommendation (S:5612). | searched whole file by regex; not read in full | NOT FOUND |
| Benchmarks | Names: LoCoMo, DialSim, LongMemEval, MemoryAgentBench, MemoryBench, PersonaMem, PrefEval, MemTrack, MSC, DuLeMon, HaluMem, LOCCO, MemBench, PerLTQA (S:830-839, 3009-3042); LongMemEval is described as "explicitly categorizing question types according to memory abilities" (S:3016-3018); HaluMem "reports memory accuracy and integrity as well as false memory rate" (S:3037-3038); MemBench "explicitly measures capacity and efficiency to capture performance and cost trade-offs under fixed memory budgets" (S:3039-3040) | I did not read Table 4 (S:2500-3005) in full | [F] user-centric benchmarks measure recall of user facts across long dialogue ("retrieving user-related facts from long dialogue and using them later", S:3008-3009) |
| Dependency distance | "dependency distance—how far apart the required information and its later use occur, such as within-turn, cross-turn, or cross-session" (S:3382-3383); "persistence under interruptions (resume after long gaps)" (S:3387) | proposed metrics ("we expect next-generation benchmarks"), not an existing benchmark | [F] |
| Critique of benchmarks | "most existing benchmarks reduce long-term personalization to synthetic factual recall"; LoCoMo "assume[s] stationary user intent"; PersonaMem "evaluates them over fully simulated sessions and does not assess memory update or refresh" (S:3955-3964); "task completion saturates even for a memoryless baseline, while recovery of the user's evolving state remains moderate and degrades further under top-K retrieval (Ma et al., 2026)" (S:3973-3975) | conflicting/limiting passage | [F] hour/day gaps between sessions are not named as a measured variable; the survey says real-user weeks/months drift is not captured |
| Agent-centric benchmarks | "remain bounded by curated environments, reset-centric task design, and short evaluation horizons" (S:3965-3967); "systematically fail to assess knowledge accumulation across episodes" (S:2363-2365) | | [F] |

Verdict PARTLY: need and benchmark names found; no measured "returns after hours/days" number found; cold start NOT FOUND.

## Q4 Cost of memory

| Statement | Verbatim (file:line) | Limits | Bearing |
|---|---|---|---|
| Token overhead | "it induces substantial token overhead, with memory contexts routinely expanding to thousands of tokens and exhibiting diminishing marginal returns (Chhikara et al., 2025)" (S:3842-3844) | one qualitative figure ("thousands of tokens"); cited paper = Mem0, arXiv:2504.19413 (S:4178-4179) | [F] |
| Latency | "This linear growth in memory cost (Kwon et al., 2023) directly translates into higher inference latency and reduced scalability" (S:3844-3845) | | [F] |
| Substrate trade-offs | Table 1 rows: retrieval latency ("Variable" for external), context window overhead ("Moderate; retrieved entries must be seri-alized into prompt"), storage cost (S:1032-1053); "retrieval adds latency" (S:1099); multiple stores "add latency and additional resource cost when querying several stores" (S:928, located by search) | | [F] qualitative, no numbers |
| Memory vs context | "a fundamental trade-off between context-budget control and long-term information accessibility" (S:2399-2401); "current approaches conflate memory capacity with prompt length" (S:3846-3847) | | [F] |
| Prohibitive cost | "naively retaining or replaying long interaction histories leads to prohibitive storage, retrieval, and inference costs, especially when deployed in real-world, always-on assistant settings" (S:3893-3894) | | [F] |
| Bounded memory | MEM1 "near-constant memory usage across arbitrarily long, multi-turn interactions" (S:1696); MemAgent "linear complexity and minimal performance degradation" (S:1700) | claims of the cited papers, no figures given here | [F] |
| Benchmark metric | "benchmarks should explicitly quantify resource-utility trade-offs, measuring memory quality as a function of token budget, storage cost, and latency" (S:3992-3994) | a recommendation | [F] the survey itself says this is not yet standard |
| Note | "Unlike fixed-task AI systems where memory primarily optimizes for efficiency and cost, foundation agents require memory that supports ..." (S:510-511) | | [O] the survey frames agent memory as serving continuity, not cost reduction; a limit for using it as support for a cost-saving claim |

Money cost: not found in the ranges read. Verdict PARTLY (qualitative only; no bill figures).

## Q5 Prefix or cache interplay

[F] KV cache appears only as an internal memory substrate: "the KV cache is a transient, inference-time memory that speeds ..." (S:993, read by search only), Table 1 (S:1050-1073), and "latent-state and KV cache substrates directly occupy the context budget" (S:1096-1097). Working memory includes "runtime states such as key-value caches" (S:1329-1330). KV-cache compression and eviction papers are cited (S:998-1011, 1157, 4104, 4282-4304, 4553, 5173).
[F] Statement that matters for the supervisor's "explicit caching" idea: KV caches "are discarded" across sessions and "lack durability" (S:1057, 1067-1068).
Not found: any statement on placing memory content in a stable prefix, cache-friendly ordering, provider prompt caching, or cache-hit billing. Searched by regex ("prefix", "KV.cache", "cache") over the whole file; only "PrefixKV" (S:5173, a vision-model reference) matched "prefix". [O] "Explicit caching" in the supervisor's sense (prompt caching of a context block) is not the survey's sense of cache (model-internal KV state and compression). Verdict NOT FOUND IN THIS TEXT.

## Q6 Deployed-agent scenarios

| Scenario | What the survey says | Limits |
|---|---|---|
| Customer support | Search for "customer", "support agent", "helpdesk", "ticket", "call center" found no match (whole-file regex). NOT FOUND. Nearest: Dialogue Systems, "memory creates the illusion of a continuous personalized relationship, managing the context window while providing conversation history" (S:3628-3630) and "Legal and Consulting" (S:3706, not read beyond the first line) | "not found" = not found by those search terms |
| Bug-fixing / cloud agents | Software Engineering: "agents operate in complex codebases requiring long-horizon reasoning, multi-file coordination, and accumulated debugging experience" (S:3656-3658); "they recall the trajectory of previous failures and fixes to achieve higher success rates in passing unit tests" (S:3663-3665); future: "shared, anonymized knowledge repositories where distributed coding agents contribute to and query a universal pool" (S:3665-3667). Agent-centric: debugging errors "follow common patterns, yet real-world systems often fail due to highly specific configuration issues, dependency conflicts" (S:1712-1714). Coding assistant example mixing user style (user-centric) and debugging strategies (agent-centric) (S:1565-1567) | no numbers; "cloud agent" not named |
| What a returning user needs | "information introduced in early rounds, such as user preferences, identity attributes, or implicit task constraints, may not immediately influence responses but often becomes decisive in later stages" (S:2380-2382); "an agent should preserve enduring user characteristics while identifying when recent interactions provide sufficient evidence to update previously inferred preferences" (S:2388-2390); "distinguish persistent preferences from temporary states" (S:1631-1632); coordination "repeatedly re-established from scratch" without retained experience (S:3816) | the support to the supervisor's returning-user need is conceptual, not measured |
| Risks | privacy leakage, memory poisoning, stale preferences (S:1643-1645, 3886-3888, 3905-3907) | limiting passages for a "load common memories" idea |

Verdict PARTLY (software engineering yes; customer support NOT FOUND).

## Q7 Anticipation

[O] Not found: no passage that predicts what a user (stranger or friend) will say, or pre-loads memory from a profile or role before the first request, with a reported effect. Searched by regex for "anticipat", "proactive", "pre-load", "first request", "role-based", "cold start" over the whole file.
Nearest passages (not the same thing):
- "proactive memory planning, where agents simulate the long-term consequences of storing, compressing, or forgetting information before committing updates" (S:3934-3936): proactive about memory updates, a future direction, no result.
- AgentFold "proactive context management, folding irrelevant trajectories" (S:3683-3684): context compaction, not prediction.
- Reference "Proactive agent: Shifting LLM agents from reactive responses to active assistance" (S:4768-4770): title only; body mention not found.
- Sarin et al.: retrieval "triggered using session-level context and user state cues" (S:1397-1398): retrieval at session start from state cues, a nearby mechanism; effect not given.
- "prospective memory" named as a composition of the five types, with no section (S:1126-1128).
- Multi-agent: "role-specific workflow and procedural memory" for "stable functional roles" (S:3824-3827): future direction, no result.
Verdict NOT FOUND IN THIS TEXT.

## What this does and does not show (for the human; no recommendation)
- [F] The survey supports the supervisor's premise that cross-session memory is treated as a core requirement for deployed agents (S:510-512, 2455-2457), and that memory and MCP-style protocols are discussed together (S:2448-2454).
- [F] It narrows two points: its "cache" is model-internal and discarded across sessions (S:1057), and it frames memory as serving continuity more than cost (S:510-511). It reports no measured cost saving, only the qualitative cost growth of memory contexts (S:3842-3845).
- [F] It does not contain customer-support use cases, cold-start treatment, or pre-loading before the first request; those parts of the supervisor's proposal cannot be backed or narrowed from this text.
- [U] Whether tool-usage memory alone or conversation memory also belongs in the policy (Q-J05) is not settled by the survey; it presents them as distinct subjects (user-centric, agent-centric). Decision belongs to the supervisor/human.
- Limitation: a survey (secondary) read in about 40% of its lines; claims about the cited papers (ToolMem 2510.06664, MemTool 2507.21428, Memp 2508.06433, Mem0 2504.19413) are the survey's, not verified against them.
