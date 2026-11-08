# Draft records for the operations branch (lead, 2026-11-08; INT-T-040)

**What this is.** These are ready-to-apply drafts for the operations branch `linux-from-v5-audit--portable-guard-and-short-state`. They
are written on `v5-p5-break-even` because the shared folder is not free (`ops/OPEN-TASKS.md` section 1), and nothing is written
there from this branch.
- **Not an authorization, and not a record yet.** The authorizations are the human's words in the intake records cited below.
  Applying this file only copies them into the operations-branch files in that branch's format.
- **Formats** follow that branch as read on 2026-11-08 (read-only `git show`, head `22e3d7d`):
  - `ops/AUTHORIZATIONS.md`: table row, then a "verbatim human text" section with the lead's record;
  - `ops/DESIGN-DECISIONS.md`: `## WD-0NN title (date)` with bullets;
  - `ops/STATE.md`: at most 40 lines and 6 KB.
- **The human's words** below are copied programmatically from the intake records (verbatim body and its sha256 prefix), not
  retyped.

**How to apply (when the shared folder is free):**
1. Rebase or check that ids AUTH-029, AUTH-030 and WD-071 to WD-075 are still free on the operations branch. If not, renumber
   here first.
2. Add the rows and sections of part 1 to `ops/AUTHORIZATIONS.md`, and the entries of part 2 to `ops/DESIGN-DECISIONS.md`.
3. Replace section A of `ops/STATE.md` with part 3; copy `ops/OPEN-TASKS.md` across.
4. Run the full verifier and the guard tests on that branch (STATE section D lists them). Commit there; the human pushes.

## Part 1. `ops/AUTHORIZATIONS.md`

### 1a. Amendment to AUTH-028 (append to its row's route cell and to its verbatim section)
Row text to append: **Amended 2026-11-07 (INT-T-026):**
- Part A on ScaDS GLM-5.3: the cap is raised to about 140 requests (free). It still waits until the GLM B2 run has ended,
  because the API might be overloaded.
- OpenAI side check: repeated with harness revision 2 (forced cold starts, 2 cold and 1 warm session per cell). Accepted at about
  $0.40 with a stop at $0.60. Actual: 193 requests, $0.445; the OpenAI side check cost $0.594 in all.
- **INT-T-027:** D-01 stays the working equation. The hosted-search variant in `calc/regime_bill_hosted.py` stays a proposal, and
  the revision is decided after part A.

Verbatim section to append:
**INT-T-026** (`requirements/intake/2026-11-07-user-p5-cap-and-openai-repeat.md`, body sha256 `66242f1b2946...`):
> 1. yes i cannept raiing the cap, but wait if GLM is still running we should wait bec the api might be overloaded.
> 2. i accept it

**INT-T-027** (`requirements/intake/2026-11-07-user-d01-variant-deferred.md`, body sha256 `3e4e7b41bc5b...`):
> except the port A capping, and the state, yeah, is okay also, but the DO1 variant, I'm not sure, should we put it, because it's also, why did you change the equation? Are we sure that this would be the new equation, or we can return back to the old one if we want? This is just a question. I'm not telling you that what you have done is wrong or right.
>
> I agree

Lead's record (not the human's words): in INT-T-026, "cannept raiing the cap" is read as "accept raising the cap". The other
readings are in the caveats of each intake record.

### 1b. New row AUTH-029: loop item P3 on OpenRouter (2026-11-07 to 2026-11-08; closed)
| AUTH-029 | human | **Scope:** loop item P3 of `design/package-v5/05` (HYP-0019: do models search for a deferred tool uninstructed?), extended by the human to a stop for a missing tool that is dynamic and deterministic, not a number of turns (INT-T-031). Lead-written tasks over AppWorld's real function-calling definitions; stub tool results. **Route:** OpenRouter only for P3 and later items, not for B2 (INT-T-028, INT-T-029). **Models:** MiniMax-M3, DeepSeek-V4.1-Flash and GLM-5.3, all on GMICloud fp8 pinned, no fallbacks (INT-T-030). **Budget:** a $10 stop for all of P3 (INT-T-029); for run 6 the human accepted going over it, with the lead's ceiling of $10.60 (INT-T-038). Actual total: $9.953. **Runs:** 1 (cells E, D, A, W; INT-T-028..030); 2 (no-match rule; INT-T-031); 3 (revised rule; INT-T-032); 4 (two-need tasks; INT-T-035); 5 (DRY; INT-T-037); 6 (DRY plus instruction; INT-T-038). Also a log replay at no cost (INT-T-036). **Research:** the lead's search (INT-T-033), then six web scouts (INT-T-034, the lead's bounds of 90 searches and 150 fetches). **Data:** AppWorld text, tool names and logs stay local and git-excluded; only counts are committed. Keys come only from the environment. **Closed** by the human on 2026-11-08 (INT-T-039): V5-R17 added to `04`, provisional. **Not covered:** P1, P2 and P4 runs; the end-to-end study; any policy parameter beyond V5-R17. | 2026-11-07 | Branch `v5-p5-break-even`, commits 8632475 to 7da7380; record `design/package-v5/inputs/p3/P3-LOG.md` | INT-T-028..039 (verbatim below) |

Verbatim section "AUTH-029 verbatim human text (messages of 2026-11-07 and 2026-11-08)":
**INT-T-028** (`requirements/intake/2026-11-07-user-openrouter-for-p3.md`, body sha256 `98a78d0b9b98...`):
> opoenrouter is in the .env you asked for, but if we will rerun p5 part A on scads after wards then start for openrouter for p3 and others that needs openrouter or to finsh its task

**INT-T-029** (`requirements/intake/2026-11-07-user-p3-choices.md`, body sha256 `f099e4dc2f14...`):
> "Which tasks should P3 (do models search for a hidden tool without being told) use? AppWorld is already installed locally in ~/r3-work."="Built tasks, real tools (Recommended)"
> "What spending limit should P3 on OpenRouter have? My estimate is about $1-2 per model for about 160 requests, before I have read the real prices."="Stop at $10 total"
> "Which models should P3 run on through OpenRouter (one provider pinned per model)?"="You pick after the listing"
> "You wrote 'others that need openrouter or to finish its task'. Did you mean the other agent's GLM B2 run should finish on OpenRouter instead of the stalled ScaDS?"="No, just P3 and later items"

**INT-T-030** (`requirements/intake/2026-11-07-user-p3-models.md`, body sha256 `ca874d9ba2ac...`):
> "Which models should P3 run on (OpenRouter, provider pinned, $10 stop in total)? Each would first run 1 task (7 sessions) as a smoke test, then all 20 tasks (140 sessions). Estimates assume about 3M prompt tokens and 0.2M output per model; ranges are 'cache works' to 'no cache'."="GLM-5.3 + MiniMax-M3 + DeepSeek (Recommended)"

**INT-T-031** (`requirements/intake/2026-11-07-user-p3-dynamic-stop-and-run2.md`, body sha256 `221694e5fe52...`):
> yes i agree on both what you asked me about but the stopping condition must noot be x number of turns it should be dynamic will you give the agent the stoping condition to go to when really no tool is found or you will think of sth dynamic but detereminstic. and p33 may have a second run yes

**INT-T-032** (`requirements/intake/2026-11-07-user-p3-run3.md`, body sha256 `d3990ba1c601...`):
> leave b2, NOOW YOU GO Run 3 with the revised rule? and Tasks that need several tools, now or later?

**INT-T-033** (`requirements/intake/2026-11-08-user-stop-research.md`, body sha256 `fb49e9934508...`):
> i accept the order and i authorize the researc, and would add that you should check where in what expeeremient we should test that stop rule. also make sure you mind that other agents and GLM is still working and accessing this repo donot do sth stupid

**INT-T-034** (`requirements/intake/2026-11-08-user-extensive-stop-research.md`, body sha256 `de0634e6473d...`):
> before we go ahead why do i feel you didnot search extensivly well, you have the ability to run sonnet 5.5 subagents and do extensive reserach please did you do so? if not then do so

**INT-T-035** (`requirements/intake/2026-11-08-user-run4-go.md`, body sha256 `4f5d16860e88...`):
> i agree on run 4 but idk should we do it with or without or by which we may start by i agree on costs too

**INT-T-036** (`requirements/intake/2026-11-08-user-choose-a-and-document.md`, body sha256 `eca96377e5cc...`):
> i choose a
>
> but i want to make sure that you are documenting our runs and decisionsnad reasons and resuls and conclusion etc!

**INT-T-037** (`requirements/intake/2026-11-08-user-run5-go.md`, body sha256 `ab6871173850...`):
> yes go ahead with run 5

**INT-T-038** (`requirements/intake/2026-11-08-user-run6-instruction.md`, body sha256 `91a7f748e190...`):
> go with ii on minimax and deepseek and GLM if possible i accept the costs

**INT-T-039** (`requirements/intake/2026-11-08-user-close-p3.md`, body sha256 `ebe0f0272b67...`):
> yes close P3 that way

Lead's record (not the human's words): P3 was authorized message by message, not in one draft. Each message's reading is in the
`caveats` field of its intake record. P3-LOG section 1 lists them, and section 2 lists what each run did under them.

### 1c. New row AUTH-030: group 1 and P2 preparation (2026-11-08)
| AUTH-030 | human | **(1) Group 1:** draft the operations-branch records (this file) and update `design/package-v5/12` (P3 done; P2's route). **(2) Prepare P2** (`05` P2, HYP-0018: does offering a subset at a fixed cached prefix keep accuracy nearly the same?): design, harness and cost estimate. **No model request**; a P2 run needs its own authorization with its cost. **(3) Web searches** on anything needed for this work; every search and fetch is recorded in the P2 preparation file and cited with URL and date. **Waiting for the human's word after group 1:** the other group 2 items (P3 sources stored as EXT; end-to-end task preparation; P1 preparation). Work in detail, systematically and scientifically. | 2026-11-08 | Branch `v5-p5-break-even` | INT-T-040 (verbatim below) |

Verbatim section "AUTH-030 verbatim human text (message of 2026-11-08)":
**INT-T-040** (`requirements/intake/2026-11-08-user-group1-and-p2-prep.md`, body sha256 `33a22aabfcfc...`):
> do group 1 now and prepare P2 then i authorize group 2 after fully completing group one but focus in details and be systematic and sceintific i even authorize you to search on anything needed while working since evice and citing it eolicilty is important

Lead's record (not the human's words): "evice" is read as "evidence" and "eolicilty" as "explicitly". "then i authorize group 2 after
fully completing group one" is read as a future authorization, so only P2 preparation is covered now.

## Part 2. `ops/DESIGN-DECISIONS.md`

## WD-071 P5 part B results; D-01 kept until part A (2026-11-07)
- **OpenAI side check** (AUTH-028; `design/package-v5/inputs/p5/RESULTS-P5-B.md`, repeat with harness revision 2): 193 requests,
  $0.445, accepted at about $0.40 with a stop at $0.60 (INT-T-026). The OpenAI side check cost $0.594 in all.
- **Bills:**
  - Individually deferred functions still bill 30% of their tokens; namespaces bill 3.6%.
  - Deferral against eager, cold start: 1.19 / 0.70 / 0.44 / 0.35 (functions) and 1.12 / 0.67 / 0.29 / 0.11 (namespaces) at 10,
    30, 100 and 300 tools.
  - Break-even is between 10 and 30 tools. A warm start shrinks deferral's advantage.
- **D-01 as written misses this route by more than the run-to-run spread** (2.2 to 7.9 times at 100 to 300 tools), so the
  AUTH-028 stop rule applied and it was reported. D-01's formula with the measured parameters reproduces the cells within 0.01
  to 0.07 at 30 to 300 tools.
- **The human (INT-T-027):** keep D-01. The hosted-search variant (`calc/regime_bill_hosted.py`) stays a proposal until part A.
- **This is not P5's test:** part A, on ScaDS with client deferral, waits for GLM B2 to end (cap about 140 requests, INT-T-026).

## WD-072 P3 runs 1-3: models search uninstructed; tool-side notes do not stop them (2026-11-07 to 2026-11-08)
- **AUTH-029.** Harness `tools/p3_uninstructed_search.py`; analysis `tools/p3_analyze.py`; results `inputs/p3/RESULTS-P3-RUN1.md`
  to `RUN3.md`.
- **Run 1** ($1.56, plus a $0.115 smoke test):
  - With the target deferred and no instruction to search, all three models searched in every session and called the target in
    19-20 of 20, as with all tools exposed. HYP-0019's falsifier is not met on this set.
  - With the target absent, 12-17 of 20 sessions were still searching at the 6-request cap.
- **Run 2** ($1.755): a no-match rule with an app listing cut runaway searching, but doubled or tripled substitute actions. Not
  recommended.
- **Run 3** ($0.726): the revised rule (rule2, novelty within the best-match apps, note only) did no harm, but stopped only 10 of
  50 sessions after the note. Run 2's attribution of the false claims to the listing was corrected.

## WD-073 P3 research, two-need run 4 and log replay (2026-11-08)
- **Research** (INT-T-033, INT-T-034; `inputs/p3/STOP-RULE-RESEARCH-20261108.md` revision 2 and six scout reports, unverified
  leads; 8 claims checked against primary pages):
  - no published deterministic stop for tool-search loops;
  - client-enforced stops work where text does not (arXiv 2610.06191, CGDP 2605.07042);
  - excluding the requested action redirects models to another (When Guardrails Redirect);
  - a "Done" stub matches the high-dishonesty condition (2609.14758).
- **Run 4** ($3.630 with smoke; two-need tasks; plain twice, note, stopreply, stopsearch):
  - A session-wide forced reply lost the doable need in 40-80% of tasks (p ≤ 0.016 in all six cells).
  - Withdrawing search kept the doable need but did not end the loop.
  - Substitutes and MiniMax's false claims occur with no rule.
- **Replay** ($0, INT-T-036; `RESULTS-P3-REPLAY-A.md`):
  - At the first NULL the doable tool was already shown but not called in 51, 51 and 67 of 80 sessions.
  - Of the candidates, only DRY (refuse calls into the dry app; end when nothing is pending) survived.

## WD-074 P3 runs 5-6 and closure: V5-R17 provisional (2026-11-08)
- **Run 5** ($1.618, DRY against plain):
  - Substitutes 12 / 4 / 6 to 5 / 1 / 3 of 40, and false claims 5 / 0 / 1 to 2 / 0 / 0.
  - The doable need fell 40 / 36 / 33 to 34 / 34 / 27, below the range of three no-rule copies.
  - The loss came from models guessing the missing tool's name until the backstop.
- **Run 6** ($0.549, DRY plus one sentence in the system text):
  - Doable need 40 / 39 / 37 of 40.
  - Backstop 3 / 0 / 1; guessed names 2 / 1 / 0.
  - Requests 32-48% below no rule.
  - Substitutes 7 / 1 / 2, false claims 3 / 0 / 0; no harm with both tools present.
- **The human closed P3** (INT-T-039).
  - V5-R17 was added to `04` (OURS, provisional), with open items: an instruction-only arm; withdrawing search_tools changes the
    tools array, against V5-R02; MiniMax's residual substitutes and false claims as an input to model choice.
  - `05` gained the end-to-end arm; `06` gained the traceability row.
- **P3 spend: $9.953.** Record: `inputs/p3/P3-LOG.md`.

## WD-075 Group 1 and P2 preparation started (2026-11-08)
- The human asked for group 1 (these drafts; the update of `12`) and P2 preparation, with web searches as needed and explicit
  citations (INT-T-040).
- No P2 request is sent. A run needs its own authorization with its cost.

## Part 3. `ops/STATE.md` section A (replacement; keep the file under 40 lines and 6 KB)
- **V5 audit** (AUTH-020) is a conceptual package. Start at `design/package-v5/00-README.md`. Working draft V5-R = DPR-0007 plus
  V5-R17 (provisional). Nothing is validated, approved or final. The benchmark register is `17`.
- **Probes R1-R3 done** (results `exchange/prior-work/v5-probes/results/`). (Keep the existing bullet.)
- **Running:** GLM-5.3 on ScaDS (AUTH-026, free): B2 running, then stop.
- **P5** (AUTH-028, amended INT-T-026/027): part B (OpenAI side check) done, $0.594 (`inputs/p5/RESULTS-P5-B.md`). Part A
  (ScaDS GLM-5.3, cap about 140) waits for B2 to end. D-01 is kept until part A.
- **P3 closed** (AUTH-029, 2026-11-08): six runs on OpenRouter, $9.953 (`design/package-v5/inputs/p3/P3-LOG.md`). Models search
  uninstructed; V5-R17 adds a stop for a missing tool, provisional.
- **P2 preparation** (AUTH-030): design, harness and cost estimate; no requests.
- **The lead's to-do list:** `ops/OPEN-TASKS.md` (not an authorization).
- (Keep the existing bullets on the questions guide, the supervisor and the thesis question.)
