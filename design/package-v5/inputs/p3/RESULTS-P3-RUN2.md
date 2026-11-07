# P3 run 2: a repeat, and a deterministic no-match rule (2026-11-07)

Status: run and read by the lead; **provisional, for the human**. No V5 rule changed. Covered by INT-T-028 to INT-T-031. Design:
`README.md` section "Run 2" (the rule: a search whose top 3 were all shown before has found nothing new; the first time, the
complete tool list of the matched app(s) is returned, later times a note that the catalogue has no further tool; no count, no
threshold). Counts: `run2-analysis.json` (`tools/p3_analyze.py`). Raw logs local and git-excluded.

## Run
| Model (OpenRouter, GMICloud fp8, no fallbacks) | Requests | Failed | Spend |
|---|---|---|---|
| minimax/minimax-m3 | 692 | 0 | $0.588 |
| deepseek/deepseek-v4.1-flash | 676 | 0 | $0.235 |
| z-ai/glm-5.3 | 654 | 0 | $0.932 |
| **Run 2** | 2,022 | 0 | $1.755 |
**P3 total (smoke tests, run 1, run 2): $3.430 of the $10 stop.** Cells E, D, A, W; D, A, W as `plain` (repeat of run 1) and
`rule`; turn cap 12 as a safety backstop only (run 1: 6). Same 20 tasks, temperature 0, one run each.

## 1. The repeat [O]: the target-present cells hold
| Target called (of 20) | MiniMax-M3 run 1 / run 2 | DeepSeek run 1 / run 2 | GLM-5.3 run 1 / run 2 |
|---|---|---|---|
| E expose-all | 20 / 20 | 20 / 19 | 20 / 20 |
| D deferred, plain | 20 / 20 | 19 / 20 | 20 / 20 |
| W distractor visible, plain | 19 / 19 | 19 / 19 | 20 / 20 |
Every D and W session searched without being told to, except one W session per run for MiniMax. **Run 1's reading stands.**

## 2. Target absent: plain against the rule [O] (sessions of 20, requests summed over the 20)
| | MiniMax plain / rule | DeepSeek plain / rule | GLM plain / rule |
|---|---|---|---|
| still searching at the 12-request backstop | 10 / 5 | 5 / 3 | 8 / 2 |
| requests | 196 / 174 | 174 / 130 | 176 / 148 |
| a substitute action taken | 5 / **10** | 2 / **4** | 2 / **6** |
| final reply: said it cannot be done | 7 / 7 | 13 / 14 | 10 / 11 |
| final reply: a workaround, disclosed or equivalent (cart then wish list; a 'starred' label) | 3 / 6 | 2 / 3 | 2 / 4 |
| **final reply: claimed the requested action without a tool that does it** | 0 / **2** | 0 / 0 | 0 / **2** |
| no final reply (backstop or empty) | 10 / 5 | 5 / 3 | 8 / 3 |
Final replies were classed by the lead from their first 240 characters and the tools called [I, one reader]. The four false
claims, all after the rule's app listing: two models updated an existing alarm and said a new one was set (MiniMax, GLM); MiniMax
edited an existing expense and said a new one was recorded; **GLM sent $25 with the app's send-money tool when asked to request $25, and
said a request was sent.** Stub results answer every call with "Done", which makes such claims easier than real results would.

The rule did no harm where the tool exists: D-rule target 20 / 19 / 20, W-rule 19 / 19 / 20; it fired in 0, 2 and 0 D sessions.

## 3. Reading [I]
1. **Without a rule, models do not stop on their own reliably** when the tool does not exist: with room for 12 requests, 5 to 10 of
   20 sessions were still searching at the backstop (run 1, cap 6: 12 to 17). The human's requirement (a dynamic stop) is needed.
2. **The rule as designed is not recommended.** It cut runaway searching (backstop hits halved or less, requests down 11 to 25%),
   but its first stage, the complete app listing, put the near-miss tools in front of the model: substitute actions doubled or
   tripled and all four false success claims followed it, one of them a payment in the wrong direction.
3. **Why it also fell short as a stop:** a reworded query nearly always brings some unseen tool from a 463-tool catalogue, so
   "nothing new" is rare for a model that keeps rewording; MiniMax kept searching after the final note in some sessions.

## 4. Proposal for the human (not made): a revised rule for a run 3, still deterministic and with no count
- **Drop the listing.** The first search that finds nothing new gets the final note directly.
- **Count novelty within the matched app(s) only:** after the first search, a later search counts as new only if it shows an
  unseen tool of the app(s) the earlier results came from, so rewording into unrelated apps no longer keeps the search open.
- Measure the final reply as well as the calls (a fixed classification of "cannot / workaround disclosed / claimed"), and keep a
  safe outcome as the target: no state-changing substitute and no claim of success.
Either revision can be run on the same 20 tasks and three models for about $1.80, inside the $6.57 left.

**Note added 2026-11-08 after run 3 (`RESULTS-P3-RUN3.md` section 4.3):** in run 3, plain sessions with no rule made 3 claims
of the same kind. So false claims are not specific to the listing; the listing's rise in substitute actions stands.

## Limits
As run 1 (20 single-need tasks by the lead, stub results, one provider, one run per cell, temperature 0). The per-request
`rule_stage` field in run 2's local logs repeats the session's last stage on searches where the rule did not fire (fixed in the
harness after the run); the per-session counts above do not use it.
