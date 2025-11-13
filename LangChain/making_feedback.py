# --------------------
# 피드백 만들어주는 모듈
# 일주일 동안 먹은 거 전부 받아서, 세부적인 맞춤형 피드백을 내놓도록 한다
# 질환별 채점한 점수도 받아서 잘했다 못했다 판단(일단은 단순 하드코딩)
# --------------------

import os, json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    model_kwargs={"response_format": {"type": "json_object"}}
)


def weekly_scoresheet(response):
    # --------------------
    # 일주일분의 데일리 스코어를 score_sum에 합산
    # 평균 내고, 0~60 / 60~80 / 80~100 구간으로 나쁨 / 괜찮음 / 좋음 판단
    # --------------------
    score_sum = 0
    num_reports = len(response["dailyReports"])
    for i in range(num_reports):
        score_sum += response["dailyReports"][i]["summarizeScore"]
    average = score_sum / num_reports

    state = ""
    if average >= 80:
        state = "good"
    elif average >= 60:
        state = "soso"
    else:
        state = "bad"

    return state

def new_health_goals(response):
    # --------------------
    # 일주일 질환별 점수를 합산 (순서대로: 황반변성, 고혈압, 심근경색, 근감소증, 고지혈증, 골질환)
    # 각 질환별로 평균을 낸 후, 10점 밑인 질환 상태가 있다면 목표로 리턴
    # --------------------

    num_reports = len(response["dailyReports"])

    macular_degeneration_score_sum = 0
    hypertension_score_sum = 0
    myocardial_infarction_score_sum = 0
    sarcopenia_score_sum = 0
    hyperlipidemia_score_sum = 0
    bone_disease_score_sum = 0

    for i in range(num_reports):
        macular_degeneration_score_sum += response["dailyReports"][i]["macularDegenerationScore"]
        hypertension_score_sum += response["dailyReports"][i]["hypertensionScore"]
        myocardial_infarction_score_sum += response["dailyReports"][i]["myocardialInfarctionScore"]
        sarcopenia_score_sum += response["dailyReports"][i]["sarcopeniaScore"]
        hyperlipidemia_score_sum += response["dailyReports"][i]["hyperlipidemiaScore"]
        bone_disease_score_sum += response["dailyReports"][i]["boneDiseaseScore"]
    
    macular_degeneration_average = macular_degeneration_score_sum / num_reports
    hypertension_average = hypertension_score_sum / num_reports
    myocardial_infarction_average = myocardial_infarction_score_sum / num_reports
    sarcopenia_average = sarcopenia_score_sum / num_reports
    hyperlipidemia_average = hyperlipidemia_score_sum / num_reports
    bone_disease_average = bone_disease_score_sum / num_reports

    disease_list = [macular_degeneration_average, hypertension_average, myocardial_infarction_average, sarcopenia_average, hyperlipidemia_average, bone_disease_average]

    health_goals = []

    for i in range(len(disease_list)):
        if disease_list[i] <= 10:
            if i == 0:
                health_goals.append("황반변성")
            if i == 1:
                health_goals.append("고혈압")
            if i == 2:
                health_goals.append("심근경색")
            if i == 3:
                health_goals.append("근감소증")
            if i == 4:
                health_goals.append("고지혈증")
            if i == 5:
                health_goals.append("뼈 질환")

    return health_goals

def recommand_recipe(response):
    # --------------------
    # 일주일치 모든 식사 내역, 유저의 건강 목표를 받는다
    # 유저의 건강 목표를 바탕으로, 이번주 식사 내역에서 부족한 영양소를 체크
    # DB 접속 안하고 텍스트파일 참조하는 방식
    # --------------------
    return 1

def weekly_health_guide(response):
    # --------------------
    # 일주일치 모든 식사 내역을 받은 후, AI를 활용해 개인 맞춤형 식사 피드백을 도출한다
    # 점수 채점 및 피드백을 한번에 모든 유저를 받아서 -> 분석 되는대로 리턴
    # 명세: 분석 요청반환
    # --------------------
    feedback = ""
    return feedback

def daily_health_guide(response):
    # --------------------
    # 하루 식사 내용을 받은 후, AI를 활용해 개인 맞춤형 식사 피드백을 도출한다
    # 점수 채점 및 피드백을 한번에 모든 유저를 받아서 -> 분석 되는대로 리턴
    # 명세: 분석 요청반환
    # --------------------
    feedback = ""
    return feedback

def meal_health_guide(response):
    # --------------------
    # 1회의 식사 내역을 받은 후, AI를 활용해 개인 맞춤형 식사 피드백을 도출한다
    # 점수 채점 및 피드백을 한번에 모든 유저를 받아서 -> 분석 되는대로 리턴
    # --------------------

    body_format = """
    {
        "reportId": 9007199254740991,
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
    """

    messages = [
        SystemMessage("""
                      너는 전문 건강 관리사야. 사람들의 식단을 보고 건강 피드백을 하는 역할을 해야 해.
                      다음의 body 양식에 정확히 일치하는 json 정보 리턴해줘. 그 외 텍스트는 금지야.

                      1) 중요한 정보
                        - status에는 오늘 식사가 어떤 점 때문에 좋았거나 나빴는지 한 줄 요약을 해줘. (예시: 야채를 많이 먹은 건강한 식사입니다!, 포화지방을 너무 많이 드신 나쁜 식사입니다.)
                        - summary에서는 식사를 꼼꼼히 분석해서 3~5줄의 리포트를 작성해줘. Foods에 있는 구체적인 음식 항목을 언급하면서 어떤 점이 좋고 나쁜지 자세하게 말해줘.
                        - severity는 INFO / WARNING / ALERT 셋 중 하나로 채워줘. 건강에 큰 이상 없으면 INFO, 경고가 필요하면 WARNING, 당장 조치가 필요하면 ALERT야.
                      
                      2) 기타 값 채우기
                        - reportId는 response에 있는 mealId를 그대로 넣어줘.
                        - errorMessage는 ""으로 비워줘.
                        - totalKcal, totalProtein, totalCarbs, totalFat, totalCalcium은 response에서 받아온 값을 그대로 넣어줘.
                        - Score가 붙은 것들은 전부 0을 넣어줘.
                      
                      \n """ + body_format),
        HumanMessage(json.dumps(response, ensure_ascii=False))
    ]
    
    feedback = llm.invoke(messages)

    if not isinstance(feedback, dict):
        feedback = {}
    if feedback["summary"] == "":
        feedback["errorMessage"] = "EmptyError"
    
    return feedback








if __name__ == "__main__":

    meal_example = {
        "mealId": 1,
        "totalKcal": 800,
        "totalProtein": 400,
        "totalCarbs": 400,
        "totalFat": 400,
        "totalCalcium": 400,
        "Summary": "잘했음",
        "Severity": "INFO",
        "isDairyIntake": true,
        "isVitaminCIntake": true,
        "isVitaminBIntake": true,
        "isFishIntake": true,
        "isNutsIntake": true,
        "isVegetableOilIntake": true,
        "isUnrefinedCarbsIntake": true,
        "foods": [
            {
                "name": "아이스",
                "kcal": 400,
                "protein": 100,
                "carbs": 100,
                "fat": 100,
                "calcium": 100,
                "servingSize": 1,
                "saturatedFatPercentKcal": 100,
                "unsaturatedFat": 100,
                "dietaryFiber": 100,
                "sodium": 100,
                "addedSugarKcal": 100,
                "processedMeatGram": 100,
                "vitaminD_IU": 100,
                "isVegetable": true,
                "isFruit": true,
                "isFried": true
            },
            {
                "name": "크림",
                "kcal": 300,
                "protein": 100,
                "carbs": 100,
                "fat": 100,
                "calcium": 100,
                "servingSize": 1,
                "saturatedFatPercentKcal": 100,
                "unsaturatedFat": 100,
                "dietaryFiber": 100,
                "sodium": 100,
                "addedSugarKcal": 100,
                "processedMeatGram": 100,
                "vitaminD_IU": 100,
                "isVegetable": true,
                "isFruit": true,
                "isFried": true
            }
        ]
    }

    print(meal_health_guide(meal_example))


    #response = {}

    #print(weekly_scoresheet(response))
    #print(new_health_goals(response))