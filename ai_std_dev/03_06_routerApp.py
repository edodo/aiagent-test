import uvicorn
from fastapi import FastAPI, APIRouter

# 1. 03_04 역할: 기초 인사 API 라우터
hello_router = APIRouter(prefix="/basic")
@hello_router.get("/hello")
async def say_hello():
    return {"message": "Hello from Basic Router!"}

# 2. 03_05 역할: 파라미터 연습 API 라우터
from pydantic import BaseModel
class UserPrompt(BaseModel):
    prompt: str

param_router = APIRouter(prefix="/param")
@param_router.post("/ask")
async def ask_ai(request: UserPrompt):
    return {"status": "success", "received": request.prompt}

# 3. 통합 게이트웨이 (Main App)
app = FastAPI(title="Integrated AI Gateway")

# 각 팀/기능별로 만든 라우터를 메인 앱에 등록
app.include_router(hello_router, tags=["Basic-Function"])
app.include_router(param_router, tags=["Parameter-Practice"])

if __name__ == "__main__":
    print("###### 다중 도메인 라우터 통합 서버 가동 ######")
    uvicorn.run(app, host="127.0.0.1", port=8000)