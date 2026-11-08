#!/bin/sh
# AUTH-026: zai-org/GLM-5.3 on ScaDS (reasoning as served, free): smoke to completion, then B1, B2, B1 repeat, B2 repeat (57 dev tasks each).
# The first smoke (tag glm-smoke) was stopped by the lead's own 590 s time limit after 12 calls; it is not counted.
cd "$(dirname "$0")"
R="venv/bin/python run_partb.py --host scads --model zai-org/GLM-5.3 --max-spend 1"
$R --tag glm-smoke2 --predictor-mode predicted --max-predicted-apis 20 --ids 50e1ac9_1 || exit $?
$R --tag glm-b1-all-tools --predictor-mode all --max-predicted-apis 1000 || exit $?
$R --tag glm-b2-control --predictor-mode predicted --max-predicted-apis 20 || exit $?
$R --tag glm-b1-all-tools-repeat --predictor-mode all --max-predicted-apis 1000 || exit $?
$R --tag glm-b2-control-repeat --predictor-mode predicted --max-predicted-apis 20
