---
id: "FND-0019"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: "T-20261019-102"
evidence: ["EXT-0131", "EXT-0158", "EXT-0074"]
---

# FND-0019: Batch 4d, missing sources (Cursor forum, Claude Code issues, ToolHop)

Scope: ledger rows C-E02/E21, C-E02/E25, C-E02/E26 and evidence for C-S03/DEFUSAGE. Sources are stored texts in `evidence/literature-20261019/` (abbreviated `lit-...`). Citations are `file:line` of the stored text. No origin extraction was run (no row named a stored origin source); the front-matter EXT ids (EXT-0131 Anthropic tool search usage, EXT-0158 Anthropic tool-use-with-caching page, EXT-0074 Anthropic advanced tool use) are existing extracts that bear on rows E25/DEFUSAGE and were NOT re-read by me in this session [U]. Everything below is a prior-art or user-report claim, not a verified fact. Forum posts and issue mirrors are not Cursor or Anthropic documentation.

## Row C-E02/E21: Cursor tool cap (forum threads, three stored texts)

Verdict: **PARTLY** (number, behaviour, dated user statements found; no official Cursor documentation text and no staff statement on a change to 80 found in these texts).

| Item | Text (file:line) | Class |
|---|---|---|
| Cap 40, tools above it invisible | `lit-cursor-forum-40-tool-limit.txt:25-27`: "I've got 50 tools enabled, but Cursor caps it at 40, meaning some tools just aren't available to the agent." Screenshot caption: "You have 50 tools from enabled servers. The limit is 40 tools – some tools may not be available to the agent." (post 20 Apr 2025, user kitaekatt) | user report quoting the Cursor UI warning |
| "hard cap to manage the context window (per Cursor's docs)" | same file:29 | user paraphrase of docs, docs not shown |
| Docs quoted by a user: first 40 sent | `lit-cursor-forum-tools-limited-40.txt:49`: "Currently, Cursor will only send the first 40 tools to the Agent." (user wesley-harding, 21 Mar 2025, quoting "Cursor – Model Context Protocol" docs page) | user quotation of vendor docs [F that the user posted it; whether the docs said so is not verifiable here] |
| Observed behaviour | `lit-cursor-forum-tools-limited-40.txt:23-25`: claude-3.5-sonnet (and 3.7) "failed to find the last 4 tools provided by slack"; seen after disabling the github server (user mieslep, 21 Mar 2025; one user, one setup) | user report |
| Cap is on tools presented, not calls | same file:69 ("it is only the 'first 40 tools'") | user |
| Possible dated change by staff | `lit-cursor-forum-tools-limited-40.txt:167` (4 Apr 2025, user "deanrie"): "Hey, I think we will be able to implement this soon." (about per-tool enable/disable). Role of this user is not shown in the text [U]; it is not stated to be staff. | unlabeled; cannot be called a staff statement from the text |
| "team said they might" raise limit | `lit-cursor-forum-40-tool-limit.txt:63` (14 Jun 2025, user algis, who also promotes his own proxy product): "the team said they might and/or add per-tool toggles" | second-hand user claim, self-interested |
| Later claim: 80 tools, no warning, dynamic context discovery | `lit-cursor-forum-quantity-limit.txt:23`: "someone say ... increased to 80. I want to confirm what the current official limit ... is." Reply (3 Mar 2026, Naufaldi_Rafif, `:35-47`): "Cursor has already implemented Dynamic Context Discovery: https://cursor.com/blog/dynamic-context-discovery"; "I'm currently running more than 80 tools enabled, and there's no warning message at all."; "In older versions of Cursor, such as v1 or versions below 2.3, you would usually get a warning suggesting limiting tools to under 50."; "This strategy reduces total agent token usage by up to 46.9%" | user reports; the 46.9% figure is repeated by a user, its source/conditions are not in this text (the blog was NOT stored, so I cannot check it) |
| Resolution | `lit-cursor-forum-quantity-limit.txt:59-61`: asker says the answer "perfectly resolved all my doubts"; no staff reply visible | |

[F] No staff or moderator statement is identifiable in any of the three texts (author roles are not shown). [O] The three texts conflict on the number in time order: 40 (Mar-Jun 2025), "warning suggesting under 50" in versions below 2.3 and "80+ with no warning" (Mar 2026). [I] The stored texts support "a 40-tool cap existed in 2025 per user reports and a quoted docs line" and "a user reported in Mar 2026 that it no longer applied"; they do not give the version or date of the change. [U] Whether "80" was ever an official figure; the dynamic-context-discovery post (not stored); the 55K attribution mentioned in the row (not in these texts; searched by reading all three in full, 126, 226, 120 lines). Behaviour above the cap is as reported by users: extra tools "stay invisible" (`lit-cursor-forum-40-tool-limit.txt:63`, algis).

Relevance to our setting: PARTIAL, it documents one vendor's fixed-count exposure cap and users' suggested "list servers then expand" workaround (`lit-cursor-forum-tools-limited-40.txt:29`, `:99-105`, user proposals, not Cursor behaviour), but nothing here measures discovery or cost.

## Row C-E02/E25 and C-S03/DEFUSAGE: Claude Code issues 59650 and 30920 (issue mirrors)

Verdict C-E02/E25: **PARTLY** (both reports read in full; the status "closed - not planned" is shown; no maintainer reply or fix is in the mirror; "the cache-read inflation anecdote" is now seen to be a single user's self-measurement, still unverified by anyone else). Verdict C-S03/DEFUSAGE: **PARTLY** (one user report asserts deferred schemas are re-read each call; no vendor confirmation in the text and the figures contradict the vendor-side meaning of "deferred" only if the user's reading is right, see below).

Issue #59650 ("Deferred MCP tool schemas inflate cache reads and per-turn token counts unnecessarily"), `lit-ccissue-59650-deferred-cache-reads.txt`:
- Status/meta: ":6" "Closed — not planned"; ":7" "Maintainer reply None cached"; ":8" "2 comments · opened May 16, 2026 · closed Jun 14, 2026". The two comments are not in the mirror. Resolution rationale: not shown.
- Conditions (`:21`, `:50-52`): "Opus 4.7, 1M context", Claude Code CLI on Windows 11/PowerShell, long multi-hour session; Claude Code version field reads only "claude code" (`:137`), "Platform: Anthropic API" (`:141`); marked a regression "Yes, this worked in a previous version" (`:129`) but "Last Working Version _No response_" (`:131-133`). [O] the form is internally inconsistent about OS/terminal (Windows vs "Terminal.app (macOS)", `:145-149`).
- The numbers (`:21`): "cumulative cache-read tokens reaching ~35.3M and at least one individual turn reported at ~150k tokens".
- `/context` breakdown (`:25-33`): "Total: 239.9k / 1M (24%); System prompt: 9.5k; System tools: 18.3k; MCP tools (active): 2.6k; MCP tools (deferred): 87.8k; System tools (deferred): 15.1k; Memory files: 1.3k; Skills: 4k; Messages: 204.2k". `:34`: "The combined ~103k of deferred tool definitions is loaded into the cache and re-read on every API call".
- Estimate by the user (`:40`): "Over 100+ API calls ... the ~103k of deferred-tool overhead alone contributes roughly 10M of cumulative cache reads for tools that were never used." [O] arithmetic of the user: 103k x ~100 calls = ~10M; this is the user's estimate, not a measured split.
- Billing statement by the user (`:41`, `:76`): "Cache reads are billed at 10% of input price"; "'35.3M cache reads' ... costs the same as ~3.5M input tokens".
- Request: lazy-load deferred schemas keeping "only names" (`:44`, `:61-65`), per-session opt-out (`:45`), a /context hint (`:46`), evictable ToolSearch results (`:47`, `:66-67`); expected end state "Base cache per API call: ~50k instead of ~240k" (`:80`).
- Internal tension [O]: the user's own breakdown lists Messages at 204.2k of 239.9k (`:33`) while saying the deferred block is ~103k (`:34`); 103k + the other items cannot sum to 239.9k together with 204.2k messages (listed items sum to about 342k, the text's "Total 239.9k" is not reconciled). I did not resolve this; the breakdown may use overlapping categories. Flag for any reuse of these numbers.
- Related titles listed on the mirror (titles only, not read): #80527 "/context counts tool schemas as 'Messages'" (Open), #97388 "Per-server defer/eager policy for MCP tool schemas" (Resolved) (`:163-174`). [I] #80527's title suggests /context category labels may be unreliable; the text of that issue is not stored.

C-S03/DEFUSAGE evidence from #59650: [F, user report] the user states deferred schemas are in "the base cache block" and "re-read on every API call regardless of whether the model invokes them" (`:107`) and that the "MCP tools (deferred): 87.8k" line was unchanged between two /context runs (`:101-103`). [U] The issue shows no raw API usage object: the 35.3M is from /cost and the per-turn ~150k is from the status line; neither is split by schema class. Contrasting vendor-side description is in EXT-0131 / EXT-0158 / EXT-0074 (not re-read by me; the lead or a peer should compare). Closed as "not planned" with no maintainer text cached: does NOT show the claim is wrong or right.

Issue #30920 ("API Error: MCP tools cannot have both defer_loading=true and cache_control set"), `lit-ccissue-30920-defer-cachecontrol.txt`:
- Meta: Reported on v2.1.69 (`:7`); "Closed — not planned" (`:6`); "Maintainer reply None cached" (`:8`); "Workaround ✓ Mentioned in description" (`:9`); "3 comments · opened Mar 5, 2026 · closed Apr 2, 2026" (`:10`); model "Opus" (`:47`), macOS (`:67`).
- Setting (`:22`): "3+ MCP servers, ~50+ tools total, every API request fails with a 400 error."
- Error (`:31-34`): "Tool 'mcp__atlassian__getConfluencePage' cannot have both defer_loading=true and cache_control set. Tools with defer_loading cannot use prompt caching."
- Cause (user's reading of client code, `:75-78`, `:88`): both flags set unconditionally; "Tool search defaults to 'tst' mode when ENABLE_TOOL_SEARCH is unset, which enables defer loading for all MCP tools."
- Workaround (`:43`): "ENABLE_TOOL_SEARCH=false claude disables defer_loading and resolves the issue."
- Not shown: the fix. The mirror's related list shows #30989 "Resolved", and #86743 "defer_loading + cache_control 400 still present in 2.1.223 (recurrence of #30920)" "Resolved" (`:98-101`); titles only. [F] the API error text itself states that deferred tools cannot use prompt caching (`:34`) [relevance to DEFUSAGE: this quoted API message is a vendor error string reproduced by a user; it bears on the caching interaction (compare EXT-0158)]. [U] Which release fixed it.

Relevance to our setting: #59650 PARTIAL (a client-side cost anecdote about unused deferred schemas, one user, 1M-context session); #30920 PARTIAL (shows deferral and prompt caching were incompatible per an API error string at one version).

## Row C-E02/E26: ToolHop (`lit-toolhop-2501.02506v4.txt`)

Verdict: **ANSWERED** for what ToolHop measures; **NOT FOUND IN THESE TEXTS** for any discovery of hidden tools or exposure/token-cost measurement.

| Item | Text (file:line) |
|---|---|
| Size | `:21` "995 user queries and 3,912 associated tools"; `:641` "3,912 locally deployable and directly executable tools" |
| Models | `:30-32`: "14 LLMs across five model families (i.e., LLaMA3.1, Qwen2.5, Gemini1.5, Claude3.5, and GPT)" |
| Headline | `:34-36`: "GPT-4o, achieves an accuracy of 49.04%"; `:931-933`: "GPT-4o, achieves only 49.04% answer correctness in this scenario. Furthermore, 9.45% of queries exhibit hallucinations." |
| Scenarios | `:886-893`: direct answer; mandatory tool use ("required to use provided tools"); free choice ("external tools are available but optional") |
| Tool effect | `:923-926`: tools raise correctness "by an average of 12.29%"; GPT family "23.59%" |
| Error types | `:900-903`: "tool hallucination, where models invoke tools not included in the provided toolset; parameter hallucination ...; parameter missing" |
| Tools per query | `:631-633`: "the number of tools required per query ranges from three to seven" |
| Limits (authors) | `:1187-1190`: lack of "an immediate strategy for enhancing these capabilities" |

[O] The task is multi-hop composition of 3-7 dependent tools per query; tool sets are locally executable and supplied; the evaluated hallucination is invoking a tool not in the provided toolset. [U] The stored text I read does not state how many tools are exposed to the model in one prompt (all 3,912 versus the query's own tools); I did not read the whole 2,213-line file (read: abstract, lines 16-43, 625-664, 828-940, 1060-1080, 1184-1203, plus keyword greps for retrieval/hidden/discover/tokens/cost). The keyword grep for "tokens", "hidden", "discover" and "retriev" found only unrelated hits (`:52`, `:78`, `:1405`, `:1808`). Free-choice results (Table 4) not tabulated by me beyond GPT-4o's row (`:832-837`, values read as Direct 23.12, Mandatory 49.04, Free 47.74, hallucination 9.45/4.31; column labelling taken from the Table 4 caption, `:838-842`, and not independently confirmed from layout). One-family-per-prompt model lists and "tool hallucination" are prompt-based observations.

Relevance to our setting: NOT RELEVANT to discovery of hidden tools or to bill; PARTIAL only as a source of a tool-hallucination rate (invoking a tool outside the provided set) in a small, supplied, locally executable set.

## Summary of verdicts

| Row | Verdict |
|---|---|
| C-E02/E21 | PARTLY |
| C-E02/E25 | PARTLY |
| C-S03/DEFUSAGE | PARTLY (single user report) |
| C-E02/E26 | ANSWERED on what ToolHop is; NOT FOUND IN THESE TEXTS for discovery or exposure cost |

## Coverage

Read in full: the three Cursor forum texts and both issue mirrors. ToolHop: partial (see above). Not read: the Cursor docs, cursor.com blog, Hajdas post, the Claude Code changelog, GitHub issue comment threads (not in mirrors), Schlapbach PDF.
