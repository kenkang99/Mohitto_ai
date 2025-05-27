# models/hairstyle.py
# 추천할 수 있는 헤어스타일 목록 저장

from sqlalchemy import Column, BigInteger, String, Text
from core.database import Base

class Hairstyle(Base):
    __tablename__ = "hairstyle_table"

    hair_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    hairstyle_name = Column(String(20), nullable=False)
    hairstyle_image_url = Column(Text, nullable=False)
    # hairstyle_explanation = Column(Text)
    
    hairstyle_sex = Column(String(10), nullable=False)
    hairstyle_type = Column(String(10))
    hairstyle_face = Column(String(5))
    hairstyle_length = Column(String(5))
    hairstyle_color = Column(String(20), default="Black")