# 10. P0 part 2: what the university API reports and honours (probe run by the human, 2026-10-27)

Status: provisional, lead, 2026-10-27. Nothing validated or final. Observations [O] are read from the six output files; interpretations [I] are marked. The probe (`design/package-v5/tools/p0_api_probe.py`, revision 1) sent five small requests per model through the human's key at `https://llm.scads.ai/v1`. The key never entered the workspace. Single runs only.

## 1. The files
Six files in `design/package-v5/inputs/`, one per model, run by the human on 2026-10-27 between 10:18 and 10:23 UTC. The human ran five further models after `gpt-oss-120b`, which was only the example in the script's usage line (the lead's choice, not a finding). **Format:** the files are UTF-16 (PowerShell's `>`), kept as written. **Redaction:** the GLM-5.3 file held LiteLLM's 64-character identifier of the key (a hash of the key, in three rate-limit messages); the lead replaced it with `<key-hash-redacted-by-lead>` before anything was committed. Hashes after redaction:

| File | Model | SHA-256 |
|---|---|---|
| `p0-api-probe-gptoss-output.txt` | openai/gpt-oss-120b | `4876c8fb7238ec725b12983f9b3d92ee3b8c7996efc2ff5675a98466ae5d0b3c` |
| `p0-api-probe-glm-output.txt` | zai-org/GLM-5.3 | `893999525f3873503a2d47d7f4ebe6fd16bae6f1e1f00e457d03c090da5f1b51` |
| `p0-api-probe-glmflash-output.txt` | zai-org/GLM-5.3-Flash | `fb5d339186e56808a0e605d0e91a24c323f63ebebdd4c7188310075a2a59b3c1` |
| `p0-api-probe-minimaxm3-output.txt` | MiniMaxAI/MiniMax-M3 | `30e44a1b571d3d8a07d4b5ec95b965cb6ee1071eca18a48214b06db1e1ecde90` |
| `p0-api-probe-minimaxm3-flash-output.txt` | MiniMaxAI/MiniMax-M3.1-Flash | `b86d00d00678bbf2928461d630f92083bb3dff7f86e8cfdde60b482ca3dfa03a` |
| `p0-api-probe-qwen27b-output.txt` | Qwen/Qwen3.8-27B | `b6ac3a9f089278e6a2adb7f2b4332c969c95c6399c268d6e7d5fc53c4e90049e` |

The `/models` endpoint answered HTTP 200 and listed 26 models in every file.

## 2. What the API reports (the cache terms of DPR-0006) [O]
Every successful response carries `prompt_tokens_details.cached_tokens` and `created_cache_tokens`, and `completion_tokens_details.reasoning_tokens`. The same 4,500-5,600-token request (20 tools plus a long system prompt, `max_tokens` 16) was sent twice:

| Model | Prompt tokens | Request 1: cached / created | Request 2 (identical): cached | Share of prompt cached on request 2 |
|---|---|---|---|---|
| gpt-oss-120b | 4,479 | 80 / 4,384 | 4,464 | 99.7% |
| GLM-5.3 | 5,027 | 0 / 4,992 | 4,928 (created 64) | 98.0% |
| MiniMax-M3.1-Flash | 5,377 | 0 / 5,376 | 5,248 (created 128) | 97.6% |
| MiniMax-M3 | 5,359 | 0 / 5,248 | 5,120 (created 128) | 95.5% |
| GLM-5.3-Flash | 5,027 | 0 / 3,456 | 3,456 | 68.7% |
| Qwen3.8-27B | 5,574 | 0 / 3,296 | 3,296 | 59.1% |

- **Prefix caching works and is reported on all six models** [O]. The cache counters are separate from fresh input, and a write counter exists. The falsifier of HYP-0020 (no separate cache-write and cache-read counts) did **not** occur.
- **Caching is partial and block-wise** [O]. The cached counts are multiples of a block (16 tokens for gpt-oss, 64 for GLM-5.3, 128 for MiniMax and GLM-Flash; Qwen's 3,296 is a multiple of 32), so a tail of the prefix is never cached. Two models cached only 59-69% of the same prompt; why is not shown [U].
- **A turn appended to the end kept the cache** [O]. On request 3 (the same prefix plus one more user turn), gpt-oss, MiniMax-M3, MiniMax-M3.1-Flash, GLM-5.3-Flash and Qwen all kept the cached prefix of request 2 and wrote only the new tail (gpt-oss: 4,464 cached, 32 created). This is the append-only behaviour V5-R02 relies on, now seen on this route. GLM-5.3 could not be tested here (below).
- **Reasoning tokens are inside the output count** [O]: in every response `reasoning_tokens` is at most `completion_tokens` (13 of 16, 16 of 16, 0 of 3). DPR-0006's rule that reasoning is priced inside output, never twice, holds on this route.
- **The first request is slower** [O, single runs, confounded by connection setup]: 0.7-5.3 s against 0.5-0.9 s for the cached repeat on every model.
- **Token counts differ by model for the same text** [O]: 4,479 (gpt-oss) to 5,574 (Qwen), a spread of about 24%, as DPR-0006 section 1 warns, so counts are compared only within a model.

## 3. What the API does not honour, or did not show [O]
- **`allowed_tools` is rejected** on every model that reached it (five): HTTP 400, "litellm.BadRequestError: Invalid tool choice ... Please ensure tool_choice follows the OpenAI spec". The service is a LiteLLM proxy. Only the Chat Completions shape (`{"type":"allowed_tools","allowed_tools":{"mode":"auto","tools":[{"type":"function","function":{"name":...}}]}}`) was tried; other shapes were not. So restriction at a fixed prefix by this parameter is **not available** here.
- **Rate limit** [O]: GLM-5.3 returned HTTP 429 on requests 3-5 ("model_per_key ... Limit type: requests. Current limit: 2", reset about a minute later). The other five models took all five requests. Any study on GLM-5.3 must space its requests.
- **Tool calling was not demonstrated on any model** [O]. With `max_tokens` 16, four models (gpt-oss, GLM-5.3-Flash, MiniMax-M3, Qwen) hit the limit (`finish_reason` "length", empty or blank text, 13 to 16 of the 16 tokens being reasoning), so `tool_choice: "required"` produced no call; GLM-5.3 was rate-limited before that request. **One model behaved differently:** MiniMax-M3.1-Flash (no reasoning tokens, `finish_reason` "stop") answered with the text "ready" and **no tool call** under `tool_choice: "required"`, so that parameter was ignored or dropped for it. This is one single-run observation.
- **Prices:** the API reports tokens only [O]. It has no bill, and the probe read none.

## 4. What this changes in V5 [I]
| V5 point | Before | After this reading |
|---|---|---|
| HYP-0020, the API exposes the cache terms | unknown | **Supported for the six models tested**: cached and created counts, reasoning inside output; prices still unknown (a price table is named by the human or taken from a hosted list price, DPR-0006 section 1) |
| Route of `04` section 5 | client-side route assumed | **Confirmed**: appends keep the cache; vendor offering mechanisms are not available; `allowed_tools` is rejected |
| HYP-0018, offering fewer tools at a fixed prefix | tested by `allowed_tools` or `tool_addition` | **Cannot be tested by `allowed_tools` here.** Left on this route: declare only the allowed tools (S1), append discovered or seeded tools, or restrict by instruction text with no enforcement; the instruction route is untested |
| The regime arithmetic (D-01) | read price assumed at 0.1 | The API reports reads and writes but states no prices; the cached share is 59-99.7% of a prefix, not 100%, so D-01's cached-prefix rows are best-case for the two partial-cache models |
| V5-R02, never change `tools` in a session | vendor documentation | **Not yet measured on this route**: the probe appended a turn but did not change the tools array; `p0_api_probe_v2.py` does (C3, C4) |
| Tool calling on these models | assumed | **Unshown**; the next probe tests it with `max_tokens` 400 |

## 5. What this reading does not show
Single runs, one prompt shape, one prefix length, one repeat, 16-token outputs. The cache behaviour of a returning user after a gap longer than the cache lifetime was not tested, and the lifetime is not known. Whether `cached_tokens` also appears for requests from other users with the same prefix (the 80 cached tokens on gpt-oss's first request hint at some shared prefix, which could also come from an earlier run) was not tested [U]. No accuracy was measured.

## 6. Next: the second probe
`design/package-v5/tools/p0_api_probe_v2.py` (the human runs it; output as UTF-8 JSON via `--out`): `max_tokens` 400; a changed tools array (one extra tool at the end, and an edited first tool) to see whether the cache survives; direct tool-call tests with `tool_choice` auto, required and named; a request for a tool that does not exist; a retry after a 429 and `--pause`. About ten requests per model. GLM-5.3 needs `--pause 35`.
