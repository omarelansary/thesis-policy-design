#!/bin/sh
# runs/b1r-remaining-ids.txt holds the 45 dev ids not finished in b1r-all-tools-reasoning, from b119b1f_1 on (written by the lead from that run's stats.json)
# AUTH-025 stage 3, resumed after the OpenRouter key limit was raised (2026-11-06): the B1-with-reasoning tasks not finished in
# b1r-all-tools-reasoning (from b119b1f_1 on, which restarts from scratch), then B2 with reasoning on all 57 tasks.
cd "$(dirname "$0")"
venv/bin/python run_partb.py --tag b1r2-all-tools-reasoning-rest --predictor-mode all --max-predicted-apis 1000 --max-spend 3.93 --reasoning --ids $(cat runs/b1r-remaining-ids.txt) || exit $?
venv/bin/python run_partb.py --tag b2r-control-reasoning --predictor-mode predicted --max-predicted-apis 20 --max-spend 1.95 --reasoning
