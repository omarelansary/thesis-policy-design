# 04. Remaining objections, experiments needed, and decisions for the human

Status: provisional, lead's assessment [I]. Nothing here is validated; no experiment is authorised. Review record: `reviews/RV-0004.md`, `challenges/CH-0035..0044.md` (one challenger, two rounds, 2 of 12 messages used on the thread). Not reviewed by a proposer or steward in this task; the challenger could not run the 3,000-instance simulation and did not verify model windows or provider tool limits.

## 1. Disposition of the challenges (what changed)
| CH | Final challenger status | Lead disposition | Change made | Residual |
|---|---|---|---|---|
| 0035 extra model call per discovery omitted | withdrawn (hand-checked on a three-call trajectory) | ACCEPT | `01`: `I_disc`, `A_t`, `phi_t`, defer-at-all test `sum s_t > Omega` | searches in trajectories that need no deferred tool are in no term; `I_disc`, `tau` must be conditional on the needed tool (minor, noted) |
| 0036 coverage bound | withdrawn | ACCEPT | `01`: definitional decomposition, `q` for any cause, unseen tail, direction of bias stated | the residual `I` is unbounded and unestimated |
| 0037 knapsack | withdrawn | ACCEPT | heuristic framing; co-needed bias direction | counts from the simulation were not re-run by the challenger |
| 0038 large-catalogue applicability | minor, open | ACCEPT | "2 of 4" scope; symmetric missing anchor; estimators listed | **fixed after round 2:** the substitute is named before D4, by a rule not using arm results (`02` D4 (d)); table cell made parallel (`03`); source of strata annotations is still undecided |
| 0039 G is not one policy | minor, resolved by relabel | PARTIAL | two layers; D4 called arm selection; `O_dev / N_dep` charged | disagreement retained (section 3) |
| 0040 D4 statistics | **maintained, should-fix (a)-(c)** | ACCEPT | **fixed after round 2:** arm table fixed before running (a), test-split failure reports OUT2 (b), power and minimum stratum with "not assessed" label (c), paired-difference ties (d), OUT2 edge widened (f) | the arm table, `alpha`, minimum stratum size are **human decisions not yet taken**; the procedure's error rates are unknown (E6). The challenger has not re-checked these last edits |
| 0041 node audit | minor, open | ACCEPT | inequality and R6 query fixed, no-recovery arm, RA12-RA13 added; R6 timing and scripted-query provenance flagged as arm specification | R6 itself has no supporting evidence |
| 0042 perverse optima | minor, open | PARTIAL | stratum guard, `O_dev`, instrument, non-token compute | reporting tokens split by outcome, naming the tool-block share, and whether provider usage counts deferred definitions belong to E1 (below) |
| 0043 unfair comparison | minor, open | ACCEPT | section 5 compares G with a fixed best arm; EXT-0053 description corrected | "hand-picked core needs no selection" corrected to "needs usage knowledge" |
| 0044 residuals of corrections 1 and 5 | withdrawn | ACCEPT | `01` wording | none |

## 2. Strongest remaining objections (ranked by how much they could change the proposal)
1. **The selection protocol is experimental arm selection, and its own error rates are unknown.** With a modest labelled set, a multi-arm tournament with a mean-and-every-stratum rule may return expose-all for lack of power or a winner that fails on new tasks. If so, G's "conditional decision" is empty in practice. (CH-0040; E6.)
2. **Models may not search.** Every recovery path (R4) rests on RA1: that the model emits a request when a needed tool is absent. Unmeasured in the record; failure is a lost task. (E2.)
3. **The tool block may be a small share of tokens.** If conversation and outputs dominate, no exposure policy saves much, and the whole line ends. Cheap to check. (E1.)
4. **Selector recall at large catalogue size has no legitimate labelled data.** The need estimator that D2 and R2 rely on is exactly what a large catalogue lacks; candidate estimators are listed, none is validated. (E3, E8.)
5. **The reference cannot run at large scale.** Every claim there is relative to a named substitute and cannot show noninferiority to the true reference. (E4.)
6. **Mean success can hide the tail.** The stratum guard addresses it but depends on which strata are pre-registered and on their size.
7. **Billed cost can reverse the token ordering.** In the one direct cache table, token reduction came with an inconclusive billed difference; the fitted multiplier is study-specific (errata 5). Not in the criterion, so a token win could be a billed loss. (E7.)
8. **No source shows a second filtering stage paying, or a system-side trigger working.** The staged form is the supervisor's requirement, not an evidenced mechanism.

## 3. Retained disagreements (not averaged away)
- **D-nodes in the supervisor-facing graph.** The challenger accepts the two-layer labelling; the lead keeps D1-D4 in the figure because AUTH-006 asks for a testable conditional decision and D1-D2 are factual conditions. Both agree D4 is not a run-time rule and not a learned rule across settings.
- **C-A versus G ordering.** The demotion of C-A rests on applicability (its core rule needs need statistics), not on a finding that G is better. The record does not rank them.
- **Size of the selection inflation.** Unmeasured; the lead expects it to matter for small dev sets, the challenger's point (c) comes from reasoning about the rule, with no data behind it, as does the lead's expectation.

## 4. Experiments needed (none authorised; in dependency order)
| # | Question | Design sketch | Resolves | Could end the line |
|---|---|---|---|---|
| E1 | Token accounting by category and catalogue size | Provider-reported input tokens per call, split into tool block, history, outputs, discovery overhead; by outcome (success and failure separately); state whether usage counts deferred definitions | objections 3, 7 (partly); CH-0042 residuals | yes (if the tool block is a small share) |
| E2 | Do models initiate search when a needed tool is absent? | Remove one needed tool per task, scope statement on and off, several models | objection 2; RA1 | yes for R4-based arms |
| E3 | Selector recall at the same search width | Disjoint labelled split, recall of the needed tool within `kappa` | objection 4; RA2, RA13 | for R2 |
| E4 | Validity of a substitute reference | Where the reference runs, compare noninferiority conclusions against the substitute rule in `02` D4 (d) | objection 5 | no |
| E5 | End-to-end noninferiority sweep | Arms from D3 with strata, three disjoint splits | objections 2, 6 | no |
| E6 | Error rates of the D4 procedure | Simulation and a cross-setting test: does the arm chosen in one setting remain feasible in another | objection 1; CH-0039/0040 | for the policy claim |
| E7 | Billed cost and cache per provider | Same trajectories, provider-reported cost, cache reads/writes | objection 7 | no |
| E8 | Validity of need estimators | Compare candidate estimators (group-level need, unseen-mass estimates, exploration logs) against held-out true need | objection 4; D2 | for C-A at scale |

## 5. Decisions for the human (not made here)
`delta` and the strata (and a minimum stratum size); `alpha` and the arm table (its size drives power); `N_dep`; tokenizer convention and whether provider usage counts deferred definitions; the substitute-reference rule (the lead's default in `02` D4 (d) is a proposal); whether tokens rather than count is the criterion (Q1); Q2-Q6 in `requirements/REGISTER.md` G.3; the label for G ("policy family plus selection protocol" is the lead's wording); whether to authorise E1 first (cheapest, can end the line).
