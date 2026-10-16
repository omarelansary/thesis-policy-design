# Proposed first session (NOT executed; for the human to adopt, change or discard)

Nothing here is authorized until you write it into `ops/AUTHORIZATIONS.md` (or tell the lead the exact words to quote). The lead cannot do this step for you.

## Before the session (human)
1. Put the thesis question text and the 2026-10-14 supervisor instructions where you want them used: save them as files in `requirements/intake/` following `requirements/intake/README.md` (source, date, who supplied it, verbatim or paraphrased, and that they are *requirements/inputs, not findings of the earlier independent research*). Then say so in the session; the lead records them in `requirements/REGISTER.md` with REQ ids and in `requirements/THESIS_QUESTION.md`.
2. Decide the scope of the first conceptual-design task and its limits. Suggested AUTH wording to adapt (all numbers are yours to choose; none are proposed here):
   > AUTH-002: Conceptual design task "<name>". Scope: <what the three agents may produce: e.g. design proposals and challenges for <topic>, no selection>. Evidence they may use: governing copies, stored sources by id, extracts. Limits: agents = 3; rounds per issue = <n>; messages per thread = <n>; web searches = <0 or n>; <other>. Out of scope: question selection, final policy, implementation, experiments, reconciliation.

## Session steps (lead)
1. Open the workspace (README.md, "Open"). Read `ops/STATE.md`; run `python tools/verify_workspace.py --quick`; expect `fail=0` and stop otherwise.
2. Confirm AUTH-002 exists and quote its scope back to the human in one sentence.
3. Create the thread (`ops/PROTOCOL.md` steps 1-4): TASK.md, `ops/threads/ACTIVE.json` (the guard refuses all messages without it and counts them against the cap), three standby agents, roster + tasking. Plan the debated issues to the message budget.
4. Suggested first thread shape (a *process* suggestion only): evidence-steward extracts and labels the passages relevant to the task (EXT ids, limits stated); design-proposer writes option proposals each with a falsifier; design-challenger attacks them; escalations go to the human unaveraged.
5. Close: SUMMARY.md, update STATE.md, run full verify, stop for review. No reconciliation with the origin, no question selection, no implementation.

## What a fresh session should refuse
Any design work without an AUTH; any selection of the thesis question or policy; any read of the origin outside `tools/origin_extract.py`; any claim that an agent or message "approved" something.
