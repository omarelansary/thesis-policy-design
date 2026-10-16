# Evidence-based research integrity assessment: final report

- Date (UTC): 2026-10-15. Coordinator: Sonnet 5.5. This activity is not Stage 5. It selects, ranks and freezes no research question, resolves none of D-a to D-j, modifies no existing record, and executes no correction.
- Labels: **F** fact (stored record or log), **I** interpretation, **Inf** inference, **U** uncertainty. Every judgment below that rests on a model-written source is labelled as such.
- Full evidence: `phaseC/C-controlled-comparison-20261015.md` (with its errata), `phaseD/D1-review-20261015.md` (verbatim), `phaseD/D1-adjudication-20261015.md`, `streamA/`, `streamB/`, `FREEZE_MANIFEST.json`.

## 1. Evidence-based verdict

**Summary (I).** The investigation found no consequential problem that invalidates any of C1-C6 or shows that an important part of the scientific landscape was missed. It did find a recurring process defect in the historical stream that makes its "not found" gap claims less secure than their wording suggests, and the extent of that defect is not yet known. The correct overall label is **mixed, with one specified unresolved point**. The result is not "adequate" and not "inadequate".

**Well supported**
- The shared-region findings replicated in the fresh stream: the tradeoff is not universal; definition-token cost is real and large; restriction helped in single-step and weak-model settings and lost to full context on the one stateful benchmark (ComplexMCP, numbers verified against stored text); token savings do not equal billed-cost savings; vendor numbers are unreplicated and contain arithmetic inconsistencies (GitHub 27.5 vs 25.5; Anthropic 85% vs about 89%). The two inconsistencies were caught independently by the fresh workers and by the historical stream on 12-13 October (F: `STAGE2_FINAL_LANDSCAPE_REPORT` §5, `STAGE3_CLAIM_LEDGER` C3-10). These are replications of reading, not independent experiments.
- The historical process's self-correction: B1 and I found several corrections already recorded and traceable (replay-direction claim withdrawn in S4G v2, TheMCPCompany "12.5%" narrowed to 3 of 24, ToolHijacker 96.7% attribution corrected, "without fallback" withdrawn, the power-vs-error-rate misreading corrected).
- The recall/recovery region (C1, C2) is covered by sources (DynamicMCPBench, FitText, CAM-DF, TheMCPCompany, PlanBench-XL) that neither fresh worker reached in 24 searches each. That is a coverage-budget difference, not evidence against or for them.

**Partially supported**
- The "not found (2-3 queries)" gap statements for C1-C6. Each is correctly bounded in wording, but D1 verified at least four cases where an item present in the historical Stage 2 corpus was later stated to be missing, unlocated, or unused (see §3). Whether any C1-C6 prior-art statement is affected has **not** been tested.
- The independent corroboration of novelty: none exists. The fresh stream's silence about the historical near-neighbours says nothing about novelty.

**Unsupported or mis-stated (corrections of record, not of conclusions)**
- "Shi et al. … never in the corpus" (Stage 3): it was logged on 11 October (R2-C104, abstract-level, include). The finding drawn from the full text stands.
- "Executor is the supervisor-named baseline": label drift from "candidate match; referent unresolved" without new evidence (carried into the S4G client-side scope argument).
- "Are Tools All We Need?" described as "could not be located" in 4c: it was in Stage 2 (S2-0098).
- The "each step saves tokens: Required" reading: already corrected into an open [Sup]/[User] question in S4D-C2, S4E-V1 and S4G.

**Material omissions:** none demonstrated at the level of a missing candidate (see §4 for candidate-area items of undetermined significance).

**Inconclusive:** reach of the corpus-integration defect into C1-C6; effect of arXiv version differences on figures used by the candidates; whether the model's initiation of search or recovery should be a measured variable in C2/C6.

**Quality of this investigation itself (disclosure).** The first draft of Phase C had errors (it treated stored paper versions as ground truth and wrongly called three worker statements errors; it claimed no record explained the corpus-integration pattern). D1 found these and I corrected them (`phaseD/D1-adjudication-20261015.md`). D1 judged a mild net tilt toward the original research in the unrevised draft; the revisions address the specific items.

## 2. Landscape correspondence

| Independently discovered (A1 ∪ A2) | Historically investigated | Preserved candidates |
|---|---|---|
| Static definition cost and accounting | Stage 2 §1.4, §1.7 | C3 (token categories), C5 |
| Selection degradation vs count/length/similarity; no factorial | Stage 2 §1.5; 4c | C4, C1 (presence term) |
| Recall/discovery under restriction; trajectory loss | Stages 2-4c in depth | C1, C2 |
| Discovery overhead, turns, working set | 4b, S4F | C2, C3, C6 (cost side) |
| Under-invocation / "unknown unknowns" | Components in corpus (LiveMCPBench, MCP-Atlas, ToolMATH); not an outcome variable | None; S4D treats model- vs system-initiated recovery as a factor (L86) but no initiation measure appears in the S4G minimum designs |
| Data-flow / tool-result cost | Open user scope question | None (excluded by D9, user decision) |
| Cache/billing | Stage 2 §1.7, ETC, scaffold study; Toollery replay stored, lightly used | C5 |
| Catalogue quality; names, namespaces, collisions | Smells paper in corpus; MS interference only in a search-log row | C4(iv), C6 |
| Non-stationary catalogues | MCPEvol-Bench logged, never discussed | None |
| Security of discovery | D-SEC (coordinator/D4C scoping) | None |
| Delegation / partitioning; learned selection | Thin, assumption-based (B1 §4) | None |
| Latent-dependency-aware discovery (A1 O5) | No counterpart | None |
| Evaluation validity, replay, judges | Deeper than fresh stream | C5, S4F replay analysis |
| Staged-disclosure policy design | Shipped mechanisms read | C6 |

Genuine differences are preserved: the fresh workers treat evaluation methodology, invocation behaviour and catalogue evolution as co-equal opportunities; the historical process narrowed to omitted-tool recovery after 4b/4c because the supervisor-derived brief frames "a way to query omitted tools" as Required. A different taxonomy is not itself a defect.

## 3. Material discrepancies

| # | Claim and primary evidence | Historical provenance | Scientific consequence | Confidence | Resolvable by a check? |
|---|---|---|---|---|---|
| 1 | Stored-but-missed pattern: Shi et al. (R2-C104 vs "never in the corpus"), 2605.00136 (S2-0098 vs "could not be located"), FitText (R1 vs absent from S4D C2 list), Toollery cache replay (stored 13 Oct, used at abstract level). F, verified by me. Contemporaneous diagnosis: `audits/S4B-C2-…` L113 ("workers under-used the stored corpus"). | Multi-agent chain with partial reads and batch-entered logs; B1 §5.1 | Weakens the assumption behind C1-C6 "not found" statements; reach unknown | High on the four instances; low on reach | **Yes**: deterministic ID audit (§5 B-2) |
| 2 | Label drift: Executor "supervisor-named baseline" (transcript names "this executor" among several projects; "baseline" is interpretive). F. | Stage 2/3 "candidate match" to Stage 4c/S4G "named baseline" | Affects the client-side-scope argument (S4G §3, §5.2) | High on drift | Partly: a question to the supervisor already proposed (S4G §9 item 5) |
| 3 | arXiv version mismatch between corpus and fresh workers (MCPVerse v2/v1, MCP-Atlas v3/v1, LiveMCPBench v2/v1). F. | Corpus stored v2/v3/v2 on 11 Oct | A candidate figure from one version may not hold in another (e.g., MCP-Atlas tools per task: 6-37 in v3; 10-25 in v1 wording) | High that versions differ; unknown whether any candidate figure changes | **Yes**: store v1 texts; compare the specific values (§5 B-1) |
| 4 | Under-invocation: MCP-Atlas v3 "strong reasoning models refuse to invoke tools"; LiveMCPBench "~1 tool"; Vercel evals [vendor, unreplicated]. No initiation measure in C2/C6 minimum designs. | Evidence was in the corpus (ToolMATH, MCP-Atlas) | May bear on recovery-arm design and interpretation; not a missing candidate | Medium that it is a gap; low on materiality | Not by search; a design decision for the user |
| 5 | A1 O5, dependency-aware discovery: no counterpart in candidate or stage reports. | Method family deprioritised in 4b as "crowded" (evidence plus assumption, B1 §4) | Undetermined | Low | Not resolvable with current evidence |
| 6 | Toollery full-library cache-hit 0.989 with no billed-cost advantage for retrieval in natural replay (single-step BFCL). F, stored text L736-787. | Stored, read at abstract/intro level | Supports C5's premise; no candidate changes | Medium-high | No further check needed |

## 4. Consequences for research-question selection

- **Remain adequately supported for consideration:** C1-C6, as bounded candidates. Nothing in the fresh stream or in B1's reconstruction demonstrates invalidity of any.
- **Need a narrowly specified evidence update:** the "not found / could not be located / abstract only" statements underlying all six candidates' novelty descriptions (discrepancy 1), and the three paper-version comparisons (discrepancy 3). This is bounded, deterministic, and carries no change to the candidates themselves.
- **Need reformulation:** none established. The Executor scope wording (discrepancy 2) and the "Required" reading are already open questions for the supervisor/user.
- **Omit a genuinely important scientific opportunity:** not demonstrated. Under-invocation (4) and dependency-aware discovery (5) are of undetermined significance.
- **Cannot yet be judged:** whether any C1-C6 novelty statement is affected by the corpus-integration pattern; whether initiation of search/recovery changes the C2/C6 designs.
- No candidate is selected, ranked or frozen here.

## 5. Minimum justified next action

**Outcome B: a small, specified evidence gap requires targeted verification.** Not A: a verified recurring defect (discrepancy 1) with unknown reach on gap statements precludes an unqualified adequacy conclusion; D1 independently holds the same view. Not C: no material part of the landscape or process is shown to need reconsideration. Not D: the evidence is sufficient to distinguish these outcomes.

Bounded scope (**not executed**):

- **B-1.** Store arXiv v1 texts for the three papers via the existing text-fetch tool (three fetches, zero searches). Compare only the specific values used in candidate or stage records: MCP-Atlas tools per task and failure split, LiveMCPBench top-k ablation, MCPVerse Table 2/4. Output: a dated record listing which figures, if any, differ by version.
- **B-2.** A deterministic audit, zero web searches and zero model calls beyond the coordinator reading hits: enumerate each statement of the type "not found", "could not be located", "never in the corpus", "abstract only", "no logged query" in S4D, S4F (prior-art and uncertainty), S4E and S4G, and the Stage 3 ledger; match each by arXiv ID, title tokens and key terms against `evidence/stage2/consolidated.json`, the L2 extraction table and `evidence/source-text` manifests; a human reads each hit; output a table of statement, hits, and whether the hit is cited in the candidate's prior-art list. No candidate edits. Stop after the table.
- **Decision rule recorded in advance:** if B-2 finds no uncited near-neighbours bearing on a C1-C6 gap statement, the historical gap statements stand as bounded. If it does, those statements need a re-review before selection, to be authorised separately.
- Not authorised by this report: any new literature search, any change to candidate records, any selection.

## 6. Auditability

**Roles and models (as observed):**
| Role | Mechanism | Model evidence | Effort |
|---|---|---|---|
| A1, A2 | Bundled Claude Code CLI 2.1.300 (`claude.exe` from the VS Code extension; found, not installed), run from empty directories under the user Temp folder, outside the repository | init record: `claude-sonnet-5-5`; `modelUsage` also lists `claude-haiku-5-5` as the WebSearch/WebFetch helper | `--effort high` (flag passed; not echoed back by the CLI) |
| B1 | Same CLI, working directory = repository | `claude-sonnet-5-5` | `--effort high` |
| D1 | `independent-challenger` agent via the Agent tool, `model: opus`, `effort: high` | Not reported in the hand-back: **requested, not verified** | high (requested) |
| Coordinator | This session | Sonnet 5.5 | per session |

**Isolation conditions (F, `streamA/*_meta.json`, `inputs/canary_isolation_check.jsonl`):**
- A1/A2 flags: `--restricted --tools "WebSearch,WebFetch" --allowedTools WebSearch WebFetch --strict-mcp-config --disable-slash-commands --no-session-persistence`; init shows tools `[WebFetch, WebSearch]`, no MCP servers, no skills, cwd `…\Temp\indep-A1` / `indep-A2`, `apiKeySource: none` (subscription login, no API key, no paid API use). A content-free canary confirmed no CLAUDE.md or memory in context and a failed `file://` read of the repo's CLAUDE.md. Tool-call logs show only WebSearch and WebFetch, with no repository terms in queries (D1 check).
- B1 flags: `--restricted --tools Read,Grep,Glob` with deny rules for `infrastructure/upstream/`, `tmp/`, `.git/`; file tools confined to the repository. B1's tool-call log shows no excluded paths; it read the admitted 2 October transcript passages only for requirement classification. No 14 October material exists in the repository.
- A1, A2 and B1 ran concurrently (user-permitted for this activity; the repo's standing "one at a time" rule was not followed); no writes were possible for any of them.
- A1/A2 exact prompt: `inputs/seed.txt` (written by the user, passed unchanged via stdin; sha256 below). B1 prompt: `inputs/b1_prompt.txt`. D1 prompt: `phaseD/D1-prompt.md`.

**Search logs:** `streamA/A1/A1_toolcalls.tsv` and `streamA/A2/A2_toolcalls.tsv` (every call and input). Counts: A1 24 WebSearch + 28 WebFetch, 53 turns; A2 24 WebSearch + 28 WebFetch, 53 turns; B1 26 Glob + 40 Grep + 104 Read, 171 turns. Zero identical search strings between A1 and A2; 12 shared fetch targets (normalised) of 23/21.

**Freeze hashes (SHA-256; manifest `FREEZE_MANIFEST.json`, frozen 2026-10-15T17:30:32Z at repository HEAD 7cf3674; committed e4f7178):**
- `inputs/seed.txt` 3e47571cedf334e8ae81a3cfda3c35c960d6b2954b1e204cffe9073995f364fe
- `streamA/A1/A1_report.md` 66d0a1d7840dc41cc151b306a5299628c0811bc35260ee216c79536bbc8ab46e
- `streamA/A2/A2_report.md` 24540b35d3ee5ba4abce071b7a5a5c74913474dff4280e463347be1f6fdb420b
- `streamB/B1/B1_report.md` 701e3bf7221c50b4ea6b3072e257006cd132715efb810493b1c2559ae54ae611
- Raw streams and launch scripts: see manifest.
- Phase C committed as 76f8cf9 before D1 read it; errata appended afterwards.

**Reviewer and adjudication:** `phaseD/D1-review-20261015.md` (verbatim; indentation removed), `phaseD/D1-adjudication-20261015.md` (14 objections: 10 confirmed or partly confirmed with corrections, 1 attribution unsupported within an otherwise confirmed objection, 3 unresolved or demoted).

**Limits of reproducibility and independence:**
- The fresh workers were not independent of the historical stream in model family, search backend, account, summariser model, or parametric priors; they were context- and repository-blind. Their readings pass through a small summariser model and 100K-character truncation; web content changes over time; the WebSearch backend is undisclosed.
- The coordinator (Sonnet 5.5), B1 (Sonnet 5.5) and the historical authors share a model family (self-review risk).
- B1 read selectively (many partial reads); its traceability matrix is a sample, not a census. Its row 14 was wrong (raw/delivered wording).
- Checks against stored texts test claims against the corpus's own versions, which differ from what the workers read in three cases.
- D1's model identity is unverified; D1's web checks are summary-level.
- The A/B/D runs were not repeated; model outputs are not deterministic.

**Files created (all new, under `integrity-investigation-20261015/`):** `.gitattributes` (`* -text`, so hashes stay stable), `FREEZE_MANIFEST.json`, `FINAL-REPORT-20261015.md`, `inputs/` (seed, B1 prompt, launchers, canary), `streamA/A1/`, `streamA/A2/`, `streamB/B1/` (reports, metadata, tool-call logs, raw streams, start/finish times), `phaseC/` (comparison with errata, crosswalk output and script), `phaseD/` (D1 prompt, review, adjudication). No existing file was modified. Commits: e4f7178 (freeze), 76f8cf9 (Phase C), and the final commit containing Phase D and this report.
**Files outside the repository (created by this activity, not committed):** `C:\Users\omr\AppData\Local\Temp\indep-A1`, `indep-A2`, `indep-canary` (empty working directories), `indep-seed\` (seed, prompts, launchers), `indep-out\`, `indep-outB\`, `indep-canary-out.jsonl`; coordinator scratch under the session scratchpad. `tmp/` in the repository is pre-existing and untouched.

**Stopped.** No correction, reselection or Stage 5 activity has been started.
