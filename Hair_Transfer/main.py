from model import StableHair
from model import model_call
import cv2
import torch
from PIL import Image
import numpy as np

id = '123'

# 샘플 이미지
source_img = './test_imgs/ID/sample.jpg'
ref_img = './test_imgs/Ref/sample.jpg'

# Stable-hair 결과 생성
bald_image, result_image = model_call(source_img, ref_img)

if isinstance(result_image, Image.Image):
    result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_RGB2BGR)
if isinstance(bald_image, Image.Image):
    bald_image = cv2.cvtColor(np.array(bald_image), cv2.COLOR_RGB2BGR)

# 결과 저장
cv2.imwrite(f'./output/bald/{id}_bald.png', bald_image)
cv2.imwrite(f'./output/result/{id}_result.png', result_image)

print("결과 이미지가 저장되었습니다.")