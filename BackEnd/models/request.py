# models/request.py
# 사용자 설문 + 이미지 분석 요청 저장

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from core.database import Base
from datetime import datetime

class Request(Base):
    __tablename__ = "request_table"

    request_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_image_url = Column(Text, nullable=False)
    hair_length = Column(String(20), nullable=False)
    hair_type = Column(String(20), nullable=False)
    sex = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)
    cheekbone = Column(String(20), nullable=False)
    mood = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 외래키: 사용자 ID
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
