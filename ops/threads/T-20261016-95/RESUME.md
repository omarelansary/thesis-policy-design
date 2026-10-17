# T-20261016-95 / AUTH-006 RESUME note (lead; task IN PROGRESS until SUMMARY.md exists)

Authority: AUTH-006 (verbatim in `ops/AUTHORIZATIONS.md`). Bounded revision; stop for human review at the end. Readiness check passed at session start (608 pass, 0 fail, no override file).

## Done and committed
- `design/package-v3/01-errata-AUTH-005.md` (five corrections + working objective C_tok; counterexample computed by the lead; Toollery fit re-checked).
- `design/package-v3/02-supervisor-decision-graph.md` (graph G: design nodes D1-D4, run nodes R1-R6; stages optional; D4 = pre-registered dev rule; C-B parts conditional).
- `design/package-v3/03-comparison.md` (G vs C-A vs expose-all vs vendor deferral; C-A demoted to component and comparator; C-B not adopted).
- Thread T-20261016-95: TASK.md; ACTIVE.json (cap 12); one challenger (id lost if session ends) tasked with 1 lead message to attack 01-03 and write CH-0035+ and RV-0004.

## Remaining
1. Collect the challenger's final report (files: `challenges/CH-0035..`, `reviews/RV-0004.md`, log `ops/threads/T-20261016-95/design-challenger.md`). If it is gone/incomplete, record it as incomplete; do not re-run past bounds.
2. Respond to each objection in `design/package-v3/04-objections-and-experiments.md` (ACCEPT / PARTIAL / REJECT with reasons; fix 01-03 where the objection shows an error; keep real disagreements; optionally ONE round-2 lead message to the challenger).
3. Write `04-objections-and-experiments.md` (strongest remaining objections, answerable-now vs needs-experiment, experiments in dependency order) and `05-presentation-outline.md` (concise, for 2026-10-21; questions for the supervisor).
4. Consistency check across package-v3 and against v2 (superseded statements listed in 01 sections 1-6); full `python tools/verify_workspace.py` (0 FAIL); delete `ops/threads/ACTIVE.json`; write thread `SUMMARY.md`; update `ops/STATE.md` and `ops/DESIGN-DECISIONS.md` (WD-019); commit; report; STOP.

## Rules
Produce only the five outputs. No threshold/stage/benefit/novelty invented. C-B not automatically adopted. Do not claim the policy is validated or final. Earlier packages unchanged. Avoid writing the name of the local-override file in shell commands or commit messages (the guard blocks that string).
