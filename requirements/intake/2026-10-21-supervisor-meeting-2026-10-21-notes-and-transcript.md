---
type: "intake-text"
id: "INT-T-002"
authorization: "AUTH-018"
supplied_by: "human (user): three Google Docs links in the message of 2026-10-21; the lead downloaded each with the export-as-plain-text URL (curl, 2026-10-21) into the session scratchpad, outside the repository, and copied the approved part here"
supplied_utc: "2026-10-21 (time of day not recorded)"
form: "transcript"
stated_nature: "Gemini meeting notes and the full automatic transcript of the supervisor meeting of 21 October 2026 (the meeting for which package v4 was prepared), as exported from the Google Doc the user linked. Whole document admitted."
meeting: "Automatic Tool Discovery"
meeting_date: "2026-10-21"
speaker_per_supplier: "A.F.M. Mohimenul Joaa (supervisor) and omar elansary (the student), as labelled in the transcript"
original_source_claim: "https://docs.google.com/document/d/140LUBL3X6NjtAXBWTgLbrrhYPCtB6pSm3qgBcfXVVJE/edit?usp=sharing (exported as text; Google document, editable by its owners)"
original_sha256: "935eae9cd97de9bb4749ee79505acbea11df41a7449c72754d7aeb1e440c2d20 (SHA-256 of the exported text as downloaded, before BOM removal and line-ending normalisation)"
approved_ranges: "whole export, lines 1-511"
excluded: "none"
caveats: "(1) Automatic speech recognition by Google Meet/Gemini; wording such as 'nobility' (novelty), 'Exeutor' (Executor), 'cloud' (Claude), 'NCP atlas' (MCP-Atlas), 'quy expansion' (query expansion) is preserved as exported and not corrected; (2) the 'Gemini notes' sections (summary, decisions, details, next steps) are machine-generated summaries, not the participants' words, and the export itself says to review them for accuracy; only transcript lines carry the speakers' words; (3) the transcript says it is 'editable' and 'might contain errors', so a later edit of the original would not be seen here; (4) speaker labels are the transcript's own; (5) line numbers refer to the export as downloaded (UTF-8 BOM removed, CRLF normalised to LF), so body line N is export line N for whole-document records."
body_sha256: "e3af023f29608ff4234b19ee02622d7db80393f18237dcb5073369c403fdaa5c"
---
<<<BEGIN-VERBATIM
Please rate the new Quick notes tab by taking a short survey.
Automatic Tool Discovery


Oct 21, 2026


Context management analysis with token reduction strategies and cost savings


Agent context management and token optimization
* Joaa proposed narrowing the practical agent scope exclusively to memory and tool calls.
* Explicit caching and memory storage reduce operational token costs by up to 80%.
* Storing tool execution responses in memory prevents redundant token consumption across conversational turns.
* MCP servers require brain storage for incoming data rather than external notepad logs.


Failure recovery and token optimization metrics
* Omar explored calculating cumulative cost reductions across multiple turns instead of single-turn optimizations.
* Joaa noted that policy recovery from occasional failures temporarily increases token usage.
* Overall average token usage and response times still yield net savings across turns.


Memory implementation and research validation approach
* Omar suggested utilizing markdown-based note systems as a memory base for progressive learning.
* Joaa advised using simple text files initially to validate the research without premature engineering.


Thesis timeline and remote work arrangements
* Omar noted the thesis registration deadline falls on February 18, with potential extension options.
* Joaa confirmed physical attendance is unnecessary, permitting online updates while Omar travels to Egypt.


Next steps
* [omar elansary] Conduct experiments: Execute multiple agent settings and configurations to collect statistical data. Provide evidence for the research paper through consistent variance testing.
* [omar elansary] Validate hypothesis: Implement a simple text based memory system using text files to test memory and tool call cost reduction. Avoid over engineering until the core concept is proven.








Want to see more? View the full notes
Tip: You can always access your full notes from the left sidebar.






You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes
Oct 21, 2026
Automatic Tool Discovery
Attachments Automatic Tool Discovery
Meeting records Transcript Recording 




Summary
Context management analysis with token reduction strategies and cost savings

Context and Token Optimization
Discussion on conversation memory and explicit caching strategies reduced token consumption overhead.

Cost Reductions and Scope
Model Context Protocol servers lowered operational costs by 80 percent while narrowing project scope.

Implementation and Timeline
Simple markdown files avoided over-engineering for research validation before the February 18th deadline.




Decisions
Aligned
* Project scope restricted to memory and tool calls The participants agreed to narrow the project scope exclusively to memory and tool calls while omitting knowledge and other features.
* Avoidance of complex engineering for validation The participants agreed to forgo complex engineering initially and use simple text files to validate the research concept.




Next steps
* [omar elansary] Conduct experiments: Execute multiple agent settings and configurations to collect statistical data. Provide evidence for the research paper through consistent variance testing.
* [omar elansary] Validate hypothesis: Implement a simple text based memory system using text files to test memory and tool call cost reduction. Avoid over engineering until the core concept is proven.




Details
Conversation Memory Scope and Context Management: omar elansary raised the problem of whether to account for conversation memory and keep instructions minimal. A.F.M. Mohimenul Joaa explained through analogies that conversational context involves multiple components, including knowledge, memory, tools, invocation settings, and input and output modalities such as images, voice, links, and text generation.
________________


Explicit Caching and Token Reduction Strategies: A.F.M. Mohimenul Joaa highlighted the problem of high token consumption for basic interactions, noting that a simple "hello" and "hi" exchange can consume 10,000 tokens instead of an ideal 10 to 30 tokens. To address this, A.F.M. Mohimenul Joaa proposed using explicit caching for memory, knowledge, and tools, explaining that standard tool calls generate massive token overhead across human messages, thinking responses, tool calls, tool responses, and artificial intelligence responses.
________________


Model Context Protocol Servers and Cost Savings: A.F.M. Mohimenul Joaa and omar elansary discussed the problem of processing and storing tool calls efficiently, comparing Model Context Protocol servers—where a brain receives information directly without a local file notepad—to writing responses into files. A.F.M. Mohimenul Joaa stated that avoiding saving every tool call directly in memory and instead utilizing searchable files can reduce overall operational costs by approximately 80%, lowering average turn costs from 0.01 cent down to 0.003 cent.
________________


Handling Turn Failures and Cumulative Cost Reductions: omar elansary asked how to calculate cost reductions cumulatively across multiple turns when capability gaps cause occasional failures. A.F.M. Mohimenul Joaa clarified that policies should allow systems to recover from failures, which may temporarily increase token usage and response time for specific failed turns (such as 3 out of 100 turns), while still achieving a net cost and time reduction across the remaining 97 successful turns.
________________


Narrowing Scope to Coding Agents and Memory Summarization: omar elansary proposed narrowing the project scope to focus on a one-hour idle gap in cloud code or command line interface memory alarms that consume 300,000 tokens. A.F.M. Mohimenul Joaa agreed that agent costs scale with turns and noted that summarizing lengthy interaction histories into a brief three-to-four line paragraph prevents doubling token costs when restarting conversations, ultimately emphasizing a concentrated focus on memory and tools.
________________


Implementation Approach and Avoiding Over-Engineering: omar elansary asked whether engineering implementations using note-taking software like Obsidian or Notion as memory bases align with the project landscape. A.F.M. Mohimenul Joaa advised that for research validation, simple text or markdown files are sufficient to inject information into prompts, instructing omar elansary not to over-engineer solutions initially until ideas and statistical variances are fully proven through broad experiments.
________________


Master Thesis Timeline and Remote Work Arrangements: omar elansary stated that their final master thesis registration deadline is February 18th within a 22-week limit, and requested permission to travel while asking if A.F.M. Mohimenul Joaa required in-person meetings prior to February. A.F.M. Mohimenul Joaa confirmed that physical meetings are unnecessary and permitted omar elansary to work remotely online, maintaining communication and project updates via WhatsApp.




You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes
How is the quality of these specific notes? Take a short survey to let us know your feedback, including how helpful the notes were for your needs.
Oct 21, 2026
Automatic Tool Discovery - Transcript
00:00:26


omar elansary: Jo can do. Hello.
A.F.M. Mohimenul Joaa: Yes, I can hear you.
omar elansary: Yeah. Hi. How are you?
A.F.M. Mohimenul Joaa: Yes, I'm doing great. What about you?
omar elansary: Good. Good. Uh well um I feel uh motivated somehow. I don't know how how do you feel?
A.F.M. Mohimenul Joaa: Okay.
omar elansary: Do you like the policy? Um you didn't like it? Um because um right now I'm doing some work, right? But uh let me know.
A.F.M. Mohimenul Joaa: Okay. So you had two question according to your last question uh message I think.
omar elansary: Yeah, I have had two questions for you and um some other like I mean some other administrative questions but um just came comes up to my mind when we have time. The last time you talked to me about the memory and personality and and more of the role based or memory of of of making sure for the memory. Um for the first question I wanted to ask should we account for the memory of the conversation itself or no?




00:01:35


omar elansary: I mean we can somehow make sure okay we don't want to save this in the memory of the conversation or we should like to make the instructions as minimal as possible. Should we account for it or no?
A.F.M. Mohimenul Joaa: Uh so that that is a different question actually. So it depends on what you are building.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: So uh let
omar elansary: Because this is also this is also this is as far as I understood we should make sure that we understand the main aspects or different aspects of what is being calculated as cost and what is not calculated and memory is one of the things that is being sent and calculated is one of the parts of the cost.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: So Mhm.
A.F.M. Mohimenul Joaa: But let's say let's say um let's make it let's u understand the problem using analogy. Okay. Uh so again you are um just outside your building talking to a stranger. Then uh what information do you recall before engaging in any conversation?




00:02:39


A.F.M. Mohimenul Joaa: What information do you recall?
omar elansary: Um,
A.F.M. Mohimenul Joaa: The name of the person if you know them.
omar elansary: you mean some truly someone new on me? Um, there is no conversation to be recalled. I'll be dynamically checking what do they say.
A.F.M. Mohimenul Joaa: Yes. Uh but let's say that person is uh your neighbor.
omar elansary: Okay. So the conversation maybe about something about our neighborhood, something about my home, something about his home, something like this two to three days u maybe one week later about like for example the stuff that's happening.
A.F.M. Mohimenul Joaa: Yeah. So, so, so that's memory. Okay. So,
omar elansary: Yes.
A.F.M. Mohimenul Joaa: that's memory about the person like what you have discussed earlier. Uh, now consider a different scenario. Now you are talking with your colleague and you are in your office and uh in that
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: specific uh settings what information do you recall?
omar elansary: Um if I'm talking for example to my colleague at work then the basics I will be talking about is something about work maybe meeting




00:03:40


A.F.M. Mohimenul Joaa: Yes. Something about work. So it involves knowledge.
omar elansary: about Yes.
A.F.M. Mohimenul Joaa: It doesn't only involve memory. So memory is like what that person um asked you or whatever the conversation you had with that person but now you are you are working on a project and you have knowledge about the project. Okay. So you also need knowledge about the project. So so there are multiple different things there are tools there are knowledge there are memory there are invocation settings there are context there are input modality output modality and all those other stuffs. Okay.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So in uh what do I mean by input modality? Um it's like you are seeing image, you are receiving voice, you are um figuring out links. Okay, those are input modalities.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: What are output modalities? You are talking, you are showing him something. All those are output modalities. Okay, or maybe you are producing some text, you are writing.




00:04:38


A.F.M. Mohimenul Joaa: Now if you say uh I want to make a aentic system and I want to make it uh in a way where this whole context management will be part of my thesis okay then you need to do everything okay
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: but let's say if you say I don't want to do everything then you can choose but then again uh why I am mentioning all this there are this explicit cache part. Okay.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: And this explicit cache doesn't stop at tools. It's also applicable for memory. It's also applicable for knowledge. Okay. And there is also this u uh dynamic context management. So what do I mean by dynamic context management? So if you have explicit cache then as the conversation grow you can add more information. The problem is let's say I say hello and you say hi and by this hello and hi we have consumed 10,000 tokens that is the problem.
omar elansary: This
A.F.M. Mohimenul Joaa: Okay, for a hello high setting that token should be 100. 100 is even more.




00:05:50


A.F.M. Mohimenul Joaa: It should be 10, 20, 30. Okay, then when you are engaging in a topic then you can take information for for the topic. Okay, you can get memory related to the topic, knowledge relevant to that topic, tools relevant to the topic and you can keep them. The awesome thing of explicit caching is like when you add some information, you can just keep them in the explicit cache and that's negligible cost. Okay, you don't need to reduce them.
omar elansary: Don't.
A.F.M. Mohimenul Joaa: When when you already have the information, you can just keep them always. Always. By always I mean for the whole conversation okay because explicit cash is negligible price and let's say you are talking with that person for 1 hour that is still negligible okay and you are not losing any context but
omar elansary: That's true.
A.F.M. Mohimenul Joaa: now if the person comes again to you and he start talking in the same topic again now the question comes again do you give all the context at the same time just by saying hello.




00:06:59


A.F.M. Mohimenul Joaa: No, you you shouldn't. Okay, because if you give again all the context uh all the memory, all the knowledge and all the tools uh again just by saying hi, there is the problem. So he doesn't want to want uh you to answer anything relevant to the uh to the work or anything relevant to the what he have asked. So then why should you?
omar elansary: True.
A.F.M. Mohimenul Joaa: So that's how the system should work. I mean in theory that is all in theory.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: Okay. Now let's go back to practical. Uh this is a little bit too much. Uh the scope is too broad. Okay. You cannot do everything but you can do only memory and tool calls. Forget about knowledge.
omar elansary: Cool.
A.F.M. Mohimenul Joaa: Forget about everything else. And memory should help tool calls. So if you for example let's say what happens right now when you ask a model about something let's say what is the current weather the model uh send a tool call and then the tool call is executed and the response of the tool call came back.




00:08:07


A.F.M. Mohimenul Joaa: Okay. So there are four message. One uh human message uh then the model thinks something. So maybe thinking response then uh the tool call then the tool response and then the AI response. So if you see it's a huge amount of tokens uh and there are human message
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: uh thinking tokens uh tool call tool response and then at the end there is AI response.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: So if you continue talking this is just one turn and you you actually saved five message for only one turn.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: So let's say in one turn if you use multiple tool calls let's say three tool calls then there are six response just by the tool calls without thinking and you don't need them do
omar elansary: Yes. Yes.
A.F.M. Mohimenul Joaa: you?
omar elansary: No.
A.F.M. Mohimenul Joaa: Nope you don't need them because you already know the response. what was the question and what was the answer.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So if you can somehow save those information in memory uh then they're much easy to consume and you also don't need to uh save this amount of




00:09:09


omar elansary: Yeah.
A.F.M. Mohimenul Joaa: information. Okay. So that that is the main point of of the whole thing and also again understand the thing that there is MCP server and CLI based tool calling. Okay.
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: So MCP server you have a brain but you don't have a notepad.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: So you have a brain and all the information that is coming it should be saved inside your brain. So let's say I I give you an image um when you execute a tool called okay the image should be saved inside your memory. I don't I haven't give you any uh any papers to write it down how the
omar elansary: Yeah.
A.F.M. Mohimenul Joaa: image looks or what the what the uh features of the image were. So uh that is actually costly because you are saving every response
omar elansary: This
A.F.M. Mohimenul Joaa: every tool call in your memory whereas what you should have done is save those in a file write it down somewhere when you need you just read them and you can also search you can just go through it you don't need to read everything you don't need to understand every token or every word by word you can just uh search and figure out okay this is the response I get it then I can do whatever with the response




00:10:25


omar elansary: Yes.
A.F.M. Mohimenul Joaa: But this is also a token saving parts. Uh why I'm saying all those things because this is hard to build. This is hard to build.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: But this is what will save you money. Okay? And this is a practical problem.
omar elansary: Yes.
A.F.M. Mohimenul Joaa: This is a really practical problem. You can save around 80% of the cost by doing this. For example, on average, if one turn uh cost you around 80 cent, say a little bit too much, let's say 0.1 cent uh 0.01 cent, so you can reduce it down to 0.003 cent. So that's that's that's nothing compared to 0.101.
omar elansary: I have one question.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Can I?
A.F.M. Mohimenul Joaa: Yes. Yeah.
omar elansary: So in in in uh two meetings before we have uh talked about something that we would like to decrease the money out of uh what we would like. So there are two ways to think about it like this.




00:11:27


omar elansary: Let's say for example we would like to decrease the money for one task or for for one turn for example and also we could also let's say for example if there are five turns okay so the first turn I have decreased the money by 10%. Second term I have decreased it by 20%. And so on and the whole stack we have decreased the money by 30% for example. This is a valid result and it is a good result right I mean we have decreased the money anyways 30% 40% conversion right this is this is possible but I mean some some somehow maybe we could start uh maybe one part could could for example let's say for example there was a capability gap okay so that capability gap because then it happened and we tested multiple times out of our way we tested multiple times this might have Then there is there there were no uh cost reduction for example for this specific turn I mean okay so this is also valid right because we have failed
A.F.M. Mohimenul Joaa: Mhm. Yes.




00:12:29


omar elansary: and we would like to to to say oh we failed in here but yeah this stage out of the capability gap we will fail so it's okay also we don't have yes yes
A.F.M. Mohimenul Joaa: Yes. That's totally okay. So uh for example uh if you give uh your whole policy a way to recover from a failure that's totally okay and because you failed I mean you have done something
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: wrong that's why you have failed and when you will recover you will use a little bit more token that's also totally understandable but
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: you are not on average you are reducing the token and you are also reducing the average response time maybe for this failure case the response time and the token both
omar elansary: Hi. Hi.
A.F.M. Mohimenul Joaa: have jumped
omar elansary: Hi. What? Can you just say the last 10 seconds? It Okay.
A.F.M. Mohimenul Joaa: Yes. Yes. Uh so what I was saying is like on average let's say there are 100 turns and let's say three of those turns are failing.




00:13:22


A.F.M. Mohimenul Joaa: Okay. So you should give uh your policy away to recover from the failure. Mhm.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So if it recover from the failure then it have to use more token and more time
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: otherwise it cannot obviously.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So let's say for three turns you are using more tokens and a little bit more time but on average for the 97 times you are reducing token and saving
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: time.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: So on average you will be a win-win situation. Okay.
omar elansary: Yes. Um, one last question. Maybe I could uh I thought I I thought about that because we about this part of the memory. I was thinking maybe we should only focus about this. You know when we use cloud and we use cloud code or CLI there is this uh alarm that shows that the memory is still warm and if you still kept IDL for time it says
A.F.M. Mohimenul Joaa: Mhm.




00:14:17


omar elansary: to you you have the next time we will be uh uh consuming 300k tokens for example.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: So what what I was thinking is is um um just to to to to to narrow it down maybe we could take this one hour gap as our memory without digging deep in conversation and digging deep in the stuff. So we have a memory and there is this memory that we would like to make sure we we we we
A.F.M. Mohimenul Joaa: Yes. Yes.
omar elansary: save it because if we proved that this if if we proved that we can save these
A.F.M. Mohimenul Joaa: Yes.
omar elansary: 300k we can prove for bigger memories but instead of just being uh uh how to say that in instead of just thinking about the whole conversations and everything we would just be thinking about this
A.F.M. Mohimenul Joaa: Yes. Yes.
omar elansary: right one.
A.F.M. Mohimenul Joaa: So for example, what you are talking about is a coding agent. Okay. The same problem is applicable for any kind of agent.




00:15:10


omar elansary: Yeah.
A.F.M. Mohimenul Joaa: It can be a salesman, it can be a recruiter, it can be whatever. Okay? Uh marketing whatever. Uh for any kind of agent, the problem is the cost per turn. So if I say hi, I need to give it some tool. I need to give lots of capabilities and memories and knowledge to that LLM. Okay, the brain. But if I just say hi, I'm not earning any money. Am I selling something? No.
omar elansary: Yep.
A.F.M. Mohimenul Joaa: But let's say the same agent a customer is talking for five or 10 turns. Now I'm selling something.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: I have already sold the item at seven turn. Okay.
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: And at seven turn I have used around let's say 20,000 token. Okay, that's acceptable because 20,000 token is two or three data I mean two or three dollar maybe or it will be less but let's say uh two or three dollar or 2 or3 that's acceptable for one sale I have used this amount of money this is not a problem but let's say every person that say hi to me is costing me two or three euro or two or three dollar is not acceptable so if you uh so the




00:16:19


omar elansary: Mhm.
A.F.M. Mohimenul Joaa: summary The whole thing is like the conversation uh memory and conversation uh token should grow with the turns and when you
omar elansary: Yes.
A.F.M. Mohimenul Joaa: stop let's say I stop at turn 10 and I haven't committed and I haven't bought anything yet. Okay, tomorrow I come back to the same agent and ask okay I have talked with you about buying this thing and I want to buy now. Now if you start from there now the cost is double because I already have used two 20,000 tokens and I start again and I'm again using 20,000 tokens to start just from here which shouldn't be what it should be is like what you have done
omar elansary: Yes. Yes.
A.F.M. Mohimenul Joaa: by this 10 uh terms it's just it can be written within maybe three or four lines you have chosen a product you have asked for discount I have approved you a
omar elansary: Yes.
A.F.M. Mohimenul Joaa: coupon or whatever this is just a salesman experiment experience I'm telling you but it can be anything okay but this can be summarized into a very small paragraph and




00:17:22


omar elansary: And just
A.F.M. Mohimenul Joaa: then I don't need to give all this uh 20,000 token and I don't need even need to save the 20,000 token I can only save the memory and even this memory can get big so I can choose part of the memory which is relevant to the question initially for that time and when he asked me more I will give more
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: information from the memory and by doing that again I'm saving lots of
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: money so that's how it should be
omar elansary: Yes. Yes.
A.F.M. Mohimenul Joaa: so uh this context is mostly I mean by context it means knowledge memory input uh modality output modality and uh tools and all those stuff okay but I I would say just focus on two things that is tools and memory because they comes hand in hand. Uh without tools you cannot have memory and without memory you will need all the tools.
omar elansary: Mhm. Yes. Um I have I have one last question to understand also that I'm um somehow in in in the correct landscape.




00:18:36


omar elansary: Um uh couple of days ago I have seen uh I right now I'm talking about the engineering wise not the scientific way.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: Um I have uh seen um someone or a repository on the GitHub that is uh doing something that like ours which is basically what is actually doing is that it is using um I don't know um you know uh it's something like notion I don't remember what's the name of it. It's obsiden. It's using as its memory base and it has built the MZ file there. So the skill what is actually done is the skill is basically making sure that every user preference or every user idea is saved there so that next times it just go and read this main thing so that it it it it learns progressively about what you're doing when why and all this stuff. So engineering wise we can just take the idea of this and check how does scientifically people does it and then we can implement it. Maybe this is am I in the correct landscape or I'm deviating.




00:19:47


A.F.M. Mohimenul Joaa: uh obsidian is kind of like notion. It's just note takingaking tool. So I cannot uh understand the uh relevance
omar elansary: I will never be using I will never I will never be using uh I will not be using obsidian or not not taking. I'm just um uh uh uh you have said something really good. You have said something that it's we have a brain but we don't have a notes and brain actually uses our memory. So a memory is basically something that you saved some information about what you have learned about. Okay.
A.F.M. Mohimenul Joaa: Oh,
omar elansary: So engineering wise people use yeah so to implement this I'm talking about implementation
A.F.M. Mohimenul Joaa: okay. Okay.
omar elansary: people have this is one of the implementation we can choose whatever implementation we wanted. I just want to understand if in in engineering wise are we good in this implementation or no this is totally different from what we want we I mean we can use databases I don't
A.F.M. Mohimenul Joaa: So,




00:20:39


omar elansary: know we I'm not sure I'm not yet I haven't yet this is just a hypothesis I can check everything but I'm just thinking
A.F.M. Mohimenul Joaa: So this is research. Okay. So we we first want to validate our idea.
omar elansary: okay
A.F.M. Mohimenul Joaa: Uh so for for validating our idea I would say even a text file a empty file is good enough. Okay. The unique to save.
omar elansary: Okay.
A.F.M. Mohimenul Joaa: conversation in a meaningful way in MD and in a text file and then uh again when you ask the same I mean start the same conversation from the same turn then part of the information from this text file should be injected in the prompt that's the main goal so we don't care about
omar elansary: Mhm. Okay.
A.F.M. Mohimenul Joaa: the engineering right now because we have to first validate our idea like okay this memory and this uh
omar elansary: Mhm.
A.F.M. Mohimenul Joaa: tool call my dynamic uh part memory and tool call works and we can save token
omar elansary: This is




00:21:29


A.F.M. Mohimenul Joaa: Because if you want to publish a paper you you need to provide numbers and numbers cannot be like okay 10 turn
omar elansary: this
A.F.M. Mohimenul Joaa: 20 turn it it need it it it need to be a very big uh experiment. So you need to have multiple different uh goals for your agent uh multiple different settings and also run all the same settings multiple time to say uh to show the statistical variance.
omar elansary: for sure. For sure. Um but I mean um um um if I found something that is uh could validate the idea and it is also engineering wise simple, we can use it. It's okay, right?
A.F.M. Mohimenul Joaa: Yes. Yes.
omar elansary: We don't have to Yeah.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: I mean I I what I understood for me is not overengineer it. That's what I'm Yes.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Okay. Perfect.
A.F.M. Mohimenul Joaa: Yes.
omar elansary: Okay. Okay. Okay.
A.F.M. Mohimenul Joaa: uh first I would say don't engineer it at all




00:22:24


omar elansary: Okay.
A.F.M. Mohimenul Joaa: because first you need to because your idea will change as you start implementing this will change so much
omar elansary: Yes.
A.F.M. Mohimenul Joaa: okay and when you have the result you can engineer it as much as you want okay then no one
omar elansary: Okay.
A.F.M. Mohimenul Joaa: will stop
omar elansary: Yes. Okay. Okay. Um, no worries. I guess right now I'm understanding well and if I have any questions I will ask you.
A.F.M. Mohimenul Joaa: Okay,
omar elansary: Uh,
A.F.M. Mohimenul Joaa: then ch if there's nothing else.
omar elansary: touch. Thank you. I have one question to you.
A.F.M. Mohimenul Joaa: Bye-bye. Sure.
omar elansary: Um my my final day on the registration is 18th of February.
A.F.M. Mohimenul Joaa: Mhm.
omar elansary: I guess um it's okay that we can submit that we could um increase one or two month if we want but for extension I mean uh but my question is throughout from today to February will you need me anyway in person
A.F.M. Mohimenul Joaa: Uh I mean you want to submit uh submit your master thesis in February.




00:23:28


omar elansary: it's uh it's already because uh we have only 22 weeks so it is already.
A.F.M. Mohimenul Joaa: Okay. So uh so it's it's recommended that you send your uh master thesis writing at
omar elansary: They just send it back.
A.F.M. Mohimenul Joaa: least uh three or four week earlier.
omar elansary: No, no, no. Um what I'm saying is that um that's what they have written the examination office
A.F.M. Mohimenul Joaa: Yes.
omar elansary: which means that we can which means that I can send my PDF and
A.F.M. Mohimenul Joaa: No, no, not not not to the examination,
omar elansary: uh Yeah,
A.F.M. Mohimenul Joaa: but to Michael and Simmon. because they need to read your uh read your master pieces.
omar elansary: I mean for I don't want I I'm I'm okay to extend it. Just what I'm telling you. I'm okay to extend if we if we found ourselves in a place that we are in good uh ter and we could have like one more one month extension. But u that's not the case right now. The the question is um do you want me from today till February or from today till next uh things because uh I want to take your permission because I might be traveling to Egypt.
A.F.M. Mohimenul Joaa: Yeah, sure.
omar elansary: Uh yeah.
A.F.M. Mohimenul Joaa: I think I don't think we need a physical meeting at all.
omar elansary: Yeah. Great. Okay.
A.F.M. Mohimenul Joaa: You can meet online and you can keep me updated on the project.
omar elansary: Okay. No worries. And if you need anything, we have a WhatsApp and let me know.
A.F.M. Mohimenul Joaa: Yes, perfect. Okay then,
omar elansary: Okay.
A.F.M. Mohimenul Joaa: Jojo.




Transcription ended after 00:25:39


This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
END-VERBATIM>>>
