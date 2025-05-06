# MTCNN.py
import cv2
from mtcnn import MTCNN

# MTCNN detector 초기화 (전역)
detector = MTCNN()

def extract_face(img, target_size=(224, 224)):
    results = detector.detect_faces(img)
    if not results:
        return cv2.resize(img, target_size)

    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height

    # 경계 확장
    adj_h = 10
    new_y1 = max(0, y1 - adj_h)
    new_y2 = min(img.shape[0], y1 + height + adj_h)
    new_height = new_y2 - new_y1

    adj_w = int((new_height - width) / 2)
    new_x1 = max(0, x1 - adj_w)
    new_x2 = min(img.shape[1], x2 + adj_w)

    face_img = img[new_y1:new_y2, new_x1:new_x2]
    return cv2.resize(face_img, target_size)
