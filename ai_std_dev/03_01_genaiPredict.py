
import os
from dotenv import load_dotenv
from google import genai

# 현재 실행 중인 파일의 이름만 추출
current_filename = os.path.basename(__file__)
print(f"###### {current_filename} Standard Start #######")

load_dotenv()

# 1. 클라이언트 초기화 (새로운 라이브러리 방식)
v_api_key = os.getenv("GEMINI_API_KEY")
# print(f"현재 로드된 키 값: {v_api_key}") # 여기서 None이 나오는지 확인
client = genai.Client(api_key=v_api_key)

context = [
    "정기적인 운동과 균형 잡힌 식단은 건강을 유지하는 데 필수적이다.",
    "매일 조금씩이라도 몸을 움직이는 습관을 들이자."
]

query = "건강을 유지하려면 어떻게 해야하나요?"
prompt = f"정보: {context}\n질문: {query}\n답변:"

try:
    # 2. 모델 호출 (버전 명시 없이도 최신 v1 경로로 자동 매핑됩니다)
    # gemini-2.5-flash 20건 gemini-2.5-flash-lite 20 건
    response = client.models.generate_content(
        model="gemini-2.5-flash",    #  gemini-2.5-flash  /  gemini-2.5-flash-lite
 
        contents=prompt
    )
    
    print("질문: ", query)
    print("답변: ", response.text)
except Exception as e:
    print(f"!! [최종 에러]: {e}")