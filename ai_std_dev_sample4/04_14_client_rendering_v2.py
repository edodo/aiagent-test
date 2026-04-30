# 04_14_client_rendering_v2.py
# 실행 방법: python -m streamlit run .\04_14_client_rendering_v2.py
# 프로그램 설명: 04_13의 기능을 확장하여, 수신된 API 데이터를 UserRead 스키마로 검증(Validation)하는 클라이언트 앱입니다.
# 데이터 규격 자산화를 통해 서버-클라이언트 간의 데이터 무결성을 확보하는 전사 표준 모델을 실습합니다.
# 사전 실행 명령: python .\04_06_fastapi_async_adapter.py (8052 포트 서버 기동 필수)
 
import streamlit as st
import requests
import pandas as pd
from pydantic import BaseModel, ValidationError # [추가된 주석] 04_13의 핵심: 무결성 검증 도구

class UserRead(BaseModel):
    id: int
    name: str
    email: str

st.set_page_config(page_title="04_14: Validated Client", layout="wide")
st.title("🌐 04_14: Client-side Rendering (Validated)")

st.sidebar.header("🔍 검색 조건")
search_name = st.sidebar.text_input("사용자 이름", key="search_input")

API_URL = "http://localhost:8052/users"

button_label = f"🔍 '{search_name}' 검색" if search_name else "🔄 전체 목록 불러오기"

if st.button(button_label):
    try:
        params = {"name": search_name} if search_name else {}
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                # [Step 1] 04_14 핵심: UserRead 스키마를 통한 데이터 무결성 검증 루프 시작
                try:
                    # [Step 2] 각 항목을 UserRead 객체로 변환하여 규격 일치 여부 확인
                    validated_data = [UserRead(**item).model_dump() for item in data]
                    
                    df = pd.DataFrame(validated_data)
                    st.dataframe(df[["id", "name", "email"]], width=1000)
                    st.success(f"✅ {len(data)}건의 규격 검증된 데이터를 가져왔습니다.")
                
                except ValidationError as e:
                    # [Step 3] 규격에 어긋나는 데이터 수신 시 장애 방어
                    st.error("❌ 데이터 규격 불일치: 전사 표준 자산 규격에 어긋나는 데이터가 수신되었습니다.")
                    st.json(e.errors())
            else:
                st.warning(f"⚠️ '{search_name}'에 대한 검색 결과가 없습니다.")
        else:
            st.error(f"서버 오류: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ 연결 실패: {e}")

with st.expander("🛠️ 현재 통신 상태"):
    st.write(f"목적지: {API_URL}")
    st.write(f"파라미터: { {'name': search_name} }")