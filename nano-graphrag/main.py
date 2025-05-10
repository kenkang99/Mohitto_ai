import argparse
import asyncio
import nest_asyncio
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from nano_graphrag import GraphRAG, QueryParam
from nano_graphrag._llm import openai_complete_if_cache

# 환경변수 로딩
load_dotenv()

# 이벤트 루프 패치
nest_asyncio.apply()

# 사용자 정의 LLM 함수
async def my_custom_llm(prompt, system_prompt=None, history_messages=[], **kwargs):
    return await openai_complete_if_cache(
        "gpt-4o-mini",  # 원하는 모델
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        **kwargs
    )

# SBERT 임베딩 모델 로딩
model_name = 'jhgan/ko-sroberta-multitask'
model = SentenceTransformer(model_name)

# nano-graphrag 요구사항에 맞게 래핑
def wrap_embedding_func_with_attrs(embedding_dim, max_token_size):
    def decorator(func):
        func.embedding_dim = embedding_dim
        func.max_token_size = max_token_size
        return func
    return decorator

@wrap_embedding_func_with_attrs(embedding_dim=768, max_token_size=512)
async def local_embedding_func(texts: list[str]) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True)

# GraphRAG 인스턴스 생성
graph_func = GraphRAG(
    working_dir="./graphrag",
    best_model_func=my_custom_llm,
    embedding_func=local_embedding_func,
    chunk_token_size=100000,
    chunk_overlap_token_size=0,
)

# 비동기 아님 - 동기로 실행
def run_query(query_text: str):
    param_local = QueryParam(mode="local")
    response_local = graph_func.query(query_text, param_local)  # await 제거
    print("=== Local RAG Recommendation ===")
    print(response_local)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hairstyle Recommendation with GraphRAG")
    parser.add_argument('--query', type=str, required=True, help="User query for hairstyle recommendation")

    args = parser.parse_args()

    run_query(args.query)  # asyncio.run 제거
