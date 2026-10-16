# Candidate-quality addendum (final bounded quality gate, D6)

- Date (UTC): 2026-10-14. Coordinator: Sonnet 5.5. Authority: `decisions/D6-candidate-quality-gate-authorization.md`. Critic: one Sonnet critic, read-only, existing evidence only, stored verbatim in `audits/S4D-C2-quality-gate-critic-C6-20261014.md`. The critic and I read the same corpus, so agreement is not independent confirmation.
- This addendum **amends** `S4D-CANDIDATE-DOSSIER-20261014.md` (v2) and `S4D-DEPENDENCY-MATRIX-20261014.md` (v2) without editing them; where they differ, this addendum governs. It selects and ranks nothing, chooses no architecture, keeps D-a to D-j open, ran no search or experiment, and used no 14 October or earlier-thesis material.
- Result: **no objection demonstrates that any of C1-C6 is invalid.** All six are preserved with the limitations below.

## 1. Checks I made before disposing of objections
Transcript L462-L468 (supervisor statements only): "Step one... Step two... Step three, step four, step five, something like this. So each step is there to save some token." Recovery follows as an addition ("Then again you also have to think like what if... the filteration that I'm doing is wrong. Then you should give some way for the LM to query..."), and the next lines say "it's not like you have to save token for each turn. You need to save token for a number of turns." The approved brief (section 1.2, L35) records "each step saves tokens" as Required; that wording is the Stage 1 summary of this passage, approved provisionally. Skill Blocks (s4b-wa-skillblocks): hybrid stubs cut SearchQA raw input by 27.4% but ALFWorld by only 3.18% with a paired interval of [-9.50%, +1.29%] (L387, L406); its cost model's net saving depends on load probability and reloads (L190). Executor's stored sources support the names-only description and a miss path with suggestions (`r4-executor-src-description`, `r4-executor-src-skills`); the field weights, suggestion limit and "no token counter" finding come from raw files read in probe P3 that are not stored as text (hashes in the probe results). The stub and detail-level evidence for tool catalogues is thin, but for skills it is controlled (n=1,400 and 276 cases), which my v2 text ("measured on one task or unmeasured") understated.

## 2. Amendments to C6
1. **"Each step must save tokens" is under-specified, and the per-step sign condition is withdrawn.** The transcript's own words are a purpose ("there to save some token") followed by a global lens (L468-L476) and by recovery as an addition (L466). A per-step tokens-only sign condition mis-scores two kinds of steps: **insurance steps** (recovery; it adds tokens when invoked and protects success) and **enabling steps** (a coarse listing or discovery step that saves nothing alone but permits a deeper cut elsewhere). In an ordered pipeline, position is also confounded with the step. C6 must pre-register which reading of "pays" it uses. The admissible readings are:
   - (a) stand-alone add-one token sign (drops insurance and enabling steps; result depends on the regime);
   - (b) conditional marginal contribution inside the composed policy by leave-one-out (credits enabling steps, but still drops insurance steps on tokens alone);
   - (c) per-policy expected-trajectory savings with steps as design rationale only (the literal global lens; C6 then approaches C3);
   - (d) Shapley-style average over step subsets (needs about 2^k cells; not unique under interaction);
   - (e) a step pays if removing it yields a policy dominated on (cumulative tokens, success) (scores insurance and enabling steps on both axes; the falsifier becomes "removing any step yields a non-dominated policy").
   Insurance steps are judged on success preserved per added token, not on a token-saving sign. No reading is chosen here. Which reading the supervisor intends ("each step saves tokens" per step, or the policy over turns) is a new question for him (section 5).
2. **A regime factor is required.** Whether a step pays depends on catalogue size, load probability and session length (Skill Blocks' net-saving formula; compgateway: filtering saved 392,000 and 1,220,000 tokens over two sessions but 128-256 for a 9-tool agent). C6 needs catalogue size and session length as factors, as C3 has. The token part of the per-step arm is largely arithmetic given load probabilities, which limits the contribution unless success and trajectory effects are what is measured.
3. **Composition and validation.** Composing a policy from steps that paid in the same data is selection on the outcome. The composition rule must be pre-specified or validated on held-out or fresh tasks; the composed policy and baselines must receive symmetric tuning; "dominates" is not the headline claim; "maintained" needs a stated test and a margin the benchmark can support (P2); the static-restriction baseline must be specified as a strong baseline.
4. **The family boundary is stated.** C6's three degrees of freedom (initial visibility, withheld detail, expansion trigger) define a **staged-disclosure family**. They are the supervisor's L462-L466 structure without its numbers; they are not architecture-neutral. Designs outside the family (code-mediated access, delegation, session eviction, gateway placement) are not instances of C6. This is a limitation of C6's scope, not a hidden assumption of the set.
5. **Prior-art wording corrected:** stub and detail-level evidence is controlled for skills (Skill Blocks: n=1,400 and 276; sign varies by regime), measured per lever without success for tool filtering (compgateway), and measured on one task for tool stubs (Missing-Memory; the 37.1% reduction is stubs plus compaction and trimming); transfer from skills to tool catalogues is an assumption that C6 and C3 make and neither examines. The K-C "disguised answer" failure is mostly avoided because "no step pays" and "composed policy dominated" are real negative outcomes, but the per-step token arm remains close to arithmetic.

## 3. C6 versus C3
- **Not distinguishable in measurements.** Both use the same token vector, success, turns, trajectories, a common harness and joint dominance. C6's baselines are C3's first two classes; C6's steps are the "deferred" and "hierarchical or graded" classes decomposed; its composed arm is one point in C3's "hierarchical or graded" class; its ablations are C2's toggle applied to other steps.
- **Distinguishable in attribution and falsifier.** C6 attributes effects to separately switchable steps (C3 gives mechanism-plus-scaffolding only) and can fail on "no step pays" (C3 cannot). C3 covers code-mediated and provider-native classes; C6 does not.
- **Collapse risk.** Under reading 2.1(c), C6 reduces to a C3 pairwise contrast with finer classes. The two share runs by design. Whether to keep them as two records or to combine them is for you; both are retained.

## 4. Set-level limitations
- **Architecture lean.** C1, C2, C3's class list and C6 presuppose a restricted or staged initial exposure followed by expansion; C2's two recovery families still assume an omitted catalogue. The set is broad across contribution types, not across architectures. The following admissible families are supported by stored evidence but are not carried by the candidates (they are **not formed, not eliminated**; they can be added as classes in C3, or as candidates, if you wish): session working-set addition and eviction (MemTool; Pichay session-scoped stubs; provider tool add/remove primitives; the 4b map says provider-absorbed); sub-agent delegation and routing; partitioning (4b: thin or training-heavy); gateway or proxy placement of the mechanism; schema or description compression and cache-stable placement. Code-mediated access appears only as one C3 class; Executor, cited as C6 prior art, is mainly code-mediated and falls outside C6's three factors.
- **Matrix wording corrected.** The D-j row ("all except C6 are non-policy contributions that he may or may not accept") read as if C6 were the one he would accept. The question applies to every candidate; C6 is the only policy-form candidate and nothing implies his acceptance.
- **"Maintained" and tokens.** For every candidate that uses "maintained", the margin that P2 supports is a constraint on the claim; the dossier stated it for C3 and C6 only. Token counts are treated as equal with no cross-model convention (Step 1 addendum).
- **Evidence provenance.** P3's tool-invoker details (field weights, suggestion limit, execution-only usage tracking) rest on raw files that were read but not stored; the main mechanism claims are supported by stored Executor sources. Further details are inconclusive until stored.

## 5. Strongest hidden assumption and limitation per candidate (none invalidates)
| Candidate | Strongest limitation recorded |
|---|---|
| C1 | binary success with deterministic scoring (which has documented errors); required-tool annotations and an all-tools arm; linked factors; the reference arm "curated" does not meet the all-tools baseline; "all / some / none" omits a present-at-name-level condition |
| C2 | presupposes an omitting first exposure; the equal-cumulative-token comparator is defined on an outcome and can only be approximated by calibration, with a tolerance not yet stated; needs annotations for natural miss rate |
| C3 | a common harness cannot hold for provider-native and code-mediated classes; class-level estimates confound implementation quality with class; the "head-to-head not found" statement sits beside stored near-misses (Skill Blocks for skills, DynamicMCPBench App. N, ToolMenuBench) and assumes skills-to-tools transfer is not a barrier |
| C4 | single-step deterministic scoring; circular lexical overlap proxy; padded and schema-varying counts are different constructs; conclusions limited to the models run |
| C5 | a "flip" depends on the policy set and the price grid; the non-arithmetic part needs provider logs; evaluator ground truth is itself disputed |
| C6 | per-step tokens-only "pays" (amended above); same-data composition; no regime factor in v2; staged-disclosure family boundary; mostly-arithmetic token arm |

## 6. Dispositions of the critic's points
| Critic point | Disposition |
|---|---|
| Per-step sign condition conflicts with recovery and enabling steps; transcript supports only a looser reading | **accepted** (verified at L462-L476); amendment 2.1 |
| C6 lacks a regime factor | **accepted**; 2.2 |
| Same-data composition, asymmetric tuning, "dominates" headline, weak static baseline | **accepted**; 2.3 |
| C6's factors are not architecture-neutral | **accepted** as a stated limitation; 2.4 |
| v2 understated stub evidence ("one task or unmeasured") | **accepted**; 2.5 |
| C6 collapses toward C3 under the literal global-lens reading | **accepted as a stated risk**; both records kept |
| Architecture lean and missing families; D-j row tilt | **accepted**; section 4 |
| Hidden assumptions per candidate | **accepted**; section 5 |
| "Several targeted searches found none" beside stored near-misses | **accepted** as a wording limitation; section 5 (C3) |
| P3 details unstored | **accepted**; section 4 |
| Any objection demonstrating invalidity | none was found by the critic or by my checks |

## 7. New questions this raises (for the user and the supervisor, not decisions now)
1. Does "each step is there to save some token" (L462-L464) mean each step individually, or the policy's steps collectively over turns (L468-L476)? How should a recovery step be judged under it?
2. Should the candidate set be widened to the families listed in section 4, or is a staged-disclosure bias acceptable for this thesis?
3. Should C3 and C6 be kept as two records, or considered together later?

## 8. Status
Candidate formation is ready to close on the S4D v2 record plus this addendum. No candidate is selected or ranked; D-a to D-j are open; no Stage 5.
