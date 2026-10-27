---
id: SUM-0053
type: summary
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-28
thread: T-20261027-122
evidence_lines: [evidence/literature-20261019/v5-xp-arxiv-2410.14594.txt, evidence/literature-20261019/v5-xp-arxiv-2401.06201.txt, evidence/literature-20261019/v5-xp-arxiv-2409.02141.txt, evidence/literature-20261019/lit-closedworld-2609.19425.txt, evidence/literature-20261019/v5-xp-arxiv-2509.26553.txt, evidence/literature-20261019/v5-xp-arxiv-2607.10059.txt, evidence/literature-20261019/v5-xp-gorilla-bfcl-v2-live.txt]
---

# SUM-0053: check of scout claims Z3-Z9 (batch Z, gate and retrieval)

SUM, unverified. Source: `design/package-v5/inputs/claims-batch-Z-gate-retrieval-20261027.md`. Line numbers refer to the stored text files. A check by grep of key numbers and phrases; "absence" statements are checked only in the lines the greps returned. [F] = fact in source.

| Claim | Verdict | Lines | Quote | Note |
|---|---|---|---|---|
| Z3 Toolshed | CONFIRMED (tool-record fields, 46/56/47, trade-off) | 46-49, 308, 494, 44-46, 142-151 | "achieves 46%, 56%, and 47% absolute improvements on the ToolE single-..." ; "name, description, argument schema, and key information, hypothetical questions" ; "selection threshold (top-k), we address trade-offs" | Dataset names for 56% (multi) and 47% (Seal-Tools) not read line by line (line 754: "On the Seal-Tools dataset (single and multi-tool evaluation)"); "Recall@5" at 209. Synthetic "key topics" at 566-567. |
| Z4 EasyTool | PARTLY | 400-412, 476, 633-639, 713-720, 866, 891-902 | "2,530" / "748" / "70.43%" / "3,881" / "97.35%"; "ChatGPT + DFSDT-EASYTOOL even surpasses GPT-4 + DFSDT"; "GPT Ada" ... "76.7" | Token numbers and percentages found. 15.0 (DFSDT, line 713/741) and 52.8 (line 720) found as table cells; the 103-token figure for RestBench and the table numbers 3/4/5 were not separately located; the 45.7 and 76.7 cells are at 896 and 902 (45.7 appears with a neighbouring cell 38.8). "Generation cost not reported": not confirmed (no search hit for such a statement, which is not proof of absence). |
| Z5 Tool2Vec | CONFIRMED | 257-289, 387-389, 407-419, 450, 551-552 | "79.97" "90.19" "93.21"; "85.88" ... "93.29" ... "94.42"; "91.80" "96.00" "96.67"; "ToolRefiner uses DeBERTaV3-xsmall (22 million parameters)" | Tool vector is the average of embeddings of queries using the tool (286-289), matching "mean". Row labelling of the I1 block is by table order (Table 1 at 367-374); I did not read the row headers. No "BM25" hit in the file (grep for BM25 returned none). Latency/cost: the file does discuss latency and cost overheads of other methods (41, 153, 170), so "no latency or cost" holds only for Tool2Vec's own results, not read in full. |
| Z6 Closed-world resolution | CONFIRMED | 85, 123, 492-499, 574-576, 659-664 | "rejects any call which does not resolve to a registered tool"; "322 genuine hallucinations"; "Gating-only executed (by construction): 322/322"; "Full stack (ours) executed: 0/322"; "leaves 0.1525 of H5 executed, 61 of the 400"; "irreducible for any closed-world schema checker" | The type-checking against the signature clause was not read. "Costs not measured": not searched. |
| Z7 FuncBenchGen | CONFIRMED | 28-33, 129 | "often make syntactically valid function calls but propagate incorrect or stale argument values across steps"; "success rate from 62.5% to 81.3% for GPT-5" | The mechanism ("restating prior variable values") was not read; the quote ends before it. |
| Z8 AgentAbstain | CONFIRMED | 17, 28-29, 94-97, 104, 374-378, 916 | "263 paired tasks across 42 executable"; "59.5% paired accuracy"; "abstention capability is largely independent"; "post-hoc abstention where agents first commit irreversible actions" | 17 models at 94-95, 114. Best model is Gemini 3.1 Pro (94). Wording differs slightly: the claim quotes "abstention capability is largely independent of general task-solving ability"; line 29 continues "largely independent" and line 916 reads "largely independent of general task-solving capability" (the word is "capability", not "ability"). |
| Z9 BFCL V2 Live | CONFIRMED | 115, 138-139, 149-151 | "2,251 question-function-answer"; "882 irrelevance detection, and 18 relevance detection entries"; "none of the function choices provided are relevant to the user query and none should be invoked" | 882/2251 = 39.2% and 18/2251 = 0.8% (arithmetic mine, [O]). Line 139 lists the category counts as 258 + 1053 + 16 + 24 + 882 + 18 = 2,251. |

## Counts

- CONFIRMED: 6 (Z3, Z5, Z6, Z7, Z8, Z9)
- PARTLY: 1 (Z4)
- NOT FOUND: 0
- CONTRADICTED: 0

## Wrong or unverified scout numbers

- Z4: the RestBench 103-token figure and the "generation cost not reported" statement were not located; the 15.0 and 52.8 cells and the 2,530 / 748 / 3,881 / 70.43% / 97.35% figures were found.
- Z8: quotation uses "ability"; the file says "capability" (line 916).
- No wrong numbers found elsewhere.
