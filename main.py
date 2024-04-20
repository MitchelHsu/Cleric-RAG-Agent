import os

from utils import *
from langchain_openai import ChatOpenAI
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

llm = ChatOpenAI(model=MODEL)


if __name__ == '__main__':
    log_paths = [os.path.join('logs', path) for path in sorted(os.listdir('logs'))]
    logs = load_logs(log_paths)

    example_prompt = PromptTemplate(
        template=example_template,
        input_variables=["question", "logs", "answer"]
    )

    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix=template,
        input_variables=["question", "logs"]
    )

    prompt_formatted = prompt.format(
        question='What product design decisions did the team make?',
        logs=logs
    )

    print(prompt_formatted)
    bullets = llm.predict(prompt_formatted)
    print(bullets)

