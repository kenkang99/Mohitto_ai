import itertools
import nest_asyncio
from nano_graphrag import GraphRAG, QueryParam
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
from nano_graphrag._llm import openai_complete_if_cache

nest_asyncio.apply()
load_dotenv()

# 프롬프트 템플릿
PROMPT_TEMPLATE = """
<SYSTEM>
너는 전문 헤어스타일리스트야. 사용자 프로필을 기반으로 맞춤형 스타일과 추천 이유를 설명해주는 역할을 맡았어.

<USER>
다음 사용자 정보를 바탕으로 어울리는 헤어스타일 10가지를 추천하고, 각각 추천하는 이유를 간단히 설명해 주세요.
- 얼굴형: {face_shape_eval}
- 모발 유형: {hair_type}
- 성별: {sex}
- 얼굴에 대한 총평: {final_evaluation}
- 이마 형태: {forehead_shape}
- 광대 특징: {cheekbone}
- 분위기: {mood}
- 관리 난이도: {difficulty}
- 머리 길이: {hair_length}
- 앞머리 여부: {has_bangs}

## 출력 조건
- 컷 스타일 최대 5가지 추천 (이름 + 추천 이유)
- 펌 스타일 최대 3가지 추천 (이름 + 추천 이유)
- 앞머리 스타일 최대 2가지 추천 (이름 + 추천 이유)
"""

def make_query_prompt(user_input):
    mood_str = ','.join(user_input['mood']) if isinstance(user_input['mood'], list) else user_input['mood']
    print(user_input)
    return PROMPT_TEMPLATE.format(
        face_shape_eval=user_input['face_shape_eval'],
        hair_type=user_input['hair_type'],
        sex=user_input['sex'],
        final_evaluation=user_input['final_evaluation'],
        cheekbone=user_input['cheekbone'],
        mood=mood_str,
        difficulty=user_input['difficulty'],
        hair_length=user_input['hair_length'],
        forehead_shape=user_input['forehead_shape'],
        has_bangs=user_input['has_bangs']
    )

async def my_custom_llm(prompt, system_prompt=None, history_messages=None, **kwargs):
    return await openai_complete_if_cache(
        "gpt-4o-mini",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages or [],
        **kwargs
    )

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

def wrap_embedding_func_with_attrs(embedding_dim, max_token_size):
    def decorator(func):
        func.embedding_dim = embedding_dim
        func.max_token_size = max_token_size
        return func
    return decorator

@wrap_embedding_func_with_attrs(embedding_dim=768, max_token_size=512)
async def local_embedding_func(texts: list[str]) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True)

graph_func = GraphRAG(
    working_dir="./graphrag",
    best_model_func=my_custom_llm,
    embedding_func=local_embedding_func,
    chunk_token_size=100000,
    chunk_overlap_token_size=0,
)

def get_first_recommendations(user_input):
    """1차 GraphRAG를 통한 헤어스타일 추천"""
    prompt = make_query_prompt(user_input)
    
    print("=== 1차 GraphRAG 호출 프롬프트 ===")
    print(prompt)
    
    param_local = QueryParam(mode="local")
    response = graph_func.query(prompt, param_local)
    
    return response