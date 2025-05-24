
import cv2
from .facemesh import extract_facial_ratios
from .extract_faceshape import predict_faceshape

def extract_feature(image):
    #image = cv2.imread(image)
    if image is None:
        print(f"[ERROR] 이미지 로드 실패")
        return {"error": "이미지 로드 실패"}

    # 얼굴형, 피부색, 비율 추출
    faceshape = predict_faceshape(image)
    top_ratio, mid_ratio, down_ratio = extract_facial_ratios(image)

    return faceshape, top_ratio, mid_ratio, down_ratio
