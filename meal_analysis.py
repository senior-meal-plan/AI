# --------------------
# 환경설정
# 받는 데이터 형식:
# {
#  "mealId": 9007199254740991,
#  "photoUrl": "string",
#  "callbackUrl": "string",
#  "whoAmIDto": {
#    "userId": 9007199254740991,
#    "userName": "string",
#    "age": 1073741824,
#    "userHeight": 0,
#    "userWeight": 0,
#    "toics": [
#      {
#        "topicId": 9007199254740991,
#        "topicType": "ALLERGEN",
#        "name": "string",
#        "description": "string",
#        "source": "string"
#      }
#    ]
#  }
#}
# --------------------

import os, json, re, base64, io
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
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

openai_client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    timeout = 60.0
)

body_format = """
{
    "mealId": 0,
    "totalKcal": 0,
    "totalProtein": 0,
    "totalCarbs": 0,
    "totalFat": 0,
    "totalCalcium": 0,
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



# --------------------
# 사진을 읽어오는 함수들
# path_to_data_url : photoUrl을 받아서 경로로 변환
# analyze_image_to_text : path_to_data_url에서 추출된 경로를 받아 사진을 텍스트 형태(밥 100g, 연어 50g...)로 변환
# --------------------

def path_to_data_url(photoUrl: str, max_size: int = 1024) -> str:
    try:
        img = Image.open(photoUrl)

        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim*ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"이미지 리사이즈: {img.size}")

        if img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = io.BytesIO()
        img.save(buffer, format = 'JPEG', quality = 75) 
        buffer.seek(0)


        b64 = base64.b64encode(buffer.read()).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{b64}"

        print(f"Data URL 크기: {len(data_url):,} bytes")
        return data_url   

    except ImportError:
        print("Pillow 미설치 - 원본 이미지 사용")
        with open(photoUrl, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"

def analyze_image_to_text(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    data_url = path_to_data_url(image_path)

    system_message = """
            너는 음식 사진을 분석하는 조리 보조 도우미야.
            사진을 보고, 눈으로 구분 가능한 각 재료와 그 재료의 대략적인 무게(g)를 추정해.
            형식은 단순한 문자열로, 예시는 다음과 같아:

            예시 1: "돼지갈비 200g, 밥 150g, 김치 50g"
            예시 2: "라면 300g, 계란 50g, 파 5g"
            예시 3: "샐러드 120g, 닭가슴살 100g, 드레싱 20g"

            JSON, 표, 코드블록을 쓰지 말고, 오직 위와 같은 한 줄짜리 문자열만 출력해.
        """

    try:
        response = openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 음식 사진을 분석해줘."},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ],
            timeout = 60
        )

        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        print(f"API Error: {type(e).__name__}: {e}")
        raise




# --------------------
# 식사 분석 함수
# analyze_meal : 음식 텍스트를 받아 분석함
# _extract_json : {} 블록만 추출
# load_json_safely : 문자열 딕셔너리 변환
# recompute_totals : 총 음식 정보 수정 (각각의 음식은 잘 계산하는데 총 정보가 깨지는 경우가 있었음)
# --------------------

def analyze_meal(meal_txt: str) -> str:
    messages = [
        SystemMessage("""
                      다음의 body 양식에 맞춰서 json 정보 리턴해줘.
                      만약 여러 음식에 대한 정보가 들어오면, foods에 각각의 음식에 대해 저장해.
                      Summary는 한 줄로 요약해서, 노인들에게 친근한 말투로 작성해. (예시: 오늘 식사를 건강하게 하셨네요! or 단 걸 줄여보면 어떨까요? or 너무 짜게 먹지 않게 주의하세요.)
                      Severity는 enum 형식이기 때문에, INFO / WARNING / ALERT 셋 중 하나로 저장해. 건강하게 먹었으면 INFO, 주의가 필요하면 WARNING, 아주 나쁘게 먹었으면 ALERT야.
                      이외의 텍스트는 덧붙이지 마. \n"""
                      + body_format),
        HumanMessage(meal_txt)
    ]

    ai_response = llm.invoke(messages)
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



# --------------------
# 메인 함수
# --------------------
def meal_analysis(meal: dict):
    meal_text = analyze_image_to_text(meal["photoUrl"])

    json_str = analyze_meal(meal_text)
    result = load_json_safely(json_str)
    result = recompute_totals(result)

    result["mealId"] = meal["mealId"]

    return result


if __name__ == "__main__":

    test_meal = {
        "mealId": 12345,
        "photoUrl": "보쌈.jpg",
        "callbackUrl": "https://example.com/callback",
        "whoAmIDto": {
            "userId": 1001,
            "userName": "김영희",
            "age": 72,
            "userHeight": 160,
            "userWeight": 58,
            "toics": [
                {
                    "topicId": 1,
                    "topicType": "ALLERGEN",
                    "name": "새우 알레르기",
                    "description": "갑각류 알레르기",
                    "source": "병원 진단서"
                },
                {
                    "topicId": 2,
                    "topicType": "DISEASE",
                    "name": "고혈압",
                    "description": "나트륨 섭취 주의",
                    "source": "건강검진"
                }
            ]
        }
    }
    
    result = meal_analysis(test_meal)

    print(result)