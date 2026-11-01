# 17. Benchmark register for V5's experiments (V5, AUTH-020 seventh amendment of 2026-11-01, INT-T-020, INT-T-021)

Status: **in progress**, lead, 2026-11-01. Nothing validated, approved or final. No design rule, requirement or parameter is changed here; proposed changes to V5 are listed for the human (section 9). Choosing a benchmark for an experiment is the human's decision; this file gives ranked candidates with reasons.

## 1. Critical reassessment of the request and of the lead's own proposal (before any search)
Labels: **[keep]** a safeguard the lead holds necessary; **[drop]** a restriction the lead holds unnecessary; **[refine]** kept in another form; **[flag]** bears on V5 and goes to the human. All [I] unless a source is cited; section 2's methods check tests them against the literature.

**1.1 Where the human's request is kept as a necessary safeguard.**
- [keep] *Construct first.* A benchmark is judged against the construct of the experiment's claim, not by its reputation or leaderboard.
- [keep] *Version lock.* Paper version, repository commit, dataset revision, date read; errata and later versions recorded.
- [keep] *Exploratory versus confirmatory.* Pilots and loop items may inform choices; the confirmatory protocol and its held-out selection are frozen before the final claims are tested. Corollary the lead adds: the held-out items must be disjoint from every item looked at in pilots, and inspecting a benchmark's *properties* (catalogue size, schemas, licence) is not the same as looking at its held-out *outcomes*.
- [keep] *Provenance of criticism.* Authors, independent reviewers and interested parties (vendors, competitors, authors of a rival benchmark) are kept apart, and apart from what this workspace has confirmed itself.
- [keep] *Native versus modified.* What the benchmark provides is kept apart from what V5 would change (request layout, catalogue padding, sessions added).
- [keep] *Subsets are not representative by default.* A subset's distribution on the properties that matter is reported beside the full set's.

**1.2 Where the lead pushes back on the request.**
- [refine] *"Prefer established, independently evaluated benchmarks" for real-world claims.* In this niche (MCP servers, large catalogues, prompt-cache cost) most benchmarks are months old and few have an independent evaluation; the older, more vetted ones tend to have small catalogues and a higher risk of being in open-weight models' training data. Independent evaluation is therefore scored as one property, weighed against construct fit, not a preference that dominates it.
- [flag] *"Real-world" has no stated target.* The thesis question is not supplied (`requirements/THESIS_QUESTION.md`) and no target deployment is named; V5 uses catalogue regimes (R-small, R-mid, R-large) and session patterns as its proxy for deployments. The register can say "representative of benchmark population X under V5's regimes", not "representative of real use".
- [flag] *Statistical adequacy needs a target difference.* Whether a sample is adequate depends on the difference it must resolve, and the human decided there is no margin (REQ-U21-07), while `05` section 3 says the end-to-end sample "is chosen so that the accuracy differences the loop could not resolve can be resolved", which presupposes one. The register reports, per candidate, the pool available for a held-out set and the difference resolvable at that size; adequacy then depends on the human choosing either an estimation-only reading (report the difference and its interval, no pass or fail) or a margin.
- [refine] *The four categories (synthetic tasks, synthetic tools, subsets, extensions) are not one axis.* A benchmark supplies up to four separable components: **tasks** (prompts with gold), **tool definitions** (the catalogue), **environment** (execution and state), **scorer**. An option can take some components from a benchmark and build others (for example real MCP definitions from a public catalogue with constructed tasks). Every candidate is therefore described by where each of the four components comes from.

**1.3 Where the lead withdraws or changes its own proposal.**
- [drop] "Never aggregate across benchmarks" and "prefer two benchmarks for the headline claim" as rules. [refine] Effects measured in a common unit (for example the paired bill ratio between arms, or a paired accuracy difference) may be synthesised across benchmarks with their heterogeneity shown; raw scores from different scorers are not pooled; the number of benchmarks follows the claim.
- [refine] "Choose before seeing results" was too blunt; it applies to the confirmatory choice and its held-out set, not to exploration.
- [drop] "Up to 7 scouts, about 150 pages" as the measure of the study; replaced by completion criteria (section 2.3).
- [drop] The claim that P5 "needs no MCP-Atlas, made-up tools are enough". P5 measures billing, which depends on how many tokens real definitions take; definitions can come from public catalogues without running their tasks. P5's options are compared like every other item's.

**1.4 What both of us had overlooked.**
- *The outcome is the bill, but benchmarks are built for accuracy.* The properties that drive V5's bill (tokens per definition, tool-result sizes, turns per task, sessions, volatile content in tool results such as timestamps) are rarely reported and must be read from data or code.
- *Harness control.* Many benchmarks ship their own agent loop and prompt; V5 needs its own request layout (a fixed tools array, discoveries appended, `04`). Replacing a benchmark's loop is a modification; it makes published leaderboard numbers incomparable (V5 compares none) and may break assumptions the scorer makes.
- *Scorer reliability.* LLM-judge scoring, possibly with a judge served by the same university API, against deterministic state or unit-test checks; for confirmatory claims a judge's agreement must be known.
- *Floor and ceiling.* If tasks are too hard or too easy for the open-weight models on the route, accuracy differences become invisible and bias the reading toward "nearly the same".
- *Contamination* of public benchmarks in open-weight training data (matters for accuracy, little for billing mechanics).
- *Our own selection bias.* V5 is this workspace's design; choosing where it looks good is the fault the human described in papers. Safeguards: rankings use properties only, are written before any V5 run on the benchmark, and an independent agent ranks the same cards without seeing the lead's ranking (section 2.2).
- *Choices already written into `05` before any register.* P3 names BFCL's withheld-function design, P1 names ATRBench as the closest stored design and P4 names MCPMark. [flag] These become candidates assessed here, not choices.
- *Licence, terms and live services.* Gated data, servers that need keys, and live web services (not reproducible, and a source of uncached variance) are properties to record.

## 2. Study design and completion criteria
### 2.1 Waves
1. **Discovery (6 scouts, parallel):** M methods literature; A MCP and large-catalogue benchmarks; B function-calling, multi-turn and stateful tool benchmarks; C multi-session, memory and personalised tool use; D catalogue sources, tool retrieval, long-horizon and large-output agent benchmarks; E criticism (audits, errata, issues, forums) of a seed list drawn from the workspace. Prompts: `inputs/scout-prompts-benchmarks-20261101.md`. Every page cited is stored by the lead (`v5-bm-*`).
2. **Property inspection (up to 2 inspectors):** read-only reading of dataset viewers, repository files and licence files for the shortlist, to confirm native properties (counts, schemas, sizes, harness structure).
3. **Verification (stewards):** claims checked against stored pages; material criticisms checked against their primary source.
4. **Register and rankings (lead), independent ranking (one design-proposer, blind to the lead's ranking).**
5. **Review (design-challengers):** one methods critic, one adversarial reviewer.

### 2.2 Ranking rules (stated before any discovery)
Per experiment: the construct (section 4); hard requirements (a candidate that fails one is rejected with the reason); scored properties; ranked candidates with their four components' sources, the modifications V5 needs, the trade-offs and the uncertainty. Independent evaluation, recency, contamination risk, scorer reliability, reproducibility, licence and cost to run are scored, none decisive alone.

### 2.3 Completion criteria (checked in section 10)
- CC1 Every selection rule cites a stored methods source or is marked as the lead's reasoning.
- CC2 Every benchmark named in the workspace for tool use, MCP or multi-session work, and every one the scouts find, is triaged in or out of scope with a reason.
- CC3 Each in-scope benchmark has a property card with every field filled or marked "not found in the places read"; versions locked.
- CC4 For each shortlisted candidate, a search for independent criticism, errata and issues was made; material criticisms are checked against their source and labelled by provenance.
- CC5 Per experiment: construct, hard requirements, ranked candidates (including constructed options), rejected options with reasons, modifications needed, uncertainty.
- CC6 The independent ranking and the challengers' reviews are recorded with every disagreement, resolved against evidence or left open for the human.
- CC7 Proposed V5 changes are listed with evidence; nothing in V5 changed.
- CC8 Unresolved limitations are listed.

## 3. Methods basis
(to be filled after wave 1)

## 4. Constructs per experiment (written before the stewards' results; the lead's reading [I] of `05`)
**Common to every option (not a discriminator).** No candidate reports the bill V5 needs (fresh, cached and cache-write tokens per request; scouts A, B, D: none found, only ATRBench and Claw-SWE-Bench state cache accounting), and every candidate ships its own agent loop. So every option needs **M0: V5's own harness** (fixed tools array, appended discoveries, usage logged per request, V5-R12), and a published accuracy number of any benchmark is not comparable with V5's runs. What distinguishes options is what remains *native* after M0: tasks, gold, tool definitions, environment and scorer.

| Item | Construct (what a result must mean) | Hard requirements (a candidate failing one is rejected for that item) | Scored properties |
|---|---|---|---|
| P5 | Billed input per request as a function of the number of definitions offered, their token sizes and the offering mode (all in the prefix, or a core plus search with the rest deferred), on this route; and whether deferred, unloaded definitions are billed. Accuracy is not measured. | H1 tool definitions real, or size-matched to a documented distribution of real ones; H2 catalogue sizes can span D-01's predicted n* for each tokenizer; H3 tool results controllable (a stub returning fixed text), so prefix identity is the experimenter's; H4 licence allows use | definition size distribution; MCP format; count available; provenance of the corpus |
| P3 | Probability that a model searches, unprompted, when the needed tool is deferred, and what follows (correct call, wrong tool, answer without a tool), per cell (deferred but present, absent, wrong tool visible, oracle), with and without a one-line index | H1 a gold set of needed tools per task, allowing equivalent alternatives (Tool-DE: one gold per query under-credits, scout D D12); H2 a catalogue in or above R-mid; H3 a chosen tool can be deferred or withheld without editing the tools array; H4 tool calls answered reproducibly (sandbox or stub); H5 no live drift between paired cells | scorer of the call (deterministic tool-call match vs judge); task count; difficulty for the route's models; contamination |
| P1 | For returning users, the effect of seeding tools needed before on the bill and on accuracy, with the seed hit rate h | H1 several sessions per user in which later sessions need tools used earlier (recurrence measured, not assumed); H2 a catalogue above n*, native or added with a reason; H3 the harness decides where memory goes (not the benchmark's system prompt); H4 no simulator or judge that the route cannot serve, or one replaceable with re-validation; H5 a check that later tasks need the history (DolphinBench's with-and-without test, scout C C37) | history provenance (human, role-played, generated); gap model; sessions per user; scorer determinism |
| P2 | Accuracy when only a subset is offered while all definitions stay in the cached prefix, against all offered, with no prefix break | H1 a gold set per task (for subsets and the oracle-registry ablation); H2 a catalogue in R-mid with all definitions declarable; H3 reproducible environment; H4 multi-step tasks | scorer reliability; repeats feasible; difficulty |
| P4 | Effect of masking old tool output on the bill and accuracy of long runs | H1 native large tool results (measured, not padded); H2 long runs; H3 deterministic final-state scorer; H4 reproducible environment | tool-result size distribution; turns per task; floor for the route's models |
| E2E | Bill per turn (A, B beside it) and accuracy of V5-R against simpler policies across catalogue regimes and session patterns, on at least two models | H1 realistic tasks with gold and a scorer whose reliability is known or measurable; H2 coverage of R-small to R-large, natively or by a declared extension; H3 a session axis (returning users with gaps) by a declared extension; H4 repeats feasible on the route | independent evaluation; known error rate; contamination; licence; cost to run; live-service dependence |

**Synthetic and constructed options are candidates under the same rules.** For P5 and P3 a constructed catalogue or constructed task cells may isolate the variable better than any benchmark (INT-T-021 section 2); for P1 and E2E a returning-user axis exists in no benchmark found (scout C section 4), so some construction is unavoidable and must carry a construction method, validated ground truth and bias controls; a synthetic-only result is not reported as real-world evidence.

## 5. Property cards
(to be filled)

## 6. Criticism and provenance
(to be filled)

## 7. Candidates per experiment
(to be filled)

## 8. Independent ranking and reviews
(to be filled)

## 9. Proposals for the human (V5 changes reported, not made)
(to be filled)

## 10. Completion check and limitations
(to be filled)
