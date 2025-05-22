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



PROMPTS[
    "community_report"
] = """You are an AI assistant that helps a human analyst to perform general information discovery. 
Information discovery is the process of identifying and assessing relevant information associated with certain entities (e.g., organizations and individuals) within a network.

# Goal
Write a comprehensive report of a community, given a list of entities that belong to the community as well as their relationships and optional associated claims. The report will be used to inform decision-makers about information associated with the community and their potential impact. The content of this report includes an overview of the community's key entities, their legal compliance, technical capabilities, reputation, and noteworthy claims.

# Report Structure

The report should include the following sections:

- TITLE: community's name that represents its key entities - title should be short but specific. When possible, include representative named entities in the title.
- SUMMARY: An executive summary of the community's overall structure, how its entities are related to each other, and significant information associated with its entities.
- IMPACT SEVERITY RATING: a float score between 0-10 that represents the severity of IMPACT posed by entities within the community.  IMPACT is the scored importance of a community.
- RATING EXPLANATION: Give a single sentence explanation of the IMPACT severity rating.
- DETAILED FINDINGS: A list of 5-10 key insights about the community. Each insight should have a short summary followed by multiple paragraphs of explanatory text grounded according to the grounding rules below. Be comprehensive.

Return output as a well-formed JSON-formatted string with the following format:
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary":<insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary":<insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# Grounding Rules
Do not include information where the supporting evidence for it is not provided.


# Example Input
-----------
Text:
```
Entities:
```csv
id,entity,type,description
1,레이어드컷,CUT,머리카락에 층을 내어 볼륨감과 가벼움을 주는 여성 커트 스타일
2,C컬펌,PERM,머리 끝을 C자 형태로 말아 자연스러운 볼륨을 주는 펌 스타일
3,시스루뱅,BANG,이마가 살짝 비치는 얇은 앞머리로 얼굴형을 보완해주는 트렌디한 스타일
4,허쉬컷,CUT,층을 크게 내어 개성 있는 느낌을 주는 커트 스타일
5,히피펌,PERM,굵은 웨이브를 전반적으로 넣어 빈티지한 분위기를 주는 펌 스타일
6,풀뱅,BANG,이마를 완전히 덮는 두꺼운 앞머리로 동안 이미지를 연출하는 스타일
```
Relationships:
```csv
id,source,target,description
1,레이어드컷,C컬펌,레이어드컷과 C컬펌은 함께 시술되어 자연스러운 볼륨감과 손질 용이성을 높여주는 조합
2,레이어드컷,시스루뱅,레이어드컷과 시스루뱅은 얼굴형 보완과 세련된 이미지를 제공하는 인기 스타일 조합
3,허쉬컷,히피펌,허쉬컷과 히피펌은 빈티지하면서도 자유로운 분위기를 연출할 수 있는 트렌디한 조합
4,허쉬컷,풀뱅,허쉬컷과 풀뱅은 동안 이미지를 강조하면서도 개성을 살려주는 스타일 조합
```
```
Output:
{{
    "title": "레이어드컷과 허쉬컷 기반 스타일 커뮤니티",
    "summary": "이 커뮤니티는 레이어드컷과 허쉬컷을 중심으로 다양한 펌과 앞머리 스타일이 조합되어 추천되는 스타일 그룹입니다. 자연스러움과 볼륨감을 살리는 조합부터 개성과 빈티지함을 강조하는 조합까지 다양한 선택지를 제공합니다.",
    "rating": 9.0,
    "rating_explanation": "다양한 얼굴형과 분위기에 맞춰 추천 가능한 조합이 많아 활용도가 높고, 블로그와 미용 전문가들이 자주 추천하는 스타일들이 포함되어 있어 높은 점수를 부여했습니다.",
    "findings": [
        {{
            "summary": "레이어드컷과 C컬펌의 볼륨 시너지",
            "explanation": "레이어드컷과 C컬펌은 함께 시술될 때 볼륨감이 극대화되며, 자연스러운 컬이 가볍고 풍성한 스타일을 완성합니다. 특히 머리 손질이 쉬워 일상 스타일링에 적합합니다."
        }},
        {{
            "summary": "레이어드컷과 시스루뱅의 얼굴형 보완 효과",
            "explanation": "시스루뱅은 레이어드컷과 함께 적용될 때 이마를 은은하게 가려 얼굴형을 보완하고 세련된 이미지를 연출합니다. 특히 동안 효과를 원하는 고객에게 추천할 수 있습니다."
        }},
        {{
            "summary": "허쉬컷과 히피펌의 빈티지 트렌드",
            "explanation": "허쉬컷의 개성 있는 층과 히피펌의 굵은 웨이브가 어우러져 빈티지하고 자유로운 분위기를 연출합니다. 최근 레트로 스타일이 인기를 끌면서 더욱 주목받는 조합입니다."
        }},
        {{
            "summary": "허쉬컷과 풀뱅의 동안 강조 스타일",
            "explanation": "허쉬컷과 풀뱅 조합은 얼굴을 작아 보이게 하고 동안 이미지를 연출하는 데 효과적입니다. 개성 있는 스타일링을 원하는 고객에게 추천할 수 있습니다."
        }}
    ]
}}



# Real Data

Use the following text for your answer. Do not make anything up in your answer.

Text:
```
{input_text}
```

The report should include the following sections:

- TITLE: community's name that represents its key hairstyle elements - title should be short but specific. When possible, include representative named hairstyle elements in the title.
- SUMMARY: An executive summary of the hairstyle community's overall structure, how its elements are related to each other, and significant information associated with these styles.
- IMPACT SEVERITY RATING: a float score between 0-10 that represents the popularity, trendiness, or recommendation strength of the hairstyle community. IMPACT is the scored importance of a hairstyle community.
- RATING EXPLANATION: Give a single sentence explanation of the IMPACT severity rating.
- DETAILED FINDINGS: A list of 5-10 key insights about the hairstyle community. Each insight should have a short summary followed by multiple paragraphs of explanatory text grounded according to the grounding rules below. Be comprehensive.

Return output as a well-formed JSON-formatted string with the following format:
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary": <insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary": <insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# Grounding Rules
Do not include information where the supporting evidence for it is not provided.

Output:
"""

PROMPTS["entity_extraction"] = """-Goal-
Given a hairstyle-related text document from Naver or Allure blogs and a list of entity types, identify all hairstyle-related entities and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the hairstyle or feature, capitalized (e.g., 레이어드컷, 시스루뱅, 가는 모발, 청순한 분위기)
- entity_type: One of the following types: [{entity_types}]
  - STYLE: Specific hairstyle names (e.g., 레이어드컷, 시스루뱅, 히피펌)
  - FEATURE: Hair characteristics, applicable face shapes, styling benefits, or emotional impressions (e.g., 가는 모발, 중단발, 청순한 분위기, 손질이 쉬움)
- entity_description: Comprehensive description of the style or feature, including what it looks like, who it suits, or the impression it creates

Format each entity as:
("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
Relationships can include:
- Styles that are frequently **recommended together**
- Features that **enhance** or **complement** each other
- Styles and features that are **incompatible**

For each relationship, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation why these entities are related (positive or negative)
- relationship_strength: a numeric score from 1 (weak or negative relation) to 10 (strong positive relation)

Format each relationship as:
("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3. Return output in Korean as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

4. When finished, output {completion_delimiter}

######################
-Examples-
######################
Example 1:

Entity_types: [STYLE, FEATURE]
Text:
"레이어드컷은 가는 모발이나 중단발에 잘 어울리고, 청순한 분위기를 만들어 준다. 특히 C컬펌과 함께 시술되면 자연스러운 볼륨감과 손질이 쉬운 스타일이 완성된다."

Output:
("entity"{tuple_delimiter}"레이어드컷"{tuple_delimiter}"STYLE"{tuple_delimiter}"머리카락에 층을 내어 볼륨감을 주는 커트 스타일"){record_delimiter}
("entity"{tuple_delimiter}"가는 모발"{tuple_delimiter}"FEATURE"{tuple_delimiter}"가는 머리카락을 가진 사람에게 어울림"){record_delimiter}
("entity"{tuple_delimiter}"중단발"{tuple_delimiter}"FEATURE"{tuple_delimiter}"어깨 정도 길이의 머리에 어울림"){record_delimiter}
("entity"{tuple_delimiter}"청순한 분위기"{tuple_delimiter}"FEATURE"{tuple_delimiter}"순수하고 깨끗한 이미지를 주는 스타일 특징"){record_delimiter}
("entity"{tuple_delimiter}"C컬펌"{tuple_delimiter}"STYLE"{tuple_delimiter}"머리 끝을 C자 형태로 말아 자연스러운 볼륨을 주는 펌 스타일"){record_delimiter}
("relationship"{tuple_delimiter}"레이어드컷"{tuple_delimiter}"가는 모발"{tuple_delimiter}"레이어드컷은 가는 모발에 자연스러운 볼륨감을 부여하여 추천됨"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"레이어드컷"{tuple_delimiter}"C컬펌"{tuple_delimiter}"레이어드컷과 C컬펌은 함께 시술 시 볼륨감과 손질 용이성을 극대화함"{tuple_delimiter}9){completion_delimiter}

######################
Example 2:

Entity_types: [STYLE, FEATURE]
Text:
"허쉬컷과 히피펌은 함께 시술되어 빈티지한 분위기를 연출하며, 가는 모발에 잘 어울린다. 하지만 볼륨이 적은 모발에는 추천되지 않는다."

Output:
("entity"{tuple_delimiter}"허쉬컷"{tuple_delimiter}"STYLE"{tuple_delimiter}"층이 크고 개성 있는 커트 스타일"){record_delimiter}
("entity"{tuple_delimiter}"히피펌"{tuple_delimiter}"STYLE"{tuple_delimiter}"굵은 웨이브로 빈티지한 분위기를 주는 펌 스타일"){record_delimiter}
("entity"{tuple_delimiter}"빈티지한 분위기"{tuple_delimiter}"FEATURE"{tuple_delimiter}"레트로 감성을 살리는 스타일 특징"){record_delimiter}
("entity"{tuple_delimiter}"가는 모발"{tuple_delimiter}"FEATURE"{tuple_delimiter}"가는 머리카락을 가진 사람에게 어울림"){record_delimiter}
("entity"{tuple_delimiter}"볼륨이 적은 모발"{tuple_delimiter}"FEATURE"{tuple_delimiter}"모발의 볼륨이 적은 특성"){record_delimiter}
("relationship"{tuple_delimiter}"허쉬컷"{tuple_delimiter}"히피펌"{tuple_delimiter}"허쉬컷과 히피펌은 빈티지한 분위기를 살려주는 트렌디한 조합임"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"허쉬컷"{tuple_delimiter}"가는 모발"{tuple_delimiter}"허쉬컷은 가는 모발과 잘 어울려 볼륨감을 보완할 수 있음"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"히피펌"{tuple_delimiter}"볼륨이 적은 모발"{tuple_delimiter}"히피펌은 볼륨이 적은 모발에는 스타일이 어색할 수 있어 비추천됨"{tuple_delimiter}3){completion_delimiter}

######################
Example 3:

Entity_types: [STYLE, FEATURE]
Text:
"시스루뱅은 둥근형 이마를 보완해 어려 보이는 이미지를 준다. 풀뱅과는 함께 추천되지 않는다."

Output:
("entity"{tuple_delimiter}"시스루뱅"{tuple_delimiter}"STYLE"{tuple_delimiter}"이마가 살짝 비치는 얇은 앞머리 스타일"){record_delimiter}
("entity"{tuple_delimiter}"둥근형 이마"{tuple_delimiter}"FEATURE"{tuple_delimiter}"둥근 이마를 가진 사람에게 어울림"){record_delimiter}
("entity"{tuple_delimiter}"어려 보이는 이미지"{tuple_delimiter}"FEATURE"{tuple_delimiter}"동안 이미지를 주는 스타일 특징"){record_delimiter}
("entity"{tuple_delimiter}"풀뱅"{tuple_delimiter}"STYLE"{tuple_delimiter}"이마를 완전히 덮는 두꺼운 앞머리 스타일"){record_delimiter}
("relationship"{tuple_delimiter}"시스루뱅"{tuple_delimiter}"둥근형 이마"{tuple_delimiter}"시스루뱅은 둥근형 이마를 보완하여 어려 보이는 이미지를 만들어 줌"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"시스루뱅"{tuple_delimiter}"풀뱅"{tuple_delimiter}"시스루뱅과 풀뱅은 서로 스타일이 상반되어 함께 추천되지 않음"{tuple_delimiter}2){completion_delimiter}
######################
-Real Data-
######################
Entity_types: [STYLE, FEATURE]
Text: {input_text}
######################
Output:
"""





PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""


PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event"]
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS[
    "local_rag_response"
] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}


---Data tables---

{context_data}


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.

If you don't know the answer, just say so. Do not make anything up.

Do not include information where the supporting evidence for it is not provided.


---Target response length and format---

{response_type}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "global_map_rag_points"
] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response consisting of a list of key points that responds to the user's question, summarizing all relevant information in the input data tables.

You should use the data provided in the data tables below as the primary context for generating the response.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.

Each key point in the response should have the following element:
- Description: A comprehensive description of the point.
- Importance Score: An integer score between 0-100 that indicates how important the point is in answering the user's question. An 'I don't know' type of response should have a score of 0.

The response should be JSON formatted as follows:
{{
    "points": [
        {{"description": "Description of point 1...", "score": score_value}},
        {{"description": "Description of point 2...", "score": score_value}}
    ]
}}

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".
Do not include information where the supporting evidence for it is not provided.


---Data tables---

{context_data}

---Goal---

Generate a response consisting of a list of key points that responds to the user's question, summarizing all relevant information in the input data tables.

You should use the data provided in the data tables below as the primary context for generating the response.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.

Each key point in the response should have the following element:
- Description: A comprehensive description of the point.
- Importance Score: An integer score between 0-100 that indicates how important the point is in answering the user's question. An 'I don't know' type of response should have a score of 0.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".
Do not include information where the supporting evidence for it is not provided.

The response should be JSON formatted as follows:
{{
    "points": [
        {{"description": "Description of point 1", "score": score_value}},
        {{"description": "Description of point 2", "score": score_value}}
    ]
}}
"""

PROMPTS[
    "global_reduce_rag_response"
] = """---Role---

You are a helpful assistant responding to questions about a dataset by synthesizing perspectives from multiple analysts.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarize all the reports from multiple analysts who focused on different parts of the dataset.

Note that the analysts' reports provided below are ranked in the **descending order of importance**.

If you don't know the answer or if the provided reports do not contain sufficient information to provide an answer, just say so. Do not make anything up.

The final response should remove all irrelevant information from the analysts' reports and merge the cleaned information into a comprehensive answer that provides explanations of all the key points and implications appropriate for the response length and format.

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".

Do not include information where the supporting evidence for it is not provided.


---Target response length and format---

{response_type}


---Analyst Reports---

{report_data}


---Goal---

Generate a response of the target length and format that responds to the user's question, summarize all the reports from multiple analysts who focused on different parts of the dataset.

Note that the analysts' reports provided below are ranked in the **descending order of importance**.

If you don't know the answer or if the provided reports do not contain sufficient information to provide an answer, just say so. Do not make anything up.

The final response should remove all irrelevant information from the analysts' reports and merge the cleaned information into a comprehensive answer that provides explanations of all the key points and implications appropriate for the response length and format.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".

Do not include information where the supporting evidence for it is not provided.


---Target response length and format---

{response_type}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
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

