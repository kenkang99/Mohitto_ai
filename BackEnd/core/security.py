# core/security.py
# 보안 관련(JWT) 파일

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 인증 방식 (Bearer 토큰)
security = HTTPBearer()

# 토큰 디코딩 함수
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

# 사용자 인증 의존성
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = int(payload["sub"])

    # mock 사용자 탐색
    from routers.auth import mock_users
    user = next((u for u in mock_users if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return user
