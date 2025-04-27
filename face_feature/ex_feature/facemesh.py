# facemesh.py
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh

# 얼굴 비율 추출 함수
def extract_facial_ratios(image):
    h, w, _ = image.shape
    
    with mp_face_mesh.FaceMesh(
        static_image_mode=True, max_num_faces=1, refine_landmarks=True
    ) as face_mesh:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return None, None, None  # 얼굴 인식 실패

        landmarks = results.multi_face_landmarks[0].landmark

        def get_point(idx):
            pt = landmarks[idx]
            return np.array([pt.x * w, pt.y * h])

        # 주요 포인트 추출
        top_point = get_point(10)        # 이마 중앙
        mid_point = get_point(9)         # 미간 중앙
        jaw = get_point(152)             # 턱 하단
        nose = get_point(2)              # 코 끝

        # 거리 계산
        top_height = np.linalg.norm(mid_point - top_point) * 2
        mid_height = np.linalg.norm(nose - mid_point)
        down_height = np.linalg.norm(jaw - nose)
        face_height = top_height + mid_height + down_height

        if face_height == 0:
            return 0, 0, 0

        # 비율 계산
        top_ratio = top_height / face_height
        mid_ratio = mid_height / face_height
        down_ratio = down_height / face_height

        return top_ratio, mid_ratio, down_ratio
