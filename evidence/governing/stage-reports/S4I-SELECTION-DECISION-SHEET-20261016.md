# Selection decision sheet: what you need in order to choose and formulate the primary question

- Date (UTC): 2026-10-16. Coordinator: Sonnet 5.5. Authority: D13. Built only from the existing Step 3 evidence (S4G v2 and its sources) **with the S4I governing erratum applied** (`candidate-questions/S4I-GOVERNING-ERRATUM-20261016.md`). No search, review, experiment or candidate generation was run; nothing here selects, ranks, freezes or designs.
- Labels: **F** fact in a stored record; **I** interpretation; **Unk** unknown; **[User]** your decision; **[Sup]** a supervisor expectation you have not resolved. "Primary" means the question whose answer is the thesis claim. "Supporting" means an experiment that makes the primary claim measurable or protects it, and is not itself the thesis claim.

## 1. The two decisions that are required

1. **Contribution-type rule [User][Sup].** Do the brief's Required policy-form items (R5 a policy with a way to query omitted tools; R8 stepwise, each step saving tokens; R9 graded exposure as a lens) bind the *main contribution*, or is a findings-type or evaluation contribution sufficient (R7: findings on what works in which cases)? Evidence: the supervisor's words on "each step saves tokens" are hedged and followed by a global lens (transcript L462-L476); the brief keeps both a findings cue and a policy cue. The record cannot settle this.
2. **The primary direction and its scope boundaries [User].** Pick one of the arrangements in section 3 (or a different arrangement of C1-C6), and accept or decline: the staged-disclosure / omitted-catalogue family as the scope; exclusion of tool-output and history overhead, session working-set management and content-level compression as *primary* subjects; client-side classes only for any class comparison.

Everything else in section 5 is deliberately left open.

## 2. What each candidate can be (primary or supporting)

Requirement keys: R1 reduce model-visible tokens; R2 maintain performance vs all-tools; R3 count discovery/selection/execution overhead; R4 judge savings globally over turns; R5 policy with a recovery path; R6 baselines (all-tools, existing projects, published methods); R7 findings on what works when; R8 stepwise; R9 graded exposure; R10 use existing work.

| | Can it be primary? | Primary claim it would carry (indicative wording, not frozen) | Supporting experiments it needs | Nearest prior art and limits (qualified) | Falsifier |
|---|---|---|---|---|---|
| C1 | No, supporting on current evidence. Two reduced forms exist (presence term alone; absence-by-presence needing observable alternatives) | Split of success lost under restriction into absence and presence terms | Is the loss budget and the miss-stratum definition for C2/C3 | ToolMATH, CAM-DF (7 tools), DynamicMCPBench App. N/S; factorial not found (3 queries). Absence is near-mechanical on the replay vehicle | Both effects within noise; loss predicted by recall alone |
| C2 | **Yes** | Value and cumulative-token price of a recovery path after an omitting exposure, including where nothing was missed, versus no recovery and versus an equal-cumulative-token static exposure | C1's forced-absence arm (miss stratum); C5 as pre-registered robustness | FitText (closest, confounded: raw-query static baseline, LLM judge, simulated server), ComplexMCP iterative search, PlanBench-XL, SING/MCP-Zero. Distinctive elements not found (3 queries) | Recovery restores little, is dominated by the matched static comparator, or restores nearly all at negligible price (question closed); all reportable |
| C3 | **Yes, if restricted to client-side classes** (your scoping decision) | Which client-side exposure classes are non-dominated on (cumulative tokens by category, end-to-end success) over trajectories, and whether that set changes with catalogue size and model strength | C5 (accounting conventions are inherent); C1-presence as size covariate; C2 only if recovery belongs to a class | DynamicMCPBench App. N, Skill Blocks (skills), ToolMenuBench (synthetic), MemTool, compgateway, **Toollery (single-step, method authors) and the CE-MCP study (1-3 servers, 34 tasks, LLM-judged, figures only), added by the erratum**. Increment may be a reporting increment. Code-mediated named baseline is outside a client-side scope | One class dominates throughout; differences within noise at available power; frontier unstable across models or harness |
| C4 | No; primary only under a mechanistic-thesis reading | Whether count, total tokens, overlap or detail level drives selection loss at matched tokens | A single-step harness (the vehicle does not serve it) | LongFuncEval, SLCA-GRPO, ToolMATH, flood test, Du et al., BoR, App. S; matched-token control not found after repeated searches | No effect beyond length, or effect only for weak models |
| C5 | No, supporting on current evidence (analysis layer) | Stability of exposure-policy conclusions across accounting conventions, evaluators and horizon | Logs from another study (none exist yet); double-graded subset | ETC grid, scaffold effect, token spend, on-device simulators, tokennotcost, **one in-domain single-step cache-regime instance (Toollery B.2), added by the erratum**; stability across conventions × evaluators × horizon not found | Conclusions invariant over plausible conventions |
| C6 | **Only if** a designed stepwise policy is the intended contribution [User][Sup] | Which steps of an ordered staged-disclosure policy pay (under a reading of "pays" fixed before running), whether they interact, and whether a composed policy chosen without looking at evaluation tasks is non-dominated | C2 (the recovery step is C2's toggle); C3 baselines; C5 | Executor and vendor deferral (shipped); Skill Blocks stubs (skills); on-device ablation, ITR, Tool Attention (**at least three** uneven component-ablation sources, per the erratum). Mechanism novelty low by construction; controlled deterministic held-out ablation not found (2 queries) | No step pays net of overhead; composed policy dominated by static restriction or all-tools; effects unstable across models; or the "pays" reading chosen after seeing results |

## 3. Three arrangements, primary versus supporting (conditional, not ranked)

| | A: recovery-centred evaluation | B: controlled class comparison | C: stepwise design with component evidence |
|---|---|---|---|
| **Primary claim** | C2 | C3 (client-side) | C6 |
| **Supporting experiments** | C1 (loss budget, miss stratum); C5 (robustness) | C5 (inherent); C1-presence (size covariate) | C2 (recovery step), C3 baselines, C5; A is a component of C |
| **Contribution type** | Evaluation of a policy component | Evaluation at class level | Design with validation |
| **Requirements met as primary** | R1-R3, R5, R7 (partly), R6 (partly) ; R4 only if sessions are built | R1-R3, R5, R6 (partly), R7, R10; R4 partly | R1-R3, R5, R6 (partly), R8-R10; R7 through step findings; R4 only if sessions are built |
| **Fits if** | a findings-type or evaluation contribution suffices and defensibility within bounded effort matters most | you want the broad comparative answer and accept client-side scope | the Required policy-form items bind the main contribution, or the supervisor expects a designed policy |
| **Main risk** | Core effect partly covered (FitText); a closed-question outcome; harness and replay dependence | Reporting increment over App. N, Toollery and CE-MCP; accounting comparability; excludes the code-mediated named baseline | Per-step results that are token arithmetic; same-data composition; collapse toward B under reading (c) of "pays"; depends on the supervisor's meaning |

R6 is partial in all three if the code-mediated existing project is not an arm. None of A, B, C is established as novel (two or three queries per gap) or as feasible (vehicle code read, never run).

## 4. Corrections already incorporated (so you do not have to carry them)

- Erratum Q-1 to Q-4 (cache-regime wording for C5; Toollery and CE-MCP as C3 near-misses; "at least three" for C6; the Dynamic ReAct efficiency claim is unsupported and not to be cited).
- Replay scoring on the closest vehicle penalises routes the single reference did not exercise; the direction of the bias is **Unk** and for C2 may *inflate* recovery's measured value (S4G §2). The fixed 12-turn budget handicaps discovery-heavy arms; magnitude **Unk**.
- Only 1,578 of 1,845 specs are reference-consistent; margin-dependent sample sizes in S4G are illustrations.
- Paper versions: the records cite the stored versions (MCPVerse v2, MCP-Atlas v3, LiveMCPBench v2); none of the v1 differences touches a C1-C6 assertion (B-1).
- "Executor" as the supervisor-named baseline is an identification made in the S4D records, not in the transcript lines; "each step saves tokens" has two textually possible readings.

## 5. Left open on purpose (no evidence-based default)

| Open item | Why it cannot be settled now | Owner |
|---|---|---|
| Margin for "maintained" (D-f) and primary-outcome formulation (D-a: tokens, money, or both) | Scientific choice; sample size depends on it | [User][Sup] |
| Meaning of "each step saves tokens" (per step or collectively) and of "pays" (five admissible readings (a)-(e), none chosen) | Transcript supports both; falsifier of C6 depends on it | [Sup] |
| Whether a mechanism, evidence or evaluation contribution counts as novel (D-g) | Supervisor expectation | [Sup] |
| Whether the code-mediated or provider-native existing project must be a baseline arm (D-i, R6) | Changes B's and C's scope | [User][Sup] |
| Models, catalogue sizes, number of repeats, resource tier | Resources unspecified | [User] |
| Whether the model's initiation of search or recovery is a measured variable | Initiation failures appear in stored sources (e.g. MCP-Atlas v3 reports strong models refusing to invoke tools on a substantial share of failures) but no candidate design names it | [User] |
| Replay-usable task count, unexercised-route and turn-budget effects, vehicle behaviour | Needs a smoke execution, which no record authorises | [User] to authorise or not |
| Architecture, infrastructure, coefficients, price tables | Not chosen anywhere | open |

## 6. To formulate the question (fill-in; I will not fill it for you)

1. **Primary claim type:** finding / evaluation / policy with validation.
2. **Contrast:** which arms, what is manipulated, what is held fixed.
3. **Regime:** catalogue-size range, model strengths, trajectory versus session horizon.
4. **Outcomes and their roles:** primary outcome; constraint (non-inferiority and its margin); diagnostics; overhead categories counted.
5. **Falsifier(s)** stated before running, both directions where possible.
6. **Supporting experiments** (from section 2) and what each is allowed to claim.
7. **Scope exclusions** (section 1 item 2).
8. **Open items you carry forward** (section 5) and who resolves each.

## 7. State at stop

The S4H audit tickets are closed for selection purposes (erratum, "Closure of audit tickets"). S4G's proposed default of a smoke execution of the vehicle as a gate before the *design* is frozen (not before the question) remains a proposal, not authorised. No Stage 5, no selection, no freeze. This sheet ends at your selection decision.
