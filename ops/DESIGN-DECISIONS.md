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

## WD-012 Review-driven corrections (RV-0001)
Applied: guard hardening (wildcard/parent/`..`/outside-workspace paths, no sanctioned-name exemption, `.git` and local-settings protection, `match()` dot bug), SendMessage allow-list, message-cap hook, config pin, `approved` records may not cite AUTH-001, deny rules for outbound/scheduling tools, CAVEATS rows 3/10/12/15 corrected, REQ-U1 and REQ-D1 scopes restored, template seeds neutralised, severity/status vocabulary unified, message kinds unified, round and message definitions, steward command form, source counts corrected, claim about C4 as a model audit removed. Not applied (kept as documented limits): OS sandbox, Bash write ownership, foreign agent-id resolution (untested), interactive/VS Code behavior (untested). Details: `ops/threads/T-20261016-91/SUMMARY.md`.
