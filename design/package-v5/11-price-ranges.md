# 11. Price ranges for the bill on the university route, and what they do to V5's arithmetic (N-39)

Status: provisional, lead, 2026-10-27. Written for the human's instruction (INT-T-011): model choice waits, the work must not depend on a model, and the lead searches benchmarks and price sources for the price ranges. The university API is free and reports tokens only (`10`), so a price table is needed only to turn token classes into dollars. All pages stored 2026-10-27 in `evidence/literature-20261019/` (manifest rows with URL, time and hashes). Prices are third-party benchmark and aggregator figures from August to October 2026, some promotional, several in conflict; none is an official price sheet read by the lead. Labels: [F] stated by the stored page; [D] derived by the lead; [U] not found.

## 1. Sources
| Id | Page (stored file) | What it gives |
|---|---|---|
| S1 | Artificial Analysis, gpt-oss-120b providers (`v5-aa-gpt-oss-120b-providers-20261027.txt`) | 16 providers; lowest input $0.03-0.05, lowest output $0.17-0.25, blended price $0.04 to $0.39 per 1M (up to 8.9x); the blend is **7:2:1 cache-hit:input:output**, labelled "general agentic"; cache write and storage are "billed separately and vary by provider" (:59-65, :105-109, :453-465) |
| S2 | PricePerToken, gpt-oss-120b (`v5-pricepertoken-gpt-oss-120b-20261027.txt`) | a provider table with input, output, cache-read and cache-write columns for 18 providers (:222-560) |
| S3 | Artificial Analysis, GLM-5.3 providers (`v5-aa-glm-5-3-providers-20261027.txt`) | 26 providers; lowest input $0.14-0.56, lowest output $0.64-1.98, blended $0.12 to $2.52 (21.6x) (:550-574) |
| S4 | Artificial Analysis, MiniMax-M3 providers (`v5-aa-minimax-m3-providers-20261027.txt`) | 12 providers; lowest input $0.23-0.28, lowest output $0.96-1.10, blended $0.18 to $0.78 (4.4x) (:368-392) |
| S5 | MiniMax pricing guide (`v5-puter-minimax-pricing-20261027.txt`) | first-party M3 $0.30 input and $1.20 output, a 50% promotion off $0.60 and $2.40; cache read $0.06; write price given for older models only, $0.375 (:36, :68, :84, :98, :124) |
| S6 | Qubrid, Qwen3.8-27B (`v5-qubrid-qwen38-27b-pricing-20261027.txt`) | list $0.72 input, $4.31 output, $0.14 cached; discounted $0.58, $3.45, $0.11; reasoning tokens bill as output (:21, :31-42) |
| S7 | eesel, GLM-5.3-Flash (`v5-eesel-glm53-flash-pricing-20261027.txt`) | Z.ai list $0.15, $0.50, cached $0.03 (promotion half that); cache storage free "limited-time"; output includes reasoning; flagship GLM-5.3 list $1.40 and $4.40 (:37-42, :56) |

## 2. The three ratios that decide the bill's structure [F, from the table above, with [D] ratios]
| Ratio | Meaning | Range seen | Evidence |
|---|---|---|---|
| **r**, cache read / input | 1.0 means no cache discount | **0.14 to 1.0**; about 0.2 for GLM-5.3-Flash (0.03/0.15), MiniMax-M3 (0.06/0.30) and Qwen3.8-27B (0.14/0.72); 0.5 at Groq (0.075/0.15); **1.0 at six gpt-oss-120b hosts that list a cache-read price equal to input** (for example CoreWeave 0.03/0.03, AkashML, Venice, DekaLLM, Crusoe, SambaNova); no cache-read price at eight of 18 | S2, S5, S6, S7 |
| **w**, cache write / input | a write premium | **1.0 (no write fee listed by any of the 18 gpt-oss-120b hosts, nor for GLM-5.3-Flash or Qwen3.8-27B) up to 1.25** (MiniMax's older models: $0.375 against $0.30); MiniMax-M3's write price is not stated [U] | S2, S5, S7 |
| **o**, output / input | | **3.1 to 7.5**: gpt-oss-120b 4.0 to 7.5 across hosts, GLM-5.3 3.1 (4.40/1.40), GLM-5.3-Flash 3.3, MiniMax-M3 4.0, Qwen3.8-27B 6.0 | S2, S5, S6, S7 |
Reasoning tokens bill as output [F] (S6, S7), the same as DPR-0006 and as the university API reports them (`10` section 2). For comparison, the frontier vendors of DPR-0006 (FND-0039) have r of 0.1 to 0.025 and w of 1.25 to 2.0: **the hosted open-weight prices have a weaker cache discount and almost no write fee**.

## 3. Named reference cases for dollar conversions (per 1M tokens, [F] from the sources; any one is an example, not a choice)
| Case | Input | Output | Cache read | r | Source |
|---|---|---|---|---|---|
| RC-1 gpt-oss-120b, cheapest hosts | 0.03 | 0.17 | 0.03 | 1.0 | S2 (CoreWeave row) |
| RC-2 gpt-oss-120b, Groq | 0.15 | 0.60 | 0.075 | 0.5 | S2 |
| RC-3 GLM-5.3-Flash, Z.ai list | 0.15 | 0.50 | 0.03 | 0.2 | S7 |
| RC-4 MiniMax-M3, first party (promotion) | 0.30 | 1.20 | 0.06 | 0.2 | S5 |
| RC-5 Qwen3.8-27B, Qubrid list | 0.72 | 4.31 | 0.14 | 0.19 | S6 |
| RC-6 GLM-5.3, Z.ai list | 1.40 | 4.40 | not found [U] | not found | S7 |
Dollar levels span about 50x across the cases (input $0.03 to $1.40), but the bill's **shape** depends only on r, w and o. A bill in dollars for any case is `input_price * (fresh + w * written + r * read) + output_price * output`, counts from the API's usage record (`10` section 2).

## 4. What the ranges do to the V5 arithmetic (D-04, `calc/price_sensitivity.py`) [D]
The break-evens of D-01 and D-02 were first computed at the frontier-vendor ratios. Recomputed over **r 0.14 to 1.0, w 1.0 and 1.25, o 3.1 to 7.5**:
- **The regime break-even hardly depends on price.** For a 10-request session, deferral beats exposing every tool above 11-13 tools with one search per session, 20-24 with three, and 52-65 with ten, across the whole range. What matters is how many searches a session makes.
- **For short sessions the direction reverses.** At 3 requests a weaker cache discount raises the break-even (10 searches: about 71-99 tools at r 0.14, 118-134 at r 1.0), because every client-side search is an extra request that re-reads the history at r.
- **The seed break-even is also set by session length and by how many matches a search returns, not by price:** 0.10-0.25 for sessions up to 10 requests and 0.34-0.57 for 30-100 requests with three matches per search; with one match it is 0.12-0.35, 0.57-0.77 at 30 requests, and never at 100.
- **Consequence:** V5's design conclusions (`04` sections 1-2) do not depend on which model or host is chosen, which is the property the human asked for. They depend on the measured number of searches per session and matches per search.

## 5. Benchmark facts worth keeping
- Artificial Analysis blends prices at **7:2:1 cache-hit:input:output** for "general agentic" use (S1, S3, S4), i.e. it assumes 70% of tokens are cache hits. V5's per-session mixes are to be measured, not assumed; the 7:2:1 mix is a reference for comparing with published blends.
- The same benchmark measures a **cache hit rate per provider** in multi-turn agentic coding sessions (S1 :205-214), which the page shows only as charts; the stored text holds no values [U]. Providers with identical prices can differ in how much of the input is served from cache.
- Prices vary up to 8.9x (gpt-oss-120b), 21.6x (GLM-5.3) and 4.4x (MiniMax-M3) across hosts of the same model (S1, S3, S4), so a single "model price" is not a stable input to a result.

## 6. What this does not show
No official price sheet was read; some figures are promotional and may change; MiniMax-M3's write price and GLM-5.3's cache price were not found; Qwen3.8-27B appears at $0.45 and $3.20 on another aggregator (not stored) against S6's $0.72 and $4.31 list. The university's own cost, if any, is not stated. The price ratios of the API the human uses are unknown: it reports tokens only.

## 7. For the human
Nothing blocks on this page. **Suggested handling of N-39:** report every result as token classes plus the three ratios (r, w, o), and add dollars under one or two reference cases only when a number for a reader is wanted. That keeps the results independent of the model, as asked. Say if you want a different choice.
