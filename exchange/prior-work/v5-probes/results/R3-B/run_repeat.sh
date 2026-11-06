#!/bin/sh
# AUTH-027: repeat of the AUTH-025 stage 3 runs (MiniMax-M3 on OpenRouter, gmicloud/fp8, reasoning on), B1 then B2, 57 dev tasks each.
cd "$(dirname "$0")"
venv/bin/python run_partb.py --tag mm3-b1r-repeat --predictor-mode all --max-predicted-apis 1000 --max-spend 4.95 --reasoning || exit $?
venv/bin/python run_partb.py --tag mm3-b2r-repeat --predictor-mode predicted --max-predicted-apis 20 --max-spend 1.95 --reasoning
