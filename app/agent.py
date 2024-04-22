from utils import preprocess_logs
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

    def summarize(self, question, logs, retriever=None):
        self.question = question
        if retriever:
            retrieved_logs = self.retrieve_logs(retriever)
            prompt_formatted = self.prompt.format(
                question=question,
                logs=retrieved_logs
            )
        else:
            self.logs = preprocess_logs(logs)

            prompt_formatted = self.prompt.format(
                question=question,
                logs=self.logs
            )

        self.response = self.llm.predict(prompt_formatted)

    def retrieve_logs(self, retriever):
        retrieved_nodes = [node for node in retriever.retrieve(self.question) if node.score > 0.5]
        retriever_nodes = sorted(retrieved_nodes, key=lambda n: n.node_id)

        return '\n'.join([node.text for node in retriever_nodes])

    def get_question(self):
        return self.question

    def get_logs(self):
        return self.logs

    def get_response_list(self):
        return self.response.split('\n')
