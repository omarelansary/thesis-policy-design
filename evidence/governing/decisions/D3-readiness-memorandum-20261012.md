# D3 readiness memorandum (for the user's decision; not a decision record)

Date (UTC): 2026-10-12. Basis: `stage-reports/STAGE2_POSTRECOVERY_GATE_ASSESSMENT-20261012.md`, `stage-reports/STAGE2_CLOSURE_AUDIT-20261012.md`, `audits/A50-recovery-verification-and-errata-20261012.md`, `stage-reports/STAGE2_FINAL_LANDSCAPE_REPORT-20261012.md`. Stage 3 and any architecture choice remain your decisions.

## 1. Verdicts
- **Original (as found): FAIL**, under brief §3.4 ("a misquoted location"). Preserved.
- **Post-recovery: INCONCLUSIVE, not PASS.** The misquoted-location trigger was re-tested and is cleared where tested (all numeric page citations in full-text candidate rows: 42 records / 175 citations; the L2 audits: 71 citations; the 46 challenger-reviewed sources). Four wrong-page records and one audit were found, always off by one page; three linked corrections were appended (R2-C218, R3-C133, R3-C134) and one unsupported assertion was withdrawn. The condition is **unverified outside that scope**, and the observed error rate there was about 8–10%. If you prefer to keep FAIL until the unscreened scope is checked, the evidence supports that too. Your call.

## 2. Remaining INCONCLUSIVE conditions
- Criterion 1: F1, F2, F6 hit the 25-query cap without the two-provider stopping condition (cannot be cured without a formal protocol revision); F3, F7, F8, F11 undetermined or thin.
- Criterion 11: reduced scope (15 of ~52 included sources; 20 of 43 pivotal sources); open objections: Shi et al. (NDSS 2026) not checked, four security-flagged excludes without an include row, three exclusion items without stored text, five abstract-level pivotal sources.
- Criteria 4, 5, 6, 7, 10, 12, 14: partial or incomplete (L2 table meets the strict reading for 68 of 208 mechanism-family sources; criterion 12 is a bounded lexical screen only; chaining and recency signals incomplete).
- Screening quality: 223 unresolved maybes, 42 contested groups, six title-only includes, unadjudicated.

## 3. Landscape conclusions safe to use as bounded evidence (verification level in brackets)
- Deferred / on-demand tool exposure is a documented feature of major providers and clients; their own docs say discovery adds a step and that changing the loaded tool set invalidates the cache [official docs]. Independent end-to-end effects were not found.
- No retrieval method wins universally; expansion benefits depend on the retriever and setting [full text: ToolRet, Re-Invoke, Weller et al.].
- In the tested filters and settings, reduced exposure lowered task success relative to full exposure; other filters or tool counts did not, and tool count does not harm monotonically [full text; no uncertainty reported in several]. No production-prevalence or "no-loss" claim is supported.
- A reduction in a token component need not reduce the bill [full text, one campaign]; the system-prompt-plus-tool-definition block was the largest cost component in the one workload that reported it, unseparated [full text]; caching changes the relation [official docs; list-price reconstruction in the cache study].
- Evaluator disagreement (18.5% of audited tasks) and rerun spread (57.9–76.8% on one benchmark) can mask several-point effects; cost reporting is rare and inconsistent [full text].
Use these with the stated qualifications in the final report and A48; do not generalize beyond the tested settings.

## 4. Claims that still need primary-source verification before use
- **O1 (gap):** "no controlled study jointly measures filtering/disclosure on task success and billed cost per success" is a bounded negative (F1, F2, F6 capped; Shi et al. and other A4 sources unchecked). It must not be treated as a gap or as novelty. Near-misses to re-read from primary text: Tool Attention, Token Reduction Is Not Cost Reduction, ProMCP, the scaffolding study (Table 5), ToolMenuBench/GIST-CMTF, Speakeasy.
- **O2–O3 (break-even, cache-aware discovery):** rest on vendor statements and one confounded scaffolding comparison; the cache study has an internal inconsistency and no quality outcome.
- **O4 (benchmark validity):** the validity audit is a v1 preprint with placeholder references and single-agent audits; re-verify from the source.
- **O5 (vendor claims):** Speakeasy, Cloudflare, GitHub are vendor self-reports; Copilot's own arithmetic is inconsistent.
- **O6 (description reliance):** Tool Preferences, MCPTox and MSB measure preference or invocation of alternative tools, not accuracy on large catalogues; 34 other rows are abstract-level.
- Any statement that rests on abstract- or snippet-level rows (A4, F9, F10, F12, F3 compression, tool merging) and any value shown only in a figure or a garbled table.

## 5. Is proceeding to Stage 3 on this evidence scientifically defensible?
**Yes, but only as an adversarial re-verification of Stage 2 outputs, not as an acceptance of them.** Stage 3 (brief/STAGE_GATES: "reviewer works from sources and claim locations, not the synthesis alone; verify identities and quoted locations; attempt to falsify leading interpretations") is the stage designed to do the verification Stage 2 could not finish. No protocol clause requires a Stage 2 PASS first. It is **not** defensible to use this evidence for a gap, a novelty claim, a savings figure, or an architecture choice. Precise restrictions I recommend you impose in D3:
1. Treat every Stage 2 artifact (records, L2 audits, A43/A44, final report, challenger reports) as untrusted input, with the INCONCLUSIVE conditions in §2 carried forward explicitly.
2. Require primary-source verification, with page and line from stored text and visual checks of garbled tables and figures, for every pivotal claim before it enters the Stage 3 claim ledger; downgrade or remove what cannot be verified (Stage 3's own promotion rule).
3. Give the reviewer the sources and locations first, not the synthesis; keep a separate Opus challenger.
4. Decide separately whether Stage 3 may fetch or search: the A4 coverage gap (Shi et al., four security excludes), the five abstract-level pivotal sources and F11 cannot be closed from stored evidence. Any such work needs your explicit authorization with logged queries and caps; none of it may weaken a criterion.
5. No candidate research questions (Stage 4) may rely on the "none found" negative until restriction 2 and, if you authorize it, the A4 follow-up are done.
6. No architecture selection, and no use of the vendor figures, the CMTF ~90% figure or the 142× figure as savings estimates.
7. Keep the frozen baseline, the post-freeze correction state and the append-only logs; any further corrections go through linked rows.

## 6. Decisions for you
(a) Accept INCONCLUSIVE as the post-recovery gate state, or keep FAIL pending exhaustive location verification. (b) Authorize Stage 3 with the restrictions above, with changes if you wish. (c) Decide whether Stage 3 may include a bounded, logged follow-up for the A4 gap and the five abstract-level pivotal sources.
