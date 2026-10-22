# V5 audit package (AUTH-020, branch `v5-audit`)

**Status: provisional, complete as a conceptual package, 2026-10-22.** Nothing here is validated, approved, selected or final; no novelty is claimed; nothing was run except the lead's two arithmetic scripts. Plan: `ops/plans/v5-audit-plan-revised.md`.

## At a glance
- **Verdict on V4: substantially revised.** The criterion becomes the bill (DPR-0006); memory and sessions enter; the request-level system selector and the system trigger leave the default.
- **The bill decides the layout, accuracy decides the rest.** Deferral with a small core and search is cheaper than exposing every tool above a break-even size between about 10 and 230 tools (depending on searches per session, definition length, and whether the small core caches, which it often does not with short definitions); above a few hundred tools it is cheaper under every variant computed (`calc/regime_bill.py`). Above that size the open question is whether the model finds the tool.
- **Offering without breaking the cache exists.** Anthropic (beta, listed models) and OpenAI let a policy change what is offered per turn while the cached definitions stay put (`03` section 2), if the student's API passes them through (unknown).
- **Recommended draft V5-R = the rival's core plus a deployment filter and a gated memory-informed offering** (`04`, DPR-0007). The rival (DPR-0008, written independently by the proposer agent) is at least as good on present evidence; memory-informed offering is kept only because REQ-U21-04 requires the combination, and is switched on only where it is measured to pay.
- **Whether memory-informed offering pays is not settled by arithmetic.** The share of seeded tools a returning user must actually call for seeding to pay ranges from about a fifth to a half, and up to "never" in long sessions when a search returns a single match (`calc/memory_seed.py`, revision 3 after two review rounds); the proof-of-concept loop has to measure it. Personalized tool memory exists in research over small tool sets; per-user seeding from a large catalogue with the bill measured was not found in a limited search.
- **First things to measure** (`05`): the university API's cache fields and mechanisms (P0); where the break-even lies on that route (P5); whether models search unprompted (P3); how often returning users need the same tools (P1).
- **Decisions needed:** supervisor Q-J31..Q-J33; student Q-U28..Q-U32 (`design/ledger/notes/QUESTIONS-FOR-*-20261022.md`); ledger changes in `08` (not applied).
- **Not verified by anyone:** the human has spot-checked no V5 row; steward, scout, blind and challenger work is model work checked by model work.

## File map
| File | Content |
|---|---|
| `01-problem-and-evidence.md` | The problem from register H; the two blind designs compared; the decisive claims re-read |
| `02-contributions-assessed.md` | Supervisor requirements and how V5-R meets them; his assertions against evidence; the student's and the assistant's inputs kept, revised or dropped |
| `03-reuse-map.md` | Established components per policy slot, with sources, verdicts and what is left untested |
| `04-design.md` | Regimes, the V5-R graph, candidates compared, failure conditions, recommendations V5-R01..R09 |
| `05-poc-loop-and-e2e.md` | Proof-of-concept items in dependency order with a decision rule; end-to-end outline; questions |
| `06-contribution-and-traceability.md` | New versus reused; register of recommendations; `tools/trace_check.py` (0 misses: pointers and ids exist; wording checked by stewards and challengers, not by the script) |
| `07-independent-review.md` | 30 challenges and their dispositions; rebuttal check RV-0023 |
| `08-ledger-proposals.md` | Proposed ledger changes (not applied) |
| `calc/` | D-01 (regime bill) and D-02 (memory break-even), revision 2, with stdout |
| `inputs/` | Blind prompts and outputs, scout prompts, search log (scout section and the lead's targeted searches) |
Records: DPR-0007 (V5-R), DPR-0008 (simplest rival, proposer), DPR-0009 (blind alternative); HYP-0015..0021; FND-0040..0042; EXT-0227, EXT-0228; RV-0021, RV-0023; CH-0075..0104. Threads T-20261022-113..117.

## Provenance of inputs (SHA-256)
blind-output-A `f730ca31efc7054e4fcdcdbd44956fb5db5b61ac471237666768290ad7fad679`; blind-output-B `01e85a50841b0b2f72691289250a33a15d080de2dd6aebafb0c80bbc8f08e1aa`; blind-prompt `cd74a7b6e79ea3dabf2354a6d9b447b87b5c96e3a7d1b5b7b6869c258afa584e`; scout-prompts `c7853210b0db03eacd5b0658a3351b22f1223e745e2567d733250982617539ad`. The search log was edited after review (section 2 added); its hash is not fixed here.

## Change log
- 2026-10-22: first drafts; steward corrections applied to `03`; independent review and revision 2 of the calculations, `01`-`06`, DPR-0007; targeted searches; this README rewritten.
