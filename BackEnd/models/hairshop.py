# models/hairshop.py
# 미용실 기본 정보

from sqlalchemy import Column, BigInteger, String, Text
from core.database import Base

class Hairshop(Base):
    __tablename__ = "hairshop_table"

    hairshop_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    hairshop_name = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    menu = Column(Text)
    phone = Column(String(20))
    intro = Column(Text)
    latitude = Column(String(30))
    longitude = Column(String(30))
