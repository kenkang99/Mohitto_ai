# schemas/recommendation.py
# 요청(request) 본문을 받을 때 자동으로 구조를 검사하고 유효성 검증(validation) 합니다.

from pydantic import BaseModel
from typing import List, Optional

class HairshopInfo(BaseModel):
    hairshop: str
    latitude: float
    longitude: float
    final_menu_price: Optional[int]
    review_count: int
    mean_score: float

class RecommendationItem(BaseModel):
    style: str
    description: str
    hair_shops: List[HairshopInfo]

class UserInfo(BaseModel):
    user_id: int
    request_id: int

class RecommendationPayload(BaseModel):
    user_info: UserInfo
    recommendations: List[RecommendationItem]

# class RecommendationPayload(BaseModel):
#     user_info: dict  # {"user_id": ..., "request_id": ...}
#     recommendations: List[RecommendationItem]