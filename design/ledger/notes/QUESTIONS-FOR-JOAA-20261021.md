# Questions for the supervisor (draft for the human to send or bring; generated from the ledger's Questions sheet on 2026-10-21, after the intake of the meetings of 2, 14 and 21 October)

Neutral wording, one issue per question, taken from the ledger (sheet Questions). Each question says what it decides and which open ledger items wait on it. 'Before implementation' marks questions linked to items whose gate is G1 (nothing can start until they are answered or the item is explicitly deferred). The ledger is the canonical record; answers go into its YOUR ANSWER column in the supervisor's own words.

**Order of use.** The first measurement of billing and cache behaviour on a named provider does not, in my reading, depend on the policy form or the arm table (it observes the provider, not a policy); the ledger currently lists the arm decision (C-D08) as a hard prerequisite for it, and that listing is an inherited assumption that the human may confirm or drop. If dropped, the first measurement needs only B (Q-J03, Q-J04, Q-J24) plus the human's authorization (Q-U14). Everything in D to G is needed before any arm experiment.


## A. What governs Project A, and what is due


## B. What to minimise and report (objective, accounting, horizon)


## C. Memory, caching and deployment (your 19 October points)

**Q-J06** [before implementation (G1: C-D08/ARMS-CACHE)] [partly answered] Joaa wrote: 'So you have to combine all three to find the best policy: MCP server context, memory, explicit caching.' How should the combination be treated in this thesis: all three as the design space, a subset, or later work?

- What the meetings already say: [Partly] Explicit cache 'applicable for memory ... knowledge' (INT-T-002 L197) in the 'all in theory' part (L221); practical scope tools and memory only (L223-L225).
- Still to ask: the part not covered above.

- Answer format: All three | A subset: ... | Later work | Other
- Why it matters: The combination has not been evaluated in the repo's sources yet; whether it is the design space is a scope choice, and the proposal can be adopted, refined or narrowed.
- Waiting on it: N-22, C-D08/ARMS-CACHE

**Q-J26** [before implementation (G1: C-D08/ARMS-CACHE)] [partly answered] Should explicit caching choices (where cache breakpoints sit, how long to retain) be variables of the policy, or recorded provider behaviour while the policy concerns what is exposed? You also mentioned implicit caching.

- What the meetings already say: [Partly] 'keep them in the explicit cache and that's negligible cost' (INT-T-002 L207-L209), in the 'all in theory' part (L221).
- Still to ask: the part not covered above.

- Answer format: Policy variables: ... | Recorded only | Both
- Why it matters: Decides whether cache layout and retention are arms or covariates.
- Waiting on it: N-26, C-D08/ARMS-CACHE


## D. The form of the policy

**Q-J09** [later gate] [partly answered] What do 'context' and 'scenario' mean: the individual request, the trajectory so far, or the deployment?

- What the meetings already say: [Partly] 14 Oct: who invokes the agent (INT-T-003 L261); 21 Oct: what the model is given, tools, knowledge, memory, settings, modalities (INT-T-002 L176-L190).
- Still to ask: the part not covered above.

- Answer format: Request | Trajectory | Deployment | Combination | Other
- Why it matters: v4 adapts at deployment level and via the request/trajectory only through optional stages.
- Waiting on it: C-D03/CONTEXT

**Q-J11** [later gate] [partly answered] Who or what should answer each stage's question: the model, a rule, or a score?

- What the meetings already say: [Partly] Stage one from who invokes (INT-T-003 L261); later stage Executor-style or semantic narrowing, 'You have to figure it out' (L306-L308).
- Still to ask: the part not covered above.

- Answer format: Model | Rule | Score | Empirical question (test both) | Other
- Why it matters: v4 leaves it empirical; a restriction changes the arms.
- Waiting on it: C-D03/ANSWERER


## E. What counts as a finding, and what to do beyond the context window


## F. Baselines


## G. Parameters and breadth of the evaluation


## H. Prior art, and the evidence on your statements

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
- **Q-J30** On 14 October you asked for a staged graph that filters tools (one question per stage, tools can be added back); on 21 O -> [Answered by the human] line 5: do both; memory deciding which tools are offered is part of the staged policy.
- **Q-J01** Does the June 2026 expose still govern the thesis scope? If anything changed, which exact clauses are amended (compact i -> [Answered by the human] line 6: the expose does not govern; its ideas are candidates verified like any other.
- **Q-J23** What did you mean by 'What you have found and narrowed down is some methodologies' (whose findings)? -> [Answered] 'What you have found and narrowed down is some methodologies ... So, we have some mechanism families' (INT-T-003 L159-L161).
- **Q-J17** Is writing the evaluation script part of the 21 Oct deliverable, and what does 'implement' cover (script, pilots, experi -> [Answered] For 21 Oct: no implementation (INT-T-003 L439); after 21 Oct: experiments with a text-file memory, no engineering, many goals, settings, repeated runs (INT-T-002 L426-L458).
- **Q-J18** Does the 21 Oct deliverable replace the 2 Oct one? Was the 2 Oct deliverable (document plus draft step-by-step policy) d -> [Answered by the human] line 7: research and a drafted policy now; proof-of-concept tests of parts in a loop; end-to-end later. | Earlier from the meetings: [Partly] 2 Oct: 'write the draft version of uh your policy' (INT-T-004 E804); 14 Oct: 'You need to give me this policy' (INT-T-003 L429-L447). Delivery of the 2 Oct draft not stated.
- **Q-J02** Is the research question's unit 'count of tools' (your 14 Oct wording) or model-visible tokens / cost, and does 'we don' -> [Answered] 'your idea was never to filter out tools. your idea was to save tokens ... The problem was to save token' (INT-T-004 E524-E526); RQ wording kept with 'count of tools' (INT-T-003 L159); 'narrowing down from 100 to 10 ... reducing 90% of token' (L377).
- **Q-J03** What should be primarily minimised or reported: model-visible input tokens, the billed cost (input, cache write, cache r -> [Answered by the human] line 8 and line 16: minimise the bill on average over turns and sessions, accuracy nearly the same; canonical equation of components. | Earlier from the meetings: [Partly] Money cost per turn, tokens and response time averaged over turns (INT-T-002 L275, L302, L354); 'we will not drop the cost' (INT-T-004 E697). No single primary estimand or price table named.
- **Q-J04** Over what horizon should cost be measured: one run, several turns within a conversation, or across sessions? Is cache ex -> [Answered] Average over many turns, a few failing turns may cost more (INT-T-002 L306-L320); a return 'tomorrow' should start from a short summary (L369-L384); 'save token for a number of turns' (INT-T-004 E778).
- **Q-J24** Which providers and models should the bill/cache analysis cover (to choose the price tables)? -> [Answered by the human] line 9: chosen when implementing.
- **Q-J19** Should the offline cost of choosing the configuration (development runs, amortised over a deployment horizon N_dep) be c -> [Answered by the human] line 10 (see Q-J03): selection and discovery cost is part of the averaged bill. | Earlier from the meetings: [Partly] 'if you use many many more token to filter out the tools then there is no value' (INT-T-004 E230-E232); amortisation not discussed.
- **Q-J05** Memory scope: only our stored record of tools previously found and used (per user or role, so a returning user starts wi -> [Answered] 'it depends on what you are building' (INT-T-002 L146); 'you can do only memory and tool calls. Forget about knowledge ... memory should help tool calls' (L223-L225); summary of interaction and tool calls, relevant part first (L245, L375-L384); 'tools and memory' (L390).
- **Q-J27** Should the policy include anticipating likely needs before the first request (from role or deployment for a new user, fr -> [Answered by the human] line 12: yes, as a small part, not the focus. | Earlier from the meetings: [Partly] Relevant part of memory first, more when asked (INT-T-002 L384); not all context 'just by saying hello' (L211-L216, theory part).
- **Q-J25** Which deployment scenarios should the policy and its evaluation target (you mentioned, for example, an automated bug-sol -> [Answered by the human] line 14: one long run and returning users. | Earlier from the meetings: [Partly] 'The same problem is applicable for any kind of agent ... a salesman ... a recruiter ... marketing' (INT-T-002 L345-L354); no scenario chosen.
- **Q-J07** Must each stage (step) save tokens, or is it enough that the whole trajectory/policy does? Does the possibility of re-ad -> [Answered] 'each step is there to save some token' (INT-T-004 E774); saving judged over a number of turns, one dearer turn 'doesn't matter' (E778-E790).
- **Q-J08** Is the staged 'one question per step' graph a binding form of the policy, or an illustration? Is a policy whose stages a -> [Answered by the supervisor's words and the human's decision] Supervisor 14 Oct: staged graph with re-adding (INT-T-003 L386-L404); the human: keep it and combine it with memory-informed tool offering (INT-T-005 line 5). | Earlier: [Partly] 14 Oct: a staged graph with re-adding, 'that is your novelty' (INT-T-003 L386-L404); 21 Oct: scope memory and tool calls, graph not mentioned (INT-T-002 L223-L225).
- **Q-J10** What does 'which one applies at which stage' mean: what are the 'stages' (policy stages or evaluation stages) and what i -> [Answered] 'which one applies at which stage. You will have different stages' (INT-T-003 L306-L308); 'At each step you have to ask yourself one question' (L390).
- **Q-J12** Is graded/partial exposure (names only, compact schema, full schema) still a required lens, as in the June L0-L3 and the -> [Answered by the supervisor's words and the human's decision] Supervisor 2 Oct: one lens, not the best way (INT-T-004 E550-E570); the human: treat such ideas as candidates (INT-T-005 lines 1, 6). | Earlier: [Partly] Partial information as 'this lens', 'not saying this is the best way', numbers 'not rigid' (INT-T-004 E550-E570, E774).
- **Q-J13** Beyond the point where all tools cannot fit in the context window, is a frontier plus a gap to a pool reference (no noni -> [Answered by the human] line 16 (no margin or budget): above the window the frontier is reported.
- **Q-J14** Does 'accuracy as high as possible' mean a margin (what size, per stratum?) or a frontier? May the tool count be a repor -> [Answered by the human] line 16: no margin, no budget, no hard thresholds; accuracy nearly the same. | Earlier from the meetings: [Partly] 'match the baseline accuracy while giving lesser and lesser tool' (INT-T-004 E206); 'accuracy as high as possible' (INT-T-003 L159); no margin.
- **Q-J15** Would regime-conditional findings (including 'not established' and negative outcomes) count as the findings you require? -> [Answered] 'even if the result is negative it's a thesis ... can you write a paper ... have to do it systematically' (INT-T-003 L363-L365).
- **Q-J16** Must the existing code-mediated project ('Executor') be a baseline arm, and which tool or project did you mean by that n -> [Answered] Executor: 'download this run this ... benchmark it ... This is your baseline. You should have multiple baselines' (INT-T-004 E622-E626); identity: the startup he shared (E583-E612).
- **Q-J20** Which numeric parameters do you want fixed now (margin, alpha, strata, epsilon, search width, discovery budget) and whic -> [Answered by the supervisor's words and the human's decision] The human: no margin, budget or threshold (line 16); error control and strata in the end-to-end phase (line 7); kappa, discovery budget and call limit are set while drafting and testing the policy, not by the supervisor. | Earlier: [Partly] Tier sizes 'not rigid' (INT-T-004 E552-E560); start with about 20 samples (E749); delta, epsilon, N_dep not addressed.
- **Q-J21** How many models or model families should evaluations cover (you said behaviour does not transfer across models)? -> [Answered by the supervisor's words and the human's decision] The human: models chosen when implementing, several available through a free university API (line 9; REQ-U21-01); the supervisor: repeated runs and several settings (INT-T-002 L441-L443). | Earlier: [Partly] Multiple goals, settings, repeated runs (INT-T-002 L441-L443); number of models not given.
- **Q-J22** Do you want a prior-art / novelty check of the staged graph (you said 'that is your novelty'), or is novelty not a thesi -> [Answered by the supervisor's words and the human's decision] Supervisor: the novelty is the systematic combination and its findings, 'sell it as a novely' (INT-T-003 L227-L233), with a monthly search not to reinvent the wheel (INT-T-004 E591-E605); the human: success is the quality of the work (line 16) and no re-invention (line 1). No separate novelty assessment. | Earlier: [Partly] 'nothing is noble [novel] ... that is actually the novelty. You have to just sell it as a novely' (INT-T-003 L227-L233); monthly search not to reinvent the wheel (INT-T-004 E591-E605).
