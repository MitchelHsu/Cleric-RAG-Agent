
# LangChain templates
template = """
You are a call log summarization agent. Your job is to extract call summary bulletins only related to the question from a sequence of call logs. Please answer with bullets points only. Do not repeat facts in different bullets, and only response on facts with final decisions, avoid include previous decisions or decision process. Above are some examples of responses.\nGive response to the following question: {question}, according to the meeting logs:\n{logs}
"""

template_v2 = """
You are a call log fact extraction agent. Your task is to process and extract information from a set of call logs based on a single question provided.

Provide a concise list of facts extracted from the call logs that directly answer the question. Avoid including the conversation process of the facts in your response.  Provide only the list, without any other text. Each bullet should only contain one single fact. Please be mindful of the order of the logs and the updated facts/information/decisions and exclude any that have been canceled, including any associated relations.
If the question seems irrelevant to the call logs provided, please just reply "The question seems irrelevant to the call logs provided.". If you cannot understand the question, just reply "Sorry, I don't understand the question.".
Above are some response examples.

Question: {question}
List of Call Logs:
{logs}
"""

example_template = """Question: {question}
List of Call Logs:
{logs}
Answer:
{answer}"""

examples = [
    {'logs': "00:00:10 - Alex: Let's choose our app's color scheme today.\n00:00:36 - Jordan: I suggest blue for a calm feel.\n00:00:51 - Casey: We need to make sure it's accessible to all users.",
     'question': 'What product design decisions did the team make?',
     'answer': "- The team will use blue for the color scheme of the app.\n- The team will make the app accessible to all users."},
    {'logs': "1\n00:01:11,430 --> 00:01:40,520\n John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.\n\n2\n00:01:41,450 --> 00:01:49,190\nSara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.\n\n3\n00:01:49,340 --> 00:01:50,040\nMike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.",
     'question': 'What are our product design decisions?',
     'answer': "- The team has decided to go with a modular design for the product.\n- The team has decided to use a responsive design to ensure the product works well on all devices.\n- The team has decided to use a dark theme for the user interface."},
    {'logs': "1\n00:01:11,430 --> 00:01:40,520\nJohn: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.\n\n2\n00:01:41,450 --> 00:01:49,190\nSara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.\n\n3\n00:01:49,340 --> 00:01:50,040\nMike: I'm on board with that.",
     'question': 'What are our product design decisions?',
     'answer': "- The team has decided to go with a modular design for the product.\n- The team has decided to use a responsive design to ensure the product works well on all devices.\n- The team has decided to provide both dark and light theme options for the user interface."},
    {'logs': "1\n00:01:11,430 --> 00:01:40,520\nJohn: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.\n\n2\n00:01:41,450 --> 00:01:49,190\nSara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.\n\n3\n00:01:49,340 --> 00:01:50,040\nMike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.",
     'question': 'What are our product design decisions?',
     'answer': "- The team has decided to focus on a desktop-first design\n- The team has decided to provide both dark and light theme options for the user interface."},
]

# OPENAI MODEL
MODEL           = 'gpt-4'

# LLamaIndex Configs
CHUNK_SIZE      = 80  # For parser
CHUNK_OVERLAP   = 20

RETRIEVE_TOP_K  = 10
