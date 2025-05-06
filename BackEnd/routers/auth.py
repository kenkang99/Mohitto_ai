from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

# DB 세션 및 사용자 모델 import
from core.database import get_db
from models.user import User

# JWT 기반 사용자 인증 의존성
from core.security import get_current_user

# API 라우터 객체 생성
router = APIRouter()

# JWT 관련 설정값
SECRET_KEY = "your_secret_key"  # 토큰 서명용 키 (배포 시에는 환경변수로 관리 필요)
ALGORITHM = "HS256"             # JWT 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 토큰 유효 시간 (분)

# ─────────────────────────────────────────────
# 데이터 클래스 (Pydantic 기반)
# ─────────────────────────────────────────────

# 회원가입 요청 형식 정의
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str

# 로그인 요청 형식 정의
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 토큰 응답 형식 정의
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ─────────────────────────────────────────────
# 회원가입 API
# ─────────────────────────────────────────────
@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # 이미 등록된 이메일인지 확인
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 이메일입니다."
        )

    # 비밀번호 해싱
    hashed_password = bcrypt.hash(request.password)

    # 새로운 사용자 객체 생성
    new_user = User(
        email=request.email,
        password=hashed_password,
        name=request.nickname
    )

    # DB에 저장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success": True, "user_id": new_user.user_id}

# ─────────────────────────────────────────────
# 로그인 API
# ─────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 사용자를 이메일로 조회
    user = db.query(User).filter(User.email == request.email).first()

    # 사용자 존재 여부 및 비밀번호 확인
    if not user or not bcrypt.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 로그인 정보입니다."
        )

    # JWT 토큰 생성
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.user_id),  # 토큰 식별자
        "exp": expire              # 만료 시간
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# ─────────────────────────────────────────────
# 사용자 프로필 조회 API (JWT 인증 필요)
# ─────────────────────────────────────────────
@router.get("/user/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    # security.py의 get_current_user가 인증된 사용자 정보를 반환
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "nickname": current_user["name"]
    }
