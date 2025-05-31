from model import model_call
import cv2
import torch
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import os
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from uuid import uuid4

app = FastAPI()

def load_image_from_url(url: str) -> Image.Image:
    response = requests.get(url)
    response.raise_for_status()
    
    return Image.open(BytesIO(response.content)).convert("RGB")

@app.post("/simulate")
def simulate(data: dict = Body(...)):
    source_url = data["user_image_url"]
    ref_url = data["ref_image_url"]

    # 이미지 불러오기
    source_img = load_image_from_url(source_url)
    ref_img = load_image_from_url(ref_url)

    # 모델 호출
    bald_image, result_image = model_call(source_img, ref_img)

    # 고유 ID 생성
    file_id = str(uuid4())

    # result_image를 OpenCV 형식으로 변환
    if isinstance(result_image, Image.Image):
        result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_RGB2BGR)

    # PNG 형식으로 메모리에 저장
    _, png_encoded = cv2.imencode(".png", result_image)
    image_bytes = BytesIO(png_encoded.tobytes())

    return StreamingResponse(image_bytes, media_type="image/png", headers={
        "Content-Disposition": f"inline; filename={file_id}_result.png"
    })
