#!/bin/bash
cd /home/omar/Documents/thesis-policy-design
set -a; . ~/r3-work/.env; set +a
IDS=$(cat /home/omar/.claude/jobs/54b71024/tmp/p1_ids35.txt)
PROG=design/package-v5/inputs/p1/local/p1-main.progress
for arm in none pop6; do
  tag=p1-main-glm-5.3-$arm-r2
  ~/r3-work/venv/bin/python design/package-v5/tools/p1_memory.py --tag $tag --arm $arm --model z-ai/glm-5.3 --price 0.70,0.13,2.2 --max-spend 2.93 --ids $IDS > design/package-v5/inputs/p1/local/$tag.console 2>&1
  echo "$(date -u +%FT%TZ) $tag exit $?: $(tail -1 design/package-v5/inputs/p1/local/runs/$tag/progress.log)" >> $PROG
done
echo "$(date -u +%FT%TZ) DONE3" >> $PROG
