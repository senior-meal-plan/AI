# --------------------
# 음식에 대한 텍스트가 들어오면 영양 성분을 분석해주는 모듈
# analyze_meal : 음식 텍스트를 받아 분석함
# _extract_json : {} 블록만 추출
# load_json_safely : 문자열 딕셔너리 변환
# recompute_totals : 총 음식 정보 수정 (각각의 음식은 잘 계산하는데 총 정보가 깨지는 경우가 있었음)
# nutrient_analysis : 양식 에러가 나지 않도록 정적으로 작업한 파이프라인
# --------------------

import os, json, re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    model_kwargs={"response_format": {"type": "json_object"}}
)

body_format = """
{
    "mealId": 0,
    "mealDate": "2025-11-01",
    "mealTime": "00:00:00",
    "mealType": "string",
    "totalKcal": 0,
    "totalProtein": 0,
    "totalCarbs": 0,
    "totalFat": 0,
    "totalCalcium": 0,
    "foods": [
        {
            "name": "string",
            "kcal": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "calcium": 0,
            "servingSize": 0,
            "saturatedFatPercentKcal": 0,
            "unsaturatedFat": 0,
            "dietaryFiber": 0,
            "sodium": 0,
            "addedSugarKcal": 0,
            "processedMeatGram": 0,
            "vitaminD_IU": 0,
            "isVegetable": true,
            "isFruit": true,
            "isFried": true
        }
    ]
}
"""

messages = [
    SystemMessage("""
                  다음의 body 양식에 맞춰서 json 정보 리턴해줘.
                  만약 여러 음식에 대한 정보가 들어오면, foods에 각각의 음식에 대해 저장해.
                  Summary와 Severity는 한국어로 작성해.
                  이외의 텍스트는 덧붙이지 마. \n"""
                  + body_format)
]



def analyze_meal(user_input: str) -> str:
    messages.append(HumanMessage(user_input))
    ai_response = llm.invoke(messages)
    messages.append(ai_response)
    return ai_response.content

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


def nutrient_analysis(user_input):
    json_str = analyze_meal(user_input)
    result = load_json_safely(json_str)
    result = recompute_totals(result)
    return result


if __name__ == "__main__":
    while True:
        user_input = input("사용자: ")
        if user_input == "exit":
            break
        messages.append(
            HumanMessage(user_input)
        )

        ai_response = llm.invoke(messages)

        messages.append(ai_response)

        print("AI: "+ai_response.content)
        