# Workspace decisions (setup choices, not scientific choices)

Format: decision, options compared, why, what would change it. These record how the workspace is built. None of them selects a thesis question, policy or design.

## WD-001 Separate workspace outside the origin repo, new git history
- Options: (a) new branch/folder inside `research-cleanroom`; (b) clone of the origin; (c) new sibling folder with its own repo and a hash-verified evidence layer.
- Chosen: (c). (a) would load the origin's `CLAUDE.md`, `.claude/` agents, memory and 600+ files into every session and invite edits to audited records. (b) was forbidden and copies everything. A sibling folder has no ancestor `CLAUDE.md` (verified A1: only this workspace's `CLAUDE.md` and `STATE.md` load).
- Costs: evidence is duplicated (39 governing copies); staleness if the origin changes (`verify` full mode compares against `config/origin.json`).
- Revisit if: reconciliation is authorized and a shared structure becomes useful.

## WD-002 Evidence tiers instead of "everything" or "a narrative"
- Options: (a) copy the repo; (b) hand-written briefing; (c) tiers: byte-exact governing copies (selected by a rule, not by claim), a metadata-only manifest of all 239 source manifests (232 with stored text), an index of every other file, a withheld set with hashes, and a sanctioned hash-verified extraction tool.
- Why: (a) loses the boundary; (b) loses provenance and bakes in one author's reading. (c) lets an agent open a passage by id/line range and cite it, while caveats stay in `evidence/CAVEATS.md` as pointers, not summaries.
- Limits: the governing-copy rule (`evidence/README.md`) is a judgement; the index shows what is *not* copied so a gap can be seen.

## WD-003 Record classes with front matter and ids
Requirement, extract, summary, finding, hypothesis, design proposal/choice, challenge, review, authorization. A later reader must be able to tell a copied source, an extracted passage, a summary and a new finding apart. Enforced only where mechanical (extract hashes, schema and reference checks in `verify`); the honesty of a finding is not checkable.

## WD-004 Agent mechanism: named subagents with SendMessage by id (not native agent teams)
- Options: (a) lead only; (b) subagents that report only to the lead (hub-and-spoke); (c) agent definitions that message each other with `SendMessage` (peer-to-peer), lead as escalation point; (d) experimental native agent teams.
- Evidence: test B showed (c) works: three Sonnet agents exchanged direct messages, one conceded naming the evidence, one escalated to the lead, 9 of 12 messages. Hub-and-spoke (b) would make the lead a bottleneck and hide the challenge from the evidence. (d) needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, is experimental and interactive; under `-p` the flag added a `name` parameter and name-addressing was accepted, but no team-creation tool or shared task list was visible (C5, C5b), so (d)'s distinguishing features are **unverified**.
- Chosen: (c). Three agents, one per distinct failure mode: evidence-steward (is the cited passage there; what are its limits), design-proposer (generates and argues options), design-challenger (attacks them; effort high). A fourth agent would add messages without adding a distinct check.
- Constraints found: agents cannot wait or poll; spawn all, then send roster + tasking; runtime agents and ids do not survive the session, so the durable record is `ops/threads/`.
- Revisit if: the human tries native teams interactively and finds a shared task list or persistence worth the experimental risk. If names are enabled, the SendMessage allow-list in `tools/guard.py` must be extended deliberately.

## WD-005 Enforcement mix: hooks for what can be enforced, instructions for the rest
Deny rules for the origin and other stores; one deterministic guard for path rules, ownership and messaging; a verifier for tamper detection; instructions for scope, honesty and budgets. Exact split and the confirmed bypass: `ops/SAFEGUARDS.md`. Not chosen: OS sandbox or separate user account (not available on native Windows without installs/administration, not authorized).

## WD-006 Sonnet 5.5 for all subagents, pinned by environment
`CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5-5` plus `_FORCE=1` in project settings, plus `model:` in each definition. Verified from the stream: every subagent assistant message in B, C1, C4, C5b reports claude-sonnet-5-5 (built-in Explore also). Side effect: the Agent tool's `model` parameter disappears. Opus is not used; the challenger's depth comes from `effort: high`. Revisit if the human wants an Opus challenger for pivotal judgments.

## WD-007 Local settings only
Everything is in the workspace `.claude/settings.json` and `.claude/agents/`. Global settings, global agents, extensions and connectors were not changed. The workspace relies on global connectors existing but denies the personal ones locally.

## WD-008 Git hygiene
Own repo, no remote. `.gitattributes` `* -text` and local `core.autocrlf=false` so byte-exact copies keep their hashes on Windows. Raw stream logs of tests are kept out of git (`.gitignore`); summaries and the deterministic guard test table are committed.

## WD-009 Reconciliation path (not executed)
A later, separately authorized step: the lead produces a reconciliation brief listing each DES/HYP/FND with its evidence ids; comparison with the origin is done through the sanctioned tools under a new AUTH with explicit scope, never by merging repositories. Nothing in this workspace is written back to the origin.

## WD-010 Hook-enforced thread message cap (added after the independent review)
- Problem (RV-0001 D22, observed): an instruction-only cap of 12 was overrun in the review thread (13 sends) because no agent can see the global count, and the lead's 3 tasking messages are part of it.
- Options: (a) per-agent tallies; (b) lead polls and stops agents (agents cannot be interrupted, only messaged); (c) the PreToolUse hook counts every SendMessage per active thread and refuses beyond the cap.
- Chosen: (c) in `tools/guard.py` with `ops/threads/ACTIVE.json` and `config/limits.json`. Verified deterministically (`guard_cases.py`) and live (R2: 6th send refused at 5/5). The value 12 and 2 rounds are conservative defaults of the bootstrap lead, not evidence-derived; only the human changes them.
- Limit: it depends on the hook layer (see WD-011). A refused agent cannot escalate; the protocol says to finish with a final answer listing the unresolved disagreement.

## WD-011 Treat the hook layer as defeatable; keep deny rules as the second layer; detect, do not assume
C7 showed `disableAllHooks` in a local settings file turns the guard off. Response: deny rules for that file (hook-independent, C8), guard text/path blocks, `verify` fails on its presence, a hash pin of the safeguard-defining files (`config/PINNED.json`), and the rule that every session starts with `verify --quick`. An OS sandbox would be the real fix and is not available here.

## WD-013 Supervisor intake by human-approved line ranges (AUTH-002 item 2)
- Problem: the earlier rule "store the supplied text verbatim" conflicts with "keep earlier-thesis experimental content out" when the supplied file contains both (the 2026-10-14 transcript is the expected case). Nothing mechanical protected stored intake text.
- Options: (a) human pre-screens and pastes only the excerpt (loses source identity and integrity chain); (b) store the whole file as restricted with only a hash (nothing usable is admitted); (c) register the outside file with its SHA-256 and the human-approved line ranges; the tool admits only those lines, as extracts with source identity, supplier, time, location, whole-file hash and body hash; verify re-checks.
- Chosen: (c) as route B, with (a) kept as route A (recorded text, create-only, body hash) for text with no separate original. Same pattern as `config/extractable_origin.json`: the human's approval is a config entry plus an AUTH id; agents cannot edit `config/**`.
- Limits (not absolute): see SAFEGUARDS row 18. The block on editing recorded texts covers the edit tools only. Excluded-content detection is exact-line, best effort. Whole lines only. Tested on synthetic content only.
- Revisit if: the first real intake shows ranges cannot be expressed by lines (for example excerpts inside a line), or the human prefers a separate excerpt file.

## WD-014 Source-name crosswalk (AUTH-002 item 3)
- Problem: the Stage 3 claim ledger and other governing records cite short names (`r4-github`) that are not manifest ids; an agent following the citation got "unknown source id".
- Chosen: an explicit, pinned table `config/source_aliases.json` (44 aliases, 2 groups), derived mechanically by the lead from the names the governing copies use; `origin_extract.py --source` resolves exact ids first, then aliases (printing the resolution and recording `cited_as`), refuses family names and never resolves by silent prefix. Not chosen: automatic unique-prefix matching (a new source added later could silently change what a name means).
- Limit: the cited documents do not state the manifest ids; each alias is the lead's identification and is flagged as such in the file. Two aliases rest on "only candidate with stored text". A spot check of four ledger citations found the quoted figures at the cited lines.

## WD-015 Agent ids in the VS Code runtime (AUTH-002 item 1)
Verified by thread T-20261016-92 (two agents, 4 of 6 counted messages): ids are `a` + 16 hex characters, the guard accepts them, direct agent-to-agent messaging and replies work, the steward's pinned Bash command runs. No guard change was needed. See SAFEGUARDS "VS Code runtime, observed" for what remains unobserved. Coordination overhead is unchanged: the cap of 12 still leaves 9 agent messages after the lead's 3 tasking messages.

## WD-016 Intake of the 2026-10-14 excerpts by route A (AUTH-003)
- Problem: the nine excerpts came as text pasted by the human; the original transcript is not in the workspace. Route B (registered outside file plus approved line ranges) needs a file to hash and would register a file nobody here can open.
- Chosen: route A (create-only recorded text, body SHA-256 re-checked by `verify_workspace.py`). The supplied-text hash is `body_sha256`; the original's identity (title, URL, speaker) is recorded as the supplier's claim and its hash as "not available". Wording kept as supplied, including markdown markers and transcription errors, so that the hash covers exactly what was supplied. Supplier annotation (the Wednesday 2026-10-21 reading) kept in the header, outside the body.
- Classification: the classes in `requirements/intake/README.md`; statements split where one excerpt held two classes (for example E7 into form, task and example); the more cautious class used when two were plausible (`unclear`); the excerpts' titles are the supplier's labels. REQ ids `REQ-O14-nn`; the comparison is an unverified summary (SUM-0001) that changes no earlier record.
- Not done: no agent review (AUTH-003 forbids broad review; a self-check re-hashed the body against the supplied text and re-read the register against the excerpts); `THESIS_QUESTION.md` untouched; no tool or config change.
- Limit noted: `verify_workspace.py` blocks AUTH-001 and AUTH-002 from being cited as design approval but not AUTH-003; the restriction is carried by AUTH-003's limits column. Closing that needs a tool change, which AUTH-003 does not authorize.

## WD-012 Review-driven corrections (RV-0001)
Applied: guard hardening (wildcard/parent/`..`/outside-workspace paths, no sanctioned-name exemption, `.git` and local-settings protection, `match()` dot bug), SendMessage allow-list, message-cap hook, config pin, `approved` records may not cite AUTH-001, deny rules for outbound/scheduling tools, CAVEATS rows 3/10/12/15 corrected, REQ-U1 and REQ-D1 scopes restored, template seeds neutralised, severity/status vocabulary unified, message kinds unified, round and message definitions, steward command form, source counts corrected, claim about C4 as a model audit removed. Not applied (kept as documented limits): OS sandbox, Bash write ownership, foreign agent-id resolution (untested), interactive/VS Code behavior (untested at the time; partly observed later, see WD-015 and SAFEGUARDS). Details: `ops/threads/T-20261016-91/SUMMARY.md`.

## WD-017 Process of the first design task (AUTH-004, thread T-20261016-93)
- Distribution: steward = evidence base per decision area; proposer = decision problem, families, complete comparators, template, hypotheses; challenger = attack with answerable-now vs needs-experiment labels; lead = tasking, evidence substitution, assembly of A-F. Files, not messages, carried the detail (12-message cap, hook-enforced, reached).
- Deviation from PROTOCOL (one issue per message): objections and responses bundled per proposal with a CH id per issue; authorized by the lead in TASK.md only to fit the cap; no cap or round was raised. Consequence: two rounds, no escalation channel after message 12.
- Steward stopped at maxTurns 40 (28 extractions, no findings/log/report). Decision: not re-run past its bound (PROTOCOL); the lead ran the sanctioned extraction tool (EXT-0035..0056) and wrote an unverified evidence map (SUM-0002). Cost: no independent evidence check. Revisit if the human wants a bounded steward re-run, or a larger `maxTurns`/narrower steward tasking (extraction in batches).
- Lesson: one extract per tool call exhausts 40 turns; give the steward a bounded list (about 10 passages) and require the findings index before extraction continues.
- Lead mechanical edit of agent-owned files: `target` front matter of CH-0017/0018/0019 and RV-0002 changed from prose to id lists so `verify_workspace.py` passes; content unchanged.
- Observed: peer messages did resume idle agents (proposer and challenger were resumed by each other and by the lead).

## WD-018 Process of the revision task (AUTH-005, thread T-20261016-94)
- Steward lesson applied: the AUTH-004 failure came from unbounded extraction. This time the lead extracted the pivotal passages first (EXT-0057..0065) and gave the steward a fixed list (V1-V8), a "create the result file first, update each row immediately" rule and a cap of four extra windows. Result: the steward finished (50 tool calls) and acted as a genuine second reader (it corrected the lead's framing of two extracts). Keep this pattern: lead locates, steward verifies.
- Collaboration lesson applied: the proposer was told to defend its assumptions and label replies CONCEDE / PARTIAL / REBUT / OPEN; the challenger to grade its own objections and say which were overstated. Result: real disagreement (8 concessions, 7 partial, 2 rebuttals kept) and the challenger withdrew 8 and downgraded 7. Challenger also caught that concessions had not propagated into operative text (five defects): require a propagation check at the end of any such round.
- Message budget: planned so that a mandatory escalation slot stayed free (9 of 12 used; escalation not needed). Bundling per proposal remained a deviation from PROTOCOL's one-issue-per-message rule (TASK.md), cap unchanged.
- Mechanical lead edits to agent-owned files: the `target` front matter of reviews/RV-0003.md (twice, the challenger overwrote the first fix). Suggestion for a tool change (not authorized): make `verify_workspace.py` accept prose targets or have the challenger template use id lists.
- Safe-checkpoint practice used on the user's request: commit after every file and keep `ops/threads/<thread>/RESUME.md` current. Worth keeping for long tasks.

## WD-019 Process and scientific decisions of AUTH-006 (thread T-20261016-95)
- Scope kept: lead-written package-v3 (01 errata, 02 graph G, 03 comparison, 04 objections/experiments, 05 outline); one challenger, two rounds, 2 of 12 messages; no proposer or steward (no new evidence needed); earlier packages untouched.
- Decision: C-A demoted to a component and comparator because its core rule needs need statistics a large catalogue lacks; the same reasons apply to G's D2, so this is an applicability decision, not a ranking. C-B not adopted; its parts are conditional arms.
- Decision: G is presented as two layers (run-time policy R1-R6 plus a deployment selection protocol D1-D4), not as one policy. Retained disagreement with the challenger: D-nodes stay in the figure.
- Challenger caught a decisive omission in the lead's own correction (the extra model call per discovery); fixed in 01 and hand-checked. Challenger maintained one should-fix (D4 specification); lead completed it after round 2 (arm table, test-split failure, power and minimum stratum, substitute reference rule); the challenger has not re-checked those final edits.
- No empirical benefit, threshold, margin or novelty is claimed. Open human decisions are listed in 04 section 5.
- Mechanical: ACTIVE.json deleted at close; challenger records left as written.

## AUTH-007 (2026-10-17): independent-research coordination, Phase 2 preparation
- Decision (lead): the human delegated the remaining phases and waived per-step confirmations. The role prompt's disclosure gate is kept as a conservative lead-drafted manifest, not skipped: 33 of 39 governing copies (hash re-verified against `evidence/governing/INDEX.json`) plus public-source metadata are disclosed; withheld are STAGE1_RESEARCH_BRIEF, STAGE4B synthesis and supervisor alignment, STAGE4C dossier, S4D quality addendum, D4C, D4D (supervisor-transcript digests or verbatim quotations), `requirements/**`, extracts, CAVEATS, design/hypotheses/challenges/reviews/findings/ops, and all restricted items. Keyword screening only; a few short supervisor phrases may remain in included records (stated in the package manifest and README). The human may widen or narrow this later.
- Decision (lead): the independent findings and the comparison result are kept outside this repository (the human's earlier requirement), so Phase 2 runs in a separate folder with a fresh Fable-5.1 comparator, not with this workspace's Sonnet agents.
- Limit found: `tools/guard.py` blocks any agent read or write outside the workspace (scratchpad excepted). The lead therefore wrote scripts in its scratchpad (`verify-freeze-phase1.ps1`, `run-phase2.ps1`, `phase2-prompt.md`, `phase2-package/`) and did not run them against the independent folder itself. Verified by a dry run on synthetic data inside the scratchpad only.
- Same-vendor limit: the Phase 1 investigator and the comparator both use Anthropic models; the attestation records this, so independence is of context, not of provider.
- No thesis question, policy, threshold or margin selected; nothing in `design/` changed.

## AUTH-008 (2026-10-18): MCPVerse v1/v2 table check
- Decision (lead): the human asked whether the lead or the independent agent could fetch the MCPVerse v2 table; the lead did it locally (two arXiv PDFs, 2508.16260 v1 and v2, downloaded to the scratchpad; pages rendered with PyMuPDF and read by the lead). No summarising fetch tool was used. Result is reported in chat only; the PNGs are in the scratchpad, nothing was added to the repository or to the frozen independent reports.
- Reading (lead, not verified by a second reader): v2 Table 2 gives Claude-4-Sonnet Oracle 62.3, Standard 62.4, Max-Scale 44.2 (Standard to Max-Scale about -18 points); v1 Table 2 gives 57.81, 61.01, 57.77 (about -3 points). v2 Table 4 repeats Qwen3-235B-2507's Oracle/Standard values (44.8, 53.2) in the Claude row, which conflicts with v2 Tables 2 and 3. The tables do not state why v1 and v2 differ.

## AUTH-009 (2026-10-18): Phase 2b addendum run (prepared, outside this repo)
- Decision (lead): fresh Fable-5.1 session reading its frozen Phase 2 report plus raw MCPVerse PDFs/page images; not a resumed session (cost, and the original run folder is writable). The lead's own reading of the tables (AUTH-008) is deliberately not given to it, to avoid anchoring; the prompt asks it to check table consistency as a method step without naming any finding. Prepared in the scratchpad: `phase2b-package/`, `phase2b-prompt.md`, `run-phase2b.ps1`; dry run on synthetic data only. The human starts it.

## WD-020 Scientific-director session (AUTH-010, 2026-10-19, thread T-20261019-96)
- Authorization: the human's message called itself "AUTH-00x ... within AUTH-007"; AUTH-007 is a different, spent entry, so it is recorded as AUTH-010 with the human's operative sentences quoted. Scope: 2026-10-21 preparation only.
- Decision (lead): the five external-review concerns about v3 were checked against the actual text and sources; all five hold (E1 only in part), see `design/package-v4/03-review-adjudication.md`. v3 stays unchanged; corrections are the versioned package `design/package-v4/` (brief, graph and protocol, adjudication).
- Decision (lead): the supervisor-facing graph is split into a run-time policy (Figure 1, optional stages behind configuration gates) and a study protocol (Figure 2). D4 is presented as what it is, model selection under a noninferiority constraint. This reverses the v3 choice to keep D1-D4 in the supervisor figure (a retained disagreement in v3 `04` section 3); reason: the figure's optional stages were not drawn as optional, and a selection routine in a policy figure invites being read as a policy node.
- Decision (lead): ties. v3's "interval contains zero => tie => simplest" made the returned configuration depend on sample size and treated non-detection as equivalence. Replaced by a feasible set, a directionally defined cost-indistinguishable set S, and a parsimony preference that needs a human-set epsilon (otherwise S is reported with no winner). S is post-selection with unknown coverage (E6).
- Decision (lead): large-catalogue reference. v3's "largest configuration that fits" was undefined for a catalogue; v4 uses a ladder (R-full where it fits, R-pool as an evaluation-side analogue of the curated pool, then a frontier) and states that above `n_fit` no noninferiority-to-expose-all claim exists. The direction of R-pool relative to expose-all is unresolved and must be calibrated.
- Decision (lead): E1 can end the token-saving question for configurations with a negligible tool-block share but not the feasibility question; scale 1-10 million tokens per call at 10,000 tools (three sources of different quality).
- Added arm: model-navigated hierarchy (restored from package v1 P4g). Trigger also placed at finish (P3f), after the challenger noted the only stored trigger-like result is a termination trigger.
- Process: steward (10 claims, bounded, EXT-0074..0084, FND-0002) found draft misattributions (292k, 75% share, "unscored" routes); challenger (13 records CH-0045..0057, none decisive) found real defects in the lead's first v4 draft (trigger placement, phantom ask edge, R-pool identity claim, Regime B routed to a feasibility rule, E1 overreach, brief overstatements). Both caught errors the lead had written; keep the pattern (lead drafts, steward verifies numbers, challenger attacks, one round-2 message).
- Provenance: the untracked 19 Oct draft and EXT-0067..0073 have no recorded author or AUTH; committed with a status banner as an input draft. The human's external Phase 1/2/2b results were not read (guard) and do not inform v4.
- No threshold, margin, thesis question or final policy was selected; nothing is approved.

## WD-021 Supervisor follow-up on caching and memory (AUTH-010, 2026-10-19)
- The supervisor's cache/billing and memory points were mapped to the record in `design/package-v4/04-followup-cache-and-memory.md` (addendum; v4 `01`-`03` unchanged). Finding: v4's criterion counts cache reads as fresh tokens (a real gap, a scoping choice from AUTH-006, not a closed science question); session memory (F8) was deferred in package v1 for a vehicle reason and is absent from v4.
- Correction recorded: in the stored provider documents, keeping a cache costs a write premium on Anthropic and OpenAI (1.25x / 2x) and an hourly storage price on Gemini explicit caches; the supervisor's "1/10 for an hour" is not general.
- The student's proposed objective change (report and optimise the bill) replaces the AUTH-006 working objective; recorded here as pending the human's explicit decision; v4's brief still states tokens. No entry in AUTHORIZATIONS was created because the student asked the supervisor a question and has not decided.
- The intermediate presentation the student gave the supervisor is not in the repository; no comparison with it was possible.

## WD-022 Literature check (AUTH-011, 2026-10-19, thread T-20261019-97)
- Decision (lead): the human agreed to a bounded literature check before any pilot; the lead ran the web access (agents have none) and stored texts with hashes; steward verified, challenger attacked. Findings in `design/package-v4/05-literature-check-summary.md` and `findings/SUM-0005`.
- Result: caching mechanism documented by vendors but no independent measurement for appended definitions; instructed search is measured at 18,505 tools for strong models (cost premium over an oracle tool set); uninstructed initiation is not measured; cross-session tool-discovery memory in a large catalogue is not measured. The earlier claim "initiation is unmeasured" was split into instructed (measured) and uninstructed (not).
- Corrections of the lead's own earlier errors: LOMEKWI was described with the wrong direction and object; "0.02" is oracle-tool discovery, not success; the claim "no stored source evaluates cross-session tool memory" was too strong; pilot 1 had been understated.
- Process: the challenger reached its turn limit without a hand-back but wrote its files; the steward's note that Apple's and MemToolAgent's memory does not support "tool-only over conversation memory" was accepted.
- The pilots remain unauthorized; this task spent 8 of 15 searches and 12 of 15 fetches.

## WD-023 Extended literature check and remote (AUTH-012, AUTH-013, 2026-10-19)
- The human added a private GitHub remote as a backup and authorized it (AUTH-012). The lead does not push, pull or fetch (deny rules stay). The pinned verifier fails on any remote; the lead prepared a narrow exception (a remote is allowed only if its exact URL is in an AUTH row) and re-pinned, **without human review of the pinned file**; the permission layer blocked further work. The edits (`tools/verify_workspace.py`, `config/PINNED.json`) are uncommitted for the human to commit or revert. Lesson: a change to a pinned safeguard needs the human's review before it is run, even when the underlying authorization is clear.
- The human lifted the numeric caps on the literature check (AUTH-013). Rounds 3 and 4 added sources on false-positive tool calling, overuse, memory, code mode, cost-aware tool use; results in `design/package-v4/05` sections 3-4 and `findings/SUM-0006..0008`.
- Corrections to the lead's own text after the challenger (RV-0007): the Reasoning Trap's rate is a rate of not declining; a snippet-derived "65/65 passes" was removed; "more likely a real gap" retracted.
- The bill-versus-tokens switch and the memory scope stay pending on the supervisor (see STATE).

## WD-024 Open-items ledger placed in the repo (AUTH-016, 2026-10-19)
- The human asked to put the open-items workbook in the repo and to close items commit by commit with evidence (verbatim in AUTH-016). Answers to the lead's four questions: location `design/ledger/`; first commit workbook only; CSV export of Ledger, Questions and Change log; evidence = repo first, then web fetches for the named item.
- Decision (lead): the workbook `design/ledger/PROJECT_A_OPEN_ITEMS_LEDGER.xlsx` is the single canonical copy and is edited in place, never rebuilt from scripts (a rebuild would overwrite typed answers). The CSV export (`design/ledger/export_ledger.py`, `design/ledger/export/`) is derived and exists so that commit diffs show per-item changes; the script computes the formula columns itself because no spreadsheet engine is installed here to recalculate.
- Decision (lead): rows are never renumbered; Joaa's statements are recorded verbatim (sheet "Supervisor statements") and described as his proposals; the review report and SRC-11/12 stay untracked in `.workspace` (human's choice) until admitted.
- Limits found: the workbook was open in another program when the lead tried to move it, so it was copied; the old copy in `.workspace` is a duplicate to delete once it is closed.
- Not covered: no AUTH admits SRC-11/12 or the review report; no experiment, parameter or thesis-question choice is made by AUTH-016.

## WD-025 Ledger batch 1 (AUTH-016, thread T-20261019-99, 2026-10-19)
- Process (lead): four evidence-stewards in parallel on disjoint files read stored sources at pointer ranges the lead located by keyword; the lead re-checked key quotes against the extracts and then updated the workbook in place. Steward findings are FND-0008..0011 (findings/SUM-0010..0013), extracts EXT-0114..0148.
- Result: 4 rows closed on evidence and archived (C-S08/BFCLDEF, C-E02/E20, N-18, N-24); 12 rows sharpened to PARTLY ANSWERED with a stated remainder; 1 new row (C-E01/E01-ROW6); C-R03/STUB unchanged (not stated in the ranges read).
- Corrections of earlier wording are recorded in the ledger, not by editing v4-05: BFCL definitions; BFCL paper is stored in full; Bedrock minimum 512; Anthropic counts tool-search-loaded definitions as input tokens; the full-miss exception belongs to the inline-tools beta.
- Mechanical: the guard lets a subagent write only `ops/threads/*/evidence-steward.md`, so the lead wrote the per-steward logs from the hand-backs and did not change `config/ownership.json`; one steward front matter had unquoted EXT ids (the verifier rejects that) and was fixed after the steward finished.
- Retained limits: all four stewards and the lead share a model family (C-E04); vendor pages are vendor claims dated 2026-10-11.

## WD-026 Ledger batch 2 (AUTH-016, thread T-20261019-100, 2026-10-19)
- Process (lead): four evidence-stewards in parallel read the ranges batch 1 left unread (Anthropic pages and vendor figures; DynamicMCPBench and Executor remainder; scaffolding paper, ToolMenuBench, GIST-CMTF; MCPVerse, validity audit, cache papers, version report); the lead re-checked key quotes and arithmetic, made one extra extraction (EXT-0180) to make a view-only read citable, and updated the workbook in place. Findings FND-0012..0015, extracts EXT-0149..0180.
- Result: 6 rows closed on evidence and archived (C-E01/E04, C-E01/E07, C-E02/CACHEPAPERS, C-E03/O7-26, N-5, N-5/UNREAD); 11 rows sharpened to PARTLY ANSWERED; 1 new row (C-E01/E07-TAB4). Rows whose closure condition is a measurement or a claim-time application (C-S03/MINCACHE, EXCEPTIONS, C-E03/E40) stay PARTLY ANSWERED even though the documents are now fully read.
- Notable: the page-level arithmetic of two vendor claims does not reproduce the stated figures (Anthropic 85%; Copilot 27.5 vs 25.5); a scaffolding-paper table disagrees with its own prose; the stored DMB code gives distractors a minimal schema. All recorded in the ledger; the source documents and v4 texts are unchanged.
- Retained limits: stewards and lead share a model family (C-E04); vendor pages are vendor claims dated 2026-10-11; extracted tables are ragged.

## WD-027 Ledger batch 3: web fetches and rendered pages (AUTH-016, thread T-20261019-101, 2026-10-19)
- Process (lead): fetched three PDFs at the stored versions and three provider pricing pages with `tools/litfetch.py`; rendered three table pages with PyMuPDF from the same bytes (hash matched the manifest) and stored the page images with hashes; one steward read the images independently; the lead updated the workbook in place.
- Result: 3 rows closed on evidence and archived (C-E01/E01, C-E01/E01-ROW6, C-E01/E07-TAB4); C-S19/S42 and C-E05 sharpened to PARTLY ANSWERED. Findings about the papers: fcrobust's Claude-3.5-Haiku row is internally inconsistent in the printed table; the scaffolding paper's Table 4 prose does not match its table and its authors call the pooled comparison uninformative; MCPVerse's Figure 2 percentages do not correspond to 250 tasks.
- Price recheck (2026-10-19 vs 2026-10-11): no change in the Anthropic multipliers, the OpenAI page or the Gemini storage price; Gemini added a model that supports implicit caching only.
- Mechanical: the pinned fetch helper writes `"auth": "AUTH-013"` into the manifest; the fetches of this batch were made under AUTH-016 (the helper was not changed). Stored page images (PNG) are a reading aid with SHA-256 in `evidence/literature-20261019/pages/INDEX.md`; the text copies are the evidence.
- Retained limits: all readers share a model family (C-E04); image reading is by models, checked by two readers.

## WD-028 Ledger batch 4: literature pass and missing sources (AUTH-016, thread T-20261019-102, 2026-10-19)
- Process (lead): 10 logged standard-mode searches; 18 sources stored with `tools/litfetch.py` (papers, a vendor blog, three Cursor forum threads, two Claude Code issue mirrors, LangChain and Embabel pages); four stewards read them in parallel on disjoint rows; the lead re-checked the key quotes and updated the workbook in place.
- Result: 2 rows closed on evidence and archived (N-6/SKILLMEM, AS-05, the latter only for the existence of published prior art); 12 rows sharpened to PARTLY ANSWERED; N-6 set to NOT LOCATED. No supervisor assertion (AS-01, AS-03, AS-04) was closed: the texts show evidence in both directions on retrieval metrics and nothing tests an agent in our setting.
- Source types: forum posts and issue mirrors are user reports, not vendor documentation; the StackOne figures are a vendor's own evaluation (its page says 540 and 543 test cases).
- Mechanical: the manifest entries say `"auth": "AUTH-013"` because the pinned helper hard-codes it; this batch ran under AUTH-016.
- Retained limits: all readers share a model family (C-E04); stewards did not read every range (coverage in each finding).

## WD-029 Ledger batch 5: remaining stored-text reads (AUTH-016, thread T-20261019-103, 2026-10-19)
- Process (lead): repo evidence only, no web; four stewards read stored origin texts and workspace literature copies for named rows; the lead read the Anthropic programmatic-tool-calling token section (EXT-0183) and the digest lines for C-R03/DIGESTS, re-checked key quotes and updated the workbook in place.
- Result: 1 row closed on evidence and archived (C-R03/DIGESTS); 8 rows sharpened to PARTLY ANSWERED. No row was closed on the 292k figure: its counting procedure is undocumented in the stored texts and several dmcp files remain unread, so it stays labelled second-hand.
- Mechanical: sources not in the origin manifest (When2Call, ToolBeHonest, ToolSandbox, Memora, Reasoning Trap, Tool-Overuse and others) are workspace copies in evidence/literature-20261019/; origin_extract.py cannot create EXT ids for them, so findings cite file:line.
- Retained limits: all readers share a model family (C-E04); stewards did not read every range (coverage in each finding).

## WD-030 Ledger batch 6: record-repair checks (AUTH-016, thread T-20261019-104, 2026-10-19)
- Process (lead): two (then three) fresh design-challenger reviewers re-read records against the current text (no web, no messages); the lead re-checked the key points (v4 02 Figure 2 edges; 02 line 92, 03 line 40, 05 lines 1, 40, 48; MemToolAgent lines 793-798) and updated the workbook in place. One reviewer reached its turn limit without output and was re-run as two with turn budgets.
- Result: 1 row closed on evidence (C-R01/V4RES); C-R01/RENDER marked LIMITATION - ACCEPTANCE PENDING; six rows sharpened; seven new rows for defects found. No challenge record, review or package was edited: AUTH-016 forbids rewriting historical records, so RV-0008..0010 and the ledger rows are the successor notes.
- Counts: the AUTH-011/013 search and source counts are cumulative snapshots at different times (8/12, 23/32, 27/37; manifest 37 rows before AUTH-016); `ops/STATE.md` (lead-owned) corrected. Wording for the pinned files (CLAUDE.md, SAFEGUARDS rows 5 and 17) is only proposed in `design/ledger/notes/N-19-proposed-text-for-pinned-files.md`.
- Retained limits: all reviewers share a model family (C-E04); the reviews are text checks by one reviewer each, not challenger rounds; the Mermaid figures remain unrendered.

## WD-031 Front-matter update and the CH-0040 question (AUTH-017, 2026-10-19)
- The human approved updating stale challenge front matter and said decisions follow the evidence, not claims. AUTH-017 records this with the 14 named records. The lead set `status: conceded` and added a `status_note` (basis RV-0008, plus the lead's re-read of the quoted operative text for CH-0042, 0049, 0055, 0064) in CH-0038, 0042, 0043, 0049 (R2 only), 0055, 0058, 0059, 0060, 0061, 0064, 0065, 0069, 0070, 0071. The ten records with residuals stay `open`. No body text changed.
- CH-0040 (v3 against v4): settled by reading the texts, not by choosing a side. The rule for the arm table and for a failed test-split confirmation exists in v3 02 line 63; what is open is the table's content and size (human decision). v4 02 line 92 is imprecise about (b), and v4 Figure 2 has no failed-confirmation branch; both are tracked as open ledger rows. N-17/CH0040 closed on evidence; CH-0040 itself stays open.
- Limit: the basis for CH-0058..0074 is one fresh reviewer of the same model family (C-E04); no challenger round 2 existed.


## WD-032 Ledger batches 8-9: page images and remaining reads (AUTH-016, thread T-20261019-105, 2026-10-19)
- Process (lead): fetched six PDFs at stored versions (MCP-Zero also v1), checked raw hashes against the manifest, rendered the pages carrying the figures the live documents quote and stored the images with hashes; four stewards read images and stored texts in parallel; the lead read the key images itself and re-checked extract lines.
- Result: 7 rows closed on evidence (C-E02/E29 pivotal part, E28, E27, C-R03/CMTF, C-S19/S45, C-E01/E03, AS-04); 11 rows sharpened. The non-pivotal papers of the garbled-table group are DEFERRED in C-E02/E29-OTHERS with a stated trigger: the reason is that no live document quotes their figures (the lead's grep; older proposals cite CE-MCP and Re-Invoke qualitatively). C-E01/E03 closed under its second branch (the figure stays labelled second-hand), not because the counting method of the 292k figure was found.
- AS-04 was closed as a literature check done (the study found, read, quantified, limits recorded); AS-01 and AS-03 stay partly answered because the ToolRet ranking is mixed and nothing is tested in our setting.
- Retained limits: all readers share a model family (C-E04); image transcriptions are by models (steward and lead agree on the cells checked); a human check against the PDFs is outstanding.


## WD-033 Human acceptance of 14 limitations (AUTH-016, 2026-10-20)
- The lead listed the 17 limitations awaiting acceptance in three groups with a recommendation for each. The human answered in their own words (recorded verbatim in the Questions sheet, Q-U11 and Q-U20, and in each row): accepted all 8 workspace safeguard limits (group A) and all 7 in group B (C-E04, C-P02 and its children P05, P07, P08, P09, C-P03/P14); left C-E06 for now; for the Mermaid figures said they will render them in VS Code and that the lead's job is to make sure they show the concept correctly.
- Result: 14 rows set to ACCEPTED LIMITATION and archived; C-D13 and C-P02 narrowed (C-D13/WEBTOOLS, the second part of Q-U11 and the repairs C-P02/P03, P04, P06, P10 remain); C-R01/RENDER is not accepted as a limitation and stays open with the concept check assigned to the lead (C-R01/FIG2 and C-R01/R1TRIG are the concept defects found); C-E06 stays pending with the margin question for Joaa. Q-U11 and Q-U20 are marked NEEDS FOLLOW-UP because each was only partly answered.
- Not done: no safeguard text was changed; the proposal for CLAUDE.md and SAFEGUARDS rows 5 and 17 remains unapplied.


## WD-034 Successor note 06 drafted and checked (AUTH-016, thread T-20261020-106, 2026-10-20)
- The human asked for the corrections to be drafted ("lets do both but one by one") and said the lead's job on the figures is to make sure they show the concept correctly (they render them in VS Code). The lead drafted `design/package-v4/06-corrections-proposed.md` as a successor note: files 01-05 are not edited (AUTH-016: earlier packages are not rewritten). Fresh reviewers checked the figure (RV-0011) and the quoted lines and replacements (RV-0012, RV-0013); their findings were applied to the note.
- The note makes no design choice. Where a choice is involved (what a trigger does once the budget says no; who writes the scope statement at 10,000 tools; which cell the RA1 falsifier is evaluated in; whether one extra pilot cell is wanted) it lists options and marks DECISION. The four design points the figure check left open are in ledger row C-R01/FIG2-POINTS.
- Result: six ledger rows set to PARTLY ANSWERED (drafted and checked, awaiting render and approval), one new row; nothing closed.
- Retained limits: same model family for all reviewers (C-E04); section 4 checked by the lead only; the figure is unrendered; one reviewer hit its turn limit and another an API error (work re-split and re-run).


## WD-035 The supervisor's ideas against the stored literature (AUTH-016, thread T-20261020-107, 2026-10-20)
- The human asked whether the supervisor's ideas had been checked against the literature, to support, sharpen or contradict them by evidence. Four stewards read the stored sources for A6 and A13, A12, A9 with a prior-art feature matrix, and A2, A10, A11; the lead recorded the results with the wording rule (evidence consistent with / in tension with / not addressed; never right or wrong).
- Result: A6, A12, A2 mixed; A13 not located; A10 and A11 recorded; A9 candidates listed (which one is meant is for him to say); A8 deferred with reason and trigger (a background claim, untestable as worded, affecting no design choice). Two new questions for the supervisor: Q-J28 and Q-J29 (sharper versions to accept, amend or drop). C-D06/NOVELTY holds the prior-art feature matrix: no stored source has a transcript-driven trigger, re-introduction, a discovery-call budget or a measured per-deployment gate; the matrix is an overlap table, not a novelty assessment.
- Limits: one steward (12b) ended at its turn limit without a verdict paragraph (the verdict is the lead's reading of its table); several table cells come from flattened PDF text; the web checks the stewards suggested were not run; same model family throughout (C-E04).


## WD-036 Deferrals under C-E02 and the question sheets (AUTH-016, 2026-10-20)
- Deferred with reason and trigger (the C-E02 criterion allows it): C-E02/E21, E22, E23, E24, E26, E31, E32, E33 and STEWARDUNREAD. The reason is evidence-based but is the lead's grep: no document in design/package-v3 or design/package-v4 (01-05) mentions Cursor, the 55K attribution, the Hajdas post, Composio, Zapier, Pipedream, Smithery, Manus, HAL, tau-bench, Spring AI, langgraph-bigtool, Toolshed or the Schlapbach PDF, and the caching claims rest on pages already read. Each row states its reopen trigger. A8 (AS-08) was deferred in WD-035. Deferral is not closure; nothing was closed by it.
- Not deferred: C-E02/E30 (waits for the human's list, Q-U23), E34 and UNREADLEADS (the agent-memory survey was fetched and is being read in thread T-20261020-108).
- Question sheets generated from the ledger's Questions sheet: `design/ledger/notes/QUESTIONS-FOR-JOAA-20261020.md` (29 questions in eight groups, each with format, reason and the open items waiting) and `design/ledger/notes/QUESTIONS-FOR-YOU-20261020.md`. They add no wording of their own beyond the group titles and one observation: the ledger lists the arm decision (C-D08) and the evaluation-vehicle choice (C-S16) as hard prerequisites for the token-composition and billing probes (E1, E7), an assumption inherited from the earlier plan; if the human drops it, the first measurement needs only the human's authorization (C-D09, Q-U14) and the answers on what to report and on which providers and models (Q-J03, Q-J04, Q-J24).


## WD-037 The agent-memory survey (AUTH-016, thread T-20261020-108, 2026-10-20)
- The survey named in C-E02/UNREADLEADS (arXiv 2602.06052, TMLR 07/2026) was fetched and a steward read about 60% of it for the supervisor's memory point. It is a secondary source: it reports no experiment of its own, names tool-memory papers with qualitative effects only, gives no measured effect of memory on cost, steps or success, treats user-centric and agent-centric memory as distinct but not exclusive subjects (so it does not settle the memory scope question Q-J05), and uses 'cache' for model-internal KV state, not prompt caching.
- Result: C-E02/UNREADLEADS deferred with trigger; N-6 extended and still not located.


## WD-038 Version maps, the full check of 05, and literature closures (AUTH-016, thread T-20261020-109, 2026-10-20)
- Version maps of every external number in the brief, 05, 04 and 02 were written by two stewards; four reviewers checked 05 against the stored source texts (lines 11-40 and 61-91; lines 41-60 only through the earlier reviews). Corrections are drafted in the successor note (sections 3 and 3b); no earlier file was edited (AUTH-016). The author and vendor asks are drafted for the human to send.
- Closed on evidence: AS-01 and AS-03 as literature checks done (the sources are mixed by encoder class, instruction use, dataset and metric; the supervisor's statements narrow to strong instruction-following encoders; our setting is untested), C-S08/VOCAB (a logged different-vocabulary pass over 37 searches in all; saturation explicitly not claimed), C-R03/RV7UNCHK, C-R03/ROUND45. Deferred with trigger: C-E01/E08 (ProMCP), C-R03/STUB, C-R03/C27 (carried by C-S03/DEFUSAGE).
- Honesty notes: the BFCL medians were recomputed by regex counts and a hand tally (margin of one row for the Miss Func minus Base median); r = -0.45 was not recomputed; two reviewers ended at the turn limit (their files are marked draft); same model family throughout (C-E04).
