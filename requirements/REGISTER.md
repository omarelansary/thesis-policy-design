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
1. The thesis research question as established with the supervisor: `requirements/THESIS_QUESTION.md` (empty until the user supplies it verbatim). Excerpt E1 (section G) is a fragment of the supervisor stating a research question; it was **not** entered there.
2. ~~The 2026-10-14 supervisor instructions and examples~~: **partly admitted on 2026-10-16 under AUTH-003** (nine user-approved excerpts, section G). The rest of the 2026-10-14 meeting remains unsupplied and is not to be inferred. New REQ ids with their own provenance; not merged into sections A-E and not findings of the independent research.
3. Any change to the research-target formulation (section A). Section G raises a question about it (G.3, Q1); the user decides.

## G. 2026-10-14 supervisor excerpts (AUTH-003; authority: supervisor, as quoted; classification: lead, proposed until the human accepts it)

**Source.** `requirements/intake/2026-10-16-supervisor-meeting-2026-10-14-excerpts.md` (INT-T-001, excerpts E1-E9, body SHA-256 `741653b0…cbe09`, create-only, re-hashed by `verify_workspace.py`). Meeting "Automatic Tool Discovery", 2026-10-14, speaker per supplier A.F.M. Mohimenul Joaa; automatic transcript; original not available here, its hash unknown; the omitted material was not seen. The E1-E9 titles are the supplier's labels, not transcript text.

**How to read this section.** The supervisor's words stay in INT-T-001; the third column below quotes only short fragments to locate the classified statement and is not a paraphrase. Classes are those of `intake/README.md`: `supervisor-requirement` (an instruction or condition stated as one), `supervisor-example` (illustrative, numbers not specifications), `supervisor-assertion` (a claim, including about novelty; to be tested, not assumed), `user-decision`, `unclear` (ask). Where a statement has two plausible classes the more cautious one is used and the alternative is named. **Nothing here is a finding, nothing selects a policy or contribution, and recording a requirement is not approval of any solution** (AUTH-003).

### G.1 Register

| id | excerpt | located by | class | note (lead's reading, [I]) |
|---|---|---|---|---|
| REQ-O14-01 | E1 | "We don't need to change it." after "most optimal way to reduce the count of tools while keeping the accuracy as high as possible… that's the research question" | supervisor-requirement | The supervisor states the research question and says it stays. The excerpt begins mid-sentence, so the question's full wording is **not** established here. Unit ("count of tools") differs from the earlier token-based wording: see G.3 C1. Does not fill `THESIS_QUESTION.md`. |
| REQ-O14-02 | E1 | "What you have found and narrowed down is some methodologies." | supervisor-assertion | A characterization of someone's earlier findings. Who "you" refers to and which findings are not stated; no inference about previous-thesis work is drawn or permitted (Stage 5 rule). |
| REQ-O14-03 | E2 | "using the same scorer… the same uh code to evaluation" | supervisor-requirement | Methodological expectation: every compared method, baselines and the proposed one, runs under one scorer and one evaluation code path. |
| REQ-O14-04 | E2 | "a b c d different baselines… e is my method… these five" | supervisor-example | "let's say": four baselines plus one method is illustrative. The earlier requirement is only "multiple baselines" (REQ-S4). |
| REQ-O14-05 | E3 | "You have to have some kind of findings otherwise it's not a master's thesis." | supervisor-requirement | Stated as a condition of the thesis. Kind and size of "findings" not stated. |
| REQ-O14-06 | E4 | "which one works at which time we have to figure it out" | supervisor-requirement | Methodological expectation: determine which methods work under which conditions. "Which one" (methods? stages? policies?) and "time" (turn? scenario?) are not defined in the excerpt. |
| REQ-O14-07 | E4 | "That's the main nobility." | supervisor-assertion | "nobility" is kept as supplied; read here as the speaker's "novelty" ([I], ASR). A claim about where the contribution lies; **not established**, no prior-art check done. |
| REQ-O14-08 | E5 | "you have to find out a policy"; "take the top five tool… This is not a policy." | supervisor-requirement | The deliverable is a policy; a fixed top-N cut-off is stated not to be one. |
| REQ-O14-09 | E5 | "based on the context and based on the scenario it will be different" | supervisor-requirement (prescriptive reading) | Alternative reading: a prediction about what the policy will turn out to be. "Context" and "scenario" are undefined. |
| REQ-O14-10 | E6 | "You have to write down a evaluation script" | supervisor-requirement | Whether this is executable code or a written evaluation specification is not stated; its timing relative to E9 is open (G.3 Q5). |
| REQ-O14-11 | E6 | "which one applies at which stage. You will have different stages." | unclear | Antecedent of "which one" and meaning of "stages" (policy stages? evaluation stages?) are not in the excerpt. "Stages" here are not the clean-room project's Stage 1-5. |
| REQ-O14-12 | E7 | "There are steps. At each step you have to ask yourself one question… Okay, that's the policy." | unclear | Binding form of the policy (sequential relevance questions, each filtering the remaining tools) or an illustration of what a policy could look like? The supplier labels the excerpt "Conceptual graph illustration"; the speaker also says "I don't know how many stage you have". Whom or what answers each question (an LLM call, a rule, a score) is not stated. |
| REQ-O14-13 | E7, E8 | "you have to find find those questions and the stages"; "that's the graph that you need to find out" | supervisor-requirement (conditional on REQ-O14-12) | If the staged form holds, finding its questions and stages (the "graph") is the task assigned to the student. |
| REQ-O14-14 | E7 | "10,000", "stage one, stage two, stage three, stage four" | supervisor-example | Catalogue size and stage count are illustrative; the speaker says the stage count is unknown to him. Not specifications. |
| REQ-O14-15 | E8 | "filtered out a tool at stage four but at stage five… you can go back and then again add the tool" | supervisor-example | A design suggestion, permissive ("can"), with hypothetical stage numbers ("let's say"). Whether re-adding is required is not stated. |
| REQ-O14-16 | E8 | "that is your novelty actually" | supervisor-assertion | A claim that the graph is the novelty. **Not established**: no prior-art or originality check has been made, and none is implied. |
| REQ-O14-17 | E9 | "by then I should have the policy" | supervisor-requirement (time-bound) | A policy is due at the next meeting. Form of the deliverable is not stated. |
| REQ-O14-18 | E9 | "I don't want you to implement anything." | supervisor-requirement | Constraint on the one-week task. Whether it also covers experiments, and what applies after that week, is not stated. |
| REQ-O14-19 | E9 + supplier note | "next witness day 11:00 a.m."; note: "Wednesday, October 21, 2026, at 11:00" | user-decision | The date is the user's reading of "next witness day", not transcript text. [O] 2026-10-14 and 2026-10-21 are both Wednesdays and seven days apart, consistent with "one week". Time zone unstated. |

### G.2 Where the comparison with 2026-10-02 lives
`requirements/COMPARISON-2026-10-14-vs-2026-10-02.md` (SUM-0001, unverified summary). It lists alignments, refinements, apparent conflicts and open questions without changing sections A-E.

### G.3 Questions for the human (not resolved by any agent)
- **Q1.** Does E1 restate the research target or replace the 2026-10-11 formulation in REQ-U1 (tokens, end-to-end performance, all overhead)? E1 speaks of "count of tools" and "as high as possible"; REQ-M1 R1 records the earlier "not filtering tools as such".
- **Q2.** Is the staged relevance-question form (REQ-O14-12) a binding form of the policy or an illustration?
- **Q3.** May E1 be entered in `THESIS_QUESTION.md` (it is a fragment), and in what exact wording?
- **Q4.** Does "each step saves tokens" (REQ-S2) still bind a design in which a later stage can re-add a tool (REQ-O14-15)?
- **Q5.** Is the "evaluation script" (REQ-O14-10) part of the 2026-10-21 deliverable, and does "implement" in REQ-O14-18 include writing it?
- **Q6.** Does the 2026-10-21 deliverable replace the time-bound October 2 one (REQ-M1 R14)? Whether the October 2 one was delivered is not known to this workspace (brief U10). Neither is closed here.

## Read this before using sections B-D
The 2026-10-02 transcript is automatic speech recognition with garbled names; two records disagree on whether "each step saves tokens" is per step or collective; the brief and the candidate records mark illustrative examples (tier sizes, 100 to 60, 27B model, 50%) as examples, not requirements. See `evidence/CAVEATS.md` rows 5, 6, 13.
