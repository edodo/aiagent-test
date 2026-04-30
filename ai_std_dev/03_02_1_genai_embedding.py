import os
from dotenv import load_dotenv
from google import genai

# 현재 실행 중인 파일명 추출 및 시작 로그
current_filename = os.path.basename(__file__)
print(f"###### {current_filename} Embedding Test Start #######")

# .env 환경 변수 로드 
load_dotenv()

# 1. 클라이언트 초기화 (보안 표준 준수) 
v_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=v_api_key)

# 2. 임베딩 대상 데이터 정의
# 5장의 RAG 실습 전, 순환 참조 없는 순수 텍스트 리스트 준비
contents_list = [
    "정기적인 운동과 균형 잡힌 식단은 건강을 유지하는 데 필수적이다.",
    "매일 조금씩이라도 몸을 움직이는 습관을 들이자.",
    "강아지는 인간의 가장 오래된 친구 중 하나이다."
]

try:
    # 3. 임베딩 모델 호출 (GCP 쿼터의 gemini-embedding-1.0에 매핑) 
    # 일일 무료 할당량 확인 후 진행 
    result = client.models.embed_content(
        model="gemini-embedding-001", # 최신 표준 모델 (또는 gemini-embedding-001)  
        contents=contents_list
    )
    
    # 4. 결과 확인 및 벡터 구조 이해
    for i, embedding in enumerate(result.embeddings):
        # 전체 벡터를 다 찍으면 너무 길므로 앞부분 5개만 출력  
        print(f"\n[문장 {i+1}] {contents_list[i][:15]}...")
        print(f"ㄴ 벡터 차원 수: {len(embedding.values)}")
        print(f"ㄴ 샘플 값(First 5): {embedding.values[:5]}")

except Exception as e:
    print(f"!! [임베딩 에러]: {e}")