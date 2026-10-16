# E. Validation strategy (conceptual; nothing here is authorized to run)

Status: provisional. Source: DPR-0003 section 3 (design-proposer), as hardened by CH-0011, CH-0013, CH-0014 and CH-0017 (design-challenger), with the lead's organisation **[lead]**. No sample size, margin or threshold is set: each depends on quantities that are unknown or are human decisions (listed in E7). A smoke execution of the closest vehicle, which S4G proposed as a gate before freezing a design, is **not** authorized by AUTH-004.

## E1. Rules fixed before any run (pre-registration) — human or supervisor decisions
1. The **reading of "pays"** (five admissible readings, none chosen; CAVEATS 5) and whether "each step saves tokens" is per step or collective.
2. The **decision rule**: one scalar rule from F1-F7, or, if Pareto reporting (F4), a stated definition of dominance and of ties.
3. The **cost convention and tokenizer** (provider-reported counts or a named tokenizer; cache read/write treatment).
4. The **reference** `pi_ref` (expose-all where it fits; otherwise a named substitute) and which of **U1-U3** the scorer reports.
5. The **strata** and the **regimes in which each component is claimed to pay**.
6. Models, catalogue sizes, providers, number of repeats, margin `delta`, turn budget.
Post-hoc readings invalidate the claim (S4D addendum 2.1, S4G L82). A component is *justified only in a stated regime* where it is non-dominated on the pre-registered rule after correction for the number of regimes, models and conventions examined; it is *not justified* if it fails that test in every regime in which it was claimed.

## E2. Baselines and arms (one scorer, one evaluation code path; REQ-O14-03, REQ-S4)
- Baselines: P0 expose all (or `pi_ref`), P1 static core, P2 single-stage top-`m`, P3 deferred loading with a search tool, P4 two-grade exposure (moderate `n`), P4g group-then-tool (large `n`), P7 append-only per-turn re-ranking, P5 stable meta-tool / code-mediated *if the human requires the named existing project as a baseline* (S4I section 5), plus published methods and named existing projects as REQ-S4 requires.
- Policy arms: the template with each node ablated: N2 off; N2 at one level (P2) vs two (P2h); N3 only; N4 only; N3 + N4; with and without the cheap-grade list; **add-only vs rewrite vs withdraw-without-rewrite** where the provider offers it.
- Added controls: an **oracle-exposure arm** (scorer-side, U1) bounding the best case; an **extra-turn-without-tools control** for any re-opened attempt at termination; a task-level oracle stratum (tasks needing a tool outside the core) instead of treatment-defined miss/no-miss strata where possible.

## E3. Outcomes (a vector, never one number)
Task success by stratum; `c_tools`; `c_vis`; `c_cum` by category (tool metadata, selector/judge, reasoning, tool outputs, discovery calls, recovery calls; cached vs uncached); `c_bill` under the named conventions; turns; overhead of the decision mechanism; recovery value (miss stratum) and **unused price** (no-miss stratum); initiation rate with the needed tool absent vs present; trigger precision and recall; cache fields where returned. Conclusions are reported under every convention in the pre-registration; a flip across conventions is a result.

## E4. Falsifiers (each is the negation of the claim, stated per regime)
| Component or claim | It is **not justified** if |
|---|---|
| N2 narrowing (either level count) | some of P0, P1, P3, P4 or P4g dominates it on the pre-registered rule in every regime in which it was claimed to pay |
| Second level of N2 (P2h) | the single-level P2 with the same selector type dominates it in every such regime |
| Group-then-tool disclosure (P4g) | P3 or P4 dominates it in every such regime |
| Recovery (N3, N4) | the no-miss-stratum overhead exceeds the measured value in the miss stratum in every such regime |
| N4 over N3 (HYP-0006) | either the recovered success in the miss stratum is not higher, or the unused price in the no-miss stratum is not lower, than the model-initiated arm, each beyond a human-set margin |
| Cheap-grade list | P2 dominates P4 in every such regime |
| Model initiation (HYP-0004) | initiation rate in a forced-absence stratum is indistinguishable from chance/prior knowledge, or restores no more success than the arm without the interface, under a human-set threshold, for each model in the declared set |
| Cost non-monotonicity (HYP-0005) | no inversion exists in any tested regime (no pair where fewer exposed tools coincides with equal or higher cumulative or billed cost beyond repeat spread) |
| Unused price small (HYP-0003) | in the no-miss stratum the path's overhead exceeds a human-set margin in some claimed regime |
| Runtime regime determinant (HYP-0001) | the non-dominated arm is fully predicted by pre-session variables, or by no variable |
| Whole proposal | in every regime where it is claimed to pay, some comparator among P0, P1, P2, P3, P4, P4g, P7 dominates it |
Ties inside repeat spread count for nothing either way. A result for one cascade (P2h or P4g) does not carry to the other.

## E5. What would make the evidence stronger, in the order the questions depend on each other **[lead]**
1. **Does restriction pay at all?** P0/P1/P2/P3/P4 on one scorer across catalogue sizes, with cache fields and billed cost: this alone can close or open the whole question (HYP-0005) and costs the least build.
2. **Do models initiate discovery?** A forced-absence stratum with a search interface (HYP-0004): decides whether any model-driven form (P3, P4, P4g, N3) is viable.
3. **Is recovery worth its unused price?** N3 vs no recovery in miss and no-miss strata (HYP-0003) with the oracle arm as headroom.
4. **Does a second stage pay?** P2h and P4g against the best single stage of the same driver type (HYP-0002), at large catalogues where the regime argument says it could.
5. **Only then:** N4 vs N3 (HYP-0006), session working sets (P8), learned selectors (P6), the code-mediated baseline.

## E6. Threats to validity (apply to every result; direction usually unknown)
Single-reference replay scoring (bias direction unknown; may inflate recovery's value); forced absence is failure by construction; stub schemas and steering messages as gold cues on the closest vehicle; no cache fields; no sessions (HYP-0001 untestable there); a fixed tool list per run (a recovery arm needs a loop change applied identically to every arm); the 12-turn budget handicaps discovery (magnitude unknown; EXT-0042's budget-30 control, exploratory, one model, n=50, found no task reaching the budget); evaluator error (18.5% evaluator-human disagreement in one audit; scorer deliberately conservative, accuracies are lower bounds, EXT-0043); only 1,578 of 1,845 specs reference-consistent; experiments ran on `dev` while code read is `main`; vendor figures unreplicated. Parameters, indexes, regime facts and the core `A` are fixed on data disjoint from the evaluation tasks, and the split is recorded.

## E7. Quantities that fix the numbers (all unset)
The margin `delta` and the sample size depend on discordance and on the replay-usable task count (unknown; S4G sample-size figures are illustrations); the turn budget `T_max`; the catalogue sizes; the models; the provider's caching rules. No power calculation is offered because its inputs are unknown.
