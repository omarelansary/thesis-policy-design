# Stage 1 research brief and proposed Stage 2 plan

Status: **revision 2**, provisionally approved by the user on 2026-10-11 with the decisions in §0. Earlier versions are in Git (`478687c` rev. 0, `e193ff2` rev. 1). Where §0 conflicts with later sections, §0 governs.

## 0. User decisions (2026-10-11), which govern Stage 2

- **Research target (replaces the §1.1 operative objective; G-a1).** Reduce **total model-visible input tokens associated with accessing large tool catalogues**, while maintaining **end-to-end task performance**, and account for **all discovery, selection and execution overhead**. This formulation is a starting target, not a justified one: Stage 2 investigates its validity and how it can be measured.
- **Independence.** No architecture is favoured: retrieval, registries, tool search, progressive disclosure, code execution or anything else. Search includes approaches the transcript did not anticipate. Previous experiments and conclusions are unavailable until Stage 5.
- **Search authorization (G-a3, G-d).** Public technical queries may be formulated and run across academic databases, GitHub, official documentation and production systems without per-query approval. No private transcript passages, identifying personal information or unpublished material are sent. Ambiguous names from the meeting (e.g. "Executor", "MCP Atlas") are **discovery leads, not verified entities**.
- **G-e.** The supervisor's factual and comparative assertions are **claims requiring evidence**.
- **G-b.** A later meeting is not assumed. The uncertainty is recorded and does not block progress.
- **G-f.** No new experiments or benchmarks in Stage 2. Published results, implementation details, benchmark methodology and feasibility may be investigated by reading documentation and source code; **no installation or execution of third-party code**.
- **Material from any later meeting.** If supplied, it becomes a new source and triggers a Stage 1 revision. Supervisor instructions are used; anything that is the student's previous work is set aside until Stage 5.
- **G-c.** No new policy is designed or committed to. Mechanisms may be mapped; any recommendation stays provisional until evidence supports it.
- **Stopping rule.** Revised so that saturation alone cannot establish comprehensive coverage or novelty (§3.2, §3.4).
- **Stage 1 closure.** One targeted re-review by the challenger; fix substantive blocking defects only.

Evidence base: S1 only, the 2026-10-02 supervisor meeting (`evidence/S1-supervisor-meeting-2026-10-02.md`). Line-level citations (L = transcript line) and IDs (R, A, P, T, G, X, U) refer to `STAGE1_MEETING_RECORD.md` (revision 1). Independent readings and challenges: `audits/A1` (independent reading), `audits/A2` (comparison), `audits/A3` (challenge of this brief).

## 1. What the supervisor requires (from S1)

Reading key: **Required** means stated as an instruction or condition. **Recommended** means advice with "should"/"first thing" but contradicted elsewhere or time-bound. **Example** means explicitly illustrative.

### 1.1 Objective

- **Required.** Save **input tokens** while **maintaining accuracy** relative to giving the model all tools (L316–328, L132–136, L438–445). "Maintaining" is the student's word, accepted by the supervisor (L323–328).
- **Which tokens.** Everything said concerns tokens spent **exposing tool definitions/descriptions** (L320, L336, L464). Whether tool outputs, reasoning tokens or the selector's own tokens count is not settled (U2).
- **Net savings.** The selection mechanism's cost must not cancel the savings (L154–156). The standard is qualitative ("many many more"). Selective, cheap LLM steps are treated as acceptable (L420–432). The unit may be tokens or money, for example if a cheaper 27B model is used (L419–420) (U2).
- **Global accounting.** Savings are judged **globally, not per turn**: a single costlier turn is acceptable if the total falls (L468–476). Two readings are open: turns within one session, or aggregate over many separate requests (U4).
- **Earlier wording.** The supervisor first stated the problem as "minimal amount of tool with maximal amount of accuracy" (L127–129). The later statement "your idea was never to filter out tools" (L316) is treated here as the operative one. That choice is one reading (T1) and is put to you at G-a.

### 1.2 Shape of the solution

- **Required.** Think of a **policy**, not only retrieval. Retrieval may be one component (L281–285, L296–298, L328).
- **Required.** A **stepwise** structure in which **each step saves tokens** (L462–464).
- **Required.** A **fallback**: "you should give some way for the LM to query the tools that is in the passive registry and get the details" for when filtering is wrong (L466).
- **Required as a lens.** Consider **graded/partial exposure** rather than give-or-withhold ("you have to look it from this lens", L336; L338).
- **Recommended.** The first filtering step should be **conservative**: remove only tools that "will never be important" (L328).
- **Example only.** Tier sizes and contents: 100→60, three bands vs two tiers, names only for the lowest tier ("This number is not rigid", L332–336; L464; "I'm not saying this is the best way", L336).

### 1.3 Building on existing work

- **Required.** Survey papers, open-source projects, startups, industry practice and the state of the art (L344–361, L409–411, L480).
  - Use and improve what exists: "you should use it. You should improve it" (L351); "take the good ideas" (L462); "never… reinvent the wheel" (L353).
  - Establish "what is working, what is not working" (L361).
- **Required.** Repeat the search **monthly** for the whole thesis (L357–361).
- **Required, time-bound.** Before the next meeting, write a document of facts, projects and papers and a **draft step-by-step policy**, with no experiments or implementation (L458–464, L482). The stated window was "within this weekend" before Monday **2026-10-05**, which has passed (U10).
- **Conflict.** "The first thing you should do is just go to this GitHub repo download this run this… benchmark it" (L367, about "Executor") conflicts with "you don't need to run any experiment" (L458) and "You don't need to implement anything" (L482). Not decided in S1 (T6, U15). Decision G-f below.

### 1.4 Evaluation expectations

- **Required.** An **all-tools baseline**, then fewer tools/tokens while matching it (L132–136).
- **Required.** **Multiple baselines**: existing projects ("Executor", L367) **and published research methods** ("There are already many many research on this field. Why they not in your paper?", L370).
- **Recommended.** Small, cheap pilots, e.g. ~20 samples (L451).
- **Required.** **Findings beyond normal retrieval**: which approaches work in which cases and why (L144–152, L189–194).
  - The specific request to analyse why the student's LLM finder worked (L192–194) depends on the student's earlier work. Under the clean-room rules that work is closed until the Stage 5 reconciliation (U7). This investigation cannot do that analysis before then.

### 1.5 LLM use

- **Discouraged.** Deriving a deterministic mechanism from one LLM's reasoning trajectories (L219–236). The certainty tiers were dismissed as "just [LLM] as judge" (L216).
- **Agreed not novel.** Using an LLM on its own to find tools (L170–173).
- **Allowed.** Selective LLM query expansion after narrowing, including a 27B model, under a cost constraint that stays in place (L416–434). The cost constraint has no stated number (U6).

### 1.6 Working arrangement

- Frequent meetings. The supervisor will review the student's policy against "first principles" and then narrow the experiments (L456, L482). Who designs the policy is ambiguous (T11, U14).

## 2. What is not yet established

- **Supervisor assertions (A1–A13) are claims to test, not facts.** Two examples:
  - "Semantic search will always win over keyword search" (L255–259, L411).
  - The **hedged** claim that in "most" production systems ~50% token reduction is "low-hanging fruit" with no accuracy loss, "maybe not for NCP atlas I don't know" (L445–449).
  - The supervisor asked for one of them to be written down "as a fact" (L316). How to treat that is your decision (G-e).
- **Internal inconsistencies** (T1–T11). Examples:
  - The objective as tool count (L127–129) vs tokens (L316).
  - Keyword search "work[s] better for these cases" (L148–150) vs "will never work" (L285).
- **Student-reported results (P1–P9) are unverified** and are neither assumed correct nor incorrect.
- **Names of products, methods, models and benchmarks** are partly speech-recognition guesses (X1–X14).
- **Gemini notes.** There are 18 recorded discrepancies between the Gemini notes and the transcript (misstatements, overstatements and omissions; G1–G18). Example: "halt code execution" (L46) for a no-experiments-this-weekend instruction (L458). Only the transcript is used as evidence.

## 3. Proposed Stage 2 plan (landscape mapping)

### 3.1 Landscape questions

| ID | Question | Notes |
|---|---|---|
| L1 | Which **mechanisms** exist for reducing the context or tokens spent on tools by LLM agents, and how do they work? | Pre-specified families, searched or explicitly excluded with reasons. Labels marked † come from unverified background knowledge and are search leads only. (a) Retrieval/filtering (lexical, dense, hybrid, rerankers, LLM-based). (b) Tiered/partial or lazy exposure, on-demand tool search and meta-tools, fallback lookup. (c) Description compression/summarisation and generic prompt-compression applied to tool schemas†. (d) Query expansion/rewriting. (e) Hierarchical routing and sub-agent delegation† with small tool sets. (f) Training-based selection and models that internalise tools†. (g) Code-execution/programmatic tool exposure†. (h) Tool deduplication/merging/curation†. (i) Caching and provider-side features. (j) No intervention: long-context models. |
| L2 | What **evidence** does each report? Token/cost reduction, accuracy or task success, the mechanism's own overhead (extra turns, latency, failed lookups), turns considered, models, benchmarks, and how each is measured. | Extraction table with locations. |
| L3 | Which **benchmarks/workloads** test tool selection or use with large tool sets (MCP-based, single- and multi-turn)? What do they count as accuracy (gold-tool match vs task success), and what validity problems are documented? | Includes whether gold-tool evaluation misses valid alternative solutions, a point raised in the meeting (P7, L201–203). |
| L4 | What does the evidence say about the supervisor's assertions? | Priority A1–A7, A9, A12, A13; each has assigned searches (3.2). Support, contradiction or none found, with no verdict beyond the sources. |
| L5 | What is **industry practice**: vendor docs, MCP specification features, agent frameworks, gateways, startups? | Distinguish documented behaviour from claims; marketing kept only as "claimed". |
| L6 | How do **token-cost economics** interact with the objective? | Pricing, prompt caching of static tool lists, cache invalidation by dynamic tool lists, latency. |
| L7 | What are the **identities** behind uncertain names (X3 "Executor", X4 "MCP atlas", X7 "reinvoke", X8 "fit text", X12 "GLM 5.3 flash", X14 paper-writing skill) and behind A9's unnamed partial-information source? | Verify or mark unresolved. |
| L9 | **Validity and measurement of the research target (§0).** How do sources define and measure model-visible input tokens (definitions, outputs, history, reasoning, cached vs uncached), catalogue size, end-to-end task performance, and the overhead of discovery, selection and execution (extra turns, latency, failures)? Is the target worthwhile relative to other cost drivers? | Added in rev. 2 at the user's request. |
| L8 | **Disconfirming questions.** (a) What share of total agent tokens do tool definitions take, compared with history and tool outputs? (b) Do many tools harm accuracy, so that filtering helps, or are many tools harmless for strong models? (c) Is the problem already solved by vendor or protocol features (commoditisation)? (d) Do lazy/meta-tool designs lose more than they save once the extra turns are counted? | Any of these could weaken the objective or its novelty. |

Out of scope for Stage 2 (unless decided otherwise at G-f):
- running experiments or baselines;
- implementing a policy;
- assessing the student's earlier results (closed until Stage 5);
- interpretability of LLM reasoning;
- candidate research questions (Stage 4).

### 3.2 Search strategy

**Providers.** Each provider is logged separately and has stated limits.

| Provider | Role | Known limits |
|---|---|---|
| OpenAlex API (project skill) | Scholarly discovery; citation chaining | Lags on recent preprints; `--year-from` is exclusive; inspect `api_url` |
| arXiv API | Preprints (main venue in this field) | Preprints are not peer-reviewed; versions change |
| ACL Anthology | *ACL venues | Search interface or site search; may need WebFetch |
| OpenReview | ICLR/NeurIPS/COLM submissions | API or site search; withdrawn and rejected papers are visible and must be labelled |
| DBLP API | Venue and bibliographic coverage check | Metadata only |
| Semantic Scholar API | Second citation graph | Rate-limited without a key (429 seen at Stage 0); logged as blocked if so |
| Crossref API (project skill) | DOI metadata only | Not a relevance index |
| Hugging Face (datasets/papers) | Benchmark datasets | Metadata of uneven quality |
| GitHub REST API (unauthenticated, via curl) | Repositories, code, licences | 60 requests/hour; stars are not quality |
| WebSearch (Claude Code tool) | Industry, docs, grey literature | US-only. Backend provider not disclosed in the tool description. Results not reproducible over time. Each result must be re-located at a primary URL. |
| Official documentation (WebFetch / `fetch_source_text.py`) | Vendor and protocol docs | Pages change; store a copy with hash |

Not available: Google Scholar, Scopus, Web of Science, paywalled full texts. These are reported as coverage limits.

**Term matrix.** Pre-registered; every family combines one term from each column.

- Object: tool / function / API / plugin / skill / action / toolset / tool library / MCP server.
- Operation: retrieval / selection / filtering / routing / discovery / loading / exposure / compression / summarisation / recommendation.
- Setting: LLM / language-model agent / agentic / function calling / context window / context engineering / token cost.

**Query families.** Generic technical terms only; no transcript text.

| # | Family | Serves |
|---|---|---|
| F1 | Tool retrieval/selection for large tool sets | L1a, L4 (A1, A3) |
| F2 | On-demand tool search, lazy/dynamic loading, meta-tools, MCP tool discovery | L1b, L5, L8d |
| F3 | Tool description compression, partial schemas, prompt compression for tools | L1c, L4 (A13) |
| F4 | Query expansion/rewriting/hypothetical documents for tool retrieval | L1d, L4 (A5) |
| F5 | Lexical vs dense vs hybrid retrieval for APIs/tools | L4 (A1, A3, A10) |
| F6 | Benchmarks for tool use with many tools; MCP benchmarks; multi-turn tool use; evaluation validity | L3, L8b |
| F7 | Hierarchical routing, sub-agents, training-based selectors, code-execution exposure, tool deduplication | L1e–h |
| F8 | Token cost of tool definitions; prompt caching; cache invalidation; long-context alternatives | L6, L8a, L1i–j |
| F9 | Misleading/poisoned tool descriptions; LLM reliance on tool names | L4 (A4) |
| F10 | Cross-model transfer of tool-selection methods | L4 (A12) |
| F11 | Industry and grey literature: gateways, routers, tool-management products, engineering blogs, changelogs, curated lists (all labelled "claimed") | L5, L4 (A6, A7), L8c |
| F12 | **Bounded pre-2023 prior art:** web-service/API discovery and API recommendation from natural-language requests | L1, Stage 4 novelty risk. Limited to 2 query variants × 2 providers; extensions logged. |
| F13 | **Named-entity discovery leads** (authorized by the user, §0; short public names only, no transcript passages): "Executor" (tool search / MCP), "MCP-Atlas" / "MCP Atlas" benchmark, "Re-Invoke" tool retrieval, the "fit text" method (descriptive query only: "hypothesis generation tool retrieval"), "GLM flash" model, "paper writing skill Claude" | L7 |

**Window.** 2023-01-01 to the search date, plus F12 and IR background for A1/A5.

**Language.** English only. Non-English work is a stated coverage limit.

**Expansion.** Backward and forward chaining (OpenAlex; Semantic Scholar if available) from 3–5 seed sources per family. Chaining stops when a round adds no new relevant source, or after 2 rounds.

**Inclusion rules, by question type:**
- Mechanism and benchmark questions (L1–L3): addresses tool selection, exposure or token cost for LLM agents, and has a primary artifact.
- Assertion, economics and disconfirming questions (L4, L6, L8): any primary source that bears directly on the assertion.
- Industry (L5): official documentation or repository, or a "claimed" grey-literature item that names the product and mechanism.

**Exclusion:** no primary artifact; generic agent surveys without tool-selection content.

**Screening.** One screener (the primary author), with an exclusion log stating reasons. The challenger audits a random sample of max(10, 20%) of exclusions.

**Saturation and stopping (rev. 2).** Saturation is a **stopping heuristic only**. It never establishes comprehensive coverage or novelty.
- A "variant" changes at least one core term from the matrix.
- A family may stop when, in **at least two providers**, two consecutive variants add no new relevant primary source in their first 20 results.
- A family stopped by the 15-query cap rather than saturation is recorded as a **coverage limit**.
- **Coverage is reported only as a bounded statement:** "within providers P, queries Q, date window D and language E, these items were found". Never "the literature contains no X".
- **Coverage is assessed with independent signals**, each reported, none sufficient alone:
  1. **Known-item recall.** The challenger lists items it expects any adequate search to find, from its own replication and from resolved L7 entities, before seeing the final inclusion list. Each miss is reported.
  2. **Author–challenger overlap** on the replicated families.
  3. **Nearest-neighbour search.** For each mechanism category and each candidate "gap", targeted searches for the closest prior art, including forward and backward citation chaining from the strongest source found.
  4. **Grey-literature and production check** (F11) for categories where academic search found little.
  5. **Recency check.** A final pass on arXiv and vendor changelogs for the last 90 days, because OpenAlex lags.
- Absence of a found source is recorded as "none found under bounds B", never as a gap. Novelty is not assessed in Stage 2.
- **Consequence of a miss.** Each known-item miss triggers a logged follow-up search in the affected family. A miss that remains unexplained counts as a pivotal objection under criterion 11.
- **Definition of pivotal.** A source or claim is pivotal if a taxonomy category, a benchmark-table row, an assertion-map disposition, an L8/L9 answer, or a "strongest prior art" entry depends on it.

**Records.**
- `searches/`: search template, with provider, exact query, UTC timestamp, counts.
- `evidence/`: one source record per included item.
- An inclusion/exclusion log and an evidence map.
- Abstract or snippet reading is labelled as such. Full-text verification only from stored text with page/line locations (`fetch_source_text.py`).

### 3.3 Independent challenge in Stage 2

- The challenger chooses at least three query families to replicate, with alternate terms and at least one different provider.
- It spot-checks max(5, 20% of included sources) at random **plus all pivotal sources** against stored full text.
- It searches for contradicting evidence for each prioritised assertion.
- It audits the exclusion sample and produces the known-item list.
- Its report goes to `audits/`.

### 3.4 Stage 2 acceptance criteria

**PASS** requires all of 1–14 (criteria 13–14 added in rev. 2).

1. Each query family F1–F13 has search records in **at least two providers** and met the stopping condition (two consecutive non-yielding variants in each of two providers). The cap may be raised from 15 to 25 queries with a logged reason. A family stopped at the cap does **not** meet criterion 1: statements that depend on it are INCONCLUSIVE (STAGE_GATES, Stage 2 row).
2. Every included item has a source record. Every pivotal statement rests on inspected full text or official documentation, with location. Where a pivotal source is inaccessible, the dependent statement is marked INCONCLUSIVE.
3. A mechanism taxonomy (L1) covering every pre-specified family: sources, or "none found" with the searches behind it. Categories that emerge from sources are added. The report states that absence of evidence is not evidence of novelty.
4. An evidence-extraction table (L2) for every included mechanism source, with locations.
5. A benchmark table (L3): tool-set size, single/multi-turn, accuracy definition, token/cost metric, access/licence, and validity issues. "Not documented" is kept separate from "not searched".
6. An assertion map (L4): for each prioritised assertion, the searches run and the supporting, contradicting and missing evidence.
7. Industry and economics sections (L5, L6). Documented behaviour is separate from claims.
8. Identity resolution (L7) for each listed name: resolved with a primary source, or unresolved with the searches tried.
9. A disconfirming-evidence section (L8). Every L8 question is answered with evidence or "none found".
10. Inclusion/exclusion log, evidence map, and a coverage-limits section: blocked providers, paywalls, language, recency, publication-bias discussion, and the known-item recall result.
11. Challenger report present, and **no unresolved pivotal objection**.
12. Compliance: no transcript passages, identifying personal data or unpublished material sent to any provider (F13 short names allowed per §0); no previous-thesis material; no new experiments or benchmark runs (§0, G-f).
13. **Validity of the research target (L9)**: what "model-visible input tokens", "large tool catalogue", "end-to-end task performance" and "discovery/selection/execution overhead" can mean operationally, with sources for each candidate measure, and evidence that supports or undermines the target as a worthwhile objective.
14. **Coverage** reported as bounded statements, with all five coverage signals (§3.2) reported; saturation never cited as proof of completeness.

PASS requires 1–14 (rev. 2).

**Verdict mapping:**
- **FAIL:** a misquoted location, a fabricated or unverifiable record, or a compliance breach under 12.
- **INCONCLUSIVE:** blocked providers, inaccessible pivotal sources, families that stopped at the cap, or open pivotal objections.
- Never promote INCONCLUSIVE to PASS.

### 3.5 Relation to the supervisor's requested document

- Stage 2 delivers the "facts, projects, papers" part (§1.3).
- The supervisor also asked for a **draft step-by-step policy**. This protocol has no stage that designs a policy: Stage 4 produces candidate research questions and Stage 5 a feasibility recommendation. You choose at G-c.
- A dated, repeatable core-query set from Stage 2 can serve as the monthly review (§1.3).

## 4. Decisions at the Stage 1 gate

**Rev. 2: all items below were decided by the user on 2026-10-11 (see §0).** They are kept for the record.
- G-a1: replaced by the §0 research target.
- G-a2: approved, with L9 added.
- G-a3: search authorized without per-query approval.
- G-a4: approved, with criteria 13–14 added.
- G-b: not assumed; non-blocking.
- G-c: no policy design.
- G-d: names usable as discovery leads.
- G-e: hypotheses.
- G-f: no runs; feasibility investigation allowed.

### Approvals (historical: superseded by §0)

- **G-a1.** §1 as the statement of requirements. This includes treating "save tokens" (L316) as the operative objective over the earlier "minimal amount of tool" (L127–129).
- **G-a2.** The landscape questions L1–L8 and the out-of-scope list.
- **G-a3.** The **providers** in §3.2 and the **query families F1–F12**, sent with generic terms only. Required by STAGE_ROUTING and the project rules.
- **G-a4.** The acceptance criteria and verdict mapping in §3.4.

### Blocking decisions

- **G-b.** Did the Monday 2026-10-05 meeting (or any later one) happen?
  - If yes, supply its notes or transcript. They become a new source and Stage 1 is revised.
  - Proposed clean-room rule: anything presented there that is the student's previous work (results, designs, code) is set aside until the Stage 5 reconciliation. Only supervisor instructions are used.
- **G-c.** The supervisor's draft policy. Options:
  1. After Stage 2, produce an **interim policy sketch** for the supervisor, labelled speculation and grounded only in Stage 2 evidence, outside the formal gates.
  2. Defer any policy to after Stage 5.
  3. Add a formal policy-design stage between Stages 4 and 5 (a protocol change).

  The supervisor's weekend deadline has passed, so timing with the supervisor is yours to manage.
- **G-d.** Approve, edit or reject each **F13 term**. These are short names derived from the private transcript and are sent to public search providers only with your approval.
- **G-e.** Treat the supervisor's stated "facts" (A1–A13) as **hypotheses to test** (the clean-room default this plan assumes), or as working assumptions.
- **G-f.** U15, the conflict between L367 and L458/L482. Options:
  1. Stage 2 runs nothing (default).
  2. Stage 2 includes a **feasibility check** of "Executor" and other baselines: install and read documentation, no benchmark runs.
  3. Benchmark runs happen in a separate approved step after Stage 2.

### Handled inclusively unless you decide otherwise

These are not blocking: the search covers every option.
- **U3** benchmarks: all.
- **U4** single-step and multi-turn: both.
- **U8** MCP-only vs any function calling: both.

Left open for later stages: U1, U2, U5, U6, U12–U14, U16. **U7** (previous work) stays closed until Stage 5.

## 5. Stage 1 gate status

**Rev. 2:** Stage 1 is closed as **PASS (provisional user approval, 2026-10-11)** after the targeted re-review (`audits/A4-stage1-rereview.md`) and the fixes for B1 and B2. The status text below is the rev. 1 record.

Rev. 1 record: **INCONCLUSIVE.** The Stage 1 outputs are complete: meeting record (rev. 1), source record, independent reading, comparison, challenge of the brief, and this revised brief and plan. PASS requires approvals G-a1 to G-a4 and decisions G-b to G-f. The challenger's blocking items (A3, F17, F19 criterion 8, F21) are addressed in this revision but have not been re-reviewed by the challenger.

Revision log:
- rev. 0, `478687c`: initial draft.
- rev. 1, 2026-10-11 (`e193ff2`): responds to A3 findings F1–F21. See the "Primary-author response" table in A3.
- rev. 2, 2026-10-11: §0 user decisions. L9 and criteria 13–14 added; stopping rule revised. Targeted re-review A4: fixed B1 (F12 now 2 providers) and B2 (cap-stopped families do not meet criterion 1). Also N2 (no third-party code execution), N3 (miss consequence), N4 (pivotal defined), N6 (later-meeting rule in §0). N1 handled by marking §4 and §5 as historical. N5 (WebSearch backend undisclosed) is recorded as an accepted coverage limit.
