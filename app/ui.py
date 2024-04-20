import time
import requests
import gradio as gr
from utils import get_url_list
from models import SubmitQuestionAndDocumentRequest, GetQuestionAndFactsResponse

base_url = 'https://cleric-agent-ad76f992e8d8.herokuapp.com/'


def fetch_facts(question, call_log_urls):
    urls = get_url_list(call_log_urls)
    payload = SubmitQuestionAndDocumentRequest(
        question=question,
        urls=urls
    ).dict()
    response = requests.post(f"{base_url}/submit_question_and_documents", json=payload)

    start_time = time.time()
    while True:
        response = requests.get(f"{base_url}/get_question_and_facts")
        if response.status_code != 200:
            # st.error(f"Unexpected status code when getting question and facts: {response.status_code}")
            return None
        try:
            data = GetQuestionAndFactsResponse(**response.json())
        except ValueError as e:
            # st.error(f"The response data does not match the expected schema: {str(e)}")
            # st.write(response.json())  # Print the invalid data for debugging
            return None

        if data.status == "done":
            break
        elif time.time() - start_time > 300:  # 5 minutes timeout
            # st.error("Timeout: Facts not ready after 5 minutes")
            return None
        time.sleep(1)

    return '\n'.join(data.facts)


with gr.Blocks() as demo:
    gr.Markdown("""
    # Cleric Call Logs Summarize Agent
    
    Please place the URLs in the Call Logs URLs text box, separated by new line.
    Place your question to this call logs, then submit! 
    """)
    error_box = gr.Textbox(label="Error", visible=False)
    with gr.Row(equal_height=True):
        call_logs_box = gr.Textbox(label='Call Logs URLs', scale=2)
        facts_box = gr.Textbox(label='Extracted Facts', scale=2)

    question_box = gr.Textbox(label='Question')
    submit_btn = gr.Button("Submit")

    submit_btn.click(
        fetch_facts,
        inputs=[call_logs_box, question_box],
        outputs=facts_box
    )

# iface = gr.Interface(
#     fn=fetch_facts,
#     inputs=["text", "text"],
#     outputs="text",
#     allow_flagging="never",
#     title="Cleric Call Logs Summarize Agent"
# )
demo.launch()

