# AUTH-005 successor package (version 2; provisional; stop for human scientific review)

Authorization: AUTH-005 (human, 2026-10-16). Thread: `ops/threads/T-20261016-94/`. Successor to `design/package/` (AUTH-004, checkpoint `2a22677`), which is **unchanged** and stays the record of the earlier analysis. Where this package corrects an earlier statement it says so (section 3). **Nothing here is validated, approved, selected as a thesis contribution, or claimed novel; nothing was implemented or run.**

## 1. What is in this package
| File | Deliverable asked for in AUTH-005 | Source records |
|---|---|---|
| `01-policy-candidate.md` | one complete provisional policy candidate, decision logic, readable graph | DPR-0004 (design-proposer) |
| `02-justification-and-alternatives.md` | why it deserves investigation; comparison with the strongest simpler and materially different alternatives | DPR-0004/0005, RV-0003 |
| `03-evaluation-outline.md` | corrected, falsifiable evaluation outline | DPR-0005, HYP-0007..0014 |
| `04-claim-to-source-register.md` | claim-to-source register for the decisive arguments | DPR-0004 section 7, FND-0001 (steward), lead checks |
| `05-unsupported-assessment.md` | candid assessment of what remains unsupported | all of the above |
| `06-disagreements.md` | material disagreements retained and what would resolve each | CH-0020..0034, RV-0003 |
| `07-supervisor-presentation-outline.md` | concise supervisor-ready presentation outline | lead |
Agent records: `design/proposals/DPR-0004`, `DPR-0005`; `hypotheses/HYP-0007..0014` (HYP-0008 supersedes HYP-0005, HYP-0010 supersedes HYP-0004, HYP-0011 supersedes HYP-0003, HYP-0012 supersedes HYP-0006); `challenges/CH-0020..0034`; `reviews/RV-0003` (final); `findings/SUM-0003-pivotal-claims-verification.md` (front matter `FND-0001`); `evidence/extracts/EXT-0057..0066`.

## 2. The result in five sentences
(1) A single complete candidate, **C-A**, survived two adversarial rounds as a coherent, specified policy: an offline break-even rule assigns a deployment-level surface of full definitions in a stable cached prefix; the rest of the catalogue is reachable only through a prompted search interface; exposure is add-only inside a session. (2) It is a parameterised combination of a static core and deferred loading, with no per-task adaptivity; it claims no novelty and **no demonstrated advantage over any comparator**. (3) Its worth is that it is fully specified, passes a row-by-row runtime-information test, contains the strongest simple rivals as special cases, and has a cheap first experiment (cost mechanics per provider) that can end the line. (4) The strongest rival, cached expose-all and vendor-native deferral, wins wherever the cache-read price is low, traffic is dense, the catalogue fits the context and usage is flat; at the read price implied by the only direct cache table in the record the whole warm tool block is cheap. (5) The supervisor's staged graph is kept as a materially different candidate (C-B), not adopted and not excluded.

## 3. Corrections to the AUTH-004 package (that package is not edited; these statements are superseded)
| AUTH-004 statement | Correction | Where |
|---|---|---|
| N0 "configuration box: regime facts -> which arms run" (C-section, DPR-0003) | withdrawn as policy content. Which arms are evaluated is evaluation design; whether to restrict at all is decided inside rule A1 (when A1 returns F = K the candidate is expose-all). No adaptivity is claimed | 01, DPR-0004 4.4 |
| Rule R-cache: exposure is add-only after the first turn (a design constraint) | now **hypothesis HYP-0009**. One provider's beta withdraws tools by reference without invalidating the cache; a rewrite is free once the cache has lapsed; a stable meta-tool is an alternative. Add-only stays the candidate's default; the other options are tested arms | 01, 03, DPR-0005 4 |
| E4: recovery justified if no-miss overhead exceeds miss-stratum value "in every regime"; strata "miss / no-miss" | wrong: strata defined by the exposed set are post-treatment, and value and price must be weighted by prevalence. Replaced by a population-level estimand, strata from a pre-run reference partition, test at the estimated prevalence (HYP-0011) | 03 |
| HYP-0006 conjunction (recovery higher **and** price lower) | wrong: a mechanism with higher recovery and higher price is not dominated. Replaced by a break-even trade-off at the estimated prevalence (HYP-0012) | 03 |
| HYP-0005 / E4 "no cost inversion observed in any tested regime" | not evidence of monotonicity; existence needs one verified instance, monotonicity needs an estimated response curve with more than two exposure levels (HYP-0008) | 03 |
| HYP-0004 "substantial share" threshold; HYP-0003 "every regime" | replaced (HYP-0010, HYP-0011) | 03 |
| U1-U3 offered inside the objective discussion | now optional diagnostics only; the primary objective (F1, O1 reading) and O2 alternative are stated separately | 01 |
| Forms S and M as the two committed forms to discuss | Form S is C-B (system-run selector with a system trigger); Form M is closest to P4g/P3. The new candidate C-A is a third, narrower form built around a decision rule; none is thereby selected | 02 |
| "vendors disagree" about mixing eager and deferred tools | vendor guidance differs and the scopes differ (OpenAI's statement is scoped to an Agents API session) | 04 |
| FitText "initiator [U]" (agent records) / "system-initiated" (lead map) | resolved from the original (AUTH-004 D3, EXT-0050/0051/0055/0056): the model emits the request, the system executes; the prompt prescribes the protocol (EXT-0065) | 04 |

## 4. How it was produced (process report)
- **Roles.** Steward: independent verification of eight pivotal claims (V1-V8) against originals, with a file created first and a hard bound of four extra windows; it **finished**, with one file written, 50 tool calls, and verdicts SUPPORTED / PARTLY / CANNOT DETERMINE per row. Proposer: candidate space of four materially different complete candidates (C-0, C-A, C-B, C-C), one chosen, plus cache analysis and evaluation outline. Challenger: 15 objections with strength grades, strongest rival argued, a row-by-row audit of the runtime-information table. Lead: tasking, passage extraction (EXT-0057..0065), assembly.
- **Disagreement was real this time.** The proposer was told to justify its assumptions and concede only on evidence or demonstrated error: 8 CONCEDE, 7 PARTIAL, 2 REBUT-kept positions. The challenger graded its own objections and, after replies, WITHDREW 8 (CH-0021, 0022 points 1-2, 0024 as a record defect, 0025, 0028, 0031, 0032, 0034), DOWNGRADED 7 to minor (CH-0020, 0023, 0026, 0027, 0029, 0030, 0033), and named which of its own objections were overstated (06). Concessions were not automatically carried into the operative text: the challenger found five propagation defects and checked the fixes by grep.
- **Cap.** 12 messages, unchanged; 9 used (steward 1, proposer 3, challenger 2, lead tasking 3). No escalation was needed. Bundling objections per proposal (one CH id per issue) remained a deviation from PROTOCOL's one-issue-per-message rule, authorised in TASK.md for the cap only. The cap still allowed only two rounds.
- **Independence limits.** Verification of the eight pivotal claims is independent of the proposer and lead. The closed-form cost expressions and the one-parameter fit to the Toollery cache table are the proposer's derivations, independently **reproduced** by the challenger but not verified by the steward. Items cited from governing copies and not re-read at the original are labelled in 04.
- **Lead edits to agent-owned files:** only the `target` front-matter format of `reviews/RV-0003.md` (twice; the challenger overwrote the first fix), so the workspace check passes; content unchanged.

## 5. Integrity checks
`python tools/verify_workspace.py` run at the second checkpoint and again before the final commit (results in `ops/threads/T-20261016-94/SUMMARY.md`); extracts are tool-written and hash-verified; no origin access, no web search, no previous-thesis material, no change to governing evidence, requirements or configuration.
