import openai
import os
import json
import re

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 헤어스타일 사전
HAIR_STYLE_DICT = {
    "남성": {
        "단일_스타일": [
            "포마드컷", "리젠트컷", "리젠트펌", "아이비리그컷", "스왓컷", "크롭컷", "바버컷", "모히칸컷",
            "시스루댄디컷", "슬릭댄디컷", "슬릭백언더컷", "가일컷", "슬릭가일컷", "투블럭컷", "댄디펌", 
            "애즈펌", "슬릭애즈펌", "가일펌", "쉐도우펌", "스핀스왈로펌", "프링펌", "아이롱펌", "샤기컷", 
            "장발", "리프컷", "울프컷", "히피펌", "빈티지펌"
        ]
    },
    "여성": {
        "단일_스타일": [
            "글래펌", "샤밍컷", "베베컷", "빈티지펌", "웨이브펌", "테슬펌", "엘리자베스펌", "그레이스펌", 
            "구름펌", "테슬컷", "슬릭컷", "페이지컷", "샌드펌", "허쉬펌", "레이어드펌", "슬릭펌", "빌드펌", 
            "허그펌", "블럭컷", "바디펌", "S컬펌", "히메컷", "뱅헤어", "물결펌", "플라워펌", "리프컷", 
            "샤기컷", "숏컷", "히피펌", "젤리펌", "C컬펌", "허쉬컷", "레이어드컷", "발레아쥬"
        ],
        "조합_스타일": [
            "태슬펌_태슬컷", "C컬펌_레이어드컷", "허그펌_레이어드컷", "웨이브펌_레이어드컷", 
            "빈티지펌_레이어드컷", "S컬펌_레이어드컷", "그레이스펌_레이어드컷", "엘리자벳펌_레이어드컷", 
            "빌드펌_레이어드컷", "샌드펌_레이어드컷", "블럭컷", "C컬펌_허쉬컷", "웨이브펌_일자컷", 
            "글램펌_레이어드컷", "히피펌_샤기컷", "히피펌_레이어드컷", "구름펌_레이어드컷", 
            "슬릭펌_슬릭컷", "C컬펌_일자컷", "허쉬펌_허쉬컷"
        ]
    }
}

SYSTEM_PROMPT = """당신은 전문 헤어스타일리스트입니다.
다음 1차 추천과 스타일 사전만을 사용하여 추천합니다.
사전 외 항목은 절대 사용하지 마세요.
"""

USER_PROMPT_TEMPLATE = """1) 아래는 1차 생성 결과입니다.
{first_response}

2) 아래는 추천에 사용할 헤어스타일 사전입니다.
{style_dict}

3) 위 사전 내에서만 추천해주세요.
   - **단일 스타일 1~2개 + 조합 스타일 1~2개** 를 골고루 추천해주세요. (최대 4개, 더 적게 해도 괜찮으며, 적절한 설명이 가능한 것만 추천해주세요.)
   - 1차 생성결과를 반영하여 가장 적절할 것 같은 스타일을 추천해주세요.
   - 각 추천 뒤에 "이 스타일이 어울리는 이유"를 1차 생성 결과를 최대한 활용하여 생성하세요.(사용자의 입력도 최대한 활용하세요.)

출력 형식 (JSON으로 출력해주세요):
{{
  "recommendations": [
    {{
      "style": "스타일명",
      "description": "추천 이유 설명"
    }}
  ]
}}

> **주의:** 절대 사전 외 항목을 생성, 변형, 언급하지 마세요.
"""

def format_style_dict(sex):
    """성별에 따른 스타일 사전을 문자열로 포맷"""
    if sex == "남성":
        return f"- 남성 단일 스타일: {', '.join(HAIR_STYLE_DICT['남성']['단일_스타일'])}"
    else:
        single_styles = ', '.join(HAIR_STYLE_DICT['여성']['단일_스타일'])
        combo_styles = ', '.join(HAIR_STYLE_DICT['여성']['조합_스타일'])
        return f"- 여성 단일 스타일: {single_styles}\n- 조합 스타일: {combo_styles}"

def call_gpt4o(system_prompt, user_prompt):
    """GPT-4o 호출"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def extract_json_from_response(response_text):
    """응답에서 JSON 추출"""
    try:
        # JSON 블록 찾기
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 중괄호로 둘러싸인 JSON 찾기
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text
        
        return json.loads(json_str)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 기본 구조로 변환 시도
        return {"recommendations": [{"style": "파싱 실패", "description": response_text}]}

def get_final_recommendations(first_response, user_sex):
    """2차 최종 헤어스타일 추천"""
    style_dict_str = format_style_dict(user_sex)
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        first_response=first_response,
        style_dict=style_dict_str
    )
    
    print("=== 2차 최종 추천 호출 ===")
    response_text = call_gpt4o(SYSTEM_PROMPT, user_prompt)
    print("Raw Response:", response_text)
    
    # JSON 추출 및 파싱
    final_recommendations = extract_json_from_response(response_text)
    
    return final_recommendations