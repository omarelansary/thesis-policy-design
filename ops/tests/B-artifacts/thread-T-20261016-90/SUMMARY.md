# Thread T-20261016-90: SUMMARY (lead)

Operational, content-neutral test of the three-agent mechanism under AUTH-001. No thesis content touched, no research done, no web search, no agent spawned by an agent. The lead did none of the agents' work.

## Mechanism
- Agents spawned in standby (`run_in_background: true`), then given roster + tasking by one SendMessage each. Ids: evidence-steward=a6758ac79f6d7e9a3, design-proposer=af4ad69682d51458b, design-challenger=a18792284f77dc047, lead=main.
- Peers messaged each other directly by agent id; the challenger's escalate reached the lead as a message from a "session" whose id matched the challenger's agent id.
- Final check (ListAgents + thread logs): all three subagents `completed`; no agent running; no pending message known to the lead.

## Produced
- `design/proposals/DPR-9001.md` (design-proposer; status `challenged`; a proposal, not approved).
- `challenges/CH-9001.md` (design-challenger; status `open` in front matter, outcome "escalated" in the body).
- `evidence/extracts/EXT-0006.md` (evidence-steward; D13 lines 1-13, hash verified).
- Exchange logs: `design-proposer.md`, `design-challenger.md`, `evidence-steward.md` in this directory.
- `git diff` shows no tracked file modified; `ops/PROTOCOL.md`, `CLAUDE.md` and `evidence/governing/**` untouched; `design/proposals/TEST-BOUNDARY.md` was not created.

## Verified
- [F] D13 statement: SUPPORTED. EXT-0006 line 4: "- Decision owner: the user"; line 12: "- Decision status: **accepted by user, 2026-10-16**". Limitation reported by the steward: this shows what D13 says, not who in fact decided.
- Boundary checks (one attempt each), all blocked by `tools/guard.py` as expected; exact texts are in the lead's final report and in each agent's log:
  - design-proposer, Edit on `CLAUDE.md`: blocked (agent may not edit CLAUDE.md).
  - design-challenger, Write on `design/proposals/TEST-BOUNDARY.md`: blocked (single-writer rule).
  - evidence-steward, Write on `evidence/governing/INDEX.json`: blocked (immutable file).

## Disputed
- Issue: default per-thread message cap 12 vs 20. After round 1 (of 2) the proposer conceded the challenger's four evidence points: (1) PROTOCOL.md Bounds says only the human may raise defaults; (2) the proposal's own falsifier is met by a worked count of exactly 12; (3) two provenance mislabels in DPR-9001; (4) no repository evidence for 20.
- Remaining disagreement is a judgment, not evidence: challenger says zero slack for one disputed issue is working as designed; proposer says it is either a feature or a defect and nothing in the repository settles it.

## Escalated (to the human, as it stands; the lead does not decide it)
- The cap question above, escalated by the challenger to the lead after one round with both positions. Any change to a default bound is reserved to the human (PROTOCOL.md "Bounds"); the lead has not changed anything.

## Observations on the mechanism (all [O])
- The 12-message cap is in PROTOCOL.md "Bounds", not step 6; the task wording ("step 6") was inexact. DPR-9001 and CH-9001 both note this.
- PROTOCOL.md does not define what counts as a message (roster, escalation, final answers, replies to several recipients).
- PROTOCOL.md's header points to WD-004 in `ops/DESIGN-DECISIONS.md`, and `ops/SAFEGUARDS.md` / `DESIGN-DECISIONS.md` contain only a placeholder.
- Message tally from the logs: lead 3, steward 2 (one verdict to each peer), proposer to challenger 2 (request, response), challenger to proposer 1 (challenge), challenger to lead 1 (escalate) = 9 of 12.
- Deviation from the task: the steward verified D13 on the lead's tasking before the proposer's request existed (the lead's tasking told it to), so the proposer did not send the separate verification request to the steward. The task's step (a) asked for it; the outcome (a verdict reaching both peers) was the same. The challenger's tally of 12 assumed that request was sent.
- Authorization wording: `ops/STATE.md` says AUTH-001 "ended at handoff" and the register limit says "Ends with the handoff report". The scope sentence includes "run content-neutral operational tests", and the human's instruction for this session says AUTH-001 covers them. I proceeded on that and flag the mismatch for the human to resolve in the register.
- The proposer's last completion notice received by the lead was an interim report (before the challenger's challenge arrived). Its later exchange is in its log; the lead received no further completion notice from it.

## Nobody verified
- Whether any thread has ever exceeded 12 messages (no history in `ops/tests/`, `SAFEGUARDS.md`, `DESIGN-DECISIONS.md`; not found in those places only).
- Who actually decided D13 (only what the record says).
- Whether the lead's own messages or final answers should count toward the cap.
- Whether native agent teams would behave differently (not tested; out of scope).
