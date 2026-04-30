# ai_std_dev_sample4/04_10_streamlit_basic.py
# 실행 방법: python -m streamlit run .\04_10_streamlit_basic.py

import streamlit as st

def main():
    st.set_page_config(page_title="4장: 스트림릿 기초", layout="centered")
    
    st.title("🎨 스트림릿 웹 UI 기초")
    st.write("파이썬 코드만으로 웹 화면을 구성하는 기본 원리를 익힙니다.")

    st.divider()

    # 1. 입력 위젯
    name = st.text_input("사용자 이름을 입력하세요", placeholder="홍길동")
    role = st.selectbox("역할 선택", ["Developer", "Architect", "Manager"])
    
    # 2. 버튼 및 상태 처리
    if st.button("인사하기"):
        st.success(f"안녕하세요 {name}님! 당신의 역할은 {role}입니다.")
        st.balloons() # 축하 효과

    # 3. 데이터 시각화 맛보기
    st.subheader("📊 샘플 데이터 출력")
    sample_data = [
        {"ID": 1, "Name": "VibeCoder", "Status": "Active"},
        {"ID": 2, "Name": "StandardAI", "Status": "Pending"}
    ]
    st.table(sample_data)

if __name__ == "__main__":
    # 실행 방법: streamlit run ai_std_dev_sample4/04_06_streamlit_basic.py
    main()