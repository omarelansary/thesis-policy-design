---
type: summary
status: unverified (pages read through WebFetch, which returns a small model's summary, not the raw page; nothing stored in
  evidence/; numbers below are as the summaries gave them and must be checked against the papers before any of them is cited)
---
# P3: how should a tool-search loop decide that nothing fits? (research note, 2026-11-08)

Covered by INT-T-033 (the human authorized the research; at most 10 web searches and 20 page fetches, the lead's bound). Used:
**7 searches, 6 fetches** (one PDF did not decode). Stored sources re-read locally: CONVOLVE (`v5-convolve-2606.28733`),
AgentAbstain (`arxiv-2607.10059`), ToolBeHonest (`arxiv-2406.20015`), BFCL v3 multi-turn (`web-bfcl-v3-multi-turn-blog`),
Tool Attention (`v5-xp-arxiv-2604.21816`), Anthropic tool search, Pydantic AI tools. No V5 rule changed.

## 1. What was found
| Source | What it says (as read) | Bearing on P3 |
|---|---|---|
| **"Judged Useless, Queried Anyway"**, arXiv 2610.06191 (new) | Seven agents call a failing source's results useless 97-100% of the time, yet rarely stop on that; "Prompt cues change when they stop but not what they stop on". **A harness rule** (after five consecutive results the agent judged useless, "only the finish action remains") raised success on failing sources for every model; non-inferior where the source works in 18 of 20 tests; k = 5 tuned on development data; a lexical detector in place of the agent's judgment was a control ("the gain comes from acting on an accurate signal"). HotpotQA and FEVER retrieval, not tool search; 7-8B open models plus Claude Haiku 4.5 and Sonnet 5 | The closest evidence for P3's problem: **the stop has to be enforced by the client; a note or a prompt does not do it.** Matches run 3 (the note reached 50 of 60 sessions; only 10 then stopped searching). Its trigger is a count (k = 5) of useless results, not of turns |
| **CONVOLVE / "Agentic Abstention"**, arXiv 2606.28733 (stored) | "Some agents never abstain when they should, while others do so only after many unnecessary interactions"; stopping rules distilled from past trajectories and put in the context raise Llama-3.3-70B's timely recall from 26.7 to 57.4 (WebShop) | Names our failure ("timely" abstention). Its remedy is in the prompt and learned per deployment, so it mixes with P3's question; possible later cell, not the rule |
| **AgentAbstain**, arXiv 2607.10059 (stored) | Paired should-act / should-abstain tasks; best model 59.5% paired accuracy; "post-hoc abstention where agents first commit irreversible actions, and then claim refusal"; no search channel | Our D and A cells are already such pairs on the same 20 tasks: **report paired accuracy** (target called in D and a safe, honest reply in A). The post-hoc pattern is our substitute-then-"couldn't" |
| **Cost-aware stopping for tool acquisition (CAM-DF)**, arXiv 2607.27083 (new) | A learned logistic stop over a score-ranked tool list (stop at the first depth with p >= 0.5); 37% fewer tools exposed at comparable success on tau-bench Retail; needs labelled required-tool sets for training; does not discuss "no tool fits" | A retrieval-depth stop, not a search-loop stop; needs training data. Not for now |
| Tool Attention, arXiv 2604.21816 (stored) | Similarity threshold calibrated once per deployment on 100-200 held-out (query, tool) pairs, maximising F1 | The `05` "score threshold" route: workable with a dense encoder and calibration data; BM25 scores are not comparable across queries, so not with our ranker |
| ToolBeHonest, arXiv 2406.20015 (stored) | Unsolvable tasks built by removing a needed tool (Missing Necessary Tools) or giving tools that cannot fully do the job (Limited Functionality Tools); models degrade most on LFT | LFT is our near-miss substitute case. **Removing one needed tool from a real multi-step task** is a ready construction for the end-to-end test |
| BFCL v3 missing functions (stored) | Withholds functions; a turn is force-terminated after more than 20 steps | A count backstop, like our 12 |
| OpenAI tool search guide (fetched); Anthropic tool search (stored) | OpenAI says nothing on no-match or limiting repeated searches; Anthropic returns an empty result, not an error | Vendors leave the stop to the application |
| Rust agent crates (agent-base, phi-agent) | Stop after max consecutive failures of the same tool | A count pattern for hard errors only; nothing on empty results |
| Searches for partially infeasible multi-step tasks | No benchmark found that scores "finish the feasible parts and report the impossible one" (PlanBench-XL and E-Bench come closest) | Run 4 would measure something the found benchmarks do not |

## 2. What run 3's logs add [O] (variant rule2, local logs, counts only)
- **Target absent:** in 0 of 50 sessions with the note was a state-changing call made before the first note; every substitute
  action and every call to a guessed name came after it (4, 8 and 8 sessions). The note arrived once in 17 sessions, more often
  in 33.
- **Target present (D, W):** the note fired in 5 of 120 sessions; in 3 of them the target had already been shown but was
  called only after the note.

## 3. Reading [I]
1. **The stop must be enforced by the client** (2610.06191; run 3). The human's requirement, dynamic and deterministic, can keep
   the signal we have (rule2: nothing unseen in the matched apps), which is deterministic and needs no count.
2. **The trade-off is in what the enforcement leaves callable.**
   - **Forced reply at the first note:** only answering remains. Run 3's logs say this would have stopped every substitute in
     cell A. It would also have cut off the 3 of 120 target-present sessions that called a tool already shown after the note.
   - **Search withdrawn at the first note, shown tools still callable:** keeps those 3. It ends runaway searching, but the
     substitutes are also shown tools, so it may not prevent them.

   The client cannot tell a shown target from a shown near miss, so only a run can say which matters more.
3. **Per need, not per session.** A task with two needs may hit the note on the missing need before the other need's tool has
   been found. A forced reply then loses the feasible need; withdrawn search may too. This is why the multi-need run comes
   before any choice.
4. The lead's earlier idea (withdraw search_tools) has, in the literature, the form "only finish remains after the stop
   signal". It was not taken from there; the lead found the paper afterwards.

## 4. Proposal for run 4 (for the human; not started)
- **Tasks:** new lead-written tasks over the same catalogue, each with two needs, in three kinds: both tools present; one present
  and one absent with the absent need named first; the same with it named second. Values in the prompt, stub results as before.
- **Variants:** plain; rule2 (note only); stop-reply (forced reply at the first note); stop-search (search withdrawn at the first
  note, shown tools still callable). No count, no prompt instruction; cap 12 as a backstop only.
- **Measures per need:** feasible need done; absent need: no substitute, no false claim, said so. Also paired accuracy over the
  three kinds, requests, and backstop hits.
- **Cost:** about $2 to $3 for three models, inside the $5.84 left; within the $10 stop.

## 5. Where the stop rule is tested (the human's question) [I]
- **P3 (the loop item):** `05` already puts the no-match rule in P3 as a recovery option. Run 4 is that test: mechanism and large
  effects only, about 20 tasks, stub results.
- **End-to-end study:** the rule becomes part of V5-R's deferral stage, so its effect on success and on the bill (requests per
  turn) is measured in the V5-R arm. The proposed vehicle is AppWorld's real multi-step tasks with one needed API removed (the
  ToolBeHonest construction), paired with the unchanged task (the AgentAbstain design). AppWorld's state checks would catch
  substitute actions, and its real results remove the stub "Done" that makes false claims easy. The task set is the human's
  choice (`05` section 3).
- **Not P1, P2 or P5.**
  - P1 runs on deferral and so will use whatever rule P3 leaves, but it does not test it.
  - P2 has no search.
  - The requests that no-match searching costs (run 3: 7.3 to 9.5 per session in cell A against 3.6 to 3.9 in D) are an input to
    the bill. Whether D-01 should carry such a term is a question for the human after part A (INT-T-027), not a P5 change.
