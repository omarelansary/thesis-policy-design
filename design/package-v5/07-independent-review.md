# 07. Independent review and adjudication (thread T-20261022-117, AUTH-020)

Status: provisional, lead, 2026-10-22. Two design-challenger instances reviewed V5 on disjoint slices; a third (rebuttal) instance then checked the lead's dispositions (RV-0023, section 4). Challenge records stay `open` in their files (the plan does not change CH statuses); the outcome of each is recorded here.

- **Slice A** (design, calculations, proposals, hypotheses): `reviews/RV-0021.md`, 18 numbered objections; `challenges/CH-0075..CH-0089` (1 blocking, 14 should-fix). The challenger had no code execution and checked the arithmetic by hand; the lead's script reruns confirmed its figures.
- **Slice B** (problem, contributions, reuse map, search log): `challenges/CH-0090..CH-0104` (1 blocking, 11 should-fix, 3 notes). The instance stopped at its turn limit before writing its review file, so **there is no RV-0022**; the challenge records are complete and are indexed below.

## 1. Slice A dispositions
| CH | Severity | Objection (short) | Disposition | What changed |
|---|---|---|---|---|
| CH-0075 | blocking | h* omits the longer carry of needed seeds and prices every avoided search as an extra request | **Conceded** | `calc/memory_seed.py` revision 2 (both discovery modes); rerun gives 0.23-0.99 (client) and 0.30-never (server), matching the challenger's hand figures; `04` section 1 sentence 3 and the M2 gate; DPR-0007, HYP-0017. HYP-0016 (proposer's) quotes the old range and is flagged here, not edited by the lead |
| CH-0076 | should-fix | discovery priced as an extra request, unlike server-side search | **Conceded** | D-01 revision 2 computes both modes; n* moves by a few tools (table B) |
| CH-0077 | should-fix | minimum cacheable length applies to the whole prefix; deferral prefix not checked | **Conceded** | D-01 uncached-core variant; n* rises to 24-168 (table B); `04` section 2 |
| CH-0078 | should-fix | every session is priced cold; R-return is not a separate regime; the shared prefix contradicts a per-return write | **Conceded** | R-return removed as a regime; table E shows the cold/warm difference only; `04` section 2 states that request rate across users decides warmth |
| CH-0079 | should-fix | a stored report of deferred definitions re-read every call is not weighed | **Conceded** | row added in `03` section 3; `04` section 5; `05` P5 checks it and moves to second place |
| CH-0080 | should-fix | headline ratios and boundaries hold only for small D and one definition length | **Conceded** | D-01 tables A-C; `04` sections 1-2 give the conditions; "2-30x" removed |
| CH-0081 | should-fix | the regime switch is not new; "recommended" rests on a requirement | **Conceded** | `06`: regime switch reused; DPR-0007 revision 2 says V5-R = DPR-0008 + S1 + gated M2, kept only because REQ-U21-04 requires the combination |
| CH-0082 | should-fix | masking in the default on one study | **Conceded** | H removed from the default; `05` P4 only for deployments with large results; beta noted |
| CH-0083 | should-fix | selector and trigger dropped by an uneven standard | **Conceded in part** | V5-R07 revised: trigger out (no source); selector replaced by a ranker inside D (embedding routing adds no model request); M2 held to the same standard by the gate. The lead keeps "each model-answered stage adds a request" as stated |
| CH-0084 | should-fix | REQ-O14F-06, REQ-O02-06, REQ-O21-03 met only nominally | **Conceded** | `02` and `04` section 3: REQ-O14F-06 "met in reduced form" (S1-excluded tools do not come back); Executor arm "required, not yet specified"; M1 now loads a summary and an index, full entries on request |
| CH-0085 | should-fix | vendor performance numbers used despite the disclaimer; Copilot's "future work" overstated | **Conceded** | `04` K0 row marks Copilot's 2-5 points "not relied on"; `03` Copilot row reworded; HYP-0017 basis reworded |
| CH-0086 | should-fix | beta and provider-specific features with no fallback; P0 cannot observe the discount | **Conceded** | `04` section 5 "Provider routes"; HYP-0020 falsifier narrowed to the observable part |
| CH-0087 | should-fix | P1 cannot end its question | **Conceded** | `05` P1 now measures h from same-user histories at a size above n*, excludes core tools, recomputes h* from observed values, and does not try to detect the bill difference directly |
| CH-0088 | should-fix | no decision rule separates "nearly the same" from "lower" | **Conceded** | `05` section 1: what about 20 samples can and cannot show; a stated asymmetric rule (the loop may remove parts, not prove them) |
| CH-0089 | should-fix | order is not dependency order; V5-R09 omits P5 | **Conceded** | order P0, P5, P3, P1, P2, P4 in `05` and V5-R09; P0 and P5 described as readings of our route, not re-tests |
| RV-0021 items 16-18 | notes | trace_check shows existence only; V5-R bill cell empty; HYP-0016/0017 measure one quantity | **Accepted** | `06` states what the check shows; `04` V5-R row now gives the M2 term's range; HYP-0016 and HYP-0017 are to be merged by their authors (the proposer owns HYP-0016) |

## 2. Slice B dispositions
| CH | Severity | Objection (short) | Disposition | What changed |
|---|---|---|---|---|
| CH-0090 | blocking | NONE FOUND rows not supported by the search log | **Conceded; resolved by searching** | four targeted searches by the lead, logged in full (`inputs/search-log-20261022.md` section 2); two absences overturned (hierarchical retrieval; personalized tool memory), one narrowed (a multi-session cache-billed harness exists), the rest reworded "NOT FOUND in a limited search"; blind instances no longer cited as support for open-web negatives |
| CH-0091 | should-fix | the slot-5 negative is a four-way conjunction | **Conceded** | `03` section 5 "which conjunct is missing" row; `02` REQ-O14F-03 row and `06` reworded |
| CH-0092 | should-fix | stored sources for the opposite conclusion missing | **Conceded** | rows added: memory-carrier cost (memskill), practitioner case for stable tool sets, skills progressive disclosure (measured library) |
| CH-0093 | should-fix | C10 attributes 13.5% to tool-list changes | **Conceded** | `01` C10 and `03` section 1 corrected (13.5% is all cache-bust events) |
| CH-0094 | should-fix | masking result carried into a cached-prefix bill without the pricing caveat | **Conceded** | `03` section 6 carries the paper's own cache findings and pricing caveat; H is not in the default |
| CH-0095 | should-fix | OpenAI `additional_tools` omitted; "two providers" not tied to the student's API | **Conceded** | `03` section 2 row; `04` sentence 2 and section 5 routes; `03` section 10 item 1 widened |
| CH-0096 | should-fix | Copilot row overstates "future work" and understates its usage-based core | **Conceded** | `03` section 4 reworded; the gap is stated as per-user or per-role seeding |
| CH-0097 | should-fix | the caching-assertion verdict omits his hedge and return-case remark | **Conceded** | `02` row now quotes INT-T-002 L209, L213, L221 and separates what he said from what he did not address |
| CH-0098 | should-fix | AS-06 and AS-12 verdicts rest on un-re-read rows | **Conceded** | `02` marks both "unverified reading" |
| CH-0099 | should-fix | "six stages" overstates; "3-4 lines" is the blind design's number | **Conceded** | `02` and `04`: three tool-deciding stages, reduced form; the summary length is a decision |
| CH-0100 | should-fix | 01 states interpretations as positions; omits REQ-U21-05, REQ-U21-11 and the H.3 relation | **Conceded** | `01` section 1 relabelled and extended |
| CH-0101 | note | C7 is a reconstructed share and not the tool block | **Accepted** | `01` C7 and `03` section 6 |
| CH-0102 | should-fix | the search log cannot support "not found" as written | **Conceded** | search log: limits paragraph and section 2 per topic; Gemini stub listed as an open item (`03` section 10) |
| CH-0103 | note | Executor's intent search appears as a CLI command | **Accepted** | `03` section 4 Executor row |
| CH-0104 | note | origin-derived rows not marked | **Accepted** | `03` header "Origin-derived rows" |

## 3. Retained disagreements
None between the lead and the two challengers after these dispositions; the rebuttal check below may add some. The lead notes one point where the evidence leaves the matter open rather than settled: whether the staged form with three tool-deciding stages satisfies the supervisor (Q-J31) is his decision, not V5's.

## 4. Rebuttal check (RV-0023)
Pending.
