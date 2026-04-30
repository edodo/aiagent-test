import os
from dotenv import load_dotenv
from google import genai

# ============================================================
# [Adapter Layer] 기술 상세 격리 영역
# ============================================================

def call_gemini_adapter(p_prompt: str, p_model: str = "gemini-2.5-flash-lite"):
    """
    구글 SDK라는 특정 기술(Infrastructure)을 이 함수 내부로 가둡니다. 
    메인 로직은 이 함수가 '어떻게' 동작하는지 몰라도 결과만 받으면 됩니다.
    """
    v_api_key = os.getenv("GEMINI_API_KEY")
    if not v_api_key:
        return "!! [에러]: API Key를 확인하세요."

    # SDK 클라이언트 객체 생성을 함수 내부로 격리 [cite: 118]
    client = genai.Client(api_key=v_api_key)
    
    try:
        response = client.models.generate_content(
            model=p_model,
            contents=p_prompt
        )
        return response.text
    except Exception as e:
        return f"!! [통신 에러]: {str(e)}"

# ============================================================
# [Business Logic Layer] 메인 실행 영역 (자산화 대상)
# ============================================================

if __name__ == "__main__":
    # 1. 환경 설정 로드
    load_dotenv()
    
    # 파일 실행 로그 출력 (03_01과 동일한 형식)
    current_filename = os.path.basename(__file__)
    print(f"###### {current_filename} Adapter 분리 연습 Start #######")

    # 2. 비즈니스 데이터 준비
    context = [
        "정기적인 운동과 균형 잡힌 식단은 건강을 유지하는 데 필수적이다.",
        "매일 조금씩이라도 몸을 움직이는 습관을 들이자."
    ]
    query = "건강을 유지하려면 어떻게 해야하나요?"
    user_prompt = f"정보: {context}\n질문: {query}\n답변:"

    # 3. 어댑터 호출 (메인 로직에서 SDK 의존성 제거) [cite: 123]
    ai_response = call_gemini_adapter(user_prompt)

    # 4. 결과 출력 (운영자님 요청 형식 준수)
    print("질문: ", query)
    print("답변: ", ai_response)