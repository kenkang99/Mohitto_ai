# Extract_Face_Feature/utils/notifier.py

import requests

def notify_main_api(user_id: int, request_id: int):
    try:
        response = requests.post("http://main-api:8000/run-recommendation/", json={
            "user_id": user_id,
            "request_id": request_id
        })
        print("[INFO] Main API 호출 완료:", response.status_code)
    except Exception as e:
        print("[ERROR] Main API 호출 실패:", e)