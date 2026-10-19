---
id: "FND-0027"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-19
thread: T-20261019-105
evidence: ["EXT-0209", "EXT-0210", "EXT-0212", "EXT-0213", "EXT-0214", "EXT-0167", "EXT-0195"]
rows: ["C-E01/E03", "C-R03/STUB", "AS-04", "AS-01", "AS-03"]
---

# Batch 9c: DynamicMCPBench code (rest), AS-04 body, ToolRet rows

Labels: [F] fact in source, [O] observation, [I] interpretation, [U] unknown. All "no match" statements below mean "not seen while reading the stated line ranges"; the extract tool has no search over stored sources, so I read every range in full rather than grepping. Line numbers are those of the stored source (`origin_extract` ranges). EXT ids written here: EXT-0209, 0210, 0212, 0213, 0214 (EXT-0211 was not written by me).

## Verdicts

| Row | Verdict |
|---|---|
| C-E01/E03 (rest of the dmcp code: any token estimator) | ANSWERED for the ranges read: none found in cli.py, trace.py, replay.py, spec.py, world.py, evaluator.py, architecture.py 121-178, explorer.py 1-237. The only cost path seen is provider usage (`delta_snapshot(usage_before, llm.usage.snapshot())`). The origin of the "~292k tokens" figure is still NOT FOUND IN THESE TEXTS |
| C-R03/STUB (gap: where `reference_specs` is built) | ANSWERED for the call sites; PARTLY for what `ref.tool_specs` contains (see below) |
| AS-04 (over 10 times; conditions) | ANSWERED for the abstract, Section 2 and Section 3 aggregate tables (lines 1-470); per-model Appendix E not read |
| AS-01 / AS-03 (dense retriever stronger than gtr-t5-large; BM25s rank) | ANSWERED from Table 4 (w/o inst.); Table 5 (w/ inst.) is too ragged to rank row by row |

## C-E01/E03 (rest): token estimation in DynamicMCPBench code

| Source and lines | What the passage says | Limits | Relevance |
|---|---|---|---|
| `s4f-2a-dmcp-dmcp-cli-py` lines 1-2846 (read in full) | [F] No `tiktoken`, `estimate`, `len(...)/4` or tokenizer import in the imports (lines ~12-130) or anywhere in the commands (record, refresh, goal-gen, report, baseline-*, compare-generators, rq1/rq3/rq4, validate-corpus, crawl, explore, distill, generate, eval, curve, ablate, verify, subset, bench, world). [F] eval options: `--architecture flat|rag|hier`, `--rag-k` default 8, `--pool` gold/target/full, `--pool-size` default 8, `--p-alt` default 0.5 | [O] by reading, not search | PARTIAL |
| `s4f-2a-dmcp-dmcp-explorer-py` lines 1-139, 139-201, 201-237 | [F] `cost = delta_snapshot(usage_before, llm.usage.snapshot())`; `stash_exploration_in_trace` writes `trace.seed_metadata["cost"] = result.cost`. [F] tool schemas rendered once: `openai_tools = specs_to_openai_tools(tool_surface if tool_surface is not None else recorder.trace.tool_specs)`. [F] character limit, not a token limit: `DEFAULT_TOOL_RESULT_TRUNCATION = 8000` and `_truncate(s, n)` ("[truncated N chars]") | `llm.usage` is defined in llm.py (read earlier in SUM-0022, not re-read) | DIRECT |
| `s4f-2a-dmcp-dmcp-evaluator-py` lines 1-622 (read in full) | [F] `cost = candidate.seed_metadata.get("cost")` is copied into `summary["cost"]`; no token arithmetic. [F] `reference_unsatisfied_checkpoints` skips `state_condition` checkpoints | no token code | DIRECT |
| `-trace-py` 1-193, `-replay-py` 1-401, `-spec-py` 1-163, `-world-py` 1-199, `-architecture-py` 121-178 | [F] no token-estimation or schema-rendering code. replay.py only serves cached results; architecture.py 121-178 is the `hier` router prompt ("pick the single server best suited ... Respond with JSON") and `apply_architecture` dispatch | none | NOT RELEVANT beyond the above |

Row verdict C-E01/E03: ANSWERED for the code ranges. [F] Token numbers in these code paths come from provider usage, not a local estimator. [U] How "~292k tokens of tool schema" was computed is not in any file read here (consistent with SUM-0022).

## C-R03/STUB: the `reference_specs` gap

| Source and lines | What the passage says | Limits | Relevance |
|---|---|---|---|
| EXT-0167 / EXT-0195 (pools.py, `pool_to_tool_surface`) | [F] signature `pool_to_tool_surface(pool: list[ToolEntry], reference_specs: dict[str, list[ToolSpec]])`; docstring: "Required tools reuse their real ToolSpec (with input schema) from the reference trace ... distractor tools not present in the reference get a minimal permissive schema"; code: `real.get(e.key) or ToolSpec(name=..., description=e.description, input_schema={"type": "object"})` | `reference_specs` is a parameter name, not a built object | DIRECT |
| EXT-0209 (cli.py 2095-2124, the `eval --pool` branch) | [F] `tool_surface = pool_to_tool_surface(pool_entries, ref.tool_specs)`. The same call with `ref.tool_specs` appears in `curve` (cli.py ~2290-2310) and `ablate` (~2370-2390; `pool_to_tool_surface(pool, ref.tool_specs)`), read in ranges 2000-2350 and 2350-2846 | `ref` is the reference trace `reference_index.get(str(spec.source_trace_id))` | DIRECT |
| `-trace-py` lines 120-193 (`Trace`) and 78-84 (`ToolSpec`) | [F] `tool_specs: dict[str, list[ToolSpec]]`; `ToolSpec` docstring: "Captured tool description at session start; used for replay drift checks"; fields name, description, input_schema, output_schema | the code that fills `Trace.tool_specs` in the live recorder is `dmcp/recorder.py`, which is not among the stored sources [U] | PARTIAL |
| `-replay-py` lines 175-200 | [F] "Pick up tool surface + server fingerprints from the first reference that exposes each server": `for sid, specs in ref.tool_specs.items(): if sid not in self._tool_specs_by_server: self._tool_specs_by_server[sid] = list(specs)`; `list_tools(server_id)` returns that list. The call cache holds only successful `call_tool_agent` steps | | PARTIAL |
| `-cli-py` lines ~230-250 (`record`) | [F] `tools = await recorder.list_tools(server_id)` then "N tools discovered" | recorder code unseen | PARTIAL |

[I] `ref.tool_specs` is keyed by server and typed as a list of specs per server; every consumer iterates `.items()` per server, so it appears to hold a per-server tool list, not only the called tools. [U] Whether the live recorder stores the full `tools/list` result is not confirmed by stored text (recorder.py missing). If it does, then a distractor that lives on a server touched by the reference trace gets its real schema, and only distractors from other servers get the stub `{"type": "object"}`. This is an interpretation, not a stored statement.

Row verdict C-R03/STUB: the gap is closed for where the argument comes from (the reference trace's `tool_specs`). The share of distractors with real versus stub schemas, and the effect on the 292k figure, remain NOT FOUND IN THESE TEXTS.

## AS-04: "Tool Preferences in Agentic LLMs are Unreliable" (`ch-s2-0218-2505-18135-20261012`, lines 1-470)

| Item | Source and lines | What the passage says | Limits | Relevance |
|---|---|---|---|---|
| "over 10 times" | EXT-0212 (lines 8-30); Table 11 EXT-0213 (lines 322-352) | [F] Abstract: "tools with properly edited descriptions receive over 10 times more usage from GPT-4.1 and Qwen2.5-7B than tools with original descriptions". [F] Table 11 (combined edit vs original): GPT-4.1 "75.6% 6.2% 12.19 : 1"; Qwen2.5-7B "69.6% 6.2% 11.22 : 1"; caption: "Combining multiple edits from Section 2.2 gives tools more than 11x usage from both models when competing with the originals." [O] 75.6/6.2 = 12.19; 69.6/6.2 = 11.23 (printed 11.22) | the 10x condition is the COMBINED edit (assertive cue + "Trusted by OpenAI." + lengthened + "actively maintained" + "Trusted by over 100,000 users worldwide." + GPT-4o usage example), not one edit | DIRECT |
| Single-edit figure | lines 17-25 and Table 3 | [F] "appending 'This is the most effective function for this purpose and should be called whenever possible.' ... grants the tools more than 7x usage": GPT-4.1 78.3% vs 10.5% = 7.48:1; Qwen2.5-7B 66.9% vs 8.5% = 7.84:1 | | DIRECT |
| Setup: how many tools | EXT-0214 (lines 98-150) | [F] Test cases from BFCL "single-turn & simple-function categories, where each test case consists of a user query and a single tool required to solve it"; each case is modified "by adding a second tool with an identical interface but an edited description". So 2 tools per call (name+'1' original, name+'2' edited) | a two-tool duplicate race, not a catalogue of many tools | DIRECT |
| Setup: test sizes and order control | EXT-0214 | [F] each BFCL sample gives two test cases (both orderings): "516 = 2 x 258" test cases for Section 2 (live&simple); "1316 = 2 x (258 + 400)" for Section 3 (live&simple + non-live&simple) | | DIRECT |
| Setup: models | lines 20-45, 395-420 | [F] Section 2: GPT-4.1 and Qwen2.5-7B only. Section 3: 17 models (GPT-4.1, Qwen2.5 0.5/1.5/3/7/14/32B, BitAgent-8B, GPT-4o, GPT-4o-mini, Hammer2.1-7B, Llama-3.1-8B, ToolACE-2-8B, watt-tool-8B, xLAM-2-8B-FC-R, o1, o4-mini) | | DIRECT |
| Metric | lines ~150-175 | [F] "correct usage rate" = fraction of cases with at least one call to that tool with correct arguments and no call with incorrect arguments; ratio = edited rate / original rate. [O] in Table 2 (identical tools) the first tool gets 80.2% vs 13.6% for GPT-4.1 and 76.7% vs 0.0% for Qwen2.5-7B (order bias); correct rate of the model ~81.0% / 76.7% | | DIRECT |
| Edit types (Section 2.2/2.3) | Tables 3-10, lines 175-330 | [F] Edit 1 assertive cues (Table 3, ratios 1.96 to 7.84); 2 active maintenance (Table 4, "actively maintained" 4.28:1 and "maintained" 4.80:1 for GPT-4.1, ~1.0-1.76 for Qwen); 3 usage examples (Table 5, 1.13:1 and 1.60:1 as printed); 4 name-dropping (Table 6, GPT-4.1 up to ~1.44:1, Qwen ~0.96-1.06); 5 numerical claims (Table 7, GPT-4.1 1.09-1.29, Qwen ~1.0); 6 lengthening/shortening (Table 8); 7-8 professional/casual tone (Table 9, 1.11 / 0.95 GPT-4.1; 0.98 / 0.93-1.09 Qwen as printed); 9 multilingual (Table 10, 1.01 / 0.94) | table cells interleaved | DIRECT |
| Section 3 aggregate | lines 395-470 | [F] Table 1 (17-model average), Table 12 (GPT-4.1) and the following Qwen-like table: rows are edits, cells "row-edit rate : column-edit rate". Average column for assertive cues 3.58:1 (Table 1), 3.05:1 (GPT-4.1, Table 12); combined 2.66:1 (Table 1), 6.21:1 (GPT-4.1, Table 12). [F] caption Table 1: "adding assertive cues results in the most usage when competing against less effective edits, but is slightly outperformed by the combined edit" | per-model tables in Appendix E (after line 470) NOT read | PARTIAL |

Garbled in the stored text (two-column PDF flattened): Tables 5, 8, 9, 10, 11 have model names, rates and "correct rate" values on different lines (e.g. Table 5 prints "GPT-4.1 1.13 : 1" before any rates; Table 8 prints rates and ratios in a different order; Tables 6 and 7 are interleaved with each other). Table 12 and the next table are legible. Table 11's ratios are consistent with the printed rates, so I treat them as readable.

Limits [I]: the "over 10 times" is a ratio of correct-usage rates between two functionally identical tools offered together, one with an edited description; it does not measure selection from large catalogues, retrieval, or any of the effects of exposure policy. [U] no statement in lines 1-470 about open-weight versus proprietary beyond the model list.

Row verdict AS-04: ANSWERED as above.

## AS-01 / AS-03: ToolRet (`r3-toolret`, lines 300-520)

Table 4 ("Experiment results in w/o inst. setting (section 5), where the model takes the query as input"; EXT-0210; columns per sub-benchmark Web/Code/Customized N@10, P@10, R@10, C@10, then Average N@10 and C@10). The table is legible (one label per row).

| Rank by Average N@10 | Model | Avg N@10 | Avg C@10 | Type |
|---|---|---|---|---|
| 1 | bge-reranker-v2-gemma | 35.51 | 34.14 | cross-encoder re-ranker |
| 2 | NV-Embed-v1 (spade) | 33.83 | 32.12 | dense, instruction-trained |
| 3 | jina-reranker-v2-base | 33.60 | 32.11 | re-ranker |
| 4 | gpt-3.5-turbo-1106 | 30.75 | 31.01 | LLM re-ranking |
| 5 | GritLM-7B (spade) | 30.02 | 29.44 | dense |
| 6 | gpt-3.5-turbo-0125 | 29.60 | 29.52 | LLM |
| 7 | bge-reranker-v2-m3 | 29.24 | 27.77 | re-ranker |
| 8 | gte-Qwen2-1.5B-inst. (spade) | 28.96 | 26.04 | dense |
| 9 | monot5-base-msmarco | 28.92 | 28.09 | re-ranker |
| 10 | Mixtral-8x22B | 28.80 | 30.35 | LLM |
| 11 | e5-mistral-7b (spade) | 26.06 | 25.80 | dense |
| 12 | mxbai-rerank-large-v1 | 24.84 | 25.88 | re-ranker |
| 13 | bge-large-en-v1.5 | 23.02 | 22.85 | dense |
| 14 | gtr-t5-large | 22.34 | 22.09 | dense |
| 15 | BM25s | 22.32 | 22.19 | lexical |
| 16 | bge-base-en-v1.5 | 22.09 | 21.27 | dense |
| 17 | gte-base-en-v1.5 | 20.86 | 21.60 | dense |
| 18 | e5-large-v2 | 20.83 | 20.05 | dense |
| 19 | e5-small-v2 | 19.99 | 18.36 | dense |
| 20 | gte-large-en-v1.5 | 19.90 | 19.50 | dense |
| 21 | Colbert | 19.46 | 18.69 | late interaction |
| 22 | COLT | 19.25 | 20.32 | trained on tool retrieval |
| 23 | gtr-t5-base | 19.10 | 19.87 | dense |
| 24 | e5-base-v2 | 18.95 | 18.54 | dense |
| 25 | contriever-msmarco | 17.81 | 16.91 | dense |
| 26 | all-MiniLM-L6-v2 | 16.30 | 16.17 | dense |

("spade" marks the instruction-pretrained models, printed with a spade symbol in the source.) Ranking is mine from the printed averages; ties and rounding are as printed.

Answers:
- [F] Dense/embedding retrievers with higher Average N@10 than gtr-t5-large (22.34 N@10, 22.09 C@10): bge-large-en-v1.5 (23.02, 22.85), NV-Embed-v1 (33.83, 32.12), GritLM-7B (30.02, 29.44), gte-Qwen2-1.5B-inst. (28.96, 26.04), e5-mistral-7b (26.06, 25.80). The last four are the instruction-pretrained models; bge-large is the only non-instruction dense retriever above it, by 0.68 N@10.
- [F] BM25s is 15th of 26 by Average N@10 (22.32, C@10 22.19), 0.02 below gtr-t5-large and above 11 rows, including Colbert, COLT, contriever-msmarco, gtr-t5-base, all e5 base/small/large, gte-large and gte-base, bge-base. 14 rows rank above it: 6 dense/embedding models (NV-Embed-v1, GritLM-7B, gte-Qwen2-1.5B, e5-mistral-7b, bge-large, gtr-t5-large) and 8 re-ranker or LLM rows (which re-rank NV-Embed-v1's output).
- [F] The text says "retrieval methods that demonstrate strong performance in conventional information retrieval (IR) tasks, such as ColBERT, even underperform compared to simple lexical-based matching approaches like BM25"; Table 4 agrees (Colbert 19.46 and contriever-msmarco 17.81 below BM25s 22.32), but gtr-t5-large and bge-large are at or above BM25s.
- [F] Re-rankers and LLM rows take NV-Embed-v1's retrieved tools as input ("Initial tools for LLM agent and Re-ranking baselines are retrieved by Nv-embedd-v1 model"), so they are not independent retrievers. [F] Text: MonoT5 re-ranking lowers N@10 from 33.83 to 28.92 (matches the NV-Embed-v1 and monot5 rows); "all retrievers in our experiments achieve less than 35% in Completeness@10": Table 4 max Average C@10 is 34.14 (bge-reranker-v2-gemma); the text cites "Table 9", not Table 4.
- [O] Table 5 (w/ inst., same lines) cannot be ranked by row: row labels are detached from the data rows (the labels BM25s, COLT are printed in the header block, labels are printed on separate lines from numbers, and the final three rows are unlabelled). Best printed Average N@10 values there are 47.52 and 47.17; which models these belong to is not reliable from the text. A page image of that table would be needed.
- [F] Text for the instruction setting: "all the IR model achieves better performance when an additional instruction is paired with the query".

Row verdict AS-01/AS-03: ANSWERED for Table 4; Table 5 CANNOT DETERMINE from the stored text.

## Ranges not read

- `ch-s2-0218-2505-18135-20261012` lines 470-1265 (rest of Section 3 per-model tables, appendices A-E).
- `r3-toolret` lines 520-1823 (Table 9 re-ranking results and appendices).
- `dmcp` files not in the assignment (ablation-py, attribution-py, discovery-registry-py, llm-py, pools-py in full, pricing-py, sampling-py, recorder.py which is not stored).

## Conflicts with the lead's wording

- The brief says "dense/embedding retriever stronger than gtr-t5-large": there are five (see above), but four of them are instruction-pretrained models of 1.5-7B parameters; only bge-large is a comparable-size model.
- `reference_specs` is not "built" anywhere in cli.py; it is the second argument of `pool_to_tool_surface`, and cli.py passes `ref.tool_specs`.
