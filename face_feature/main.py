import cv2
from ex_feature.evaluate import evaluate_feature
import json
import re

id = '123'

if __name__ == "__main__":
    image_path = "sample.jpg"   # 필요하면 경로 수정

    if image_path is None:
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")
    else :
        result_dict = evaluate_feature(image_path, id)

    with open(f"{id}.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
