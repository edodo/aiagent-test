import psycopg2
import os
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    print("###### [STEP 0] Direct DB Logic Start ######")
    
    # DATABASE_URL 존재 여부 체크
    if not DATABASE_URL:
        print("!! 에러: .env 파일에 DATABASE_URL이 설정되어 있지 않습니다.")
        return

    try:
        # Context Manager(with)를 사용하여 안전하게 리소스 관리
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # [수정] copy 버전처럼 temp_users를 조회
                cur.execute("SELECT * FROM temp_users LIMIT 10")
                
                # 컬럼명 추출
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                
                if not rows:
                    print("조회된 데이터가 없습니다.")
                    return

                # 결과 출력
                for row in rows:
                    # 1. 인덱스 기반 접근 (불편함과 위험성을 보여주는 코드)
                    print(f"인덱스 접근: ID={row[0]}, Name={row[1]}") # 컬럼 순서 바뀌면 바로 깨짐

                    # 2. 딕셔너리 변환(모든 컬럼을 유연하게 대응하도록 딕셔너리 형태로 변환) 
                    user_data = dict(zip(colnames, row))
                    print(f"조회 데이터: {user_data}")
                    
    except Exception as e:
        print(f"!! DB 연결 또는 쿼리 에러: {e}")
    finally:
        print("###### [STEP 0] Direct DB Logic End ######")

# [보완] 파이썬 스크립트가 직접 실행될 때 main() 함수를 호출하도록 함
if __name__ == "__main__":
    main()