# N-19: proposed wording for pinned files (for the human's review; nothing here has been applied)

Written 2026-10-19 by the lead (Sonnet 5.5) for ledger row N-19. `CLAUDE.md` and `ops/SAFEGUARDS.md` row text predate AUTH-012, AUTH-014, AUTH-015 and AUTH-016. `CLAUDE.md` is pinned in `config/PINNED.json`; changing it needs the human's review and a re-pin. `ops/SAFEGUARDS.md` is not pinned but is a safeguard record, so the same review applies. The proposals only describe what the authorization register already says; they widen nothing.

## 1. CLAUDE.md, "What you may and may not do", bullet 4 (line 11)
Current: "No remote repositories, pushes, pulls, clones, software installs or purchases. Commits are local and need the human's approval prompt."

Proposed: "No remote repositories except the private remote the human authorized in AUTH-012 (pushes by the human only), no pulls, clones, software installs or purchases. Public web searches and fetches by the lead are allowed only inside an AUTH that names the topic (AUTH-011, AUTH-013, AUTH-016); fetched text is stored under `evidence/literature-*` with URL, time and SHA-256 and is source material, not a finding; agents have no web tools. Commits are local and need the human's approval prompt."

## 2. ops/SAFEGUARDS.md row 5
Current: "No git remote, push, pull, fetch, clone, `git config`; no package installs (pip/npm/winget/choco). ..."

Proposed addition at the start: "Exception: the one authorized remote `origin` (AUTH-012); `verify` flags any other remote; pushes are the human's. The pinned fetch helper `tools/litfetch.py` (AUTH-015) is the only sanctioned download route (http(s) only, writes only under `evidence/literature-20261019/`); other download routes (`curl`, `Invoke-WebRequest`) are still unlisted (RV-0001 D5)."

## 3. ops/SAFEGUARDS.md row 17
Current: "2 rounds per issue, no spawning, no web"

Proposed: "2 rounds per issue, no spawning; no web for agents (the lead's web use is limited by the AUTH that covers the task: AUTH-011, AUTH-013, AUTH-016)".

## What I did not change
No file was edited for this note except `ops/STATE.md` (lead-owned), where the AUTH-011/013 search and source counts were corrected (see ledger row N-19 and WD-030).
