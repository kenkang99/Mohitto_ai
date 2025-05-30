# 가상환경이 없으면 생성
rm -rf graphrag_venv
python3 -m venv graphrag_venv
source graphrag_venv/bin/activate

# 1) pip / 빌드 도구 업그레이드
python -m pip install --upgrade pip 

# 2) 필수 패키지 설치
pip install -r requirements.txt

# 3) 애플리케이션 실행
#python main.py
uvicorn main:app --host 127.0.0.1 --port 8002