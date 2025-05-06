# routers/styles.py
# 사용자의 스타일 조회, 시뮬레이션, 추천 저장
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from core.security import get_current_user

router = APIRouter()

# 응답 모델 정의 (ERD 기준에 맞춤)
class Hairstyle(BaseModel):
    hair_id: int
    hairstyle_name: str
    hairstyle_image_url: str
    hairstyle_explanation: Optional[str] = None

class SimulationResponse(BaseModel):
    image_url: str
    success: bool

# 스타일 리스트 조회
@router.get("/styles", response_model=List[Hairstyle])
async def get_styles(
    search: Optional[str] = None,
    sort: Optional[str] = None
):
    styles = [
        {
            "hair_id": 1,
            "hairstyle_name": "댄디컷",
            "hairstyle_image_url": "https://example.com/styles/dandy.jpg",
            "hairstyle_explanation": "깔끔하고 단정한 스타일"
        },
        {
            "hair_id": 2,
            "hairstyle_name": "리프컷",
            "hairstyle_image_url": "https://example.com/styles/leaf.jpg",
            "hairstyle_explanation": "자연스러운 층낸 스타일"
        }
    ]

    # 검색 필터링
    if search:
        styles = [s for s in styles if search.lower() in s["hairstyle_name"].lower()]

    # 정렬 옵션 적용
    if sort == "latest":
        styles.reverse()
    elif sort == "name":
        styles.sort(key=lambda x: x["hairstyle_name"])

    return styles

# 스타일 시뮬레이션 (특정 스타일 ID)
@router.get("/styles/{style_id}/simulate", response_model=SimulationResponse)
async def simulate_style(
    style_id: int,
    current_user: dict = Depends(get_current_user)
):
    # 추후 실제 모델 연동
    return {
        "image_url": f"https://example.com/simulations/user_{current_user['user_id']}_style_{style_id}.jpg",
        "success": True
    }

# 스타일 시뮬레이션 (이미지 업로드 기반 추천)
@router.post("/simulate-hairstyle")
async def simulate_hairstyle(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # 향후 YOLO, 얼굴형 분석 기반 추천 모델 연동 필요
    return {
        "success": True,
        "image_url": "https://example.com/simulations/result.jpg",
        "style_list": [
            {
                "hair_id": 1,
                "hairstyle_name": "댄디컷",
                "confidence": 0.95
            },
            {
                "hair_id": 2,
                "hairstyle_name": "리프컷",
                "confidence": 0.85
            }
        ]
    }

# 추천 스타일 저장 (hair_recommendation_table에 해당)
@router.post("/user/hairstyles")
async def save_user_hairstyle(
    hairstyle_id: int,
    current_user: dict = Depends(get_current_user)
):
    # 실제 구현 시 DB에 저장 필요
    # 저장 필드: user_id, hair_id, is_saved, created_at, request_id (외래키로 연결)
    return {
        "success": True,
        "saved_at": datetime.utcnow().isoformat(),
        "user_id": current_user["user_id"],
        "hair_id": hairstyle_id
    }
