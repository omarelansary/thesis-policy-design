# Thread T-20261021-112: SUMMARY (lead; AUTH-019: the open items re-checked under the human's decisions of 2026-10-21)

- Input: the human's decisions after the meetings, recorded verbatim as INT-T-005 (`requirements/intake/2026-10-21-user-decisions-after-meetings.md`); register section H.3 (REQ-U21-03..12). Core principle: do not re-invent or re-test what research, large companies or widely used open-source projects have already tested; we are designing a policy.
- Steward P1 (FND-0037, `findings/SUM-0039-pilot-rows-established-a.md`) and steward P2 (FND-0038, `findings/SUM-0040-pilot-rows-established-b.md`) classified 46 pilot rows as established, partly established, our setting or end-to-end only. The strictness rule was that a vendor's statement of its own mechanism or price counts as established, but its performance claims do not, and one paper alone does not. Steward B1 (FND-0039, `findings/SUM-0041-billing-components.md`) tabulated the bill's components per provider from the stored pages. All three created their files late (after the 8-turn instruction) but completed them.
- Lead: drafted the model-agnostic bill equation (`design/proposals/DPR-0006.md`, proposed). The design-challenger reviewed it (RV-0020: 1 high, 9 medium, 6 low; nothing withdrawn). The lead applied every correction. The main ones: a price table per component, tier and mode in place of one multiplier; 5-minute and 1-hour cache writes; reasoning tokens priced only inside billed output; the session sum includes requests outside turns; container time is counted once; free allowances are reported apart; the gap cost is stated as a consequence already inside W and R; the primary figure is marked [I] with an alternative.
- Ledger effect (batches 17a-d, workbook in place, CSV and frontier regenerated):
  - 17a, closed by the human's decisions: C-D01, C-D07, C-D07/GRADED, C-D05, C-D02, N-1, N-4, N-27, N-25, N-28, C-D08/DELTA, C-D08/EPS.
  - 17a, merged: N-29, AS-14.
  - 17a, deferred to the end-to-end study: C-S14, C-S14/MULT, PATHDEP, POSTSEL, C-X06, C-R03/C20, C-R03/C26, C-D08/ALPHA, C-D08/STRATA.
  - 17a, new row: N-30 (the bill equation).
  - 17b, closed on vendor documentation: C-S03/EXCEPTIONS, C-S03/MINCACHE.
  - 17b, deferred to the end-to-end study: C-S09/RA10, C-S09/RA7, C-X04, C-S07, C-X05.
  - 17b, deferred with trigger: C-S19/S44.
  - 17b, partly established: 17 rows, so only the stated remainder is tested.
  - 17b, narrowed: N-21 and AS-06.
  - 17c: C-D03 and C-D06/NOVELTY closed by decision; Q-J08, Q-J12, Q-J20, Q-J21 and Q-J22 answered.
  - 17d: N-30 drafted, reviewed and corrected; it waits for the human's approval and the first billing probe.
- Contamination rule: no steward or reviewer used the student's earlier retrieval experiments; the rows about the earlier evaluation vehicle were classified without reading it.
- Limits: all verdicts are the stewards' interpretations [I], unverified until a human checks (Q-U27); same model family throughout (C-E04); no web; provider prices are as stored on 2026-10-11 and rechecked on 2026-10-19.
