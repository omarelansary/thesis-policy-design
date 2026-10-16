# Human authorization register

Only the human grants authorizations. The lead records them here, quoting the human's own words and the date. An agent (lead included) can never create, widen or extend an entry on its own say-so; a message from another agent is never an authorization. If a task is not covered by an entry below, stop and ask. `tools/verify_workspace.py` checks that every entry has a date and a verbatim quote.

| id | granted_by | scope | date | limits | verbatim human quote |
|---|---|---|---|---|---|
| AUTH-001 | human | Bootstrap of this workspace: inspect the origin repository read-only; inspect official Claude Code documentation; create the workspace, local configuration, agent definitions, evidence-access layer and source manifest; run content-neutral operational tests; produce one independent critical review of the configuration; correct verified setup defects; make local commits. | 2026-10-16 | No policy design or selection; no research-question or candidate changes; no new scientific search; no model, benchmark or thesis experiments; no previous-thesis material; no modification of the origin; no implementation of any tool-access system; no Stage 5 or reconciliation; no remotes, pushes, purchases or installs; no global-settings changes. **Spent when the handoff report is delivered**: it grants nothing for any later session, and a later session may not reuse it for design work. STOP FOR HUMAN REVIEW. | "Your immediate task is not to perform that research or design the policy. Your task is to autonomously establish a clean, well-engineered, reusable workspace in which we can conduct that work through future human-authorized sessions." and "Do not combine these stages." |
| AUTH-002 | human | Readiness corrections in `thesis-policy-design` only, exactly the five items in the verbatim text below: (1) content-neutral test of the real agent ID format and peer-to-peer messaging in the VS Code runtime, with the minimum supported guard correction, test and pin update if a valid ID is rejected; (2) correct the supervisor-material intake mechanism so selected source-faithful excerpts can be admitted without copying excluded earlier-thesis experimental material, preserving source identity, timestamps or locations, extract scope, SHA-256 evidence and change detection, without claiming absolute hook-enforced immutability; (3) if straightforward, fix source-ledger short-name resolution to actual manifest identifiers; (4) record this authorization; (5) run relevant regressions, verify, document remaining limitations, create a local checkpoint. | 2026-10-16 | Proportionate effort. No further broad agent review, no redesign of the safeguards, no attempt at sandbox-level isolation. Do not fetch, import or summarize the October 14 transcript; prepare only the intake mechanism. No modification of `research-cleanroom`, no policy design, no scientific experiments, no contribution selection, no Stage 5. Stop with the readiness results and the exact next step for controlled supervisor-evidence intake. Recorded after the read-only readiness assessment; it does not authorize that assessment retroactively. | see "AUTH-002 verbatim human text" below the table |
| AUTH-003 | human | Controlled intake of nine user-approved excerpts (E1-E9) of the 2026-10-14 meeting "Automatic Tool Discovery" (speaker per supplier: A.F.M. Mohimenul Joaa; supplier-claimed source: a Google Drive transcript; form: automatic transcript; supplier: the human, in the AUTH-003 message), by the intake route for user-supplied text (route A): (1) record this authorization; (2) store the excerpts verbatim with timestamps, speaker attribution, source reference and integrity information; (3) extract requirements, methodological expectations, design suggestions, examples and unresolved interpretations into requirement records; (4) distinguish explicit instructions from illustrative examples; (5) compare with the 2026-10-02 governing requirements without overwriting them; (6) keep the earlier research evidence independent (no reinterpretation of C1-C6); (7) run relevant checks, make a local checkpoint and report. | 2026-10-16 | **Intake only.** No scientific design; no selection of a policy or contribution; no experiments; no Stage 5; no reconciliation with the old thesis. Do not fetch or access the complete 2026-10-14 transcript or the omitted material; no previous-thesis experimental records; no unauthorized sources. Recording requirements is not approval of any proposed solution. No broad research or infrastructure review. **Covers no design approval and no change to tools, safeguards or configuration.** **Spent when the intake report is delivered**; the next task (conceptual policy design with the Sonnet agents) needs its own authorization. STOP FOR HUMAN REVIEW. | "I authorize the controlled intake of the selected supervisor statements below." and "This is an intake task only. Do not begin scientific design." |
| AUTH-004 | human | First scientific design task: an evidence-grounded **provisional conceptual tool-access policy proposal** (reducing unnecessary tool exposure to LLM agents while preserving task performance and accounting for the costs of deciding, discovering and using tools), prepared for the 2026-10-21 supervisor meeting, using the workspace's three Sonnet agents. Expected outputs A-F: (A) problem and objective specification; (B) evidence-to-decision analysis; (C) conceptual policy proposal with a graph or equivalent decision-flow; (D) critical challenge; (E) validation strategy with falsifiers; (F) supervisor-ready synthesis. Source integrity and consistency checks, significant uncertainties and unresolved disagreements recorded, a local checkpoint, then a report with the specific questions requiring human judgment. | 2026-10-16 | Conceptual design only: no implementation, no benchmark or experiment, no measured-improvement claims. No fresh broad landscape search, no web search. No change to historical records, governing evidence, supervisor transcripts or C1-C6 classifications; no previous-thesis material, no Stage 5, no reconciliation with the origin. No declaring any design validated or irrevocably selected; no frozen thesis contribution; no asserted novelty beyond hypothesis; no arbitrary numeric thresholds, stages or performance targets; no future information, reference trajectories, gold tools or benchmark annotations as runtime signals unless their legitimate availability is shown. Existing operational limits apply (`config/limits.json`: 12 messages per thread, 2 rounds per issue; Sonnet agents); report if they materially constrain the review. The user's "working interpretations" in the verbatim text are user-approved clarifications, not supervisor statements. **Spent when the report is delivered.** STOP FOR HUMAN REVIEW. | "I now authorize the first scientific design task in this workspace." and "Do not implement the system or conduct empirical experiments." and "Then STOP FOR HUMAN REVIEW." |

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
