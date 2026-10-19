# 04. Follow-up: the supervisor's cache and memory points (2026-10-19)

Authorization: AUTH-010 (preparation for the 2026-10-21 meeting; the supervisor's message arrived after package v4 was committed). Author: lead (Sonnet 5.5). **Provisional addendum to `01`-`03`; it changes none of them.** The supervisor's chat messages (pasted by the student) are the supervisor's statements, not findings; the student's draft reply to them had not been answered when this was written. Source facts below come from provider documents **stored in the workspace as of their 2026-10-11 retrieval** (extracts EXT-0085..0089, 0091, 0092) and are vendor claims; prices change. Nothing here was run.

## 1. The supervisor's points against what v4 and the earlier packages hold
| Supervisor's point | Status in the repository | Verdict |
|---|---|---|
| The bill has three token kinds (input, cached, output); implicit and explicit caching exist and must enter the policy | Cache behaviour and billed cost are *recorded separately and kept out of the criterion* by the AUTH-006 working objective. The v4 criterion `C_tok` counts "input tokens as reported by the provider", which counts a cache read the same as a fresh token. Earlier packages analysed caching (DPR-0005, HYP-0007/0009, add-only rule R-cache, errata 5) | **A real gap in v4, by design choice, not a closed question.** The choice is reversible by the human. |
| Cached tokens cost about 1/10; keeping a cache costs money over time | True in part; see section 2 (the "paid for how long" part is true for Gemini explicit caches, not for Anthropic or OpenAI) | Needs the precise cost model (section 3) |
| Memory: a user who returns after hours or days must not start from nothing; matters for deployed agents | Package v1 had **F8, session working set** (reuse discovered tools across turns or sessions) and deferred it: "no session horizon fixed"; the closest vehicle has no sessions, so the regime hypothesis HYP-0001 is untestable there (DPR-0002; package A D4; package E). **v4 omits it entirely.** | **Omission in v4.** Deferred earlier for a vehicle reason, not a scientific one. |
| Combine MCP context, memory and explicit caching to find the best policy | v4 covers the first; the second and third only as recorded variables | Three interacting dimensions (section 5) |
| Human analogy: do not load everything first; context grows; explored information is kept in cache | This is the v4 design principle already (small stable prefix, append on demand, definitions stay until the task ends) | Supports the design; adds the *session* horizon |

## 2. Billing facts in the stored documents (what to say, and one correction)
- **Anthropic** (EXT-0085): 5-minute cache write 1.25x base input price; 1-hour write 2x; cache read 0.1x, **0.05x on Opus 5.5 and Sonnet 5.5, 0.025x on Fable 5.1**; a read refreshes the cache at no extra cost; "caching pays off after one cache read for the 5-minute duration ... or after two cache reads for the 1-hour duration". Automatic and explicit breakpoints both exist.
- **OpenAI** (EXT-0086..0088): on GPT-5.6 and later, cache writes cost 1.25x the uncached rate, reads 0.1x (0.05x on one model); older models have no cache-write charge; reuse refreshes the lifetime; extended retention up to 24 hours on listed models; lifetimes typically 5-10 minutes in memory, 30 minutes to 24 hours otherwise.
- **Gemini** (EXT-0089): context caching has a **storage price per million tokens per hour** ($0.50 through 2026, $1.00 from 2027 in the block read; model name outside the window), besides a cached-input price. Implicit caching is on by default for newer models (stored page lines 200-206, read by the lead; the extract EXT-0090 is a navigation-menu window that missed it, so this is not citable from an extract yet).
- **Correction to the supervisor's wording ("1/10 of input token for an hour").** On Anthropic and OpenAI the cost of keeping a cache is a *one-time write premium* (1.25x or 2x), then reads at a fraction; there is no per-hour rent in the stored pricing. The hourly rent exists for Gemini explicit caches. So the "time" cost is provider-specific, and the longest lifetime depends on the provider (Anthropic 1 hour; OpenAI up to 24 hours on some models), not 1 hour in general. The student's draft statement "the longest lifetime I found in Anthropic's documentation is one hour" is correct as stated for Anthropic.
- **Output tokens** are a third bill line. Discovery calls add output tokens (the model writes a request); v4's criterion excluded output.

## 3. First-order cost model [I], what changes under a bill criterion
Take a stable prefix of `L` tokens (the tool block), `T` model calls in a session, write multiplier `w`, read multiplier `r`, cache alive. Cost in fresh-input-token equivalents: uncached `L*T`; cached `L*(w + (T-1)*r)`. Ratio cached/uncached:

| `T` | r=0.1, w=1.25 | r=0.1, w=2 (1 hour) | r=0.05, w=1.25 |
|---|---|---|---|
| 1 | 1.25 | 2.00 | 1.25 |
| 3 | 0.48 | 0.73 | 0.45 |
| 10 | 0.22 | 0.29 | 0.17 |
| 30 | 0.14 | 0.16 | 0.09 |

Consequences (derived; none is a result):
1. **The bill saving from restricting exposure is smaller than the token saving** by about this ratio: at 10 calls, roughly 5 times smaller. A restriction that is attractive in tokens can be small or negative in dollars when the whole tool block sits in a warm cached prefix. This is the "token win could be a billed loss" objection (v4 `01` section 6 item 6) made quantitative, and it is consistent with the stored Toollery table (a 97.5% token cut with an inconclusive billed difference under a warm cache, a 97.5% billed cut with the cache suppressed; EXT-0061/0062).
2. **It does not remove the large-catalogue problem.** A prefix that exceeds the window cannot be cached at all; for the 10,000-tool example restriction is still required.
3. **Discovery gets cheaper in dollars than in tokens:** the extra model call re-reads the cached prefix at `r`, not at full price. What it can break is the cache itself: a change **inside** the prefix (insertion, removal, reordering of definitions) invalidates everything after it. The stored cache study reports that dynamic function calling and dynamic content make cache benefits less consistent and recommends placing dynamic content at the end (abstract only read, EXT-0091: costs reduced 41-80%; "avoiding dynamic traditional function calling"). This supports the **append-only** default of v4 for the tools added by P1, P2, P3; it is a hypothesis for our setting.
4. **Across sessions the cache is usually cold.** If the gap between sessions exceeds the lifetime, every session pays a write (`w`) on its first call, for the whole prefix including any restored context. The per-session write cost is proportional to the *size of the prefix at session start*; a smaller start prefix pays a smaller write.
5. Therefore the **session horizon `T` and the number of sessions** become regime variables next to catalogue size; v4 listed trajectory length but not sessions.

## 4. Memory: scope options and a recommendation
The student's draft reply proposes *tool memory only*: a stored record of which tools were found and used before, per user or role, so a returning user starts with them. Three scopes:
- **M-a, tool-usage memory (the student's proposal).** Store which tools a user or role used; at session start seed the core or the first search with them. This is F8 of the first package. Information class: **D** (derived from earlier sessions), legitimate at runtime if the evaluation sessions are disjoint from the sessions the memory was built on.
- **M-b, conversation or task memory** (history, summaries). A returning session must restore context; this costs tokens and, after cache expiry, a write. It is the same for every exposure arm, so it is **a common cost term**, reported and held fixed, not designed here.
- **M-c, full agent memory systems.** A separate research area; out of scope.
**Recommendation [I]:** adopt M-a as the policy component, treat M-b as a reported common term, and ask the supervisor explicitly whether his example ("the user leaves and comes back after days") is about M-a or M-b. A scope that excludes M-b is defensible only if said so; his wording is about contextual memory.
What the stored sources hold on memory: MemTool (EXT-0092, abstract only read: **short-term memory for tools within a multi-turn conversation**; autonomous tool removal 90-94% for reasoning models and 0-60% for medium-sized ones over 100 consecutive interactions on ScaleMCP; mentions long-term sessions as the setting but studies tool removal in-conversation) and a paper on a "missing memory hierarchy" (title only). **No stored source evaluates cross-session tool memory.** "Not found in the stored sources" is not "does not exist", and no new search is authorised.
Risks of M-a [I, untested]: (i) it pays only if tools repeat across a user's sessions, an unmeasured rate; (ii) stale tools and changed permissions; (iii) a per-user seeded prefix makes the prefix user-specific and can **fragment cache sharing across users** (whether a provider shares a cache across users with an identical prefix is provider-specific and not established here), so seed the memory *after* a shared prefix, as an append; (iv) it needs a session-level evaluation vehicle; the closest benchmark has none.

## 5. The three dimensions together (how they interact)
- **Prefix layout decides the cache:** shared stable prefix (system, core, discovery interface) first; role/user memory-seeded tools next; per-request narrowing (P1) and discoveries (P2, P3) appended after, never inserted before.
- **Memory shrinks discovery,** and with it the number of mid-trajectory appends and the extra calls; it can increase the start prefix, hence the first-call write.
- **Caching changes which saving counts:** the token criterion rewards removing definitions from a cached prefix; the bill criterion rewards it much less and instead penalises prefix changes and cold starts.
- New arm candidates (hypotheses, not additions to the arm table yet): memory-seeded core after a shared prefix; core re-ordering vs append-only; a one-hour versus five-minute write choice by expected session gap.

## 6. The student's two draft answers
1. **Memory scope (M-a only).** Reasonable and consistent with F8; add the caveat that the supervisor's example is about contextual memory (M-b) and ask which he means; state that M-b is held as a common term. Also state that no stored source tests cross-session tool memory and the vehicle has no sessions.
2. **"Report and optimise the bill; token reduction stays as the mechanism."**
 - Direction supported by section 3: the bill, not the raw token count, is what the cache changes.
 - It **replaces the AUTH-006 working objective** (minimise model-visible input tokens; billed cost recorded separately). The human may change that, but it needs an explicit new entry so the records do not drift; v4's brief still says tokens.
 - Make it concrete: report tokens by class (fresh input, cache write, cache read, output), then the bill under a **named provider and price table**; the optimum is provider-specific and prices move (the stored Gemini storage price doubles on 2027-01-01; Anthropic read multipliers differ by model).
 - "Across sessions" needs the session horizon and gap distribution as stated regime parameters; the cold-cache first call is a cost every session.
 - Output tokens must enter (discovery requests are output).
 - Keep reporting tokens as the provider-independent quantity so results transfer.

## 7. What is closed, open, or needs an authorization
- **Closed by scope, not by science (reversible by the human):** billed cost kept out of the criterion (AUTH-006); sessions and memory deferred (F8); no web search or new literature search (AUTH-010 and limits); no experiments.
- **Open, answerable from stored sources:** a proper reading of the stored cache sources (the cache study full text, the cache-aware compression and routing papers, the MCP caching specification of 2026-07-28, the Bedrock page) and of MemTool beyond its abstract. A bounded steward task inside AUTH-010; not yet done.
- **Open, needs a new authorization:** any search beyond stored sources (long-term and cross-session agent memory benchmarks; provider caching changes after 2026-10-11); any measurement (token classes by catalogue size and session gap; cache hit rates under discovery; tool repeat rates across sessions).
- **Not answerable without experiments:** whether restriction pays in dollars at realistic `T` and session gaps; whether models search; tool repeat rate across sessions; cache sharing across users.

## 8. Proposed revisions to the brief if the human adopts the bill criterion (not made)
1. Criterion paragraph: bill under a named price table as primary cost estimand, token classes reported, tokens retained as the provider-independent mechanism and a secondary estimand.
2. Add a session-start node M0 (load shared prefix, then memory-seeded tools) and a session boundary (cold cache) to Figure 1; add the prefix-layout rule.
3. Add `T`, session count and gap, and provider price table to the regime variables (`02` Figure 2).
4. Add the cost model of section 3 as the break-even accounting, and update E1 to record billed cost and cache fields beside tokens.
5. Add the supervisor's memory question and the contextual-memory scope question to the list for him.
