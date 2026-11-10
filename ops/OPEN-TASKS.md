# Open tasks (the lead's to-do list; not a record, not an authorization)

Started 2026-11-07 by the lead, after the human asked to save the waiting work "in a long term place" (chat message; no intake record). Read it at the start of a session, next to
`ops/STATE.md`. **When an item is finished, delete its line in the same commit as the work**, and say which commit did it in the
commit message. Nothing here authorizes anything: each item names the AUTH or decision that covers it, or says it waits for one.

Kept on `v5-p5-break-even`, with the records (WD-082 moved them here from the Linux branch, which now holds only the
Windows/Linux switch). `ops/STATE.md` section A points here.

## 1. Waiting on a condition (the lead does these when the condition is met)
- [ ] **End-to-end study, from P3 and the preparation** (`05` section 3; V5-R17 open items a-c; `inputs/e2e/E2E-TASKS-DESIGN.md`):
      instruction-only arm; the stop's treatment of the tools array (V5-R02); model differences as an input to model choice; the
      run without "The task is doable" on the unchanged tasks. Waits for the end-to-end authorization.

## 2. Waiting on the human (or Windows)
- [ ] **Raw records backup (AUTH-035, WD-089):** archives and key are ready (`~/r3-work/raw-records-backup/`, `~/r3-work/raw-records-backup.KEY`). Your steps are in
      `design/package-v5/tools/raw_backup/README.md`: copy the key to a safe place; install git-lfs; review `PROPOSED.gitattributes` and re-pin; add the
      archives; push `v5-raw-records-backup`; fresh-clone test; Drive upload (not the key); tell the lead the results.
- [ ] **Answer the analysis questions** (AUTH-034; artifact https://claude.ai/artifact/DmcYSDBuCxEgyq52wBkjDR, section "Questions for you"):
      P4 on long tasks or parked; P1 choices (per-user memory live, synthetic users); discovery form for the end-to-end study;
      university API or OpenRouter; models; HYP-0019; review of the lead's AUTH-033 limits.
- [ ] **Push** (INT-T-047, WD-082): `v5-p5-break-even` (the research records now live here, with the P5, P3 and P2 work), and
      force-push the Linux branch, reset to 5abc9ac (administrative only; origin has d5ae226). Its rebase onto `v5-audit` 77357c1 is
      still to do (WD-072). The human pushes.
- [ ] **End-to-end and P1 decisions** (`E2E-TASKS-DESIGN.md` section 5; `P1-PREP.md` section 3): whether the bill and accuracy arms
      keep AppWorld's prompt as shipped; which tasks; the form of "removed"; P1's construction, arms and measures.
- [ ] Workbook entries listed in `design/ledger/notes/ANSWERS-20261107.md` (no openpyxl here; the human or a Windows session).
- [ ] `design/package-v5/17` section 9 (postponed by the human, INT-T-023 on `v5-audit`: "leave them as is ... postpone").
- [ ] `design/package-v5/08` section 5 proposals (rechecked without changes, as asked).
- [ ] Q-U15, Q-U25, Q-U27 (open in `design/ledger/notes/QUESTIONS-FOR-YOU-20261107.md`).

## 3. Belongs to the other agent (listed so it is not lost; the lead does not act on it)
- (nothing open; GLM B2 finished 2026-11-08, WD-071)
