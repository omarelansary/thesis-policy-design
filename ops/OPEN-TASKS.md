# Open tasks (the lead's to-do list; not a record, not an authorization)

Started 2026-11-07 at the human's request so that waiting work is not forgotten. Read it at the start of a session, next to
`ops/STATE.md`. **When an item is finished, delete its line in the same commit as the work**, and say which commit did it in the
commit message. Nothing here authorizes anything: each item names the AUTH or decision that covers it, or says it waits for one.

Written on branch `v5-p5-break-even` (42d9ff2). When the operations branch is next updated, add a pointer to this file in
`ops/STATE.md` and bring the file across.

## 1. Waiting on a condition (the lead does these when the condition is met)
- [ ] **P5 part A on ScaDS GLM-5.3** (AUTH-028; cap about 140 requests, INT-T-026). Condition: GLM B2 has ended ("wait if GLM is
      still running ... the api might be overloaded"). Command: `python3 design/package-v5/tools/p5_break_even.py --route scads
      --model zai-org/GLM-5.3 --sessions 2 --warm-sessions 1 --max-requests 140 --out design/package-v5/inputs/p5/scads-glm53`,
      then `tools/p5_analyze.py` on its log; scan outputs for key material before commit. Status 2026-11-07 16:03 UTC: B2 nearly
      stalled (1 of 36 tasks since 13:55, repeated 900 s timeouts).
- [ ] **Operations-branch records** (branch `linux-from-v5-audit--portable-guard-and-short-state`). Condition: the other agent
      says the shared folder is free. To write: AUTH-028 amendment for INT-T-026 (part A cap about 140; OpenAI repeat accepted at
      about $0.40, stop $0.60; 193 requests, $0.445; OpenAI total $0.594); WD-071 (part B results with harness revision 2, the
      proposed D-01 variant, the B2 stall, INT-T-027: D-01 kept, variant decided after part A); STATE.md update with a pointer
      here. Then run the full verifier there.
- [ ] **D-01 revision decision** (INT-T-027). Condition: part A results are in. Put part A's comparison with D-01 and the
      proposed variant (`design/package-v5/calc/regime_bill_hosted.py`) to the human; the human decides.
- [ ] **P3 record and decision** (runs 1 to 4 done 2026-11-07/08, `design/package-v5/inputs/p3/RESULTS-P3-RUN1.md` to
      `RESULTS-P3-RUN4.md`; $7.786 of $10): enter the P3 AUTH row (INT-T-028..036) and WD with the operations-branch records; option (a)
      done (INT-T-036, `RESULTS-P3-REPLAY-A.md`): DRY survives the replay; the human decides on run 5 (plain against DRY, about
      $1.40 of the $2.21 left); keep `design/package-v5/inputs/p3/P3-LOG.md` up to date with every run and decision.

## 2. Waiting on the human (or Windows)
- [ ] Workbook entries listed in `design/ledger/notes/ANSWERS-20261107.md` (no openpyxl here; the human or a Windows session).
- [ ] `design/package-v5/17` section 9 (postponed by the human: "leave them as is ... postpone").
- [ ] `design/package-v5/08` section 5 proposals (rechecked without changes, as asked).
- [ ] Q-U15, Q-U25, Q-U27 (open in `design/ledger/notes/QUESTIONS-FOR-YOU-20261107.md`).

## 3. Belongs to the other agent (listed so it is not lost; the lead does not act on it)
- [ ] GLM B2 run (AUTH-026, "Finish GLM B2, then stop"): tasks 22-57, resumed from 37a8675_1. No auto-resume after a reboot;
      rerunning the same script reuses its tag (AppWorld issue #203). Whether to continue, pause or stop it is the human's call.
