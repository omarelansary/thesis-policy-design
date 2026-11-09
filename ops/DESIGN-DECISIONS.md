
## WD-084 P2b done on OpenRouter (2026-11-09)
- **The human:** keep the full design (INT-T-046); effort as served and both repeats (INT-T-048); ScaDS with a longer timeout (INT-T-049); then OpenRouter GMICloud fp8, diff first, no cap, cost watched (INT-T-050, INT-T-051).
- **Changes (the lead, approved as diffs):** `p2_offering.py --timeout` (c657ac3) and `--provider` (ad0383d). **Before:** a fixed 300 s timeout and no provider pin. **Why:** ScaDS stalls; then ScaDS's own 900 s cut (HTTP 408) made the timeout useless, so the route moved.
- **Result (`design/package-v5/inputs/p2/RESULTS-P2B.md`):** $5.781, 855 calls, 0 failed; `instr` against `all` +0.067 (−0.033 to +0.217), 0 calls outside the subset in 60 task-runs, calls x0.93, cost x0.80, noise 1 of 30. HYP-0018 gains it, status stays `proposed` (INT-T-044).
- **Not the university route:** GMICloud fp8 at effort "as served" (behaves like high) against ScaDS's W4A8 at max. The three ScaDS attempts are kept, not pooled, not scored.
- **Added:** `tools/p2_paired.py` (reproduces main-paired-summary.json exactly), `tools/p2b_effort_probe.py`.
- **Proposed, not made:** `04`'s P2 note still ends "P2b checks it on the university API"; the lead's proposed replacement is in the commit message of this entry, for the human.
