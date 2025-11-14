def weekly_anlysis(weekly: dict):
    return 0


# --------------------
# 일주일분의 데일리 스코어를 score_sum에 합산
# 평균 내고, 0~60 / 60~80 / 80~100 구간으로 나쁨 / 괜찮음 / 좋음 판단
# --------------------
def weekly_scoresheet(response):
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



# --------------------
# 일주일 질환별 점수를 합산 (순서대로: 황반변성, 고혈압, 심근경색, 근감소증, 고지혈증, 골질환)
# 각 질환별로 평균을 낸 후, 10점 밑인 질환 상태가 있다면 목표로 리턴
# --------------------
def new_health_goals(response):

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
