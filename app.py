import streamlit as st
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="내신 등급 상호 변환기", page_icon="🔄")

# --- 모바일 반응형 CSS 주입 ---
st.markdown("""
    <style>
    .responsive-title {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    @media (max-width: 768px) {
        .responsive-title {
            font-size: 1.6rem;
        }
    }
    </style>
    <div class="responsive-title">🔄 내신 등급 상호 환산기 (5등급 ↔ 9등급)</div>
""", unsafe_allow_html=True)

st.write("2028학년도 대입제도 개편 대비 내신 등급 변환 가이드의 표본 데이터를 바탕으로 등급을 상호 환산합니다[cite: 4].")

# 1. 문서 기반 기준점 데이터 설정 (1.00 ~ 5.00까지 0.05 단위, 총 81개 구간) 
grade_5_points = np.round(np.linspace(1.00, 5.00, 81), 2)

# 대진대학교 문서 내 '9등급(평균)' 데이터 
grade_9_avg_points = [
    1.18, 1.36, 1.51, 1.63, 1.73, 1.85, 1.95, 2.05, 2.14, 2.25,
    2.34, 2.42, 2.48, 2.61, 2.69, 2.79, 2.82, 2.97, 3.06, 3.15,
    3.21, 3.33, 3.40, 3.53, 3.60, 3.68, 3.77, 3.86, 3.97, 4.03,
    4.11, 4.20, 4.27, 4.38, 4.45, 4.54, 4.62, 4.71, 4.78, 4.86,
    4.94, 5.04, 5.14, 5.21, 5.30, 5.37, 5.46, 5.52, 5.63, 5.70,
    5.80, 5.84, 5.96, 6.05, 6.11, 6.20, 6.27, 6.37, 6.48, 6.56,
    6.65, 6.74, 6.84, 6.91, 7.01, 7.10, 7.20, 7.31, 7.38, 7.42,
    7.51, 7.60, 7.75, 7.90, 7.96, 8.07, 8.14, 8.25, 8.49, 8.64,
    8.74
]

# 2. 상호 변환을 위한 탭 구성
tab1, tab2 = st.tabs(["📊 5등급 ➔ 9등급 변환", "🔍 9등급 ➔ 5등급 역산"])

# --- 탭 1: 5등급에서 9등급으로 변환 ---
with tab1:
    st.subheader("5등급제 ➔ 9등급제")
    input_grade_5 = st.number_input(
        "5등급제 내신 평균을 입력하세요 (1.00 ~ 5.00):", 
        min_value=1.00, max_value=5.00, value=2.50, step=0.01, key="g5_input"
    )
    
    if st.button("9등급 평균으로 변환", key="btn_to_9"):
        converted_9_grade = np.interp(input_grade_5, grade_5_points, grade_9_avg_points)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 5등급 평균", f"{input_grade_5:.2f} 등급")
        col2.metric("최종 9등급 환산 평균", f"{converted_9_grade:.2f} 등급")

# --- 탭 2: 9등급에서 5등급으로 역산 ---
with tab2:
    st.subheader("9등급제 ➔ 5등급제")
    # 표본 데이터 기준 최소/최대 등급 제한 
    input_grade_9 = st.number_input(
        "9등급제 내신 평균을 입력하세요 (1.18 ~ 8.74):", 
        min_value=1.18, max_value=8.74, value=4.11, step=0.01, key="g9_input"
    )
    
    if st.button("5등급 평균으로 역산", key="btn_to_5"):
        # 역방향 선형 보간: x와 y의 위치를 서로 바꾸어 계산합니다.
        converted_5_grade = np.interp(input_grade_9, grade_9_avg_points, grade_5_points)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 9등급 평균", f"{input_grade_9:.2f} 등급")
        col2.metric("최종 5등급 환산 평균", f"{converted_5_grade:.2f} 등급")

# 하단 출처 표시
st.caption("※ 본 환산 결과는 대진대학교 입학팀의 전국 23개 고교 고3 표본(6,087명) 데이터를 바탕으로 산출되었습니다[cite: 176, 178].")
