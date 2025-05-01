from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from core.security import get_current_user

router = APIRouter()

class Style(BaseModel):
    id: int
    name: str
    image_url: str
    short_description: Optional[str] = None

class SimulationResponse(BaseModel):
    image_url: str
    success: bool

# 스타일 리스트 조회
@router.get("/styles", response_model=List[Style])
async def get_styles(
    search: Optional[str] = None,
    sort: Optional[str] = None
):
    # Mock data - 실제 구현시 데이터베이스에서 조회
    styles = [
        {
            "id": 1,
            "name": "댄디컷",
            "image_url": "https://example.com/styles/dandy.jpg",
            "short_description": "깔끔하고 단정한 스타일"
        },
        {
            "id": 2,
            "name": "리프컷",
            "image_url": "https://example.com/styles/leaf.jpg",
            "short_description": "자연스러운 층낸 스타일"
        }
    ]
    
    # 검색어 필터링
    if search:
        styles = [s for s in styles if search.lower() in s["name"].lower()]
    
    # 정렬
    if sort == "latest":
        styles.reverse()
    elif sort == "name":
        styles.sort(key=lambda x: x["name"])
        
    return styles

# 스타일 시뮬레이션
@router.get("/styles/{id}/simulate")
async def simulate_style(
    style_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Mock response - 실제 구현시 AI 모델을 통한 시뮬레이션 수행
    return {
        "image_url": f"https://example.com/simulations/user_{current_user['id']}_style_{style_id}.jpg",
        "success": True
    }

# 스타일 시뮬레이션 (이미지 업로드)
@router.post("/simulate-hairstyle")
async def simulate_hairstyle(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # 이미지 처리 로직 구현 필요
    return {
        "success": True,
        "image_url": "https://example.com/simulations/result.jpg",
        "style_list": [
            {
                "id": 1,
                "name": "댄디컷",
                "confidence": 0.95
            },
            {
                "id": 2,
                "name": "리프컷",
                "confidence": 0.85
            }
        ]
    }

# 추천 스타일 저장
@router.post("/user/hairstyles")
async def save_user_hairstyle(
    hairstyle_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Mock response - 실제 구현시 데이터베이스에 저장
    return {"success": True} 