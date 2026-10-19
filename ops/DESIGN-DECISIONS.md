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
