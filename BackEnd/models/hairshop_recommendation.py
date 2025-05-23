# models/hairshop_recommendation.py
# 어떤 추천 결과에 대해 어떤 미용실을 추천했는지 저장

from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Integer, Float, Text
from core.database import Base
from datetime import datetime

class HairshopRecommendation(Base):
    __tablename__ = "hairshop_recommendation_table"

    hairshop_rec_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    hairshop = Column(Text, nullable=False)
    is_saved = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    final_menu_price = Column(Integer)
    review_count = Column(Integer)
    mean_score = Column(Float)

    hair_rec_id = Column(BigInteger, ForeignKey("hair_recommendation_table.hair_rec_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
