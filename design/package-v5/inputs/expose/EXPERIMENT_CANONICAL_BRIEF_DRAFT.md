# Stateful Momentum Portfolio Active Registry

## Status

Draft. This is the private canonical experiment brief for the active-registry mechanism-isolation experiment.

**2026-07-17 execution note:** this brief is the broader mechanism design
draft. For the first controlled implementation, P1-006/P1-007 and
`audits/p1_010_controlled_bm_experiment_registry.md` control the executable
method registry, budgets, split, and tuning protocol. Dense/hybrid/reranking,
planner, schema, routing, and downstream caller entries below remain deferred
unless a later decision explicitly promotes them.

**P1-011 note:** P1-010 established the controlled transport-and-metric
pipeline, not a portfolio-method winner. P1-011 confirmed that M2/M3 active
set differences concern unlabelled tools under the current fixture. Do not
promote the broader portfolio claim below until the method is either narrowed
to tool-name-prefix diversity or evaluated through a separately specified,
semantically aligned fixture.

## Exact experiment name

**Stateful Momentum Portfolio Active Registry: Mechanism-Isolation Experiment**

Short name: **Active Registry Mechanism Isolation**

## Relation to the registered thesis

The registered thesis architecture is broader than this experiment. The full thesis includes access filtering, hybrid retrieval and reranking, schema-to-interface compression, a session-scoped active registry, and an execute / expand / abstain router evaluated against full-schema prompting, retrieval baselines, compact interfaces, and stateless retrieval.

This experiment isolates one component: the active-registry controller. It asks whether a fixed-budget, session-scoped active tool set can be maintained better than repeated retrieval by keeping still-useful tools, adding complementary tools, evicting stale tools, reducing redundant or distracting tools, and recovering from topic shifts.

This experiment does not replace later schema-compression, downstream tool-call, router, latency, or abstention evaluation. It is a prerequisite diagnostic slice.

## Research question

Can a stateful momentum-based portfolio active registry improve active tool-set quality across multi-turn sessions compared with per-turn retrieval baselines, under the same active-set budget?

More precisely:

> Under fixed budget `B`, does a controller using tool/domain momentum, decay, topic-shift reset, exploration slots, and portfolio diversification improve gold-tool coverage, precision, retention, eviction, distractor exposure, redundancy, churn, and topic-shift recovery compared with strong stateless and simple stateful retrieval baselines?

## Mechanism isolated

The isolated mechanism is active-set control:

```text
Passive Registry P
  -> candidate retrieval/reranking
  -> active-registry controller
  -> active set A_t
```

The controller maintains `A_t` across turns using:

- current-query relevance
- retained-tool momentum
- unused-tool decay
- topic-shift reset or penalty
- fresh retrieval / exploration slots
- portfolio selection for capability coverage and low redundancy
- optional planner-derived capability signals

Planner output is not the core mechanism. It is an optional signal that must be tested through ablations.

## What is explicitly not being tested

- Schema-to-interface compression variants
- L0-L3 compact-interface comparison
- Full JSON tool-call generation
- Argument validation or invalid-call rate
- Live API execution
- Execute / expand / abstain routing
- Logprob or uncertainty routing
- Real access-control or security policy enforcement
- Prefix caching
- End-to-end latency as a primary claim
- Learning from production logs

These are postponed stages, not rejected thesis components.

## Core variables

| Symbol | Meaning | Controller-visible? |
|---|---|---|
| `P` | Passive registry of all ToolCards. | Yes |
| `T_i` | Tool `i` in `P`. | Yes |
| `Card_i` | Stable ToolCard metadata for selection. | Yes |
| `S_i` | Full schema for `T_i`. | No in this phase, except as opaque reference. |
| `q_t` | User query at turn `t`. | Yes |
| `h_t` | Conversation history before turn `t`. | Yes |
| `A_t` | Active registry selected for turn `t`. | Output |
| `A_{t-1}` | Previous active registry. | Yes |
| `B` | Active-set budget in tools or tokens. | Yes |
| `R_t` | Retrieved candidate set. | Yes |
| `C_t` | Candidate pool after retrieval/reranking. | Yes |
| `domain_t` | Controller-estimated domain distribution. | Yes if estimated from visible fields. |
| `G_t` | Gold tools required for turn `t`. | Evaluation-only |
| `Useful_t` | Gold tools plus explicitly allowed support tools for turn `t`. Support tools must be labeled before evaluation, not inferred after seeing model output. For no-tool tasks, `Useful_t` is empty. | Evaluation-only |
| `D_t` | Semantically similar but wrong distractor tools. | Evaluation-only |
| `F_t` | Forbidden tools for the current task. | Evaluation-only unless simulating an oracle filter. |
| `K_t` | Previously active tools still useful at turn `t`. | Evaluation-only |
| `E_t` | Previously active tools that should be evicted. | Evaluation-only |
| `shift_t` | Gold topic-shift label. | Evaluation-only unless using an oracle ablation. |
| `Pred_t` | Tools added only for expected next use. | Controller-derived if implemented. |

## ToolCard representation

Use one fixed representation in the primary mechanism experiment:

```json
{
  "tool_id": "jira.create_issue",
  "domain": "jira",
  "capability": "issue_creation",
  "description": "Create a new issue or defect.",
  "input_concepts": ["summary", "description", "project_key", "issue_type"],
  "output_concepts": ["issue_key", "issue_url"],
  "risk_level": "write",
  "positive_intents": ["create bug", "open defect", "file issue"],
  "negative_intents": ["attach evidence", "update existing issue"],
  "related_tools": ["jira.search_duplicate", "jira.attach_file"],
  "full_schema_ref": "schema://jira/create_issue"
}
```

ToolCards are selection metadata. They are not evidence that schema compression works.

## Hypotheses

### H1 - Momentum improves continuity

Momentum-based state improves same-topic multi-turn sessions compared with retrieve-from-scratch baselines.

Expected effects:

- Retention Accuracy increases.
- Churn on same-topic turns decreases.
- Gold Recall@B improves or remains competitive in multi-turn sessions.

### H2 - Topic-shift reset reduces stale pollution

Decay and topic-shift reset reduce old-topic registry pollution after hard topic shifts.

Expected effects:

- Eviction Accuracy increases after hard shifts.
- Registry Pollution decreases.
- Topic-Shift Recovery is faster.
- Tunnel Vision Rate decreases.

### H3 - Portfolio selection reduces redundancy and distractors

Portfolio selection improves active-set diversity compared with individually top-ranked retrieval.

Expected effects:

- Redundancy Rate decreases.
- Distractor Rate decreases.
- Precision@B increases.
- Capability Coverage@B increases on multi-intent tasks.

### H4 - Stateful momentum portfolio is strongest overall

Combining momentum, decay, topic-shift handling, exploration, and portfolio selection yields the best balance of recall, precision, retention, eviction, and robustness.

Expected effects:

- Competitive Gold Recall@B.
- Higher Precision@B and Capability Coverage@B.
- Lower distractor exposure and redundancy.
- Better retention in same-topic sessions.
- Better recovery after hard topic shifts.

### H5 - Planner is optional, not necessary

Planner-derived capability signals may improve coverage, but the architecture should still outperform baselines without planner input.

Required ablation:

- `with_planner_signal`
- `without_planner_signal`

## Baselines

Baselines must use the same passive registry, active budget `B`, visible metadata, and candidate-generation limits unless explicitly marked as oracle.

| ID | Baseline | Purpose |
|---|---|---|
| B0 | Random under budget | Sanity lower bound only. |
| B1 | Dense top-k retrieve-from-scratch | Basic stateless retrieval baseline. |
| B2 | BM25 or sparse top-k retrieve-from-scratch | Lexical retrieval baseline. |
| B3 | Hybrid dense + sparse retrieve-from-scratch | Stronger stateless retrieval baseline. |
| B4 | Hybrid + rerank retrieve-from-scratch | Strong retrieval/reranking baseline. |
| B5 | Keep-last-k stateful retrieval | Simple memory baseline: retain prior active tools plus fresh retrieval. |
| B6 | Sticky top-k with decay | Simple stateful baseline without portfolio optimization. |
| B7 | Oracle candidate pool | Upper-bound ablation where gold tools are guaranteed in candidates, but selection still has budget constraints. |

Proposed methods:

| ID | Method | Purpose |
|---|---|---|
| M1 | Momentum Registry | Tests retention, decay, and topic-shift behavior. |
| M2 | Portfolio Registry | Tests coverage/diversity without state. |
| M3 | Stateful Momentum Portfolio Registry | Tests the full isolated active-registry controller. |
| M4 | Stateful Momentum Portfolio with planner signal | Optional variant to test whether planner-derived capabilities help. |

## Datasets and tool pools

### Controlled synthetic benchmark

Purpose: isolate active-registry mechanics with labels that standard benchmarks often lack.

The synthetic benchmark should provide:

- passive registries from 500 to 10,000 ToolCards
- overlapping domains and capabilities
- redundant alternatives
- semantically similar distractors
- forbidden/high-risk tools
- multi-turn sessions
- same-topic, related-shift, and hard-shift transitions
- gold tools per turn
- support tools where appropriate
- stale/retain/evict labels
- no-tool or irrelevant tasks for exposure behavior

Synthetic data is diagnostic, not final proof of usefulness.

### External benchmark adaptation

External benchmarks test transfer beyond controlled labels.

| Benchmark | Role | Expected limits |
|---|---|---|
| API-Bank | Small dialogue-based sanity check. | May need derived or manual labels for retention/eviction. |
| ToolBench / ToolLLM | Large API-pool stress test if reproducible. | Live or historical API volatility may limit execution claims. |
| BFCL-style validation | Downstream function-calling and relevance/irrelevance validation after active-set quality is stable. | Does not directly test all active-registry state metrics. |
| OpenAPI collections such as APIs-guru | Possible source for real tool schemas or metadata extraction. | Requires normalization into ToolCards; extraction bias must be documented. |

External benchmarks must not replace the controlled benchmark. They validate transfer for the metrics they can support.

## Metrics

### Primary active-set metrics

| Metric | Definition | Applies to |
|---|---|---|
| Gold Recall@B | `|A_t intersect G_t| / |G_t|`; if `G_t` is empty, report separately as no-tool case. | Synthetic and external where gold labels exist. |
| Precision@B | `|A_t intersect Useful_t| / |A_t|`; if `A_t` is empty, define as 1 for no-tool tasks and 0 for tasks with required tools. | Synthetic and external where useful/support labels exist. |
| Capability Coverage@B | Required capabilities covered by at least one active tool divided by required capabilities. | Synthetic and manually/derived labeled external subsets. |
| Redundancy Rate | Fraction of active tools beyond the allowed count per capability group. | Synthetic and ToolCard-normalized external pools. |
| Distractor Rate | `|A_t intersect D_t| / |A_t|`; if `A_t` is empty, 0. | Synthetic and labeled external subsets. |

### Stateful metrics

| Metric | Definition | Applies to |
|---|---|---|
| Retention Accuracy | `|A_t intersect K_t| / |K_t|`; skip or mark undefined when `K_t` is empty. | Synthetic and annotated external subsets. |
| Eviction Accuracy | `|E_t minus A_t| / |E_t|`; skip or mark undefined when `E_t` is empty. | Synthetic and annotated external subsets. |
| Churn | `1 - |A_t intersect A_{t-1}| / |A_t union A_{t-1}|`. | All multi-turn runs. |
| Registry Pollution | Old-topic or no-longer-useful active tools divided by `|A_t|`; if `A_t` is empty, 0. | Synthetic and annotated external subsets. |
| Topic-Shift Recovery | Number of turns after a shift until Gold Recall@B and Registry Pollution meet predeclared thresholds within a predeclared horizon. Default thresholds and horizon must be frozen in Phase 0 before coding. | Synthetic and annotated external subsets. |
| Tunnel Vision Rate | New-domain gold tools missed while old-domain tools occupy active slots. | Synthetic and annotated external subsets. |

### Secondary metrics

| Metric | Definition | Applies to |
|---|---|---|
| Forbidden Exposure Rate | Any `F_t` tool exposed in `A_t`; not a security claim. | Synthetic or oracle-labeled tasks. |
| NoGold Empty/NoTool Rate | No-tool tasks where `A_t` is empty or explicitly marked no-tool. | Synthetic no-tool tasks. |
| Token Cost | Initially `|A_t|`; later tokenized ToolCard length if fixed `B` is not enough. | All runs. |
| Prediction Hit Rate | Fraction of prediction-slot tools useful in the next 1-3 turns. | Only if prediction slots are implemented. |

## Validity threats

| Threat | Risk | Mitigation |
|---|---|---|
| Synthetic overfitting | Mechanism may exploit artificial patterns. | Use multiple generators, held-out domains, and external adaptation. |
| Label leakage | Gold/distractor/shift labels may enter scoring. | Enforce controller-visible vs evaluation-only data split. |
| Weak baselines | Easy wins over flat top-k may not be convincing. | Include strong hybrid/reranked and simple stateful baselines. |
| Budget unfairness | Methods may see different candidate or active budgets. | Freeze `B`, retrieval depth, reranking access, and metadata access. |
| Planner confounding | Planner output may dominate the result. | Make planner optional and ablate it. |
| Metric ambiguity | Precision, pollution, and no-tool cases can be gamed. | Define zero-denominator and support-tool policies before coding. |
| External label gaps | API-Bank, ToolBench, or BFCL may not expose retention/eviction labels. | Restrict metrics, derive labels cautiously, or annotate subsets. |
| Schema mismatch | ToolCards may hide full-schema complexity. | Do not make schema-compression claims in this experiment. |
| Latency overclaim | Smaller active sets do not guarantee faster systems. | Keep latency out of the core mechanism claim. |

## Ablations

Required:

- without momentum
- without decay
- without topic-shift reset
- without exploration slots
- without portfolio redundancy penalty
- without planner signal
- without retained tools, equivalent to retrieve-from-scratch
- oracle topic-shift labels vs detected topic shift
- oracle candidate pool vs retrieved candidate pool

Optional:

- different active budgets `B`
- different candidate pool sizes
- prediction slot enabled vs disabled
- domain momentum only vs tool momentum only
- capability grouping from metadata vs planner-derived capabilities

## Acceptance criteria

The experiment is successful enough to justify downstream thesis integration if:

1. M3 improves Precision@B, Redundancy Rate, and Distractor Rate over B3/B4 without unacceptable Gold Recall@B loss.
2. M1 or M3 improves Retention Accuracy and same-topic churn over retrieve-from-scratch baselines.
3. M1 or M3 improves Eviction Accuracy and Registry Pollution after hard topic shifts.
4. M3 remains competitive when planner signal is removed.
5. Results are robust across at least two active budgets and multiple synthetic domains.
6. External adaptation does not contradict the controlled benchmark on supported metrics.

The direction is weak if:

1. Stateful momentum does not improve retention or churn.
2. Topic-shift reset does not reduce stale pollution.
3. Portfolio selection reduces distractors only by dropping required tools.
4. Strong hybrid/reranked baselines match or beat M3 across primary metrics.
5. Gains disappear when planner signal is removed.

## Implementation phases

### Phase 0 - Protocol freeze

Freeze:

- ToolCard schema
- controller-visible fields
- evaluation-only labels
- baseline set
- metric definitions
- Topic-Shift Recovery thresholds and maximum recovery horizon
- budget and candidate limits
- synthetic generator specification

### Phase 1 - Controlled registry and labels

Build:

- passive ToolCard registry
- multi-turn task sessions
- gold/support/distractor/forbidden labels
- topic-shift labels
- retain/evict labels

No LLM caller is used.

### Phase 2 - Single-turn active-set selection

Compare stateless retrieval and portfolio selection on single-turn and multi-intent cases.

Primary metrics:

- Gold Recall@B
- Precision@B
- Capability Coverage@B
- Redundancy Rate
- Distractor Rate

### Phase 3 - Multi-turn state

Compare retrieve-from-scratch, simple stateful retrieval, momentum registry, and stateful momentum portfolio.

Primary metrics:

- Retention Accuracy
- Eviction Accuracy
- Churn
- Registry Pollution
- Gold Recall@B
- Precision@B

### Phase 4 - Topic-shift stress test

Run same-topic, related-shift, and hard-shift sessions.

Primary metrics:

- Topic-Shift Recovery
- Registry Pollution
- Eviction Accuracy
- Tunnel Vision Rate
- Gold Recall@B after shift

### Phase 5 - External benchmark adaptation

Adapt only after controlled metrics work.

Recommended order:

1. API-Bank-style dialogue sanity check.
2. ToolBench / ToolLLM-style large-pool stress test if feasible.
3. BFCL-style downstream validation after active-set quality is stable.

Use only metrics supported by available or derived labels.

### Phase 6 - Optional downstream caller evaluation

Expose `A_t` to an LLM/tool caller only after active-set metrics are stable.

Possible metrics:

- tool-call success
- wrong-tool call rate
- invalid argument rate
- no-tool behavior
- prompt tokens
- latency as secondary deployment evidence

### Phase 7 - Optional schema representation ablation

Compare ToolCard, conservative compact interface, full schema, and aggressive compact interface.

This is a later schema-compression experiment, not part of the core active-registry mechanism isolation.

## Non-goals

- Proving the full thesis architecture in one experiment
- Proving schema compression works
- Proving end-to-end tool-calling correctness
- Proving real execution safety
- Proving latency always improves
- Building a new benchmark as the thesis contribution
- Optimizing retrieval as the primary novelty
- Treating planner output as the mechanism
- Claiming external validity from synthetic results alone
- Citing local working notes as external evidence

## Readiness decision

This experiment is **conditionally ready for implementation planning** and **not ready for coding**.

Implementation planning can begin if it preserves this brief as the source of truth. Coding should wait until Phase 0 items are frozen in implementation tickets.
