"""Apply the operations-branch records (INT-T-045) to a worktree of linux-from-v5-audit--portable-guard-and-short-state.
The human's words are copied from the intake records on v5-p5-break-even (verbatim body and its sha256 prefix), never retyped.
Usage: python3 ops/drafts/apply_ops_records.py WORKTREE_ROOT   (run from the v5-p5-break-even checkout)
Writes: ops/AUTHORIZATIONS.md (AUTH-028 amendment; AUTH-029, AUTH-030, AUTH-031 rows and verbatim sections),
ops/DESIGN-DECISIONS.md (WD-073 to WD-081), ops/STATE-ARCHIVE.md (the current STATE verbatim), ops/STATE.md (rewritten within
40 lines and 6 KB), ops/OPEN-TASKS.md (copied). Refuses to run twice (checks that AUTH-029 is absent).
"""
import glob, hashlib, os, re, sys

WT = sys.argv[1]
SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BODY = {}
for f in glob.glob(os.path.join(SRC, "requirements/intake/2026-11-0[78]-user-*.md")):
    s = open(f, encoding="utf-8").read()
    i = re.search(r'id: "([^"]+)"', s).group(1)
    b = re.search(r"<<<BEGIN-VERBATIM\n(.*)\nEND-VERBATIM>>>", s, re.S).group(1)
    sha = re.search(r'body_sha256: "([0-9a-f]+)"', s).group(1)
    assert hashlib.sha256(b.encode("utf-8")).hexdigest() == sha, f"{i}: body hash mismatch"
    BODY[i] = (b, os.path.relpath(f, SRC), sha)


def verb(i):
    b, f, sha = BODY[i]
    return f"**{i}** (`{f}` on `v5-p5-break-even`, body sha256 `{sha[:12]}...`):\n" + "\n".join("> " + l if l else ">" for l in b.split("\n")) + "\n"


def first_line(i, n=140):
    b = BODY[i][0].replace("\n", " ").replace("|", "/")
    if len(b) <= n:
        return b
    return b[:n].rsplit(" ", 1)[0] + " ..."


A = os.path.join(WT, "ops/AUTHORIZATIONS.md")
auth = open(A, encoding="utf-8").read()
assert "| AUTH-029 |" not in auth, "already applied"
lines = auth.split("\n")
k = next(i for i, l in enumerate(lines) if l.startswith("| AUTH-028 |"))
cells = lines[k].split(" | ")
assert len(cells) == 6
cells[4] += (" **Amended 2026-11-07 (INT-T-026):** part A's cap raised from about 100 (94 planned, WD-070) to about 140 requests (the lead's reading of \"cannept raiing the cap\", see below); part A waits until GLM B2 has ended; "
             "the OpenAI side check repeated with harness revision 2, accepted at about $0.40 with a stop at $0.60 (actual: 193 requests, "
             "$0.445; OpenAI side check $0.594 in all). **INT-T-027 (2026-11-07), the lead's reading** (the human asked about the "
             "equation, then wrote \"I agree\"): D-01 stays the working equation; the hosted-search variant stays a proposal until part A. **INT-T-041 (2026-11-08):** the human allowed the lead to run part A (per the lead's "
             "record below, the lead's own start had been refused by the auto-mode permission classifier); part A ran 2026-11-08, 138 requests, free (`RESULTS-P5-A.md` "
             "on `v5-p5-break-even`). **INT-T-043 (2026-11-08):** the human: \"keep D-01 and add the hosted variant\"; the lead's "
             "wording: D-01 kept as the working equation and the hosted variant adopted as D-01h, a separate mode for vendor-hosted search "
             "(the lead's reason, not the human's: D-01 fits the client route).")
cells[5] = cells[5].rstrip(" |") + "; amendments INT-T-026, INT-T-027, INT-T-041, INT-T-043 (verbatim in the AUTH-028 amendment section) |"
lines[k] = " | ".join(cells)
rows = [
    "| AUTH-029 | human | Loop item P3 of `design/package-v5/05` (HYP-0019: do models search for a deferred tool without being told to?), "
    "extended on the human's request (INT-T-031) to a stop for a missing tool that is dynamic and deterministic, not a number of turns; lead-written "
    "tasks over AppWorld's real function-calling definitions, stub tool results; six runs, a stop-rule research step and a log replay. "
    "**Closed** by the human on 2026-11-08 (INT-T-039): V5-R17 added to `04`, provisional. | 2026-11-07 | Route OpenRouter for P3 and "
    "later items, not for B2 (INT-T-028, INT-T-029); models MiniMax-M3, DeepSeek and GLM-5.3 (INT-T-030: the human chose the lead's "
    "recommended set); the provider GMICloud fp8, no fallbacks and the DeepSeek-V4.1-Flash id were the lead's choices from the OpenRouter "
    "listing (INT-T-029: \"You pick after the listing\"); a $10 stop for all of P3 (INT-T-029), for run 6 the human accepted going over it, lead's ceiling $10.60 (INT-T-038); "
    "actual total $9.953. Research: the lead's search (INT-T-033, 7 searches), then six web scouts within the lead's bounds of 90 searches "
    "and 150 fetches (INT-T-034). AppWorld text, tool names and logs local and git-excluded; counts only committed; keys only from the "
    "environment. Not covered: P1, P2 and P4 runs; the end-to-end study; any policy parameter beyond V5-R17. Record: "
    "`design/package-v5/inputs/p3/P3-LOG.md` on `v5-p5-break-even` (commits 8632475 to 7da7380). | \"" + first_line("INT-T-028") +
    "\" and INT-T-029 to INT-T-039 (verbatim in the AUTH-029 section) |",
    "| AUTH-030 | human | **(1) Group 1:** draft the operations-branch records and update `design/package-v5/12` (P3 done; P2's route). "
    "**(2) P2 preparation** (`05` P2, HYP-0018): design, harness and cost estimate, no model request. **(3) Web searches** on anything needed "
    "for this work, each recorded and cited. **(4) Group 2** after group 1 (INT-T-040: \"then i authorize group 2 after fully completing "
    "group one\"; group 1 done at 385237a; its contents were defined by the lead in its list of 2026-11-08, not in the human's words): "
    "end-to-end task preparation, P1 preparation, and the P3 sources stored as EXT. No later message of the human says \"go\" for "
    "group 2; the lead started it after group 1 on its own reading (lead's record below). **(5) Applying the records** on this branch "
    "(option (a) of INT-T-042, quoted under AUTH-031; INT-T-045: \"yes its free aplly the records\"), with a review by several Sonnet 5.5 "
    "subagents in more than one round (INT-T-045). | 2026-11-08 | "
    "Preparation sends no model request; a run needs its own authorization with its cost. Searches and fetches are logged in the file they "
    "support. AppWorld data stay local; counts only committed. This branch is written only after the human's \"its free\" (INT-T-045), "
    "in a separate git worktree (the lead's precaution, so jobs running in the research checkout are not disturbed); the human pushes. | \"" + first_line("INT-T-040") + "\" and INT-T-045 (verbatim in the AUTH-030 section) |",
    "| AUTH-031 | human | P2 runs. **Pilot** (INT-T-041: \"run P5 and p2 parallel\", read by the lead as the pilot it proposed: 5 dev "
    "tasks, arm `all`, gpt-5-mini and gpt-5.4-mini). **Main run A and B** (INT-T-042: \"i agree on P2 main A and B\"; the arms `all`, `enf`, "
    "`instr`, `drop`, the 30 AppWorld dev tasks, 2 repeats and the Responses API are the lead's proposal in RESULTS-P2-PILOT). **P2b** "
    "(INT-T-044: \"run P2b\"; `all` against `instr` on ScaDS `zai-org/GLM-5.3`, the same tasks, 2 repeats, as the lead proposed). | 2026-11-08 | Pilot stop $2 and main-run "
    "per-model caps $6 and $11 are the lead's figures (P2-DESIGN.md; the caps sum to about 1.5 times the estimate of about $11.6 that INT-T-042 "
    "approved); costs watched and reported to the human run by run (INT-T-042: \"watch both costs as it go so i can topup\"). Actual: pilot "
    "$0.316, main run $12.377, P2 total $12.693. P2b free, paced at one call per 31 s for ScaDS's limit of 2 requests per minute. "
    "Keys only from the environment; AppWorld text and tool names local; counts only committed. Results: `design/package-v5/inputs/p2/` on "
    "`v5-p5-break-even`. | \"" + first_line("INT-T-042") + "\", INT-T-041, INT-T-044 (verbatim in the AUTH-031 section) |",
]
lines[k + 1:k + 1] = rows
auth = "\n".join(lines).rstrip("\n") + "\n"
auth += ("\n## AUTH-028 amendments, verbatim human text (messages of 2026-11-07 and 2026-11-08)\n" + verb("INT-T-026") + "\n" + verb("INT-T-027")
         + "\n" + verb("INT-T-041") + "\n" + verb("INT-T-043") +
         "\nLead's record (not the human's words): in INT-T-026, \"cannept raiing the cap\" is read as \"accept raising the cap\". In INT-T-027 "
         "the human first accepted the part A cap and the state (\"except the port A capping, and the state, yeah, is okay also\"), then "
         "asked whether the old equation can be restored, said it was only a question, and wrote \"I agree\" after the lead's recommendation; "
         "the lead reads \"I agree\" as agreement with its proposal that D-01 stays and the hosted variant waits for part A; INT-T-043 later settled the matter. "
         "INT-T-041's "
         "\"i allow you too run it\" refers to the part A command the lead had given after its own start was refused by the permission "
         "classifier. Other readings are in each intake record's `caveats`.\n")
auth += "\n## AUTH-029 verbatim human text (messages of 2026-11-07 and 2026-11-08)\n" + "\n".join(verb(f"INT-T-0{n}") for n in range(28, 40))
auth += ("\nLead's record (not the human's words): P3 was authorized message by message, not as one draft. In INT-T-029 and INT-T-030 only "
         "the text after each \"=\" is the human's choice; the text before it is the lead's question with its options, and \"(Recommended)\" is "
         "the lead's label; INT-T-029's \"You pick after the listing\" left the provider and the model ids to the lead. INT-T-031 asked for a stop that is not a number of turns and left its form to the lead (\"will you give the agent "
         "the stoping condition ... or you will think of sth dynamic but detereminstic\"); the client-side deterministic stop is the lead's "
         "choice, and \"p33\" is read as \"P3 run 2\". INT-T-035 is read as approval of run 4 and its cost, with the repeated plain run left to "
         "the lead, who chose it. INT-T-032 (\"NOOW YOU GO Run 3 with the revised rule?\") is read as an instruction to run run 3. INT-T-036 "
         "\"a\", INT-T-038 \"ii\" and INT-T-039 \"that way\" refer to the lead's own options: (a) a per-need rule designed by replay on run 4's "
         "logs; (ii) DRY plus one sentence in the system text; the closing proposal (DRY plus the sentence as V5-R17, provisional, the "
         "instruction-only arm and model differences carried to the end-to-end study). Their wording is the lead's. Each message's reading is in the `caveats` of its intake record; "
         "`design/package-v5/inputs/p3/P3-LOG.md` section 1 lists them and section 2 what each run did.\n")
auth += ("\n## AUTH-030 verbatim human text (messages of 2026-11-08)\n" + verb("INT-T-040") + "\n" + verb("INT-T-045") +
         "\nLead's record (not the human's words): in INT-T-040, \"evice\" is read as \"evidence\" and \"eolicilty\" as \"explicitly\". \"then i "
         "authorize group 2 after fully completing group one\" is the only authorization for group 2. INT-T-041 asked whether group 2 comes "
         "now or waits for P2's outcomes and did not say which; the lead started group 2 after group 1 was complete (385237a) and read the "
         "human's continuing instructions (INT-T-042, INT-T-045) as consent. That reading is the lead's. INT-T-040's own intake caveat read "
         "the quoted sentence as meaning that group 2 waits for the human's word once group 1 is complete; no later message of the human "
         "saying so is recorded. Group 2 sends no model request. "
         "\"yes its free\" (INT-T-045) answers the lead's request to say when this branch is free; the lead reads it as \"the other session "
         "is not writing here, apply the records\". INT-T-042 (quoted under AUTH-031) chose option (a) for these records; option (a), in the "
         "lead's words (INT-T-042 caveats): the lead applies the drafted records on this branch in a separate worktree, and the human pushes. INT-T-045 also "
         "decided the end-to-end prompt change and the P1 order (WD-081).\n")
auth += ("\n## AUTH-031 verbatim human text (messages of 2026-11-08)\n" + verb("INT-T-041") + "\n" + verb("INT-T-042") + "\n" + verb("INT-T-044") +
         "\nLead's record (not the human's words): INT-T-041's \"run P5 and p2 parallel\" is read as approving the P2 pilot as proposed "
         "(`P2-DESIGN.md` section 8 stage 1), not the main run, which INT-T-042 approved. INT-T-042's \"P2 main A and B\" and INT-T-044's \"run "
         "P2b\" approve the lead's proposals; their arms, task counts, models and repeats are the lead's wording, not the human's.\n")
open(A, "w", encoding="utf-8", newline="\n").write(auth)

WD = """
## WD-073 P5 part B (OpenAI side check) results; D-01 kept until part A (2026-11-07)
- **Numbering:** WD-073 to WD-081 were drafted on `v5-p5-break-even` and numbered after WD-072 when applied on 2026-11-08 (WD-078, last bullet). Their dates are those of the events. Paths below are on `v5-p5-break-even` unless said otherwise.
- **What ran** (AUTH-028, INT-T-026): OpenAI `gpt-5.4-mini` hosted tool search.
  - **Before:** harness revision 1 ($0.149). Its sessions started warm from the calibration requests, and it had one session per cell.
  - **Change:** revision 2 forces cold starts (a fresh marker in tool 0) and runs 2 cold and 1 warm session per cell.
  - **Why:** to control the cache state and give a spread.
  - 193 requests, $0.445; the side check cost $0.594 in all (`design/package-v5/inputs/p5/RESULTS-P5-B.md`).
  - It is not P5's test. The human, 2026-11-07, as quoted in `RESULTS-P5-B.md` (no intake record holds it): "this test does not count as P5 test yet".
- **Result:**
  - Individually deferred functions still bill 30% of their tokens; namespaces bill 3.6%.
  - Deferral against eager, cold, at 10/30/100/300 tools: 1.19/0.70/0.44/0.35 (functions) and 1.12/0.67/0.29/0.11 (namespaces). Break-even between 10 and 30.
  - D-01 as written missed this route by 2.2 to 7.9 times at 100-300 tools, more than the run-to-run spread, so AUTH-028's stop rule applied. D-01's formula with the measured parameters reproduces the cells within 0.01 to 0.07 at 30-300 tools, and is 0.14 to 0.15 too low at 10.
- **Limits:** one model, one stub catalogue, one task, low reasoning effort, hosted search only.
- **Change proposed by the lead, not made:** a hosted-search variant (`design/package-v5/calc/regime_bill_hosted.py`). **Before:** `04` had D-01 only. The lead's reading of INT-T-027 (the human asked about the equation, then wrote "I agree"): D-01 stays, and the variant stays a proposal until part A.

## WD-074 P3 runs 1-3: models search uninstructed; tool-side notes do not stop them (2026-11-07 to 2026-11-08)
- **Setup** (AUTH-029; INT-T-028 to INT-T-030):
  - OpenRouter, provider GMICloud fp8 pinned without fallback; MiniMax-M3, DeepSeek-V4.1-Flash and GLM-5.3.
  - Tasks built by the lead over AppWorld's 463 real tool definitions, with stub results; temperature 0, seed 7; a $10 stop for all of P3.
  - Harness `design/package-v5/tools/p3_uninstructed_search.py`, analysis `design/package-v5/tools/p3_analyze.py`.
  - Results `design/package-v5/inputs/p3/RESULTS-P3-RUN1.md` to `RUN3.md`.
  - Smoke 1: 78 requests, $0.115 (87002c6).
- **Run 1** ($1.56):
  - With the target deferred and no instruction to search, all three models searched in every session and called the target in 19-20 of 20, as with all tools exposed. HYP-0019's falsifier is not met on this set.
  - With the target absent, 12-17 of 20 sessions were still searching at the 6-request cap.
- **Run 2** ($1.755; INT-T-031):
  - **Who and why:** the lead added a no-match rule with an app listing, after run 1's runaway searching and the human's request for a stop that is not a number of turns.
  - **What it did:** it cut runaway searching, but doubled or tripled substitute actions.
  - **Why dropped:** the listing put near-miss tools in front of the model.
  - The per-request rule-stage logging was fixed after the run (781d987).
- **Run 3** ($0.726; INT-T-032):
  - **Who and why:** the lead's revised rule2, to remove run 2's side effect while keeping a stop. **Before:** the run 2 rule with the listing.
  - **The rule:** no listing; novelty only within the best-match apps; otherwise only a note.
  - **What it did:** no harm, but only 10 of 50 sessions stopped after the note.
  - **Why not kept as the stop:** a note is not a stop.
  - Run 2's attribution of the false claims to the listing was corrected: they also occur with no rule.

## WD-075 P3 stop-rule research, two-need run 4 and log replay (2026-11-08)
- **Research, revision 1** (INT-T-033; the lead alone, 7 searches, 6 fetches):
  - It found arXiv 2610.06191: only "finish" remains after five judged-useless results.
  - Run 3's logs showed every target-absent substitute came after the first note, while 3 of 120 target-present sessions called an already-shown target after it.
  - The lead's own idea, withdrawing search_tools when the note comes, was judged weak for multi-need tasks.
  - The human accepted the lead's order research → per-need rule → two-need run (INT-T-033: "i accept the order").
- **Research, revision 2** (INT-T-034; six web scouts within the lead's bounds of 90 searches and 150 fetches: 80 searches, 126 fetches; 8 claims checked against primary pages; `design/package-v5/inputs/p3/STOP-RULE-RESEARCH-20261108.md`):
  - No published deterministic stop for tool-search loops was found.
  - Client-enforced stops work where text does not (arXiv 2610.06191; CGDP, 2605.07042).
  - Excluding the requested action redirects models to another ("When Guardrails Redirect").
  - A "Done" stub matches the high-dishonesty condition (2609.14758).
- **Run 4** ($3.630 with smoke, INT-T-035; two-need tasks; plain twice, note, stopreply, stopsearch):
  - Smoke 4 ($0.120): GLM kept emitting tool calls after all tools were removed. **Before:** the session went on to the cap. **Change (the lead):** the forced reply now ends the session itself. **Effect:** such sessions are ended and recorded as "stop ignored" (21, 29 and 31 of 40 in run 4's forced-reply sessions with a missing tool, `RESULTS-P3-RUN4.md`).
  - A session-wide forced reply lost the doable need in 40-80% of tasks (p <= 0.016 in all six cells).
  - Withdrawing only search kept the doable need, but did not end the loop.
  - The note alone had no effect.
  - Substitutes, and MiniMax's false claims (6-8 of 40), occur with no rule.
- **Replay** ($0, INT-T-036; `design/package-v5/inputs/p3/RESULTS-P3-REPLAY-A.md`):
  - The replayed first no-match matched the logged one in 180 of 180 sessions.
  - At the first no-match, the doable tool was already shown but not called in 51, 51 and 67 of 80 sessions.
  - **Who and why, DRY:** the lead's rule (refuse calls into an app where nothing new was found; end only when nothing is pending), designed from run 4's logs. A session-wide stop loses tools already found.
  - **Replay figures:** DRY kept the doable need in 30/36/33 of 40 (the logged search-withdrawn sessions, no end rule: 32/38/34); substitutes 14/9/9 → 5/2/4 (same baseline); it ended 8 to 20 of 40 sessions early and saved 10 to 29% of their requests (82, 96 and 37 in all); still at the backstop 15/2/9.
- **Documentation:** the human asked that runs, decisions, reasons, results and conclusions be documented: `design/package-v5/inputs/p3/P3-LOG.md`.

## WD-076 P3 runs 5-6 and closure: V5-R17 provisional (2026-11-08)
- **Run 5** ($1.618, INT-T-037; DRY against plain):
  - Substitutes 12/4/6 → 5/1/3 of 40; false claims 5/0/1 → 2/0/0.
  - The doable need fell 40/36/33 → 34/34/27, more than the replay predicted, and below the range of three no-rule copies (run 4 plain, run 4 plainB, run 5 plain).
  - The loss came mostly while models guessed the missing tool's name until the backstop.
  - The human asked whether run 4 should be rerun without its repeated plain run (recorded in `RESULTS-P3-RUN5.md` section 1a and `P3-LOG.md`; no intake record holds the question); no rerun was needed (d929585).
- **Run 6** ($0.549, INT-T-038; the human accepted going over $10; the ceiling of $10.60 is the lead's, and was not needed):
  - **Change (the lead's option (ii), chosen by the human in INT-T-038):** one sentence added to the system text on what to do when the catalogue has no tool for a need. **Before:** DRY alone.
  - **Why:** run 5's loss happened while models guessed names.
  - **What it did:** doable need 40/39/37 of 40; backstop 3/0/1; guessed names 2/1/0; requests 32-48% below no rule; substitutes 7/1/2; false claims 3/0/0; with both tools present, both needs done 20/17/19 of 20 against 18-20/18/20 with no rule (one run per cell).
- **Change (INT-T-039): V5-R17 added to `04`** (the lead's rule, OURS, provisional): the stop plus the sentence.
  - **Before:** `04` had no rule for a missing tool.
  - **Why:** models search uninstructed but keep searching for a missing tool (WD-074), and the human asked for a dynamic, deterministic stop.
  - **Open items, recorded in V5-R17:**
    - an instruction-only arm, for the end-to-end study;
    - withdrawing search_tools changes the tools array, against V5-R02;
    - MiniMax's residual substitutes and false claims (model choice).
  - `05` gained the end-to-end arm and `06` the traceability row. P3 total: $9.953.

## WD-077 Group 1 and P2 preparation (2026-11-08)
- **The request:** the human (INT-T-040) asked for group 1, then P2 preparation, with web searches as needed and explicit citations.
- **Group 1, done at 385237a:**
  - ready-to-apply drafts of these records (`ops/drafts/OPS-BRANCH-RECORDS-DRAFT-20261108.md`);
  - `design/package-v5/12-experiment-readiness.md` section 6: P2's route per provider. OpenAI enforces `allowed_tools`, keeps the cache, and allows at most 128 tools; ScaDS refuses it; GMICloud accepts it without enforcing it.
- **P2 preparation (02c3d78):**
  - `design/package-v5/inputs/p2/P2-DESIGN.md`, with its evidence table and search log;
  - harness `design/package-v5/tools/p2_offering.py` (the lead; there was no P2 harness before), reusing AppWorld's own function-calling agent with two hooks (the declared list and the offer);
  - a dry run and a mock test.

## WD-078 P5 part A started; P2 pilot; P2 main run started (2026-11-08)
- **P5 part A** (INT-T-041):
  - The first attempt stopped after 4 requests: ScaDS allows 2 requests per minute on GLM-5.3 (`design/package-v5/10-p0-university-api-reading.md` line 40).
  - **Change (the lead):** rerun with a 31 s pause (`design/package-v5/inputs/p5/scads-glm53-r2/`). **Before:** no pause.
- **P2 pilot** (AUTH-031, $0.316):
  - 3 of 5 tasks on every working run; about 8 calls per task and about 17,000 prompt tokens per call; cached share 0.78-0.86.
  - **Change (the lead): Chat Completions → Responses API** for both models. **Why:** gpt-5.4-mini rejects function tools with reasoning on Chat Completions. **What it did:** the main run had 0 failed calls (WD-080). The rejected pilot run on Chat Completions is kept as a record and is not in the pilot's figures.
  - **Change (the lead): a stop after two failed model calls in a row.** **Before:** no such stop. **Why:** AppWorld's agent had absorbed the rejected calls silently. **Effect:** none was needed in the main run (0 failed calls).
- **P2 main run** (INT-T-042): 4 arms × 2 repeats × 30 tasks per model, with per-model caps of $6 and $11, run by `design/package-v5/tools/p2_main_driver.py` (repeat 1 of all arms, then repeat 2).
- **Records:**
  - When the human chose option (a), this branch had moved to 94be01c with the other agent's WD-071 and WD-072.
  - So the drafts were renumbered (WD-073 to WD-081) and not applied until the human said "its free" (INT-T-045).

## WD-079 P5 part A results; D-01 kept, D-01h added (2026-11-08)
- **Result** (`design/package-v5/inputs/p5/RESULTS-P5-A.md`; ScaDS GLM-5.3, client deferral, 138 requests, free):
  - Deferral / expose-all, cold: 1.03-1.06 (10 tools), 0.44-0.46 (30), 0.14-0.15 (100), 0.048-0.049 (300). Break-even between 10 and 30, close to 10.
  - D-01 as written is within 0.01-0.03 at 30-300 tools and overstates at 10 (1.29).
  - Warm starts shrink deferral's advantage.
- **Analysis fix (the lead):**
  - **Before:** `design/package-v5/tools/p5_analyze.py` compared D-01 only at 10 tools, because the deferral prefix, which does not depend on n, was calibrated once.
  - **Change:** it reuses that calibration for every n.
  - **Effect:** the comparison at 30-300 tools on this route is new; no earlier statement rested on it.
- **Change (INT-T-043, deciding INT-T-027):**
  - **D-01 kept** as the working equation for the client route.
  - **D-01h added** (`design/package-v5/calc/regime_bill_hosted.py`) as a separate mode for vendor-hosted search.
  - **Before:** `04`'s D-01 entry named only `design/package-v5/calc/regime_bill.py`, and V5-R03 chose by D-01 alone.
  - **Why (the lead's reason; the human gave none):** D-01 fits our route (part A) and missed the vendor route (part B). The name D-01h and the words "separate mode" are the lead's.
  - **Limits:** one model, one route, stub tools of about 230 tokens, one three-turn task, 2 cold and 1 warm session per cell; no accuracy. D-01 with an uncached core does not fit (2 to 2.7 times too high).
  - Applied to `04` (the D-01 entry and V5-R03) and `06`; the variant's numbers are unchanged.

## WD-080 P2 main run results and decisions; P2b started (2026-11-08)
- **Result** (`design/package-v5/inputs/p2/RESULTS-P2-MAIN.md`; 16 runs, 480 task-runs, 0 failed calls, $12.377; P2 total $12.693):
  - **Setup:** AppWorld dev, 30 Spotify tasks; 128 tools declared; oracle subsets of 6-10.
  - **Server-enforced offering (`allowed_tools`)** kept the cache and was enforced: 0 calls outside the subset in 120 task-runs.
  - **Accuracy against offering all, per task:** gpt-5-mini +0.117 (95% scenario-bootstrap interval +0.033 to +0.217); gpt-5.4-mini −0.050 (−0.167 to +0.050). Run-to-run flips: 6 and 8 of 30. HYP-0018's falsifier is not met.
  - **The instruction form** broke the subset and doubled the calls on gpt-5-mini (5 and 14 calls outside), and was followed on gpt-5.4-mini.
  - **Declaring only the subset** cost 10-20% less, at the same accuracy within the intervals.
  - **Cost and sessions:** `enf` against `all`: calls x1.08 (gpt-5-mini) and x1.32 (gpt-5.4-mini), cost x1.02 and x1.15; restricting to the oracle subset made gpt-5.4-mini work around it (in `all` it had used 18 and 26 calls outside the oracle list). `instr` on gpt-5-mini: calls x2.03, cost x1.37.
- **Decisions (INT-T-044):** V5 keeps the offering stage.
  - **Change: a note in `04` after V5-R17** (the human: "add note"; the wording is the lead's). **Before:** `04` had no statement on which offering form to use. **Why:** P2's cost and instruction results.
  - **Change: HYP-0018 gains P2's result** (before: no result section). **Its status stays `proposed`** (the human: "donot close it we moght need more eviddenve").
  - **Not shown by P2** (HYP-0018 "Not shown"): realistic subsets that miss needed tools; catalogue sizes other than 128; other benchmarks; Anthropic's mechanism; accuracy differences of a few points.
  - `05` P2 row status; the `12` section 6 pointer was updated after the run (a8278c7).
- **P2b started** on ScaDS GLM-5.3 (`all` against `instr`, 2 repeats). Harness options added by the lead (before: none for ScaDS):
  - **pacing, 31 s:** ScaDS's limit of 2 requests per minute;
  - **429 retry:** so a refused request does not count as a failure;
  - **seed 100 and temperature 0:** as in R3 Part B on ScaDS, so the runs are comparable;
  - **no reasoning field:** reasoning as served.
- **Change (the lead): large local logs gzipped.** **Before:** AppWorld's plain-text console logs exceeded the verifier's 5 MB check. **What it did:** lossless; the files stay local and git-excluded, and the check passes.

## WD-081 Group 2 preparation; records applied; end-to-end prompt change; P1 order (2026-11-08)
- **Group 2:** started by the lead after group 1 was complete. This is the lead's reading of INT-T-040; INT-T-041 asked whether to wait and recorded no answer (AUTH-030, lead's record).
- **End-to-end pairs** (`design/package-v5/inputs/e2e/E2E-TASKS-DESIGN.md`):
  - AppWorld tasks with one state-changing needed API removed. 108 of 147 train and dev tasks have a candidate.
  - With P2's successful traces (FeasiGen's rule), 16 dev tasks in 6 scenarios are validated.
  - A deterministic scorer from the complete-task status and the recorded calls: honest decline, false claim, substitute.
  - An AppWorld API identifier in two design notes was replaced by a description (838ec25).
- **Change record: AppWorld's "The task is doable" line (INT-T-045).**
  - **Who added it, where:** AppWorld, in the "Key Instructions" of its current agent prompts (function-calling agent `instructions.txt` line 41; also the full-code and ReAct prompts). The legacy prompt has no such line. All P2 runs used it.
  - **What it does [I]:**
    - On AppWorld's own tasks, which are all checked solvable, it is true and discourages giving up.
    - On a removed-API variant it is false, and pushes the model toward a substitute or a false claim.
    - Its size on solvable tasks is not measured [U].
  - **Change (INT-T-045: "remove the task is doable"):** the lead reads this as removing only the words "The task is doable, but", in both halves of every pair, and keeping the exit to status "fail"; the human did not specify the scope.
  - **How its effect is recorded:**
    - Run the unchanged dev tasks once without the words, against P2's `all` runs with them. That is one run per model, about $0.50 and $1.00, and needs the end-to-end authorization.
    - Yardstick: P2's run-to-run flips (6 and 8 of 30).
    - On variants: the declines, substitutes and false claims.
- **P1** (`design/package-v5/inputs/p1/P1-PREP.md`):
  - AppWorld's own users give 34 returning users and 64 returns. Outside the core, seed recall averages 0.19 and precision 0.14 (zero in 36 of 64).
  - **Before:** `05` P1 planned a declared construction of users, in effect a synthetic set.
  - **Order (INT-T-045:** the human asked "can we start by appworld first then try adding synthetic?"; the lead reads this as approval of the order): start with AppWorld's natural users. The condition "add a synthetic set only if the high-recurrence band proves too thin" is the lead's. `05` P1's wording is not changed yet.
- **Still open, not decided:**
  - whether the end-to-end bill and accuracy arms, which have no removed API, keep AppWorld's prompt as shipped (the lead recommends keeping it);
  - which tasks (validated dev only, or more);
  - the form of "removed" (declared set or searchable catalogue);
  - P1's construction, arms and measures (proposed in `P1-PREP.md` section 3).
  - Neither the end-to-end variant mode nor the P1 harness is written.
- **Records applied (INT-T-045):**
  - The AUTH-028 amendment, AUTH-029 to AUTH-031, and WD-073 to WD-081.
  - **STATE rewritten (the lead).** **Why:** sections A and C were out of date after P5, P3 and P2. **What it did:** section A now points to WD-073 to WD-081 and to `ops/OPEN-TASKS.md`; section D states that the rebase onto 77357c1 is not done. The previous STATE is archived verbatim.
  - `ops/OPEN-TASKS.md` added (the lead's to-do list, started 2026-11-07 after the human asked to keep waiting work in a long-term place; copied here so this branch's STATE can point to it).
  - The human's words were copied from the intake records by `ops/drafts/apply_ops_records.py`.
  - Reviewed before commit by Sonnet 5.5 subagents at high effort in two rounds (INT-T-045): round 1 by three reviewers (completeness; facts and numbers; format, rules and change records), round 2 by two (resumed after a usage limit through messaging thread T-20261108-01). Their findings and the lead's fixes are listed in the message of the commit that adds this entry.
- **Not done: the P3 sources stored as EXT.** `tools/litfetch.py` on `v5-p5-break-even` checks that branch's AUTH table, which ends at AUTH-020. Letting it read this branch's AUTH-030 is a tool change for the human to review.
"""
D = os.path.join(WT, "ops/DESIGN-DECISIONS.md")
d = open(D, "rb").read()  # mixed line endings (older CRLF, newer LF): keep every original byte and append in LF
assert b"## WD-073" not in d
open(D, "wb").write(d + WD.encode("utf-8"))

S = os.path.join(WT, "ops/STATE.md")
old = open(S, encoding="utf-8").read()
ar = os.path.join(WT, "ops/STATE-ARCHIVE.md")
open(ar, "a", encoding="utf-8", newline="\n").write(
    "\n## STATE.md as it stood at 94be01c before the records of 2026-11-08 (WD-081) (verbatim, indented 4 spaces as the section before)\n\n"
    + "".join(("    " + l) if l.strip() else l for l in old.splitlines(True)))
new = old
a0 = new.index("## A. Research work")
b0 = new.index("## B. Standing decisions")
A_NEW = """## A. Research work (V5; `v5-audit`, and branch `v5-p5-break-even`, not merged)
- **V5 audit** (AUTH-020): conceptual package; start at `design/package-v5/00-README.md`. Working draft V5-R = DPR-0007, plus V5-R17 (provisional). Nothing is validated, approved or final. Benchmark register `17`.
- **Probes R1-R3 and GLM-5.3 on ScaDS done** (AUTH-024 to AUTH-027; results `exchange/prior-work/v5-probes/results/` and `R3-GLM/`): merged into `v5-audit` and pushed (77357c1; WD-071, WD-072).
- **P5 done** (AUTH-028): part B, OpenAI side check, $0.594 (WD-073); part A, ScaDS GLM-5.3, free: break-even between 10 and 30 tools; D-01 fits the client route; D-01 kept, D-01h added for vendor-hosted search (WD-079).
- **P3 closed** (AUTH-029): six runs, $9.953; models search uninstructed; V5-R17 adds a stop for a missing tool, provisional (WD-074 to WD-076; `design/package-v5/inputs/p3/P3-LOG.md`).
- **P2 done** (AUTH-030, AUTH-031): OpenAI, $12.69; server-enforced offering at a fixed prefix kept the cache, with no accuracy loss beyond run-to-run variation (oracle subsets, 128 tools); HYP-0018 kept open; P2b running on ScaDS (WD-077, WD-078, WD-080).
- **End-to-end and P1 prepared** (AUTH-030, WD-081): 16 validated task pairs; AppWorld's natural returning users first. The end-to-end study waits for its own authorization.
- **Answers of 2026-11-07** (INT-T-023, INT-T-024; `design/ledger/notes/ANSWERS-20261107.md` on `v5-r3-part-b-results`): `17` section 9 postponed; research question entered as pointers (`requirements/THESIS_QUESTION.md`; that file and the answers file are on `v5-audit`); Executor closed for now (WD-069). Still open: the workbook (no `openpyxl` on Linux); Q-U15, Q-U25, Q-U27; the supervisor's verdict on V5 (Q-J31, Q-J32; Q-J33 only for an Executor baseline).
- **The lead's to-do list:** `ops/OPEN-TASKS.md` (not an authorization).

"""
new = new[:a0] + A_NEW + new[b0:]
new = new.replace("It is rebased onto `v5-audit` after each merge; the human force-pushes it.", "It is rebased onto `v5-audit` after each merge; the human force-pushes it. The rebase onto 77357c1 is not done yet (WD-072).")
new = new.replace("- Authorizations in force include AUTH-020 (V5 audit), AUTH-024 to AUTH-027 (R3 probes and follow-ups), AUTH-028 (P5) and AUTH-021 to AUTH-023 (machine portability, see D).",
                  "- Authorizations: AUTH-020 (V5 audit), AUTH-021 to AUTH-023 (machine portability, see D), AUTH-024 to AUTH-027 (R3 probes; done), AUTH-028 (P5; done), AUTH-029 (P3; closed), AUTH-030 (group 1 and 2, P2 preparation) and AUTH-031 (P2 runs, P2b).")
open(S, "w", encoding="utf-8", newline="\n").write(new)
n_lines, n_bytes = new.count("\n"), len(new.encode("utf-8"))
assert n_lines <= 40 and n_bytes < 6000, (n_lines, n_bytes)
o = open(os.path.join(SRC, "ops/OPEN-TASKS.md"), encoding="utf-8").read()
open(os.path.join(WT, "ops/OPEN-TASKS.md"), "w", encoding="utf-8", newline="\n").write(o)
print(f"applied; STATE {n_lines} lines, {n_bytes} bytes; intake bodies verified: {sorted(BODY)}")
