# 08. Proposed ledger changes from V5 (for the human's review; NOT applied)

Status: proposals, lead, 2026-10-22. The workbook `design/ledger/PROJECT_A_OPEN_ITEMS_LEDGER.xlsx` is **not** edited (AUTH-020 limits). On approval (Q-U31) each change is applied by AUTH-016's rules: evidence per status change, the change log, archive, CSV export. Row ids and current statuses are from `design/ledger/notes/FRONTIER-20261021.md`. "Narrow" = the row stays open with a smaller remainder.

## 1. Rows V5 can narrow or close on evidence
| Row (current status) | Proposed | Evidence | Remainder |
|---|---|---|---|
| N-6 memory of which tools exist or were discovered, across sessions (NOT LOCATED) | Narrow: personalized tool memory over small tool sets exists; per-user seeding from a large catalogue with a bill not found in a limited search; becomes a test | `03` section 5; `inputs/search-log-20261022.md`; FND-0042 | HYP-0017, `05` P1 |
| N-7 prefix layout and cross-user cache sharing; memory seeds could fragment a shared prefix (OPEN) | Narrow: resolved in design by seeding after the shared prefix through offering mechanisms | `04` V5-R06; L/v5-anthropic-midconv-sysmsg-20261022.md:27; L/v5-openai-prompt-caching-20261022.md:441 | Provider sharing scope still unstated |
| AS-07 Executor exposes connection prefixes and meta-tools (PARTLY) | Narrow: identity and catalogue read (`UsefulSoftwareCo/executor`, MIT, 4,235 stars); MCP surface not in the README | L/v5-executor-readme-20261022.md:5-7, :123; L/v5-gh-api-executor-20261022.dat | Read Executor's MCP docs (`05` P0) |
| C-D08/EXEC identity of Executor and whether it must be an arm (PARTLY) | Narrow: identified as above; required as a baseline (REQ-O02-06) | same | Version pin; Q-J33 |
| AS-09 the partial-information idea comes from another party's documentation (PARTLY) | Narrow: vendors ship partial-information tiers (OpenAI deferred function shows name and description, schema deferred; namespaces show only their own description) | L/v5-openai-tool-search-20261022.md:22 | The supervisor names his source (Q-J28) |
| AS-13 filtering 100 to 60 and names-only tiers keep accuracy (NOT LOCATED) | Narrow: the tier form exists in vendor products; its accuracy effect is not reported | same; `02` section (b) | A graded-exposure arm if the loop needs it |
| AS-15 explicit cache additions at negligible cost for the whole conversation (PARTLY) | Narrow: desk arithmetic done (consistent per request against re-sending; cost grows with every request and recurs after gaps against not adding) | `calc/memory_seed.stdout.txt` part 2; DPR-0006 section 3 | Billing probe (C-X07, `05` P0) |
| C-S04 warm-hit arithmetic omits TTL, concurrency, growing suffix, session gaps (PARTLY) | Narrow: TTL and gap cost now in D-01 and D-02 with DPR-0006 | `calc/regime_bill.py`, `calc/memory_seed.py` | Concurrency; our gap distribution |
| C-S02/INVERSION fewer exposed tokens can cost more in billed terms (PARTLY) | Narrow: D-01 locates the regime (below a break-even of about 10-230 tools, depending on searches per session, definition length and whether the core caches) | `calc/regime_bill.stdout.txt`; L/v5-synthorai-mcp-overhead-20261022.txt:176 | `05` P5 reading |
| C-S03/DEFUSAGE deferred or withdrawn definitions in usage and bill (PARTLY) | Narrow: OpenAI individually deferred functions still send name and description | L/v5-openai-tool-search-20261022.md:22 | Gemini; the university API (HYP-0020) |
| C-S11/TRIG system trigger for a missing tool (OPEN) | Defer with trigger: dropped from V5-R's default (no source supports it); reopen if `05` P3 shows models rarely search | `04` V5-R07; `03` section 7 | — |
| C-S11/CASCADE does a multi-stage cascade dominate the best single stage (OPEN) | Narrow: hierarchical retrieval exists (AnyTool); no multi-stage run-time policy measured on the bill was found in a limited search; Copilot's shipped two levels and its stated cache-miss cost per group expansion | EXT-0228; `03` section 4 | — |
| C-E02/E31 ScaleMCP, MemTool, Toolshed, Manus, Spring AI, langgraph-bigtool follow-up unclear (DEFERRED) | Close in part: ScaleMCP, MemTool, Manus, langgraph-bigtool stored and checked; Spring AI and Toolshed remain unread | FND-0040..0042; search log | Spring AI (origin `r4-spring-tool-search-blog`), Toolshed |
| C-E02/E25 Claude Code deferral bug reports known by title only (PARTLY) | Narrow: one cache-bust issue stored with its community data; Claude Code's own tool-search docs stored | L/v5-ccissue-92033-cachebust-20261022.txt:180-190; L/v5-claudecode-mcp-20261022.md:1441 | Other issues are mirrors only |
| C-D08/ARMS-CACHE new arm candidates from the cache and memory addendum (OPEN) | Narrow: arms fixed for the loop in `05` P1-P2 | `05` section 1 | Loop results |
| C-S08/UNINSTR uninstructed search initiation (PARTLY) | Unchanged in substance; now HYP-0019 with a test design | `05` P3 | — |
| C-X07 billing and cache probe (PARTLY) | Narrow: split into P0 (API fields) and P5 (regime reading) | `05` section 1 | — |

## 2. New rows proposed
| Row | Title | Closes by |
|---|---|---|
| N-31 | Does the university API report cache writes and reads and apply cache prices (HYP-0020)? | `05` P0 reading |
| N-32 | Offering fewer tools at a fixed cached prefix: accuracy effect (HYP-0018) | `05` P2 |
| N-33 | Regime switch by D-01: does the first-order arithmetic hold on our model and catalogue? | `05` P5 |
| N-34 | June exposé ideas to be tested against V5's result once V5 is accepted | Human supplies the exposé (Q-U32) |
| N-35 | The lead's `git push` (and at times `git commit`) is refused by the auto-mode classifier even with allow rules; the human pushes | Operational; accepted limitation or a settings change by the human |
| N-36 | Steward, scout and blind outputs in V5 are model work checked by model work; the human has not spot-checked any V5 row | Human spot-check of a sample of `03` rows |

## 3. New questions proposed
Supervisor: Q-J31, Q-J32, Q-J33 (`05` section 3). Human: Q-U28 to Q-U32 (`05` section 4).

## 4. Applied (2026-10-22, the human's acceptance Q-U31, INT-T-006 line 8)
Applied by `design/package-v5/tools/apply_ledger_20261022.py` (in place; Change log rows appended above the append-only note) and exported with `design/ledger/export_ledger.py`: 17 rows changed as in section 1, updated with the P0 part-1 reading of the university API (vendor deferral and offering mechanisms not available there); 6 new rows N-31..N-36 (N-31 starts PARTLY ANSWERED from the status page); 9 questions Q-J31..Q-J33 and Q-U28..Q-U33 with the answers of INT-T-006 (Q-J31, Q-J32 answered by the student on the supervisor's behalf; Q-J33 reworded and open; Q-U30 explained and open; Q-U33 new); 7 links; 95 Change log rows. The Overview sheet's formulas need a recalculation in a spreadsheet program (the export does not need it). The frontier page was not regenerated.
- Addendum 2026-10-25 (INT-T-008): Q-U30 answered (A headline, B beside; N-30 note); Q-U32 carried out and N-34 closed by evidence (`09`) and moved to Archive; Q-U33 deferred by the human (N-31 next action); 11 Change log rows; formulas re-indexed and checked for all ledger rows; export regenerated. Applied by `design/package-v5/tools/apply_ledger_20261025.py`.
- Addendum 2026-10-22 (INT-T-007): Q-J33 answered (REQ-J22-04); C-D08/EXEC closed by decision and AS-07 closed by evidence (Executor's MCP documentation), both moved to Archive with formulas of the rows below re-indexed and checked; 9 + 2 Change log rows; export regenerated.
