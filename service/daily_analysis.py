# 점수 계산 코드 수정하면 끝난다


# 받는 데이터 형식:
#{
#  "reportId": 9007199254740991,
#  "whoAmIDto": {
#    "userId": 9007199254740991,
#    "userName": "string",
#    "age": 1073741824,
#    "userHeight": 0,
#    "userWeight": 0,
#    "Gender": "string",
#    "topics": [
#      {
#        "topicId": 9007199254740991,
#        "topicType": "ALLERGEN",
#        "name": "string",
#        "description": "string",
#        "source": "string"
#      }
#    ]
#  },
#  "meals": [
#    {
#      "mealType": "BREAKFAST",
#      "mealTime": {
#        "hour": 1073741824,
#        "minute": 1073741824,
#        "second": 1073741824,
#        "nano": 1073741824
#      },
#      "photoUrl": "string",
#      "foods": [
#        {
#          "name": "string",
#          "kcal": 0,
#          "protein": 0,
#          "carbs": 0,
#          "fat": 0,
#          "calcium": 0,
#          "servingSize": 0,
#          "saturatedFatPercentKcal": 0,
#          "unsaturatedFat": 0,
#          "dietaryFiber": 0,
#          "sodium": 0,
#          "addedSugarKcal": 0,
#          "processedMeatGram": 0,
#          "vitaminD_IU": 0,
#          "isVegetable": true,
#          "isFruit": true,
#          "isFried": true
#        }
#      ]
#    }
#  ],
#  "callbackUrl": "string"
#}

# topictype: "ALLERGEN""HEALTH_GOAL""DISEASE_HISTORY"



# --------------------
# 환경설정
# --------------------

import os, json, re, base64, io, requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage



# --------------------
# LLM 설정 및 return body format 세팅
# --------------------

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    model_kwargs={"response_format": {"type": "json_object"}}
)

body_format = {
  "reportId": 0,
  "status": "string",
  "errorMessage": "string",
  "totalKcal": 0,
  "totalProtein": 0,
  "totalCarbs": 0,
  "totalFat": 0,
  "totalCalcium": 0,
  "summary": "string",
  "severity": "string",
  "summarizeScore": 0,
  "basicScore": 0,
  "macularDegenerationScore": 0,
  "hypertensionScore": 0,
  "myocardialInfarctionScore": 0,
  "sarcopeniaScore": 0,
  "hyperlipidemiaScore": 0,
  "boneDiseaseScore": 0
}



# --------------------
# 건강 점수 계산 함수
# basic_score: 기본 점수 계산
# mucular_score: 황반변성 점수 계산
# hypertension_score: 고혈압 점수 계산
# myocardial_score: 심근경색 점수 계산
# sarcopenia_score: 근감소증 점수 계산
# hyperlipidemia_score: 고지혈증 점수 계산
# bone_score: 뼈 질환 점수 계산
# --------------------

def basic_score(daily: dict):
    basicScore = 60
    return basicScore

def macular_score(daily: dict):
    macularDegenerationScore = 1
    return macularDegenerationScore

def hypertension_score(daily: dict):
    hypertensionScore = 2
    return hypertensionScore

def myocardial_score(daily: dict):
    myocardialInfarctionScore = 3
    return myocardialInfarctionScore

def sarcopenia_score(daily: dict):
    sarcopeniaScore = 4
    return sarcopeniaScore

def hyperlipidemia_score(daily: dict):
    hyperlipidemiaScore = 5
    return hyperlipidemiaScore

def bone_score(daily: dict):
    boneDiseaseScore = 6
    return boneDiseaseScore



# --------------------
# 점수 합산 함수
# total_sum: totalKcal, totalProtein, totalCarbs, totalFat, totalCalcium 계산
# score_sum: 점수를 리포트에 입력 및 기본점수와 대표질환점수(여러개면 평균) 합산
# --------------------

def total_sum(meals: list, result: dict):
    kcal = 0
    protein = 0
    carbs = 0
    fat = 0
    calcium = 0

    for i in meals:
        for j in i["foods"]:
            kcal += j["kcal"]
            protein += j["protein"]
            carbs += j["carbs"]
            fat += j["fat"]
            calcium += j["calcium"]

    result["totalKcal"] = kcal
    result["totalProtein"] = protein
    result["totalCarbs"] = carbs
    result["totalFat"] = fat
    result["totalCalcium"] = calcium

    return result

def score_sum(daily: dict, result: dict):

    result["basicScore"] = basic_score(daily)
    result["macularDegenerationScore"] = macular_score(daily)
    result["hypertensionScore"] = hypertension_score(daily)
    result["myocardialInfarctionScore"] = myocardial_score(daily)
    result["sarcopeniaScore"] = sarcopenia_score(daily)
    result["hyperlipidemiaScore"] = hyperlipidemia_score(daily)
    result["boneDiseaseScore"] = bone_score(daily)

    disease_average_score = 0

    topic_list = daily["whoAmIDto"]["topics"]
    disease_list = []
    for topic in topic_list:
        if topic["topicType"] == "DISEASE_HISTORY":
            disease_list.append(topic["name"])

    for i in disease_list:
        if i == "황반변성":
            disease_average_score += result["macularDegenerationScore"]
        elif i == "고혈압":
            disease_average_score += result["hypertensionScore"]
        elif i == "심근경색":
            disease_average_score += result["myocardialInfarctionScore"]
        elif i == "근감소증":
            disease_average_score += result["sarcopeniaScore"]
        elif i == "고지혈증":
            disease_average_score += result["hyperlipidemiaScore"]
        elif i == "뼈 질환":
            disease_average_score += result["boneDiseaseScore"]

    if len(disease_list) == 0:
        disease_average_score = 20
    else:
        disease_average_score = disease_average_score / len(disease_list)

    result["summarizeScore"] = result["basicScore"] + disease_average_score

    return result


# --------------------
# AI 평가 함수
# feedback: AI가 피드백을 주어 summary와 severity를 입력하는 함수
# --------------------

def feedback(daily: dict, result: dict):
    meals_text = json.dumps(daily["meals"], ensure_ascii = False, indent = 2)
    system_prompt = """
        너는 60~80대 어르신의 하루 식단을 평가하는 영양사 AI야.

        [해야 할 일]
        1. 하루 동안 먹은 모든 식사를 보고, 건강 측면에서 간단히 평가해라.
        2. 아래 두 가지 값을 JSON 형식으로만 반환해야 한다.

        [summary 작성 규칙]
        - 한국어로 2~3문장으로 작성한다.
        - 존댓말(친절하고 부드러운 말투)을 사용한다.
        - 탄수화물/단백질/지방의 균형, 채소·과일 섭취 여부, 짠 음식·기름진 음식·단 음식·가공육 여부 등 주요 특징을 꼭 언급한다.
        - 개선이 필요한 점이 있으면 구체적으로 한두 가지 정도만 짚어서 제안해 준다.
        - 지나치게 무섭게 말하지 말고, "다음에는 이렇게 해보시면 더 좋겠습니다." 같은 톤으로 말한다.

        [severity 규칙]
        - 아래 셋 중 하나만 사용해야 한다. (다른 문자열 절대 금지)
            - "GOOD": 전반적으로 균형이 괜찮고 큰 문제는 없을 때
            - "SOSO": 대체로 괜찮지만 짜게 먹거나, 기름기·당류가 조금 많은 등 주의가 필요한 부분이 있을 때
            - "BAD" : 아주 짜거나, 매우 기름지거나, 단 음식/튀김/가공육 위주의 식단처럼 건강에 좋지 않은 편일 때

        [출력 형식 - 반드시 이 JSON 구조만 반환]
        {
          "summary": "여기에 2~3문장 요약",
          "severity": "GOOD 또는 SOSO 또는 BAD"
        }
        기타 설명, 말머리, 코드블록 표시는 절대 붙이지 마라.
    """

    messages = [
        SystemMessage(system_prompt),
        HumanMessage(
            "다음은 어떤 어르신의 하루 식단 정보입니다.\n"
            "이 정보를 바탕으로 하루 식단을 평가해 주세요.\n\n"
            f"{meals_text}"
        ),
    ]

    try:
        ai_response = llm.invoke(messages)
        parsed = json.loads(ai_response.content)

        summary = str(parsed.get("summary", "")).strip()
        severity = str(parsed.get("severity", "")).strip().upper()

        if severity not in {"GOOD", "SOSO", "BAD"}:
            severity = "SOSO"

        result["summary"] = summary
        result["severity"] = severity

    except Exception as e:
        result["summary"] = ""
        result["severity"] = "SOSO"
        result["status"] = "ERROR"
        result["errorMessage"] = f"식단 요약 생성 중 오류가 발생했습니다: {e}"

    return result



# --------------------
# 메인 함수
# --------------------

def daily_analysis(daily: dict):
    result = body_format.copy()
    result["reportId"] = daily["reportId"]

    try:
        result = total_sum(daily["meals"], result)
        result = score_sum(daily, result)
        result = feedback(daily, result)

        if result["status"] != "ERROR":        
            result["status"] = "SUCCESS"
            result["errorMessage"] = "none"

    except Exception as e:
        result = body_format.copy()
        result["reportId"] = daily["reportId"]
        result["status"] = "ERROR"
        result["errorMessage"] = str(e)

    return result



# --------------------
# 테스트용 코드
# --------------------

if __name__ == "__main__":

    test_daily_json = """
    {
        "reportId": 12353,
        "whoAmIDto": {
            "userId": 9007199254740991,
            "userName": "철수철수",
            "age": 65,
            "userHeight": 170,
            "userWeight": 78,
            "Gender": "MALE",
            "topics": [
              {
                "topicId": 9007199254740991,
                "topicType": "ALLERGEN",
                "name": "갑각류",
                "description": "갑각류 알러지",
                "source": "string"
              },
              {
                "topicId": 9007199254740992,
                "topicType": "DISEASE_HISTORY",
                "name": "황반변성",
                "description": "황반변성 질환",
                "source": "string"
              },
              {
                "topicId": 9007199254740993,
                "topicType": "DISEASE_HISTORY",
                "name": "뼈 질환",
                "description": "뼈 질환",
                "source": "string"
              }
            ]
          },
          "meals": [
            {
            "mealType": "BREAKFAST",
            "mealTime": 10:00:00
              "photoUrl": "string",
              "foods": [
                {
                  "name": "밥",
                  "kcal": 130.0,
                  "protein": 2.7,
                  "carbs": 28.2,
                  "fat": 0.3,
                  "calcium": 10,
                  "servingSize": 100,
                  "saturatedFatPercentKcal": 0,
                  "unsaturatedFat": 0.1,
                  "dietaryFiber": 0.4,
                  "sodium": 0,
                  "addedSugarKcal": 0,
                  "processedMeatGram": 0,
                  "vitaminD_IU": 0,
                  "isVegetable": false,
                  "isFruit": false,
                  "isFried": false
                },
                {
                  "name": "미역국",
                  "kcal": 80,
                  "protein": 5,
                  "carbs": 8,
                  "fat": 3,
                  "calcium": 150,
                  "servingSize": 200,
                  "saturatedFatPercentKcal": 10,
                  "unsaturatedFat": 2,
                  "dietaryFiber": 1,
                  "sodium": 500,
                  "addedSugarKcal": 0,
                  "processedMeatGram": 0,
                  "vitaminD_IU": 0,
                  "isVegetable": true,
                  "isFruit": false,
                  "isFried": false
                }
              ]
            },
            {
            "mealType": "DINNER",
            "mealTime": 10:00:00
              "photoUrl": "string",
              "foods": [
                {
                  "name": "돼지갈비",
                  "kcal": 300,
                  "protein": 25,
                  "carbs": 10,
                  "fat": 18,
                  "calcium": 20,
                  "servingSize": 150,
                  "saturatedFatPercentKcal": 40,
                  "unsaturatedFat": 8,
                  "dietaryFiber": 0,
                  "sodium": 500,
                  "addedSugarKcal": 20,
                  "processedMeatGram": 0,
                  "vitaminD_IU": 0,
                  "isVegetable": true,
                  "isFruit": false,
                  "isFried": false
                }
              ]
            }
          ],
          "callbackUrl": "string"
        }
    """

    test_daily = json.loads(test_daily_json)
    result = daily_analysis(test_daily)

    print(result)