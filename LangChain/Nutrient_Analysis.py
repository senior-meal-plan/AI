import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = "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"
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
    SystemMessage("다음의 body 양식에 맞춰서 json 정보 리턴해줘. 만약 여러 음식에 대한 정보가 들어오면, foods에 각각의 음식에 대해 저장해. \n" + body_format)
]

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