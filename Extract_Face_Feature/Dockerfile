# Extract_Face_Feature/Dockerfile
FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
#COPY db_utils.py .
#COPY rds_config.py .
COPY ex_feature/ ./ex_feature/
COPY api_notifier.py .  
# FastAPI에서 알림용 함수로 쓰기 때문

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]