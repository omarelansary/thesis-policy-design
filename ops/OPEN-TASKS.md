# Open tasks (the lead's to-do list; not a record, not an authorization)

Started 2026-11-07 at the human's request so that waiting work is not forgotten. Read it at the start of a session, next to
`ops/STATE.md`. **When an item is finished, delete its line in the same commit as the work**, and say which commit did it in the
commit message. Nothing here authorizes anything: each item names the AUTH or decision that covers it, or says it waits for one.

Written on branch `v5-p5-break-even` (42d9ff2). When the operations branch is next updated, add a pointer to this file in
`ops/STATE.md` and bring the file across.

## 1. Waiting on a condition (the lead does these when the condition is met)
- [ ] **Operations-branch records** (branch `linux-from-v5-audit--portable-guard-and-short-state`). **Drafts ready to apply** (INT-T-040): `ops/drafts/OPS-BRANCH-RECORDS-DRAFT-20261108.md` (AUTH-028 amendment, AUTH-029 P3, AUTH-030, WD-071 to WD-075, STATE section A); ids checked free on that branch at 22e3d7d. Condition: the other agent
      says the shared folder is free. To write: AUTH-028 amendment for INT-T-026 (part A cap about 140; OpenAI repeat accepted at
      about $0.40, stop $0.60; 193 requests, $0.445; OpenAI total $0.594); WD-071 (part B results with harness revision 2, the
      proposed D-01 variant, the B2 stall, INT-T-027: D-01 kept, variant decided after part A); STATE.md update with a pointer
      here. Then run the full verifier there.
- [ ] **P3 records on the operations branch** (P3 closed 2026-11-08, INT-T-039; record in `design/package-v5/inputs/p3/P3-LOG.md`;
      $9.953 of the $10 stop): enter the P3 AUTH row (INT-T-028..039, including the run 6 ceiling of INT-T-038) and WD entries
      (runs 1-6, V5-R17 with its open items) with the other operations-branch records.
- [ ] **End-to-end study, from P3** (`05` section 3, V5-R17 open items a-c): instruction-only arm; the stop's treatment of the
      tools array (V5-R02); model differences as an input to model choice. Waits for the end-to-end authorization.

- [ ] **P2 decisions** (run done 2026-11-08, `design/package-v5/inputs/p2/RESULTS-P2-MAIN.md`, $12.69): the human decides on
      section 4 (keep the offering stage; the per-model instruction check P2b, free on ScaDS; a `04` note that declaring only the
      subset is cheaper for a subset fixed for a whole session; HYP-0018 result recorded with a status the human chooses).
- [ ] **Group 2** (INT-T-040: authorized after group 1 is complete; group 1 done at 385237a): P3 sources stored as EXT;
      end-to-end task preparation; P1 preparation. Waits for the human's word.

## 2. Waiting on the human (or Windows)
- [ ] Workbook entries listed in `design/ledger/notes/ANSWERS-20261107.md` (no openpyxl here; the human or a Windows session).
- [ ] `design/package-v5/17` section 9 (postponed by the human: "leave them as is ... postpone").
- [ ] `design/package-v5/08` section 5 proposals (rechecked without changes, as asked).
- [ ] Q-U15, Q-U25, Q-U27 (open in `design/ledger/notes/QUESTIONS-FOR-YOU-20261107.md`).

## 3. Belongs to the other agent (listed so it is not lost; the lead does not act on it)
- [ ] GLM B2 run (AUTH-026, "Finish GLM B2, then stop"): tasks 22-57, resumed from 37a8675_1. No auto-resume after a reboot;
      rerunning the same script reuses its tag (AppWorld issue #203). Whether to continue, pause or stop it is the human's call.
