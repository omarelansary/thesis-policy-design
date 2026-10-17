# 05. Candid assessment of what remains scientifically unsupported

Status: lead's assessment [I], drawn from DPR-0004/0005, RV-0003 and the steward's verification. "Not found" means not found in the stored corpus and these extracts, never "does not exist".

## 1. What the candidate does not have
- **No demonstrated advantage over any comparator.** C-A is a parameterised combination of a static core and deferred loading. It contains expose-all, a static core and a listed grade as special cases, differs from vendor-native deferral in how its core is chosen, and may be tied by an empirical size sweep.
- **No per-task adaptivity.** The only in-session adaptation is the model's own search.
- **No novelty claim** and no basis for one: the stored corpus contains close overlaps (vendor deferred search with cache-preserving append, namespace-level first disclosure, FitText re-retrieval, just-in-time schema loading, Skill Blocks for skills, programmatic tool calling). Whether C-A is a thesis contribution is the human's decision.
- **Completeness only under one objective reading.** Rule A1 minimises cost (O1). Under O2 (minimise exposure subject to success and cost) the rule must be replaced.

## 2. Unsupported or unmeasured, grouped by what depends on it
| Question | Why it matters | State |
|---|---|---|
| Does restriction lower **billed** cost at non-inferior success, on any provider? | whether any restriction is justified over cached expose-all | no stored source measures billed cost with success; the only direct cache table is single-step, provider and pricing unstated, difference inconclusive |
| What is the cache-read multiplier on the tested provider, and how does it vary? | the cost region where C-A can win (the Table 15 fit implies about 0.0088, an order of magnitude below the vendor-page values) | derived from one table; **cache state, not exposure count, is the first-order cost driver there** |
| Do deferred or withdrawn definitions count toward billed or model-visible tokens? | the whole case for deferral and for withdrawal on the provider that offers it | not stated in any extract (steward V2 CANNOT DETERMINE); A0 would measure it |
| Does a **stable** restricted surface keep its hit rate? Is the cause of Toollery's low hit rate per-query variation? | the cache-compatibility argument for C-A | HYP-0007; the cause is the proposer's inference only |
| Do models invoke a search interface when a needed tool is absent, prompted and unprompted? | every model-driven form (C-A, vendor deferral, C-C) | not measured; the under-invocation evidence concerns the task's own tools and does not say they were visible; FitText prescribes the protocol by prompt with no other tool visible; one exploratory control shows a model stopping far below its budget |
| Is call frequency in successful dev runs an adequate proxy for need? How biased is conditioning on success? | rule A1's central input | HYP-0014; no estimator exists where the reference policy cannot run (the flat catalogue exceeds context) |
| Is usage concentrated enough for a core to exist? | whether C-A reduces to a poor core or to expose-all | no data |
| Does a second filtering stage pay? Does a system trigger beat model emission? | the supervisor's staged graph; C-B | not shown either way (a two-stage router matched single-stage retrieval in success; no token data) |
| Does retrieval-based restriction lower success at the catalogue sizes of interest? | the accuracy side of the primary rule | mixed single-benchmark results (several lowered success; strong models largely mitigated distraction; flat cost 8 points on one model/draw, intervals about ±8) |
| How large are the replay, reachability, turn-budget and judge effects on any search or recovery estimate? | validity of any evaluation on the closest vehicle | direction unknown; may inflate recovery's value |
| Is `epsilon := delta` adequate? | the tolerance on unreached needs | conservative only if the frequency estimates are unbiased |

## 3. Quantities no one has set
`delta`; the cost margin of reading O2; the equivalence margin for the cost-response test; every per-falsifier margin; the number of deployed sessions `N_dep`; the cost convention and tokenizer; the reference policy where expose-all does not fit; the claimed range of prevalence and horizon; the search width, search budget, ranker type and the interface-contract wording (to be fixed on dev data). No power calculation is offered because its inputs are unknown.

## 4. Limits of this package's own evidence
- Of the eight pivotal passages the steward checked, 4 were SUPPORTED (V1, V4, V5, V7) and 4 PARTLY (V2, V3, V6, V8; V2 and V3 each with a CANNOT DETERMINE component); **no pivotal claim was found false**, but several framings in earlier records were corrected (the non-deferred-tool rule was in a different extract; "no advantage" is not "costs more"; "vendors disagree" ignored scope).
- The closed-form cost algebra and the Toollery fit are derivations, independently reproduced by the challenger, **not verified by the steward**; one numerical statement in the proposer's text (141 turns per unit of system-prompt share) disagrees with its own formula (about 115).
- Items cited from governing copies and not read at the original are listed in 04 section C.
- Every cache number is provider-specific (Anthropic's documentation for lifetime and multipliers; one beta for withdrawal by reference).
- The review had two adversarial rounds inside a 12-message cap; the proposer defended this time, but a symmetric debate of more rounds could change the grades.

## 5. Possible conclusion the evidence does not rule out
That the answer in the tested regimes is **cached expose-all** or **vendor-native deferral with a swept core**, and that the thesis finding is where, and why, anything more elaborate pays or does not. The candidate and its first experiment are designed so that this outcome is a clear, reportable result and not a failure.
