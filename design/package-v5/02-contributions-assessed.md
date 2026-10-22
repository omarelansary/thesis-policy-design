# 02. The three voices assessed: supervisor, student, assistant (V5, AUTH-020)

Status: provisional, lead, 2026-10-22. Rule (plan section A row 7): rows the register classes as **requirements** are inputs; V5 states how it meets each and never grades them. Rows classed as **assertions** are checked against evidence as "consistent / in tension / not addressed", with what would settle each. The supervisor's files-not-context and "hello/hi" remarks are illustrations of the aim, not claims to test (REQ-U21-12). Nobody is called right or wrong.

## (a) The supervisor's requirements, and how V5-R meets them
| Requirement | V5-R (`04`) |
|---|---|
| REQ-O14F-01 the research question (count of tools, accuracy as high as possible) | The count is the means; the bill is the objective as the human set it (REQ-U21-07); the number of tools offered is reported per turn |
| REQ-O21-01 memory and tool calls only; REQ-O21-03 tool question-answer pairs and a short summary, relevant part first, more when asked | M1 loads the short summary and an index of past tool question-answer pairs; full entries only when the model asks (memory tool view); W writes them; knowledge retrieval is out |
| REQ-O21-02 whether conversation memory belongs depends on what is built | Kept to a short summary in service of tool calls (its length is a decision, `04` section 7) |
| REQ-O21-07 recover at a higher cost on a few turns; judge on average | Discovery D is the recovery; the bill is averaged (DPR-0006 section 4) |
| REQ-O21-08 any kind of agent | No domain assumption in any stage; S1 is per deployment |
| REQ-O21-09 plain Markdown memory first, "don't engineer it at all"; big experiment for publishable numbers | V5-R05; `05` loop first, end-to-end later |
| REQ-O14F-06 staged graph, one question per stage, open count, a filtered tool may come back | **Met in reduced form.** Three stages decide which tools the model sees: S1 (deployment configuration), M2 (gated memory-informed offering) and D (discovery); S2 chooses a prefix layout and W writes memory. A tool held back by M2 or by deferral comes back through D; a tool excluded by S1 does not (S1 is the deployment's permission set). Multi-step narrowing is not a separate stage (`04` section 3); each stage is kept only if `05` shows it pays |
| REQ-O14F-04 stage one filters by who invokes | S1 deployment filter |
| REQ-O14F-05 Executor-style listing or semantic narrowing, possibly in several steps | Vendor deferral and search (D), with a ranker inside D; multi-level retrieval exists in research (AnyTool) and Copilot ships two levels, but no multi-stage run-time policy measured on the bill was found in a limited search (`03` section 4), so several steps are not a separate stage in the default |
| REQ-O02-01 all-tools baseline; REQ-O02-06 Executor baseline, several baselines | K0, DPR-0008, DPR-0009 and K1 as baselines; the Executor arm is required but defined only after its MCP surface is read (`05` P0), so it is not yet specified |
| REQ-O02-02 filtering must not cost more than it saves; REQ-O02-08 cost constraint stays with a helper model | Every stage's requests are in the bill (DPR-0006 section 3); no helper model in the default |
| REQ-O02-09 each step saves tokens; a way to query held-back tools; judged over turns | D; the bill per turn averaged over turns |
| REQ-O02-07 keep the earlier work in a branch, start by analysing what is available | V5 is on its own branch and starts from the reuse map |
| REQ-O14F-02 a negative result is still a thesis | "No improvement established" stays an admissible verdict (`04` section 8) |
| REQ-O21-10, REQ-O14F-07, REQ-O02-10 (dates, small first experiments) | Recorded; `05` starts small |

## (b) The supervisor's assertions against the evidence
| Assertion | Status | Evidence | What would settle it |
|---|---|---|---|
| REQ-O21-04 / AS-15: information added to an explicit cache can stay for the whole conversation at negligible cost | His words: "keep them always ... for the whole conversation ... because explicit cash is negligible price and let's say you are talking with that person for 1 hour that is still negligible" (INT-T-002 L209); he raises the return case himself right after (L211), answers that not everything should be given again "just by saying hi" (L219), and calls the passage "all in theory" (L221). V5-R follows L219: memory seeds wait for the first user turn that names a task (`04` section 3). **Consistent with the stored prices within one conversation, compared with re-sending**: after a 1.25x write each cached request costs 0.1x of input, 0.21 of re-sending after 10 requests. **Not addressed by him, and growing**: compared with not adding the tokens, each request adds 0.1 of a fresh send (2.15 fresh sends after 10, 11.15 after 100); within one hour that holds only if requests keep the cache alive (5-minute lifetime, or the 2x 1-hour write); Gemini explicit caches also charge storage per hour. "Negligible" and "explicit cache" are not defined in the transcript | INT-T-002 L209, L211, L219, L221; D-02 part 2 (`calc/memory_seed.stdout.txt`); FND-0039; DPR-0006 section 3 | One billing probe per provider used (ledger C-X07); his definition of "negligible" |
| REQ-O21-05: tool responses in files, searched when needed, "save around 80%" | Illustration of the aim (REQ-U21-12). Direction consistent for long tool-heavy runs (masking halved cost in coding agents); magnitude workload-dependent (programmatic calling -38% on one benchmark, +8% on another; tool outputs about 3.3% of cost in coding agents) | `03` section 6 | Not needed as a claim; the PoC measures the result share of our workload |
| REQ-O21-06: "hello" can cost 10,000 tokens | Illustration (REQ-U21-12). Mechanism consistent: every definition is sent with every request (FND-0038 row AS-14); the fixed prefix carried 74.7% of the bill in one study | FND-0038; `03` section 6 | One usage-field reading on our setup |
| REQ-O14F-03: nothing here is groundbreaking; the novelty is the combination; the staged graph "is your novelty" | Consistent with "nothing groundbreaking": every mechanism exists, including hierarchical retrieval and personalized tool memory (`03` sections 4-5). On the combination: no source was found, in a limited search, that seeds tool definitions per user from a large catalogue with the bill measured (`03` section 5, missing-conjunct row). The staged part of V5-R is its smallest part (`04` section 3), so "the staged graph is the novelty" is not what V5 would defend | `03`; `inputs/search-log-20261022.md` section 2 | A wider search |
| REQ-O02-05 / AS-09: the partial-information idea comes from someone else's documentation; Executor does the same | Consistent in part: vendors ship tiers of partial information. OpenAI shows an individually deferred function's name and description and defers its schema; a namespace shows only its own name and description; Claude Code defers MCP tools by default (`03` section 3). Whose documentation the supervisor meant is not identified (Q-J28). Executor's README shows a shared catalogue with intent search and per-tool policy (`03` section 4) | L/v5-openai-tool-search-20261022.md:22; L/v5-claudecode-mcp-20261022.md:1441; L/v5-executor-readme-20261022.md:5-7, :123 | The supervisor names the source |
| AS-07: Executor exposes connection prefixes and meta-tools instead of all tools | Not addressed by the stored README (it describes the catalogue and policy, not the MCP surface); the meta-tool surface is scout-reported from a third-party mirror | `03` section 4 | Read Executor's own MCP documentation when pinning the version |
| AS-13: filtering 100 to 60 is a safe big win; names only for the lowest tier keeps accuracy | Not addressed as a number (no source has the 100-to-60 step); the names-and-descriptions tier exists in vendor products (above) but its accuracy effect is not reported | FND-0038 row AS-13; `03` section 3 | A graded-exposure arm in `05`, if the loop needs it |
| AS-06: about 50% reduction with no accuracy loss is low-hanging fruit | **Unverified reading**: FND-0038 row AS-06 says the universal form does not hold (method matters), but that row rests on the ledger's batch-12 text, which FND-0038 itself marks as not re-read at source. Not needed as a number under REQ-U21-07 | FND-0038 row AS-06 ("not re-read here") | Re-read the batch-12 sources if the claim is ever used |
| AS-12: LLM behaviour does not transfer across models | **Unverified reading**: FND-0038 row AS-12 (signs mostly shared, sizes vary) rests on the same un-re-read ledger text | FND-0038 row AS-12 | End-to-end study on more than one model |
| AS-02, AS-08, AS-10, AS-11 | Not addressed by V5 (background or analogy claims; ledger keeps them as limitations) | ledger | — |

## (c) The student's inputs
| Input | Verdict | Reason |
|---|---|---|
| Tool memory as the memory scope (the draft reply recorded in V4 `04` section 6) | **Keep, widened**: the supervisor's answer includes tool question-answer pairs and a short summary (REQ-O21-03); V5-R carries both | REQ-O21-03 |
| A one-hour idle-gap rule (INT-T-002 L331-L345, no yes or no from the supervisor) | **Revise**: becomes the cache-lifetime choice per deployment by expected gap (DPR-0006 gap cost; `04` section 7 keeps it a decision) | DPR-0006 section 3 |
| Bill, not tokens; model-agnostic equation (INT-T-005) | A decision, not graded; implemented as DPR-0006 | REQ-U21-07 |
| Staged and memory combined (INT-T-005) | A decision; implemented as M2 after the shared prefix, in the tested policy for returning users and tested in `05` P1 (REQ-J22-01); D-02 gives the threshold for reading the result | REQ-U21-04 |
| The June exposé ideas | Deferred by the human until V5 is finished (AUTH-020) | — |
| The 21 Oct briefing (eleven ideas, reuse hypothesis, seed map) | Not available in the workspace; not assessed (plan row 20) | — |

## (d) The assistant's inputs (earlier lead work)
| Input | Verdict | Reason |
|---|---|---|
| V4's token criterion | **Drop** | Replaced by REQ-U21-07 |
| V4's request-level system selector (P1) and system trigger (P3) as optional stages | **Trigger: drop from the default. Selector: replace by a ranker inside D** | No source supports the trigger; a model-answered selector adds a request, while an embedding ranker adds an embedding call instead [I] (EXT-0228 does not state this; its embedding cost is not yet a DPR-0006 term), so V5-R uses a ranker inside D instead of a separate selector stage |
| V4's append-only rule for added tools | **Keep** | Now stated by two providers (`03` sections 2-3) |
| V4's "show everything may win at small sizes" | **Keep, bounded** | D-01: below a break-even between about 10 and 230 tools (depending on searches per session, definition length and whether the small core caches), and only if the block caches |
| V4 `04` cost model and memory options (M-a, M-b) | **Keep, superseded** by DPR-0006 and V5-R's M1-W | — |
| V4 `04` risk that per-user seeds split a shared cache | **Keep, resolved in design** | V5-R06 places seeds after the shared prefix via slot 2 |
| DPR-0006 bill equation | **Keep unchanged** | Reviewed (RV-0020) |
| The original V5 plan's "both criteria, always" | **Drop** | Contradicts REQ-U21-07 (plan section A row 3) |
