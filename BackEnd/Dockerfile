# 베이스 이미지 선택
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# 로컬 파일을 컨테이너에 복사
COPY . .

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
