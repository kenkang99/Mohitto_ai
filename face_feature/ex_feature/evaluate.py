# evaluate.py
import cv2
import json
from .facemesh import extract_facial_ratios
from .extract_face_feature import predict
from .stone_classifier import extract_face_colors

def evaluate_feature(image_path, id):
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] 이미지 로드 실패")
        return {"error": "이미지 로드 실패"}

    faceshape = predict(image)
    top_ratio, mid_ratio, down_ratio = extract_facial_ratios(image)
    skin_tone = extract_face_colors(image_path)

    forehead_eval = ""
    if top_ratio is not None:
        if top_ratio < 0.328:
            forehead_eval = "좁은 편에 속합니다."
        elif 0.328 <= top_ratio <= 0.338:
            forehead_eval = "크지 않은 편에 속합니다."
        elif 0.338 <= top_ratio <= 0.346:
            forehead_eval = "평균적인 크기에 속합니다."  
        elif 0.346 <= top_ratio <= 0.354:
            forehead_eval = "작지 않은 편에 속합니다."      
        else:
            forehead_eval = "넓은 편에 속합니다."
    else:
        forehead_eval = "정보 없음"

    # 간단 요약 생성
    summary=""
    if faceshape and skin_tone and top_ratio:
        summary = f"{faceshape}형 얼굴이며, 피부색은 {skin_tone}입니다. 이마의 넓이는 {forehead_eval}"
    else:
        summary = "얼굴 인식이 불완전하거나 일부 정보가 부족합니다."

    result = {
        'ID' : id,
        "얼굴형": faceshape,
        "피부색": skin_tone,
        "상안부 비율": round(top_ratio, 3) if top_ratio is not None else None,
        "중안부 비율": round(mid_ratio, 3) if mid_ratio is not None else None,
        "하안부 비율": round(down_ratio, 3) if down_ratio is not None else None,
        "이마 평가": forehead_eval,
        "요약": summary
    }

    # 콘솔에도 출력
    print("\n=== 얼굴 분석 결과 ===")
    for k, v in result.items():
        print(f"{k} : {v}")
    return result
