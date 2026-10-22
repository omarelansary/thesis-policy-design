# 06. Contribution and traceability (V5, AUTH-020)

Status: provisional, lead, 2026-10-22. Machine check: `python design/package-v5/tools/trace_check.py` (every literature pointer resolves to a stored file and existing lines; every record id exists; every V5-Rnn and D-nn of `04` is listed here).

## 1. New, reused, needs validation
| Part of V5-R | Status | Where searched for prior work |
|---|---|---|
| Cached prefix, invalidation rules, prices | Reused (vendor mechanism) | `03` section 1 |
| Offering at a fixed prefix | Reused mechanism (Anthropic beta, OpenAI); effect in our setting needs validation (HYP-0018) | `03` section 2 |
| Deferral and search, append-only | Reused (vendor mechanism); uninstructed use needs validation (HYP-0019) | `03` section 3 |
| Usage-based core, groups, routing | Reused (Copilot's shipped design, EXT-0228) | `03` section 4 |
| Deployment filter (S1) | Reused mechanism (static allow-lists) | `03` section 4 |
| Regime switch (S2) by D-01 | **New as a rule** (derived arithmetic over vendor prices and minimums); needs a reading (P5) | scout groups 1-2; blind A and B |
| Memory-informed offering after the shared prefix (M2-M3) | **New**; needs validation (HYP-0017) | scout group 3; blind A and B; V4 `04` section 4; steward C |
| Markdown memory file (M1, W) | Reused (the supervisor's prescription; Anthropic memory tool as carrier) | `03` section 5 |
| Observation masking (H) | Reused result (one study); transfer needs validation (HYP-0021) | `03` section 6 |
| Bill criterion | Reused (DPR-0006) | — |

## 2. Thesis sufficiency against the recorded criteria only
- A negative or not very novel result is still a thesis; a paper needs a systematic study (REQ-O14F-02): V5's admissible outcomes include dropping every new part.
- The novelty is combining approaches and showing what works and what does not (REQ-O14F-03): the new parts are the combination (M2-M3 with S2); each is falsifiable in `05`.
- Success is the quality of the work, nothing missed (REQ-U21-11): the reuse map lists every slot with its sources and its limits; gaps are stated as NONE FOUND with the places searched.

## 3. Register of recommendations and derivations
| Id | Pointer |
|---|---|
| V5-R01 | DPR-0006; `04` section 6 |
| V5-R02 | L/v5-anthropic-tool-use-caching-20261022.md:57-63; L/v5-anthropic-midconv-sysmsg-20261022.md:27; L/v5-openai-prompt-caching-20261022.md:440-441; L/v5-ccissue-92033-cachebust-20261022.txt:180-190 |
| V5-R03 | D-01; FND-0037 (minimum length, EXT-0150) |
| V5-R04 | L/v5-anthropic-tool-use-caching-20261022.md:49; L/v5-openai-tool-search-20261022.md:5 |
| V5-R05 | REQ-O21-09; L/v5-anthropic-memory-tool-20261022.md:29 |
| V5-R06 | L/v5-anthropic-midconv-sysmsg-20261022.md:27, :452; L/v5-openai-prompt-caching-20261022.md:441; HYP-0017 |
| V5-R07 | EXT-0228 (a group expansion costs a cache miss and a round trip); `03` section 4 (multi-step narrowing NONE FOUND) |
| V5-R08 | L/v5-complexitytrap-2508.21433.txt:23-25; L/v5-anthropic-context-editing-20261022.md:71; HYP-0021 |
| V5-R09 | `05` section 1 |
| D-01 | `calc/regime_bill.py`, `calc/regime_bill.stdout.txt` |
| D-02 | `calc/memory_seed.py`, `calc/memory_seed.stdout.txt` |
