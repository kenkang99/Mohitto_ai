# main.py

from fastapi import FastAPI
from routers import auth, user

app = FastAPI()

# 루트 경로 추가
@app.get("/")
def root():
    return {"message": "FastAPI 서버가 정상 작동 중입니다."}

app.include_router(auth.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
