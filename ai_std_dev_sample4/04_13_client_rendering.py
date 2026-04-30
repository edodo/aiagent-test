# 04_13_client_rendering.py
# 실행 방법: python -m streamlit run .\04_13_client_rendering.py
# 프로그램 설명: 04_06에서 구축한 FastAPI 서버에 API 요청을 보내고, 응답 데이터를 화면에 렌더링하는 클라이언트 앱입니다.
# 이 프로그램 실행 전에 04_06에서 FastAPI 서버가 다른 터미널 실행 중이어야 합니다. 검색 기능도 포함되어 있습니다. 
# 사전 실행 명령:  python .\04_06_fastapi_async_adapter.py

import streamlit as st
import requests
import pandas as pd
from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    name: str
    email: str

st.set_page_config(page_title="04_13: Traceable Client", layout="wide")
st.title("🌐 04_13: Client-side Rendering")

st.sidebar.header("🔍 검색 조건")
search_name = st.sidebar.text_input("사용자 이름", key="search_input")

API_URL = "http://localhost:8052/users" # 04_06 서버 연동

button_label = f"🔍 '{search_name}' 검색" if search_name else "🔄 전체 목록 불러오기"

if st.button(button_label):
    try:
        params = {}
        if search_name:
            params["name"] = search_name
        
        # [Step 1] API 서버에 데이터 요청
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                # [Step 2] 수신 데이터를 별도 검증 없이 즉시 데이터프레임으로 변환
                df = pd.DataFrame(data)
                st.dataframe(df[["id", "name", "email"]], width=1000)
                st.success(f"✅ {len(data)}건의 데이터를 성공적으로 가져왔습니다.")
            else:
                st.warning(f"⚠️ '{search_name}'에 대한 검색 결과가 없습니다.")
        else:
            st.error(f"서버 오류: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ 연결 실패: {e}")

with st.expander("🛠️ 현재 통신 상태"):
    st.write(f"목적지: {API_URL}")
    st.write(f"파라미터: { {'name': search_name} }")