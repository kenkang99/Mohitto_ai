# routers/auth.py
# /singup, /login, /user/profile
# 회원가입/로그인 관련 API

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta

from core.security import get_current_user

router = APIRouter()

# 모의 사용자 저장소
mock_users = [
    {
        "id": 1,
        "email": "test@example.com",
        "password": "password123",
        "nickname": "테스트유저"
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
    # 이메일 중복 여부 확인
    for user in mock_users:
        if user["email"] == request.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 가입된 이메일입니다."
            )

    # 새로운 사용자 추가
    new_user = {
        "id": len(mock_users) + 1,
        "email": request.email,
        "password": request.password,
        "nickname": request.nickname
    }
    mock_users.append(new_user)

    return {"success": True, "user_id": new_user["id"]}

# /login
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = next(
        (u for u in mock_users if u["email"] == request.email and u["password"] == request.password),
        None
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 로그인 정보입니다."
        )

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user["id"]),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# /user/profile
@router.get("/user/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "nickname": current_user["nickname"]
    }