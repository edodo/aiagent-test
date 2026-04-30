import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI Parameter Practice")

# [실습 가이드]
# 1. Query Parameter: URL 뒤에 ?key=value 형태로 전달 (간단한 검색/필터용)
# 2. Path Parameter: URL 경로의 일부로 전달 (특정 리소스 식별용)
# 3. Request Body: JSON 객체 형태로 전달 (LLM 프롬프트 등 복잡한 데이터용)

# Request Body를 위한 데이터 구조 정의 (Pydantic 모델)
class UserPrompt(BaseModel):
    prompt: str
    persona: str = "전문 AI 조력자"

@app.get("/hello/{name}")
async def say_hello_path(name: str, age: int = 20):
    """
    Path & Query Parameter 실습
    - 호출 예시: http://localhost:8000/hello/chulsoo?age=25
    """
    return {
        "message": f"Hello {name}!",
        "age_info": f"You are {age} years old.",
        "type": "Path & Query Parameter Test"
    }

@app.post("/ask")
async def ask_ai(request: UserPrompt):
    """
    Request Body 실습 (POST 방식)
    - LLM 서비스화의 핵심인 JSON 데이터 수신 구조입니다.
    """
    return {
        "received_prompt": request.prompt,
        "applied_persona": request.persona,
        "status": "success",
        "type": "Request Body (JSON) Test"
    }

if __name__ == "__main__":
    import uvicorn
    current_filename = os.path.basename(__file__)
    print(f"###### {current_filename} API 파라미터 연습 Start #######")
    uvicorn.run(app, host="127.0.0.1", port=8000)