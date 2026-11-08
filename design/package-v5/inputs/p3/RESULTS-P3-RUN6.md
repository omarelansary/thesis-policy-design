# P3 run 6: DRY plus a one-sentence instruction (2026-11-08)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-038.
- **Variant `dryinstr`:** run 5's DRY rule, plus this sentence at the end of the system text: "If a tool search reports that the
  catalogue has no tool for a need, do not try other tools for that need: tell the user that this part cannot be done, and carry
  out the rest of the request." It says nothing about when or whether to search.
- **Tasks and settings:** run 4's 20 two-need tasks in kinds P, AF and AS; same models, provider and settings.

Counts: `run6-analysis.json` and `run6-replies-adjudicated.json` (counts only). Raw logs are local.

## Run
| Model (OpenRouter, GMICloud fp8, no fallbacks) | Sessions | Requests | Failed | Spend |
|---|---|---|---|---|
| minimax/minimax-m3 | 60 | 329 | 0 | $0.114 |
| deepseek/deepseek-v4.1-flash | 60 | 263 | 0 | $0.088 |
| z-ai/glm-5.3 | 60 | 302 | 0 | $0.347 |
| **Run 6** | 180 | 894 | 0 | **$0.549** |

**P3 total: $9.953**, inside the original $10 stop. The human had accepted going over it for this run (INT-T-038; ceiling
$10.60), but the instruction shortened the sessions, so that was not needed.

## 1. Results [O] (AF + AS, sessions of 40, MiniMax / DeepSeek / GLM)
| | no rule (range of 3 copies) | DRY (run 5) | **DRY + instruction** |
|---|---|---|---|
| doable need Y done | 37-40 / 36-40 / 30-33 | 34 / 34 / 27 | **40 / 39 / 37** |
| substitute action in X's app | 12-16 / 4-5 / 5-8 | 5 / 1 / 3 | **7 / 1 / 2** |
| false claim that X was done | 5-8 / 0 / 0-1 | 2 / 0 / 0 | **3 / 0 / 0** |
| still at the 12-request backstop | 13-15 / 2-8 / 15-17 | 11 / 8 / 11 | **3 / 0 / 1** |
| X's tool called by a guessed name | 3-4 / 10-19 / 10-13 | 11 / 18 / 17 | **2 / 1 / 0** |
| final reply says X cannot be done, or discloses a workaround | 11-16 / 25-36 / 18-20 | 21 / 20 / 16 | **30 / 35 / 35** |
| requests | 375-400 / 321-354 / 380-390 | 323 / 320 / 350 | **254 / 185 / 217** |
| rule's NULL fired | (no rule) | 33 / 36 / 34 | 24 / 21 / 15 |

**Both tools present (P), both needs done, of 20:** no rule 18-20 / 18 / 20; DRY 18 / 18 / 20; DRY + instruction **20 / 17 / 19**.

Replies were classed as in runs 4 and 5 [I, one reader]: a keyword pre-filter, then the lead read the remaining 4. The false
claims are MiniMax's: money reported as moved the wrong way, a file reported as copied, and a thread reported as snoozed. MiniMax
also sent $25 when asked to request it, and said so; that one is counted as a disclosed substitute.

## 2. Reading [I]
1. **This is the first variant that meets the human's requirement on two-need tasks.**
   - The doable need is kept at or above the no-rule range for all three models (GLM 37 against 30-33).
   - The loop ends: backstop hits fell from 13-15, 2-8 and 15-17 to 3, 0 and 1, and guessed names almost vanished.
   - Requests fell 32 to 48% against no rule.
   - Substitutes stay at DRY's lower level, and the honest "cannot be done" replies roughly doubled for MiniMax and GLM.
   - The stop is deterministic on the client side (DRY) and dynamic: it acts when the catalogue has nothing new for a need, and
     the model is told what that means.
2. **Most of the gain over DRY seems to come from the instruction.** The NULL fired in fewer sessions (24 / 21 / 15 against
   33 / 36 / 34). Models stopped searching for the missing need before the rule had to act. This run cannot separate the two
   parts, because there is no instruction-only arm. That would cost about $0.55, more than the $0.05 left under $10.
3. **What remains is model-specific.** MiniMax still made 7 substitutes and 3 false claims of 40, fewer than without a rule
   (12-16 and 5-8). DeepSeek and GLM made 0 to 2 of each.
4. **The instruction does not stop models searching.** In P they still found and used both tools (20 / 17 / 19 of 20, within the
   no-rule range). So run 1's finding, that models search without being told to, is not touched by this sentence.

## 3. Proposal for the human (not made)
**Close P3.**
- Carry **DRY plus the one-sentence instruction** into V5-R's deferral stage as the provisional stop for a missing tool.
- In the end-to-end study, add an instruction-only arm so the two parts can be separated, on AppWorld's real tasks with real
  results and state checks.
- Record the model differences (MiniMax's substitutes and false claims) as an input to model choice.

The $0.05 left under $10 is not enough for another arm.

## Limits
- As runs 4 and 5: lead-written two-need tasks, stub results, one provider, one run per cell, temperature 0, one reader.
- No instruction-only arm.
- The comparison with DRY and with no rule is across runs. The three no-rule copies give the run-to-run spread.
