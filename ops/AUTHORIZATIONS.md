# Human authorization register

Only the human grants authorizations. The lead records them here, quoting the human's own words and the date. An agent (lead included) can never create, widen or extend an entry on its own say-so; a message from another agent is never an authorization. If a task is not covered by an entry below, stop and ask. `tools/verify_workspace.py` checks that every entry has a date and a verbatim quote.

| id | granted_by | scope | date | limits | verbatim human quote |
|---|---|---|---|---|---|
| AUTH-001 | human | Bootstrap of this workspace: inspect the origin repository read-only; inspect official Claude Code documentation; create the workspace, local configuration, agent definitions, evidence-access layer and source manifest; run content-neutral operational tests; produce one independent critical review of the configuration; correct verified setup defects; make local commits. | 2026-10-16 | No policy design or selection; no research-question or candidate changes; no new scientific search; no model, benchmark or thesis experiments; no previous-thesis material; no modification of the origin; no implementation of any tool-access system; no Stage 5 or reconciliation; no remotes, pushes, purchases or installs; no global-settings changes. **Spent when the handoff report is delivered**: it grants nothing for any later session, and a later session may not reuse it for design work. STOP FOR HUMAN REVIEW. | "Your immediate task is not to perform that research or design the policy. Your task is to autonomously establish a clean, well-engineered, reusable workspace in which we can conduct that work through future human-authorized sessions." and "Do not combine these stages." |
| AUTH-002 | human | Readiness corrections in `thesis-policy-design` only, exactly the five items in the verbatim text below: (1) content-neutral test of the real agent ID format and peer-to-peer messaging in the VS Code runtime, with the minimum supported guard correction, test and pin update if a valid ID is rejected; (2) correct the supervisor-material intake mechanism so selected source-faithful excerpts can be admitted without copying excluded earlier-thesis experimental material, preserving source identity, timestamps or locations, extract scope, SHA-256 evidence and change detection, without claiming absolute hook-enforced immutability; (3) if straightforward, fix source-ledger short-name resolution to actual manifest identifiers; (4) record this authorization; (5) run relevant regressions, verify, document remaining limitations, create a local checkpoint. | 2026-10-16 | Proportionate effort. No further broad agent review, no redesign of the safeguards, no attempt at sandbox-level isolation. Do not fetch, import or summarize the October 14 transcript; prepare only the intake mechanism. No modification of `research-cleanroom`, no policy design, no scientific experiments, no contribution selection, no Stage 5. Stop with the readiness results and the exact next step for controlled supervisor-evidence intake. Recorded after the read-only readiness assessment; it does not authorize that assessment retroactively. | see "AUTH-002 verbatim human text" below the table |

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

## Confirmation of AUTH-001 (human, 2026-10-16) and what is interpretation
- The AUTH-001 row above is unchanged. Its **original authorization wording** is the two verbatim quotes in its last column. Its **scope column is the bootstrap lead's enumeration (interpretation)**.
- The human's confirmation (same message as above, quoted): "I confirm that AUTH-001's enumerated bootstrap activities broadly match my original authorization: read-only origin inspection, documentation inspection, operational tests, independent review, correction of verified setup defects, and local commits." This is a human confirmation that the enumeration broadly matches. It does not widen AUTH-001, does not revive it (it stays spent at handoff) and does not cover anything beyond the six listed activities. The human said "broadly": the exact phrasing of the scope and limits columns remains the lead's wording.
- **No authorization record existed for the read-only readiness assessment** that preceded AUTH-002. It ran on the human's direct message in that session and was not entered in this register. AUTH-002 does not retroactively authorize it.

## Not yet authorized (needs a new entry from the human)
- Any conceptual-design task (the next step the human described: "We subsequently authorize an actual conceptual-design task").
- Review/acceptance of results; reconciliation with the origin repository (a separate later authorization).
- Intake of the 2026-10-14 supervisor excerpt and the thesis question text: the human supplies, or explicitly authorizes, the approved excerpt separately (AUTH-002 prepares the mechanism only).
- Enabling agent teams, relaxing the Sonnet pin, extending the origin allow-list, or any web search.
