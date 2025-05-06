# evaluate.py
import cv2
import json
from .facemesh import extract_facial_ratios
from .extract_faceshape import predict_faceshape
from .stone_classifier import extract_face_colors
from .extract_face_feature import extract_feature

def evaluate_feature(image_path):

    # 이미지 정보 추출
    faceshape, top_ratio, mid_ratio, down_ratio, skin_tone = extract_feature(image_path)

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

    return faceshape_eval, skin_tone, forehead_eval, central_eval, low_eval
