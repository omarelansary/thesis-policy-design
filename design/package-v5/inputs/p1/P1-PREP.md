# P1 preparation: returning users from AppWorld's own supervisors (2026-11-08)

Status: **preparation only, desk work** (group 2, INT-T-040). No model request. Nothing here is validated, approved or final. No
V5 rule changed. Counts only: no user identity, task text or API name is committed. They come from AppWorld's protected local
data.

## 1. Why
- **`05` P1** (HYP-0017) asks whether memory-informed offering (M2: seeding tools a returning user used before) helps returning
  users, on the bill and on accuracy.
  - It must be tested at a catalogue size above n*, on returning sessions only, with recurrence measured from gold.
  - The recurrence must vary over a grid that includes values where seeding should not pay.
- **`17` found no benchmark** that combines at least 100 declared definitions with tools that recur across a user's sessions. So
  `05` planned a declared construction (`17` sections 7 and 9 item 2).

## 2. What AppWorld already contains [O]
Every AppWorld task names its user (the supervisor) and a date (`specs.json`). Over train and dev (147 tasks, 83 users):
- **34 users are returning users:** they own tasks from 2 to 5 different scenarios, one task per scenario.
  - 15 users have 2 sessions, 10 have 3, 7 have 4, 2 have 5.
  - By split: 22 users span train and dev, 10 are train only, 2 dev only.
- **64 returning sessions:** each user's sessions ordered by the task date, from the second session on.
- **Recurrence of needed APIs**, measured from AppWorld's ground-truth required APIs:

| Measure, per returning session | Counting all needed APIs | Excluding the supervisor app and logins (always in V5's core) |
|---|---|---|
| Recall: share of this session's needed APIs used in the user's earlier sessions | mean 0.49; quartiles 0.34 / 0.43 / 0.60 | **mean 0.19; quartiles 0 / 0 / 0.33; zero in 36 of 64; all in 3** |
| Precision of seeding everything used before: share of the seeds this session needs | mean 0.38; quartiles 0.27 / 0.32 / 0.50 | **mean 0.14; quartiles 0 / 0 / 0.25; zero in 36 of 64** |
| Seed set size (excluding core), median | — | 6 APIs |

**Reading [I].**
- The first column is inflated by tools that V5 keeps in the core anyway; the second is the one that matters for M2.
- On AppWorld's own users, seeding is mostly **below** D-02's break-even. `04` (summary item 3, D-02 revision 4,
  `calc/memory_seed.stdout.txt`) says the share of seeded tools that must be called ranges "from about a fifth to a half, and up to
  'never' in long sessions". Most returns here are at zero. About a quarter are at or above 0.25.
- So AppWorld supplies natural users on both sides of the threshold: the grid `05` asks for, without an invented history. It also
  warns that the natural recurrence is low.

## 3. Proposed construction (for the human; not made)
- **Users:** the 34 returning users; sessions in date order. The first session builds the memory file, later ones are measured.
- **Memory:**
  - V5-R05's plain Markdown file: a short summary, plus the tools used and when.
  - V5-R13's rule-based tool record: written after a session that passes the gate; append-only.
  - M2 seeds = the recorded tools, outside the core.
- **Arms** (`05` P1, already named there):
  - no memory;
  - memory-seeded (M2);
  - oracle memory: seeds = the session's own gold APIs, an upper bound;
  - optional: usage-informed retrieval in D (`15` PL-5).
- **Catalogue:** all of a session's apps, plus distractors, to sit above n*. Deferral with client search, as in P3, with
  V5-R17's stop.
- **Gaps between sessions:** set by design, shorter and longer than the cache lifetime (REQ-U21-10; `10` section 11 measured 2
  to 5 hours). The task dates are not real gaps.
- **Measures:**
  - the bill per session by DPR-0006, including W's cost (V5-R16);
  - task success (AppWorld's evaluator);
  - over-calling of seeded tools (CTXbench's naming effect, `05` P1);
  - seed precision and recall per session (the table above).
- **Unit of analysis:** the user (34 users; `05`), results stated by recurrence band (zero, low, high).

## 4. Limits and open points
- 34 users and 64 returns is small. Recurrence is low and lumpy (36 returns at zero), so the high-recurrence band has only about
  16 returns.
- A declared synthetic set (`05`'s original plan) could add users at controlled recurrence. AppWorld's users would then serve
  as the natural reference.
- AppWorld's scenarios differ in their tasks, not only in their users, so the session order by date is a construction, not a
  recorded history.
- The run needs the deferral harness of P3 joined to AppWorld's agent (as the end-to-end preparation also needs). It is not
  written.

## 5. Decision on the order (the human, 2026-11-08, INT-T-045)
- **The human's question:** why a synthetic set would be needed.
- **The lead's answer [I]:**
  - AppWorld's natural users give only about 16 returning sessions with any seed overlap above 0.25, and 36 of 64 with none
    (section 2). The band where M2 should pay may be too thin to show an effect.
  - A synthetic set would add users at controlled recurrence. It was `05`'s original plan, because `17` found no benchmark with
    natural recurrence.
- **Decision:** start with AppWorld's natural users only. Add a synthetic set later, and only if the high-recurrence band proves
  too thin to read.
- **Change record:** `05` P1's wording ("multi-session users built by a declared construction") is not changed yet. AppWorld's
  natural users are a construction too: the session order by date is chosen. The synthetic part becomes optional, conditional on
  that result.

## 6. Desk check of HYP-0017's falsifier on these users (2026-11-10; no model request) [O], then [I]
- **Script:** `design/package-v5/tools/p1_recurrence.py` (rebuilt; the script behind section 2 was not kept). It reproduces
  section 2's non-core column exactly: recall 0.19 (quartiles 0 / 0 / 0.33, zero in 36, all in 3), precision 0.14 (0 / 0 / 0.25,
  zero in 36), median seed set 6. It does **not** reproduce the "all APIs" column (it gives recall 0.55, precision 0.44, against
  0.49 and 0.38); that column's definition was not recorded. The non-core column is the one M2 depends on.
- **The falsifier** (HYP-0017): the seed precision h stays below the break-even h* of `calc/memory_seed.py` (revision 4) for the
  observed session length T, matches per search K and discovery mode. Here, client-side search, seeds = every non-core API needed
  in the user's earlier sessions, h from AppWorld's required APIs (gold), T on a grid around P2's median of 8 requests.

| K | r (cache read) | T = 3 | T = 8 | T = 10 | T = 30 |
|---|---|---|---|---|---|
| 1 | 0.1 | h* 0.21: 17/64 | 0.27: 15/64 | 0.29: 14/64 | 0.50: 7/64 |
| 1 | 0.025 | 0.26: 15/64 | 0.28: 15/64 | 0.29: 14/64 | 0.37: 9/64 |
| 3 | 0.1 | 0.15: 22/64 | 0.18: 20/64 | 0.20: 20/64 | 0.30: 14/64 |
| 3 | 0.025 | 0.17: 21/64 | 0.18: 20/64 | 0.19: 20/64 | 0.23: 16/64 |

  (Each cell: h* and the returning sessions whose h reaches it. r = 0.05 lies between the two rows; the script prints it.)
- **Reading [I].** On AppWorld's natural users, seeding everything a user needed before pays in at most about a third of returning
  sessions (7 to 22 of 64), and the mean precision (0.14) is below every h* in the grid (lowest 0.15). By gold, the falsifier is
  met on average for this seed rule on these users. This does not yet falsify HYP-0017:
  - h counts tools the task **needs**; the falsifier counts tools **called**, which a run would measure (models also call
    seeded tools they do not need: the over-calling `05` P1 asks about);
  - it tests one seed rule (everything used before); a narrower rule (for example, tools used in two or more earlier sessions)
    would have a different h, and is untested;
  - W, the cost of writing the memory, is not included (it would lower the saving further); T and K are assumed, not measured
    on these tasks;
  - the users are a construction (section 4).
- **What it changes for P1 (for the human):** a model run on these users would most likely show M2 not paying, which is a result
  (a negative result is still a thesis). Where M2 could pay, the high-recurrence returns, there are only 14 to 22 sessions.

## 7. Step A: seed rules compared on gold (AUTH-033, 2026-11-10; no model request) [O], then [I]
- **Script:** `design/package-v5/tools/p1_seed_rules.py`. Seeds come from history only. Net = needed seeds x saving - unneeded
  seeds x cost (`calc/memory_seed.py` revision 4, client-side search), in fresh-input-token equivalents per returning session;
  per needed seed 2,155 saved and per unneeded seed 488 spent at K = 3, T = 8, r = 0.1. A whole session of P2's size bills
  roughly 50,000 (approximate).

| Rule | Sessions with seeds | Mean seeds | Mean h | Mean recall | Net, K=3 T=8 | Net, K=1 T=8 | Net, K=3 T=30 | Sessions h >= h* (K=3 T=8) |
|---|---|---|---|---|---|---|---|---|
| all used before (M2 as written) | 64/64 | 6.1 | 0.14 | 0.19 | -963 | -1,594 | -3,700 | 20/64 |
| used in 2+ earlier sessions | 15/64 | 0.3 | 0.30 | 0.02 | +88 | +10 | -15 | 5/64 |
| most recent session only | 64/64 | 3.8 | 0.14 | 0.13 | -507 | -919 | -2,157 | 21/64 |
| apps used in 2+ earlier sessions | 20/64 | 7.3 | 0.06 | 0.12 | -2,187 | -2,612 | -5,766 | 0/64 |
| **pop6: six APIs most needed by other users (outside the current scenario)** | 64/64 | 6.0 | **0.24** | **0.38** | **+956** | -256 | -1,132 | **36/64** |

- **Reading [I].** Per-user memory loses on the bill in every setting: the user's own history predicts too little. A role memory
  (the tools other users need most; HYP-0017 says "this user or role") gains about 2% of a short session with three matches per
  search, and loses with one match or in long sessions. pop6 does not depend on the user, so it is closer to a larger core
  chosen from usage (S1; Copilot's core, EXT-0228) than to personal memory. Excluding the current scenario's sibling tasks did not
  change pop6's result.
- **Chosen for step B:** pop6 (the only rule with a positive net), against no memory and oracle seeds (the session's own gold).

## 8. Step B plan (AUTH-033; harness not yet written; checkpoint of 2026-11-10)
- **Harness** `design/package-v5/tools/p1_memory.py`, a copy of `p2_offering.py`'s structure (AppWorld's
  `simplified_function_calling` agent and prompts as shipped, its evaluator, a new root and experiment per run, the same
  OpenRouter hook: provider pin, billed cost, two-failure stop, 402 stop).
- **Declared at start:** core = all supervisor APIs and every app's login API; one search tool `tools__search` (the name needs
  exactly one `__`, or AppWorld's agent skips it); then the arm's seeds (none, pop6, or oracle).
- **Search:** the harness rewrites each `tools__search` call's code into a `print` of the top 3 BM25 matches over all non-core
  APIs (P3's ranker), and appends their definitions to the declared tools from the next request (V5's discovery).
- **No stop rule:** every P1 task is doable; V5-R17 acts only after a no-match signal, and its forced reply would end an AppWorld
  session without `complete_task`. Held equal across arms (a deviation from section 3, recorded here).
- **Memory from gold:** pop6 needs no per-user memory; oracle uses the session's gold. First sessions are not run.
- **Runs:** the 64 returning sessions x 3 arms x 2 repeats on `z-ai/glm-5.3` (OpenRouter, GMICloud). A smoke of 3 sessions
  first gives the cost per session. If the projection exceeds AUTH-033's $12, the oracle arm (an upper bound, not needed for the
  falsifier) is dropped before any repeat is cut (INT-T-048).
- **Measures:** success, billed cost and DPR-0006 components, calls, searches, seeds called (measured h) and seeds called but not
  needed (over-calling).

## 9. Rule fixed during step B, before any arm comparison (2026-11-10 00:55 UTC)
- **Observed in the first run (none, repeat 1), 16 sessions:** mean $0.078 per session, twice the smoke's $0.037, because one
  session ran to AppWorld's 50-step cap (49 calls, $0.58); the others average about $0.044. Cached share 0.68 (P2: about 0.9):
  each discovery appends to the tools array, which the chat template places before the messages, so the cached prefix ends there
  (V5-R02's question; [O] here, the mechanism [I]).
- **Rule (the lead; AUTH-033's $12 for P1 and $3 per run are kept, not raised):** if the first run stops at its $3 cap, the
  other three runs (pop6 r1, none r2, pop6 r2) use exactly the sessions the first run completed, so all arms and repeats share
  one session set and no repeat is cut. The sessions are AppWorld's returning sessions in their fixed order, so the set is a
  prefix of that order, not a choice by outcome.
- **Applied (03:20 UTC):** none r1 completed 44 sessions ($3.002), pop6 r1 completed the first 35 of them ($3.008; one session ran
  to the step cap). The repeat-2 runs use exactly those 35 sessions, the set every run can share, with $2.93 each (P1 total:
  smoke $0.110 + $3.002 + $3.008 + $0.021, an aborted start of none r2 on 44 sessions stopped by the lead after 6 calls, kept as
  `p1-aborted-none-r2-44ids`, + 2 x $2.93 <= $12). On these 35 sessions repeat 1 cost $2.457 (none) and $2.549 (pop6).
