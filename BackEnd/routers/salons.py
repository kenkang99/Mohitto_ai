from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from core.security import get_current_user

router = APIRouter()

class Salon(BaseModel):
    id: int
    name: str
    address: str
    contact: str
    rating: float
    review_count: int

# 미용실 리스트 조회 (스타일 기준)
@router.get("/styles/{id}/salons", response_model=List[Salon])
async def get_salons_by_style(
    style_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Mock data - 실제 구현시 데이터베이스에서 조회
    salons = [
        {
            "id": 1,
            "name": "살롱드파리",
            "address": "서울시 강남구 역삼동 123-45",
            "contact": "02-1234-5678",
            "rating": 4.5,
            "review_count": 128
        },
        {
            "id": 2,
            "name": "헤어스타일",
            "address": "서울시 마포구 서교동 456-78",
            "contact": "02-9876-5432",
            "rating": 4.8,
            "review_count": 256
        }
    ]
    return salons

# 미용실 저장
@router.post("/user/salons")
async def save_user_salon(
    salon_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Mock response - 실제 구현시 데이터베이스에 저장
    return {"success": True} 