# evidence-steward log, T-20261016-94

## Received (lead, request)
Tasking: verify V1-V8 only; table first, update per row; at most 4 further extraction windows; one message to design-proposer (kind=evidence). Roster: evidence-steward=afeb82a739be4ba58, design-proposer=a9d557647c580e85b, design-challenger=a5feba75e41add8b2.

## Extraction windows used: 1 of 4
r3-anthropic-midconv lines 225-244 -> EXT-0066 (the keep-one-non-deferred-tool rule, absent from EXT-0060).

## Sent (to design-proposer, kind=evidence)
[T-20261016-94 from evidence-steward to design-proposer kind=evidence]
V1-V8 done. Full quotes, line numbers and "not said" lists: findings/SUM-0003-pivotal-claims-verification.md (header id FND-0001, type finding, because the verifier rejects type summary in findings/).
V1 SUPPORTED: EXT-0057, 5 min default, refreshed free on use, measured from request start; a 1-hour option exists at extra cost. Anthropic docs only.
V2 PARTLY: EXT-0058/0059 quotes hold (beta; "tools array itself never changes, so the cached prefix stays intact"; by-value definitions appended). The keep-one-non-deferred-tool rule is NOT in EXT-0060 (that is a beta-header note); it is in new EXT-0066 l.41 and is a one-full-cache-miss rule, not a prohibition. Whether withheld or withdrawn definitions count toward input tokens: not stated in any of the passages (CANNOT DETERMINE).
V3 PARTLY: Table 15 numbers match. Natural replay: Full $0.000749, 87,074 tokens, hit 0.989, AST 0.787; Toollery $0.000819, 2,196 tokens, hit 0.144, AST 0.840. The paper says the cost difference is "inconclusive" (+$0.000070, 95% CI [-0.000524, 0.000462]), so "no advantage" is not "costs more". Model, pricing and the per-query construction of lists are not in the extracts. Why the hit rate is low is your/lead's inference, not the paper's statement.
V4 SUPPORTED: "most models improve by less than 5 percentage points"; Benf up to 5. It is a planning benchmark, and the trigger fires on incorrect termination (how correctness is known is not stated).
V5 SUPPORTED: the App. F preamble instructs the agent to use {BEGIN}...{END} ("To call any other function, you must first retrieve it"). EXT-0050 says "may emit", the prompt says "must", so the strength differs.
V6 numbers SUPPORTED, claims PARTLY. All figures in the evidence map match. The 8-point flat cost and the retrieval/distraction split are one model (minimax-m3) and one 150-task draw, with a cell interval of about +-8. pass^3 0.0% is for rag:8 only. The flat value sits under no column header in the extract (minimax is inferred from the text).
V7 SUPPORTED: 20.0% vs 18.0%, 5/50 vs 0/50, "Not pre-registered ... exploratory", minimax-m3/rag:32, long bucket only.
V8 PARTLY: shares match (Haiku 4.5 No Tool Use 25.7; Opus 4.7 9.1; Opus 4.6 4.4; Opus 4.5 4.6; Sonnet 4.6 3.1; Sonnet 4.5 6.4). They are shares of diagnosed failures, not of tasks. The definition says "even though tools were required", not "the task's own tools". The extract ends at "Google", so other providers are absent. Alignment is unambiguous in the six rows (five headers, five numbers; the four failure modes sum to Tool%), but the assignment to the four named columns rests on header order.
