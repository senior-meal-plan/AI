# --------------------
# 구동시켜보기 위한 샘플 파이프라인
# --------------------

import os, json, re
from dotenv import load_dotenv

from image_to_txt import analyze_image_to_text   # 사진 → "돼지갈비 200g, 밥 150g" 같은 문자열
from nutrient_analysis import analyze_meal       # 문자열 → LLM이 만든 JSON 문자열

# -------------------
# _extract_json : {} 블록만 추출
# load_json_safely : 문자열 딕셔너리 변환
# recompute_totals : 총 음식 정보 수정 (각각의 음식은 잘 계산하는데 총 정보가 깨지는 경우가 있었음)
# -------------------
def _extract_json(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("JSON 텍스트가 str가 아닙니다.")
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    return m.group(0) if m else text

def load_json_safely(text: str) -> dict:
    text = _extract_json(text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fixed = text.replace("'", '"')
        return json.loads(fixed)

def recompute_totals(d: dict) -> dict:
    kcal = prot = carbs = fat = ca = 0.0
    for f in d.get("foods", []) or []:
        kcal  += float(f.get("kcal", 0) or 0)
        prot  += float(f.get("protein", 0) or 0)
        carbs += float(f.get("carbs", 0) or 0)
        fat   += float(f.get("fat", 0) or 0)
        ca    += float(f.get("calcium", 0) or 0)
    d["totalKcal"]     = round(kcal, 2)
    d["totalProtein"]  = round(prot, 2)
    d["totalCarbs"]    = round(carbs, 2)
    d["totalFat"]      = round(fat, 2)
    d["totalCalcium"]  = round(ca, 2)
    return d

def main():
    load_dotenv()

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
    json_str = analyze_meal(meal_str)

    result = load_json_safely(json_str)
    result = recompute_totals(result)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
