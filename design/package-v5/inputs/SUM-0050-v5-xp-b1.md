---
id: SUM-0050
type: summary
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-28
thread: T-20261027-122
evidence_lines: [v5-xp-anthropic-tool-search-doc.txt, v5-xp-anthropic-tool-caching-doc.txt, v5-xp-claude-prompt-caching-doc.txt, v5-xp-openai-tool-search-doc.txt, v5-xp-anthropic-advanced-tool-use.txt, v5-xp-anthropic-code-exec-mcp.txt, v5-xp-openrouter-tool-search.txt, v5-xp-litellm-anthropic-tool-search.txt, v5-xp-litellm-mcp.txt]
---

# SUM-0050: batch X claims X1-X7 checked against stored text (SUM, unverified)

Files are in `evidence/literature-20261019/`. Line numbers are those of the stored .txt. This is a check of scout claims against stored text (a summary I wrote), not a finding. Each row reports what the stored page says (a prior-art claim), not whether it is true.

| # | Verdict | Lines | Short exact quote | Note |
|---|---|---|---|---|
| X1 | CONFIRMED | tool-search-doc 131, 244, 252, 258, 327, 484, 522 | "The API runs the search and returns the matching tools as tool_reference blocks (up to 5 by default" ; "You still send every tool's full definition in the tools array on every request" ; "Keep your 3–5 most frequently used tools non-deferred" ; "The prefix is untouched, so prompt caching is preserved." ; "the tool definitions that search loads into context count as input tokens like any other tool definition" ; "by returning tool_reference blocks from a custom tool" | The page also says Claude can set a limit "to any integer from 1 to 10,000" (l.484). Line 258 holds both the "excludes deferred tools from the system-prompt prefix" and "appends a tool_reference block inline ... then expands it into the full tool definition" sentences. No wrong number. |
| X2 | CONFIRMED | tool-caching-doc 100, 102, 108, 136; prompt-caching-doc 529 | "adding tools dynamically through tool search does not break your cache" ; "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" (prompt-caching-doc table row marks ✘✘✘ for tools, system, messages) ; "Tool searchDiscovered tools load as tool_reference blocks, preserving prefix cache" | Wording "invalidates the entire cache" is from the prompt-caching table only. |
| X3 | CONFIRMED | openai-tool-search-doc 840, 856, 858, 924, 2315, 2323 | "For an individual deferred function, the model still sees the function name and description, so in practice tool search is mostly deferring the parameter schema." ; "aim to keep each namespace to fewer than 10 functions" ; "In the Responses API, only gpt-5.4 and later models support tool_search." ; "changing the loaded tool set will break the model's cache from that point forward" ; "they are injected at the end of the context window" | Client mode: "The model emits a tool_search_call, your application performs the lookup, and you return a matching tool_search_output." No wrong number. |
| X4 | CONFIRMED | advanced-tool-use 55-60, 66 | "Total context consumption: ~77K tokens" ; "Total context consumption: ~8.7K tokens" ; "Only the Tool Search Tool loaded upfront (~500 tokens)" ; "(3-5 relevant tools, ~3K tokens)" ; "an 85% reduction" ; "Opus 4 improved from 49% to 74%, and Opus 4.5 improved from 79.5% to 88.1%" ; "Tool Search Tool doesn't break prompt caching" | The 49-74 and 79.5-88.1 figures are stated as "Internal testing" on the page. The 24 Nov 2025 date was not checked in this pass. |
| X5 | CONFIRMED | code-exec-mcp 128, 134 | "Including a detail level parameter in the search_tools tool ... (such as name only, name and description, or the full definition with schemas)" ; "reduces the token usage from 150,000 tokens to 2,000 tokens" | Line 134 describes the detail parameter as an option ("also helps"), with no measurement. The 150,000 to 2,000 figure is for a filesystem-exploration example (l.128), not for the detail-level parameter. The 4 Nov 2025 date was not checked. |
| X6 | CONFIRMED (one cap nuance) | openrouter-tool-search 38, 96, 114, 135, 180, 194, 35 | "Tool search works on any model and any provider" ; "matched case-insensitively against each deferred tool's name, description, argument names, and argument descriptions" ; "Discovering a tool does not disturb the tools already in the conversation, so prompt caching is preserved across a search" ; "The Chat Completions API does not accept it in tools and returns a 400" ; "BetaServer tools are currently in beta" ; l.194 "max_results5 ... Capped at 50." | Nuance on numbers: l.135, for the `deferred_tools` protocol, says "max_results defaults to 5 and accepts 1 to 100"; l.194, for the tool's parameter, says "Capped at 50". The scout's "cap 50" holds for the tool parameter only. |
| X7 | CONFIRMED (absence limited to the two files) | litellm-anthropic-tool-search 17-20; litellm-mcp 201, 298, 936 | Table lists "Anthropic API", "Azure Anthropic (Microsoft Foundry)", "Google Cloud Vertex AI", "Amazon Bedrock" ; "LiteLLM will fetch and transform the MCP server's tools into OpenAI-compatible function calls" ; "make the server available to every LiteLLM API key, even if the key/team doesn't list the server in its MCP permissions" | "No dynamic discovery documented": grep of litellm-mcp for discover/dynamic/search matched only OAuth discovery and dynamic client registration (l.107, 418), not tool discovery. The search covered these two files only. Access control by key and team appears at l.201 and l.298. |

## Counts
CONFIRMED 7 (X6 and X7 with the notes above), PARTLY 0, NOT FOUND 0, CONTRADICTED 0.

## Claims that did not hold
None of X1-X7. Notes only: X6 cap of 50 applies to the tool parameter while the `deferred_tools` field accepts 1 to 100; X4 and X5 publication dates were not checked.
