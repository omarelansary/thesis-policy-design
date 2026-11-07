# P3: uninstructed search for a deferred tool (preparation, 2026-11-07)

Status: harness written and tested against a local mock server; **no request sent to any model yet**. Covered by the human's
INT-T-028 and INT-T-029 (P3 on OpenRouter, about 20 tasks built over AppWorld's real definitions, stop at $10 in total, models
proposed by the lead and confirmed by the human before any run); the P3 AUTH row is still to be entered in
`ops/AUTHORIZATIONS.md` with the operations-branch records (`ops/OPEN-TASKS.md`). Question and cells: `05` P3, HYP-0019.

## What is where
- Harness: `design/package-v5/tools/p3_uninstructed_search.py` (its docstring is the specification: cells, prompt variants,
  search and call tools, outcome classes, stops).
- **Local only, git-excluded** (`.git/info/exclude`): `design/package-v5/inputs/p3/local/` holds the task file, the request and
  session logs and OpenRouter's listings. AppWorld's data folder says public copies of it or its derivatives must be encrypted;
  the tasks name AppWorld tools and the logs hold tool names and search queries, so they stay on this laptop. What is committed
  per run is the `--analyze` summary: counts per cell and variant, outcome per task id, hashes of the harness, tasks and catalogue.

## Design in brief
- **Catalogue:** AppWorld 0.2.0 function-calling definitions, 9 apps, 463 tools (its documentation app is left out because it is a
  discovery route of its own; the supervisor app's five tools other than complete_task are the visible core). Catalogue hash
  (all files, as read) `232b91973726...`.
- **Tasks:** 20, one per target tool, two or three per app, each with a similar but wrong tool (for example the opposite action or
  the read-only twin), every required value given in the prompt. Written by the lead; gold by construction; not AppWorld's tasks.
- **Cells:** E expose-all (control, 468 tools, about 74K characters/4 of prefix), D deferred (core + search_tools + call_tool,
  about 500), A target absent, W distractor visible; D, A, W with and without a one-line index of app names that does not say how
  to reach them. 7 sessions per task, 140 per model, one user turn each, at most 6 requests.
- **No instruction to search** in the system text. search_tools and call_tool describe themselves in one line each.
- **Ranker check (no model):** with the whole task prompt as the query the target is in the top 3 for 17 of 20 tasks; with the
  tool-name words it is first or second for all 20. The target's rank is logged for every search, so a ranker miss is told apart
  from a model that did not search.
- **Mock test:** all cells, outcome classes, the spend counter and the stop after two failed requests behave as specified.
