# Questions for the supervisor (draft for the human to send or bring; generated from the ledger's Questions sheet on 2026-10-20)

Neutral wording, one issue per question, taken from the ledger (sheet Questions). Each question says what it decides and which open ledger items wait on it. 'Before implementation' marks questions linked to items whose gate is G1 (nothing can start until they are answered or the item is explicitly deferred). The ledger is the canonical record; answers go into its YOUR ANSWER column in the supervisor's own words.

**Order of use.** The first measurement of billing and cache behaviour on a named provider does not, in my reading, depend on the policy form or the arm table (it observes the provider, not a policy); the ledger currently lists the arm decision (C-D08) as a hard prerequisite for it, and that listing is an inherited assumption that the human may confirm or drop. If dropped, the first measurement needs only B (Q-J03, Q-J04, Q-J24) plus the human's authorization (Q-U14). Everything in D to G is needed before any arm experiment.


## A. What governs Project A, and what is due

**Q-J01** [before implementation (G1: C-D01, C-D07)] Does the June 2026 expose still govern the thesis scope? If anything changed, which exact clauses are amended (compact interfaces L0-L3, execute/expand/abstain, lifecycle/removal, staged policy, evaluation)?

- Answer format: Governs unchanged | Amended in these clauses: ... | Replaced by the October staged-policy framing | Other
- Why it matters: Decides which parts of Project A every test and design choice must cover; the repo cannot see the June text.
- Waiting on it: C-D01, C-D07

**Q-J23** [before implementation (G1: C-D01/REFERENT)] What did you mean by 'What you have found and narrowed down is some methodologies' (whose findings)?

- Answer format: Free text
- Why it matters: Undefined referent in excerpt E1; low priority.
- Waiting on it: C-D01/REFERENT

**Q-J17** [before implementation (G1: C-D05)] Is writing the evaluation script part of the 21 Oct deliverable, and what does 'implement' cover (script, pilots, experiments)?

- Answer format: Script due | Policy only | Script allowed but no runs | Other
- Why it matters: Hard gate before any implementation.
- Waiting on it: C-D05

**Q-J18** [before implementation (G1: C-D05)] Does the 21 Oct deliverable replace the 2 Oct one? Was the 2 Oct deliverable (document plus draft step-by-step policy) delivered?

- Answer format: Replaces | Adds to | Other; Delivered: yes/no
- Why it matters: Not known to the repo.
- Waiting on it: C-D05


## B. What to minimise and report (objective, accounting, horizon)

**Q-J02** [later gate] Is the research question's unit 'count of tools' (your 14 Oct wording) or model-visible tokens / cost, and does 'we don't need to change it' keep the 'count of tools' wording?

- Answer format: Count of tools | Tokens | Cost | Combination: ... | Other
- Why it matters: Changes the criterion and which surface is chosen; with thousands of tools the count cannot decide feasibility (tokens do).
- Waiting on it: C-D02

**Q-J03** [before implementation (G1: C-D08/EC5)] What should be primarily minimised or reported: model-visible input tokens, the billed cost (input, cache write, cache read and output tokens under a named price table), or a stated combination? Should output tokens count?

- Answer format: Tokens | Bill | Both with priority ... | Other; Output tokens: count / report only / ignore
- Why it matters: Replaces the AUTH-006 working objective if it changes; fixes what pilots report as primary (they can record everything either way).
- Waiting on it: C-D02, N-1, N-4, C-D08/EC5

**Q-J04** [before implementation (G1: C-D08/EC1)] Over what horizon should cost be measured: one run, several turns within a conversation, or across sessions? Is cache expiry between sessions in scope?

- Answer format: One run | Several turns | Across sessions (with session gap assumptions ...) | Cache expiry in/out of scope
- Why it matters: Across sessions adds session count and gap as regime variables and needs a session vehicle.
- Waiting on it: N-3, C-D02, C-D08/EC1

**Q-J24** [before implementation (G1: C-D08/EC1)] Which providers and models should the bill/cache analysis cover (to choose the price tables)?

- Answer format: Provider/model list
- Why it matters: Prices and cache rules are provider-specific.
- Waiting on it: C-D08/EC1

**Q-J19** [later gate] Should the offline cost of choosing the configuration (development runs, amortised over a deployment horizon N_dep) be charged to the policy, and over what horizon?

- Answer format: Charged over N = ... | Reported only | Not counted
- Why it matters: Part of the accounting contract.
- Waiting on it: C-S17, C-S20


## C. Memory, caching and deployment (your 19 October points)

**Q-J05** [before implementation (G1: C-D07)] Memory scope: only our stored record of tools previously found and used (per user or role, so a returning user starts with those tools), or also storage/summarisation of conversation history, or full agent memory?

- Answer format: Tool-usage memory only | Plus conversation memory | Full agent memory | Other
- Why it matters: Decides whether cross-session discovery memory (N-6, N-7) is in the thesis, deferred, or enlarged.
- Waiting on it: N-2, N-6, N-7, C-D07, N-22

**Q-J06** [before implementation (G1: C-D07, C-D08/ARMS-CACHE)] Joaa wrote: 'So you have to combine all three to find the best policy: MCP server context, memory, explicit caching.' How should the combination be treated in this thesis: all three as the design space, a subset, or later work?

- Answer format: All three | A subset: ... | Later work | Other
- Why it matters: The combination has not been evaluated in the repo's sources yet; whether it is the design space is a scope choice, and the proposal can be adopted, refined or narrowed.
- Waiting on it: N-22, C-D07, C-D08/ARMS-CACHE

**Q-J26** [before implementation (G1: C-D08/ARMS-CACHE)] Should explicit caching choices (where cache breakpoints sit, how long to retain) be variables of the policy, or recorded provider behaviour while the policy concerns what is exposed? You also mentioned implicit caching.

- Answer format: Policy variables: ... | Recorded only | Both
- Why it matters: Decides whether cache layout and retention are arms or covariates.
- Waiting on it: N-26, C-D08/ARMS-CACHE

**Q-J27** [before implementation (G1: C-D08/ARMS-CACHE)] Should the policy include anticipating likely needs before the first request (from role or deployment for a new user, from memory for a returning user), as in your stranger/colleague analogy, or is the first-request context left to the discovery stages?

- Answer format: Include: ... | Out of scope | Later
- Why it matters: Decides whether new-user seeding is a mechanism to evaluate.
- Waiting on it: N-27, C-D08/ARMS-CACHE

**Q-J25** [later gate] Which deployment scenarios should the policy and its evaluation target (you mentioned, for example, an automated bug-solving cloud agent and a customer-support agent), and does that imply repeated returning users or mostly single long runs?

- Answer format: Scenario list: ... | Session pattern: ...
- Why it matters: Fixes the session pattern and whether memory and cache expiry between sessions matter.
- Waiting on it: N-25


## D. The form of the policy

**Q-J07** [later gate] Must each stage (step) save tokens, or is it enough that the whole trajectory/policy does? Does the possibility of re-adding a tool change your answer?

- Answer format: Per stage | Per trajectory | Per policy over many requests | Other
- Why it matters: Decides how 'a stage pays' is tested and whether insurance/recovery stages are allowed.
- Waiting on it: C-D04

**Q-J08** [later gate] Is the staged 'one question per step' graph a binding form of the policy, or an illustration? Is a policy whose stages appear only where a stated test justifies them (including zero narrowing stages) acceptable?

- Answer format: Binding | Illustration; stages only where justified | Other
- Why it matters: If binding, the graph must contain real narrowing stages even if the study finds none pays.
- Waiting on it: C-D03

**Q-J09** [later gate] What do 'context' and 'scenario' mean: the individual request, the trajectory so far, or the deployment?

- Answer format: Request | Trajectory | Deployment | Combination | Other
- Why it matters: v4 adapts at deployment level and via the request/trajectory only through optional stages.
- Waiting on it: C-D03/CONTEXT, C-D03

**Q-J10** [later gate] What does 'which one applies at which stage' mean: what are the 'stages' (policy stages or evaluation stages) and what is 'which one'? What does 'time' mean in 'which one works at which time'?

- Answer format: Free text
- Why it matters: Undefined antecedents in the excerpts E4 and E6.
- Waiting on it: C-D03/STAGES

**Q-J11** [later gate] Who or what should answer each stage's question: the model, a rule, or a score?

- Answer format: Model | Rule | Score | Empirical question (test both) | Other
- Why it matters: v4 leaves it empirical; a restriction changes the arms.
- Waiting on it: C-D03/ANSWERER

**Q-J12** [before implementation (G1: C-D07/GRADED, C-D07, C-D08/EC3)] Is graded/partial exposure (names only, compact schema, full schema) still a required lens, as in the June L0-L3 and the 2 Oct tier example?

- Answer format: Required | Optional | Dropped
- Why it matters: The 14 Oct excerpts describe keep/remove and re-adding, not grades.
- Waiting on it: C-D07/GRADED, C-D07, C-D08/EC3


## E. What counts as a finding, and what to do beyond the context window

**Q-J13** [before implementation (G1: C-D08/DELTA)] Beyond the point where all tools cannot fit in the context window, is a frontier plus a gap to a pool reference (no noninferiority to expose-all) acceptable? Who sets the margin or token budget from which a policy is chosen?

- Answer format: Acceptable; margin/budget set by ... | Not acceptable; require ... | Other
- Why it matters: Without it no claim above n_fit can be made against expose-all.
- Waiting on it: C-E06, C-S13, C-S13/CALIB, C-D08/DELTA

**Q-J14** [before implementation (G1: C-D08/DELTA, C-D08/STRATA)] Does 'accuracy as high as possible' mean a margin (what size, per stratum?) or a frontier? May the tool count be a reported variable while tokens are the criterion?

- Answer format: Margin of ... | Frontier | Other; Count: reported / criterion
- Why it matters: Fixes delta and whether noninferiority testing is used at all.
- Waiting on it: C-D08/DELTA, C-D08/STRATA, C-D02, C-S14

**Q-J15** [later gate] Would regime-conditional findings (including 'not established' and negative outcomes) count as the findings you require? Is a regime map a sufficient contribution?

- Answer format: Yes | No | Only if ... | Other
- Why it matters: Decides whether a null/conditional result is a thesis; also whether a big study is worthwhile.
- Waiting on it: C-D06


## F. Baselines

**Q-J16** [before implementation (G1: C-D08/GATEWAY, C-D08/EXEC, C-D08)] Must the existing code-mediated project ('Executor') be a baseline arm, and which tool or project did you mean by that name?

- Answer format: Required arm | Optional | Not an arm | Identity: ...
- Why it matters: The identification of 'Executor' is the researchers', not in the transcript lines.
- Waiting on it: C-D08/GATEWAY, C-D08/EXEC, C-D08


## G. Parameters and breadth of the evaluation

**Q-J20** [before implementation (G1: C-D08)] Which numeric parameters do you want fixed now (margin, alpha, strata, epsilon, search width, discovery budget) and which may be set after a pilot?

- Answer format: List: now / after pilot
- Why it matters: A parameter can be deferred to a documented pilot only if it cannot change the pilot's interpretation.
- Waiting on it: C-D08

**Q-J21** [before implementation (G1: C-D08/EC1)] How many models or model families should evaluations cover (you said behaviour does not transfer across models)?

- Answer format: N models; families: ...
- Why it matters: Drives cost and the sample plan.
- Waiting on it: AS-12, C-D08/EC1


## H. Prior art, and the evidence on your statements

**Q-J22** [later gate] Do you want a prior-art / novelty check of the staged graph (you said 'that is your novelty'), or is novelty not a thesis requirement?

- Answer format: Check required | Not required | Other
- Why it matters: v4 makes no novelty claim; every mechanism exists.
- Waiting on it: C-D06/NOVELTY

**Q-J28** [later gate] Which documentation or source did you mean when you said the partial-information idea comes from another party's documentation (transcript 00:41:23)?

- Answer format: Name or link ... | Cannot recall | Not needed
- Why it matters: The stored sources hold twenty candidates of five kinds (hidden definitions with a search tool, facade with children revealed on use, names plus short descriptions, a listing step apart from a schema step, a category statement); without his answer the prior art for this idea cannot be named.
- Waiting on it: AS-09

**Q-J29** [later gate] The stored literature suggests sharper versions of four of your statements. Do you accept, amend or drop each? (A6) Token reduction keeps accuracy while the required tools stay reachable and costs accuracy when a filter drops them or is lexical. (A12) Effect sizes and model rankings vary by model while the sign of exposure-reduction effects is often shared, so evaluate on several models and report per model. (A2) A symbolic selector with annotated contracts beat the all-tools LLM arm (85.7% vs 32.1%; 97.0% vs 53.5%), but no source gives an LLM selector the same annotations. (A11) In ComplexMCP an LLM-written query beat an embedded question (36.88 vs 27.65 for Gemini-3-flash).

- Answer format: Accept / Amend: ... / Drop, for each of the four
- Why it matters: Turns the evidence into statements the supervisor owns; shapes the evaluation (how many models, which selector arms).
- Waiting on it: AS-06, AS-12, AS-02, AS-11

