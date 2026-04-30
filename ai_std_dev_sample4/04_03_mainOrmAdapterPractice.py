import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. 인프라 설정
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 도메인 모델 정의
class User(Base):
    __tablename__ = "temp_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

# 3. 기술 어댑터 (전문 기술 영역을 함수로 격리)
def execute_fetch_adapter(model_class, filter_dict: dict = None):
    # 좋은 예: 모든 DB 상세 기술(Session, Query)을 이 어댑터 함수 내부에 격리
    print(f"[Adapter] 좋은 사례 로그: 전문 어댑터가 기술 상세를 격리 처리합니다.")
    db = SessionLocal()
    try:
        query = db.query(model_class)
        if filter_dict:
            # 제네릭한 필터 처리 기술
            for key, value in filter_dict.items():
                query = query.filter(getattr(model_class, key) == value)
        return query.all()
    finally:
        db.close()

# 4. 비즈니스 로직 (도메인 영역)
def list_users(name: str = None):
    # 좋은 예: 로직 함수는 인프라를 몰라도 됨. 어댑터에 조회를 요청함
    print(f"\n[Logic] 좋은 사례 로그: 비즈니스 로직은 어댑터에 조회를 요청합니다.")
    filter_params = {"name": name} if name else None
    return execute_fetch_adapter(User, filter_params)

def main():
    print("###### 04_03: 기술 격리형(Adapter Practice) 실습 Start ######")
    
    # 전체 조회 호출
    users = list_users()
    print(f">> 전체 조회 결과 건수: {len(users)}")
    
    # 필터 조회 호출 (임꺽정)
    lim = list_users("홍길동")
    if lim:
        print(f">> 검색 성공: {lim[0].name} ({lim[0].email})")

    print("###### 04_03 실습 End ######")

if __name__ == "__main__":
    main()