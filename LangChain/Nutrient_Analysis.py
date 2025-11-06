# --------------------
# 음식에 대한 텍스트가 들어오면 영양 성분을 분석해주는 모듈
# body_format 수정 필요
# --------------------

import os
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