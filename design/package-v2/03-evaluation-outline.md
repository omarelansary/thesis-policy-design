# 03. Corrected, falsifiable evaluation outline (conceptual; nothing here is authorized to run)

Status: provisional. Source: DPR-0005 section 6 and HYP-0007..0014 (design-proposer), after challenges CH-0028..0033 and RV-0003. It supersedes the AUTH-004 `E-validation-strategy.md` where they differ (see `00-README.md` section 3). No margin, sample size, repeat count or threshold is set; each is a human decision or depends on an unknown (section 9).

## 1. Estimand: population level, one scorer
For each arm `a` and task population `D`: mean success `Y_a` and mean cost vector `C_a` over tasks drawn from `D`, estimated on the **same tasks** for all arms under one scorer and one evaluation code path (REQ-O14-03). Contrasts are against the reference policy and pairwise, with intervals. The headline is the pair (success difference, cost difference) and the admissibility test `Y_a >= Y_ref - delta` (the primary rule, reading O1; reading O2 in 01 section 8). Unit of analysis: the task, clustered by session for multi-turn runs.

## 2. Strata that do not condition on treatment (correction 5a)
- A **reference partition** is fixed before the run and applied identically to all arms: tasks whose scorer-side required set (class P at runtime, scorer only) intersects the catalogue outside a dev-frequency core of a named size (a second size as sensitivity). The partition is a property of the task and the fixed core, **not of any arm's exposure**, so it is pre-treatment. It is not the C-A surface (that would privilege C-A).
- An arm's **own** miss indicator (the required set not within its exposure) is a post-treatment mediator: reported descriptively, never used to form comparison strata.
- Prevalence `w = P(miss stratum)` is estimated from the sample, then varied by post-stratification reweighting as a **transportability** report, because the benchmark's prevalence is not the deployment's.

## 3. Recovery economics across the miss and no-miss populations (correction 5a)
For the search path: value `V` (success gain in the miss stratum), price `U` (cost increase in the no-miss stratum), price in misses `P1`. Population net effect (as the pair, or in cost units under a pre-registered rule): `w (V - P1) - (1 - w) U`; break-even prevalence `w* = U / (V - P1 + U)` when `V > P1`. It is a **function of `w`**. The test (HYP-0011) is evaluated at the **estimated** prevalence of the declared population with its interval. "Positive at some `w` in a range" was dropped as near-vacuous (at `w = 1` it equals `V - P1`). Under the primary rule the test is admissibility and cost at the estimated prevalence, so no exchange rate is smuggled in. An **extra-turn control** (same number of extra turns, no tools) separates tool value from a second attempt. The only stored evidence on enforced extra exploration (a planning benchmark, not a tool setting; the extra turn is triggered by an incorrect termination, so a runtime trigger could not replicate it) found gains under five percentage points for most models (EXT-0063/0064; steward V4 SUPPORTED); it bounds a perfect-trigger control and does not support a runtime trigger.

## 4. Initiation mechanisms: a trade-off, not a conjunction (correction 5b)
Mechanisms: prompted model emission, unprompted model emission, a system trigger, none, the extra-turn control. Estimate (recovery, unused price, price-in-misses) for each as in section 3. A mechanism with higher recovery **and** higher unused price is **not dominated**. Compare by (i) dominance when it holds; (ii) otherwise the net at the estimated prevalence, with the break-even prevalence between two mechanisms `w_SM = dU / (dR - dP + dU)` and the curve over `w` as transportability; (iii) under the primary rule, admissibility and cost at the estimated prevalence. The earlier conjunction falsifier (HYP-0006) is replaced by HYP-0012. FitText's emission is prescribed by prompt with no other tool visible (EXT-0065; steward V5 SUPPORTED), so it is evidence for prompted emission at best, not for spontaneous initiation.

## 5. Cost response: curves, not "no inversion observed" (correction 5c)
- **Existence** of a cost inversion (a restricted arm costs more than a fuller one): needs **one verified instance**, a cell whose interval for (restricted minus full billed cost) lies wholly above zero while the restricted arm exposes fewer tokens. The Toollery natural cell is not one (interval includes zero; steward V3). Falsified only by a sweep that contains no such cell.
- **Monotonicity** of cost in exposure: needs an estimated response curve with intervals by regime, **more than two exposure levels** (two levels give a sign, not a shape), crossed with surface stability (stable vs varying), cache state (cold, natural, warm), horizon, and provider cache multipliers. The model's prediction (DPR-0005 sections 3.1-3.3) is falsified when it lies outside the interval, **only when interval half-widths are below a human-set equivalence margin; otherwise the result is inconclusive**. Cache read and write multipliers are calibrated on separate probes of the tested provider (the earlier mix of one provider's read multiplier with another's write multiplier was an error, CH-0028).
- "No inversion observed" supports neither claim.

## 6. Arms
Reference policy (expose-all, or a named substitute where the catalogue exceeds context; the claim is then relative to it); static core; vendor-native deferral with a hand-picked non-deferred set; listed grade; **frequency core with the same size as C-A's surface, without and with search**; **frequency core with size chosen by a dev sweep on the measured criterion**; C-A with ablations (no search; search without the instruction; ranker variants; surface-change options: add-only, boundary rewrite, free-rewrite window, withdraw-by-reference where offered); C-B; C-C where feasible; an **oracle-exposure arm** (scorer-side) as headroom; the **extra-turn control**.

## 7. Falsifiers (each is the negation of its claim, per regime, after correction for the number of regimes, models and conventions)
| Component (record) | Claim | It is **not justified** if |
|---|---|---|
| Whole candidate (HYP-0013) | C-A is non-dominated by the comparators in some regime | in every claimed regime some comparator (including the frequency-core and sweep arms) dominates on the pre-registered rule |
| Core rule A1 (HYP-0014) | the estimated core covers more held-out usage than size-matched controls | it does not, in every claimed population |
| Stable surface (HYP-0007) | its hit rate is not lower than the full library's | lower beyond spread in some claimed cell |
| Cost response (HYP-0008) | an inversion exists; the response follows the model | no verified inversion in the sweep; or the prediction lies outside the interval (only when interval half-widths are below the equivalence margin) |
| Add-only (HYP-0009) | not beaten on billed cost at non-inferior success | another surface-change arm is cheaper beyond spread in a claimed regime |
| Initiation (HYP-0010) | prompted (and, separately, unprompted) models search when a needed tool is absent | the rate is not above the no-interface baseline, per model and condition |
| Recovery (HYP-0011) | the recovery arm is preferred to no recovery at the estimated prevalence | at that prevalence (with its interval) the pre-registered rule does not prefer it |
| Initiator (HYP-0012) | a system trigger is preferable to model emission at the estimated prevalence | the pre-registered rule does not prefer it there |
Ties inside the repeat spread count for nothing either way. A result for one provider does not carry to another. Hypotheses HYP-0013's dev-sweep arm is the proposer's addition; no source supports it as a standard comparator.

## 8. Order of questions (cheapest first; each can end the line)
1. **Cost mechanics per provider** (cache-read and write multipliers, lifetime, minimum cacheable length, billing of deferred definitions, hit rate of stable vs varying surface; HYP-0007, 0008): decides whether cost differences exist at all.
2. **Usage concentration on dev data** (HYP-0014): decides whether a core exists and whether A1 beats the sweep.
3. **Prompted and unprompted initiation** (HYP-0010): decides whether model-driven deferral is viable.
4. **Population-level recovery and the initiator comparison** (HYP-0011, 0012).
5. **The full comparison** (HYP-0013).

## 9. Threats to validity and what the human must set
Threats (apply to all, direction usually unknown): single-reference replay scoring (may inflate recovery's value); forced absence is failure by construction; stub schemas and steering error messages as gold cues on the closest vehicle; no cache fields and no sessions there; a fixed tool list per run (a search arm needs a loop change applied identically to all arms); the 12-turn budget (EXT-0042's budget-30 control is exploratory, one model, 50 tasks); evaluator error; single-step benchmarks cannot show loop effects; every cache number is provider-specific; vendor statements are unreplicated; multiplicity across regimes, models and conventions; a dev/test split recorded.
The human sets before any run: `delta` and whether the tolerance on unreached needs may be tighter, O1 vs O2 and the cost margin, the cost convention and tokenizer, the reference policy or substitute, the primary criterion (Q1), the claimed range of prevalence and horizon, the per-falsifier margins and equivalence margin, the number of deployed sessions `N_dep`, repeats and models. **A smoke execution of the closest vehicle remains unauthorized.**
