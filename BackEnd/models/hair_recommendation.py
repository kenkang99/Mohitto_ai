# models/hair_recommendation.py
# 어떤 요청에 대해 어떤 스타일을 추천했는지 기록

from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, Text
from core.database import Base
from datetime import datetime

class HairRecommendation(Base):
    __tablename__ = "hair_recommendation_table"

    hair_rec_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    simulation_image_url = Column(Text, nullable=False)
    hair_name = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    is_saved = Column(Integer, default=0)

    # 외래키 연결
    request_id = Column(BigInteger, ForeignKey("request_table.request_id"), nullable=False)
    hair_id = Column(BigInteger, ForeignKey("hairstyle_table.hair_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)