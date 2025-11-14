# 점수 계산 코드 만들기
# AI의 평가 코드 만들기
# 샘플 데이터 수정해서 서버 테스트


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


# --------------------
# 환경설정
# --------------------

import os, json, re, base64, io, requests
from PIL import Image
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
    return basicScore

def macular_score(daily: dict):
    return macularDegenerationScore

def hypertension_score(daily: dict):
    return hypertensionScore

def myocardial_score(daily: dict):
    return myocardialInfarctionScore

def sarcopenia_score(daily: dict):
    return sarcopeniaScore

def hyperlipidemia_score(daily: dict):
    return hyperlipidemiaScore

def bone_score(daily: dict):
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
        if topic["topicType"] == "DISEASE":
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
# summary: 지피티가 요약하기
# severity: GOOD SOSO BAD 중에 고르기
# --------------------




# --------------------
# 메인 함수
# --------------------

def daily_analysis(daily: dict):
    result = body_format.copy()
    result["reportId"] = daily["reportId"]

    try:
        result = total_sum(daily["meals"], result)
        result = score_sum(daily, result)

        # AI 한마디 넣기
        
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

    test_daily = {
        "reportId": 12353,
        "whoAmIDto": {
            "userId": 9007199254740991,
            "userName": "철수철수",
            "age": 65,
            "userHeight": 170,
            "userWeight": 78,
            "Gender": "male",
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
                "topicType": "DISEASE",
                "name": "황반변성",
                "description": "황반변성 질환",
                "source": "string"
              },
              {
                "topicId": 9007199254740993,
                "topicType": "DISEASE",
                "name": "뼈 질환",
                "description": "뼈 질환",
                "source": "string"
              }
            ]
          },
          "meals": [
            {
            "mealType": "BREAKFAST",
            "mealTime": {
                "hour": 1073741824,
                "minute": 1073741824,
                "second": 1073741824,
                "nano": 1073741824
              },
              "photoUrl": "string",
              "foods": [
                {
                  "name": "밥",
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
                  "isVegetable": false,
                  "isFruit": false,
                  "isFried": false
                },
                {
                  "name": "미역국",
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
                  "isVegetable": false,
                  "isFruit": false,
                  "isFried": false
                }
              ]
            },
            {
            "mealType": "DINNER",
            "mealTime": {
                "hour": 1073741824,
                "minute": 1073741824,
                "second": 1073741824,
                "nano": 1073741824
              },
              "photoUrl": "string",
              "foods": [
                {
                  "name": "돼지갈비",
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
                  "isFruit": false,
                  "isFried": false
                }
              ]
            }
          ],
          "callbackUrl": "string"
        }
    
    result = daily_analysis(test_daily)

    print(result)