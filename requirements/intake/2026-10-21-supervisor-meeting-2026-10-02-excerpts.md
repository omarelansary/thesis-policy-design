---
type: "intake-text"
id: "INT-T-004"
authorization: "AUTH-018"
supplied_by: "human (user): three Google Docs links in the message of 2026-10-21; the lead downloaded each with the export-as-plain-text URL (curl, 2026-10-21) into the session scratchpad, outside the repository, and copied the approved part here"
supplied_utc: "2026-10-21 (time of day not recorded)"
form: "transcript"
stated_nature: "Six approved excerpts of the automatic transcript of the meeting of 2 October 2026, as exported from the Google Doc the user linked; the passages hold the supervisor's statements; the student's reports of his earlier experiments and the Gemini notes are excluded by the human's intake decision of 2026-10-21. Each excerpt is preceded by a bracketed line giving its export line range and time-codes (lead's locator, not part of the transcript)."
meeting: "Automatic Tool Discovery"
meeting_date: "2026-10-02"
speaker_per_supplier: "A.F.M. Mohimenul Joaa (supervisor) and omar elansary (the student), as labelled in the transcript"
original_source_claim: "https://docs.google.com/document/d/1CtzIl4EdPqDqPKXIWoUVFZUvRwv7RjWSG0bRZ8faFBU/edit?usp=sharing (exported as text; Google document, editable by its owners)"
original_sha256: "caaa78f152e09ed444c96ec15879ac62776070af4c801732d0691496ca31655c (SHA-256 of the exported text as downloaded, before BOM removal and line-ending normalisation)"
approved_ranges: "export lines 181-236 (00:10:16-00:13:11); export lines 362-488 (00:26:09-00:34:35); export lines 500-672 (00:35:52-00:46:52); export lines 676-676 (00:46:52, one line); export lines 686-792 (00:47:52-00:54:03); export lines 802-829 (00:55:30-end)"
excluded: "export lines 1-180 (Gemini notes and the student's report of earlier experiments), 237-361, 489-499, 673-675, 677-685, 793-801, 830-832 (the student's reports of earlier experimental work, and the closing line)"
caveats: "(1) Automatic speech recognition by Google Meet/Gemini; wording such as 'nobility' (novelty), 'Exeutor' (Executor), 'cloud' (Claude), 'NCP atlas' (MCP-Atlas), 'quy expansion' (query expansion) is preserved as exported and not corrected; (2) the 'Gemini notes' sections (summary, decisions, details, next steps) are machine-generated summaries, not the participants' words, and the export itself says to review them for accuracy; only transcript lines carry the speakers' words; (3) the transcript says it is 'editable' and 'might contain errors', so a later edit of the original would not be seen here; (4) speaker labels are the transcript's own; (5) line numbers refer to the export as downloaded (UTF-8 BOM removed, CRLF normalised to LF), so body line N is export line N for whole-document records."
body_sha256: "faba79eecd1a8b2f913e487ad51871add36732ecdc7cc9a966163c0ef57f549b"
---
<<<BEGIN-VERBATIM
[export lines 181-236, transcript time-codes 00:10:16-00:13:11]
00:10:16


omar elansary: Second, please.
A.F.M. Mohimenul Joaa: So you are actually filtering out tools from passive registry and giving some of them to the active registry and while doing that you are ensuring that accuracy is not dropping.
omar elansary: The accus is not what again.
A.F.M. Mohimenul Joaa: accuracy is not dropping.
omar elansary: Yes, for sure. Yes, we are on. Yes, that's a good that's a good summarization. Thank you.
A.F.M. Mohimenul Joaa: Okay. So now you can do it in multiple ways.
omar elansary: Yes. Amen.
A.F.M. Mohimenul Joaa: So I'm again I'm telling it filteration because let's say you have 20 30 tools in the passive registry. You are taking maybe eight or 10 tools from them. Okay, it's just a basic filteration. And now why it's filteration? The logic is not defined anywhere. No one know what is the best filteration logic which will give me minimal amount of tool with maximal amount of accuracy.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: That's the optimization problem we're solving here.
omar elansary: Yes.




00:11:13


A.F.M. Mohimenul Joaa: Minimal amount of tool maximum amount of accuracy. So first you need the baseline. So initially when we talked I think in the last time uh I told you that you need the baseline. So the baseline would be giving all the tools that you have in your passive registry and then uh then figuring out the accuracy I mean running the model and seeing like what is the accuracy. Okay.
omar elansary: I I have made so I have done so.
A.F.M. Mohimenul Joaa: Okay. So you have the baseline accuracy.
omar elansary: Mhm. Yes.
A.F.M. Mohimenul Joaa: Now you want to match the baseline accuracy while giving lesser and lesser tool each time.
omar elansary: I have done so also.
A.F.M. Mohimenul Joaa: So okay.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: Okay.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: uh now as you reduce the number of tools you have some kind of mechanism like uh maybe by keyword search, hybrid search, semantic search those are very basic uh ideas but that that's the novelty. Okay.




00:12:09


A.F.M. Mohimenul Joaa: So you have to figure out what is working and what is not working because it's a master's thesis otherwise if you just norm if you just do normal retrieval then okay okay you have done
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: something but why is the novey at least you have to have some kind of findings okay retrieval
omar elansary: Yes.
A.F.M. Mohimenul Joaa: works but for these cases retrieval doesn't work okay keyword search work
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: better for these cases while retrieval work for those cases maybe something else okay
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: so This filteration is your noity like you have to figure out algorithm
omar elansary: Okay.
A.F.M. Mohimenul Joaa: which doesn't again there is so many optimization thing you have to do okay because you cannot use many tokens because you're saving tokens the main uh proposition of your work is that I'm saving some tokens but by not giving all the tools to the L1 then again
omar elansary: Just
A.F.M. Mohimenul Joaa: if you use many many more token to filter out the tools then there is no value you are doing more work to save token.




[export lines 362-488, transcript time-codes 00:26:09-00:34:35]
00:26:09


A.F.M. Mohimenul Joaa: I no Omar you have to think it from first principle. So even if you solve it for one LLM,
omar elansary: Yeah,
A.F.M. Mohimenul Joaa: you cannot solve it for all LM.
omar elansary: just
A.F.M. Mohimenul Joaa: Every LLM thinks differently. Okay. They have their own ways of thinking. So you are trying to do one of the hardest thing that is uh any of us wanted to know it's like interpretability problem like how did you come up with this this is a question that no one of none of us know okay that's why we are not using llm in the very critical areas like uh
omar elansary: Mhm. Yes.
A.F.M. Mohimenul Joaa: suggesting medicine or maybe uh judging someone for someone's crime so we are still figuring it out okay that's a very big problem that you are going into and I don't think you will find a solution the way you are trying to do because you are use again using the same LLM to tell you like how to find this




00:26:57


omar elansary: Yes.
A.F.M. Mohimenul Joaa: solution. It's never going to work.
omar elansary: Mhm. Yes.
A.F.M. Mohimenul Joaa: And if even if you look at the industry, the industry is trying to solve the same problem for a couple of years right now. Okay? But we don't have the solution.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: It's a black box. So you have to look it from a different lens.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: Look it from a different lens. Now how can you look it from a different lens? So let's say you have a tool.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: Okay. Now this MCP thingy why MCP thing works you have to first look look into that MCP works because why MCP works with
omar elansary: What? Oh,
A.F.M. Mohimenul Joaa: LLM that's the first thing that you have to ask MCP works because in every tool you are actually giving what this tool does and whatever par what parameter this tool takes and what will be the output of this tool you are giving a way for




00:27:51


omar elansary: maybe
A.F.M. Mohimenul Joaa: the LLM to know what will be done by this tool. Now let's say if you say uh addition tool let's say you say the name of the tool is addition but inside the tool you do subtraction will lm know
omar elansary: No.
A.F.M. Mohimenul Joaa: is that LLM's responsibility to figure it out no believes you okay LLM always believes
omar elansary: No.
A.F.M. Mohimenul Joaa: you it says okay if you you say this addition it should be addition I will just call this tool okay so understand this very first thing that tools works because you give some kind of assumption to the lln that if it call this tool it will do this kind of task okay just like humans how let's say if I start a laptop if I click on zoom link my assumption is I will be able to connect with Omar or maybe this is
omar elansary: What is it?
A.F.M. Mohimenul Joaa: a provide me this link so I will be able to talk with Omar now let's say if it doesn't let me talk with Omar and connect with some random guy.




00:28:58


A.F.M. Mohimenul Joaa: Come on. It was a assumption. Okay. And it works like that. That's why we work like that. The same thing LLM works because the assumption was like that. Now let's come back to this whole idea to in for your case. So you have some tools. You want the LLM to know what these tools will do. Now you don't want to give the LLM all the tools because your assumption is you don't need all the tools to run the current task that you that is at hand.
omar elansary: Yes. Mhm.
A.F.M. Mohimenul Joaa: Okay. So how do you remove those? So the initial idea is obviously semantic can you cannot beat semantic with any of those if you look keyword or whatever if you do semantic properly I mean semantic
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: search properly with a bigger model uh I mean with a uh awesome encoding model it will
omar elansary: And
A.F.M. Mohimenul Joaa: beat you always that's the first principle if you look at it because why you may ask Bye.




00:29:58


A.F.M. Mohimenul Joaa: Because semantic is doing the same thing LLM is doing. What is a vector search? In semantic search, what you do? You search over a vector I mean vector database.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So in the vector database,
omar elansary: Yes.
A.F.M. Mohimenul Joaa: there are encoding embeddings. So the embeddings are the representation of the text like the addition. This function will add one a plus b. This is a text. You are just converting this text into embedding and saving it in a vector database and then searching the
omar elansary: Oops.
A.F.M. Mohimenul Joaa: cosine similarity of the text. If you look at the problem, the problem at hand is you don't have the same text as the query. The query is can you do this math? Okay, the query is can you do this math in the equation there? Maybe a plus b + c minus d into f whatever. Okay. Then what the LLM is doing is looking at this and there is some functions which says addition which says subtraction which says multiplication.




00:31:00


A.F.M. Mohimenul Joaa: It's look at the equation and figure out okay this equation looks like addition this part is look like subtraction this part looks like multiplication. Okay I have tools. So why cannot I why why don't I use those tools? Okay if you look it from the semantic point of view there is no similarity. You said can you do this math? Whereas the text in the functions are addition, subtraction, multiplication. You never said addition, subtraction, multiplication. Did you?
omar elansary: No, I never
A.F.M. Mohimenul Joaa: Yes. So that's the problem. So how do we solve this quy expansion? What does ky expansion mean? I mean that this is one of the first principle. If you look if you break the problem from one at a layer, the problem is you say you can you do this math. If you expand this then this will come up like there is a subtraction, there is addition, there is multiplication.




00:31:53


A.F.M. Mohimenul Joaa: Okay. Now there are some similarity between the words. Okay. Now if you look at the tools the tool says okay can you do addition can you do sub? You can do subtraction by using this tool you can do addition by this tool and multiplication by this tool. And you have the query where there is also this word presence. Then if you run cosine simulator obviously the cosine similarity score will be higher than just running on can you do this math. Make sense?
omar elansary: Yes. And we are on the same page actually.
A.F.M. Mohimenul Joaa: Okay.
omar elansary: I
A.F.M. Mohimenul Joaa: So until until this is already what we already know. There is no novelty. Whatever I have said you already said there is no novelty in that because retrieval people already
omar elansary: Wait.
A.F.M. Mohimenul Joaa: know it works. Qu expansion people already know. Why qu expansion is important? Because of these reasons.




00:32:41


A.F.M. Mohimenul Joaa: Okay people already know that. So this is already known. Now, now here comes your problem. So, your problem is, can I somehow figure this out? Not by retrieval. I never stayed you. have to do retrieval order. Okay,
omar elansary: Thank you.
A.F.M. Mohimenul Joaa: I always said it's a policy.
omar elansary: Oops.
A.F.M. Mohimenul Joaa: You have to find the policy. Okay, by making it vague. Why why I call it policy? Why I never called it retrieval? Because retrieval is only one policy. Okay, there may be so so many other policies. But the first principle always says again keyword search will never work. Any symbolic algorithm will never work here. Even the semantic one is not working. How would you I mean how would you assume that a keyword search will work here? Because keyword search is always a layer comes a layer before semantic search.




00:33:38


A.F.M. Mohimenul Joaa: Keyword search is just counting the keywords that is matched between two different queries.
omar elansary: It's
A.F.M. Mohimenul Joaa: Okay. And semantic it it's a layer after that. It just create a embedding from the whole query and then figure out like is there a similarity between these embeddings. So it's made it a little bit abstract. So you don't have to match direct words like wife and spouse both means the same. So the embedding will be same. You don't have to write wife as a wife. You can also write I mean you can also interchangeably use a spouse. Okay.
omar elansary: I I have one one after you finish I have one thing to say.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: Um there is thing that you said that I would like to uh elaborate. You said that retrieval is a part of a policy or one not part retrieval
A.F.M. Mohimenul Joaa: Good. Yes.
omar elansary: is one way uh of again you said that is one




[export lines 500-672, transcript time-codes 00:35:52-00:46:52]
00:35:52


omar elansary: So, I'm looking for nothing and I'm don't know what I'm looking about. Um this part is I would like to need I need an elaboration about
A.F.M. Mohimenul Joaa: Okay. So you are only looking from one lens. Let's just go back and zoom out. Okay. Not zoom in. You are again zooming in on retrieval.
omar elansary: okay because Oh yeah.
A.F.M. Mohimenul Joaa: Okay. If you zoom out.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Okay.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: Okay. So if you zoom out you will see I don't have to keep every detail initially to the llm okay lm is the key embedding is the key okay we
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: cannot go I mean you can never make a symbolic algorithm which will give you better result for all the cases that alm can handle you may come up with one which will give you better result for one or two cases okay but for all the cases you
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: will never be able to Because first principle says it is not possible.




00:36:49


A.F.M. Mohimenul Joaa: Okay.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: Because if you look at the technology it's superior than keyword search obviously. Okay. Now as that is you have to write it down as a fact. Okay. That is a fact. You cannot change it. Now if you zoom out if you say I will give only the tools that is relevant to this query to the LLM. That is a bad assumption. Rather your idea was never to filter out tools. Your idea was to save tokens. What was the problem?
omar elansary: Yes.
A.F.M. Mohimenul Joaa: The problem was to save token.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: We don't want to give all the token that is not necessary for the LLM at the first page. So for example, let's say if I only say hi and I give 30, 20, 400 tools to the LLM. What's the point? What's the point? It will just be a save uh input token and I will incur so many cost.




00:37:43


A.F.M. Mohimenul Joaa: So again the problem is saving token and
omar elansary: save saving and and and and maintaining the accuracy.
A.F.M. Mohimenul Joaa: uh yes token and
omar elansary: So right now I have saved the token but I cannot maintain the accuracy.
A.F.M. Mohimenul Joaa: accuracy.
omar elansary: That's the main problem that I'm trying to solve by time.
A.F.M. Mohimenul Joaa: Yes yes yes saving token and mary accuracy. So if you look zoom out you can say I will give you partial information not full information. You may ask for full information when you need it. Okay that's one of the policy you can go for that. Now obviously you as you said retrieval is part of the policy. So yeah I can filter out tools but not so harshly that I will filter out tools which are not important. I mean tools which are important. Okay. So what I can do is like I will just filter out tools which I think will never be important for this query. Okay.




00:38:35


A.F.M. Mohimenul Joaa: Okay. By doing that maybe there are 100 tools. I reduce it down to 60 tools. Okay. I at least remove 40 big win for you. Okay. Now from 60 I cannot say like which tools are important.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: I mean which tools are not important because all of them looks important to me. Okay. As at least from the semantic point of view. Okay. because there is math and there is addition. Math is related to addition. So yeah all of them may be important. I don't know. So then how would you do that? Again one solution is query expansion. Another solution is you can you can again categorize the tools. You have six tools. Categorize them in multiple section. Figure out okay there are 20 tools. This number is not rigid again.




00:39:20


A.F.M. Mohimenul Joaa: Okay this 20 is not rigid. You figure it out by yourself. This 60 is not rigid. 20 tools is very important. Maybe after query expansion what I found is like 20 is very relevant. Okay, then give the 20 then from 20 to 40 is not that
omar elansary: the I can see it's
A.F.M. Mohimenul Joaa: relevant. Okay, not that relevant but maybe important. So I at least need the LLM to know like these tool exists. If you need more information ask I will give you. Okay, from 40 to 60 those are important but the LLM just need to know the name of the tool. It doesn't need to know anything about the tool anything else about the tool. So you are cutting down tokens while keeping the accuracy. This is I mean this is just only one way. Okay. I'm not saying this is the best way but you have to look it from this lens.




00:40:13


A.F.M. Mohimenul Joaa: It's not always like okay give or don't give. You can also give partial information. Is it clear? Hello.
omar elansary: Can you hear me? I can hear you.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Hello.
A.F.M. Mohimenul Joaa: Uh is it clear what I what I what I just mentioned?
omar elansary: Yes, that's cool.
A.F.M. Mohimenul Joaa: Okay. Then again uh if you look at the current startups, there are many startup. I already shared this exeutor with you. Did I uh I did I
omar elansary: No, I haven't seen them.
A.F.M. Mohimenul Joaa: did share this executor. Uh this is a startup and they're doing the same stuff. Okay. There are multiple other if you just do a cloud web search you will find so many other you just need to write down the problem the problem you have and you you need to ask it like give me all the startup or all the opensource projects that is already working on that you will find multiple okay




00:41:23


omar elansary: Mhm.
A.F.M. Mohimenul Joaa: and you will also find papers on that so that is a very good source from where you can see what is already happening and what is not happening because don't take all the burden on yourself Okay, if someone have already figured out something,
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: you should use it. You should improve it.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: Okay, you should never in reinvent the wheel. So now what right now what you are doing is you are reinventing the wheel. What I have said,
omar elansary: Um
A.F.M. Mohimenul Joaa: what I have said this partial thingy this is also this also cames out from someone else. I didn't invent it. Okay, I just read their doc and figured out. Okay. Yeah, that's awesome idea. Someone else have come up with this idea, but that is a useful idea. Why shouldn't I use it? Okay.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So, first thing you need to do every month, not at the start of your master's thesis, every month of your master's thesis, you should always search the web and figure out what is the kind status.




00:42:20


A.F.M. Mohimenul Joaa: Okay?
omar elansary: Love it.
A.F.M. Mohimenul Joaa: what is working, what is not working, what is the industry uh practice and what is the current sa state-of-the-art for this and if you look at executor they are doing the same thing that I already mentioned okay they are just giving you partial information that they are just creating a instead of giving all the information to the LLM they're creating some instruction for the LM and letting it know okay you have these tools it's actually giving some extra tools tools. If you look at it, if you look at without executor, with exeutor is actually giving some extra tools. Without executor, it's just listing down all the tools, okay, that you have given it in the MCD server. So, it's actually this amount of tokens. And with executor,
omar elansary: Okay.
A.F.M. Mohimenul Joaa: what it's doing, it's just not giving any tool, but again, you have to come out to your own policy. What it's doing is like, okay, available connection prefix, these are the connections.




00:43:19


A.F.M. Mohimenul Joaa: So it says like you can connect with GitHub, you can connect with Strike, you can connect with Zer and Sentry and how to connect with those. You don't need to know. I will give you some tools. What are the tools? These are the tools. If you need the uh tool search, then do the tool search. If you need uh the path or some item, do that. If you need the detail of the tool, do that. If you need the result of any tool, you can also do that. So this is some extra tools that is actually giving to the algorithm. Okay, instead of giving all the tools and this is open source why shouldn't you use it?
omar elansary: I haven't seen it.
A.F.M. Mohimenul Joaa: You should the first thing that you the first thing you should do is just go to this GitHub repo download this run this and figure out okay benchmark it how much uh token are they saving and what are the accuracy for them.




00:44:07


omar elansary: Yeah.
A.F.M. Mohimenul Joaa: This is your baseline. You you should have multiple baselines. Even if you try to publish a paper, people will ask the same question. There are already many many research on this field. Why they not in your paper? Okay. And with plot this is so much easier. You can
omar elansary: I have been running code as you can see as you can see I've been running code for a long time and I have I don't know maybe maybe my my criteria was basically about retrieval that's why it It never saw this. Uh
A.F.M. Mohimenul Joaa: um you have to write very good prompts. So right now if you look we are not doing the work everything is done by cloud. Then the only way you do is either you write very good prompt or you use the special plug-in that people have already built for that. So for example, let's say I I need to write a paper.




00:44:59


A.F.M. Mohimenul Joaa: I don't write a paper anymore. Okay, at least not the draft version. Yeah, I obviously go through the paper that CL and then edit it. Okay, but the draft version,
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: why should I waste my time? So there is multiple plugin you can just search make papering skill for plot and if you go it's very
omar elansary: Oh.
A.F.M. Mohimenul Joaa: famous.
omar elansary: Listen.
A.F.M. Mohimenul Joaa: Sorry, not this one. This is not that famous. I think this one. Yes, look at it. 50k start. So you will also find something similar to that. Okay, you have to figure out which plug-in to use, which tool to use with plot also. These are also tools. Okay, they are nothing special,
omar elansary: Yes.
A.F.M. Mohimenul Joaa: the same things. And then uh give it proper prompt. Okay,
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: initially uh when you are starting the research, you should uh not give very big task to the task plot.




00:45:54


A.F.M. Mohimenul Joaa: Okay, you should first uh go hand in hand with plot and see all the results that plot comes up with and guide it at any step and when you have the results then you can start uh automating more and more. Okay.
omar elansary: Um, let's say now I'm more disappointed.
A.F.M. Mohimenul Joaa: No,
omar elansary: But the question is I
A.F.M. Mohimenul Joaa: don't don't get more disappointed. This one I already shared with you two months earlier.
omar elansary: I because you mentioned uh Behan someone else. So I thought this was so
A.F.M. Mohimenul Joaa: Uh I don't know. I don't know. I think I mentioned you. Uh yes.
omar elansary: um it was for something like this.
A.F.M. Mohimenul Joaa: You see when was it?
omar elansary: It's Bahai also this one Bahai.
A.F.M. Mohimenul Joaa: Uh it's August 29.
omar elansary: So I thought I thought You just mentioned
A.F.M. Mohimenul Joaa: It's from August 29.
omar elansary: this one behind. So I just said
A.F.M. Mohimenul Joaa: Oh, okay. Okay.




[export lines 676-676, transcript time-codes 00:46:52, one line]
A.F.M. Mohimenul Joaa: Okay. So, so, so I just forwarded it from someone else that's why. Okay. So, it cames from there. But what I
[export lines 686-792, transcript time-codes 00:47:52-00:54:03]
00:47:52


A.F.M. Mohimenul Joaa: uh I would say keep it as it is. Create a new branch and First start analyzing what is available. Okay,
omar elansary: Okay.
A.F.M. Mohimenul Joaa: see all the papers uh read all the papers and then uh all the opensource projects and see how they are doing it. And again you don't need to remember all the stuff. The main thing is retrieval will sorry semantic search will always win over keyword search. Okay. Second, uh, query expansion is a very awesome tool that you have. Now, what is query expansion?
omar elansary: Yes.
A.F.M. Mohimenul Joaa: The idea is you have a query, you are expanding it. The same thing applies. You have some description, you can narrow it down. Okay?
omar elansary: But credit expansion credit expansion needs LM.
A.F.M. Mohimenul Joaa: You can summarize it.
omar elansary: So um we will drop the cost constraint.
A.F.M. Mohimenul Joaa: Uh, no, we will not drop the cost. first con state but




00:48:56


omar elansary: I can use a 27B. It's it would be really good for quitting.
A.F.M. Mohimenul Joaa: yes you can use 27B but again uh query expansion is only necess I mean how should I put it so if you use any of this tool at a specific point where it's necessary it's not going to in not going to give you very much uh cost okay the cost will not be that much high. So for example,
omar elansary: Okay. Yeah.
A.F.M. Mohimenul Joaa: let's say you have identified five tools.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: Now you don't know which one is the target tool. Okay. Then you will obviously do query expansion will you not? What does the LM do? It just do reasoning uh tokens. It use reasoning tokens. So what is reasoning token? It just says okay I need to do this math and what is in this map?
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: There is addition, subtraction and multiplication. Okay, I have these tools.




00:49:48


A.F.M. Mohimenul Joaa: Uh what are the tools? It's addition, multiplication, subtraction. Okay, I can just call them. Okay, but I need to find out the order. Uh, so ma for mathematics, the multiplication comes first, then addition and then subtraction. Okay, then I would call them in this order. So it just thought it out loud. That's good expansion, isn't it?
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So it's already using it.
omar elansary: Please.
A.F.M. Mohimenul Joaa: If you use it earlier, then what what's the harm? But you cannot use it on every tool.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: You have to narrow it down first. Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So,
omar elansary: Yes.
A.F.M. Mohimenul Joaa: so you have a very good uh proposition. So, again uh here hear it out loud. Right now the problem is if you look at any agentic tool the problem is the baseline is you give it all the tools.
omar elansary: Mhm.




00:50:40


A.F.M. Mohimenul Joaa: Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: And that's very very expensive. Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: And just narrow it down. the first step just narrow it down and saying okay these tools are not necessary I only need these tools maybe it's just narrowing down 50% that is a huge win you are reducing token by 50%.
omar elansary: Maybe
A.F.M. Mohimenul Joaa: Now from 50% to 10% that's a battle you have to work through. Okay.
omar elansary: There.
A.F.M. Mohimenul Joaa: If you reduce until 50% the accuracy is not hit at all. It should be like that the accuracy most in most of the cases maybe not for NCP atlas I don't know but for most uh production system 50% token reduction is just uh the lowhanging fruit. Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So yes uh again I I also shared maybe something make make your experiment very uh simple and less expensive okay you don't need to run all the things you don't you have maybe 800 tools 800 queries you don't need to do that figure out 20 just uh start working with 20 sample and see what's the




00:52:01


omar elansary: I do this as dry on here. I always do a hypothesis and then try you continue with the hyp.
A.F.M. Mohimenul Joaa: Okay.
omar elansary: But yeah,
A.F.M. Mohimenul Joaa: Uh so Omar I think we need uh frequent meetings.
omar elansary: yeah, I guess so.
A.F.M. Mohimenul Joaa: So um yes uh let's meet on Monday and within this weekend uh I would recommend just at least figure out the policy and you don't need to run any experiment. Okay. on your mind.
omar elansary: Yes, sir.
A.F.M. Mohimenul Joaa: You start with a paper with the empty white paper. Okay? Write down facts all the facts that you have. Write down all the projects that you found find that you find from uh web search and uh and the papers. Okay? Read those papers.
omar elansary: I was seeing
A.F.M. Mohimenul Joaa: Read those projects and take the good ideas and write your plan. I will narrow it down. Narrow the tools step by step. Step one, discard all the irrelevant tools.




00:52:58


A.F.M. Mohimenul Joaa: Step two, uh take the remaining tools and uh maybe uh divide them down in a way that only the first uh n number of tools will get the whole description and the remaining ones will only get the name of the tool. So something like that. Okay. And step three, step four, step five, something like this. So each step is there to save some token.
omar elansary: Thank
A.F.M. Mohimenul Joaa: Okay, same some token. Then again you also have to think like what if what if the filteration that I'm doing is is wrong. Then you should give some way for the LM to query the tools that is in the passive registry and get the details from those tools. Okay.
omar elansary: you. Right here.
A.F.M. Mohimenul Joaa: So it's not like you have to save token for each turn. You need to save token for a number of turns. So for example,
omar elansary: Yes.
A.F.M. Mohimenul Joaa: let's say You talked with the LM for 100 times and you save token 80%.




00:54:03


A.F.M. Mohimenul Joaa: Okay, you saved 80% of the token. That's a win.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: But in this 100 time, one time what you have done is like earlier it was uh 2,000 token. Now it's 4,000 token. It doesn't matter does it because for the other turns you have saved the token. So it's only one one turn that is actually using more token than the earlier. It can happen. So you have to look it from the global lens,
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: not from a local one. Okay?
[export lines 802-829, transcript time-codes 00:55:30-end]
A.F.M. Mohimenul Joaa: Yes. Yes. Yes. Yes. Because you need to do a a proper search for papers and open source projects and then
omar elansary: okay Yes. Yes.
A.F.M. Mohimenul Joaa: uh at least write the draft version of uh your policy. You don't need to implement anything. We can discuss the policy. I thought like you can't find out your policy by yourself but uh right now I think it's it would be better if you just tell me your policy first then we will go through all the basic things like will this work what the first principle says and maybe we will assume some stuff and narrow down your uh your experiments.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Okay. Great.
A.F.M. Mohimenul Joaa: Okay,
omar elansary: Thank you for your time.
A.F.M. Mohimenul Joaa: then let's meet on but uh on Monday I don't have time in the morning.
omar elansary: I'm very sorry for all of this.
A.F.M. Mohimenul Joaa: So maybe Maybe in the afternoon.
omar elansary: We can do it. Yeah, we can do it at 45. It's okay for me. If you are still at the still at the If you are still at work,
A.F.M. Mohimenul Joaa: Uh 3:30. Will that work?
omar elansary: I will confirm on you maybe tomorrow today by night
A.F.M. Mohimenul Joaa: Okay.
omar elansary: day.
A.F.M. Mohimenul Joaa: Okay.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Okay. Okay then.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Chow. Chiao.
omar elansary: Thank you very much.
A.F.M. Mohimenul Joaa: Bye-bye.
omar elansary: Byebye.




END-VERBATIM>>>
