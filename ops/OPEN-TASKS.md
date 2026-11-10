# Open tasks (the lead's to-do list; not a record, not an authorization)

Started 2026-11-07 by the lead, after the human asked to save the waiting work "in a long term place" (chat message; no intake record). Read it at the start of a session, next to
`ops/STATE.md`. **When an item is finished, delete its line in the same commit as the work**, and say which commit did it in the
commit message. Nothing here authorizes anything: each item names the AUTH or decision that covers it, or says it waits for one.

Kept on `v5-p5-break-even`, with the records (WD-082 moved them here from the Linux branch, which now holds only the
Windows/Linux switch). `ops/STATE.md` section A points here.

## 1. Waiting on a condition (the lead does these when the condition is met)
- [ ] **P1 and P4 under AUTH-033 (the lead, human away).** Done: P1 step A (`inputs/p1/P1-PREP.md` section 7), P4 step A
      (`inputs/p4/P4-REPLAY-A.md`). **Running since 2026-11-10 00:22 / 00:40 UTC:** P1 step B (`tools/p1_memory.py`; runs
      `p1-main-glm-5.3-{none,pop6}-r{1,2}` in `inputs/p1/local/runs/`, $3 cap each; oracle arm dropped for cost) and P4 step B
      (`p2_offering.py --mask 30000,3,5000`; runs `p4-mask-glm-5.3-r{1,2}` in `inputs/p2/local/runs/`, $2.50 cap each; P2b's
      `all` runs are the keep arm). When they end: analyse (`p2_analyze.py`, `p2_paired.py`, per-session P1 counts), results
      files, HYP-0017/HYP-0021 result sections (status unchanged), WD entry, STATE.
- [ ] **End-to-end study, from P3 and the preparation** (`05` section 3; V5-R17 open items a-c; `inputs/e2e/E2E-TASKS-DESIGN.md`):
      instruction-only arm; the stop's treatment of the tools array (V5-R02); model differences as an input to model choice; the
      run without "The task is doable" on the unchanged tasks. Waits for the end-to-end authorization.

## 2. Waiting on the human (or Windows)
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
