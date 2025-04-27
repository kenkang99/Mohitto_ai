# draw_jaw.py
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 초기화 (전역)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def render_selected_facemesh(image, facial_feature_indices):
    if image is None:
        print("[!] 이미지가 None입니다.")
        return None

    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        annotated_image = image.copy()
        face_landmarks = results.multi_face_landmarks[0].landmark

        def get_point(idx):
            pt = face_landmarks[idx]
            return int(pt.x * w), int(pt.y * h)

        for region, indices in facial_feature_indices.items():
            pts = [get_point(idx) for idx in indices]
            for i in range(len(pts) - 1):
                # 💛 노란선(BGR): (0, 255, 255)
                cv2.line(annotated_image, pts[i], pts[i + 1], (0, 255, 255), 3)

        return annotated_image
    else:
        print("[!] 얼굴 감지 실패")
        return image
