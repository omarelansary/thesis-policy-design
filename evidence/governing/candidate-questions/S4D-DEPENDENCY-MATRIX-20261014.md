# Dependency matrix for candidates C1-C6 (v2, after the independent challenge)

- Date (UTC): 2026-10-14. Companion to `S4D-CANDIDATE-DOSSIER-20261014.md` (v2). Existing evidence only; D-a to D-j unresolved; no scores, tallies or ranks. v1 is preserved in git; changes are listed in the dossier section 9 and `audits/S4D-V1-…`.
- Key for section 2: **P** = the candidate is defined for any choice, but the choice changes its design or claim; **S** = the choice determines whether this kind of candidate is wanted; **F** = the choice determines feasibility; **X** = needed before any execution; **-** = no dependence.

## 1. How each candidate relates to the requirements (text, not categories)
| Requirement | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|
| R1 tokens | token vector of the pools only | cumulative tokens including recovery | cumulative tokens by category | informs which tokens matter | how tokens are counted | per-step net token savings |
| R2 performance kept | accuracy side of restricted vs reference exposure | success restored by recovery | frontier analysis; "maintained" needs a stated test and margin | informs what can be hidden | evaluator sensitivity of the success side | success cost of each step; composed policy vs baselines under a stated test |
| R3 overhead | no | recovery and search tokens, turns, over-search | discovery and recovery counted by design | no | defines what overhead is counted | step overhead netted in the per-step condition |
| R4 horizon | no | only if session reuse is modelled | session-length sweep | no | horizon sensitivity | trajectory; session if modelled |
| R5 policy and recovery | quantifies what recovery would need to restore | recovery component | policy classes, recovery inherent to some | no | no | recovery as one step |
| R6 baselines | all-tools or curated arms | no-recovery and static comparators | the baselines are the arms | all-tools accuracy as a function of the catalogue; no existing-project baselines | informs | all-tools and static restriction |
| R7 findings / algorithm cue | findings on causes of loss | findings on recovery value | findings on which classes pay | findings on degradation factors (the "why" side) | findings on conclusion stability | findings on which steps pay; a designed policy |
| R8 stepwise (policy form) | not required | not required | not required | not required | not required | central |
| R9 graded lens (policy form) | not required | not required | one class among others | factor (iv) is the evidence such a lens would rely on | not required | a factor |
| R10 use and improve existing work | builds on App. N, ToolMATH, CAM-DF | builds on active-discovery and Executor-type recovery | head-to-head of existing classes | builds on token-length and distractor studies | builds on cost-accounting studies | builds on shipped stepwise designs |

## 2. Decision dependency
| Decision | C1 | C2 | C3 | C4 | C5 | C6 | Note |
|---|---|---|---|---|---|---|---|
| D-a objective and formulation | P (F4/F5; F1/F2 slices) | P (F1-F5) | P (F4/F5 natural) | - (coefficient-free; supplies the success-exposure relation) | P (studies the formulations) | P (F1-F5; per-step net savings sign condition) | no candidate needs a scalar or coefficient |
| D-b contribution type | S | S | S | S | S | S (the policy-design candidate) | evaluation (C1-C3, C5), mechanistic (C1 partly, C4), methodology (C5), design (C6) |
| D-c resources, models, budget, time | F | F | F | F (model set bounds the claims) | F (logs: tables or runs) | F | no candidate is excluded by any particular resource profile; resources are unspecified |
| D-d security in scope | - | - | - | - | - | - | outside the alignment boundary unless scope changes |
| D-e horizon | - | P | P (central) | - | P (central) | P | trajectory vs session length |
| D-f endpoint and margin | P (slices) | P (ratio needs a minimum loss) | P (test for "maintained") | P (detectable differences) | P (evaluator sensitivity) | P (test for composed policy) | margin not fixed anywhere |
| D-g meaning of "novelty" | P | P | P | P | P | P | decides whether evidence-based evaluation, mechanistic finding or a designed policy counts |
| D-h numeric overhead limit | - | P | P | - | P (filter-model price ratio) | P | no number given by the supervisor |
| D-i baselines and execution | X (vehicle) | X (vehicle, recovery baselines) | X (several baselines) | X (benchmark data and models) | X (variant-dependent) | X (baselines, vehicle) | no execution authorised |
| D-j put reformulations to the supervisor | P | P | P | P | P | P | applies to every candidate: all except C6 are non-policy contributions that he may or may not accept |

## 3. What would distinguish candidates (evidence or decision), without ranking
| Distinguishing item | Kind | Bears on | How |
|---|---|---|---|
| Does a count, overlap or detail-level effect exist for current strong models at matched tokens? | evidence (pilot) | C4; the presence term of C1; the step choices of C6 | a null makes C4 a bounded null and shrinks C1's presence term |
| How large is the success loss at moderate cuts (about 40-50%) at catalogue sizes of a few hundred tools? | evidence (pilot) | C1, C2, C3, C6 | decides whether misses matter in the regime the supervisor described (N13) |
| Natural miss prevalence and alternative-path success | evidence (pilot) | C1, C2 | decides whether injected-miss designs describe real behaviour |
| Discordance, policy-by-task variance, token-trajectory variance | evidence (pilot) | all | converts the parametric formulas into sample sizes |
| Can any public vehicle build required-plus-r pools, expose modes and usage? | evidence (code inspection or a bounded run; needs D-i) | C1, C2, C3, C5, C6 | decides between a vehicle and a new harness |
| Provider usage logs with caching under different exposure policies | evidence (access) | C5 (non-arithmetic content), C3 and C6 provider arms | separates convention arithmetic from real cache behaviour |
| Whether the supervisor requires a designed policy or accepts evidence-based findings | decision (D-b, D-g, D-j) | all | determines which kinds are wanted |
| Which formulation the thesis claim takes (curve vs operating point) | decision (D-a, D-f) | C2, C3, C5, C6 | changes the outcome definition and the analysis |
| Available models, API access and budget | decision (D-c) | all | sets the model set and arms; not a reason to remove a candidate |

## 4. Parametric feasibility summary (formulas only; no host-specific claims)
- Paired contrast: n = 7.84 (d/R + tau^2) / D^2 (P2 form). A simple effect has variance 2 sigma^2/n_cell, a main effect averaged over the other factor sigma^2/n_cell, an interaction 4 sigma^2/n_cell (equal cells). Ratio estimands need Fieller-type intervals. Joint dominance needs both axes to pass.
- Attempts = tasks x arms (or cells) x R x models (x sizes). Input tokens = attempts x tokens per attempt (a pilot output). One benchmark reports 3.4k-25.7k per attempt and a whole-catalogue prompt 10-30x that of any other cell (dynamicmcpbench L1030-L1031, author-stated).
- Money = tokens by category x a price table; the price table, cache regime and filter-model ratio are application parameters (D-a, D-c).

## 5. Open items that no candidate resolves
Frontier-model count effect at matched tokens; the supervisor's 40-50% premise; real-use definition share; whether any vehicle supports forced inclusion; the execution status of any vehicle; searches aimed at the C1, C2, C5 gaps (not run in this step).
