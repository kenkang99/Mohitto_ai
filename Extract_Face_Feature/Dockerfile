FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY db_utils.py .
COPY rds_config.py .
COPY ex_feature/ ./ex_feature/

CMD ["python", "main.py", "1", "1"] 
# 지금은 1,1 로 강제
# ENTRYPOINT ["python", "main.py"] # 추후 api로 전달되면 수정