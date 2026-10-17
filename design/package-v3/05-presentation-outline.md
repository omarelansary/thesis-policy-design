# 05. Presentation outline for the 2026-10-21 meeting (about ten minutes plus discussion)

Status: provisional. Every statement about effectiveness is a hypothesis; nothing was implemented or run. Evidence labels: *read* = a source passage was read, and for eight pivotal passages independently checked against the original; *vendor* = a vendor's documentation claim; *derived* = arithmetic from extracts; *untested* = a hypothesis with a stated falsifier. The working objective is an instruction for this revision, **not** a quotation of the supervisor, and the noninferiority margin is **not** decided.

## Slide 1. The problem and what is being measured
Reduce tool exposure to LLM agents while preserving task success, counting the cost of deciding, discovering and using tools. Working objective: **minimise cumulative model-visible input tokens over complete trajectories subject to end-to-end success not below the reference by a margin (undecided), mean and within strata, all overhead included.** Recorded separately: tool count, token categories, billed cost, cache behaviour.

## Slide 2. What the evidence says, in four lines
- Retrieval-based narrowing scored below a curated pool in one benchmark, and below full exposure in two others; in the one benchmark that ran flat, `rag:32` matched it on one model *(read; intervals about ±8)*.
- A tool that is never shown can never be called: on tasks the retriever never surfaced, success was 0% across four models in one benchmark *(read, checked)*.
- Fewer model-visible tokens need not mean lower billed cost: in the one direct cache table, 97.5% fewer input tokens came with an inconclusive billed difference; the cache multiplier implied by that table is a **fitted, study-specific number**, not a billing rate *(read, derived)*.
- No stored source shows a second filtering stage paying or failing to pay; none supports a system-side re-adding trigger; whether models search when a needed tool is absent is unmeasured.

## Slide 3. What we corrected since the last review (say this early)
Five substantive errors in the previous version were found and corrected, not disclaimed: (1) break-even equations that added success to cost (now separate estimands, a feasibility-then-cost rule); (2) a missed-tool probability treated as a success bound (it bounds only coverage; a residual term is unbounded; the safety claim was withdrawn); (3) a greedy core rule claimed cost-minimising (it is not; a four-tool counterexample; no optimality or safety property); (4) a candidate that could not run on the large-catalogue problem it was for (its core rule needs usage statistics a large catalogue does not provide); (5) a cache multiplier treated as a price. The challenger also found an omission in our own correction (the extra model call each discovery causes) which we then fixed.

## Slide 4. The decision graph (draw the Mermaid graph from `02`)
Two layers, said plainly. **Run-time policy:** assemble a stable prefix (optional core + discovery interface + scope statement) -> optional per-request narrowing -> agent step -> if a capability is missing, the model asks -> system searches and appends -> back to the agent step; optional system trigger. **Deployment selection protocol:** does the catalogue fit; do usage statistics exist; build the arms; choose the cheapest arm that stays noninferior (three disjoint splits, mean and strata, multiplicity controlled), expose-all if that wins.

## Slide 5. How it answers your three requirements, and where it does not
- *Context:* the request enters only if per-request narrowing is selected; the trajectory enters through the model's own search and an optional trigger.
- *Staged narrowing:* core -> per-request -> in-run discovery, each **optional**; the number of stages is an output of a stated rule and may be zero.
- *Reintroduction:* the model's search re-adds a capability; it re-adds something an earlier stage *removed* only if per-request narrowing is present.
- We did not invent stages, thresholds or benefits to resemble the example. If the rule returns search-only, the realised policy is vendor-style deferral and the staged content is empty for that regime.

## Slide 6. Comparison with the rivals
Expose-all (the reference where it fits; under the token criterion it pays its whole tool block every call), vendor deferral (a hand-picked few tools plus search), our earlier candidate C-A (a computed core plus search; now a component, because its rule needs usage statistics a large catalogue lacks and its safety claim was withdrawn). The strongest rival to the graph is a **small hand-picked core plus vendor search**: fewest components, no selection procedure to pay for.

## Slide 7. Strongest remaining objections (one line each; detail in `04`)
The selection protocol is experimental arm selection, not a runtime decision, and its own error rates are unknown; models may not search; selector recall at large catalogue size has no legitimate labelled data; the tool block may be a small share of total tokens; mean success can hide the tail; the reference cannot run at large scale, so every claim there is relative to a substitute.

## Slide 8. Experiments that would resolve them (in dependency order; none authorised)
Token accounting by category at several catalogue sizes (cheap, may end the line) -> initiation of search when a needed tool is absent -> selector recall at the same search width on a disjoint labelled split -> end-to-end noninferiority sweep across arms with strata -> error rates of the selection procedure across settings -> billed-cost and cache report per provider.

## Slide 9. Questions for you (they change what the proposal should be)
1. Is the research question's unit "count of tools" or model-visible tokens and cost, and does the earlier "save tokens, never filter out tools" formulation still hold?
2. Is the staged question-per-step form binding, or would a policy whose stages appear only when a stated test justifies them be acceptable?
3. Does "each step saves tokens" mean per step or collectively over a trajectory, and does a later re-add violate it?
4. Would a well-founded conditional result ("a second stage does not pay in regime X"; "expose-all wins on provider Y") count as the findings required, and as the contribution?
5. Must the code-mediated existing project be a baseline arm? What margin counts as "maintained"?

## For the student (not for the slides)
Decide: whether to present the graph as "a policy family plus a selection protocol" (the accurate description) or only its run-time half; whether tokens is your working criterion; and whether to ask for a bounded cost-accounting experiment first (cheapest, can end the line). Do not present the policy as validated, final, novel or better than any rival.
