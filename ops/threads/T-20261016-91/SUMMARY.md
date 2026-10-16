# T-20261016-91 SUMMARY: independent critical review of the workspace configuration

Written by the coordinating lead (the outer session), not by the thread's own lead: that lead session ended while waiting for the last completion notices and wrote no SUMMARY. This summary is based on `reviews/RV-0001.md`, the three agent logs, the thread lead's final reports (`ops/tests/raw/R-review-thread.jsonl`, git-ignored) and the checks I ran afterwards. Authorization: AUTH-001 (bootstrap: "one independent critical review of the configuration"; pre-handoff).

## What happened
- Three Sonnet 5.5 agents (evidence-steward, design-proposer, design-challenger; 317 subagent messages, all `claude-sonnet-5-5`) exchanged messages by agent id. The challenger wrote RV-0001 (D1-D27, none rated "blocks handoff"). The proposer conceded or confirmed most items and found D4 and the Q3 steering items independently. The steward checked Q4 and the peers' factual claims by Read/Grep (its Bash was denied: compound command, project folder not yet trusted).
- **Cap overrun:** the thread lead counted 13 SendMessage calls against the cap of 12; the agents' own tallies stopped at 9-10 because none can see the others' sends (D22). This was observed, not simulated.
- The thread lead correctly declined to run a command on the steward's behalf that the steward's permissions denied, and wrote a harness (`lead_guard_runs.py`) for the challenger's escalated guard cases instead of running risky commands.
- Not completed by the agents: runtime execution of any guard case (they cannot), whether a foreign agent id resolves (U1), `splitlines()` behavior (U2). I ran the first and third; U1 remains untested.

## Verified by execution after the review (by me)
| Item | Result |
|---|---|
| Challenger cases T1-T4, T6a, T6b, T7 against the original guard | all exit 0 (not blocked), as the challenger predicted: D1, D2, D5, D7 confirmed. T5 exit 2 as predicted. Output: `lead_guard_runs.py` |
| Same cases against the fixed guard | all exit 2 (`guard_runs_after_fixes.txt`) |
| D3: can a git-ignored `settings.local.json` disable the guard? | **Yes (C7)**: `{"disableAllHooks": true}` turned all hooks off in a throwaway copy. Deny rules still held (C8). Severity raised above the review's "should fix" |
| U2 (`splitlines()` vs LF line numbers) | **Yes**: 7 of 233 stored texts contain characters that Python's `splitlines()` treats as line breaks (form feed etc.), so extract line numbers would not match `sed`/`grep -n`. Fixed: LF-only counting in `origin_extract.py` and `verify` |
| Message cap (D22) | Replaced by a hook-enforced cap (WD-010); live regression R2 refused the 6th send at 5/5 |

## Disposition of every defect entry
| # | Review severity | Status | What was done / what remains |
|---|---|---|---|
| D1 | should fix | **fixed, residual** | guard blocks wildcard `research-clean*`/`cleanroom`, parent-directory paths, `..`, any Read/Grep/Glob/Write path outside the workspace. Residual: unusual wildcards in Bash text and interpreter-built paths (documented) |
| D2 | note | **fixed** | exemption for sanctioned-tool names removed |
| D3 | should fix | **confirmed, mitigated, residual** | deny rules (hook-independent) for the file, guard block, `verify` fails if present, config pin. Residual: hooks can be disabled by configuration (SAFEGUARDS, WD-011); user-level settings unchecked |
| D4 | note | **fixed** | `match()` rewritten (no `lstrip`, escaped dots) |
| D5 | note | **partly fixed** | `.git/**` blocked for edit tools. Command-prefix deny rules and bypassPermissions behavior remain documented limits |
| D6 | should fix | **partly fixed** | `RemoteTrigger`, `PushNotification`, `CronCreate`, `ScheduleWakeup` denied; the remainder (and built-in agent types' Bash) listed in SAFEGUARDS #7, #13 |
| D7 | should fix | **documented** | SAFEGUARDS #10 no longer says the guard "blocks messages to other sessions"; foreign agent-id resolution untested (U1) |
| D8 | note | **documented** | lead model not enforced (SAFEGUARDS #12) |
| D9 | should fix (human) | **partly fixed, human decision remains** | (c) `verify` rejects `approved` records citing AUTH-001. (a)(b) documented in SAFEGUARDS #15; AUTH-001 wording clarified as spent at handoff. **The human should confirm that AUTH-001's scope column fairly enumerates the bootstrap brief** |
| D10 | should fix | **fixed** | C3 re-run as a script with saved output (`c3_tamper.py`, `C3-output.txt`) |
| D11 | note | **fixed** | C4 removed as a model-audit citation; R and R2 added |
| D12 | note | **fixed** | the message-count dispute is resolved by WD-010; SAFEGUARDS no longer says "rounds respected" without the caveat |
| D13 | note | **fixed** | wording says the connectors were absent/needs-auth, not a live denied call |
| D14 | note | **fixed** | `verify` docstring and STATE corrected |
| D16 | should fix | **fixed** | template `basis` seeds no longer include REQ-D1 |
| D17 | should fix | **fixed** | REGISTER D states the scope of R5/R8/R9 |
| D18 | should fix | **fixed** | CAVEATS header, rows 3, 10, 12, 15 corrected against the sources (row 12's pointer was wrong: it cited a report that does not contain the claim) |
| D19 | should fix | **fixed** | REQ-U1 marked historical and Stage-2-scoped |
| D20 | note | **fixed** | CLAUDE.md line 3 attributes the framing to the human's description |
| D21 | note | **left as is** | governing core includes the latest candidate documents by an openly stated rule |
| D22 | should fix | **fixed** | WD-010 |
| D23-D27 | note | **fixed** | round defined; message kinds unified; steward command form and trust note; vocabulary unified; maxTurns fallback |

Steward's Q4 extras, all fixed: source counts (232 with text / 5 failed / 2 test artefacts), the "recomputed hash" sentence, CAVEATS pointer off by one (S4G L4), row 12, row 3 scope ("for C2"), `design/` directory tracking.

## Disputed or escalated
Nothing disputed between agents. Escalated to the human: D9 (scope of AUTH-001), the 12/2 defaults (WD-010), and the residual that hooks can be disabled by configuration.

## What nobody verified
Interactive/VS Code behavior; whether a foreign agent id resolves; adversarial prompt injection through evidence; the review itself shares model family, account and tooling with the system it reviews (it is an independent check by a separate agent context, not an independent organization).
