# RESULTS-P5-B: OpenAI hosted tool search, gpt-5.4-mini (AUTH-028 part B; lead, 2026-11-07)

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
- **AUTH-028 stop rule.** The as-written predictions are contradicted by more than any spread seen here, so this is reported before the next item. Revising D-01 (a vendor-hosted variant with a visible deferred part, a measured surface, appended tokens per search, a warm-start case and the non-tool part) is a design change that AUTH-028 does not cover. It is proposed for the human's decision, not made.

## 4. Limits
- One session per cell and one run; cache state not controlled (warm from calibration); two cache misses.
- One model (`gpt-5.4-mini`), reasoning effort low.
- A stub catalogue with short descriptions, one simple task, and outputs of about 250 tokens per session.
- Hosted tool search only; client-executed search was not run.
- Nothing here bears on ScaDS (part A), where the harness defers the whole definition and appends 3 definitions per search, which is closer to D-01's assumptions.
