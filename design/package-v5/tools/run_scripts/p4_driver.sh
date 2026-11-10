#!/bin/bash
# P4 step B (AUTH-033): masking arm on P2b's 30 tasks, 2 repeats; P2b's two 'all' runs are the keep-everything arm.
cd /home/omar/Documents/thesis-policy-design
set -a; . ~/r3-work/.env; set +a
PROG=design/package-v5/inputs/p4/local/p4-main.progress; mkdir -p design/package-v5/inputs/p4/local
for rep in 1 2; do
  tag=p4-mask-glm-5.3-r$rep
  ~/r3-work/venv/bin/python design/package-v5/tools/p2_offering.py --tag $tag --arm all --api chat_completions --model z-ai/glm-5.3 --base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --provider GMICloud --no-reasoning-param --seed 100 --temperature 0 --timeout 600 --price 0.70,0.13,2.2 --max-spend 2.5 --mask 30000,3,5000 > design/package-v5/inputs/p4/local/$tag.console 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) $tag exit $rc: $(tail -1 design/package-v5/inputs/p2/local/runs/$tag/progress.log)" >> $PROG
  if [ $rc -ne 0 ]; then echo "STOP after $tag (exit $rc)" >> $PROG; exit $rc; fi
done
echo "$(date -u +%FT%TZ) DONE" >> $PROG
