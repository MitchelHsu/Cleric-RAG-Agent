from langchain_openai import ChatOpenAI
from config import examples, example_template, template_v2
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate


class Agent:
    def __init__(self, model):
        self.llm = ChatOpenAI(model=model)

        # Example template
        self.example_prompt = PromptTemplate(
            template=example_template,
            input_variables=['question', 'logs', 'answer']
        )

        # Few shot prompt template containing examples and instructions
        self.prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=self.example_prompt,
            suffix=template_v2,
            input_variables=['question', 'logs']
        )

        self.question = None
        self.logs = None
        self.response = None

    def process_request(self, question, logs):
        self.question = question
        self.logs = logs

        prompt_formatted = self.prompt.format(
            question=question,
            logs=logs
        )

        self.response = self.llm.predict(prompt_formatted)

    def get_question(self):
        return self.question

    def get_logs(self):
        return self.logs

    def get_response_list(self):
        return self.response.split('\n')
