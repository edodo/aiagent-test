import importlib.util, sys, os, uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# 숫자로 시작하는 모듈 동적 로드
def load_numeric_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))
adapter05 = load_numeric_module("adapter05", os.path.join(current_dir, "04_05_mainAsyncOrmAdapterPractice.py"))

app = FastAPI(title="04_06: Async Adapter API")

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True) # Pydantic V2

@app.get("/users", response_model=List[UserRead])
async def get_users(name: Optional[str] = None):
    print(f" >>> [API Request] Received name: '{name}'")
    filter_params = {"name": name.strip()} if name and name.strip() else None
    return await adapter05.execute_async_fetch_adapter(adapter05.User, filter_params)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8052)