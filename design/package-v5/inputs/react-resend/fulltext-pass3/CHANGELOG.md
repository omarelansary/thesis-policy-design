# Third pass (full-text verification) and its adversarial review: what changed and why (2026-11-09)

Retracted after the review (verified by me against the sources):
- "Incomplete subsets raise the bill" (2610.41905's 15.1M vs 7.4M prompt tokens compare the retriever's 16-API exposure with gold-only exposure over all 60 tasks). Stored records show opposite signs by model: MiniMax-M3 incomplete sets 14.8 turns / 504k prompt tokens vs 8.4 / 105k (observational); GLM-5.3 tasks missing the credentials function 192k vs 741k (agent gave up).
- "Published results fit the M/c break-even": cumulative break-even is ~M(2-c)/c (173 turns at M=10, c=0.1; 84 at c=0.2; 26 at a 55% hit rate); Complexity Trap's halving at 44-50 turns is NOT reproduced.
- "Real sessions are 8x longer": TraceLab's 84 steps are per session; ~8 steps per user request, comparable to an AppWorld task.

Softened/corrected: tool-definition share 58-68% (derived); power numbers as ranges (+-5.5 to +-8 at 2 runs, 65-135 scenarios for a 3-point margin); AppWorld paper oracle gains reported for all agent types; TheMCPCompany steps (Opus +5%); Exgentic dollar deltas added; "estimation-only is forced by sample size".

New from stored data (no new runs): all-tools/subset bill ratio vs cache-read ratio r (MiniMax token totals held fixed): 1.16 (r=.025), 1.36 (.05), 1.70 (.1), 2.19 (.2), 2.97 (.5), 3.49 (1.0).

Files: FULLTEXT_VERIFICATION_LEDGER.tsv (per paper), reports/ (four readers), review/ (adversarial review + its scripts), code/ (download script, power simulation).
Full texts were downloaded to a temporary job folder (untrusted data, not kept); URLs are arXiv ids in the ledger.

## Final checks (same day, after the review)
- Step-capped runs dominate some bills: share of arm bill MiniMax all 0%, MiniMax subset 18%, GLM all 25%, GLM subset 75% (88% of prompt tokens). Ratio of mean per-task bills all/subset: MiniMax 2.19 -> 2.59, GLM 1.51 -> 4.11 with capped runs removed (the mean of paired per-task ratios is 3.4 and 10.3: state which ratio is meant).
- Cold-start counterfactual: all-tools bills +22.7% (MiniMax), +21.2% (GLM); subset arms +0.1-0.2%.
- Typical-task anatomy of the subset arms (capped removed): output 39% (MiniMax) / 50% (GLM) is the largest item; history 40% / 22%; predictor 5% / 13%. The earlier "history becomes the bottleneck" reading was a runaway-run effect for GLM.
- Incomplete-set effect: DeepSeek none; MiniMax none at the typical task (mean inflated by three step-capped runs, all incomplete-set); GLM lower (agent gave up).
- Blind replication of all of the above reproduced (final-checks/blind_replication.md). final_checks.py reproduces items 1-2.
