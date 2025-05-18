import cv2
import uuid
import os
import pandas as pd
import stone 

def extract_face_colors(image):
    # 1. 임시 파일명 생성
    temp_path = f"temp_{uuid.uuid4().hex}.jpg"

    # 2. 이미지 저장
    cv2.imwrite(temp_path, image)

    try:
        # 3. stone 라이브러리에 파일 경로 전달
        result = stone.process(temp_path, image_type="color", return_report_image=True)

        face_data = []
        for face in result.get('faces', []):
            face_id = face.get('face_id')
            for color_info in face.get('dominant_colors', []):
                face_data.append({
                    'face_id': face_id,
                    'color': color_info['color'],
                    'percent': float(color_info['percent'])
                })

        color_df = pd.DataFrame(face_data)
        skin_color = color_df['color'].iloc[0]  # 첫 번째 dominant color
        return skin_color

    finally:
        # 4. 파일 정리
        if os.path.exists(temp_path):
            os.remove(temp_path)
