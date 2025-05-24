#!/usr/bin/env python3
# recommend_hair_from_image.py

import argparse
import pandas as pd
import stone
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import sys

# ─── 1) 후보 헤어 컬러 HEX 매핑 ─────────────────────
HAIR_COLOR_HEX = {
    'Dark Choco':      '#3E2C1C',
    'Whale Deep Blue': '#1A2B3C',
    'Dark Ash':        '#4A4A4A',
    'Dusty Ash':       '#6E6E6E',
    'Ash Taupe Gray':  '#7F7F7F',
    'Ash Rose':        '#B76E79',
    'Matt Brown':      '#5C3A21',
    'Ferry Violet':    '#8F3E97',
    'Ash Beige':       '#C5B398',
    'Milk Tea Gray':   '#A49E8F',
    'Deep Bordo Rose': '#7B1E39',
    'Rose Pink':       '#F09199',
    'Sunset Orange':   '#FA5F1A',
    'Ash Black':       '#2A2A2A',
    'Gold Brown':      '#B8860B',
    'Ash Blue':        '#556B7B',
    'Pink Red':        '#D8415F',
    'Red Brown':       '#8B3E2F',
    'Burgundy':        '#800020',
    'Red Wine':        '#722F37',
}

# ─── 2) 허용된 분위기 태그 리스트 (변경 금지) ─────────────
ALLOWED_VIBES = [
    '세련된', '부드러운', '깔끔한', '귀여운', '단정한', '우아한',
    '독특한', '사랑스러운', '고급스러운', '차분한', '따뜻한', '강렬한'
]

# ─── 3) 컬러별 대표 분위기 태그 매핑 ────────────────
VIBE_TAGS = {
    'Dark Choco':      ['따뜻한', '고급스러운'],
    'Whale Deep Blue': ['차분한', '세련된'],
    'Dark Ash':        ['깔끔한', '단정한'],
    'Dusty Ash':       ['차분한', '세련된'],
    'Ash Taupe Gray':  ['단정한', '고급스러운'],
    'Ash Rose':        ['사랑스러운', '우아한'],
    'Matt Brown':      ['단정한', '차분한'],
    'Ferry Violet':    ['독특한', '사랑스러운'],
    'Ash Beige':       ['단정한', '세련된'],
    'Milk Tea Gray':   ['부드러운', '차분한'],
    'Deep Bordo Rose': ['고급스러운', '우아한'],
    'Rose Pink':       ['귀여운', '사랑스러운'],
    'Sunset Orange':   ['따뜻한', '강렬한'],
    'Ash Black':       ['깔끔한', '단정한'],
    'Gold Brown':      ['고급스러운', '따뜻한'],
    'Ash Blue':        ['차분한', '세련된'],
    'Pink Red':        ['사랑스러운', '강렬한'],
    'Red Brown':       ['따뜻한', '세련된'],
    'Burgundy':        ['고급스러운', '우아한'],
    'Red Wine':        ['고급스러운', '우아한'],
}

def hex_to_lab(hex_color: str):
    r, g, b = (int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    rgb = sRGBColor(r/255, g/255, b/255)
    lab: LabColor = convert_color(rgb, LabColor)
    return lab.lab_l, lab.lab_a, lab.lab_b

def extract_face_colors(image_path: str) -> pd.DataFrame:
    result = stone.process(image_path, image_type="color", return_report_image=True)
    face_data = []
    for face in result.get('faces', []):
        face_id = face.get('face_id')
        for ci in face.get('dominant_colors', []):
            face_data.append({
                'face_id': face_id,
                'color': ci['color'],
                'percent': float(ci['percent'])
            })
    return pd.DataFrame(face_data)

def recommend_hair_colors(
    skin_hex: str,
    desired_vibes: list[str],
    top_n: int = 3,
    w_L: float = 1.5,
    w_a: float = 1.2,
    w_b: float = 1.0,
    vibe_bonus: float = 20.0
) -> list[str]:
    skin_L, skin_a, skin_b = hex_to_lab(skin_hex)
    hair_lab = {name: hex_to_lab(hex_code) for name, hex_code in HAIR_COLOR_HEX.items()}

    scores = []
    for name, (hL, ha, hb) in hair_lab.items():
        dL, da, db = skin_L - hL, skin_a - ha, skin_b - hb
        distance_score = abs(dL) * w_L + abs(da) * w_a + abs(db) * w_b
        tags = VIBE_TAGS.get(name, [])
        matches = set(tags) & set(desired_vibes)
        score = distance_score - vibe_bonus * len(matches)
        scores.append((score, name))

    scores.sort(key=lambda x: x[0])
    return [name for _, name in scores[:top_n]]

def get_recommendation(image_path: str, vibes: list[str], top_n: int = 3):
    df = extract_face_colors(image_path)
    if df.empty:
        raise ValueError("얼굴을 인식할 수 없습니다.")
    skin_hex = df.sort_values('percent', ascending=False)['color'].iloc[0]
    recs = recommend_hair_colors(skin_hex, vibes, top_n=top_n)
    return skin_hex, recs

# CLI 전용 진입점
if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(
        description="이미지에서 피부색 추출 + 분위기 태그 기반 헤어 컬러 추천"
    )
    parser.add_argument('--image', required=True, help='입력 이미지 경로')
    parser.add_argument('--vibes', required=True, nargs=3, metavar='VIBE',
                        help=f'원하는 분위기 태그 3개 (가능: {", ".join(ALLOWED_VIBES)})')
    parser.add_argument('--top_n', type=int, default=3, help='추천 개수 (기본=3)')
    args = parser.parse_args()

    for vibe in args.vibes:
        if vibe not in ALLOWED_VIBES:
            print(f"지원하지 않는 분위기 태그: {vibe}")
            sys.exit(1)

    try:
        skin_hex, recs = get_recommendation(args.image, args.vibes, args.top_n)
        print(f"Detected skin color: {skin_hex}")
        print(f"Recommended hair colors: {', '.join(recs)}")
    except Exception as e:
        print(f"오류 발생: {e}")