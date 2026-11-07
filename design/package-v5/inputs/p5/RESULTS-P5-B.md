# RESULTS-P5-B: OpenAI hosted tool search, gpt-5.4-mini (AUTH-028 part B; lead, 2026-11-07)

**What this is and is not (the human, 2026-11-07: "this test does not count as P5 test yet").** It is a side check of a vendor mechanism: whether OpenAI bills deferred definitions that are never loaded. **It is not P5's test.** P5 asks for the break-even on our own route, ScaDS with client-side deferral (`05` P5; `04` section 5), and that is part A, not yet run. Two faults of this run also rule it out as a template:
- Its sessions started warm from the calibration requests, so the cache state was not controlled.
- It had one session per cell, so there is no spread to judge against.

The harness was revised for part A (revision 2: a fresh marker per cold session, two cold and one warm session per cell; `README.md`). The figures below stand as what this run measured.

## Repeat with harness revision 2 (2026-11-07, 15:09-15:14 UTC): use these figures; the first run's sections below are kept as recorded
- **Approval and spend.** The human accepted the repeat at "about $0.40, stop at $0.60" (INT-T-026). It took 193 requests, all HTTP 200, and cost $0.445. The OpenAI side check cost $0.594 in all (first run $0.149).
- **Files:**
  - Harness revision 2: `87905175...045409`.
  - Log `openai-gpt54mini-r2/requests.jsonl`: `795277a0...4f8b10`.
  - Analysis `openai-gpt54mini-r2-analysis.json`: `c47dab03...297e51`.
  - Script `p5_analyze.py`: `452e3cf7...22c8f9`.
- **Design:** 13 calibration requests with markers of their own; per size and arm, 2 cold sessions (fresh marker in tool 0), then 1 warm session reusing the second cold session's marker.
- **The control worked [O].** Every cold session started with 0 cached tokens. Warm sessions started 60-99.6% cached, with one exception: the eager warm session at 30 tools started with 0 cached, so the warm ratios at 30 are not readable.

**Billed tokens per deferred definition (calibration, unchanged from the first run) [O].** Individually deferred functions bill 51.5 tokens of 171 at 300 tools (30%). In namespaces it is 6.2 (3.6%).

**Bill ratio deferral / eager, whole session, fresh-token equivalents [O]** (cold = mean of the 2 cold sessions, the two values in brackets)

| n | deferred_fn cold | deferred_ns cold | deferred_fn warm | deferred_ns warm |
|---|---|---|---|---|
| 10 | 1.19 (1.18, 1.20) | 1.12 (1.12, 1.13) | 1.33 | 1.29 |
| 30 | 0.70 (0.71, 0.70) | 0.67 (0.67, 0.67) | not readable* | not readable* |
| 100 | 0.44 (0.44, 0.44) | 0.29 (0.29, 0.29) | 0.58 | 0.42 |
| 300 | 0.35 (0.35, 0.35) | 0.11 (0.10, 0.13)** | 0.39 | 0.21 |

`*` The eager warm session at 30 tools missed the cache (see above).
`**` The two cold sessions loaded different amounts with their first search: 325 and 1,360 tokens (in the second, the whole namespace of the needed tool). What hosted search loads varies between identical sessions.

**Reading [I]:**
- **Break-even (cold start): between 10 and 30 tools in both arms.** At 10 tools deferral costs 12-20% more; at 30 it saves about 30%.
- **The two cold sessions agree within 0.02**, except the 300-tool namespace cell (0.03, because of the different load).
- **A warm start shrinks deferral's advantage.** It lowers both bills, but eager's more, because eager's cached prefix is larger; the warm ratios are 0.04 to 0.17 higher than the cold ones.
- **D-01 as written** (server mode, its defaults) predicts 1.32, 0.44, 0.13 and 0.044. At 10 tools it overstates deferral's cost (1.32 against 1.12 to 1.20); at 30 to 300 tools it understates it. At 100 and 300 tools the measured ratio is 2.2 to 7.9 times the prediction. This is far more than the cold-session spread, so the AUTH-028 stop rule applies (reported here; the revision of D-01 is the human's decision).
- **D-01's formula with the measured parameters** reproduces the cold cells within 0.01 to 0.07 at 30 to 300 tools in both arms; at 10 tools it is 0.14 to 0.15 too low.
- **What D-01's defaults miss on vendor-hosted search:** the deferred part that stays billed (30% for functions), the searchable surface (1,300 to 16,000 tokens instead of 300), the tokens a search loads (about 310 for one function, up to 1,360 for a namespace), and the non-tool part of the session (about 2,100 to 2,500 equivalents in both arms).

**Break-even against size of saving (proposed variant, `calc/regime_bill_hosted.py` and its stdout; not adopted) [D].** D-01's server mode was rewritten with the measured terms: the billed share v of a deferred definition, the search tool's surface, the tokens a search loads, the non-tool part and the start state. Three things follow:
- **The break-even barely moves.** With d = 171 and T = 5 it is 11 tools (individually deferred functions, cold) and 13 (namespaces, cold); 16 and 22 when warm. D-01-like defaults give 11. The measured break-even, between 10 and 30, agrees. **D-01's break-even holds; what it gets wrong is how much deferral saves above it.**
- **Most of that gap is the billed share v.** At 300 tools the cold ratio is 0.06 with v = 0, 0.09 with v = 0.036 (namespaces) and 0.35 with v = 0.30 (functions). The non-tool part X does not move n*, because it adds to both arms; it only pulls the ratio towards 1.
- **The variant fits the side check's cold cells within 0.01 to 0.10, except functions at 10 tools (1.03 against 1.19).** This is a fit to the same data, not a test.

**Decision (the human, 2026-11-07, INT-T-027): D-01 stays the working equation; the variant stays a proposal; whether to revise D-01 is decided after P5 part A on ScaDS, which tests D-01's own client mode.** Nothing is adopted.

**Still the side check, not P5's test:** one model, one stub catalogue, one task, low reasoning effort, hosted search only.

Status: run complete, all 12 cells. Labels: [O] measured from the usage records, [D] arithmetic, [I] reading. **One session per cell, one model, one stub catalogue:** read as a first measurement, not an estimate with a range. No accuracy claim.

## Setup
- **Harness:** `design/package-v5/tools/p5_break_even.py`, SHA-256 `5e19e674...ff54ff`, the same version for every run (see `run-meta.json`).
- **Analysis:** `design/package-v5/tools/p5_analyze.py` (`4bf5a157...`). Output: `openai-gpt54mini-analysis.json` (`678dd4cd...`).
- **Model and settings:** `gpt-5.4-mini`, served as `gpt-5.4-mini-2026-03-17`. Responses API, `store` false, reasoning effort low.
- **Arms:** `eager` (all n definitions offered); `deferred_fn` (5 core tools, the other definitions deferred, plus `tool_search`); `deferred_ns` (deferred definitions in namespaces of at most 10, plus `tool_search`).
- **Sizes and task:** 10, 30, 100 and 300 tools; 13 calibration requests ("Reply with OK."); one session of three user turns per size and arm.
- **Prices:** OpenAI's page read on 2026-11-07 (`evidence/literature-20261019/price-openai-20261107.md`): $0.75 input, $0.075 cached and $4.50 output per million tokens, no write charge. In D-01's terms: r = 0.1, w = 1, o = 6.
- **Runs and logs** (2026-11-07, UTC):
  - `openai-gpt54mini-smoke`: 3 requests.
  - `openai-gpt54mini`: 60 requests, 13:37-13:44. It stopped after two broken-pipe failures just before the laptop's desktop session was killed (13:45); the 300-tool cells and the 10-tool eager session were left unfinished.
  - `openai-gpt54mini-resume300` (15 requests) and `openai-gpt54mini-resume10` (5 requests), 13:59-14:00: the missing sessions, same harness. The analysis keeps only complete sessions.
- **Spend: $0.149 in all** (smoke $0.004, first run $0.108, resumes $0.035 and $0.002), against the accepted estimate of $0.80 and the stop at $1.20.

## 1. Are deferred definitions that are never loaded billed? Yes, in part [O]
Calibration requests, no tool needed. A full definition bills about 171 tokens at every size (the stub catalogue, OpenAI's tokenizer).

| n | eager prompt | deferred_fn prompt | billed per deferred function | deferred_ns prompt | billed per deferred function in a namespace |
|---|---|---|---|---|---|
| 10 | 1,738 | 1,523 | 127 (75%) | 1,355 | 94 (55%) |
| 30 | 5,159 | 2,530 | 66 (38%) | 1,769 | 35 (21%) |
| 100 | 17,129 | 6,032 | 54 (32%) | 2,337 | 15 (9%) |
| 300 | 51,368 | 16,065 | 51 (30%) | 2,716 | 6 (4%) |

- **Individually deferred functions** still bill about 30% of a full definition. As OpenAI's page says, the model "still sees the function name and description", so only the parameter schema is deferred (L/v5-openai-tool-search-20261022.md:22). In these stubs the description is short and the bulk is in the schema, so with longer descriptions the share would be higher [I].
- **Namespaces** bill only their own lines: about 6 tokens per tool at 300.
- At 10 and 30 tools the per-tool figures include the fixed cost of the `tool_search` definition itself, which is not subtracted.

## 2. Session bills and the break-even [O]
Whole session (system text, history, tool results and output included), in fresh-input-token equivalents (DPR-0006) and in dollars.

| n | eager | deferred_fn (ratio) | deferred_ns (ratio) |
|---|---|---|---|
| 10 | 3,081 ($0.0023) | 4,575 (1.49) | 3,790 (1.23) |
| 30 | 5,122 ($0.0038) | 4,525 (0.88) | 7,091 (1.39)* |
| 100 | 10,944 ($0.0082) | 6,257 (0.57) | 5,922 (0.54) |
| 300 | 28,242 ($0.0212) | 11,207 (0.40) | 7,275 (0.26) |

`*` The last request of this session had no cache hit (0 of 2,692 tokens) on an unchanged prefix. One other request (smoke, turn 2) did the same. Two of 77 successful requests therefore missed the cache entirely: OpenAI's caching is not guaranteed request by request.

**Break-even in this run:**
- `deferred_fn`: between 10 and 30 tools.
- `deferred_ns`: between 10 and 100 tools; 30 is not readable because of the cache miss.
- Above that, the saving grows with n. At 300 tools the bill is 0.40 (`deferred_fn`) and 0.26 (`deferred_ns`) of eager's.

Every session searched once (twice at `deferred_ns` 100), called the needed tool twice and ended the third turn without a tool call. This is a check that the sessions ran as designed, not an accuracy result.

**Warm starts favour eager here** [O/I]. The calibration requests and the interrupted attempts had just sent the same prefixes, so every eager session started 95-99.7% cached, and the deferred sessions 63-98%. D-01 prices a cold start. On this table a cold start adds (1 − r) × prefix to the first request: about 46,000 equivalents for eager at 300 tools. With every arm started cold, the ratios at 300 would be about 0.34 (`deferred_fn`) and 0.13 (`deferred_ns`) instead of 0.40 and 0.26 [D].

## 3. Against D-01 [D]
| n | arm | measured | D-01 as written | D-01 with measured parameters |
|---|---|---|---|---|
| 10 | fn / ns | 1.49 / 1.23 | 1.32 | 1.11 / 1.08 |
| 30 | fn / ns | 0.88 / 1.39* | 0.44 | 0.83 / 0.85 |
| 100 | fn / ns | 0.57 / 0.54 | 0.13 / 0.20 | 0.53 / 0.43 |
| 300 | fn / ns | 0.40 / 0.26 | 0.044 | 0.39 / 0.21 |

- **D-01 as written** (`calc/regime_bill.py`, server mode, its defaults) is too optimistic for deferral at 100 and 300 tools: the measured ratio is 2.8 to 9.0 times the predicted one. It assumes four things that do not hold here:
  - The whole definition is deferred; here names and descriptions stay billed (section 1).
  - A search appends 3 definitions; here it adds about 310 tokens (one schema) for `deferred_fn` and 300 to 1,350 tokens (the loaded namespace) for `deferred_ns`.
  - The search tool costs 300 tokens; here the searchable surface costs 1,300 to 16,000 tokens.
  - Every session starts cold, and only the tool block is priced; here the sessions started warm, and the rest of the session (about 2,200 to 2,600 equivalents) is the same in both arms, which pulls every ratio towards 1.
- **D-01's formula with the measured parameters** (the surface from calibration, the tokens added by the first search, each session's start state, and eager's non-tool part) reproduces `deferred_fn` within 0.01 to 0.06. For `deferred_ns` the gap is 0.05 to 0.11, apart from the cache-miss cell. So D-01's structure holds; its default parameters do not fit vendor-hosted search.
- **AUTH-028 stop rule.** The as-written predictions are contradicted by more than any spread seen here, so this is reported before the next item. Revising D-01 (a vendor-hosted variant with a visible deferred part, a measured surface, appended tokens per search, a warm-start case and the non-tool part) is a design change that AUTH-028 does not cover. It is proposed for the human's decision, not made; the human deferred that decision until part A (INT-T-027).

## 4. Limits
- One session per cell and one run; cache state not controlled (warm from calibration); two cache misses.
- One model (`gpt-5.4-mini`), reasoning effort low.
- A stub catalogue with short descriptions, one simple task, and outputs of about 250 tokens per session.
- Hosted tool search only; client-executed search was not run.
- Nothing here bears on ScaDS (part A), where the harness defers the whole definition and appends 3 definitions per search, which is closer to D-01's assumptions.
