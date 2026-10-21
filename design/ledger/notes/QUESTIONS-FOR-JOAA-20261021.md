# Questions for the supervisor (draft for the human to send or bring; generated from the ledger's Questions sheet on 2026-10-21, after the intake of the meetings of 2, 14 and 21 October)

Neutral wording, one issue per question, taken from the ledger (sheet Questions). Each question says what it decides and which open ledger items wait on it. 'Before implementation' marks questions linked to items whose gate is G1 (nothing can start until they are answered or the item is explicitly deferred). The ledger is the canonical record; answers go into its YOUR ANSWER column in the supervisor's own words.

**Order of use.** The first measurement of billing and cache behaviour on a named provider does not, in my reading, depend on the policy form or the arm table (it observes the provider, not a policy); the ledger currently lists the arm decision (C-D08) as a hard prerequisite for it, and that listing is an inherited assumption that the human may confirm or drop. If dropped, the first measurement needs only B (Q-J03, Q-J04, Q-J24) plus the human's authorization (Q-U14). Everything in D to G is needed before any arm experiment.


## A. What governs Project A, and what is due

**Q-J30** [before implementation (G1: N-28, C-D08)] On 14 October you asked for a staged graph that filters tools (one question per stage, tools can be added back); on 21 October you narrowed the practical scope to memory and tool calls. How do the two fit: is tool filtering one part of a memory-and-tools policy (memory deciding which tools are offered), does the staged graph remain the form of the policy, and which comparison should be the thesis's main one?

- Answer format: Graph stays, memory is one stage | Memory-and-tools replaces the graph | Both, with this main comparison: ... | Other
- Why it matters: Every pilot and the evaluation contract depend on it (N-28, C-D03, C-D08).
- Waiting on it: N-28, C-D03, C-D08

**Q-J01** [before implementation (G1: C-D01, C-D07)] Does the June 2026 expose still govern the thesis scope? If anything changed, which exact clauses are amended (compact interfaces L0-L3, execute/expand/abstain, lifecycle/removal, staged policy, evaluation)?

- Answer format: Governs unchanged | Amended in these clauses: ... | Replaced by the October staged-policy framing | Other
- Why it matters: Decides which parts of Project A every test and design choice must cover; the repo cannot see the June text.
- Waiting on it: C-D01, C-D07

**Q-J18** [before implementation (G1: C-D05)] [partly answered] Does the 21 Oct deliverable replace the 2 Oct one? Was the 2 Oct deliverable (document plus draft step-by-step policy) delivered?

- What the meetings already say: [Partly] 2 Oct: 'write the draft version of uh your policy' (INT-T-004 E804); 14 Oct: 'You need to give me this policy' (INT-T-003 L429-L447). Delivery of the 2 Oct draft not stated.
- Still to ask: the part not covered above.

- Answer format: Replaces | Adds to | Other; Delivered: yes/no
- Why it matters: Not known to the repo.
- Waiting on it: C-D05


## B. What to minimise and report (objective, accounting, horizon)

**Q-J03** [before implementation (G1: C-D08/EC5)] [partly answered] What should be primarily minimised or reported: model-visible input tokens, the billed cost (input, cache write, cache read and output tokens under a named price table), or a stated combination? Should output tokens count?

- What the meetings already say: [Partly] Money cost per turn, tokens and response time averaged over turns (INT-T-002 L275, L302, L354); 'we will not drop the cost' (INT-T-004 E697). No single primary estimand or price table named.
- Still to ask: the part not covered above.

- Answer format: Tokens | Bill | Both with priority ... | Other; Output tokens: count / report only / ignore
- Why it matters: Replaces the AUTH-006 working objective if it changes; fixes what pilots report as primary (they can record everything either way).
- Waiting on it: C-D02, N-1, N-4, C-D08/EC5

**Q-J24** [before implementation (G1: C-D08/EC1)] Which providers and models should the bill/cache analysis cover (to choose the price tables)?

- Answer format: Provider/model list
- Why it matters: Prices and cache rules are provider-specific.
- Waiting on it: C-D08/EC1

**Q-J19** [later gate] [partly answered] Should the offline cost of choosing the configuration (development runs, amortised over a deployment horizon N_dep) be charged to the policy, and over what horizon?

- What the meetings already say: [Partly] 'if you use many many more token to filter out the tools then there is no value' (INT-T-004 E230-E232); amortisation not discussed.
- Still to ask: the part not covered above.

- Answer format: Charged over N = ... | Reported only | Not counted
- Why it matters: Part of the accounting contract.
- Waiting on it: C-S17, C-S20


## C. Memory, caching and deployment (your 19 October points)

**Q-J06** [before implementation (G1: C-D07, C-D08/ARMS-CACHE)] [partly answered] Joaa wrote: 'So you have to combine all three to find the best policy: MCP server context, memory, explicit caching.' How should the combination be treated in this thesis: all three as the design space, a subset, or later work?

- What the meetings already say: [Partly] Explicit cache 'applicable for memory ... knowledge' (INT-T-002 L197) in the 'all in theory' part (L221); practical scope tools and memory only (L223-L225).
- Still to ask: the part not covered above.

- Answer format: All three | A subset: ... | Later work | Other
- Why it matters: The combination has not been evaluated in the repo's sources yet; whether it is the design space is a scope choice, and the proposal can be adopted, refined or narrowed.
- Waiting on it: N-22, C-D07, C-D08/ARMS-CACHE

**Q-J26** [before implementation (G1: C-D08/ARMS-CACHE)] [partly answered] Should explicit caching choices (where cache breakpoints sit, how long to retain) be variables of the policy, or recorded provider behaviour while the policy concerns what is exposed? You also mentioned implicit caching.

- What the meetings already say: [Partly] 'keep them in the explicit cache and that's negligible cost' (INT-T-002 L207-L209), in the 'all in theory' part (L221).
- Still to ask: the part not covered above.

- Answer format: Policy variables: ... | Recorded only | Both
- Why it matters: Decides whether cache layout and retention are arms or covariates.
- Waiting on it: N-26, C-D08/ARMS-CACHE

**Q-J27** [before implementation (G1: C-D08/ARMS-CACHE)] [partly answered] Should the policy include anticipating likely needs before the first request (from role or deployment for a new user, from memory for a returning user), as in your stranger/colleague analogy, or is the first-request context left to the discovery stages?

- What the meetings already say: [Partly] Relevant part of memory first, more when asked (INT-T-002 L384); not all context 'just by saying hello' (L211-L216, theory part).
- Still to ask: the part not covered above.

- Answer format: Include: ... | Out of scope | Later
- Why it matters: Decides whether new-user seeding is a mechanism to evaluate.
- Waiting on it: N-27, C-D08/ARMS-CACHE

**Q-J25** [later gate] [partly answered] Which deployment scenarios should the policy and its evaluation target (you mentioned, for example, an automated bug-solving cloud agent and a customer-support agent), and does that imply repeated returning users or mostly single long runs?

- What the meetings already say: [Partly] 'The same problem is applicable for any kind of agent ... a salesman ... a recruiter ... marketing' (INT-T-002 L345-L354); no scenario chosen.
- Still to ask: the part not covered above.

- Answer format: Scenario list: ... | Session pattern: ...
- Why it matters: Fixes the session pattern and whether memory and cache expiry between sessions matter.
- Waiting on it: N-25


## D. The form of the policy

**Q-J08** [later gate] [partly answered] Is the staged 'one question per step' graph a binding form of the policy, or an illustration? Is a policy whose stages appear only where a stated test justifies them (including zero narrowing stages) acceptable?

- What the meetings already say: [Partly] 14 Oct: a staged graph with re-adding, 'that is your novelty' (INT-T-003 L386-L404); 21 Oct: scope memory and tool calls, graph not mentioned (INT-T-002 L223-L225).
- Still to ask: the part not covered above.

- Answer format: Binding | Illustration; stages only where justified | Other
- Why it matters: If binding, the graph must contain real narrowing stages even if the study finds none pays.
- Waiting on it: C-D03

**Q-J09** [later gate] [partly answered] What do 'context' and 'scenario' mean: the individual request, the trajectory so far, or the deployment?

- What the meetings already say: [Partly] 14 Oct: who invokes the agent (INT-T-003 L261); 21 Oct: what the model is given, tools, knowledge, memory, settings, modalities (INT-T-002 L176-L190).
- Still to ask: the part not covered above.

- Answer format: Request | Trajectory | Deployment | Combination | Other
- Why it matters: v4 adapts at deployment level and via the request/trajectory only through optional stages.
- Waiting on it: C-D03/CONTEXT, C-D03

**Q-J11** [later gate] [partly answered] Who or what should answer each stage's question: the model, a rule, or a score?

- What the meetings already say: [Partly] Stage one from who invokes (INT-T-003 L261); later stage Executor-style or semantic narrowing, 'You have to figure it out' (L306-L308).
- Still to ask: the part not covered above.

- Answer format: Model | Rule | Score | Empirical question (test both) | Other
- Why it matters: v4 leaves it empirical; a restriction changes the arms.
- Waiting on it: C-D03/ANSWERER

**Q-J12** [before implementation (G1: C-D07/GRADED, C-D07, C-D08/EC3)] [partly answered] Is graded/partial exposure (names only, compact schema, full schema) still a required lens, as in the June L0-L3 and the 2 Oct tier example?

- What the meetings already say: [Partly] Partial information as 'this lens', 'not saying this is the best way', numbers 'not rigid' (INT-T-004 E550-E570, E774).
- Still to ask: the part not covered above.

- Answer format: Required | Optional | Dropped
- Why it matters: The 14 Oct excerpts describe keep/remove and re-adding, not grades.
- Waiting on it: C-D07/GRADED, C-D07, C-D08/EC3


## E. What counts as a finding, and what to do beyond the context window

**Q-J13** [before implementation (G1: C-D08/DELTA)] Beyond the point where all tools cannot fit in the context window, is a frontier plus a gap to a pool reference (no noninferiority to expose-all) acceptable? Who sets the margin or token budget from which a policy is chosen?

- Answer format: Acceptable; margin/budget set by ... | Not acceptable; require ... | Other
- Why it matters: Without it no claim above n_fit can be made against expose-all.
- Waiting on it: C-E06, C-S13, C-S13/CALIB, C-D08/DELTA

**Q-J14** [before implementation (G1: C-D08/DELTA, C-D08/STRATA)] [partly answered] Does 'accuracy as high as possible' mean a margin (what size, per stratum?) or a frontier? May the tool count be a reported variable while tokens are the criterion?

- What the meetings already say: [Partly] 'match the baseline accuracy while giving lesser and lesser tool' (INT-T-004 E206); 'accuracy as high as possible' (INT-T-003 L159); no margin.
- Still to ask: the part not covered above.

- Answer format: Margin of ... | Frontier | Other; Count: reported / criterion
- Why it matters: Fixes delta and whether noninferiority testing is used at all.
- Waiting on it: C-D08/DELTA, C-D08/STRATA, C-D02, C-S14


## F. Baselines


## G. Parameters and breadth of the evaluation

**Q-J20** [before implementation (G1: C-D08)] [partly answered] Which numeric parameters do you want fixed now (margin, alpha, strata, epsilon, search width, discovery budget) and which may be set after a pilot?

- What the meetings already say: [Partly] Tier sizes 'not rigid' (INT-T-004 E552-E560); start with about 20 samples (E749); delta, epsilon, N_dep not addressed.
- Still to ask: the part not covered above.

- Answer format: List: now / after pilot
- Why it matters: A parameter can be deferred to a documented pilot only if it cannot change the pilot's interpretation.
- Waiting on it: C-D08

**Q-J21** [before implementation (G1: C-D08/EC1)] [partly answered] How many models or model families should evaluations cover (you said behaviour does not transfer across models)?

- What the meetings already say: [Partly] Multiple goals, settings, repeated runs (INT-T-002 L441-L443); number of models not given.
- Still to ask: the part not covered above.

- Answer format: N models; families: ...
- Why it matters: Drives cost and the sample plan.
- Waiting on it: AS-12, C-D08/EC1


## H. Prior art, and the evidence on your statements

**Q-J22** [later gate] [partly answered] Do you want a prior-art / novelty check of the staged graph (you said 'that is your novelty'), or is novelty not a thesis requirement?

- What the meetings already say: [Partly] 'nothing is noble [novel] ... that is actually the novelty. You have to just sell it as a novely' (INT-T-003 L227-L233); monthly search not to reinvent the wheel (INT-T-004 E591-E605).
- Still to ask: the part not covered above.

- Answer format: Check required | Not required | Other
- Why it matters: v4 makes no novelty claim; every mechanism exists.
- Waiting on it: C-D06/NOVELTY

**Q-J28** [later gate] [partly answered] Which documentation or source did you mean when you said the partial-information idea comes from another party's documentation (transcript 00:41:23)?

- What the meetings already say: [Partly] 'this partial thingy ... cames out from someone else ... I just read their doc' (INT-T-004 E593); Executor 'doing the same thing' (E605-E607); not named.
- Still to ask: the part not covered above.

- Answer format: Name or link ... | Cannot recall | Not needed
- Why it matters: The stored sources hold twenty candidates of five kinds (hidden definitions with a search tool, facade with children revealed on use, names plus short descriptions, a listing step apart from a schema step, a category statement); without his answer the prior art for this idea cannot be named.
- Waiting on it: AS-09

**Q-J29** [later gate] The stored literature suggests sharper versions of four of your statements. Do you accept, amend or drop each? (A6) Token reduction keeps accuracy while the required tools stay reachable and costs accuracy when a filter drops them or is lexical. (A12) Effect sizes and model rankings vary by model while the sign of exposure-reduction effects is often shared, so evaluate on several models and report per model. (A2) A symbolic selector with annotated contracts beat the all-tools LLM arm (85.7% vs 32.1%; 97.0% vs 53.5%), but no source gives an LLM selector the same annotations. (A11) In ComplexMCP an LLM-written query beat an embedded question (36.88 vs 27.65 for Gemini-3-flash).

- Answer format: Accept / Amend: ... / Drop, for each of the four
- Why it matters: Turns the evidence into statements the supervisor owns; shapes the evaluation (how many models, which selector arms).
- Waiting on it: AS-06, AS-12, AS-02, AS-11


## Already answered in the meetings of 2, 14 and 21 October (AUTH-018; not to be asked again)
- **Q-J23** What did you mean by 'What you have found and narrowed down is some methodologies' (whose findings)? -> [Answered] 'What you have found and narrowed down is some methodologies ... So, we have some mechanism families' (INT-T-003 L159-L161).
- **Q-J17** Is writing the evaluation script part of the 21 Oct deliverable, and what does 'implement' cover (script, pilots, experi -> [Answered] For 21 Oct: no implementation (INT-T-003 L439); after 21 Oct: experiments with a text-file memory, no engineering, many goals, settings, repeated runs (INT-T-002 L426-L458).
- **Q-J02** Is the research question's unit 'count of tools' (your 14 Oct wording) or model-visible tokens / cost, and does 'we don' -> [Answered] 'your idea was never to filter out tools. your idea was to save tokens ... The problem was to save token' (INT-T-004 E524-E526); RQ wording kept with 'count of tools' (INT-T-003 L159); 'narrowing down from 100 to 10 ... reducing 90% of token' (L377).
- **Q-J04** Over what horizon should cost be measured: one run, several turns within a conversation, or across sessions? Is cache ex -> [Answered] Average over many turns, a few failing turns may cost more (INT-T-002 L306-L320); a return 'tomorrow' should start from a short summary (L369-L384); 'save token for a number of turns' (INT-T-004 E778).
- **Q-J05** Memory scope: only our stored record of tools previously found and used (per user or role, so a returning user starts wi -> [Answered] 'it depends on what you are building' (INT-T-002 L146); 'you can do only memory and tool calls. Forget about knowledge ... memory should help tool calls' (L223-L225); summary of interaction and tool calls, relevant part first (L245, L375-L384); 'tools and memory' (L390).
- **Q-J07** Must each stage (step) save tokens, or is it enough that the whole trajectory/policy does? Does the possibility of re-ad -> [Answered] 'each step is there to save some token' (INT-T-004 E774); saving judged over a number of turns, one dearer turn 'doesn't matter' (E778-E790).
- **Q-J10** What does 'which one applies at which stage' mean: what are the 'stages' (policy stages or evaluation stages) and what i -> [Answered] 'which one applies at which stage. You will have different stages' (INT-T-003 L306-L308); 'At each step you have to ask yourself one question' (L390).
- **Q-J15** Would regime-conditional findings (including 'not established' and negative outcomes) count as the findings you require? -> [Answered] 'even if the result is negative it's a thesis ... can you write a paper ... have to do it systematically' (INT-T-003 L363-L365).
- **Q-J16** Must the existing code-mediated project ('Executor') be a baseline arm, and which tool or project did you mean by that n -> [Answered] Executor: 'download this run this ... benchmark it ... This is your baseline. You should have multiple baselines' (INT-T-004 E622-E626); identity: the startup he shared (E583-E612).
