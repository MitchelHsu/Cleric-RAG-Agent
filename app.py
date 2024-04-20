import time
from agent import Agent
from config import MODEL
from pydantic import BaseModel
from typing import List, Optional
from flask import Flask, jsonify, request
from utils import read_documents, preprocess_logs

app = Flask(__name__)
agent = Agent(model=MODEL)
processing = False
submitted_data = None


class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: Optional[List[str]]
    status: str

class SubmitQuestionAndDocumentRequest(BaseModel):
    question: str
    documents: List[str]


@app.route('/get_question_and_facts', methods=['GET'])
def get_response():
    global submitted_data, processing, agent
    print('RECEIVED GET')

    if not submitted_data:
        return 'No data found.'

    if processing:
        response = GetQuestionAndFactsResponse(
            question=submitted_data.question,
            facts=[],
            status='processing'
        )
        return jsonify(response.dict())

    response = GetQuestionAndFactsResponse(
        question=submitted_data.question,
        facts=agent.get_response_list(),
        status='done'
    )

    return jsonify(response.dict()), 200


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question():
    global submitted_data, processing, agent
    print('HEREHERHEHERHERHERER')
    processing = True
    request_content = request.get_json()
    submitted_data = SubmitQuestionAndDocumentRequest(**request_content)

    logs = read_documents(submitted_data.documents)
    processed_logs = preprocess_logs(logs)

    agent.process_request(
        question=submitted_data.question,
        logs=processed_logs
    )

    processing = False
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
