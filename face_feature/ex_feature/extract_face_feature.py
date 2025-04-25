# extract_face_feature.py
import os
import cv2
import torch
import numpy as np
from torchvision import transforms
from transformers import ConvNextForImageClassification, AutoFeatureExtractor
from .draw_jaw import render_selected_facemesh
from .MTCNN import extract_face

# MediaPipe 중 턱선의 인덱스
facial_feature_indices = {
    "jawline": [234, 93, 132, 58, 172, 136, 150, 149, 176,
                148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454]
}

# 클래스 정의
CLASS_NAMES = ["Oval", "Heart", "Square", "Round", "Oblong"]

# 모델 로드 및 출력층 수정
model = ConvNextForImageClassification.from_pretrained("facebook/convnext-base-224")
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(0.5),
    torch.nn.Linear(model.classifier.in_features, len(CLASS_NAMES))
)
model_path = os.path.join(os.path.dirname(__file__), 'model', 'Best_Model.pth')
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# Feature Extractor 로드
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/convnext-base-224")
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=feature_extractor.image_mean, std=feature_extractor.image_std)
])

def predict(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 턱선 시각화
    image_with_jaw = render_selected_facemesh(image_rgb, facial_feature_indices)

    # 얼굴 검출 (MTCNN)
    face_img = extract_face(image_with_jaw)

    # 전처리 및 예측
    input_tensor = transform(face_img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        logits = outputs.logits
        _, predicted = logits.max(1)
        pred_class = CLASS_NAMES[predicted.item()]
        prob = torch.nn.functional.softmax(logits, dim=1)[0][predicted.item()].item()

    return pred_class
