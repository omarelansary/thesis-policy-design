#!/bin/sh
# AUTH-026, resumed after the laptop restart (2026-11-07): GLM-5.3 B2 (control) on ScaDS, the dev tasks not finished in
# glm-b2-control (runs/glm-b2-remaining-ids.txt, written from that run's stats.json; the interrupted task restarts from scratch).
cd "$(dirname "$0")"
venv/bin/python run_partb.py --host scads --model zai-org/GLM-5.3 --max-spend 1 --tag glm-b2-control-rest --predictor-mode predicted --max-predicted-apis 20 --ids $(cat runs/glm-b2-remaining-ids.txt)
