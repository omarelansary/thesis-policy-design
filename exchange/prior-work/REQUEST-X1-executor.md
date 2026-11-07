# Request X1 to the human's describing agent: the Executor test repository (written by the reader, 2026-11-07)

**What this is.** The human asked for an agent that fetches the repository where the human ran the Executor tests and describes it (INT-T-023 line 20, REQ-U1107-06). The reader's pointer to this request is THREAD E-30. The rules of `README.md` in this folder apply in full: describe, do not conclude; no result values, effect sizes or verdicts; point to where you read each statement; write only inside `exchange/prior-work/`. This request adds the points below and narrows rule 5.

**Why.** Two open questions depend on it. The supervisor's question Q-J33 asks which Executor a baseline should use: Executor's own MCP setup as shipped (the open-source project now at UsefulSoftwareCo/executor), or a configuration of the human's. The reader's design (`design/package-v5/03` section 4a) reuses Executor in parts and keeps "Executor as shipped" as an optional baseline. PWD-017 already describes the 426-slot run. What it does not say is how far the tested Executor differs from Executor as shipped, or what a new run would need.

## Hard rules for X1
1. **Fetch and read only.** Fetch the repository (or repositories) on your side, outside `thesis-policy-design` and outside its parent folder, read-only. Do not run, build or install anything from it, and run no model calls.
2. **Rule 5 is suspended for X1.** No reruns, even where the model set has changed. If you think a rerun is needed, say so once in THREAD.md with the reason; the human decides and authorizes it separately.
3. **Result folders stay closed.** Do not open scoring, analysis or completion records that hold result values, for example `PO/exb_scores_*`, `PO/exb_analysis_*`, sealed pilot scores, or validity and freeze records with figures. File names, sizes and hashes may be listed. If a file mixes setup and results, describe the setup part and say that the file also holds results.
4. **No secrets or personal data.** Write no keys, tokens, key identifiers, e-mail addresses, private hostnames or personal paths. Use placeholders such as `<repo>` and `<home>`.

## What to describe (write `PWD-019.md` in the template of `README.md`, plus the extra sections below)
1. **Where it is.** The human will clone their thesis workspace, which holds the Executor work in `thesis-private`, for you to explore (INT-T-024 line 4). Repository names, remote URLs if public (otherwise "private"), branch and commit of each part read, and the date fetched. PWD-017 names `thesis-main`, `mcp-atlas-ramya-handoff` (branch `g8-mech-pilot`), `PUBX/`, `PRIV/` and `PO/`. Say which of these you could reach, and whether the clone is one of the two copies of the thesis workspace that were reported in the Windows parent folder.
2. **Executor as tested against Executor as shipped.**
   - The Executor commit used (PWD-017 says `98d606b`), its upstream repository and how far it is behind or ahead of upstream at fetch time (commit count and date).
   - Every local change to Executor's own code or configuration: file, kind of change (patch, setting, wrapper), and its stated purpose.
   - Which of Executor's documented tools (`skills`, `search`, `describe`, `call`, `execute`, `resume`) were offered to the model, and how. PWD-017 lists three provider tools: `execute`, `skills`, `resume`. Say where `search`, `describe` and `call` went, for example inside code mode.
   - How the 20 per-server MCP facades were built, and whether they change tool names, descriptions or schemas against the MCP-Atlas servers.
   - Scoped connections, approvals and limits as configured (code size, call count, time, output bytes) against Executor's documented defaults.
3. **The harness.** The runner (`run_executor_baseline.py` and anything it calls): how a slot is run, the system and user messages (PWD-017: no system prompt), the retry and turn caps, how the tools array is built per call and whether it stays fixed within a run, and what is logged per call (field names only: tokens, cached tokens, cache-write tokens, cost, provider, model id as served).
4. **What a new run would need.** Models and providers the contracts name, and which of them are served now: check the live status at https://llm.scads.ai/status/state.json and give the time read. Also the software needed (container, Node or Deno, MCP servers, keys for which services, without the keys themselves), any MCP-Atlas server that needs an outside service, and the requests per slot as recorded (count of calls only, no outcome).
5. **Licences.** The licences of Executor, MCP-Atlas and the facades, as stated in the repositories.
6. **Reusable materials.** Path, format and size of each: task list (ids only), tool catalogue, facades, runner, trace-audit script, contract JSONs.
7. **Not done or not recorded.** For example the uncommitted scoring amendment in a worktree, and the untracked records PWD-017 mentions.

**Reply.** `PWD-019.md` in this folder, and a THREAD.md entry answering E-30 that lists the files written, the UTC time of the fetch, and every point you could not answer and why.
