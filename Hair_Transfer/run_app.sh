# 가상환경 생성
#rm -rf stable_hair_venv
python3 -m venv stable_hair_venv
source stable_hair_venv/bin/activate

# 1) pip / 빌드 도구 업그레이드
python -m pip install --upgrade pip

# 2) 필수 패키지 설치
pip install -r requirements.txt

# 3) 애플리케이션 실행
python main.py