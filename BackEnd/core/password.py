# core/password.py
# 해시 + 솔트 추가 코드
from passlib.context import CryptContext

# bcrypt를 기본 알고리즘으로 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 해시 생성 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 해시 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
