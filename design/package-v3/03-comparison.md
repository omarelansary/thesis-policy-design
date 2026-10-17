# 03. Short comparison: graph G against C-A, expose-all and vendor deferral

Status: provisional, lead's assessment [I]. Everything about effectiveness is a hypothesis. Criterion for this comparison is the working objective of AUTH-006: cumulative model-visible input tokens over complete trajectories, subject to end-to-end success not below the reference by `delta` (undecided). Tool count, token categories, billed cost and cache behaviour are recorded separately and are not in the criterion.

## 1. Should C-A be the principal proposal? No: a component and a comparator
1. **Applicability.** Rule A1 needs need statistics from a feasible reference. For the original large-catalogue problem (catalogue beyond context) it cannot run; the core stage is skipped there (errata, correction 4).
2. **The distinctive content is a heuristic ordering with no optimality or safety property** (errata, corrections 2-3); the surface is finally chosen by an end-to-end sweep, which any candidate can use.
3. **Its structure is a known pattern.** Static core plus search plus append is vendor deferral with a computed core. Under the token criterion the cache terms that made it distinctive in v2 leave the criterion; what remains is "core ranked by incremental token saving per unit of miss mass, cut by sweep".
4. **What survives of C-A:** the core stage S1 of G (eligible only with need statistics), the explicit runtime-information discipline, the sweep arms (equal-size frequency core, swept frequency core) that keep a rule honest, and the A0-style measurement habit. C-A remains an arm and a comparator inside G.

## 2. Should C-B be the principal proposal? Not adopted; its parts are conditional stages
C-B (system-run query-conditioned selector plus a system trigger, never asking the model) is the closest to the supervisor's staged, context-dependent, re-adding picture. The evidence does not justify selecting it: retrieval-based narrowing lowered success in several settings; an unreached tool is almost a certain failure in the benchmark that measured it (one model, intervals about ±8); a two-stage router matched single-stage retrieval in success with no token data; **no stored source supports a system-side trigger** (the only trigger-like result, enforced extra exploration, is oracle-triggered, from a planning benchmark, and gave under five points). G keeps its parts as stages R2 (per-request narrowing), R2 level 2, and R6 (trigger), each **present only if D4 selects it**.

## 3. Comparison table
| | **G** (this proposal) | **C-A** | **Expose-all** | **Vendor deferral** |
|---|---|---|---|---|
| What it is | design-time rule D4 selects a run-time configuration among arms; stages optional | one surface from a break-even rule; search; add-only | the whole catalogue visible every turn | a hand-picked few tools visible plus a search tool; discovered tools appended |
| Who decides what is visible | operator by pre-registered dev rule (design time); system selector (if selected); the model (via requests) | operator rule (offline); the model (via search) | nobody | operator hand-pick; the model (via search) |
| Context-sensitivity (supervisor) | request-level (R2, if selected) and trajectory-level (R4-R6) | trajectory-level only (model search) | none | trajectory-level only |
| Staged narrowing | core -> per-request narrowing -> in-run discovery, each optional | core -> in-run discovery | none | core -> in-run discovery |
| Reintroduction | model-emitted request by default; trigger optional | model-emitted request | not needed | model-emitted request |
| Applicable at large catalogue (reference cannot run) | **yes**, with the core stage skipped and claims relative to a named substitute | **no** as specified (core rule needs need statistics) | no (does not fit) | yes (core hand-picked, no estimator) |
| Tokens (primary criterion) | tool block reduced to what D4 selects, plus selector/search/recovery overhead | core plus discovered tools plus search overhead | whole tool block every turn | hand core plus discovered tools plus search overhead |
| Success risk | selector recall (R2); non-initiation (R4); interference from appended results | non-initiation; interference; core miss | distraction (mixed evidence); none from reachability | non-initiation; interference; core miss |
| Evidence status | hypothesis; rule makes its choice testable | hypothesis | the reference where it fits; accuracy effect of many tools mixed (several settings lower; strong models largely mitigate) | vendor-shipped; unmeasured by the record; vendor guidance on mixing eager and deferred differs in scope |
| Billed cost and cache | recorded; not in the criterion; depends on an unknown provider multiplier | recorded; v2 rule used billed terms | recorded; a warm cache cuts billed cost per token on some providers but **not** tokens | recorded |
| What would make it lose | a simpler arm is feasible and cheaper at every size | a swept or hand-picked core ties it; the large-catalogue regime | a restricted arm is feasible and cheaper; the catalogue exceeds context | an equal-size or swept frequency core beats the hand-pick (or ties) |

## 4. What this comparison does not show
Which arm is best: the record does not discriminate. G's content over vendor deferral is the explicit D4 decision, the optional per-request narrowing and trigger stages as testable arms, and the discipline (runtime-information table, sweep arms, estimands); that is a methodological structure, not a demonstrated improvement. Expose-all remains the reference and, where it fits and nothing restricted is feasible and cheaper, the answer. Under the token criterion expose-all is not "cheap because cached": caching changes billing, not what the model reads.
