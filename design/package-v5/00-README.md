# V5 audit package (AUTH-020, branch `v5-audit`)

**Status: provisional, complete as a conceptual package, 2026-10-22.** Nothing here is validated, approved, selected or final; no novelty is claimed; nothing was run except the lead's two arithmetic scripts. Plan: `ops/plans/v5-audit-plan-revised.md`.

## At a glance
- **Verdict on V4: substantially revised.** The criterion becomes the bill (DPR-0006); memory and sessions enter; the request-level system selector and the system trigger leave the default.
- **The bill decides the layout, accuracy decides the rest.** Deferral with a small core and search is cheaper than exposing every tool above a break-even size between about 10 and 230 tools (depending on searches per session, definition length, and whether the small core caches, which it often does not with short definitions); above a few hundred tools it is cheaper under every variant computed (`calc/regime_bill.py`). Above that size the open question is whether the model finds the tool.
- **Offering without breaking the cache exists.** Anthropic (beta, listed models) and OpenAI let a policy change what is offered per turn while the cached definitions stay put (`03` section 2), but the student's university API serves open-weight models only (P0 part 1, from its public status data), so V5 runs on the client-side route: a client ranker (the API has embedding and rerank models), appended definitions, and the bill computed from token counts with a named price table.
- **Working draft V5-R (DPR-0007, chosen by the student, REQ-U22-02) = the rival's core plus a deployment filter plus memory-informed offering for returning users** (`04`). The rival (DPR-0008, written independently by the proposer agent) is at least as good on present evidence; memory-informed offering is in the tested policy because REQ-U21-04 requires the combination and the answer for the supervisor (REQ-J22-01) asks for it to be tested properly with returning users (`05` P1).
- **Whether memory-informed offering pays is not settled by arithmetic.** The share of seeded tools a returning user must actually call for seeding to pay ranges from about a fifth to a half, and up to "never" in long sessions when a search returns a single match (`calc/memory_seed.py`, revision 3 after two review rounds); the proof-of-concept loop has to measure it. Personalized tool memory exists in research over small tool sets; per-user seeding from a large catalogue with the bill measured was not found in a limited search.
- **First things to measure** (`05`): the university API's cache fields and mechanisms (P0); where the break-even lies on that route (P5); whether models search unprompted (P3); how often returning users need the same tools (P1).
- **Decided so far (2026-10-22 to 25):** DPR-0007 is the working draft; memory is tested with returning users; Executor is a source of parts; the headline average is total bill over total turns with the mean of session rates beside it. **Done 2026-10-27:** the university API probe, first round (`10-p0-university-api-reading.md`): cache terms are reported, appends keep the cache, `allowed_tools` is rejected. **Second probe done 2026-10-27:** tool calling works on gpt-oss-120b, MiniMax-M3 and GLM-5.3; a changed tools array rewrote 65-99% of the prompt on GLM-5.3 (supports V5-R02) and left the cache almost intact on the other two (unexplained). **Third probe done 2026-10-27 by the human (`10` section 9):** a plain prefix cache on GLM-5.3 and MiniMax-M3 (the cost of a change is everything after it), unexplained on gpt-oss-120b; cache lifetime under 5 hours on two models and over 5.5 on one. **Still open:** a literature verification of `11` and the equations (AUTH-020 amendment of 2026-10-27, in progress); the choice of models (deferred by the human: the work must not depend on a model, N-38) and the handling of prices (`11`: token classes plus three ratios; the break-evens barely depend on them, N-39); the supervisor may confirm Q-J31..Q-J33 in his own words.
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
| `12-experiment-readiness.md` | Which loop items can start, which cannot, and a draft of what the experiments' authorization would need to say |
| `11-price-ranges.md` | Price ranges of hosted open-weight models from the providers' own pages (revision 2), the three ratios r, w, o that decide the bill's shape, reference cases, and how they affect the break-evens (D-04) |
| `15-landscape-memory-and-tool-loading.md` | Landscape of persistent memory, learning and tool loading in coding agents, products, open-source projects, memory services and research (AUTH-020 fourth amendment, INT-T-015): 7 scouts, 149 pages stored, 65 of 205 claims checked (45 confirmed, 19 partly, 1 contradicted); nothing in V5 changed, seven proposals for the human (PL-1 to PL-8, PL-4 withdrawn as a change); challenger RV-0026 applied; the human accepted the split of the proposals (REQ-U28-01): V5-R12 to V5-R16 in `04`, P1 extended in `05`, section 6.1 |
| `14-expose-ideas-verified.md` | The exposé-derived ideas (V5-R10, V5-R11, eviction, validation gate, enriched text, hybrid retrieval) against literature and open-source projects; 62 scout claims checked against about 58 stored pages, challenger RV-0025 applied |
| `13-literature-verification.md` | Multi-agent literature verification of `11`, the cost equation and the cache mechanics (stewards FND-0043..0045, challenger RV-0024); what is supported, corrected, or unverified |
| `10-p0-university-api-reading.md` | What the university API reports and honours, from the human's probe of six models (cache counters, appended turn, `allowed_tools`, rate limit) |
| `09-expose-ideas-checked.md` | The exposé's and the experiment brief's ideas, each kept, revised, parked or dropped against the stored evidence (Q-U32) |
| `07-independent-review.md` | 30 challenges and their dispositions; rebuttal check RV-0023 |
| `08-ledger-proposals.md` | Proposed ledger changes (not applied) |
| `calc/` | D-01 (regime bill), D-02 (memory break-even), D-03 (compact appended entries) and D-04 (price range), with stdout |
| `inputs/` | Blind prompts and outputs, scout prompts, search log (scout section and the lead's targeted searches) |
Records: DPR-0007 (V5-R), DPR-0008 (simplest rival, proposer), DPR-0009 (blind alternative); HYP-0015..0021; FND-0040..0042; EXT-0227, EXT-0228; RV-0021, RV-0023; CH-0075..0104. Threads T-20261022-113..117.

## Provenance of inputs (SHA-256)
blind-output-A `f730ca31efc7054e4fcdcdbd44956fb5db5b61ac471237666768290ad7fad679`; blind-output-B `01e85a50841b0b2f72691289250a33a15d080de2dd6aebafb0c80bbc8f08e1aa`; blind-prompt `cd74a7b6e79ea3dabf2354a6d9b447b87b5c96e3a7d1b5b7b6869c258afa584e`; scout-prompts `c7853210b0db03eacd5b0658a3351b22f1223e745e2567d733250982617539ad`. The search log was edited after review (section 2 added); its hash is not fixed here.

## Change log
- 2026-10-22: first drafts; steward corrections applied to `03`; independent review and revision 2 of the calculations, `01`-`06`, DPR-0007; targeted searches; this README rewritten.
