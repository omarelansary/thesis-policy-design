# Candidate dossier: narrower research-question candidates (existing evidence only)

- Date (UTC): 2026-10-14. Authority: `decisions/D5-candidate-formation-authorization.md`. Coordinator: Sonnet 5.5. Version **v2**, after the independent challenge (`audits/S4D-C1-…`, dispositions `audits/S4D-V1-…`). v1 (commit a63457a) is preserved in git. v2 corrects errors the challenge and my re-checks found (section 9) and adds a sixth candidate.
- This dossier selects no research question, ranks no candidate, fixes no coefficient, margin or architecture, runs nothing and starts no Stage 5. D-a to D-j are open; each candidate carries them as parameters.
- Sources: the approved clean-room corpus through Stage 4c, the Step 1 outputs and the admitted 2 October requirements. No searches, fetches, previous-thesis material or other meetings. Ids: N1-N13, P1-P3 = findings/probes in `stage-reports/STAGE4C_DECISION_EVIDENCE_DOSSIER-20261013.md` (with the errata in `audits/S4D-V1-…` section 3); "4b" = the Stage 4b synthesis/map with C3's corrections; `source-id Lnnn` = a line in `evidence/source-text/<id>/text.txt`; "via 4b/4c" marks a statement I did not re-read in this step.
- Labels: F fact in a source, I interpretation, U unknown, S speculation. Novelty, alignment, identifiability, statistical feasibility and practical feasibility are reported separately and never combined or ranked. "Not found" always means not found under the Stage 4/4b/4c bounds, and for C1 no logged query was aimed at the gap, while for C2, C5 and C6 only adjacent queries exist (section 5).

## 1. Alignment boundary: requirements from the approved brief and the transcript
**Overarching thesis problem (brief section 0):** reduce total model-visible input tokens associated with accessing large tool catalogues while maintaining end-to-end task performance, accounting for discovery, selection and execution overhead; its validity is open to challenge. It bounds what a candidate may address and is not evidence for any mechanism.

| ID | Requirement (status in the brief; transcript) | Applies to |
|---|---|---|
| R1 | Reduce model-visible tokens spent on tool access (Required; L316-L330) | all |
| R2 | Maintain end-to-end performance relative to the all-tools baseline (Required; L132-L136) | all |
| R3 | Count discovery, selection and execution overhead (brief section 0; L154-L156) | all |
| R4 | Judge savings globally over turns (Required; L468-L476) | all |
| R5 | A policy, not only retrieval (Required; L281-L285), with a way to query omitted tools when filtering is wrong (Required; L466) | solution form of a policy contribution |
| R6 | Baselines: all-tools, existing projects, published methods (Required; L132-L136, L344-L370) | all |
| R7 | Findings on what works in which cases (L142-L152) and "figure out [the] algorithm" (L152) (contribution cues; the L189-L194 cue is tied to the student's earlier finder, 4c dossier section 1) | contribution type |
| R8 | Stepwise structure in which each step saves tokens (Required; L462-L464) | solution form of a policy contribution |
| R9 | Graded or partial exposure as a lens, not a mandate (Required "as a lens"; L336-L338) | solution form of a policy contribution |
| R10 | Use and improve existing work; do not reinvent (Required; L351-L353) | all |

**Tension recorded, not resolved:** brief section 0 says no architecture is favoured. R5, R8 and R9 are therefore treated as requirements on the *form* of a policy-type contribution; evaluation or mechanistic candidates are not required to satisfy them but must say how they relate. The 4b synthesis treats graded exposure as a lens rather than a mandate while the brief records it as "required as a lens"; this dossier follows the brief.

**Illustrative only (Example in the brief):** the 100/60/20/40 counts ("not rigid", L332-L338), names-only for the lowest tier, query expansion, the 27B filter model, "steps three to five, something like this", the hedged 50% remark. No candidate is built on these. Graded or hierarchical exposure appears as one class in C3 and as a factor in C6, and the resemblance is flagged where it occurs.

**Formulation menu carried unresolved:** F1-F7 of `STEP1_ADDENDUM_D-A_FORMULATION-20261014.md`.

## 2. Candidate set at a glance
| ID | Narrower question (short) | Type | What it can establish | What it cannot establish |
|---|---|---|---|---|
| C1 | How is the success lost under restricted exposure split between absence of required tools and presence of other tools? | evaluation with causal content | simple effects of absence and presence across scale, depth and model; non-additivity | whether any policy avoids misses; cumulative tokens including discovery; cost |
| C2 | What does a recovery path restore after a miss, at what cumulative-token and turn price, including on tasks with no miss? | evaluation of a policy component | value and price of recovery vs no recovery and vs an equal-cumulative-token static exposure | the best initial exposure; cost without prices |
| C3 | Which exposure-policy classes are non-dominated on (cumulative tokens by category, success) over trajectories? | evaluation at policy-class level | which classes are dominated in the tested conditions | why (mechanism); a new method |
| C4 | Does selection degrade with tool count, total tokens, semantic overlap or visible-detail level for current models? | mechanistic | factor structure of selection degradation at the tested scale | cumulative tokens, overhead, multi-turn effects, policy effectiveness |
| C5 | Do conclusions about token-reducing exposure survive changes of accounting convention, evaluator and horizon? | evaluation methodology | when token- and cost-based or short- and long-horizon views agree or diverge | which policy is best; mechanism |
| C6 | For an ordered, stepwise exposure policy whose steps must each save tokens, which steps pay net of overhead, and does a composed policy dominate baselines? | policy design with validation | which steps pay, and whether a composed policy is non-dominated in the tested regime | that the mechanism is novel; transfer beyond the tested harness and models |

**Considered and not formed (not eliminated):** security of discovery (needs a change of objective, 4b); capacity as an objective (arithmetic); objective validation by real-use traces (the public trace set does not separate tool definitions, N8); a break-even horizon model (a parameter in C3, C5, C6); another retriever, description rewriting, a new benchmark (rejected on evidence in 4b, not revisited). The v1 reason for not forming a policy candidate ("any X is an architecture choice") is withdrawn: C6 states the policy question architecture-agnostically.

## 3. Lineage to earlier items (disclosed, with changes of treatment)
| Candidate | Descends from | Earlier verdict | Treatment here |
|---|---|---|---|
| C1 | RQ-B / D-RECALL (recall dose-response) and the distraction term of D-REL | 4b: RQ-B "retained only as a factor"; PlanBench-XL and CAM-DF support demotion | reformulated as an attribution (simple effects) question; the demotion is neither endorsed nor reversed; the challenge says its core is weakened (section 4) |
| C2 | RQ-B's fallback arm; the recovery requirement R5 | 4c: recovery "not resurrected as standalone" | formed as a standalone candidate because recovery is a binding requirement and D5 authorises formation; a change of treatment, not of epistemic status |
| C3 | RQ-A / D-COST broadened; K-C as one class | 4b C3: D-COST "not defensible as worded"; cost-prediction estimand abandoned | estimand is non-dominance on (tokens, success), not cost prediction |
| C4 | D-REL cut down (contrasts a and b) plus the residue-tier contrast (c) | 4b/C3: D-REL defensible only as targeted contrasts, not shown novel | contrasts kept; residue tier restored as factor (iv) |
| C5 | RQ-A (ii)-(iii) accounting residual, K-D, and the L9 validity question | 4b: cache-break accounting rejected as non-durable | different estimand (stability of conclusions), same arithmetic risk, stated |
| C6 | K-C (graded exposure policy) and the 4c policy/method row | Stage 4: rejected as a standalone method contribution (shipped practice; disguised-answer check failed as worded) | the K-C verdict about the mechanism stands; C6 claims evidence about components, not mechanism novelty, and must be answerable "no step pays" |

## 4. Candidate records

### Parametric conventions used below (corrected in v2)
- Paired contrast on binary success: n = 7.84 (d/R + tau^2) / D^2 (P2 form; D = detectable difference or margin; d = discordance; R = runs per task; tau = policy-by-task interaction), 80% power, one-sided 0.025 (or two-sided 0.05 for superiority). Assumptions as P2.
- Factorial: in an equal-cell 2x2, a simple effect has variance 2 sigma^2/n, a main effect averaged over the other factor sigma^2/n, an interaction 4 sigma^2/n; interactions are usually smaller than main effects, so the n for an interaction is several times that for a main effect.
- Ratio estimands (e.g. fraction of loss restored): precision degrades as the denominator shrinks; use Fieller-type intervals, not the delta method, when the loss interval approaches zero.
- Pareto/dominance claims: both axes must pass (intersection-union), so power is lower than for either axis alone; "attribution shares" are not unique under interaction (report simple effects).
- Multiplicity grows with cells and arms; the number of cells, arms and models is a design parameter, not a fixed number.
- Token axis: variance across trajectories is not established; one source reports that a roughly 2% effect was "drowned by turn-count variance" and that only distributions over three or more runs are trustworthy (s4-compgateway, via 4b; U). No claim is made that the token axis needs fewer tasks.
- Compute volume: attempts = tasks x arms (or cells) x R x models; input tokens = attempts x tokens per attempt (pilot output; 3.4k-25.7k per attempt in one benchmark, and a whole-catalogue prompt 10-30x that of any other cell, author-stated, dynamicmcpbench L1030-L1031).

### C1. Absence versus presence: attributing exposure-induced success loss
- **Precise question:** Relative to a reference exposure (all tools where feasible, otherwise curated), how is the end-to-end success loss under a restricted exposure split between (a) the absence of required tools, net of alternative paths, and (b) the presence of other tools (count, tokens, overlap), reported as simple effects with their interaction, across catalogue size, cut depth (including moderate cuts) and model strength?
- **Type:** empirical evaluation with causal (mechanistic) content.
- **Motivation:** the one public decomposition reports k=8 retrieval loss of -16.0 to -23.3 points across four models (strongest lose most) and an 8.0-point drop for all 1,168 tools on one model (dynamicmcpbench L1014-L1058); it is descriptive: retrieved pools are nearest-neighbour hard distractors, reachable tasks are easier, no paired interval is given, per-cell intervals are about +-8, and reachability is defined through equivalence sets, which already absorbs substitution (L1004-L1009).
- **Alignment (separate):** addresses R2 (accuracy side) and, through the token vector of the pools, part of R1; with an all-tools arm it addresses R6 partly; informs R5 and R7. Does not address R3, R4, R8-R9.
- **Compatible formulations:** F4/F5 (success against exposed-token level); F1/F2 as slices.
- **Assumptions:** a vehicle with deterministic effect scoring or annotated required tools; ability to construct pools independent of a retriever (U; not verified on any public vehicle, N11); independent runs given the task.
- **Measurement requirements:** manipulated: required-tool presence (all / some / none), number and type of other tools, model; outcome: end-to-end success by deterministic checks (note evaluator error structure, section 4/C5); per-attempt token vector; alternative-path success among tasks with a required tool absent (CAM-DF reports 24% in its "insufficient" condition); analysis on probability and logit scales, because a floor near zero when a tool is absent can manufacture an interaction; an all-tools arm where feasible.
- **Nearest prior art:** ToolMATH (gold-only, gold-present and distractors-only conditions, similarity levels and distractor budgets to 50, separate Adaptability and Robustness diagnostics, six models including Claude-4.6, GPT-5 and Gemini-3.1-Pro, a hard split where tools are necessary; Adaptability figures are for three non-frontier models and tool optionality limits their meaning: toolmath L213-L218, L244, L362-L370); CAM-DF (insufficient and full-vs-oracle contrasts, 0.67 / 0.24 / 0.58, a distraction contrast that did not replicate under a second simulator, s4-costaware-acq near L1023-L1050); DynamicMCPBench Appendix N; PlanBench-XL (blocking with discovery always available); TheMCPCompany (Missed Tools 12.5% of retrieval-only failures, instruction drift dominant: L1144-L1150); CloudUse (end-to-end accuracy modelled as recall times selection accuracy given recall, s4-clouduse L1192-L1195, via 4b); LongFuncEval; SLCA-GRPO; Bitter Lesson flood test (n=31).
- **Residual gap (bounded):** a manipulated absence-by-presence factorial at catalogue scale on real tool-calling tasks with a token vector and several models. No logged query was aimed at this gap, so "not found" rests on coverage not designed for it.
- **Alternative explanations:** absence is close to tautological under effect scoring; what remains is C4's question measured end to end; ToolMATH and CAM-DF may already provide the qualitative result; tasks solvable without tools make exposure effects uninformative.
- **Falsifier:** both effects within noise for current models; loss predicted by recall alone (CloudUse form) with no presence-by-absence interaction; negligible alternative-path success so that absence equals failure.
- **What would invalidate the contribution:** a published manipulated factorial of this kind; evidence that the closest vehicle cannot build required-plus-r pools and no substitute exists.
- **Identifiability:** catalogue size, cut depth and r are algebraically linked under forced inclusion (pool = required + r; cut = 1 - pool/N), the same over-parameterisation C3 found in D-REL; only a subset of these can be crossed. "Curated" as the reference does not satisfy the all-tools baseline in R2.
- **Statistical feasibility:** per simple effect, n by the paired-contrast form; interaction several times larger; cells multiply attempts; multiplicity across cells.
- **Practical feasibility (parametric):** pool size drives tokens per attempt; the vehicle question is open.
- **Can establish:** simple effects of absence and presence, and whether they interact, in the tested regime. **Cannot:** unique attribution shares; that a policy avoids misses; discovery overhead; cost.
- **Challenge outcome (preserved):** its non-trivial content may already exist at small scale in ToolMATH and CAM-DF, and its absence term is near-tautological on the closest vehicle; if sustained, the remainder is C4 end to end.
- **Epistemic status:** plausible within bounds; novelty uncertain and weakened by the prior art above; identifiability limited by the algebraic link and the scale dependence.

### C2. The value and price of a recovery path
- **Precise question:** When an initial restricted exposure omits a required tool, how much of the lost end-to-end success does a recovery path restore, and what does it add to cumulative model-visible tokens (by category) and turns, relative to (a) no recovery and (b) a static exposure with the same cumulative tokens, measured on tasks with a miss, tasks without a miss, and at the natural miss rate?
- **Type:** empirical evaluation of a policy component.
- **Recovery is defined by interface:** the system can obtain omitted tools after a miss. Two families are treated as a factor: model-initiated (the model queries the omitted catalogue) and system-initiated (error-triggered re-retrieval or escalation to a larger exposure). The query-formulation quality of model-initiated recovery is a second factor.
- **Motivation:** the supervisor requires a way to query omitted tools when filtering is wrong (L466). Retrieval is the largest error class in one failure taxonomy (50.00%, two Claude models, one framework, 4b); in another benchmark, missed tools are 12.5% of one model's failures while instruction drift dominates (TheMCPCompany L1144-L1150). PlanBench-XL always gives discovery and shows that extra enforced exploration adds less than 5 points (s4b-wd-planbenchxl L537-L558), so recovery effectiveness is evidently bounded by something other than permission to search.
- **Alignment:** addresses R1, R2, R3, R5, R6 (no-recovery and static baselines); R4 only if session reuse is modelled; R7 partly; R8/R9 not required.
- **Compatible formulations:** F1-F5; F4/F5 most natural.
- **Assumptions:** misses can be induced or identified; injected misses are unlike real retriever misses (4b objection), so natural misses must also be sampled; the harness holds the search backend fixed.
- **Measurement requirements:** success; token vector including search and describe calls and returned schemas; turns; over-search cost on tasks without a miss; natural miss prevalence; comparator (b) at equal cumulative tokens as primary and equal initial tokens as secondary (an equal-initial-token comparator is nearly degenerate); a presence-without-use control, acknowledged as difficult because any extra tool changes behaviour.
- **Nearest prior art:** SING and MCP-Zero (active discovery; success tables compare only ground-truth servers, MCP-Zero and SING; Embedding-only is in the discovery tables only: sing L340-L347, L433-L453); Executor (names first, describe, suggestions on a missed path; no token logging in the files read, P3); provider tool search (vendor claims unreproduced); PlanBench-XL; CAM-DF; TheMCPCompany (search persistence, L631-L633 via 4b); ToolMenuBench (lists recovery-menu filtering as future work, via the challenge); LiveMCPBench taxonomy.
- **Residual gap (bounded):** fallback on/off at a controlled miss with an equal-cumulative-token static comparator and cumulative accounting. Only an adjacent query (S4-Q007) exists; none was aimed at it.
- **Alternative explanations:** recovery effectiveness is a property of harness, prompt and model persistence; provider-trained search interfaces may not transfer; vendor-internal evaluations may exist.
- **Falsifier:** recovery restores little, or is dominated by the static comparator at equal cumulative tokens; or restores nearly all at negligible cost (question closed). Both reportable.
- **What would invalidate the contribution:** a published paired fallback toggle; a demonstration that results are fully harness-dependent.
- **Identifiability:** estimand is "recovery family X under harness H" conditional on how misses arise; the conditional-on-injected-miss estimand cannot by itself show net value (over-search and natural prevalence are required).
- **Statistical feasibility:** contrasts by the paired form; the restored fraction is a ratio (Fieller intervals; needs a minimum loss).
- **Practical feasibility (parametric):** multi-turn volume; a provider-native arm needs an accounting convention (N4).
- **Can establish:** where recovery pays and where it is dominated, in tokens and success, including its cost on tasks without a miss. **Cannot:** the best initial exposure; cost without prices.
- **Challenge outcome (preserved):** the value of recovery depends on harness, prompt and persistence, so any result may describe one harness and an assumed miss rate; the 4c "monotone decline" motivation was a misread and is corrected.
- **Epistemic status:** plausible within bounds; mechanisms are published or shipped; the gap is an evaluation gap.

### C3. Policy classes on the (cumulative tokens, success) plane
- **Precise question:** Across exposure-policy classes (static full; static restricted by lexical or dense retrieval; deferred with on-demand schema; hierarchical or graded; code-mediated), which are non-dominated on cumulative model-visible tokens by category and end-to-end success over task trajectories, and does the non-dominated set change with catalogue size, session length and model strength?
- **Type:** empirical evaluation at policy-class level (one architecture-agnostic reading of "find the policy"; C6 is another). Graded exposure is one class and gets no privilege.
- **Motivation:** shipped and published classes exist; a controlled head-to-head with success and token categories is not found under the bounds; nearest comparisons are for skills, synthetic, or confounded.
- **Alignment:** R1, R2 (through a stated non-inferiority test or frontier analysis; a Pareto analysis alone does not test "maintained"), R3, R5, R6, R10 addressed; R4 partly; R7 through findings on which classes pay.
- **Compatible formulations:** F4/F5; F1-F3 as slices; F6/F7.
- **Assumptions:** classes implemented under a common harness; all-tools feasible at tested sizes (N3); an accounting convention for provider-native and code-mediated arms.
- **Measurement requirements:** token vector by category and model; success by deterministic checks with evaluator-error awareness; turns; repeats; session-length sweep. **Unidentified quantity:** comparable token accounting across client, provider-native and code-mediated classes (programmatic results are excluded from usage: r4-anthropic-ptc L1433), which is not an assumption but an open measurement problem.
- **Nearest prior art:** Skill Blocks (four mechanisms, paired, cache-read-discounted, skills); ToolMenuBench (six methods, synthetic and mocked, privileged-information filter by the same authors); MCPVerse; compgateway (priced at cache tiers, no success); r4-scaffolding; TheMCPCompany; SING/MCP-Zero; DynamicMCPBench App. N (rag/hier/flat, 150 tasks, flat on one model); MemTool (multi-turn dynamic tool removal across modes, s4-memtool L20-L35 via the challenge); vendor claims.
- **Residual gap (bounded):** independent, controlled head-to-head of at least two classes on one tool-catalogue workload with success, token categories and repeats. Several targeted searches (Stage 4, 4c) found none; near misses are listed.
- **Alternative explanations:** harness effects may exceed policy effects; provider co-training; obsolescence; the gap may be a reporting increment (token categories, repeats) over existing comparisons.
- **Falsifier:** one class dominates throughout; differences within noise at the available power; the frontier unstable across models.
- **What would invalidate the contribution:** a published controlled comparison; a harness-dominance result.
- **Identifiability:** estimand is "mechanism plus its required scaffolding"; no single-factor attribution; joint dominance needs an intersection-union test.
- **Statistical feasibility:** pairwise contrasts by the paired form; joint dominance lower power; multiplicity across arms.
- **Practical feasibility (parametric):** the largest implementation and accounting burden of the set; baselines per D-i.
- **Can establish:** which classes are dominated in the tested conditions. **Cannot:** why; a new method; durability.
- **Challenge outcome (preserved):** the gap may be a reporting increment; "mechanism plus scaffolding" does not transfer; a Pareto analysis does not test "maintained" without a margin P2 shows is unattainable below about 8 points on most stored benchmarks.
- **Epistemic status:** plausible within bounds; identifiability limited by scaffolding and accounting comparability.

### C4. Which property of a catalogue degrades selection?
- **Precise question:** For current models and catalogues within their windows, does tool selection (single-step or short multi-step) degrade with (i) number of tools at fixed total tokens, (ii) total tokens at fixed number, (iii) semantic overlap at fixed count and tokens, or (iv) the amount of per-tool detail visible at fixed count (for example name only, name with description, full schema), and does this depend on model strength and on tool-set realism?
- **Type:** mechanistic investigation.
- **Motivation:** vendor capacity heuristics disagree with no stated basis (via 4b); LongFuncEval confounds count and length by construction; evidence on frontier models is mixed and weak (N6).
- **Alignment:** informs R1 and R2 (what content can be hidden without losing accuracy); R7 as the "why" side only; does not address R3-R5, R6 beyond the all-tools accuracy as a function of the catalogue (no existing-project baselines), R8-R9 (factor (iv) is the evidence the "lens" R9 would rely on, but it is a factor, not a policy).
- **Compatible formulations:** coefficient-free; supplies the success-exposure relation used inside F4/F5.
- **Assumptions:** contrasts constructible as in P1: overlap at fixed count and tokens by selection; count at fixed tokens either with schema size and descriptive text varying together (a granularity-type question) or by padding (a different construct, Du et al.); both pre-registered separately. "Realism" is defined operationally as real-registry schemas versus templated synthetic schemas, and by the schema-length distribution.
- **Measurement requirements:** single-step accuracy with deterministic checks (AST or effect), a no-tool control, token counts per prompt, model strength levels.
- **Nearest prior art:** LongFuncEval; SLCA-GRPO; ToolMATH; Bitter Lesson flood test; ToolMenuBench; MCPVerse; Du et al.; Tool-DC; Less-is-More on small models (s4b-wb-lessismore L25-L30, via the challenge); DynamicMCPBench; provider differences in residue (OpenAI keeps name and description of deferred tools visible; Anthropic only the search tool: via 4b).
- **Residual gap (bounded):** a token-matched count control for function calling and a crossed overlap contrast for current models; several targeted searches found none.
- **Alternative explanations:** the general length effect; frontier saturation; padding type defines the construct; model-version dependence.
- **Falsifier:** no effect beyond length; effect only for weak models; overlap explains everything; detail level irrelevant.
- **What would invalidate the contribution:** a published token-matched study; vanishing effects for current models in realistic regimes (a bounded null, reportable).
- **Identifiability:** P1: overlap measured with a lexical proxy is circular; schema length tracks descriptive text and parameter count together (Spearman 0.94 and 0.86; 0.78 and 0.65 between them), so contrast (i) varies complexity and informativeness unless padded; factor (iv) is confounded with total tokens unless matched.
- **Statistical feasibility:** item-level paired contrasts by the paired form; interactions with model strength several times larger.
- **Practical feasibility (parametric):** items are cheap but prompts with many tools are long; conclusions are limited to the models run.
- **Can establish:** factor structure of selection degradation at the tested scale. **Cannot:** cumulative tokens, overhead, multi-turn behaviour, policy effectiveness, cost.
- **Challenge outcome (preserved):** it does not measure the thesis objective (4b's original objection); factor (iv) was restored because it is the link to exposure design and was dropped without reason in v1.
- **Epistemic status:** plausible; novelty uncertain; reportable outcomes include a bounded null.

### C5. Stability of conclusions across accounting conventions, evaluators and horizons
- **Precise question:** For token-reducing exposure policies, do the conclusions (ordering, Pareto non-dominance, and the claim that accuracy is maintained) remain stable across (i) accounting conventions: raw model-visible tokens, cache-discounted effective tokens, price-weighted cost under varied cache regimes and filter-model price ratios, and the divergence between usage-reported and model-visible tokens for server-side or programmatic mechanisms; (ii) evaluators: deterministic effect or state checks versus LLM judges, both of which have documented error structures; (iii) horizon: per request, per trajectory, and as a function of session length? A "flip" is defined as a change in the ordering or in a dominance relation under a convention change, with its frequency estimated by bootstrap over tasks.
- **Type:** evaluation methodology (sensitivity analysis). It can ride on the runs of other candidates or on published tables; it is a separate estimand, not a separate experiment.
- **Motivation:** token reduction does not imply cost reduction (cached reads about a tenth; a 38.4% reduction in delivered tool-output tokens raised billed cost by 6.8% with CI [+2.8, +11.3], r3-tokennotcost L18-L22; a cache-hit drop from 100% to 25% that lasted one turn, r4-missing-memory-hierarchy L717-L721; vendor-reported 77% modelled vs 13% measured savings, N8); evaluators disagree with humans on 18.5% of audited tasks across deterministic (BFCL, tau2) and LLM-judged benchmarks, with a 23-rerun range of 57.9-76.8% (SD 5.4) in one pipeline (r3-validityaudit L12-L19, L412-L416, L496-L497); DynamicMCPBench's deterministic scorer has 230 false negatives (L986-L991).
- **Alignment:** addresses R1 (how tokens are counted), R3, R4; R2 partly (evaluator sensitivity); informs R6; not R5, R8, R9.
- **Compatible formulations:** all of F1-F7; produces the coefficient regions of F5.
- **Assumptions:** usage-level or per-attempt logs for at least two policies on the same tasks; declared price and cache models.
- **Measurement requirements:** per-attempt token vector; conventions applied post hoc to the same trajectories; at least two evaluators on the same outputs; session-length sweep; flip frequency.
- **Nearest prior art:** r3-tokennotcost; CAPC (two-tier cost model, aggregate reconciliation within 1%, via 4b); Skill Blocks (d=0.1 sensitivity); validity audit; Missing-Memory; compgateway; TraceLab (prefix 59.5% of estimated cost in coding agents); the vendor blog.
- **Residual gap (bounded):** stability of exposure-policy conclusions across conventions and evaluators. Only an adjacent query (S4-Q010) exists; none was aimed at it.
- **Alternative explanations (main weakness):** given a trajectory, cost is a deterministic function of the token vector and prices, so convention sensitivity is partly arithmetic; its non-arithmetic content is policy-dependent cache behaviour and trajectory variation (needs provider logs) and evaluator error structure.
- **Falsifier:** conclusions are invariant over plausible conventions (tokens suffice as a proxy), or flip only under implausible coefficients.
- **What would invalidate the contribution:** showing that it reduces to arithmetic with no trajectory- or cache-dependence; or existing work already giving the sensitivity.
- **Identifiability:** post hoc conventions are identified by construction; real cache behaviour only from provider runs.
- **Statistical feasibility:** flip frequency by bootstrap over tasks; evaluator effects need a double-graded subset; no closed formula is claimed.
- **Practical feasibility (parametric):** cheapest variant is a re-analysis of published per-attempt tables (which lack cache fields); fuller variants reuse other candidates' logs.
- **Can establish:** when views agree or diverge for the tested policies. **Cannot:** which policy is best; mechanism; behaviour at untested prices.
- **Challenge outcome (preserved):** it is in practice a sensitivity component of C3 or C2 (disclosed), its accounting arm is arithmetic, and its v1 grader framing rested on a misread (corrected here).
- **Epistemic status:** plausible; novelty uncertain; arithmetic risk substantial.

### C6. A stepwise exposure-policy family: which steps pay, and does a composed policy dominate baselines?
- **Precise question:** For an exposure policy specified as an ordered sequence of steps each required to save tokens (the approved structure), with generic degrees of freedom (what is visible at the start, how much per-tool detail is withheld, what triggers expansion), how much does each step save in cumulative model-visible tokens by category net of overhead, what does it cost in success and turns, do the steps interact, and does a composed policy of the steps that individually pay dominate the all-tools and static-restriction baselines over trajectories?
- **Type:** policy design with validation (design plus evaluation). No instance of any step is specified here; steps are factors.
- **Resemblance flagged:** the step structure comes from the approved requirements (R8, R9, R5), not from the numbers or tier layouts the supervisor gave as examples; it is the candidate most directly shaped by the supervisor's stated structure, and is conditional on the user wanting a policy contribution.
- **Motivation:** the approved brief requires a stepwise, token-saving, recoverable policy; component evidence on which steps pay in tool catalogues is thin: stubs and detail levels exist in practice but are measured on one task or unmeasured (via 4b).
- **Alignment:** R1-R6, R8-R10 addressed as a design; R7 through the finding on which steps pay.
- **Compatible formulations:** F1-F5; each step's requirement "must save tokens" is a net-savings sign condition (net of overhead), evaluated before any margin or coefficient.
- **Assumptions:** factors implementable generically across a harness; baselines per D-i; an accounting convention for server-side steps (N4).
- **Measurement requirements:** add-one and leave-one-out step ablations with token vectors by category; success; turns; interaction among steps (non-additivity); composed policy vs all-tools and static restriction at a stated test; pre-registered per-step hypotheses.
- **Nearest prior art:** Executor (names first, describe on demand, suggestions on miss: P3); OpenAI tool search (name and description visible, schema deferred) and Anthropic inline discovery (via 4b); Speakeasy progressive search (vendor); r3-toolattention (savings projected, not measured, via 4b); r4-missing-memory-hierarchy stubs (one task); compgateway stubs; Skill Blocks hybrid stubs and SkillJuror layout (skills, N5); SING; BoR adaptive depth and MagicSelector (retrieval-depth policies, N1); BPS set-level selection under a token budget (skills, N10); the Stage 4 K-C record.
- **Residual gap (bounded):** component-level evidence on per-step savings and success cost, with cumulative accounting and composed-policy validation against strong baselines. Only adjacent queries exist (S4-Q003, Q004, Q008) plus the Stage 4 K-C reasoning.
- **Alternative explanations:** the mechanisms are shipped; any result may describe one harness; per-step effects may be non-additive, so "each step saves tokens" may fail on interaction; the K-C record failed the disguised-answer check as worded, so this candidate must be answerable "no step pays".
- **Falsifier:** no step pays net of overhead; the composed policy is dominated by a simple static restriction or all-tools; step effects unstable across models.
- **What would invalidate the contribution:** shipped systems or papers with component ablations on cumulative tokens; evidence that closed provider-native deferral subsumes any client-side design.
- **Identifiability:** step ablations are manipulable; arms differ in prompt content and turns; server-side steps have non-comparable accounting; interactions grow with the number of steps (cells = 2^k before fractional designs).
- **Statistical feasibility:** each ablation contrast by the paired form; multiplicity grows with steps; composed-policy dominance needs the intersection-union test; "maintained" needs a margin the benchmark can support (P2).
- **Practical feasibility (parametric):** the heaviest design and implementation burden, and depends most on D-c and D-i.
- **Can establish:** which steps pay in the tested conditions; whether a composed policy is non-dominated there. **Cannot:** that the mechanism is novel; transfer beyond the harness and models; cost without prices.
- **Challenge outcome:** not reviewed by the challenger (added after it); to be covered by any later review.
- **Epistemic status:** plausible within bounds; mechanism novelty low by construction; the contribution claim is evidence.

## 5. Search coverage statement
| Candidate | Logged queries near its gap (from `searches/stage4`, `stage4b`, `stage4c`) | Consequence |
|---|---|---|
| C1 | none aimed at an absence-by-presence factorial | "not found" rests on coverage not designed for it |
| C2 | S4-Q007 (discovery overhead of on-demand loading) is adjacent; none aimed at a fallback toggle with an equal-cumulative-token comparator | partial at best |
| C3 | S4-Q005, Q006, Q009, Q011; S4C-Q004, Q010 | targeted |
| C4 | S4B-Q25, Q30; S4C-Q005, Q007, Q015 | targeted; repeated negatives |
| C5 | S4-Q010 (evaluation variance and cost-aware reporting) is adjacent; none aimed at stability of conclusions across conventions and evaluators | partial at best |
| C6 | S4-Q003, Q004 (source paths of two frameworks), S4-Q008 (progressive disclosure of tool definitions) and the Stage 4 K-C reasoning | partial |
No new search was run in this step (not authorised), so these statements stand until a later step decides otherwise.

## 6. Why the candidates are distinct, and where they overlap
| Pair | Shared | Different estimand |
|---|---|---|
| C1 and C2 | induced-miss manipulation | C1 attributes loss; C2 measures restoration and its price including on no-miss tasks |
| C1 and C4 | distractor and overlap manipulation | C1 includes absence against a reference; C4 isolates what in a present catalogue degrades selection (C1's presence term is C4's subject measured end to end) |
| C2 and C3 | harness and multi-turn runs | C2 isolates one component; C3 compares whole classes |
| C3 and C6 | policy comparison on trajectories | C3 asks which existing classes are non-dominated; C6 asks which steps of a stepwise design pay and validates a composed policy |
| C3 and C5 | trajectory logs | C5 is a sensitivity analysis of C3-type conclusions and may ride on C3 or C2 runs |
Candidates can be combined later; none depends on another to be well defined.

## 7. Separated dimension notes (descriptive; no scores, no ordering)
| | Novelty | Thesis alignment | Identifiability | Statistical feasibility | Practical feasibility |
|---|---|---|---|---|---|
| C1 | weakened by ToolMATH and CAM-DF; gap not searched for | accuracy side and part of tokens; no discovery or horizon | linked factors, scale-dependent interaction, forced inclusion unverified | simple effects as the paired form; interaction several times larger | vehicle and pool construction open |
| C2 | mechanisms shipped; evaluation gap not searched for | covers recovery and overhead | miss mechanism, presence control, comparator class | ratio estimand (Fieller) | multi-turn; provider arm needs a convention |
| C3 | reporting-level increment possible; searched | covers objective, overhead, baselines; "maintained" needs a test | scaffolding; accounting comparability unidentified | joint dominance lower power; multiplicity | largest implementation and accounting burden |
| C4 | token-matched control not found; searched repeatedly | indirect | padded vs schema-varying; circular proxy | item-level; interactions several times larger | claims limited to models run |
| C5 | arithmetic risk; evaluator part is non-arithmetic; gap not searched for | accounting definitions and horizon | post hoc identified; cache behaviour needs logs | bootstrap flip frequency | cheapest variant is a re-analysis |
| C6 | mechanism novelty low by construction; evidence claim; partly searched | closest to the stated policy structure (flagged) | arms differ in prompt and turns; interactions | ablations, multiplicity, dominance | heaviest design |

## 8. Challenge summary
One independent challenge (Opus 5.5 High per the project rule, recorded in D5; read-only, existing evidence only) is stored verbatim in `audits/S4D-C1-…`, with my checks and dispositions in `audits/S4D-V1-…`. Its five most consequential points (the incomplete requirement list; undisclosed lineage; C1's core weakened by its own prior art; C2's misreads and design flaws; optimistic statistics and alignment statements) were all confirmed by re-reading primary text and are addressed above. No candidate was eliminated; the objection that would most justify dropping or rewriting each is recorded in its record.

## 9. Corrections made in v2
Requirement list rebuilt from the brief (R8-R10 added; R7 expanded); C6 added; lineage disclosed; C2 recovery defined as a family and its motivation corrected (PlanBench-XL discovery always on; SING success tables); C1 rewritten (simple effects, scale dependence, alternative-path success, ToolMATH presence conditions, CAM-DF contrasts); C4 restored the detail-level factor and defined realism; C5 grader framing corrected (18.5% is evaluator-human disagreement including deterministic benchmarks); statistical conventions corrected (interaction factor, ratio intervals, joint dominance, multiplicity, removal of the token-axis claim); "38.4%" restated as delivered tool-output tokens; cache drop restated as one turn; "128" restated as total schemas; "+-8" restated as per-cell. Earlier files are unchanged; errata are in `audits/S4D-V1-…` section 3.
