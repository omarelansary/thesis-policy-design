# 07. Supervisor-ready presentation outline (for the 2026-10-21 meeting)

Status: provisional outline; every effectiveness statement is a hypothesis. Nothing was implemented or run. Evidence labels: *read* = a source passage was read and, for eight pivotal passages, independently checked against the original; *vendor* = a vendor's own documentation claim; *derived* = arithmetic from extracts; *untested* = a hypothesis with a stated falsifier. Suggested length: about ten minutes, then discussion.

## 1. The problem, and what is being traded (1 slide)
Reduce unnecessary tool exposure to LLM agents while preserving task performance and counting the costs of deciding, discovering and using tools. Four quantities are kept distinct: number of tools, model-visible tokens, cumulative tokens, billed cost. *Fewer tools does not by itself mean lower cumulative or billed cost, or higher success.* The formulation (cost reading O1 or exposure reading O2; count or tokens, Q1) is a choice that needs your decision.

## 2. What the evidence says, in four lines (1 slide)
- Restricting exposure by retrieval lowered success in several controlled settings *(read)*; strong models largely mitigated distraction in one study *(map)*.
- Cache pricing makes visible-token savings an unreliable proxy for billed savings; in the one direct cache table, a restricted per-request list showed a lower cache hit rate and **no billed-cost advantage** (difference inconclusive; single-step replay; provider and price unstated) *(read, checked)*; the cache state moved the full-library cost about 50 times *(read)*.
- A tool that is not exposed can never produce a call or an error, so its need can be signalled only by the model's request or an inference from other signals *(reasoning)*.
- No stored source shows a second filtering stage paying or failing to pay on tools; a two-stage router matched single-stage retrieval in success *(read; no token data)*.

## 3. The candidate policy in one picture (1 slide; graph in `01-policy-candidate.md`)
Offline, an explicit break-even rule decides which tools sit in a stable cached prefix (using usage frequency, definition length, cache prices, expected session length). The rest is reachable only through a prompted search tool; found tools are **appended** after the cache breakpoint; nothing is removed inside a session. If the rule keeps everything, the policy *is* expose-all. Every decision has a stated question, actor, inputs and class, rule and test; no runtime decision uses gold tools, reference trajectories or benchmark annotations.

## 4. What it is *not* (1 slide; say this early)
A parameterised static core plus deferred loading. No stages. No per-task adaptivity. No novelty claim. No demonstrated advantage. The supervisor's staged graph (system-run relevance questions, a later stage re-adding a tool) is kept as a materially different candidate (C-B) and is an arm of the evaluation.

## 5. Why it is still worth testing (1 slide)
It is fully specified; it contains expose-all, a static core and a listed grade as special cases; arms were added so the new decision rule cannot hide behind a larger or better core (a frequency core of equal size, with and without search; a core whose size is swept empirically); and the first experiment (cost mechanics per provider) is cheap and can end the line. The strongest rival, cached expose-all, wins when the read price is low, traffic dense, the catalogue fits and usage is flat; the candidate wins only in named regimes whose numeric region is unknown.

## 6. How the evaluation is built to be able to say no (1 slide)
One scorer for every arm; population-level estimands; strata fixed before the run (not by what an arm exposed); recovery judged by value and price weighted by miss prevalence; initiators compared as a trade-off, not a conjunction; cost judged by response curves with more than two exposure levels, not by "no inversion observed"; every component has a falsifier that is the negation of its claim. Order of questions: cost mechanics, usage concentration, initiation, recovery and initiator, full comparison.

## 7. What is unsupported (1 slide)
Billed-cost savings from any restriction; whether deferred definitions are billed; whether a stable surface keeps its hit rate; whether models search when a needed tool is absent; whether call frequency measures need; whether a second stage pays; whether a system trigger beats model emission. The review was adversarial and the proposer defended its assumptions; the challenger withdrew or downgraded most objections but maintained that the candidate survives only as a conditional case.

## 8. Questions for the supervisor (the last slide; they change what the proposal should be)
1. Is the research question's unit "count of tools" (as in your restatement) or model-visible tokens and cost? Does "we don't need to change it" keep the earlier "never filter out tools, save tokens" formulation?
2. Is the staged relevance-question form (stages, each filtering the remaining tools) binding on the policy, or an illustration? Would a policy with **no stages**, a cache-aware core plus on-demand search, be acceptable as "the policy" for this week?
3. What does "each step saves tokens" mean: per step, or collectively over a session? Does a later re-add violate it?
4. Does a well-founded **negative or conditional result** ("a second stage does not pay in regime X"; "expose-all wins on provider Y") count as the findings required for the thesis, and as the contribution?
5. Must the code-mediated existing project (the named baseline) be a baseline arm?
6. What margin counts as "maintained", and is a written evaluation specification (rather than runnable code) the expected evaluation script this week?

## 9. Decisions you (the student) need to make before the meeting
O1 vs O2; whether to present C-A alone, or C-A with C-B as the supervisor's own form; the order in which to ask questions 1 and 2 (they change the candidate); whether to authorize a bounded, separately-authorized smoke execution of the closest evaluation vehicle (not authorized now).
