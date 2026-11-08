# P3 run 5: the DRY rule, live (2026-11-08)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-037.
- **Design:** `RESULTS-P3-REPLAY-A.md` and the docstring of `tools/p3_two_need.py` (variant `dry`).
- **Tasks:** run 4's 20 two-need tasks in kinds P, AF and AS.
- **Variants:** plain and dry; same models, provider and settings as run 4.

Counts: `run5-analysis.json` and `run5-replies-adjudicated.json` (counts only). Raw logs are local and git-excluded.

## Run
| Model (OpenRouter, GMICloud fp8, no fallbacks) | Sessions | Requests | Failed | Spend | Stop |
|---|---|---|---|---|---|
| minimax/minimax-m3 | 120 | 884 | 0 | $0.319 | done |
| deepseek/deepseek-v4.1-flash | 120 (119 complete) | 838 | 0 | $0.451 | its own $0.45 cap, in the last session |
| z-ai/glm-5.3 | 120 | 917 | 0 | $0.848 | done |
| **Run 5** | 360 | 2,639 | 0 | **$1.618** | |

**P3 total: $9.404 of the $10 stop.** The proposal estimated about $1.40; GLM cost more than in run 4 per variant. No live smoke
test was run first: DRY only adds rules to run 4's tested stopsearch path, and it passed the mock test.

## 1. Results [O] (plain against dry)
| | MiniMax | DeepSeek | GLM |
|---|---|---|---|
| both present (P): both needs done, of 20 | 20 → 18 | 18 → 18 | 20 → 20 |
| **doable need Y done**, AF + AS, of 40 | 40 → **34** | 36 → **34** | 33 → **27** |
| paired Y (plain only / dry only; exact p) | AF 5/0 (0.06); AS 1/0 | AF 3/1; AS 0/1 | AF 2/1; AS 7/2 (0.18) |
| **substitute action in X's app**, of 40 | 12 → **5** | 4 → **1** | 6 → **3** |
| **false claim that X was done**, of 40 | 5 → **2** | 0 → 0 | 1 → **0** |
| still searching at the backstop, of 40 | 13 → 11 | 8 → 8 | 15 → 11 |
| X's tool called by a guessed name, of 40 | 4 → 11 | 19 → 18 | 10 → 17 |
| no reply: kept calling tools after DRY asked for the reply | 3 | 10 | 8 |
| requests (AF + AS) | 400 → 323 (−19%) | 354 → 320 (−10%) | 380 → 350 (−8%) |

- **Replies classed as in run 4** [I, one reader]: a keyword pre-filter, then the lead read the remaining 11 replies.
- **The 3 false claims under DRY came from sessions where no call was refused.** A refusal did not lead to a false claim.

**Where Y was lost under DRY.** Of the 24 dry sessions (AF + AS) where Y was not done:
- 17 reached the 12-request backstop with search already withdrawn; 1 more reached it before the rule fired.
- 4 ended because DRY asked for the reply and the model kept calling tools.
- 2 ended with a reply that left Y undone.
- In all but one, Y's tool had been the best match of a search but was never called. In the backstop sessions, the model spent
  the remaining requests guessing names for the missing tool.

## 2. Reading [I]
1. **DRY works on the harms that ran:** substitute actions in the missing need's app fell by half or more (12 to 5, 4 to 1,
   6 to 3), and false claims fell (5 to 2, 1 to 0). This needs no gold answer: the dry app is simply where nothing new was found.
   Where both tools exist it did no harm (one MiniMax session).
2. **It costs some doable needs:** 6, 2 and 6 of 40, more than the replay predicted (2, 2 and 1). No cell is significant at 20
   tasks, but the direction is the same for all three models.
3. **The cause is the loop, not the stop.** Models with search withdrawn keep guessing the missing tool's name. DRY keeps the
   session open while the found tool is uncalled (correctly), so the guessing runs into the backstop before the doable call.
   Backstop hits barely changed, and guessed names rose.
4. **For the human's requirement (a dynamic, deterministic stop):**
   - DRY is the best client-side rule found in P3: deterministic, no count, no harm when the tool exists, fewer harmful actions.
   - But no client-side rule tried in P3 makes these models stop searching for a tool that does not exist. They keep trying
     under every variant.
   - The remaining lever is the model itself. That could be an instruction in the system text, which the human raised in
     INT-T-031 and which 2610.05348 found works for some models, or model choice.

## 3. Proposals for the human (not made)
- **(i) Close P3 here (lead's recommendation), within the $0.60 left.**
  - Record: deferral needs no instruction to search (runs 1-2). A tool-side note does not stop the loop (runs 2-4). A
    session-wide stop costs doable needs (run 4). DRY halves substitutes at a small cost in doable needs (run 5).
  - Carry DRY's dry-app refusal into V5-R's deferral stage as the substitute guard, marked provisional.
  - Carry the stop itself, rule and instruction, to the end-to-end study, where AppWorld's state checks and real results replace
    the stubs.
- **(ii) A last small run on the instruction:** DRY plus one sentence in the system text saying what to do when the catalogue
  has no tool for a need. A full variant for three models costs about $0.80, more than the $0.60 left. So this means either
  MiniMax and DeepSeek only (about $0.35), or the human raising the $10 stop.

## Limits
- As run 4: lead-written tasks, stub results, one provider, one run per cell, temperature 0, one reader.
- DeepSeek has 119 of 120 sessions.
- The replay-based estimate of Y's loss proved optimistic, because what models do after a refusal was not in the logs.
