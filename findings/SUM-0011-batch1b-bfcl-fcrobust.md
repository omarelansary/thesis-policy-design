---
id: FND-0009
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-99
evidence: ["EXT-0116", "EXT-0117", "EXT-0119", "EXT-0121", "EXT-0125", "EXT-0128", "EXT-0146", "EXT-0147"]
---

# Batch 1b: BFCL (r3-bfcl) and fcrobust (r3-fcrobust)

Labels: [F] fact in source, [O] observation, [I] interpretation, [U] unknown. Quotes are verbatim from the EXT files; source line numbers are lines of the stored text (EXT front matter gives line_start). Two extra reads beyond the six listed (EXT-0146, EXT-0147) were used for C-E02/E20; 8 of 9 permitted extractions in total.

Sources: r3-bfcl = Patil et al., ICML 2025 (PMLR v267 patil25a PDF), retrieved 2026-10-11, 1347 stored lines. r3-fcrobust = arXiv 2504.00914v1, retrieved 2026-10-11, 411 stored lines.

## Row C-S08/BFCLDEF

Current ledger wording: irrelevance = no provided function is relevant and the correct behaviour is to make no call; relevance = a relevant function exists and the model must call it.

Verdict: **PARTLY** (irrelevance and relevance: paper wording is shorter and differs in one respect; multi-turn categories: ANSWERED at the level of Section 3.3).

Quotes:
- [F] EXT-0116 (r3-bfcl 3.1, source lines 134-135): "Irrelevance refers to cases where tools are available but not invoked. Detailed definitions are provided in Appendix C."
- [F] EXT-0121 (Appendix C, source lines 954-958): "Relevance (R): At least one function call is expected. |F | ≥ 1, |fˆ(P )| ≥ 1 (7)" and "Irrelevance (I): Single or multiple available tools, but no function invocation is expected. |F | ≥ 1, fˆ(P ) = ∅ (8)".
- [F] EXT-0119 (Appendix E, source lines 889-891 and 903-906; construction of irrelevance entries): "Function Parameter Removal: ... the model was expected to either ask a follow-up question to clarify the missing information or return an error message instead of making a function call (which would be considered a hallucination). This will be used in the irrelevance category." and "Function Removal: ... The model was expected to either ask for more information on the missing function or produce an error indicating the absence of a relevant function for the query. This will be used in the irrelevance category."
- [F] EXT-0117 (3.3 Multi-turn, source lines 187-198): "It is divided into four categories: Base category covers the basic multi-turn user queries asking everyday tasks and providing all necessary information. Missing Parameters tests the model's ability to recognize when critical parameter information is missing from the user request and cannot be inferred from the system. Missing Functions tests the model to identify when no available function can fulfill the user request. Long Context challenges the model's ability to maintain accuracy in multi-turn long context queries or function call results. Detailed definitions are provided in Appendix D."

What the passages do NOT show:
- [O] The paper's relevance definition says only that "at least one function call is expected"; the words "a relevant function exists" are not in the quoted text (it is implied by "tools are available" being expected to be called, but is not stated).
- [O] The paper's irrelevance definition says "no function invocation is expected"; it does not say "no provided function is relevant". Its construction text (EXT-0119) shows irrelevance entries are also built by removing parameter information from the prompt while keeping the matching function in the list (a relevant function exists but the call is not expected). The ledger sentence "irrelevance = no provided function is relevant" therefore covers only the Function Removal construction, not the Parameter Removal one. This is a difference from the current wording.
- [U] Appendix D (multi-turn formal definitions, begins at EXT-0121 end, source ~line 969) beyond the heading was not read. Section 4's definition of the "Hallucination Measure" (how irrelevance/relevance accuracy is scored) was not read.

Limits: paper text, ICML 2025 version; the prose is the authors' definition, not a vendor claim. Equations (7)-(8) are rendered from a PDF text layer.

[I] effect on ledger row: the stored paper supports "irrelevance = tools available, no call expected" and "relevance = at least one call expected"; the "no function is relevant" gloss matches one of the two construction methods only.

## Row C-E02/E20

Current ledger wording: "BFCL ICML 2025 paper seen only as a snippet."

Verdict: **ANSWERED** for the existence of full text and the per-model numbers; **CANNOT DETERMINE** for total page count from the pages read (see below).

- [F] The stored text is 1347 lines with page markers; EXT-0146 shows "=== [page 6] ===" with the title "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models" and "Table 1: Evaluating different LLMs on BFCL. The categories are defined in Section 4". EXT-0147 (source lines 1320-1347, end of stored text) shows appendices up to "J. Format Instruction Prompt for Agentic Task" and a final page number "22". EXT-0121 shows Appendix C and D; EXT-0119 shows Appendix E content; EXT-0147 shows Appendix I and J.
- [O] So the stored text is not a snippet: it runs from the body through at least Appendix J, last visible page number 22. I did not read whether reference pages lie between the body and appendices (unread ranges), and the number "22" is the footer of the last stored page, not a statement by the source of total pages.
- [F] Table 1 header (EXT-0146, source lines 303-309): "Model Overall Acc Single Turn Crowd Sourced Hallucination Measure Multi Turn Agentic" with sub-columns "AST Execute", "Simple Multiple Parallel Parallel Multiple" repeated, and "Irrelevance Relevance Base Miss Func Miss Param Long Context Web Search Memory SQL".
- [F] Per-model Irrelevance and Relevance numbers are in the text layer (EXT-0146). Table 1 rows as read (the last nine numbers of each row, mapped to Irrelevance, Relevance, Base, Miss Func, Miss Param, Long Context, Web Search, Memory, SQL; mapping is by position and row value counts are consistent at 21 after Overall for the rows I counted, but the layout is ragged and unaligned for the header):

| Model (as printed) | Irrelevance | Relevance |
|---|---|---|
| gpt-4o-2024-11-20 (Prompt) | 83.8 | 83.3 |
| gpt-4o-2024-11-20 (FC) | 83.1 | 83.3 |
| GPT-4-turbo-2024-04-09 (FC) | 83.8 | 72.2 |
| GPT-4o-mini-2024-07-18 (FC) | 74.7 | 83.3 |
| o1-2024-12-17 (Prompt) | 87.8 | 72.2 |
| Qwen2.5-72B-Instruct (Prompt) | 72.8 | 100.0 |
| Gemini-2.0-Flash-Exp (Prompt) | 86.4 | 77.8 |
| ToolACE-2-8B (FC) | 90.1 | 72.2 |
| Amazon-Nova-Pro-v1:0 (FC) | 71.0 | 77.8 |
| Qwen2.5-32B-Instruct (FC) | 81.9 | 64.7 |
| Gemini-2.0-Flash-Exp (FC) | 91.5 | 55.6 |
| BitAgent-8B | 82.4 | 83.3 |
| GPT-4o-mini-2024-07-18 (Prompt) | 80.7 | 83.3 |
| Claude-3.5-Sonnet-20241022 (FC) | 74.0 | 77.8 |
| o1-mini-2024-09-12 (Prompt) | 89.6 | 61.1 |

(15 rows read, lines to ~source 340; the table continues beyond the extract; Irrelevance/Relevance as a percentage is assumed from the header, the unit is not stated in the extract.)

What the passages do NOT show: the table's rows beyond line 340, other tables, whether per-model numbers elsewhere differ (e.g. later leaderboard versions); how Irrelevance/Relevance are scored (Section 4 unread). [O] In some rows (e.g. gpt-4o FC, Gemini FC) the printed spacing is shifted ("62.5 6.0 37.5"), so a column assignment by position is an inference, not printed alignment. [I] effect on ledger row: the "snippet only" wording is contradicted for the stored text; the stored text is the full paper including Table 1 with irrelevance and relevance columns for the models read.

Limits: PMLR proceedings version (patil25a), retrieved 2026-10-11; a snapshot of leaderboard numbers at paper time.

## Row C-E01/E01

Current ledger wording: "fcrobust BFCL range disputed; original table not rendered."

Verdict: **PARTLY**: the table is in the text layer but ragged (model names detached from rows); numbers below are exact as printed. **CONTRADICTS** the claim "original table not rendered" in the sense that numeric cells are present; the model-to-row mapping is uncertain.

Setup [F] (EXT-0125, source lines 158-161 and 169-178 and 196-199): "We report AST averaged over the 200 dataset examples, including three variants: (a) the original version, (b) original ("thin") toolkit + rephrased user request, (c) expanded toolkit + original user request." Measure = AST accuracy (BFCL first evaluation phase only: "we, therefore, adhere to the first evaluation phase – namely, AST"). Expanded toolkit: "The mean number of tools in the expanded toolkit is 5.6 compared to the 2.7 (seemingly unrelated) tools in the original BFCL dataset, meaning that three semantically-related functions were added on average to each one of the 200 testcases." Models listed: GPT4o-mini, o1-mini, Claude-3.5-Haiku, Claude-3.5-Sonnet, Llama3.1-70B, Llama3.3-70B, Granite3.1-8B-instruct, DeepSeek-v2.5, Qwen2.5-72B (9).

Lines 145-146 [F] (EXT-0125 lines 27-28): "tions led to a notable drop in benchmark perfor-" / "mance – we analyze and interpret this decline, and". Qualitative only; the sentence starts at the rephrasing example ("What is the humidity level in Miami,Florida in the upcoming 7 days?" rephrased as "How will the humidity levels change over the next seven days in Miami,FL?"). No number.

Line 171 [F] (EXT-0125, the 70-90% sentence in the right column; source lines 169-171; the two columns are interleaved in the text layer): "Further systematic analysis of error types distribution reveals that 70–90% of errors indeed stem from mis-match in parameter value assignment. We conclude that the majority of failures in this case can be attributed to the evaluation approach drawback rather than agents' sensitivity." The condition: errors under the rephrased-query condition (orig. toolkit + rephrased query), cause = exact-match parameter value mismatch. No model is named; the quoted text does not give the per-model breakdown.

Table 2 left (EXT-0128, source lines 217-237; printed text): columns "original | orig. toolkit reph. query | exp. toolkit orig. query"; caption (source lines 239-243): "Models' AST performance drop is evident when rephrasing the original query, and also when using the original query with extended toolokit (left); relative percent drop is specified in brackets." Rows as printed, in print order (model names are printed as a separate stacked column; the names in print order are Llama3.1-70B, Llama3.3-70B, DeepSeek-V2.5, Qwen2.5-72B, Granite3.1-8B-instruct, Claude-3.5-Haiku, Claude-3.5-Sonnet, gpt4o-mini, o1-mini; the names are interleaved with the first rows so the row-to-name mapping is NOT recoverable with certainty):

| Row (print order) | original | orig. toolkit + rephrased query | expanded toolkit + original query |
|---|---|---|---|
| 1 | 0.965 | 0.825 (-15%) | 0.925 (-4%) |
| 2 | 0.945 | 0.785 (-17%) | 0.905 (-4%) |
| 3 | 0.965 | 0.835 (-14%) | 0.950 (-2%) |
| 4 | 0.975 | 0.850 (-13%) | 0.965 (-1%) |
| 5 | 0.945 | 0.770 (-19%) | 0.870 (-8%) |
| 6 | 0.925 | 0.765 (-11%) | 0.870 (-2%) |
| 7 | 0.915 | 0.845 ( -8%) | 0.890 (-3%) |
| 8 | 0.925 | 0.765 (-17%) | 0.870 (-6%) |
| 9 | 0.905 | 0.770 (-15%) | 0.885 (-2%) |

Nine rows, nine named models. Error-analysis columns (right half, "exp. toolkit + orig. query: error analysis (%)": wrong syntax, wrong function, wrong num of functions, wrong param. assignment) per row, same order: 1: 0.00 0.45 0.10 0.45; 2: 0.00 0.23 0.46 0.31; 3: 0.00 0.56 0.00 0.44; 4: 0.00 0.29 0.00 0.71; 5: 0.09 0.50 0.18 0.23; 6: 0.00 0.44 0.00 0.56; 7: 0.00 0.29 0.00 0.71; 8: 0.26 0.42 0.00 0.32; 9: 0.33 0.27 0.00 0.43.

Observations:
- [O] Printed relative drops: rephrased query -8% to -19% (rows 7 and 5); expanded toolkit -1% to -8% (rows 4 and 5). Absolute AST: original 0.905-0.975; rephrased 0.765-0.850; expanded 0.870-0.965.
- [O] My recomputation from the printed absolute values: row 6 gives (0.765-0.925)/0.925 = -17.3% (printed -11%) and (0.870-0.925)/0.925 = -5.9% (printed -2%); rows 6 and 8 have identical absolute values (0.925, 0.765, 0.870) but printed different percentages (-11%/-2% vs -17%/-6%). The other seven rows recompute to the printed percentages within rounding. Either the row 6 percentages or its absolute values are misprinted or misaligned in the text layer; this cannot be resolved from the stored text. Neither alternative moves the overall printed range.
- [F] Caption says "The best result in a column (the lowest performance drop) is boldfaced." Boldface is not visible in the text layer.
- [F] The paper's text "(Table 2, left)": "expanding an agent's toolkit with a set of related functions caused performance degradation across the board".
- [U] Which of the nine rows corresponds to which model: not determinable here. Which BFCL category the 200 testcases come from: not stated in the lines read (the paper's abstract and Section 2.1, source lines 1-139, were not read). Whether the range quoted elsewhere in the ledger (the "dispute") matches -8 to -19% and -1 to -8%: the dispute itself is not in this text.
- [O] The paper states, for the rephrase condition, that the drop is mostly attributable to the exact-match evaluation ("the majority of failures in this case can be attributed to the evaluation approach drawback rather than agents' sensitivity"); the expanded-toolkit condition's errors are described as "wrong function selected, wrong number of functions generated (typically two instead of one), wrong parameter assignment ... parameter hallucinations".

Limits: arXiv v1 preprint, single version stored, not peer-reviewed in this form; 200 testcases; AST phase only; table ragged. [I] effect on ledger row: the stored text gives the figures as printed per condition (no single range is needed); the original table is partly rendered, with one internal inconsistency (row 6) that should be noted.

## Not read / not run
- r3-bfcl: Section 4 (metric definitions, Hallucination Measure), Appendix D beyond its heading, Appendix C beyond Relevance/Irrelevance, the remaining rows of Table 1 beyond ~line 340, references.
- r3-fcrobust: lines 1-139 (abstract, Section 2.1), lines 246-411 (rest of results, Section 3.3 mitigation, appendices).
