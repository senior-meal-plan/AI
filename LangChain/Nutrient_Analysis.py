# mealID 포맷 생각하기

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o")  #gpt 모델 설정

body_format = """
{
    "mealId": 0,
    "totalKcal": 0,
    "totalProtein": 0,
    "totalCarbs": 0,
    "totalFat": 0,
    "totalCalcium": 0,
    "Summary": "string",
    "Severity": "string",
    "foods": [
        {
            "name": "string",
            "kcal": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "calcium": 0,
            "servingSize": 0
        }
    ]
}
"""

messages = [
    SystemMessage("""
                  다음의 body 양식에 맞춰서 json 정보 리턴해줘.
                  만약 여러 음식에 대한 정보가 들어오면, foods에 각각의 음식에 대해 저장해.
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