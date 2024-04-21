from agent import Agent
from config import MODEL
from flask import Flask, jsonify, request
from utils import read_documents, preprocess_logs, validate_request_logs
from models import GetQuestionAndFactsResponse, SubmitQuestionAndDocumentsResponse, SubmitQuestionAndDocumentRequest

app = Flask(__name__)
agent = Agent(model=MODEL)
processing = False
submitted_data = None


@app.route('/get_question_and_facts', methods=['GET'])
def get_response():
    global submitted_data, processing, agent

    if not submitted_data:
        response = GetQuestionAndFactsResponse(
            question='',
            facts=[],
            status='No data found, please submit data'
        )
        return jsonify(response.dict()), 200

    if processing:
        response = GetQuestionAndFactsResponse(
            question=submitted_data.question,
            facts=[],
            status='processing'
        )
        return jsonify(response.dict()), 200

    response = GetQuestionAndFactsResponse(
        question=submitted_data.question,
        facts=agent.get_response_list(),
        status='done'
    )

    return jsonify(response.dict()), 200


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question():
    global submitted_data, processing, agent
    processing = True
    request_content = request.get_json()

    try:
        submitted_data = SubmitQuestionAndDocumentRequest(**request_content)
    except ValueError as e:
        response = SubmitQuestionAndDocumentsResponse(status=f'Request payload does not match expected schema: {str(e)}')
        return jsonify(response.dict())

    try:
        validate_request_logs(submitted_data.documents)
    except ValueError as e:
        response = SubmitQuestionAndDocumentsResponse(status=f'URL validation failed: {e}')
        return jsonify(response.dict())

    try:
        logs = read_documents(submitted_data.documents)
    except Exception as e:
        response = SubmitQuestionAndDocumentsResponse(status=f'URL read failed: {e}')
        return jsonify(response.dict())

    processed_logs = preprocess_logs(logs)

    agent.process_request(
        question=submitted_data.question,
        logs=processed_logs
    )

    processing = False
    response = SubmitQuestionAndDocumentsResponse(status='success')
    return jsonify(response.dict()), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
