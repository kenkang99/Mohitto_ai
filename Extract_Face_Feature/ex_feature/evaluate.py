# evaluate.py
import cv2
import json
import requests
import numpy as np
from .facemesh import extract_facial_ratios
from .extract_faceshape import predict_faceshape
# from .stone_classifier import extract_face_colors
from .extract_face_feature import extract_feature

def read_image_from_url(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise FileNotFoundError(f"[다운로드 실패] 이미지를 불러올 수 없습니다: {url}")
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"[디코딩 실패] OpenCV가 이미지를 디코딩하지 못했습니다: {url}")
    return image

def evaluate_feature(image_path):
    # 이미지 정보 추출
    image = read_image_from_url(image_path)
    faceshape, top_ratio, mid_ratio, down_ratio = extract_feature(image)

    # 얼굴형 생성
    faceshape_eval = ""
    if faceshape is not None:
        if faceshape == "Oval":
            faceshape_eval = "계란형"
        elif faceshape == "Heart":
            faceshape_eval = "하트형"
        elif faceshape == "Square":
            faceshape_eval = "네모형"
        elif faceshape == "Round":
            faceshape_eval = "둥근형"
        elif faceshape == "Oblong":
            faceshape_eval = "긴형"
        else:
            faceshape_eval = "정보 없음"

    # 이마 평가
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

    # 중안부 평가
    central_eval = ""
    if mid_ratio is not None:
        if mid_ratio < 0.326:
            central_eval = "좁은 편에 속합니다."
        elif 0.326 <= mid_ratio <= 0.333:
            central_eval = "크지 않은 편에 속합니다."
        elif 0.333 <= mid_ratio <= 0.341:
            central_eval = "평균적인 크기에 속합니다."  
        elif 0.341 <= mid_ratio <= 0.349:
            central_eval = "작지 않은 편에 속합니다."      
        else:
            central_eval = "넓은 편에 속합니다."
    else:
        central_eval = "정보 없음"

    # 하안부 평가
    low_eval = ""
    if down_ratio is not None:
        if down_ratio < 0.304:
            low_eval = "좁은 편에 속합니다."
        elif 0.304 <= down_ratio <= 0.316:
            low_eval = "크지 않은 편에 속합니다."
        elif 0.316 <= down_ratio <= 0.327:
            low_eval = "평균적인 크기에 속합니다."  
        elif 0.327 <= down_ratio <= 0.34:
            low_eval = "작지 않은 편에 속합니다."      
        else:
            low_eval = "넓은 편에 속합니다."
    else:
        low_eval = "정보 없음"

    # 얼굴 비율 중 어떤 부위가 유독 긴지 판단
    region_status = "비율 정보 부족"
    if top_ratio and mid_ratio and down_ratio:
        max_val = max(top_ratio, mid_ratio, down_ratio)
        if max_val == top_ratio:
            region_status = "상안부가 유독 김"
        elif max_val == mid_ratio:
            region_status = "중안부가 유독 김"
        elif max_val == down_ratio:
            region_status = "하안부가 유독 김"

        # 세 비율이 유사한 경우
        if abs(top_ratio - mid_ratio) < 0.05 and abs(mid_ratio - down_ratio) < 0.05:
            region_status = "3개 비율이 유사함"

    # 얼굴형별 종합 평가 문장 매핑
    evaluation_table = {
        # 하트형
        ("하트형", "상안부가 유독 김"): "이마가 강조되어 얼굴 상단의 이미지가 강합니다.",
        ("하트형", "중안부가 유독 김"): "중앙이 길어 얼굴이 전체적으로 늘씬하고 또렷한 느낌을 줍니다.",
        ("하트형", "하안부가 유독 김"): "하관이 강조되어 상대적으로 날카롭고 선이 도드라지는 인상입니다.",
        ("하트형", "3개 비율이 유사함"): "전체적으로 균형 잡힌 부드러운 인상을 주는 얼굴입니다.",

        # 계란형
        ("계란형", "상안부가 유독 김"): "이마가 넓고 눈썹 위로 시선이 모이며, 지적인 분위기가 느껴집니다.",
        ("계란형", "중안부가 유독 김"): "중안부가 강조되어 차분하고 또렷한 인상을 주며, 안정감 있는 이미지입니다.",
        ("계란형", "하안부가 유독 김"): "아래쪽이 강조되어 신뢰감 있고 단단한 인상을 줍니다.",
        ("계란형", "3개 비율이 유사함"): "이상적인 균형을 가진 얼굴로, 누구에게나 편안하고 조화로운 인상을 줍니다.",

        # 둥근형
        ("둥근형", "상안부가 유독 김"): "이마와 볼이 강조되어 부드럽고 친근한 느낌입니다.",
        ("둥근형", "중안부가 유독 김"): "눈과 코 중심부가 길어져 귀여움과 함께 깔끔한 이미지가 함께 느껴집니다.",
        ("둥근형", "하안부가 유독 김"): "하관이 부각되어 생기 있고 활달한 인상을 줍니다.",
        ("둥근형", "3개 비율이 유사함"): "전체적으로 부드럽고 온화한 인상을 주며, 친근한 이미지가 강조됩니다.",

        # 네모형
        ("네모형", "상안부가 유독 김"): "이마와 얼굴 외곽이 강하게 표현되어 단호하고 카리스마 있는 인상을 줍니다.",
        ("네모형", "중안부가 유독 김"): "중앙이 강조되어 높은 시선 집중도를 보입니다.",
        ("네모형", "하안부가 유독 김"): "강한 하관이 부각되어 주도적이고 결단력 있는 인상을 줍니다.",
        ("네모형", "3개 비율이 유사함"): "균형 잡힌 각진 얼굴로, 세련되고 자신감 있는 인상을 줍니다.",

        # 긴형 (타원형)
        ("긴형", "상안부가 유독 김"): "이마가 강조되어 고요하고 차분한 느낌의 인상을 줍니다.",
        ("긴형", "중안부가 유독 김"): "중앙이 길어 이성적이고 절제된 분위기가 느껴지는 얼굴입니다.",
        ("긴형", "하안부가 유독 김"): "하관이 길어 얼굴 하단이 강조되며, 진중하고 깊은 인상을 줍니다.",
        ("긴형", "3개 비율이 유사함"): "전반적으로 조화로운 비율로, 성숙하고 안정적인 인상을 줍니다.",
    }

    # 종합 평가 문장 생성
    final_evaluation = evaluation_table.get((faceshape_eval, region_status), "얼굴형 및 비율 정보 기반 평가를 제공하기 어렵습니다.")

    return faceshape_eval, forehead_eval, central_eval, low_eval, final_evaluation