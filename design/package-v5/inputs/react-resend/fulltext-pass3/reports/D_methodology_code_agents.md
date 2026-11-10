# Group D full-text verification (2026-11-09)

Labels: [F] stated in the paper, [O] observed by me in text/tables, [I] my interpretation or computation, [U] unknown. Line numbers refer to `tmp/fulltext/<id>/paper.txt`. Web search found no replication or critique of 2602.07150 and no explanation of the Exgentic AppWorld collapse. The Pydantic article was read through WebFetch's summariser (second-hand).

## 1. 2602.07150 On Randomness in Agentic Evals (ICLR 2026 workshop, KTH)
1. **Design.** 3 models (Qwen3-32B, DeepSWE-preview, Devstral-2-123B) x 2 scaffolds x 2 temperature settings (0 and vendor default) = 12 rows; 10 runs each of SWE-Bench-Verified (N=500); 12x10x500 = 60,000 trajectories (Table 1, l.278). Qwen/DeepSWE on local vLLM, Devstral via Mistral API.
2. **Metrics.** Resolution rate per run, pass@k, pass^k. No dollars, no billing, no caching (tokens only as volume, 25.58B).
3. **Statistics.** Table 1: mean/SD/min/max of the 10 run-level rates. Table 2 (l.582): z-based two-sample power calculation using the SD of the run-level benchmark rate (0.7/1.5/1.8 = min/median/max observed). Shapiro-Wilk 11 of 12 pass.
4. **Headline.** Run min-max range 2.2-6.0 pp; SD 0.7-1.8 pp; pass@5 minus pass@1 up to 24.9 pp; trajectories diverge at median token 5-56.
5. **Limitations.** One benchmark, open-weight models, coding. Power analysis varies run seed only, tasks fixed, so it ignores task-sampling variance. No clustering, no cost.
6. **Statements.**
 - "2.2-6.0 pp depending on which run": ACCURATE (l.~298). It is a range of 10 draws, so it grows with run count; SD is the better summary.
 - "SD above 1.5 pts even at temperature 0": OVERSTATED. Abstract says "exceeding 1.5"; Table 1 t=0 SDs are 1.2, 1.8, 1.0, 1.5, 1.6, 1.7: three exceed 1.5, one equals, two are below. Correct form: "1.0-1.8 pp at t=0, not lower than at default temperature" (l.309).
 - "60,000 trajectories, 3 models, 2 scaffolds, SWE-Bench-Verified; recommends multiple runs and power analysis": ACCURATE.
 - Derived claim "at SD 1.5, 2 pt needs ~9 runs, 1 pt ~36": the paper itself says it, not a derivation by the earlier researcher (Section 3.2, l.633: "Detecting a 2% improvement at p < 0.05 with 80% power requires approximately 9 runs per agent under test, while detecting a 1% improvement requires 36 runs"; Table 2). I reproduce 8.83 and 35.3. Precisions: "per agent" = per arm; SD is the SD of the whole-benchmark resolution rate across runs (N=500), not per-task; conditional on the fixed task set.
7. **Generalisation [I].** The SD does not transfer; it scales with 1/sqrt(N). From the thesis's identical-run disagreement d = 6/9/12 of 57 the per-run SD of the pass rate is sqrt(d/2)/57 = 3.0/3.7/4.3 pp. With the paper's formula, runs per arm for 80% power, alpha 0.05, tasks fixed:

| true difference | d=6 | d=9 | d=12 |
|---|---|---|---|
| 2 pp | 36 | 54 | 73 |
| 5 pp | 6 | 9 | 12 |
| 8 pp | 2.3 | 3.4 | 4.5 |
| 10 pp | 1.4 | 2.2 | 2.9 |

So with 1-2 runs only differences of about 10 pp or more are detectable, before task-sampling variance.

## 2. 2411.00640 Miller, Adding Error Bars to Evals
1. Design: statistical note, fictional data plus one real table (Anthropic models on DROP, RACE-H, MGSM). 2. Accuracy only; no cost. 3. CLT SE, clustered SE (Eq. 4), resampling K answers per question, paired SE (Eq. 7-8, clustered version), sample-size/MDE (Eq. 9-10).
4. Headline: Table 4 (l.169) clustered/naive SE ratio 3.05 (DROP, 588 clusters, 9,622 questions), 1.10 (RACE-H), 1.88 (MGSM); paired differences are "a free reduction in estimator variance" (l.377-378); K=1 to 10 answers lowers MDE 13.2% to 7.5% (l.473).
5. Limitations: asymptotic; needs many clusters; real clusters large (DROP about 16 questions/passage).
6. "Clustered SEs can be over 3x naive": ACCURATE but selective (one of three evals; others 1.1x, 1.9x). "Paired differences recommended": ACCURATE.
7. [I] With clusters of 3 the inflation is at most about sqrt(3) = 1.7x (perfect within-cluster correlation). Repeats K shrink only the within-question variance term, not question-sampling variance, which dominates at 57 tasks.

## 3. 2503.01747 Bowyer et al. (ICML 2025 position paper)
1. Simulation of coverage/width for CLT, bootstrap, Wilson, Clopper-Pearson (CP), Bayesian intervals: single model, clustered questions, paired comparison, F1; synthetic truth (generative model Eq. 8) plus an N=20 tool-use illustration. 2. Accuracy only. 3. Coverage vs nominal.
4. Headline: 95% CLT interval has 92.5% coverage at N=100 (l.~302); bootstrap also under-covers (Table 1, l.596); clustered: "neither simple CLT nor clustered CLT intervals produce correct coverage" in small data (Fig. 3 caption, l.297-299); paired: non-Bayesian methods severely under-cover (Fig. 5, l.458).
5. Limitations: position paper on simulated data; uniform priors; repeated runs not modelled.
6. Statement: MOSTLY ACCURATE; "exact" is OVERSTATED. They prefer Wilson (approximate) or Bayesian beta-Bernoulli and call CP, the exact interval, "overly conservative (too wide)"; "We would, therefore, recommend using WS or Bayesian intervals" (l.331); for paired data, paired Bayes.
7. [I] 19 clusters is exactly the regime where the clustered-CLT SE is unreliable; use a cluster-level exact/randomisation or Bayesian analysis as a cross-check.

## 4. Computation for the thesis design [I; my simulation, not from the papers]
Design: 19 scenarios x 3 tasks; net +5 passes of 57 in one paired run, 9-13 discordant tasks.

| split (b,c) | McNemar exact p | exact CP CI -> net passes (conditional on discordants) | cluster bootstrap, discordants random | cluster bootstrap, discordants concentrated in scenarios | exact cluster sign-flip p (random / concentrated) |
|---|---|---|---|---|---|
| 7,2 | 0.18 | -1.8 to +8.5 | 0 to +10 | -2 to +14 | 0.13 / 0.50 |
| 8,3 | 0.23 | -2.4 to +9.7 | -1 to +11 | -3 to +15 | 0.23 / 0.38 |

+5 of 57 (8.8 pp) is consistent with zero under every method; sensible interval about -2 to +11 passes (-4 to +19 pp), wider if flips cluster in scenarios (concentrated placement is my adverse assumption; the real pattern is [U]).

Generative simulation: task logit = 0.4 + scenario effect (SD 1.0) + task effect (SD 3.5, calibrated so identical runs disagree on about 11/57) + arm-by-task interaction (SD 0.7); K runs per arm; paired per-task mean; cluster-bootstrap CI; 250 studies per cell.

| K runs/arm | 95% half-width | power at true +5 pp | +10 pp | +18 pp | false positives |
|---|---|---|---|---|---|
| 1 | 11.0 pp | 12% | 37% | 86% | 7% |
| 2 | 8.1 pp | 18% | 58% | 98% | 3% |
| 4 | 5.9 pp | 32% | 84% | 100% | 6% |

With 2 runs x 57 tasks the half-width is about 8 pp (+-4.6 passes); 80% power needs roughly 13-14 pp at K=2 or about 9 pp at K=4. Half-width scales as 1/sqrt(scenarios): +-3 pp at K=2 needs about 130 scenarios (about 400 tasks). All depend on my assumed variance split; indicative only.

## 5. 2512.06710 Mustahsan et al., ICC (v1; you.com)
1. Design: GAIA validation set (165 questions; Levels 1/2/3 = 53/86/26) with GPT-4o-search and GPT-5-search, 64 trials per question; FRAMES with 50 of 824 questions (l.447); other models in appendix with fewer trials; timeouts (120 s) scored incorrect. 2. Accuracy and ICC(1,1); no cost or caching. 3. Bootstrap/Wilson CIs, Bonett SE of ICC.
4. Headline: ICC GAIA 0.304-0.774, FRAMES 0.4955-0.7118. Convergence table (l.288-300): ICC at n=2,...,64 trials, e.g. Level 1 GPT-4o 0.648, 0.614, 0.587, 0.574, 0.567, 0.561; Level 3 GPT-4o 0.428 ... 0.304. Text (l.304): "Convergence occurs by n of about 8-16 for Levels 1-2 and by n of about 32 for Level 3".
5. Limitations (l.436-452): mainly OpenAI models, 50 FRAMES questions. [O] Convergence judged by eye against the 64-trial value.
6. Statement ACCURATE as abstract reading but MISLEADING: "trials" are repeated attempts per question; "structured" = GAIA Levels 1-2/FRAMES, "complex" = GAIA Level 3 (26 questions); it is how many trials make the ICC estimate (a reliability ratio) stabilise, not how many runs are needed to detect an accuracy difference. Tasks are web-search QA, not stateful environments.
7. [I] ICC is a useful diagnostic for the thesis noise floor; it gives no run budget for arm comparisons.

## 6. 2510.11977 HAL (ICLR 2026)
1. Design: 21,730 rollouts, 9 benchmarks, 142 combinations from 186 runs (A4.1), about $40K. 2. Dollars computed from logged tokens times a price table; tokens separate (Fig. A2). No billing data. 3. Mostly single runs (A3 item 1, l.1446-1448: "we were forced to rely on single runs without statistical validation for most evaluations").
6. Statements (all are the authors' own statements):
 - Price table fixed at 2025-09-24: ACCURATE (l.344-345; Table A11 l.2351; DeepSeek-R1 priced from Together.ai).
 - Token vs dollar Pareto differ: ACCURATE (l.558-561): Opus 4.1 on the token frontier in 3 of 8 benchmarks, on the dollar frontier once; attributed to price volatility.
 - "21 of 36 equal or lower accuracy with higher reasoning effort": ACCURATE as quoted (l.565-567) but [I] counts single runs on small benchmarks (e.g. SWE-bench Verified Mini, 50 tasks), includes ties, and HAL's own A3 item 1 undercuts it.
 - Incomplete caching accounting: ACCURATE (A4.1, l.1513-1515): only SWE-Agent "uses caching", costs "report full token prices instead"; other scaffolds not described [U].
 - OpenRouter quantisations: ACCURATE (l.260-261; A3 item 4, l.1466-1469) but stated as a risk ("could serve ... FP4 for one call and FP8 for another"), not measured.

## 7. 2605.19537 Pape et al., Silent Hyperparameter (NeurIPS 2026)
1. Design: 5 engines (vLLM, SGLang, llama.cpp, LMDeploy, Ollama) vs transformers; 5 open models 4B-30B; GPQA, GSM8K, SimpleQA, LiveCodeBench, FP16 greedy; plus a literature survey. 2. Accuracy, disagreement, length error; single-turn, no tools, no dollars.
4. Headline (Table 1, l.300-330): R1-Distill-Qwen-7B GSM8K: transformers 78.47, llama.cpp 78.24, LMDeploy 73.54, Ollama 61.87, SGLang 78.24, vLLM 78.32; max-min 16.60 (l.242).
6. "Up to 16.6 points": ACCURATE for one model-benchmark cell. "with prefix caching among the causes": OVERSTATED. The authors attribute much of the large gaps to "correctable systematic defaults": Ollama's default repetition penalty 1.1 ("raises GSM8K accuracy by 11.67 points", l.378-381) and BOS-token handling. Prefix caching is under "optimization-induced numerical variance" (l.391-394): "negligible effects to several percentage points", mixed sign (GPQA +3.54 Ollama, -0.51 llama.cpp); "no individual numerical optimization that consistently increases or decreases performance". Ordering preserved in 19 of 20 pairs (l.245).
7. [I] Serving stack perturbs outputs by about the run-to-run noise scale; caching does not systematically bias accuracy; nothing about billing. Supports recording provider/quantisation/caching in each arm's definition.

## 8. 2602.22953 Exgentic / General Agent Evaluation (v2, May 2026)
1. **Design.** 5 architectures (ReAct, ReAct Short, Smolagent, OpenAI Solo+MCP, Claude Code) x 5 models (Opus 4.5, Gemini 3, GPT 5.2, DeepSeek-V3.2, Kimi-K2.5) x 6 benchmarks; 100 random instances each (50 tau2-Airline); about $20K; provider-default sampling, max 100 turns (Table 26, l.2324); open models on Azure Foundry, thinking enabled (Table 27). One run per cell (Table 25, l.2128: "#runs" collapsed to one row).
2. **Metrics.** Binary success. "Cost per Task ... using LiteLLM's pricing data" (l.334-335); Table 2 cost is bench-weighted across the six benchmarks (Table 10); per-benchmark cost is not in the paper (only in the release's `audit_cost.py`, l.2425). Cache accounting: NOT FOUND IN TEXT ("caching" appears only as an orchestrator feature, l.992).
3. **Statistics.** Per-cell Wilson CIs +-7-13 pp (Table 2 caption l.121); paired t, McNemar, eta-squared over 15 closed-model configurations. No repeats, so no run-to-run estimate.
4. **Assessment checks.** All Table 2 AppWorld values ACCURATE: Opus Smolagent 0.70, ReAct 0.61, Short 0.64, OpenAI Solo 0.68, Claude Code 0.66; Gemini 0.13/0.50/0.55/0.57; GPT 5.2 ReAct 0.00, Short 0.22 (Claude Code and Solo also 0.00); DeepSeek max 0.13; Kimi max 0.11. "100 test_normal tasks": PARTLY; the text says "100 randomly sampled instances"; the name test_normal appears only in a loader note about a deprecated "appworld_test_normal_old" subset (l.2393) [U]. "0.5% vs 27.8%": ACCURATE but closed-source only ("a closed-source statistic", l.~418); with the open models architecture is detectable (F(4,136)=3.82, p=0.006); interaction 5.4%. "Cost per configuration average over benchmarks; caching not described; one run": ACCURATE.
5. **Why open-weight models score near zero on AppWorld.** Not diagnosed. The only statement: "a capability ceiling for tool-rich autonomous interaction over ~468 actions" (l.500-503). For tau2 they give a mechanism (94% of Kimi sessions on autonomous architectures take zero steps, a first-turn protocol violation); for AppWorld there is no tool-call failure, timeout or turn-cap rate. [O] Each of about 468 AppWorld APIs is a separate tool/function (l.926-930), even for Smolagent; failed ReAct runs use 111% more steps than successes (Table 14). Capability, schema overload, call formatting and turn exhaustion cannot be separated [U].
6. **How shortlisting works** (l.1087-1112): per turn, if more than k=30 actions, the same backbone LLM is given the full catalog as text plus history as text and returns 30 tool names as JSON; only those go to the main call. Table 12 (l.1785): AppWorld delta Opus +3, Gemini +5, GPT 5.2 +22 (128-tool API cap), DeepSeek -5, Kimi +1 pp; all but GPT 5.2 inside one Wilson half-width. Cost delta per task Opus -$1.97 (5.75 to 3.78), GPT 5.2 +$0.09. [O] ReAct and ReAct Short are identical on all non-AppWorld columns (e.g. Opus BC+ 0.49/0.49, SWE 0.61/0.61), so those cells are shared rows, not independent runs, and the 0.5% architecture figure double-counts them. [I] The delta is bench-weighted, so AppWorld alone is about four times larger (about -$8 per task) and net of the shortlisting calls; cache awareness unknown. This is the one datum directly useful for the thesis (pruning offered tools cut the Opus bill by about a third at accuracy equal within noise) but it is one run, one model.
7. **Harness sensitivity vs the official AppWorld agents [I].** The thesis agents (AppWorld's simplified code-in-interpreter agents; MiniMax-M3 about 80%) differ from Exgentic's setting (hundreds of function schemas, provider endpoints, thinking on). Its best open model is 0.13 and best closed code-action model 0.70, so the harness plausibly explains much of the gap, but there is no ablation. The paper is inconsistent: Section 3.1 (l.291-294) "adopts the native interpreter-based interaction protocol", the appendix makes each API a protocol action [O]. Table 25 lists ReAct/Opus BC+ as 0 completed while Table 2 shows 0.49 [U].

## 9. 2609.11999 Is Bash All You Need? (Microsoft; Sept 2026)
1. **Design.** 5 interfaces (Tool-only, Bash+Tool, Bash, Bash+Synthesis, PTC) x Opus-4.8 and GPT-5.5 x TheAgentCompany (174 tasks, 60 typed tools built by the authors, GPT-5 coworkers) and APEX-Agents (480 tasks, 20 tools, LLM judge). PTC is the authors' own restricted-Python runtime, not the vendor API feature.
2. **Metrics.** Score and pass rate; tokens (input including cache-read, cache-read, output); "$/task: mean estimated inference cost at GitHub Copilot list rates" (Table 1 caption l.139-141). So dollars are computed list-price estimates, cache-read tokens counted inside input and shown separately; whether they are priced at the cache rate is not stated [U].
3. **Statistics.** 95% bootstrap CIs over tasks; paired differences by task; no cluster handling; no repeat statement; no limitations section found by grep [O].
4. **Headline (Table 1).** TAC Opus: Tool-only 44.9 / $1.20 / 945k tokens, Bash 69.4 / $0.37 / 264k, PTC 52.9 / $0.64 / 406k; TAC GPT-5.5: 45.3 / $0.66, 67.1 / $0.56, 45.1 / $0.54; APEX scores 37.8-48.5 with PTC $0.48-0.61 vs Tool-only $0.52-0.73. Tool-call success (Table 2): PTC 65.2% on TAC (others 91.5-93.3%), 86.2% on APEX. Table 6: PTC removes 97.6k uncached and 86.8k cache-read tokens per TAC task vs Tool-only.
6. Statement: ACCURATE with precisions. 52.9/45.1 vs 69.4/67.1 are TAC only (APEX gaps 8.4, 6.8 pp). 65.2% is TAC only and "success" is calls reporting success inside generated programs, not comparable across interfaces. Relevant "typed tools" comparison is PTC vs Tool-only: score equal or slightly lower except TAC/Opus (+8 pp); cost lower by 2% (APEX GPT) to 47% (TAC Opus). PTC vs Bash conflates catalog restriction with shell access.
7. [I] The best dollar and cache-token data in this set, but single runs, list prices, bespoke PTC, LLM judge.

## 10. 2608.06370 The Bitter Lesson of Tool Calling (PwC)
1. **Design.** 309-entry BFCL v4 subset, 14 models, JSON vs PTC (typed Python stubs that echo arguments, run in a subprocess, "no additional inference turns"), three ablations with n=31-52 (chaining, fan-out 7-48, context rot with 128 schemas). Temperature 0.
2. **Metrics.** Exact match of emitted calls. Some token counts; no dollars, no caching.
3. **Statistics.** Wilson CIs; authors say individual model results are "directional" and make "no claim that any individual model result is statistically significant" (l.255-262).
4. **Headline.** Table 2 (l.225-244): PTC >= JSON by point estimate in 11 of 14 models; GPT-4o 81.9 to 55.0, GPT-4.1 81.9 to 62.1, GPT-5.4-mini 79.3 to 55.0 (a "\n" escaping failure); CI half-widths 3.7-5.5 pp. Appendix Table 6: macro-average JSON 78.6 vs PTC 77.0. Equal LLM calls by design (l.146). Fan-out token crossover at N about 26 (l.338): N=30 3,559 JSON vs 3,380 PTC; N=48 5,097 vs 3,535. Limitation 4: PTC has a fixed prompt overhead, 1.5x input tokens on chaining; output tokens same.
6. "11 of 14": ACCURATE as point estimates but OVERSTATED as "at least as good": no model difference is individually significant, the mean is lower for PTC, ties are included. "1.5x input on chaining": ACCURATE. "Crossover near 26": ACCURATE, but N is parallel calls in a synthetic enumeration task, not calls in an agent run. "Same LLM-call count": ACCURATE, and in tension with the paper's explanation of the chaining gain as "the extra inference turn JSON incurs per link" [O]. "Echo stubs": ACCURATE (Limitation 1: "argument serialization accuracy, not end-to-end tool-use correctness"). No evidence about the bill.

## 11. Pydantic article "Why code mode is the future" (vendor blog; via summariser)
Author is at Pydantic (commercial interest). 5,276 runs = 3,500 + 576 + 1,200 across three tiers; 8 models, 5 small CRUD apps with single-item tools. Long tier (12 tests): cost -58%, success +16.0 pp (failed runs 67/288 to 21). N=5 small tasks: +21%, +35%, +38% cost on 3 of 5. Everyday tier -16% cost, +1.6 pp ("noise"). Cost from `genai-prices` list prices, caching not mentioned [U]. Bootstrap over tests, 3-4 repeats, 24 runs per arm per N, 5 of 25 gaps clear zero; "the benchmark code isn't public". Assessment ACCURATE against the fetch; strength low (12 long tests pooled over eight models, vendor, unreproducible; 50 x 4 x 8 x 2 = 3,200, not 3,500 [U]). Hypothesis only.

## 12. Cross-questions
**(a) Runs and tasks for "accuracy nearly the same".** That claim needs a margin m and an interval inside +-m. No margin is set (standing decision), so the defensible statement now is estimation: paired, cluster-aware difference with interval, reported beside the identical-arm disagreement (6-12 of 57). From section 4, at 57 tasks / 19 clusters / K=2 the half-width is about 8 pp: it can exclude losses larger than about 8-12 pp and cannot support "nearly the same" for m below about 8 pp. K=4 gives about 6 pp. m = 3 pp would need about 130 scenarios at K=2 (or about 56 scenarios at K=4, the size of a 168-task split [I]). Wording: "no difference detected; interval -x to +y pp; accuracy loss up to y pp not excluded".
**(b) Are code-vs-function-calling comparisons valid evidence about the BILL?** Mostly no: 2608.06370 has no cost and equal LLM calls with echo stubs; 2609.11999 has list-rate dollars from single runs with a bespoke PTC and LLM judge; Exgentic has bench-averaged LiteLLM dollars, one run, and only one controlled ablation; Pydantic is a vendor blog; HAL ignores caching. They agree on a mechanism (programs return selected data, shrinking re-sent context) and on a call-count break-even, but none measures a billed amount under caching or shows run-to-run noise.
**(c) Cache-aware cost?** HAL no (authors state it). Exgentic not described. 2609.11999 partly: cache-read tokens reported, pricing of them unstated, list rates. 2608.06370 no cost. Pydantic not stated. 2605.19537 not about billing. None is a billed-dollar anchor.

## 13. Changes to recommendations
Rescale the 9/36-run figures to N=57 (SD 3-4 pp) and attribute them to the paper; write "SD 1.0-1.8 pp at t=0"; quote Miller as "up to 3.05x (1.1x, 1.9x elsewhere)"; recommend Wilson/Bayesian, not Clopper-Pearson; drop prefix caching from the 16.6-point claim; treat Exgentic as having no cache-aware or per-benchmark cost and its open-weight AppWorld collapse as harness evidence; compare PTC with Tool-only; treat the Pydantic article as an anecdote.

## 14. Verdict table
| paper | strength | one-sentence demonstration | assessment accuracy | consequence |
|---|---|---|---|---|
| 2602.07150 | medium | 10 runs x 12 SWE-Bench-V configs: run ranges 2.2-6.0 pp, SD 0.7-1.8 pp, also at t=0 | mostly accurate; "SD>1.5 at t=0" overstated; 9/36 are the paper's own | method yes, numbers rescale to N=57 (SD 3-4 pp) |
| 2411.00640 | high (method) | clustered SE up to 3.05x naive on DROP; paired cuts variance | accurate, selective | paired + cluster analysis; smaller inflation for clusters of 3 |
| 2503.01747 | medium-high (simulation) | CLT/bootstrap under-cover at small N; Wilson/Bayes fix it | mostly accurate; "exact" overstated | Wilson/Bayes; 19 clusters still fragile |
| 2512.06710 | low-medium | GAIA ICC estimates stabilise by 8-16 (L1-2) or 32 (L3) of 64 trials | accurate but misleading | not a run budget for comparisons |
| 2510.11977 | medium-high | dollar vs token Pareto differ; fixed Sept-2025 prices; caching missing; single runs | accurate, all authors' statements | cost-accounting caveats; 21/36 is noise-limited |
| 2605.19537 | medium | backend shifts single-turn scores up to 16.6 pp, mostly default parameters | 16.6 accurate; caching link overstated | record serving stack per arm |
| 2602.22953 | medium, 1 run/cell | 25 configs x 6 benchmarks: AppWorld extremely harness-dependent; shortlisting cut Opus cost by about a third | Table 2 accurate; 0.5/27.8 closed-only; no cache or per-benchmark cost | harness-sensitivity and shortlisting datum only |
| 2609.11999 | medium | PTC cuts tokens vs typed tools at similar score but trails bash | accurate with precisions | best dollar+cache data; single run, list price |
| 2608.06370 | low-medium | PTC >= JSON by point estimate in 11/14 models, echo stubs | mostly accurate; mean lower, no cost | no bill evidence |
| Pydantic | low (vendor) | long tasks -58% cost, +16 pp; small tasks +21-38% on 3 of 5 | accurate vs fetch | anecdote |

## 15. Could not verify
Exgentic: split name, open-weight failure cause, cache pricing, per-benchmark cost, Table 25 mismatch. 2609.11999: cache-read pricing, repeats. Pydantic: all numbers (summariser), caching. My simulations assume a logit-normal variance split; real flip clustering is unknown.
