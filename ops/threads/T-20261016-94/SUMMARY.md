# T-20261016-94 SUMMARY: AUTH-005 scientific adjudication and revision (written by the lead; ACTIVE.json deleted, no further messaging)

## Produced
- Successor package `design/package-v2/` (00 README, 01 candidate, 02 justification and alternatives, 03 evaluation outline, 04 claim-to-source register, 05 unsupported assessment, 06 disagreements, 07 presentation outline). The AUTH-004 package `design/package/` is unchanged.
- Records by owner. Proposer: DPR-0004, DPR-0005, HYP-0007..0014 (supersessions: HYP-0008 replaces HYP-0005, HYP-0010 replaces HYP-0004, HYP-0011 replaces HYP-0003, HYP-0012 replaces HYP-0006). Challenger: CH-0020..0034 (14 `conceded`, 1 `withdrawn` as recorded), RV-0003 (final). Steward: `findings/SUM-0003-pivotal-claims-verification.md` (front matter `FND-0001`; filename kept because it is cited), EXT-0066. Lead: EXT-0057..0065, TASK.md, RESUME.md, package-v2.
- Messages: **9 of 12** (`messages.log`): lead 3 tasking, steward -> proposer 1, proposer -> challenger 3, challenger -> proposer 2. No escalation (none was needed).

## Completion status per agent
All three completed with final reports. Steward: V1-V8 done (4 SUPPORTED, 4 PARTLY; V2 and V3 each with a CANNOT DETERMINE component), 50 tool calls, one extra extraction window. Proposer: all 3 messages used, two propagation rounds of edits after the cap-free file work. Challenger: 2 rounds, 15 objections graded, final report.

## What is disputed
Nothing material between the agents after two rounds (06 section A lists where emphasis still differs: need-proxy adequacy; whether a regime exists where the candidate beats cached expose-all; whether model-actor nodes need a rule; whether recoverability separates C-A from C-B; whether the price model adds anything over an empirical sweep; the adequacy of `epsilon := delta`). Human decisions: O1 vs O2, Q1, `delta` and the other margins, `N_dep`, cost convention, reference policy, whether a stage-free candidate is acceptable.

## Constraints on the review (report to the human)
Cap 12 and two rounds unchanged. Challenger and lead agree no third round was available. The closed-form cost algebra and the Toollery fit are derivations reproduced by the challenger, not by the steward. Items from governing copies not read at the original are listed in 04 section C.

## Lead actions outside agent work
Recorded AUTH-005; extracted EXT-0057..0065 (sanctioned tool, lead-chosen ranges, steward-verified); read the Toollery replay setup (model and pricing are not in the stored text); recomputed the T* slope (about 115, not 141); re-applied a mechanical `target` front-matter fix to `reviews/RV-0003.md` (the challenger overwrote the first); made a safe checkpoint on the user's request mid-task (commits d061064, 648398f and the package-v2 WIP commits).

## What no one verified
Toollery model/pricing/list construction and the cause of its low hit rate; billing of deferred or withheld definitions; whether the closest evaluation vehicle can run free sessions; all vendor cache statements beyond what the documents say; ER-R, MCP-Zero, ITR (beyond its ablation table), PlanBench-XL beyond the extracted passage; ledger rows C3-*/K*.

## Verification at close
At the final work commit `e81244b` and the audit commit `67abc5f` the verifier reported one FAIL: an unreviewed local override file under `.claude/` (git-ignored). It was not inspected by the lead because the guard blocks shell access to it. **Resolved (2026-10-17):** the human inspected it (only saved Bash permissions, no hook-disabling settings), moved it outside the workspace, and the full verifier then passed: 610 pass, 0 warn, 0 fail at `67abc5f`. No operational blocker remains on AUTH-005.
