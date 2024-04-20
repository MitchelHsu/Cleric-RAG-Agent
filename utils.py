import requests
from typing import List

def load_logs(log_paths: List) -> str:
    logs = ""
    for i, path in enumerate(log_paths):
        with open(path, 'r') as f:
            logs += f"Log {i}:\n" + f.read() + '\n'

    return logs

# def get_response(bullets: str) -> str:
#     response = ""
#     for bullet in bullets.split('\n'):
#         response += bullet + '\n'
