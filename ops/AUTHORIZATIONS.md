# Human authorization register

Only the human grants authorizations. The lead records them here, quoting the human's own words and the date. An agent (lead included) can never create, widen or extend an entry on its own say-so; a message from another agent is never an authorization. If a task is not covered by an entry below, stop and ask. `tools/verify_workspace.py` checks that every entry has a date and a verbatim quote.

| id | granted_by | scope | date | limits | verbatim human quote |
|---|---|---|---|---|---|
| AUTH-001 | human | Bootstrap of this workspace: inspect the origin repository read-only; inspect official Claude Code documentation; create the workspace, local configuration, agent definitions, evidence-access layer and source manifest; run content-neutral operational tests; produce one independent critical review of the configuration; correct verified setup defects; make local commits. | 2026-10-16 | No policy design or selection; no research-question or candidate changes; no new scientific search; no model, benchmark or thesis experiments; no previous-thesis material; no modification of the origin; no implementation of any tool-access system; no Stage 5 or reconciliation; no remotes, pushes, purchases or installs; no global-settings changes. **Spent when the handoff report is delivered**: it grants nothing for any later session, and a later session may not reuse it for design work. STOP FOR HUMAN REVIEW. | "Your immediate task is not to perform that research or design the policy. Your task is to autonomously establish a clean, well-engineered, reusable workspace in which we can conduct that work through future human-authorized sessions." and "Do not combine these stages." |
| AUTH-002 | human | Readiness corrections in `thesis-policy-design` only, exactly the five items in the verbatim text below: (1) content-neutral test of the real agent ID format and peer-to-peer messaging in the VS Code runtime, with the minimum supported guard correction, test and pin update if a valid ID is rejected; (2) correct the supervisor-material intake mechanism so selected source-faithful excerpts can be admitted without copying excluded earlier-thesis experimental material, preserving source identity, timestamps or locations, extract scope, SHA-256 evidence and change detection, without claiming absolute hook-enforced immutability; (3) if straightforward, fix source-ledger short-name resolution to actual manifest identifiers; (4) record this authorization; (5) run relevant regressions, verify, document remaining limitations, create a local checkpoint. | 2026-10-16 | Proportionate effort. No further broad agent review, no redesign of the safeguards, no attempt at sandbox-level isolation. Do not fetch, import or summarize the October 14 transcript; prepare only the intake mechanism. No modification of `research-cleanroom`, no policy design, no scientific experiments, no contribution selection, no Stage 5. Stop with the readiness results and the exact next step for controlled supervisor-evidence intake. Recorded after the read-only readiness assessment; it does not authorize that assessment retroactively. | see "AUTH-002 verbatim human text" below the table |
| AUTH-003 | human | Controlled intake of nine user-approved excerpts (E1-E9) of the 2026-10-14 meeting "Automatic Tool Discovery" (speaker per supplier: A.F.M. Mohimenul Joaa; supplier-claimed source: a Google Drive transcript; form: automatic transcript; supplier: the human, in the AUTH-003 message), by the intake route for user-supplied text (route A): (1) record this authorization; (2) store the excerpts verbatim with timestamps, speaker attribution, source reference and integrity information; (3) extract requirements, methodological expectations, design suggestions, examples and unresolved interpretations into requirement records; (4) distinguish explicit instructions from illustrative examples; (5) compare with the 2026-10-02 governing requirements without overwriting them; (6) keep the earlier research evidence independent (no reinterpretation of C1-C6); (7) run relevant checks, make a local checkpoint and report. | 2026-10-16 | **Intake only.** No scientific design; no selection of a policy or contribution; no experiments; no Stage 5; no reconciliation with the old thesis. Do not fetch or access the complete 2026-10-14 transcript or the omitted material; no previous-thesis experimental records; no unauthorized sources. Recording requirements is not approval of any proposed solution. No broad research or infrastructure review. **Covers no design approval and no change to tools, safeguards or configuration.** **Spent when the intake report is delivered**; the next task (conceptual policy design with the Sonnet agents) needs its own authorization. STOP FOR HUMAN REVIEW. | "I authorize the controlled intake of the selected supervisor statements below." and "This is an intake task only. Do not begin scientific design." |
| AUTH-004 | human | First scientific design task: an evidence-grounded **provisional conceptual tool-access policy proposal** (reducing unnecessary tool exposure to LLM agents while preserving task performance and accounting for the costs of deciding, discovering and using tools), prepared for the 2026-10-21 supervisor meeting, using the workspace's three Sonnet agents. Expected outputs A-F: (A) problem and objective specification; (B) evidence-to-decision analysis; (C) conceptual policy proposal with a graph or equivalent decision-flow; (D) critical challenge; (E) validation strategy with falsifiers; (F) supervisor-ready synthesis. Source integrity and consistency checks, significant uncertainties and unresolved disagreements recorded, a local checkpoint, then a report with the specific questions requiring human judgment. | 2026-10-16 | Conceptual design only: no implementation, no benchmark or experiment, no measured-improvement claims. No fresh broad landscape search, no web search. No change to historical records, governing evidence, supervisor transcripts or C1-C6 classifications; no previous-thesis material, no Stage 5, no reconciliation with the origin. No declaring any design validated or irrevocably selected; no frozen thesis contribution; no asserted novelty beyond hypothesis; no arbitrary numeric thresholds, stages or performance targets; no future information, reference trajectories, gold tools or benchmark annotations as runtime signals unless their legitimate availability is shown. Existing operational limits apply (`config/limits.json`: 12 messages per thread, 2 rounds per issue; Sonnet agents); report if they materially constrain the review. The user's "working interpretations" in the verbatim text are user-approved clarifications, not supervisor statements. **Spent when the report is delivered.** STOP FOR HUMAN REVIEW. | "I now authorize the first scientific design task in this workspace." and "Do not implement the system or conduct empirical experiments." and "Then STOP FOR HUMAN REVIEW." |
| AUTH-005 | human | Bounded scientific adjudication and revision of the AUTH-004 package: develop one defensible, sufficiently specified **provisional conceptual policy candidate** (or demonstrate that none is presently defensible), applying the eight "Required scientific corrections" in the verbatim text; check a small justified set of pivotal source passages against the already authorized original evidence; use the Sonnet agents proportionately with real disagreement preserved; deliver the candidate with decision logic and graph, justification, comparison with the strongest simpler and materially different alternatives, a corrected falsifiable evaluation outline, a claim-to-source register, a candid unsupported-claims assessment and a supervisor-ready presentation outline; successor records only, the AUTH-004 package and provenance preserved; local checkpoint; stop for human scientific review. | 2026-10-16 | No implementation, benchmark execution, broad literature search, previous-thesis material, origin-repository modification, Stage 5 or final contribution selection. No novelty, optimality, accuracy-preservation or cost-reduction claims without experimental evidence. No rewriting of history: AUTH-004 records stay; revisions are new records or explicitly versioned successor documents. Existing operational limits apply (`config/limits.json`: 12 messages per thread, 2 rounds per issue; Sonnet agents; no web search): the human has not raised them. Nothing in this task approves a design (`approved` needs the human and a design-level AUTH). **Spent when the report is delivered.** STOP FOR HUMAN SCIENTIFIC REVIEW. | "This task is a bounded scientific revision, not a restart." and "Produce a local checkpoint and stop for human scientific review before any further work." |
| AUTH-006 | human | Bounded scientific correction of the AUTH-005 v2 package and a supervisor-facing conceptual policy: (1) correct the dimensional inconsistency of the recovery and initiator break-even equations (success vs cost kept as separate estimands under a noninferiority-constrained objective unless an exchange rate is justified); (2) identify what a missed-tool probability bound requires and correct claims beyond the evidence; (3) examine A1's greedy core-selection rule; (4) examine applicability of C-A to the original large-catalogue problem; (5) treat Toollery's inferred cache multiplier as a fitted study-specific parameter; reassess whether C-A is the principal proposal or a comparator; examine C-B and alternatives against the supervisor's requirement; produce one concrete provisional supervisor-facing decision graph; working operational objective: minimise cumulative model-visible input tokens over complete trajectories while preserving end-to-end task success, including all decision/discovery overhead, with tool count, token categories, billed cost and cache behaviour recorded separately. Outputs only: a corrected errata record for AUTH-005, the decision graph and explanation, a short comparison against C-A, expose-all and vendor deferral, the strongest remaining objections and experiments, and a presentation outline for 2026-10-21. | 2026-10-17 | Bounded revision, not a new research phase. Preserve earlier packages (successor documents only). Existing sources and targeted agent criticism only when necessary; no broad literature search, implementation, experiments or Stage 5 reconciliation. Do not invent stages, thresholds, empirical benefits or novelty; do not automatically adopt C-B; do not claim the objective is an exact supervisor quotation, that the noninferiority margin is decided, or that the policy is validated or final. If the local-settings warning persists, stop and request human intervention (it did not: verifier clean at session start). Existing operational limits unchanged (12 messages per thread, 2 rounds, Sonnet agents, no web search). Nothing in this task approves a design. **Spent when the report is delivered.** STOP FOR HUMAN REVIEW. | "This task is a bounded revision, not a new research phase." and "Check internal consistency, record a local checkpoint, and stop for human review." |
| AUTH-007 | human | Independent-research coordination, Phase 2 PREPARATION only: (1) record this authorization; (2) screen the existing governing records and assemble a **disclosure package** in the lead's scratchpad (outside this repository), with a manifest stating for every file whether it is included, why, and every exclusion; (3) write the comparator's prompt and a launcher so that a fresh Fable-5.1 comparator, run through the human's API key in a folder outside this repository, can compare the frozen Phase 1 dossier (kept outside this repository) with the disclosed material; (4) update `ops/` records. The Phase 1 blind investigation (run 20261017-163102) and its freeze are outside this repository and are not records here. | 2026-10-17 | Nothing independent is copied into this repository. No change to `evidence/governing/**`, `requirements/**` or any frozen record. No origin access (the package is built only from workspace copies). Excluded by the lead: `evidence/restricted.json` items, `requirements/**` (verbatim supervisor excerpts, 2026-10-14 material), `evidence/extracts/**`, `evidence/README.md`, the AUTH-004..006 design packages and challenge/review records, and the governing documents that are digests of the supervisor meeting (see the AUTH-007 section below). No experiments, implementation or new searches by agents in this workspace (the external comparator uses its own web access under the human's API budget; spend cap set in the launcher, default 25 USD, 200 turns). No thesis question, policy, threshold or margin is selected. The comparator's output is stored outside this repository and enters it only by a later human decision. | "i would like to delegate that to you so this what i was trying ot do here is your propes role, u should take the lead and implemnt and loop and finish this and try not to contaminate, some of the stuff in the role prompt could be outpdated understand the general idea and verfy by checking the repos" / "i want this to be more of autonmous i have no time now to keep wathcing and doing stupid yes and no and running commands, so u can either make a strong prompt and we delegeate the task delegated to u and the state to another agent to use the FABEL API independely and finish the phases, or you do it" |
| AUTH-008 | human | Read-only retrieval of two public PDFs (arXiv 2508.16260 v1 and v2, MCPVerse) into the lead's scratchpad outside this repository, local rendering/extraction of the tables with installed tools (pdftotext, PyMuPDF), and a report of the table values in chat to settle the v1/v2 discrepancy the independent comparator could not resolve. | 2026-10-17 | Two PDFs only, from arxiv.org; no other web access, no search, no installs. Nothing is stored in this repository except this record and a decision-log line; the extracted tables stay in the scratchpad and are not added to the frozen independent reports. The values are a reading of the PDFs by the lead, not a verified finding. No change to design packages. | "you or the agent at thesis indepeendant can go fetch the MCPVerse v2 table?" |
| AUTH-009 | human | Preparation of a Phase 2b addendum run OUTSIDE this repository: a fresh Fable-5.1 session (human's API key) receives its own frozen Phase 2 report plus the raw MCPVerse v1/v2 PDFs and page images (no lead interpretation) and writes a revised judgement. The lead builds the evidence package and the launcher in its scratchpad only. | 2026-10-18 | Nothing independent enters this repository. The lead's own reading of the tables is withheld from the run's inputs. Spend cap set in the launcher (default 12 USD, 100 turns); at most about ten web calls inside the run for author clarification and current cache pricing. No other disclosure beyond the existing AUTH-007 package. No experiments. The human starts the launcher. | "now i guess we should add the findings or give acces to the fable for the pdfs it wanted, and then we should run the fabel through API and make that fabel answer its judgment after revising the new findings it neededthe new data brought to it" |
| AUTH-010 | human | Scientific-director session of 2026-10-19 (the human's message is headed "AUTH-00x" and says "within AUTH-007"; AUTH-007 is already a different, spent entry, so the lead records this one under the next free id): take ownership of the AUTH-006 scientific review and the preparation for the 2026-10-21 11:00 supervisor meeting; independently adjudicate the external review's concerns (D4 as arm selection, ties versus equivalence, graph inconsistencies with optional stages and bypass paths, overinterpretation of E1, missing full-exposure reference at large catalogue size); make bounded scientific corrections as versioned successor documents; prepare a concise supervisor-ready explanation; use the existing Sonnet agents where useful; commit locally. | 2026-10-19 | Not authorized (human's words): implement the policy, run scientific experiments, enter Stage 5, inspect excluded previous-thesis material, modify the origin repository, change global settings, push remotely, authorize a new research direction. Keep completed packages intact (versioned corrections only). No broad literature search restart, no repeat of completed audits without a specific material reason. Existing operational limits unchanged (`config/limits.json`: 12 messages per thread, 2 rounds per issue; Sonnet agents; no web search): the human has not raised them. Does not approve any design (`approved` needs the human) and does not select the thesis question, margins or a final policy. Covers only the 2026-10-21 preparation; later tasks need their own entry. | "You are authorized to make bounded scientific corrections, improve the conceptual presentation, prepare a concise supervisor-ready explanation, and commit the resulting documents locally under the repository's authorization and provenance rules." and "Do not implement the policy, run scientific experiments, enter Stage 5, inspect excluded previous-thesis material, modify the original research repository, change global settings, push remotely, or authorize a new research direction on my behalf." |

## AUTH-002 verbatim human text (message of 2026-10-16, after the readiness assessment)
> I conditionally accept the workspace bootstrap and readiness assessment.
>
> I confirm that AUTH-001's enumerated bootstrap activities broadly match my original authorization: read-only origin inspection, documentation inspection, operational tests, independent review, correction of verified setup defects, and local commits. Preserve the original authorization wording and distinguish it from your interpretation. Do not retrospectively invent authorizations.
>
> You are now authorized to perform only the following readiness corrections in `thesis-policy-design`:
>
> 1. Verify the actual agent ID format and peer-to-peer messaging in this VS Code runtime through a small, content-neutral test. If the guard rejects a valid ID, implement the minimum supported correction, test it and update its configuration pin.
>
> 2. Correct the supervisor-material intake mechanism so that selected, source-faithful excerpts can be admitted without copying excluded earlier-thesis experimental material. Preserve original source identity, timestamps or locations, extract scope, SHA-256 integrity evidence and change detection. Do not claim hook-enforced immutability is absolute.
>
> 3. If straightforward, fix the source-ledger short-name resolution so cited sources can be opened reliably using their actual manifest identifiers.
>
> 4. Record the authorization for this task using the exact scope of this message. Do not retroactively claim that an authorization record existed before the read-only assessment.
>
> 5. Run relevant regressions, verify the workspace, document any remaining limitations and create a local checkpoint.
>
> Use proportionate effort. Do not start another broad agent review, redesign the safeguards, or attempt to achieve sandbox-level isolation.
>
> Do not fetch, import or summarize the October 14 transcript during this task. Prepare only the intake mechanism; I will supply or explicitly authorize the approved supervisor extract separately.
>
> Do not modify `research-cleanroom`, begin policy design, run scientific experiments, select a contribution or enter Stage 5.
>
> Stop with the readiness results and the exact next step for controlled supervisor-evidence intake.

## AUTH-003 verbatim human text (message of 2026-10-16)
The excerpts E1-E9 and their provenance block are **not repeated here**; they are stored once, verbatim, in `requirements/intake/2026-10-16-supervisor-meeting-2026-10-14-excerpts.md`. The elision is marked `[...]`. All other text of the message is quoted below, including its Instructions, Boundaries and Stop sections.

> # AUTH-003 — Controlled Supervisor Requirements Intake
>
> The workspace bootstrap and readiness corrections have been accepted through checkpoint `64ae6d9`.
>
> I authorize the controlled intake of the selected supervisor statements below.
>
> **This is an intake task only. Do not begin scientific design.**
>
> ## Source
>
> - Meeting: Automatic Tool Discovery
> - Date: October 14, 2026
> - Speaker: A.F.M. Mohimenul Joaa
> - Source: [Google Drive meeting transcript](https://docs.google.com/document/d/1BOvGNy-q5WQpc_V6D6v6TDr2UlBRzjaEJjwJmMyxHOA/edit)
> - Form: Automatically generated meeting transcript
> - Supplier: User-approved excerpts supplied through this message
> - Verification limitation: The original transcript is not available for direct verification inside this workspace. Preserve the excerpts' provenance and distinguish the supplied text hash from any unverified original-file hash.
>
> The following excerpts were selected from the transcript. The omissions between excerpts are deliberate. Do not fetch, reconstruct or import the omitted material.
>
> [...] (excerpts E1-E9: see the intake file named above)
>
> The meeting occurred October 14, so the agreed target is Wednesday, October 21, 2026, at 11:00.
>
> ## Instructions
>
> Follow the established workspace intake protocol, using the appropriate mechanism for user-supplied excerpts.
>
> 1. Record this authorization as AUTH-003, preserving the authorized scope.
>
> 2. Store the approved excerpts with their timestamps, speaker attribution, source reference and integrity information. Preserve the wording, including transcription errors. Do not silently clean or correct the quoted passages.
>
> 3. Extract the supervisor requirements, methodological expectations, design suggestions, examples and unresolved interpretations into the appropriate requirement records.
>
> 4. Distinguish explicit instructions from illustrative examples. In particular, do not treat the suggested multi-stage graph, its number of stages, or its claimed novelty as independently scientifically established.
>
> 5. Compare the admitted requirements with the existing October 2 governing requirements. Identify genuine changes, refinements, apparent conflicts and open questions without overwriting historical records.
>
> 6. Preserve the independence and provenance of the earlier research evidence. Do not reinterpret or reclassify C1–C6 as a consequence of this intake.
>
> 7. Run the relevant checks, create a local checkpoint, and report exactly what was admitted and how it was classified.
>
> Use appropriate verification and critical review, but do not initiate another broad research or infrastructure review.
>
> ## Boundaries
>
> Do not access the complete October 14 transcript, previous-thesis experimental records or unauthorized source material.
>
> Do not begin conceptual policy design, select a policy or scientific contribution, run experiments, enter Stage 5 or reconcile with the old thesis.
>
> Do not assume that recording these requirements constitutes approval of a proposed scientific solution.
>
> ## Stop
>
> Return a short intake report containing:
>
> - Recorded source and authorization
> - Admitted requirements and classifications
> - Alignment or conflicts with October 2 requirements
> - Remaining ambiguities
> - Verification results
> - Git checkpoint
>
> Then STOP FOR HUMAN REVIEW.
>
> The next task will be separately authorized conceptual policy design with the Sonnet agents.

## AUTH-004 verbatim human text (message of 2026-10-16, after the AUTH-003 checkpoint `9664e4a`)
The whole message is quoted below. The "Working interpretations" are the human's clarifications for this task; they are not supervisor statements and not findings.

> # AUTH-004 — Evidence-Grounded Conceptual Policy Design
>
> The controlled supervisor intake AUTH-003 has been completed at checkpoint `9664e4a`.
>
> I now authorize the first scientific design task in this workspace.
>
> ## Objective
>
> Develop a scientifically defensible **conceptual tool-access policy proposal** addressing the established overarching thesis question: reducing unnecessary tool exposure to LLM agents while preserving task performance and accounting for the costs of deciding, discovering and using tools.
>
> This task is intended to prepare a substantive conceptual proposal for the supervisor meeting on October 21, 2026.
>
> Do not implement the system or conduct empirical experiments.
>
> ## Working interpretations
>
> For this design task, use the following clarifications:
>
> - The overarching research question is established; do not replace it with C1–C6.
> - Tool count, model-visible tokens, cumulative token consumption and billed cost are distinct quantities. The exact optimization formulation remains a scientific choice requiring justification.
> - A conceptual staged policy is an expected supervisor deliverable, but its architecture, stages, mechanisms and effectiveness are not predetermined.
> - Individual stages may create overhead. Their justification depends on the overall objective and their effects on task performance.
> - Design the evaluation strategy now; implementation is not authorized.
> - October 21 is the immediate conceptual policy deliverable deadline.
>
> These are user-approved working interpretations, not claims that the supervisor said these exact words.
>
> ## Scientific approach
>
> Use the independently collected research evidence, governing reports, caveats, prior-art analysis and approved supervisor requirements already available in the workspace.
>
> Determine what design decisions the evidence supports, which alternatives remain viable, where important uncertainties lie, and what scientifically defensible policy proposal could follow.
>
> Do not assume that retrieval, staged filtering, graphs, gateways, code-mediated access, dynamic registries, recovery, or any particular combination must be the solution.
>
> Avoid selecting a method merely because it appears in the supervisor's examples or in the earlier research.
>
> Challenge the assumption that a multi-stage architecture is automatically superior to a simpler policy.
>
> For every consequential proposed decision, distinguish:
>
> - Empirical evidence supporting it.
> - Theoretical reasoning and its assumptions.
> - Engineering judgment.
> - Untested hypotheses.
> - Counterevidence and plausible failure cases.
>
> Inspect original supporting source passages where necessary. Do not rely solely on previous summaries or automatically trust source aliases.
>
> Do not undertake a fresh broad landscape search.
>
> ## Multi-agent collaboration
>
> Use the workspace's existing Sonnet collaboration mechanisms.
>
> Determine how to distribute the scientific work among the configured agents according to their capabilities and responsibilities.
>
> I expect meaningful criticism and direct discussion, not three agreeable summaries.
>
> Agents must be able to challenge each other's assumptions, demand evidence and identify alternatives.
>
> Do not force consensus. Preserve consequential disagreements and their implications.
>
> Keep collaboration proportional to the task. Respect the existing operational limits, and report if they materially constrain the scientific review.
>
> ## Design requirements
>
> Establish the decision problem before proposing its solution.
>
> In particular, examine what information is actually available when the policy must make a decision, what it can legitimately infer, and which information would only become available after execution.
>
> Consider the available mechanism families broadly enough to avoid prematurely committing to one architecture.
>
> A proposed policy must make its decisions interpretable and testable. Explain what determines each decision, what information it needs, what it costs, and what happens when its assumptions fail.
>
> Examine whether recovery or later capability disclosure is necessary, and what consequences those operations may have.
>
> Do not insert arbitrary numeric thresholds, stages or performance targets.
>
> Do not use future information, reference trajectories, gold tools or benchmark annotations as runtime decision signals unless their legitimate availability is demonstrated.
>
> Do not assume that fewer exposed tools necessarily means fewer cumulative tokens or higher task success.
>
> ## Expected outputs
>
> Produce a coherent, reviewable package appropriate for scientific discussion with the supervisor:
>
> **A. Problem and objective specification**
>
> What problem the policy addresses, what is being optimized, which constraints matter, and what remains unspecified.
>
> **B. Evidence-to-decision analysis**
>
> Which decisions the literature and existing findings can justify, what alternatives exist, and where reasoning depends on assumptions rather than results.
>
> **C. Conceptual policy proposal**
>
> A clear, readable representation of the proposed decision logic and transitions, supported by explanation.
>
> A graph or equivalent decision-flow representation should be included to address the supervisor's request. Do not force additional stages or branches merely for visual complexity.
>
> The proposal may be provisional. It must not be presented as experimentally validated.
>
> **D. Critical challenge**
>
> The strongest scientific objections, simpler alternatives, unsupported decisions, potential prior-art overlap and possible failure modes.
>
> Explain which objections are currently answerable and which require experiments.
>
> **E. Validation strategy**
>
> A proportionate plan for investigating the proposed policy against appropriate baselines, including performance, cumulative costs, overhead, recovery and relevant ablations.
>
> Identify falsifiers rather than writing a plan that can only confirm the proposal.
>
> **F. Supervisor-ready synthesis**
>
> A concise explanation of the policy, why its decision logic was proposed, what is supported by current evidence, what is not yet established, and what experimental work would be required next.
>
> Keep this scientifically accurate even if the conclusion is that parts of the proposed policy are not presently justified.
>
> ## Boundaries
>
> Do not modify historical research records, governing evidence, supervisor transcripts or prior candidate classifications.
>
> Do not reopen general research discovery or the completed audit tickets.
>
> Do not access previous-thesis experimental material or enter Stage 5.
>
> Do not implement the policy, execute benchmarks, claim measured improvements or reconcile this work into the origin repository.
>
> Do not freeze a final thesis contribution or assert established novelty where the evidence supports only a hypothesis.
>
> You are authorized to develop, compare, criticize and recommend **provisional conceptual designs**, but not to declare one experimentally validated or irrevocably selected.
>
> ## Completion
>
> Use the workspace's existing documentation, decision and challenge conventions where helpful, without creating unnecessary process overhead.
>
> Check source integrity and internal consistency. Record significant uncertainties and unresolved disagreements.
>
> Create an appropriately scoped local checkpoint.
>
> Report the proposed conceptual design, its scientific justification, the most serious criticisms, what remains unresolved, and the specific questions requiring human judgment.
>
> Then STOP FOR HUMAN REVIEW.
>
> Do not autonomously proceed to implementation, additional research stages or reconciliation.

Lead's notes on AUTH-004 (interpretation, not human text): (1) The message says the overarching question "is established" but did not supply its wording; `requirements/THESIS_QUESTION.md` stays a placeholder and agents use the Objective sentence above as the working statement, quoted, never paraphrased into a narrower question. (2) The register-row scope column is the lead's enumeration of the message; the two quotes in the last column are the operative human words. (3) `tools/verify_workspace.py` still excludes only AUTH-001/002 from design approval; nothing in this task makes any record `approved`.

## AUTH-005 verbatim human text (message of 2026-10-16, after the AUTH-004 checkpoint `2a22677`)
> # AUTH-005 — Scientific Adjudication and Conceptual Policy Revision
>
> AUTH-004 is complete at checkpoint `2a22677`. I have reviewed the uploaded A–F package and evidence map.
>
> This task is a bounded scientific revision, not a restart.
>
> The previous package is accepted as an exploratory analysis, but it is not yet accepted as the conceptual policy for the October 21 supervisor meeting.
>
> ## Goal
>
> Develop one defensible, sufficiently specified **provisional conceptual policy candidate** from the existing evidence and alternatives, while preserving the unresolved scientific questions and stronger simpler comparators.
>
> Do not assume Form S, Form M, or the existing N0–N4 template is correct.
>
> Determine whether a coherent candidate can be justified and explain why it is worth testing. Do not select it on the basis of resemblance to the supervisor's example.
>
> ## Required scientific corrections
>
> 1. Distinguish a configurable policy family from an actual proposed policy with specified decision conditions, inputs, actors and transitions.
>
> 2. Re-examine whether N0 is a deployment configuration, a learned or explicit policy-selection rule, or merely an experimental arm selector. Do not claim adaptivity without an actual decision mechanism.
>
> 3. Specify the decision questions in the proposed policy. It is acceptable to leave numeric parameters for later validation, but not to leave fundamental decision logic undefined.
>
> 4. Reconsider add-only exposure as a hypothesis rather than an automatically justified architectural constraint. Analyze session horizon, cache assumptions, withdrawal and stable-interface alternatives.
>
> 5. Correct the validation logic, especially recovery economics across miss/no-miss populations, trade-offs between initiation mechanisms, and claims based on failure to observe cost inversions.
>
> 6. Separate the primary research objective and measurable outcomes from optional diagnostic definitions of "unnecessary exposure". Distinguish optimization criteria, reporting requirements and strata.
>
> 7. Preserve strict runtime-information constraints and test whether any proposed decision relies on information unavailable when it must act.
>
> 8. Check a small, justified set of pivotal source passages against the already authorized original evidence. Do not repeat the failed broad evidence-steward exercise. Label anything left second-hand.
>
> ## Critical collaboration
>
> Use the available Sonnet agents proportionately.
>
> The proposer must justify its own assumptions rather than automatically concede challenges. The challenger must defend its criticisms and recognize when they are overstated.
>
> Do not force consensus. Retain material disagreements and identify what would resolve them.
>
> Do not create a new architecture simply to demonstrate novelty.
>
> ## Deliverables
>
> Provide:
>
> - One complete provisional policy candidate, with explicit decision logic and a readable graph.
> - A brief justification for why that candidate deserves investigation.
> - A comparison with the strongest simpler and materially different alternatives.
> - A corrected, falsifiable evaluation outline.
> - A claim-to-source register for the decisive arguments.
> - A candid assessment of what remains scientifically unsupported.
> - A concise supervisor-ready presentation outline.
>
> Preserve the original AUTH-004 package and its provenance. Make revisions through clear new records or explicitly versioned successor documents; do not rewrite history.
>
> You may conclude that no single candidate is presently defensible. If so, demonstrate precisely why, which minimal decision is missing, and what evidence would resolve it. Do not fabricate a selection.
>
> ## Boundaries
>
> No implementation, benchmark execution, broad literature search, previous-thesis material, origin-repository modification, Stage 5, or final scientific contribution selection.
>
> Do not claim novelty, optimality, accuracy preservation, or cost reductions without experimental evidence.
>
> Produce a local checkpoint and stop for human scientific review before any further work.

Lead's note on AUTH-005 (interpretation): the message does not change `config/limits.json`; the 12-message cap, 2 rounds per issue, Sonnet pin and no-web-search rules stay in force and the task is planned inside them.

## AUTH-006 verbatim human text (message of 2026-10-17, after the AUTH-005 checkpoint `67abc5f`)
> # AUTH-006 — Scientific Corrections and Supervisor-Ready Policy
>
> AUTH-005 has been completed at checkpoint `67abc5f`. Its successor package has received external scientific review.
>
> This task is a bounded revision, not a new research phase.
>
> Before working, verify the workspace is operationally ready. If the local-settings warning persists, stop and request human intervention. Do not bypass the guard.
>
> ## Scientific corrections
>
> Review and correct these substantive issues in the v2 package:
>
> 1. The recovery and initiator break-even equations combine success probabilities with monetary/token costs. Correct their dimensional inconsistency. Under a noninferiority-constrained objective, keep success and cost as separate estimands unless an exchange rate is explicitly justified.
>
> 2. A1's missed-tool probability is not automatically an upper bound on task-success degradation. Identify the assumptions necessary for any bound, distinguish surrogate coverage from end-to-end success, and correct claims that exceed the evidence.
>
> 3. Examine A1's greedy core-selection rule. Determine whether it actually minimizes incremental cost, how changing the core affects discovery failure probabilities, and whether any optimality or safety property is established.
>
> 4. Examine whether C-A is applicable to the original large-catalogue problem when full-exposure reference runs cannot fit and the proposed need-frequency estimates become unavailable.
>
> 5. Treat Toollery's inferred cache multiplier as a provider- and study-specific fitted parameter, not a verified universal billing rate.
>
> Do not merely add disclaimers where a mathematical or logical correction is required.
>
> ## Supervisor alignment
>
> Reassess whether C-A should be the principal conceptual thesis proposal or a simpler comparator.
>
> The supervisor requested a justified decision-oriented policy that accounts for context, staged narrowing, and possible reintroduction of omitted capabilities.
>
> Examine C-B and the available alternatives against that requirement and the independent evidence.
>
> Produce one concrete **provisional supervisor-facing decision graph**, specifying its questions, information, actors, actions, transitions, and recovery assumptions.
>
> A stage may be skipped where there is no defensible reason for using it. Do not invent stages, thresholds, empirical benefits, or novelty merely to resemble the supervisor's example.
>
> Do not automatically adopt C-B. If the evidence does not justify selecting a specific mechanism, preserve the uncertainty and explain a testable conditional decision.
>
> Maintain the distinction between a conceptual hypothesis and an empirically supported policy.
>
> ## Objective
>
> Use as the working operational objective: minimize cumulative model-visible input tokens over complete trajectories while preserving end-to-end task success. Include all decision/discovery overhead.
>
> Record tool count, token categories, billed cost and cache behavior separately. Do not claim that the objective formulation is an exact supervisor quotation or that the noninferiority margin has been decided.
>
> ## Outputs
>
> Produce only:
>
> - A corrected scientific errata record for AUTH-005.
> - A defensible supervisor-facing conceptual policy graph and explanation.
> - A short comparison against C-A, expose-all and vendor deferral.
> - The strongest remaining objections and the experiments needed to resolve them.
> - A concise presentation outline suitable for October 21.
>
> Preserve earlier packages. Use existing sources and targeted agent criticism only when necessary. No broad literature search, implementation, experiments or Stage 5 reconciliation.
>
> Check internal consistency, record a local checkpoint, and stop for human review.
>
> Do not claim the policy is validated or final.

Lead's note on AUTH-006 (interpretation): the message does not change `config/limits.json`. The "working operational objective" is the human's instruction for this task, not a supervisor quotation.

Note on the register rows: `tools/verify_workspace.py` excludes only AUTH-001 and AUTH-002 from citation as a design approval. The restriction on AUTH-003 (it covers no design approval) is therefore carried by its limits column and this note, not by the check. See the intake report for the recommendation.

## Confirmation of AUTH-001 (human, 2026-10-16) and what is interpretation
- The AUTH-001 row above is unchanged. Its **original authorization wording** is the two verbatim quotes in its last column. Its **scope column is the bootstrap lead's enumeration (interpretation)**.
- The human's confirmation (same message as above, quoted): "I confirm that AUTH-001's enumerated bootstrap activities broadly match my original authorization: read-only origin inspection, documentation inspection, operational tests, independent review, correction of verified setup defects, and local commits." This is a human confirmation that the enumeration broadly matches. It does not widen AUTH-001, does not revive it (it stays spent at handoff) and does not cover anything beyond the six listed activities. The human said "broadly": the exact phrasing of the scope and limits columns remains the lead's wording.
- **No authorization record existed for the read-only readiness assessment** that preceded AUTH-002. It ran on the human's direct message in that session and was not entered in this register. AUTH-002 does not retroactively authorize it.

## Not yet authorized (needs a new entry from the human)
- ~~Any conceptual-design task~~: the first one is authorized by AUTH-004 (2026-10-16). Any further design task, any approval (`approved`) of a design choice, and any task beyond AUTH-004's scope still needs a new entry.
- Review/acceptance of results; reconciliation with the origin repository (a separate later authorization).
- The thesis question text (`requirements/THESIS_QUESTION.md`): still not supplied. AUTH-003 admitted supervisor excerpts E1-E9 as requirement inputs; it did not authorize filling that file, and E1 begins mid-sentence. (The 2026-10-14 excerpt intake itself is covered by AUTH-003.)
- Enabling agent teams, relaxing the Sonnet pin, extending the origin allow-list, or any web search.

## AUTH-007 verbatim human text (messages of 2026-10-17, after the Phase 1 freeze `phase1-20261017-163102`)
> i would like to delegate that to you so this what i was trying ot do here is your propes role, u should take the lead and implemnt and loop and finish this and try not to contaminate, some of the stuff in the role prompt could be outpdated understand the general idea and verfy by checking the repos
>
> i want this to be more of autonmous i have no time now to keep wathcing and doing stupid yes and no and running commands, so u can either make a strong prompt and we delegeate the task delegated to u and the state to another agent to use the FABEL API independely and finish the phases, or you do it

Lead's interpretation (not the human's words): the human delegates the coordination of the remaining phases and waives per-step confirmations. The role prompt's rule that disclosure needs an approved manifest is kept: the lead drafts a **conservative** manifest itself and records it as a lead decision, which the human may widen or narrow later. The human's messages do not authorize reading the origin repository, previous-thesis material, the restricted files, or the 2026-10-14 supervisor excerpts for the comparator, so those stay excluded. The message does not change `config/limits.json` or the guard; the lead cannot read or write outside this workspace (the guard blocks it) and therefore prepares scripts that the human starts with one command and one pasted key.

## AUTH-008 verbatim human text (message of 2026-10-17/18, after the Phase 2 freeze)
> you or the agent at thesis indepeendant can go fetch the MCPVerse v2 table?

Lead's interpretation (not the human's words): the message is a question; the lead reads it as a request that one of the two parties fetch the table, and chose to do it locally (no model summariser, no API key). It does not extend to any other web access.

## AUTH-009 verbatim human text (message of 2026-10-18)
> now i guess we should add the findings or give acces to the fable for the pdfs it wanted, and then we should run the fabel through API and make that fabel answer its judgment after revising the new findings it neededthe new data brought to it

Lead's interpretation (not the human's words): 'add the findings or give access to the pdfs' is read as permission to supply the raw PDFs (chosen to avoid anchoring the comparator on the lead's reading); the run is a fresh session that audits its frozen report, not a resumed session.

## AUTH-010 verbatim human text (message of 2026-10-19, session renamed "Thesis Policy — Scientific Director | Oct 21")
The operative sentences are quoted; the message's long role description is summarised by the register row.
> You are taking over as the **scientific director, critical research adviser and orchestrator** of my master's thesis policy-design work.
>
> The previous external review considered v3 conditionally suitable for supervisor discussion, with concerns about: D4 potentially being ordinary experimental arm selection rather than a distinctive policy contribution. Statistical ties being mistaken for demonstrated equivalence. Possible graph inconsistencies involving optional stages and bypass paths. E1's diagnostic potentially being overinterpreted as a reason to abandon the broader research problem. The missing full-exposure reference in large-catalogue regimes.
>
> These are **review hypotheses, not instructions to agree**. Independently inspect the actual documents and decide which objections hold.
>
> You are authorized to make bounded scientific corrections, improve the conceptual presentation, prepare a concise supervisor-ready explanation, and commit the resulting documents locally under the repository's authorization and provenance rules.
>
> Keep previously completed packages intact or use versioned corrections.
>
> Do not implement the policy, run scientific experiments, enter Stage 5, inspect excluded previous-thesis material, modify the original research repository, change global settings, push remotely, or authorize a new research direction on my behalf.
>
> Those require separate approval.

Lead's note (interpretation, not the human's words): the human asks for continuing adviser behaviour in this session; this entry covers the 2026-10-21 preparation only. Scientific decisions that belong to the human (margins, thesis question, Q1-Q6, which reference at large scale) are not made by the lead.
