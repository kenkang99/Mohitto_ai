import stone
import cv2
import pandas as pd

def extract_face_colors(image):
    result = stone.process(image, image_type="color", return_report_image=True)
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
    skin_color= color_df['color'].iloc[0]
    return skin_color