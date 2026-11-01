# Scout M report (thread T-20261101-127, TASK M: methods for choosing and using benchmarks)
Model output of a general-purpose scout at high effort, received by the lead 2026-11-01 from its hand-back. Sections 3 to 6 copied as delivered; section 1 (instruction files: CLAUDE.md and ops/STATE.md; read only the allowed files) and section 2 (compact cards of the methods sources, versions repeated in the claims) omitted by the lead. A lead, not evidence; only stored pages are cited.

Scout's tool note: WebFetch returns a model-written digest and caps verbatim quotes at about 125 characters; PDF URLs came back unreadable, so arXiv HTML pages were used where possible; "search summary" marks claims seen only in search results. About 50 searches and fetches.

## 3. Claims table
id | source (type; interest) | URL | version | quote and location | bears on | reading

M1 | Dehghani et al., "The Benchmark Lottery" (independent; Google researchers) | https://arxiv.org/abs/2107.07002 | Jul 2021 | search summary: "the relative performance of algorithms may be altered significantly simply by choosing different benchmark tasks" | methods | CONTEXT (PROBLEM for a free choice made after seeing results)
M2 | Perlitz et al., "Benchmark Agreement Testing Done Right" (independent; IBM) | https://arxiv.org/html/2407.13696v2 | v2 | §3.1 "The Choice of Reference Benchmark Matters": agreement "significantly vary across different appropriate reference benchmarks" | methods | CONTEXT
M3 | same | same | v2 | §4 "Use More Models and Sample Them Randomly" (at least 10 models); §1 "agreement over a few top-ranked models remains low" | E2E, methods | PROBLEM for agreement claims from 2-3 models
M4 | Siska et al. (independent) | https://aclanthology.org/2024.acl-long.560/ | ACL 2024 | Abstract: "accounting for correlations across test prompts can change model rankings on major benchmarks" | methods, E2E | PROBLEM for pooling that treats items as independent
M5 | search summary, a 2026 preprint on random effects treating each task as a study (not opened) | not stored | 2026 | I² of 91-95% in some domains | E2E | CONTEXT; no methods paper prescribing pooling for LLM benchmarks found
M6 | Hofman et al., "Pre-registration for Predictive Modeling" (independent) | https://arxiv.org/pdf/2311.18807 (search summary only) | 30 Nov 2023 | "Pre-specifying certain components of a learning pipeline alone is not necessarily enough to prevent overfitting"; participants "might have produced biased estimates of out-of-sample performance had they not adhered to the protocol" | methods | FIT for freezing a protocol, not a guarantee
M7 | Kapoor et al., "AI Agents That Matter" (authors; later built HAL) | https://arxiv.org/html/2407.01502v1 | v1 | §5: "many agent benchmarks do not include held-out test sets"; "including 7 that have no hold-out"; "We analyzed 17 agent benchmarks"; Table 1 holdout counts: distribution-specific 1/1, task-specific 3/6, domain-general 1/8, fully general 0/2 | methods, E2E | FIT for a held-out set disjoint from pilots
M8 | same | same | v1 | §5.1: "WebArena lacks a held-out test set for evaluating whether an agent can perform well on unseen web tasks" | methods | CONTEXT
M9 | Zhu et al., Agentic Benchmark Checklist (benchmark-design authors) | https://arxiv.org/html/2507.02825v5 | v5 | §4.1 T.4-T.6: "Relying on dynamic resources... is not recommended"; T.9 oracle solver; T.10 "Inspect outliers in pilot experiments" | all | FIT; live services a validity risk; oracle arm recommended
M10 | same | same | v5 | Abstract: "τ-bench counts empty responses as successful"; §5.2: 38% of airline and 6% of retail tasks intentionally unsolvable, a trivial agent scores 38% (digest) | P1, P3, E2E | PROBLEM for tau-bench as scorer; second source needed
M11 | same | same | v5 | §4.2 O.c.1: LLM-as-judge items require pilot-testing judge accuracy and self-consistency; O.g.1-3 state-modification checks | methods | FIT
M12 | same | same | v5 | §4.3 R.10 "measures of statistical significance"; Appendix D scores most benchmarks 0 on R.10 (digest) | methods | CONTEXT; does not discuss cost or user simulators (digest)
M13 | Reuel et al., BetterBench (independent of assessed benchmarks) | https://arxiv.org/html/2411.12990 | v1 | "46 best practices"; "24 AI benchmarks"; §7 14 of 24 did not run multiple evaluations, report significance or uncertainty (digest paraphrase); 17 of 24 lack easy replication scripts | methods | CONTEXT; not specific to agents
M14 | Bean et al., "Measuring what Matters" (academic review) | https://arxiv.org/html/2511.04703v1 | v1 | "systematic review of 445 LLM benchmarks"; §3.6 "only 16.0% of reviewed benchmarks conducted any statistical testing"; §3.3 "Employ sampling strategies to ensure task items are representative of the overall task space"; §3.4 "Newly constructed datasets should be preferred to reused datasets" | methods | CONTEXT; conflicts with a "prefer established" rule
M15 | Kapoor et al., AI Agents That Matter | https://arxiv.org/html/2407.01502v1 | v1 | §2 "AI agent evaluations must be cost-controlled"; §2.3 "'State-of-the-art' agent architectures for HumanEval do not outperform simple baselines"; §6 "agent evaluations are rarely accompanied by error bars"; "many reported accuracy scores were above the maximum of five runs"; one SWE-bench run can cost over USD 8,000 | all | FIT for bill with accuracy and run variance
M16 | Kapoor et al., HAL | https://arxiv.org/abs/2510.11977 | v1 | Abstract (digest): 21,730 rollouts, 9 models, 9 benchmarks, about $40,000; "Higher reasoning effort reduced accuracy in most runs"; agents "searched for the benchmark on HuggingFace instead of solving the assigned task"; 2.5B tokens released | methods, E2E | CONTEXT; logs a possible source of token and cost per task
M17 | Polo et al., tinyBenchmarks | https://arxiv.org/html/2402.14992v2 | v2 | "it is sufficient to evaluate this LLM on 100 curated examples"; §1 "achieving average estimation error under 2%"; §6.2 "The main limitations ... are related to potential severe distribution shifts"; §2 assumes "access to correctness evaluations for a set of LLMs" | P1-P3, E2E | PROBLEM: needs prior response banks; static QA only; stratified random sampling is its baseline (§3.1)
M18 | Kipnis et al., metabench | https://arxiv.org/html/2407.12844v2 | v2 | 1.24% RMSE per benchmark, 0.58% total (search summary); §2.3 higher-dimensional models "require much larger subjects-to-items ratios"; §1.1 over 5000 LLMs; §4.1 static benchmarks "run the risk of being memorized" | methods | PROBLEM for reuse
M19 | Ndzomga, "Efficient Benchmarking of AI Agents" (single-author preprint) | https://arxiv.org/abs/2603.23749 | v1, 24 Mar 2026 | "absolute score prediction degrades under this shift, while rank-order prediction remains stable"; tasks "with intermediate historical pass rates (30-70%)"; cuts tasks by "44-70%" | P1-P3, E2E | FIT/PROBLEM: rank, not absolute; needs history; mid-difficulty filtering is exploratory only
M20 | Heineman et al., Signal and Noise | https://arxiv.org/html/2508.13144v1 | v1 | §3 "Signal measures how spread out scores are for different models on a single benchmark"; "larger benchmarks may not necessarily be better for comparing models" | methods | CONTEXT; noise across checkpoints, not agent runs
M21 | Miller, "Adding Error Bars to Evals" | https://arxiv.org/html/2411.00640v1 | v1 | §2.2 "the cluster adjustment in our real-world example is far from trivial (up to 3X)" | E2E, P1 | FIT: cluster tasks sharing a user, server or history
M22 | same | same | v1 | §4.2 "We therefore recommend using the paired version of the standard error estimate wherever practicable." | all | FIT for paired arms
M23 | same | same | v1 | §3.1 "The first strategy for reducing the expected conditional variance is to resample the model a number of times."; §3.3 against lowering temperature "unless the purpose is to study the model at the new temperature" | E2E | FIT, QA setting
M24 | same | same | v1 | §5 "new evals should contain at least 1,000 questions in order to have good signaling ability" | P1-P3 | PROBLEM for 20-sample loop items (matches `05` section 1); a worked example, not a rule
M25 | search summary, several 2026 preprints on equivalence testing (not opened) | not stored | 2026 | "the sample needed for an equivalence claim scales with 1/m²"; one retrieval-agent paper uses a one-sided non-inferiority test with a -2 point margin set in advance | E2E | CONTEXT: non-inferiority needs a margin; without one, estimation only
M26 | Yao et al., tau-bench (authors; Sierra) | https://arxiv.org/pdf/2406.12045 | ICLR 2025 | search summary: "pass^8 below 25%" on retail for gpt-4o with function calling | P1, P3, E2E | CONTEXT: run-to-run inconsistency large
M27 | Zheng et al., MT-Bench (judge-method authors) | https://arxiv.org/html/2306.05685v4 | v4 | §4.2 GPT-4 agreement with humans "reaches 85%, which is even higher than the agreement among humans (81%)"; §3.3 "Most LLM judges favor the first position"; 80 questions, 58 labelers | methods | FIT/CONTEXT: validated for chat, not tool-call correctness
M28 | Feuer et al. (independent) | https://arxiv.org/html/2509.20293v1 | v1 | "Schematic adherence quantifies how much of a judge's overall verdict is explained by the explicit evaluation schema"; unexplained variance above 90% for one judge (digest) | methods | PROBLEM for judge-scored claims
M29 | practitioner blogs (search results only) | not stored | 2026 | "raw agreement overstated judge quality by 33 to 41 points against Cohen's kappa" (secondary) | methods | CONTEXT, weak
M30 | Singh et al., The Leaderboard Illusion (Cohere-affiliated) | https://arxiv.org/html/2504.20879v1 | v1/v2 | "we identify 27 private LLM variants tested by Meta in the lead-up to the Llama-4 release"; "relative performance gains of up to 112% on the arena distribution"; §6 "Prohibit score retraction after submission." | methods | CONTEXT (PROBLEM for choose-after-seeing)
M31 | Xu et al., contamination survey | https://arxiv.org/pdf/2406.04244 | Jun 2024 | search summary only | methods | CONTEXT, not read
M32 | Gill et al., "What Has Been Lost with Synthetic Evaluation?" (independent) | https://arxiv.org/abs/2505.22830 | v3, 3 Oct 2025 | generated variants "less challenging for LLMs than their human-authored counterparts"; valid under guidelines "at a fraction of the cost" | P2, P3, methods | PROBLEM/FIT: constructed tasks valid but easier; reading comprehension, not tool use
M33 | Zhou et al., "Mind the Sim2Real Gap" (independent; CMU) | https://arxiv.org/abs/2603.11245 | v2, 31 Jul 2026 | "451 participants, 165 tasks"; "benchmarking 31 LLM simulators"; simulated users "overly cooperative", an "easy mode"; best simulator USI 76.0 against 92.9 for humans (search summary) | P1, E2E | PROBLEM for simulator-based tasks
M34 | Seshadri et al., "Lost in Simulation" (independent) | https://arxiv.org/abs/2601.17087 | v2, 28 Jan 2026 | success shifts "up to 9 percentage points" depending on the user LLM; "systematic miscalibration" | P1, E2E | PROBLEM: fix and report the simulator model
M35 | Roig, KAMI (vendor author, Kamiwaza) | https://arxiv.org/abs/2511.08042 | v1, 11 Nov 2025 | "traditional benchmark rankings are a poor predictor of practical agentic performance"; 170,000 items, 5.5 billion tokens, 35 configurations | CONTEXT | interested party

(M5, M25, M29, M31 rest on search summaries only.)

### Where the sources disagree or leave gaps
- Reused versus new data: Bean §3.4 prefers new data; Kapoor and Zhu stress holdout and validity of whatever is used; Gill shows newly generated data can be easier. "New" is not automatically better.
- Subsets: tinyBenchmarks and metabench reconstruct scores from large response banks; Ndzomga preserves rank and says absolute scores degrade; none addresses an unbiased paired difference and bill on a subset of agent tasks.
- Sample size: Miller's 1,000 in his example; `05`'s 20-sample items already say they cannot resolve small differences; Heineman: bigger not always better.
- Significance reporting: Bean 16.0%, BetterBench 14 of 24; different samples.
- tau-bench user simulator: ABC silent; Zhou and Seshadri (independent of each other, both 2026) find problems.

## 4. Not found (in the places read)
A methods procedure for pooling effects across heterogeneous LLM or agent benchmarks; preregistration guidance specific to LLM or agent evaluation; agent-specific guidance on clustered errors where tasks share servers or users; a primary study of LLM judges scoring tool-call correctness; sample-size guidance for a cost-ratio outcome. Not read: "Reliability without Validity" (named in a blog), the preprints behind M5 and M25; Raji et al. 2021 and Xu et al. known only from search summaries. Queries: Miller error bars; AI Agents That Matter; ABC; BetterBench; Measuring what Matters; HAL; tinyBenchmarks; metabench; Signal and Noise; BenchBench; Leaderboard Illusion; Benchmark Lottery; LLM-judge reliability (2); user-simulator reliability; Raji 2021; preregistration in ML; contamination survey; synthetic evaluation validity; meta-analysis across benchmarks; tau-bench pass^k; non-inferiority in LLM evaluation; agent benchmark subsets; Bean checklist.

## 5. Possible wrong assumptions
- Bill versus accuracy: the checklists concern accuracy and validity; only Kapoor discusses cost and HAL reports it per run; no source treats cached-input or cache-write cost as a benchmark output; Miller's sample-size guidance does not cover a cost ratio.
- Subsetting: representativeness methods need response banks that do not exist here; report the subset's distribution on the properties that matter and limit the claim to them.
- User simulators inflate success (two independent 2026 studies); for P1, simulated histories may overstate memory benefit.
- Non-inferiority: without a margin (REQ-U21-07), only estimation with an interval; `05` section 3's sample phrase has no target until a margin or estimation-only reporting is chosen.
- Pilot-to-confirmatory split: holding out items is supported, but a paper protocol does not prevent overfitting; tool-set size, catalogue padding and prompt variants must also be frozen before the confirmatory run, not only the items.

## 6. URLs to store
https://arxiv.org/html/2411.00640v1 | html
https://arxiv.org/html/2407.01502v1 | html
https://arxiv.org/html/2507.02825v5 | html
https://arxiv.org/html/2411.12990 | html
https://arxiv.org/html/2511.04703v1 | html
https://arxiv.org/abs/2510.11977 | html
https://arxiv.org/html/2402.14992v2 | html
https://arxiv.org/html/2407.12844v2 | html
https://arxiv.org/abs/2603.23749 | html
https://arxiv.org/html/2508.13144v1 | html
https://arxiv.org/html/2407.13696v2 | html
https://aclanthology.org/2024.acl-long.560/ | html
https://arxiv.org/abs/2603.11245 | html
https://arxiv.org/abs/2601.17087 | html
https://arxiv.org/abs/2505.22830 | html
https://arxiv.org/html/2509.20293v1 | html
https://arxiv.org/html/2306.05685v4 | html
https://arxiv.org/html/2504.20879v1 | html
https://arxiv.org/pdf/2311.18807 | pdf
https://arxiv.org/pdf/2111.15366 | pdf
https://arxiv.org/abs/2107.07002 | html
https://arxiv.org/pdf/2406.12045 | pdf
https://arxiv.org/pdf/2406.04244 | pdf
https://arxiv.org/abs/2511.08042 | html
https://arxiv.org/abs/2602.15532 | html
