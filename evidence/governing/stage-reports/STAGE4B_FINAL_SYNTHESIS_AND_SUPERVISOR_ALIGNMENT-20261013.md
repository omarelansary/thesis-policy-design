# Stage 4b final synthesis and supervisor-alignment addendum

- Date (UTC): 2026-10-13. Authority: `decisions/D4C-supervisor-alignment-integration.md` (extends D4B; no new searches, reviews or experiments). Starting HEAD 8432cad.
- Inputs: opportunity map with its section 11 corrections (`STAGE4B_OPPORTUNITY_MAP-20261013.md`), C1/C2/C3 (`audits/S4B-C1…C3`), coordinator checks (`S4B-V3…V7`), Stage 4 records, the admitted S1 transcript, the approved brief, and the external GPT-6 Luna High audit (`audits/S4B-L1-gpt6-luna-scope-alignment-audit-20261013.md`, preserved verbatim and kept separate from C3).
- This document selects no research question, fixes no architecture, claims no novelty and starts no Stage 5. Decisions D-a, D-b and D-c remain with you.
- Labels: F fact in a source, O observation, I interpretation, U uncertainty, S speculation. Transcript citations are line numbers in `inputs/stage1/supervisor-transcript-2026-10-02.md`; the transcript is automatic speech recognition.
- Clean-room note: the transcript contains student-reported results about earlier work. They are unverified under the brief and were not read for content or used here. No previous-thesis repository, note or conclusion was accessed. While locating the git state, a listing of global git `safe.directory` entries revealed the paths (not contents) of unrelated repositories; none was opened.

## 1. What Joaa required, and what he offered as examples
Details with line references: `audits/S4B-V7-coordinator-check-of-L1-20261013.md` section 1-2.

**Requirements (instructions in his own words):**
1. An all-tools baseline, then matching its accuracy while giving "lesser and lesser" tools (L132-136).
2. Filter and discovery overhead must not cancel the savings: "if you use many many more token to filter out the tools then there is no value" (L154-156).
3. A policy, not only retrieval: "I always said it's a policy ... retrieval is only one policy" (L281-285).
4. A stepwise structure "each step is there to save some token" (L462-464).
5. A way for the model to query the omitted tools when the filtering is wrong (L466).
6. Global, multi-turn accounting: save "for a number of turns", not per turn (L468-476). The horizon (one session or aggregate across requests) is not stated.
7. Multiple baselines, including open-source projects (he names Executor) and published methods, for tokens and accuracy (L344-370); use and improve existing work (L349-357).
8. Contribution: "findings" on what works in which cases, plus a filtration algorithm (L142-152); and "it's not about the solution, it's more about the problem ... analyze ... why" (L189-194).

**Examples and lenses (not mandates):** partial information as "one of the policy" (L328); the 100/60/20/40 tool numbers ("not rigid", L332-336); names-only for the lowest tier ("I'm not saying this is the best way", L336); steps three to five "something like this" (L464); the hedged "50% reduction is low-hanging fruit" (L449).

**Not settled:** the numeric cost constraint (L416-420), whether the unit is tokens or money (brief U2; his motive is cost, L320, L443, while his stated problem is tokens, L322), the accounting horizon, and what counts as novelty beyond the two cues in item 8.

I: Joaa's two novelty cues pull in different directions. "Algorithm/policy" supports a design contribution. "Analyze the problem ... why ... not about the solution" and "findings" support a diagnostic or evaluation contribution. Neither the transcript nor the brief chooses between them. Luna's reading that the novelty type is unsettled is right; she did not cite L189-194.

## 2. Evaluation of Luna's audit (not treated as authoritative)
**Accepted:**
- The Stage 4b ranking is a defensibility ranking, not a thesis-fit ranking (map section 8 and C1/C2/C3 each rank on defensibility). This is now explicit below.
- Stage 4b's widening of the search space was authorized and is not drift; making a different objective primary (security, general reliability, capacity) would be a scope change needing agreement.
- The "directness test": a candidate should say whether it measures (a) model-visible input tokens including follow-up, (b) end-to-end performance, and (c) discovery, selection, recovery and execution overhead over a stated horizon; otherwise it is a supporting experiment.
- "Maintained accuracy" needs a non-inferiority criterion with margin and power, not a non-significant difference (Luna item 6, agreeing with C3).
- Tier sizes and thresholds are experimental factors, not answers; the policy should specify what is visible first, when detail is revealed and what happens after a miss.

**Corrected or qualified:**
- Three of five time citations in her requirements matrix do not match the stored transcript headings (the "more work to save token" remark is at 12:09-13:11 and the global lens at 52:58-54:03, not 43:50-47:57; the policy remark is at 32:41-34:35, not 26:53-29:59; the stepwise/fallback passage is at 52:01-54:03, not 32:08-33:53 and 46:02-47:57). The substance was confirmed by line check; the timestamps should not be reused.
- She says D-COST "substitutes billed cost for the approved token target". The brief itself leaves open whether the unit is tokens or money (U2), and Joaa motivates the work by cost as well as tokens. The accurate statement is that D-COST needs an explicit decision on D-a, and Joaa's agreement if cost becomes the primary measure.
- She lists graded exposure as required; the brief's wording is "required as a lens", with tier sizes as examples.
- She characterises D-REL as "mechanistic or supporting". That is a fair alignment label but she did not take up C3's more basic objection that D-REL as worded cannot be run as a factorial; this synthesis does.
- She does not discuss that Joaa's own "analyze why" cue and the brief's "which approaches work in which cases and why" make a diagnostic contribution a legitimate reading of the thesis, nor that the existing-project baselines he asked for are themselves a required evaluation component (item 7 above).

**Disagreements between the assessments (kept separate):**
| Topic | C3 | Luna | Coordinator |
|---|---|---|---|
| D-REL | Most defensible if cut to targeted contrasts; the factorial is not executable; frontier-saturation null is a risk | Strong supporting study, but linkage to token accounting, end-to-end success and policy is missing | Both hold: defensible as diagnostic; as the thesis contribution it needs the linkage Luna names |
| D-COST | Not defensible as worded (estimand and falsifier defects); arithmetic, power and obsolescence risks | Closest evaluation of an exposure policy; alignment depends on D-a and D-b | Both hold: aligned in what it measures, weak as worded; repairable as an estimation study |
| Ranking | Defensibility ranking by critics | Defensibility is not thesis fit | Agree with Luna; no single ordering is given below |
| Merging D-REL and D-COST | Offers a two-phase merged design but notes Phase 2 cannot be powered for 5 pp | Join only if the design can sustain both | You asked not to merge artificially; both designs are kept separate here and the merged option is reported with its costs |
| Security (D-SEC) | Narrowed by RACG; triviality risk; scope question | Genuine change of objective if central | Agree; remains an alternative needing your and Joaa's agreement |

## 3. The four dimensions, kept apart
Ratings are coordinator judgments with their basis; they are ordinal and are not summed. "Alignment" is judged against Joaa's requirements in section 1 and the approved brief.

| Candidate (after C3 corrections) | Scientific defensibility | Thesis alignment | Novelty uncertainty | Feasibility (assumption-dependent) |
|---|---|---|---|---|
| **A. D-REL, cut down**: targeted contrasts (count at fixed tokens with a pre-registered padding construct; overlap at fixed count and tokens; residue tier at fixed count) | Moderate-high for the single-step core: clean manipulation, deterministic grading. Risks: frontier saturation null, padding defines the construct, overlap measured by embeddings is circular, general length effect (Du et al.) | Partial and indirect: speaks to the accuracy constraint and to which content can be hidden; no cumulative token accounting, no end-to-end success, no policy or recovery as specified | Medium: ToolMenuBench, LongFuncEval, SLCA-GRPO (hard vs random distractors) overlap; token-matched count control not found in the stored corpus (bounded) | High with open-weight local models; moderate with API budget; multi-turn cost arm is underpowered |
| **B. D-COST (RQ-A) repaired as an estimation study**: success-adjusted cost of 2-3 exposure policies with a pre-specified decomposition | Low-moderate as worded (falsifier has no interval method; estimand excludes large catalogues); moderate if repaired | Direct for the measurement part of the objective (usage by category, success, trajectory overhead); weak for policy design; depends on D-a for the headline unit | Medium: many near-misses (Skill Blocks, CAPC, compression-gateway, TokenNotCost, scaffolding study); bounded negative survived; vendor-internal tests unknown | Moderate-low: provider access, budget, harness dominance, power (critic estimates about 600 paired tasks for 5 points, about 155 for 10 points; assumptions), rapid obsolescence |
| **C. Policy designed and evaluated** (the literal reading of items 3-6: a stepwise policy with deferral/partial exposure and recovery, tested against baselines with global accounting; tier sizes and thresholds as factors) | Moderate if components are factors with pre-specified comparisons; weak if reported as one policy vs one baseline | Highest literal alignment with Joaa's items 3-7 | Low-moderate: shipped graded/deferred mechanisms (OpenAI visible name+description; Anthropic inline discovery; OpenDev detail levels; Spring/bigtool); novelty would have to come from evidence about when components help | Moderate-low: implementation, many factors, scope creep, same power problem; baselines (Executor, provider search) need an authorised execution step |
| **D. Recovery study** (omitted required tools, fallback on/off; was RQ-B) | Moderate as a component; weak standalone (PlanBench-XL and CAM-DF show monotone decline) | Direct for item 5 (what happens when filtering is wrong) | Medium-high risk of already being answered; residual gap is fallback on/off and recall calibration | Moderate; needs annotated oracle tools |
| **E. Non-inferiority design (D-NI)** | High (standard statistics) | Required component: gives "maintaining accuracy" a testable meaning | Not a contribution; informal NI checks exist in the corpus | High |
| **F. Eager vs deferred crossover (N2)** | Moderate; model saturation (SKILL-USE analogy) and provider co-training threaten durability | Direct for partial-information/on-demand exposure if tokens and success are measured over turns | Low-medium (Skill Blocks for skills; vendor claims untested independently) | Moderate |
| **G. D-SEC** (exposure mechanism and description-borne attack success) | Moderate: binary outcome, but RACG already shows ISR tracks exposure; residual gap is model-initiated search and stubs | Low as a primary objective: needs a scope change; relevant as a constraint on a policy | Medium | High client-side |
| **H. Objective-validation studies** (real-use magnitude of definition overhead; capacity boundary) | Moderate; magnitude data are anecdotal or single-user | Indirect: tests whether the target is worth optimising | Medium (no independent multi-user breakdown found) | Low-uncertain: needs traces not known to be public |

Not carried forward as thesis candidates (reasons in map section 5 and C3): another retriever, tool tokens/fine-tuned selection, "does code mode save tokens", cache-break accounting, permission-versus-fallback, a deferral-threshold constant, a new benchmark, catalogue drift, partitioning/memory, energy, compact formats, description rewriting.

## 4. What each candidate could contribute to Joaa's objective
Objective as approved: reduce cumulative model-visible input tokens while maintaining end-to-end performance, counting discovery, selection, recovery and execution overhead. The columns below are assessed separately. "Direct" means the candidate's own primary measurements address it; "indirect" means it informs it; "no" means it does not.

| | Cumulative input tokens incl. overhead | Accuracy / end-to-end success maintained | Reliability (variance, consistency) | Context capacity | Billed cost | Discovery / recovery overhead |
|---|---|---|---|---|---|---|
| A. D-REL cut down | indirect (token content varied in single-step prompts) | direct for selection accuracy; indirect for end-to-end | direct (repeated-run selection correctness) | indirect (where count or tokens start to bind) | no | no |
| B. D-COST repaired | direct | direct | indirect (repeats needed for power) | no (restricted to sizes where every arm fits) | direct | direct (turns, discovery calls) |
| C. Policy designed and evaluated | direct if accounting is built in | direct | indirect | direct if the policy is also run where the all-tools baseline cannot fit (then the baseline comparison is lost) | secondary | direct (recovery is part of the policy) |
| D. Recovery study | indirect | direct | indirect | no | indirect | direct (recovery cost and success) |
| E. D-NI | no | direct (defines "maintained") | no | no | no | no |
| F. Eager vs deferred crossover | direct if measured over turns | direct | indirect | indirect | direct if tier-priced | direct (search turns) |
| G. D-SEC | no | no (attack success) | no | no | no | no |
| H. Objective validation | direct for magnitude (if data exist) | no | no | direct (capacity boundary) | indirect | no |

I: Only B, C and F measure the tokens-plus-overhead side of the objective themselves; only A and D isolate mechanisms for it. No single candidate covers all columns without becoming larger than a master's thesis; combining them is a scoping decision for you, not something this synthesis does.

## 5. Is the objective itself valid? Evidence, and alternatives needing agreement
**What the evidence supports (and does not):**
- F: for stable catalogue prefixes, cached reads are priced at about a tenth of fresh input, so saving cached definition tokens saves much less money than the token count suggests; a preprint reports that a large `tools=` array was implicitly cached and that explicit caching then saved only 18.3% (n=15 queries); production traces report a 98% median KV hit rate; token reduction in tool outputs raised billed cost by 6.8% in one paired study (outputs, not definitions). Provider-documented append mechanisms preserve the cache. I: as a cost objective, "fewer model-visible tokens" is weak when caches are warm and prefixes stable.
- F: capacity and accuracy are separate motivations that caching does not address (140.2k of a window in one deployment; provider limits). I: as a capacity or accuracy objective, token reduction remains meaningful.
- F/U: the effect of catalogue size on accuracy is contested and confounded (count tied to length; MCPVerse mostly degrades with larger toolsets but a few agentic models improve; ToolMenuBench is synthetic; a hard-distractor effect appears in RL-trained 3B-8B models). Joaa's hedged claim that 50% reduction costs no accuracy is untested in the corpus.
- U: magnitude of definition overhead in real use is anecdotal. Joaa's motive (L320, L443) is cost, so a cost-based objective is not foreign to him, but it is the part the evidence weakens most.

**Alternatives that would need Joaa's agreement (they are not assumptions of this document):**
- Cost per successful task as the primary measure (brief U2 leaves the unit open; he has not agreed).
- Selection reliability at scale as the primary objective, with token reduction a means (supported by the "analyze the problem" cue but a change of emphasis).
- Context capacity as the principal rationale.
- Security of discovery as the primary objective (a scope change).
- A multi-criteria objective: tokens, success (non-inferior), cost and reliability reported as separate outcomes with a pre-stated decision rule, instead of one scalar.

## 6. C3's objections incorporated and what remains unresolved
**Incorporated:** D-REL as originally worded is not experimentally viable (count, total tokens and residue tier are linked), so it appears only as targeted contrasts; overlaps with ToolMenuBench, RACG, PlanBench-XL, CAM-DF, SLCA-GRPO and Skill Blocks are listed under novelty uncertainty; the confirmatory phase is underpowered for a tight non-inferiority margin, so no design here assumes it; D-COST's falsifier and estimand defects are stated; TSCG, MCPVerse, ToolHijacker and equivalence-testing corrections are in map section 11; critic agreement is not treated as independent confirmation.

**Unresolved scientific objections:**
1. Frontier models may show little or no tool-count effect within their windows, leaving a null or a model-version-specific result (A; also F).
2. The general length effect may explain much of any count effect (Du et al., general domain).
3. Billed cost given a trajectory is largely arithmetic and provider-specific; shipped features are making the cache-break angle obsolete (B, F).
4. Statistical power: critic estimates (about 600 paired tasks for a 5-point margin under an assumed 20% discordance) are unverified assumptions; a tight "maintained accuracy" margin may be unattainable at thesis budgets.
5. Provider search interfaces are co-trained with their models; client-side or open-weight results may not transfer.
6. Several prior-art sources (CIPO, HyperTool, ReCache, ToolSearcher, SING, ToolMATH) were read at abstract level; vendor and blog items (Cursor, Vanta, issue 83756, Arcade) are unstored triage.
7. Baseline execution: Joaa told the student to run Executor and benchmark it (L367); the brief's no-execution rule (G-f) and the clean-room stage rules mean running any baseline needs a later explicit authorisation.
8. Coverage: OpenAlex, GitHub and harness web search only; no vendor-internal evaluations; no independent evaluation of provider tool search found (not proof of absence).

## 7. Decisions remaining before research-question selection
**D-a (primary objective).** Consequences of each choice:
| Choice | What follows | Risks |
|---|---|---|
| Model-visible input tokens, cumulative with overhead (Joaa's wording) | Candidates B, C, F become the natural measurement carriers; A and D support them; token accounting by category (fresh, cached, output, search/recovery) must be fixed; cost is reported but not primary | Under warm caches, token savings may not translate into cost or even matter beyond capacity; you must state why tokens matter (capacity, latency, accuracy) or accept that the result may be "tokens mislead" |
| Billed cost per successful task | B becomes central; needs provider access, budget and tier-priced reconciliation; the supervisor's agreement on unit is needed | Obsolescence; arithmetic; power; departs from his token wording |
| Selection reliability / context capacity | A becomes central (cheapest to run); token reduction is a means; an applied arm (F) connects back to tokens | Needs Joaa's agreement that the thesis is primarily diagnostic; null-result risk; weaker link to savings |
| Multi-criteria set reported separately | Honest about the evidence; allows A and B-type measurements side by side | Needs a pre-stated decision rule and may be larger than one thesis can power |

**D-b (contribution type).**
| Choice | What follows | Risks |
|---|---|---|
| Evaluation/diagnostic thesis (A and/or B, with D-NI and baselines) | Supported by his "findings" and "analyze the problem, why" cues; smaller design space; policy appears only as the arms tested | Does not by itself deliver "find the policy"; he must agree it satisfies the requirement |
| Policy designed and evaluated (C) | Matches his items 3-6 literally; components become factors; baselines must include existing projects | Low method novelty (shipped mechanisms); larger scope; the policy's novelty must come from evidence on when and why |
| Ask Joaa to choose between the two readings | Resolves ambiguity cheaply; he asked for a draft policy before experiments (L480-482) | Delay; he may require a policy |
| A and B combined | Covers more columns of section 4 | You asked not to merge artificially; C3 reports the confirmatory part cannot be powered for a tight margin; high scope risk |

**D-c (constraints).**
| Constraint | Consequence |
|---|---|
| Local GPU, open-weight models only | A feasible and cheap; provider-native deferral, caching and billed cost are not testable; B largely unavailable; C possible only with client-side policies |
| Modest API budget | A with a frontier model; small B or F pilots with wide intervals; claims limited to estimation |
| Larger API budget and provider access | B and F become feasible; power still limits tight non-inferiority; results are provider- and date-specific |
| Duration | Longer allows a diagnostic phase then a small confirmatory phase; short duration forces a single design |

**Further decisions this synthesis exposes (not yet asked of you):**
- D-d: is security of discovery in scope (G), or a constraint only?
- D-e: accounting horizon for "global" savings (one session, a number of turns, or aggregate across requests; brief U4).
- D-f: performance endpoint (selection accuracy vs end-to-end success) and the non-inferiority margin.
- D-g: what "novelty" must mean for the thesis (algorithm, findings, evaluation).
- D-h: the numeric cost constraint on filter and discovery steps (unspecified).
- D-i: which baselines must be run (Executor, provider tool search, published methods) and when their execution is authorised.
- D-j: whether and how to put the objective reformulations (cost, reliability, capacity, multi-criteria) to Joaa before selecting a question.

No candidate is recommended here. Selection requires D-a, D-b and D-c at minimum.

## 8. Status
Stage 4b synthesis complete; stopped before research-question selection. No Stage 5, no experiments, no previous-thesis comparison, no architecture design.
