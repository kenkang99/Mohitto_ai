# models/result.py
# 얼굴형, 피부톤 등 분석 결과 저장

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from core.database import Base
from datetime import datetime

class Result(Base):
    __tablename__ = "result_table"

    result_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    face_type = Column(String(20), nullable=False)
    skin_tone = Column(String(20), nullable=False)
    forehead = Column(String(20), nullable=False)
    sex = Column(String(20), nullable=False)
    top_rate = Column(String(50))           
    middle_rate = Column(String(50))       
    bottom_rate = Column(String(50))       
    rec_color = Column(String(255))         
    summary = Column(String(255))           
    created_at = Column(DateTime, default=datetime.utcnow)

    # 외래키: 요청 ID
    request_id = Column(BigInteger, ForeignKey("request_table.request_id"), nullable=False)
