# P4 step A: tool-result clearing replayed on the logged P2 sessions (AUTH-033, 2026-11-10; no model request)

- **Question (HYP-0021, `05` P4):** does clearing old tool results lower the bill once the cache rewrite it causes is counted?
- **Rule replayed:** Anthropic's `clear_tool_uses` as documented (stored source
  `evidence/literature-20261019/v5-anthropic-context-editing-20261022.md`: lines 38-40, behaviour; lines 1724-1732, defaults;
  lines 395-410, example). When a request's input exceeds the trigger, the oldest tool results are replaced by a placeholder,
  keeping the last 3; it applies only if at least `clear_at_least` tokens go. Two settings, neither chosen here: the vendor's
  defaults (trigger 100,000, keep 3, no minimum) and its documented example (30,000, 3, 5,000).
- **Method:** `design/package-v5/tools/p4_replay.py` on the local logs of P2 main (gpt-5-mini, gpt-5.4-mini) and P2b
  (GLM-5.3 on GMICloud). Per request: prompt minus tokens cleared so far; cached minus the same, except on a request with new
  clearing, where only the part before the first newly cleared message stays cached. Output unchanged; same model behaviour
  assumed. List prices as billed in P2 and P2b. The replayed baselines match the billed amounts (GLM $5.797 replayed, $5.781
  billed; the OpenAI runs lack 28 task logs and are compared on the rest).

## Result [O]
| Model | Task-runs | Vendor default: fired / bill | Vendor example: fired / tokens cleared / bill |
|---|---|---|---|
| gpt-5-mini | 240 | 0 / unchanged | 31 / 405,836 / $4.006 -> $4.055 (**+1.2%**) |
| gpt-5.4-mini | 240 | 0 / unchanged | 30 / 408,500 / $8.371 -> $8.451 (**+1.0%**) |
| GLM-5.3 | 120 | 0 / unchanged | 59 / 744,854 / $5.797 -> $6.231 (**+7.5%**) |

## Reading [I]
- With the vendor's defaults, clearing never fires on our tasks: no request came near 100,000 input tokens (largest 49,014).
- With the documented example it fires in 12-49% of the task-runs and **raises** the bill on every model: the rewrite of the
  cached suffix after a clear costs more than the cleared tokens save over the few requests left in these short sessions. This
  is the direction of HYP-0021's falsifier, on the bill alone and with the model's behaviour held fixed.
- Not shown: accuracy, and whether a model re-fetches cleared results (which would raise the bill further). Step B tests both
  live on GLM-5.3, reusing P2b's two `all` runs as the keep-everything arm.
- Limits: AppWorld's short tasks (median 8 requests); long tasks, where clearing is meant to pay, are not in our data (`05` P4
  named MCPMark, not run). OpenAI and GMICloud charge no cache-write premium; with Anthropic's (1.25x) the rewrite costs more.

## Step B rule, fixed during the run (2026-11-10 01:25 UTC; after seeing the first 7 tasks' costs, before any accuracy)
- **Observed [O]:** mask repeat 1, first 7 tasks: billed $1.003 against $0.422 for the same tasks in P2b's keep-everything run 1,
  and about twice the calls (for example 20 against 8, 19 against 7). [I] After a clear the model seems to call tools again; this is not decomposed (`RESULTS-P4.md`).
- **Rule (the lead; AUTH-033's $8 for P4 is kept):** if mask repeat 1 stops at its $2.50 cap, repeat 2 runs exactly the tasks
  repeat 1 completed, with a cap of $3.60 (smoke $0.40 + $2.50 + $3.60 = $6.50, within $8), and the keep arm is P2b's two `all`
  runs on the same tasks. The tasks are P2b's in their fixed order, so the set is a prefix of that order.
