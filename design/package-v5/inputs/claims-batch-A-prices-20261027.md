# Batch A claims to check: primary price sources (thread T-20261027-119; leads from scout 1, not evidence)

Stored pages are in `evidence/literature-20261019/`, named `v5-lit-<name>-20261027.*` (html pages are `.txt`, raw pages `.md`/`.txt`; list them with the file tool). Earlier stored aggregator pages used by `design/package-v5/11-price-ranges.md`: `v5-aa-*-20261027.txt`, `v5-pricepertoken-gpt-oss-120b-20261027.txt`, `v5-puter-minimax-pricing-20261027.txt`, `v5-qubrid-qwen38-27b-pricing-20261027.txt`, `v5-eesel-glm53-flash-pricing-20261027.txt`. All prices USD per 1M tokens; r = cache-read / input; w = cache-write / input; o = output / input.

| # | Claim (scout 1) | Stored page |
|---|---|---|
| A1 | DeepSeek `deepseek-flash`: cache hit 0.003 off-peak and 0.006 peak; miss 0.15 and 0.30; output 0.60 and 1.20. `deepseek-v4-pro`: hit 0.022 and 0.044; miss 0.66 and 1.32; output 1.98 and 3.96. "Off-peak rates are half of the peak rates." No write or storage fee listed | v5-lit-deepseek-pricing |
| A2 | Z.ai GLM-5.3: input 1.4, cached 0.26, cached-input storage "Limited-time Free", output 4.4. GLM-5.3-Flash: 0.15, cached 0.03, storage limited-time free, output 0.50 | v5-lit-zai-pricing |
| A3 | Z.ai caching: implicit, no configuration, `usage.prompt_tokens_details.cached_tokens`; hits "usually 50% of standard price"; "reasonable time limits"; no minimum length or storage fee stated | v5-lit-zai-cache |
| A4 | MiniMax-M3 (input up to 512k): input 0.30, output 1.20, cache read 0.06; above 512k: 0.60, 2.40, 0.12; "Permanent 50% off"; "Cache write: Not listed" | v5-lit-minimax-pricing |
| A5 | MiniMax text caching: automatic; "512 or more input tokens"; M3 and M3.1-Flash supported; `cached_tokens` field; no write multiplier or expiry stated | v5-lit-minimax-caching |
| A6 | MiniMax Anthropic-compatible cache page: M2.7 cache read 0.06 and cache write 0.375 against input 0.30; explicit mode with a 5-minute lifetime; whether automatic mode charges a write fee | v5-lit-minimax-anthropic-cache |
| A7 | Alibaba Model Studio `qwen3.8-27b`: Singapore 0.5 input, 3 output; China (Beijing) 0.424 and 1.696; implicit-cache price not listed | v5-lit-alibaba-model-pricing (7,472 lines; search for the model name) |
| A8 | Alibaba context cache: explicit mode hit 10% of input, creation 125%, minimum 1,024 tokens, TTL 5 minutes (reset on hit); implicit mode hit 20%, creation 100%, minimum 1,024, TTL indeterminate; the two modes are mutually exclusive | v5-lit-alibaba-context-cache |
| A9 | Groq gpt-oss-120b: input 0.15, cached 0.075, output 0.60 | v5-lit-groq-gptoss120b |
| A10 | Groq caching: automatic, no extra fee, 50% discount on cached input, expires after 2 hours without use, minimum 128 to 1,024 tokens by model | v5-lit-groq-prompt-caching |
| A11 | Fireworks standard: gpt-oss-120b input 0.15, cached 0.015, output 0.60; GLM 5.3 1.40, 0.26, 4.40; MiniMax M3 0.30, 0.06, 1.20; Qwen 3.8 27B not listed | v5-lit-fireworks-pricing |
| A12 | Together: gpt-oss-120B 0.15, cached not listed, 0.60; GLM-5.3 1.40, 0.26, 4.40; GLM-5.3-Flash 0.15, 0.03, 0.50; MiniMax M3 0.30, 0.06, 1.20; MiniMax M3.1 Flash 0.15, 0.015, 0.60 | v5-lit-together-pricing and v5-lit-together-serverless-models |
| A13 | DeepInfra gpt-oss-120b: 0.037 input, 0.17 output, cached not listed. Baseten: input 0.10, output 0.50. Cerebras: input 0.35, output 0.75 | v5-lit-deepinfra-gptoss120b, v5-lit-baseten-gptoss120b, v5-lit-cerebras-gptoss |
| A14 | CoreWeave via W&B Inference: input 0.03, output 0.17, **no cached price listed** | v5-lit-wandb-coreweave-gptoss |
| A15 | Artificial Analysis caching page: GLM-5.3 hosts mostly 1.40 and 0.26 with no write fee; outliers Bitdeer 0.63 and 0.12, Makora 0.14 and 0.10, Multiverse 0.20 and 0.02, Supernova 2.80 and 0.52; "Alibaba Cloud (explicit cache): writes billed at 125% of standard input; hits at 10%" | v5-lit-aa-caching |

## Then check these statements of `design/package-v5/11-price-ranges.md` against the pages above
- Section 2: r range 0.14 to 1.0; w 1.0 to 1.25; o 3.1 to 7.5. Which official pages fall outside (scout 1 reports r of 0.02 to 0.10 at DeepSeek, Fireworks gpt-oss-120b, Together M3.1-Flash and Alibaba explicit; o of 2.14 at Cerebras; an o of 7.5 not found on any official page)?
- Section 2 and RC-1: the aggregator `v5-pricepertoken-gpt-oss-120b-20261027.txt` lists CoreWeave with a cache-read price equal to input (r = 1.0); A14 lists none. Do the official pages of the six hosts the document names as "r = 1.0" (CoreWeave, AkashML, Venice, DekaLLM, Crusoe, SambaNova) list a cache-read price at all? Only CoreWeave and Crusoe-like pages may be stored; say what is not stored.
- RC-5: Qwen3.8-27B at 0.72 / 4.31 / 0.14 (Qubrid) against A7.
- RC-6: "cache price not found" for GLM-5.3 against A2 and A11.
