# V5 audit package (AUTH-020, branch `v5-audit`)

**Status: provisional, INCOMPLETE, checkpoint of 2026-10-22.** Nothing here is validated, approved, selected or final; no novelty is claimed. Plan: `ops/plans/v5-audit-plan-revised.md`.

## At a glance (draft)
- In bill terms, deferral with search beats expose-all from about 10-75 tools upward under the stored prices (`calc/regime_bill.py`); above that, accuracy is the open question.
- Anthropic (beta) and OpenAI let a policy change what is offered per turn without touching the cached definitions (`03` section 2); this lets the supervisor's stages act without cache breaks.
- Draft verdict: V4 substantially revised (`04` section 1). Recommended candidate V5-R: deployment filter, regime switch, memory-informed offering after a shared prefix, vendor discovery, masking, a Markdown memory file.
- Untested in our setting (to `05`): memory hit rate against the break-even of `calc/memory_seed.py`; offering accuracy at a fixed prefix; uninstructed recovery; university API cache fields.

## File map and state
| File | State |
|---|---|
| `inputs/blind-prompt-20261022.md`, `inputs/blind-output-A/B-20261022.md` | done (T-20261022-113) |
| `inputs/scout-prompts-20261022.md`, `inputs/search-log-20261022.md` | done (T-20261022-114; scout reports are not stored, only the pages they cited) |
| `calc/regime_bill.py`, `calc/memory_seed.py` and stdout | done (D-01, D-02) |
| `01-problem-and-evidence.md` | draft; C7 pointer to fix (see `03` section 11) |
| `03-reuse-map.md` | draft; steward corrections listed in section 11, **not yet applied** |
| `04-design.md` | draft; written before the steward corrections; check each against them |
| `02-contributions-assessed.md` | not started |
| `05-poc-loop-and-e2e.md`, `06-...`, `07-...`, `08-ledger-proposals.md` | not started |
| `design/proposals/DPR-0007/0008/0009`, `hypotheses/HYP-0015+` | not started |

## RESUME HERE (next session)
1. `python tools/verify_workspace.py --quick`; `git status`; confirm branch `v5-audit`.
2. Apply the corrections in `03` section 11 to `03`, `01` (C7) and `04` (check sentence-level claims that rest on them).
3. Write `02-contributions-assessed.md` (supervisor requirements: how V5-R meets each; assertions REQ-O21-04/05/06, REQ-O14F-03, REQ-O02-05 and AS rows against evidence; note that OpenAI individually deferred functions show name and description only, L/v5-openai-tool-search-20261022.md:22, a vendor form of the supervisor's partial-information tiers).
4. Spawn the design-proposer for DPR-0008 (simplest rival) with `01`, `03`, `04` section 2 and the requirements; write DPR-0007 (V5-R) and DPR-0009 (blind alternative); HYP-0015+ with falsifiers.
5. `05`, `06`; then T-20261022-117 (two challengers plus one rebuttal), `07`; then `08-ledger-proposals.md`, question sheets, STATE, WD-043, full verifier.
6. Pushes: the classifier refuses the lead's `git push`; the human pushes `v5-audit`.

## Provenance of inputs (SHA-256)
blind-output-A `f730ca31efc7054e4fcdcdbd44956fb5db5b61ac471237666768290ad7fad679`; blind-output-B `01e85a50841b0b2f72691289250a33a15d080de2dd6aebafb0c80bbc8f08e1aa`; blind-prompt `cd74a7b6e79ea3dabf2354a6d9b447b87b5c96e3a7d1b5b7b6869c258afa584e`; scout-prompts `c7853210b0db03eacd5b0658a3351b22f1223e745e2567d733250982617539ad`.
