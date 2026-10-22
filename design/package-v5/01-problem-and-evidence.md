# 01. The problem, the blind designs, and the decisive claims (V5, AUTH-020)

Status: provisional, lead, 2026-10-22. Nothing validated, approved or final. Requirements are quoted by register id (`requirements/REGISTER.md` section H); they are inputs and are not graded here.

## 1. The problem as the decision-makers set it
- **Research-question sentence (supervisor's).** "which method is the most optimal way to reduce the count of tools while keeping the accuracy as high as possible", "We don't need to change it" (REQ-O14F-01). Entering it in `requirements/THESIS_QUESTION.md` stays the human's decision. The supervisor states both the count and token saving (REQ-O02-03, REQ-O02-09); reading tokens as the aim and the count as the means is the ledger's reading (Q-J02, REGISTER H.2), not his statement.
- **Objective (the human's decision).** Minimise the bill on average over turns and sessions while accuracy stays **nearly the same**; no margin, budget or hard threshold; a model-agnostic billing equation (REQ-U21-07). Note the wording difference: the supervisor says accuracy "as high as possible", the human "nearly the same"; V5 follows the human's decision and reports accuracy beside the bill so either reading can be applied. The equation is DPR-0006 (proposed, reviewed in RV-0020); V5 uses it unchanged.
- **Standard of success.** The quality of the work: every scientific and engineering approach considered, nothing missed (REQ-U21-11); the gaps V5 leaves are listed in `03` and the search log, not hidden.
- **Scope.** Memory and tool calls only; memory serves tool calls; conversation memory as a short summary (REQ-O21-01, REQ-O21-03). Knowledge retrieval is out.
- **Form.** The staged policy and memory deciding which tools are offered are one combined policy (REQ-U21-04). Stages: one question per stage, number of stages open, a filtered tool may come back later (REQ-O14F-06); a way to ask for held-back tools (REQ-O02-09).
- **Horizon.** Averaged over many turns; a dearer recovery turn is acceptable (REQ-O21-07); sessions are one long run or returning users (REQ-U21-10); any kind of agent (REQ-O21-08).
- **Baselines.** All tools (REQ-O02-01); Executor (REQ-O02-06); several baselines.
- **Process.** Research and a drafted policy; a proof-of-concept loop with plain Markdown memory, "don't engineer it at all" until results; then an end-to-end study with repeated runs (REQ-U21-06, REQ-O21-09). Models are chosen when implementing, through the university API (REQ-U21-08, REQ-U21-01).
- **Principle.** Reuse what research, large companies or widely used open source already tested (REQ-U21-03). The earlier 27-method retrieval work stays out (REQ-U21-02); read together with REQ-U21-03, earlier work enters only when the human places it explicitly and it is verified (REGISTER H.3 relation). The June exposé's ideas are candidates to keep or drop with a reason (REQ-U21-05); by the human's 22 Oct decision they are tested only after V5 is finished (AUTH-020 limits).

**Decision points** (lead's reading [I], consistent with both blind instances): D0 session start or return (known: deployment, invoker, memory, time since the last request, catalogue); D1 each user turn (known: message, history, memory); D2 each model request inside a turn (known: tool results, the model's own requests); D3 end of turn or session (what to write to memory). The bill terms at each are DPR-0006 section 2; the cold-start and gap terms are DPR-0006 section 3.

## 2. The two blind designs (thread T-20261022-113)
Both outputs are stored verbatim: `inputs/blind-output-A-20261022.md` (SHA-256 `f730ca31…d679`, including a lead's note at the end on the independence check) and `inputs/blind-output-B-20261022.md` (`01e85a50…e1aa`); prompt `inputs/blind-prompt-20261022.md` (`cd74a7b6…584e`). Both instances received CLAUDE.md and ops/STATE.md automatically (which name the earlier packages); both state they opened neither earlier package. Instance A read lines 100-189 of the 21 Oct file, which include machine-written notes, and states it used only transcript lines. The tool logs were not inspected line by line; the check rests on the instances' own path lists.

| Part | A (evidence-led) | B (simplest-first) | Agreement |
|---|---|---|---|
| Stable cached prefix | P0: system, small core, category index | S0: all tools, byte-stable, caching on | Both make the cached prefix the base |
| Invoker or role filter at session start | P1 | P1 | Both |
| Deferral plus search, append-only | P2 | P3 | Both; both cite the vendor statement that appends keep the prefix |
| Memory | P3 read and P5 write (tool question-answer pairs plus a 3-4 line summary; memory may pre-load tools) | P2 summary at session end, injected next session; memory-informed pre-loading deferred until search round trips are measured | Both keep a short summary; they differ on memory choosing tools |
| Cache lifetime and keep-alive | not a part | P4 (5 min against 1 h against keep-alive) | B only |
| Tool results out of context | P4 conditional | considered, not added (tool outputs about 3.3% of cost in coding agents) | Both treat it as conditional |
| Multi-stage narrowing (1,000 to 10) | cut: no evidence that extra stages pay; each adds a request and a cache risk | not added; trigger: catalogue still too large after the filter and deferral | Both leave it out |
| Simplest rival | R0 all tools, caching, summary; R1 static core plus native tool search ("likelier practical winner") | Rival A = S0; rival B shell and filesystem; rival C a cheaper model | Both name expose-all with caching as the rival |
| Missing knowledge | cache sharing across users; university API caching; memory versus full history on the bill | same, plus the gap distribution and university API cache fields | Same core gaps |

**What neither blind instance had.** Their allow-list held the provider pages stored on 2026-10-11 and 2026-10-19. The scouts found the current Anthropic mid-conversation tool changes (`tool_addition`/`tool_removal`, beta), which let a stage change what is *offered* per turn while the cached prefix stays intact (`03` section 2). That one mechanism changes the trade-off both designs reasoned about (`04` section 3).

## 3. Decisive claims V5 relies on, re-read against primary text
Labels as in CLAUDE.md. "Lead" = read by the lead at the cited lines in this session; "steward" = checked in T-20261022-115 (`03` section 11).

| # | Claim | Label | Pointer | Checked |
|---|---|---|---|---|
| C1 | The cache is a prefix hierarchy tools, system, messages; a change invalidates that level and all after; `tool_choice` changes invalidate only messages (Anthropic) | [F] | L/v5-anthropic-tool-use-caching-20261022.md:57-63 | lead |
| C2 | Deferred tools are not in the prefix; discovered definitions are appended inline; the prefix is untouched (Anthropic) | [F] | same file :49 | lead |
| C3 | OpenAI tool search injects discovered tools at the end; changing the loaded tool set breaks the cache from that point; gpt-5.4 and later only | [F] | L/v5-openai-tool-search-20261022.md:5, :7, :860 | lead |
| C4 | OpenAI: restrict with `allowed_tools` while keeping `tools` stable | [F] | L/v5-openai-prompt-caching-20261022.md:440-441 | lead |
| C5 | Anthropic: offer or withdraw tools per turn with the `tools` array unchanged, cache intact; beta; by-value addition keeps the cache except when no non-deferred tool exists | [F] | L/v5-anthropic-midconv-sysmsg-20261022.md:20, :27, :452 | lead |
| C6 | Any change to the available tool set invalidates the cached prefix; caching cut cost 41-80% in one multi-turn agent study | [F, one study] | L/v5-dontbreakcache-2601.06007v2.txt:33, :525-527 | lead |
| C7 | In coding-agent workloads the harness base (system prompt and tool definitions together) was 74.7% of a reconstructed cost; accessible content about 6%; tool outputs about 3.3%. It does not separate the tool block from the system prompt | [F, one study, coding agents] | L/pdf-tokennotcost-2607.12161v5.txt:200-224, :240-243, :298 | lead (scope noted after CH-0101) |
| C8 | Observation masking more than halved cost against the raw agent at equal solve rate (coding agents) | [F, one study] | L/v5-complexitytrap-2508.21433.txt:24, :96-100 | lead |
| C9 | A small tool block can fall below the minimum cacheable length and not cache; one added tool re-wrote a 4,082-token block | [F as a self-reported measurement] | L/v5-synthorai-mcp-overhead-20261022.txt:176 | lead |
| C10 | In 506 local session logs, 2,766 cache-bust events re-billed 224.4M input tokens, 13.5% of spend; 1,399 mid-session tool, skill or MCP-list mutations occurred in 38% of sessions; the commenter links the busts to tool schemas entering after the first request, but the 13.5% is attributed to all cache-bust events, not to tool-list changes alone | [F as a user report] | L/v5-ccissue-92033-cachebust-20261022.txt:180-192 | lead (corrected after CH-0093) |
| C11 | Executor is an open-source integration layer with one shared catalogue, per-tool policy and intent search | [F] | L/v5-executor-readme-20261022.md:5-7, :28-32, :123 | lead |
| C12 | Vendor tool-search accuracy gains (49% to 74%) | vendor performance claim, not established | L/v5-anthropic-advanced-tool-use-20261022.txt | not re-read; not relied on |
| C13 | Personalized tool memory exists over small tool sets (PRTA, memory-conditioned tool calling); no source was found that seeds tool definitions per user from a large catalogue at session start with the bill measured | not found in a limited search | `inputs/search-log-20261022.md` section 2; `03` section 5 | lead (revised after CH-0090, CH-0091) |

## 4. The V4 claims, against this evidence
| V4 position (`design/package-v4/01`) | V5 reading |
|---|---|
| Criterion: input tokens, the bill recorded separately | Replaced by the human's bill objective (REQ-U21-07); tokens remain components of DPR-0006 |
| Memory and sessions omitted (V4 `04` section 1 records the omission) | Required now (REQ-U21-04, REQ-U21-10); `04` adds them |
| Append-only default for added tools rests on vendor statements, not a measurement (V4 `04` section 3) | Still a vendor statement, now from two providers (C2, C3) and with a by-reference offering mechanism (C5); the effect in our setting is still OURS |
| "Show everything" may win at small catalogues | Supported in bill terms below a break-even size between about 10 and 170 tools, depending on searches per session, definition length and whether the small core caches (`calc/regime_bill.stdout.txt`, revision 2), and only where the tool block caches (C9) |
| The staged form's content is an output of a study | Kept: stages are kept only where `05` shows they pay |
| No novelty claim | Kept |
