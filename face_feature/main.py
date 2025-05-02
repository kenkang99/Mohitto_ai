import cv2
from ex_feature.evaluate import evaluate_feature
from ex_feature.result import generate_summary
import json
import re

id = '123'
curl = '직모'
length = '장발'
dyeing = "X"
forehead = "둥근 모양"
clown = "많이 도드라짐"
mood = "우아한"
care_level = "쉬움"

if __name__ == "__main__":
    image_path = "sample.jpg"   # 필요하면 경로 수정

    if image_path is None:
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")
    else :
        result_dict = generate_summary(image_path, id, curl, length, dyeing, forehead, clown, mood, care_level)

    with open(f"{id}.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
