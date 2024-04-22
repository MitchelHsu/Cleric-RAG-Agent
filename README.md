
# Cleric Call Logs Retrival Augmented Generation Agent

This is a call logs RAG agent PoC.
You can test it [here](https://huggingface.co/spaces/MitchelHsu/cleric-agent-ui).


### Implemented Architecture

The figure below shows the architecture of my implementation.
The core component is packaged as a container and hosted within GCP (Google Cloud Platform), and the UI is hosted with [HuggingFace Spaces](https://huggingface.co/spaces).

![System Architecture](static/sys_arch.png)


### Run with Docker

Pull the image from [this](https://hub.docker.com/repository/docker/mitchhsu/cleric-agent/general) container repo, the 
latest version is `v0.3`, you can use `latest` as well:
```shell
docker pull mitchhsu/cleric-agent:<version> 
```

Run container, the port of the application is set at `8000`:
```shell
docker run -p <host_port>:8000 mitchhsu/cleric-agent:<version>
```

To run the UI, just run:
```shell
python app/ui.py
```
Remember to install the dependencies by running `pip install -r requirements.txt`.


### Implementation Details

- `app/app.py`: Implements the API using Python Flask, there are two endpoints provided:
  - `submit_question_and_documents`: Handles user submissions of documents and question. Respond `"sucess"` if submission was successful. Error handling are covered when request schema mismatch, URLs format error, document load error, and no logs found.
  - `get_question_and_facts`: Handles user query of question and facts. Respond respective status of the query (`"done"`, `"processing"`, `"No data found"`).

    The endpoint also creates a `VectorStoreIndex` to split data into chunks, then passes a retriever for the Agent to retrieve relevant information.
- `app/agent.py`: Implements the agent logic, including prompt engineering. The agent is responsible for constructing a response given the call logs. Here I use `FewShotPromptTemplate` and `PromptTemplate` to format the prompt pass to `gpt`.
- `app/ui.py`: Implements the user interface using [gradio](https://www.gradio.app/).
- `app/utils.py`: Implements helper functions, such as URL validation, document retrieving, etc.
- `app/configs.py`: Stores configurations such as prompt templates and model selection.
- `app/models.py`: Defines the `pydantic` models for API request and response.
