# 간단 요약 생성

from .evaluate import evaluate_feature
from .color_recommend import get_recommendation

def generate_summary(image_path, id, curl, length, dyeing, forehead, clown, mood, care_level):

    # 컴퓨터 추출 정보 불러오기
    faceshape_eval, forehead_eval, central_eval, low_eval, final_evaluation = evaluate_feature(image_path)
    if dyeing == "O":   
       skin_hex, recs = get_recommendation(image_path, mood)
    else:
       skin_hex = "염색 정보 없음"
       recs = []

    result = {
        "id" : id,
        "모발" : curl,
        "길이" : length,
        "염색" : dyeing,
        "피부색" : skin_hex,
        "추천 염색" : recs,
        "이마 모양" : forehead,
        "광대" : clown,
        "기분" : mood,
        "관리 난이도" : care_level,
        "얼굴형": faceshape_eval,
        "이마 평가": forehead_eval,
        "중안부 평가": central_eval,
        "하안부 평가": low_eval,
        "얼굴 분석 총평" : final_evaluation
    }

    # 콘솔에도 출력
    print("\n=== 얼굴 분석 결과 ===")
    for k, v in result.items():
        print(f"{k} : {v}")
    return result