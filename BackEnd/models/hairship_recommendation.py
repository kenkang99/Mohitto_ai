# models/hairshop_recommendation.py
# 어떤 추천 결과에 대해 어떤 미용실을 추천했는지 저장

from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from core.database import Base
from datetime import datetime

class HairshopRecommendation(Base):
    __tablename__ = "hairshop_recommendation_table"

    hairshop_rec_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_saved = Column(Boolean, default=False)

    hairshop_id = Column(BigInteger, ForeignKey("hairshop_table.hairshop_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    hair_rec_id = Column(BigInteger, ForeignKey("hair_recommendation_table.hair_rec_id"), nullable=False)
