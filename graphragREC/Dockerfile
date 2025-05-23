# graphragREC/Dockerfile
FROM python:3.10

WORKDIR /app

# 시스템 의존성 (필요 시만 사용)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 코드 복사
COPY . .

# FastAPI 앱 실행 (내부 포트는 8002로 맞춰둠)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]