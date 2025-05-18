# main.py
from fastapi import FastAPI, Depends
from routers import auth, user, styles, salons
from routers.analyze import router as analyze_router
from core.database import engine, Base, get_db
from sqlalchemy import text

app = FastAPI()

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