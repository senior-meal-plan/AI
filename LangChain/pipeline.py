# --------------------
# 구동시켜보기 위한 샘플 파이프라인
# image_to_txt : 사진에 있는 음식을 텍스트로 바꾸는 모듈
# nutrient_analysis : 음식 텍스트를 받아 영양 정보를 추출하는 모듈
# --------------------

import json, os
from image_to_txt import *  
from nutrient_analysis import *  

if __name__ == "__main__":
    # --------------------
    # 경로를 절대화해서 사진을 불러옴(차후 수정)
    # 사진을 보고 음식과 그램수를 분석
    # 칼로리와 영양소 분석
    # 딕셔너리로 파싱해서 총 영양소 계산
    # 출력
    # --------------------

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.abspath(os.path.join(BASE_DIR, "..", "반상.jpg"))

    meal_str = analyze_image_to_text(image_path)
    result = nutrient_analysis(meal_str)

    print(json.dumps(result, ensure_ascii=False, indent=2))
