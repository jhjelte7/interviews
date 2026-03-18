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
    "_description": "Interview structure to qualitatively investigate how adults approached a repeated task in which they used a slider to report whether they thought it was more likely to be the green wheel or the yellow wheel after a series of spin results.",
    "moderate_answers": True,
    "moderate_questions": True,
    "summarize": True,
    "max_flags_allowed": 3,

    "first_question": "In the task, you saw a series of spin results and used a slider to show whether you thought it was more likely to be the green wheel or the yellow wheel. Can you walk me through how you used those spin results to decide where to put the slider?",

    "interview_plan": [
        {
            "topic": "Explore in depth how the interviewee used the sequence of spin results during a round. Ask how they reacted to each new spin result, whether early results mattered more than later ones or vice versa, whether some results changed their mind a lot while others changed it only a little, and how they decided when to move the slider more or less. Probe for step-by-step reasoning and concrete examples from the task.",
            "length": 5
        },
        {
            "topic": "Explore the interviewee's general approach or strategy across rounds. Ask whether they had a rule of thumb, whether that approach changed over time, whether they looked for patterns, counted colors, focused on recent results, stuck with a first impression, or did something else. Probe for how stable or flexible their approach was and how they handled mixed or surprising results.",
            "length": 5
        },
        {
            "topic": "Explore how the interviewee would explain the best way to do the task to a friend, and what mistakes they think other people might have made. Ask what a good approach would be, what people should pay attention to, and what can go wrong when someone sees a sequence of spin results and has to decide where to place the slider. Probe for misunderstandings, shortcuts, overconfidence, giving too much weight to one result, giving too little weight to new results, or getting confused by mixed evidence, but keep the wording natural and non-technical.",
            "length": 5
        }
    ],

    "closing_questions": [
        "Before we finish, is there anything else about how you used the spin results that we have not talked about yet?",
        "Looking back, what do you think was the main thing shaping how you moved the slider?"
    ],

    "termination_message": "The interview is over. Please proceed to the next page.---END---",
    "flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
    "off_topic_message": "I might have misunderstood your response, but it seems that your answer may not be about the task. Please try to answer the question again in your own words, preferably with a bit more detail, or say directly if you prefer not to answer.",
    "end_of_interview_message": "Thank you for explaining how you approached the task. Your responses are very valuable for our research. Please proceed to the next page.---END---",

    "summary": {
        "prompt": """
            CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about how adults approached a repeated decision task.

            In the task, the interviewee saw a sequence of spin results and used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel.

            INPUTS:
            A. Interview Plan:
            {topics}

            B. Previous Conversation Summary:
            {summary}

            C. Current Topic:
            {current_topic}

            D. Current Conversation:
            {current_topic_history}

            TASK: Maintain an ongoing conversation summary that captures how the interviewee responded to the sequence of spin results, what approach they used across rounds, how they think the task should best be done, and what mistakes they think other people may have made.

            GUIDELINES:
            1. Relevance: Prioritize information that explains the interviewee's reasoning process in the task.
            2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary while avoiding redundancy.
            3. Structure: Follow the chronology of the interview.
            4. Neutrality: Stay close to the interviewee's own language. Do not impose technical, statistical, or economic interpretations unless the interviewee explicitly uses them.
            5. Task focus: Track how the interviewee describes reacting to each new spin result, handling conflicting or mixed results, deciding whether to move the slider a little or a lot, and changing or keeping an overall approach across rounds.
            6. Detail: Preserve useful details about rules of thumb, attention to early versus later results, confidence, hesitation, and descriptions of common mistakes.
            7. Sensitivity: Note confusion, inconsistency, uncertainty, or especially revealing examples that may matter for later probing.

            YOUR RESPONSE: Provide a succinct but comprehensive summary of the interview so far.
        """,
        "max_tokens": 1000,
        "model": "gpt-4o"
    },

    "transition": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview about how adults approached a repeated decision task.

            In the task, the interviewee saw a sequence of spin results and used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Conversation:
            {current_topic_history}

            C. Next Interview Topic:
            {next_interview_topic}

            TASK: Introduce the next interview topic by asking a natural transition question.

            GUIDELINES:
            1. Open-endedness: Ask an open-ended question that invites explanation and reflection.
            2. Natural transition: Where helpful, connect the next question to something the interviewee has already said.
            3. Clarity: Clearly introduce the next topic without sounding repetitive or mechanical.
            4. Neutrality: Do not suggest a correct strategy or imply that a particular answer is expected.
            5. Interview style: Sound like a thoughtful qualitative interviewer, not a survey. Open space for the interviewee to explain their reasoning in depth.

            IMPORTANT:
            The interview should explore:
            - how the interviewee responded to the sequence of spin results,
            - what overall approach they used across rounds,
            - how they would explain the best way to do the task,
            - what mistakes they think other people might have made.

            YOUR RESPONSE: Provide only the next transition question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "probe": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You are conducting a qualitative interview about how adults approached a repeated decision task.

            In the task, the interviewee saw a sequence of spin results and used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel.

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
            2. Neutrality: Do not lead the interviewee toward a specific theory, rule, or interpretation.
            3. Respect: Treat uncertainty or confusion carefully.
            4. Relevance: Focus on understanding how the interviewee reacted to the sequence of spin results and chose where to place the slider.
            5. Focus: Ask about one issue at a time.
            6. Interview style: Behave like a good qualitative interviewer. Listen carefully and probe what is still unclear, important, or revealing.

            PROBING GUIDELINES:
            1. Sequence: Ask how the interviewee responded when a new spin result came in and whether that changed their view a little or a lot.
            2. Timing: Probe whether early results mattered more, later results mattered more, or whether they tried to use all results together.
            3. Mixed evidence: Ask how they handled rounds where the results pointed in different directions.
            4. Strategy: Probe for rules of thumb, counting, pattern-seeking, sticking with a first impression, relying on recent results, or changing approach across rounds, but do so in natural language.
            5. Change over time: Ask whether they approached later rounds differently from earlier rounds.
            6. Clarification: If the interviewee says something broad like "I just followed the spins" or "I guessed," ask what that meant in practice.
            7. Reflection: In later stages, ask what a friend should do and what mistakes others may have made.
            8. Minimal suggestion: Prefer prompts like "Can you walk me through that?", "What made you move the slider then?", "How did that next result affect you?", "What did you do when the results were mixed?", or "Can you give me an example?" Avoid technical language.

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
    "_description": "Interview structure to qualitatively investigate how children approached a task in which they used a slider to say whether they thought it was more likely to be the green wheel or the yellow wheel after seeing the result of a spin.",
    "moderate_answers": True,
    "moderate_questions": True,
    "summarize": True,
    "max_flags_allowed": 3,

    "first_question": "In the task, you used a slider to show whether you thought it was more likely to be the green wheel or the yellow wheel after you saw the spin result. Can you tell me how you decided where to put the slider?",

    "interview_plan": [
        {
            "topic": "Explore how the child did the task. Ask the child to explain what they thought about when they saw the spin result, how they thought about the green wheel and the yellow wheel, how sure or unsure they felt, and how they decided where to put the slider. Ask simple follow-up questions and keep going until the child's way of thinking is clear.",
            "length": 5
        },
        {
            "topic": "Explore how the child would explain to a friend the best way to do the task. Ask what they think a friend should look at, what a good way to do it is, and how someone should decide where to put the slider. Ask for examples and simple explanations.",
            "length": 4
        },
        {
            "topic": "Explore what mistakes the child thinks other people might have made in the task. Ask about ways someone might get confused, forget something important, use the slider badly, or make the wrong choice after seeing the spin result. Ask for examples if the child can give them.",
            "length": 4
        }
    ],

    "closing_questions": [
        "Before we finish, is there anything else you want to tell me about how you did the task?",
        "What do you think was the most important part when you chose where to put the slider?"
    ],

    "termination_message": "The interview is over. Please proceed to the next page.---END---",
    "flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
    "off_topic_message": "I might have misunderstood your answer. Please try to answer the question again in your own words, maybe with a little more detail, or say if you do not want to answer.",
    "end_of_interview_message": "Thank you for telling me how you did the task. Your answers are very helpful. Please proceed to the next page.---END---",

    "summary": {
        "prompt": """
            CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about how children approached a task.

            In the task, the child used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel after seeing the result of a spin.

            INPUTS:
            A. Interview Plan:
            {topics}

            B. Previous Conversation Summary:
            {summary}

            C. Current Topic:
            {current_topic}

            D. Current Conversation:
            {current_topic_history}

            TASK: Maintain an ongoing conversation summary that captures how the child says they did the task, how they think a friend should do it, and what mistakes they think other people may have made.

            GUIDELINES:
            1. Relevance: Prioritize information that helps explain how the child thought through the task.
            2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary while avoiding redundancy.
            3. Structure: Follow the chronology of the interview.
            4. Neutrality: Stay close to the child's own words and examples. Do not add technical labels unless the child clearly uses them.
            5. Developmental sensitivity: Preserve signs of uncertainty, confusion, confidence, simple rules, and concrete examples.
            6. Task focus: Keep track of how the child describes using the spin result, thinking about the green wheel and the yellow wheel, and deciding where to put the slider.
            7. Detail: Keep useful examples and descriptions that help explain the child's reasoning.

            YOUR RESPONSE: Provide a succinct but comprehensive summary of the interview so far.
        """,
        "max_tokens": 1000,
        "model": "gpt-4o"
    },

    "transition": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview with a child about how they approached a task.

            In the task, the child used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel after seeing the result of a spin.

            INPUTS:
            A. Previous Conversation Summary:
            {summary}

            B. Current Conversation:
            {current_topic_history}

            C. Next Interview Topic:
            {next_interview_topic}

            TASK: Introduce the next interview topic by asking a natural and child-appropriate transition question.

            GUIDELINES:
            1. Open-endedness: Ask an open-ended question using simple and clear language.
            2. Natural transition: Where useful, connect the next question to what the child has already said.
            3. Clarity: Focus on one idea at a time.
            4. Neutrality: Do not suggest a right answer.
            5. Interview style: Sound like a gentle interviewer who wants to understand how the child was thinking, not like a test or quiz.

            IMPORTANT:
            The interview should explore three broad areas:
            - how the child did the task,
            - how they would explain the best way to do it to a friend,
            - what mistakes they think other people might have made.

            YOUR RESPONSE: Provide only the next transition question.
        """,
        "temperature": 0.7,
        "model": "gpt-4o",
        "max_tokens": 300
    },

    "probe": {
        "prompt": """
            CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You are conducting a qualitative interview with a child about how they approached a task.

            In the task, the child used a slider to show whether they thought it was more likely to be the green wheel or the yellow wheel after seeing the result of a spin.

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
            2. Neutrality: Do not lead the child toward a specific answer.
            3. Respect: Be gentle if the child seems unsure or confused.
            4. Relevance: Focus on how the child used the spin result, thought about the two wheels, and chose where to put the slider.
            5. Focus: Ask about one thing at a time.
            6. Interview style: Be like a kind interviewer trying to understand what the child was thinking. Listen carefully and ask about what is still unclear or interesting.

            PROBING GUIDELINES:
            1. Ask the child to explain what they did step by step.
            2. Ask for simple examples when useful.
            3. If the child says something short like "I guessed" or "I just knew," ask what that means in a simple way.
            4. Ask how sure or unsure the child felt, when that seems helpful.
            5. In the second topic, help the child explain how they would tell a friend to do the task.
            6. In the third topic, help the child explain what mistakes other people might have made.
            7. Prefer simple prompts like "Can you tell me more?", "How did you choose?", "What made you think that?", "What happened in your head then?", or "Can you give me an example?"
            8. Avoid technical or abstract words. Keep questions clear and easy for an 8-year-old to understand.

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
