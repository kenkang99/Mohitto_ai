import pymysql
from rds_config import rds_config

def get_latest_request():
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
            sql = "SELECT * FROM request_table ORDER BY created_at DESC LIMIT 1"
            cursor.execute(sql)
            return cursor.fetchone()
    finally:
        conn.close()
