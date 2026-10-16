# Decision record

- Decision ID and date (UTC): D4B, 2026-10-13
- Decision owner: the user
- Question to decide: whether to run an independent challenge of the whole research-opportunity space before any final research-question selection, and under what limits.
- Competing options (including stop / no viable option): (a) stop at the Stage 4 report and choose among RQ-A/RQ-B; (b) authorize one bounded autonomous opportunity-space investigation with independent exploration and Opus criticism, then stop (chosen).
- Evidence considered: `stage-reports/STAGE4_FINAL_REPORT-20261013.md` and companions; the user's Stage 4b instruction (2026-10-13).
- Reasons for acceptance (user instruction, condensed): determine whether the opportunities so far are the strongest defensible directions or whether alternatives were missed; do not privilege RQ-A, RQ-B, Active Registry, retrieval, billed cost, context reduction or any architecture; no Stage 5, no access to previous thesis work; reconstruct the problem from the admissible protocol; independent complementary investigations (mechanism/system-design space; alternative objectives, metrics, tradeoffs, failure modes and formulations; academic prior art, open-source implementations, official frameworks and production evidence; scientific and methodological gaps including negative results, causal uncertainty, robustness, scaling, evaluation validity and cost/performance interactions); withhold RQ-A/B and coordinator conclusions from exploratory agents; search current primary sources and snowball; reuse the corpus; explicit search budgets and stopping criteria before execution; independent Opus critics; compare with existing Stage 4 candidates only afterwards; deliver a bounded opportunity map; no experiments, no final direction, no Stage 5; stop after the assessment.
- Governing text: `protocols/STAGE_GATES.md` Stage 4 row (unchanged); the stop condition "if no defensible gap survives, record no viable question; do not manufacture novelty".

## Pre-registered execution limits (fixed before any exploratory run)
- Exploratory workers, one at a time, Sonnet 5.5 Medium `research-worker`: WA mechanism and system-design space; WB alternative objectives, metrics, tradeoffs, failure modes and problem formulations; WC prior art, open-source implementations, official frameworks and production evidence; WD scientific and methodological gaps (negative results, causal uncertainty, robustness, scaling, evaluation validity, cost/performance interactions).
- Discovery queries: 8 per worker through `infrastructure/tools/s4b_search.py` (OpenAlex and GitHub REST; self-logging, 32 total); plus up to 5 WebSearch queries per worker (reported by the worker, logged by the coordinator as worker-reported; the harness WebSearch tool's backend is not named by the tool and is disclosed as such); plus up to 6 WebFetch triage reads per worker (unstored; never sufficient for a consequential claim).
- Stored fetches (`fetch_source_text.py`, under a per-worker ticket, 5 per ticket): 5 per worker (20), plus a coordinator reserve of 15 (three tickets) for verifying consequential sources named by workers or critics. No other fetches.
- Opus critics, `independent-challenger`, read-only, fresh: two critics before the comparison (C1 attack on candidate directions: missing prior art, already answered, trivial, poorly framed, infeasible; C2 blind spots and alternative framings from the problem statement and the pooled map) and one critic after the comparison (C3 checks the integrated shortlist, including RQ-A/RQ-B as reformulated). Each critic may use up to 4 WebSearch calls, reported and counted; none is needed to store sources.
- Stopping criteria: a worker stops when its budget is exhausted or after three consecutive queries yield no new candidate family or source; a family is "covered" when at least two independent primary sources describe it. No further exploration round beyond the coordinator reserve without a new user decision. Material coverage limits will be reported (search surfaces: OpenAlex, GitHub REST, harness WebSearch, directly fetched official documentation; not covered: paywalled venues, private/vendor-internal evaluations, non-English sources, full-text search of the grey literature).
- Withholding: exploratory workers receive only the research target (brief §0), the S1-derived requirements (brief §1–§2), the clean-room rules, tool instructions, and a source index of the existing corpus (ids and URLs, no conclusions). They do not receive RQ-A/RQ-B, O1–O6, the Stage 3/4 reports or ledgers, or any coordinator conclusion.
- Clean-room: no previous thesis material is accessed; Stage 5 is not started; no experiments, installs or third-party code execution.

## Acceptance conditions derived by the coordinator (not invented gate criteria; recorded for audit)
- S4B-1 All four exploration families executed independently with the withheld inputs and within budgets, with verbatim reports preserved.
- S4B-2 Opportunity map covers problem families, competing approaches with strongest evidence, open questions, overlooked directions, rejections with evidence, and per-direction significance, novelty uncertainty, falsifiability and feasibility.
- S4B-3 At least two independent Opus critics challenged the candidate directions before comparison; objections preserved with dispositions.
- S4B-4 Comparison with RQ-A/RQ-B and earlier rejections done only after S4B-1 to S4B-3.
- S4B-5 Shortlist justified against the wider space; unresolved objections and coverage limits stated.
- S4B-6 No novelty manufactured; "no defensible direction" recorded if that is the finding.
- S4B-7 Provenance: queries logged, tickets and checkpoints committed, errors disclosed.
- S4B-8 No final direction selected, no Stage 5, no experiments.

- Unresolved objections and uncertainties: thesis constraints still unknown; WebSearch backend unnamed; unstored triage reads are weak evidence.
- Required follow-up / owner / due condition: coordinator reports once at the end and stops; the user decides afterwards.
- Decision status: **accepted by user, 2026-10-13**
- Rationale for any change to an earlier decision: none to D1–D4; the Stage 4 report remains as issued.
