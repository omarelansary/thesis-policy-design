---
id: "FND-0026"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-105
evidence: ["EXT-0151", "EXT-0153", "EXT-0180", "EXT-0203", "EXT-0204"]
---

# Batch 9b: MCPVerse (v2 vs v1) rows C-S19/S43, S45, S42 (remaining), S40-S41

Sources. v2: workspace copy `evidence/literature-20261019/pdf-mcpverse-2508.16260v2.txt` (cited `v2:LINE`; 1280 lines, differs in line numbering from the origin text `r3-mcpverse`, 963 lines, EXT-0151/0153/0180). v1: origin source `s4h-b1-mcpverse-v1-2508-16260` (545 lines, two-column layout, ragged; EXT-0203 = lines 232-241, EXT-0204 = lines 300-345). Page image `pages/mcpverse-2508.16260v2-p5.png` read (Figure 2 pies, section 3.2). Ranges not read: v2 lines 60-130 (Table 1), 835-930 (references); v1 lines 1-60 read only via no-write, not stored; v1 has no appendix text in the stored copy (545 lines end at references); no page image of v2 p7 (Table 2) exists, so Table 2 cells are from the text layer only.

Labels: [F] fact in source, [O] observation by steward, [I] interpretation, [U] unknown.

## S43 retrieve mode (v2 section 4.3, v2:748-786; also EXT-0153 stored lines 520-545, EXT-0180)

| Row | Source and lines | What the passage says | Limits | Relevance |
|---|---|---|---|---|
| Embedding model | v2:755-756 | [F] "we use OpenAI's text-embedding-3-large model to embed the descriptions of all MCP servers and store them in a database" | Server-level, not tool-level | DIRECT |
| What is embedded (query side) | v2:757-759 | [F] "each tested model first generates the descriptions of the MCP servers it needs. These descriptions are also embedded with text-embedding-3-large" | Query is a model-written server description, not the task text | DIRECT |
| top-k and pool | v2:759-762 | [F] "the top-5 most relevant servers are selected using cosine similarity. These retrieved servers are then mounted"; "in retrieve mode, more servers may be mounted but the selection is less precise" | Pool = all 65 MCP servers (v2:318, 138) by implication [I]; text of 4.3 does not state the pool size. Top-5 is servers, so tool count per run is not stated [U] | DIRECT |
| Who judges; does the judge see retrieval | v2:345-348, 1114-1116; 990-1013 | [F] Section 4.3 says nothing on the judge. Main text: "we employ an LLM and prompt to assess semantic equivalence" (no model named, v2:345-346); Appendix F: "Our primary evaluation was conducted using the open-source model QwQ-32B as the judge" (v2:1114). The judge prompt (Table 6) receives only question, reference answer and model output | [O] The prompt has no field for the toolset or retrieval mode, so the judge cannot see retrieval by construction of that prompt. [U] whether a different judge was used for Table 4: not stated | DIRECT |
| Statement on judge behaviour in retrieve mode | v2:748-786 | NOT FOUND: no sentence on judge behaviour, judge agreement or judge bias in retrieve mode (searched v2 for "judge", "retriev", "Retrieve"; hits listed at v2:145,169,325,345-348,749-786,1112-1266) | | DIRECT |
| Table 4 results and the text claim | v2:763-785 | [F] "model performance in retrieve mode is consistently and significantly lower than in oracle mode and standard mode." Table 4 rows: DeepSeek-V3.1-Terminus 56.6 / 52.1 / 39.8; Qwen3-235B-2507 44.8 / 53.2 / 39.4; Claude-4-Sonnet 44.8 / 53.2 / 40.3; GPT-5 68.1 / 23.4* / 45.0 (Oracle / Standard / Retrieve) | [O] GPT-5 Retrieve 45.0 is higher than its Standard 23.4 (the Standard cell is prompt-based, asterisk), so "consistently lower than ... standard" does not hold for GPT-5 on the printed numbers. Only 4 models; no tool-count or token figure for Retrieve | DIRECT |

Verdict S43: ANSWERED for embedding model, query construction, top-5 servers, judge prompt inputs; NOT FOUND for judge behaviour in retrieve mode and for the retrieved tool count or token size.

## S45 internal contradictions in v2 (all by line)

| # | Item | Lines | Observation |
|---|---|---|---|
| 1 | Task types: two vs three | text v2:264-266, 275 "two main types: Information Retrieval and System Operation" vs Figure 2(a) (image p5): Information Retrieval 39.2%, System Interaction 40.2%, Hybrid Tasks 20.6%; caption v2:270 | [F] text says two; the figure shows three, with a third "Hybrid" category and the name "System Interaction" differing from "System Operation". Pie percentages sum to 100.0 |
| 2 | Max-Scale models: two (text) vs three (Table 2) | v2:320-322 "only models with extended context capabilities, such as Claude-4-Sonnet and Gemini-2.5-Pro"; 551-552 "can only be evaluated with models such as Claude-4-Sonnet and Gemini-2.5-Pro"; 571-572 "feasible only for Claude-4-Sonnet and Gemini-2.5-Pro"; Table 2 Qwen3-235B-2507 row v2:454-468 Max-Scale cells 31.6 / 44.3 / 23.7 / 26.7 | [F] Table 2 gives Qwen3-235B-2507 a Max-Scale score (context window 1M). Text says "such as", in 571 "only". Fig. 3 text 4.2.2 line 640-641 "For those evaluable at Max-Scale" does not name them |
| 3 | 140k vs 147k tokens | v2:18, 140, 552, 571 (147k) vs v2:319 (about 140k) | [F] same Max-Scale toolset given as "approximately 140k" in 3.3 and "exceeding 147k"/"approximately 147k" elsewhere. v1 had the same pair (EXT-0204 context; v1 line ~238-240: "approximately 140k" and "approximately 147k") |
| 4 | Tool counts: 550+/552, 220+, 128/512 caps | v2:17 "more than 550"; 139 "552 unique tools"; 259 "more than 552"; 315 "32 MCPs (totaling 220+ tools)"; 318 "550+ tools" | [O] 550+ vs 552 vs "more than 552" are mutually loose, not strictly contradictory. v1 said 218 tools for Standard (v1 EXT-0204 area, line ~262-290: "218 tools in our Standard mode"); v2 says 220+. Table 2 Max Tool Count: GPT-5 "-" (v2:510) while text v2:554 and 573 says GPT-5 caps tools at 128 |
| 5 | Sample counts | v2:264 "250 tasks"; Figure 2 percentages (L1 31.9, L2 45.4, L3 22.7; time-sensitive 14.2) | [O] 31.9% / 45.4% / 22.7% of 250 give 79.75 / 113.5 / 56.75 tasks, non-integers; 14.2% of 250 = 35.5. So the percentages do not correspond to integer counts of 250 tasks [I] percentages may be of a different count or rounded; the text does not say |
| 6 | Number of models | v2:148 "benchmarked 12 leading LLMs"; v2:548-550 lists 12 names (DeepSeek-V3, V3.1-Terminus, R1-0528, Claude-4-Sonnet, Qwen3-235B-A22B, Qwen3-235B-2507, Qwen3-30B-A3B, Gemini-2.5-Pro, GPT-4o, GPT-5, Kimi-K2, GLM-4.5); Table 2 has 12 rows; Table 5 (hyperparameters, v2:960-986) has 8 rows (no V3.1-Terminus, Qwen3-235B-2507, GPT-5, GLM-4.5) | [F] 12 consistently in text and Table 2; Table 5 lists only 8, though v2:954 "for each model, as detailed in Table 5". v1 said "8 leading LLMs" (EXT-0204 context, v1 text near line 82: "we benchmarked 8 leading LLMs") |
| 7 | Appendix references | v2:325 Appendix B, 348 Appendix D, 556 Appendix E, 557 Appendix C | [F] all four exist (v2:932, 952, 988, 1053). No reference found in the main text to Appendix F (judge analysis, v2:1112) or G; [O] no non-existent appendix reference found |
| 8 | Oracle definition | v2:309-312 "minimal set of tools"; v2:155 "only per-question minimal MCPs"; v2:761 "annotated ground-truth servers" | [O] tool-level vs MCP-level wording; v1 said "minimal set of MCPs" |
| 9 | Table 2 cells that duplicate another row | v2:495 (Gemini-2.5-Pro Max-Scale cells) and v2:503 (GPT-4o Standard cells) both "31.4* 37.7* 35.7* 20.8*"; v2 Table 8 GPT-4o Standard (QwQ) 31.38 / 37.66 / 35.71 / 20.75 (v2:1228-1231) | [O] The Gemini Max-Scale cells are identical to GPT-4o Standard. Layout in the text layer is ragged (the cells appear in the Gemini row at 495 and the GPT-4o row at 503), so this may be a copy error in the paper or an extraction artefact; cannot be determined without the page image [U]. The v1 Gemini Max-Scale was 42.28 / 60.00 / 42.64 / 24.19 (EXT-0204 text, ragged) so a value change in v2 is not itself inconsistent |
| 10 | Table 4 vs Table 2 | v2:774-781 vs v2:454-468, 424-438 | [F] Table 4 Qwen3-235B-2507 44.8 / 53.2 equals Table 2 (44.8 / 53.2, v2:457,461). Table 4 Claude-4-Sonnet gives Oracle 44.8 / Standard 53.2, but Table 2 Claude is 62.3 / 62.4 (v2:427,431) and Table 3 62.28 / 62.36. The Claude cells in Table 4 are identical to the Qwen3-235B-2507 cells (not to Gemini; Gemini is not in Table 4) |
| 11 | Retrieve vs Standard claim | v2:763 vs v2:782-785 | see S43 row (GPT-5 Retrieve 45.0 > Standard 23.4*) |
| 12 | Claim of Claude-4-Sonnet "improving" | v2:23, 158 vs Table 2 | [O] Oracle 62.3 to Standard 62.4 is +0.08 (Fig. 3 label "+0.08", v2:594); described as "higher score in Standard mode than in the simpler Oracle mode" (v2:158-159). Not a contradiction but a gain of 0.1 point on 250 tasks; no variance reported [U] |

Verdict S45: ANSWERED (12 items, items 1, 2, 3, 6, 10 are clear textual contradictions; 4, 5, 9 are possible; 7 none found). CANNOT DETERMINE for item 9 (needs a page image of v2 p7).

## S40-S41 v1 versus v2 Claude-4-Sonnet scores and cause of shift

Transcription of the v1 Table 2 (EXT-0204, lines 300-345; ragged, rows interleaved because of two-line model names). The Claude row has to be read from the line printed under "GPT-4o-20241120 128k" (EXT-0204 line 5 of the table): `57.81 68.33 53.49 51.61 | 61.01 70.00 56.59 56.45 | 57.77 66.66 55.04 51.61`. [O] The same line also carries the label "GPT-4o-20241120 128k" and the row labelled "Claude-4-Sonnet 200k" carries R1-style numbers (`50.77 ... 50.28`), so labels and values are offset. My assignment: Oracle avg 57.81 (L1-L3 mean = 57.81), Standard avg 61.01 (mean = 61.01), Max-Scale avg 57.77 (mean = 57.77). The L1-L3 means check arithmetically: (68.33+53.49+51.61)/3 = 57.81; (70.00+56.59+56.45)/3 = 61.01; (66.66+55.04+51.61)/3 = 57.77. [I] This arithmetic supports the column assignment although the label alignment is ragged.

| Row | Source and lines | What the passage says | Limits | Relevance |
|---|---|---|---|---|
| v1 scores | EXT-0204 | v1: Claude-4-Sonnet Oracle 57.81, Standard 61.01, Max-Scale 57.77 (by the arithmetic above) | Ragged layout | DIRECT |
| v2 scores | v2:427, 431, 435 (and 566-570) | Claude-4-Sonnet Oracle 62.3, Standard 62.4, Max-Scale 44.2; "Standard and Max-Scale are led by Claude-4-Sonnet with 62.4 and 44.2" | Table 2 text layer | DIRECT |
| v1 internal inconsistency | EXT-0204 text | v1 prose: "Its average score rises from 57.77 to 61.01, a relative increase of 5.61%" while the same prose says the Oracle score is "57.81"; 57.77 is the Max-Scale cell in the v1 table. (61.01-57.77)/57.77 = 5.61%. v1 abstract/intro "accuracy of only 57.77%" as top model (v1 line ~82 area) | [O] v1 prose uses 57.77 as the Oracle baseline though the table gives 57.77 for Max-Scale and 57.81 for Oracle. v1 also states a decrease for Max-Scale vs Standard is absent from its prose ("Only one model benefits") [I] | DIRECT |
| Differences | v1 vs v2 | Oracle +4.5 (57.81 to 62.3); Standard +1.4 (61.01 to 62.4); Max-Scale -13.6 (57.77 to 44.2). Ranking: v1 top Claude in Standard; v2 top Oracle GPT-5 68.1 | Arithmetic by steward | DIRECT |
| Judge change | EXT-0203 vs v2:1114-1120 | v1: "The scoring model we use for the LLM-as-a-judge is GPT-4o-20241120. We note that using open-source models, such as Qwen-32B, also yields a consistent ranking of results (see Appendix 2...)". v2: "Our primary evaluation was conducted using the open-source model QwQ-32B as the judge ... GPT-4o as an alternative judge" | [F] primary judge changed from GPT-4o to QwQ-32B between versions (neither version says it changed) | DIRECT |
| Judge effect size within v2 | v2:1133-1142, Table 8 | Claude-4-Sonnet Standard: GPT-4o 61.26 vs QwQ-32B 62.36, a gap of 1.10; other rows within about 0.4-1.6 (e.g. Qwen3-235B-2507 51.61 vs 53.18) | Table 8 is Standard mode only; no Oracle or Max-Scale judge comparison | PARTIAL |
| Other version differences visible in the texts | v1 vs v2 | Models 8 (v1) vs 12 (v2); Standard 218 tools (v1) vs 220+ (v2); Figure 3 L1/L2/L3 shares v1 24.0/51.2/24.8 vs v2 31.9/45.4/22.7; time-sensitive 20.0% (v1) vs 14.2% (v2); annotator tool Trae (v1) vs Cursor (v2); Oracle "MCPs" (v1) vs "tools" (v2); Max-Scale context 140k only (v1 abstract) vs 147k (v2 abstract); a Retrieve section and a judge appendix added in v2; v1 Table 4 was dialogue length, v2 Table 4 is Retrieve | [O] The tasks' level mix and time-sensitivity share differ, so the task set or its labels changed between versions | PARTIAL |

What the texts say about the cause of the shift. [U] Neither v1 nor v2 states why the Claude-4-Sonnet scores changed; v2 contains no mention of an earlier version, a re-run, a re-scoring or a change of judge (searched v2 for revis, updated, re-run, rerun, re-evaluat, re-scor, previous/earlier version: only DOI strings matched). Candidate factors that the texts show as different (judge, task-level mix, tool count, Oracle definition, model set) are listed above; the texts do not attribute the shift to any of them. [O] The judge alone (Table 8) moves the Standard score by about 1 point, which is smaller than the Oracle (+4.5) and Max-Scale (-13.6) shifts, but Table 8 does not cover those modes, so the judge's contribution to those two shifts cannot be determined from the texts. 

Verdict S40-S41: ANSWERED for the numbers (with ragged-layout caveat resolved by arithmetic) and for the Table 4 copied cells (Claude = Qwen3-235B-2507 cells 44.8 / 53.2; Gemini not in Table 4); the cause of the shift is NOT FOUND IN THESE TEXTS.

## S42 (remaining): what else the texts say that bears on reliance

| Row | Source and lines | Passage | Limits | Relevance |
|---|---|---|---|---|
| Native vs prompt-based function calling in Standard | v2:725-747; Table 3 | Claude-4-Sonnet native 62.36 vs prompt-based 15.10 in Standard; "a substantial mismatch between the function-calling templates in our prompt and those from the model's original training ... hallucination, exceeding 70%" | The prompt-based method is the arm used for GPT-4o, GPT-5, Kimi (Standard) and Gemini (Max-Scale), so those cells mix model and delivery mechanism (v2:561-562) | PARTIAL |
| Max-Scale decline | v2:640-642 | "For those evaluable at Max-Scale, performance further decreases from Standard to Max-Scale" | Only Claude (62.4 to 44.2), Qwen3-235B-2507 (53.2 to 31.6), Gemini (45.3 to 31.4*) | DIRECT |
| Benchmark does not test retrieval first | v2:299-307 | design choice: "A retriever trained on existing patterns might inadvertently hinder this crucial exploratory potential" (author's rationale, not a result) | Stated hypothesis, not tested except in 4.3 | PARTIAL |
| Dialogue-length analysis | v1 only (EXT-0204 region, v1 Table 4) | v1 had dialogue lengths per level; not present in the v2 text | Out of v2 | NOT RELEVANT |

Verdict S42 (remaining): PARTLY (the Standard/Max-Scale decline and the delivery-mechanism confound are in the texts; no token-per-task or cost figures anywhere in v1 or v2).

## Statements for the lead
- [F] The v2 Table 4 Claude cells (44.8 / 53.2) are the same as the Qwen3-235B-2507 cells in Tables 2 and 4, and differ from Claude's Table 2 and Table 3 values (62.3 / 62.4).
- [F] v2 4.3 claims retrieve mode is lower than both Oracle and Standard; the GPT-5 row (45.0 vs Standard 23.4*) does not fit that sentence.
- [U] Cause of v1-to-v2 shift is not given in either text.
- [O] Wording check on the lead's list: "57.81 / 61.01 / 57.77" are Oracle / Standard / Max-Scale in the v1 table by cell arithmetic, but the v1 prose uses 57.77 as the Oracle starting value, so "57.81 (Oracle) vs 57.77 (Max-Scale)" is a v1 internal inconsistency, not only a version difference. The "Claude / Gemini Oracle and Standard identical" idea is not what the text shows: the identical pairs are Claude vs Qwen3-235B-2507 in Table 4, and Gemini Max-Scale vs GPT-4o Standard in Table 2 (the latter possibly extraction artefact).
