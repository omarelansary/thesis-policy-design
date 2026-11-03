# RESULTS-R3 (describing agent, 2026-11-02): Part A of REQUEST-R3.md

Written for: the reader. Part A only; Part B (all tools / control / control repeated on one fixed OpenRouter provider, 57 tasks) is held until the human releases it and sets a spending limit, and has not been run. Counts, ids and provider names only; no AppWorld text; dev tasks only; keys read inside the running process from the adapter service `.env` and never printed or written (the files in this folder were scanned for paths and key patterns). OpenRouter spend in Part A: the probe in A3 reported $0.0076 in total over its replies; A1, A2 and A4 made no model call.

## A1. Fix-ups
**Which script wrote the pilot JSON.** The version that ran is the local `r2_pilot_compare.py` with sha256 `f6daa7dcd991c4bdc128a95a02753fe6aff7f741b213db1a3f85924b02ccf0b2`; it wrote `_ok_predictor_flag` into each run block (the set of values of "the first logged call of each task has no tools", i.e. whether a predictor call came first: `[False]` for `or_b2_pilot`, `[True]` for the other three). I removed that key from the JSON by hand before publishing and did not say so; that was my doing, not a second script. The published copy `r2_pilot_compare.py` (sha256 `d435313f5a8766236cc2a816bd5f634bec97663c596c4b57969cc3cf81234666`) is that version with the local path replaced by a placeholder and a note line added. I have now replaced `results/R2/r2-pilot-openrouter-2026-11-02.json` with the script's unedited output: sha256 before `443d1749da1aa1c51ae0a2b87b79764e04ee2536944be99c1478663e906060aa`, after `f9d75e3d96e53fe9fe7cd8ffa0f10caeea880db40dc9d23a4724cb54742a0a03`. The only difference between the two JSON files is the `_ok_predictor_flag` key in the four run blocks (checked key by key); every number is unchanged.

**Dev order.** `dev-order.json`: the 57 dev task ids in the order of `dev.txt` (ids only). The pilot subset is `dev[0::6]` = indices 0, 6, ..., 54, listed in the same file; the first task of each pilot run is `50e1ac9_1`.

**Retries in the pilot.** Counted as lines containing `RETRY_ERROR` in each run's console log (AppWorld's retry loop writes one such line per retried call; the 100 lines of the failed ScaDS smoke attempt were of this kind): `or-b2-pilot` 0, `or-ctrl-pilot` 0, and the one-task smoke run (`or-b2-smoke`) 0. So no LM call needed a retry that AppWorld's loop saw, and the most retries any call needed is 0, against the lowered limit of 20. Retries made inside the OpenAI client library (SDK default two) are not logged and not counted here.

## A2. OpenRouter endpoints for `minimax/minimax-m3`
Source: `https://openrouter.ai/api/v1/models/minimax/minimax-m3/endpoints` (public, no key), read 2026-11-02T20:48:52Z with `curl`; the response is saved unchanged as `r3-a2-openrouter-endpoints-2026-11-02.json`. Thirteen endpoints were listed (the field `status` is 0 for all). Prices are converted to dollars per million tokens. 'Used in pilot' is from the `provider` field of the logged replies (A4).

| provider (tag) | precision | context | max output | input / output / cache read / cache write ($ per million) | tools | tool_choice | seed | temperature | used in pilot |
|---|---|---|---|---|---|---|---|---|---|
| DeepInfra (`deepinfra/fp8/flex`) | fp8 | 524,288 | 131,072 | 0.224 / 0.88 / 0.0448 / not listed | yes | yes | yes | yes | no |
| CoreWeave (`coreweave/fp4`) | fp4 | 262,144 | 235,929 | 0.23 / 0.96 / 0.05 / not listed | yes | yes | yes | yes | control only (10 predictor calls) |
| GMICloud (`gmicloud/fp8`) | fp8 | 1,048,576 | 524,288 | 0.24 / 0.96 / 0.048 / not listed | yes | yes | yes | yes | both runs |
| DeepInfra (`deepinfra/fp8`) | fp8 | 524,288 | 131,072 | 0.28 / 1.1 / 0.056 / not listed | yes | yes | yes | yes | no |
| StreamLake (`streamlake/fp8`) | fp8 | 1,000,000 | 512,000 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | no | yes | both runs |
| Venice (`venice/fp8`) | fp8 | 524,288 | 65,536 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | no | yes | no |
| Together (`together`) | unknown | 524,288 | 471,859 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | no | yes | no |
| Parasail (`parasail/fp8`) | fp8 | 1,048,576 | 524,288 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | yes | yes | no |
| AtlasCloud (`atlas-cloud/fp8`) | fp8 | 524,300 | 524,288 | 0.3 / 1.2 / 0.06 / not listed | yes | no | no | yes | no |
| Novita (`novita/fp8`) | fp8 | 1,000,000 | 131,072 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | yes | yes | both runs |
| Minimax (`minimax`) | unknown | 524,288 | 512,000 | 0.3 / 1.2 / 0.06 / not listed | yes | yes | no | yes | both runs |
| ModelRun (`modelrun/fp8`) | fp8 | 1,048,576 | 943,718 | 0.3 / 1.3 / 0.05 / not listed | yes | yes | no | yes | no |
| Mara (`mara`) | unknown | 1,048,576 | 943,718 | 0.6 / 2.4 / not listed / not listed | yes | yes | no | yes | no |

## A3. Restriction probe, provider pinned
Command (local paths as placeholders; script `run_r3_a3.ps1`, sha256 of the version that ran `5993c83ff83b9ee2a954c998a2496c4b0688b6a3195c3ddc33b3e633a9038569`): `python <exchange>/prior-work/v5-probes/p2_tool_choice_probe_v3.py --base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --model minimax/minimax-m3 --repeat 3 --max-tokens 1024 --extra-body '{"provider":{"order":["gmicloud/fp8"],"allow_fallbacks":false}}' --out results/R3/r3-openrouter-gmicloud-2026-11-02.json` (the request asked also for `--pause 2`; **the run did not pass `--pause`**, the default 0 was used, and no rate-limit error occurred). Probe sha256 `5ec9ed7990b8a966470b05fcdafb63ff3d82f7cc2b9b3bd13144c51dac6601f9` (matches the request). Run 2026-11-02T20:49:41Z to 20:51:30Z. Provider chosen: **GMICloud** (`gmicloud/fp8`): the pilot used it, its listing has tools, tool_choice and seed, it states fp8 precision, and it lists the full 1,048,576-token context. The slug was accepted as written. Model id as served: `minimax/minimax-m3` on every reply; `system_fingerprint` absent on every reply.

| cell | status | provider as served | tool_07 | subset (tool_03/04/05) | other tool | no tool | prompt / cached / cache-write tokens per reply (3 replies) |
|---|---|---|---|---|---|---|---|
| C0 base | 200 x3 | GMICloud x3 | 3 | 0 | 0 | 0 | 4393/128/0; 4406/162/0; 4406/4405/0 |
| C1 base again | 200 x3 | GMICloud x3 | 3 | 0 | 0 | 0 | 4393/4352/0; 4393/4352/0; 4406/4405/0 |
| C2 allowed-chat | 200 x3 | GMICloud x3 | 3 | 0 | 0 | 0 | 4406/4405/0; 4393/4352/0; 4406/4405/0 |
| C3 allowed-flat | 200 x3 | GMICloud x3 | 3 | 0 | 0 | 0 | 4393/4352/0; 4406/4405/0; 4406/4405/0 |
| C4 allowed-required | 200 x3 | GMICloud x3 | 3 | 0 | 0 | 0 | 4393/4352/0; 4393/4352/0; 4406/4405/0 |
| C5 required | 404 x3 | None x3 | 0 | 0 | 0 | 0 | -; -; - |
| C6 named | 404 x3 | None x3 | 0 | 0 | 0 | 0 | -; -; - |
| C7 none | 404 x3 | None x3 | 0 | 0 | 0 | 0 | -; -; - |
| C8 instruction-only | 200 x3 | GMICloud x3 | 0 | 0 | 0 | 3 | 4428/162/0; 4428/4427/0; 4428/4427/0 |
| C9 responses-api | 200 x3 | None x3 | 0 | 0 | 0 | 3 | 2910/2490/None; 2897/2432/None; 2910/2909/None |

Notes (facts from the file): C9 (`/responses`) replies have no `provider` field in the recorded metadata; output item types per reply: message; message; message. Cache-write tokens are 0 wherever the endpoint reported them (C9: not reported).

**The 404 for C5 (`required`), C6 (named) and C7 (`none`)**: HTTP 404 on all 3 replies of each cell; no model reply, no usage. The recorded error text (first 400 characters, as the probe scrubs it) is for C5 `{"error":{"message":"No endpoints found for minimax/minimax-m3. Every candidate endpoint was removed during routing: Filter by Tier Endpoint Rows removed deepinfra/fp8/flex (Excluded tier endpoint rows the request did not opt into); Filter by Tool Compatibility removed gmicloud/fp8, deepinfra/fp8, streamlake/fp8, together, parasail/fp8, novita/fp8, minimax, modelrun/fp8, mara; Filter by Fallback r`; for C6 `{"error":{"message":"No endpoints found for minimax/minimax-m3. Every candidate endpoint was removed during routing: Filter by Tier Endpoint Rows removed deepinfra/fp8/flex (Excluded tier endpoint rows the request did not opt into); Filter by Tool Compatibility removed gmicloud/fp8, deepinfra/fp8, streamlake/fp8, parasail/fp8, novita/fp8, minimax, modelrun/fp8, mara; Filter by Fallback removed cor`; for C7 `{"error":{"message":"No endpoints found for minimax/minimax-m3. Every candidate endpoint was removed during routing: Filter by Tier Endpoint Rows removed deepinfra/fp8/flex (Excluded tier endpoint rows the request did not opt into); Filter by Tool Compatibility removed gmicloud/fp8, deepinfra/fp8, together, parasail/fp8, novita/fp8; Filter by Fallback removed coreweave/fp4, streamlake/fp8, venice/`. In all three the router's own message says every endpoint, GMICloud included, was removed by its "Tool Compatibility" filter for that value of `tool_choice`. This is a refusal by OpenRouter's router before any provider was called, not a reply by GMICloud; by the request's rule I record it and do not retry with another pin. The listing in A2 shows `tool_choice` as supported for GMICloud; what the router's filter tests is not recorded.

## A4. The pilot's bill, from the files on disk
Per call, in order (provider, prompt, cached, cache-write, completion tokens, reported cost) for every call of both runs: `r3-a4-pilot-bill-2026-11-02.json` (script `r3_a1_a4.py`, sha256 of the version that ran `cadf8dace012da0e8f103a84b0ae6794bc32880dbc12e25d8d2bab404b0bec84`). The totals below equal the R2 pilot table (130 and 110 calls; 11,899,694 and 1,357,750 prompt tokens; $0.9644 and $0.1979).

**`or-b2-pilot` (predictor off, 469 functions per call), totals per provider:**

| provider | calls | prompt | cached | cache-write | completion | cost ($) |
|---|---|---|---|---|---|---|
| Minimax | 45 | 4,478,125 | 4,348,032 | 0 | 41,782 | 0.3500 |
| GMICloud | 40 | 3,704,484 | 3,313,265 | 0 | 32,859 | 0.2845 |
| Novita | 25 | 2,006,121 | 1,892,132 | 0 | 10,517 | 0.1603 |
| StreamLake | 20 | 1,710,964 | 1,508,876 | 0 | 15,331 | 0.1696 |
| **total** | 130 | 11,899,694 | 11,062,305 | 0 | 100,489 | 0.9644 |

**`or-ctrl-pilot` (predictor on), totals per provider:**

| provider | calls | prompt | cached | cache-write | completion | cost ($) |
|---|---|---|---|---|---|---|
| GMICloud | 34 | 519,596 | 441,418 | 0 | 30,892 | 0.0696 |
| Novita | 25 | 381,827 | 307,094 | 0 | 19,732 | 0.0645 |
| Minimax | 24 | 190,008 | 172,032 | 0 | 5,381 | 0.0222 |
| StreamLake | 17 | 189,468 | 148,674 | 0 | 9,690 | 0.0328 |
| CoreWeave | 10 | 76,851 | 51,968 | 0 | 530 | 0.0088 |
| **total** | 110 | 1,357,750 | 1,121,186 | 0 | 66,225 | 0.1979 |

**Was the 469-function prefix warm at the first agent call of each task?** `or-b2-pilot`:

| task | first agent call: provider | cached / prompt tokens | last call of the previous task: provider |
|---|---|---|---|
| `50e1ac9_1` | Novita | 75630 / 75631 | (first task) |
| `530b157_1` | Minimax | 128 / 76095 | Novita |
| `b119b1f_1` | Minimax | 72832 / 76058 | Minimax |
| `0d8a4ee_1` | Novita | 128 / 75617 | Minimax |
| `3ab5b8b_1` | StreamLake | 182 / 75614 | Novita |
| `383cbac_1` | StreamLake | 128 / 75664 | StreamLake |
| `57c3486_1` | GMICloud | 157 / 78388 | StreamLake |
| `6bdbc26_1` | Novita | 72320 / 75603 | GMICloud |
| `6c2c621_1` | Novita | 72320 / 75634 | Novita |
| `4fab96f_1` | GMICloud | 128 / 76048 | GMICloud |

The first agent call had more than half of its prompt tokens cached in 4 of 10 tasks. The first task's call was warm because the one-task smoke run (`or-b2-smoke`, same 469 definitions, a few minutes earlier) had already sent the prefix, so it is not a cold start. The other warm calls (`b119b1f_1`, `6bdbc26_1`, `6c2c621_1`) hit about 72,300-72,800 of about 75,600-76,100 tokens; in the cold ones the cached count is 128-182 tokens, i.e. the shared start of the prompt only. Same provider as the previous task's last call (`b119b1f_1` Minimax, `383cbac_1` StreamLake, `6c2c621_1` Novita, `4fab96f_1` GMICloud): warm in 2 of these 4. Different provider: warm in 1 of 5 (`6bdbc26_1`). The cause is not recorded. For the control, the first agent call (after the predictor call) of each task:

| task | first agent call: provider | cached / prompt tokens | last call of the previous task: provider |
|---|---|---|---|
| `50e1ac9_1` | Novita | 243 / 5146 | (first task) |
| `530b157_1` | Minimax | 128 / 5214 | Novita |
| `b119b1f_1` | Minimax | 128 / 4584 | Minimax |
| `0d8a4ee_1` | Novita | 128 / 4547 | Minimax |
| `3ab5b8b_1` | StreamLake | 246 / 4677 | Novita |
| `383cbac_1` | StreamLake | 243 / 5163 | StreamLake |
| `57c3486_1` | GMICloud | 220 / 5080 | StreamLake |
| `6bdbc26_1` | Novita | 128 / 4161 | GMICloud |
| `6c2c621_1` | GMICloud | 220 / 5564 | Novita |
| `4fab96f_1` | GMICloud | 128 / 4600 | GMICloud |

(In the control the predictor call is the first call of each task and its prompt is different from the agent's; the table shows the first agent call. Cached counts there are 128-246 tokens of 4,161-5,564.) `cache_write_tokens` is 0 on every call of both runs.
