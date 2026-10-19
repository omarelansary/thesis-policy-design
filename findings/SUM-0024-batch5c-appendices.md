---
id: "FND-0022"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-103
evidence: ["EXT-0185", "EXT-0188", "EXT-0189", "EXT-0192", "EXT-0199", "EXT-0200"]
---

# Batch 5c: appendices of five stored sources, ledger row C-E02/STEWARDUNREAD

Scope: AUTH-016, repo evidence only, no web. Reading only; no verdict on any claim. [F] fact in a stored source, [O] observation, [I] interpretation, [U] unknown. Line numbers are stored-text line numbers from `origin_extract.py`. Lines marked "~" were located by counting inside a window and are approximate (+/- 5). Extracts: EXT-0185 (LiveMCPBench v2 lines 1120-1165, Appendix J prompts), EXT-0188 (SING 905-947, Table 7 trace), EXT-0189 (SING 670-704, failure taxonomy), EXT-0192 (cache study 600-632, Appendix A), EXT-0199 (TheMCPCompany 1584-1650, Table 12 prompt), EXT-0200 (TheMCPCompany 1361-1415, Appendix E and E.1).

Topics: T1 agent starts discovery for a tool it cannot see (with or without instruction); T2 cost of discovery steps; T3 cache read/write figures tied to tool definitions; T4 prompts on tool search or use.

## 0. Ledger row text (as read)
"Steward did not read appendices of TheMCPCompany, LiveMCPBench, When2Call, SING, the cache study" (design/ledger/export/ledger.csv, row C-E02/STEWARDUNREAD; detail: "v4-05 section 5: TheMCPCompany trajectories and appendices, LiveMCPBench appendices other than cited, When2Call appendices, SING appendices (prompts) and the cache-study appendices were not read.").

## 1. Summary table (one row per source)

| Source | Appendix contents (headings, lines) | T1 | T2 | T3 | T4 | Verdict |
|---|---|---|---|---|---|---|
| s4-themcpcompany-2510-19286-20261013 (3527 lines) | see 2.1 | YES, with instruction (and one counter-observation) | PARTLY (call counts, no tokens or money in the parts read) | NOTHING in parts read | YES, exact wording | ANSWERED for T1, T4; PARTLY for T2; T3 not found in the parts read |
| r3-livemcpbench (v2, 1195 lines) | see 2.2 | prompt-level only | one sentence on expenditure method, no figures | NOTHING | YES, exact wording | ANSWERED |
| s4h-b1-livemcpbench-v1-2508-01780 (v1, 903 lines) | see 2.3 | as v2 | NOTHING (no expenditure sentence) | NOTHING | YES (same prompts) | ANSWERED |
| s4c-g2-sing-2606-16591 (1118 lines) | see 2.4 | one traced example, no instruction text for the agent | NOTHING quantified | NOTHING | NO agent system prompt; only data-synthesis prompts | ANSWERED |
| r3-dontbreakcache (732 lines) | see 2.5 | NOTHING (not an MCP/tool-discovery study) | pricing table only | prices and thresholds only; no hit rates in the appendix | NOTHING | ANSWERED |
| When2Call | not stored | | | | | NOT FOUND IN THE STORED SOURCES (see 2.6) |

## 2. Per source

### 2.1 TheMCPCompany (`s4-themcpcompany-2510-19286-20261013`)
Read coverage: lines 880-1960 and 1300-1760 in full (pages 14-32); lines 1960-3527 NOT read (remaining sample trajectories G.1-G.6, page 32 onward; the list of trajectories is at ~1735-1750). Main text before line ~880 not read in this batch.

Appendix structure [F]: references end p.15 (~970); p.16 Table 5 (~975-1006, "MCPAgent's tool calling statistics"); A "DETAILED ANALYSIS OF AZURE COMPOSITE TASKS" (~1008-1090); B "MCPAGENT ERROR ANALYSIS ON THEAGENTCOMPANY TASKS" (~1100-1120, Table 6); C "TOOL RETRIEVAL ANALYSIS" (~1125-1190, Tables 7-8); D "TASK ADAPTATION AND ORACLE TOOL SELECTION DETAILS" (~1195-1340, incl. "Oracle Tool Set Limitations"); E "AGENT IMPLEMENTATION DETAILS" (1362-1395) and E.1 "TOOL FINDER FUNCTION" (~1395-1415); F "MCP TOOL DOCUMENTATIONS" (~1418-1430, Table 9 JSON spec, ~1440-1500); Tables 10-13 prompts (1510-1700); G "SAMPLE TRAJECTORIES" G.1-G.6 (~1735 to 3527).

| Topic | Passage (verbatim, EXT or lines) | Limits (authors / mine) | Relevance |
|---|---|---|---|
| T4, T1 (instruction) | Table 12 (EXT-0199, lines 1588-1650): "In addition to the tools that are given to you in the current context window, there are tens of thousands of other external tools that you can use. However, they are not immediately available to you." ... "To use external tools, you first have to find the tools that you need. You should use the "find tools" tool to search for useful tools. Think of "find tools" as a search engine for tools." ... "If you fail to find the correct tools the first time, change the query and search again." ... "You should attempt 3-4 different potential trajectories with different tools and try to find a feasible solution for the task based on the available tools before giving up." ... "If you fail at any step, regardless of whether you have used external tools in that step, you should search for potential external tools that could help you accomplish that step successfully." | Caption: "The additional information appended to OpenHands ... CodeAct system prompt for MCPAgent, which uses tool retrieval". [O] The prompt both tells the agent that unseen tools exist and instructs it to search; this is instructed discovery, so these texts cannot show whether an agent would search unprompted. No ablation without this block appears in the parts read. | DIRECT for T4 (exact prompt wording) and for T1 (the search behaviour is instructed). |
| T1 (direct-call behaviour) | EXT-0200 (Appendix E, lines 1361-1415): "In our experiments, we notice that LLMs often call the MCP tools directly and do not use the call tool function from the gateway MCP server. To avoid runtime errors, we allow the agent to call the MCP tools directly. Then, we post-process the LLM response and replace direct MCP tool calls with calls to the call tool function." | No count or rate is given for how often; no statement whether the directly called tools had been found via find_tools first. [U] whether such calls name tools the agent could not see. | PARTIAL: shows a deviation between instructed use of the gateway and observed calls; says nothing numeric. |
| T1 (what the agent can see) | EXT-0200: "The find tools function ... accepts two arguments: the search query (query argument - required) and the number of tools to retrieve (num tools argument - optional). The tool finder function returns five tools by default (num tools=5)." Also: "we use an earlier version of our Azure MCP server, with about 13,000 tools." | [F] retrieval is dense (embedding + cosine), over name, description and argument names/descriptions/types of each tool. | DIRECT for what the discovery step is; PARTIAL for T1. |
| T2 (counts of search steps) | Table 5 (~975-1006): columns "#Retrieved Tools", "#MCP Calls", "Failed Calls (%)", "#Retrieval Attempts", "Query Length"; e.g. Primitive, Sonnet 4: 19.1 / 9.5 / 22.1 / 4.2 / 42.8; Composite, Opus 4.1: 59.0 / 10.7 / 16.0 / 6.9 / 44.3 (column alignment in the stored text is broken for some rows, so read the table with care). Caption: "Query length is measured in number of characters." | [O] The extraction scrambles several rows (the "Composite" block wraps into the next lines); the values above are the two rows whose alignment is unambiguous. No tokens, money or latency in Table 5. | PARTIAL: shows number of retrieval attempts per task (a round count), not cost in tokens or money. |
| T2 (budget) | Appendix A (~1050): "GPT-5 keeps updating the secrets and different application settings until it runs out of budget and fails." | "budget" is not defined in the parts read. [U] what unit. | NOT RELEVANT beyond noting a budget exists. |
| T1, T4 (retrieval limits) | Appendix B Table 6 (~1108): "Instruction Drift w/ Wrong Tools 33.3 / Instruction Drift w/ Correct Tools 50.0 / Missed Tools 12.5 / Others 4.1" (percent of 24 failed tasks, GPT-4.1 fails with retrieval but succeeds with the oracle set); "Missed Tools: the agent fails to find the correct tools, acknowledges this, and terminates the conversation." | 24 tasks, one model. | PARTIAL for T1: failure modes of instructed discovery, including giving up. |
| T3 | Nothing in lines 880-1960 read (no cache read/write or hit-rate figure). [U] for lines 1960-3527. | | NOT RELEVANT in the parts read. |
| Oracle set (context) | "the average number of tools in the oracle tool sets is 6.5, which is sufficiently small, and all oracle tools can be provided to the LLM directly, without retrieval or significant increase in the context length." (~1352-1356, Appendix D) | | PARTIAL, background on the comparison condition (oracle set vs retrieval). |
| Trajectory form | G.1 (lines ~1760-1960): the assistant calls `find_tools` with queries such as "internal azure management tool list resources web app logs" and receives a short list of tool names; later calls the named tools. | Appendix G truncates long inputs and outputs ("Long tool inputs and outputs have also been truncated"); abbreviated by the authors ("[ ... agent keeps looking for different tools ... ]"). | PARTIAL: confirms find_tools is invoked in the instructed setup. |

### 2.2 LiveMCPBench v2 (`r3-livemcpbench`, 1195 lines)
Read: lines 560-1195 (references, appendices A-J, all pages 9-18). Lines 1-559 (main text) not read here.
Appendix headings (approximate lines): A Limitations (~726-760); B Ethical Considerations (~760-775); C LLM Usage (~777); D Reproducibility statement (~780); E Details of Task Construction, E.1 Task Statistics, E.2 Annotation Principles (~790-885); F Details of LiveMCPTool Collection, F.1 Toolset Statistics, F.2 Tool Verification (~860-915); G Implementation Details (~885-905); H Evaluation Analysis, H.1 Metrics and Judge, H.2 Tool-Use Hallucination, H.3 Error evaluation case, H.4 Human Key Points, H.5 Key-point examples (~915-1040); I Case Study: Error Examples (Figures 14-17, ~1040-1115); J Prompts (1120-1195, EXT-0185 = 1120-1165).

| Topic | Passage | Limits | Relevance |
|---|---|---|---|
| T4 | EXT-0185 (Appendix J): "You are an agent designed to assist users with daily tasks by using external tools. You have access to two tools: a retrieval tool and an execution tool. The retrieval tool allows you to search a large toolset for relevant tools, and the execution tool lets you invoke the tools you retrieved." Route tool prompt: "When faced with user needs, you (LLM) are unable to solve them on your own and do not have the tools to solve the problem." ... "This is the first step in executing unknown tasks, known as the "discovery" phase, aimed at finding the correct tool." | [F] the agent is told both tools exist and when to use the route tool. | DIRECT for T4. |
| T1 | Same prompts: the route tool description says to use it "When a user proposes a new task and you (LLM) are unsure which specific tool to use"; Appendix I, Figure 16 trace: "Let me first search for the appropriate tool to create this file." Figure 15 trace: "Let me search for the appropriate tool to get this information." | These are illustrative error cases chosen by the authors (single examples), not rates. Instructed setting (the agent is told it has a retrieval tool). | PARTIAL: shows search behaviour under instruction; no un-instructed condition. |
| T2 | Appendix G (lines 899-901): "We compute the total expenditure based on the model prices provided by OpenRouter as of January 31, 2026, accounting for both input and output tokens." Appendix I (~1035): error shares "Query Error (13.33%), Retrieve Error (50.00%), Tool Error (18.33%), and Other Error (18.33%)". | No figure for per-step or per-task cost in the appendix; the expenditure numbers, if any, are in the main text (not read). Cache pricing not mentioned. | PARTIAL for T2: gives the method of cost computation only. |
| T3 | Nothing on cache read/write in lines 560-1195. | | NOT RELEVANT. |
| Hallucination (adjacent) | H.2: "we analyzed 814 tool invocations produced by Claude-Sonnet-4. Only 9.00% involved hallucination"; "The inconsistency rate was only 1.6%. Among 11 observed hallucination-induced errors, 8 were detected by the evaluator, yielding a 72.7% detection rate." | Evaluator-agreement material; one model family. Not among T1-T4, noted because the batch also touches evaluator validity. | NOT RELEVANT to T1-T4. |

### 2.3 LiveMCPBench v1 (`s4h-b1-livemcpbench-v1-2508-01780`, 903 lines)
Read: lines 480-903 (references end ~560; pages 9-15). Lines 1-479 not read here.
Appendix headings (approximate lines): A Limitations (~565); B Ethical Considerations; C Details of Task Construction (C.1 Task Statistics, C.2 Annotation Principles); D Details of LiveMCPTool Collection (D.1 Toolset Statistics); E Implementation Details (E.1 Computing Resources and Private Models, E.2 Tool Retrieval Configuration, ~690-715); F Evaluation Analysis (F.1, F.2); G Case Study: Error Examples; H Prompts (H.1 MCP Copilot Agent Prompt, H.2 LiveMCPEval Prompt, ~815-903).
- T4: the same copilot, route, execute and evaluation prompts as v2 (text at ~815-880). [F] The v1 appendix contains no sentence on expenditure computation (v2 Appendix G adds one). [O] I did not diff the two versions beyond that.
- E.2 (~700-715): "standardized framework using Qwen2.5-72B-Instruct for tool summarization and Qwen3-Embedding-0.6B for embedding"; "we conducted all experiments within a tightly controlled window (July 20-27, 2025)". No cost or token figures.
- T1, T2, T3: nothing beyond the illustrative error figures (Figures 12-15). T3: nothing.

### 2.4 SING (`s4c-g2-sing-2606-16591`, 1118 lines)
Read: lines 560-1118 (references, appendices A-D, Tables 4-9). Main text not read here.
Appendix headings (approx): A Additional Details (~712) with A.1 Failure Analysis Taxonomy (~713-730 and EXT-0189 lines 670-704 for the numbered categories), A.2 Server Discovery with Different Decomposition Models (Table 4, ~735-800), A.3 Extra Details of Server Collection (Table 5, ~800-830); B Prompts (~835-900): B.1 Single-Tool Query Generation, B.2 Multi-Tool Query Extension, B.3 Batch Intention Generation; C Examples (~905-990): C.1 Query and Intention Synthesis Example (Table 6), C.2 Tool Substitutability Example (Table 7, EXT-0188), C.3 Error Examples by Type (Table 8); D Benchmark Comparison (Table 9, ~990-1118).

| Topic | Passage | Limits | Relevance |
|---|---|---|---|
| T1 | A.1 (EXT-0189): "For the default setting where no discovery step exists, this category is not applicable." and (Discovery Error) "This category is not applicable to the default setting, where tools are directly exposed without discovery." EXT-0188 Table 7: trace "1 search_tools(query="geocode national park lat lon", top_k=5) -> 5 servers from 779-pool", "2 get_tool_schema(...)", "4 execute_tool(...)". | [F] Table 7 is one MCP-Atlas execution "under the 779-server global pool"; no text states whether the agent was told to call search_tools. [U] instruction text for the agent in the appendix: none found. | PARTIAL: shows a discovery-then-schema-then-execute call pattern in one example; two conditions ("default" with directly exposed tools, and discovery) are named. |
| T2 | Nothing quantified (no tokens, rounds or money) in A-D. Table 7 shows a 5-call trace only. Table 4 reports Recall@5, Full-Recall@5, MRR for server discovery (e.g. Restricted setting, DeepSeek-V3.2 average 0.7251 / 0.5036 / 0.8162), which is retrieval quality, not cost. | | NOT RELEVANT to cost; Table 4 is relevant to discovery quality only. |
| T3 | Nothing on cache. | | NOT RELEVANT. |
| T4 | Appendix B holds only data-synthesis prompts (GENERATE_PROMPT, EXTEND_PROMPT, BATCH_INTENTION_PROMPT; "We use the following prompt to synthesize realistic user instructions..."). [F] No agent system prompt about tool search or tool use appears in lines 560-1118. | The ledger row says "SING appendices (prompts)": the prompts there are for building the corpus, not for the tested agent. [U] whether the agent prompt is in the main text or elsewhere (not read). | PARTIAL: confirms what the appendix prompts are (and are not). |

### 2.5 Cache study (`r3-dontbreakcache`, 732 lines)
Read: lines 330-732 (body from Section 6 Ablation, conclusion, references, appendices A-C). Lines 1-329 not read here.
Appendix headings: A "Prompt caching pricing at time of evaluation" (~603-632; Tables 3 and 4); B "Prompt Caching Mechanism" (~635-655, Figure 5); C "Cache Strategy Implementations" (~656-732, C.1 No Cache, C.2 Full Context Caching, C.3 System Prompt Only Caching, C.4 Exclude Tool Results Caching; Figures 6-9).

| Topic | Passage | Limits | Relevance |
|---|---|---|---|
| T3 | EXT-0192, Table 3 (USD per 1M tokens, "early January 2026"): GPT-4o input 2.50, output 10.00, cached 1.25; GPT-5.2 1.75 / 14.00 / 0.175; Claude Sonnet 4.5 3.00 / 15.00 / cached 0.30 / write 3.75; Gemini 2.5 Pro (<=200K) 1.25 / 10.00 / 0.125. Table 4 minimum cacheable prompt: 1,024 tokens (GPT-4o, GPT-5.2, Claude Sonnet 4.5), 4,096 (Gemini 2.5 Pro). Also "Google additionally charges for context cache storage ($4.50 per million tokens per hour)". | Prices are the authors' snapshot from provider documentation, not measured; no cache-hit rates in the appendix. | DIRECT for price and threshold figures; NOT RELEVANT for hit rates. |
| T3 (tool definitions) | C.4 (Figure 9 text): "UUIDs are appended after the system prompt and after each tool result to break the cacheable prefix at these boundaries. This prevents session-specific tool results from being cached". Body 6.3 (outside appendix, read for context): "the cacheable prefix length, primarily determined by the system prompt, is the dominant factor in caching effectiveness." | [F] The study varies cache boundaries around the system prompt and tool results; none of the read text varies tool definitions or tool-list changes. [U] whether tool definitions are part of the system prompt in their set-up (lines 1-329 not read). | PARTIAL: nothing on tool-definition caching in the read text. |
| T1, T2, T4 | Nothing: no tool discovery, no agent prompts quoted in the appendix. | The study covers long-horizon tasks with web and research benchmarks per references; no MCP discovery. | NOT RELEVANT. |

### 2.6 When2Call
Searched `--list-sources --grep` for: "when2call", "irrelevance", "2504", "call", "when". Hits were unrelated (r3-fcrobust, s3-shi-toolhijacker, s4b-wb-carboncall for "2504"; various function-calling docs for "call"). Also searched `evidence/sources.json` for "when2call" and "when 2 call": no match. Verdict: **NOT FOUND IN THE STORED SOURCES**. The appendices of When2Call cannot be read here; a read would need a new stored source (not in this batch's scope, no web).

## 3. Verdicts per ledger sub-item

| Item | Verdict | Note |
|---|---|---|
| TheMCPCompany appendices | PARTLY | Appendices A-F and Tables 5-13 read; sample trajectories G.1-G.6 mostly NOT read (lines ~1960-3527). |
| LiveMCPBench appendices (v1 and v2) | ANSWERED | Appendices read in full. |
| SING appendices | ANSWERED | Appendices A-D read in full; prompts are synthesis prompts. |
| Cache-study appendices | ANSWERED | A-C read in full; main text lines 1-329 not read. |
| When2Call appendices | NOT FOUND IN THESE TEXTS | Not stored. |

## 4. What the appendices do and do not show (no verdict on any claim)
- [F] In TheMCPCompany and LiveMCPBench the agent is told in its system or tool prompt that it has a search tool and when to use it (EXT-0199, EXT-0185). [I] These texts therefore cannot show uninstructed discovery by themselves; no uninstructed condition was found in the read parts.
- [F] TheMCPCompany reports in Appendix E that models "often call the MCP tools directly" instead of via the gateway call_tool function (EXT-0200); no rate is given.
- [F] No appendix read contains cache read/write counts or hit rates tied to tool definitions; the cache study appendix gives provider prices and minimum thresholds (EXT-0192).
- [F] No appendix read gives token or money cost of discovery steps; TheMCPCompany Table 5 gives counts of retrieval attempts per task, LiveMCPBench v2 Appendix G gives only the pricing method.

## 5. Not read (honest coverage)
- TheMCPCompany: lines 1-879 (main text), 1960-3527 (trajectories G.1 second half to G.6).
- LiveMCPBench v2: lines 1-559; v1: lines 1-479 (main texts, which may hold cost tables).
- SING: lines 1-559 (main text).
- Cache study: lines 1-329 (main text, including set-up and results tables).
- Line numbers marked "~" are approximate.
