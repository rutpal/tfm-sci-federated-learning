import requests

ENDPOINT_URL = "https://script.google.com/macros/s/AKfycbxJxNenedeR3EGhgxFPo30ZZl_sEdXVq14dJeGGDpR-ZkJnWbqr9PQhdN5-YWa85-uL/exec"

response = requests.post(
    ENDPOINT_URL,
    data={
        "filename": "test.txt",
        "file": "dGVzdA=="  # "test" en base64
    }
)

print(response.text)