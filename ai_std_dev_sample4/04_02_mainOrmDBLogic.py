import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. 인프라 설정 (프로그램 내부 포함)
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

# 3. 비즈니스 로직 (함수 내부에 기술이 엉킨 사례)
def fetch_users_with_infra_coupling(name: str = None):
    # 나쁜 예: 함수 내에서 직접 세션을 생성하고 SQLAlchemy 문법을 사용함
    print(f"\n[Logic] 나쁜 사례 로그: 직접 세션을 생성하여 {name if name else '전체'} 조회를 처리합니다.")
    
    db = SessionLocal() 
    try:
        query = db.query(User)

        if name:
            query = query.filter(User.name == name)
        return query.all()
    finally:
        print("[Logic] 나쁜 사례 로그: 직접 세션을 닫습니다.")
        db.close()

def main():
    print("###### 04_02: 기술 결합형(Anti-Pattern) 실습 Start ######")
    
    # 전체 데이터 조회
    users = fetch_users_with_infra_coupling()
    print(f">> 전체 조회 결과 건수: {len(users)}")
 
    for user in users:
        # 💡 핵심: 튜플 인덱스가 아닌 '속성'으로 접근
        print(f"조회 데이터: {user.id}, {user.name}, {user.email}")    
    
    # 필터 조회 (홍길동)
    hong = fetch_users_with_infra_coupling("홍길동")
    if hong:
        print(f">> 검색 성공: {hong[0].name} ({hong[0].email})")

    print("###### 04_02 실습 End ######")

if __name__ == "__main__":
    main()