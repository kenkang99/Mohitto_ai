# routers/analyze.py
# CV모델 완료후 실행되는 api: GraphRAG 서버로 데이터 전달

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import requests
from core.database import get_db
from core.recommendation import get_analysis_payload

router = APIRouter()

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
        response = requests.post("http://nano-graphrag:8000/generate", json=payload)
        response.raise_for_status()

        print("[INFO] GraphRAG 응답 수신 성공")
        print(f"[DEBUG] GraphRAG 응답 데이터: {response.json()}")

        return {"message": "추천 성공", "result": response.json()}
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] GraphRAG 요청 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"GraphRAG 호출 실패: {e}")