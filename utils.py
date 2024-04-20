template = """You are a call log summarization agent. Your job is to extract call summary bulletins only related to the question from a sequence of call logs. Please answer with bullets points only. Do not repeat facts in different bullets. Above are some examples of responses.\nGive response to the following question: {question}, according to the meeting logs:\n{logs} """

example_template = """Question: {question}\nLogs:\n{logs}\nAnswer:\n{answer}"""

examples = [
    {'logs': "00:00:10 - Alex: Let's choose our app's color scheme today.\n00:00:36 - Jordan: I suggest blue for a "
             "calm feel.\n00:00:51 - Casey: We need to make sure it's accessible to all users.",
     'question': 'What product design decisions did the team make?',
     'answer': "- The team will use blue for the color scheme of the app.\n- The team will make the app accessible to "
               "all users."},
    {'logs': "1\n00:01:11,430 --> 00:01:40,520 John: After giving it some more thought, I believe we should also "
             "consider a light theme option for the user interface. This will cater to users who prefer a brighter "
             "interface. \n2 \n00:01:41,450 --> 00:01:49,190 Sara: That's a great idea, John. A light theme will "
             "provide an alternative to users who find the dark theme too intense.\n 3\n00:01:49,340 --> 00:01:50,"
             "040 Mike: I'm on board with that.",
     'question': 'What are our product design decisions?',
     'answer': "- The team has decided to go with a modular design for the product.\n- The team has decided to use a "
               "responsive design to ensure the product works well on all devices.\n- The team has decided to provide "
               "both dark and light theme options for the user interface."},
]

MODEL = 'gpt-4'


def load_logs(log_paths: list) -> str:
    logs = ""
    for i, path in enumerate(log_paths):
        with open(path, 'r') as f:
            logs += f"Log {i}:\n" + f.read() + '\n'

    return logs

# def get_response(bullets: str) -> str:
#     response = ""
#     for bullet in bullets.split('\n'):
#         response += bullet + '\n'
