# P2 main run: offering a subset at a fixed cached prefix (2026-11-08)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-042 (Main A and B approved;
costs watched for top-ups).
- **Design:** `P2-DESIGN.md`, with the API switched to Responses after the pilot (`RESULTS-P2-PILOT.md`).
- **Counts:** `main-analysis.json` (`tools/p2_analyze.py`; per run, and per task by AppWorld task id) and
  `main-paired-summary.json` (the paired estimates below).
- Logs and AppWorld outputs are local and git-excluded.

## Run
- **Tasks:** the 30 eligible AppWorld dev tasks (10 scenarios, Spotify only).
- **Catalogue:** 128 tools declared (supervisor, spotify, phone), the same for every task. The oracle subset is 6-10 tools.
- **Models:** gpt-5-mini (served `gpt-5-mini-2025-08-07`) and gpt-5.4-mini (served `gpt-5.4-mini-2026-03-17`); OpenAI Responses
  API, reasoning effort low, temperature 1.0 (the models' fixed default).
- **Arms:** `all`, `enf` (`allowed_tools`), `instr` (one sentence), `drop` (subset only declared); 2 repeats each. 16 runs, 480
  task-runs.
- **Reliability:** 0 failed model calls and 0 task exceptions.
- **Spend:**

| Model | Main run | Cap | Pilot | Total |
|---|---|---|---|---|
| gpt-5-mini | $4.006 | $6 | $0.162 | $4.168 |
| gpt-5.4-mini | $8.371 | $11 | $0.154 | $8.525 |
| **P2** | **$12.377** | $17 | $0.316 | **$12.693** |

Estimate before the run: about $11.6. The running total was reported to the human run by run.

## 1. Results per run [O] (tasks solved of 30, by AppWorld's evaluator)
| Model | Arm | Repeat 1 | Repeat 2 | Calls per task | Prompt tokens per call | Cached share | Cost per task | Calls outside the subset |
|---|---|---|---|---|---|---|---|---|
| gpt-5-mini | all | 20 | 18 | 11.6 | about 19,500 | 0.91 | $0.016 | 12 / 17 (allowed) |
| | enf | 22 | 23 | 11.8 / 13.3 | about 20,400 | 0.93 | $0.016 | 0 |
| | instr | 19 | 17 | 24.3 / 23.0 | about 20,150 | 0.95-0.97 | $0.022 | 5 / 14 |
| | drop | 17 | 19 | 12.4 / 10.1 | 9,600-12,300 | 0.86-0.88 | $0.013 | 0 |
| gpt-5.4-mini | all | 19 | 21 | 7.6 / 7.2 | about 19,500 | 0.86-0.90 | $0.036 | 18 / 26 (allowed) |
| | enf | 20 | 17 | 9.9 / 9.6 | about 19,700 | 0.89-0.90 | $0.041 | 0 |
| | instr | 17 | 23 | 6.9 / 7.6 | 17,900-19,300 | 0.90 | $0.031 | 0 |
| | drop | 23 | 22 | 8.9 / 8.0 | 8,000-8,800 | 0.74-0.75 | $0.032 | 0 |

**Run-to-run noise:** the two identical `all` runs disagree on 6 (gpt-5-mini) and 8 (gpt-5.4-mini) of 30 tasks.

## 2. Paired estimates against `all` [O]
Per task, the difference in successes averaged over the two repeats. The 95% interval is a bootstrap over the 10 scenarios
(4,000 resamples, fixed seed). A positive value means better than `all`.

| Arm | gpt-5-mini: of 60 (all: 38) | difference per task, 95% interval | gpt-5.4-mini: of 60 (all: 40) | difference per task, 95% interval |
|---|---|---|---|---|
| **enf** (server-enforced subset) | **45** | **+0.117, [+0.033, +0.217]** | 37 | −0.050, [−0.167, +0.050] |
| instr (instruction, unenforced) | 36 | −0.033, [−0.283, +0.183] | 40 | 0.000, [−0.133, +0.117] |
| drop (subset only declared) | 36 | −0.033, [−0.167, +0.083] | 45 | +0.083, [−0.067, +0.233] |

**Calls and cost against `all`** (both repeats):
- `enf`: calls x1.08 / x1.32, cost x1.02 / x1.15.
- `instr`: calls x2.03 / x0.98, cost x1.37 / x0.87.
- `drop`: calls x0.97 / x1.14, cost x0.80 / x0.90.

## 3. Reading [I]
1. **HYP-0018's falsifier is not met on this set.** Offering only the subset at the unchanged cached prefix, enforced by the
   server, gave no accuracy loss beyond run-to-run variation on either model.
   - gpt-5-mini improved by about 12 points per task, an interval that excludes zero. gpt-5.4-mini's −5 points has an interval
     that includes zero.
   - This is the "may improve" side of HYP-0018. A loop item cannot separate a small loss from "nearly the same" (`05` section
     1), so the end-to-end study gets the small effects.
2. **The mechanism holds** (`05` P2's ending condition):
   - `allowed_tools` did not break the cache: cached shares in `enf` are equal to or above `all` on both models.
   - It was enforced: 0 calls outside the subset in all 120 `enf` task-runs.
   - This is the Manus principle "Mask, Don't Remove" (E6) on a vendor API.
3. **The instruction is not a substitute for enforcement on every model.**
   - gpt-5-mini broke the stated subset (5 and 14 calls outside) and needed twice as many calls (cost x1.37).
   - gpt-5.4-mini followed it (0 calls outside) at no extra cost.
   - So the portable form depends on the model, as R2's probe suggested (`10` section 12). It needs a check per model before
     V5 relies on it on an unenforced route.
4. **Removal is cheaper per session, not better.**
   - Declaring only the subset gave the same accuracy within the intervals, and cost 10-20% less: the prefix is about 8,000-12,000
     tokens instead of about 19,500, even though it caches less (0.74-0.88).
   - So for a subset fixed for a whole session, removal is the cheaper form. P2 does not test it, but removal's prefix differs per
     task and per user, which costs the sharing across users (V5-R06).
   - Fixed-prefix offering is what matters when the offered set **changes within a session** (V5's discoveries and M2 seeds,
     V5-R02).
   - [U] Which form is cheaper over many users depends on the request rate across users (`04` "Cold and warm starts"). D-01 and
     D-01h can price it.
5. **Restriction can lengthen sessions.**
   - Under `enf`, gpt-5.4-mini needed 32% more calls. With all tools it had used 18 and 26 calls outside the oracle list, so the
     oracle subset is not the only working path, and restricting it to the oracle makes the model work around.
   - Realistic subsets from memory or prediction will miss some needed tools. That is P1's and the end-to-end study's question.

## 4. What this changes, proposals for the human (not made)
- **V5 keeps the offering stage** (S1 and M2 offering at a fixed prefix).
  - On OpenAI it is supported by a mechanism that keeps the cache and is enforced, with no accuracy loss on this set.
  - On the university API (no enforcement), the instruction form needs a per-model check. Free follow-on P2b: `all` against
    `instr` on ScaDS GLM-5.3, with the same tasks and harness.
- **Add to `04` section 6 as a note:** for a subset fixed for a whole session, declaring only the subset is cheaper. Fixed-prefix
  offering is for subsets that change within a session, or that are shared across users.
- **HYP-0018:** record this result in its file, with status `supported on this set (P2, two OpenAI models, oracle subset)`. The
  human decides on any status change.

## 5. Also produced: validated end-to-end task pairs
P2's successful runs (2 to 16 per task) validate removed APIs for the end-to-end preparation (`inputs/e2e/`): **16 dev tasks in 6
scenarios** now have a removed API that every successful run called (FeasiGen's rule). Counts: `inputs/e2e/e2e-variants-summary.json`.

## Limits
- One benchmark (AppWorld dev, Spotify tasks); one catalogue size (128, OpenAI's maximum); oracle subsets only.
- Two OpenAI models; two repeats at temperature 1.0; 30 tasks in 10 scenarios.
- The interval is a scenario bootstrap with 10 clusters, which is rough.
- Costs use the prices read on 2026-11-08 (`P2-DESIGN.md` E2).

## Corrections of 2026-11-09 (lead, AUTH-032 as amended by INT-T-103)
Found while building the results deck (`design/package-v5/deck/CLAIM-LEDGER.md`). The text above is left as it was; each point names the line it corrects.
- Lines 58 to 61: "no accuracy loss beyond run-to-run variation" and "improved by about 12 points" are stronger than the evidence. The intervals (bootstrap over 10 scenarios, called rough at line 104) allow losses up to 17 points (gpt-5.4-mini, enforced) and 28 points (gpt-5-mini, instruction); no per-repeat McNemar test is below 0.05; gpt-5-mini's +0.117 has the opposite sign on gpt-5.4-mini and six contrasts were made without correction. Supported wording: no detectable difference, small effects not excluded.
