# Workspace state (imported into every session; keep under 40 lines and under 6 KB)

Earlier versions, verbatim and dated: `ops/STATE-ARCHIVE.md`. Nothing here is an authorization; read `ops/AUTHORIZATIONS.md`.

## A. Research work (V5; lives on `v5-audit`)
- **V5 audit** (AUTH-020) is a conceptual package. Start at `design/package-v5/00-README.md`. Working draft V5-R = DPR-0007. Nothing is validated, approved or final. The benchmark register is `17`; its section 5 holds the probe results.
- **Probes R1-R3 done (2026-11-01 to 11-06; results `exchange/prior-work/v5-probes/results/`).** AppWorld, MiniMax-M3, OpenRouter with one provider: offering all 469 definitions costs 2.2-2.6 times the predictor subset, with about 96% of the prompt in cache reads; no accuracy difference is visible in four runs (B1 50/45, B2 46/46 of 57, with reasoning on); the reasoning mode must be fixed per run: off, the model passed only 24-28; AUTH-024/025/027 spend: $4.26, $4.80, $4.43; R3 Part B, its follow-ups and the docs refresh of 2026-11-07 are on output branch `v5-r3-part-b-results`, **merged into `v5-audit` on 2026-11-08 (77357c1; the human: "yes i accept mergeing!")**.
- **GLM-5.3 on ScaDS done (AUTH-026, 2026-11-08, free, one run per arm):** B1 23, B2 24 of 57; B1/B2 prompt 2.17x, computed bill about 1.5x (1.08-1.80 over 47 endpoints); GLM's own predictor dropped the credentials function in 22 B2 tasks, all failed. Results in `R3-GLM/` (branch `v5-r3-glm-results`), records on `v5-r3-part-b-results` (THREAD E-35); **both merged into `v5-audit` 2026-11-08 (77357c1), not pushed**.
- **P5 authorized (AUTH-028, 2026-11-07), P5 only;** route accepted: ScaDS GLM-5.3 after GLM B2 ends, OpenAI billing check only after an accepted estimate; harness written and mock-tested on branch `v5-p5-break-even` (`design/package-v5/inputs/p5/README.md`); nothing real sent. ScaDS part (94 requests, free) can start now that GLM B2 has ended; OpenAI part (73 requests, about $0.80, stop $1.20) needs `OPENAI_API_KEY` in `~/r3-work/.env` and a price recheck. Executor: described (PWD-019) and the investigation closed for now (REQ-U1107-14); it reopens only for a baseline run, Joaa's answer to Q-J33, or a new dependency.
- **The human answered the questions guide on 2026-11-07** (INT-T-023, REQ-U1107-01..09; per question: `design/ledger/notes/ANSWERS-20261107.md`, on `v5-r3-part-b-results`). `17` section 9 is postponed; `08` section 5 was rechecked, unchanged; the workbook is not yet edited (no `openpyxl` on Linux). Follow-up INT-T-024: research question entered as pointers (`requirements/THESIS_QUESTION.md`), Q-U16 declined, Q-U17 keep. Still open: Q-U15, Q-U25, Q-U27.
- **Waiting on the supervisor:** his verdict on V5 (not yet given); Q-J31 and Q-J32 depend on it; Q-J33 is asked only if Executor is run as a baseline.
- **Thesis question:** set by the professor and Joaa; entered as their words with pointers (14 Oct wording, 21 Oct scope) in `requirements/THESIS_QUESTION.md` on `v5-r3-part-b-results`. No policy has been selected.

## B. Standing decisions of the human (details: `requirements/REGISTER.md` section H)
- Minimise the bill on average over turns and sessions, with accuracy nearly the same; no margin or budget; model-agnostic billing equation (DPR-0006).
- Headline average A, with B beside it. Estimation-only reporting (INT-T-022).
- Memory scope = memory and tool calls. A negative result is still a thesis.
- Process: research and drafted policy, then a proof-of-concept loop, then end-to-end. Earlier retrieval work stays outside.
- The university API (ScaDS) serves open-weight models only, and its proxy refuses `allowed_tools`.
- The human's `.workspace/` stays untracked and is never pushed.

## C. Operating rules
- Authorizations in force include AUTH-020 (V5 audit), AUTH-024 to AUTH-027 (R3 probes and follow-ups), AUTH-028 (P5) and AUTH-021 to AUTH-023 (machine portability, see D).
- Run allow-listed commands alone, never chained (WD-042, WD-043). The guard allows only `git push [-u] origin v5-audit` and the same for the Linux branch; the human pushes anything else.
- Agents: evidence-steward, design-proposer, design-challenger; protocol `ops/PROTOCOL.md`.
- Research outputs go on a branch cut from `v5-audit` and reach it by merge, only when the human says so (WD-061).

## D. Machines and branches (operations only; not research)
- **This branch, `linux-from-v5-audit--portable-guard-and-short-state`, carries only the Windows/Linux switch:** the cross-platform guard and tests, the verifier fix, the SSH remote on Linux, the Linux-run AUTH rows and this file. No research content. It is rebased onto `v5-audit` after each merge; the human force-pushes it.
- **Not yet tested on Windows.** Before merging it into `v5-audit`, run on Windows: `python tools/verify_workspace.py`, `python ops/tests/guard_cases.py`, `python ops/tests/finding_citation_cases.py` (WD-059).
- **Linux notes:** `python` must exist (symlink to `python3`); 224 WARN lines are expected: origin extracts cannot be re-verified there; AppWorld and the run scripts live in `~/r3-work` (outside the repository); the API keys are in `~/r3-work/.env`, which the human empties when done.
- **Open for the human:** whether Bash `git commit` should ask first again.

## Next action for any session
Read this file, run `python tools/verify_workspace.py --quick` (expect `fail=0` on this branch), check `ops/AUTHORIZATIONS.md`, and work only inside an AUTH.
