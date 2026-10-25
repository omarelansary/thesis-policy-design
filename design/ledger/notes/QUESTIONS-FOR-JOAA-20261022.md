# Questions for the supervisor from the V5 audit (2026-10-22; successor to QUESTIONS-FOR-JOAA-20261021.md, which is unchanged)

Written for: A.F.M. Mohimenul Joaa, through the student. Source: `design/package-v5/05-poc-loop-and-e2e.md` section 4. These are proposed rows; they enter the ledger only when the student approves `design/package-v5/08-ledger-proposals.md`.

1. **Q-J31. Is this staged form what you meant?** The policy has three stages that decide which tools the model sees: what the deployment or invoker may use at all; which tools this user needed before (offered at session start, only where it pays); and on-demand search for anything else, which also brings back anything held back. By default only two of these act: offering from memory stays off until it is measured to pay, and a small deployment simply exposes all its tools. It has no separate per-request filtering stage and no 1,000-to-10 cascade, because each extra model-answered step costs a request and the evidence for extra steps on the bill is missing. Is that acceptable as the staged graph of 14 October?
2. **Q-J32. Count offered or definitions sent?** Two providers now let a policy change which tools are *offered* each turn while all definitions stay cached. That reduces the number of tools the model sees, but not the definitions billed (they are read at the cache price on every request). When you say "reduce the count of tools", do you mean the tools offered to the model, or the definitions sent and billed?
3. **Q-J33. Which Executor?** Should the Executor baseline use Executor's own MCP setup as shipped (the open-source project now at UsefulSoftwareCo/executor), or a configuration you have in mind?

## Status (2026-10-22, after INT-T-006 and INT-T-007)
All three were answered by the student on the supervisor's behalf (REGISTER H.4); the supervisor may still confirm in his own words.
- Q-J31: answered (REQ-J22-01). The staged approach is a starting point; memory must not stay off and is tested with returning users.
- Q-J32: answered (REQ-J22-02). The count of tools was an example; the goal is the bill.
- Q-J33: answered (REQ-J22-04). Executor is a source of reusable parts and an optional baseline (`design/package-v5/03` section 4a).
