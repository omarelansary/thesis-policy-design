#!/bin/bash
# R3 Part B, AUTH-024: B1 -> B2 -> B3, sequential; stops at the first non-zero exit (spend cap = 1.5 x approved estimate)
cd "$(dirname "$0")" || exit 1
venv/bin/python run_partb.py --tag b1-all-tools --predictor-mode all --max-predicted-apis 1000 --max-spend 7.0 || exit $?
venv/bin/python run_partb.py --tag b2-control --predictor-mode predicted --max-predicted-apis 20 --max-spend 1.5 || exit $?
venv/bin/python run_partb.py --tag b3-control-repeat --predictor-mode predicted --max-predicted-apis 20 --max-spend 1.5 || exit $?
