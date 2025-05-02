# routers/user.py
# 사용자 관련 API: 스타일 추천, 미용실 추천, 얼굴 분석 요청

from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from core.security import get_current_user  # 공통 인증 모듈 사용

router = APIRouter()

# 응답 모델 정의 (ERD 기준 필드명 반영)
class Style(BaseModel):
    hair_id: int
    hairstyle_name: str
    hairstyle_image_url: str

class Hairshop(BaseModel):
    hairshop_id: int
    hairshop_name: str
    address: str
    link: str

class RecommendedStyle(BaseModel):
    hair_id: int
    hairstyle_name: str
    hairstyle_image_url: str
    description: str

# 사용자별 추천 스타일 조회
@router.get("/user/hairstyles", response_model=List[Style])
def get_user_styles(current_user: dict = Depends(get_current_user)):
    return [
        {
            "hair_id": 1,
            "hairstyle_name": "가일컷",
            "hairstyle_image_url": "https://example.com/style1.jpg"
        },
        {
            "hair_id": 2,
            "hairstyle_name": "댄디컷",
            "hairstyle_image_url": "https://example.com/style2.jpg"
        }
    ]

# 사용자별 추천 미용실 조회
@router.get("/user/hairshops", response_model=List[Hairshop])
def get_user_hairshops(current_user: dict = Depends(get_current_user)):
    return [
        {
            "hairshop_id": 1,
            "hairshop_name": "살롱드헤어 신촌점",
            "address": "서울특별시 마포구 신촌로 45",
            "link": "https://hairshop.example.com/shop1"
        },
        {
            "hairshop_id": 2,
            "hairshop_name": "이철헤어커커 강남점",
            "address": "서울특별시 강남구 테헤란로 101",
            "link": "https://hairshop.example.com/shop2"
        }
    ]

# 얼굴 분석 요청 (설문 + 이미지)
@router.post("/analyze-face")
def analyze_face(
    gender: str = Form(...),
    hair_condition: str = Form(...),
    length: str = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # 실제 구현 시 request_table + result_table에 저장 필요
    return {
        "message": "얼굴 분석이 완료되었습니다.",
        "user_id": current_user["user_id"],
        "survey": {
            "gender": gender,
            "hair_condition": hair_condition,
            "length": length
        },
        "image_filename": image.filename
    }

# 추천 스타일 리스트 조회 (mock)
@router.get("/recommend/styles", response_model=List[RecommendedStyle])
def recommend_styles(current_user: dict = Depends(get_current_user)):
    return [
        {
            "hair_id": 1,
            "hairstyle_name": "리프컷",
            "hairstyle_image_url": "https://example.com/styles/leafcut.jpg",
            "description": "부드럽고 자연스러운 느낌을 주는 스타일입니다."
        },
        {
            "hair_id": 2,
            "hairstyle_name": "댄디컷",
            "hairstyle_image_url": "https://example.com/styles/dandycut.jpg",
            "description": "깔끔하고 단정한 인상을 주는 베스트셀러 스타일입니다."
        },
        {
            "hair_id": 3,
            "hairstyle_name": "쉐도우펌",
            "hairstyle_image_url": "https://example.com/styles/shadowperm.jpg",
            "description": "볼륨감 있게 연출되어 얼굴형 보완에 효과적입니다."
        }
    ]
