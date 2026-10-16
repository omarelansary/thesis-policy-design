# Thread T-20261016-92: TASK (agent-ID and peer-messaging smoke test; content-neutral)

- Authorization: AUTH-002 item 1: "Verify the actual agent ID format and peer-to-peer messaging in this VS Code runtime through a small, content-neutral test."
- Question or artifact to produce: (a) the real format of the agent ids returned by the Agent tool in this runtime and whether tools/guard.py accepts them; (b) whether two agents can message each other directly and receive the reply; (c) whether the evidence-steward's Bash can run the sanctioned verify command. No scientific content is involved.
- Out of scope: everything in AUTH-002 limits; no evidence extraction, no design, no records other than the two agents' own thread logs.
- Evidence the agents may use: none. Do not read other files than this TASK.md, ops/PROTOCOL.md and your own thread log.
- Issues to be debated: none. Procedure: lead spawns two agents in standby; lead sends each a roster plus one instruction; evidence-steward sends one message to design-proposer containing a nonce supplied by the lead; design-proposer replies with the same nonce and the word RECEIVED; evidence-steward then runs `python tools/verify_workspace.py --quick` as a single command and reports its SUMMARY line.
- Bounds: agents = [evidence-steward, design-proposer]; no rounds; cap 6 (lead 2 tasking messages + 2 peer messages + 2 spare); web searches = 0; no agent spawning by agents.
- Deliverables and owners: ops/threads/T-20261016-92/evidence-steward.md -> evidence-steward (log of messages it sent or received, verbatim); ops/threads/T-20261016-92/design-proposer.md -> design-proposer (same); SUMMARY.md -> lead.
- Escalate to the lead when: a send is refused (quote the refusal text verbatim in the final answer).
- Stop condition: both agents give a final answer. The lead then deletes ACTIVE.json, writes SUMMARY.md and continues with the remaining AUTH-002 items.
