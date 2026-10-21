---
id: "FND-0036"
type: finding
status: unverified-until-human-checks
created_by: evidence-steward
created_utc: 2026-10-21
thread: T-20261021-111
evidence: ["EXT-0004"]
---

# Check of MEETINGS-MAPPING-20261021, rows Q-J16..Q-J29, sections B, C, D (Steward M2)

Rows are appended below as checked. File lines are given as "file line N".

## Conventions
- INT-T-002 / INT-T-003: mapping `L n` = body line n = file line n+19 (checked: INT-T-003 file 448 = L429; INT-T-002 file 242 = L223). INT-T-004: export line E = file line + 160 (excerpt 1), +284 (2), +294 (3), +304 (5), +312 (6); E676 = file 380 (excerpt 4). Gemini notes not used. Labels: [F] fact in source, [O] observation, [I] interpretation. Statements are the supervisor's requirements, proposals or assertions, not findings. The student's reports of earlier experiments appear next to some passages (e.g. INT-T-004 file 245-247) and were not used.

## Section A, rows Q-J16..Q-J29

| Row | Verdict | Check |
|---|---|---|
| Q-J16 | CONFIRMED (with notes) | [F] INT-T-004 E617 (file 323) "go to this GitHub repo download this run this and figure out okay benchmark it how much uh token are they saving"; E626 (file 332) "This is your baseline. You should have multiple baselines." Range E583-E626 correct. Notes: (a) at E576-E577 (file 282-283) the student answers "No, I haven't seen them" to "I already shared this exeutor with you"; (b) INT-T-003 L265 (file 284) "You don't even need a executor you can narrow it down easily" and L306-L308 (file 325-327) "The second step would be something like executor. You have to find out like is executed the better approach or ... semantic search ... which one is better" show Executor also as a stage-2 candidate, not only a baseline (missing from the mapping); (c) the identity of the project rests on ASR "exeutor" plus "open source ... GitHub repo". |
| Q-J17 | CONFIRMED | INT-T-003 L386 (file 405) "don't implement anything"; L439 (file 458) "I don't want you to implement anything"; INT-T-002 L426 (file 445) "even a text file a empty file is good enough"; L441-L443 (file 460-462) "very big uh experiment ... multiple different goals ... multiple different settings ... run all the same settings multiple time ... statistical variance"; L453 (file 472) "first I would say don't engineer it at all". [O] "the idea" in L426 is "this memory and tool call", not the staged filtering graph. |
| Q-J18 | CONFIRMED | INT-T-004 E804 (file 492) "at least write the draft version of uh your policy. You don't need to implement anything"; INT-T-003 L429 (file 448) "You need to give me this policy. You are just beating around the bush but not giving me this policy"; L447 (file 466) "next witness day 11:00 a.m. ... by then I should have the policy". Nothing in INT-T-002 sets a new deliverable (its only policy mention, L135, is the student's). |
| Q-J19 | CONFIRMED (+ supplement) | E230-E232 (file 70-72): "you cannot use many tokens because you're saving tokens ... if you use many many more token to filter out the tools then there is no value". Missing supplement: E697 (file 393) supervisor "Uh, no, we will not drop the cost. first con state but", answering the student's "So um we will drop the cost constraint." (file 392, student's words); E706 (file 402) query expansion used "at a specific point where it's necessary ... the cost will not be that much high" (an assertion). [O] No passage charges the cost of producing summaries or memory (INT-T-002 L384). |
| Q-J20 | UNDERSTATED | E749 (file 445) "start working with 20 sample" is correct. More bears on numbers: E552 (file 258) "This number is not rigid again."; E559-E560 (file 265-266) "this 20 is not rigid. You figure it out by yourself. This 60 is not rigid."; E743-E747 (file 439-443) "narrowing down 50% ... you are reducing token by 50%", "If you reduce until 50% the accuracy is not hit at all ... maybe not for NCP atlas I don't know". Right effect: PARTLY for tier and reduction figures (he calls his own numbers illustrative and leaves them to the student; one hedge "I don't know"); NOT ADDRESSED stays for delta, epsilon, N_dep. |
| Q-J21 | CONFIRMED (weak link) | INT-T-002 L441-L443 correct. E367-E369 (file 83-85) "you cannot solve it for all LM. Every LLM thinks differently" is said in an argument about asking an LLM to find the filter (interpretability), not about the evaluation set; it supports model-dependence only by inference. "Settings" in L442 is not said to mean models. |
| Q-J22 | OVERSTATED; also WRONG LINE | L227-L233 correct (file 246 "if you are not doing groundbreaking research there is nothing nothing is noble", file 252 "You have to just sell it as a novely"). Wrong line: "that is your novelty" is L404 (file 423), not L397 (file 416 is a time-code line); the same wrong L397 occurs in row Q-J08 (M1's). ANSWERED holds for what counts as novelty (combination; what works and what does not). "No separate novelty assessment is required" is not said and has conflicting passages: INT-T-004 E591-E595 (file 297-301) "you should never in reinvent the wheel ... every month ... you should always search the web and figure out what is the kind status"; E455 (file 171) "there is no novelty in that" (about query expansion); INT-T-003 L214 (file 233) "none of them have any novelty"; E212, E228 (file 52, 68) "that's the novelty" / "This filteration is your noity" (a different novelty locus on 2 Oct). Right effect: PARTLY (meaning of novelty answered; whether a literature check is owed is not settled, he recommends monthly searching). |
| Q-J23 | CONFIRMED | INT-T-003 L159 (file 178) "What you have found and narrowed down is some methodologies."; L161 (file 180) "So, we have some mechanism families". Reinforced by L308 (file 327) "we already have different mechanism family". No reliance on excluded experiments. |
| Q-J24 | CONFIRMED (NOT ADDRESSED) | Searched all of INT-T-003 for provider, price and model names: nothing from the supervisor. Nearest (missing from mapping): E705-E706 (file 401-402) student "I can use a 27B", supervisor "yes you can use 27B but again ... query expansion is only necess..." (model size of a helper; no provider or bill). |
| Q-J25 | OVERSTATED | L345 (file 364) "what you are talking about is a coding agent. ... The same problem is applicable for any kind of agent"; L354 (file 373) "It can be a salesman, it can be a recruiter ... Uh marketing whatever. ... the problem is the cost per turn". Corrections: "support" is not in the passage (recruiter and marketing are); "none is fixed" is not said. He answers the student's narrowing proposal (L338-L344) with "Yes. Yes." (file 358, 360, 362) and then generalises; which scenarios the thesis uses is not stated. Right effect: PARTLY. |
| Q-J26 | OVERSTATED | L207-L209 (file 226, 228) quoted correctly ("keep them in the explicit cache and that's negligible cost"; "keep them always ... for the whole conversation"). Qualifier missed: L221 (file 240) "So that's how the system should work. I mean in theory that is all in theory."; then L223 (file 242) "Now let's go back to practical ... the scope is too broad ... only memory and tool calls", where explicit caching is not repeated; L193-L195 (file 212-214) "if you say I don't want to do everything then you can choose". Right effect: PARTLY (explicit caching proposed in an ideal design; whether it is a policy variable in the practical scope is not said). The same hedge touches row Q-J06 (M1's). |
| Q-J27 | CONFIRMED (with the hedge) | L207 (file 226); L211-L216 (file 230-235: "do you give all the context at the same time just by saying hello." ... "No, you you shouldn't."); L384 (file 403: "I can choose part of the memory which is relevant ... when he asked me more I will give more"). L207-L216 precede the L221 "in theory" hedge; L384 follows "go back to practical", so the reading holds for the practical part too. |
| Q-J28 | OVERSTATED | E593 (file 299) and E605-E607 (file 311-313) correct. E676 (file 380) "So, so, so I just forwarded it from someone else that's why. ... it cames from there" answers the student's confusion about a plugin or item shared on 29 August (E658-E668, file 364-374), not the partial-information idea. Drop E676. Right effect: PARTLY stands on E593 and E605-E607 only. |
| Q-J29 | CONFIRMED | No passage cited; asked after these meetings; nothing to check. |

## Section B

| Row | Verdict | Check |
|---|---|---|
| Q-U19 | CONFIRMED | INT-T-003 L363 (file 382) "even if it's not that novel even if the result is negative it's a thesis okay" ; time-code 00:25:36 at file 373. ASR garble follows ("and migrate bound to market"); next sentence L365 "The problem is can you write a paper and get it accepted." |
| Q-U05 | UNDERSTATED | L429 correct. Missing: INT-T-002 L135 (file 154), the student's words "Do you like the policy? Um you didn't like it?", imply that a policy was sent between 14 and 21 Oct (student's words only; the supervisor replies "you had two question", file 155). |
| Q-U07 | CONFIRMED | L135 is the student's question; the supervisor's next line (file 155) moves to "two question"; no comment on the policy anywhere in INT-T-002. |
| Q-U02, Q-U03 | CONFIRMED | E689 (file 385): "I would say keep it as it is. Create a new branch and First start analyzing what is available." What "it" is is not said. |

## Section C

| Item | Verdict | Check |
|---|---|---|
| C1 | CONFIRMED | Quote matches `ops/AUTHORIZATIONS.md` line 516 exactly. Reading marked "to confirm"; it follows the words. |
| C2 | OVERSTATED (reading) | Quote matches line 518 exactly. The words say "keep it but take care where you use it because it might be interpreted differently" and "never let it contaminate our work"; the mapping reads "not used, cited or reconciled", stricter than "take care where you use it" (it agrees with the 2026-10-21 contamination rule in the TASK, not with the quoted sentence alone). "E689 is the origin of that branch" is an inference: the human says "we branched a new branch", without naming the supervisor's advice as cause. |

## Section D

| Item | Verdict | Check |
|---|---|---|
| D1 scope change | UNDERSTATED | L223-L225 (file 242-244) and L390 (file 409) correct; L386-L404 correct. Missing from "is not said": file 409 "just focus on two things that is tools and memory because they comes hand in hand. Uh without tools you cannot have memory and without memory you will need all the tools", and file 244 "memory should help tool calls". He ties the two; he does not say whether the staged graph stays. |
| D2 tool results to files | CONFIRMED | L254-L262 (file 273-281) MCP "brain but you don't have a notepad", "save those in a file ... you can also search"; L275 (file 294) "You can save around 80% of the cost by doing this. For example ... 0.01 cent ... 0.003 cent" (the figures are given "for example" and self-corrected mid-sentence; ASR "0.101"); L271 (file 290) "this is hard to build". Range L250-L267 is loose but covers it. |
| D3 trivial exchange | CONFIRMED | L197-L207 (file 216-226) "let's say I say hello and you say hi and ... we have consumed 10,000 tokens that is the problem ... It should be 10, 20, 30." Framed as "let's say", a stated example, not a reported measurement. |
| D4 explicit caching negligible | OVERSTATED | Lines correct (L207-L209); the "in theory" hedge at L221 (file 240) is omitted, see Q-J26. |
| D5 experiment requirements | CONFIRMED | L441-L443 and E749 correct. Note the two differ in function: 2 Oct "start working with 20 sample and see" (a start), 21 Oct L441 (file 460) "numbers cannot be like okay 10 turn 20 turn it need to be a very big experiment" (a publication requirement, in turns). |
| D6 implementation stance | CONFIRMED | L426-L453 (file 445-472); "MD and ... text file", "injected in the prompt" at file 447. |
| D7 timeline | OVERSTATED | The deadline and the 22 weeks are the student's words (L473 file 492 "my final day on the registration is 18th of February"; L484 file 503 "we have only 22 weeks"), and the student adds he could extend by one or two months (file 494, 513). The supervisor's words: L485-L487 (file 504-506) "it's recommended that you send your master thesis writing at least uh three or four week earlier"; L491-L493 (file 510-512) "not to the examination, but to Michael and Simmon. because they need to read" (the transcript does not call them examiners); L497-L499 (file 516-518) "I don't think we need a physical meeting at all. You can meet online". |

## Missing from the mapping (line, question)
1. E697 (file 393), supervisor keeps the cost constraint; Q-J03, Q-J19.
2. E552, E559-E560, E743-E747: his figures "not rigid", 50% reduction "low-hanging" with hedge; Q-J20, Q-J14, Q-J12.
3. INT-T-003 L265, L306-L308: Executor as "you don't even need" and as stage-2 option; Q-J16, Q-J11.
4. INT-T-002 L135: student implies a policy was sent; Q-U05.
5. INT-T-002 file 409 (L390): "tools and memory ... hand in hand"; D1, Q-J08.
6. INT-T-002 L221: "in theory" hedge; Q-J26, Q-J06, Q-J27, D4.
7. E591-E595, E455, E212, E228, INT-T-003 L214: novelty and monthly search; Q-J22.
8. E705-E706: 27B helper model; Q-J21, Q-J24.
9. INT-T-003 L284-L294 (file 303-313): student's one-line problem statement (context window) accepted ("that's the main problem we are solving"); beyond-window handling still not addressed (Q-J13). INT-T-002 L384 (file 403) "even this memory can get big so I can choose part of the memory": a partial hint for Q-J13, in memory not tools.

## Tally (27 rows: J16-J29 = 14, B = 4, C = 2, D = 7)
CONFIRMED 17 (J16, J17, J18, J19, J21, J23, J24, J27, J29, U19, U07, U02/U03, C1, D2, D3, D5, D6); OVERSTATED 7 (J22, J25, J26, J28, C2 reading, D4, D7); UNDERSTATED 3 (J20, U05, D1); WRONG LINE 1 (L397 to L404, in J22 and J08); NOT SUPPORTED 0.
