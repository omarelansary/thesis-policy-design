# Open tasks (the lead's to-do list; not a record, not an authorization)

Started 2026-11-07 by the lead, after the human asked to save the waiting work "in a long term place" (chat message; no intake record). Read it at the start of a session, next to
`ops/STATE.md`. **When an item is finished, delete its line in the same commit as the work**, and say which commit did it in the
commit message. Nothing here authorizes anything: each item names the AUTH or decision that covers it, or says it waits for one.

Kept on `v5-p5-break-even`, with the records (WD-082 moved them here from the Linux branch, which now holds only the
Windows/Linux switch). `ops/STATE.md` section A points here.

## 1. Waiting on a condition (the lead does these when the condition is met)
- [ ] **P2b** (AUTH-031, INT-T-044; full design kept, INT-T-046): `all` against `instr` on ScaDS GLM-5.3, 2 repeats, paced at 31 s.
      Attempt 1 (tag prefix `p2b`, from 2026-11-08 20:52 UTC) stopped itself at task 6 of 30 of its first run at 23:10 UTC: two
      calls in a row timed out (each about 900 s: 300 s client timeout and two retries); the successful calls had a median of 11 s,
      a 90th percentile of 245 s and a maximum of 711 s. ScaDS showed GLM-5.3 up again at 23:12, so attempt 2 (prefix `p2b2`,
      same settings) started from task 1, so that each run is complete; attempt 1 is kept and not pooled. Attempt 2 stopped the
      same way at task 7 at 2026-11-09 03:00 UTC (60 calls in about 3.8 h). **Not restarted: waits for the human** (a longer client
      timeout is a harness change to show first; or another time of day; or a smaller design). INT-T-048: effort stays as
      served and both repeats stay. INT-T-049: ScaDS, with `--timeout 1200` (default 300 kept); attempt 3 (prefix `p2b3`)
      started 2026-11-09 about 09:05 UTC from task 1. Attempts 1 and 2 kept, not pooled.
      Attempt 3 stopped at task 5 at 13:30 UTC (two tasks in a row ended with HTTP 408 from ScaDS: each try cut at about 900 s by
      the server, so the 1200 s client timeout does not help; median call 26 s by day). Three attempts: 190 calls, 10 failed.
      INT-T-050/051: moved to OpenRouter, GMICloud fp8 pinned (`--provider`, diff approved), no spending cap (the human; key
      limit raised to $60, $31.99 left at the start), effort as served (on GMICloud it behaves like "high"; ScaDS's default is
      "max": a route difference to report), timeout 600 s. Started 2026-11-09 14:10 UTC, prefix `p2b-or`. ScaDS attempts kept, not pooled.
      Serving facts (stored 2026-11-09, `evidence/literature-20261019/p2b-scads-glm53-model-page-20261109.txt`): ScaDS runs
      `gpustack/GLM-5.3-W4A8` (4-bit weights, 8-bit activations) on 8 H100 over two nodes as an HPC Slurm job (offline between
      jobs); thinking defaults to max effort, which P2b uses (no reasoning field sent). OpenRouter's GMICloud serves fp8. Its finish line
      carries AppWorld's frozen clock (2023-05-18), not the real time. When attempt 2 ends: `design/package-v5/tools/p2_analyze.py`,
      a results file, and HYP-0018's result section updated (its status stays `proposed`).
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
