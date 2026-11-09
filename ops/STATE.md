# Workspace state (imported into every session; keep under 40 lines and under 6 KB)

Earlier versions, verbatim and dated: `ops/STATE-ARCHIVE.md`. Nothing here is an authorization; read `ops/AUTHORIZATIONS.md`.

## A. Research work (V5; `v5-audit`; `v5-p5-break-even` merged into it 2026-11-09, WD-085)
- **V5 audit** (AUTH-020): conceptual package; start at `design/package-v5/00-README.md`. Working draft V5-R = DPR-0007, plus V5-R17 (provisional). Nothing is validated, approved or final. Benchmark register `17`.
- **Probes R1-R3 and GLM-5.3 on ScaDS done** (AUTH-024 to AUTH-027; results `exchange/prior-work/v5-probes/results/` and `R3-GLM/`): merged into `v5-audit` and pushed (77357c1; WD-071, WD-072).
- **P5 done** (AUTH-028): part B, OpenAI side check, $0.594 (WD-073); part A, ScaDS GLM-5.3, free: break-even between 10 and 30 tools; D-01 fits the client route; D-01 kept, D-01h added for vendor-hosted search (WD-079).
- **P3 closed** (AUTH-029): six runs, $9.953; models search uninstructed; V5-R17 adds a stop for a missing tool, provisional (WD-074 to WD-076; `design/package-v5/inputs/p3/P3-LOG.md`).
- **P2 done** (AUTH-030, AUTH-031): OpenAI, $12.69; server-enforced offering at a fixed prefix kept the cache, with no accuracy loss beyond run-to-run variation (oracle subsets, 128 tools). P2b ($5.78, OpenRouter GMICloud; ScaDS could not finish it): GLM-5.3 followed the instruction-only subset fully; HYP-0018 kept open (WD-077 to WD-080, WD-084).
- **End-to-end and P1 prepared** (AUTH-030, WD-081): 16 validated task pairs; AppWorld's natural returning users first. The end-to-end study waits for its own authorization. P4's condition not met in P2's logs (`inputs/p4/P4-CONDITION-CHECK.md`; the human decides). Slides (`v5-slides`, other session) are updated with all results at the end (INT-T-053).
- **Answers of 2026-11-07** (INT-T-023, INT-T-024; `design/ledger/notes/ANSWERS-20261107.md` on `v5-r3-part-b-results`): `17` section 9 postponed; research question entered as pointers (`requirements/THESIS_QUESTION.md`; that file and the answers file are on `v5-audit`); Executor closed for now (WD-069). Still open: the workbook (no `openpyxl` on Linux); Q-U15, Q-U25, Q-U27; the supervisor's verdict on V5 (Q-J31, Q-J32; Q-J33 only for an Executor baseline).
- **The lead's to-do list:** `ops/OPEN-TASKS.md` (not an authorization).

## B. Standing decisions of the human (details: `requirements/REGISTER.md` section H)
- Minimise the bill on average over turns and sessions, with accuracy nearly the same; no margin or budget; model-agnostic billing equation (DPR-0006).
- Headline average A, with B beside it. Estimation-only reporting (INT-T-022).
- Memory scope = memory and tool calls. A negative result is still a thesis.
- Process: research and drafted policy, then a proof-of-concept loop, then end-to-end. Earlier retrieval work stays outside.
- The university API (ScaDS) serves open-weight models only, and its proxy refuses `allowed_tools`.
- The human's `.workspace/` stays untracked and is never pushed.

## C. Operating rules
- Authorizations: AUTH-020 (V5 audit), AUTH-021 to AUTH-023 (machine portability, see D), AUTH-024 to AUTH-027 (R3 probes; done), AUTH-028 (P5; done), AUTH-029 (P3; closed), AUTH-030 (group 1 and 2, P2 preparation), AUTH-031 (P2 runs, P2b) and AUTH-033 (P1 and P4 by the lead while the human is away; the lead's limits). AUTH-032 is the deck session's (`v5-slides`).
- Run allow-listed commands alone, never chained (WD-042, WD-043). The guard allows only `git push [-u] origin v5-audit` and the same for the Linux branch; the human pushes anything else.
- Agents: evidence-steward, design-proposer, design-challenger; protocol `ops/PROTOCOL.md`.
- Research outputs go on a branch cut from `v5-audit` and reach it by merge, only when the human says so (WD-061).

## D. Machines and branches (operations only; not research)
- **Branch `linux-from-v5-audit--portable-guard-and-short-state` carries only the Windows/Linux switch** (AUTH-021 to AUTH-023: cross-platform guard and tests, verifier fix, SSH remote). Reset to 5abc9ac on 2026-11-08 (INT-T-047, WD-082): its research records (AUTH-024 to AUTH-031, WD-062 to WD-081, STATE) now live on `v5-p5-break-even`; old tip kept as `backup/linux-records-before-split-20261108`. The human force-pushes it (origin had d5ae226) and rebases it onto `v5-audit` after merges (not yet onto 77357c1).
- **The switch is not yet tested on Windows.** Before merging the Linux branch into `v5-audit`, run on Windows: `python tools/verify_workspace.py`, `python ops/tests/guard_cases.py`, `python ops/tests/finding_citation_cases.py` (WD-059).
- **Linux notes:** `python` must exist (symlink to `python3`); 224 WARN lines are expected: origin extracts cannot be re-verified there; AppWorld and the run scripts live in `~/r3-work` (outside the repository); the API keys are in `~/r3-work/.env`, which the human empties when done.
- **Open for the human:** whether Bash `git commit` should ask first again.

## Next action for any session
Read this file, run `python tools/verify_workspace.py --quick` (on `v5-p5-break-even` expect the 3 literature-summary FAILs that the Linux branch's verifier fix removes), check `ops/AUTHORIZATIONS.md`, and work only inside an AUTH.
