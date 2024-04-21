import time
import requests
import gradio as gr
from utils import get_url_list
from models import SubmitQuestionAndDocumentRequest, GetQuestionAndFactsResponse, SubmitQuestionAndDocumentsResponse

base_url = 'https://cleric-agent-api-untxx3isja-uc.a.run.app'
# base_url = 'http://localhost:8000'


def fetch_facts(question, call_log_urls):
    if len(call_log_urls) == 0:
        raise gr.Error('Please input call log.')

    if len(question) == 0:
        raise gr.Error('Please input question.')

    urls = get_url_list(call_log_urls)
    payload = SubmitQuestionAndDocumentRequest(
        question=question,
        documents=urls
    ).dict()

    response = requests.post(f"{base_url}/submit_question_and_documents", json=payload)
    response = SubmitQuestionAndDocumentsResponse(**response.json())
    if response.status != 'success':
        raise gr.Error('Input error: ' + response.status)

    start_time = time.time()
    while True:
        response = requests.get(f"{base_url}/get_question_and_facts")
        if response.status_code != 200:
            raise gr.Error('Server response error.')

        data = GetQuestionAndFactsResponse(**response.json())
        if data.status == "done":
            break
        elif time.time() - start_time > 300:
            return None
        time.sleep(1)

    return '\n'.join(data.facts)


with gr.Blocks() as demo:
    gr.Markdown("""
    # Cleric Call Logs Summarize Agent
    
    ### Instructions:
    1. Enter the URLs in the "Call Log URLs" text box, separating each URL with a new line.
    2. Add your question related to these call logs.
    3. Click the "Submit" button to proceed.
    """)
    error_box = gr.Textbox(label="Error", visible=False)
    with gr.Row(equal_height=True):
        call_logs_box = gr.Textbox(label='Call Log URLs', lines=10)
        facts_box = gr.Textbox(label='Extracted Facts', lines=10)

    question_box = gr.Textbox(label='Question')
    submit_btn = gr.Button("Submit")

    submit_btn.click(
        fetch_facts,
        inputs=[question_box, call_logs_box],
        outputs=facts_box
    )

demo.launch()

