#!/bin/sh
# AUTH-025 stage 3: B1 and B2 again with reasoning on (gmicloud/fp8); stop each run at 1.5x its estimate
cd "$(dirname "$0")"
venv/bin/python run_partb.py --tag b1r-all-tools-reasoning --predictor-mode all --max-predicted-apis 1000 --max-spend 4.95 --reasoning || exit $?
venv/bin/python run_partb.py --tag b2r-control-reasoning --predictor-mode predicted --max-predicted-apis 20 --max-spend 1.95 --reasoning
