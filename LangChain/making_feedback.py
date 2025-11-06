# --------------------
# 피드백 만들어주는 모듈
# 일주일 동안 먹은 거 전부 받아서, 세부적인 맞춤형 피드백을 내놓도록 한다
# 질환별 채점한 점수도 받아서 잘했다 못했다 판단(일단은 단순 하드코딩)
# --------------------

import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    # 명세: 분석 요청반환
    # --------------------
    feedback = ""
    return feedback



if __name__ == "__main__":
    response = {}

    print(weekly_scoresheet(response))
    print(new_health_goals(response))