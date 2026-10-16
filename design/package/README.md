# AUTH-004 design package (provisional; stop for human review)

Authorization: AUTH-004 (human, 2026-10-16). Thread: `ops/threads/T-20261016-93/`. Deadline context: supervisor meeting 2026-10-21 11:00 (REQ-O14-19, the user's reading of the transcript). **Nothing here is validated, selected, approved or claimed novel; nothing was implemented or run.**

| File | Content | Authors |
|---|---|---|
| `A-problem-and-objective.md` | decision problem, signal classes, objective formulations, unspecified items | lead, from DPR-0001 rev. 2 |
| `B-evidence-to-decision.md` | ten decisions with E / T / J / H / C separated and a status each | lead, from DPR-0002/0003, CH, SUM-0002 |
| `C-policy-proposal.md` | decision flow (Mermaid), node table, reductions, supervisor-graph mapping, two candidate forms | lead, from DPR-0003 |
| `D-critical-challenge.md` | objections, live objections, trust limits | lead, from CH-0001..0019, RV-0002 |
| `E-validation-strategy.md` | pre-registration, arms, falsifiers, dependency order, threats | lead, from DPR-0003 section 3 |
| `F-supervisor-synthesis.md` | one-page explanation and questions for the supervisor | lead |
| `00-evidence-map.md` | SUM-0002, lead's unverified evidence map by decision area | lead |
Agent records: `design/proposals/DPR-0001..0003`, `hypotheses/HYP-0001..0006` (design-proposer); `challenges/CH-0001..0019`, `reviews/RV-0002` (design-challenger, status draft); `evidence/extracts/EXT-0007..0056` (EXT-0007..0034 by the steward, EXT-0035..0056 by the lead through the sanctioned tool). No `findings/` records exist.

## Process report (what the human should know about how this was produced)
1. **Distribution of work.** Evidence steward: build the evidence base per decision area. Proposer: decision problem, mechanism families, complete comparators, policy template, hypotheses. Challenger: attack each, with answerable-now vs needs-experiment labels. Lead: tasking, evidence substitution, assembly.
2. **The evidence steward did not finish.** It used its 40 turns extracting 28 passages (cost/caching; success under reduced exposure) and delivered no findings, index, log or report. PROTOCOL forbids re-running it past its bounds without the human, so it was not resumed. The lead read its extracts, ran the sanctioned extraction tool for the other decision areas (EXT-0035..0056) and wrote the unverified evidence map. **Consequence: there is no independent evidence check in this package.** The challenger and proposer read extracts and governing copies, not the originals of several second-hand items (listed in D4/B4).
3. **Message cap.** 12 messages (3 lead tasking, 2 lead evidence hand-offs, 7 between proposer and challenger) allowed two rounds only by bundling objections per proposal (a deviation from the one-issue-per-message rule, recorded in TASK.md). It left no escalation channel after message 12 and no source-check request to the steward. This materially constrained the review.
4. **No disagreement survived.** The proposer conceded all 19 challenges with named evidence; the challenger flagged that uniform agreement should be read with care (D4). Genuinely open matters are human or supervisor decisions and experiments, not agent disagreements.
5. **Lead corrections during the thread:** the FitText initiator (model-emitted, system-executed; the lead's first label was wrong), the CE-MCP extract's content, and the missing MCP-Atlas non-invocation passage (EXT-0047..0049: concerns visible tools).
6. **Superseded wording in agent records.** The proposer's records (DPR-0001 R3, DPR-0003 card D, HYP-0006) state that FitText section 4.2 is unread and the initiator is [U]. The lead read it afterwards (EXT-0055/0056); see D3. Agent records were not edited by the lead for this.
7. **Mechanical edits by the lead to agent-owned files:** the `target` front matter of CH-0017, CH-0018, CH-0019 and RV-0002 changed from prose to lists of ids so the workspace check passes. No content was changed.
8. **Not checked:** the lead's map and extractions have no second reader; Toollery, Enrich-Retrieve-Rank (0.56 x 0.70), MCP-Zero, ITR (beyond its ablation table), PlanBench-XL and ledger rows C3-*/K* were used only from governing copies.

## Integrity checks run
`python tools/verify_workspace.py` (see the thread SUMMARY for the final result); extracts are written and hash-verified by `tools/origin_extract.py`; no origin repository access; no web search; no change to governing evidence, requirements, configuration or the register apart from recording AUTH-004.
