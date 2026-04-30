from fastapi import FastAPI
import uvicorn  

# 1. 앱 객체 생성 (서버 인스턴스)
app = FastAPI(title="Hello AI API")

# 2. 라우팅 설정 (GET 방식)
@app.get("/hello")
async def say_hello(): # 단순한 JSON 응답 통해 서버 기동 확인
    return {"message": "Hello, AI Standard API!"}

# 서버 기동을 위한 핵심 코드 추가
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)