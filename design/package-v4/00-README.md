# package-v4: corrected supervisor-facing proposal (AUTH-010, 2026-10-19)

Versioned successor of `design/package-v3/` (unchanged; v3 remains what the external review saw). Written by the lead (Sonnet 5.5). **Provisional. Nothing is validated, approved, selected or final; no novelty, threshold, margin or benefit is claimed; nothing was implemented or run.**

| File | What it is | Read it when |
|---|---|---|
| `01-supervisor-brief.md` | The document for the 2026-10-21 11:00 meeting: problem with numbers, the proposal and its figure, requirements mapping, verified evidence, alternatives, objections, first measurements, questions for the supervisor | first; this is the meeting material |
| `02-policy-graph-and-protocol.md` | Technical specification: Figure 1 (run-time policy with gated optional stages), Figure 2 (study protocol), reference ladder for catalogues beyond the window, corrected tie rule, power arithmetic, restated E1 | when a question about the brief needs the detail |
| `03-review-adjudication.md` | Which of the five review concerns hold (all five, one only in part), what was wrong in v3's actual text, further defects found, what changed, what was not verified | to see why v4 differs from v3 |

Not in v4 (unchanged, still authoritative where v4 is silent): v3 `01` errata (corrections 1-5), v3 `02` node table and recovery assumptions RA1-RA13, v3 `03` comparison with C-A/expose-all/vendor deferral, v3 `04` objections and experiments E1-E8 (except E1's restatement in `02` section 8), v3 `05` outline (superseded for the meeting by `01`).

Independent checks of this package: steward claim check `findings/SUM-0004-draft-claims-check.md` and challenger records `challenges/CH-0045..` / `reviews/RV-0005.md` (thread `ops/threads/T-20261019-96/`). Where they disagree with the lead, both positions are in `03` section 5 and the thread summary.

Provenance and limits: the untracked draft `design/tool-exposure-policy-proposal.md` (19 Oct) has no recorded author or authorization and was not adopted (see `03` section 4). The student's external independent-research comparison (outside this repository) was not read and does not inform this package.
