# Workspace state (imported into every session; keep under 40 lines and under 6 KB)

Earlier versions, verbatim and dated: `ops/STATE-ARCHIVE.md`. Nothing here is an authorization; read `ops/AUTHORIZATIONS.md`.

## A. Research work (V5; `v5-audit`, and branch `v5-p5-break-even`, not merged)
- **V5 audit** (AUTH-020): conceptual package; start at `design/package-v5/00-README.md`. Working draft V5-R = DPR-0007, plus V5-R17 (provisional). Nothing is validated, approved or final. Benchmark register `17`.
- **Probes R1-R3 and GLM-5.3 on ScaDS done** (AUTH-024 to AUTH-027; results `exchange/prior-work/v5-probes/results/` and `R3-GLM/`): merged into `v5-audit` and pushed (77357c1; WD-071, WD-072).
- **P5 done** (AUTH-028): part B, OpenAI side check, $0.594 (WD-073); part A, ScaDS GLM-5.3, free: break-even between 10 and 30 tools; D-01 fits the client route; D-01 kept, D-01h added for vendor-hosted search (WD-079).
- **P3 closed** (AUTH-029): six runs, $9.953; models search uninstructed; V5-R17 adds a stop for a missing tool, provisional (WD-074 to WD-076; `design/package-v5/inputs/p3/P3-LOG.md`).
- **P2 done** (AUTH-030, AUTH-031): OpenAI, $12.69; server-enforced offering at a fixed prefix kept the cache, with no accuracy loss beyond run-to-run variation (oracle subsets, 128 tools); HYP-0018 kept open; P2b running on ScaDS (WD-077, WD-078, WD-080).
- **End-to-end and P1 prepared** (AUTH-030, WD-081): 16 validated task pairs; AppWorld's natural returning users first. The end-to-end study waits for its own authorization.
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
- Authorizations: AUTH-020 (V5 audit), AUTH-021 to AUTH-023 (machine portability, see D), AUTH-024 to AUTH-027 (R3 probes; done), AUTH-028 (P5; done), AUTH-029 (P3; closed), AUTH-030 (group 1 and 2, P2 preparation) and AUTH-031 (P2 runs, P2b).
- Run allow-listed commands alone, never chained (WD-042, WD-043). The guard allows only `git push [-u] origin v5-audit` and the same for the Linux branch; the human pushes anything else.
- Agents: evidence-steward, design-proposer, design-challenger; protocol `ops/PROTOCOL.md`.
- Research outputs go on a branch cut from `v5-audit` and reach it by merge, only when the human says so (WD-061).

## D. Machines and branches (operations only; not research)
- **This branch, `linux-from-v5-audit--portable-guard-and-short-state`, carries only the Windows/Linux switch:** the cross-platform guard and tests, the verifier fix, the SSH remote on Linux, the Linux-run AUTH rows and this file. No research content. It is rebased onto `v5-audit` after each merge; the human force-pushes it. The rebase onto 77357c1 is not done yet (WD-072).
- **Not yet tested on Windows.** Before merging it into `v5-audit`, run on Windows: `python tools/verify_workspace.py`, `python ops/tests/guard_cases.py`, `python ops/tests/finding_citation_cases.py` (WD-059).
- **Linux notes:** `python` must exist (symlink to `python3`); 224 WARN lines are expected: origin extracts cannot be re-verified there; AppWorld and the run scripts live in `~/r3-work` (outside the repository); the API keys are in `~/r3-work/.env`, which the human empties when done.
- **Open for the human:** whether Bash `git commit` should ask first again.

## Next action for any session
Read this file, run `python tools/verify_workspace.py --quick` (expect `fail=0` on this branch), check `ops/AUTHORIZATIONS.md`, and work only inside an AUTH.
