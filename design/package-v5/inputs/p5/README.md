# P5 break-even: harness, run plan and cost estimate (AUTH-028; lead, 2026-11-07)

Status (2026-11-08): **P5's test (part A, ScaDS, our route) is done** (`RESULTS-P5-A.md`: break-even between 10 and 30 tools, close to 10; D-01 as written fits this route within 0.01-0.03 at 30-300 tools). Earlier status (2026-11-07, later): P5's test had not been run. The OpenAI runs (part B) are a side check of vendor billing, not P5's test: `RESULTS-P5-B.md`. The first run cost $0.149; the repeat with revision 2 cost $0.445 (2 cold and 1 warm session per cell; INT-T-026). Part A's cap is raised to about 140 requests (INT-T-026); it waits for GLM B2 to end. Its lessons changed the harness (revision 2, below).

## Harness
`design/package-v5/tools/p5_break_even.py` (standard library only). Revision 1 (`5e19e674...ff54ff`) ran part B; **revision 2** (`87905175...045409`) is for part A; each run records the hash of the version that ran in `run-meta.json`).
- **Catalogue:** stub tools generated from a fixed seed. Each is about 1,100 characters of JSON (about 275 tokens; D-01 assumed 250), with a short description and the bulk in the parameter schema. The needed tool, `orders_get_shipping_status`, is in every catalogue and never in the deferral core.
- **Task:** one session of three user turns: the status of order 4471, the same for 4472, then both in one sentence. The harness answers every tool call with fixed stub data.
- **Arms:**
  - ScaDS: `expose_all` (all n definitions in `tools`) against `deferral`. The deferral core is 5 tools plus `search_tools` and `call_tool`. Search results come back as a tool result, so `tools` never changes (V5-R02); each search returns 3 definitions, as D-01 assumes (K = 3).
  - OpenAI: `eager` against hosted tool search, with deferred functions (`deferred_fn`) and with namespaces of at most 10 functions (`deferred_ns`).
- **Sizes:** 10, 30, 100 and 300 tools. These bracket D-01's break-evens: 12-57 with a cached core, 37-136 with an uncached core.
- **Calibration requests** ("Reply with OK.", no tool needed) give the tokens per definition. On OpenAI they also answer P5's second question: are deferred definitions that were never loaded billed?
- **Recorded per request:** prompt, cached, cache-write, reasoning and completion tokens; the served model id; latency; tool names called. No message text is stored.
- **Stops:** HTTP 401, 402 or 403; two failures in a row; the request cap; the spending cap.
- **Analysis:** `--analyze` reports the bill ratio of deferral to expose-all per size, in DPR-0006 fresh-token equivalents.
- **Mechanism caveat:** search plus `call_tool` is this harness's way of keeping `tools` fixed on ScaDS. It is not the client-side mechanism P2 still has to choose (`17` section 9, item 8).

## Revision 2 (2026-11-07, after part B)
- **Cold starts are forced.** A fresh random marker leads the description of tool 0, the first definition in both arms. On ScaDS GLM-5.3 the tools come before the system text (`10` section 9), so the marker has to sit in a tool to make the whole prefix new.
- **Repeats.** Each size and arm gets 2 cold sessions, each with its own marker, which gives a spread. Then 1 warm session reuses the last marker, which gives the warm start that D-01 only describes as a difference (table E).
- **Calibration requests get markers of their own**, so they cannot warm a session.
- **Analysis.** `design/package-v5/tools/p5_analyze.py` compares the ScaDS results with D-01 in its client mode (search is a separate request), with both the cached-core and the uncached-core variants.
- **Request count (mock run): 138** (6 calibration, 88 cold, 44 warm). That is above AUTH-028's "at most about 100 requests per model". Options:
  - (a) Raise the cap to about 140 for this free route (recommended).
  - (b) Keep 100: 2 cold sessions and no warm session (about 94 requests).
  - (c) Keep 100: 1 cold and 1 warm session (about 94).

## Run plan
| Part | Route, model | Requests (from the mock run) | Cost | When |
|---|---|---|---|---|
| A. Break-even curve | ScaDS, `zai-org/GLM-5.3`, reasoning as served | 138 with revision 2 (option a), or about 94 (options b, c) | free | After the AUTH-026 GLM B2 run ends (AUTH-028). On 2026-11-07 at 13:20 UTC it was at task 21 of 57 after 9.5 h, so roughly 10 to 16 h more: the night of 7 to 8 November or the morning of 8 November. At B2's latency of 2026-11-06 (about 1 min per call), 138 requests take about 2 to 3.5 h. |
| B. Are deferred definitions billed? | OpenAI, `gpt-5.4-mini`, Responses API, reasoning effort low | 73 (13 calibration; 1 session x 4 sizes x 3 arms) | **about $0.80; stop at $1.20** | Any time, independent of ScaDS. Needs an OpenAI key in `~/r3-work/.env` as `OPENAI_API_KEY`: that file holds only OpenRouter and ScaDS keys now. |

**How the OpenAI estimate is made.** Prices are from the stored OpenAI price page of 2026-10-19 (`evidence/literature-20261019/price-openai-20261019.md`, standard tier): `gpt-5.4-mini` costs $0.75 per million input tokens, $0.075 cached and $4.50 output.
- The calibration requests send about 120,000 input tokens per arm, uncached: about $0.09 each.
- Eager sessions send about 620,000 input tokens. With about 80% cached, that is about $0.13.
- The deferred arms cost the same as eager in the worst case, if deferred definitions are billed in full: about $0.45 for both together.
- Output: about 22,000 tokens, about $0.10.
- The total is about $0.80. The mock run with only a third cached came to $1.20, which is the stop (1.5 times the estimate).

**Before part B:** the price page must be read again on the day of the run, since it is three weeks old. A first single request checks that `gpt-5.4-mini` accepts `tool_search` (the stored page says "gpt-5.4 and later"; whether mini is included is [U]). If it does not, the fallback is `gpt-5.4`, which costs about 3.3 times as much: about $2.70, stop at $4. That needs your approval of the new estimate first.

## Not covered
P1 to P4, any policy parameter, any accuracy claim. A result that contradicts D-01 or D-04 by more than the run-to-run spread is reported, and the design is revised before the next item (AUTH-028 stop rule).
