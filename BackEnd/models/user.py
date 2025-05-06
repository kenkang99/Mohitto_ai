# models/user.py
# AWS RDS의 user_table을 사용할 수 있도록 SQLAlchemy로 정의한 데이터 모델

from sqlalchemy import Column, BigInteger, String, DateTime, Text
from core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user_table"

    user_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt 해시 저장
    created_at = Column(DateTime, default=datetime.utcnow)
