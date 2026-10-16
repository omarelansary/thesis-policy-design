# F. Supervisor-ready synthesis (provisional; for the 2026-10-21 meeting)

Everything below is a conceptual proposal. Nothing was implemented or run; no improvement is claimed; no component is shown to work. Evidence labels: *read* = a source passage was read by the team; *vendor* = a vendor's own documentation claim; *untested* = a hypothesis with a stated falsifier.

## F1. The policy in one paragraph
The policy decides **what the model can see and reach, and when that may grow**. Before a run, an operator configures, from facts measured on separate data, which arm applies: expose everything, a static core, or narrowing (N0). At the first turn, an always-present core and an access interface are fixed (N1); optionally the remaining catalogue is narrowed from the request text and catalogue metadata alone, at one level or two (group, then tool), with a disclosure grade per tool (N2). During the run exposure **only grows**: the model may ask for a tool to be searched, described or upgraded (N3), and optionally the system may add tools on a trigger built from runtime-observable signals (N4). Nothing at runtime uses gold tools, reference trajectories or benchmark annotations, and every decider's cost is counted. Every node can be switched off, and the result then reduces to a simpler policy: static core, deferred loading, or expose-all.

## F2. Why this decision logic
- The cost of a visible tool is paid on every turn it is re-read, but **fewer exposed tools does not by itself mean lower cumulative tokens, lower billed cost, or higher success**: caches price re-reads at a fraction of input (*vendor*), discovery adds turns and decider tokens, a tool list rewritten mid-session can invalidate a cache (*vendor*), and reduced exposure lowered success in several controlled settings (*read*). So the regime decision is made by configuration, restriction is one arm among several, and cost is reported as a vector.
- Decisions sit **where their information exists**: request text and catalogue metadata are available before the first turn; the trajectory exists only afterwards; a removed tool can never generate a call or an error, so its need can be signalled only by the model's own request or by an inference from other signals, each of which has a measurable error.
- A staged filter is **a hypothesis, not a presumption**: a stage pays only if it reads candidates more cheaply than the next stage and its recall effect is not negative; the cost/recall model gives conditions, not a sign.

## F3. What current evidence supports
- Reduced exposure by retrieval lowered success in ComplexMCP, ToolMenuBench keyword filters, LiveMCPBench depth and DynamicMCPBench retrieval conditions; flat exposure still cost 8 points in one benchmark (*read*). Strong models largely mitigated distraction up to the tested range (*read*).
- Cache pricing makes visible-token savings an unreliable proxy for billed savings (*vendor pricing; one corpus on tool-output compression*). No stored source measures billed cost of catalogue filtering together with success.
- Removal without recovery lost recall in an on-device study; re-retrieval over the evolving context raised pass rate for one benchmark and model, with confounds (*read*). In that method the model emits the request and the system executes it.
- Vendors ship deferred, cache-preserving discovery and namespace-level first disclosure (*vendor*); a two-stage router was indistinguishable in success from single-stage retrieval in one benchmark, with no token data (*read*).

## F4. What is not established
- That any second filtering stage pays, or that it does not; that models invoke a search interface when a needed tool is absent; that a system-side trigger beats model initiation; that recovery's value exceeds its unused price; that add-only exposure preserves caches in practice; that billed cost falls under any restriction.
- That the staged graph, its stage count, or any combination is novel: the novelty statements are the supervisor's assertions and no prior-art check beyond the stored corpus was made; the stored corpus contains close overlaps (vendor deferred search, namespace disclosure, FitText re-retrieval, JIT schema loading, Skill Blocks, CE-MCP).
- Any threshold, width, stage count or margin.

## F5. Experimental work that would be needed next (in dependency order)
1. Restrict-or-not across catalogue sizes with cache fields and billed cost (one scorer, all comparators).
2. Forced-absence stratum with a search interface: do models initiate?
3. Recovery value vs unused price, with an oracle-exposure bound.
4. Two-level vs single-level selection, system-run and model-driven, at large catalogues.
5. Then trigger-based recovery, working sets, learned selectors, the code-mediated baseline.
Prerequisites: the objective formulation, the "pays" reading, the decision rule and the regimes claimed must be fixed **before** any run; a smoke execution of the closest vehicle is the proposed gate and needs separate authorization.

## F6. Questions for the supervisor (they change what the proposal should be)
1. Is "count of tools" (E1) the unit of the research question, or shorthand for model-visible tokens or cost? Does it keep the earlier "never to filter out tools, save tokens" formulation?
2. Is the staged relevance-question form binding on the policy, or an illustration (REQ-O14-12)? Is a policy that reduces to "deferred loading with a model-emitted search path" acceptable as the policy?
3. What does "each step saves tokens" mean: per step, or collectively over a session? Does a later stage re-adding a tool violate it?
4. Does a well-founded **negative or conditional result** ("a second stage does not pay in regime X") count as the findings required for the thesis, and as novelty?
5. Must a code-mediated existing project (the named baseline) be a baseline arm?
6. What margin counts as "maintained", and does the deliverable include an evaluation script (written specification) beyond this policy?
