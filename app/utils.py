import requests
import validators
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
        response.raise_for_status()
        logs.append(response.text)

    return logs


def preprocess_logs(logs: List[str]):
    return '\n'.join(logs)


def validate_request_logs(urls: List[str]):
    for url in urls:
        if not validators.url(url):
            raise ValueError(f'The following URL is invalid: {url}')
