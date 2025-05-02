from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt  # 해싱 라이브러리

from core.security import get_current_user

router = APIRouter()

# 모의 사용자 저장소
mock_users = [
    {
        "user_id": 1,
        "name": "홍길동",
        "email": "test@example.com",
        "password": bcrypt.hash("password123"),  # 해시 + 솔트 된 비밀번호
        "created_at": "2024-12-01 12:00:00"
    }
]

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 요청 바디 클래스
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# /signup
@router.post("/signup")
def signup(request: SignupRequest):
    for user in mock_users:
        if user["email"] == request.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 가입된 이메일입니다."
            )

    hashed_password = bcrypt.hash(request.password)

    new_user = {
        "user_id": len(mock_users) + 1,
        "name": request.nickname,
        "email": request.email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    mock_users.append(new_user)

    return {"success": True, "user_id": new_user["user_id"]}

# /login
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = next((u for u in mock_users if u["email"] == request.email), None)

    if not user or not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 로그인 정보입니다."
        )

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user["user_id"]),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# /user/profile
@router.get("/user/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "nickname": current_user["name"]
    }