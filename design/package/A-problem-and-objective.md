# A. Problem and objective specification

Status: **provisional, unvalidated, lead-assembled** from DPR-0001 rev. 2 (design-proposer), after challenges CH-0001..0006 and CH-0017 (design-challenger). Nothing here is selected, approved, measured or claimed novel. Labels: [F] stated in a cited source, [I] interpretation, [U] unknown. Detail and ids: `design/proposals/DPR-0001.md`.

## A1. The problem, in the user's words
Working statement (AUTH-004, quoted, not narrowed): *"reducing unnecessary tool exposure to LLM agents while preserving task performance and accounting for the costs of deciding, discovering and using tools."* The thesis question's own wording is still not in `requirements/THESIS_QUESTION.md`; the supervisor's restatement is a mid-sentence fragment (E1: "most optimal way to reduce the count of tools while keeping the accuracy as high as possible ... We don't need to change it"). Whether that fragment keeps, narrows or replaces the earlier token-based formulation is open (REGISTER G.3 Q1).

A policy decides, at defined points, **what an agent's model can see and reach**. Every visible tool costs tokens on every turn it is re-read, may change how well the model chooses, and may be unneeded. Every restriction costs something too (the decider, the extra turns to discover a hidden tool, the cases where a needed tool was removed).

## A2. What is being traded (four quantities, kept distinct)
| Quantity | Meaning | Why it is not a proxy for the others |
|---|---|---|
| `c_tools` | number of tools exposed at a turn (weighted by disclosure grade) | a few heavy tools can outweigh many light ones |
| `c_vis` | model-visible tokens of tool metadata at a turn | depends on tokenizer and on how the provider renders tools |
| `c_cum` | cumulative tokens over the session, **by category**: tool metadata, selector/judge, reasoning, tool outputs, discovery calls, recovery calls; cached or not | extra turns re-read context; decider tokens count |
| `c_bill` | billed cost under stated conventions (uncached, cache read, cache write, output, per-call fees) | cache reads are billed at a fraction of input price (0.1x in the Anthropic pricing page, EXT-0021), so visible-token savings can overstate billed savings [F, vendor; EXT-0016/0018 make the same point for tool-output compression in one corpus] |

[I] Fewer exposed tools does not by itself imply lower `c_cum` or `c_bill`, nor higher success (AUTH-004). The stored corpus contains **no source that measures billed cost of catalogue filtering together with task success** (ledger C3-19, a bounded negative).

## A3. "Unnecessary exposure" has to be defined, and only in the scorer
Three non-equivalent definitions (DPR-0001 R1); none may be used by a runtime component:
- **U1**: a tool in view that no successful reference or successful run requires (needs gold or a success set: legitimate only for scoring and analysis).
- **U2**: a tool in view that was not called in the run (post-execution, and policy-dependent, because calls depend on what was visible).
- **U3**: visible tokens beyond a declared sufficient set (needs a definition of "sufficient"; unset).
Which one the thesis reports is a choice for the human; it must be fixed before any run.

## A4. Decision points and what each may use
| Point | When | May use | Note |
|---|---|---|---|
| D0 | before the first model turn | request text, catalogue metadata, model/provider facts, offline artefacts built on separate data | a staged filter that finishes before the first call changes no cached prefix |
| D1 | between turns | the above plus the transcript, the model's own calls, tool results and errors | |
| D2 | inside a turn, at the model's request | the request itself (search / describe / upgrade) | depends on the model initiating at all |
| D4 | end of session / between sessions | persistent artefacts, working set | session horizon unset; deferred |
| D5 | at termination | the model's own end-of-attempt event | re-opening a finished attempt mixes tool value with a second attempt |
| (D3) | the regime gate | *adopted as operator configuration, not a runtime node*: the quantities that would decide whether restriction pays (load probability, session length, cache share) are future or provider-internal | a runtime determinant survives only as hypothesis HYP-0001 |

## A5. Signal classes (the legitimacy rule)
**R** available at decision time by construction; **D** derived from separate offline data (leakage risk: must record training data and a train/test split); **X** exists only after execution; **P** prohibited at runtime (gold tools, reference trajectories, benchmark annotations) unless legitimate availability is demonstrated. Key entries (full register S1-S19 in DPR-0001):
- R: user request; catalogue names, descriptions, schemas and sizes; model and provider capabilities; transcript so far; the model's own calls; tool results and errors (from the first call on); the model's explicit search/describe request.
- D: usage statistics, embeddings or a trained selector built from other tasks.
- X: "this tool turned out relevant"; final success. A **removed** tool can never produce a call or an error, so for it only the model's own request, or a system-side inference from other R signals (inability text, termination, repeated failure, re-ranking with context), can signal need; each inference is a classifier whose error is a cost.
- P: gold tool lists, reference trajectories, annotated required tools, task-category labels, and tool names leaked in a benchmark's task text.
- A vehicle caveat: on the closest evaluation vehicle, stub schemas for distractors and error messages that steer toward the reference route make S2 and S7 *contaminated* signals there even though they are clean in deployment (S4G L23, L26).
- A checkable test for a claimed legitimate signal: run the component with annotation fields removed or permuted; if the output changes it uses them (necessary test only; it does not catch correlated-field leakage).

## A6. Actions available
Expose everything; change nothing; remove; add / re-add; regrade (name only, name plus description, full schema); provide a discovery interface (search/describe) instead of schemas; provide a mediated path (programmatic/gateway); ask. "Expose everything" and "change nothing" are policies in the space, and comparators.

## A7. Objective formulations (none chosen)
| | Statement | Needs | Weakness |
|---|---|---|---|
| F1 | minimise cost subject to success >= reference - `delta` | a reference `pi_ref` and a margin | `delta` is an unjustified free parameter; undefined where no reference is feasible |
| F2 | maximise success subject to cost <= `B` | a budget | `B` is arbitrary unless it comes from a deployment |
| F3 | minimise cost - `lambda` x success | an exchange rate | results flip with `lambda` |
| F4 | report the Pareto set over (success, cost vector) | nothing | yields a frontier, not "a policy" (REQ-O14-08 asks for one) |
| F5 | each step must reduce cost | separability | one reading of "each step saves tokens" |
| F6 | cost summed globally over the session | a horizon | "turns in one session" vs "many requests" is open |
| F7 | F1/F2 applied per stratum (miss / no-miss, rarely used tools) | scorer-side strata | a mean can be maintained while a stratum is sacrificed; an omitted tool is a hard failure |

**Reference `pi_ref`.** Expose-all is the intended reference, but on the closest vehicle the flat catalogue (~292k tokens by the repo's estimate) exceeds the context of 2 of 4 matrix models (S4G L28). Then `pi_ref` must be a named substitute and the claim "maintained" is only relative to it; a gold-derived pool is weaker and favours restriction.

## A8. Constraints that hold for any proposal
One scorer and one evaluation code path for all methods (REQ-O14-03); all-tools and multiple baselines (REQ-S4); selector cost counts (REQ-S1); no thresholds, stage counts or targets (AUTH-004); policy parameters, indexes and regime facts fixed on data disjoint from the evaluation tasks; no implementation (REQ-O14-18).

## A9. What remains unspecified, and who may specify it
Thesis-question wording and the Q1 reading (human, supervisor); which of U1-U3 and F1-F7, the margin `delta`, budget `B`, rate `lambda`; the "pays" reading (five admissible readings, none chosen, CAVEATS 5); disclosure grade set, widths, stage count, selector type; cost convention and tokenizer; session horizon; whether a code-mediated/gateway path counts as exposure; which models, catalogues and providers; whether a named existing project (code-mediated) must be a baseline arm (S4I section 5).
