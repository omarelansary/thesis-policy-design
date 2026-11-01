# MPT: Multi-Session Personalized Tool Calling

Anonymized release accompanying the paper. This repository contains the benchmark
data, the construction pipeline, and the evidence-interference scorer.

## Contents

```
data/
├── histories.json        459 user histories (sessions + preference annotations)
├── instances.json        4,695 evaluation instances (query + gold, FK → histories)
├── pref_groups.json      5 preference groups / 59 (domain, slot, value) rules
└── queries/              query templates (multiturn/singleturn × hint/nohint)
                          + pref_group.json, pref_list.json
construction/             construction scripts (source corpora required; see "Pipeline" below)
analysis/
└── interference.py       evidence-interference scorer (Sec. 7.1)
```

## Data model

The release is relational: each **history** is stored once, and each **instance**
references its history by `example_id`. Joining is one line:

```python
import json
hist = {h["example_id"]: h for h in json.load(open("data/histories.json"))}
for inst in json.load(open("data/instances.json")):
    history = hist[inst["example_id"]]   # sessions, preference annotations
    query   = inst["query"]              # user request with the target parameter unspecified
    gold    = inst["reference_ground_truth"]
```

### histories.json (459 records)

| field | description |
|---|---|
| `example_id` | unique history id |
| `sessions` | ordered list of past sessions; each has `dialogue` (turns) and `api_call` (tool calls executed in that session; may be empty — 7.1% of sessions contain no call) |
| `api_calls` | history-level aggregation: (domain, slot, value) triples observed ≥2 times with a unique settled value |
| `api_calls_drop` | aggregated triples removed due to conflicting repeated values |
| `api_calls_pref` | preference annotations: per value group, the supporting evidence with per-value counts |
| `meta.subset` | `mix` (299) / `conflict_ordered` (80) / `conflict_noise` (80) |

Conflict histories additionally carry `meta.majority` / `meta.minority`
(the dominant and competing preference, derivable from `api_calls_pref` counts),
`session_labels`, and `meta.arrangement` (`ordered`: minority-evidence sessions
precede majority; `noise`: controlled shuffle).

### instances.json (4,695 records)

| field | description |
|---|---|
| `sample_id` | unique instance id |
| `example_id` | FK into histories.json |
| `query` | the evaluated request (hint condition; no-hint templates in `data/queries/`) |
| `query_type` | `singleturn` (2,387) / `multiturn` (2,308) |
| `pref_type` | reasoning type — `easy` = Preference Recall (1,375), `medium` = Preference Induction (1,944), `hard` = Preference Transfer (1,376) |
| `condition` | `{single,multi}_{easy,medium,hard}` |
| `conflict` | whether the history carries competing preference evidence (920 true) |
| `reference_ground_truth` | gold tool call(s) for the unspecified target parameter |

### Identity harmonization

Histories that merge two DuRecDial 2.0 seekers (`conflict_durec_*`) originally
contained two self-reported identities. In these 96 histories, user-stated names,
ages, and gender terms (and the assistant's address forms) are rewritten to a single
identity, chosen deterministically so that both arrangements of a pair agree.
Only dialogue text changes (204 turns); every API call, gold argument, session label,
celebrity mention, and turn count is unchanged.

## Key statistics

- 459 histories / 6,961 sessions / 4,695 instances; 10.2 instances per history on average.
- **164 histories (35.7%) support two or more distinct preferences** (up to four),
  accounting for 2,432 instances (51.8%). A history supporting several preferences
  yields separate instances for each.
- Evidence interference (Sec. 7.1): mean 0.701, sd 0.165; 46.9% of instances have
  at least one competing (C > 0) observation.
- Preferences (Table 2): low_cost, high_cost, prefers_star, eco, solo_usage.

## Pipeline

Construction scripts under `construction/`, in execution order. They document the
construction process; running them requires the source corpora (SGD, DuRecDial 2.0,
HomeBench), which are not redistributed here.

1. `build_common_pref.py` / `build_pref_groups.py` — preference dictionary from the three source tracks (SGD, DuRecDial 2.0, HomeBench).
2. `mix600.py` — order-preserving session interleaving of source personas into mixed histories (tiers: solo / 2-way / 3-way).
3. `build_conflict.py` / `build_conflict_mixed.py` / `build_conflict_arrangements.py` — conflict histories (strict-plurality competing evidence) and the ordered/noise arrangements.
4. `build_downsized.py` — stratified downsizing preserving rare query-support pools.
5. `build_merged_queries.py` — unified query set (multiturn/singleturn × hint/nohint).

`analysis/interference.py` recomputes the evidence categories (R/C/N) and the
interference score for every instance directly from the released files.

## License

Released under **CC BY-NC-SA 4.0**. MPT derives from the Schema-Guided Dialogue
dataset (CC BY-SA 4.0), DuRecDial 2.0, and HomeBench; source attributions apply.
