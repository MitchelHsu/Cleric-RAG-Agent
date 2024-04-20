import requests
from typing import List


def load_logs(log_paths: List) -> str:
    logs = ""
    for i, path in enumerate(log_paths):
        with open(path, 'r') as f:
            logs += f"Log {i}:\n" + f.read() + '\n'

    return logs


def get_url_list(call_log_urls: str) -> List[str]:
    return call_log_urls.split('\n')


def read_documents(documents: List[str]) -> List[str]:
    logs = []
    for url in documents:
        response = requests.get(url)
        logs.append(response.text)

    return logs


def preprocess_logs(logs: List[str]):
    return '\n'.join(logs)
