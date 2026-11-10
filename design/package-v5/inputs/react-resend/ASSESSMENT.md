# ReAct re-send cost and the tool-exposure policy: independent assessment

As of 2026-11-09. Research owner: Claude (Sonnet 5.5), for the thesis `thesis-policy-design` (branches `v5-audit`, `v5-p5-break-even`). Nothing in the repository was changed, no paid run was made, nothing was committed.

The supervisor's observation is correct and already inside every bill we measured: in our 469-tool runs, re-reading the fixed prefix on each request was 66% of the bill. It does not require changing V5-R's rules. It does narrow what V5-R's measured savings can be said to show, and it exposes two gaps: AppWorld's native code-writing agent was never a comparison, and the number-of-requests lever was never analysed. The shared Claude chat does not support "the model waits"; it says the opposite.

**Second pass (added after a wider literature search; sections 7 and 8).** Eight independent researchers searched seven research communities and a coverage critic looked for omissions and contrary evidence. Nothing found overturns the assessment above, and nothing found removes the re-read charge on the routes the thesis uses. Four points change: whether clearing old tool results pays depends on trajectory length and cache behaviour, and on the cache-priced routes we measured our short tasks are below the break-even; omitting a needed tool can be fatal to accuracy, while its effect on the bill depends on how the agent behaves; a code-agent arm should start as a small pilot because the published comparisons are not like for like; and our cost split comes from single tasks of 10-13 requests, not from long multi-request sessions. A third pass then checked 31 sources against their full texts, and an adversarial review of that pass retracted or softened several statements; section 9 lists the changes. Final checks on the stored runs found that a few step-capped runs dominate some bills, which changes the GLM ratio (section 9.6). Revised recommendations are in section 8 and supersede section 5 where they differ.

## Decisions that need you

1. **Ask the supervisor one question:** what does "already solved" mean (serving-side KV retention, programmatic tool calling, or plain prompt caching), and is reducing the number of model calls now in scope? His 21 October scope was "memory and tool calls only" (REQ-O21-01). Your answer decides items 2 and 3 of the next-steps table.
2. **Authorize writing this analysis into the repository** (cost-anatomy note, corrected reuse-map rows). This session may not write under `.claude/` and did not write to the repo.
3. **Only if call-reduction or Anthropic programmatic tool calling becomes in scope:** authorize a small paid measurement (see Next steps). Otherwise run nothing for this concern.

**Added after the final checks:** 4. Decide how the results deck should present the GLM-5.3 bill ratio. The published 1.5x is mostly a runaway-loop effect in the subset arm: 7 step-capped runs are 75% of that arm's bill, and the ratio of mean per-task bills is 4.1x without them. Both numbers should be shown (section 9.6). 5. Decide whether the step cap and stop rule should be treated as a bill lever in its own right, since runaway runs re-send history up to 50 times.

## Verdict in one table

| Question | Answer | Weight |
| --- | --- | --- |
| Is the re-send cost real in our runs? | Yes. Fixed-prefix cache reads are 66% of both all-tools bills. | High: reproduced by two independent computations to the cent |
| Does V5-R's measured saving work through that term? | Yes, in these runs. The cache-read price difference explains 104% (MiniMax) and 129% (GLM) of the all-vs-subset gap. | Moderate: near-identity, and the arms differ in more than tool exposure |
| Does the Claude chat show the model can wait? | No. It says APIs are stateless and Claude Code resends the whole conversation each request. | High: Claude Code cost docs say the same |
| Must V5-R's rules change? | No evidence says so. Its claims need narrower scope and two added analyses. | Moderate |
| Must V5-R stay unchanged? | Its comparison set is incomplete: no code-agent baseline, no call-count analysis. | Moderate |

## 1. What we already knew

The repo modelled and measured the re-send cost before the supervisor raised it. It never analysed how to reduce the number of requests.

| Mechanism | Where it sits in the record |
| --- | --- |
| Bill is a sum over every request, with cache reads priced separately | `design/proposals/DPR-0006.md` sections 1-2 ("a request is one API call") |
| Cached prefix = tools, system, messages; editing the tools array rewrites the rest, appending does not | V5-R02, `design/package-v5/04-design.md`; probes P0 (`10-p0-university-api-reading.md`) |
| A client-side search is an extra request that re-reads the cached prefix | `design/package-v5/calc/regime_bill.py:15-16`; `04-design.md` section 2 |
| Cache reads dominate agent bills | `03-reuse-map.md` rows on Bai et al. (2604.22750) and 2607.12161 (system prompt plus tool definitions = 74.7% of billed cost) |
| Our own runs: 96% of the all-tools prompt is cache reads; 4.4x the prompt tokens cost 2.6x | `exchange/prior-work/v5-probes/results/R3-B/RESULTS-R3-B.md` |
| Number of requests is a cost driver | P3: the stop rule cut requests 32-48%; P2: the instruction-only arm on gpt-5-mini made 2.03x the calls for 1.37x the cost (`inputs/p2/RESULTS-P2-MAIN.md`) |
| Programmatic tool calling exists as an option | `03-reuse-map.md:105` ("REUSE as a conditional option"); vendor numbers -38% billed input, about +8% cost on tau2-bench |
| Observation masking is deferred | `05-poc-loop-and-e2e.md:18`, `12-experiment-readiness.md:13` (P4, "not needed yet") |
| The supervisor's own framing | 2026-10-02 and 2026-10-21 meeting records: explicit caching for tools and memory; savings judged over many turns, not per turn |

**Not found in the places searched** (`git grep` over `v5-audit`, design, ops, exchange, requirements): any use of AppWorld's code-writing agents (`react_code`, `simplified_react`, "code agent" return nothing relevant); any analysis of parallel tool calls or plan-first designs; any decomposition of a bill into prefix, history and output; InferCept, Continuum, AsyncLM, ReWOO, LLMCompiler, `previous_response_id`, WebSocket mode.

## 2. What the investigation establishes

### 2.1 The supervisor's premise, claim by claim

| Claim (supervisor or the shared chat) | Verdict | Evidence |
| --- | --- | --- |
| Each tool call is another model request carrying the same input; only the result is appended | **Correct** | Claude Code docs: it "sends your full conversation with every request, and each time Claude uses tools it sends another request carrying that batch of tool results." Anthropic caching docs: "Cache remains valid when only tool results are provided as user messages." |
| So the cost doubles, or 3 calls cost 3x | **Imprecise** | Repeated tokens are billed at the cache-read price (0.2x input on MiniMax-M3 and GLM-5.3 hosts; 0.1x, 0.05x, 0.025x on Anthropic models; 0.1x on gpt-5-mini). Output is not repeated. Our all-tools runs still spent 66% of the bill on prefix reads. |
| Claude Code "makes the LLM wait" | **Not supported** | Same Claude Code cost page; the shared chat's first answer rejects the premise. The API ends generation at `tool_use`. |
| Without caching cost grows quadratically; with caching it is near-linear | **Partly** | True of uncached input in general. With a large constant prefix cost is already near-linear (our all-tools arms). Where history dominates (subset arms) the quadratic part stays, only at the cheaper price. |
| Programmatic tool calling (PTC) is the closest thing to waiting | **Right in kind** | Docs: the model "is not re-sampled between the tool calls inside one code execution." But each pause is a new request that must "send the full conversation history plus your tool result" and "the same `tools` array." |
| "The resume requests don't run model inference" | **Plausible, billing unknown** | The docs never say how a resume request is billed. I searched the saved full text of the PTC page: only the vendor efficiency claims and "tool results from programmatic calls do not count toward your input/output token usage." |
| "Cut input tokens by 24% on two benchmarks" | **Misattributed** | It comes from Anthropic's web-search dynamic-filtering post (BrowseComp, DeepsearchQA; Sonnet 4.6, Opus 4.6), not PTC. The same post says price-weighted tokens rose for Opus 4.6. |
| "Docs don't say whether Haiku 5.5 supports PTC" | **Outdated** | The PTC page's supported-models list includes `claude-haiku-5-5`. |
| Sandbox cost, 4-minute timeout | **Confirmed** | $0.05 per container-hour, 5-minute minimum, 1,550 free hours a month; free when web search or fetch is in the request. |
| The chat's worked example (6x fewer tokens, 2-3x with caching) | **Depends on an unstated assumption** | I recomputed it. Cold 10k prefix: 3.1-3.3x. Warm prefix: 14-20x. If every resume is billed as a cache read of the prefix: 2.4-2.6x. |

Independent support for the cost shape: Bai et al. report that cache reads dominate raw volume and dollar cost in every phase of a Sonnet 4.5 case study. The Claude Code study (2607.12161) puts the harness base, meaning system prompt plus tool definitions, at 71.6% of context, 92.0% of cache reads and 74.7% of cost over 11,773 requests, from a reconstructed corpus with inferred cache attribution in which system prompt and tool definitions cannot be separated. Don't Break the Cache (2601.06007) measures 41-80% savings from caching on long agent sessions.

Other ways to cut re-sends, with what is actually known:

- **Server-side state** (OpenAI `previous_response_id`): OpenAI's docs say all previous input tokens "are billed as input tokens." No billing change. WebSocket mode claims up to about 40% faster for 20+ tool calls; the page says nothing about billing.
- **KV retention during tool calls** (InferCept, Continuum): self-hosted serving research; reports throughput and completion-time gains. I found no commercial API that passes this into price.
- **Plan-first designs** (ReWOO): 64% fewer tokens averaged over six benchmarks, but on 2023-era models, with a static plan. AppWorld's own plan-then-execute baseline did worse than ReAct for GPT-4o at about twice the cost.
- **Parallel calls:** our agent already does this (section 2.3).

### 2.2 Cost anatomy of our AppWorld runs

Source: per-request usage in the stored `lm_calls.jsonl` of runs `mm3-b1r-repeat`, `mm3-b2r-repeat`, `glm-b1-all-tools`, `glm-b2-control` plus `glm-b2-control-rest` (57 dev tasks each, reasoning on, one run per cell). "Prefix" is the first agent request of each task: system text, demonstrations, tool definitions, task. A prefix cache fills from the front, so cached tokens are allocated to the prefix first. Prices are the recorded ones: MiniMax-M3 on GMICloud 0.24 / 0.96 / 0.048 and GLM-5.3 at GMICloud prices 0.70 / 2.20 / 0.13 dollars per million tokens (fresh input / output / cache read). The reconstructed totals equal the recorded bills, and an independent re-derivation by a second agent matched them.

| Arm | Bill | Requests per task | Prefix: cache read | Prefix: fresh | History: cache read | History: fresh | Output | Predictor call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MiniMax, all 469 tools | $3.04 | 9.8 | **66%** | 6% | 7% | 6% | 14% | none |
| MiniMax, subset of at most 20 | $1.39 | 11.4 | 10% | 6% | 25% | 17% | **38%** | 4% |
| GLM, all 469 tools | $10.58 (computed) | 13.0 | **66%** | 1% | 14% | 3% | 16% | none |
| GLM, subset of at most 20 | $7.02 (computed) | 11.1 | 5% | 2% | **49%** | 6% | 35% | 4% |

Three readings, each limited as stated:

1. **The saving works through the prefix-read term.** The difference in cache-read cost equals 104% (MiniMax) and 129% (GLM) of the all-vs-subset bill gap (about 90% for GLM per task once its step-capped runs are removed); higher output in the subset arms offsets 7% and 26%. Caution: this is close to an accounting identity, because the all-tools bill is 73-80% cache reads. The subset arm also differs in the predictor call, step counts, output length (GLM writes 68% more output per request) and accuracy. It shows where the saving appears, not that nothing else changed.
2. **After the tool block shrinks, output and history take over, and runaway runs dominate the tail.** With the step-capped runs removed (2 of 57 MiniMax and 7 of 57 GLM subset tasks), output is the largest item of the subset bill, 39% (MiniMax) and 50% (GLM); history reads plus fresh history are 40% and 22%, the predictor 5% and 13%. With all tasks, GLM's history reads are 49% of its bill, but those 7 runaway runs are 75% of that arm's bill (section 9.6). The fixed prefix is only 29% and 9% of agent prompt tokens, against 89% and 82% in the all-tools arms. This is the part of the supervisor's concern that V5-R does not yet address.
3. **"Prefix reads dominate" is not general.** On OpenAI (P2, 128 tools, about 19.5k-token prompts) the all-tools arm's bill is 25-33% cache read, 30-41% fresh input and 34-38% output. Dropping unneeded tools cut the prompt per call from 19.5k to 8.5-11k tokens but the bill only 10-20%, because the cache-hit rate fell (about 90% to 74%) and output stayed. The repo never claimed a saving for the `enf` arm (subset enforced at a fixed prefix); it cost x1.02 and x1.15 as designed.

### 2.3 What a step looks like in these runs

- **Parallel tool calls are already in use.** 23-57% of requests that call tools carry two or more calls (MiniMax all 57%, MiniMax subset 51%, GLM all 26%, GLM subset 23%), averaging 2.4-4.3 calls per tool-calling request, with up to 48-62 calls in one request. The R3 runs set `parallel_tool_calls` true.
- **Median growth per step is 0.65-1.3k tokens** (90th percentile 3.8-8.0k); 40-54% of steps add more than 1k tokens. Growth includes the assistant's own call arguments.
- **Requests per task:** median 10-11, 90th percentile 13-18 (50 where a step cap was hit). The repo's break-even tables assume 10; that matches.

### 2.4 AppWorld has a code-writing agent we never used

AppWorld ships `simplified_react_code_agent` and `simplified_full_code_agent` next to the `simplified_function_calling_agent` we ran. The code ReAct agent works in a persistent Python REPL, learns APIs on demand through `apis.api_docs`, and has no tool-definition block at all; its own code sets a cache breakpoint at the last message. The AppWorld paper (2407.18901) reports for GPT-4o on the normal test set: ReAct (code) TGC 48.8, plan-then-execute 44.6, full-code 33.9, iterative parallel function calling 32.1. Per-example cost was about $0.70, $1.33, $0.02 and $0.33, at June 2024 prices and without caching. For GPT-4 Turbo the function-calling baseline scored higher (30.4 against 26.8). The evidence is old, one benchmark and prompt-based models, so it does not say which design wins today. It does show that the benchmark's own design avoids the exposed-tool-list problem by construction, which is exactly the kind of rival a reader of the thesis will ask about.

### 2.5 Analyses I computed and chose not to rely on

- **A "perfect batching" saving of 46-60% of the bill.** Dropped. The proxy (a step whose arguments use no value first seen in the previous step) swings from 29% to 93% under reasonable detector choices, mislabels pagination loops and final `complete_task` calls, and has no ground truth.
- **A bound on history clearing (re-reads of history older than 5 steps: 2%, 10%, 9%, 36% of the bill).** Not a saving. Clearing a result rewrites every later cached token at the fresh price; with a crude penalty, clearing every step becomes a net loss. Only batched clearing could pay, which is what the repo's `clear_at_least` rule is for.
- **Scaling slopes of cost against requests.** Dropped. They follow mechanically from the prefix share, the request count is endogenous, and the confidence intervals are wide.

## 3. What this means for the thesis

| Existing claim, assumption or plan | Effect | Why |
| --- | --- | --- |
| Objective is the bill, per request, with cache reads priced (DPR-0006) | **Strengthened** | The supervisor's concern is the cache-read term; the equation already has it, and tokens alone would have hidden it (4.4x tokens, 2.6x bill). |
| Never edit the tools array in a session; append only (V5-R02) | **Unaffected** | It is the same cache logic the supervisor described; Anthropic's docs list tool-definition changes as invalidating the whole cache. |
| A predicted subset of at most 20 tools cuts the bill 2.2-2.6x (MiniMax) and about 1.5x (GLM, computed; 4.1x as a ratio of mean per-task bills without its seven step-capped runs, which are 75% of the subset bill) | **Unaffected as a measurement, narrower as a claim** | It holds for a 469-tool prefix, warm back-to-back caching, one benchmark, two open-weight models, single runs. The saving appears as the prefix-read term; the arms also differ in predictor, steps and output. |
| "Cache reads shrink the gap" and "the prefix carries the bill" as general statements | **Weakened** | OpenAI P2 at 128 tools: reads are 25-33% of the bill; fresh input and output are as large. Cache price, prefix size and hit rate decide. |
| D-01 break-even (tool block only, warm cache) | **Unaffected** | It compares layouts; the subset arms show history is 22-40% of the bill for typical tasks (more where runs hit the step cap), so D-01 gives a difference, not a total. State that. |
| The tasks run back to back, so the 469-tool prefix stayed warm (96.8-99% cached) | **New caveat** | After a gap beyond the cache lifetime the first request re-pays the prefix at the fresh or write price, so the 66% is a warm-cache figure. |
| GLM bills are computed from list prices on a free server | **Unchanged caveat, now sharper** | Timed-out requests (75 in the GLM subset arm and 2 in the all-tools arm, per the results deck) are not in the usage logs, so not in the computed bills; if a provider charged for them the bills are low. |
| Memory-informed offering (P1) | **Unaffected** | Its saving, if any, runs through the same prefix-read term; nothing here tests it. |
| P4 (clear old tool results) "not needed yet" | **Reframed, not triggered** | History re-reads are the main remaining input cost in the subset arms, but the trigger ("deployments with large tool results") has no number, and naive per-step clearing loses money. Define the trigger first. |
| The comparison set (all tools, subset, deferral, search and stop rules) | **Incomplete** | No code-agent arm and no analysis of the number of requests. Whether that matters depends on how the thesis question is read (see next steps). |

**Net:** V5-R's rules do not need to change on this evidence, and the evidence does not show V5-R beats the alternatives that remove the tool block in other ways. Both statements hold at once.

## 4. What remains uncertain

| Open point | Why it matters | Can it be resolved? |
| --- | --- | --- |
| How Anthropic bills a PTC resume request (full history and tools array re-sent) | If each resume is billed as a prefix read, PTC does not remove the term that tool exposure shrinks, and the two mechanisms add rather than substitute | Yes, one small paid test with an Anthropic key; docs are silent |
| Whether Anthropic's -38%, +8% and 20-40% PTC figures include caching, and are tokens or dollars | They are the only numbers behind "PTC saves money" | No: vendor-internal, benchmark unnamed |
| What the supervisor means by "solved" | Decides whether call-reduction is in scope | Yes, one question to him |
| How much of the sequential steps a model could merge without seeing results | Sets any ceiling for batching or PTC on AppWorld | Not from these traces; needs a code-agent or PTC-style run |
| Whether the cost anatomy holds on other models, tasks and cold caches | External validity | Partly: P2b and the end-to-end study will add cells |
| Whether any API passes KV-retention savings into price | Would change the economics of re-reads | I found none; absence in a limited search |
| Independent replication of the vendor tool-search numbers (85% fewer definition tokens; 49% to 74% accuracy) | Relevant to the deferral regime | I found none |

## 5. What should happen next

*Revised after the second literature pass: see section 8, which supersedes the rows below where they differ (P4, the code-agent arm, evaluation reporting).*

| # | Action | Evidence behind it | Alternative and trade-off | Authority |
| --- | --- | --- | --- | --- |
| 1 | Ask the supervisor what "solved" means and whether call-reduction is in scope; send him the cost-anatomy table (2.2) and the corrected premise (2.1) | His premise is right about re-sends and wrong about waiting; the shared chat agrees. Scope was set at REQ-O21-01 | Skip and proceed: risks a mismatch on what the thesis must compare | You |
| 2 | Record this analysis in the repo: a cost-anatomy note, the P2 decomposition, and corrections to the reuse map (PTC resume billing unknown; Haiku 5.5 listed; code agents; parallel calls; WebSocket and `previous_response_id` change latency, not billing) | Sections 1-2; this session could not write under `.claude/` and did not write to the repo | Keep it outside the repo: the evidence trail stays incomplete | You, then the lead |
| 3 | Add to every savings claim its conditions: warm back-to-back cache, cache-read price ratio (0.19-0.2 here), prefix size, computed GLM bill, unbilled timeouts. Add a price-ratio sensitivity of the all-vs-subset ratio computed from the stored totals (arithmetic, no run) | Sections 2.2 and 3; the repo already has a 47-endpoint spread (1.08-1.80) for GLM | None needed; this is bookkeeping | Lead |
| 4 | Give P4 a numeric trigger (for example, the share of the bill in history re-reads) before deciding to run it; if it runs, use batched clearing with the rewrite cost counted | History is 22-40% of typical-task subset bills (49% of GLM's with its runaway runs); per-step clearing loses money under a crude penalty (2.5) | Drop P4: the largest remaining input cost stays unaddressed | You |
| 5 | **Code-agent arm.** Option A: do not run; state it as a limit of the comparison. Option B: run AppWorld's `simplified_react_code_agent` on the same 57 dev tasks, same models and hosts, one or two runs per model, and report bill and accuracy beside V5-R | AppWorld's own agents have no tool block; the paper shows code ReAct beating function calling for GPT-4o and the reverse for GPT-4 Turbo. No such arm exists in the record | A is free but leaves "most optimal method" open. B is a comparison, not part of the policy; I estimate its cost near the existing MiniMax runs ($1.4-3.0 each) but have not priced it \[S\]. If B is wanted it is cheaper to add before the end-to-end design is frozen | You, after item 1 |
| 6 | Only if Anthropic PTC becomes in scope: one small paid test of how a resume request is billed. Pad the tools array to about 20k tokens, make five programmatic calls, read `usage` on each request | The docs require full history and the same tools array on resume and do not state the billing | Do not test: report PTC as an unknown, vendor-measured option | You (Anthropic key and spend) |
| 7 | Run nothing for parallel calls, plan-first, or KV retention | Parallel calls are already used (23-57% of requests); the others are provider-side or unproven on current models; no hypothesis here is open that such a run would close | Revisit after the supervisor's answer | none |

**What I would not change now:** the policy rules, the bill equation, the headline average, the planned P1 and end-to-end items. **What I would not conclude:** a deployment saving percentage; a saving from batching or history clearing; that prefix reads dominate on every provider; that the supervisor is wrong or right (his premise holds; his conclusion that the problem is solved does not follow from the sources I could open).

## 6. How this was checked

- **Three separate efforts.** (a) A literature investigator ran with no access to the repo and wrote tagged findings; I spot-checked its PTC quotes and the AppWorld table against the raw saved pages, and the Claude Code, OpenAI and arXiv claims against primary pages. (b) I analysed the raw per-request traces. (c) A second agent, given my claims but not my scripts, re-derived them from the raw files and tried to refute them.
- **What the replication changed.** It found a real error: in the subset arms the first request of each task is the predictor call, so my first split of those arms used the wrong prefix. It is corrected in 2.2 (the earlier numbers said prefix 42% and 15% of tokens; the right ones are 29% and 9%). It also showed that the 104% and 129% figures are close to an accounting identity, and that my batching proxy, history-clearing bound and scaling slopes could not support claims. I removed those from the conclusions.
- **What stayed.** Totals reproduce to the cent in two independent computations; the all-tools splits (66/6/7/6/14 and 66/1/14/3/16) were confirmed; front-fill, pro-rata and back-fill allocation give the same prefix-read share for the all-tools arms.
- **Refinements to my first message in this session.** I now say the prefix-read share is specific to the 469-tool open-weight runs (I had called P2 "consistent with" the same effect without decomposing it), and I add the warm-cache and unbilled-timeout caveats. The shared chat, which I could not read before, rejects the "model waits" premise itself.
- **Reproducing.** Scripts, both sub-reports and a README are in `~/Documents/react-resend-investigation/` (outside the repo). Core step: per request, fresh = prompt - cached at the input price, cached at the cache-read price, completion at the output price; the cached tokens fill the first-request prefix before history. Data stay in `~/r3-work/runs/` (git-excluded). The `.env` there was never read.

## Sources

Opened and read in full or in the passages quoted:

- [Claude Code: manage costs](https://code.claude.com/docs/en/costs)
- [Anthropic: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic: programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [OpenAI: conversation state](https://developers.openai.com/api/docs/guides/conversation-state) and [WebSocket mode](https://developers.openai.com/api/docs/guides/websocket-mode)
- [AppWorld, arXiv 2407.18901](https://arxiv.org/abs/2407.18901)
- [Bai et al., arXiv 2604.22750](https://arxiv.org/abs/2604.22750); [Token Reduction Is Not Cost Reduction, arXiv 2607.12161](https://arxiv.org/abs/2607.12161); [Don't Break the Cache, arXiv 2601.06007](https://arxiv.org/abs/2601.06007)
- [InferCept, arXiv 2402.01869](https://arxiv.org/abs/2402.01869); [Continuum, arXiv 2511.02230](https://arxiv.org/abs/2511.02230); [AsyncLM, arXiv 2412.07017](https://arxiv.org/abs/2412.07017); [ReWOO, arXiv 2305.18323](https://arxiv.org/abs/2305.18323)

Taken from the literature investigator's report and not re-opened by me: Anthropic's web-search dynamic-filtering post and the Pydantic AI, Cloudflare Code Mode and arXiv 2609.11999 / 2608.06370 / 2602.15945 summaries (abstract level only); OpenRouter's public model catalogue prices (cache-read 0.2x on minimax-m3 and glm-5, 0.083x on deepseek-v4-pro, 0.05x on Sonnet 5.5).

Repository references are `v5-audit` paths as named in each row; the checked-out branch is older, so they were read with `git show v5-audit:<path>`. The two presentations the supervisor received are the sources for what had been communicated.

## 7. Second pass: the wider research landscape

### 7.1 How the search was done

The first assessment drew on one investigator and the repo's stored literature. This pass reopened the search from first principles, one researcher per community, each with its own vocabulary, a mandatory query log, a source log with read depth and an evidence grade, and a list of what was excluded and why. A separate critic then read all logs and searched for omissions and for evidence against the working conclusion.

| Lane | Community and vocabulary | Queries logged | Sources logged | Excluded |
| --- | --- | --- | --- | --- |
| L1 | Inference serving, KV-cache and agent workload traces | 24 | 25 | 6 |
| L2 | Cost accounting, evaluation statistics, run-to-run variance | 34 | 23 | 7 |
| L3 | Tool retrieval, tool overload, MCP and tool search | 22 | 27 | 7 |
| L4 | Code-as-action, programmatic calling, planning, batching | 21 | 27 | 8 |
| L5 | Context management, compaction, masking, agent memory | 16 | 26 | 4 |
| L6 | Provider pricing, caching rules, practitioner postmortems | 29 | 33 | 5 |
| L7 | AppWorld and comparable benchmarks | 20 | 28 | 5 |
| Critic | Omissions and contrary evidence, adjacent fields | 18 | 11 | 0 |

The logs hold 184 queries and about 200 source rows (some sources recur across lanes). Grades: **E** peer-reviewed or replicated with code, **M** measured by its authors, **V** vendor claim, **T** proposal without measurement, **DOC** a documented provider behaviour, **U** unverified. Most 2026 sources are unreviewed preprints, several only weeks old, and many were read at abstract level.

**Quality assurance.** The lanes returned their findings through a summarising reader, so I did not accept them. I opened the primary source for 18 decision-relevant claims. Fourteen held (some with caveats or relabelling), two held only in part (TokenPilot and Physical Cost of Context), and two failed: ToolChoiceConfusion's "state-aware filter 0.99" is the authors' own method (the state-aware baseline scores 0.65 against 0.83 for all tools) and one cache-hit claim was cited to an unrelated paper (arXiv 2609.26891), which I discarded. The run-variance paper is an arXiv preprint, not an ICLR paper as a lane labelled it. A lane's rule that "calls fall faster than cost" is true for Claude 4.5 on AppWorld (calls -7.6%, cost -4.2%) but not for GPT-5.1 (calls -11.9%, cost -15.0%).

### 7.2 What the wider literature establishes

| # | Finding | Grade | Meaning for this thesis |
| --- | --- | --- | --- |
| 1 | Re-sent prefix is the normal cost shape of agent traffic. TraceLab (4,265 Claude Code and Codex sessions): 95.7% of input tokens were prefix, 59.5% of list-price cost. Bai et al.: cache reads dominate dollars in every phase of a Sonnet 4.5 case study. The Claude Code study (2607.12161): harness base 74.7% of cost (one merged system-prompt-plus-tool-definitions row, cache attribution inferred) | M | Confirms the supervisor's premise and that our 66% is typical for a large fixed prefix |
| 2 | But the share depends on prices and mix. Quesma (1,740 attempts): cache reads were 94-98% of input tokens but 26-30% of the bill, and output was about 56% of cost on DeepSeek's cheap reads. A tool's own "tokens saved" counter said 89% while cost rose 5-17% | M | Do not pool the 66% across routes; always report the token-class split with the price schedule |
| 3 | Nothing found removes the re-read charge. Serving research (InferCept, Continuum, KVFlow, Mooncake) improves latency, throughput and GPU use, not customer price. OpenAI `previous_response_id` bills all prior input; WebSocket mode is a latency claim; Batch and Flex halve input and cached input alike. No flat session pricing found | M, DOC | "Solved" holds for latency. For the bill the lever is r, the cache-read price ratio. Vendor mechanisms that reshape what is re-read (tool search, context editing) exist but have no cache-priced evidence |
| 4 | r varies about 40-fold: 0.025x (Fable 5.1), 0.05x (Opus and Sonnet 5.5), 0.1x (most Anthropic, OpenAI), and 0.10 to about 1.0 across 45 GLM-5.3 endpoints on OpenRouter (mode 0.186). Cache writes cost 1.25x to 2.5x on newer OpenAI and Anthropic models, nothing on our routes | DOC | Exposure control pays most where r is high and prefixes are large, least at r = 0.025-0.05: on the stored MiniMax token totals, with the token mix held fixed, the all-tools to subset bill ratio is 1.16 at r=0.025, 1.36 at 0.05, 1.70 at 0.1, 2.19 at 0.2 and 3.5 at r=1. Supports a model-agnostic bill equation |
| 5 | Real sessions span many user requests. Copilot: 761M LLM calls, KV hit rate about 90% within a turn and 55% across turn boundaries. TraceLab: about 84 steps per session but about 8 per user request; hits fall after gaps over 5 minutes and almost all miss after 1 hour | M | Our split comes from single 10-13-request tasks, comparable to one TraceLab user request; cache decay and history growth across a long session are not represented. In Copilot's traces the system prompt is 14% of input tokens, history 48% and function-call messages 28% (tool definitions are not broken out). State this regime |
| 6 | Whether clearing old tool results pays depends on trajectory length. On 30-40-turn SWE-bench runs, random short-delay deletion was never cheaper under an assumed 1:0.1:5 cache model (0 of 42 setups; 26 significantly dearer; one self-hosted model, costs estimated from token logs, cache-write premiums ignored), and keeping the last five observations raised uncached prefill by 608% on one stack (tokens and GPU time, not dollars; quality result inconclusive). Rolling masking with a 10-turn window halved cost on SWE-agent runs averaging 44-50 turns (cap 250), including API-billed Gemini. Threshold-triggered and bounded-suffix methods report 21-87% savings: single runs, no statistics, cache accounting unclear | M | A first-order model of mine (not a paper's) gives a cumulative break-even of about M(2-c)/c turns for window M and cache-read ratio c: roughly 85-190 turns for M=10 at c=0.2-0.1, about 26 turns at a 55% hit rate. It does not reproduce Complexity Trap's halving at 44-50 turns (imperfect caching or a heavy tail of long runs may explain it; untested). For windows of 5 or more it predicts no payback within 13 turns at c of 0.1 or higher; a window of 2 could break even near turn 11 at c=0.2 before re-fetching, longer runs, accuracy and write fees, which drove the measured losses. Weak or absent caching changes the answer |
| 7 | A missing needed tool can be fatal; whether it raises or lowers the bill depends on how the agent behaves. One single-author preprint (345 AppWorld queries; official code agent with DeepSeek-V3.2; tools outside the set hidden): untrained structures making at most one LLM call complete at most 10% of queries at k=16 (a trained retriever .33, an LLM-heavy hierarchy .30); in a 60-task check, tasks with a complete set passed 21 of 21 and with an incomplete set 2 of 39, but gold-API exposure passed 26 of the same 39, complete-set tasks are easier, there was no all-tools arm. The retriever's 16-API exposure used twice the prompt tokens of gold-only exposure (15.1M vs 7.4M) and 32 vs 19 median steps, a contrast of exposures, not of complete against incomplete sets. AppWorld's own paper (GPT-4o) found predicted sets within 0.9-2.4 points of oracle sets for function calling, but code-style agents gained 5-10 points from oracle sets. On a synthetic benchmark non-oracle subsets lost 11-22 points, mostly on two weaker models. LiveMCPBench: retrieval errors were half of the failures of two Claude models. LongFuncEval's 7-85% drop is mostly for small models | M | The damaging case is omitting a function the agent needs (GLM-5.3 passed 0 of 22 tasks missing the credentials function) rather than incompleteness as such (MiniMax-M3 passed 13 of 19 incomplete sets). The 2-of-39 and 13-of-19 figures differ in agent, model and definition and are not reconciled. The bill effect differs by model in our stored records: MiniMax-M3 incomplete sets looked 5x dearer on average (504k against 105k prompt tokens), but all three step-capped runs were incomplete-set tasks and without them the groups match (8.4 turns each; 86k against 105k tokens); DeepSeek-V4.1-Flash shows no difference (23 of 27 against 25 of 30 passed); GLM-5.3 tasks missing the credentials function used 192k against 741k because the agent gave up early |
| 8 | Independent evidence supports the direction, none of it cache-priced. TheMCPCompany (175 tasks): oracle tool sets cost 2-35% less than retrieval and 44-70% less than browsing across six models, and retrieval trails the oracle by 2-16 points depending on the model; oracle runs took fewer steps for five of six models (4-24%) and more for Opus 4.1 (+5%), so definition size is not isolated. Exgentic: shortlisting changed AppWorld success by +22, +5, +3, +1, -5 points (one run per cell, all but the GPT-5.2 tool-cap case inside one confidence half-width; it adds one LLM call per turn); its six-benchmark average cost per task, not cache-priced, fell for Opus 4.5 ($5.75 to $3.78) and rose for GPT-5.2 ($0.17 to $0.26). Vanta (production): cost per run -48%, completion +5% relative, cache hit rate fell, no controls stated | M, V | Direction plausible; magnitude open. Vanta also shows hit rate is the wrong objective, the bill is |
| 9 | Code-action and call-reduction are model-dependent. Exgentic (AppWorld, 100 tasks, one run): code agent 0.70 with Opus 4.5 but 0.13 with Gemini 3; open-weight models at most 0.13 (undiagnosed, in a harness whose AppWorld protocol the paper describes inconsistently; another study's official code agent with DeepSeek-V3.2 passed 46 of 60 tasks given gold APIs); architecture shifts results up to 12 points within a model. AppWorld-UL: code beat function calling in most of its model pairs on a user-interaction metric (single runs; its function-calling agent used a predicted subset while the code agent read docs on demand, so it is not like for like). AWO meta-tools on AppWorld: calls -7.6% to -11.9%, cost -4% to -15% (five login bundles mined from the test tasks themselves, one run; it adds tools rather than removing them). Programmatic calling resends the tools array on resume | M, V | Complement, not substitute. A code-agent arm is a legitimate comparator whose outcome cannot be predicted |
| 10 | Evaluation noise is large. Over 10 runs of SWE-Bench Verified (500 tasks, 3 models, 2 scaffolds) the run-to-run SD of the pass rate was 0.7-1.8 points, also at temperature 0, with a min-to-max range of 2.2-6.0; the authors' power calculation needs about 9 runs per arm for a 2-point difference. Scaled to 57 tasks, our identical-run disagreements imply a single-arm SD of 3-4 points (4-6 for a paired difference of single runs). Clustered tasks inflate standard errors; token-based and dollar-based rankings can differ; reasoning effort acts as a hidden treatment; backend and provider shift scores | M | Supports estimation-only reporting. In my simulation (assumed variance split) a paired, cluster-aware 95% interval at 57 tasks and 2 runs per arm is about ±5.5 to ±8 points depending on how many tasks flip between identical runs (6 to 12), slightly wider with only 19 clusters, so it can exclude only losses beyond roughly 6-12 points; cost ratios are measurable |
| 11 | Vendors document both exposure routes as cache-preserving, and one new variant. Anthropic beta `tool_addition` and `tool_removal` change what is offered while the `tools` array stays fixed, so the cache holds (Claude models only). OpenAI documents `allowed_tools` as a way to keep cache savings | DOC | Confirms V5-R02. Append-only is the portable rule for open-weight routes; the tools array still carries every definition, so these protect the cache, they do not shrink the fixed block |

### 7.3 What I looked for and did not find

Not found in the places searched: any study that splits a cache-priced bill into tool-definition prefix, history and output while varying tool exposure (our split would be new measurement, not replication); a controlled all-tools against subset comparison on a 400+-tool stateful benchmark reporting pass rate and cost together; independent replication of vendors' tool-search accuracy claims; a billing statement for programmatic-calling resume requests; hit-rate data for MiniMax-M3 or GLM-5.3 on hosted endpoints; a modern independent re-evaluation of ReWOO or LLMCompiler; any source arguing that bill-per-successful-task is the wrong objective. Absence in a bounded search is not proof of absence.

### 7.4 Alternative readings I considered

- **"Caching makes exposure control moot."** Rejected for our routes (66% of the all-tools bill is prefix reads at r about 0.2). Plausible where r is 0.025-0.05, sessions are long, or the catalogue is small: on OpenAI at 128 tools reads were 25-33% of the bill.
- **"The bill is the wrong objective."** Nothing found supports this. One practitioner source notes model rankings reverse as prices change, which supports keeping price parameters explicit.
- **Cheaper ways to shrink the fixed prefix without changing exposure:** schema compression (TSCG, single author, claims 52-57% fewer schema tokens; Atlassian's compressor, vendor, 17.6k to 0.5k tokens on a 94-tool server) and engine-level KV sharing of tool schemas (ReCache, 3.7x faster time to first token, needs attention-level control, so unavailable on hosted APIs). I have not verified the first two. They are an unexplored comparator, not evidence against the policy.
- **Our all-tools prefix was warm only because tasks ran back to back.** After a gap beyond the cache lifetime its first request pays the full price, so the measured saving is conservative for the cold case.

## 8. Revised assessment and recommendations

### 8.1 What changed, what did not

| Item | After the second pass |
| --- | --- |
| The supervisor's premise (every tool call re-sends the prefix) | **Confirmed, and quantified by independent traces.** The "model waits" idea has no support; the nearest mechanisms are engine-side and unavailable to a customer |
| "Already solved" | **Holds for latency, not for the bill.** The bill falls to r times the prefix; r is 0.025-1.0 by route |
| V5-R rules (append-only, regime switch, deployment filter) | **Unchanged.** Vendors document the same cache rules; Anthropic's new mid-conversation tool changes are a provider-specific alternative |
| Measured saving from the predicted subset | **Unchanged as a measurement; scope narrowed further.** Single 10-13-request tasks, big catalogue, warm cache, open-weight routes. Multi-request sessions with gaps are not represented |
| P4 (clear old tool results) | **Revised.** Whether per-step clearing pays depends on window, trajectory length and cache behaviour; by a first-order model it does not pay within 10-13 requests for windows of 5 or more at cache-read ratios of 0.1 or higher. Any revival should be defined by trajectory length and the route's cache behaviour |
| Subset predictor | **Elevated.** Omitting a needed function is the main accuracy risk; the effect on the bill depends on agent behaviour (in our records: no typical-task difference for MiniMax-M3 or DeepSeek-V4.1-Flash, early give-up for GLM-5.3, and runaway step-capped loops in 3 of 19 MiniMax incomplete-set tasks); the predictor is itself a cost (4% of the subset bills) |
| Code-agent arm | **Revised to a pilot first.** Published comparisons are not like for like and are model- and harness-dependent; the open-weight 'floor' in one study is a harness result |
| Evaluation plan | **Strengthened.** Estimation-only reporting is forced by the current sample size and the measured run noise |

### 8.2 Recommendations (supersede section 5 where they differ)

| # | Action | Evidence | Alternative and consequence | Authority |
| --- | --- | --- | --- | --- |
| 1 | Ask the supervisor what "solved" means and whether call-reduction is in scope; show him the cost split and the independent traces | Sections 2.2 and 7.2 (rows 1-3) | Skip: risk a mismatch on what the thesis must compare | You |
| 2 | Record the cost analysis and this second-pass ledger in the repo; add the regime statement (single 10-13-request tasks, about one user request; multi-request sessions average about 84 steps) to every savings claim | Rows 2, 4, 5 | Keep outside the repo: the evidence trail stays incomplete | You, then the lead |
| 3 | Report predictor completeness (share of tasks with every required API offered, per model) and the predictor's own cost as first-class results; keep the supervisor functions (profile, credentials) always offered outside the cap, as the AppWorld retrieval study does. This is free: the stored R2 and R3 records contain the data | Row 7; MiniMax 38 of 57 complete, GLM 22 tasks missing the credentials function, all failed | None needed | Lead |
| 4 | Do not run per-step clearing at 10-13 requests on routes with cache-read ratios of 0.2 or less; revisit it where caching is weak or absent. If P4 is revived, define it by trajectory length and test ingestion-time truncation or offload, or batched clearing, priced with cache-write cost | Row 6: loss at 30-40 turns, gain at 44-250 turns, plus my break-even model; the positive batched results are unreplicated single runs on other benchmarks | Drop P4: leaves history re-reads (22-40% of typical-task subset bills) unaddressed | You |
| 5 | **Code-agent arm as a pilot:** AppWorld's native react code agent, 5-10 dev tasks, one model, same billing equation. Expand only if the pilot returns usable accuracy | Row 9: results are model- and harness-dependent, and one study's open-weight collapse is undiagnosed (another study ran the official code agent with DeepSeek-V3.2 successfully); no cache-priced comparison exists. My cost guess is small but unpriced \[S\] | Option A: no arm; state it as a limit. Full arm now: spends before knowing the models can drive the agent | You, after item 1 |
| 6 | Evaluation hygiene with no new run: log first-request cached tokens per task; report the warm (back-to-back) and a cold-start case computed from the stored first-request sizes; keep concurrency and task order fixed; keep estimation-only reporting with paired, cluster-aware intervals | Row 10; warm-prefix confound in section 7.4 | None; this is arithmetic and bookkeeping | Lead |
| 7 | Programmatic-calling resume billing test only if Anthropic programmatic calling becomes in scope | Still undocumented after the wider search | Report it as an unknown vendor option | You (key and spend) |
| 8 | Optional, low priority: schema compression as a comparator that keeps the tool set and the prefix stable | Row 7.4 bullet 3; evidence is single-author or vendor and unverified by me | Ignore until the supervisor's scope is known | You |

**Unchanged from before:** no new experiment is justified to answer the supervisor's concern itself; the policy, the bill equation and the headline average stay as they are.

### 8.3 Remaining uncertainty after the second pass

| Open point | Can it be resolved? |
| --- | --- |
| Billing of programmatic-calling resume requests | Yes, one small paid test; docs silent |
| Whether the cost split holds on long sessions, other models and cold caches | Partly, from P2b, the end-to-end study and a cold-start computation |
| Whether a code agent on MiniMax or GLM can use AppWorld at all in the official harness | Yes, with the pilot |
| Magnitude of tool-exposure savings under cache-priced billing outside our runs | Only by new measurement; nobody has published it |
| Reliability of the 2026 preprints (unreviewed, mostly abstract-level reads) | Re-read the full text before citing any number in the thesis |
| Independent replication of vendor tool-search accuracy claims | Not resolvable from here |

### 8.4 Search coverage: my judgement

Coverage is reasonable for the question asked: seven communities, an independent omission search, and my own checks of 18 claims. I cannot show it is complete. The critic found omissions the lanes missed (the AppWorld retrieval-completeness paper, KV-level schema reuse, schema compression), which is why I reread the completeness paper and ran our own records against it. The residual risk is in unread full texts and in 2026 preprints that may change. If a decision depends on one number from section 7.2, open the source first.

## Additional sources (second pass)

Opened by me, abstract or full text as noted in the verification ledger: [Mid-conversation tool changes (Anthropic)](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages); [On Randomness in Agentic Evals, 2602.07150](https://arxiv.org/abs/2602.07150); [Quesma: does RTK make AI coding cheaper](https://quesma.com/blog/does-rtk-make-ai-coding-cheaper/); [Vanta: the cache miss that made our agent faster](https://www.vanta.com/resources/the-cache-miss-that-made-our-agent-faster); [Agentic Coding in the Wild (Copilot traces), 2608.00101](https://arxiv.org/abs/2608.00101); [Hidden Costs of Forgetting, 2610.35496](https://arxiv.org/abs/2610.35496); [General Agent Evaluation (Exgentic), 2602.22953](https://arxiv.org/abs/2602.22953); [Optimizing Agentic Workflows using Meta-tools, 2601.22037](https://arxiv.org/abs/2601.22037); [ToolChoiceConfusion, 2606.06284](https://arxiv.org/abs/2606.06284); [TraceLab, 2606.30560](https://arxiv.org/abs/2606.30560); [TheMCPCompany, 2510.19286](https://arxiv.org/abs/2510.19286); [TokenPilot, 2606.17016](https://arxiv.org/abs/2606.17016); [The Physical Cost of Context, 2610.34763](https://arxiv.org/abs/2610.34763); [Completeness and Cost of Retrieval Structures, 2610.41905](https://arxiv.org/abs/2610.41905); [LongFuncEval, 2505.10570](https://arxiv.org/abs/2505.10570); [ReCache, 2608.19662](https://arxiv.org/abs/2608.19662).

Full query, source and exclusion logs for all eight researchers, their reports, and my verification ledger are in `~/Documents/react-resend-investigation/literature-pass2/` (outside the repo). Sources I did not open myself are marked as lane-reported in the ledgers and are not relied on for any number in this document.

## 9. Third pass: full-text verification

The second pass left many sources read at abstract level or through summarising readers. This pass downloaded the full PDFs (with appendices) of 31 sources and tested the assessment's wording against the text. Four independent readers each took a theme and had to find overstatements in my wording and evidence inside the papers that cuts against how they are cited. I read eight of the most consequential papers myself (Hidden Costs, Physical Cost of Context, Complexity Trap, the AppWorld retrieval-completeness study, Exgentic, the Claude Code cost study, TraceLab, the Copilot traces) and resolved disagreements against the text. The per-paper ledger is `FULLTEXT_VERIFICATION_LEDGER.tsv` in the supporting-files folder (outside the repo).

### 9.1 Conclusions that changed

| # | What the assessment said | What the full text shows | Effect |
| --- | --- | --- | --- |
| 1 | Per-step context clearing loses money once cache pricing applies | Only on 30-40-turn runs. Complexity Trap's rolling 10-turn masking halved cost on 44-50-turn runs (cap 250), also on API-billed Gemini. Two other studies lost on shorter runs | **Rewritten** as dependent on trajectory length and cache behaviour. The P4 trigger is not met at 10-13 requests on routes with cache-read ratios of 0.2 or less |
| 2 | Hidden Costs: "cheaper in 26 of 42 setups under flat pricing" | Those are mostly point estimates (6 significant). Deletion was random, on one self-hosted model, with cost estimated from token logs at an assumed 1:0.1:5 ratio, every matching prefix assumed cached, cache-write premiums ignored. Batched deletion was not tested, and the authors decline to infer that it would pay | **Qualified**: mechanism robust, magnitudes model-specific |
| 3 | Physical Cost: masking pays only below a 0.55 cache hit rate | 0.55 scales the observed hit tokens in a first-order formula; it is not a hit-rate threshold. The +608% is one stack, one request at a time, one trajectory per task, in tokens and GPU time. The 26-vs-29 quality result fails a non-inferiority gate but is inconclusive | **Corrected** |
| 4 | Only batched or ingestion-time methods have positive evidence | Rolling masking also has positive evidence (Complexity Trap). The batched evidence is weak: TokenPilot's saving comes mostly from prefix stabilisation, with single runs and no statistics; AgentDiet has no statistics and undocumented cache accounting | **Corrected** |
| 5 | Subset completeness decides accuracy (21 of 21 against 2 of 39) | The agent was the official **code** agent with DeepSeek-V3.2, tools outside the set hidden, 60 random test tasks, one run, no all-tools arm. Gold exposure passed 26 of the same 39 incomplete tasks and complete-set tasks are easier. The doubled prompt tokens (15.1M against 7.4M) and 32-against-19 median steps compare the retriever's 16-API exposure with gold-only exposure, not complete with incomplete sets. AppWorld's own paper found predicted sets within 0.9-2.4 points of oracle sets for GPT-4o | **Rescoped**: omitting a needed function can be fatal; the effect on the bill differs by model |
| 6 | Open-weight models score at most 0.13 on AppWorld (Exgentic) | The paper does not diagnose it, calls it a "capability ceiling", describes its AppWorld protocol inconsistently (native interpreter in section 3.1, about 468 function actions in the appendix), lists ReAct/Opus on BrowseComp+ as 0 of 100 completed beside 0.49 in the main table, and reports cost only as a six-benchmark average without caching | **Downgraded** to harness-sensitivity evidence |
| 7 | Run noise: SD above 1.5 points even at temperature 0 | SD is 0.7-1.8 points over 10 runs on 500 tasks (at temperature 0: 1.2, 1.8, 1.0, 1.5, 1.6, 1.7). The "9 runs for 2 points, 36 for 1 point" figures are the paper's own. At 57 tasks our identical-run disagreements imply a single-arm SD of 3-4 points | **Rescaled** |
| 8 | Harness base is 74.7% of cost (system prompt plus tool definitions) | It comes from a reconstructed corpus with inferred cache attribution, and the paper says the two components cannot be split. Its 5-minute cache carry-over confound is unresolved | **Qualified**: cite for structure, not as a tool-definition share |
| 9 | AppWorld-UL: code beats function calling for five model pairs | The function-calling agent used a predicted API subset while the code agent read docs on demand; the metric is a user-interaction score on a perturbed benchmark; "most" pairs, single runs | **Downgraded**: not like for like |
| 10 | AWO meta-tools cut AppWorld cost 4-15% | It adds five login bundles mined from the same 168 test tasks, one run; it is not a tool-reduction study. GPT-5.1's cost there is 74% output tokens | **Contextualised** |
| 11 | Bai et al.: runs differ up to 30x | "30x" appears only in the abstract and introduction; the body gives about 2x | **Corrected** to 2x |
| 12 | ToolChoiceConfusion: a good filter keeps 0.99 success | 0.99 is the authors' oracle-grade method, which uses gold contracts and true state. Real baseline filters lost 11-22 points; the all-tools mean of 0.83 is carried by two weaker models | **Corrected** |

### 9.2 Conclusions that survived

| Conclusion | Why it survived |
| --- | --- |
| The supervisor's premise (every tool call re-sends the prefix) is correct and the "model waits" idea has no support | Claude Code's cost page (read in full) and the OpenAI conversation-state page say so; no source read in full contradicts it |
| Nothing found removes the re-read charge on our routes | No full text claims a billing change; serving results are latency, throughput or GPU measures |
| Token reduction is not cost reduction | The Claude Code cost study and the Quesma post agree; the first is billed and paired but uses its authors' own product and cannot exclude cache carry-over |
| The share of the bill that is re-read context is route-specific | 26% (DeepSeek route, Quesma) to 59.5% (TraceLab list prices) to 66% of our all-tools bills |
| No source measures the tool-definition share of an agent bill | Reader B concluded the same; the repo's own first-request prefix is the only direct measurement. From the stored R1 token counts (about 61-64k of the 76k-token prefix are definitions) I estimate 86-94% of the fixed prefix (the R1 counts scaled to 469 APIs give 86%; subtracting the subset arm's tool-free base of about 4.7k tokens gives about 94%), so roughly 58-68% of the all-tools bill, since the fixed prefix (reads plus its fresh first request) is 67-72% of it \[derived; R1 counted the earlier 457-API data\] |
| Estimation-only reporting is forced at the current sample size | Run noise, cluster size and the interval simulation (9.3) |
| Mid-conversation tool changes and programmatic-call resumes do not shrink the fixed block | Verified in the vendor documentation: the tools array stays and is re-sent |

### 9.3 What the deeper reading added

- **The bill effect of a wrong subset is unresolved.** The one study that measured exposures (a code agent, 16-API retriever exposure against gold-only exposure) found twice the prompt tokens and 68% more steps, but that contrast is not complete against incomplete sets. In our stored records there is no consistent effect: none for DeepSeek, none at the typical MiniMax task (its 504k-against-105k mean is three step-capped runs), lower for GLM-5.3 because the agent gave up. The risk is runaway loops, which hit 3 of 19 MiniMax incomplete-set tasks and none of 38 complete ones.
- **A break-even model for clearing (mine, not a paper's).** An unmasked call re-reads all earlier observations at the cache-read price c and bills one new turn at full price. Masking with window M re-bills about M turns at full price but reads few. Per call, masking wins once the trajectory exceeds about M/c turns; cumulatively it needs about M(2-c)/c turns (checked numerically: 173 turns for M=10 at c=0.1, 84 at c=0.2, 11 for M=2 at c=0.2). With a hit rate h the effective ratio is h\*c+(1-h), which pulls the threshold to about 26 turns at a 55% hit rate. The model ignores accuracy, re-fetching, extra turns and write fees, which drove the losses in Hidden Costs. It does not reproduce Complexity Trap's halving at 44-50 turns on Gemini; imperfect caching or a heavy tail of long runs may explain it, and I have not tested either. No paper tests windows on 10-13-request tasks.
- **Evaluation power (my simulation, assumed variance split).** With 57 tasks in 19 clusters of 3 and 2 runs per arm, the paired, cluster-aware 95% interval is about ±5.5 points if identical runs disagree on 6 tasks and ±8 if on 12 (two separate simulations agree), slightly wider with only 19 clusters. A net gain of 5 passes with 9-13 flipped tasks is consistent with zero under McNemar, exact, cluster-bootstrap and sign-flip methods. A 3-point margin would need roughly 65-135 scenarios at 2 runs. Wilson or Bayesian intervals are preferred over exact Clopper-Pearson, which the source calls too conservative.
- **Composition of real sessions.** Copilot's production traces: history 48%, function-call messages 28%, system prompt 14%, other 10% of input tokens; hit rate about 90% within a turn and 55% across turns. So the tool block is a small share of input in long sessions, and our 66% should be stated as a short-task, large-catalogue regime.

### 9.4 Evidence status

| Status | Sources |
| --- | --- |
| Full text including appendices, tested against the text | 31 papers listed in the ledger |
| Page text only (summarising reader or direct fetch) | Vanta, Quesma, llm-d, OpenRouter newsletter, Pydantic article, Anthropic and OpenAI documentation |
| Not examined beyond the abstract | ReCache, TSCG, Prefix Stability, Switchcraft, Continuum and InferCept details, vendor tool-search accuracy claims |
| Not run | No authors' code was executed and nothing was replicated. Figure-only numbers (for example Bai's phase plots) could not be read from extracted text |
| Still open | How a programmatic-calling resume request is billed; independent replication of vendor tool-search accuracy; the 2/39 against 13/19 reconciliation; whether the AppWorld open-weight collapse in Exgentic is capability or harness |

### 9.5 Independent critical review of this assessment

A reviewer who had not seen my reasoning read sections 1-9, tested more than twenty claims against the full texts and the raw traces, re-simulated the power numbers and re-derived the break-even model. I verified its main objections myself before applying them. Three statements were retracted, several softened, and one of the reviewer's own sub-claims corrected.

| Review finding | Check against the source | Change made |
| --- | --- | --- |
| "Incomplete sets raise the bill" is unsupported: the 15.1M against 7.4M prompt tokens compare the retriever's 16-API exposure with gold-only exposure over all 60 tasks | Confirmed in the paper's text. In our GLM data, tasks missing the credentials function used 192k prompt tokens against 741k; in our MiniMax data the 504k-against-105k mean is three step-capped runs (without them the groups match), and DeepSeek shows no difference | **Retracted** as a general claim. Replaced with a model-dependent finding from the stored records |
| The break-even "M/c" is per call, not cumulative, and "published results fit" is false | Re-derived: cumulative threshold M(2-c)/c, checked numerically (173 turns at M=10, c=0.1). It fails to reproduce Complexity Trap's halving at 44-50 turns | **Retracted** the fit claim; recorded the formula, the hit-rate effect and the unexplained case. The reviewer's "no window of 2 or more pays within 13 turns" is also too strong: M=2 at c=0.2 breaks even near turn 11 in the idealised model |
| "Real sessions are 8x longer" compares unlike units | TraceLab: about 84 steps per session but about 8 steps per user request, so an AppWorld task resembles one request | **Retracted**; regime statement reworded |
| Tool-definition share "55-60%" is understated | Fixed prefix is 67-72% of the all-tools bill; definitions are 86-94% of it | Changed to 58-68%, labelled derived |
| Power numbers hold only at the upper end of the assumptions | Re-simulated by two readers: half-width about ±5.5 points at 6 flipped tasks, ±8 at 12 | Given as ranges; "130 scenarios" became 65-135 |
| The AppWorld paper's "within 0.9-2.4 points of oracle" is selective | Holds for function calling only; code-style agents gained 5-10 points | Both now stated |
| TheMCPCompany "4-24% fewer steps" omits Opus 4.1 | Opus took 5% more steps | Corrected |
| Exgentic dollar results omitted while saying nothing is cache-priced | Per-task averages exist, not cache-priced, mixed sign | Added with the caveat |
| "Estimation-only is the right choice" | Forced by the current sample size, not right in itself | Reworded |
| "Cache-read price makes exposure control pay least at 0.025-0.05" was unmeasured | Computed from the stored MiniMax token totals: the all-tools to subset ratio is 1.16 at r=0.025 and 2.19 at 0.2 | Added with the computation |

**Conclusions the review left standing:** the supervisor's premise is correct; nothing found removes the re-read charge on the measured routes; the lever is the cache-read ratio times the fixed prefix; once the tool block shrinks, output and history become the main costs for typical tasks and runaway runs dominate the tail; the corrections to Hidden Costs, Physical Cost, ToolChoiceConfusion and Exgentic; a pilot before a full code-agent arm.

**Not checked by the reviewer or by me:** Bai et al.'s 30x against 2x, the Quesma and Vanta pages beyond their text, the SWE-agent turn cap in Complexity Trap, and whether a heavy tail of long runs explains its Gemini result.

### 9.6 Final robustness checks on the stored runs

Read-only arithmetic on the per-request logs; no new runs. Step-capped means a run that used about the 50-step limit.

| Check | Result | Consequence |
| --- | --- | --- |
| Share of each arm's bill from step-capped runs | MiniMax all-tools: 0 runs, 0%. MiniMax subset: 2 runs, 18%. GLM all-tools: 3 runs, 25%. GLM subset: 7 runs (12% of tasks), **75%** of the bill and 88% of prompt tokens | Bill per turn is dominated by a few runaway failures in some arms. Report it with and without them, and show the capped share |
| Ratio of mean per-task bills, all-tools to subset | MiniMax 2.19 with all tasks, 2.59 with capped runs removed. GLM **1.51** with all tasks, **4.11** with capped runs removed | The GLM ratio in the results deck is mostly a runaway-loop effect. Removing failures changes the population, so show both. The mean of paired per-task ratios is far larger (3.4 for MiniMax, 10.3 for GLM) because of the heavy tails, so state which ratio is meant |
| Anatomy of a typical subset task (capped runs removed) | MiniMax: prefix 18%, history 40%, output 39%, predictor 5%. GLM: prefix 15%, history 22%, output 50%, predictor 13%. All-tools arms: prefix reads 66% (MiniMax) and 71% (GLM) | Output and reasoning is the largest single item once tools are reduced; the GLM history share of 49% was the runaway runs |
| Cold-start counterfactual: the first request of every task finds no cache (no write fee on these routes) | All-tools bills +22.7% (MiniMax) and +21.2% (GLM); subset bills +0.1% and +0.2%. Per-task ratios: MiniMax 2.19 to 2.69, GLM 1.51 to 1.82 | The warm cache was worth about a fifth of the all-tools bill. Measured ratios are conservative for cold deployments, and more so where writes carry a premium |
| Incomplete-set effect, third model | DeepSeek-V4.1-Flash: 23 of 27 incomplete-set tasks passed against 25 of 30 complete, with the same turns and prompt tokens | Accuracy and cost effects of an incomplete set are model-dependent, and absent for this model |
| Resume billing of programmatic calls, two more targeted searches | No measured usage for resume requests found in documentation, issues or posts | Unchanged: only a paid test resolves it |
| The repo's own P4 condition check (P2 logs, OpenAI, 2026-11-09) | Old tool results were 13.1% of billed input; masking could save at most 2.4-4.3% of the total before rewrite costs | Same direction as this assessment: P4's condition is not met on short tasks |

### 9.7 Completion status

Criteria I set: every number that drives a recommendation is traceable to a verified source or a reproducible computation; the document has no known internal contradiction; each consequential open question is either resolved by read-only work or needs authority I do not have; the final state has been checked after its last substantive edits.

| Criterion | Status |
| --- | --- |
| Traceability | Met. 31 full texts and the raw traces; ledgers and scripts in the supporting-files folder |
| Internal consistency | Met after two reviews, a targeted sweep of retracted wording, and a blind replication of the numbers in 9.6 (all reproduced; one wording ambiguity fixed) |
| Open questions | Four remain, none resolvable by more reading: how programmatic-call resumes are billed (needs a paid test), whether Complexity Trap's Gemini halving reflects imperfect caching or long-run tails (needs its raw data), the 2-of-39 against 13-of-19 reconciliation (needs the other study's labels), and independent replication of vendor tool-search claims |
| Diminishing returns | Reached. The last three rounds each changed a number, not a conclusion about the supervisor's concern, and the remaining uncertainty is mostly about generality, which only new runs on other models and longer sessions can address |

**What would change my conclusions:** a measured resume bill showing programmatic calls shrink the prefix charge; a cache-priced run of the code agent that beats the subset policy on bill at equal accuracy; or end-to-end results (the planned study) showing the cost anatomy differs on returning users.
