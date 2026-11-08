---
type: summary
status: unverified (pages read through WebFetch, which returns a small model's summary, not the raw page; nothing stored in
  evidence/; numbers are as the summaries gave them unless marked [checked], which means the lead re-fetched the primary page
  and found the figure there; none of them may be cited as EXT before the page is stored and extracted)
---
# P3: how should a tool-search loop decide that nothing fits? (research note, 2026-11-08, revision 2)

- **Revision 1** (INT-T-033): the lead alone, 7 web searches and 6 fetches.
- **Revision 2** (INT-T-034): the human asked for an extensive search.
  - Six general-purpose web scouts ran in one round. Together they used 80 of 90 searches and 126 of 150 fetches.
  - The lead spot-checked eight claims against their primary pages (8 of 15 fetches).
  - The scout reports are in `stop-research-scouts-20261108/` (S1 to S6), copied as received. They are leads, not evidence.
- Stored sources re-read locally: CONVOLVE, AgentAbstain, ToolBeHonest, BFCL v3, Tool Attention, Anthropic tool search, Pydantic
  AI.
- No V5 rule changed.

## 1. What is known, in eight points [F as reported; I where marked]
1. **Nothing published tests a deterministic stop for a tool-search loop, per need or otherwise.** No tool-retrieval benchmark
   found has queries whose tool is absent from the catalogue. The named tool-retrieval systems (MCP-Zero, ScaleMCP, Dynamic
   ReAct, AnyTool, RAG-MCP, ToolGen, MassTool) leave the stop to the model, to a fixed cap, or to nothing (S1, S2, S6; "not
   found" in the places searched). **P3's question is open in the literature** [I].
2. **A stop works when the client enforces it; text does not.**
   - arXiv 2610.06191: after five useless results, "only the finish action remains". This raised success for every model, and
     prompts "change when they stop but not what they stop on".
   - **CGDP, arXiv 2605.07042 [checked]**: a programmatic gate. It fires when the query is similar to recent queries (Jaccard)
     AND the share of unseen retrieved items is low, for p consecutive rounds. It then "forces the agent to give a final answer".
     - On one setup it gave +16.2% accuracy and saved 39% of tokens; averaged over three agents it gave +1.1% to +6.9%.
     - LLM-judged gates did worse: "spirals into infinite loops" (−3.3% accuracy, +159% tokens) or "premature stopping" (−5.0%).
     - Its threshold values are in an appendix the fetch did not reach.
   - **CrewAI [checked]**: on the fourth identical call with the same result, a note to "give its final answer"; on the fifth,
     "CrewAI stops its tool use". Any changed call or result resets the count.
   - Pydantic AI's loop detector says its nudge can be ignored and should be paired with a hard limit; OpenHands halts on
     repeated action and observation (S3, S4).
   - The ladder "note, then hard stop" is the common design. It is measured only in 2610.06191 and CGDP.
3. **A result that replaces the search results with a refusal helps some models and not others.** "Search Engines Never Say No",
   arXiv 2610.05348 [checked]:
   - The refusal raised abstention on unanswerable questions from 23% to 97% (Qwen3-8B/32B) and 28% to 57% (Haiku 4.5). It beat
     a system-prompt instruction by 51 points on average.
   - Search-R1 ignored it and fabricated retrievals.
   - Sonnet 5.5 and Opus 5.5 rose only 2 points, but followed a system-prompt directive (+16).
   - [I] Our rule2 already had this form: the search result was replaced by the note. In tool search it stopped only 10 of 50
     sessions, which is weaker than in their QA setting. The effect depends on the model, so models must not be pooled.
4. **The trigger we have is reasonable; a BM25 score threshold is not.**
   - "Selection Is Retrieval, Abstention Is Not", arXiv 2609.18672 [checked]: on 70 actions, BM25 score features separate
     in-catalogue from out-of-catalogue requests at an AUC of at most 0.697, against 0.806 for a frozen encoder.
   - Counting raw novelty fails because each rewording surfaces some unseen item (S3). Our scope restriction (only tools of the
     best match's apps count as new) addresses that. In run 3 it fired in 50 of 60 target-absent sessions and 5 of 120
     target-present ones.
   - CGDP adds query similarity as a second condition.
5. **Why substitutes came after the note.** "When Guardrails Redirect", NeurIPS 2026 [checked]: when the requested target is
   excluded, the model can be redirected "to another executable but unrequested target". Excluding it "never reduces the
   wrong-target modification rate", while "strict request matching prevents all wrong-target modifications in the execution
   replay".
   - [I] Our note tells the model the requested action is unavailable, and the model redirects to a near miss. Run 3's logs
     agree: 0 substitutes before the first note, all after it.
   - A stop that leaves state-changing tools callable cannot prevent this. A forced reply can.
   - Request matching needs the requested action. In P3 that is the gold answer, so it can only be a scoring category there,
     not a mitigation. In deployment it would need intent extraction, which is not deterministic.
6. **False claims and our stub "Done".** "Fabrication After Tool Failure", arXiv 2609.14758 [checked]:
   - Dishonesty was 0.0% when the tool returns status:error and 45.3% when it returns status:ok with a bad value.
   - One sentence requiring `retrieval_status: OK or FAILED` cut it from 14.10% to 0.87%.
   - [I] Our stub answers every call with an ok-like "Done", which is their high-dishonesty condition. Requiring the flag is a
     prompt instruction, but checking it by regex is deterministic.
   - FTA (arXiv 2609.35732, unchecked) reports false success falling from 22.8% to 0.8% with a structured final report.
   - Both are prompt-side, so for P3 they would be a separate cell, not the stop rule.
7. **Evaluation designs to reuse** (S2, S6):
   - paired should-act / should-abstain tasks (AgentAbstain; our D and A cells already are such pairs);
   - False Continue Rate and the tokens of continuing against stopping (FeasiGen, arXiv 2605.28532; "up to 73.9%" [checked]);
   - ToolSandbox's "minefields", near-miss calls defined in advance. Our tasks already name a distractor for each target;
   - AppWorld's state diff and SABench's separate collateral-damage rate;
   - MCPHallu's Unreachable Goal tasks, where the average score is 0.458 and 23.2% pass [checked]. Its graded
     early-declaration score was not checked;
   - per-need labels instead of a prefix score.
8. **Per need:** the only per-subquery stops found use a trained verifier (HALT) or a planner (TOOLQP, PLUTo). None is
   deterministic. Scout 6's suggestion is to infer "threads" from the search stream (query similarity, or the app of the best
   match) and stop only a dry thread. **No source measures this** [I].

## 2. What run 3's logs add [O] (rule2, local logs, counts only)
- **Target absent:** in 0 of 50 sessions with the note was a state-changing call made before the first note; every substitute and
  every call to a guessed name came after it. The note arrived once in 17 sessions and more often in 33.
- **Target present:** the note fired in 5 of 120 sessions. In 3 of them the target had already been shown but was called only
  after the note.

## 3. Reading [I]
1. **Keep the trigger, change the enforcement.** The novelty signal within the matched apps is deterministic, needs no count, and
   fired where it should. What failed is the enforcement. A note, even one that replaces the results, leaves the decision to the
   model (points 2 and 3).
2. **The enforcement must remove the chance to act on a near miss** (point 5).
   - **Forced reply at the first note** (CGDP's form, and 2610.06191's) would have stopped every substitute in run 3. Its cost is
     the 3 of 120 target-present sessions that called a shown target after the note.
   - **Withdrawing only search_tools** keeps those 3, but leaves the near misses callable.
3. **Per need, a global stop has a predictable harm.** If the missing need is searched first, a global stop fires before the
   other need's tool is found. No source offers a tested per-need rule, so run 4 should measure that harm. Its logs (which apps
   each need's searches hit) are then the development data for a per-thread rule. That is how 2610.06191 and CGDP chose their
   parameters.
4. **The lead's withdraw idea was not taken from a source.** It turns out to match published designs (point 2). They differ in
   leaving only "finish" rather than the tools already shown.

## 4. Revised proposal for run 4 (for the human; not started)
- **Tasks:** 20 lead-written tasks over the same catalogue, each with two needs, in three kinds:
  - both tools present;
  - one tool absent, its need named first;
  - one tool absent, its need named second.

  Each need has a near-miss tool, a "minefield", fixed before the run. Values are given in the prompt, and results are stubs
  ("Done"), as before. That is a stated limitation (point 6).
- **Variants** (no prompt instruction in any; turn cap 12 as a backstop only):
  1. **plain**, run twice to measure the run-to-run flip rate;
  2. **note** (rule2 as in run 3);
  3. **stop-reply:** at the first note the result is a typed `{"status": "no_match"}` and the next request carries no tools, so
     the model must answer;
  4. **stop-search:** at the first note the same typed result, then search_tools is withdrawn and call_tool stays for tools
     already shown.
- **Scoring per need:**
  - feasible need: done, cut off by the rule, or not attempted;
  - absent need: honest decline, substitute (minefield or another state-changing call), false claim, or still searching at the
    backstop.
- **Also reported:** paired accuracy over the kinds; requests and tokens after the first note; per model, exact McNemar on
  discordant tasks. At 20 tasks only large effects show: at least 6 tasks changing one way are needed for p < 0.05.
- **Cost:** 5 runs of variants × 60 task-kinds × 3 models = 900 sessions, about $2.7 to $3.6, inside the $5.84 left. Without
  the repeated plain run, about $2.2 to $2.9.
- **Not in run 4:**
  - a per-thread rule, to be designed from run 4's logs;
  - a structured final-status cell, which is prompt-side (point 6);
  - request-bound execution gates, which need the gold answer in P3 (point 5).

## 5. Where the stop rule is tested (the human's question) [I]
- **P3:** run 4 above. `05` already places the no-match rule in P3 as a recovery option.
- **End-to-end study:** the rule becomes part of V5-R's deferral stage, and its effect on success and requests per turn is
  measured in the V5-R arm. The vehicle would be AppWorld's real multi-step tasks:
  - with the needed APIs masked as FeasiGen does (point 7), paired with the unchanged task;
  - AppWorld's state checks would score substitutes as collateral damage;
  - its real results remove the stub "Done" (point 6).

  The task set is the human's choice (`05` section 3).
- **Not P1, P2 or P5.**
  - P1 uses whatever rule P3 leaves; P2 has no search.
  - The requests spent on no-match searching (run 3: 7.3 to 9.5 per session in cell A against 3.6 to 3.9 in D) are an input to
    the bill. Whether D-01 carries such a term is the human's decision after part A (INT-T-027).
