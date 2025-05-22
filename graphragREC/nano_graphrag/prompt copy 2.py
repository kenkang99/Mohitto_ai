"""
Reference:
 - Prompts are from [graphrag](https://github.com/microsoft/graphrag)
"""

GRAPH_FIELD_SEP = "<SEP>"
PROMPTS = {}

PROMPTS[
    "claim_extraction"
] = """-Target activity-
You are an intelligent assistant that helps a human analyst to analyze claims against certain entities presented in a text document.

-Goal-
Given a text document that is potentially relevant to this activity, an entity specification, and a claim description, extract all entities that match the entity specification and all claims against those entities.

-Steps-
1. Extract all named entities that match the predefined entity specification. Entity specification can either be a list of entity names or a list of entity types.
2. For each entity identified in step 1, extract all claims associated with the entity. Claims need to match the specified claim description, and the entity should be the subject of the claim.
For each claim, extract the following information:
- Subject: name of the entity that is subject of the claim, capitalized. The subject entity is one that committed the action described in the claim. Subject needs to be one of the named entities identified in step 1.
- Object: name of the entity that is object of the claim, capitalized. The object entity is one that either reports/handles or is affected by the action described in the claim. If object entity is unknown, use **NONE**.
- Claim Type: overall category of the claim, capitalized. Name it in a way that can be repeated across multiple text inputs, so that similar claims share the same claim type
- Claim Status: **TRUE**, **FALSE**, or **SUSPECTED**. TRUE means the claim is confirmed, FALSE means the claim is found to be False, SUSPECTED means the claim is not verified.
- Claim Description: Detailed description explaining the reasoning behind the claim, together with all the related evidence and references.
- Claim Date: Period (start_date, end_date) when the claim was made. Both start_date and end_date should be in ISO-8601 format. If the claim was made on a single date rather than a date range, set the same date for both start_date and end_date. If date is unknown, return **NONE**.
- Claim Source Text: List of **all** quotes from the original text that are relevant to the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. Return output in English as a single list of all the claims identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

4. When finished, output {completion_delimiter}

-Examples-
Example 1:
Entity specification: organization
Claim description: red flags associated with an entity
Text: According to an article on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B. The company is owned by Person C who was suspected of engaging in corruption activities in 2015.
Output:

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}Company A was found to engage in anti-competitive practices because it was fined for bid rigging in multiple public tenders published by Government Agency B according to an article published on 2022/01/10{tuple_delimiter}According to an article published on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B.)
{completion_delimiter}

Example 2:
Entity specification: Company A, Person C
Claim description: red flags associated with an entity
Text: According to an article on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B. The company is owned by Person C who was suspected of engaging in corruption activities in 2015.
Output:

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}Company A was found to engage in anti-competitive practices because it was fined for bid rigging in multiple public tenders published by Government Agency B according to an article published on 2022/01/10{tuple_delimiter}According to an article published on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B.)
{record_delimiter}
(PERSON C{tuple_delimiter}NONE{tuple_delimiter}CORRUPTION{tuple_delimiter}SUSPECTED{tuple_delimiter}2015-01-01T00:00:00{tuple_delimiter}2015-12-30T00:00:00{tuple_delimiter}Person C was suspected of engaging in corruption activities in 2015{tuple_delimiter}The company is owned by Person C who was suspected of engaging in corruption activities in 2015)
{completion_delimiter}

-Real Data-
Use the following input for your answer.
Entity specification: {entity_specs}
Claim description: {claim_description}
Text: {input_text}
Output: """

PROMPTS["community_report"] = """
-목표-
머리스타일 도메인에서 추출된 엔티티와 관계 정보를 바탕으로, 스타일 조합 커뮤니티(스타일 클러스터)에 대한 종합 보고서를 작성합니다.  
- 제공된 엔티티 및 관계 데이터만 사용하세요. 추가적인 추론이나 일반화는 금지합니다.

# 보고서 구조 (기존 GraphRAG 호환 + 도메인 최적화)
```json
{
  "title": <커뮤니티 제목>,             // 예: "레이어드컷 + C컬펌 커뮤니티"
  "summary": <커뮤니티 요약>,          // 2~3문장: 주요 특징 요약
  "rating": <0~10>,                    // 추천 점수 (정수 또는 소수 가능)
  "rating_explanation": <점수 설명>,    // 한 문장 설명
  "findings": [                        // 5~10개 인사이트
    {
      "summary": <인사이트 요약>,      // 예: "볼륨감 강화"
      "explanation": <근거 설명>       // 예: "C컬펌으로 레이어드컷의 층감이 살아납니다."
    },
    ...
  ]
}
```

## 필드 설명
- **title**: 대표 스타일명 또는 스타일 조합
- **summary**: 스타일 조합의 주요 특징 및 추천 이유 요약
- **recommendation_score**: 0~10 범위의 점수 (정수 또는 소수)
- **score_explanation**: 추천 점수 한 문장 근거
- **findings**: 도메인 관련 인사이트 5~10개
  - 어울리는 얼굴형, 모발 특징, 손질 난이도, 계절·TPO 추천 등 포함

# 작성 예시
```csv
Entities:
id,entity,type,description
1,레이어드컷,CUT,가벼운 층으로 볼륨을 살리는 커트
2,C컬펌,PERM,끝을 C자 형태로 말아 자연스러운 볼륨을 주는 펌
3,시스루뱅,BANG,이마가 은은하게 비치는 얇은 앞머리

Relationships:
id,source,target,description
1,레이어드컷,C컬펌,레이어드컷과 C컬펌은 함께 시술되어 풍성한 볼륨을 구현함
2,레이어드컷,시스루뱅,레이어드컷과 시스루뱅은 얼굴형 보완을 위해 자주 조합됨
```
```json
{
  "title": "레이어드컷 + C컬펌 커뮤니티",
  "summary": "레이어드컷에 C컬펌을 조합하여 층감과 볼륨을 극대화하고, 시스루뱅으로 얼굴형을 부드럽게 보완하는 스타일 조합입니다.",
  "recommendation_score": 8.5,
  "score_explanation": "블로그 언급 빈도가 높고 유지 기간과 재현성이 우수하기 때문입니다.",
  "findings": [
    {"summary": "볼륨감 강화", "explanation": "C컬펌으로 레이어드컷의 층감이 살아나 자연스러운 볼륨을 완성합니다."},
    {"summary": "얼굴형 보완", "explanation": "시스루뱅이 이마 라인을 부드럽게 감싸 얼굴을 갸름하게 보이게 합니다."}
  ]
}
```

# 실사용 규칙
오직 제공된 엔티티 및 관계 정보에 근거한 내용만 포함하고, 허위 추론이나 상상은 금지합니다.

Text:
```
{input_text}
```

출력:
JSON 포맷에 맞춰 결과 문자열만 반환하세요.
"""



PROMPTS["entity_extraction"] = """
-목표-
네이버 블로그(머리스타일별 설명) 및 Allure 블로그(최신 트렌드) 문서에서 **머리스타일의 특징과 관련된 정보를 추출**합니다.

-단계-
1. 스타일 특징 추출:
아래 항목들 중 **본문에 명시된 특징만** 추출하세요.
- 어울리는 모발 특징 (예: 곱슬, 직모, 굵은 모발, 가는 모발 등)
- 어울리는 길이 (예: 단발, 중단발, 장발 등)
- 어울리는 이마 모양 (예: 둥근형, M자형, 네모형)
- 어울리는 광대 특징 (예: 광대가 큰 얼굴, 광대가 좁은 얼굴 등)
- 만들어주는 분위기 (예: 청순, 시크, 우아함, 러블리, 성숙한, 어른스러운, 어려보이는 등)
- 손질 난이도 (쉬움, 보통, 어려움)
- 어울리는 얼굴형 (예: 계란형, 둥근 얼굴형, 각진 얼굴형 등)
- 어울리는 이마 비율 (예: 이마가 넓은, 좁은)

형식:
("feature"<|>특징명<|>설명)

2. 필요 시 스타일 요소 간 관계 추출:
같이 자주 언급되는 스타일 간 관계를 추출합니다.
형식:
("relationship"<|>스타일1<|>스타일2<|>설명<|>강도)

3. 모든 항목을 **{record_delimiter}** 로 구분하여 출력하고, 마지막에 {completion_delimiter}를 출력하세요.


#################### 예시 1 ####################
Text:
"레이어드컷은 가는 모발이나 중단발에 잘 어울리고, 청순한 분위기를 만들어 준다. 손질도 쉬운 편이다."

Output:
("feature"<|>"어울리는 모발 특징"<|>"가는 모발")##
("feature"<|>"어울리는 길이"<|>"중단발")##
("feature"<|>"분위기"<|>"청순한 분위기")##
("feature"<|>"손질 난이도"<|>"쉬움")<|COMPLETE|>


#################### 예시 2 ####################
Text:
"히피펌은 굵은 곱슬머리에 추천되며, 시크하고 성숙한 이미지를 준다. 유지관리는 조금 어려운 편이다."

Output:
("feature"<|>"어울리는 모발 특징"<|>"굵은 곱슬머리")##
("feature"<|>"분위기"<|>"시크하고 성숙한 분위기")##
("feature"<|>"손질 난이도"<|>"어려움")<|COMPLETE|>


#################### 예시 3 ####################
Text:
"시스루뱅은 둥근형 이마나 좁은 이마를 보완해 어려 보이는 이미지를 완성해 준다."

Output:
("feature"<|>"어울리는 이마 모양"<|>"둥근형 이마")##
("feature"<|>"어울리는 이마 비율"<|>"좁은 이마")##
("feature"<|>"분위기"<|>"어려 보이는 이미지")<|COMPLETE|>


#################### 예시 4 (관계 예시 1) ####################
Text:
"허쉬컷과 레이어드컷은 모두 중단발과 잘 어울려 자연스러운 볼륨감을 연출한다."

Output:
("feature"<|>"어울리는 길이"<|>"중단발")##
("relationship"<|>"허쉬컷"<|>"레이어드컷"<|>"허쉬컷과 레이어드컷은 중단발과 잘 어울리고 볼륨감을 준다."<|>8)<|COMPLETE|>


#################### 예시 5 (관계 예시 2) ####################
Text:
"가르마펌과 애즈펌은 모두 직모에 잘 어울리며, 세련된 이미지를 연출한다."

Output:
("feature"<|>"어울리는 모발 특징"<|>"직모")##
("feature"<|>"분위기"<|>"세련된 이미지")##
("relationship"<|>"가르마펌"<|>"애즈펌"<|>"가르마펌과 애즈펌은 직모에 어울리고 세련된 분위기를 만든다."<|>9)<|COMPLETE|>


####################
실제 데이터:
Text: {input_text}
####################
Output:
"""



PROMPTS[
    "summarize_entity_descriptions"
] = """당신은 아래에 제공된 데이터를 종합적으로 요약하는 역할을 맡은 유용한 어시스턴트입니다.
하나 또는 두 개의 엔티티와, 해당 엔티티(또는 엔티티 그룹)와 관련된 설명 목록이 제공됩니다.
이 모든 설명을 **하나의 포괄적인 설명**으로 통합해 주세요.  
모든 설명에서 수집된 정보를 반드시 포함해야 합니다.

설명 간에 **모순되는 내용이 있다면**, 이를 **해결하여 일관된 하나의 설명**을 제공해 주세요.  
설명은 반드시 **3인칭 시점**으로 작성하고, **엔티티 이름**을 포함시켜 어떤 엔티티에 대한 설명인지 **명확히 드러내 주세요**.

#######
-데이터-
엔티티: {entity_name}
설명 목록: {description_list}
#######
출력:
"""



PROMPTS[
    "entiti_continue_extraction"
] = """이전 추출에서 많은 엔티티가 누락되었습니다.  
아래에 이전과 동일한 형식으로 추가 엔티티를 입력해 주세요:
"""


PROMPTS[
    "entiti_if_loop_extraction"
] = """여전히 누락된 엔티티가 있을 수 있습니다.  
남아 있는 엔티티가 **추가로 필요한지 여부**를 **YES | NO**로 답변해 주세요.
"""


PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event"]
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"


PROMPTS[
    "local_rag_response"
] = """---역할---

당신은 제공된 데이터 테이블을 기반으로 질문에 답변하는 유용한 어시스턴트입니다.


---목표---

사용자의 질문에 적절하게 응답할 수 있도록,  
요구된 **응답 길이 및 형식**에 맞게 입력된 데이터 테이블의 **모든 관련 정보를 요약**하고,  
필요할 경우 **일반적인 지식도 포함**하여 응답을 생성하세요.

답을 모르는 경우, **모른다고만 말하세요**. **절대로 아무것도 지어내지 마세요.**
근거가 제공되지 않은 정보는 **절대로 포함하지 마세요.**


---목표 응답 길이 및 형식---

{response_type}


---데이터 테이블---

{context_data}


---목표---

사용자의 질문에 적절하게 응답할 수 있도록,  
요구된 **응답 길이 및 형식**에 맞게 입력된 데이터 테이블의 **모든 관련 정보를 요약**하고,  
필요할 경우 **일반적인 지식도 포함**하여 응답을 생성하세요.

답을 모르는 경우, **모른다고만 말하세요**. **절대로 아무것도 지어내지 마세요.**
근거가 제공되지 않은 정보는 **절대로 포함하지 마세요.**


---목표 응답 길이 및 형식---

{response_type}

응답에는 **필요한 섹션과 설명**을 추가하고,  
**Markdown 형식**을 사용해 스타일링해 주세요.
"""

PROMPTS[
    "global_map_rag_points"
] = """---역할---

당신은 제공된 데이터 테이블을 기반으로 질문에 답변하는 유용한 어시스턴트입니다.


---목표---

사용자의 질문에 응답하는 주요 포인트 목록을 생성하여, 입력된 데이터 테이블의 모든 관련 정보를 요약한 응답을 작성하세요.

응답을 생성할 때는 아래에 제공된 데이터 테이블을 **주요 문맥**으로 사용해야 합니다.
답을 모르는 경우나 입력된 데이터 테이블이 충분한 정보를 제공하지 않는 경우, 모른다고만 말하세요. **절대로 아무것도 지어내지 마세요.**

응답의 각 포인트는 다음 요소를 반드시 포함해야 합니다:
- 설명(Description): 해당 포인트에 대한 포괄적인 설명
- 중요도 점수(Importance Score): 사용자의 질문에 답변하는 데 있어 해당 포인트의 중요도를 0~100 사이의 정수로 표시. '모르겠다'와 같은 답변은 0점을 부여

응답은 다음과 같은 **JSON 형식**으로 작성해야 합니다:
{{
    "points": [
        {{"description": "포인트 1에 대한 설명...", "score": 점수값}},
        {{"description": "포인트 2에 대한 설명...", "score": 점수값}}
    ]
}}

응답 시 반드시 원래 의미와 "shall", "may", "will"과 같은 **조동사의 사용**을 그대로 유지해야 합니다.
근거가 제공되지 않은 정보는 절대로 포함하지 마세요.


---데이터 테이블---

{context_data}

---목표---

사용자의 질문에 응답하는 주요 포인트 목록을 생성하여, 입력된 데이터 테이블의 모든 관련 정보를 요약한 응답을 작성하세요.

응답을 생성할 때는 아래에 제공된 데이터 테이블을 **주요 문맥**으로 사용해야 합니다.
답을 모르는 경우나 입력된 데이터 테이블이 충분한 정보를 제공하지 않는 경우, 모른다고만 말하세요. **절대로 아무것도 지어내지 마세요.**

응답의 각 포인트는 다음 요소를 반드시 포함해야 합니다:
- 설명(Description): 해당 포인트에 대한 포괄적인 설명
- 중요도 점수(Importance Score): 사용자의 질문에 답변하는 데 있어 해당 포인트의 중요도를 0~100 사이의 정수로 표시. '모르겠다'와 같은 답변은 0점을 부여

응답은 다음과 같은 **JSON 형식**으로 작성해야 합니다:
{{
    "points": [
        {{"description": "포인트 1에 대한 설명", "score": 점수값}},
        {{"description": "포인트 2에 대한 설명", "score": 점수값}}
    ]
}}
"""


PROMPTS[
    "global_reduce_rag_response"
] = """---역할---

당신은 여러 분석가가 제공한 관점을 종합하여 데이터셋에 대한 질문에 답변하는 유용한 어시스턴트입니다.


---목표---

요구된 **응답 길이 및 형식**에 맞게,  
데이터셋의 서로 다른 부분을 분석한 **여러 분석가의 보고서**를 종합하여 사용자의 질문에 답변하세요.

아래에 제공된 분석가들의 보고서는 **중요도 순으로 내림차순 정렬**되어 있음을 유의하세요.

답을 모르는 경우나 제공된 보고서가 충분한 정보를 제공하지 않는 경우, **모른다고만 말하세요.**  
**절대로 아무것도 지어내지 마세요.**

최종 응답은 **분석가들의 보고서에서 불필요한 정보를 모두 제거**하고,  
**정리된 정보**를 **모든 주요 포인트와 그 의미를 설명하는 포괄적인 답변**으로 통합해야 합니다.  
응답은 **요구된 길이와 형식**에 적절하게 작성되어야 합니다.

응답에는 **필요한 섹션과 설명**을 추가하고,  
**Markdown 형식**을 사용해 스타일링해 주세요.

응답 시 반드시 원래 의미와 **"shall", "may", "will"** 과 같은 **조동사의 사용**을 그대로 유지해야 합니다.

근거가 제공되지 않은 정보는 **절대로 포함하지 마세요.**


---목표 응답 길이 및 형식---

{response_type}


---분석가 보고서---

{report_data}


---목표---

요구된 **응답 길이 및 형식**에 맞게,  
데이터셋의 서로 다른 부분을 분석한 **여러 분석가의 보고서**를 종합하여 사용자의 질문에 답변하세요.

아래에 제공된 분석가들의 보고서는 **중요도 순으로 내림차순 정렬**되어 있음을 유의하세요.

답을 모르는 경우나 제공된 보고서가 충분한 정보를 제공하지 않는 경우, **모른다고만 말하세요.**  
**절대로 아무것도 지어내지 마세요.**

최종 응답은 **분석가들의 보고서에서 불필요한 정보를 모두 제거**하고,  
**정리된 정보**를 **모든 주요 포인트와 그 의미를 설명하는 포괄적인 답변**으로 통합해야 합니다.  
응답은 **요구된 길이와 형식**에 적절하게 작성되어야 합니다.

응답 시 반드시 원래 의미와 **"shall", "may", "will"** 과 같은 **조동사의 사용**을 그대로 유지해야 합니다.

근거가 제공되지 않은 정보는 **절대로 포함하지 마세요.**


---목표 응답 길이 및 형식---

{response_type}

응답에는 **필요한 섹션과 설명**을 추가하고,  
**Markdown 형식**을 사용해 스타일링해 주세요.
"""


PROMPTS[
    "naive_rag_response"
] = """You're a helpful assistant
Below are the knowledge you know:
{content_data}
---
If you don't know the answer or if the provided knowledge do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.
---Target response length and format---
{response_type}
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["default_text_separator"] = [
    # Paragraph separators
    "\n\n",
    "\r\n\r\n",
    # Line breaks
    "\n",
    "\r\n",
    # Sentence ending punctuation
    "。",  # Chinese period
    "．",  # Full-width dot
    ".",  # English period
    "！",  # Chinese exclamation mark
    "!",  # English exclamation mark
    "？",  # Chinese question mark
    "?",  # English question mark
    # Whitespace characters
    " ",  # Space
    "\t",  # Tab
    "\u3000",  # Full-width space
    # Special characters
    "\u200b",  # Zero-width space (used in some Asian languages)
]

