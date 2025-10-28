import os, json
from dotenv import load_dotenv

from image_to_txt import analyze_image_to_text
from nutrient_analysis import analyze_meal

def main():
    load_dotenv() 

    # 샘플 사진 절대경로
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "..", "반상.jpg")
    image_path = os.path.abspath(image_path)
    
    # 사진 → 문자열(음식 종류별)
    meal_str = analyze_image_to_text(image_path)

    # 문자열 → 영양소 데이터
    result = analyze_meal(meal_str)

    # 출력
    print("\n=== 최종 영양 분석(JSON) ===")
    print(result)

if __name__ == "__main__":
    main()
