---
id: FND-0004
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-98
evidence: ["EXT-0074"]
---
# Literature check, extended (AUTH-013), steward 4a: topic B (search/request channel use; calling a tool when none fits; deciding whether to call)

SUM (my summary, unverified). Quotes are verbatim from the stored texts in `evidence/literature-20261019/`, cited `file:line` (lines of the stored text; file names abbreviated: TS = arxiv-2408.04682, SM = arxiv-2502.11435, TO = arxiv-2604.19749, SC = arxiv-2412.12151, TB = arxiv-2406.20015, RT = arxiv-2510.22977, AL = arxiv-2404.19705, AR = arxiv-2602.07213, AS = arxiv-2512.16883). No origin extractions were used; EXT-0074 in the front matter is only the list entry required to be non-empty from the earlier pass and is not cited here (no new EXT created). Labels: [F] fact in source, [O] my observation, [I] interpretation, [U] unknown. Tables in the stored texts are flattened, one cell per line; where I assign a cell to a column I say "by column position" and give the line.

Reading coverage (honest): TS read abstract, intro, section 3 categories, section 4 results, Table 5, limitations, C.5 caption; not read: appendices A, B (tool design), D.1-D.3 (ReAct prompting, turn counts), Figure 3 (the image of the hallucination case). SM read abstract, section 3 (preliminaries), results text for Tables 3-4, discussion, limitations; Table 3 (lines 755-771) and Table 4 (774-827) partly; not read: appendices A-C (data construction, training), Figure 2 values (image, no numbers in text). TO read abstract, intro, section 3 (Table 1, Figure 2), limitations; not read: sections 4-6 (DPO and reward analysis), appendices C-G. SC read abstract, intro, setup, section 4.1-4.3 partly, limitations; not read: Tables 2-5 numbers, appendix. TB read abstract, section 3.3, Tables 1-3, section 5 error text, limitations; not read: appendices (prompts, per-subtask examples, Table 4, Table 9), Figure 4 numbers (image). RT read abstract, intro, section 3, section 4 (Tables 1-3), section 6 (Table 4), limitations, Appendix A.2 prompts, Appendix B (Table 5); not read: section 5 mechanistic analysis, DPO details, judge prompt text. AL read abstract, intro, section 3 partly, section 4 (Tables 1, 3, 4 partly); not read: related work, conclusion, Figure 2 (image). AR read in full (short). AS read abstract, intro, section 3, Table 1, 5.3 partly, limitations, Appendix C Tables 8-10 (flattened), prompts; not read: Tables 2-3 per-model numbers, appendices D, G.

## Per-source table (fixed questions 1-4)

### 1. TS ToolSandbox (Apple), arxiv-2408.04682
1. Measured: [F] "1032 test scenarios" crafted by 2 internal domain experts (TS:472-474); "34 tools" in 11 domains (TS:484-485); 13 models in Table 5 (7 proprietary, 6 open) (TS:638-858); same "minimalist prompt" for all (TS:600-605). Insufficient Information (II) scenarios withhold a tool needed for the task (TS:559-566). The number of II scenarios is not stated in the part I read [U]. Tool set per scenario: "available tools" are defined per scenario (TS:468-470); "0 / 3 / 10 distraction tools / all tools" ablations exist (TS:861-862).
2. Number or sentence: TS:559-567 "The insufficient information category is used for scenarios where the agent is not able to perform the task on purpose, by withholding a tool that would be needed for the task. This category exercises if the agent is able to identify that it cannot complete the task, as opposed to hallucinating tools or tool arguments". TS:940-948 "Insufficient Information performance overall negatively correlates with other categories. The stronger the model performance on complex tasks, the worse the insufficient information performance". TS:998-1002 (Figure 20 caption) "With only search_contacts as available tool, GPT-3.5 hallucinated remove_contact as a tool." Per-model II values: see rate table below (a similarity score, not a rate).
3. Limits: [F] authors say models Hermes and Mistral "struggle at identifying when a tool call should be issued" and their high II score "should be considered a side effect instead of a positive outcome" (TS:870-881). [F] user simulator is "subject to non-negligible hallucination" (TS:1084-1086). [O] II is scored by milestones/minefields as similarity, not as a percentage of scenarios with a hallucinated call. [O] No description of a search/request channel; the model is not offered a way to ask for tools. One run per model in the cells; "4 repeated trials" is mentioned for another purpose (TS:354). [O] 2024 models (GPT-4o 2024-05-13, Claude-3) only.
4. Relevance: PARTIAL. It measures how often models call or invent a tool when the needed one is withheld (closest to "calling when none fits"), but the tool set is small, the missing tool is not discoverable through any channel, and the metric is a similarity score.

### 2. SM SMART, arxiv-2502.11435
1. Measured: [F] "tool overuse" = tool called when parametric knowledge suffices; rate O = alpha*beta (SM:256-269). Llama-3.1-8B and Mistral-7B on GSM8K, each with tool access and free choice (SM:273-282); "Llama's rate exceeding 50%" (SM:284-285). Agent systems XAgent and AgentGPT, 50 GSM8K queries, "instructed the models to use tools only when necessary" (SM:300-303). Later: SMARTAgent fine-tuned on tools Search, Code, AskUser (SM:1551-1562 region; line 418 "AskUser"); domains Math, Time, Intention. Tool set: 3 tools, not a catalogue.
2. Sentence: SM:283-285 "both models exhibit significant tool overuse, with Llama's rate exceeding 50%". SM:900-903 "SMARTAgent reduces unnecessary tool calls by up to 50% compared to prompting the base model with tool access. However, despite this reduction, tool overuse persists". SM:958-961 "We also observe instances of tool underuse, especially in large-scale models like GPT-4o and Llama-70B, where agents neglect to call essential tools". SM:877-882 larger models "use tools less frequently in the Intention domain data".
3. Limits: [F] "we evaluate our approach on two major model families" (SM:1037-1038); domains limited to Math, Intention, Time (SM:1027-1029). [O] Overuse rate in Figure 2 and Table 6 are images; the numeric values of the Llama and Mistral overuse rates are not in the text (only "exceeding 50%"). [O] Overuse is defined on questions the model can already answer without a tool; this is not "no visible tool fits". [O] Table 4 (SM:774-827) has no per-column header for Time/Intention and is ragged; I did not use it for rates.
4. Relevance: PARTIAL. Shows that with a tool present and optional, small models call it unnecessarily and larger models sometimes underuse it; no large catalogue and no discovery channel.

### 3. TO Tool-Overuse Illusion, arxiv-2604.19749
1. Measured: [F] 3 model groups: frontier by API (GPT-5.2, Gemini-3, Claude-Haiku-4.5, DeepSeek-V3.2, DeepSeek-R1, GLM-4.6), RLVR-trained, OSS (TO:365-377); GSM8K and AIME24/25; avg@8; the tool is a Python interpreter (limitation, TO:1306). Section 3.2: all provided tools irrelevant to the query, BFCL irrelevance detection (TO:454-463).
2. Sentences: TO:98-100 "an average of 0.93 unnecessary tool calls per query that requires no external assistance" (OSS average per Table 1, TO:341-344). TO:463-467 "top-tier models achieve only 80.2% accuracy on average, indicating a 19.8% tendency to spuriously invoke tools ... This problem is more severe in open-source models, with error rates rising to 37.5%." Figure 2 per-model scores: rate table below.
3. Limits: [F] TO:1306-1308 "our experiments focus exclusively on code-as-tool scenarios (Python interpreters) for mathematical reasoning ... findings may not fully generalize to other tool types (e.g., search engines, APIs)". [O] Irrelevance detection (Figure 2) is described in one paragraph; the number of items and the tool set size are not given in lines 454-471 [U]. [O] Figure 2 is a bar-chart extraction: it lists 10 models, DeepSeek-V3.2 (a frontier model in Table 1) does not appear, and DeepSeek-R1 is counted in the "Frontier" mean 80.2: (85.11+84.96+79.42+77.85+73.55)/5 = 80.18 by my arithmetic, so the average is of 5 frontier models, not 6. Qwen2.5-32B (73.75) is printed after DeepSeek-R1 (73.55) (TO:418-421).
4. Relevance: PARTIAL. The irrelevance result is a rate of calling a tool when none fits, for 10 models, but the setting is BFCL-style (tools given, all irrelevant), not an MCP catalogue with a search channel.

### 4. SC SMARTCAL, arxiv-2412.12151
1. Measured: [F] open-domain QA on Mintaka, PopQA, Entity Questions, tail-popularity subsets (SC:403-421); gpt-4-turbo, gpt-3.5-instruct, llama-3-70b-instruct (SC:437-444); frameworks ART and DSP, which have a toolbox (several tool types) (SC:455-458; tool names in Figure 4 not read).
2. Sentence: SC:72-77 "the tracking of LLM tool usage across ChatGPT series ... and llama-3-instruct on Entity Questions data shows that on average, a model misuses one or more types of tools in over 20% of its total reasoning steps." SC:77-83 ">90% of its stated confidence falls in the confidence bin where the reported confidence level is higher than the actual answering accuracy".
3. Limits: [F] SC:794-796 "our experiments and results are limited to a subset of the existing datasets". [O] "misuse" is not "call when no tool fits"; it is wrong-type tool use within a step. Tail questions chosen to need retrieval (SC:411-416). Synthetic template QA for two datasets (SC:430-436). Rates by model not found in text I read.
4. Relevance: NOT RELEVANT for our rate question (calibration of tool confidence in QA with a few tools). Kept for the "common issue regardless of model capability" claim (SC:23-26) which is the authors' statement, not tested on catalogues.

### 5. TB ToolBeHonest, arxiv-2406.20015
1. Measured: [F] 700 samples (350 solvable, 350 unsolvable; 7 subtasks of 50+50), 3 levels, 1,050 test samples (TB:664-693); 14 LLMs, 7 proprietary and 7 open-weight (TB:712-728); temperature 0 (TB:736-743); toolset size "# of Tools Provided (Avg.)" 4.2-6.1, overall 5.4 (TB:637-645). Scenarios: missing necessary tools (MNT), potential tools (PT), limited functionality tools (LFT) (TB:504-568). Data synthesised with Gemini-1.0-Pro and GPT-4o and manually filtered (TB:585-611).
2. Sentences: TB:516-517 "LLMs might engage in hallucinatory behavior, such as invoking non-existent tools." TB:1146-1149 "Solvability hallucination. LLMs often fail to identify that a task or subtask is unsolvable ... This is the most common error". TB:1241-1243 "LLMs are prone to hallucinations even in straightforward tool-using tasks under unsolvable conditions." Rates by model: Table 2 and Table 3 (below).
3. Limits: [F] TB:1257-1264 only 7 open models, "limited scope of only seven models could introduce bias"; TB:1268-1273 tool descriptions follow MetaTool practice, "only tool names are provided without additional details such as API parameters", so "discrepancies between our evaluation benchmarks and real-world applications"; TB:1284 data "derived from synthetic sources". [O] Crucially, the model is given an explicit exit: an "UnsolvableGoal()" tool described as "Called when the goal is found to be unsolvable with existing tools" (TB:87-88) and an "UnsolvableQuery" tool (TB:345-347). The L1 task asks the model directly "whether the task is solvable or unsolvable" (TB:330-337). So this is prompted behaviour with a stated exit, not uninstructed. [O] Table 3 text calls the two numbers "Solvable Score / Unsolvable Score"; it does not say the unsolvable score at L1 is a detection rate; I read it that way.
4. Relevance: PARTIAL. Gives per-model scores for noticing that a tool is missing when the task states solvability as a question and an exit tool is offered; it does not test spontaneous use of a request channel.

### 6. RT The Reasoning Trap, arxiv-2510.22977
1. Measured: [F] SimpleToolHalluBench with two settings: No-Tool-Available (NTA) and Distractor-Tool (DT); 296 tools selected from AgentSafetyBench, queries generated by ChatGPT-4o; hallucination rate = fraction flagged by an LLM-as-judge (RT:238-262). NTA system prompt is "You are a helpful assistant." and provides no tools (RT:1274-1277, 1286). DT supplies one irrelevant tool (RT:228-237, 1278-1281). Models: Qwen2.5-7B, Llama3.1-8B, Qwen3-8B/32B, plus Table 5 Qwen3-4B/235B, DeepSeek-V3/R1, Kimi-K2 (RT:497-528, 1736-1767).
2. Sentences: RT:70-74 "tool hallucination, which occurs when models either fabricate non-existent tools or misappropriate available but irrelevant tools". RT:1783-1788 "DeepSeek-R1 (671B) ... exhibits higher hallucination rates (17.6% RNTA) compared to ... DeepSeek-V3 (10.8%)". Rates: table below.
3. Limits: [F] RT:987-992 "benchmark ... focuses on single-step tool invocation scenarios; real-world agentic systems often involve multi-step tool chains". [O] NTA gives the model no tools and no channel at all; the "tool call" it makes is a fabricated call in text. It is not a model with an available search tool deciding not to use it. [O] Judge model and its accuracy not read (RT:1479-1486 region). [O] Prompt-engineering mitigation ("You must not use any tools that are not explicitly provided to you", RT:900-902) only moved ReCall-7B from 90.2 to 87.5 (RT:879-886).
4. Relevance: PARTIAL. It is the nearest published rate of "calling or inventing a tool when none exists", for 13 model configurations, but the setting has no tool list and no request channel.

### 7. AL Adapt-LLM, arxiv-2404.19705
1. Measured: [F] Llama-2 7B fine-tuned (LoRA) to emit a special token <RET> when it does not know the answer; PopQA test; IR system Contriever, one passage (AL:433-445, 481-485, 499-508). Training on NQ and SQuAD (AL:523-525).
2. Sentence: AL:604-606 "the ADAPT-LLM model generates the <RET> token for approximately 82-83% of the questions in the PopQA dataset". Table 3: NQ 82.26% <RET> usage; SQuAD 83.93% (AL:455-466, columns by position as the table header is flattened and shifted).
3. Limits: [O] The behaviour is trained in, not prompted or spontaneous; one 7B model; one test set (PopQA); retrieval is a single IR system, not a catalogue; the decision is "ask for context", closest to a request token but it is supervised fine-tuning. [F] AL:643-644 adding context to questions answered directly lowered accuracy "up to 7 absolute points".
4. Relevance: NOT RELEVANT for uninstructed initiation (trained token), PARTIAL for showing that a request signal can be learned. No tool catalogue.

### 8. AR Adaptive retrieval in chain-of-thought, arxiv-2602.07213
1. Measured: [F] Llama-3.1-8B-Instruct, zero-shot; system prompt instructs: "If you need to look up a formula, definition, or problems, you can use the <search> tool" (AR:365-367); GSM8K (1,319 problems) and MATH-500 (AR:199, 570); retrieval corpora MathPile or OpenMathInstruct-2.
2. Sentences: AR:135-137 "On the GSM8K benchmark, the agent invoked retrieval in only 7.0% of cases ... 38.8% on the much harder MATH-500". AR:140-141 "from 14.0% on Level 1 problems to 60.4% on Level 5 problems". AR:211-213 accuracy without retrieval 84.2% (GSM8K) and 63.7% (MATH-500).
3. Limits: [O] The search channel is described in the prompt, so this is instructed use. Single 8B model. Math domain. Table 1 header is ragged: an unnamed first value column "43.7% / 29.8%" precedes CoT (AR:108-128); I read it as the no-CoT baseline [I]. [O] Internal inconsistency: text says retrieval "helping in 57 cases (5.3%) and hurting in 16 (1.5%)" (AR:200-201) whereas Table 4 shows 59 and 14 (AR:556-557). The text also says "Static retrieval ... accuracy declines by 6.3pp" and "Adaptive ... exceeding the CoT baseline by 1.1 pp" with a single greedy run, no confidence interval.
4. Relevance: PARTIAL. A rate of using an instructed search channel by difficulty; one small model; no catalogue.

### 9. AS AdaSearch, arxiv-2512.16883
1. Measured: [F] search agents trained by RL from Qwen2.5 (3B, 7B) and Llama; Search-R1 official checkpoint re-evaluated (AS:370-380); QA benchmarks (macro-averaged); F1dec = F1 of "search not needed" decisions against oracle labels from the model's own parametric answer (AS:309-319).
2. Sentences: AS:383-388 "its F1dec is 0 because the model invokes search for every query. This overreliance ... exemplifies tool overuse". Table 1 (AS:338-347): Search-R1 EM 39.4, F1dec 0.0; "RL w/o Search" EM 27.6.
3. Limits: [F] AS:1562-1565 "we only evaluated models up to 7B parameters". [O] Search-R1 is trained with the search tool and its prompt says "You can search as many times as you want" (AS:3050); channel is instructed and RL-trained. Table 1 is ragged: by column position Search-R1 reads TP 0.0, TN 72.4, FP 0.0, FN 27.6 (AS:341-342), and the RL w/o Search row has F1dec 27.6 although the stated formula with TP/FP above would not give that number; I could not reconcile it [U]. Tables 8 and 9 are flattened and the column headers are separated from the numbers (AS:2425-2447); I did not use them.
4. Relevance: PARTIAL. Another observation that an RL-trained 7B agent that has a search tool uses it on all queries; nothing on a hidden catalogue.

## Rate tables (cells with file:line; by column position where noted)

### R1. ToolSandbox Table 5, Insufficient Information column (8th value of each model block: average, STC, MTC, SUT, MUT, SD, C, II, ...; header TS:859-863). Score is an average similarity, higher = fewer hallucinated calls; not a percent of scenarios.
| Model | II score | line | all-category avg (line) |
|---|---|---|---|
| GPT-4o-2024-05-13 | 42.0 | TS:646 | 73.0 (639) |
| Claude-3-Opus | 57.3 | TS:663 | 69.2 (656) |
| GPT-3.5-Turbo-0125 | 22.3 | TS:680 | 65.6 (673) |
| GPT-4-0125-Preview | 33.6 | TS:697 | 64.3 (690) |
| Claude-3-Sonnet | 44.2 | TS:714 | 63.8 (707) |
| Gemini-1.5-Pro-001 | 76.2 | TS:731 | 60.4 (724) |
| Claude-3-Haiku | 39.4 | TS:748 | 54.9 (741) |
| Gemini-1.0-Pro | 65.5 | TS:765 | 38.1 (758) |
| Hermes-2-Pro-Mistral-7B | 48.3 | TS:782 | 31.4 (775) |
| Mistral-7B-Instruct-v0.3 | 76.8 | TS:799 | 29.8 (792) |
| C4AI-Command-R-v01 | 47.8 | TS:816 | 26.2 (809) |
| Gorilla-Openfunctions-v2 | 69.2 | TS:833 | 25.6 (826) |
| C4AI Command R+ | 35.3 | TS:850 | 24.7 (843) |
[O] Each model block has 16 values (not ragged). [F] The authors say the high scores of weak models are "a side effect instead of a positive outcome" (TS:875-881).

### R2. Tool-Overuse Illusion Figure 2, irrelevance detection score (%): higher = fewer spurious calls (TO:407-427; error rate = 100 - score by the authors' own reading, TO:463-467)
| Model | score | line |
|---|---|---|
| Claude-Haiku-4.5 | 85.11 | TO:409 |
| GLM-4.6 | 84.96 | TO:411 |
| GPT-5.2 | 79.42 | TO:413 |
| Qwen3-8B | 79.07 | TO:415 |
| Gemini3-Pro-Preview | 77.85 | TO:417 |
| DeepSeek-R1 | 73.55 | TO:419 |
| Qwen2.5-32B-inst | 73.75 | TO:421 |
| Qwen2.5-7B-inst | 65.16 | TO:423 |
| Llama3.2-3B-inst | 52.06 | TO:425 |
| Llama3.1-8B-inst | 42.70 | TO:427 |
Means stated: frontier 80.2%, OSS 62.5% (TO:428-429). [O] DeepSeek-V3.2, GPT-5.2's peers in Table 1, are missing from this figure list (see source 3).

### R3. Reasoning Trap hallucination rates (%), No-Tool-Available (NTA) and Distractor-Tool (DT) (lower is better)
| Model / config | R_NTA | R_DT | lines |
|---|---|---|---|
| Qwen2.5-7B Instruct | 34.8 | 54.7 | RT:503-504 |
| Qwen2.5-7B R1-Distill | 74.3 | 78.7 | RT:506-507 |
| Llama3.1-8B Instruct | 62.5 | 99.7 | RT:510-511 |
| Llama3.1-8B R1-Distill | 96.3 | 100 | RT:513-514 |
| Qwen3-8B Think Off / On | 4.1 / 5.4 | 36.2 / 56.8 | RT:517-521 |
| Qwen3-32B Think Off / On | 5.1 / 8.8 | 46.6 / 50.7 | RT:524-528 |
| Qwen3-4B(2507) Instruct / Thinking | 3.4 / 29.4 | 24.0 / 32.1 | RT:1742-1745 |
| Qwen3-235B(2507) Instruct / Thinking | 3.7 / 6.1 | 23.3 / 30.7 | RT:1749-1753 |
| DeepSeek-671B V3 / R1 | 10.8 / 17.6 | 33.8 / 42.6 | RT:1756-1760 |
| Kimi-K2-1T Instruct / Thinking | 1.0 / 4.4 | 15.5 / 21.3 | RT:1762-1767 |
| ReCall-7B (GRPO on SynTool) | 90.2 | 100.0 | RT:880-881 |
[O] Cells are by position in Tables 1 and 5 (two numbers after each config). Tables are not ragged. No GPT-4o, Claude or Gemini rows.

### R4. ToolBeHonest Table 2 (percent; by column position per model: MNT L1-EM, L2-PR, L3-PR, L3-MS; PT same four; LFT same four; Overall; header TB:772). L1-EM is exact match on a binary solvable/unsolvable question over solvable and unsolvable samples together, not a hallucination rate.
| Model | MNT L1-EM | PT L1-EM | LFT L1-EM | Overall | lines |
|---|---|---|---|---|---|
| GPT-3.5-Turbo | 16.0 | 5.0 | 33.0 | 13.4 | TB:775, 779, 783, 787 |
| Gemini-1.0-Pro | 12.0 | 3.0 | 25.0 | 20.6 | TB:789, 793, 797, 801 |
| GPT-4-0613 | 59.3 | 44.0 | 31.0 | 31.7 | TB:803, 807, 811, 815 |
| GPT-4-1106 | 44.7 | 32.0 | 42.0 | 32.5 | TB:817, 821, 825, 829 |
| GPT-4-Turbo | 58.7 | 45.0 | 42.0 | 35.9 | TB:831, 835, 839, 843 |
| GPT-4o | 53.3 | 47.0 | 56.0 | 37.0 | TB:845, 849, 853, 857 |
| Gemini-1.5-Pro | 62.7 | 56.0 | 69.0 | 45.3 | TB:859, 863, 867, 871 |
| Llama-3-70B | 31.3 | 19.0 | 34.0 | 14.6 | TB:958, 962, 966, 970 |
| Llama-3-8B | 13.3 | 7.0 | 45.0 | 8.1 | TB:930, 934, 938, 942 |
| Mistral-7B | 27.3 | 20.0 | 31.0 | 10.1 | TB:944, 948, 952, 956 |
| Mixtral-8x7B | 4.0 | 0.0 | 18.0 | 4.8 | TB:888, 892, 896, 900 |
| Llama-2-7B / 13B / 70B | 5.3 / 16.7 / 17.3 | 4.0 / 2.0 / 2.0 | 46.0 / 20.0 / 33.0 | 6.5 / 3.7 / 7.9 | TB:902, 874, 916 (MNT); 906, 878, 920 (PT); 910, 882, 924 (LFT); 914, 886, 928 |
[O] Table 2 is not ragged (13 values per model). Model rows are in the order printed, not sorted by size.

### R5. ToolBeHonest Table 3, "Solvable Score / Unsolvable Score" (TB:1158-1186). Only 4 models; ragged: Gemini-1.0-Pro L2, L3, Overall are packed on one line (TB:1169) while L1 is on its own line (TB:1168).
| Model | L1 | L2 | L3 | Overall |
|---|---|---|---|---|
| Gemini-1.0-Pro | 98.9 / 13.1 (1168) | 83.1 / 10.0 | 84.3 / 29.5 | 88.7 / 20.6 (all TB:1169) |
| GPT-4o | 95.4 / 52.3 (1171) | 88.3 / 53.9 | 83.2 / 21.0 | 89.0 / 37.0 (all TB:1172) |
| Llama-3-8B | 93.7 / 20.6 (1175) | 74.9 / 3.6 | 64.4 / 4.2 | 77.6 / 8.1 (TB:1175-1178) |
| Llama-3-70B | 100.0 / 28.6 (1180) | 86.2 / 23.1 | 66.8 / 3.3 | 84.3 / 14.6 (TB:1180-1182) |
[I] If the unsolvable L1 score is the detection rate, GPT-4o would miss 47.7% of unsolvable tasks at L1 (100-52.3). The source does not state this conversion.

### R6. Other rates
- SMART: Llama-3.1-8B tool overuse on GSM8K "exceeding 50%" (SM:284-285); Mistral-7B value only in an image [U].
- Adapt-LLM Llama-2-7B <RET> rate on PopQA: 82.26% (NQ-trained) and 83.93% (SQuAD-trained) (AL:456, 462; column by position).
- Adaptive retrieval Llama-3.1-8B: search used in 7.0% (GSM8K) and 38.8% (MATH-500) of problems (AR:135-137).
- AdaSearch Qwen2.5-7B Search-R1: searches on every query (AS:384-385); F1dec 0.0 (AS:340).

## Topic B update
Question: does anything here give a rate for how often a model with a search/request channel that is not told to use it uses it when no visible tool fits, or a rate of calling or inventing a tool when none exists?

1. Uninstructed use of a search/request channel when no visible tool fits: [U] Not found in the nine stored texts. Every text with a search or request channel either tells the model about it in the prompt (AR:365-367; AS:3050 for Search-R1; ToolBH offers an UnsolvableQuery/UnsolvableGoal exit and asks the solvability question directly, TB:87-88, 330-337) or trains it in (AL: fine-tuned <RET> token; AS: RL; SM: SMARTAgent fine-tuned with AskUser/Search). Searched: the nine files named in the task, by reading the method sections and grepping for the channel terms. [O] Nothing here tests a channel present in the tool list with a neutral description and no instruction.
2. Rate of calling or inventing a tool when none exists: partly yes, with different definitions and no MCP-scale catalogue:
   - RT NTA (no tools provided at all): from 1.0% (Kimi-K2 Instruct) to 96.3% (Llama3.1-8B R1-Distill); Qwen3-8B Think Off 4.1%, DeepSeek-V3 10.8%, DeepSeek-R1 17.6% (table R3). Judge-based, single step.
   - RT DT (one irrelevant tool provided): 15.5% to 100% (table R3).
   - TO irrelevance detection (all provided tools irrelevant): frontier mean 80.2% correct, i.e. "19.8% tendency to spuriously invoke tools"; open-source error rate 37.5% (TO:463-467); per model in table R2.
   - TS Insufficient Information (similarity score, not a rate) for 13 models (table R1); TB L1-EM and the Table 3 unsolvable score for 4 models (tables R4, R5); these are different quantities and should not be pooled with RT or TO.
3. [O] Conflicting or limiting readings: the two kinds of evidence point in different directions on strong models. RT reports low rates for large instruct models in the no-tool setting (1.0-10.8% for Kimi-K2 Instruct, Qwen3-235B Instruct, DeepSeek-V3), but TO reports about 20% spurious calls for frontier models when irrelevant tools are present, and TS reports the lowest II scores among the strongest 2024 models. The settings differ (no tools vs irrelevant tools), so I cannot say which applies to a hidden catalogue [U]. RT also shows reasoning variants hallucinate more (RT:1783-1793).
4. [O] None of the nine reports a bill, token count, or cost of the extra calls.

## What I could not read or verify
- Figure and chart values (SM Figure 2, Table 6; TO Figures 3-6; TB Figure 4; AL Figure 2) are images; their numbers are not in the stored text.
- Appendices not listed as read in the coverage paragraph, including the judge prompt and judge accuracy in RT, all of SC Tables 2-5, TS appendices D.1-D.3, TO sections 4-6, AS Tables 2-3.
- No claim has been checked against the PDFs; the stored text is a PDF text extraction (flattened tables).
