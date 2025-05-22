# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user, styles, salons
from routers.analyze import router as analyze_router
from core.database import engine, Base, get_db
from sqlalchemy import text

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",
    "http://localhost:19006",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:19006",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",
    "exp://localhost:19000",
    "exp://127.0.0.1:19000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 루트 경로 추가
@app.get("/")
def root():
    return {"message": "FastAPI 서버가 정상 작동 중입니다."}

# 데이터베이스 연결 테스트 엔드포인트
@app.get("/test-db")
def test_db(db = Depends(get_db)):
    try:
        # 간단한 쿼리 실행
        result = db.execute(text("SELECT 1"))
        return {"message": "데이터베이스 연결 성공!", "result": result.scalar()}
    except Exception as e:
        return {"message": "데이터베이스 연결 실패", "error": str(e)}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(styles.router)
app.include_router(salons.router)
app.include_router(analyze_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)