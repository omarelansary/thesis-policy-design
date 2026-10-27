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
| V5-R02, never change `tools` in a session | vendor documentation | **Measured on one of three models** (section 7): on GLM-5.3 one added tool at the end of the list rewrote 65% of the prompt and an edit of the first tool rewrote 99%; gpt-oss and MiniMax-M3 kept almost all of their cache, which is unexplained until the third probe |
| Tool calling on these models | assumed | **Shown on gpt-oss-120b, MiniMax-M3 and GLM-5.3** (section 7): `auto`, `required` and a named tool all produced the right call; the models need no MCP server, only function definitions in the request |

## 5. What this reading does not show
Single runs, one prompt shape, one prefix length, one repeat, 16-token outputs. The cache behaviour of a returning user after a gap longer than the cache lifetime was not tested, and the lifetime is not known. Whether `cached_tokens` also appears for requests from other users with the same prefix (the 80 cached tokens on gpt-oss's first request hint at some shared prefix, which could also come from an earlier run) was not tested [U]. No accuracy was measured.

## 6. The second probe
`design/package-v5/tools/p0_api_probe_v2.py` was run by the human on 2026-10-27 (section 7).

## 7. The second probe: tool calling and a changed tools array (run 2026-10-27, 11:35-11:37 UTC)
Files (UTF-8 JSON, `max_tokens` 400, no key material, scanned): `inputs/p0-api-probe2-output.json` (gpt-oss-120b and MiniMax-M3, SHA-256 `a9934bea563b0dbc658d6ea9b1e4362fa6c67c639cda39baa1cd8352c5a0730a`) and `inputs/p0-api-probe2-glm-output.json` (GLM-5.3, `eb0a7fe2b2c2f4c34157bad8c3f2278aa0b6bf345ded228a2fa9fd8d187c1019`). Single runs at temperature 0. The script retries a rate-limited request after 65 s without recording the retry, so GLM-5.3 may have waited unseen.

**Tool calling works [O].** On all three models, asking "Call tool_07 now with note 'x'" produced a call to `tool_07` with the argument `{"note": "x"}` under `tool_choice` auto, `required` and a named function (nine of nine). The models need no MCP server: the request carries function definitions and our harness would be the client that runs them (the human's remark is right, and V5 does not depend on MCP).

**A request for a tool that does not exist [O], one run each:** gpt-oss-120b made no call and said the tool does not exist; MiniMax-M3 made no call, said so and listed the available tools; **GLM-5.3 called `tool_09`**, a wrong tool with a similar name, with the argument `{"note": "x"}`. This is the wrong-tool failure the earlier papers describe (FND-0016 and KAIST arXiv 2406.12307 in V4 `01` section 4), seen once; it is not a ranking of the models.

**The cache after the tools array changed [O]:**

| Model | Base prompt | Extra tool at the end of the list | First tool edited | Original request again |
|---|---|---|---|---|
| GLM-5.3 | 5,027 (4,928 cached) | **1,728 of 5,116 cached, 3,328 created** | **0 of 5,033 cached, 4,992 created** | 4,928 cached again |
| gpt-oss-120b | 4,479 (4,464 cached) | 4,528 of 4,541 cached | 4,480 of 4,485 cached | 4,464 cached |
| MiniMax-M3 | 5,359 (5,120 cached, 128 created) | 5,248 of 5,453 cached | 5,120 of 5,365 cached | 5,120 cached |

- **GLM-5.3 behaves like a plain prefix cache [O].** Its tools sit at the start of the prompt: the unchanged first 1,728 tokens (the 20 tools) were reused when a tool was added at the end of the list, and everything after was rewritten (3,328 tokens, 65% of the prompt); an edit of the first tool rewrote the whole prompt (99%). The original prompt was still cached afterwards. **This supports V5-R02 on this route: never change the tools array in a session.**
- **gpt-oss-120b and MiniMax-M3 are not explained [U].** After the same changes they reported 95-100% of the prompt cached. For gpt-oss, 4,528 cached tokens is **more than the 4,479 tokens of the original prompt**, which a plain prefix cache could only report if that exact variant had been sent before. Two explanations stand: (a) an earlier, unrecorded run of the same probe primed those variants (the transcript shows two runs but does not say whether the probe was run before); (b) these two deployments do not cache as a plain prefix. The third probe separates them (nonce-marked variants and edit positions). Until then, V5-R02 is measured on one model of three. (Update: the third probe, section 9, answers this for MiniMax-M3.)
- **The first request of the run was already cached on all three models [O]**, about 75 minutes after the first probe sent the same prefix (4,464, 5,120 and 4,928 tokens). If no other run intervened, **the cache lived at least about 75 minutes** on this route. The lifetime mode of the third probe tests longer gaps.
- **MiniMax-M3 re-creates a 128-token block on every request** (created 128 on all nine requests of the run, identical ones included). If a write carries a premium on this service, which it does not state, this model would pay it on every request.

## 8. What the two probes still do not show
No prices; no accuracy; one prompt shape; single runs; temperature 0. The returning-user gap beyond about 75 minutes was not tested. Whether MiniMax-M3.1-Flash honours `tool_choice` required (it did not in the first probe, at 16 tokens) was not re-tested. Which model to use is open: the data shows no model to exclude. The human prefers models other than gpt-oss-120b (REQ-U22-13), which the lead records as a lean, not a finding.

## 9. The third probe: nonce-marked variants (run by the human 2026-10-27, 16:43-17:08 UTC)
Files (UTF-8 JSON, no key material, scanned): `inputs/p0-api-probe3-output.json` (gpt-oss-120b and MiniMax-M3, SHA-256 `d3fcd7c336fe6b055726118d90b3c58be20b750c7c46e1ada8bfbbe89ca49baf`) and `inputs/p0-api-probe3-glm-output.json` (GLM-5.3, `7483f72e310022cf0d678b8e093f5a43447233f3d7f870591cc1cc9271dfb967`). Each changed variant carries a fresh random marker, so no earlier run can have cached it. The lead's earlier line "ready now: the third probe, which is human-run" was wrong: the human had already run it; the lead had not looked in the inputs folder (REQ-U22-17).

Cached tokens (of the prompt) per variant; the number of tokens rewritten is the prompt minus the cached part:

| Variant | GLM-5.3 (base 5,027) | MiniMax-M3 (base 5,359) | gpt-oss-120b (base 4,479) |
|---|---|---|---|
| V0 base, first request of the session | 4,928 cached | **0** cached | **64** cached |
| V1 tool added at the end of the list | 1,792 of 5,129 | 4,992 of 5,468 | 64 of 4,556 |
| V2 first tool edited | **0** of 5,040 | 3,200 of 5,374 | 64 of 4,494 |
| V3 tool_10 edited | 832 of 5,040 | 3,968 of 5,374 | 3,248 of 4,494 |
| V4 tool_20 edited | 1,664 of 5,040 | 4,992 of 5,374 | 3,808 of 4,494 |
| V5 marker at the end of the system prompt | 4,928 of 5,042 | 3,072 of 5,375 | 64 of 4,495 |
| V6 marker at the start of the system prompt | 1,792 of 5,041 | **0** of 5,375 | 64 of 4,495 |
| V7 base again | 4,928 | 5,120 | 4,464 |

- **GLM-5.3 and MiniMax-M3 behave as plain prefix caches [O].** A change invalidates everything after it, and the amount reused rises with the position of the change. GLM-5.3 reuses 1,792 tokens whenever only the system text changes (V6), which equals the whole tool block, so its template puts **the tools first, then the system text**; an edit of the first tool rewrote 99% of the prompt. MiniMax-M3 reuses 3,072 tokens when the system text's end changes (V5) and 3,200 when the first tool changes, so its template puts **the system text first, then the tools**; a change at the start of the system text rewrote everything. The order of the cached counts follows the position of the edit on both models.
- **gpt-oss-120b does not follow a plain prefix pattern [O, unexplained].** An edit of the first tool, a tool added at the end, and a change at the start or the end of the system prompt each reused only 64 tokens, although each shares at least 3,248 tokens with the base request that had just been cached; edits of the middle and last tool reused 3,248 and 3,808. The base request itself was fully reused later (V7, 4,464). The lead does not know why; requests reaching different servers behind the proxy, or a cache that stores only some prefixes, would produce this, but this is not shown by the data [U].
- **The earlier odd result is explained for MiniMax-M3 [I].** In the second probe the same edits left 95-100% of the prompt cached, which a cold plain prefix cache could not do (here the same kinds of edit lost 40-100%). That points to earlier unrecorded runs having primed those exact variants; the human can confirm.
- **Lifetime [O, if nobody touched the prefix in between].** The base prefix sent about 5 hours earlier was **gone** on gpt-oss-120b (64 cached) and MiniMax-M3 (0 cached), and **still cached** on GLM-5.3 after about 5.5 hours (4,928 cached). With the 75 minutes seen before, the lifetime is at least about 75 minutes everywhere, under 5 hours on two models and over 5.5 hours on one. A returning user after a few hours therefore meets a cold or a warm cache depending on the model.
- **What it means for V5 [I].** V5-R02 (never change the tools array in a session) is now supported on two models by controlled variants, with the cost of a change equal to everything after it. Where the tools sit in the prompt differs by model, so the safe rule does not depend on the layout: keep the system text and tools identical and put everything that changes (seeds, discoveries, memory) at the end, as V5-R06 already does.

## 10. What the three probes still do not show
No prices; no accuracy; one prompt shape; single runs. gpt-oss-120b's cache behaviour is unexplained. The lifetime needs a gap-run mode result (the third probe's `--mode lifetime`, not yet run). Whether `cached_tokens` is billed at a lower price on this service is not stated.
