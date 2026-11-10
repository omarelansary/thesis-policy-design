#!/bin/bash
# P1 main runs (AUTH-033): none r1, pop6 r1, none r2, pop6 r2; each capped at $3 (4 x 3 = $12, AUTH-033's P1 limit).
cd /home/omar/Documents/thesis-policy-design
set -a; . ~/r3-work/.env; set +a
PROG=design/package-v5/inputs/p1/local/p1-main.progress
for rep in 1 2; do for arm in none pop6; do
  tag=p1-main-glm-5.3-$arm-r$rep
  ~/r3-work/venv/bin/python design/package-v5/tools/p1_memory.py --tag $tag --arm $arm --model z-ai/glm-5.3 --price 0.70,0.13,2.2 --max-spend 3 > design/package-v5/inputs/p1/local/$tag.console 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) $tag exit $rc: $(tail -1 design/package-v5/inputs/p1/local/runs/$tag/progress.log)" >> $PROG
  if [ $rc -ne 0 ]; then echo "STOP after $tag (exit $rc)" >> $PROG; exit $rc; fi
done; done
echo "$(date -u +%FT%TZ) DONE" >> $PROG
