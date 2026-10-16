# T-20261016-92 SUMMARY: agent-ID and peer-messaging smoke test (AUTH-002 item 1; content-neutral)

Written by the lead. Sources: the two agents' thread logs, their final reports (delivered to the lead as hand-back messages), `messages.log`.

## Results
- [O] The Agent tool in this VS Code runtime has no `name` parameter; spawn returns an agent id of the form `a` + 16 lowercase hex characters (both ids matched `a[0-9a-f]{16}`). The SendMessage tool description in this runtime also mentions names, teammates and `ListAgents` targets; the guard still refuses those (by design, WD-004).
- [O] The guard accepted lead -> agent (2 sends), agent -> agent (steward -> proposer, proposer -> steward). `messages.log` shows 4 of 6 counted sends, attributed to `lead`, `evidence-steward`, `design-proposer`. No send was refused. **No guard correction was needed and none was made.**
- [O] Nonce round trip worked: the steward's message containing NONCE-4c81e7 reached the proposer; the proposer's reply "NONCE-4c81e7 RECEIVED" reached the steward.
- [O] The evidence-steward's Bash ran `python tools/verify_workspace.py --quick` as a single command without a denial (output: pass=125 warn=1 fail=0; the warning was uncommitted changes of this session).
- [O] This runtime delivers an agent's final report to the lead through a separate hand-back channel (the steward saw a "[handback-send-enforce]" reminder). That channel is not SendMessage, is not matched by the guard and is not counted against the cap.

## Not shown by this test
- [U] Whether an idle (finished) agent is resumed by a message from a *peer* rather than the lead: the lead's messages resumed both agents; the proposer's reply reached the steward while it was running.
- [U] Behaviour with three agents, with contested issues, near the cap, or with two threads at once; agent-team features; whether ids resolve across sessions.
- [U] Token cost of the test was not recorded beyond the harness figures (about 13-18k tokens per agent for these trivial turns).
- A different Claude Code version could change the id format; the guard fails closed if it does, so the symptom would be refused sends, not a bypass.
