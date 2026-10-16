# Workspace state (imported into every session; keep under 40 lines)

- Phase: **bootstrap complete, awaiting human review** (set by the lead 2026-10-16). No design task is authorized.
- Authorizations in force: AUTH-001 only (bootstrap; ended at handoff). See `ops/AUTHORIZATIONS.md`.
- Origin snapshot: research-cleanroom commit `67e5eeec4b61` (2026-10-16). 39 governing copies, 239 stored sources, restricted set withheld. Details: `evidence/README.md`.
- Thesis question: **not yet supplied** (`requirements/THESIS_QUESTION.md`). 2026-10-14 supervisor instructions: **not yet supplied** (`requirements/intake/`).
- Candidate set C1-C6 and the S4G directions are historical assessments; no selection was ever made. Nothing in this workspace has selected a question, policy or architecture.
- Agents: evidence-steward, design-proposer, design-challenger (Sonnet 5.5). Runtime agents from the bootstrap are gone; definitions persist. Protocol: `ops/PROTOCOL.md`.
- Last full verification: see `ops/tests/` (latest log) and run `python tools/verify_workspace.py`.
- Open items for the human: (1) review the workspace and `ops/SAFEGUARDS.md` limits; (2) supply the thesis question and 2026-10-14 material; (3) authorize the first design task (suggested entry: `ops/FIRST_SESSION.md`); (4) decide whether to try native agent teams (untested here).
- Next action for any session: read this file, run `python tools/verify_workspace.py --quick`, and wait for an AUTH.
