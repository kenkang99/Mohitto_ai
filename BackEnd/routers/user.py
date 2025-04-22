# /routers/user.py
# /user/hairstyles, /user/hairshops, /analyze-face
# 사용자 관련 API: 헤어스타일, 미용실 조회 및 얼굴 분석

from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

router = APIRouter()

# JWT 설정
SECRET_KEY = "secret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 사용자 정보 디코딩 유틸 함수
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="사용자 ID가 없습니다.")
        return {"id": user_id, "nickname": "테스트유저"}
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

# 응답 모델 정의
class Style(BaseModel):
    id: int
    name: str
    image_url: str

class Hairshop(BaseModel):
    id: int
    name: str
    address: str
    link: str
    
class RecommendedStyle(BaseModel):
    id: int
    name: str
    image_url: str
    description: str

# /user/hairstyles
@router.get("/user/hairstyles", response_model=list[Style])
def get_user_styles(current_user: dict = Depends(get_current_user)):
    return [
        {"id": 1, "name": "가일컷", "image_url": "https://example.com/style1.jpg"},
        {"id": 2, "name": "댄디컷", "image_url": "https://example.com/style2.jpg"}
    ]

# /user/hairshops
@router.get("/user/hairshops", response_model=list[Hairshop])
def get_user_hairshops(current_user: dict = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "name": "살롱드헤어 신촌점",
            "address": "서울특별시 마포구 신촌로 45",
            "link": "https://hairshop.example.com/shop1"
        },
        {
            "id": 2,
            "name": "이철헤어커커 강남점",
            "address": "서울특별시 강남구 테헤란로 101",
            "link": "https://hairshop.example.com/shop2"
        }
    ]

# /analyze-face
@router.post("/analyze-face")
def analyze_face(
    gender: str = Form(...),
    hair_condition: str = Form(...),
    length: str = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "얼굴 분석이 완료되었습니다.",
        "user_id": current_user["id"],
        "survey": {
            "gender": gender,
            "hair_condition": hair_condition,
            "length": length
        },
        "image_filename": image.filename
    }
    
# /recommend/styles
@router.get("/recommend/styles", response_model=list[RecommendedStyle])
def recommend_styles(current_user: dict = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "name": "리프컷",
            "image_url": "https://example.com/styles/leafcut.jpg",
            "description": "부드럽고 자연스러운 느낌을 주는 스타일입니다."
        },
        {
            "id": 2,
            "name": "댄디컷",
            "image_url": "https://example.com/styles/dandycut.jpg",
            "description": "깔끔하고 단정한 인상을 주는 베스트셀러 스타일입니다."
        },
        {
            "id": 3,
            "name": "쉐도우펌",
            "image_url": "https://example.com/styles/shadowperm.jpg",
            "description": "볼륨감 있게 연출되어 얼굴형 보완에 효과적입니다."
        }
    ]