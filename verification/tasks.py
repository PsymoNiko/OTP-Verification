import requests
from celery import Celery

import os

API_KEY = os.environ.get('API_KEY')

app = Celery('tasks', broker='redis://localhost:6379')


@app.task()
def send_OTP(phone_number: str, otp: str) -> None:
    url = "https://api.sms.ir/v1/send/verify/"
    data = {
        "mobile": phone_number,
        "templateId": 100000,
        "parameters": [
            {
                "name": "Code",
                "value": otp
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": API_KEY
    }
    requests.post(url, json=data, headers=headers)
