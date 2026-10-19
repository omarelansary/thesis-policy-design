# Steward 2b log (lead, from the hand-back)
- Findings: findings/SUM-0015-batch2b-dmb-executor-rest.md (FND-0013). Extractions: EXT-0157, 0160, 0162, 0165, 0167, 0168, 0170, 0172. No messages sent.
- Verdicts: C-E01/E03 NOT STATED for the 292K counting method (57.3 to 36.7 is a pass-rate drop; e9.1 qwen cells 54.0/30.7 differ, unexplained); C-R03/STUB ANSWERED for the code read (distractors outside the reference get input_schema {"type":"object"}; ToolEntry has no schema field); AS-07 / C-D08/EXEC NOT STATED (no prefix, details or results tool; CLI/SDK commands only).
- Lead re-check: EXT-0162, 0167 confirmed.
- Not read: e9.1 lines 136-801; pools.py 1-30; sampling.py 1-40 and 313-357; Executor README lines 1-60 and 115-135 were read in batch 1.
