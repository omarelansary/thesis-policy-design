#!/bin/bash
# P1 remaining runs (P1-PREP section 9): pop6 r1, none r2, pop6 r2 on none r1's 44 completed sessions; $2.96 each ($12 - $0.11 - $3.00 = $8.89).
cd /home/omar/Documents/thesis-policy-design
set -a; . ~/r3-work/.env; set +a
IDS=$(cat /home/omar/.claude/jobs/54b71024/tmp/p1_ids.txt)
PROG=design/package-v5/inputs/p1/local/p1-main.progress
for run in "pop6 1" "none 2" "pop6 2"; do
  set -- $run; tag=p1-main-glm-5.3-$1-r$2
  ~/r3-work/venv/bin/python design/package-v5/tools/p1_memory.py --tag $tag --arm $1 --model z-ai/glm-5.3 --price 0.70,0.13,2.2 --max-spend 2.96 --ids $IDS > design/package-v5/inputs/p1/local/$tag.console 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) $tag exit $rc: $(tail -1 design/package-v5/inputs/p1/local/runs/$tag/progress.log)" >> $PROG
done
echo "$(date -u +%FT%TZ) DONE2" >> $PROG
