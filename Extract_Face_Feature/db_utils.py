# Extract_Face_Feature/db_utils.py
import pymysql
from datetime import datetime
from rds_config import rds_config

# 가장 최근 1개의 request를 가져옴
def get_latest_request(user_id: int, request_id: int):
    conn = pymysql.connect(
        host=rds_config['host'],
        user=rds_config['user'],
        password=rds_config['password'],
        database=rds_config['database'],
        port=rds_config['port'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            # request ID와 user ID가 일치하는 사진만 가져옴: 추후 api서버에서 user id와 request id를 모델로 송신예정
            sql = """
                SELECT * FROM request_table
                WHERE user_id = %s AND request_id = %s
                LIMIT 1
            """
            cursor.execute(sql, (user_id, request_id))
            return cursor.fetchone()
    finally:
        conn.close()

# DB에 업로드
def save_result_to_db(result: dict, request_id: int):
    conn = pymysql.connect(
        host=rds_config['host'],
        user=rds_config['user'],
        password=rds_config['password'],
        database=rds_config['database'],
        port=rds_config['port'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO result_table (
                    face_type, skin_tone, forehead, sex,
                    top_rate, middle_rate, bottom_rate,
                    created_at, request_id, rec_color,
                    summary
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                result.get("얼굴형"),
                result.get("피부색"),
                result.get("이마 모양"),
                result.get("성별", "unknown"),
                result.get("이마 평가"),
                result.get("중안부 평가"),
                result.get("하안부 평가"),
                datetime.now(),
                request_id,
                ", ".join(result.get("추천 염색", [])),
                result.get("얼굴 분석 총평")
            ))
        conn.commit()
    finally:
        conn.close()