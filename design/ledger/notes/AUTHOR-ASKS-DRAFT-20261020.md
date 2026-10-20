# Drafted questions to authors and vendors (for the human to send; nothing has been sent, and the lead has no way to send them)

Written 2026-10-20 by the lead for ledger rows C-S19/S40, S41, S42, S43, C-E03/O7-27, C-E01/E02 and C-S05. Each ask is short and neutral, names the exact place in the source, and states what we already read, so the reply can be one sentence. Where the human sends one, the date and the reply go into the ledger row (Questions or Status basis). A reply, not our reading, closes these rows; until then they stay as external items and nothing else waits on them.

## 1. MCPVerse authors (arXiv 2508.16260; versions v1 and v2; GitHub issues or the corresponding author)
Rows: C-S19/S40, S41, S42, S43.
Message: "We are reading MCPVerse v2 for a thesis and found five places where we could not tell what the paper intends. Could you tell us which is right? (1) Table 4 gives Claude-4-Sonnet Oracle 44.8 and Standard 53.2, the same as Qwen3-235B-2507, while Tables 2 and 3 give Claude 62.3 / 62.4 (62.28 / 62.36). Which values are Claude's? (2) In Table 2 the Gemini-2.5-Pro Max-Scale cells (31.4*, 37.7*, 35.7*, 20.8*) equal the GPT-4o-20241120 Standard cells; is that intended? (3) Section 4.1 says Max-Scale can only be run by Claude-4-Sonnet and Gemini-2.5-Pro, but Table 2 gives Qwen3-235B-2507 a Max-Scale score (31.6). (4) Claude-4-Sonnet Max-Scale is 57.77 in v1 and 44.2 in v2, Oracle 57.81 vs 62.3; what changed between the versions (judge, tasks, models, prompts)? (5) Which judge produced Table 4, and how many tasks are there at each level (Figure 2's percentages do not give whole numbers for 250 tasks)? Thank you."

## 2. Authors of the validity audit (arXiv 2607.02577)
Row: C-E03/O7-27.
Message: "In your audit of evaluator-human agreement, how were the 496 audited items chosen (every task, or only flagged instances: Section 3.3 says 'flagged', Section 4.1 says 'each task')? BFCL v4 is '200 audited tasks' in one sentence and a '50-task multi-turn base export' in the next; which is right? Are the 496 'tasks' (abstract) or 'executions' (contributions)? Will the trace artifacts be released, and when? Thank you."

## 3. Anthropic (engineering blog 'advanced tool use'; the documentation feedback channel or a developer-relations contact)
Row: C-S05.
Message: "The advanced-tool-use post reports Opus 4 improving from 49% to 74% (and Opus 4.5 from 79.5% to 88.1%) with tool search. Is there a public description of the task set, its size, the number of runs and an interval, and of how many tools were exposed in each arm? We could not find one and would like to cite the figure with its limits."

## 4. Authors of Toollery (arXiv 2609.22218)
Row: C-E01/E02.
Message: "Your replay library, the selectors compared and the pricing protocol are not stated in the text we have. Is there a repository or an appendix that gives (a) the replay library, (b) whether the selectors are comparable (same inputs), (c) the pricing protocol behind the fitted multiplier?"

## Not drafted
- C-E02/E25 (Claude Code issue 59650): a user report; no ask would add to it.
- Scaffolding paper (median failed vs completed run) and ToolRet (Figure 6 vs Table 14 oracle values): internal inconsistencies of the papers, noted in the ledger; they matter only if those numbers are quoted.
