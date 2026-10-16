# thesis-policy-design

A reusable workspace for **future, human-authorized, conceptual** work on a tool-access policy design for a master's thesis, using a small team of communicating Sonnet 5.5 agents. It was bootstrapped on 2026-10-16 from the completed clean-room research repository (the *origin*), which stays untouched. **No design, selection, search, experiment or reconciliation has been done here.**

## Open (fresh Claude session)
```
cd C:\Users\omr\Documents\thesis-policy-design
claude
```
or open that folder in VS Code and start Claude Code there. Accept the folder-trust dialog. (All bootstrap tests ran non-interactively in a folder Claude Code reported as **not yet trusted**: the project's `permissions.allow` entries were ignored, while deny rules, the hook, the model pin and the agents took effect. Interactive behavior after trust is untested.) Then: check `/hooks` and `/permissions`, run `python tools/verify_workspace.py --quick` (expect `fail=0`), and stop if it reports FAIL. Do not start from the origin folder: its own instructions and agents would load.

## Where things are
| What | Where |
|---|---|
| Operating instructions (loaded every session) | `CLAUDE.md`, `ops/STATE.md` |
| Enforced configuration | `.claude/settings.json`, `tools/guard.py`, `config/ownership.json`, `.claude/agents/*.md` |
| What is enforced vs only instructed, tests, known bypasses | `ops/SAFEGUARDS.md`, `ops/tests/README.md` |
| Why it is built this way | `ops/DESIGN-DECISIONS.md` |
| Agent protocol and thread records | `ops/PROTOCOL.md`, `ops/threads/` |
| What the human has authorized | `ops/AUTHORIZATIONS.md` |
| Evidence (governing copies, source manifest, extraction tool, caveats) | `evidence/`, `tools/origin_extract.py` |
| Requirements and inputs from the human | `requirements/` |
| Proposed first session (not executed) | `ops/FIRST_SESSION.md` |
| Integrity check | `python tools/verify_workspace.py [--quick]` |
