# routers/salons.py
# 스타일 기반 미용실 추천 조회, 미용실 추천 저장 기록

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from core.security import get_current_user

router = APIRouter()

# 응답 모델 
class Hairshop(BaseModel):
    hairshop_id: int
    hairshop_name: str
    address: str
    menu: Optional[str]
    phone: Optional[str]
    intro: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]

# 스타일별 미용실 추천
@router.get("/styles/{style_id}/salons", response_model=List[Hairshop])
async def get_salons_by_style(
    style_id: int,
    current_user: dict = Depends(get_current_user)
):
    salons = [
        {
            "hairshop_id": 1,
            "hairshop_name": "살롱드파리",
            "address": "서울시 강남구",
            "menu": "컷 15000원",
            "phone": "02-1234-5678",
            "intro": "고급 헤어살롱",
            "latitude": "37.4980",
            "longitude": "127.0276"
        },
        {
            "hairshop_id": 2,
            "hairshop_name": "이철헤어커커",
            "address": "서울시 마포구",
            "menu": "컷 17000원",
            "phone": "02-9876-5432",
            "intro": "세련된 디자인 전문",
            "latitude": "37.5500",
            "longitude": "126.9100"
        }
    ]
    return salons

# 사용자의 추천 미용실 저장 기록 (hairshop_recommendation_table 대응)
@router.post("/user/salons")
async def save_user_salon(
    salon_id: int,
    current_user: dict = Depends(get_current_user)
):
    # 실제 저장 시: user_id, hairshop_id, hair_rec_id, is_saved, created_at 등 저장 필요
    return {
        "success": True,
        "saved_at": datetime.utcnow().isoformat(),
        "user_id": current_user["user_id"],
        "hairshop_id": salon_id
    }
