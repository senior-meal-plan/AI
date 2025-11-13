# --------------------
# 이미지를 받아서 그 안에 있는 음식을 텍스트로 바꿔주는 모듈
# 김 10g, 밥 20g같은 식으로 말해준다
# path_to_data_url : 이미지 파일을 base64 data URL로 변환
# analyze_image_to_text : 이미지를 재료 문자열로 변환
# --------------------


import os
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

SYSTEM_PROMPT = """
        너는 음식 사진을 분석하는 조리 보조 도우미야.
        사진을 보고, 눈으로 구분 가능한 각 재료와 그 재료의 대략적인 무게(g)를 추정해.
        형식은 단순한 문자열로, 예시는 다음과 같아:

        예시 1: "돼지갈비 200g, 밥 150g, 김치 50g"
        예시 2: "라면 300g, 계란 50g, 파 5g"
        예시 3: "샐러드 120g, 닭가슴살 100g, 드레싱 20g"

        JSON, 표, 코드블록을 쓰지 말고, 오직 위와 같은 한 줄짜리 문자열만 출력해.
    """


def path_to_data_url(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mime = "image/jpeg"
    if ext == ".png":
        mime = "image/png"
    elif ext == ".webp":
        mime = "image/webp"
    elif ext == ".gif":
        mime = "image/gif"

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def analyze_image_to_text(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    data_url = path_to_data_url(image_path)

    messages = [
        SystemMessage(SYSTEM_PROMPT),
        HumanMessage(content=[
            {"type": "text", "text": "이 음식 사진을 분석해줘."},
            {"type": "image_url", "image_url": {"url": data_url}},
        ])
    ]

    response = llm.invoke(messages)
    return response.content.strip()


if __name__ == "__main__":
    image_path = input("이미지 경로를 입력하세요: ").strip()
    result = analyze_image_to_text(image_path)
    print("\n분석 결과:")
    print(result)
