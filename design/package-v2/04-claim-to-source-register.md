# 04. Claim-to-source register for the decisive arguments

Status: provisional; assembled by the lead from DPR-0004 section 7 (design-proposer), the evidence-steward's verification file (`findings/SUM-0003-pivotal-claims-verification.md`, front matter `FND-0001`), the challenger's re-checks (RV-0003) and the lead's own checks. Evidence is quoted by extract id; extracts are tool-written and hash-verified, and show what a source says, **not** that it is true.

**Labels.** **SV** = verified by the evidence-steward against the original passage, with its verdict (SUPPORTED / PARTLY / CANNOT DETERMINE). **RP** = read by the proposer or lead in the extract, not checked against the original by the steward. **MAP** = relied on the AUTH-004 evidence map (SUM-0002, lead's unverified reading), not re-read in this task. **2H** = second-hand (cited by an agent from a governing copy, never read at the original). **DERIVED** = arithmetic or inference from extracts (reproduced independently where stated). **UNSUPPORTED** = hypothesis or unknown. Vendor documentation is a vendor claim.

## A. Decisive arguments
| # | Decisive argument (what it supports in C-A) | Source | Label and limits |
|---|---|---|---|
| 1 | Default cache lifetime 5 minutes, refreshed at no extra cost on each use, measured from the start of the request (session cadence; free-rewrite window) | EXT-0057 | **SV** V1 SUPPORTED. Anthropic documentation only; a 1-hour option exists at extra cost; silent on other providers |
| 2 | Cache write 1.25x (5 min) and read 0.1x (0.025x / 0.05x on named models) of base input price (the multipliers in A1) | EXT-0021 | RP, vendor price page; the multipliers must be estimated per tested provider |
| 3 | Editing the tools array invalidates the cache for the whole conversation; mid-conversation tool changes by reference or by value leave the tools array and earlier messages intact (withdrawal without rewrite; add-only is not forced on that provider) | EXT-0058, EXT-0059 | **SV** V2 PARTLY: quotes hold; a beta; one provider |
| 4 | Keep at least one non-deferred tool, else the first by-value definition costs one full cache miss; a search tool counts as non-deferred | EXT-0066 | **SV** (steward found it under V2; it is **not** in EXT-0060, whose label does not match its body) |
| 5 | Whether withheld or withdrawn or deferred definitions count toward billed or model-visible tokens (the measured `c_def`) | EXT-0058..0060, EXT-0066 | **UNSUPPORTED**: V2 CANNOT DETERMINE; "not stated" |
| 6 | Anthropic deferred tools: every definition still sent in `tools` each request; deferred ones excluded from the prefix; the appended `tool_reference` leaves the cache intact | EXT-0009 | RP, vendor claim |
| 7 | OpenAI: a deferred function still shows name and description (so deferral mostly defers the schema); mixing eager and deferred "supported but generally not recommended" **in an Agents API session**; "Discovery adds a step" | EXT-0010, EXT-0012 | RP, vendor. Vendor guidance **differs with different scopes**; "vendors disagree" was overstated and withdrawn |
| 8 | Adding or removing definitions mid-conversation invalidates the cache; a stable `call_tool` meta-tool keeps the array unchanged | EXT-0014 | RP, guidance (not measurement) |
| 9 | Toollery natural replay: full library $0.000749, 87,074 tokens, hit 0.989, AST 0.787; restricted $0.000819, 2,196 tokens, hit 0.144, AST 0.840; difference "inconclusive", +$0.000070, 95% CI [-0.000524, 0.000462]; cache-suppressed and forced-warm rows differ by orders of magnitude | EXT-0061, EXT-0062 | **SV** V3 PARTLY: numbers match; "no advantage" is not "costs more"; single-step BFCL replay, per-request means; **model, pricing and how the candidate lists were built are not in the stored text** (lead grep of the source confirms) |
| 10 | The low Toollery hit rate is caused by per-query variation of the candidate list | EXT-0062 + inference | **UNSUPPORTED** (inference; the cause is not stated in the source) |
| 11 | A linear price model with one cache-read multiplier of about 0.0088 fits all six Table 15 cells; break-even restricted hit rate about 0.22; predicted cost ratio about 1.09 | EXT-0062 | **DERIVED**, proposer's arithmetic, **independently reproduced by the challenger** (read ratio 0.0087-0.0089); not steward-verified. The implied multiplier is far below the vendor-page ones, so it is a property of that provider/table, not a general value |
| 12 | Enforced extra exploration after an incorrect termination: "most models improve by less than 5 percentage points" (extra-turn control) | EXT-0063, EXT-0064 | **SV** V4 SUPPORTED. A blocked-action planning benchmark, not tool exposure; the trigger needs knowing the answer is incorrect |
| 13 | FitText instructs the agent by prompt to use the {BEGIN}...{END} protocol and the only starting function is "Finish" (so its emission is prescribed, not spontaneous) | EXT-0065 (+ EXT-0050/0051/0055/0056) | **SV** V5 SUPPORTED; "may emit" in the method vs "must" in the prompt; the model emits, the system only de-duplicates and executes |
| 14 | DynamicMCPBench App. N Table 7: curated (about 8 tools) 37.3/42.7/44.0/54.0; rag:k below it; `hier` (two-stage router) indistinguishable from rag:16/32; flat 36.0 on one model; retrieval loss and distraction separable; pass^3 0.0% on tasks the retriever never surfaced | EXT-0053 | **SV** V6: numbers SUPPORTED; the decomposition claims PARTLY (one model, one 150-task draw, single attempts, intervals about ±8; "pass^3 0.0%" is for rag:8 only; the flat value sits under no column header) |
| 15 | Budget-30 control: pass 20.0% vs 18.0%; 5/50 vs 0/50 tasks reached the budget; "Not pre-registered", exploratory | EXT-0042 | **SV** V7 SUPPORTED; one model/cell; no interval; extract ends mid-sentence |
| 16 | No Tool Use shares of diagnosed failures (Haiku 4.5 25.7%, Opus 4.7 9.1%, ...) and the definition "even though tools were required" | EXT-0047..0049 | **SV** V8 PARTLY: shares of failures, not tasks; the definition does not say the needed tools were visible, so it does **not** decide whether models search for an absent tool |
| 17 | Removal without recovery lowers recall ("If the required tool is not selected in the first stage, its full schema is unavailable") | EXT-0045, EXT-0046 | RP; small on-device paper; a P3/P4 pattern, not a filtering cascade |
| 18 | A break-even accounting form for loading optional material exists | EXT-0041 | RP; skills, not tools; transfer is an assumption; its `r` (reloads) is not A1's `r` (cache read multiplier) |
| 19 | Retrieval lowered success in several settings; more tools hurt in some | EXT-0026, 0028, 0033, 0034 | MAP (AUTH-004 evidence map; not re-read) |
| 20 | The record does not show a second filtering stage paying | EXT-0053 `hier`; EXT-0054 | EXT-0053 **SV** as row 14; EXT-0054 RP (weak source) |
| 21 | Usage is concentrated enough for a core to exist | none | **UNSUPPORTED** (HYP-0014) |
| 22 | Models search when told to and a tool is absent | none | **UNSUPPORTED** (HYP-0010) |
| 23 | A stable restricted surface keeps its hit rate | none | **UNSUPPORTED** (HYP-0007) |

## B. Lead's own checks in this task
| # | Check | Result |
|---|---|---|
| L1 | DPR-0005 section 3.2 says the varying-surface threshold rises "by about 141 turns per unit of s" | with `T* = (rho+s)(w-r)/(r(1-rho))`, `rho = 0.025`, `r = 0.0088`, `w = 1` the slope is about **115**; `T* = 2.9` at `s = 0` is correct. **Discrepancy in the proposer's text; qualitative point unchanged.** Recorded here, the record not edited |
| L2 | Toollery's replay model, pricing and candidate-list construction | not in the stored text (grep of the source); only the offline-construction pricing is stated (a different step) |
| L3 | FitText's initiator | model-emitted request, system-executed retrieval, prompt-prescribed (EXT-0050/0051/0055/0056/0065) |
| L4 | EXT-0060's label vs body | the label "Keep_one_non-deferred_tool" is wrong; the rule is in EXT-0066 |
| L5 | Ledger scope drift in the proposer's first draft | corrected in the final record (row 7 above) |

## C. Items used only to bound claims; never relied on for a decision (second-hand)
Enrich-Retrieve-Rank (0.56 x 0.70 decomposition), MCP-Zero routing, ITR beyond its ablation table (EXT-0054), PlanBench-XL beyond the extracted passage, Executor passthrough default, the ledger rows C3-*/K* and Toollery's wider claims (cited from governing copies or by the challenger; **not read at the original**); CE-MCP figures (the extract has a qualitative result sentence only, EXT-0044); the AUTH-004 evidence-map rows (EXT-0015, 0016, 0018, 0026, 0030, 0032-0034).

## D. What the steward did not check
Table 15's model and pricing; PlanBench-XL Fig. 4 values (caption only); the pass^3 sample count for unreachable tasks; whether other FitText modes use a different prompt; provider differences for mid-conversation tool changes beyond what EXT-0058 states; all closed-form cost algebra (checked only by the challenger).
