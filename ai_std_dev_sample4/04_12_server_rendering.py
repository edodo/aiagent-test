# 04_12_server_rendering.py  
# 실행 방법: python -m streamlit run .\04_12_server_rendering.py

import streamlit as st
import pandas as pd
import importlib.util
import sys
import os

def import_numeric_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(current_dir, "04_03_mainOrmAdapterPractice.py")
adapter_mod = import_numeric_module("adapter_practice", target_path)

def run_server_side_app():
    st.title("🖥️ 04_12: Server-Side Rendering")
    st.markdown("비즈니스 로직이 DB 데이터를 조회하여 UI 규격으로 변환하는 과정을 확인합니다.")

    search_name = st.sidebar.text_input("검색할 이름 (홍길동 등)")
    
    # [Step 1] 기존 04_03의 기술 어댑터 직접 호출
    filter_params = {"name": search_name} if search_name else None
    users = adapter_mod.execute_fetch_adapter(adapter_mod.User, filter_params)

    if users:
        # [Step 2] 데이터 가공 (ORM 객체 -> UI용 List/Dict)
        display_data = []
        for u in users:
            display_data.append({
                "번호": u.id,
                "이름": u.name,
                "이메일": u.email,
                "생성일": u.created_at.strftime("%Y-%m-%d %H:%M")
            })
        
        st.subheader(f"📊 조회 결과 (총 {len(users)}건)")
        st.dataframe(pd.DataFrame(display_data), use_container_width=True)
    else:
        st.info("데이터가 없습니다. DB 연결 상태를 확인하세요.")

if __name__ == "__main__":
    run_server_side_app()