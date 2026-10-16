# Decision record

- Decision ID and date (UTC): D2, 2026-10-12
- Decision owner: the user
- Question to decide: how to close Stage 2 honestly and with bounded effort. The original acceptance criteria stay in force (Path A). This record settles the closure procedure, the population definitions, the reduced independent-challenge scope for this closure attempt, and the relation to Stage 3.

## Governing text (exact references)

- Gate semantics: `protocols/STAGE_GATES.md`, intro ("`PASS` means every stated acceptance condition has evidence … Never promote an inconclusive result to pass. A human may revise a plan, but the revision and reason must be recorded before work continues"), Stage 2 row, and "Minimum recovery record" ("Retrying must not weaken the acceptance condition").
- Approved acceptance criteria 1–14 and verdict mapping: `stage-reports/STAGE1_RESEARCH_BRIEF.md` §3.4 (approved in D1, G-a4, with criteria 13–14 added in rev. 2). Searching, stopping and coverage signals: §3.2. Independent challenge: §3.3.
- Operating rules: `STAGE2_WORKFLOW.md`, `protocols/STAGE2_RESEARCHER_INSTRUCTIONS.md`, `STAGE_ROUTING.md`. `CLAUDE.md` (the user decides objectives and approves final scientific claims; no silent change of a gate).
- Prior decision: `decisions/D1-stage1-gate.md`.
- Current state: `stage-reports/STAGE2_LANDSCAPE_AND_ACCEPTANCE_AUDIT-20261011.md`, `audits/A7-stage2-acceptance-gap-matrix.md`, `STAGE2_AUTOCHECKPOINT.json`.

## Independent review findings

- An independent Opus review reported a possible mismatch between the approved acceptance contract and the execution workflow. **Its text is not stored in this repository and the coordinator has not seen it**; the findings are known only through the user's summary on 2026-10-12. This record does not claim to quote it. Action for the user: if the review should be a citable evidence item, supply or save it verbatim under `audits/`.
- The five claims in the user's summary were checked by the coordinator against the governing text on 2026-10-12. Results are in "Findings" below. The coordinator did not assume the review is correct.

## Findings (coordinator verification, 2026-10-12)

1. **Criterion 1.** Brief §3.4(1): "A family stopped at the cap does **not** meet criterion 1: statements that depend on it are INCONCLUSIVE." The verdict mapping lists "families that stopped at the cap" as INCONCLUSIVE. Search logs show F1, F2 and F6 at their raised 25-query caps with the two-provider stopping condition met in at most one provider (F1: OpenAlex met, arXiv 1 of 2; F6: arXiv met at query 25, OpenAlex 1 of 2; F2: GitHub side unsaturated, 25th query failed). **PASS is therefore unreachable under the approved criterion. This is the designed outcome (INCONCLUSIVE), not a defect.** Criterion 1 is not revised. F11 (5 searches) and F3/F7/F8 (unreconstructed notes) are not cap-stopped; they are reported from the logs as they stand.
2. **Criteria 2 and 4.** Criterion 2 requires full text or official documentation for every *pivotal statement*, not for every included item. The acceptance audit's phrase "claim-by-claim location audit across the included evidence" is broader than the criterion and is withdrawn by this record (dated note; the audit is not overwritten). Criterion 4 requires an L2 "extraction table with locations" for *every included mechanism source*. The coverage requirement is strict, but a table row is lighter than the per-source audits A28–A39. The queue of one-paper audits (11 completed) is mis-scaled for roughly 200 sources.
3. **Stage 3.** No clause in `STAGE_GATES.md`, `STAGE_ROUTING.md` or brief §3 requires Stage 2 PASS before Stage 3. "Does not authorize Stage 3" in the acceptance audit is that document's own wording, not a protocol clause. A user decision to proceed after INCONCLUSIVE would be recorded separately, carry forward the unresolved items, and keep claims that depend on cap-stopped families INCONCLUSIVE. Earlier coordinator reports that said "Stage 3 blocked" meant "not authorized".
4. **Challenger sampling.** Original requirement, brief §3.3: replicate at least three query families; spot-check "max(5, 20% of included sources) at random **plus all pivotal sources**" against stored full text; contradiction search per prioritised assertion; audit max(10, 20%) of exclusions; known-item list. Feasibility is a cost question, not a logical impossibility (see "Challenger scope").
5. **Deliverables from consolidation.** See "Minimum remaining closure steps".

## Decision

### D2-1 Criteria retained (Path A)
All 14 criteria and the verdict mapping stay as approved. No criterion, cap or stopping rule is revised. Criterion 1 is recorded as **unmet** for F1, F2 and F6 under the current cap rules. No further searches are run to manufacture a PASS. Unmet or partial criteria are reported as such. The expected Stage 2 verdict is INCONCLUSIVE.

### D2-2 Extraction queue stopped
The automatic one-paper L2 extraction queue is stopped. A further source-level extraction is allowed only when the pivotal-source inventory shows a pivotal statement with no location-cited basis, and only with its own committed ticket.

### D2-3 Population definitions (effective, provenance-backed decisions)
- **Rule.** A source group's decision is derived from the logged candidate rows, following `corrects` chains so that a linked correction supersedes the row it corrects (correction history is not a separate vote). Per group the effective set is then classified:
  - **A, uncontested include:** all effective rows are `include`.
  - **B, contested include:** `include` together with `maybe` or `exclude`.
  - **C, unresolved maybe:** only `maybe`.
  - **D, effective exclude:** `exclude` only, or `exclude` with `maybe`.
- **A historical include flag is not a final inclusion.** B is reported as contested and C as unresolved screening. Neither is promoted by this record.
- **Indicative counts at HEAD `da70baa` (index sha256 `ec7a32a9d203effd5b771d9081534ef6355545b38a7a9a1d856f537044be631b`), 506 groups, 669 rows:** A 217; B 42 (38 include+maybe, 4 include+exclude); C 223; D 24 (23 exclude-only, 1 exclude+maybe). Ten correction rows changed the decision of the row they correct. These counts are **not frozen**. The freeze manifest (step 1 below) records the final counts, hashes and sampling seed.
- **Sampling frame for "included sources"** = A ∪ B (indicatively 259), with each item's stratum labelled. **Exclusion frame** = groups carrying an effective `exclude` (D plus the 4 include+exclude conflicts, indicatively 28).
- Limitations to be reported: the single-screener basis, the large unresolved C set (223 groups), 38 contested include+maybe groups, and the fact that the A21–A27 provenance reviews inform but do not adjudicate the contested groups.

### D2-4 Criterion 4 (extraction table)
The L2 table is generated from existing evidence at each source's recorded verification level (fulltext / official-docs / abstract / snippet / metadata). Missing fields and missing locations are marked explicitly ("not documented" kept distinct from "not searched" and "not extracted"). It cites A28–A39 where they exist. No completeness is manufactured and no new extraction is performed to fill cells. Criterion 4 is recorded **PARTIAL** wherever the original requirement (location-cited evidence for every included mechanism source) is unmet.

### D2-5 Criterion 11 and the independent challenge: original requirement vs this closure attempt

**Original requirement (unchanged, brief §3.3).** At least three replicated families; a random sample of max(5, 20%) of the **full included population** (indicatively 52 of 259), **unioned with all pivotal sources**, checked against stored full text; contradiction search per prioritised assertion; an exclusion sample of max(10, 20%) (10 of 28); a known-item list.

**Authorized limitation for this closure attempt only.** The user has provisionally authorized a reduced-scope review on 2026-10-12 to prioritise claims that materially influence the research-direction decision. This is an explicit, recorded limitation of this attempt. It is not a retroactive change to criterion 11 or to §3.3. Every shortfall against the original requirement is recorded in the final audit, and criterion 11 is reported **PARTIAL or INCONCLUSIVE, never PASS**, unless the original requirement is actually met.

**Reduced scope (proposed concrete sizes and budget):**

| Component | Original | This attempt |
|---|---|---|
| Decision-critical pivotal sources | all pivotal | up to 20, ranked by the number of pivotal statements depending on them (taxonomy categories, benchmark rows, A1/A3/A5/A6/A13 dispositions, L8 and L9 answers, strongest prior art), plus any source that is the sole support for a disposition. The coordinator lists every pivotal source not reviewed. |
| Random included sample | ceil(20% × frame), indicatively 52 | 15, drawn at random with a recorded seed from the **full** A ∪ B frame. The union with the pivotal set is taken afterwards, and overlaps are counted once. There is no restriction to non-pivotal sources. |
| Exclusion sample | max(10, 20%) | 10 of the exclusion frame, drawn with a recorded seed, plus any of the 4 include+exclude conflicts not drawn (original size met). |
| Replication of at least 3 families | required | A5 (F1, F2, F8; small checks on F3, F12) is used. The audit confirms whether a different provider was used for at least one family. If not confirmed, that component is INCONCLUSIVE. No new replication searches. |
| Contradiction search per prioritised assertion | required | The A5 D1–D6 leads and stored evidence only. Assertions not independently contradiction-searched are named. No new searches. |
| Known-item list | required | A5 baseline plus the mechanical recall refresh. |

**Execution budget.** The challenger is `independent-challenger` (Opus 5.5 High) and is read-only. It receives a frozen manifest (IDs, claims, locations, stored-text paths) and not the synthesis conclusions. A5 stays unmodified. At most **3 sequential runs**, each reviewing at most 20 items: run 1 the decision-critical set, run 2 the random inclusion sample, run 3 the exclusion sample. The coordinator may make up to **20 source-text fetches** (`fetch_source_text.py`; no searches) for sampled or critical items without stored text. A failed or inaccessible fetch leaves that item INCONCLUSIVE and it is not replaced. Each run is reported to `audits/` and committed before the next starts.

**Targeted escalation.** If the challenger identifies a consequential gap, the coordinator may propose one further run of at most 15 items aimed at it. It is executed only with the user's explicit approval. Consequential means any of: a misquoted or unverifiable location (FAIL-class under the verdict mapping), a decision-critical claim contradicted by its source, or a pivotal objection that cannot be resolved from stored text. Any finding that meets the FAIL conditions in §3.4 is reported as a FAIL condition, not softened.

### D2-6 No closure searches by default
No new searches are run for recency, citation chaining, F11 top-up or uncovered-assertion contradiction. The coverage signals that need searches (3 chaining, 4 grey/production, 5 global 90-day recency) are reported as **bounded and not completed**, under criterion 14's "reported" wording. Any closure search would need a separate approval with logged queries and caps.

### D2-7 Compliance
Criterion 12 is audited at record level by a scripted scan of the logs and tickets plus a coordinator review. Mechanical work uses the `infrastructure/tools/` scripts, not LLM agents.

### D2-8 Stage 3
**D2 does not authorize Stage 3.** After the Stage 2 closure record is complete, the user decides separately (D3) whether the INCONCLUSIVE evidence suffices to proceed and under what restrictions.

## Minimum remaining closure steps (sequential, coordinator is sole writer)

1. **Freeze manifest.** Record the HEAD, hashes of the logs and index, the final A/B/C/D counts, the frames, and the seeds. Commit it.
2. **Mechanical refresh** of the A5 known-item recall against the current index (`stage2_known_item_recall.py`), and the scripted compliance scan.
3. **Pivotal-source inventory** with a location for each pivotal statement (criterion 2), and the ranked decision-critical set. Name any pivotal statement lacking a location-cited basis.
4. **Integrated L1–L9 deliverables** from existing evidence, with unmet items marked:
   - taxonomy (3)
   - extraction table (4, per D2-4)
   - benchmark table (5)
   - assertion map (6)
   - industry and economics (7)
   - identity (8)
   - disconfirming answers (9)
   - inclusion/exclusion log, evidence map and coverage limits (10)
   - L9 integration (13)
   - bounded coverage statements with the five signals (14)
5. **Challenger runs** per D2-5 (up to 3, then escalation only with approval).
6. **Final audit of criteria 1–14**, the gate verdict (expected INCONCLUSIVE), the shortfalls against the original criterion 11, and the minimum recovery record required by `STAGE_GATES.md` (failed condition, evidence examined, what was not available, bounded retry if any, owner and action, whether prior outputs need correction).
7. **Stop** and hand the user the closure record for the separate D3 decision.

## Unresolved objections and uncertainties
- The independent review text is not in the repository (see above).
- The pivotal-source set is not yet enumerated, so the number of unreviewed pivotal sources is unknown until step 3.
- The 223 unresolved maybe groups and 42 contested groups remain unadjudicated; the reduced random sample is about 6% of the frame, so it supports spot-check statements only, not a claim about the inclusion error rate.
- Claims that depend on F1, F2 and F6 remain INCONCLUSIVE regardless of this closure.

## Required follow-up / owner / due condition
- Owner: the coordinator, after the user signs this record. No synthesis, challenger run, search, extraction or Stage 3 work starts before then.

## Decision status
**Accepted by the user (final approval) on 2026-10-12, at commit `d9fe44e`, with Path A and the clarifications below. Active.**

### User final approval and clarifications (2026-10-12)
1. The reduced challenger review stays capped at **20 decision-critical pivotal sources**. Sole-support sources are prioritized within that limit. Pivotal sources that cannot be reviewed are enumerated with their consequences. The budget is not expanded without the user's approval.
2. The independent Opus process review is to be preserved verbatim at `audits/STAGE2_INDEPENDENT_OPUS_REVIEW_2026-10-12.md`. **At the time of this approval record the file was not present in the working tree or repository** (searched the project, Documents, Downloads and Desktop to depth 3). It has therefore not been verified against the original or committed. The "Independent review findings" section above still rests on the user's summary until the file is supplied. Its secondary scientific findings are not independently verified primary-source evidence.
3. All 14 acceptance criteria stay unchanged. Stage 2 may close INCONCLUSIVE and must not be declared PASS falsely.
4. Stage 3 stays unauthorized pending the user's separate D3 decision.
5. Only closure step 1 (the freeze manifest) is authorized for the next unit. The following steps need further instruction.

## Rationale for any change to an earlier decision
- No criterion or protocol rule is changed.
- Supersedes only the acceptance audit's "Exact next safe actions" item that continues one-paper extraction. This is recorded by D2-2, and the audit is not edited.
- The audit's wording on criterion 2 is withdrawn by D2 Findings 2.
