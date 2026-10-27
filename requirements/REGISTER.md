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

## H. Supervisor meetings of 2, 14 and 21 October 2026 (AUTH-018; route A intake INT-T-002, INT-T-003, INT-T-004; authority: supervisor, as transcribed; classification: lead, checked by two stewards in FND-0035 and FND-0036; proposed until the human accepts it)

Pointers: `INT-T-002 Lnnn` = body line nnn of `requirements/intake/2026-10-21-supervisor-meeting-2026-10-21-notes-and-transcript.md` (file line nnn + 19); `INT-T-003 Lnnn` likewise for the 14 October file; `INT-T-004 Ennn` = export line nnn of the 2 October excerpts. Only transcript lines are used; the Gemini notes are machine summaries. The words stay in the intake files; the rows below carry pointers and a classification, not paraphrases that replace them. Mapping and checks: `design/ledger/notes/MEETINGS-MAPPING-20261021.md`, `findings/SUM-0037`, `findings/SUM-0038`.

### H.1 Register
| ID | Pointer | Class | Note |
|---|---|---|---|
| REQ-O21-01 | INT-T-002 L223-L225, L390 | supervisor-requirement | Practical scope: memory and tool calls only ("Forget about knowledge. Forget about everything else. And memory should help tool calls"; "tools and memory ... comes hand in hand"). |
| REQ-O21-02 | INT-T-002 L146, L212-L214 | supervisor-requirement | Whether conversation memory belongs "depends on what you are building"; if the whole context management is the thesis, everything is needed; otherwise one may choose. |
| REQ-O21-03 | INT-T-002 L245, L375-L384 | supervisor-example | Memory holds the questions and answers of tool calls and a short summary of past interaction; the relevant part is injected first and more is given when asked. |
| REQ-O21-04 | INT-T-002 L197-L209, hedge L221 | supervisor-assertion | Explicit caching applies to memory, knowledge and tools; added information can stay cached for the whole conversation at "negligible cost". Said in the part he calls "all in theory"; the cost statement is a claim to test against the stored price evidence. |
| REQ-O21-05 | INT-T-002 L250-L275 | supervisor-example and supervisor-assertion | Tool responses written to files and searched when needed, rather than kept in the context (the 'MCP brain without notepad' contrast); "You can save around 80% of the cost by doing this". |
| REQ-O21-06 | INT-T-002 L190-L207 | supervisor-assertion | A trivial "hello" and "hi" can consume 10,000 tokens where 10-30 would do. |
| REQ-O21-07 | INT-T-002 L302-L320 | supervisor-requirement | The policy may recover from failures at a higher cost on a few turns; savings in tokens and response time are judged on average over many turns. |
| REQ-O21-08 | INT-T-002 L345-L354 | supervisor-requirement | The problem applies to any kind of agent (coding, sales, recruiting, marketing); the cost per turn is the problem. The student's narrower one-hour idle-gap proposal (L331-L345) receives no explicit yes or no in the transcript. |
| REQ-O21-09 | INT-T-002 L426-L458 | supervisor-requirement | Validate first with a plain text or Markdown memory injected into the prompt; "don't engineer it at all" until results; publishable numbers need a very big experiment with multiple goals and settings and repeated runs to show statistical variance. |
| REQ-O21-10 | INT-T-002 L481-L500 | supervisor-requirement | Send the thesis to Michael and Simon three or four weeks before submission; meetings can be online. The 18 February registration deadline and the 22-week limit are the student's statements (L470-L494). |
| REQ-O14F-01 | INT-T-003 L157-L159 | supervisor-requirement | The research question in full: "which method is the most optimal way to reduce the count of tools while keeping the accuracy as high as possible", "We don't need to change it" (completes the fragment REQ-O14-01). |
| REQ-O14F-02 | INT-T-003 L363-L365 | supervisor-requirement | A negative or not very novel result is still a thesis; a paper needs a systematic study. |
| REQ-O14F-03 | INT-T-003 L214, L227-L233, L404 | supervisor-assertion | Nothing here is groundbreaking; the novelty is combining approaches and showing what works and what does not, to be "sold" as novelty; the staged graph "is your novelty". |
| REQ-O14F-04 | INT-T-003 L261-L265 | supervisor-example | Stage one filters by who invokes the agent (the AI-salesman example). |
| REQ-O14F-05 | INT-T-003 L266-L318 | supervisor-example | A later stage is Executor-style capability listing or semantic narrowing ("which one is better ... You have to figure it out"); narrowing in several steps (1,000 to 800, 500, 200, 10). |
| REQ-O14F-06 | INT-T-003 L386-L404 | supervisor-requirement | The policy is a staged graph: one question per stage, the number of stages open, a tool filtered out may be added again at a later stage. |
| REQ-O14F-07 | INT-T-003 L429-L447 | supervisor-requirement (time-bound, date passed) | Deliver the policy by Wednesday 21 October 11:00, without implementation. |
| REQ-O02-01 | INT-T-004 E202-E206 | supervisor-requirement | A baseline with all tools; match its accuracy with fewer tools. |
| REQ-O02-02 | INT-T-004 E228-E232 | supervisor-requirement | Filtering must not cost more tokens than it saves ("if you use many many more token to filter out the tools then there is no value"). |
| REQ-O02-03 | INT-T-004 E524-E542 | supervisor-requirement | The aim is saving tokens while maintaining accuracy, not filtering tools as such. |
| REQ-O02-04 | INT-T-004 E550-E570 | supervisor-example | Partial information: drop the clearly irrelevant tools (100 to 60), then tiers (full description; known to exist; name only); "not saying this is the best way", the numbers "not rigid". |
| REQ-O02-05 | INT-T-004 E593, E605-E607 | supervisor-assertion | The partial-information idea comes from someone else's documentation; Executor "is doing the same thing" (A9). |
| REQ-O02-06 | INT-T-004 E626 | supervisor-requirement | Executor is a baseline; several baselines are needed. |
| REQ-O02-07 | INT-T-004 E689 | supervisor-requirement | Keep the earlier work as it is in a new branch and start by analysing what is available. |
| REQ-O02-08 | INT-T-004 E697 | supervisor-requirement | "we will not drop the cost" (the cost constraint stays when using a helper model). |
| REQ-O02-09 | INT-T-004 E774-E790 | supervisor-requirement | Each step is there to save tokens; give the model a way to query the tools held back in case the filtering was wrong; the saving is judged over a number of turns, one dearer turn does not matter. |
| REQ-O02-10 | INT-T-004 E749, E804 | supervisor-example (time-bound) | Start experiments small (about 20 samples); for that week, a draft policy without implementation. |
| REQ-U21-01 | ops/AUTHORIZATIONS.md (AUTH-018 section) | user-decision | "executor doesnot have to be locked i am using an API free from my university and it offer bunch of different AI models." |
| REQ-U21-02 | ops/AUTHORIZATIONS.md (AUTH-018 section) | user-decision | The earlier retrieval work (27 methods) is kept but must never contaminate this work; whether it will be needed is not known. |

### H.2 Relations to earlier requirements (recorded, not resolved)
- REQ-O21-01 (scope: memory and tool calls) and REQ-O14F-06 (staged tool-filtering graph): the 21 October meeting does not say whether the graph remains the form of the policy under the narrowed scope (ledger N-28).
- REQ-O14F-01 (count of tools) and REQ-O02-03 / REQ-O02-09 (save tokens, judged over turns): he states both; on 14 October he equates narrowing from 100 to 10 tools with "reducing 90% of token" (INT-T-003 L377). The ledger reads tokens as the objective and the tool count as the means (Q-J02).
- REQ-O21-04 (caching at negligible cost for the whole conversation) and the stored provider pages (cache writes 1.25x or 2x the input price, reads 0.1x, lifetimes of 5 minutes or 1 hour on Anthropic; storage charged per hour for Gemini explicit caches): a claim to test, not a contradiction resolved here (ledger AS-15).
- G.3 Q1 and Q3: the full research-question sentence is now available (REQ-O14F-01); entering it in `THESIS_QUESTION.md` stays the human's decision.
- G.3 Q2 and Q4: answered in part (REQ-O14F-06; REQ-O02-09).
- G.3 Q5: for the 21 October deliverable, no implementation (REQ-O14F-07); after 21 October, experiments with a minimal memory (REQ-O21-09). G.3 Q6: the 21 October deadline continues the 2 October request for a draft policy (REQ-O02-10); whether the 2 October draft was delivered is not stated.

### H.3 The human's decisions after the meetings (INT-T-005, AUTH-019; class user-decision; pointers are body lines of `requirements/intake/2026-10-21-user-decisions-after-meetings.md`)
| ID | Pointer | Decision (short; the words are in the intake file) |
|---|---|---|
| REQ-U21-03 | line 1 | Do not re-invent or re-test what research, large companies or widely used open-source projects have already tested; reuse what fits a point of the design, including earlier work after verification, and build on it; we are designing a policy. |
| REQ-U21-04 | line 5 | The staged policy and memory deciding which tools are offered are combined (both). |
| REQ-U21-05 | line 6 | The June expose does not govern; its ideas are candidates, verified against the others and kept or dropped with a stated reason. |
| REQ-U21-06 | line 7 | Process: research and a drafted policy; proof-of-concept tests of parts in a loop (test, verify, improve; not rigorous or full); then an end-to-end study and final findings. |
| REQ-U21-07 | line 8, line 16 | Objective: minimise the bill on average over turns and sessions while keeping accuracy nearly the same; a model-agnostic billing equation with its components (input, reasoning, output, tools, prompt caching); no margin, budget or hard threshold. Replaces the AUTH-006 working objective of 19 October. |
| REQ-U21-08 | line 9 | Models and providers are chosen when implementing. |
| REQ-U21-09 | line 12 | Anticipation by likelihood (who asks, in what setting) is in scope as a small part, not the focus. |
| REQ-U21-10 | line 14 | Session patterns: one long run and returning users. |
| REQ-U21-11 | line 16 | Success is the quality of the work (every scientific and engineering approach considered, nothing missed), not a particular result. |
| REQ-U21-12 | line 20 | The supervisor's files-not-context and 'hello/hi' remarks are illustrations of the thesis aim, not separate claims. |

Relation recorded: REQ-U21-03 allows reusing earlier work after verification, while REQ-U21-02 keeps the earlier retrieval work out so that it never contaminates this work; read together, earlier work enters only when the human places it explicitly and it is verified, which the ledger records as a decision when it happens (C-D11 reopen trigger).

### H.4 The human's answers after the V5 audit (INT-T-006, 2026-10-22; pointers are body lines of `requirements/intake/2026-10-22-user-answers-after-v5.md`)
| ID | Pointer | Class | Decision (short; the words are in the intake file) |
|---|---|---|---|
| REQ-U22-01 | line 2 | user-decision | Q-U28: the university API's public status page may be fetched to see which models the key offers (done: `evidence/literature-20261019/v5-scads-llm-state-20261022.json`). No API request with the key is authorised by these words. |
| REQ-U22-02 | line 4 | user-decision | Q-U29: DPR-0007 is the working draft. Not an approval (no DES record). |
| REQ-U22-03 | line 6 | unclear | Q-U30: the human asks whether lowering each session's bill per turn lowers the total bill per turn; no choice of the primary averaging yet. |
| REQ-U22-04 | line 8 | user-decision | Q-U31: the ledger changes proposed in `design/package-v5/08-ledger-proposals.md` are accepted. |
| REQ-U22-05 | line 10 | user-decision | Q-U32: check the exposé's ideas only, "nothing more nothing less", as ordinary candidate ideas that predate V1 and were never checked for reuse; two files outside the workspace are named (lines 12-20). |
| REQ-J22-01 | line 23 | user-decision on the supervisor's behalf | Q-J31: the staged approach is a starting point, the staged form was an example and may change; memory must not stay switched off, it must be tested properly in the right place. |
| REQ-J22-02 | line 25 | user-decision on the supervisor's behalf | Q-J32: "reduce the count of tools" was an example of what could lower the bill; focus on the goal (the bill). |
| REQ-J22-03 | line 27 | unclear | Q-J33: the question about the Executor arm was not understood. |

| REQ-J22-04 | INT-T-007 line 1 | user-decision on the supervisor's behalf (reported second-hand) | Q-J33 answered: Executor (the GitHub project) could be a baseline but need not be taken as one or forced; learn from it and reuse it in parts, understanding how it works, its parts, its strengths and weaknesses. Narrows REQ-O02-06 for this work: Executor is a source of reusable parts and an optional baseline. |
| REQ-U22-06 | INT-T-007 line 3 | unclear | Q-U30 still unclear to the human; the lead re-explains. The human also asks the lead to give itself access to the two outside paths of INT-T-006 (not done: changing the guard is the human's, see WD-045). |
| REQ-U22-07 | INT-T-007 line 6 | user-decision (method question) | The human has the API key and URL and asks how they should be checked; answered with a script the human runs (`design/package-v5/tools/p0_api_probe.py`), so the key never enters the workspace or the transcript. |
| REQ-U22-08 | INT-T-008 line 1-2 | user-decision | Q-U30 answered: A (total bill over total turns) is the headline figure, with B (the mean of each session's bill per turn, the lead's recommendation) reported beside it. Settles DPR-0006 section 4's open choice for V5; DPR-0006 itself is unchanged. |
| REQ-U22-09 | INT-T-008 line 4-7 | user-decision | Q-U32 carried out: the exposé PDF (SHA-256 6c47e236...1632c) and the experiment brief (SHA-256 a25af925...a4b01) were placed in `design/package-v5/inputs/expose/` for checking, ideas only; the brief's status notes about an earlier experiment are not used (REQ-U21-02). Result: `design/package-v5/09-expose-ideas-checked.md`. |
| REQ-U22-10 | INT-T-008 line 9 | user-decision | The API probe (Q-U33) cannot be run now; accepted: nothing else waits on it. |
| REQ-U22-11 | INT-T-009 line 1 | user-decision (action report) | Q-U33 carried out by the human: the probe was run on gpt-oss-120b and five further models, outputs placed in `design/package-v5/inputs/`; supersedes REQ-U22-10's deferral. Reading: `design/package-v5/10-p0-university-api-reading.md`. |

Relations recorded: REQ-J22-02 settles H.2's count-versus-tokens relation for this work in favour of the bill (with REQ-U21-07); REQ-J22-01 replaces V5-R's "memory-informed offering off by default" with "memory-informed offering in the tested policy"; REQ-J22-01 and REQ-J22-02 are the student's answers for the supervisor, so the supervisor's own confirmation remains possible.

## Read this before using sections B-D
The 2026-10-02 transcript is automatic speech recognition with garbled names; two records disagree on whether "each step saves tokens" is per step or collective; the brief and the candidate records mark illustrative examples (tier sizes, 100 to 60, 27B model, 50%) as examples, not requirements. See `evidence/CAVEATS.md` rows 5, 6, 13.
