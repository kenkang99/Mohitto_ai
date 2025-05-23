# routers/analyze.py
# 컨테이너간 통신

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import requests

from models.hair_recommendation import HairRecommendation
from models.hairshop_recommendation import HairshopRecommendation
from core.database import get_db
from core.recommendation import get_analysis_payload
from schemas.recommendation import RecommendationPayload

router = APIRouter()

# 1. 기존: Main → GraphRAG 요청
@router.post("/run-recommendation/")
def run_recommendation(
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    user_id = data.get("user_id")
    request_id = data.get("request_id")

    print(f"[DEBUG] 요청 수신됨 - user_id: {user_id}, request_id: {request_id}")

    if not user_id or not request_id:
        print("[ERROR] user_id 또는 request_id가 없음")
        raise HTTPException(status_code=400, detail="user_id 또는 request_id가 누락되었습니다.")

    # payload 구성
    payload = get_analysis_payload(db, user_id, request_id)
    if not payload:
        print("[ERROR] get_analysis_payload 실패 - 데이터 없음")
        raise HTTPException(status_code=404, detail="요청 또는 분석 결과가 없습니다.")

    print(f"[INFO] payload 준비 완료 → GraphRAG 전송 시작\n{payload}")

    try:
        response = requests.post("http://nano-graphrag:8002/recommend", json=payload)
        response.raise_for_status()

        print("[INFO] GraphRAG 응답 수신 성공")
        print(f"[DEBUG] GraphRAG 응답 데이터: {response.json()}")

        return {"message": "추천 성공", "result": response.json()}
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] GraphRAG 요청 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"GraphRAG 호출 실패: {e}")
    
# 2. GraphRAG → Main 추천 결과 저장
@router.post("/save-recommendation/")
def save_recommendation(payload: RecommendationPayload, db: Session = Depends(get_db)):
    user_id = int(payload.user_info["user_id"])
    request_id = int(payload.user_info["request_id"])

    for rec in payload.recommendations:
        hair_rec = HairRecommendation(
            simulation_image_url="dummy.jpg",  # 추후 얼굴 시뮬레이션 이미지로 교체
            hair_name=rec.style,
            description=rec.description,
            is_saved=0,
            request_id=request_id,
            hair_id=1,  # TODO: style 이름 기반 hair_id 매핑 로직 필요
            user_id=user_id
        )
        db.add(hair_rec)
        db.flush()

        for shop in rec.hair_shops:
            # db.add(HairshopRecommendation(
            #     hairshop=shop.hairshop,
            #     is_saved=0,
            #     latitude=shop.latitude,
            #     longitude=shop.longitude,
            #     final_menu_price=shop.final_menu_price,
            #     review_count=shop.review_count,
            #     mean_score=shop.mean_score,
            #     hair_rec_id=hair_rec.hair_rec_id,
            #     user_id=user_id
            # ))
            db.add(HairshopRecommendation(
                hairshop=shop.hairshop or "미정",
                is_saved=0,
                latitude=shop.latitude or 0.0,
                longitude=shop.longitude or 0.0,
                final_menu_price=shop.final_menu_price or 0,
                review_count=shop.review_count or 0,
                mean_score=shop.mean_score or 0.0,
                hair_rec_id=hair_rec.hair_rec_id,
                user_id=user_id
            ))

    db.commit()
    print(f"[INFO] user_id={user_id}, request_id={request_id} 추천 결과 DB 저장 완료")
    return {"message": "추천 결과 DB 저장 완료"}