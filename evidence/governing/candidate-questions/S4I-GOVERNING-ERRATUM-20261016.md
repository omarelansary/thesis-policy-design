# S4I governing erratum: authoritative wording qualifications after the S4H audit

- Date (UTC): 2026-10-16. Coordinator: Sonnet 5.5. Authority: D13 (user, 2026-10-16), accepting the S4H closure at checkpoint `7d024b2` as the governing evidence-audit outcome.
- Basis: `s4h-closure-20261016/S4H-CLOSURE-ADDENDUM.md` (findings F-1, F-2, F-4, F-5; sha256 `3cf6cf1d…c536b`), `audit-s4h-20261015/B2-REPORT.md`, `B1-source-version-report.md`.
- **Nature of this record.** It qualifies wording only. It does **not** reclassify C1-C6, does not change any novelty, feasibility or contribution conclusion, and introduces no new evidence. The original records are frozen and unchanged; where a wording below differs from an original, this erratum governs the *wording*, and the original remains the record of what was written and when. Reclassification would require new contradictory evidence.
- Originals referenced (git blob ids at `7d024b2`): S4G brief `6009e80e16b1`; S4F prior-art assessment `9e53735d1138`; S4D dossier `dbb503e8e001`; S4F uncertainty addendum `c3721326de8e`; STAGE4_FINAL_REPORT `6f0f9d54a8bd`; STAGE4_PRIOR_ART_COMPARISON `e4d19779b8a3`.

## Q-1 (S4H finding F-1): C5, cache-regime axis

| | |
|---|---|
| Original wording | S4F-PA L52: "What remains untested (I): … cache regimes for exposure policies that mutate the prefix; …". S4G L48 (and the C5 row of S4G §5.4): "Each axis has prior art in other domains (ETC, scaffold effect, token spend, on-device simulators); exposure-specific stability not found (3 queries)". S4F-PA L54: "each axis has partial prior art in other domains (coding agents, deep search, on-device agents)". |
| Authoritative wording | "Cache regimes for exposure policies that mutate the prefix are untested **beyond one single-step replay** (Toollery appendix B.2, Table 15: full library versus top-10 retrieval under natural, cache-suppressed and forced-warm regimes; one selector; the method's own authors) and are untested for multi-turn trajectories and for more than two policies." / "Each axis has prior art **mostly** in other domains (…); **the cache-regime axis also has one in-domain, single-step instance (Toollery B.2)**; exposure-specific stability across conventions, evaluators and horizon was not found (3 queries)." |
| Evidence | Toollery (`s4b-wd-toollery-20261013`) L736-752, L782-791: hit rate .989 (full library) versus .144 (retrieval) in the natural regime; input tokens −97.5%; billed-input-cost difference "inconclusive" (95% CI [−$0.000524, +$0.000462]); −97.5% billed input with caching suppressed. |
| Unchanged | C5 remains "partial prior art; exposure-specific stability not found". Its contribution, falsifier and feasibility statements stand. The S4F-PA expectation of a mixed outcome is supported, not weakened, by this instance. |

## Q-2 (S4H finding F-2): C3, near-miss list

| | |
|---|---|
| Original wording | S4G L46: "Head-to-head with token categories not found, but near-misses exist (App. N at 150 tasks, Skill Blocks for skills); increment may be a reporting increment"; S4G L72 nearest prior art; S4D L113: "… near misses are listed"; S4F-UA L12. |
| Authoritative wording | Add two near-misses to the C3 list: (i) **Toollery** (Tables 4 and 15): two classes (static full library, retrieval-restricted) with accuracy, input tokens, latency, billed input cost and cache hit rate; single-step; run by the method's authors; in Table 4 the full-library rows use a different selector (DeepSeek V3.2) from the top-10 rows (DeepSeek-V4-Pro). (ii) **CE-MCP study** (arXiv 2602.15945, `r2-ce-mcp-2602-15945-20261011`): traditional versus code-execution MCP agents on MCP-Bench, 10 servers (1-3 per task), 34 tasks, three GPT models, input/output tokens, turns and time, LLM-judged fulfilment, no repeats or intervals stated; results in figures only (magnitudes not recoverable from the stored text). |
| Unchanged | The gap statement ("independent, controlled head-to-head of at least two classes on one tool-catalogue workload with success, token categories and repeats; not found") stands. "Increment may be a reporting increment" is reinforced. No change to C3's contribution or its client-side scoping. |

## Q-3 (S4H finding F-4): C6 source count

| | |
|---|---|
| Original wording | S4G L49 and S4F-PA L68: "Component ablation exists in three uneven sources (one measured, compound step, F1; one unclear; one projected)". |
| Authoritative wording | "Component ablation of exposure-related steps appears in **at least three** uneven sources (the three named); further stored sources vary a token-saving component outside staged exposure (Notation Matters: content-format compression with accuracy cost; the tool-schema compression study: budget-dependent effect). The count is a selection, not a census." |
| Unchanged | "A controlled, deterministic, held-out ablation of staged exposure was not found" stands. "Mechanism novelty is low by construction" (S4G L81) stands. |

## Q-4 (S4H finding F-5): Dynamic ReAct, unsupported efficiency claim

| | |
|---|---|
| Standing note | The abstract's "reduces tool loading by up to 50% while maintaining task completion accuracy" (`s4-dynreact-2509-20386-20261013` L21-22) and the conclusion's "improvements in both efficiency and accuracy compared to static tool loading approaches" (L602) are **not supported by the paper's own text**: the only quantitative evidence is retrieval Top-5/Top-10 on a proprietary registry, and the "50%" is a relative Top-5 gain (40% → 60%, L498). Its stated architecture pros and cons (e.g. "Caching Efficiency", "Performance Degradation", L355, L360) are unmeasured assertions. These claims must not be cited as evidence. |
| Consistency with the record | STAGE4_PRIOR_ART_COMPARISON L21 already states this ("Abstract claims not supported by body measurements"). STAGE4_FINAL_REPORT L17 groups Dynamic ReAct with methods "evaluated on retrieval or LLM-judged selection and completion metrics"; for this source that wording overstates (retrieval accuracy only). |
| Unchanged | No C1-C6 statement relies on these claims. Dynamic ReAct remains contextual for C3 and C6 (mechanism and class description). |

## Items from the S4H closure that need no wording change

F-3 (client-side code-mode token accounting is not an obstacle in the CE-MCP study; the open accounting problem is provider-native programmatic calling) and F-6 (Prompt-Induced Waste as other-domain harness-dependence evidence) require no qualification of the governing records and are left to the addendum.

## Governing reading order for selection purposes

1. S4G selection-ready brief v2 (`stage-reports/S4G-SELECTION-READY-BRIEF-20261015.md`) **with this erratum**.
2. S4F prior-art assessment v2, uncertainty addendum v2, vehicle report v2; S4E report; S4D dossier v2, matrix v2, quality addendum.
3. Integrity-investigation errata and S4H audit/closure documents for provenance only.

## Closure of audit tickets for selection purposes

The following are closed for selection purposes; no further audit, review, search, experiment or candidate-generation round is open: COORD-S4H-AUDIT-20261015-01 (complete), COORD-S4H-CLOSURE-20261016-01 (complete), the integrity investigation (`integrity-investigation-20261015/`, final report `FINAL-REPORT-20261015.md`; its B-1/B-2 follow-ups are the two S4H units), and D1/D11/D12 limits as recorded. Reopening requires new contradictory evidence and a new decision record.
