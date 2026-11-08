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
