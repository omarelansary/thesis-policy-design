# B-2: evidence-to-claim audit of availability, examination and coverage statements

- Date (UTC): 2026-10-15. Coordinator: Sonnet 5.5. Authority: D11 (user, 2026-10-15). Unit ticket COORD-S4H-AUDIT-20261015-01. Corpus snapshot: repository HEAD bdc41f0 (B-1 texts included). Nothing in the existing records was modified.
- Labels: **F** fact (stored record or log, with file and line), **I** interpretation, **Inf** inference, **U** uncertainty. "Claim date" is the git-blame commit time of the line carrying the current wording; for documents revised in place the earlier wording is in git history and was not reconstructed line by line.
- What this is not: not human validation (no human has reviewed it); not a re-search (zero web searches in B-2); not a re-derivation of any scientific result; no candidate selection, no new candidate, no policy design.
- Artifacts: `B2-claim-to-source-audit-table.csv` (all 1,358 extracted claims), `B2-searchlog-note-claims.csv` (66 search-log note claims), `B2-consequential-claims.md` (148 adjudicated claims in 30 subject blocks), `B2-evidence-packet.md` (exact passages for human judgment), `B2-corpus-inventory.md`, `B1-source-version-report.md`, `data/` (machine outputs), `tools/` (the scripts that produced them).

## 1. Method (deterministic where possible)

1. **Inventory** (`tools/build_inventory.py`): 239 stored source texts (manifest URL, arXiv id and version, capture time, pages, characters, warnings), 672 candidate-log records with `logged_at_utc` and verification level, 506 consolidated groups, 352 search-log rows. SHA-256 of every stored text and source file recomputed against its manifest: **0 mismatches** (37 manifests carry extraction warnings). A timestamped timeline per subject (`tools/lookup.py`) lets each claim be matched to the corpus **as of its claim time**.
2. **Extraction** (`tools/extract_claims.py`): regex sweep with synonyms over 153 original stage, candidate, decision and audit/handoff files: not found / not located / absent / unavailable; not in the corpus / not fetched / not stored / not logged; abstract-, snippet-, metadata-level / not read / unverified; no study / not tested / not reported / residual gap. **1,358 fragments** kept with exact quotation, file, line, nearest heading, blame time and file-creation time. Search-log note fields scanned separately (66).
3. **Partition** (`tools/partition_claims.py`): 54 process/scope/rule fragments (not prior-work claims); 64 per-record depth annotations (checked mechanically against the record's own field: 61 match, 3 explained mismatches); the rest read.
4. **Reading**: I read all 367 fragments from stage-reports, candidate-questions and decisions, and all 85 "not in corpus" and 186 "not found" fragments in audit records. Subjects were then checked against the timeline and the stored text (E-packet for exact passages).
5. **Near-neighbour screen** (`tools/citation_map.py`, `tools/scan.py`): for each stored text, whether it is named in (S) the strict candidate chain (candidate-questions, S4E/S4F/S4G, STEP1), (B) any stage report/candidate/decision, (A) audits only. 95 stored texts are not named in the strict chain; 37 not in any report. All 95 abstracts were read (`data/strict_uncited_abstracts.txt`); about twelve with possible bearing on a C1-C6 gap statement were read further. Co-occurrence scans of the stored texts were used to test the wording of the C1-C6 "not found" statements.
6. **Classification** against the contemporaneous record: SUPPORTED, CONTRADICTED, AMBIGUOUS (inadequately specified), UNDETERMINABLE (cannot be decided from local evidence; this includes every statement of the form "no prior work exists").

## 2. Results

| Tier | Meaning | Rows | Result |
|---|---|---|---|
| T0 | process/scope/rule wording | 54 | not prior-work claims |
| T1 | individually adjudicated against timeline and stored text | 148 (in 30 subject blocks) | SUPPORTED 119 · AMBIGUOUS 19 · CONTRADICTED 2 · UNDETERMINABLE 8 |
| T2 | other statements in governing records (definitional caveats, reading-depth declarations, one-paper content statements) | 247 | classified by rule; aggregate depth distribution verified (see below) |
| T3 | audit/critic/worker statements | 910 | 78 SUPPORTED (record-level and sid-level depth checks), 2 AMBIGUOUS, 830 inventoried (UNDETERMINABLE as stated; adopted statements are adjudicated at the governing location) |

Mechanical confirmations (F): the Stage 2 draft's depth distribution of the 208 mechanism-family groups (fulltext 47, official-docs 27, readme 1, abstract 74, metadata 11, snippet 48) reproduces exactly from the L2 table; 669 candidate rows existed by 2026-10-12T19:52 and 506 groups; 223 groups carry only "maybe"; 21 vehicle files and 24 Stage 4 texts are stored as stated; all hashes match. "42 contested groups" equals the L2 population class B; groups with a decision conflict number 51 (the term is defined by class, not by conflict).

## 3. Discrepancies, traced forward

Only discrepancies with a plausible effect on a scientific assertion are listed; the others are in the tables. Causes are not asserted where the original record does not state one.

| # | Statement (location, written) | Contemporaneous corpus | Class | Forward trace into current C1-C6 records | Effect |
|---|---|---|---|---|---|
| D-1 | Shi et al. "was never in the corpus" (STAGE3_FINAL_REPORT:21, 10-12 23:24) | R2-C104 abstract-level include, 10-11 14:21 | CONTRADICTED | Full text read in Stage 3; D-SEC not a candidate | none (wording) |
| D-2 | Five abstract-level pivotal sources incl. S2-0218 (D3-stage3:11, 10-12 20:15) | S2-0218 stored full text 10-12 19:25; reviewed in A46 | CONTRADICTED for one of five | Stage 2 final report already says "full text now read" | none |
| D-3 | "Leads not fetched … 2607.02577" (S4F-UA:46, 10-15 10:58) | Same arXiv id stored since 10-11 12:18 as a different title; S4F-Q011 itself notes it as stored | AMBIGUOUS (id vs title cannot be reconciled locally) | The text (18.5% evaluator disagreement) is already used for C5 | none |
| D-4 | C2 nearest-prior-art list omits FitText (S4D:92, 10-14 21:41); S4F-Q005 note says FitText was "previously read at abstract level" | FitText full text stored 10-11 14:18; record R1-C190 fulltext | AMBIGUOUS (the gap statement itself says no search was aimed at it); note CONTRADICTED | Corrected 10-15 in S4F-PA v2, S4F-UA, S4G (FitText is named nearest prior art, confounds stated) | corrected |
| D-5 | "C3's lead 2605.00136 could not be located; not used" (4c N12 ii, 10-13) | R3-C062 abstract-level since 10-11 12:24; backend title search failed (S4C-Q014) | AMBIGUOUS | Stored and used by S4F (NoopTool presence control added to C2 identifiability) | corrected |
| D-6 | Stage 4 "no calibration of offline recall against outcome … found" (10-13 06:48) | DynamicMCPBench abstract-level record since 10-11; full text 10-13 12:00 | AMBIGUOUS (near-neighbour logged, content unread) | 4c N2 / S4D use it fully | corrected |
| D-7 | Critic-identified omissions of stored near-neighbours (S4B-C2 10-13 07:55; S4D-C1 10-14; S4E-C1 10-14 22:20: PlanBench-XL, ToolMenuBench note, TheMCPCompany, Appendix S, BoR) | all stored before the critic reports | SUPPORTED (the critics were right) | Each dispositioned in the next record (S4B-V4/V6, S4D-V1, S4E-V1); BoR and Appendix S are in the S4E report and S4F-UA | corrected |
| D-8 | Executor as "supervisor-named baseline" | Stage 2/3: "candidate match; referent unresolved" | label drift (not an availability claim; B1/X2) | Open question for the supervisor (S4G §9 item 5) | scope wording of C3 |
| D-9 | **Not corrected:** stored texts not named in the strict chain that bear on near-miss or prior-art lists: Toollery (single-step full-library vs top-10, AST accuracy and billed input cost under natural / cache-suppressed replay; text L330-337, L736-790); Prompt-Induced Waste (value of an efficiency intervention changes with the harness); Notation Matters (token-optimised formats cost up to ~14 pp accuracy for up to 27% fewer tokens in agentic loops); Tool-Schema Compression/TSCG; CacheRouter (feasibility prototype, no comparison arm; already discussed in STAGE4_PRIOR_ART_COMPARISON §5) | stored 10-11 to 10-13, before S4D v2 | not contradicting any gap statement; near-miss / prior-art lists incomplete | C3 ("head-to-head … near-misses exist"), C5 (partial prior art in other domains), C6 ("three uneven sources") | novelty wording, low (human judgment: E5, E7) |
| D-10 | Bounded negatives ("no independent evaluation of provider tool search", "no multi-user definition share", "token-matched count control not found" …) | the corpus screen found no stored text that closes any of them | SUPPORTED within the corpus; UNDETERMINABLE as statements about the literature | stated as bounded in every governing record | none |

## 4. Impact on the latest C1-C6 assessments

| Candidate | Statement checked (S4G §4 / S4F) | Result | Residual |
|---|---|---|---|
| C1 | manipulated absence × presence factorial not found (3 queries); "no logged query was aimed at it" (S4D) | Corpus screen finds the cited near-neighbours (ToolMATH, CAM-DF, SLCA-GRPO, TheMCPCompany, ToolMenuBench, App. S) and nothing that closes it; SimpleToolHallu was in the corpus as an abstract-level record under another title | none |
| C2 | core effect partly covered by FitText; distinctive elements not found | FitText omission at S4D v2 was corrected on 10-15; remaining wording correct. The S4F-Q005 depth note is a log misstatement | none |
| C3 | head-to-head with token categories not found; near-misses exist | Literal statement stands for trajectory level; near-miss list omits Toollery (single-step; cost under cache regimes) | optional note (D-9) |
| C4 | token-matched count control not found after repeated searches | Stands; S4G's C4 line lists App. S but not BoR (BoR is in the S4E report and S4F-UA); Tool-Use Tax's presence control concerns a different construct | none |
| C5 | exposure-specific stability not found; partial prior art in other domains | Stands; additional other-domain instances are stored and uncited (Prompt-Induced Waste, Toollery replay, CacheRouter) | optional note (D-9) |
| C6 | component ablation in three uneven sources; controlled deterministic held-out version not found | "Three" is a selection; other measured token-saving components are stored (Notation Matters, TSCG); the absence claim stands | optional note (D-9) |
| Vehicle / feasibility | counts of stored vehicle files, "cr_recall.py … not stored" | supported | none |

No contemporaneous record contradicts a **gap** statement for C1-C6. What the audit finds are (i) wording errors about availability that have no downstream scientific consequence (D-1, D-2, D-3), (ii) omissions from prior-art lists that were detected by independent critics and corrected in the next record (D-4, D-6, D-7), and (iii) an uncorrected remainder of uncited near-neighbours that affect only how complete the near-miss lists are (D-9).

On cause: the chronology shows that independent critics repeatedly flagged omissions of stored items (S4B-C2 L113-115 attribute the 4b omissions to the workers not looking at the stored corpus) and that each was addressed in the following record. This audit does not establish a single cause across stages and does not need one for the decision below.

## 5. Final decision

**Overall status: outcome 2: material discrepancies exist, and their consequences are already corrected in the governing records, with the following exceptions.**

- **Exception A (outcome 4 for absence claims):** no statement of the form "no prior work exists / no study found" can be confirmed or refuted from local evidence. The corpus screen is consistent with each C1-C6 gap statement as written; that is all it can show.
- **Exception B (not corrected; for human judgment, not reconsideration):** D-9. These stored texts are not named in the strict governing chain. None contradicts a gap statement. They bear on the completeness of the nearest-prior-art lists for C3, C5 and C6. I do not find that any candidate assessment **requires** targeted reconsideration; whether to add a dated note listing these near-misses is a human decision (evidence packet E5, E7).
- **Exception C (record hygiene, no scientific consequence):** D-1, D-2, D-3 and the S4F-Q005 depth note are wording errors that remain in the original records. Nothing was edited, as instructed.

Outcome 3 (targeted reconsideration of a current assertion) is **not** indicated by this audit. If a human reader of the evidence packet disagrees about E5 or E7, the assertions in question would be exactly: C3's "near-misses exist" list, C5's "partial prior art in other domains" list, and C6's "three uneven sources" wording.

## 6. Limits of this audit

1. **Extraction recall is unknown.** Regex synonyms are broad, but claims phrased without those cues are missed; the set is exhaustive for the patterns used, not for all possible phrasing.
2. **Not every row is individually adjudicated.** T2 (247) and T3 (910) are classified by rule or inventoried; adopted statements are adjudicated at their governing location. The 830 T3 "UNDETERMINABLE" rows are audit-internal statements that I did not reproduce against the corpus one by one.
3. **Near-neighbour reading is partial.** Of 95 strict-uncited texts all abstracts were read, about twelve more deeply (CacheRouter, Prompt-Induced Waste, Notation Matters, TSCG, StackOne, Toollery, CIPO/HyperTool at abstract level, others). `r2-ce-mcp` (code-execution design choices), Dynamic ReAct, Toolshed and a few others were not read beyond their abstracts, so I make no statement on whether they bear on C3.
4. **Alias matching is heuristic** (stored id, arXiv id, id segments, title prefix); a name used in a report in a form I did not anticipate would show as uncited. Counts of "uncited" are upper bounds.
5. **Claim dating by git blame** gives the commit time of the current wording; for files revised in place, the earlier wording is not reconstructed.
6. **Single coordinator.** No second reader checked these classifications; the classifications are mine (a Sonnet 5.5 model). The earlier independent investigation's D1 reviewer is not a human either. No part of this is human validation.
7. **Stored texts are the corpus's own copies**; extraction layouts are garbled in places (MCPVerse tables); line numbers refer to `text.txt`.
8. **No web access in B-2**; B-1 fetched three public PDFs only.
