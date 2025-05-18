import cv2
import requests
import sys
import os
import numpy as np
import json
import uuid
from datetime import datetime
from db_utils import get_latest_request, save_result_to_db
from ex_feature.result import generate_summary

# 입력 인자 (API로 부터 받은 정보들: 밑에 주석으로 추후에 api -> 모델 로직 수정후 대체)
user_id = int(sys.argv[1])
request_id = int(sys.argv[2])
# user_id = int(os.environ["USER_ID"])  
# request_id = int(os.environ["REQUEST_ID"])

# ✅ S3 URL에서 이미지 불러오기
def read_image_from_url(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise FileNotFoundError(f"[다운로드 실패] 이미지를 불러올 수 없습니다: {url}")
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"[디코딩 실패] OpenCV가 이미지를 디코딩하지 못했습니다: {url}")
    return image

if __name__ == "__main__":
    info = get_latest_request(user_id, request_id)

    print("[DEBUG] DB에서 가져온 요청 정보:", info)
    if not info:
        raise ValueError("요청 정보를 찾을 수 없습니다.")

    request_id = str(info["request_id"])
    image_url = info["user_image_url"]

    # ✅ S3 URL에서 이미지 불러오기
    image = read_image_from_url(image_url)

    result_dict = generate_summary(
        image,
        request_id,
        info["hair_type"],
        info["hair_length"],
        "X" if info["dyed"] == 0 else "O",
        info["forehead_shape"],
        info["cheekbone"],
        info["mood"],
        info["difficulty"]
    )
    
    result_dict["request_id"] = request_id
    result_dict["성별"] = info["sex"]
    
    final_result = {
        "request_id": request_id,
        "input": {
            "user_image_url": info["user_image_url"],
            "hair_type": info["hair_type"],
            "hair_length": info["hair_length"],
            "dyed": info["dyed"],
            "forehead_shape": info["forehead_shape"],
            "cheekbone": info["cheekbone"],
            "mood": info["mood"],
            "difficulty": info["difficulty"]
        },
        "result": result_dict
    }

    file_name = f"recommend_{request_id}_{uuid.uuid4().hex}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)

    print(f"✅ 추천 결과 저장 완료: {file_name}")
    
    ##### DB에 result 추가
save_result_to_db(result_dict, int(request_id))
print(f"✅ 분석 결과 DB 저장 완료 (request_id={request_id})")