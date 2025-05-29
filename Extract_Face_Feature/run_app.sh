# 처음 run_app.sh 실행하는 거면 아래 두 주석 해제하고 진행해야함
#rm -rf face_feature_venv
#python3 -m venv face_feature_venv
source face_feature_venv/bin/activate

# 1) pip / 빌드 도구 업그레이드
python -m pip install --upgrade pip 

# 2) 필수 패키지 설치
pip install -r requirements.txt

# 3) 애플리케이션 실행
# python main.py
uvicorn main:app --host 127.0.0.1 --port 8000 # 이거 실행 안될 시 위에껄로 해보셈