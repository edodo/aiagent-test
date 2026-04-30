import os
import asyncio
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from dotenv import load_dotenv

# 1. 인프라 설정 (파일 내부 내제화)
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
# 비동기 전용 프로토콜(asyncpg)로 변환
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

# 3. 비즈니스 로직 (함수 내부에 비동기 기술이 엉킨 사례)
async def fetch_users_async_coupled(name: str = None):
    # ⚠️ 나쁜 예: 비즈니스 로직 함수가 비동기 세션 생명주기와 SQLAlchemy 문법을 직접 관리함
    print(f"\n[Logic] 나쁜 사례(Async) 로그: 직접 비동기 세션을 생성하여 {name if name else '전체'} 조회를 처리합니다.")
    
    async with AsyncSessionLocal() as db:
        try:
            query = select(User).order_by(User.id.desc())
            if name:
                query = query.filter(User.name == name)
            
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            print(f"!! 에러 발생: {e}")
            return []
        # async with 블록 종료 시 세션이 자동 반환되나, 로직과 기술의 결합도는 여전히 높음

async def main():
    print("###### 04_04: 비동기 기술 결합형(Anti-Pattern) 실습 Start ######")
    
    # 전체 조회
    users = await fetch_users_async_coupled()
    print(f">> 비동기 전체 조회 결과 건수: {len(users)}")
    
    # 필터 조회 (홍길동)
    hong = await fetch_users_async_coupled("홍길동")
    if hong:
        print(f">> 비동기 검색 성공: {hong[0].name} ({hong[0].email})")

    print("###### 04_04 실습 End ######")

if __name__ == "__main__":
    asyncio.run(main())