# Run scripts of P1, P2b and P4 (AUTH-033, AUTH-034; copied 2026-11-10)

These are the shell scripts the lead used to chain and watch runs, copied **verbatim** from the lead's scratch folder
(`/home/omar/.claude/jobs/54b71024/tmp/`). They contain no key material: each loads the keys from `~/r3-work/.env` into the
environment. They still point at that scratch folder for the task-id lists (copies in `ids/`) and at each other's state files,
so to rerun, copy `ids/*.txt` back or edit the paths. Everything runs from the repository root.

The harnesses themselves are in `design/package-v5/tools/` (each header has its usage). A run's exact settings are in its
`run-meta.json` (model, provider, seed, temperature, timeout, price, cap, tasks, SHA-256 of the harness version); raw logs are
local and git-excluded (`design/package-v5/inputs/<experiment>/local/`), counts are in the committed `*-analysis.json`.

## Python and environment
- AppWorld-based harnesses (`p1_memory.py`, `p2_offering.py`, `p2_main_driver.py`, `aw_eval_per_task.py`, `p4_replay.py`):
  `~/r3-work/venv/bin/python` (AppWorld 0.2.0, data in `~/r3-work/aw-root/data`).
- Analysis scripts and the P3 harnesses: `python3` (standard library; `p4_replay.py` needs `tiktoken`, in the venv).
- Keys: `set -a; . ~/r3-work/.env; set +a` (never printed). Model prices as passed with `--price` (input, cached input, output,
  dollars per million tokens).

## What was run, in order (settings from the runs' `run-meta.json`)
| Run | Command shape | Settings |
|---|---|---|
| P2 main, gpt-5-mini | `p2_main_driver.py --model gpt-5-mini --price 0.25,0.025,2.0 --cap 6` | OpenAI Responses API, effort low, temperature 1.0; arms all, enf, instr, drop; 2 repeats; tag prefix `p2-main` |
| P2 main, gpt-5.4-mini | `p2_main_driver.py --model gpt-5.4-mini --price 0.75,0.075,4.5 --cap 11` | same |
| P2b attempts 1 to 3 (ScaDS, stopped by timeouts) | `p2_main_driver.py --model zai-org/GLM-5.3 --price 0,0,0 --cap 1 --arms all,instr --repeats 2 --api chat_completions --tag-prefix p2b[2,3] --extra "--base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --no-reasoning-param --seed 100 --temperature 0 --min-interval 31 --retry-429 6 [--timeout 1200]"` | not scored |
| P2b on OpenRouter | `p2_main_driver.py --model z-ai/glm-5.3 --price 0.70,0.13,2.2 --cap 9999 --arms all,instr --repeats 2 --api chat_completions --tag-prefix p2b-or --extra "--base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --provider GMICloud --no-reasoning-param --seed 100 --temperature 0 --timeout 600"` | watched by `p2bor_watch.sh` |
| P1 smoke | `p1_memory.py --tag p1-smoke-none --arm none --model z-ai/glm-5.3 --price 0.70,0.13,2.2 --max-spend 1 --limit 3` | 3 sessions |
| P1 main, step 1 | `p1_driver.sh` (none r1, then pop6 r1, none r2, pop6 r2, each `--max-spend 3`; it stopped after none r1 at its cap) | watched by `p1_watch.sh` |
| P1 main, step 2 | `p1_driver2.sh` (pop6 r1, none r2, pop6 r2 on the 44 sessions of none r1, `--max-spend 2.96`); stopped by the lead after pop6 r1 and 6 calls of none r2 | `ids/p1_ids.txt`, `p1_watch2.sh` |
| P1 main, step 3 | `p1_driver3.sh` (none r2 and pop6 r2 on the 35 sessions pop6 r1 completed, `--max-spend 2.93`) | `ids/p1_ids35.txt`, `p1_watch3.sh` |
| P4 smoke | `p2_offering.py --tag p4-smoke-mask-glm-5.3 --arm all --api chat_completions --model z-ai/glm-5.3 --base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --provider GMICloud --no-reasoning-param --seed 100 --temperature 0 --timeout 600 --price 0.70,0.13,2.2 --max-spend 0.6 --mask 30000,3,5000 --ids <2 longest tasks>` | 2 tasks |
| P4 main | `p4_driver.sh` (mask r1 `--max-spend 2.5`; stopped at its cap after 20 tasks), then mask r2 by hand on `ids/p4_ids.txt` with `--max-spend 3.6` | |
| Scoring | `aw_eval_per_task.py RUN_DIR "ID ID ..."` for every run that a cap stopped | one session at a time |

The P3 harnesses (`p3_uninstructed_search.py`, `p3_two_need.py`) were run from the repository root with `python3`, keys in the
environment, their task files and catalogue under `inputs/p3/local/`; their runs and costs are in `inputs/p3/P3-LOG.md`.
