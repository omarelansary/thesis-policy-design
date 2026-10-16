# Decision record

- Decision ID and date (UTC): D4D, 2026-10-13
- Decision owner: the user
- Question to decide: whether to run one targeted evidence-closure campaign on the decision-critical gaps left by Stage 4b, before any research-question decision, and under what limits.
- Competing options (including stop / no viable option): (a) stop at the Stage 4b synthesis and decide with the current evidence; (b) run a bounded evidence-gap campaign, then stop before any research-question decision (chosen by the user's instruction of 2026-10-13).
- Evidence considered: HEAD 97bd23a; `stage-reports/STAGE4B_FINAL_SYNTHESIS_AND_SUPERVISOR_ALIGNMENT-20261013.md`, `STAGE4B_OPPORTUNITY_MAP-20261013.md` (with section 11), `audits/S4B-C1…C3`, `S4B-L1`, `S4B-V3…V7`, `STAGE1_RESEARCH_BRIEF.md` (rev. 2), `STAGE4_CANDIDATE_QUESTIONS-20261013.md`, and the supervisor-instruction passages of the S1 transcript (read only to reconstruct requirements; student-reported results not read or used).
- Governing text: `protocols/STAGE_GATES.md` (unchanged); `CLAUDE.md` clean-room rules. This campaign is not a restart of the landscape survey and not a Stage 5 step.

## Pre-registered limits (fixed before any new search, fetch or probe)

| Resource | Limit |
|---|---|
| Discovery queries, OpenAlex and GitHub REST, through `infrastructure/tools/s4c_search.py` (self-logging) | 24 |
| Harness WebSearch (backend unnamed; each result re-located at a primary URL before use) | 16, logged with `s4c_search.py log-web` |
| WebFetch triage reads (unstored; never sufficient for a consequential claim) | 10 |
| Stored fetches with `fetch_source_text.py` | 18 (single bounded unit; written reason below) |
| Research-worker (Sonnet 5.5 Medium) extraction tasks, run one at a time | at most 2 |
| Independent adversarial review (Sonnet 5.5 Medium, read-only, fresh context) | exactly 1, after the evidence is assembled |
| Technical probes | at most 3; at most 2 hours execution in total; external API spending EUR 0 (no provider key is present in this environment, so no attributable spend is possible) |
| Opus | not used (not separately authorized) |
| Previous thesis material, Stage 5, runs of third-party code, full benchmark runs | prohibited |

Reason for a single larger unit (ticket COORD-S4C-GAP-20261013-01): the campaign is one coherent closure task whose steps share one gap register; splitting it into 30-minute units would only multiply commits. The ticket is updated at each stage so a quota interruption can resume from it.

## Decision-critical gap register (written before searching; impact = could the answer change which directions remain viable or how they are worded)

| ID | Gap | Why it could change the decision | Planned closure method |
|---|---|---|---|
| G1 | Has count vs tokens vs overlap been separated for current models? Closest prior art for D-REL (SLCA-GRPO, ToolMATH, ToolMenuBench, Du et al., new terms such as tool-space interference) | Decides whether D-REL's contrast is a gap or already done | Primary-text reading of stored and 1-3 new sources; 2 new-terminology searches |
| G2 | Paired eager vs deferred/progressive-disclosure studies (SkillJuror, ToolSearcher, SING, DynamicMCPBench, Dynamic ReAct) | Decides whether the deferral crossover (N2/F) and part of policy evaluation (C) is answered | Primary-text reading of the named 2026 abstracts-only sources |
| G3 | Adaptive exposure / escalation policies in academic work (variable k, confidence-triggered expansion, learned exposure, cascades, bandits) | The surviving "policy" reading (C) was judged only against shipped vendor mechanisms; academic adaptive policies were not searched as a family | 3-4 targeted searches; read the 1-2 closest sources |
| G4 | Is the model-visible token accounting observable? Provider usage fields, caching fields, tool-search billing, count-tokens endpoints | Decides whether D-COST/F can attribute tokens to definitions, discovery and recovery, and whether D-a (tokens vs cost) is measurable | Stored official documentation re-read with exact field names; WebFetch of the current docs only where stored copies are stale |
| G5 | Statistical feasibility of "maintained accuracy" and of the applied arms (power, margin, clustering, repeat runs); sizes of public benchmarks | Decides whether any non-inferiority claim is achievable at thesis budgets | Offline exact/simulated power computation (probe P2) + benchmark-size table from stored extractions |
| G6 | Is "count at fixed tokens" technically identifiable with real public catalogues without padding? | Decides whether D-REL's central contrast is constructible, or confounded by construction | Offline probe P1 on public tool-schema data |
| G7 | Magnitude of definition overhead in real use; capacity as an objective | Decides whether tokens-as-objective is worth optimising | 2 searches for multi-user or trace-based breakdowns; otherwise bounded |
| G8 | Do current frontier models still show tool-count degradation within their windows? | C3's strongest objection to D-REL; also bears on every accuracy-maintenance claim | Search for 2026 frontier results; primary-text reading |
| G9 | D-SEC residual gap (attacks on model-initiated or deferred search) | Alternative objective; C3 narrowed it | 2 searches with new terms |
| G10 | Alternative system designs (code-mediated, gateways, hierarchical) head-to-head evidence; status of the supervisor-named baseline "Executor" | Decides whether "baseline execution" (D-i) and design-space claims are supportable | 2-3 searches; repository inspection by file listing and reading only |
| G11 | Public benchmarks able to support a catalogue-scaled, deterministic, end-to-end comparison (task count, grading, catalogue scaling, licence) | Decides feasibility of any Phase-2-type study | Table from stored extractions + at most 2 new fetches |

## Stopping criteria

- A gap is INVESTIGATED when its pivotal prior-art sources have been read at primary text with locations, or its probe has run; it is BOUNDED when two consecutive distinct queries (different core terms) add no new relevant primary source, or the budget for it is spent. Bounded absence is reported as "none found under bounds B", never as a gap.
- The campaign stops when every gap rated high impact (G1, G2, G3, G4, G5, G6, G8) is INVESTIGATED or BOUNDED, or when a limit above is reached. Hitting a limit is reported as a limit, not hidden.
- Exceeding any limit requires the user's approval; the coordinator stops and asks.

## Roles and separation

- Researcher (coordinator, Sonnet 5.5 Medium): all searches, source reading and probes; labels fact / observation / interpretation / inference / uncertainty / speculation.
- Research-worker (Sonnet 5.5 Medium): bounded extraction only; returns quoted material with locations, no verdicts.
- Critic: independent Sonnet 5.5 Medium; its findings are stored separately and dispositions recorded by the coordinator. Agreement among agents that read the same corpus is not independent confirmation.

## Outputs (new files only; earlier records are not edited)

`decisions/D4D-…` (this file), `searches/stage4c/`, `audits/S4C-*`, `probes/S4C-*`, `stage-reports/STAGE4C_DECISION_EVIDENCE_DOSSIER-20261013.md`.

- Unresolved objections and uncertainties at authorization: thesis constraints (duration, compute, provider access, budget) are not in the clean-room corpus; the WebSearch backend is unnamed; the unit and horizon of the supervisor's objective remain D-a and D-e for the user.
- Required follow-up: the coordinator reports once and stops before any research-question decision.
- Decision status: **accepted by user, 2026-10-13** (instruction text of 2026-10-13, "Final Independent Evidence-Gap Investigation"). Limits above are the coordinator's choices within the user's suggested caps (three probes, two hours, EUR 5).
