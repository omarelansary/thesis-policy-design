---
id: "FND-0023"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-103
evidence: ["EXT-0202", "EXT-0109", "EXT-0113"]
---
# Batch 5d, row C-R03/RV7UNCHK: items RV-0007 listed as "Not checked", read against the stored texts

SUM (my summary, unverified) plus FND statements; verbatim passages are quoted with `file:line` of the stored text. Only one new EXT was created (EXT-0202, ReCache limitations). The other stored texts are workspace copies in `evidence/literature-20261019/` (fetched under AUTH-011/013), which are not origin manifest sources, so `origin_extract.py` cannot make EXT ids from them (`--list-sources --grep` finds none of them, e.g. grep "2504" lists only fcrobust, toolhijacker, carboncall). Their passages are therefore cited by file and line, as the earlier steward summaries (FND-0004, FND-0005) did. Labels: [F] fact in a stored text, [O] observation, [I] interpretation, [U] unknown. No web, no messages, no design proposal.

File abbreviations: W2C = arxiv-2504.18851.txt; TB = arxiv-2406.20015.txt; TS = arxiv-2408.04682.txt; SM = arxiv-2502.11435.txt; SC = arxiv-2412.12151.txt; AL = arxiv-2404.19705.txt; AS = arxiv-2512.16883.txt; AR = arxiv-2602.07213.txt; RT = arxiv-2510.22977.txt; TO = arxiv-2604.19749.txt; MEMORA = arxiv-2604.20006.txt; BFCLB = web-bfcl-v3-multi-turn-blog.txt (all under `evidence/literature-20261019/`). ReCache = origin source `s4b-wa-recache-20261013` (arXiv 2608.19662, 1159 lines).

## Where each claim sits
- RV-0007 "Not checked" list: `reviews/RV-0007.md:38`: "When2Call 1.2%-67% and its model list; ToolBeHonest and ToolSandbox claims; SMART/SMARTCAL/Adapt-LLM/outcome-driven search; Memora; ReCache; whether the 3.1 text of the Reasoning Trap matches released data; Tool-Overuse irrelevance set composition; adaptive-retrieval appendix prompt; ..."
- The claims themselves are in `design/package-v4/05-literature-check-summary.md` (lines 30, 55, 56, 60) and in `findings/SUM-0006-literature-b2.md` / `SUM-0007-literature-ac2.md`. They are **not** in `evidence/governing/` except ReCache, which governing records mention only as an unverified abstract-level read: `STAGE4B_OPPORTUNITY_MAP-20261013.md:73` "The workers' abstract-level reads of 2026 papers (CIPO, HyperTool, ReCache, ToolSearcher, SING and others) are unverified." and `STAGE4B_FINAL_SYNTHESIS_AND_SUPERVISOR_ALIGNMENT-20261013.md:107` "Several prior-art sources (CIPO, HyperTool, ReCache, ToolSearcher, SING, ToolMATH) were read at abstract level". Grep of `evidence/governing/` for When2Call, ToolBeHonest, ToolSandbox, SMARTCAL, Adapt-LLM, Memora, Reasoning Trap, Tool-Overuse found no other hit (the D3 "Memora..." hits are the word "memorandum").

## Per-item table
Format: Row | source and lines | what the passage says | limits | relevance.

### 1. When2Call "1.2%-67%" and model list
Claim (05:30): "with **no tool provided**, models choose 'tool call' (hallucinated call) at 1.2%-67% depending on model: Llama 3.2 3B 52%, 3.1 8B 67%, 3.1 70B 57%, Qwen 2.5 21-23%, xLAM 8x22B 9.0%, GPT-4o 26% (18-item subset), tuned Mistral-NeMo-Minitron 1.2-1.9% | multiple-choice menu with 'unable to answer'; no search channel; single turn; synthetic data".

| Row | Source and lines | Passage | Limits (authors / mine) | Relevance |
|---|---|---|---|---|
| Definition | W2C:557-562; 1343-1347 | "We define tool hallucination to occur when the model chooses the tool call answer even though no tool specifications were provided for that question"; "If a model chooses the tool call answer in this scenario, they are necessarily hallucinating the tool." | [F] the event is choosing option (b) in the four-way menu, on questions with zero tools. | DIRECT: this is the quantity quoted. |
| Menu, not free generation | W2C:398-401; 135-142; 676-689 | "We implement the multiple-choice evaluation using log-probability over the four possible answers"; options: tool call, ask for more information, unable to answer, direct answer. GPT-4o etc. are scored by an LLM judge (GPT-4-Turbo-04-09) that classifies free-form output into the same four categories. | [F] confirms "multiple-choice menu with unable to answer", single question per item. [O] "Tool Hall%" for community models is a log-probability choice among four listed answers, for closed models a judged free-form output: two procedures in one table column (Tables 3 and 4). | DIRECT. |
| Range 1.2 to 67 | W2C Table 3, lines 449-541; Table 12, lines 1609-1744 | Tool Hall% column: Llama 3.2 3B 52% (461), Llama 3.1 8B 67% (467), Llama 3.1 70B 57% (473), Qwen 2.5 3B 23% (479), 7B 21% (485), 72B 23% (491), xLAM 7B 24% (497), xLAM 8x22B 9.0% (503), MNM 8B When2Call-RPO 1.2% (539). Table 12 adds Llama 3.2 1B 43% (1622), Qwen 0.5B 20%, 1.5B 23%, 14B 21%, 32B 17% (1646-1676), xLAM 1B 40%, 8x7B 13% (1688, 1700). | [O] the 1.2% end is **the authors' own RPO-trained model**; among models the authors did not train, the Table 12 span is 9.0% (xLAM 8x22B) to 67% (Llama 3.1 8B). Rows are given as whole percents (52%, 67%) except where a decimal is printed, so precision differs by row. The claim's "Qwen 2.5 21-23%" is correct for 3B/7B/72B (23, 21, 23) and also for 1.5B (23) and 14B (21); 32B is 17%, 0.5B is 20%. | DIRECT: supports the range as stated. |
| "Tuned MNM 1.2-1.9%" | W2C Table 3 lines 506-541 | MNM 4B baseline SFT 16%, 4B When2Call-SFT 4.3%, 4B When2Call-RPO 1.9%, 8B baseline 19%, 8B When2Call-SFT 7.0%, 8B When2Call-RPO 1.2%. | [O] "tuned 1.2-1.9%" holds for RPO only; the When2Call-SFT variants are 4.3% and 7.0%, and the same base models without When2Call data are 16-19%. | DIRECT: supported for RPO, incomplete for "tuned". |
| GPT-4o 26%, "18-item subset" | W2C Table 4, lines 718-723; Table 2, lines 317-338 | GPT-4o: When2Call F1 61.3, Acc 61.3%, Tool Hall% 26%; also GPT-4o-Mini 41% (727), GPT-4-Turbo-04-09 22% (733). Table 2: "LLM-as-judge subset" row has tools-provided columns 0 / 1 / 2+ = 18 / 61 / 221 (lines 333-335), and "We use 100 representative examples from each category" (690-691). Full test set: 258 / 712 / 2,682 (322-324). | [F] the 18 is the zero-tool count of the judge subset; I read the flattened table by position and the row sums to 300 (18+61+221 = 300), matching the three answer types with 100 items each (b, c, d; 0 for (a), lines 329-332). [O] **26% is not a whole number of 18 items** (4/18 = 22.2%, 5/18 = 27.8%), so the 26% for the closed models cannot be a simple count over those 18 items; the stored text does not say how it was computed [U]. [O] 05 omits GPT-4o-Mini 41% and GPT-4-Turbo 22%. | PARTIAL: number supported, base of "18-item subset" supported, but the arithmetic does not reconcile. |
| Other limits named in 05 ("no search channel; single turn; synthetic data") | W2C:940-943 "a new synthetically generated dataset"; 255-262 questions generated by Mixtral 8x22B | [F] synthetic; [O] I found no search or request channel in the text I read (grep "search" not run on the whole text; see coverage). | | DIRECT. |

**Verdict: ANSWERED (supported, with three wording limits: the 1.2% end is the authors' own tuned model; "tuned 1.2-1.9%" is RPO only; GPT-4o 26% is on 18 zero-tool items and does not reconcile as k/18).** Model list: 05 names 9 of the 24 rows of Table 12.

### 2. ToolBeHonest and ToolSandbox claims
Claim (05:55): "ToolBeHonest (14 models, 700 samples, 4-6 tools each) and ToolSandbox (34 tools) report scores for recognising unsolvable tasks, but the model is asked outright or given an exit tool, so the behaviour is prompted; ToolSandbox's category is a similarity score, not a rate."

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| TB 14 models | TB:712-728 | "We collect 14 widely-used LLMs, comprising 7 proprietary and 7 open-weight models"; list of 14 names. | [F] | DIRECT. Supported. |
| TB 700 samples | TB:682-696 | "resulting in a total of 700 samples in our ToolBH benchmark"; "total number of test samples to 1, 050". | [F] 350 solvable + 350 unsolvable (664-681). [O] 05 does not mention the 1,050 level-samples. | DIRECT. Supported. |
| TB "4-6 tools each" | TB:637-645 | "# of Tools Provided (Avg.)" per subtask 4.3, 6.0, 6.0, 4.2, 6.1, 5.5, 5.9; overall 5.4. | [O] these are **averages**; "4-6 each" is a paraphrase of averages (4.2-6.1), not a per-sample range. | DIRECT. Supported as an average. |
| TB prompted / exit tool | TB:87-88; 329-337; 345-347 | Example prompt tool list ends "UnsolvableGoal(): Called when the goal is found to be unsolvable with existing tools." Level-1: "the model must comprehend the user query and the tool descriptions, then determine and indicate whether the task is solvable or unsolvable." Level-2: "we introduce an 'UnsolvableQuery' tool to address situations where the available tools cannot achieve the sub-goals." | [F] supports "asked outright (L1) or given an exit tool (L2, example)". | DIRECT. Supported. |
| TS 34 tools | TS:484-487 | "We designed 34 tools in TOOLSANDBOX, covering 11 domains". | [F] | DIRECT. Supported. |
| TS category is a similarity score | TS:859-863 (Table 5 caption); 559-567 | "Comparing the average similarity score broken down by scenario category..."; Insufficient Information is "scenarios where the agent is not able to perform the task on purpose, by withholding a tool that would be needed for the task." | [F] supports "similarity score, not a rate". [F] **scenario count now found:** Table 6 (TS:1818-1835) lists INSUFFICIENT_INFORMATION 224 of 1032 scenarios (categories overlap: "one test scenario can be assigned with multiple scenario categories"); FND-0004 had this as [U]. | DIRECT. Supported. |
| TS authors' caveat | TS:870-881 | Hermes and Mistral "struggle at identifying when a tool call should be issued"; their higher Insufficient Information rating "should be considered a side effect instead of a positive outcome." | [F] | PARTIAL: limit on reading the II column. |

**Verdict: ANSWERED (supported). Nothing in the quoted lines contradicts 05:55. One refinement: "4-6 tools each" is an average; TS II count is 224.**

### 3. SMART / SMARTCAL / Adapt-LLM / "outcome-driven search"
Claims: 05:56 "the RL-trained Search-R1 7B searches on every query; Adapt-LLM's `<RET>` token is fine-tuned in"; FND-0004 rows 2, 4, 7, 9 and R6. "Outcome-driven search" is not a phrase in 05 or the governing records; the only stored source using "outcome-driven" is AdaSearch (AS:37 "a simple two-stage, outcome-driven RL framework"), which I took to be what RV-0007 meant [I].

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| SMART overuse | SM:256-285 | "Tool overuse refers to the excessive reliance on external tools when an agent model could have successfully completed the task using its parametric knowledge alone"; O = alpha * beta; "both models exhibit significant tool overuse, with Llama's rate exceeding 50%". | [F] Llama-3.1-8B and Mistral-7B, GSM8K, tools available "and independently decides whether to use them". [O] O is a share of **all** questions (alpha*beta); the text gives only "exceeding 50%". Agent systems row: "instructed the models to use tools only when necessary" (SM:300-303). | PARTIAL: tool present and optional; no hidden catalogue, no discovery channel. Supported. |
| SMARTCAL misuse | SC:68-83 | "a model misuses one or more types of tools in over 20% of its total reasoning steps"; "more than 90% of its stated confidence falls in the confidence bin where the reported confidence level is higher than the actual answering accuracy". | [F] models: ChatGPT series and llama-3-instruct, Entity Questions. [O] "misuses a type of tool" is not "calls a tool when none fits". | NOT RELEVANT for a spurious-call rate; supported as the authors' statement. |
| Adapt-LLM fine-tuned token | AL:346-348, 433-444, 499-513, 604-606; Table 3 AL:447-467 | "The fine-tuning process entails training the base LLM on our dataset"; Llama-2 7B with LoRA, fine-tuned on NQ and SQuAD; "the ADAPT-LLM model generates the <RET> token for approximately 82-83% of the questions in the PopQA dataset"; Table 3: NQ 82.26%, SQuAD 83.93%. | [F] 05's "fine-tuned in" is supported. [O] Table 3 header is flattened (448-454); the two percentages sit in the first value column (456, 462), consistent with the caption "percentage of PopQA questions for which the model requests additional context" (467-468). | PARTIAL: shows a trained request signal; not prompted or uninstructed. |
| Search-R1 searches every query | AS:370-388; prompt AS:3044-3054 | "Search-R1 ... equips LLMs with search access and optimizes them with outcome rewards ... its F1dec is 0 because the model invokes search for every query." The search system prompt: "if you find you lack some knowledge, you can call a search engine by <search>query</search> ... You can search as many times as you want." | [F] supported. [O] the channel is described in the prompt and RL-trained; Qwen2.5-7B-Base only. | PARTIAL: supported; instructed and trained. |
| "Outcome-driven" AdaSearch itself | AS:35-44 | AdaSearch "a simple two-stage, outcome-driven RL framework ... significantly improves search-decision quality and reduces unnecessary search calls, with only a small trade-off in QA accuracy relative to always-search." | [F] 05 does not report AdaSearch's own result; FND-0004 row 9 reports only the Search-R1 baseline. [O] AdaSearch's trained numbers (Tables 2-3) were not read here. | PARTIAL. |

**Verdict: ANSWERED for the four statements in 05:56 and FND-0004 (supported). The phrase "outcome-driven search" has no separate claim in the origin records; I read it as AdaSearch [I]. AdaSearch's own improved-model numbers: NOT READ here.**

### 4. Memora
Claim (05:60): "Memora has no tool component".

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| No tool component | MEMORA:14-39; grep of the whole file for tool / API / MCP / function call / catalog (case-insensitive) | Abstract: "a long-term memory benchmark spanning weeks to months long user conversations. The benchmark evaluates three memory-grounded tasks: remembering, reasoning, and recommending." The only whole-text hits for tool/API terms are generic: "memory APIs" (666), "AI offers artists new tools for generating" (3323), "niche tool" (3330), "Proprietary API" (3405-3413); no hit for MCP, function call, catalog. | [F] over the whole file by keyword (the earlier steward grepped too but did not read the results section). [O] keyword absence is not proof; the results section (about 740-1300) was still not read line by line [U]. | NOT RELEVANT to tool choice. Supported at keyword level. |

**Verdict: ANSWERED at keyword level over the whole stored text (no tool-use task found); line-by-line reading of the results section not done.**

### 5. ReCache
Claims: SUM-0007 row 7 (KV reuse in self-hosted inference, not provider billing; reuse needs attention changes and fine-tuning); governing records say abstract-level read, unverified.

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| What it is | `s4b-wa-recache-20261013` lines 1-30, 90-100; EXT-0109, EXT-0113 (earlier extracts) | Abstract: "Agentic language models repeatedly encode tool and skill schemas that recur across requests in different combinations and orders, preventing standard prefix caching from reusing their key-value (KV) states." Introduction: "Although this representation differs from conventional full-context prefill, lightweight fine-tuning adapts the model to the resulting attention and positional patterns". | [F] supports "KV reuse inside the model; changes attention masks; needs fine-tuning". | DIRECT for SUM-0007's description. |
| Setting limits | EXT-0202 (lines 625-650) | "Our evaluation focuses on two Qwen3 backbones, with end-to-end experiments primarily conducted on Qwen3-4B"; "Since ReCache modifies attention masks and positional layouts, the current study focuses on trainable settings, while adapting it to frozen models is left for future work."; "ReCache is designed for environments with relatively stable system instructions and resource schemas ... Extending reuse to highly dynamic resource environments ... provides another avenue for future exploration." | [F] a limit not previously quoted: authors state it is for stable schemas and trainable models. [O] this bears on whether a provider-side API user could apply it: the text says frozen models are future work. | PARTIAL: supports SUM-0007 "not something an agent calling a hosted API can apply" (that sentence is SUM-0007's inference; the text says "frozen models ... future work"). |
| Progressive disclosure statement | `s4b-wa-recache-20261013` lines 47-52 | "agentic systems commonly adopt progressive disclosure and retrieve only task-relevant schemas during execution (Shi et al., 2025; Zheng et al., 2026)." And related work: "Retrieval reduces the number of resources in the prompt, but it does not eliminate repeated encoding of recurring resources." | [F] authors' assertion with citations; no measurement of provider billing. | PARTIAL: context only. |
| Numbers | EXT-0109 (abstract), EXT-0113 | "82.3% versus 82.4% Inv-F1", "3.655x time-to-first-token speedup", "92.43%" KV memory, "1.423x" attention. | [F] no dollar or billed-token figure anywhere in the read ranges. | NOT RELEVANT to billed cost. |

**Verdict: ANSWERED for what SUM-0007 claims (supported). Not read: method sections 3-4 and experiment tables beyond EXT-0109/0113 and lines 90-200, 618-650. The governing records' "abstract level, unverified" status is still true of the parts not read.**

### 6. Reasoning Trap: does the 3.1 text match the released data?
Claim (05:53): the NTA queries name the missing tool, system prompt "You are a helpful assistant.", judge DeepSeek-R1; RV-0007 asked whether the 3.1 text matches the released data.

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| Section 3.1 on NTA | RT:215-226 | NTA: "The system prompt provides no tools, but the user query explicitly requires external tool invocation to be answered correctly (e.g., 'What is the current time in Park Forest Village?')." | [F] the example is a query that does **not** name a tool. | DIRECT. |
| Appendix A.1 on NTA | RT:1241-1248 | "No-Tool-Available Task (NTA): We generate Explicit Invocation Queries where the user directly names the required tool (e.g., 'Please use the get_restaurant_address tool to find...'). In this setting, the system prompt contains no tools". DT queries are "Implicit Requirement Queries" "without naming it" (1249-1253). | [F] **the paper's own section 3.1 example and appendix A.1 describe NTA queries differently** (implicit time question versus explicit tool naming). 05:53 relies on A.1. [O] 05 did not note this internal inconsistency. | DIRECT: the 05 statement is supported by A.1 and is contradicted in spirit by the 3.1 example. |
| Tool counts | RT:238-240; 1230-1234; 1266-1267 | 3.1: "selecting 296 tools from AgentSafetyBench"; A.1: "We began by selecting 349 diverse tools ... final set of 296 x 2 tool-query pairs" after manual QC by two annotators. | [F] consistent (349 then filtered to 296); 05 uses 296 elsewhere. | PARTIAL. |
| Judge and criteria | RT:1478-1485; 1519-1521 | "We employ DeepSeek-R1 ... as the judge"; "we manually inspected a subset of the judgments and found that the vast majority were consistent with human evaluation"; for NTA: "If the LLM directly answer user query, it should be considered a hallucination". | [F] supports 05:53. [O] no agreement figure or subset size is given. | DIRECT. |
| Released data | RT:44-46 | "Our data and codes are available at https://github.com/albert-y1n/Reasoning_Trap." | [U] the released data are not stored; no web access allowed in this batch. | DIRECT: cannot be checked here. |

**Verdict: PARTLY. "Does the 3.1 text match the released data": CANNOT DETERMINE from the stored sources (the repository is not stored). What can be said: the stored text is internally inconsistent between 3.1 (example query without a tool name) and A.1 (explicit tool name), and 05's reading rests on A.1.**

### 7. Tool-Overuse irrelevance set composition
Claim (05:54; RV-0007): irrelevance detection over 10 models, means 80.2% (frontier) and 62.5% (open-source).

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| What is stated | TO:454-471 | "We evaluate the cases where the provided tools are all irrelevant to the user's query ... Following BFCL (Patil et al., 2025), the standard benchmark for tool-use evaluation, we report irrelevance detection results. ... a correct response should either explain the tool's irrelevance or provide a standard text response without a function call. ... top-tier models achieve only 80.2% accuracy on average, indicating a 19.8% tendency to spuriously invoke tools ... error rates rising to 37.5%." Figure 2 caption: TO:430-435; group labels "OSS LLMs (62.5%)", "Frontier LLMs (80.2%)" (428-429). | [F] the set is described only as "following BFCL"; **the number of items, the BFCL version or split (v1/v2/v3 irrelevance or live irrelevance), the number and size of tool lists, and the number of runs are not stated** in the text. A grep of the whole file finds "BFCL" only at lines 459 and 1215 (reference). The appendix (G.1 and others) covers GSM8K/AIME simple-complex splits, not this set. | DIRECT: composition NOT FOUND in this text. |
| Setting conflict | TO:1306-1308 | "our experiments focus exclusively on code-as-tool scenarios (Python interpreters) for mathematical reasoning ... findings may not fully generalize to other tool types". | [O] a BFCL-style irrelevance set (function-calling tools) sits beside a limitation that says only Python-interpreter tools were used; the text does not reconcile them. | DIRECT. |
| Cross-source cue | W2C Table 3 BFCL Irr. Acc column (lines 452, 463, 469 ...), BFCLB:687-688 | W2C reports BFCL Irrelevance accuracy for, e.g., Llama 3.1 8B 40.0% (469) and Llama 3.2 3B 46.6% (463); TO Figure 2 gives Llama3.1-8B 42.70 (427), Llama3.2-3B 52.06 (425). The BFCL blog says the irrelevance category checks "if the model makes any function call". | [O] same direction, values differ by a few points; versions differ (W2C: BFCL v2; TO: not stated). Not a verification of TO's set. | PARTIAL. |

**Verdict: NOT FOUND IN THESE TEXTS (set composition: number of items, version, tool-list sizes). Setting conflict (BFCL-style irrelevance versus the "Python interpreter only" limitation) stays open.**

### 8. Adaptive-retrieval appendix prompt
Claim (05:56; FND-0004 row 8): Llama-3.1-8B used a prompted `<search>` tool in 7.0% (GSM8K) and 38.8% (MATH-500); RV-0007: "appendix prompt not read".

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| The prompt | AR:360-373 (A.2.5) | "You are an expert mathematician. Think step-by-step. Write every reasoning step inside `<think> ... </think>` blocks. If you need to look up a formula, definition, or problems, you can use the <search> tool by writing a search query inside the <search> tag like this: <search>your search query</search>  After retrieval, you may: 1. Use the information if helpful 2. Explicitly state "Retrieved information not helpful" and continue without it ..." | [F] the search channel is **described in the system prompt** with an optional ("you can", "If you need to") wording and a template, and an explicit "not helpful" exit; so the 7.0% / 38.8% are rates of **prompted, permissive** use, as FND-0004 labelled them (instructed). [O] a **no-CoT prompt** (A.2.2) and a **static retrieval prompt** (A.2.4) exist; the integration prompt (A.2.6) after retrieval says "If the retrieval is not helpful ... state 'Retrieval not used'". [O] the retrieval-rate figures are in the main text (AR:135-137), and the prompts are "exact prompts ... verbatim" (AR:325-326). | DIRECT: supports FND-0004's "instructed use" label; the wording is permissive, not mandatory. |

**Verdict: ANSWERED (the appendix prompt is now read; it matches FND-0004's description).**

### 9. "The steward's per-source rows other than Bifrost and Tool-Overuse" (also in the ledger row text)
Not part of the steward 5d task list in TASK.md (the TASK lists the first nine items); I read rows for the items above only. **NOT DONE here** (listed for the lead).

## Summary of verdicts
| Item | Verdict |
|---|---|
| When2Call 1.2-67% and model list | ANSWERED, supported with three wording limits |
| ToolBeHonest, ToolSandbox | ANSWERED, supported ("4-6 each" is an average; TS II = 224 scenarios) |
| SMART, SMARTCAL, Adapt-LLM, outcome-driven (AdaSearch) | ANSWERED, supported; "outcome-driven search" has no separate claim in the origin records |
| Memora | ANSWERED at keyword level (whole text) |
| ReCache | ANSWERED for SUM-0007's claims; new limitation quoted (EXT-0202); parts not read |
| Reasoning Trap 3.1 vs released data | PARTLY: released data not stored (CANNOT DETERMINE); internal 3.1 vs A.1 inconsistency found |
| Tool-Overuse irrelevance set composition | NOT FOUND IN THESE TEXTS |
| Adaptive-retrieval appendix prompt | ANSWERED |

## Read coverage (honest)
- W2C: read 1-30 (partial), 105-164, 255-262, 300-362, 360-440, 440-592 (Table 3 and text), 676-770, 810-830, 935-975, 1335-1365, 1600-1750. **Not read:** related work 880-935, training details 590-675, Tables 6-11 and prompts 1365-1600 beyond what is cited, confusion matrices 1880-1960. Not grepped: "search" over the whole file.
- TB: read 80-92, 325-352, 625-729. Not read: results discussion, appendices (FND-0004 read Tables 1-3).
- TS: read 480-488, 555-570, 855-885, 936-950, 1810-1838, 1990-2020. Not read: appendices D, B.
- SM: read 252-308. SC: read 66-90. AL: read 425-470, 598-610 (plus grep). AS: read 30-50, 366-394, 3040-3060. AR: read 128-144, 320-400 (grep for the rest). RT: read 40-50, 200-275, 1225-1295, 1470-1530 (grep for 3.1). TO: read 396-476, 1298-1312 (grep for BFCL/appendix). MEMORA: read 1-70, grep whole file; results section lines about 740-1300 **not read line by line**.
- ReCache: read 1-200, 618-650 (via origin_extract, hash verified 78cc8b9a3978); EXT-0109/0113 were read by the earlier steward. **Not read:** 200-470 (method, datasets), 470-618 only through EXT-0113, 780-1159 (references, appendix).
- Governing records: grepped for the item names; read STAGE4B lines 72-73 and 105-107 only.
- No claim was checked against the original PDFs; stored texts are PDF extractions with flattened tables.
