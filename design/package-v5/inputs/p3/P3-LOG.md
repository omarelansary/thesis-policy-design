# P3 log: runs, decisions, reasons, results, conclusions (kept up to date; INT-T-036)

The one place that ties P3 together, in order. Each row points to the record that holds the detail:
- the human's own words in `requirements/intake/`;
- the result files here;
- the commits.

This log is the lead's summary [I]; the records it points to govern. When the operations branch is free, its rows become the P3
AUTH row in `ops/AUTHORIZATIONS.md` and WD entries in `ops/DESIGN-DECISIONS.md` (`ops/OPEN-TASKS.md`).

**Question** (`05` P3, HYP-0019): do models search for a deferred tool when nobody tells them to? And when the tool does not
exist, what makes them stop? The second question was added by the human (INT-T-031: the stop must be dynamic and
deterministic, not a number of turns).

**Fixed throughout:**
- **Route:** OpenRouter, provider GMICloud fp8 pinned, no fallbacks (INT-T-028, INT-T-030). One provider served all three models.
- **Models:** MiniMax-M3, DeepSeek-V4.1-Flash, GLM-5.3.
- **Tasks and tools:** lead-written tasks over AppWorld's real tool definitions, 463 tools (INT-T-029). Results are stubs.
- **Settings:** temperature 0, seed 7.
- **Budget:** a $10 stop for all of P3 (INT-T-029).
- **Licence:** AppWorld text, tool names and logs stay local; only counts are committed.

## 1. Decisions by the human
| Intake | Date | Decision (summary; verbatim in the record) |
|---|---|---|
| INT-T-028 | 11-07 | Use OpenRouter for P3 and the other items that need it; not for B2 |
| INT-T-029 | 11-07 | Tasks built over AppWorld's real tools; stop at $10 in total; the lead picks models after the listing |
| INT-T-030 | 11-07 | Models: GLM-5.3, MiniMax-M3, DeepSeek-V4.1-Flash, all on GMICloud fp8 |
| INT-T-031 | 11-07 | A no-match rule and a second run; the stop must be dynamic (or deterministic), not a number of turns |
| INT-T-032 | 11-07 | Leave B2; go on with run 3 using the revised rule; asked whether multi-tool tasks come now or later |
| INT-T-033 | 11-08 | Accepts the order research → per-need rule → multi-need run; authorizes the research; asks where the stop rule is tested; take care of the other agents and GLM |
| INT-T-034 | 11-08 | The search was not extensive enough: run Sonnet subagents for extensive research |
| INT-T-035 | 11-08 | Agrees to run 4 and its cost; leaves the repeated plain run and where to start to the lead |
| INT-T-036 | 11-08 | Chooses option (a): design a per-need rule by replay on run 4's logs; document runs, decisions, reasons, results and conclusions |
| INT-T-037 | 11-08 | Approves run 5: plain against DRY, about $1.40 |

## 2. Runs
| Run | Commit | What changed, and why | Requests / spend | Result [O] | Conclusion [I] |
|---|---|---|---|---|---|
| Smoke 1 | 87002c6 | Check the harness on one task per model | 78 / $0.115 | Harness works; outcome classes fixed after reading the logs | — |
| 1 | 2602c28 | First test of the question: cells E (all tools), D (deferred), A (absent), W (wrong tool visible); plain and index prompts; cap 6 | 1,684 / $1.560 | Deferred target: searched in every session, called in 19-20 of 20 (E 20 of 20). Absent target: 2-3 of 20 substitutes, but 12-17 of 20 still searching at the cap | HYP-0019's falsifier is not met. The weak point is the missing tool: models do not stop. A no-match rule is proposed |
| 2 | 781d987 | Human: a stop that is not a turn count (INT-T-031). Rule `rule`: nothing new in the top 3 → the full tool list of the matched app once, then "no further tool"; cap 12 as backstop only | 2,022 / $1.755 | Repeat of run 1 holds. The rule cut backstop hits and 11-25% of requests, but substitutes doubled or tripled and 4 false success claims followed the listing | The listing showed near-miss tools: not recommended. Revision: no listing; novelty counted within the matched app |
| 3 | b317b9b | Rule `rule2` (INT-T-032): no listing; a search is new only if it shows an unseen tool of a best-match app; otherwise only the note | 1,898 / $0.726 | No harm where the tool exists; substitutes no longer rose (+1, within spread). But the note reached 50 of 60 sessions and only 10 then stopped. 3 false claims without any rule | A note in the result is not a stop. Run 2's reading corrected: false claims occur without the listing. Proposal: withdraw search when the note comes (the lead's own idea, not from a source) |
| Research rev. 1 | 90291bf | Human questioned the withdraw idea and asked whether earlier designs or sources hold ideas (INT-T-033) | 7 searches, 6 fetches | Sources found: 2610.06191 (only "finish" left after 5 useless results); earlier designs had a search budget (DPR-0004) and a score threshold (`05`). Run 3 logs: all substitutes came after the first note; 3 of 120 present-target sessions called the target after it | The lead agreed the withdraw idea was weak for multi-need tasks. Order agreed: research → per-need rule → two-need run |
| Research rev. 2 | 80736a8 | Human: not extensive enough (INT-T-034). Six web scouts, 8 claims checked by the lead | 80 searches, 126 fetches | No published deterministic stop for tool-search loops. Enforcement works and text does not (2610.06191, CGDP 2605.07042, CrewAI). A refusal result helps only some models (2610.05348). Excluding the requested action redirects to another (Guardrails Redirect). A "Done" stub favours false claims (2609.14758) | Keep the trigger; change the enforcement; test it on two-need tasks, because a session-wide stop predictably harms the doable need |
| Smoke 4 | 55dd9a4 | Check the two-need harness on one task per model | 268 / $0.120 | GLM keeps emitting tool calls with no tools offered | The forced reply now ends the session itself ("stop ignored") |
| 4 | 4a5a650 | Two-need tasks in kinds P, AF, AS; plain twice, note, stopreply, stopsearch (INT-T-035) | 6,282 / $3.510 | Both present: no harm. Forced reply: the doable need was lost in 40-80% of tasks (p ≤ 0.016, all cells), and most models kept calling tools after the stop. Search withdrawn: the doable need was kept, but the loop did not end (guessed names and backstop hits went up). Note: no effect. Substitutes and MiniMax's false claims (6-8 of 40) occur with no rule | No session-wide or search-only stop meets the requirement. The rule must be scoped per need. Next: design it by replay on run 4's logs (INT-T-036) |
| Replay (a) | 4d20137 | Human chose option (a) (INT-T-036): replay candidate per-need rules on run 4's logs; no requests | 0 / $0 | Replay check: 180 of 180 replayed first NULLs match the logged ones. At the first NULL, the doable tool was already shown but not called in 51, 51 and 67 of 80. Ending at the m-th misstep trades the doable need against requests (a count). DRY (search withdrawn; shown tools in the dry app refused; end only when nothing is pending) kept Y at 30, 36 and 33 of 40 (no end rule: 32, 38, 34), cut substitutes from 14, 9, 9 to 5, 2, 4, saved 10-29% of requests; still at the backstop in 15, 2, 9 | DRY is the only candidate that survives the replay. A live run 5 (plain against DRY, about $1.40) is proposed, not started |

| 5 | e906aff, e697e2c | Human approved run 5 (INT-T-037): the only candidate that survived the replay, DRY, tested live against plain | 2,639 / $1.618 | Both present: no harm. Doable need 40→34, 36→34, 33→27 of 40 (more than the replay predicted). Substitutes 12→5, 4→1, 6→3; false claims 5→2, 0→0, 1→0. Backstop barely changed; guessed names rose; requests −8 to −19%. Y was lost mostly at the backstop, while the model guessed the missing tool's name | DRY is the best client-side rule found: deterministic, no count, fewer harmful actions, no harm when the tool exists. But no client-side rule makes these models stop searching for a missing tool. The lever left is the model (an instruction, or model choice). Lead recommends closing P3 |
| Note on run 5 | (next commit) | Human asked whether run 4 should be rerun without the repeated plain run | 0 / $0 | No rerun needed: that run would have been a subset of run 4. Run 4 plain, run 4 plainB and run 5 plain are three copies of the no-rule condition. For all three models DRY lies below the whole no-rule range on the doable need (37-40 / 36-40 / 30-33 against 34 / 34 / 27) and on substitutes (12-16 / 4-5 / 5-8 against 5 / 1 / 3); the backstop count varies too much to read | DRY's gain on substitutes and its small cost in doable needs are both very probably real (`RESULTS-P3-RUN5.md` section 1a) |
**Spend:** P3 total $9.404 of $10 (runs and smoke tests; per-run figures in the result files). $0.60 left.

## 3. Standing conclusions [I] (revised as runs come in)
1. Models search for a deferred tool without being told to (runs 1-2). For these models and tasks, deferral needs no
   instruction to search.
2. When the tool is missing, models do not stop on their own, and a message from the search tool does not stop them (runs 1-4).
3. A stop the client enforces does work, but over the whole session it costs the needs that could be done (run 4). Scoped to the
   app where nothing was found (DRY, run 5), it halves substitute actions at a small cost in doable needs. It still does not make
   models stop searching for a tool that does not exist (runs 2-5).
4. Substitute actions and false claims are model behaviour, not caused by the rules (runs 3-4). A search stop cannot prevent
   them; they need a separate safeguard on state-changing calls, which only the end-to-end study can score.

## 4. Open
- **Next:** the human decides on `RESULTS-P3-RUN5.md` section 3: (i) close P3 (lead's recommendation), or (ii) a last small instruction run within the $0.60 left.
- **Records for the operations branch:** P3 AUTH row (INT-T-028 to INT-T-036), WD entries, STATE pointer (`ops/OPEN-TASKS.md`).
- **Where the stop rule is tested:** P3, then the V5-R arm of the end-to-end study (`STOP-RULE-RESEARCH-20261108.md` section 5).
