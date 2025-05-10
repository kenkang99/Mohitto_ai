# nano-graphrag

## 개요
머리스타일 추천을 위한 간단한 GraphRAG 기반 질의 시스템.

---

## ✅ 실행 방법

1. **폴더 이동**
    ```bash
    cd nano-graphrag
    ```

2. **필요 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

3. **머리스타일 추천 실행**
    ```bash
    python -m nano_graphrag.main --query "나는 둥근형 얼굴이고, 직모에 굵은 모발을 가졌으며, 관리 난이도 쉬운 남성 스타일을 추천해줘."
    ```

---

## ✅ 환경 설정 (필수)
- `.env` 파일을 생성해 OpenAI API 키를 설정해야 합니다.
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

---

## ✅ 의존성
- `requirements.txt` 참고

---

## ✅ 라이선스
MIT License