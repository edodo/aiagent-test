import os
import asyncio
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from dotenv import load_dotenv

# 1. 인프라 설정
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
ASYNC_DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 2. 도메인 모델 정의
class User(Base):
    __tablename__ = "temp_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

# 3. 비동기 기술 어댑터 (전문 기술 영역을 별도 함수로 격리)
async def execute_async_fetch_adapter(model_class, filter_dict: dict = None):
    # ✅ 좋은 예: 비동기 세션 관리, execute, scalars 등의 '기술 상세'를 이 어댑터에 유배시킴
    print(f"[Adapter] 좋은 사례(Async) 로그: 전문 비동기 어댑터가 기술 상세를 격리 처리합니다.")
    
    async with AsyncSessionLocal() as db:
        query = select(model_class).order_by(model_class.id.desc())
        if filter_dict:
            for key, value in filter_dict.items():
                query = query.filter(getattr(model_class, key) == value)
        
        result = await db.execute(query)
        return result.scalars().all()

# 4. 비즈니스 로직 (도메인 영역)
async def list_users_async(name: str = None):
    # ✅ 좋은 예: 로직 함수는 await만 할 뿐, DB 드라이버나 SQLAlchemy 문법을 전혀 모름
    print(f"\n[Logic] 좋은 사례(Async) 로그: 비즈니스 로직은 비동기 어댑터에 조회를 요청합니다.")
    filter_params = {"name": name} if name else None
    
    # 도메인 로직은 어댑터와의 계약(인터페이스)에만 의존
    return await execute_async_fetch_adapter(User, filter_params)

async def main():
    print("###### 04_05: 비동기 기술 격리형(Adapter Practice) 실습 Start ######")
    
    # 전체 조회 호출
    users = await list_users_async()
    print(f">> 비동기 격리형 조회 결과 건수: {len(users)}")
    
    # 필터 조회 호출 (임꺽정)
    lim = await list_users_async("홍길동")
    if lim:
        print(f">> 비동기 격리형 검색 성공: {lim[0].name} ({lim[0].email})")

    print("###### 04_05 실습 End ######")

if __name__ == "__main__":
    asyncio.run(main())