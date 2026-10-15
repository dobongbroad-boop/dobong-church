"""
도봉교회 히어로 사진 보정 스크립트
------------------------------------------------------
카카오톡으로 받은 교회 건물 사진을 웹사이트 배경(히어로 이미지)용으로
자동 보정 + 배너 비율로 잘라주는 스크립트입니다.

사용법
1) 컴퓨터에 Pillow 설치:  pip install pillow
2) 아래 INPUT_PATH 를 실제 사진 파일 경로로 수정
3) 실행:  python enhance_hero.py
4) 만들어진 hero.jpg 파일을 index.html과 같은 폴더의 assets/ 안에 넣으면
   웹사이트 메인 화면에 자동으로 표시됩니다.
------------------------------------------------------
"""

from PIL import Image, ImageEnhance, ImageOps

INPUT_PATH = "https://drive.google.com/drive/u/0/folders/1aVU7UH-2eAijE2sScPCy8Fwn0V_TumcM"      # 원본 사진 경로로 수정하세요
OUTPUT_PATH = "assets/hero.jpg"      # 결과물 (이 이름 그대로 두세요)
TARGET_SIZE = (2000, 1125)           # 가로로 넓은 배너 비율 (16:9)

def enhance_hero(input_path, output_path, size):
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)  # 휴대폰 사진 회전 정보 보정

    # 배너 비율(16:9)에 맞춰 중앙 기준으로 크롭
    target_ratio = size[0] / size[1]
    w, h = img.size
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * 0.35)  # 건물 상단(십자가)이 잘리지 않도록 위쪽에 여유
        img = img.crop((0, top, w, top + new_h))

    img = img.resize(size, Image.LANCZOS)

    # 자연스러운 보정: 대비, 채도, 밝기를 살짝 올려 선명하게
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.12)
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    img.save(output_path, quality=90)
    print(f"완료: {output_path} ({size[0]}x{size[1]})")

if __name__ == "__main__":
    enhance_hero(INPUT_PATH, OUTPUT_PATH, TARGET_SIZE)
