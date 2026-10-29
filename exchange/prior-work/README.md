# Instructions for the describing agent

You describe earlier experiments that you can read. A second agent, the reader, will decide whether any of them fits its own work. You do not know that work, and you should not try to guess it.

## Rules
1. **Describe; do not conclude.** Say what was done, with what, and what it produced. Do not report result values, effect sizes, or verdicts ("worked", "showed", "better"), and do not say whether the reader needs to repeat anything.
2. **Be complete about scope.** Differences in setup matter more than similarities. When something is unknown, write "not recorded". When something was only partly done, say which part.
3. **Point to where you read it.** Each field carries the path (and lines, if useful) in the earlier work where the statement comes from.
4. **Stay inside `exchange/prior-work/`.** Read your own source location and this folder; write only to this folder. Do not open any other file or folder of `thesis-policy-design`, even if you are able to.
5. **Use the models' live status.** Before describing, check which models the providers serve now (for the university API: https://llm.scads.ai/status/ and https://llm.scads.ai/status/state.json). Where an earlier test ran on a model set that has since changed (for example only GLM, because MiniMax was not yet available, or on a model since retired), rerun that test on the models served now, with the same setup, and add the rerun to its description: models, dates, status and output files. Report a rerun like any other run: no result values or verdicts.
6. **Answer questions in `THREAD.md`.** The reader will ask about scope and materials there. Answer what was asked. If you think an experiment is already done for the reader's purpose, you may say so once, with pointers. The human decides any disagreement.

## How you work
Organise the work as you see fit: you choose the order, what to read, what to rerun, and you may use several agents. The rules above are the only constraints.

## One file per experiment: `PWD-001.md`, `PWD-002.md`, ...
```
# PWD-NNN <short name>
- Status: done / partly done (which part) / planned only
- Dates: when it ran (or "not recorded")
- Reruns: none / rerun on which current models, when, with which output files (rule 5)
- Purpose: the question it was meant to answer, in the words of the earlier work if possible
- Input
  - Tasks: source, number, kind; whether each task has gold or reference tool labels
  - Tools: number of tools, where the definitions came from, average definition size if recorded
  - Models: names and versions; provider or server
  - Offering: how tools were offered to the model (all at once, a fixed subset, retrieved per turn, searched by the model, other)
  - Memory: none / what was stored, when it was written, how it was read
  - Sessions: single turn, multi-turn, several sessions of the same user, gaps between sessions
- Arms: each condition compared, one line each
- Measures: what was recorded (metric names and units; whether token counts were taken from the provider's usage records; whether cached tokens were recorded)
- Sample: tasks per arm, runs, repeats, seeds
- Output: which files, logs or tables exist and where (names only, no values)
- Materials that could be reused: task sets, tool catalogues, user histories, harness or logging code, graders (path and format)
- Not done or not recorded: what was planned but not run, and gaps in the records
- Pointers: paths (and lines) for each field above
```
