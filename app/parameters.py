"""
################################################
###           DOCUMENTATION                  ###
################################################

This file allows users to specificy all parameters of the AI interviewer application. The parameters are stored in a
dictionary called INTERVIEW_PARAMETERS. You can specify multiple parameter sets for different types of interviews.
For example, one could randomize people into different interviews (e.g. about the stock market or about voting behaviors).
Each parameter set can be identified with a custom key (e.g. "STOCK_MARKET" or "VOTING"). You have to supply these
keys when making requests to the AI interviewer application to tell the application which parameter set to use.

We provide the parameter sets used in our paper as an example from which to build your own interview structure.
We also provide a template for additional interview configurations. You can add as many parameter sets as you like.

We describe all parameters that should be included in a parameter set below:


################################################
###           GENERAL PARAMETERS             ###
################################################

0) META DATA (OPTIONAL): The following parameters allow you to provide additional information about the interview configuration.
						 This may help with remembering the purpose of the configuration or provide additional context for yourself.
- _name (str): 			A name for the interview configuration (e.g. "STOCK_MARKET" or "VOTING")
- _description (str): 	A description of the interview configuration and its purpose.


1) OPTIONAL FEATURES: The following parameters active optional features of the AI interviewer application.

- summarize (book): 				whether to active the summarization agent for the interview (default: True)
- moderate_answers (bool): 			Whether the moderator agent should review answers from the interviewee and potentially flag them (default: True)
- moderate_questions (bool): 		whether AI-generated interview questions should be reviewed with OpenAI's moderation endpoint
									before sending them back to the interviewee (default: True)


2) INTERVIEW STRUCTURE and PRE-DETERMINED MESSAGES: The following parameters define the structure of the interview and
the messages that are displayed to the interviewee at various stages of the interview if specific conditions are met.
The first_question and the interview_plan variable are the most critical parameters.

- first_question (str): 			The opening question for the interview.
									All interviews will start with this message.
- interview_plan (list): 			The interview plan for the interviews. This is a list of dictionaries that define
									the scope and length of each subtopic
									of the following form [{"topic": str, "length": int}, ...] where:
									- topic (str): 		a description of the subtopic to be covered in the interview
									- length (int): 	the total number of questions to ask for this subtopic
									The topic description can be short or long, depending on the level of detail you want to provide.
									It could even mention specific follow-up questions that should be asked in specific circumstances.
									Feel free to experiment with the number of topics, the number of questions per topic,
									and the level of detail in the topic descriptions.
- closing_questions (str): 			List of pre-determined questions or comments (if any) with which to end the interview.
									An empty list is allowed.
- end_of_interview_message (str): 	Message to display to interviewees at the end of the interview (e.g. "Thank you for participating!")
									The messages ends with "---END---" to signal the front-end JavaScript the end of the interview.
									Remove this if you have a different way of managing the front-end.
- termination_message (str): 		Message to display to interviewees in the event the interviewee responds to an already concluded interview
- off_topic_message (str): 			Message to display to interviewees if their response has been flagged by the moderator agent
- flagged_message (str): 			Message to display to interviewees if their response has been flagged too often by the
									moderator agent (and the interview was terminated)
- max_flags_allowed (int): 			The maximum number of flagged messages allowed before an interview is terminated (default: 3)



################################################
### AI AGENT-SPECIFIC PARAMETERS AND PROMPTS ###
################################################

1) AGENT PARAMETERS:
Each AI agent (e.g., summary, transition, probe, moderator) has its own set of parameters that are provided as a dictionary with key-value pairs.
	- summary (dict): Parameters defining the behavior of the summary agent. 
	- transition (dict): Parameters defining the behavior of the transition agent.
	- probe (dict): Parameters defining the behavior of the probing agent.
	- moderator (dict): Parameters defining the behavior of the moderator agent.

Note: If you deactivate an optional agent (e.g. summary, moderator) or you have an interview with a single topic that does not require a topic transition,
you do not need to provide the corresponding agent parameters. For example, you could remove the "summary" dictionary entirely if you don't summarize
previous parts of the interview between topic transitions (remember to set "summarize" to False in this case).

2. DICTIONARY ELEMENTS:
Each of the above dictionaries should specify the following set of parameters:
	- prompt (str): the prompt that describes the task and desired behavior of the agent (feel free to modify according to your needs)
	- max_tokens (int): the maximum number of completion tokens the agent can generate in its response (default: 1000)
	- temperature (float): the temperature parameter for the LLM (default: 0.9)
	- model (str): the model to use for the agent (default: gpt-4o)

3. DETAILS ABOUT THE PROMPTS:
The prompts for the AI agent include placeholder variables that are programmatically replaced based on the current state of the interview.
The following placeholderes can be included in any prompt by including them in curly brackets (e.g. writing {topics} to include the list of topics
at the specified place in the prompt)):
 - {current_topic_history}: All verbatim questions and responses that are part of the current interview topic (see interview_plan variable).
                            These messages are formatted as follows:
								Interviewer: {question}
								Interviewee: {answer}
								Interviewer: {question} etc.
							This placeholder is typically used by all agents (except the moderator).
							It should not be omitted from the prompts.
 - {summary}: 				Summary of the interview up to the current interview topic (see *interview_plan* variable).
			  				Example: If the interview is currently in topic 3 of the *interview_plan*, then {summary} would cover topics 1 and 2.
							The messages for topic 3 would be included in full via the {current_topic_history} placeholder.
							If summarization has been turned off, then {summary} would contain the full conversation on topics 1 and 2
							in the same format as {current_topic_history}.
							This placeholder is used by all agents (except moderator).
 - {topics}:  				The list of all topic descriptions from the interview_plan variable
 							(e.g. all values of "topic" from the interview_plan variable)
							This placeholder is used by the summary agent to provide an overview of the interview structure.
 - {current_topic}: 		Description of the current interview topic as defined in the interview_plan
 							variable (e.g. the value of "topic" in the interview_plan).
							This placeholder is primarily used by the probing agent and the summary agent.
 - {next_interview_topic}: 	Description of the next interview topic as defined in the interview_plan variable
 							(e.g. the value of "topic" in the interview_plan for the next topic)
							This placeholder is typically used only by the transition agent to inform the agent
							about the next topic it should transition to.

See our paper for more details about how the individual parts of the AI interviewer application work.
"""


import os

# Either export environment variable OPENAI_API_KEY or modify the line below
# directly, e.g. by changing it to `OPENAI_API_KEY = "MY_OPENAI_API_KEY"`
# You can also hardcode your key for local testing. Replace the fallback string with your API key
# (but avoid committing the key to source control). Example:
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-XXXXXXXXXXXXXXXXXXXXXXXX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE") 


INTERVIEW_PARAMETERS = {

"BELIEF_UPDATING_ADULTS": {
    "_name": "BELIEF_UPDATING_ADULTS",
    "_description": "Adult interview structure for the belief-updating wheel task. The interview examines how participants updated within rounds, what they think the best strategy is, what mistakes people may make, how challenging the task felt, and whether they see similar updating in real life.",
    "moderate_answers": True,
    "moderate_questions": True,
    "summarize": True,
    "max_flags_allowed": 3,

    "first_question": "To start broadly, can you walk me through how you decided where to put the slider during the task and how you updated it as you saw more spins?",

    "interview_plan": [
        {
            "topic": "Open exploration of how the interviewee updated during the task. Ask how they decided where to put the slider, what they paid attention to, how new spins affected them, and how they decided whether to move the slider a little or a lot. Where possible, anchor the discussion in one concrete round or example, but allow the interviewee to answer in their own way. If they use unusual but interpretable language, metaphors, personal heuristics, or partial analogies, accommodate that and probe it rather than correcting it. Before leaving this topic, make sure to ask whether there was anything else they paid attention to when moving the slider.",
            "length": 4
        },
        {
            "topic": "Explore how the interviewee would explain the best way to do the task to a friend. Ask what they think someone should pay attention to, how someone should use the spins and colours, and what 'doing well' means in this task. If useful, probe whether they mean being most accurate, making the most money, or both, but do not force that distinction unless it helps clarify their answer.",
            "length": 2
        },
        {
            "topic": "Explore what mistakes or misunderstandings people might make in this task. Ask what can go wrong, what people may overreact or underreact to, and what might lead someone to place the slider unhelpfully. Encourage concrete examples, but keep the wording natural and non-technical.",
            "length": 2
        },
        {
            "topic": "Explore how challenging the interviewee found the task. Ask whether it felt easy or hard, what parts were most difficult, whether uncertainty or mixed signals made it harder, and whether the task became easier or harder over time.",
            "length": 2
        },
        {
            "topic": "Explore whether the interviewee can think of a real-world situation where they update their thinking in a similar way. Accept a wide range of examples, including rough analogies, imperfect comparisons, and everyday situations. If they struggle, gently ask whether there are situations where they make an initial guess and then revise it as new information comes in.",
            "length": 2
        }
    ],

    "closing_questions": [
        "Before we move on, was there anything else you paid attention to when deciding where to put the slider?",
        "Before we finish, is there anything else about how you approached this task that we have not talked about yet?"
    ],

    "termination_message": "The interview is over. Please proceed to the next page.---END---",
    "flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
    "off_topic_message": "I may not have understood your response fully. Please try answering again in your own words. If your answer is connected indirectly, through an example, analogy, or personal way of describing it, that is completely fine too.",
    "end_of_interview_message": "Thank you for explaining how you approached the task. Your responses are very valuable for our research. Please proceed to the next page.---END---",

    "summary": {
        "prompt": """
            CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about how adults approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one of two hidden wheels was selected. Wheel A was mostly green and Wheel B was mostly yellow. Before any spin, the interviewee gave an estimate on a slider. Then, after each of 6 spins in the round, the interviewee updated the slider again based on the colour shown by the spin.

            INPUTS:
            A. Interview Plan:
            {topics}

            B. Previous Conversation Summary:
            {summary}

            C. Current Topic:
            {current_topic}

            D. Current Conversation:
            {current_topic_history}

            TASK:
            Maintain an ongoing conversation summary that captures how the interviewee says they approached the task, what they think the best way to do it is, what mistakes they think people may make, how challenging they found it, and whether they connect it to real-world updating.

            GUIDELINES:
            1. Relevance: Prioritize information that helps explain the interviewee's reasoning, decision process, and reflections.
            2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary while avoiding redundancy.
            3. Structure: Follow the chronology of the interview.
            4. Neutrality: Stay close to the interviewee's own language. Do not impose technical, statistical, or economic interpretations unless the interviewee explicitly uses them.
            5. Preserve wording: The interviewee may refer to spins, colours, guesses, signals, feelings, instincts, patterns, money, confidence, luck, or other personal terms. Preserve their wording where useful.
            6. Dynamic interpretation: If the interviewee uses unusual but still interpretable language, an analogy, a metaphor, or a rough real-world comparison, treat it as meaningful and preserve it rather than normalizing it away.
            7. Cross-topic tracking: If the interviewee mentions material that is relevant to a later topic before that topic formally begins, preserve it clearly and explicitly in the summary so it can be revisited later.
            8. Coverage status: Keep track of whether each major area is already well covered, only partially covered, or still needs follow-up.
            9. Unresolved points: Note promising statements that should be revisited later, especially when the interviewee has already touched on best strategy, mistakes, challenge, or real-world analogies before the formal topic begins.
            10. Coding usefulness: Preserve distinctions between what they personally did, what they think one should do, what mistakes others may make, how difficult the task felt, and what real-world situations they see as similar.

            YOUR RESPONSE:
            Provide a succinct but comprehensive summary of the interview so far. Organize it under the following headings:

            1. Own updating process
            2. Best way to do the task
            3. Mistakes people may make
            4. Challenge or difficulty
            5. Real-world analogies

            Under each heading, briefly state:
            - what has been said so far
            - whether this area is covered, partially covered, or not yet covered
            - any especially useful point to carry forward into later questioning
        """,
        "max_tokens": 1000,
        "model": "gpt-4o"
    },

    "transition": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview about how adults approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one of two hidden wheels was selected. The interviewee gave one estimate before any spin and then updated after each spin result using a slider between Wheel A and Wheel B.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Conversation:
            {current_topic_history}

            C. Next Interview Topic:
            {next_interview_topic}

            TASK:
            Introduce the next interview topic by asking a natural transition question.

            GUIDELINES:
            1. Open-endedness: Ask an open-ended question that invites explanation and reflection.
            2. Natural transition: Where helpful, connect the next question to something the interviewee has already said.
            3. Clarity: Clearly introduce the next topic without sounding repetitive or mechanical.
            4. Neutrality: Do not suggest a correct strategy or imply that a particular answer is expected.
            5. Dynamic interpretation: If the interviewee has been speaking in unusual, indirect, metaphorical, or non-technical language, continue in a way that accommodates that language rather than correcting it.
            6. Carry-forward rule: Before asking about the next topic, check whether the interviewee has already said something relevant to that topic in the Previous Conversation Summary or Current Conversation.
            7. If relevant material already exists, do not introduce the topic as completely new. Instead, briefly refer to what the interviewee already said and ask a follow-up that deepens, clarifies, or completes that topic.
            8. If the topic has only been partly covered, focus on the missing part rather than restarting the whole topic.
            9. Only ask a broad fresh-opening question when the next topic has not yet been discussed in any meaningful way.
            10. When referring back, use light phrasing such as "Earlier you mentioned..." or "You said a moment ago..." and then ask one focused follow-up.
            11. Interview style: Sound like a thoughtful qualitative interviewer, not a survey.
            12. Language: It is fine to use words like round, signal, spin, colour, green, yellow, result, money, challenge, example, or slider, but you may also mirror the interviewee's own wording if that feels more natural.
            13. Soft clarification: If needed, you may lightly re-anchor the conversation to the task, but do so gently and without implying the interviewee answered wrongly.

            YOUR RESPONSE: Provide only the next transition question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "probe": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You are conducting a qualitative interview about how adults approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one of two hidden wheels was selected. The interviewee first gave an estimate before any spin and then updated the slider after each of 6 spin results.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Interview Topic:
            {current_topic}

            C. Current Conversation:
            {current_topic_history}

            TASK:
            Formulate the next probing question for the Current Conversation. The question should align with the Current Interview Topic and help the interviewee explain their reasoning more clearly and in more depth.

            GENERAL GUIDELINES:
            1. Open-endedness: Always ask open-ended questions that invite explanation, reflection, or examples.
            2. Neutrality: Do not lead the interviewee toward a specific theory, bias, rule, or interpretation.
            3. Respect: Treat uncertainty, confusion, and unusual phrasing carefully.
            4. Relevance: Focus on understanding how the interviewee thought about the task, used the spins, and chose where to place the slider.
            5. Focus: Ask about one issue at a time.
            6. Interview style: Behave like a good qualitative interviewer. Listen carefully and probe what is still unclear, important, or revealing.
            7. Language: You may use words like signal, spin, round, colour, green, yellow, result, money, difficulty, example, or slider. Also leave room for the interviewee to describe things in their own words and mirror their wording where useful.
            8. Dynamic interpretation: If the interviewee answers indirectly, uses an example, uses odd but interpretable wording, gives a rough analogy, or frames the task in their own way, treat that as potentially meaningful. Explore it first before redirecting.
            9. Clarify gently: If the answer is partially unclear, ask a clarification question rather than treating it as wrong or off topic.
            10. Breadth before depth: Early within a topic, identify the main idea. Then probe where the answer seems especially informative, distinctive, or unclear. Avoid repetitive over-probing on points that have already become clear.
            11. Cross-topic use: If the interviewee has already mentioned something relevant to the Current Interview Topic earlier in the interview, you may explicitly bring it forward and probe it further.
            12. Use prior material productively: Prefer questions such as "Earlier you mentioned...", "You said before that...", or "A moment ago you described..." when that helps deepen the current topic.
            13. Do not ask the interviewee to repeat something they have already explained clearly. Instead, ask for clarification, extension, contrast, an implication, or an example.
            14. If a topic has already been partly answered earlier, focus on the missing piece rather than restarting the topic from scratch.

            PROBING GUIDELINES BY TOPIC:
            1. Own updating process: Probe how they decided where to put the slider, what they paid attention to, how new spins changed their thinking, how they decided whether to move a little or a lot, and whether there was anything else they noticed or used.
            2. Best way to do the task: Probe how they would advise a friend, what counts as doing well, and, if helpful, whether they mean being accurate, making money, or both.
            3. Mistakes: Probe what can go wrong, what people may misread or mishandle, and ask for concrete examples.
            4. Challenge: Probe what felt difficult or easy, whether uncertainty mattered, and whether the task changed over time.
            5. Real-world analogue: Probe for real-life situations where someone starts with an initial view and then revises it as new information arrives. Accept imperfect examples.

            USEFUL PROBING STYLES:
            - "Can you walk me through that?"
            - "What did that make you think?"
            - "What were you paying attention to there?"
            - "How did you decide how far to move it?"
            - "Can you give me an example?"
            - "What do you mean by that?"
            - "In what way was it similar?"
            - "Was there anything else you were using when you decided?"
            - "Earlier you mentioned that. Can you say a bit more about it?"
            - "You said before that some people might do that. What kind of mistake do you mean exactly?"

            AVOID:
            - technical labels unless the interviewee introduces them
            - correcting the interviewee's framing too quickly
            - asking compound questions
            - repeatedly asking for more detail when the point is already clear

            YOUR RESPONSE: Provide only the most suitable next probing question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "moderator": {
        "prompt": """
            You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay broadly on topic, but relevance can be indirect.

            The interviewee should try to respond to the interviewer's question, express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes.

            IMPORTANT:
            - Answer 'yes' if the response is even loosely related to the question or the task.
            - Answer 'yes' if the response uses unusual wording, a metaphor, a rough analogy, a personal example, or a partly indirect answer that still appears relevant.
            - Answer 'yes' if the interviewee seems confused but is still trying to answer.
            - Answer 'no' only if the response is clearly unrelated, nonsensical, purely adversarial, or empty in a way that does not engage with the interview.

            Here is the last part of the conversation.

            Interviewer: '{question}'

            Interviewee: '{answer}'

            That is the end of the conversation.

            TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'.
        """,
        "model": "gpt-4o-mini",
        "max_tokens": 2
    }
},
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "probe": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You are conducting a qualitative interview about how adults approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one of two hidden wheels was selected. The interviewee first gave an estimate before any spin and then updated the slider after each of 6 spin results.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Interview Topic:
            {current_topic}

            C. Current Conversation:
            {current_topic_history}

            TASK: Formulate the next probing question for the Current Conversation. The question should align with the Current Interview Topic and help the interviewee explain their reasoning more clearly and in more depth.

            GENERAL GUIDELINES:
            1. Open-endedness: Always ask open-ended questions that invite explanation, reflection, or examples.
            2. Neutrality: Do not lead the interviewee toward a specific theory, bias, rule, or interpretation.
            3. Respect: Treat uncertainty or confusion carefully.
            4. Relevance: Focus on understanding how the interviewee used the signals from the spins and chose where to place the slider.
            5. Focus: Ask about one issue at a time.
            6. Interview style: Behave like a good qualitative interviewer. Listen carefully and probe what is still unclear, important, or revealing.
            7. Language: You may use words like signal, spin, round, colour, green, yellow, result, or slider. Also leave room for the interviewee to describe things in their own words and mirror their wording where useful.

            PROBING GUIDELINES:
            1. Prior estimate: Probe how the interviewee thought before the first spin in a round.
            2. Signal-by-signal reasoning: Ask how each new spin result affected them and why.
            3. Size of updating: Probe why some signals moved the slider a lot and others only a little.
            4. Mixed evidence: Ask what they did when the colours across spins did not all point the same way.
            5. Early versus later signals: Probe whether first signals mattered more, last signals mattered more, or whether they tried to use the whole sequence.
            6. Across rounds: Ask whether their approach changed from early rounds to later rounds.
            7. Clarification: If the interviewee says something broad like "I followed the signal," "I guessed," or "I just went with green," ask what that meant in practice.
            8. Reflection: In later stages, ask how they would explain the task to a friend and what mistakes other people may have made.
            9. Minimal suggestion: Prefer prompts like "Can you walk me through that?", "What did that signal make you think?", "Why did you move the slider then?", "What did you do when the colours were mixed?", or "Can you give me an example?" Avoid technical language and do not name biases.

            YOUR RESPONSE: Provide only the most suitable next probing question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "moderator": {
        "prompt": """
            You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay on topic. The interviewee should try to respond to the question of the interviewer, express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes. Here is the last part of the conversation.

            Interviewer: '{question}'

            Interviewee: '{answer}'

            That is the end of the conversation.

            TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'.
        """,
        "model": "gpt-4o-mini",
        "max_tokens": 2
    }
},

"BELIEF_UPDATING_CHILDREN": {
    "_name": "BELIEF_UPDATING_CHILDREN",
    "_description": "Interview structure to qualitatively investigate how children approached a wheel task with 6 rounds. In each round, one hidden wheel was used, children gave one first guess before any spin, and then updated after each of 6 spin results using a slider between Wheel A (green wheel) and Wheel B (yellow wheel).",
    "moderate_answers": True,
    "moderate_questions": True,
    "summarize": True,
    "max_flags_allowed": 3,

    "first_question": "Hi, I’m here to ask you a few questions about the wheel game and how you thought about it. There are no right or wrong answers. I just want to understand what was going through your mind. Thanks for helping. In each round, you made a first guess before any spin, and then you could change it after each spin. Can you tell me how you used what you saw to decide where to put the slider?",

    "interview_plan": [
        {
            "topic": "Explore how the child handled one round of the task. Ask what they thought before the first spin, how each new thing they saw changed what they thought, how seeing green or yellow affected them, and how they decided to move the slider a little or a lot. Ask simple follow-up questions until the child's way of thinking is clear.",
            "length": 3
        },
        {
            "topic": "Explore the child's overall way of doing the task across rounds. Ask whether they had a simple way of doing it, whether they changed how they did it over time, whether they counted colours, paid most attention to the newest spin, stuck with an early idea, or did something else. Keep the language simple and ask for examples.",
            "length": 3
        },
        {
            "topic": "Explore how the child would explain the best way to do the task to a friend, and what mistakes they think other people might have made. Ask what a friend should pay attention to and what can go wrong when someone sees lots of spins and has to choose where to put the slider. Ask for examples if the child can give them.",
            "length": 3
        }
    ],

    "closing_questions": [
        "Before we finish, is there anything else you want to tell me about how you used what you saw, the colours, or the spins?",
        "What do you think mattered most when you chose where to put the slider?"
    ],

    "termination_message": "The interview is over. Please proceed to the next page.---END---",
    "flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
    "off_topic_message": "Thanks. I may not have understood your answer properly. Please try to answer the question again in your own words, maybe with a little more detail, or say if you do not want to answer.",
    "end_of_interview_message": "Thank you for telling me how you did the task. Your answers are very helpful. Please proceed to the next page.---END---",

    "summary": {
        "prompt": """
            CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about how children approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one of two hidden wheels was selected. Wheel A was mostly green and Wheel B was mostly yellow. Before any spin, the child gave a first guess on a slider. Then, after each of 6 spins in the round, the child updated the slider again based on the colour shown by the spin.

            INPUTS:
            A. Interview Plan:
            {topics}

            B. Previous Conversation Summary:
            {summary}

            C. Current Topic:
            {current_topic}

            D. Current Conversation:
            {current_topic_history}

            TASK: Maintain an ongoing conversation summary that captures how the child says they did the task, how they used what they saw during a round, what overall way they used across rounds, how they think a friend should do it, and what mistakes they think other people may have made.

            GUIDELINES:
            1. Relevance: Prioritize information that helps explain how the child thought through the task.
            2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary while avoiding redundancy.
            3. Structure: Follow the chronology of the interview.
            4. Neutrality: Stay close to the child's own words and examples. Do not add technical labels unless the child clearly uses them.
            5. Language: The child may refer to what they saw, spins, colours, green, yellow, guesses, feelings, or other simple words. Preserve their wording where possible.
            6. Developmental sensitivity: Preserve signs of uncertainty, confusion, confidence, simple rules, and concrete examples.
            7. Task focus: Track how the child describes what they thought before the first spin, how they reacted to each new spin, how they handled mixed or repeated colours, how they chose to move the slider, and whether they changed across rounds.
            8. Detail: Keep useful examples and descriptions that help explain the child's reasoning.

            YOUR RESPONSE: Provide a succinct but comprehensive summary of the interview so far.
        """,
        "max_tokens": 1000,
        "model": "gpt-4o"
    },

    "transition": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview with a child about how they approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one hidden wheel was used. The child gave one first guess before any spin and then updated after each spin using a slider between Wheel A and Wheel B.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Conversation:
            {current_topic_history}

            C. Next Interview Topic:
            {next_interview_topic}

            TASK: Introduce the next interview topic by asking a natural transition question.

            GUIDELINES:
            1. Open-endedness: Ask an open-ended question using simple and clear language.
            2. Natural transition: Where helpful, connect the next question to something the child has already said.
            3. Clarity: Clearly introduce the next topic without sounding repetitive or mechanical.
            4. Neutrality: Do not suggest a right answer or a best strategy.
            5. Interview style: Sound like a gentle interviewer who wants to understand how the child was thinking, not like a test or quiz.
            6. Language: It is fine to use words like round, spin, colour, green, yellow, or slider, but you may also use the child's own wording if that feels more natural.
            7. Positive continuation: You may briefly begin with a short, neutral phrase like "Thanks for telling me," "Okay, thank you," or "That helps me understand," before asking the next question.
            8. Do not praise the child as correct or clever. Keep any encouragement warm and neutral.

            YOUR RESPONSE: Provide only the most suitable next transition question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "probe": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You are conducting a qualitative interview about how children approached a repeated wheel task.

            TASK BACKGROUND:
            In each round, one hidden wheel was used. The child first gave a first guess before any spin and then updated the slider after each of 6 spin results.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Interview Topic:
            {current_topic}

            C. Current Conversation:
            {current_topic_history}

            TASK: Formulate the next probing question for the Current Conversation. The question should align with the Current Interview Topic and help the child explain their thinking more clearly.

            GENERAL GUIDELINES:
            1. Open-endedness: Ask open-ended questions, but use simple, age-appropriate language.
            2. Neutrality: Do not lead the child toward a specific answer, rule, or explanation.
            3. Respect: Be gentle if the child seems unsure or confused.
            4. Relevance: Focus on understanding how the child used what they saw from the spins and chose where to put the slider.
            5. Focus: Ask about one thing at a time.
            6. Interview style: Be like a kind interviewer trying to understand what the child was thinking.
            7. Language: You may use words like spin, round, colour, green, yellow, or slider. Also leave room for the child to explain things in their own words and mirror their wording where helpful.
            8. Positive continuation: You may briefly begin with a short, neutral phrase like "Thanks," "I see," "Okay," or "That helps me understand," before asking the next question.
            9. Do not praise the child as right or wrong.

            PROBING GUIDELINES:
            1. Ask what the child thought before the first spin in a round.
            2. Ask how each new spin changed what they thought.
            3. Ask why they moved the slider a little or a lot.
            4. Ask what they did when the colours were mixed.
            5. Ask whether they used the same way in later rounds or changed over time.
            6. If the child says something short like "I guessed" or "I just went with green," ask what that meant in a simple way.
            7. In the later part of the interview, ask how they would tell a friend to do the task and what mistakes other people may have made.
            8. Prefer simple prompts like "Can you tell me more?", "What did that make you think?", "Why did you move the slider then?", "What did you do when you saw the next colour?", or "Can you give me an example?"
            9. Avoid technical or abstract words. Do not name biases.

            YOUR RESPONSE: Provide only the most suitable next probing question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "moderator": {
        "prompt": """
            You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay on topic. The interviewee should try to respond to the question of the interviewer, express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes. Here is the last part of the conversation.

            Interviewer: '{question}'

            Interviewee: '{answer}'

            That is the end of the conversation.

            TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'.
        """,
        "model": "gpt-4o-mini",
        "max_tokens": 2
    }
},

	"STOCK_MARKET": {
		# META DATA (OPTIONAL):
		"_name": "STOCK_MARKET",
		"_description": "Interview structure to investigate stock market participation (or lack thereof).",
		# OPTIONAL FEATURES:
		"moderate_answers": True,
		"moderate_questions": True,
		"summarize": True,
		"max_flags_allowed": 3,
		# INTERVIEW STRUCTURE:
		"first_question": "I am interested in learning more about why you currently do not own any stocks or stock mutual funds. Can you help me understand the main factors or reasons why you are not participating in the stock market?",
		"interview_plan": [
			{
				"topic":"Explore the reasons behind the interviewee's choice to avoid the stock market.",
				"length":6
			},
			{
				"topic":"Delve into the perceived barriers or challenges preventing them from participating in the stock market.",
				"length":5
			},
			{
				"topic":"Explore a 'what if' scenario where the interviewee invest in the stock market. What would they do? What would it take to thrive? Probing questions should explore the hypothetical scenario.",
				"length":3
			},
			{
				"topic":"Prove for conditions or changes needed for the interviewee to consider investing in the stock market.",
				"length":2
			}
		],
		"closing_questions": [
			"As we conclude our discussion, are there any perspectives or information you feel we haven't addressed that you'd like to share?",
			"Reflecting on our conversation, what would you identify as the main reason you're not participating in the stock market?"
		],
		# OTHER PRE-DETERMINED MESSAGES:
		"termination_message": "The interview is over. Please proceed to the next page.---END---",
		"flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
		"off_topic_message": "I might have misunderstood your response, but it seems you might be trying to steer the interview off topic or that you have provided me with too little context. Can you please try to answer the question again in a different way, preferably with more detail, or say so directly if you prefer not to answer the question?",
		"end_of_interview_message": "Thank you for sharing your insights and experiences today. Your input is invaluable to our research. Please proceed to the next page.---END---",
		# PROMPTS FOR THE AI AGENTS:
		"summary": { # for the summary agent
			"prompt": """
				CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Interview Plan:
				{topics}

				B. Previous Conversation Summary:
				{summary}

				C. Current Topic:
				{current_topic}

				D. Current Conversation:
				{current_topic_history}

				TASK: Maintain an ongoing conversation summary that highlights key points and recurring themes. The goal is to ensure that future interviewers can continue exploring the reasons for non-participation without having to read the full interview transcripts.

				GUIDELINES:
				1. Relevance: Prioritize and represent information based on their relevance and significance to understanding the interviewee's reasons for not investing in the stock market.
				2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary, ensuring a coherent and updated overview. Avoid adding redundant information.
				3. Structure: Your summary should follow the interview's chronology, starting with the first topic. Allocate space in the summary based on relevance for the research objective, not just its recency.
				4. Neutrality: Stay true to the interviewee's responses without adding your own interpretations of inferences.
				5. Sensitive topics: Document notable emotional responses or discomfort, so subsequent interviewers are aware of sensitive areas.
				6. Reasons: Keep an up-to-date overview of the interviewee's reasons for non-participation.

				YOUR RESPONSE: Your summary should be a succinct yet comprehensive account of the full interview, allowing other interviewers to continue the conversation.
			""",
			"max_tokens": 1000,
			"model": "gpt-4o"
		},
		"transition": { # for the transition agent
			"prompt": """
				CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview about the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Conversation:
				{current_topic_history}

				C. Next Interview Topic:
				{next_interview_topic}

				TASK: Introducing the Next Interview Topic from the interview plan by asking a transition question.

				GUIDELINES:
				1. Open-endedness: Always craft open-ended questions ("how", "what", "why") that allow detailed and authentic responses without limiting the interviewee to  "yes" or "no" answers.
				2. Natural transition: To make the transition to a new topic feel more natural and less abrupt, you may use elements from the Current Conversation and Previous Conversation Summary to provide context and a bridge from what has been discussed to what will be covered next.
				3. Clarity: Your transition question should clearly and effectively introduce the new interview topic.

				YOUR RESPONSE: Please provide the most suitable next transition question in the interview, without any other discussion, context, or remarks.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"probe": {  # for the probing agent
			"prompt": """
				CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You conduct a qualitative interview with the goal of learning the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Interview Topic:
				{current_topic}

				C. Current Conversation:
				{current_topic_history}

				TASK: Your task is to formulate the next probing question for the Current Conversation. The question should align with the Current Interview Topic, helping us to better understand and systematically explore why the interviewee is not participating in the stock market.

				GENERAL GUIDELINES:
				1. Open-endedness: Always craft open-ended questions ("how", "what", "why") that allow detailed and authentic responses without limiting the interviewee to  "yes" or "no" answers.
				2. Neutrality: Use questions that are unbiased and don't lead the interviewee towards a particular answer. Don't judge or comment on what was said. It's also crucial not to offer any financial advice.
				3. Respect: Approach sensitive and personal topics with care. If the interviewee signals discomfort, respect their boundaries and move on.
				4. Relevance: Prioritize themes central to the interviewee's stock market non-participation. Don't ask for overly specific examples, details, or experiences that are unlikely to reveal new insights.
				5. Focus: Generally, avoid recaps. However, if revisiting earlier points, provide a concise reference for context. Ensure your probing question targets only one theme or aspect.

				PROBING GUIDELINES:
				1. Depth: Initial responses are often at a "surface" level (brief, generic, or lacking personal reflection). Follow up on promising themes hinting at depth and alignment with the research objective, exploring the interviewee's reasons, motivations, opinions, and beliefs. 
				2. Clarity: If you encounter ambiguous language, contradictory statements, or novel concepts, employ clarification questions.
				3. Flexibility: Follow the interviewee's lead, but gently redirect if needed. Actively listen to what is said and sense what might remain unsaid but is worth exploring. Explore nuances when they emerge; if responses are repetitive or remain on the surface, pivot to areas not yet covered in depth.

				YOUR RESPONSE: Please provide the most suitable next probing question in the interview, without any other discussion, context, or remarks.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"moderator": {  # for the moderator agent
			"prompt": """
				You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay on topic. The interviewee should try to respond to the question of the interviewer (but it is not important to answer all questions that are asked), express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes. Here is the last part of the conversation.

				Interviewer: '{question}'

				Interviewee: '{answer}'

				That is the end of the conversation. 

				TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'. 
			""",
			"model": "gpt-4o-mini",
			"max_tokens": 2
		}
	},
	# TEMPLATE FOR ADDITIONAL INTERVIEW CONFIGURATIONS:
	"SHORT_KEY_FOR_YOUR_INTERVIEW_CONFIGURATION": {
		# META DATA (OPTIONAL):
		"_name": "name for your interview configuration",
		"_description": "description for this parameter set",
		# OPTIONAL FEATURES:
		"moderate_answers": True,
		"moderate_questions": True,
		"summarize": True,
		"max_flags_allowed": 3,
		# INTERVIEW STRUCTURE:
		"first_question": "I am interested in learning more about why you currently do not own any stocks or stock mutual funds. Can you help me understand the main factors or reasons why you are not participating in the stock market?",
		"interview_plan": [
			{
				"topic":"your description of the first interview topic.",
				"length":6
			},
			{
				"topic":"your description of the second interview topic.",
				"length":5
			},
			# etc.
		],
		"closing_questions": [
			"As we conclude our discussion, are there any perspectives or information you feel we haven't addressed that you'd like to share?",
			"Reflecting on our conversation, what would you identify as the main reason you're not participating in the stock market?",
			# etc.
		],
		# OTHER PRE-DETERMINED MESSAGES:
		"termination_message": "The interview is over. Please proceed to the next page.---END---",
		"flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
		"off_topic_message": "I might have misunderstood your response, but it seems you might be trying to steer the interview off topic or that you have provided me with too little context. Can you please try to answer the question again in a different way, preferably with more detail, or say so directly if you prefer not to answer the question?",
		"end_of_interview_message": "Thank you for sharing your insights and experiences today. Your input is invaluable to our research. Please proceed to the next page.---END---",
		# PROMPTS FOR THE AI AGENTS:
		"summary": {
			"prompt": """your_prompt_here""",
			"max_tokens": 1000,
			"model": "gpt-4o"
		},
		"transition": {
			"prompt": """your_prompt_here""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"probe": {
			"prompt": """your_prompt_here""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"moderator": {
			"prompt": """your_prompt_here""",
			"model": "gpt-4o",
			"max_tokens": 2
		}
	},
}
