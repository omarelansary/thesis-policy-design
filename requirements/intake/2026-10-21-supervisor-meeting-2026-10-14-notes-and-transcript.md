---
type: "intake-text"
id: "INT-T-003"
authorization: "AUTH-018"
supplied_by: "human (user): three Google Docs links in the message of 2026-10-21; the lead downloaded each with the export-as-plain-text URL (curl, 2026-10-21) into the session scratchpad, outside the repository, and copied the approved part here"
supplied_utc: "2026-10-21 (time of day not recorded)"
form: "transcript"
stated_nature: "Gemini meeting notes and the full automatic transcript of the supervisor meeting of 14 October 2026, as exported from the Google Doc the user linked (the same document INT-T-001 names as the supplier-claimed origin of its nine excerpts). Whole document admitted except one line."
meeting: "Automatic Tool Discovery"
meeting_date: "2026-10-14"
speaker_per_supplier: "A.F.M. Mohimenul Joaa (supervisor) and omar elansary (the student), as labelled in the transcript"
original_source_claim: "https://docs.google.com/document/d/1BOvGNy-q5WQpc_V6D6v6TDr2UlBRzjaEJjwJmMyxHOA/edit?usp=sharing (exported as text; Google document, editable by its owners)"
original_sha256: "4bbe741be00de1a259a8668f8be5327214b6af65ef306b7d465d8bcc0f73ab70 (SHA-256 of the exported text as downloaded, before BOM removal and line-ending normalisation)"
approved_ranges: "whole export except line 106"
excluded: "line 106 (replaced in the body by a bracketed placeholder so that body line N stays export line N)"
caveats: "(1) Automatic speech recognition by Google Meet/Gemini; wording such as 'nobility' (novelty), 'Exeutor' (Executor), 'cloud' (Claude), 'NCP atlas' (MCP-Atlas), 'quy expansion' (query expansion) is preserved as exported and not corrected; (2) the 'Gemini notes' sections (summary, decisions, details, next steps) are machine-generated summaries, not the participants' words, and the export itself says to review them for accuracy; only transcript lines carry the speakers' words; (3) the transcript says it is 'editable' and 'might contain errors', so a later edit of the original would not be seen here; (4) speaker labels are the transcript's own; (5) line numbers refer to the export as downloaded (UTF-8 BOM removed, CRLF normalised to LF), so body line N is export line N for whole-document records."
body_sha256: "e8e8f3996d58c3add7ca38e5981050d24ad9933eb0e130ae4c74f0b92244175c"
---
<<<BEGIN-VERBATIM
Please rate the new Quick notes tab by taking a short survey.
Automatic Tool Discovery


Oct 14, 2026


Retrieval mechanism review and core question clarification leading to systematic graph-based policy design.


Research Question and Thesis Requirements
* A.F.M. Mohimenul Joaa confirmed the research question focuses on identifying optimal methods to reduce tool counts for LLMs while maintaining high accuracy.
* A master's thesis requires original experimental findings and systematic evaluation rather than a basic literature review or survey paper.


Tool Filtering Methodologies and Systematic Policy
* Evaluated various mechanism families including static retrieval, progressive disclosure, hierarchy-based structuring, and gateway architectures.
* Academic novelty stems from combining existing approaches into a systematic, multi-stage filtering policy driven by operational context.
* Tool reduction progressively scales down large tool sets across multiple stages, allowing tools to be re-evaluated within a graph-based policy.


Next steps
* [omar elansary] Define Tool Policy: Develop a systematic graph and policy consisting of decision questions to filter down tool sets for Large Language Models. This approach must outline specific stages to reduce the number of tools while maintaining output quality.








Want to see more? View the full notes
Tip: You can always access your full notes from the left sidebar.






You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes
Oct 14, 2026
Automatic Tool Discovery
Attachments Automatic Tool Discovery
Meeting records Transcript Recording 




Summary
Retrieval mechanism review and core question clarification leading to systematic graph-based policy design.

Review of Retrieval Mechanisms
Static retrieval and gateway architectures were shared. Technical audio difficulties occurred during the review.

Core Research Question Clarification
Research question targets reducing tool count while maintaining accuracy. Focus remains on evaluating narrowed methodologies.

Systematic Graph-Based Policy
Design a multi-stage graph-based policy instead of writing code. Filter tools progressively through decision trees.




Decisions
Aligned
* Retention of current research question formulation The participants agreed to keep the existing research question focusing on finding the most optimal method to reduce tool count while maintaining high accuracy.
* Adoption of multi-stage graph filtering approach The participants agreed to build a systematic, multi-stage graph policy for filtering tools through successive stages instead of implementing a single-step reduction.




Next steps
* [omar elansary] Define Tool Policy: Develop a systematic graph and policy consisting of decision questions to filter down tool sets for Large Language Models. This approach must outline specific stages to reduce the number of tools while maintaining output quality.




Details
* Review of Retrieval Mechanisms and Architecture Ideas: omar elansary shared a PDF detailing updates and various mechanism families, including static retrieval, progressive retrieval, deferred progressive disclosure, hierarchy-based tools, and gateway architectures (00:00:05). omar elansary explained that the gateway architecture maintains a fixed number of tools in context and fetches more as needed, whereas the hierarchy-based approach requires a pre-structured database of tools (00:01:48). A.F.M. Mohimenul Joaa experienced technical difficulties and audio interruptions while reviewing these proposals (00:04:42).
* Clarification of the Core Research Question: Due to audio issues, A.F.M. Mohimenul Joaa read aloud omar elansary's written questions concerning thesis contributions, scoping, and success metrics (00:05:42). A.F.M. Mohimenul Joaa clarified that the research question remains unchanged: determining which method is the most optimal way to reduce the count of tools while keeping accuracy as high as possible. Both participants aligned on the understanding that omar elansary's focus should be on evaluating the narrowed-down methodologies rather than altering the core question (00:07:04).
* Thesis Requirements and Novelty Definition: A.F.M. Mohimenul Joaa explained the difference between a publishable evaluation paper and a literature review, emphasizing that a master's thesis requires original empirical findings evaluated against existing baselines rather than just a survey (00:12:13). When omar elansary inquired about establishing novelty, A.F.M. Mohimenul Joaa noted that true novelty in this context involves combining different approaches, thoroughly understanding the core problem, and demonstrating what works and what does not (00:14:32).
* Contextual Tool Filtering and Multi-Step Reduction: A.F.M. Mohimenul Joaa used an AI salesman example to illustrate how the current context can immediately filter out irrelevant tools, such as excluding business intelligence tools when the agent is speaking with a customer rather than the business owner (00:17:37). They discussed how tool reduction should not be a single-step process, but rather a multi-stage funnel—such as reducing 1,000 tools down to 800, then 500, then 200, and finally 10—using context, semantic search, and execution policies (00:19:57) (00:21:47).
* Developing a Systematic Graph-Based Policy: omar elansary proposed combining these solutions like a puzzle with connecting bridges, asking if this constituted a valid thesis approach (00:24:31). A.F.M. Mohimenul Joaa confirmed that the thesis was already officially approved, but emphasized that a publishable paper requires a systematic approach (00:25:36). A.F.M. Mohimenul Joaa instructed omar elansary not to implement any code yet, but instead to design a graph-based policy—a multi-stage decision tree where tools can be filtered out at one stage and re-added at a later stage if found relevant (00:26:43).
* Meeting Wrap-Up and Deadlines: omar elansary requested a copy of the meeting transcription to review past discussions, and A.F.M. Mohimenul Joaa confirmed that the transcript link provided in the group description would be accessible (00:28:35). A.F.M. Mohimenul Joaa established a firm deadline for omar elansary to develop and deliver the tool-filtering policy by next Wednesday at 11:00 AM (00:30:12).




You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes
How is the quality of these specific notes? Take a short survey to let us know your feedback, including how helpful the notes were for your needs.
Oct 14, 2026
Automatic Tool Discovery - Transcript
00:00:05


A.F.M. Mohimenul Joaa: Yes, we can start.
omar elansary: Um, have you seen what I have sent here?
A.F.M. Mohimenul Joaa: Uh, what have you sent me? Oh, the dog.
omar elansary: The PDF with Yes.
A.F.M. Mohimenul Joaa: Uh no, but uh can you help me go through it right now because I I actually it just got out of
omar elansary: Yeah,
A.F.M. Mohimenul Joaa: my head. Okay.
omar elansary: I think I can.
A.F.M. Mohimenul Joaa: These updates since meeting since last meeting.
omar elansary: I tried to make it as short as possible.
[export line 106 not admitted: the supervisor reads out a results sentence from the student's earlier PDF (earlier experimental content, excluded by the human's intake decision of 2026-10-21)]
omar elansary: Um, give me a second.
A.F.M. Mohimenul Joaa: static and progressive retrieval deferred progressive disclosure? So I'm not understanding what does the mean by only these words.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: I mean I understand there are some different kind of retrieval mechanism but uh can
omar elansary: So,
A.F.M. Mohimenul Joaa: you give a little bit more cont




00:01:48


omar elansary: so basically um so basically each each one of them is doing things. So basically the first one is the retrieval that I was doing. Um, you were right about me just focusing on one stuff and focusing on the retrieval. But to be honest, I was uh completely um um blind blind about that we can solve stuff without even uh giving the right tool because we're not aiming for the best accuracy. We're aiming for the balance. Okay. So the best first is the I was doing okay. The second one is the um idea is let's say for example we have um uh uh like showing less details as long as we go. Okay. So let's say for example depends on which one we rank details. Okay. The the third one from is uh u you uh load Don't. So let's say this is more of of of um of what we actually uh wanted in the beginning of the exploding that we have uh okay we will have more of of we might not need this because is is enough.




00:03:11


omar elansary: Okay. Uh the other one the graph and the hierarchy based is um it it does like a hierarchy of what we for tools and the problem out of it is that if we have the hierarchy then we must have the tools before we do anything. So this might not be a plug and play uh solution. Okay, this should we should have a database of the of the tools and we should do like a structure before we even this would be a good idea if we are going to ship this to someone directly. So we did that and then we do a hierarchy. Uh but for a plug and play our main solutions it can idea the next two ideas are basically a gateway where the architecture that I proposed for you which for example uh the what they are saying is that um the KV cach in the in thems often and changing it this might be a problem of the of the accuracy of out of of um so the idea is that they take up to uh gateway that have for example five tools search uh uh re whatever five five only these five tools models nothing but these in the beginning and all the time.




00:04:42


omar elansary: So when model would like to get more it does for the its for search and ask for the other one and and goes on and on. So the system but gateway inside is what we actually give out for the model. So the idea is okay if we think about this like that. So in multiple turns the turns uh the context has has decreased because we are always the the only five or whatever the fixed number always. Okay. And depending on that maybe on it goes for
A.F.M. Mohimenul Joaa: Okay, okay, okay. I got it. I got it. Your internet is not very good, Omar. I cannot uh hear you clearly. Either it's yours or it's mine. I think it's yours.
omar elansary: Can you hear me now? Wait,
A.F.M. Mohimenul Joaa: Yes. Yes, I can hear you.
omar elansary: I'ming the
A.F.M. Mohimenul Joaa: But you're uh sometime the Yeah, it's broken. Most of the time it's broken.




00:05:42


omar elansary: I have I have one last thing to the rest of it which is according Eight. which you a sub a box and it it out the or write out what it thinks of is the code and what's the tools um um and from this have like what we see and we put the output for these are the methods
A.F.M. Mohimenul Joaa: I didn't understand one word because it's broken. I'm really sorry. Okay, what I can do is like I can read the questions. Okay. Uh what should count as the thesis contribution? Okay, this is your first question. How narrow should the final research question be? uh how should success be measured and should I freeze the research question now from the current uh evidence or run one narrowly scope diagnostic first to choose between the remaining questions okay uh so Omode uh we already have the research question okay so the research question will be the same uh it's like how much which method is the




00:07:04


omar elansary: Yes.
A.F.M. Mohimenul Joaa: most optimal way to reduce the count of tools while keeping the accuracy as high as possible. Okay, that's the research question. It's simple. We don't need to change it. What you have found and narrowed down is some methodologies.
omar elansary: There are some questions.
A.F.M. Mohimenul Joaa: So, we have some mechanism families. Uh yes.
omar elansary: Nothing.
A.F.M. Mohimenul Joaa: Hello. Hello.
omar elansary: Yeah. Can you hear me?
A.F.M. Mohimenul Joaa: Yes, I can hear you, but it's broken. Yes. Can you hear me? Hello. Hello.
omar elansary: Hello. You can hear me.
A.F.M. Mohimenul Joaa: Yes, I can hear you now. It's much better. Uh, so can you repeat your last question because I didn't hear you at all. It was so broken.
omar elansary: hear me now.
A.F.M. Mohimenul Joaa: Yes, I can hear you.
omar elansary: Okay, wait a bit.
A.F.M. Mohimenul Joaa: Okay, Omar, can you can you repeat your last question?




00:11:05


omar elansary: My last question was basically I I'm I'm I'm okay with the research question. I don't want to to to change the research question. Maybe I miss this. I'll mainly talk about the tough questions, you know, the narrowing out of the of what we are doing. uh because um um um there are a lot of stuff that we would like to see uh we are that we would like to to test and the thing is that I'm thinking maybe we would like it to make maybe an architecture based or maybe an engineering based solution or maybe we could um have um you know like probing and testing and and evaluating the the outputs Oh, what do you think? Um,
A.F.M. Mohimenul Joaa: it depends on you. So if you want a uh evaluation I mean for example let's say I recently published a paper where I had a methodology okay so initially the idea was to be create a method which works on that specific problem again it comes down to the first principle okay so what is the problem and how which is the real solution so if you have the problem and you analyze all




00:12:13


omar elansary: Mhm. Mhm.
A.F.M. Mohimenul Joaa: the current solutions and then figure out the actual solution then implement your package or whatever uh as a solution that's one thing and that is not publishable by itself because you have to prove like it works so how you prove that it works you have to compare it against existing
omar elansary: It's true.
A.F.M. Mohimenul Joaa: baselines so you will say like okay there are a b c d different baselines and let's say e is my method so I will have these five different uh methods doing the same thing using the same scorer are using the same uh code to evaluation for evaluation and then you will have multiple tables with results like okay my approach works on this their approach work on that and all these things okay so you already have a approach and you are evaluating it it against multiple others so that's a normal way of writing paper now if you say okay I don't
omar elansary: Mhm. Mhm.
A.F.M. Mohimenul Joaa: have my own method I just want to do a evaluation on the existing ones then that's a literature review okay that's not a uh that's either a literature degree or a survey paper.




00:13:25


omar elansary: Move.
A.F.M. Mohimenul Joaa: So for a survey paper, yeah, that is also doable. But uh for a master's thesis, a survey paper doesn't work. Okay? So you have to think I mean there should be some kind of nobility like if you are doing a survey paper then where is your nobility? You haven't said anything. I mean even a survey paper can be a master thesis when you have your findings. By findings I mean you have to say okay I have run this experiment.
omar elansary: Oh my god.
A.F.M. Mohimenul Joaa: I have understood the problem to the u to the uh core and this is the actual solution. This works because of this works because of this and this works because of this and if we combine all of this then we get the best result. You have to have some kind of findings otherwise it's not a master's thesis. Oops.
omar elansary: Um, Uh but okay. So um what what do you think I should be doing right now?




00:14:32


omar elansary: Um uh I I send you what I um um what I have been working on. Um but um I mean mostly right now I'm working on the noity or where should I keep an eye on what should I defend or mainly I said um where is the where is my contribution in the in the landscape of of this what we're doing. So, am I in the right direction right now or I could uh go back uh multiple steps or I should go forward? What do you think?
A.F.M. Mohimenul Joaa: uh access strategy. Okay, let me just read it uh loud. Okay, give me a one moment. Is it represent a different access strategy? The model starts with a small G. I used to hear over this. So uh okay change to visual. So if you look at all these method, none of them have any novelty. Each of them is some uh just uh
omar elansary: Yes, these all all the explanation explanation




00:16:51


A.F.M. Mohimenul Joaa: yes.
omar elansary: of the landscape. None of them is a true novelty. I didn't just any novelty yet. That's the thing. All these are just explanation of this landscape so that I can build on or I have a have a base what is the novelty and what's not a novelty.
A.F.M. Mohimenul Joaa: Yes. So,
omar elansary: Oh yes,
A.F.M. Mohimenul Joaa: so again let me let me uh clarify novelty. So if you are not doing groundbreaking research there is nothing nothing is noble. Okay.
omar elansary: it's
A.F.M. Mohimenul Joaa: So what we are doing is like combining different approach. Uh what we are doing is like figuring out what is the real problem and how to solve it.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: Okay. What that works and what that doesn't work. That's it. So that is actually the novelty.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: You have to just sell it as a novely. Okay.
omar elansary: Yes.




00:17:37


A.F.M. Mohimenul Joaa: because that's the academic lango nothing else.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So if you look at the whole problem the problem is either this part is the problem you say the tool visibility discovery execution style interaction length and result handling at the same time.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So which one works at which time we have to figure it out. That's the main nobility. Okay. So if you have 1 tools so again look at the problem. The problem is if you have many many many many tools then you need to narrow it down. You don't even need a executor you can narrow it down easily.
omar elansary: Is it
A.F.M. Mohimenul Joaa: Okay then narrow it down because let's say if you have uh a task at your hand and you know this task doesn't care about these tools. Okay I can give you example for example let's say you are making a AI salesman.
omar elansary: okay?
A.F.M. Mohimenul Joaa: Okay.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: And now this AI salesman talks with the customer and also talks with the business owner.




00:18:41


omar elansary: Yes.
A.F.M. Mohimenul Joaa: Now based on who is invoking the salesman who is invoking the LM okay you will change the tools. If it's talking with the customer then it doesn't need any tool relevant to uh business intelligence does it? No it just need to serve the customer. But while it's talking with the business owner, the face has changed. The role of the chatbot has changed. Now it need to know like today how many customer I have served, what is my revenue today? Uh which product have been sold many many many time most of the times those things those are business intelligence tools. So by just changing the invocation you have changed the list of tools. So the first step is like who is invoking like what's the current context based on the current context some tools are irrelevant I don't need to provide them to the they will never be needed so that's the initial uh narrowing down of tools then the second step is okay now again if I still have let's say thousand of tools then again I don't need thousand of tools I do know that I only need relevant number of tools even if I narrow it down to 200 I know this those 200 tools are important.




00:19:57


A.F.M. Mohimenul Joaa: All the other tools are not important. So I can already do that. Then from this 200 you can look at the execution exeutor part. So ex what does executor does? Exeutor is doing like uh okay you have let's say three or four different web apps like GitHub, notion and whatever whatever and you are just letting the LLM know like okay you have these capabilities you can use them whenever you need. I'm not giving you the whole tool set but I'm just letting you know that these capabilities are present. So that's a different approach. So you have to find out a policy. I was again in from the first point I was telling you you have to find out a policy and the policy is not that simple like okay five tool uh take the top five tool take the top eight tool. This is not a policy. The policy will be different. It will be. based on the context and based on the scenario it will be different.




00:20:52


A.F.M. Mohimenul Joaa: Okay. And also based tools that is provided to the LM.
omar elansary: So what What I what I understood right now is that you can say okay there is a step that I can show you the tool but you're not allowed to execute it and there's a step that I cannot show you the tool and otherwise you can't ex execute am I am I getting this right so step number okay
A.F.M. Mohimenul Joaa: No, you are not. No, no, no, no.
omar elansary: yeah
A.F.M. Mohimenul Joaa: Again, understand the problem. So what is the problem? Can you tell me in one line?
omar elansary: our problem or or the okay so the problem is that uh
A.F.M. Mohimenul Joaa: Yes. Yes. Our problem
omar elansary: we don't like to we would we would not like to give the LM all the tools at once and because this is will explode the complex window and we will have um I mean this is the oneline easy way so I I would like to give the the the the tool needed for the task




00:21:47


A.F.M. Mohimenul Joaa: Yes.
omar elansary: yes that's the main problem we are solving maybe
A.F.M. Mohimenul Joaa: Yes. So yes, that's the main problem we are solving.
omar elansary: Just
A.F.M. Mohimenul Joaa: So the first first thing that you will do is based on context what is the current context and based on the current context what are the relevant tools and this doesn't u include tools which will be used in the same turn. For example, what I what the example that I have mentioned the business intelligent will be never called when the agent is talking with a customer will it because it's talking with the customer. Customer will never ask how many product have been sold today. Will the customer ask this to the salesman? Nope. Only the owner can ask this question and even if the customer ask this question to the salesman, the salesman is not will not answer this. Will that? Nope.
omar elansary: No
A.F.M. Mohimenul Joaa: So the first step is based on the context just filter out tools.




00:22:43


A.F.M. Mohimenul Joaa: Okay. The second step would be something like executor. You have to find out like is executed the better approach or narrow narrow down the tools based on the
omar elansary: heat. Almost.
A.F.M. Mohimenul Joaa: semantic search is a better approach which one is better which one is good which one is bad. You have to figure it out. Okay. So the thing that you have mentioned this is awesome. Okay. So we already have different mechanism family but each of them are different. You have to write down a evaluation script and you have to figure out which one applies at which stage. You will have different stages. Okay.
omar elansary: This
A.F.M. Mohimenul Joaa: So and narrowing down of tool is not only one not one step job. It's not like I have 1,000 tool I will narrow it down to 10 tools. It's not like that. It's more like I have 1,000 tool.




00:23:31


A.F.M. Mohimenul Joaa: I will narrow it down to 800. Then from 800 to 500, 500 to let's say 200, then 200 to 10, something like that.
omar elansary: I have one question.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Let's say because it it came to my mind as I I can see it as you as you that both of these are not all all contributing in the same step. They are all conting but not in the same
A.F.M. Mohimenul Joaa: Omar,can you can you speak a little bit slowly because I don't know I'm not understanding your what you're saying.
omar elansary: what I'm what I'm saying is that uh most if we I would just like to make a ground for you what we understand right now that most of these builds are not uh
A.F.M. Mohimenul Joaa: I know. Nope. Either your microphone is very bad or the internet. I don't know. I'm not understanding one word.
omar elansary: give me one second one Right now you can hear me
A.F.M. Mohimenul Joaa: Uh, can you try again?
omar elansary: right now.




00:24:31


omar elansary: You can hear me
A.F.M. Mohimenul Joaa: Yes, I can hear you, but I cannot understand your words. They're so mingled.
omar elansary: and then how about this?
A.F.M. Mohimenul Joaa: Yes. Yes. Slow.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: Speak slowly. Okay. Sorry,
omar elansary: Okay.
A.F.M. Mohimenul Joaa: I'm giving you
omar elansary: Yes. So the thing is that um let's think about it like
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: this. Most of these these methods contribute at different steps in the execution or in the in the in the solution that we have right so we are on the same page right now.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: So I was thinking about something and I'm not sure if this is might be uh a good um a good novality or not. Let's say if we can have a good combination of these solutions to solve the main problems we are trying to
A.F.M. Mohimenul Joaa: Uhoh.
omar elansary: do. I mean, think of it as puzzling those solutions and maybe adding some bridges between them so that we have




00:25:36


A.F.M. Mohimenul Joaa: She's
omar elansary: the solution for our main research question. So, uh uh uh um is this possible? It's okay. Is this can this be a thesis or no? Can this be a thesis? Not
A.F.M. Mohimenul Joaa: Uh so you already have this uh so for example when you submitted your signed document from Michael and Simon I think you already have that is the proof that this is a thesis.
omar elansary: this.
A.F.M. Mohimenul Joaa: Okay. So that is not the problem.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: The problem was is okay. So problem is you have to write a paper. So when you submit your thesis even if it's not that novel even if the result is negative it's a thesis okay and migrate bound to market.
omar elansary: It's
A.F.M. Mohimenul Joaa: The problem is can you write a paper and get it accepted. So for that have to do it systematically.
omar elansary: okay.
A.F.M. Mohimenul Joaa: Okay. The first thing that you have to do to submit a paper is your work have to be systematic.




00:26:43


A.F.M. Mohimenul Joaa: So by systematic what do you mean? You have to say okay this is the problem. The problem is big. I have studied it and this is the real problem.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: Those tools are not important. They will never be called. Okay done. I'm filtering them out. The second step this this. The third step this this this. And the fourth step this. And by doing this 1 2 3 four steps I'm narrowing down from 100 to 10. So I am reducing 90% of token users. Okay. So that's what you need to say. But this have to be systematic. I cannot emphasis it more. Okay.
omar elansary: Yeah. Okay. So, I guess I have to uh uh continue or finding a solution and then building a systematic approach. Maybe the next time maybe on Monday or Tuesday we can have another meeting if you have time and we make sure that I am on the right track.




00:27:39


A.F.M. Mohimenul Joaa: Yes. So again don't implement anything. The first step that you need to do is figure out a I would say it's more like
omar elansary: Yes.
A.F.M. Mohimenul Joaa: a tree type of graph. Okay. So you start with 10,000 programs.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: There are steps. At each step you have to ask yourself one question. Is all these 10,000 question relevant in this current scenario? If none of the tools, some of the tools are not relevant then you have to filter them. Then the second step again another question. Okay. Based on this question you will filter down more. Then doing this stage one, stage two, stage three, stage four. I don't know how many stage you have but you have to find find those questions and the stages. Okay, that's the policy. Okay.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: And it's not like a not like when you filter down filter one tool out you cannot add it again.




00:28:35


A.F.M. Mohimenul Joaa: It's it's a uh more like a graph.
omar elansary: What is
A.F.M. Mohimenul Joaa: That's why I didn't say it's a tree. Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So for example let's say you have uh filtered out a tool at stage four but at stage five you found like this tool is relevant then you can go back and then again add the tool. Okay. So that's the graph that you need to find out and that is your novelty actually. Okay, that you have studied this problem and you have figured out those are the question that one need to
omar elansary: Okay.
A.F.M. Mohimenul Joaa: ask to filter out the tools.
omar elansary: Okay, great. Uh, I have to leave for the meeting. Um, maybe if this meeting uh transcription u came to you by email, uh, maybe send it to me or it's not your
A.F.M. Mohimenul Joaa: This is actually this is actually your link. So I think this will be sent to you and this is a link that you have provided in the group




00:29:25


omar elansary: Okay, great.
A.F.M. Mohimenul Joaa: description.
omar elansary: Please, I I love this transcription if you don't if you don't mind because sometimes I forget some stuff and I return back to it. So,
A.F.M. Mohimenul Joaa: Okay.
omar elansary: sorry. Yeah, thank you. Thanks for your time and I hope you would do well with your uh deadline and if I need anything I
A.F.M. Mohimenul Joaa: Yes.
omar elansary: will.
A.F.M. Mohimenul Joaa: Yes. That's actually submitted. So let's see. Finger crossed.
omar elansary: Yes, you would do good. If you need anything, I can help.
A.F.M. Mohimenul Joaa: Sure. Sure.
omar elansary: Thank you.
A.F.M. Mohimenul Joaa: Okay. But I need a deadline from you.
omar elansary: Okay,
A.F.M. Mohimenul Joaa: You need to give me this policy. You are just beating around the bush but not giving me this policy.
omar elansary: true. True. I how much I can give you a deadline. If I give you a deadline, I will be exceeding it for sure.




00:30:12


omar elansary: Um so from where I am right now to where you can give me a deadline. Give me you as yourself a deadline so that I can
A.F.M. Mohimenul Joaa: One week is good enough. I don't want you to implement anything. I just want you to ask sit down and ask this question to yourself. So I have 1,00 and how can I narrow it down?
omar elansary: I ask this
A.F.M. Mohimenul Joaa: You already have studied the literature. You know all the methods.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So you have to figure out the question and which method is more most appropriate for that.
omar elansary: Yes. Yes. Okay. Can you repeat the question again? We have 10,00 tools and we'd like to introduce this to as much as possible for the context we need. So this is the question that I'm looking at.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: What's the method of this? Okay, great. Thank you for your time and uh if I found
A.F.M. Mohimenul Joaa: So, let's uh target next witness day 11:00 a.m. Okay. So, by then I should have the policy.
omar elansary: Okay, perfect.
A.F.M. Mohimenul Joaa: Okay. Chow.
omar elansary: Okay,
A.F.M. Mohimenul Joaa: Chiao.
omar elansary: thank you. My wife




Transcription ended after 00:31:18


This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
END-VERBATIM>>>
