# --------------------
# 기본 점수 및 6개 질환에 대해 점수 매기는 모듈
# --------------------

from openai import OpenAI
import json, os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT_BASIC = """
        너는 영양학 점수 계산 전문가야. 다음의 공식을 사용해 JSON 데이터를 계산해.

        1) 단백질 점수:
            Sprotein = 20 × min(1, P / (R × W))
            (P: 단백질 g, W: 체중 kg, R: 1.2)

        2) 탄단지 균형 점수:
            Sdaily = 10 × max(0, 1 − ⅓(|C − 0.50|/0.15 + |P − 0.20|/0.10 + |F − 0.30|/0.10))
            (C: 탄수화물 g, P: 단백질 g, F: 지방 g)
            Smeals = 5 × 평균(max(0, 1 − ⅓(|cm − 0.50|/0.12 + |pm − 0.20|/0.12 + |fm − 0.30|/0.12)))
    """

SYSTEM_PROMPT_DISEASE = """
    """

def ai_calculate_nutrition_score(meal_json: dict):
    # 1️⃣ 수식 프롬프트
    formulas = """
너는 영양학 점수 계산 전문가다. 다음의 공식을 사용해 JSON 데이터를 계산하라.

1) 단백질 점수:
    Sprotein = 20 × min(1, P / (R × W))
    (P: 단백질 g, W: 체중 kg, R: 권장비율 일반 1.0, 시니어 1.2)

2) 하루 탄단지 비율 점수:
    Sdaily = 10 × max(0, 1 − ⅓(|C − 0.50|/0.15 + |P − 0.20|/0.10 + |F − 0.30|/0.10))

3) 끼니별 보정 점수:
    Smeals = 5 × 평균(max(0, 1 − ⅓(|cm − 0.50|/0.12 + |pm − 0.20|/0.12 + |fm − 0.30|/0.12)))

4) 최종 점수:
    Smacro = min(Sdaily + Smeals, 15)

출력은 다음 JSON 형태로 정확히 반환하라:
{
  "Sprotein": float,
  "Sdaily": float,
  "Smeals": float,
  "Smacro": float,
  "ratios": {"C_ratio": float, "P_ratio": float, "F_ratio": float}
}
모든 계산은 소수점 둘째 자리까지 반올림.
"""

    # 2️⃣ LLM 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": formulas},
            {"role": "user", "content": f"입력 데이터:\n{json.dumps(meal_json, ensure_ascii=False)}"}
        ],
        temperature=0
    )

    # 3️⃣ 결과 파싱
    try:
        result_text = response.choices[0].message.content.strip()
        result = json.loads(result_text)
        return result
    except Exception:
        return {"error": "파싱 실패", "raw": result_text}

