import os
from dotenv import load_dotenv
from google import genai

# [함수 정의] 추론 로직을 별도의 단위(Unit)로 분리
def call_gemini_inference():
    """
    Gemini 모델 호출을 담당하는 함수 (내부 데이터 하드코딩)
    """
    # [데이터 준비] 입문자 실습을 위해 함수 내부에 직접 정의
    context = [
        "정기적인 운동과 균형 잡힌 식단은 건강을 유지하는 데 필수적이다.",
        "매일 조금씩이라도 몸을 움직이는 습관을 들이자."
    ]
    query = "건강을 유지하려면 어떻게 해야하나요?"
    
    # Payload 구성 (기존 로직 유지) 
    prompt = f"정보: {context}\n질문: {query}\n답변:"

    # [인증 및 클라이언트 생성] 
    v_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=v_api_key)

    try:
        # [모델 호출] SDK 핵심 메서드 실행 
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        # 처리 결과 반환 
        return query, response.text 
        
    except Exception as e:
        # 런타임 에러 트래핑 
        return query, f"!! [최종 에러]: {e}"

# [Main 실행절] 프로그램의 진입점 스크립트 직접 실행 시에만 동작하는 진입점(main)을 정의하여 
# 환경 변수를 로드하고, 독립적으로 격리된 함수를 호출하여 로직의 정상 동작을 즉각 검증
if __name__ == "__main__": 
    # 시스템 경로 처리 및 환경 변수 로드 
    current_filename = os.path.basename(__file__)
    print(f"###### {current_filename} Standard Start (Functional) #######")
    
    load_dotenv()

    # 함수 호출 및 결과 출력
    q, ai_response = call_gemini_inference()
    
    print("질문: ", q)
    print("답변: ", ai_response)