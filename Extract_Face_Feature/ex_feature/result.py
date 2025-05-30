# # ✅ S3 URL에서 이미지 불러오기
# def read_image_from_url(url):
#     response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     if response.status_code != 200:
#         raise FileNotFoundError(f"[다운로드 실패] 이미지를 불러올 수 없습니다: {url}")
#     img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
#     image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#     if image is None:
#         raise ValueError(f"[디코딩 실패] OpenCV가 이미지를 디코딩하지 못했습니다: {url}")
#     return image

# if __name__ == "__main__":
#     info = get_latest_request(user_id, request_id)

#     print("[DEBUG] DB에서 가져온 요청 정보:", info)
#     if not info:
#         raise ValueError("요청 정보를 찾을 수 없습니다.")

#     request_id = str(info["request_id"])
#     image_url = info["user_image_url"]

#     # ✅ S3 URL에서 이미지 불러오기
#     image = read_image_from_url(image_url)

#     result_dict = generate_summary(
#         image,
#         request_id,
#         info["hair_type"],
#         info["hair_length"],
#         "X" if info["dyed"] == 0 else "O",
#         info["forehead_shape"],
#         info["cheekbone"],
#         info["mood"],
#         info["difficulty"]
#     )
    
#     result_dict["request_id"] = request_id
#     result_dict["성별"] = info["sex"]
    
#     final_result = {
#         "request_id": request_id,
#         "input": {
#             "user_image_url": info["user_image_url"],
#             "hair_type": info["hair_type"],
#             "hair_length": info["hair_length"],
#             "dyed": info["dyed"],
#             "forehead_shape": info["forehead_shape"],
#             "cheekbone": info["cheekbone"],
#             "mood": info["mood"],
#             "difficulty": info["difficulty"]
#         },
#         "result": result_dict
#     }

#     file_name = f"recommend_{request_id}_{uuid.uuid4().hex}.json"
#     with open(file_name, "w", encoding="utf-8") as f:
#         json.dump(final_result, f, ensure_ascii=False, indent=2)

#     print(f"✅ 추천 결과 저장 완료: {file_name}")
    
#     ##### DB에 result 추가
#     save_result_to_db(result_dict, int(request_id))
#     print(f"✅ 분석 결과 DB 저장 완료 (request_id={request_id})")
    
#     ##### main api 호출
#     notify_main_api(user_id, int(request_id))
#     print(f"✅ Main API에 분석 완료 알림 전송 완료 (user_id={user_id}, request_id={request_id})")


# 간단 요약 생성

from .evaluate import evaluate_feature
from .color_recommend import get_recommendation

def generate_summary(image_path, curl, length,  forehead, clown, mood, care_level,dyeing="X"):

    # 컴퓨터 추출 정보 불러오기
    faceshape_eval, forehead_eval, central_eval, low_eval, final_evaluation = evaluate_feature(image_path)
    if dyeing == "O":   
       skin_hex, recs = get_recommendation(image_path, mood)
    else:
       skin_hex = "염색 정보 없음"
       recs = []

    result = {
        
        "hair_type" : curl,
        "hair_length" : length,
        "difficulty" : care_level,
        "dyed" : dyeing,
        "skin" : skin_hex,
        "recs" : recs,
        "forehead_shape" : forehead,
        "cheekbone" : clown,
        "mood" : mood,
        "faceshape_eval": faceshape_eval,
        "forehead_eval": forehead_eval,
        "central_eval": central_eval,
        "low_eval": low_eval,
        "final_evaluation" : final_evaluation
    }


    return result


