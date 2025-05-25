from sqlalchemy.orm import Session
from models.request import Request
from models.result import Result

def get_analysis_payload(db: Session, user_id: int, request_id: int):
    print(f"[DEBUG] 분석 시작 - user_id: {user_id}, request_id: {request_id}")

    # 1. 요청 정보 (설문 결과)
    request_info = db.query(Request).filter_by(user_id=user_id, request_id=request_id).first()
    print(f"[DEBUG] request_info 조회 결과: {request_info}")

    # 2. 얼굴 분석 결과
    result_info = db.query(Result).filter_by(request_id=request_id).first()
    print(f"[DEBUG] result_info 조회 결과: {result_info}")

    if not request_info or not result_info:
        print("[ERROR] request_info 또는 result_info가 존재하지 않습니다.")
        return None

    print("[INFO] DB에서 request/result 정보 모두 정상 조회됨")

    mood = request_info.mood
    if isinstance(mood, list):
        mood = ", ".join(mood)
    
    return {
        "user_id": str(user_id),
        "request_id": request_id,

        # 사용자 입력 정보
        "hair_length": request_info.hair_length,
        "hair_type": request_info.hair_type,
        "sex": request_info.sex,
        "cheekbone": request_info.cheekbone,
        "mood": mood,
        "forehead_shape": request_info.forehead_shape,
        "difficulty": request_info.difficulty,
        "has_bangs": request_info.has_bangs,
        "face_shape": result_info.face_type,

        # 얼굴 분석 정보
        # "face_shape": result_info.face_type,
        # "skin_tone": result_info.skin_tone,
        # "forehead": result_info.forehead,
        "summary": result_info.summary
    }
