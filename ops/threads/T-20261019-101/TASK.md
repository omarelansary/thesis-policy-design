# Thread T-20261019-101: TASK (lead; AUTH-016, ledger batch 3: independent reading of three rendered PDF pages)

- Authorization: **AUTH-016**. The lead rendered three PDF pages to images (stored with hashes in `evidence/literature-20261019/pages/`, see `INDEX.md`) and read them; this task is an **independent second reading** of the same images by one steward. No web access, no design proposals.
- Do **not** create a findings file and do not write under `ops/threads/` (the guard blocks it); do not use `origin_extract.py`. Use the `Read` tool on the image files below (it displays images) and answer in your final message only.
- Read each image, transcribe exactly what is printed (including any oddity), do the arithmetic yourself and show it. Do not look at, or ask for, the lead's own transcription. Label [F] printed, [O] your observation, [I] interpretation, [U] unreadable or unknown.

## Image 1: `evidence/literature-20261019/pages/fcrobust-2504.00914v1-p5.png` (page 5 of fcrobust, Table 2)
Transcribe Table 2 completely: for each of the nine model rows give `original`, `orig. toolkit reph. query` (value and the printed percentage in brackets) and `exp. toolkit orig. query` (value and printed percentage), and the four error-analysis columns. Then recompute each relative drop as (value / original - 1) x 100 and list every row where a printed percentage differs from your recomputation by more than 1 percentage point. State which rows have identical absolute values.

## Image 2: `evidence/literature-20261019/pages/scaffold-2608.08654v1-p14.png` (page 14 of the scaffolding paper, section 4.2)
Transcribe Table 4 (arm, runs, tokens, cost at list price, cost cached-discounted) and quote verbatim the paragraph that starts "The two arms are close in cost" and the sentence(s) that explain why the comparison is uninformative. Compute the MCP-to-command-line ratio for tokens, list-price cost and discounted cost. Say whether the paragraph's wording ("twice the tokens", "about ten per cent more at list price", "half as much again once cached input is discounted") matches your ratios. Also transcribe the Figure 4 labels (medians, schemas per request, number of completed runs per bar).

## Image 3: `evidence/literature-20261019/pages/mcpverse-2508.16260v2-p5.png` (page 5 of MCPVerse v2, section 3.2 and Figure 2)
Transcribe the printed task total, the printed tool count, and every percentage in the three pie charts (a) task types, (b) complexity levels, (c) time sensitivity. For each percentage compute the implied task count if the total is 250 and say whether it is a whole number. Report whether the number 311 or any other task total appears anywhere on the page.

Final answer: the three transcriptions and calculations, plus a one-line statement per image of anything unreadable.
