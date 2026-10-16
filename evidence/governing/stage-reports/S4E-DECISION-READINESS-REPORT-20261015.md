# S4E decision-readiness report: what stands between C1-C6 and a defensible selection

- Date (UTC): 2026-10-15. Coordinator: Sonnet 5.5. Authority: D8. Evidence: the S4D candidate dossier v2, dependency matrix v2 and quality addendum (which governs where they differ), D7, Stage 4b/4c findings and errata, Step 1 records, probes P1-P3, the admitted 2 October requirements. Independent review: one Opus-level critic (`audits/S4E-C1-…`), adjudicated in `audits/S4E-V1-…`; my pre-critic analysis is preserved in `audits/S4E-A-…` (hash-verified). Corrected conclusions below replace the Phase A conclusions where they differ.
- This report selects, ranks and eliminates nothing; D-a to D-j stay open parameters. No new search, fetch, execution, 14 October material, earlier thesis work or Stage 5. Labels: F fact, I interpretation, U unknown, S speculation (effort estimates are S).
- Corrections that matter to the earlier record (details in `audits/S4E-V1-…`): (i) the brief keeps "findings on which approaches work in which cases and why" as Required, so the S4D requirement list and 4c section 1 under-stated support for findings-type contributions; (ii) the P2 "41%" is power at a true 2-point loss, not an error rate, and sample sizes computed for zero true loss are optimistic (table in section 5); (iii) DynamicMCPBench Appendix S (distractor quantity and strategy, five models, accuracy flat, but within pools that already contain the needed tools) is close prior art for the presence terms of C1 and C4; (iv) BoR's only downstream test is a single forced-choice step whose "end-to-end" is presentation times choice accuracy; (v) CAM-DF's contrasts come from 7 read tools and TheMCPCompany's 12.5% is 3 of 24 tasks; (vi) "each step saves tokens" and "save tokens over turns" are about steps and turns respectively, so the per-step reading is not settled by the transcript.

## 1. Status matrix (descriptive; no scores, no order)
| | Estimand and cluster | Closest prior art now | Selection blockers (decisions) | Blocker only for a novelty claim | Evidence-only unknowns |
|---|---|---|---|---|---|
| C1 absence vs presence | loss attribution; cluster {C4, C1-presence} and {C1-absence, C2} | DynamicMCPBench App. N and App. S, ToolMATH, CAM-DF (7 tools), CloudUse | whether brief 1.2 binds the main contribution (it decides if a findings-type question can be the thesis) | no aimed search was run; App. S already shows a small-pool null for presence | absence and presence effects at catalogue scale and moderate cuts; whether pool size scales on any vehicle |
| C2 recovery value and price | what recovery restores and costs, incl. no-miss tasks; cluster {C1-absence, C2} | SING and MCP-Zero, PlanBench-XL enforced exploration (<5 points), TheMCPCompany (3 of 24), Executor | same as C1; a recovery hook must exist on a vehicle | only adjacent queries (S4-Q007) | natural miss prevalence; harness dependence |
| C3 policy classes | class-level non-dominance; cluster {C3, C6, C5} | Skill Blocks (skills), DynamicMCPBench App. N, ToolMenuBench, MemTool, compgateway | accounting convention across client, provider-native and code-mediated classes (a design/decision) | targeted searches exist; skills-to-tools transfer assumed | which classes are dominated |
| C4 selection-degradation factors | factor causation; cluster {C4, C1-presence} | LongFuncEval, SLCA-GRPO, ToolMATH, flood test, Du et al., BoR (frontier, single step), DynamicMCPBench App. S | its fit to the objective (alignment decision) | searched repeatedly; none found | whether any effect exists for strong models at matched tokens |
| C5 conclusion stability | invariance of conclusions under conventions; cluster {C3, C6, C5} | r3-tokennotcost, CAPC, Skill Blocks sensitivity, validity audit | a source of logs (resources or other candidates' runs) | no aimed search; arithmetic risk | provider cache behaviour under policies |
| C6 stepwise policy family | step-level contributions and composed-policy validation; cluster {C3, C6, C5} | Executor, vendor deferral, Skill Blocks hybrid stubs, SkillJuror, SING, K-C record | meaning of "each step saves tokens" (supervisor); keep-separate-from-C3 decision | partial searches only | which steps pay |
Estimand independence: six records are not six independent studies. The measurement clusters are {C4, C1-presence}, {C1-absence, C2}, {C3, C6, C5}; each cluster can share runs (section 3).

## 2. Decisive blockers, separated
**Decisions that genuinely block a defensible selection (all for the user, some with the supervisor):**
1. **What kind of contribution counts.** Whether the brief's section 1.2 items (stepwise, fallback, graded lens; Required) bind the main contribution or any policy-form contribution only, and whether the brief's Required "findings on which approaches work in which cases and why" suffices on its own (D-b, D-g; the brief's own section 0/1.2 tension, which the S4D dossier settled by interpretation).
2. **Meaning of "each step is there to save some token"**: per step, or collectively over turns, and how a recovery step is judged. Needed before C6's falsifier is frozen, not before shortlisting.
3. **Resource tier (D-c), only if the selection must be feasibility-informed.** `STAGE_GATES.md` places documented constraints in Stage 5, so this is not strictly a scientific blocker; it determines which candidates are executable.
**Evidence-only unknowns (cannot be preconditions of selection):** frontier count effect at matched tokens; discordance and policy-by-task variance; natural miss prevalence; provider cache behaviour; the supervisor's 40-50% hedged premise (a hypothesis to test, brief G-e); real-use definition share.
**Unresolved assumptions to carry as reportable limitations:** harness dependence; skills-to-tools transfer; binary success and independence; token equality across models; results tied to model versions; staged-disclosure scope of C2 and C6.
**Not blockers:** D-a formulation (stays parametric; whether money is a reported outcome can be decided later), D-d, D-e, D-f (but see the P2 correction), D-h, D-i for anything non-executing, D-j (blocks freezing a selected question, not shortlisting).

## 3. Shared vehicles and supporting experiments (no merging, no selection)
| Shared item | Candidates it could serve | Status |
|---|---|---|
| V1: a deterministic, effect-scored catalogue-scale benchmark with pool control (DynamicMCPBench-type; 1,845 tasks over 1,168 tools; code and data licences verified to exist, not executed) | C1, C2 (needs a recovery arm added), C3, C6, and C5 via its logs | pool-size scaling, recovery hook and per-call token logging unverified (read-only code inspection) |
| V2: a single-step selection harness with deterministic grading (BFCL-type) | C4; C1's presence term at small pools | its null at small pools (App. S) shapes expectations |
| V3: per-attempt token and usage logs from any of the above, or published per-attempt tables | C5 (cheapest variant on published tables, which lack cache fields) | not examined |
| Supporting pilot (not authorised, not a precondition): one small run set yielding discordance, policy-by-task variance, token variance, natural miss prevalence and a first look at the count effect | informs C1, C2, C3, C4, C6 | requires D-i and resources |

## 4. Smallest sensible design per candidate (parametric arithmetic, not a plan)
Assumptions (I): detectable difference D = 10 points, discordance 0.20, one run per task, no policy-by-task interaction, true difference 0. A paired simple contrast needs about 157 tasks; an interaction in a paired 2x2 needs about twice that; the numbers rise sharply for smaller D or a nonzero true loss (section 5).
| | Smallest sensible design | Order of magnitude |
|---|---|---|
| C1 | one catalogue size, one reference arm (all-tools where feasible), 2x2 of absence x presence, 2 models | about 157 tasks per simple effect, about 314 for the interaction; about 1,250 attempts per model |
| C2 | no-recovery, recovery, equal-cumulative-token static comparator, on induced-miss tasks and on no-miss tasks | about 157 + 157 tasks per paired contrast; about 940 attempts per model and recovery family |
| C3 | 3-4 classes on one vehicle at two sizes | pairwise contrasts at 157 tasks each; joint dominance and multiplicity push this up (not quantified) |
| C4 | 3 contrasts x 2 model strengths, deterministic items | n = 7.84 d/D^2 per contrast; about 314 items at d = 0.10 and D = 5 points; model-by-factor interactions about double |
| C5 | bootstrap flip frequency on whatever logs exist | no closed form; depends on the logs |
| C6 | k add-one/leave-one-out ablations plus composed policy on held-out tasks | k x 157 tasks plus a held-out set; 2^k cells if interactions are estimated |

## 5. The statistical correction (affects every "maintained" claim)
Sample sizes in P2 and in Step 1 assumed a true difference of zero. Approximate tasks for 80% power at a true loss delta: M = 5 points: 628 (delta 0), 980 (-1), 1,742 (-2); M = 10 points: 157 (0), 194 (-1), 245 (-2), 627 (-5) (d = 0.20, R = 1, tau = 0; I). At n = 628 and M = 5, power is 0.80, 0.61 and 0.41 at true differences of 0, -1 and -2 points; these are powers, not false-acceptance rates. The practical consequence is that a policy that costs even one or two points needs far more tasks to be shown non-inferior, and the margin remains a decision (D-f).

## 6. Is a Step 2 necessary? What would it accomplish?
- **Not necessary to make a selection.** A selection can be made now under the stated uncertainties.
- **Necessary before any novelty claim and before a feasible plan.** Step 2 is small and has two purposes: to find out whether the closest vehicle can do what C1, C2, C3, C5 and C6 need, and to test whether the gaps for C1, C2, C5 and C6 are already filled. It would reduce those two differentiating uncertainties and nothing else.
- **Proposed minimal package** (none performed):
| # | Check | Scope | Priority | Effort (S) | Authorisation needed |
|---|---|---|---|---|---|
| 2a | Read-only inspection of the closest vehicle's code and dataset schema | pool-size parameter and its range; exposure modes; presence of a recovery hook; per-call token logging; offline replay; required-tool annotations; licences. No installation or execution | high; serves C1, C2, C3, C5, C6 | 2-4 hours | a new decision record permitting fetches (D8 set zero); brief G-f permits reading source |
| 2b | Aimed nearest-neighbour searches, only for candidates you shortlist | gap statements of C1 (absence x presence), C2 (fallback toggle with equal-cumulative-token comparator), C5 (conclusion stability), C6 (step ablations) plus a recency pass; up to about 12 logged queries | after a shortlist | 2-3 hours with one worker | your approval of providers and queries (`CLAUDE.md`) |
| 2c | Re-analysis of published per-attempt tables | which token and cache fields exist, for C5's cheapest variant | low; optional | about 1 hour | none beyond existing stored texts |
| 2d | Store the Executor tool-invoker text | only if Executor becomes a baseline | low; optional | 1 fetch | fetch authorisation |
- **Not recommended now:** a feasibility execution (needs D-i and D-c), pilots, re-searching C3 or C4, any TraceLab raw-field analysis.

## 7. Questions that truly require your decision before selection
**Must be answered (or consciously accepted as open) before selecting:**
1. Do the brief's Required policy-form items (stepwise, fallback, graded lens) bind the main contribution, or is a findings-type contribution (Required in the brief: which approaches work in which cases and why) enough? Is "novelty" an algorithm, an evidence-based finding, or an evaluation?
2. If you want an executable selection: a coarse resource tier (API/provider access yes or no, model classes, budget order, time).
3. Is money (billed cost) in scope as a reported outcome? (Formulations stay parametric either way.)
4. Include or decline, as an explicit scope decision, the families the evidence supports but the set does not carry: content-level token reduction (compression and informativeness trade-off), and session working-set management; also the sub-agent, partitioning and gateway families if you want exhaustiveness.
5. Authorise Step 2a (read-only inspection), and, after a shortlist, Step 2b.
**For the supervisor, not now:** the meaning of "each step saves tokens" (per step or per policy over turns, and how recovery is judged); whether he requires a designed policy; what novelty means; the margin for "maintained".
**Can remain open:** D-a formulation, D-d, D-e, D-f, D-h, D-i for execution, D-j.

## 8. Any evidence-supported reason to reopen candidate formation?
No evidence-supported reason requires it. Two things could change wording or scope without reopening: (i) Step 2a/2b outcomes (a gap found already filled would reword or merge a candidate); (ii) your decision on question 4 above (including a distinct family would add records). The supervisor's hedged 40-50% premise is a slice of C1/C3, not a new family, and using it as a yardstick risks steering by his example.

## 9. What is established, what is uncertain, what Step 2 would accomplish
- **Established:** the candidate set has no invalid member; its estimands form three measurement clusters; the brief supports findings-type contributions more than the S4D record said; sample-size claims are more optimistic than stated; Appendix S and BoR narrow C1 and C4; the vehicle question is the main practical differentiator.
- **Still uncertain:** novelty of C1, C2, C5, C6 (no aimed searches); whether any vehicle supports catalogue-scale pool control and recovery; the frontier count effect; the meaning of the step requirement; whether brief 1.2 binds the main contribution.
- **Step 2 would accomplish:** a verified answer on vehicle capability and on whether four candidate gaps are already filled. It would not settle any effect size.
- **Authorisation needed next:** your answers to section 7 (at least question 1) and, if you want Step 2, authorisation for 2a and later 2b.
