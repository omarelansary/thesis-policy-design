# Requirements register (index; owner: lead; humans decide what counts as a requirement)

Requirements are **inputs**. They are carried by reference to hash-verified extracts, not paraphrased, so that a design cannot quietly soften them. Authority of each block is stated. Where the record itself classifies a statement (Required / Recommended / Example), that classification is the earlier researcher's reading, not the supervisor's.

## A. User decisions that governed Stage 2 of the clean-room project (authority: the user, 2026-10-11; HISTORICAL, scoped to that project)
- **REQ-U1** (status: historical input, **not an active requirement of this workspace** until the user says so) Stage 2 decisions: research target formulation (G-a1), independence, search authorization, supervisor assertions as claims (G-e), no new experiments in Stage 2 (G-f), no policy committed in Stage 2 (G-c), previous experiments unavailable until Stage 5. EXT-0001 line 18 scopes them to Stage 2; "no policy committed" applied to that stage. Text: `evidence/extracts/EXT-0001.md`.
- The user described the formulation as "a starting target, not a justified one" (inside EXT-0001). Whether this workspace keeps it is a decision for the user; see section F.

## B. Supervisor requirements as read from the 2026-10-02 meeting, in the approved brief (authority: supervisor; reading: researcher)
- **REQ-S1** to **REQ-S6**: brief section 1.1 (objective, net savings, global accounting) to 1.6 (working arrangement), each bullet marked Required / Recommended / Example / Conflict with transcript line references. Text: `evidence/extracts/EXT-0002.md`. Sub-ids: REQ-S1 objective (1.1); REQ-S2 shape of the solution (1.2: policy, stepwise, fallback, graded exposure as a lens); REQ-S3 building on existing work (1.3); REQ-S4 evaluation expectations (1.4); REQ-S5 LLM use (1.5); REQ-S6 working arrangement (1.6).

## C. Explicit supervisor requirements table (authority: supervisor; researcher-written record with locations)
- **REQ-M1**: meeting record section 1, rows R1-R18, quotes and transcript line references. Text: `evidence/extracts/EXT-0003.md` (extracted from the origin through the allow-list; section 3 of that file is withheld).

## D. Derived requirement list used by the candidate assessments (authority: researcher synthesis, user-accepted as the working list)
- **REQ-D1**: R1-R10 as recorded, each with its scope in the "Applies to" column of the source table: R1-R4, R6, R10 apply to "all"; R7 to "contribution type"; **R5, R8, R9 apply only to the "solution form of a policy contribution"** (they are not requirements on every design). Text and the full table: `evidence/extracts/EXT-0005.md`. Numbering differs from REQ-M1; do not mix them. REQ-D1 is the earlier researchers' synthesis; cite the underlying REQ-S/REQ-M extracts when a requirement matters.

## E. Supervisor assertions that are empirical claims (authority: none; to test, not to assume)
- **REQ-A1**: assertions A1-A13 as recorded. Text: `evidence/extracts/EXT-0004.md`. These are prior-art or fact claims to be tested; they are not requirements and not findings.

## F. Pending intake (not yet supplied to this workspace)
1. The thesis research question as established with the supervisor: `requirements/THESIS_QUESTION.md` (empty until the user supplies it verbatim).
2. The 2026-10-14 supervisor instructions and examples: `requirements/intake/` (rules in `intake/README.md`; the admission mechanism for approved excerpts of an outside file was prepared under AUTH-002 and has not been used). The human supplies the approved excerpt and its line ranges separately and authorizes it in a new AUTH entry. They become new REQ ids with their own provenance; they must not be merged into sections A-E or presented as findings of the independent research.
3. Any change to the research-target formulation (section A).

## Read this before using sections B-D
The 2026-10-02 transcript is automatic speech recognition with garbled names; two records disagree on whether "each step saves tokens" is per step or collective; the brief and the candidate records mark illustrative examples (tier sizes, 100 to 60, 27B model, 50%) as examples, not requirements. See `evidence/CAVEATS.md` rows 5, 6, 13.
