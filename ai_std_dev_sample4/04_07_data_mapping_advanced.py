import importlib.util, sys, os, uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

# 1. 숫자로 시작하는 04_06 모듈 동적 로드
def load_numeric_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))
server06 = load_numeric_module("server06", os.path.join(current_dir, "04_06_fastapi_async_adapter.py"))

# ---------------------------------------------------------
# 2. Schema 자산화 (입력과 출력 규격 정의)
# ---------------------------------------------------------

# [핵심] 조회 파라미터 자산화: 필터 조건을 객체로 관리
class UserSearchSch(BaseModel):
    name: Optional[str] = Field(None, description="검색할 사용자 이름")
    # 향후 email, role 등 필터 추가 시 이 객체만 수정하면 됨

# [핵심] 응답 데이터 자산화: 물리-논리 분리
class UserReadMdl(BaseModel):
    user_id: int = Field(validation_alias="id") # DB 'id' -> API 'user_id'
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True) # ORM 자동 매핑

# ---------------------------------------------------------
# 3. FastAPI 앱 설정
# ---------------------------------------------------------
app = FastAPI(title="04_07: Parameter & Data Mapping Server")

@app.get("/users/advanced", response_model=List[UserReadMdl])
async def get_users_mapped(filters: UserSearchSch = Depends()):
    """
    [Depends]를 통해 쿼리 파라미터를 UserSearch 객체로 자동 매핑합니다.
    """
    print(f"\n >>> [API Request] Received filters: {filters.model_dump()}")
    
    # 파이단틱 객체를 딕셔너리로 변환하여 어댑터에 전달
    filter_dict = filters.model_dump(exclude_none=True)
    
    # 04_06에서 로드한 adapter05 자산 재활용
    users = await server06.adapter05.execute_async_fetch_adapter(
        server06.adapter05.User, 
        filter_dict if filter_dict else None
    )
    
    return users

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8053)