# Questions for the student from the V5 audit (2026-10-22; successor to QUESTIONS-FOR-YOU-20261020.md, which is unchanged)

Source: `design/package-v5/05-poc-loop-and-e2e.md` section 5 and `08-ledger-proposals.md`.

1. **Q-U28.** Authorise the first proof-of-concept step (P0): a few requests on the university API to see whether it reports cache writes and reads and which tool mechanisms it passes through, plus reading Executor's own MCP documentation. Then the loop item by item.
2. **Q-U29.** Take V5-R (`design/proposals/DPR-0007.md`, revision 2) as the working draft to show the supervisor, or keep V4?
3. **Q-U30.** Which average of the bill is primary: total bill over total turns, or the mean of each session's bill per turn (DPR-0006 section 4)?
4. **Q-U31.** Apply the ledger changes proposed in `design/package-v5/08-ledger-proposals.md`?
5. **Q-U32.** Once V5 is accepted, supply the June exposé so its ideas can be tested against V5's result.
6. **Pushes.** The lead's `git push` is refused by the auto-mode classifier; push `v5-audit` yourself, or change that setting if you want the lead to push.

## Status (2026-10-22, after INT-T-006 and INT-T-007)
- Q-U28: answered in part (the status page was read). Next step is Q-U33.
- Q-U29: answered. DPR-0007 is the working draft.
- Q-U30: answered 2026-10-25: A (all money divided by all turns) is the headline, with B (the average of each session's cost per turn) beside it.
- Q-U31: answered. The ledger changes are applied.
- Q-U32: answered and done 2026-10-25: the two files were checked, ideas only (`design/package-v5/09-expose-ideas-checked.md`).
- Q-U33: **open, deferred by you on 2026-10-25** (cannot run it now; nothing else waits on it). Run `design/package-v5/tools/p0_api_probe.py` with your key in your own terminal when able and save the output to `design/package-v5/inputs/p0-api-probe-output.txt`.
- Pushes: `git push origin v5-audit`.
