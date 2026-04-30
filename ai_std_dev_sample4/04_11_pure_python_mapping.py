# 04_11_pure_python_mapping.py
# 실행방법:  python -m streamlit run .\04_11_pure_python_mapping.py 
# 판다스 없이 딕셔너리 리스트만으로 표의 타이틀과 데이터를 매핑하는 실습

import streamlit as st

st.title("📊 04_11: Pure Python Data Mapping")

# 1. 자산 규격 정의 (Key가 곧 표의 타이틀이 됨)
# 별도의 타이틀 정의 코딩 없이도 'ID', 'Name'이 헤더로 작동함
raw_assets = [
    {"ID": 1, "Name": "VibeCoder", "Role": "Architect"},
    {"ID": 2, "Name": "StandardAI", "Role": "Developer"}
]

st.subheader("1. 딕셔너리 리스트 매핑 (List[Dict])")
st.table(raw_assets) # 리스트의 Key를 헤더로 자동 인식

# 2. 열 중심 매핑 (Dict[List])
column_assets = {
    "부서": ["AI연구소", "플랫폼팀"],
    "인원": [12, 8]
}

st.subheader("2. 열 중심 매핑 (Dict[List])")
st.dataframe(column_assets) # 딕셔너리의 Key를 열 제목으로 자동 인식